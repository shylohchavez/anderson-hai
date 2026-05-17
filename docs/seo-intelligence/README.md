# Anderson Heating, Air & Insulation — SEO Intelligence System

This directory contains a comprehensive, automated SEO intelligence and monitoring system built to help Anderson HAI dominate search rankings in their 10 target cities. The system uses the Scrape.do API to gather data without being blocked, providing insights into competitors, keyword rankings, content opportunities, and more.

**System Goal:** Achieve and maintain #1 rankings for target keywords across all service areas through data-driven automation and surveillance.

## 🚀 Quick Start

To run the entire SEO intelligence suite and generate a master report, execute the master script:

```bash
# Ensure the script is executable
chmod +x scripts/seo-intelligence/run_all.sh

# Run the full suite
./scripts/seo-intelligence/run_all.sh
```

The script will:
1.  Run all five monitoring modules.
2.  Gather fresh data on competitors, rankings, content gaps, local SEO, and technical SEO.
3.  Generate individual markdown reports for each module.
4.  Consolidate everything into a single `MASTER-SEO-REPORT-YYYY-MM-DD.md`.
5.  Store all raw data (JSON) and reports (MD) in `data/seo-intelligence/reports/`.

**Latest reports are always available in `data/seo-intelligence/reports/latest/`.**

---

## 🔧 System Modules

The system is composed of five core Python scripts, each responsible for a different area of SEO intelligence.

### 1. `competitor_monitor.py`
Monitors the online presence of key competitors.
- **What it does:** Scrapes competitor websites and Google Maps listings.
- **Intelligence:** Tracks changes in services, pricing (if available), Google reviews, and ratings. Detects when competitors update their websites.
- **Usage:** `python3 scripts/seo-intelligence/competitor_monitor.py [gmb|reviews|websites|report|full]`

### 2. `keyword_rank_tracker.py`
Tracks Anderson HAI's search engine ranking for critical keywords against competitors.
- **What it does:** Uses Scrape.do's Google Search API to perform real searches from target city locations.
- **Intelligence:** Provides exact ranking positions for Anderson and competitors, identifies who holds the top spots, and extracts "People Also Ask" questions for content ideas. Keywords are tiered by priority to manage credit usage.
- **Usage:** `python3 scripts/seo-intelligence/keyword_rank_tracker.py [estimate|track|report|quick] [tier1|tier2|tier3]`

### 3. `content_gap_analyzer.py`
Finds what content is ranking #1 for important non-branded keywords that Anderson is missing.
- **What it does:** Searches for high-intent queries (e.g., "how much does ac repair cost dalton ga") and analyzes the top results.
- **Intelligence:** Generates a prioritized list of content Anderson needs to create to capture this traffic, from pricing guides to educational blog posts.
- **Usage:** `python3 scripts/seo-intelligence/content_gap_analyzer.py [estimate|analyze|report]`

### 4. `local_seo_monitor.py`
Monitors factors critical for local search rankings.
- **What it does:** Tracks Google's local 3-pack (map pack) results for each target city. It also checks for Anderson's presence and consistency across major online directories (Yelp, BBB, etc.).
- **Intelligence:** Identifies where Anderson is (and isn't) visible in local map results and flags inconsistencies in their business listings (Name, Address, Phone) that could harm rankings.
- **Usage:** `python3 scripts/seo-intelligence/local_seo_monitor.py [estimate|pack|citations|competitors|report|full]`

### 5. `technical_seo_monitor.py`
Keeps an eye on competitors' technical SEO tactics.
- **What it does:** Scrapes competitor `sitemap.xml` files to discover new pages they publish. It also extracts and monitors their `schema.org` structured data.
- **Intelligence:** Provides immediate alerts when a competitor launches a new service page, publishes a new blog post, or implements advanced schema markup (like FAQPage or Service), revealing their SEO strategy.
- **Usage:** `python3 scripts/seo-intelligence/technical_seo_monitor.py [pages|schema|report|full]`

---

## ⚙️ Configuration

- **API Token:** The scripts use the `SCRAPE_DO_TOKEN` environment variable. It's also hardcoded as a fallback.
- **Data Storage:** All raw data and reports are stored in `~/.openclaw/workspace/data/seo-intelligence/`.
- **Competitors & Keywords:** Competitor lists, target cities, and keywords can be easily modified in the top sections of each Python script.

## 💰 API Credit Usage

The system is designed to be budget-conscious.
- **Estimates:** Each script can be run with the `estimate` command to see how many credits a run will consume without actually making API calls.
- **Tiered Tracking:** Keyword tracking is split into tiers (`tier1`, `tier2`, `tier3`) so that the most important keywords can be tracked weekly while less critical ones are tracked bi-weekly or monthly, saving credits.
- **Total Cost:** A full weekly run (Tier 1 keywords) will consume approximately **800-1000 credits**.

## 🗓️ Automation (Cron Job)

To automate this system, set up a cron job to run the `run_all.sh` script weekly.

1.  Open the crontab editor: `crontab -e`
2.  Add the following line to run the script every Monday at 4 AM:
    ```
    0 4 * * 1 /home/shyloh/.openclaw/workspace/scripts/seo-intelligence/run_all.sh > /home/shyloh/cronlogs/seo-intel-$(date +\%Y\%m\%d).log 2>&1
    ```

This ensures a fresh intelligence report is ready for review at the start of each week.
