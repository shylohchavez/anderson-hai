#!/bin/bash
# Anderson HAI - Post-Deploy Site Validator
# Run after every git push to catch broken pages/links
# Usage: bash validate-site.sh

SITE_DIR="$(dirname "$0")"
cd "$SITE_DIR"

echo "=== ANDERSON HAI SITE VALIDATOR ==="
echo "Date: $(date)"
echo ""

ERRORS=0

# 1. Check all HTML files have content in body
echo "--- CHECK 1: Empty body tags ---"
for f in *.html; do
    BODY=$(sed -n '/<body/,/<\/body>/p' "$f" | wc -c)
    if [ "$BODY" -lt 200 ]; then
        echo "FAIL: $f has empty body ($BODY bytes)"
        ERRORS=$((ERRORS+1))
    fi
done
echo "  Done"

# 2. Check all footers have links
echo "--- CHECK 2: Footer links ---"
for f in *.html; do
    COUNT=$(sed -n '/<footer/,/<\/footer>/p' "$f" 2>/dev/null | grep -c 'href=')
    if [ "$COUNT" -lt 5 ]; then
        echo "FAIL: $f footer has only $COUNT links (need 5+)"
        ERRORS=$((ERRORS+1))
    fi
done
echo "  Done"

# 3. Check all internal links point to existing files
echo "--- CHECK 3: Broken internal links ---"
for f in *.html; do
    grep -oP 'href="([^"#]*\.html)"' "$f" | sed 's/href="//;s/"//' | while read link; do
        if [ ! -f "$link" ]; then
            echo "FAIL: $f links to $link (file missing)"
            ERRORS=$((ERRORS+1))
        fi
    done
done
echo "  Done"

# 4. Check viewport meta on all pages
echo "--- CHECK 4: Viewport meta ---"
for f in *.html; do
    if ! grep -q 'viewport' "$f"; then
        echo "FAIL: $f missing viewport meta"
        ERRORS=$((ERRORS+1))
    fi
done
echo "  Done"

# 5. Check phone number present
echo "--- CHECK 5: Phone number ---"
for f in *.html; do
    if ! grep -q '706.*629.*0749\|7066290749' "$f"; then
        echo "WARN: $f missing phone number"
    fi
done
echo "  Done"

echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo "ALL CHECKS PASSED"
else
    echo "FAILED: $ERRORS issues found"
fi
