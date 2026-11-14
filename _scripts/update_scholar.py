"""Refresh _data/scholar.yml from Google Scholar.

Run by the GitHub Actions workflow before the Jekyll build. It reads the public
profile page directly (one request). If Google blocks that, and the repository
has a SERPAPI_KEY secret, it asks SerpAPI (serpapi.com) for the same numbers.
If both fail or the data looks wrong, the file is left as is so the site keeps
its last good numbers. Uses only the Python standard library.
"""
import datetime
import html
import json
import os
import pathlib
import re
import sys
import urllib.parse
import urllib.request

SCHOLAR_ID = "OCnQzOQAAAAJ"
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "_data" / "scholar.yml"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def from_profile_page():
    page = get(f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en")
    cells = [int(n) for n in re.findall(r'class="gsc_rsb_std">(\d+)<', page)]
    if len(cells) < 6:
        raise RuntimeError("metrics table not found (probably a captcha page)")
    since = re.search(r">Since (\d{4})<", page)

    # Year labels run oldest to newest. Bars carry z-index 1 for the newest
    # year, 2 for the year before, and so on; years without citations have no bar.
    years = [int(y) for y in re.findall(r'class="gsc_g_t"[^>]*>(\d{4})<', page)]
    per_year = {y: 0 for y in years}
    for z, count in re.findall(r'class="gsc_g_a"[^>]*z-index:(\d+)"[^>]*><span class="gsc_g_al">(\d+)<', page):
        i = len(years) - int(z)
        if 0 <= i < len(years):
            per_year[years[i]] = int(count)

    return {
        "citations": cells[0], "citations_since": cells[1],
        "h_index": cells[2], "h_index_since": cells[3],
        "i10_index": cells[4], "i10_index_since": cells[5],
        "since_year": int(since.group(1)) if since else None,
        "per_year": per_year,
    }


def from_serpapi(key):
    query = urllib.parse.urlencode(
        {"engine": "google_scholar_author", "author_id": SCHOLAR_ID, "hl": "en", "api_key": key}
    )
    data = json.loads(get(f"https://serpapi.com/search.json?{query}"))
    if "error" in data:
        raise RuntimeError(data["error"])

    table = {}
    since_year = None
    for row in data["cited_by"]["table"]:
        for metric, values in row.items():
            table[metric] = values
            for k in values:
                if k.startswith("since_"):
                    since_year = int(k.split("_")[1])

    def pick(metric, which):
        values = table[metric]
        if which == "all":
            return int(values["all"])
        return int(next(v for k, v in values.items() if k.startswith("since_")))

    return {
        "citations": pick("citations", "all"), "citations_since": pick("citations", "since"),
        "h_index": pick("h_index", "all"), "h_index_since": pick("h_index", "since"),
        "i10_index": pick("i10_index", "all"), "i10_index_since": pick("i10_index", "since"),
        "since_year": since_year,
        "per_year": {int(g["year"]): int(g["citations"]) for g in data["cited_by"].get("graph", [])},
    }


def current_citations():
    match = re.search(r"^citations:\s*(\d+)", DATA_FILE.read_text(encoding="utf-8"), re.M)
    return int(match.group(1)) if match else 0


def render(m):
    today = datetime.date.today()
    lines = [
        "# Google Scholar metrics - updated automatically every day by",
        "# .github/workflows/jekyll.yml (_scripts/update_scholar.py).",
        "# You can still edit these numbers by hand; the next successful update overwrites them.",
        f"profile: https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en",
        f"updated: {today.strftime('%B %Y')}",
        f"citations: {m['citations']}",
        f"h_index: {m['h_index']}",
        f"i10_index: {m['i10_index']}",
        '# "Since" column on Scholar',
        f"since_year: {m['since_year'] or today.year - 5}",
        f"citations_since: {m['citations_since']}",
        f"h_index_since: {m['h_index_since']}",
        f"i10_index_since: {m['i10_index_since']}",
        "# Citations per year (the bar chart on your Scholar profile)",
        "per_year:",
    ]
    lines += [f"  - {{year: {y}, count: {c}}}" for y, c in sorted(m["per_year"].items())]
    return "\n".join(lines) + "\n"


def fetch():
    try:
        m = from_profile_page()
        print("Read the Google Scholar profile page.")
        return m
    except Exception as e:
        print(f"Google Scholar profile page not readable ({html.unescape(str(e))}).")

    key = os.environ.get("SERPAPI_KEY", "").strip()
    if not key:
        print("No SERPAPI_KEY secret set, so there is no backup source.")
        return None
    try:
        m = from_serpapi(key)
        print("Read the numbers through SerpAPI.")
        return m
    except Exception as e:
        print(f"SerpAPI request failed ({e}).")
        return None


def main():
    m = fetch()
    if m is None:
        print("Keeping existing numbers.")
        return 0
    if m["citations"] <= 0 or not m["h_index"] or not m["per_year"]:
        print("Scholar returned incomplete data; keeping existing numbers.")
        return 0
    if m["citations"] < current_citations() * 0.5:
        print(f"Citations dropped to {m['citations']}, which looks wrong; keeping existing numbers.")
        return 0

    DATA_FILE.write_text(render(m), encoding="utf-8")
    print(f"Updated: {m['citations']} citations, h-index {m['h_index']}, i10-index {m['i10_index']}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
