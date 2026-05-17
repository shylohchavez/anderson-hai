#!/usr/bin/env python3
"""
Anderson HAI — Competitor Intelligence Monitor
Scrapes competitor websites, Google Maps listings, and reviews
to track changes, pricing, and market positioning.

Uses Scrape.do API for all scraping.
Credit cost: ~10 credits per Google Maps/Search call, 1-5 for general web scraping.
"""

import requests
import json
import os
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

# === CONFIGURATION ===
SCRAPE_DO_TOKEN = os.environ.get("SCRAPE_DO_TOKEN")
DATA_DIR = Path(os.path.expanduser("~/.openclaw/workspace/data/seo-intelligence"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Anderson HAI info
ANDERSON = {
    "name": "Anderson Heating, Air & Insulation",
    "phone": "(706) 629-0749",
    "website": "johnandersonservice.com",
    "search_query": "Anderson Heating Air Insulation Calhoun GA",
}

# Primary competitors by market
COMPETITORS = {
    "calhoun": [
        {"name": "Cherokee Mechanical", "website": "cherokeemech.com", "search": "Cherokee Mechanical Calhoun GA"},
        {"name": "Calhoun Air Care", "website": "calhounaircare.com", "search": "Calhoun Air Care Calhoun GA"},
    ],
    "dalton": [
        {"name": "Dalton Heating & Air", "website": None, "search": "Dalton Heating Air Dalton GA"},
        {"name": "Lee Company", "website": "leecompany.com", "search": "Lee Company HVAC Dalton GA"},
        {"name": "Adams Air", "website": None, "search": "Adams Air Dalton GA HVAC"},
    ],
    "rome": [
        {"name": "CoolRay Heating and Air", "website": "coolray.com", "search": "CoolRay Heating Air Rome GA"},
    ],
    "cartersville": [
        {"name": "SP Heating & Air", "website": None, "search": "SP Heating Air Cartersville GA"},
        {"name": "Chastain Plumbing Heating Cooling", "website": None, "search": "Chastain Plumbing Heating Cartersville GA"},
        {"name": "Weaver Heating & Air", "website": None, "search": "Weaver Heating Air Cartersville GA"},
    ],
}

# Target cities for monitoring
TARGET_CITIES = [
    "Calhoun", "Dalton", "Rome", "Cartersville", "Adairsville",
    "Chatsworth", "Jasper", "Ellijay", "Fairmount", "Resaca"
]


def make_request(url, params=None, max_retries=3):
    """Make API request with retry logic and rate limiting."""
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params=params, timeout=45)
            if resp.status_code == 200:
                return resp.json() if 'json' in resp.headers.get('content-type', '') else resp.text
            elif resp.status_code == 429:
                wait = 2 ** (attempt + 1)
                print(f"  ⏳ Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            elif resp.status_code == 502:
                time.sleep(2)
                continue
            else:
                print(f"  ⚠️ HTTP {resp.status_code}: {resp.text[:200]}")
                return None
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                print(f"  ❌ Request failed: {e}")
                return None
            time.sleep(2)
    return None


def scrape_google_maps_business(search_query):
    """Get business details from Google Maps search."""
    url = "https://api.scrape.do/plugin/google/maps/search"
    params = {
        "token": SCRAPE_DO_TOKEN,
        "q": search_query,
        "gl": "us",
        "hl": "en",
    }
    return make_request(url, params)


def scrape_google_maps_reviews(place_id, sort="newest", num=20, start=0):
    """Get reviews for a business from Google Maps."""
    url = "https://api.scrape.do/plugin/google/maps/reviews"
    params = {
        "token": SCRAPE_DO_TOKEN,
        "place_id": place_id,
        "sort": sort,
        "num": num,
        "start": start,
    }
    return make_request(url, params)


def scrape_competitor_website(website_url):
    """Scrape a competitor's website for content analysis."""
    url = "https://api.scrape.do"
    params = {
        "token": SCRAPE_DO_TOKEN,
        "url": f"https://{website_url}",
        "output": "markdown",
    }
    return make_request(url, params)


def get_competitor_gmb_data():
    """Fetch Google Maps data for all competitors and Anderson."""
    print("📍 Fetching Google Maps business data...")
    results = {"anderson": None, "competitors": {}, "timestamp": datetime.now().isoformat()}

    # Get Anderson's data first
    print(f"  🔍 {ANDERSON['name']}...")
    anderson_data = scrape_google_maps_business(ANDERSON["search_query"])
    if anderson_data and "local_results" in anderson_data:
        results["anderson"] = anderson_data["local_results"][0] if anderson_data["local_results"] else None
    time.sleep(1)

    # Get each competitor
    for market, competitors in COMPETITORS.items():
        results["competitors"][market] = []
        for comp in competitors:
            print(f"  🔍 {comp['name']} ({market})...")
            data = scrape_google_maps_business(comp["search"])
            if data and "local_results" in data:
                match = None
                for r in data.get("local_results", []):
                    if comp["name"].lower() in r.get("title", "").lower():
                        match = r
                        break
                if not match and data.get("local_results"):
                    match = data["local_results"][0]
                results["competitors"][market].append({
                    "name": comp["name"],
                    "data": match,
                    "website": comp["website"],
                })
            time.sleep(1)  # Rate limiting

    # Save results
    outfile = DATA_DIR / "competitor-gmb-data.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  ✅ Saved to {outfile}")
    return results


def compare_reviews():
    """Compare review counts and ratings across competitors."""
    print("\n📊 Review Comparison Analysis...")

    data_file = DATA_DIR / "competitor-gmb-data.json"
    if not data_file.exists():
        print("  ⚠️ No GMB data found. Run get_competitor_gmb_data() first.")
        return

    with open(data_file) as f:
        data = json.load(f)

    report = ["# Competitor Review Comparison", f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]

    # Anderson stats
    if data.get("anderson"):
        a = data["anderson"]
        report.append(f"## Anderson HAI")
        report.append(f"- **Rating:** {a.get('rating', 'N/A')} ⭐")
        report.append(f"- **Reviews:** {a.get('reviews', 'N/A')}")
        report.append("")

    # Competitor stats
    report.append("## Competitors by Market")
    for market, comps in data.get("competitors", {}).items():
        report.append(f"\n### {market.title()}")
        for comp in comps:
            d = comp.get("data", {}) or {}
            report.append(f"- **{comp['name']}:** {d.get('rating', '?')} ⭐ ({d.get('reviews', '?')} reviews)")

    report_text = "\n".join(report)
    outfile = DATA_DIR / "review-comparison.md"
    with open(outfile, "w") as f:
        f.write(report_text)
    print(f"  ✅ Report saved to {outfile}")
    return report_text


def monitor_competitor_websites():
    """Scrape competitor websites and detect changes."""
    print("\n🌐 Monitoring competitor websites...")
    changes_detected = []
    hashes_file = DATA_DIR / "website-hashes.json"

    # Load previous hashes
    prev_hashes = {}
    if hashes_file.exists():
        with open(hashes_file) as f:
            prev_hashes = json.load(f)

    current_hashes = {}

    for market, competitors in COMPETITORS.items():
        for comp in competitors:
            if not comp.get("website"):
                continue
            print(f"  🔍 Scraping {comp['website']}...")
            content = scrape_competitor_website(comp["website"])
            if content:
                content_str = str(content)
                content_hash = hashlib.md5(content_str.encode()).hexdigest()
                current_hashes[comp["website"]] = {
                    "hash": content_hash,
                    "timestamp": datetime.now().isoformat(),
                    "length": len(content_str),
                }

                # Check for changes
                prev = prev_hashes.get(comp["website"], {})
                if prev and prev.get("hash") != content_hash:
                    changes_detected.append({
                        "competitor": comp["name"],
                        "website": comp["website"],
                        "market": market,
                        "prev_length": prev.get("length", 0),
                        "new_length": len(content_str),
                        "detected": datetime.now().isoformat(),
                    })
                    print(f"    ⚠️ CHANGE DETECTED on {comp['website']}!")

                    # Save the new content for diff analysis
                    content_file = DATA_DIR / f"website-content-{comp['website'].replace('.', '-')}.md"
                    with open(content_file, "w") as f:
                        f.write(content_str[:50000])  # Cap at 50KB
            time.sleep(1)

    # Save current hashes
    with open(hashes_file, "w") as f:
        json.dump(current_hashes, f, indent=2)

    if changes_detected:
        changes_file = DATA_DIR / "website-changes.json"
        with open(changes_file, "w") as f:
            json.dump(changes_detected, f, indent=2)
        print(f"  🚨 {len(changes_detected)} website changes detected!")
    else:
        print("  ✅ No website changes detected.")

    return changes_detected


def generate_competitor_intel_report():
    """Generate a comprehensive competitor intelligence report."""
    print("\n📋 Generating Competitor Intelligence Report...")

    report = [
        "# Anderson HAI — Competitor Intelligence Report",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Markets Monitored:** {', '.join(TARGET_CITIES)}",
        "",
    ]

    # Load GMB data
    gmb_file = DATA_DIR / "competitor-gmb-data.json"
    if gmb_file.exists():
        with open(gmb_file) as f:
            gmb = json.load(f)

        report.append("## 📍 Google Maps Presence")
        report.append("")
        if gmb.get("anderson"):
            a = gmb["anderson"]
            report.append(f"### Anderson HAI (Our Listing)")
            report.append(f"- Rating: **{a.get('rating', 'N/A')}** ⭐ ({a.get('reviews', 'N/A')} reviews)")
            report.append(f"- Address: {a.get('address', 'N/A')}")
            report.append(f"- Phone: {a.get('phone', 'N/A')}")
            report.append("")

        for market, comps in gmb.get("competitors", {}).items():
            report.append(f"### {market.title()} Market")
            for comp in comps:
                d = comp.get("data") or {}
                report.append(f"**{comp['name']}**")
                report.append(f"- Rating: {d.get('rating', '?')} ⭐ ({d.get('reviews', '?')} reviews)")
                report.append(f"- Address: {d.get('address', 'N/A')}")
                report.append(f"- Website: {comp.get('website', 'N/A')}")
                report.append("")

    # Load website changes
    changes_file = DATA_DIR / "website-changes.json"
    if changes_file.exists():
        with open(changes_file) as f:
            changes = json.load(f)
        if changes:
            report.append("## 🚨 Recent Website Changes Detected")
            for ch in changes:
                report.append(f"- **{ch['competitor']}** ({ch['website']}): Content changed, {ch.get('prev_length', 0)} → {ch.get('new_length', 0)} chars")
            report.append("")

    # Competitive advantages
    report.extend([
        "## 💪 Anderson Competitive Advantages",
        "- **48 years in business** (since 1978) — most competitors under 30 years",
        "- **632+ Google reviews** at 4.8★ — likely highest in all markets",
        "- **BPI + NATE certified** — not all competitors have this",
        "- **In-house sheet metal shop** — unique differentiator",
        "- **10-city coverage** — broader reach than most local competitors",
        "- **Whole-home energy approach** — most competitors are HVAC-only",
        "",
        "## 🎯 Action Items",
        "- [ ] Verify competitor review counts monthly — maintain 2x review lead",
        "- [ ] Monitor competitor pricing pages for changes",
        "- [ ] Track new competitors entering target markets",
        "- [ ] Check for competitor Google Ads in target keywords",
        "- [ ] Monitor competitor schema markup improvements",
    ])

    report_text = "\n".join(report)
    outfile = DATA_DIR / "competitor-intel-report.md"
    with open(outfile, "w") as f:
        f.write(report_text)
    print(f"  ✅ Report saved to {outfile}")
    return report_text


# === MAIN EXECUTION ===
if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"

    if mode == "gmb":
        get_competitor_gmb_data()
    elif mode == "reviews":
        compare_reviews()
    elif mode == "websites":
        monitor_competitor_websites()
    elif mode == "report":
        generate_competitor_intel_report()
    elif mode == "full":
        get_competitor_gmb_data()
        compare_reviews()
        monitor_competitor_websites()
        generate_competitor_intel_report()
    else:
        print(f"Usage: {sys.argv[0]} [gmb|reviews|websites|report|full]")
