#!/usr/bin/env python3
"""
Anderson HAI — Content Gap Analysis
Identifies what content ranks #1 for target keywords that Anderson is missing.
Generates actionable content recommendations.

Credit cost: 10 credits per Google Search query.
"""

import requests
import json
import os
import time
import re
from datetime import datetime
from pathlib import Path
from collections import Counter

SCRAPE_DO_TOKEN = os.environ.get("SCRAPE_DO_TOKEN", "SCRAPE_DO_TOKEN_REMOVED")
DATA_DIR = Path(os.path.expanduser("~/.openclaw/workspace/data/seo-intelligence"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

ANDERSON_DOMAINS = ["johnandersonservice.com", "shylohchavez.github.io/anderson-hai"]

# Content gap keywords — things homeowners search that Anderson should rank for
CONTENT_GAP_QUERIES = [
    # Cost / pricing queries (high commercial intent)
    "how much does AC repair cost {city} GA",
    "HVAC installation cost {city} GA",
    "furnace replacement cost Georgia",
    "heat pump installation cost NW Georgia",
    "insulation cost per square foot Georgia",
    "duct cleaning cost {city} GA",

    # How-to / educational queries (top of funnel)
    "how often should I change my air filter",
    "what size HVAC system do I need",
    "heat pump vs furnace Georgia",
    "signs I need a new AC unit",
    "how to reduce energy bills Georgia",
    "what is a BPI energy audit",
    "crawlspace encapsulation benefits",
    "spray foam vs blown insulation Georgia",

    # Emergency / urgent queries
    "AC not cooling {city} GA",
    "furnace blowing cold air fix",
    "HVAC emergency service near me {city} GA",

    # Seasonal queries
    "spring AC maintenance checklist Georgia",
    "winter heating preparation Georgia",
    "when to service AC before summer",

    # Brand / comparison queries
    "Trane vs Carrier HVAC Georgia",
    "best HVAC brands for Georgia climate",
    "MRCOOL mini split reviews",

    # Local / specific queries
    "Georgia Power rebate HVAC 2026",
    "TVA weatherization program Georgia",
    "energy rebates northwest Georgia",
]

SAMPLE_CITIES = ["Calhoun", "Dalton", "Rome"]  # Use subset for city-specific queries


def search_google(query):
    """Search Google via Scrape.do."""
    url = "https://api.scrape.do/plugin/google/search"
    params = {
        "token": SCRAPE_DO_TOKEN,
        "q": query,
        "gl": "us",
        "hl": "en",
    }
    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, timeout=45)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                time.sleep(2 ** (attempt + 1))
            else:
                return None
        except Exception:
            time.sleep(2)
    return None


def analyze_content_gaps():
    """Run content gap analysis."""
    print("🔍 Running Content Gap Analysis...")

    # Build query list, expanding city templates
    queries = []
    for q in CONTENT_GAP_QUERIES:
        if "{city}" in q:
            for city in SAMPLE_CITIES:
                queries.append(q.format(city=city))
        else:
            queries.append(q)

    credits_needed = len(queries) * 10
    print(f"   {len(queries)} queries × 10 credits = {credits_needed} credits")

    gaps = []
    anderson_rankings = []
    paa_questions = set()

    for i, query in enumerate(queries):
        print(f"  [{i+1}/{len(queries)}] '{query}'...")
        serp = search_google(query)
        if not serp:
            continue

        # Check if Anderson ranks
        anderson_pos = None
        organic = serp.get("organic_results", [])
        for r in organic:
            link = r.get("link", "")
            if any(d in link for d in ANDERSON_DOMAINS):
                anderson_pos = r.get("position")
                break

        # Get top result
        top_result = organic[0] if organic else None

        # Collect People Also Ask
        for paa in serp.get("related_questions", []):
            q_text = paa.get("question", "")
            if q_text:
                paa_questions.add(q_text)

        entry = {
            "query": query,
            "anderson_position": anderson_pos,
            "top_result": {
                "title": top_result.get("title", "") if top_result else "",
                "link": top_result.get("link", "") if top_result else "",
                "snippet": top_result.get("snippet", "") if top_result else "",
            } if top_result else None,
            "top_5": [
                {
                    "position": r.get("position"),
                    "title": r.get("title", ""),
                    "link": r.get("link", ""),
                    "snippet": r.get("snippet", "")[:150],
                }
                for r in organic[:5]
            ],
            "has_featured_snippet": bool(serp.get("answer_box") or serp.get("featured_snippet")),
            "has_local_pack": bool(serp.get("local_results")),
        }

        if anderson_pos is None or anderson_pos > 10:
            gaps.append(entry)
        else:
            anderson_rankings.append(entry)

        time.sleep(1.5)

    # Save raw data
    results = {
        "timestamp": datetime.now().isoformat(),
        "total_queries": len(queries),
        "gaps": gaps,
        "ranking": anderson_rankings,
        "paa_questions": sorted(paa_questions),
    }
    with open(DATA_DIR / "content-gap-analysis.json", "w") as f:
        json.dump(results, f, indent=2)

    # Generate report
    generate_content_gap_report(results)
    return results


def generate_content_gap_report(data=None):
    """Generate actionable content gap report."""
    if data is None:
        gap_file = DATA_DIR / "content-gap-analysis.json"
        if not gap_file.exists():
            print("No gap analysis data. Run analyze_content_gaps() first.")
            return
        with open(gap_file) as f:
            data = json.load(f)

    gaps = data.get("gaps", [])
    ranking = data.get("ranking", [])
    paa = data.get("paa_questions", [])

    report = [
        "# Anderson HAI — Content Gap Analysis Report",
        f"**Date:** {data.get('timestamp', '')[:10]}",
        f"**Queries Analyzed:** {data.get('total_queries', 0)}",
        f"**Ranking (Page 1):** {len(ranking)}",
        f"**Content Gaps:** {len(gaps)}",
        "",
        "---",
        "",
    ]

    # Priority content to create
    report.append("## 🚨 HIGH PRIORITY — Content Anderson Needs")
    report.append("*These are queries where Anderson is NOT on page 1 but should be.*\n")

    # Categorize gaps
    cost_gaps = [g for g in gaps if any(w in g["query"].lower() for w in ["cost", "price", "how much"])]
    emergency_gaps = [g for g in gaps if any(w in g["query"].lower() for w in ["emergency", "not cooling", "cold air"])]
    educational_gaps = [g for g in gaps if any(w in g["query"].lower() for w in ["how", "what", "when", "signs", "vs"])]
    local_gaps = [g for g in gaps if any(w in g["query"].lower() for w in ["georgia", "rebate", "tva"])]
    other_gaps = [g for g in gaps if g not in cost_gaps + emergency_gaps + educational_gaps + local_gaps]

    if cost_gaps:
        report.append("### 💰 Pricing / Cost Content (High Commercial Intent)")
        for g in cost_gaps:
            top = g.get("top_result", {}) or {}
            report.append(f"- **Query:** `{g['query']}`")
            report.append(f"  - #1 result: [{top.get('title', 'N/A')}]({top.get('link', '')})")
            report.append(f"  - **Action:** Create pricing guide page targeting this query")
        report.append("")

    if emergency_gaps:
        report.append("### 🚨 Emergency / Urgent Content")
        for g in emergency_gaps:
            top = g.get("top_result", {}) or {}
            report.append(f"- **Query:** `{g['query']}`")
            report.append(f"  - #1 result: [{top.get('title', 'N/A')}]({top.get('link', '')})")
        report.append("")

    if educational_gaps:
        report.append("### 📚 Educational / How-To Content")
        for g in educational_gaps:
            top = g.get("top_result", {}) or {}
            report.append(f"- **Query:** `{g['query']}`")
            report.append(f"  - #1 result: [{top.get('title', 'N/A')}]({top.get('link', '')})")
        report.append("")

    if local_gaps:
        report.append("### 📍 Local / Rebate Content")
        for g in local_gaps:
            top = g.get("top_result", {}) or {}
            report.append(f"- **Query:** `{g['query']}`")
            report.append(f"  - #1 result: [{top.get('title', 'N/A')}]({top.get('link', '')})")
        report.append("")

    # Where Anderson IS ranking
    report.append("## ✅ Where Anderson IS Ranking (Page 1)")
    for r in ranking:
        report.append(f"- `{r['query']}` — **#{r['anderson_position']}**")
    report.append("")

    # People Also Ask — content opportunities
    report.append("## 💡 People Also Ask — Blog Post Opportunities")
    report.append("*Create FAQ content or blog posts answering these questions:*\n")
    for q in paa[:30]:
        report.append(f"- {q}")
    report.append("")

    # Recommended content calendar
    report.append("## 📅 Recommended Content Calendar")
    report.append("")
    report.append("### Week 1-2: Cost/Pricing Pages (Highest ROI)")
    report.append("- Create: 'AC Repair Cost in [City] GA — Complete 2026 Guide'")
    report.append("- Create: 'HVAC Installation Cost Georgia — What to Expect'")
    report.append("- Create: 'Insulation Cost Per Square Foot — NW Georgia Pricing'")
    report.append("")
    report.append("### Week 3-4: Educational Content")
    report.append("- Create: 'Heat Pump vs Furnace: Which Is Better for Georgia?'")
    report.append("- Create: '7 Signs You Need a New AC Unit'")
    report.append("- Create: 'What Is a BPI Energy Audit? Complete Guide'")
    report.append("")
    report.append("### Week 5-6: Local Authority Content")
    report.append("- Create: 'Georgia Power HVAC Rebates 2026 — Complete Guide'")
    report.append("- Create: 'TVA Weatherization Program — How to Qualify'")
    report.append("- Create: 'Energy Rebates for NW Georgia Homeowners'")

    report_text = "\n".join(report)
    outfile = DATA_DIR / "content-gap-report.md"
    with open(outfile, "w") as f:
        f.write(report_text)
    print(f"✅ Report saved to {outfile}")
    return report_text


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "estimate"

    if mode == "estimate":
        # Count queries without running them
        queries = []
        for q in CONTENT_GAP_QUERIES:
            if "{city}" in q:
                for city in SAMPLE_CITIES:
                    queries.append(q.format(city=city))
            else:
                queries.append(q)
        print(f"📊 Content Gap Analysis would use {len(queries)} queries × 10 = {len(queries) * 10} credits")
    elif mode == "analyze":
        analyze_content_gaps()
    elif mode == "report":
        generate_content_gap_report()
    else:
        print(f"Usage: {sys.argv[0]} [estimate|analyze|report]")
