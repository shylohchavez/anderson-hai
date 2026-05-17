#!/bin/bash
"""
Anderson HAI Review Automation Setup Script
Sets up directories, permissions, and tests the system
"""

echo "🚀 Setting up Anderson HAI Review Automation System..."

# Make all Python scripts executable
chmod +x anderson_review_automation.py
chmod +x hermes_daily_reviews.py  
chmod +x website_reviews_generator.py

# Create required directories
echo "📁 Creating directories..."
mkdir -p /home/shyloh/.hermes/shared/anderson-website/api-data
mkdir -p /home/shyloh/.hermes/shared/anderson-website/case-studies
mkdir -p /home/shyloh/.openclaw/workspace/anderson-reviews-backup

echo "✅ Directories created"

# Test the system
echo "🧪 Testing Anderson review automation..."
python3 anderson_review_automation.py

if [ $? -eq 0 ]; then
    echo "✅ Main automation test passed!"
    
    # Test website generator
    echo "🌐 Testing website generator..."
    python3 website_reviews_generator.py
    
    if [ $? -eq 0 ]; then
        echo "✅ Website generator test passed!"
        
        echo ""
        echo "🎉 ANDERSON REVIEW AUTOMATION SETUP COMPLETE!"
        echo ""
        echo "📊 System Status:"
        echo "  ✅ Main automation script ready"
        echo "  ✅ Hermes daily sync ready"
        echo "  ✅ Website generator ready"
        echo "  ✅ All directories created"
        echo ""
        echo "📁 Generated Files:"
        echo "  📊 Review data: /home/shyloh/.hermes/shared/anderson-website/api-data/reviews.json"
        echo "  🌐 Website HTML: /home/shyloh/.hermes/shared/anderson-website/reviews-*.html"
        echo "  📝 Case studies: /home/shyloh/.hermes/shared/anderson-website/case-studies/"
        echo "  💾 Backups: /home/shyloh/.openclaw/workspace/anderson-reviews-backup/"
        echo ""
        echo "🔄 To run daily automation via Hermes:"
        echo "  python3 /home/shyloh/.openclaw/workspace/hermes_daily_reviews.py"
        echo ""
        echo "🎯 Next Steps:"
        echo "  1. Review generated files to confirm quality"
        echo "  2. Integrate HTML into website"
        echo "  3. Set up Hermes cron job for daily updates"
        echo "  4. Monitor credit usage on Scrape.do"
        echo ""
        
    else
        echo "❌ Website generator test failed"
        exit 1
    fi
else
    echo "❌ Main automation test failed"
    exit 1
fi