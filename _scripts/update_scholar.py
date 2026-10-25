"""Refresh _data/scholar.yml from Google Scholar.

Run by the GitHub Actions workflow before the Jekyll build. If anything goes
wrong (Google blocks the request, data looks wrong), the file is left as is so
the site keeps its last good numbers.
"""
import datetime
import pathlib
import re
import sys

SCHOLAR_ID = "OCnQzOQAAAAJ"
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "_data" / "scholar.yml"


def current_citations():
    match = re.search(r"^citations:\s*(\d+)", DATA_FILE.read_text(encoding="utf-8"), re.M)
    return int(match.group(1)) if match else 0


def fetch():
    from scholarly import scholarly

    author = scholarly.search_author_id(SCHOLAR_ID)
    return scholarly.fill(author, sections=["indices", "counts"])


def render(a):
    today = datetime.date.today()
    per_year = sorted((int(y), int(c)) for y, c in a["cites_per_year"].items())
    lines = [
        "# Google Scholar metrics - updated automatically every week by",
        "# .github/workflows/jekyll.yml (_scripts/update_scholar.py).",
        "# You can still edit these numbers by hand; the next successful update overwrites them.",
        f"profile: https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en",
        f"updated: {today.strftime('%B %Y')}",
        f"citations: {a['citedby']}",
        f"h_index: {a['hindex']}",
        f"i10_index: {a['i10index']}",
        '# "Since" column on Scholar',
        f"since_year: {today.year - 5}",
        f"citations_since: {a['citedby5y']}",
        f"h_index_since: {a['hindex5y']}",
        f"i10_index_since: {a['i10index5y']}",
        "# Citations per year (the bar chart on your Scholar profile)",
        "per_year:",
    ]
    lines += [f"  - {{year: {y}, count: {c}}}" for y, c in per_year]
    return "\n".join(lines) + "\n"


def main():
    try:
        author = fetch()
    except Exception as e:
        print(f"Could not reach Google Scholar ({e}); keeping existing numbers.")
        return 0

    citations = int(author.get("citedby") or 0)
    if citations <= 0 or not author.get("hindex") or not author.get("cites_per_year"):
        print("Scholar returned incomplete data; keeping existing numbers.")
        return 0
    if citations < current_citations() * 0.5:
        print(f"Citations dropped to {citations}, which looks wrong; keeping existing numbers.")
        return 0

    DATA_FILE.write_text(render(author), encoding="utf-8")
    print(f"Updated: {citations} citations, h-index {author['hindex']}, i10-index {author['i10index']}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
