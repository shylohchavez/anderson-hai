#!/usr/bin/env python3
"""
Anderson HAI — Technical SEO Surveillance Monitor
Tracks competitor site changes, new pages, and schema markup.

- Uses sitemap scraping to discover new pages.
- Uses general web scraping to extract schema.org markup.
- Compares schemas over time to detect changes.

Credit cost: 1-5 credits per general scrape, varies by site complexity.
"""

import requests
import json
import os
import time
import hashlib
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

SCRAPE_DO_TOKEN = os.environ.get("SCRAPE_DO_TOKEN", "SCRAPE_DO_TOKEN_REMOVED")
DATA_DIR = Path(os.path.expanduser("~/.openclaw/workspace/data/seo-intelligence"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

COMPETITORS = [
    {"name": "Cherokee Mechanical", "website": "cherokeemech.com"},
    {"name": "Calhoun Air Care", "website": "calhounaircare.com"},
    {"name": "CoolRay", "website": "coolray.com"},
    {"name": "Lee Company", "website": "leecompany.com"},
]


def api_request(url, params, retries=3):
    """Make Scrape.do API request."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=60)
            if resp.status_code == 200:
                return resp.text
            elif resp.status_code == 429:
                time.sleep(2 ** (attempt + 1))
            else:
                return None
        except requests.RequestException:
            time.sleep(2)
    return None


def find_sitemap(domain):
    """Attempt to find a competitor's sitemap."""
    robots_url = f"https://{domain}/robots.txt"
    print(f"  🔍 Checking {robots_url} for sitemap...")
    content = api_request("https://api.scrape.do", {"token": SCRAPE_DO_TOKEN, "url": robots_url})
    if content:
        for line in content.splitlines():
            if line.lower().startswith("sitemap:"):
                sitemap_url = line.split(":", 1)[1].strip()
                print(f"    ✅ Found sitemap: {sitemap_url}")
                return sitemap_url

    # Common fallbacks
    potential_sitemaps = [f"https://{domain}/sitemap.xml", f"https://{domain}/sitemap_index.xml"]
    for url in potential_sitemaps:
        print(f"  🔍 Trying fallback: {url}...")
        resp = requests.head(url, timeout=10)
        if resp.status_code == 200:
            print(f"    ✅ Found sitemap: {url}")
            return url

    return None


def scrape_sitemap(sitemap_url):
    """Scrape a sitemap and extract all URLs."""
    content = api_request("https://api.scrape.do", {"token": SCRAPE_DO_TOKEN, "url": sitemap_url})
    if not content:
        return []

    urls = set()
    try:
        root = ET.fromstring(content)
        for url_element in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            urls.add(url_element.text)
    except ET.ParseError:
        print(f"    ⚠️ Failed to parse sitemap XML for {sitemap_url}")
        # Fallback for plain text sitemaps
        for line in content.splitlines():
            if line.strip().startswith("http"):
                urls.add(line.strip())

    return sorted(list(urls))


def monitor_new_pages():
    """Monitor competitor sitemaps for new pages."""
    print("📜 Monitoring for New Competitor Pages...")
    prev_pages_file = DATA_DIR / "competitor-pages.json"
    prev_pages = {}
    if prev_pages_file.exists():
        with open(prev_pages_file) as f:
            prev_pages = json.load(f)

    current_pages = {"timestamp": datetime.now().isoformat()}
    new_pages_report = []

    for comp in COMPETITORS:
        if not comp.get("website"):
            continue

        domain = comp["website"]
        print(f"\n--- {comp['name']} ({domain}) ---")
        sitemap_url = find_sitemap(domain)
        if not sitemap_url:
            print("    ❌ No sitemap found.")
            current_pages[domain] = prev_pages.get(domain, {"urls": [], "count": 0})
            continue

        urls = scrape_sitemap(sitemap_url)
        current_pages[domain] = {"urls": urls, "count": len(urls)}

        # Compare to previous run
        prev_url_set = set(prev_pages.get(domain, {}).get("urls", []))
        new_urls = [u for u in urls if u not in prev_url_set]

        if new_urls:
            print(f"    🚨 Found {len(new_urls)} new pages for {comp['name']}:")
            for url in new_urls:
                print(f"      - {url}")
                new_pages_report.append({"competitor": comp['name'], "url": url})
        else:
            print("    ✅ No new pages detected.")
        time.sleep(1)

    # Save current state and new pages report
    with open(prev_pages_file, "w") as f:
        json.dump(current_pages, f, indent=2)

    if new_pages_report:
        report_file = DATA_DIR / "new-pages-report.json"
        with open(report_file, "w") as f:
            json.dump(new_pages_report, f, indent=2)

    return new_pages_report


def extract_schema_from_html(html):
    """Find and parse ld+json schema from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    schemas = []
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            schema_data = json.loads(script.string)
            schemas.append(schema_data)
        except json.JSONDecodeError:
            continue
    return schemas


def monitor_schema_changes():
    """Monitor competitor homepages for schema changes."""
    print("\n🔬 Monitoring Competitor Schema Markup...")
    prev_schemas_file = DATA_DIR / "competitor-schemas.json"
    prev_schemas = {}
    if prev_schemas_file.exists():
        with open(prev_schemas_file) as f:
            prev_schemas = json.load(f)

    current_schemas = {"timestamp": datetime.now().isoformat()}
    schema_changes_report = []

    for comp in COMPETITORS:
        domain = comp["website"]
        print(f"--- {comp['name']} ({domain}) ---")
        url = f"https://{domain}"

        # Scrape homepage HTML
        html = api_request("https://api.scrape.do", {"token": SCRAPE_DO_TOKEN, "url": url, "render": "true"})
        if not html:
            print("    ❌ Failed to scrape homepage.")
            continue

        # Extract schema
        schemas = extract_schema_from_html(html)
        if not schemas:
            print("    ⚠️ No ld+json schema found.")
            current_schemas[domain] = {"hash": None, "types": []}
            continue

        # Create a hash of the schema to detect changes
        schema_str = json.dumps(schemas, sort_keys=True)
        schema_hash = hashlib.md5(schema_str.encode()).hexdigest()
        schema_types = [s.get('@type', 'Unknown') for s in schemas]

        print(f"    ✅ Found schema types: {', '.join(map(str, schema_types))}")
        current_schemas[domain] = {"hash": schema_hash, "types": schema_types}

        # Compare to previous run
        prev = prev_schemas.get(domain, {})
        if prev and prev.get("hash") != schema_hash:
            print(f"    🚨 SCHEMA CHANGE DETECTED for {comp['name']}!")
            change_details = {
                "competitor": comp['name'],
                "url": url,
                "prev_types": prev.get("types", []),
                "new_types": schema_types,
            }
            schema_changes_report.append(change_details)

            # Save old and new schema for diffing
            with open(DATA_DIR / f"schema-{domain}-old.json", "w") as f:
                 json.dump(json.loads(prev.get("schema_str", "{}")), f, indent=2)
            with open(DATA_DIR / f"schema-{domain}-new.json", "w") as f:
                 json.dump(schemas, f, indent=2)

        # Store full string for future diffing
        current_schemas[domain]["schema_str"] = schema_str

    # Save current state and report
    with open(prev_schemas_file, "w") as f:
        json.dump(current_schemas, f, indent=2)

    if schema_changes_report:
        report_file = DATA_DIR / "schema-changes-report.json"
        with open(report_file, "w") as f:
            json.dump(schema_changes_report, f, indent=2)

    return schema_changes_report


def generate_tech_seo_report():
    report = [
        "# Anderson HAI — Technical SEO Surveillance Report",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        ""
    ]

    # New pages
    new_pages_file = DATA_DIR / "new-pages-report.json"
    if new_pages_file.exists():
        with open(new_pages_file) as f:
            pages = json.load(f)
        if pages:
            report.append("## 📜 New Competitor Pages Detected")
            for page in pages:
                report.append(f"- **{page['competitor']}** published: `{page['url']}`")
            report.append("")

    # Schema changes
    schema_changes_file = DATA_DIR / "schema-changes-report.json"
    if schema_changes_file.exists():
        with open(schema_changes_file) as f:
            changes = json.load(f)
        if changes:
            report.append("## 🔬 Schema Markup Changes Detected")
            for ch in changes:
                report.append(f"- **{ch['competitor']}** updated their schema:")
                report.append(f"  - Previous types: `{ch['prev_types']}`")
                report.append(f"  - New types: `{ch['new_types']}`")
            report.append("")

    report.append("## 🎯 Action Items")
    report.append("- [ ] Review new competitor pages for content/service updates.")
    report.append("- [ ] Analyze schema changes for new SEO tactics.")
    report.append("- [ ] Periodically check Anderson's own sitemap for errors.")
    report.append("- [ ] Validate Anderson's schema markup on key pages.")

    report_text = "\n".join(report)
    outfile = DATA_DIR / "technical-seo-report.md"
    with open(outfile, "w") as f:
        f.write(report_text)
    print(f"\n✅ Report saved to {outfile}")
    return report_text


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"

    if mode == "pages":
        monitor_new_pages()
    elif mode == "schema":
        monitor_schema_changes()
    elif mode == "report":
        generate_tech_seo_report()
    elif mode == "full":
        monitor_new_pages()
        monitor_schema_changes()
        generate_tech_seo_report()
    else:
        print(f"Usage: {sys.argv[0]} [pages|schema|report|full]")
