#!/usr/bin/env python3
"""
Anderson HAI — Local SEO Monitor
Tracks competitor Google Maps listings, local pack rankings,
citation consistency, and directory presence.

Credit cost: 10 credits per Maps API call, 10 per Search API call.
"""

import requests
import json
import os
import time
from datetime import datetime
from pathlib import Path

SCRAPE_DO_TOKEN = os.environ.get("SCRAPE_DO_TOKEN", "SCRAPE_DO_TOKEN_REMOVED")
DATA_DIR = Path(os.path.expanduser("~/.openclaw/workspace/data/seo-intelligence"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

CITIES = ["Calhoun", "Dalton", "Rome", "Cartersville", "Adairsville",
          "Chatsworth", "Jasper", "Ellijay", "Fairmount", "Resaca"]

ANDERSON_NAP = {
    "name": "Anderson Heating, Air & Insulation",
    "address": "519 Pine Street, Calhoun, GA 30701",
    "phone": "(706) 629-0749",
    "website": "johnandersonservice.com",
}

# Directories to check for citation consistency
CITATION_DIRECTORIES = [
    {"name": "Yelp", "search": "Anderson Heating Air Insulation site:yelp.com"},
    {"name": "BBB", "search": "Anderson Heating Air Insulation site:bbb.org"},
    {"name": "YellowPages", "search": "Anderson Heating Air Insulation Calhoun GA site:yellowpages.com"},
    {"name": "Angi", "search": "Anderson Heating Air Insulation site:angi.com"},
    {"name": "HomeAdvisor", "search": "Anderson Heating Air Insulation site:homeadvisor.com"},
    {"name": "Facebook", "search": "Anderson Heating Air Insulation Calhoun site:facebook.com"},
    {"name": "MapQuest", "search": "Anderson Heating Air Insulation site:mapquest.com"},
    {"name": "Manta", "search": "Anderson Heating Air Insulation site:manta.com"},
    {"name": "Porch", "search": "Anderson Heating Air Insulation site:porch.com"},
    {"name": "Carrier Dealer", "search": "Anderson Heating Air Insulation site:carrier.com"},
]


def api_request(url, params, retries=3):
    """Make API request with retries."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=45)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                time.sleep(2 ** (attempt + 1))
            elif resp.status_code == 502:
                time.sleep(2)
            else:
                return None
        except Exception:
            time.sleep(2)
    return None


def track_local_pack_rankings():
    """Track who shows up in Google's local 3-pack for HVAC searches in each city."""
    print("📍 Tracking Local Pack Rankings...")

    results = {"timestamp": datetime.now().isoformat(), "cities": {}}
    query_count = 0

    for city in CITIES:
        query = f"HVAC {city} GA"
        location = f"{city},Georgia,United States"
        print(f"  🔍 [{query_count + 1}/{len(CITIES)}] '{query}'...")

        serp = api_request(
            "https://api.scrape.do/plugin/google/search",
            {"token": SCRAPE_DO_TOKEN, "q": query, "gl": "us", "hl": "en", "location": location}
        )

        city_data = {"query": query, "local_pack": [], "anderson_in_pack": False}

        if serp:
            # Extract local pack results
            local = serp.get("local_results", [])
            if not local:
                local = serp.get("local_map", {}).get("local_results", [])

            for r in local:
                entry = {
                    "position": r.get("position"),
                    "title": r.get("title", ""),
                    "rating": r.get("rating"),
                    "reviews": r.get("reviews"),
                    "type": r.get("type", ""),
                }
                city_data["local_pack"].append(entry)

                # Check if Anderson is in the pack
                if "anderson" in entry["title"].lower():
                    city_data["anderson_in_pack"] = True
                    city_data["anderson_position"] = entry["position"]

        results["cities"][city] = city_data
        query_count += 1
        time.sleep(1.5)

    outfile = DATA_DIR / "local-pack-rankings.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  ✅ Saved to {outfile}")
    return results


def check_citation_consistency():
    """Check Anderson's NAP (Name, Address, Phone) consistency across directories."""
    print("\n📋 Checking Citation Consistency...")

    results = {"timestamp": datetime.now().isoformat(), "citations": []}

    for directory in CITATION_DIRECTORIES:
        print(f"  🔍 Checking {directory['name']}...")

        serp = api_request(
            "https://api.scrape.do/plugin/google/search",
            {"token": SCRAPE_DO_TOKEN, "q": directory["search"], "gl": "us", "hl": "en"}
        )

        citation = {
            "directory": directory["name"],
            "found": False,
            "url": None,
            "title": None,
            "snippet": None,
        }

        if serp:
            organic = serp.get("organic_results", [])
            if organic:
                top = organic[0]
                citation["found"] = True
                citation["url"] = top.get("link", "")
                citation["title"] = top.get("title", "")
                citation["snippet"] = top.get("snippet", "")[:200]

                # Check for NAP consistency in snippet
                snippet_lower = citation["snippet"].lower() if citation["snippet"] else ""
                citation["has_phone"] = "706" in snippet_lower and "629" in snippet_lower
                citation["has_address"] = "pine" in snippet_lower or "calhoun" in snippet_lower

        results["citations"].append(citation)
        time.sleep(1.5)

    outfile = DATA_DIR / "citation-consistency.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  ✅ Saved to {outfile}")
    return results


