# Refresh _data/visitors.yml from GoatCounter.
#
# Run by the GitHub Actions workflow before the Jekyll build. If anything goes
# wrong (no API key, GoatCounter unreachable, no visits yet), the file is left
# as is so the build still succeeds.
require "json"
require "net/http"
require "time"
require "uri"

SITE = ENV.fetch("GOATCOUNTER_URL", "https://kieutruong.goatcounter.com")
TOKEN = ENV["GOATCOUNTER_TOKEN"].to_s
COUNTING_SINCE = Time.utc(2026, 11, 1)
TOP_COUNTRIES = 8
PAGE_SIZE = 100 # The most the API returns per request
DATA_FILE = File.expand_path("../_data/visitors.yml", __dir__)


def get(path, params)
  uri = URI("#{SITE}/api/v0/#{path}")
  uri.query = URI.encode_www_form(params)
  request = Net::HTTP::Get.new(uri)
  request["Authorization"] = "Bearer #{TOKEN}"
  request["Content-Type"] = "application/json"
  response = Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == "https", open_timeout: 20, read_timeout: 30) do |http|
    http.request(request)
  end
  raise "HTTP #{response.code}" unless response.is_a?(Net::HTTPSuccess)

  JSON.parse(response.body)
end


def fetch_total
  get("stats/total", start: COUNTING_SINCE.iso8601)["total"].to_i
end


def fetch_countries
  countries = []
  loop do
    page = get("stats/locations", start: COUNTING_SINCE.iso8601, limit: PAGE_SIZE, offset: countries.size)
    stats = Array(page["stats"])
    countries.concat(stats)
    break unless page["more"] && stats.any?
  end
  # Visits GoatCounter couldn't place are listed under a name like "(unknown)"
  countries.reject { |c| c["name"].to_s.empty? || c["name"].start_with?("(") }
           .sort_by { |c| -c["count"].to_i }
end


def render(visits, countries)
  lines = [
    "# Visitor numbers from GoatCounter - refreshed automatically by",
    "# .github/workflows/jekyll.yml (_scripts/update_visitors.rb).",
    "# The home page hides the visitor box while visits is 0.",
    "updated: #{Time.now.utc.strftime('%-d %B %Y')}",
    "since: #{COUNTING_SINCE.strftime('%B %Y')}",
    "visits: #{visits}",
    "country_count: #{countries.size}",
    "# Countries with the most visits",
    "countries:",
  ]
  lines += countries.first(TOP_COUNTRIES).map { |c| "  - {name: #{c['name'].to_json}, count: #{c['count'].to_i}}" }
  lines.join("\n") + "\n"
end


def main
  if TOKEN.empty?
    puts "GOATCOUNTER_TOKEN is not set; keeping existing numbers."
    return
  end

  begin
    visits = fetch_total
    countries = fetch_countries
  rescue StandardError => e
    puts "Could not read GoatCounter (#{e.message}); keeping existing numbers."
    return
  end

  if visits <= 0 || countries.empty?
    puts "GoatCounter has no visits to show yet; keeping existing numbers."
    return
  end

  File.write(DATA_FILE, render(visits, countries))
  puts "Updated: #{visits} visits from #{countries.size} countries."
end

main
