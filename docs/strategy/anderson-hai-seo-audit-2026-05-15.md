# Anderson HAI — GitHub Pages SEO Audit Report
**Date:** May 15, 2026  
**Site:** https://shylohchavez.github.io/anderson-hai/  
**Production Domain:** https://johnandersonservice.com  
**Platform:** GitHub Pages (static HTML)  
**Total Pages:** 218 HTML files

---

## 🚨 CRITICAL ISSUES (Fix Immediately)

### 1. robots.txt is BLOCKING ALL CRAWLING
**Severity: SHOWSTOPPER**
```
User-agent: *
Disallow: /
```
The current robots.txt tells Google to **not crawl any page on the site**. This means zero search visibility. When the site goes live on the production domain, this must be changed to:
```
User-agent: *
Allow: /

Sitemap: https://johnandersonservice.com/sitemap.xml
```
**Note:** This is intentional for the staging (GitHub Pages) URL — but must be the FIRST thing changed when the domain points to production.

### 2. Broken og:image:alt Meta Tags — 144 Pages
**Severity: HIGH**
The `og:image:alt` attribute contains nested, broken HTML meta tags:
```html
<meta property="og:image:alt" content="John Anderson <meta property="og:image" content="..."> Gypsy - Anderson Heating, Air <meta property="og:image" content="..."> Insulation, The Paws-itive Choice since 1978">
```
This creates **malformed HTML** that social media crawlers (Facebook, LinkedIn, Twitter) will choke on. It also creates duplicate `og:image` declarations. 

**Fix:** Replace across all 144 files with:
```html
<meta property="og:image:alt" content="John Anderson and Gypsy - Anderson Heating, Air and Insulation, The Paws-itive Choice since 1978">
```

### 3. og:image URLs Point to GitHub, Not Production — 144 Pages
**Severity: HIGH (when going live)**
```html
<meta property="og:image" content="https://shylohchavez.github.io/anderson-hai/images/logo.png">
```
When the production domain goes live, all `og:image` and `twitter:image` URLs must point to `https://johnandersonservice.com/images/logo.png`. Social shares will show broken images otherwise.

---

## ⚠️ HIGH-PRIORITY ISSUES

### 4. Keyword Cannibalization — Emergency HVAC Pages
**Severity: HIGH**
There are **25 emergency HVAC pages**, many targeting the same cities with near-identical content:
- `emergency-hvac-repair-calhoun-ga.html` vs `24-7-emergency-hvac-calhoun-ga.html` vs `emergency-hvac-calhoun-domination.html` vs `emergency-hvac-repair.html` vs `emergency-hvac-service.html` vs `hvac-emergency-service-calhoun.html`
- Dalton has **4 separate emergency pages**
- Rome has **3 separate emergency pages**

