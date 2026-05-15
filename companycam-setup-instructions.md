# CompanyCam Geo SEO Setup Instructions

## Current Status
- ✅ **Hidden geo page created:** `companycam-geo-seo.html`
- ✅ **Meta robots:** `noindex, follow` (hidden from humans, crawlable by search engines)
- ✅ **Rich geo schema:** GPS coordinates for all major service areas
- ✅ **Local SEO benefit:** Geographic documentation for map pack rankings

## What's Live Now
The current page has:
- **Geographic coordinates** for all 9 service cities
- **Rich schema markup** with GPS data for each location
- **Service area documentation** optimized for local SEO
- **Hidden from humans** but discoverable by search engines

## To Upgrade to Real CompanyCam API Photos

### Step 1: Get CompanyCam API Access
1. Log into CompanyCam account
2. Go to: https://app.companycam.com/access_tokens
3. Generate new API token
4. Requires Pro/Premium/Elite plan (API not available on free plan)

### Step 2: Configure the Script
1. Edit `companycam-geo-seo.py`
2. Replace `YOUR_COMPANYCAM_API_TOKEN` with real token
3. Run script: `python3 companycam-geo-seo.py`

### Step 3: What the API Version Does
- **Pulls real photos** from all Anderson HAI projects
- **Extracts GPS coordinates** from actual job site photos
- **Generates updated HTML** with real geotagged content
- **Maintains hidden status** (noindex but crawlable)

### API Version Benefits
- **Real geo data** from actual job sites vs manual coordinates
- **Dynamic updates** as new projects get photographed
- **Richer schema** with actual photo metadata
- **More authentic signals** for Google's local algorithm

## SEO Strategy
The hidden geo page helps with:
- **Local search rankings** (Google sees geographic service proof)
- **Map pack positioning** (geotagged content signals service areas)
- **Geographic relevance** for "near me" searches
- **Service area authority** across NW Georgia cities

## Current Implementation
For now, the manual coordinate version provides:
- ✅ **Immediate SEO benefit** without API setup
- ✅ **Proper schema markup** for all target cities
- ✅ **Hidden from users** as intended
- ✅ **Crawlable by search engines** for ranking signals

## Future CompanyCam Integration
When ready for full API integration:
1. Set up CompanyCam Pro+ plan
2. Generate API token
3. Run the Python script
4. Real geotagged photos replace coordinate documentation
5. Ongoing automation pulls new project photos

**Bottom Line:** Current version gives immediate local SEO benefit. API version adds authenticity when CompanyCam access is available.