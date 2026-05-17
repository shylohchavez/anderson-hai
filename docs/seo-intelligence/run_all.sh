#!/bin/bash
#
# Anderson HAI SEO Intelligence System - Master Runner
# ======================================================
# This script executes all SEO monitoring modules in sequence
# and generates a unified final report.
#
# Schedule this to run weekly via cron for automated insights.
# Example cron:
# 0 4 * * 1 /home/shyloh/.openclaw/workspace/scripts/seo-intelligence/run_all.sh > /home/shyloh/cronlogs/seo-intel.log 2>&1

set -e
export PYTHONUNBUFFERED=1
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DATA_DIR="/home/shyloh/.openclaw/workspace/data/seo-intelligence"
REPORTS_DIR="$DATA_DIR/reports/$(date +%Y-%m-%d)"
LATEST_REPORTS_DIR="$DATA_DIR/reports/latest"

echo "======================================================"
echo "🚀 Anderson HAI SEO Intelligence System"
echo "Date: $(date)"
echo "Data Directory: $DATA_DIR"
echo "======================================================"

# Create directories for today's reports
mkdir -p "$REPORTS_DIR"
rm -rf "$LATEST_REPORTS_DIR"
mkdir -p "$LATEST_REPORTS_DIR"

# --- Module 1: Competitor Intelligence ---
echo -e "\n[1/5] Running Competitor Intelligence Monitor..."
python3 "$BASE_DIR/competitor_monitor.py" full
echo "[1/5] Competitor Intelligence Monitor finished."

# --- Module 2: Keyword Ranking Tracker ---
# Run Tier 1 weekly, Tier 2 on the 1st and 15th, Tier 3 on the 1st.
DAY_OF_MONTH=$(date +%d)
echo -e "\n[2/5] Running Keyword Ranking Tracker..."
echo "  - Running Tier 1 (weekly)..."
python3 "$BASE_DIR/keyword_rank_tracker.py" track --tier tier1
if [[ "$DAY_OF_MONTH" == "01" || "$DAY_OF_MONTH" == "15" ]]; then
    echo "  - Running Tier 2 (bi-weekly)..."
    python3 "$BASE_DIR/keyword_rank_tracker.py" track --tier tier2
fi
if [[ "$DAY_OF_MONTH" == "01" ]]; then
    echo "  - Running Tier 3 (monthly)..."
    python3 "$BASE_DIR/keyword_rank_tracker.py" track --tier tier3
fi
echo "[2/5] Keyword Ranking Tracker finished."

# --- Module 3: Content Gap Analysis ---
echo -e "\n[3/5] Running Content Gap Analyzer..."
python3 "$BASE_DIR/content_gap_analyzer.py" analyze
echo "[3/5] Content Gap Analyzer finished."

# --- Module 4: Local SEO Monitor ---
echo -e "\n[4/5] Running Local SEO Monitor..."
python3 "$BASE_DIR/local_seo_monitor.py" full
echo "[4/5] Local SEO Monitor finished."

# --- Module 5: Technical SEO Surveillance ---
echo -e "\n[5/5] Running Technical SEO Surveillance Monitor..."
python3 "$BASE_DIR/technical_seo_monitor.py" full
echo "[5/5] Technical SEO Surveillance Monitor finished."


# --- Final Report Generation ---
echo -e "\n---"
echo "📊 Generating All Reports and Final Summary..."

# Generate individual reports from the data gathered
python3 "$BASE_DIR/competitor_monitor.py" report
python3 "$BASE_DIR/keyword_rank_tracker.py" report --tier tier1
python3 "$BASE_DIR/content_gap_analyzer.py" report
python3 "$BASE_DIR/local_seo_monitor.py" report
python3 "$BASE_DIR/technical_seo_monitor.py" report

# Consolidate into a single master report
MASTER_REPORT_FILE="$REPORTS_DIR/MASTER-SEO-REPORT-$(date +%Y-%m-%d).md"
{
    echo "# Anderson HAI - MASTER SEO INTELLIGENCE REPORT"
    echo "## Generated: $(date)"
    echo ""
    echo "---"
    echo ""
    cat "$DATA_DIR/competitor-intel-report.md"
    echo ""
    echo "---"
    echo ""
    cat "$DATA_DIR/ranking-report-tier1.md"
    echo ""
    echo "---"
    echo ""
    cat "$DATA_DIR/content-gap-report.md"
    echo ""
    echo "---"
    echo ""
    cat "$DATA_DIR/local-seo-report.md"
    echo ""
    echo "---"
    echo ""
    cat "$DATA_DIR/technical-seo-report.md"
} > "$MASTER_REPORT_FILE"

echo "✅ Master report created at: $MASTER_REPORT_FILE"

# Copy all generated reports to the daily and latest directories
cp $DATA_DIR/*.md "$REPORTS_DIR/"
cp $DATA_DIR/*.json "$REPORTS_DIR/"
cp $REPORTS_DIR/* "$LATEST_REPORTS_DIR/"

echo "✅ All reports copied to $REPORTS_DIR and $LATEST_REPORTS_DIR"

echo "======================================================"
echo "✅ SEO Intelligence Run COMPLETE."
echo "Master report: $LATEST_REPORTS_DIR/$(basename $MASTER_REPORT_FILE)"
echo "======================================================"