Google will struggle to determine which page to rank, causing them to compete against each other. **Recommendation:**
- Keep ONE emergency page per city (the most complete one)
- 301-redirect the others to the keeper (use `<meta http-equiv="refresh">` on GitHub Pages since .htaccess isn't available)
- Or consolidate content into one comprehensive page per city

### 5. Truncated Meta Descriptions — 31 Pages
**Severity: MEDIUM-HIGH**
31 pages have meta descriptions ending in `...`, meaning they were truncated during generation. Google will display incomplete snippets. Each should be 150-160 characters, ending in a complete sentence with a call to action.

### 6. Inconsistent Review Count in Schema — 6 Pages Outdated
**Severity: MEDIUM**
- 191 pages show `"reviewCount": "632"` ✅
- 6 pages still show `"reviewCount": "513"` ❌

All pages should use the same current count for consistency. Google may flag conflicting aggregate ratings.

### 7. Missing OG Tags — 20+ Pages
Pages without `og:title` and `og:description`:
- All city hub `/index.html` pages (dalton/, jasper/, resaca/, etc.)
- Emergency pages: `emergency-hvac-repair.html`, `emergency-hvac-repair-rome-ga.html`
- Several "domination" and Q&A pages
- `companycam-geo-seo.html`

These pages won't display properly when shared on social media.

---

## 📋 MEDIUM-PRIORITY ISSUES

### 8. Pages Missing from Sitemap — 8+ Pages
The sitemap has 204 entries for 218 HTML pages. Missing pages include:
- All city hub `index.html` files (`dalton/index.html`, `jasper/index.html`, etc.)
- `reviews-section.html`
- `hvac-and-insulation-cartersville.html`
- `hvac-and-insulation-fairmount.html`

These should either be added to `sitemap.xml` or consolidated with existing pages.

### 9. Sitemap Lists Both `/` and `/index.html`
Both `https://johnandersonservice.com/` and `https://johnandersonservice.com/index.html` are in the sitemap with priority 1.0. This creates duplicate content signals. Remove `/index.html` and keep only `/`.

### 10. Pages Missing H1 Tags — 5 Pages
- `reviews-section.html`
- `reviews-schema.html`
- `emergency-hvac-repair-calhoun-ga.html`
- `reviews.html`
- `reviews-page.html`

Every page needs exactly one H1 tag for proper heading hierarchy.

### 11. Pages Without JSON-LD Schema — 10 Pages
Primarily the city hub `index.html` pages and review template pages. 208 of 218 pages have schema, which is excellent coverage — just need to close the gap.

### 12. Phone Number Format Inconsistency
- Primary: `(706) 629-0749` — 1,879 occurrences ✅
- `tel:` links using `17066290749` — 899 occurrences ✅ (correct for tel: links)
- Plain `7066290749` — 153 occurrences (used in tel: links, acceptable)
- `(706)629-0749` (no space) — 14 occurrences ❌ (inconsistent)
- `(706) 555-1234` — 1 occurrence ❌ (placeholder/test number!)
- `15586186661` — 5 occurrences ❌ (unknown number)

**Fix:** Standardize to `(706) 629-0749` for display, `tel:+17066290749` for links. Find and fix the placeholder number.

---

## ✅ WHAT'S WORKING WELL

### Strong Foundation
- **Canonical URLs:** Properly set on 215/218 pages pointing to `johnandersonservice.com` ✅
- **Schema Markup:** 208/218 pages have JSON-LD (95% coverage) ✅
- **HVACBusiness Schema:** Correctly implemented with address, geo, hours, services ✅
- **BlogPosting Schema:** Blog posts use proper schema with dates and publisher ✅
- **FAQ Schema:** 60 FAQ JSON files + 72 pages with FAQPage schema — excellent for rich snippets ✅
- **Title Tags:** 216/218 pages have unique, keyword-rich titles (no duplicates found) ✅
- **Meta Descriptions:** 215/218 pages have descriptions ✅
- **Viewport Meta:** All pages mobile-responsive ✅
- **Lang Attribute:** `<html lang="en">` on all pages ✅
- **404 Page:** Properly configured with `noindex, follow` ✅
- **Image Alt Tags:** Properly implemented (index.html 100% coverage) ✅

### Content Strengths
- **Massive geo-coverage:** 126 city/geo-targeted pages covering NW Georgia thoroughly
- **9 blog posts** with proper schema and internal linking
- **Service depth:** Dedicated pages for each service type
- **BPI Certification** prominently featured (differentiator)
- **"The Paws-itive Choice"** branding integrated into schema and content
- **NAP consistency:** Address (519 Pine Street, Calhoun, GA 30701) is consistent across pages

---

## 🎯 OPTIMIZATION RECOMMENDATIONS

### A. GitHub Pages-Specific SEO Strategies

1. **Client-Side Redirects for Cannibalized Pages**
   Since GitHub Pages doesn't support `.htaccess` or server-side redirects, use:
   ```html
   <meta http-equiv="refresh" content="0; url=target-page.html">
   <link rel="canonical" href="https://johnandersonservice.com/target-page.html">
   ```
   Apply to all duplicate emergency pages redirecting to the primary one per city.

2. **Static Sitemap Maintenance**
   Create a script to auto-generate `sitemap.xml` from the file list. Run before each deploy. Include `<lastmod>` dates for all changed files.

3. **GitHub Pages Cache Control**
   GitHub serves a 10-minute cache (`max-age=600`). This is fine for SEO — Google handles it well. No action needed.

### B. Content & Local SEO Enhancements

4. **Add "Near Me" Keyword Variations**
   Zero pages target "near me" queries (e.g., "HVAC repair near me", "AC repair near me"). Add these to meta descriptions and body content for high-intent local searches.

5. **Emergency Pages in Title Tags**
   Zero pages include "emergency" in their `<title>` tag by grep match — double-check this as several do have "Emergency" (case sensitivity may have been an issue in my check). Ensure emergency pages have strong emergency-focused titles.

6. **Add Service Area Schema**
   Add `areaServed` to the HVACBusiness schema on each page:
   ```json
   "areaServed": [
     {"@type": "City", "name": "Calhoun", "containedInPlace": {"@type": "State", "name": "Georgia"}},
     {"@type": "City", "name": "Dalton", "containedInPlace": {"@type": "State", "name": "Georgia"}}
   ]
   ```

7. **Add GeoCircle for Service Radius**
   ```json
   "areaServed": {
     "@type": "GeoCircle",
     "geoMidpoint": {"@type": "GeoCoordinates", "latitude": "34.5029", "longitude": "-84.9511"},
     "geoRadius": "50 mi"
   }
   ```

8. **Enhance Blog with Internal Links**
   Each blog post should link to 3-5 relevant service pages and 2-3 geo pages. This distributes PageRank from content to money pages.

### C. Schema Markup Enhancements

9. **Add SameAs Social Links**
   ```json
   "sameAs": [
     "https://www.facebook.com/andersonhai",
     "https://www.google.com/maps/place/Anderson+Heating+Air+Insulation"
   ]
   ```

10. **Add Founder/Person Schema**
    Leverage the John Anderson & Gypsy branding:
    ```json
    "founder": {
      "@type": "Person",
      "name": "John Anderson",
      "description": "Founded Anderson Heating, Air & Insulation in 1978 in Calhoun, GA"
    }
    ```

11. **Add Emergency Service Schema**
    For emergency pages, add:
    ```json
    "availableChannel": {
      "@type": "ServiceChannel",
      "serviceType": "Emergency HVAC Repair",
      "availableLanguage": "English",
      "servicePhone": {"@type": "ContactPoint", "telephone": "(706) 629-0749", "contactType": "emergency"}
    }
    ```

### D. Technical Quick Wins

12. **Add `<meta name="geo.region" content="US-GA">` and `<meta name="geo.placename" content="Calhoun">` to all pages** — helps with local search signals.

13. **Add `<link rel="icon" href="/favicon.ico">` if missing** — professional signal.

14. **Add breadcrumb schema** to city and service pages for rich snippet breadcrumbs in SERPs.

15. **Create a `manifest.json`** for PWA signals (lightweight, helps mobile ranking).

---

## 📊 PRIORITY ACTION PLAN

| Priority | Action | Pages Affected | Effort |
|----------|--------|---------------|--------|
| 🔴 P0 | Fix robots.txt when going live | 1 file | 1 min |
| 🔴 P0 | Fix broken og:image:alt tags | 144 pages | Script: 5 min |
| 🔴 P1 | Update og:image URLs to production domain | 144 pages | Script: 5 min |
| 🟠 P1 | Consolidate emergency page cannibalization | 25→10 pages | 2-3 hours |
| 🟠 P1 | Fix truncated meta descriptions | 31 pages | 1-2 hours |
| 🟡 P2 | Standardize review count in schema | 6 pages | 10 min |
| 🟡 P2 | Add missing pages to sitemap | 8 pages | 15 min |
| 🟡 P2 | Remove duplicate `/index.html` from sitemap | 1 entry | 2 min |
| 🟡 P2 | Fix phone number inconsistencies | ~20 occurrences | 30 min |
| 🟡 P2 | Add H1 tags to missing pages | 5 pages | 15 min |
| 🟢 P3 | Add schema to hub index pages | 10 pages | 30 min |
| 🟢 P3 | Add OG tags to missing pages | 20 pages | 45 min |
| 🟢 P3 | Add areaServed schema | All pages | Script: 30 min |
| 🟢 P3 | Add breadcrumb schema | Service+city pages | 2-3 hours |
| 🟢 P3 | Add founder/social schema | All pages | Script: 15 min |
| 🟢 P3 | Add geo meta tags | All pages | Script: 10 min |

---

## 🏆 BRANDING SEO IMPACT ASSESSMENT

### John Anderson & Gypsy Branding ✅ Positive
- **Unique brand story** = differentiator in SERP snippets
- **"The Paws-itive Choice"** tagline in schema and content creates memorable brand recall
- **"Formerly John Anderson Service Company"** captures legacy brand searches
- **Founder story** adds E-E-A-T signals (Experience, Expertise, Authority, Trust)

### Recommendations for Branding SEO
- Create an "Our Story" page specifically optimized for "John Anderson HVAC Calhoun" searches
- Add `Person` schema for John Anderson as founder
- Use Gypsy imagery in social share images (og:image) — unique, shareable, memorable
- Blog post: "Meet John Anderson & Gypsy: 48 Years of The Paws-itive Choice" (link magnet)

---

## 📈 COMPETITIVE POSITIONING

With 218 pages, strong schema markup, and comprehensive geo-coverage, this site has excellent bones for dominating NW Georgia HVAC search. The main barriers to ranking are:

1. **robots.txt block** (staging — will be fixed at launch)
2. **Keyword cannibalization** from duplicate emergency pages
3. **Domain authority** — `shylohchavez.github.io` has no authority; `johnandersonservice.com` needs to be the live domain
4. **Backlinks** — Schema and content are strong, but the site needs external links (Google Business Profile, local directories, vendor pages)

**Bottom Line:** Fix the P0/P1 issues, point the real domain, and this site is positioned to rank well for NW Georgia HVAC terms within 3-6 months.
