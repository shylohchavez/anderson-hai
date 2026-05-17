#!/usr/bin/env python3
"""
Anderson HAI — Keyword Ranking Tracker
Uses Scrape.do Google Search API to track keyword positions
for Anderson HAI vs competitors across all 10 target cities.

Credit cost: 10 credits per search query (Google Search API).
Budget-conscious: Prioritizes high-impact keywords first.
"""

import requests
import json
import os
import time
import re
from datetime import datetime
from pathlib import Path

# === CONFIGURATION ===
SCRAPE_DO_TOKEN = os.environ.get("SCRAPE_DO_TOKEN", "SCRAPE_DO_TOKEN_REMOVED")
DATA_DIR = Path(os.path.expanduser("~/.openclaw/workspace/data/seo-intelligence"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Our domains to track
ANDERSON_DOMAINS = [
    "johnandersonservice.com",
    "shylohchavez.github.io/anderson-hai",
]

# Target cities
CITIES = ["Calhoun", "Dalton", "Rome", "Cartersville", "Adairsville",
          "Chatsworth", "Jasper", "Ellijay", "Fairmount", "Resaca"]

# Keyword templates — {city} gets replaced with each target city
# Tiered by priority (Tier 1 tracked weekly, Tier 2 biweekly, Tier 3 monthly)
KEYWORD_TEMPLATES = {
    "tier1": [  # 10 credits each × 10 cities = 100 credits per run
        "HVAC {city} GA",
        "AC repair {city} GA",
        "heating repair {city} GA",
    ],
    "tier2": [  # Run biweekly
        "air conditioning {city} GA",
        "furnace repair {city} GA",
        "heat pump {city} GA",
        "HVAC company {city} GA",
        "AC installation {city} GA",
    ],
    "tier3": [  # Run monthly
        "emergency HVAC {city} GA",
        "duct cleaning {city} GA",
        "insulation {city} GA",
        "energy audit {city} GA",
        "HVAC maintenance {city} GA",
        "mini split {city} GA",
        "water heater {city} GA",
        "24/7 AC repair {city} GA",
    ],
}

# Known competitor domains for identification
COMPETITOR_DOMAINS = {
    "cherokeemech.com": "Cherokee Mechanical",
    "calhounaircare.com": "Calhoun Air Care",
    "coolray.com": "CoolRay",
    "leecompany.com": "Lee Company",
    "premierindoor.com": "Premier Indoor",
}


def search_google(query, location=None):
    """Search Google via Scrape.do and return parsed results."""
    url = "https://api.scrape.do/plugin/google/search"
    params = {
        "token": SCRAPE_DO_TOKEN,
        "q": query,
        "gl": "us",
        "hl": "en",
        "device": "desktop",
    }
    if location:
        params["location"] = location

    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, timeout=45)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                time.sleep(2 ** (attempt + 1))
            elif resp.status_code == 502:
                time.sleep(2)
            else:
                print(f"  ⚠️ HTTP {resp.status_code} for '{query}'")
                return None
        except requests.RequestException as e:
            if attempt == 2:
                print(f"  ❌ Request failed: {e}")
            time.sleep(2)
    return None


def find_position(serp_data, target_domains):
    """Find position of target domain in SERP results."""
    if not serp_data:
        return None, None

    organic = serp_data.get("organic_results", [])
    for result in organic:
        link = result.get("link", "")
        for domain in target_domains:
            if domain in link:
                return result.get("position", None), link

    return None, None


def find_competitors_in_serp(serp_data, known_domains):
    """Find known competitors in SERP results."""
    if not serp_data:
        return []

    found = []
    organic = serp_data.get("organic_results", [])
    for result in organic:
        link = result.get("link", "")
        for domain, name in known_domains.items():
            if domain in link:
                found.append({
                    "name": name,
                    "position": result.get("position"),
                    "link": link,
                    "title": result.get("title", ""),
                })
    return found


def extract_local_pack(serp_data):
    """Extract local pack (map pack) results."""
    if not serp_data:
        return []

    # Scrape.do returns local results in various fields
    local = serp_data.get("local_results", [])
    if not local:
        local = serp_data.get("local_map", {}).get("local_results", [])

    pack = []
    for r in local:
        pack.append({
            "position": r.get("position"),
            "title": r.get("title", ""),
            "rating": r.get("rating"),
            "reviews": r.get("reviews"),
            "address": r.get("address", ""),
        })
    return pack


def track_keywords(tier="tier1", cities=None):
    """Track keyword rankings for specified tier and cities."""
    cities = cities or CITIES
    templates = KEYWORD_TEMPLATES.get(tier, KEYWORD_TEMPLATES["tier1"])

    total_queries = len(templates) * len(cities)
    credits_needed = total_queries * 10
    print(f"🔍 Tracking {tier} keywords: {len(templates)} templates × {len(cities)} cities = {total_queries} queries ({credits_needed} credits)")

    results = {
        "tier": tier,
        "timestamp": datetime.now().isoformat(),
        "total_queries": total_queries,
        "credits_used": credits_needed,
        "rankings": {},
    }

    query_count = 0
    for city in cities:
        results["rankings"][city] = {}
        location = f"{city},Georgia,United States"

        for template in templates:
            keyword = template.format(city=city)
            print(f"  [{query_count + 1}/{total_queries}] '{keyword}'...")

            serp = search_google(keyword, location=location)
            if not serp:
                results["rankings"][city][keyword] = {"position": None, "error": True}
                continue

            # Find Anderson's position
            position, url = find_position(serp, ANDERSON_DOMAINS)

            # Find competitors
            competitors_found = find_competitors_in_serp(serp, COMPETITOR_DOMAINS)

            # Get local pack
            local_pack = extract_local_pack(serp)

            # Get People Also Ask
            paa = serp.get("related_questions", [])

            results["rankings"][city][keyword] = {
                "position": position,
                "url": url,
                "competitors": competitors_found,
                "local_pack": local_pack,
                "people_also_ask": [q.get("question", "") for q in paa[:5]],
                "top_3": [
                    {"position": r.get("position"), "title": r.get("title", ""), "link": r.get("link", "")}
                    for r in serp.get("organic_results", [])[:3]
                ],
            }

            query_count += 1
            time.sleep(1.5)  # Be gentle with rate limits

    # Save results
    date_str = datetime.now().strftime("%Y-%m-%d")
    outfile = DATA_DIR / f"rankings-{tier}-{date_str}.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)

    # Also save as "latest"
    latest_file = DATA_DIR / f"rankings-{tier}-latest.json"
    with open(latest_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Saved rankings to {outfile}")
    return results


def generate_ranking_report(tier="tier1"):
    """Generate a human-readable ranking report with trends."""
    latest_file = DATA_DIR / f"rankings-{tier}-latest.json"
    if not latest_file.exists():
        print(f"No ranking data found for {tier}. Run track_keywords first.")
        return

    with open(latest_file) as f:
        data = json.load(f)

    report = [
        "# Anderson HAI — Keyword Ranking Report",
        f"**Tier:** {tier.upper()}",
        f"**Date:** {data.get('timestamp', 'Unknown')[:10]}",
        f"**Queries:** {data.get('total_queries', 0)} ({data.get('credits_used', 0)} credits)",
        "",
    ]

    # Summary stats
    all_positions = []
    top_3_count = 0
    top_10_count = 0
    not_ranking = 0

    for city, keywords in data.get("rankings", {}).items():
        for keyword, info in keywords.items():
            pos = info.get("position")
            if pos:
                all_positions.append(pos)
                if pos <= 3:
                    top_3_count += 1
                if pos <= 10:
                    top_10_count += 1
            else:
                not_ranking += 1

    total = len(all_positions) + not_ranking
    avg_pos = sum(all_positions) / len(all_positions) if all_positions else 0

    report.extend([
        "## 📊 Summary",
        f"- **Average Position:** {avg_pos:.1f}",
        f"- **Top 3 Rankings:** {top_3_count}/{total} ({top_3_count/total*100:.0f}%)" if total else "",
        f"- **Page 1 (Top 10):** {top_10_count}/{total} ({top_10_count/total*100:.0f}%)" if total else "",
        f"- **Not Ranking:** {not_ranking}/{total}",
        "",
    ])

    # City-by-city breakdown
    report.append("## 📍 Rankings by City")
    for city in CITIES:
        keywords = data.get("rankings", {}).get(city, {})
        if not keywords:
            continue

        report.append(f"\n### {city}, GA")
        report.append("| Keyword | Position | Top Competitor | Notes |")
        report.append("|---------|----------|----------------|-------|")

        for keyword, info in keywords.items():
            pos = info.get("position")
            pos_str = f"#{pos}" if pos else "Not found"
            pos_emoji = "🏆" if pos and pos <= 3 else ("✅" if pos and pos <= 10 else "⚠️")

            # Top competitor
            comps = info.get("competitors", [])
            comp_str = f"{comps[0]['name']} (#{comps[0]['position']})" if comps else "-"

            report.append(f"| {keyword} | {pos_emoji} {pos_str} | {comp_str} | {', '.join(info.get('people_also_ask', [])[:2])} |")

    # Opportunities section
    report.extend([
        "",
        "## 🎯 Opportunities",
        "### Keywords Where We're NOT in Top 3:",
    ])

    for city, keywords in data.get("rankings", {}).items():
        for keyword, info in keywords.items():
            pos = info.get("position")
            if not pos or pos > 3:
                who_ranks = info.get("top_3", [])
                top_str = ", ".join([f"{r.get('title', '')[:40]}" for r in who_ranks[:2]])
                report.append(f"- **{keyword}** — {'#' + str(pos) if pos else 'Unranked'} (Top: {top_str})")

    # People Also Ask opportunities
    report.extend([
        "",
        "### 💡 People Also Ask (Content Opportunities):",
    ])
    all_paa = set()
    for city, keywords in data.get("rankings", {}).items():
        for keyword, info in keywords.items():
            for q in info.get("people_also_ask", []):
                if q:
                    all_paa.add(q)
    for q in sorted(all_paa)[:20]:
        report.append(f"- {q}")

    report_text = "\n".join(report)
    outfile = DATA_DIR / f"ranking-report-{tier}.md"
    with open(outfile, "w") as f:
        f.write(report_text)
    print(f"✅ Report saved to {outfile}")
    return report_text


def estimate_credits(tier="tier1", cities=None):
    """Estimate credits needed without making any API calls."""
    cities = cities or CITIES
    templates = KEYWORD_TEMPLATES.get(tier, [])
    total = len(templates) * len(cities) * 10
    print(f"📊 Credit Estimate for {tier}:")
    print(f"   {len(templates)} keywords × {len(cities)} cities × 10 credits = {total} credits")
    return total


# === MAIN ===
if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "estimate"
    tier = sys.argv[2] if len(sys.argv) > 2 else "tier1"

    if mode == "estimate":
        for t in ["tier1", "tier2", "tier3"]:
            estimate_credits(t)
            print()
    elif mode == "track":
        track_keywords(tier=tier)
    elif mode == "report":
        generate_ranking_report(tier=tier)
    elif mode == "quick":
        # Quick check: Just Calhoun + Dalton, tier1 only
        track_keywords(tier="tier1", cities=["Calhoun", "Dalton"])
        generate_ranking_report(tier="tier1")
    else:
        print(f"Usage: {sys.argv[0]} [estimate|track|report|quick] [tier1|tier2|tier3]")