def monitor_competitor_gmb_changes():
    """Track changes in competitor Google Maps listings over time."""
    print("\n📍 Monitoring Competitor GMB Changes...")

    competitors = [
        "Cherokee Mechanical Calhoun GA",
        "Calhoun Air Care Calhoun GA",
        "Dalton Heating Air Dalton GA",
    ]

    results = {"timestamp": datetime.now().isoformat(), "competitors": []}

    for comp_query in competitors:
        print(f"  🔍 {comp_query}...")
        data = api_request(
            "https://api.scrape.do/plugin/google/maps/search",
            {"token": SCRAPE_DO_TOKEN, "q": comp_query}
        )

        if data and data.get("local_results"):
            r = data["local_results"][0]
            results["competitors"].append({
                "query": comp_query,
                "title": r.get("title", ""),
                "rating": r.get("rating"),
                "reviews": r.get("reviews"),
                "address": r.get("address", ""),
                "phone": r.get("phone", ""),
                "website": r.get("website", ""),
                "place_id": r.get("place_id", ""),
            })
        time.sleep(1)

    outfile = DATA_DIR / "competitor-gmb-changes.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  ✅ Saved to {outfile}")
    return results


def generate_local_seo_report():
    """Generate comprehensive local SEO report."""
    report = [
        "# Anderson HAI — Local SEO Intelligence Report",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    # Local pack rankings
    pack_file = DATA_DIR / "local-pack-rankings.json"
    if pack_file.exists():
        with open(pack_file) as f:
            pack_data = json.load(f)

        report.append("## 📍 Local 3-Pack Rankings")
        report.append("*Who shows in Google's map pack for 'HVAC [City] GA':*\n")

        in_pack_count = 0
        for city, data in pack_data.get("cities", {}).items():
            in_pack = "✅" if data.get("anderson_in_pack") else "❌"
            if data.get("anderson_in_pack"):
                in_pack_count += 1

            report.append(f"### {city} — Anderson in Pack: {in_pack}")
            for r in data.get("local_pack", []):
                marker = "**→**" if "anderson" in r.get("title", "").lower() else "  "
                report.append(f"{marker} #{r.get('position', '?')}: {r.get('title', 'Unknown')} ({r.get('rating', '?')}⭐, {r.get('reviews', '?')} reviews)")
            report.append("")

        report.append(f"**Summary:** Anderson in local pack for {in_pack_count}/{len(pack_data.get('cities', {}))} cities")
        report.append("")

    # Citation consistency
    cite_file = DATA_DIR / "citation-consistency.json"
    if cite_file.exists():
        with open(cite_file) as f:
            cite_data = json.load(f)

        report.append("## 📋 Citation Directory Presence")
        report.append("| Directory | Found | URL | Phone Match | Address Match |")
        report.append("|-----------|-------|-----|-------------|---------------|")

        for c in cite_data.get("citations", []):
            found = "✅" if c.get("found") else "❌"
            phone = "✅" if c.get("has_phone") else "❌"
            addr = "✅" if c.get("has_address") else "❌"
            url = c.get("url", "N/A")[:50]
            report.append(f"| {c['directory']} | {found} | {url} | {phone} | {addr} |")
        report.append("")

    # Competitor GMB
    comp_file = DATA_DIR / "competitor-gmb-changes.json"
    if comp_file.exists():
        with open(comp_file) as f:
            comp_data = json.load(f)

        report.append("## 🏢 Competitor GMB Listings")
        for comp in comp_data.get("competitors", []):
            report.append(f"### {comp.get('title', 'Unknown')}")
            report.append(f"- Rating: {comp.get('rating', '?')} ⭐ ({comp.get('reviews', '?')} reviews)")
            report.append(f"- Phone: {comp.get('phone', 'N/A')}")
            report.append(f"- Website: {comp.get('website', 'N/A')}")
            report.append("")

    # Action items
    report.extend([
        "## 🎯 Local SEO Action Items",
        "- [ ] Claim/update any missing directory listings",
        "- [ ] Fix any NAP inconsistencies found above",
        "- [ ] Respond to all recent Google reviews within 24h",
        "- [ ] Add photos to GMB listing weekly",
        "- [ ] Post Google Business updates weekly",
        "- [ ] Request reviews from recent satisfied customers",
        "- [ ] Monitor competitor review velocity monthly",
    ])

    report_text = "\n".join(report)
    outfile = DATA_DIR / "local-seo-report.md"
    with open(outfile, "w") as f:
        f.write(report_text)
    print(f"✅ Report saved to {outfile}")
    return report_text


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "estimate"

    if mode == "estimate":
        pack_credits = len(CITIES) * 10
        cite_credits = len(CITATION_DIRECTORIES) * 10
        comp_credits = 3 * 10
        total = pack_credits + cite_credits + comp_credits
        print(f"📊 Local SEO Monitor Credit Estimate:")
        print(f"   Local pack: {len(CITIES)} cities × 10 = {pack_credits}")
        print(f"   Citations: {len(CITATION_DIRECTORIES)} directories × 10 = {cite_credits}")
        print(f"   Competitor GMB: 3 × 10 = {comp_credits}")
        print(f"   TOTAL: {total} credits")
    elif mode == "pack":
        track_local_pack_rankings()
    elif mode == "citations":
        check_citation_consistency()
    elif mode == "competitors":
        monitor_competitor_gmb_changes()
    elif mode == "report":
        generate_local_seo_report()
    elif mode == "full":
        track_local_pack_rankings()
        check_citation_consistency()
        monitor_competitor_gmb_changes()
        generate_local_seo_report()
    else:
        print(f"Usage: {sys.argv[0]} [estimate|pack|citations|competitors|report|full]")
