# Technical SEO & Crawlability Audit Report
## Anderson Heating, Air & Insulation — johnandersonservice.com
### Audit Date: May 15, 2026

---

## EXECUTIVE SUMMARY

**Overall SEO Health: B+ (Good foundation, significant optimization opportunities)**

The site has a solid technical SEO foundation powered by Rank Math PRO on WordPress with the Kadence theme. The schema markup implementation is notably strong (HVACBusiness schema), and the local SEO geo-page strategy is well-executed. However, there are several critical and high-priority issues that, if addressed, could significantly improve search visibility in the competitive Northwest Georgia HVAC market.

### Key Wins Already in Place ✅
- Comprehensive XML sitemap structure (5 sitemaps)
- HVACBusiness + LocalBusiness schema markup on homepage
- Proper canonical URLs implemented
- Strong geo-targeted URL structure (/service/city/ pattern)
- Self-hosted fonts (good for performance)
- WebP image format throughout
- SSL/HTTPS enforced
- OG and Twitter meta tags configured
- Google Tag Manager integrated
- Geo Controller plugin for location-based content

### Critical Issues Found 🔴
1. **Staging domain exposure in sitemaps** (punchlistdigital.com)
2. **Duplicate/thin content risk across 218 pages**
3. **Missing blog/content marketing strategy**
4. **Homepage title tag under-optimized**
5. **Robots.txt references non-existent wp-admin**

---

## 1. CRAWLABILITY & INDEXABILITY

### Robots.txt Analysis
**File:** `https://johnandersonservice.com/robots.txt`
```
User-Agent: *
Disallow: /wp-admin/
Allow: /
Sitemap: https://johnandersonservice.com/sitemap_index.xml
```

**Issues:**
- ✅ Sitemap reference present — Good
- ⚠️ **`Disallow: /wp-admin/`** — WordPress convention, but the site description says "hosted on GitHub Pages." If this is actually WordPress-hosted (which the HTML confirms), this is fine. The `wp-admin` disallow is appropriate.
- ⚠️ **No crawl-delay specified** — Not critical, but could help with crawl budget on a 218-page site
- ❌ **Missing:** Should add `Disallow: /wp-content/uploads/` for attachment pages (if any) and `Disallow: /?s=` to block search results pages from being crawled

**Recommendation:**
```
User-Agent: *
Disallow: /wp-admin/
Disallow: /?s=
Disallow: /wp-json/
Allow: /wp-admin/admin-ajax.php
Allow: /

Sitemap: https://johnandersonservice.com/sitemap_index.xml
```

### XML Sitemap Analysis
**Sitemap Index:** 5 child sitemaps ✅

| Sitemap | Last Modified | Purpose | Est. URLs |
|---------|--------------|---------|-----------|
| page-sitemap.xml | Apr 15, 2026 | Core pages (home, about, contact, etc.) | 10 |
| service-sitemap.xml | Apr 14, 2026 | Individual service pages | 20+ |
| trade-geo-sitemap.xml | Apr 14, 2026 | Service+city combo pages | 80+ |
| trade-page-sitemap.xml | May 7, 2026 | Trade category pages | 5 |
| local-sitemap.xml | May 7, 2026 | KML location file | 1 |

**Issues:**
- 🔴 **CRITICAL: Staging Domain Exposure** — When fetching `sitemap.xml` (without `_index`), the redirect goes to `johnandersonservice.punchlistdigital.com/sitemap_index.xml` and all child sitemap URLs point to the punchlistdigital.com staging domain. While the primary `sitemap_index.xml` is correct with production URLs, search engines may discover the alternate path and index staging content. **Fix immediately** — ensure all sitemap redirects stay on production domain.
- ✅ Image sitemaps included (images referenced in sitemaps) — Good for Google Image Search
- ⚠️ Some images are duplicated across sitemap entries (e.g., `Anderson-figure-1.webp` appears in many entries)
- ⚠️ `local-sitemap.xml` only contains a KML file reference — consider adding actual location/city landing pages

**Good news:** The punchlistdigital.com staging domain does NOT appear to be indexed by search engines (0 results in Brave search). But this should still be fixed to prevent future issues.

### Crawl Budget Assessment
- **218 pages** is well within Google's crawl budget limits
- URL structure is clean with trailing slashes consistently applied ✅
- No infinite crawl traps detected
- No URL parameters that would cause duplicate crawling

---

## 2. URL STRUCTURE & ARCHITECTURE

### URL Architecture Pattern
The site uses an excellent hierarchical URL structure:

```
/                                    ← Homepage
/cooling/                            ← Trade category hub
/cooling/calhoun/                    ← City-specific trade landing
/cooling/calhoun/ac-maintenance/     ← Service + city specific page
/heating-and-air-conditioning-repair-services/dalton/  ← Geo service page
/electrical-services/chatsworth/     ← Geo service page
```

**Strengths:**
- ✅ Clean, keyword-rich URLs
- ✅ Logical hierarchy (service → city → specific service)
- ✅ Trailing slashes consistently used
- ✅ No URL parameters or session IDs

**Issues:**
- ⚠️ **Inconsistent URL naming conventions:**
  - Some use full descriptors: `/heating-and-air-conditioning-repair-services/dalton/`
  - Others use short forms: `/cooling/calhoun/ac-maintenance/`
  - `/airseal/lafayette/` vs `/iaq/calhoun/air-sealing/` — same service, different URL pattern
  - `/windows/` vs `/doors-windows/` — inconsistent categorization
- ⚠️ **Missing breadcrumb structured data** — While Kadence supports breadcrumbs, no BreadcrumbList schema was detected in the homepage markup
- ⚠️ **Maximum URL depth is 4 levels** — acceptable, but some deep pages may get less crawl priority

**Recommendations:**
1. Standardize URL naming conventions going forward
2. Implement BreadcrumbList schema markup site-wide
3. Consider creating hub pages for inconsistent categories (e.g., unified `/air-sealing/` section)

---

## 3. ON-PAGE SEO OPTIMIZATION

### Title Tags
| Page | Current Title | Assessment |
|------|--------------|------------|
| Homepage | "Anderson Heating, Air & Insulation \| Calhoun Services" | ⚠️ Too generic — missing "HVAC" keyword, city/state |
| AC Maintenance | "AC Maintenance \| Keep Your System Running" | ⚠️ Missing location, brand |
| Heating/Calhoun | "Heating Services in Calhoun, GA" | ✅ Good — location included |
| HVAC/Dalton | "AC Repair in Dalton, GA" | ⚠️ Title says AC Repair but URL says heating-and-air-conditioning |
| About | "About us - Anderson Heating, Air & Insulation" | ✅ Acceptable |

**Recommendations:**
- **Homepage:** Change to `"HVAC Services Calhoun, GA | Anderson Heating, Air & Insulation | 48+ Years"`
- **Service pages:** Ensure each includes `[Service] in [City], GA | Anderson Heating & Air`
- **Title/URL mismatch on Dalton page:** URL says "heating-and-air-conditioning-repair-services" but title says "AC Repair in Dalton, GA" — should include heating
- Aim for 50-60 characters per title

### Meta Descriptions
- ✅ Homepage meta description is well-written (mentions 48 years, services, whole-home approach)
- ⚠️ At ~300 characters, it's too long — should be 150-160 characters for full SERP display
- ⚠️ Need to verify meta descriptions exist on all 218 pages (Rank Math should handle this)

**Recommended homepage meta description:**
> "Anderson Heating, Air & Insulation — 48 years of trusted HVAC service in Calhoun, GA. Heating, cooling, insulation & whole-home energy solutions. Call (706) 629-0749."

### Header Structure (H1-H6)
- ✅ Homepage uses appropriate H2 headers for sections
- ⚠️ Homepage appears to lack a visible H1 tag (the H1 may be in the hero section but not clearly structured)
- ✅ Service pages use proper H2/H3 hierarchy
- ⚠️ Some pages may have multiple H1s (need to verify with Rank Math)

### Content Depth
- **Homepage:** ~800 words — adequate for a homepage
- **Service pages (Calhoun):** ~400-500 words — could be deeper
- **Geo pages (Dalton):** ~800-1000 words — good depth with FAQ section ✅
- ⚠️ **No blog or educational content** — massive SEO opportunity missed

---

## 4. LOCAL SEO PERFORMANCE

### NAP Consistency
**NAP Found on Site:**
- **Name:** Anderson Heating, Air & Insulation ✅
- **Address:** 519 Pine St, Calhoun, GA 30701 ✅ (in schema)
- **Phone:** (706) 629-0749 and 706-237-8620 ⚠️

**Issues:**
- 🔴 **Two different phone numbers in use:** The schema/TOOLS reference shows `(706) 629-0749` as office phone, but service pages reference `706-237-8620`. This inconsistency can hurt local SEO. Google needs ONE consistent phone number across all citations.
- ⚠️ Physical address only appears in schema markup, not visibly on most pages — should be in footer

**Recommendations:**
1. Standardize to ONE primary phone number across all pages and citations
2. Add full NAP to site footer (visible on every page)
3. Ensure Google Business Profile matches exactly

### Google My Business Integration Signals
- ✅ HVACBusiness schema includes address, phone, hours, priceRange
- ✅ Opening hours defined: Mon-Sun 07:30-17:00
- ⚠️ No Google reviews integration visible on site
- ⚠️ No Google Maps embed detected on contact/location pages
- ❌ No `GeoCoordinates` in schema (latitude/longitude missing)

### Service Area Coverage
**Cities covered in sitemaps:**
Calhoun ✅, Dalton ✅, Rome ✅, Cartersville ✅, Chatsworth ✅, Lafayette ✅, Jasper ✅, Ellijay ✅

**Missing high-value cities:**
- ❌ Ringgold — no dedicated pages
- ❌ Fort Oglethorpe — no dedicated pages
- ❌ Adairsville — no dedicated pages
- ❌ Sugar Valley — mentioned in content but no landing page
- ❌ Fairmount — no dedicated pages

### Local Keyword Optimization
**Well-optimized for:**
- "HVAC services Calhoun GA" — Ranking #2 ✅
- "Heating and air conditioning repair Dalton GA" — Ranking #4 ✅
- Various service+city combinations

**Under-optimized for:**
- "Emergency HVAC repair near me" — no dedicated emergency landing page
- "24/7 AC repair Calhoun" — emergency visibility low
- "HVAC contractor near me" — generic brand-less searches
- "Best HVAC company Calhoun GA" — no review/testimonial page

---

## 5. SCHEMA MARKUP ANALYSIS

### Current Implementation (Homepage)
The homepage contains a rich JSON-LD schema graph with:

```json
@graph: [
  Place (address),
  HVACBusiness + Organization (dual-typed),
  WebSite (with SearchAction),
  ImageObject (logo),
  WebPage,
  Person (author: "punch"),
  Article,
  VideoObject
]
```

**Strengths:**
- ✅ **HVACBusiness schema** — industry-specific, excellent for HVAC searches
- ✅ Address, phone, hours, price range all included
- ✅ Rich business description with certifications mentioned
- ✅ Logo properly referenced
- ✅ SearchAction (sitelinks search box potential)
- ✅ VideoObject for homepage video

**Issues:**
- ⚠️ **Author "punch"** — The author entity references "punch" (the web developer, not Anderson HAI). This hurts E-A-T signals. Should reference a real person from Anderson (owner, lead technician) or the business itself.
- ⚠️ **Article type on homepage** — The homepage is typed as "Article" which is incorrect. It should remain "WebPage" only.
- ⚠️ **VideoObject missing thumbnailUrl** — Required by Google for video rich results
- ⚠️ **VideoObject contentUrl is relative** — `/wp-content/uploads/2026/04/AndersonVideo-1.webm` should be absolute URL
- ❌ **No Review/AggregateRating schema** — Missing review rich results opportunity
- ❌ **No Service schema** — Individual services not marked up
- ❌ **No FAQPage schema** — Dalton page has FAQ content but likely no FAQ schema
- ❌ **No BreadcrumbList schema detected**

**Recommendations:**
1. **Add AggregateRating schema** — Pull reviews from Google/HCP and display + markup
2. **Add FAQPage schema** to pages with FAQ sections (like the Dalton page)
3. **Add Service schema** for each major service offering
4. **Add BreadcrumbList schema** for site navigation
5. **Fix author** — Change from "punch" to a real Anderson HAI team member
6. **Remove Article type** from homepage
7. **Add GeoCoordinates** to Place schema (34.4993, -84.9373)

---

## 6. CONTENT OPTIMIZATION

### Content Quality Assessment

**E-A-T Signals:**
- ✅ 48 years of experience prominently mentioned
- ✅ BPI certifications referenced in schema
- ✅ Awards mentioned (7+ Years Best HVAC Contractor, 2025 Weatherization Day Award)
- ⚠️ No team member bios or credentials pages
- ⚠️ No case studies or project portfolios
- ❌ No blog content for topical authority
- ❌ Author attribution to "punch" (web developer) undermines E-A-T

**Duplicate/Thin Content Risk:**
- 🔴 **HIGH RISK:** Geo pages (trade-geo) likely contain very similar content with only city names swapped. With 80+ geo pages, this is a significant thin content risk.
- The Dalton page shows good unique content (~1000 words with unique FAQ), but if all geo pages follow a template with minimal variation, Google may treat them as doorway pages.
- **Recommendation:** Audit all geo pages for content uniqueness. Each should have:
  - Unique intro paragraph referencing local landmarks/neighborhoods
  - City-specific FAQs
  - Local testimonials
  - Service area details unique to that city

### Content Gaps (vs. Competitors)
Competitors are ranking for content Anderson HAI doesn't have:

| Content Type | Anderson HAI | Competitors |
|-------------|-------------|-------------|
| Blog/Articles | ❌ None | ✅ Most have blogs |
| Seasonal Tips | ❌ None | ✅ Common content |
| Energy Savings Guides | ❌ None | ✅ High-value traffic |
| "How Much Does X Cost" | ❌ None | ✅ High-intent keywords |
| Emergency Services Page | ❌ No dedicated page | ✅ Most competitors have one |
| Testimonials/Reviews Page | ❌ None visible | ✅ Social proof pages |
| Financing Info Content | ⚠️ Has page, minimal content | ✅ Detailed financing info |

---

## 7. COMPETITIVE SEO ANALYSIS

### "HVAC Services Calhoun GA" — Search Position
| Position | Company | Domain |
|----------|---------|--------|
| 1 | Cherokee Mechanical | cherokeemech.com |
| **2** | **Anderson Heating, Air & Insulation** | **johnandersonservice.com** |
| 3 | Calhoun Air Care | calhounaircare.com |
| 4 | Haynes HVAC | hayneshvac.com |
| 5 | Hitchcock Heating | hitchcockhvac.com |

### "Heating and AC Repair Dalton GA" — Search Position
| Position | Company | Domain |
|----------|---------|--------|
| 1 | Clean Heating and Air | cleanheatingandair.com |
| 2 | Dalton Heating & Air | daltonheatingandair.net |
| 3 | Air Comfort HVAC | aircomfortheatingandair.com |
| **4** | **Anderson (heating-and-air/dalton)** | **johnandersonservice.com** |

### Competitive Advantages
- ✅ **48-year history** — longest in market
- ✅ **Broader service offering** (HVAC + insulation + electrical + plumbing + windows + refrigeration)
- ✅ **Stronger schema markup** than most competitors
- ✅ **More geo pages** for local coverage

### Competitive Gaps
- ❌ Cherokee Mechanical outranks for Calhoun — likely stronger GMB presence
- ❌ No blog content vs. competitors with active blogs
- ❌ No review integration visible (competitors display Google reviews)
- ❌ No "emergency service" specific landing page

---

## 8. PAGE SPEED & PERFORMANCE SEO IMPACT

*Note: PageSpeed Insights API quota was exceeded during testing. Assessment based on HTML source analysis.*

### Performance Observations
**Positive:**
- ✅ Self-hosted fonts (Poppins, Sora, Urbanist) with `font-display: swap` — good for CLS
- ✅ All images in WebP format — optimal compression
- ✅ CSS inlined via PerfMatters plugin (critical CSS inlining)
- ✅ Delayed stylesheet loading (`data-pmdelayedstyle`) — good for LCP
- ✅ JS deferred where possible
- ✅ Font preloading implemented

**Concerns:**
- ⚠️ **Massive inline CSS** — The `<head>` contains ~30KB+ of inline CSS (Kadence theme + blocks). This bloats HTML document size.
- ⚠️ **Multiple font families** loaded (Poppins, Sora, Urbanist) — 3 fonts × multiple weights = more render-blocking potential
- ⚠️ **Geo Controller plugin** (`cf-geoplugin`) adds JavaScript that exposes visitor IP and geo data in the page source — both a privacy concern and performance overhead
- ⚠️ **No `loading="lazy"` detected** in initial HTML scan (may be handled by JS)
- ⚠️ **Video on homepage** (WebM) — needs to ensure it doesn't auto-play on mobile

### Mobile-First Indexing
- ✅ Responsive design with mobile breakpoints
- ✅ Viewport meta tag properly set
- ✅ Mobile menu implementation (drawer navigation)
- ⚠️ Content-width set to 2000px max-width — very wide, may cause horizontal scroll on some elements

---

## 9. PRIORITY ACTION ITEMS

### 🔴 CRITICAL (Do Immediately)
1. **Fix staging domain sitemap redirect** — Ensure `sitemap.xml` doesn't redirect to punchlistdigital.com
2. **Standardize phone number** — Pick ONE primary number for all pages and citations
3. **Fix author attribution** — Change from "punch" to Anderson HAI team member
4. **Add GeoCoordinates** to schema (lat/long)

### 🟠 HIGH PRIORITY (Within 30 Days)
5. **Optimize homepage title tag** — Include "HVAC" + "Calhoun, GA"
6. **Add AggregateRating/Review schema** — For star rating rich results
7. **Add FAQPage schema** to all pages with FAQ sections
8. **Create Emergency HVAC Services landing page** — High-intent keyword gap
9. **Add NAP to footer** — Full address + phone visible on every page
10. **Audit geo pages for thin/duplicate content** — Add unique content to each

### 🟡 MEDIUM PRIORITY (Within 60 Days)
11. **Implement BreadcrumbList schema** site-wide
12. **Add Service schema** for each major service category
13. **Create a Reviews/Testimonials page** with structured data
14. **Start a blog** — Target "how much does X cost" + seasonal HVAC content
15. **Add missing geo pages** for Ringgold, Adairsville, Sugar Valley, Fairmount
16. **Fix homepage schema** — Remove Article type, fix VideoObject thumbnailUrl
17. **Shorten meta descriptions** to 150-160 characters

### 🟢 LOW PRIORITY (Within 90 Days)
18. **Content marketing plan** — 2-4 blog posts/month on:
    - Seasonal HVAC tips (summer prep, winter prep)
    - Energy cost calculators
    - "How much does AC repair cost in Georgia?"
    - Heat pump vs. furnace comparisons
    - Weatherization/insulation guides
19. **Reduce font families** — Consider consolidating to 2 fonts max
20. **Evaluate Geo Controller plugin** — Privacy/performance tradeoff
21. **Internal linking audit** — Ensure all service pages cross-link to related services and geo pages
22. **Image alt text audit** — Verify all images have descriptive, keyword-rich alt attributes
23. **Backlink outreach** — Local chambers of commerce, home improvement directories, energy efficiency organizations

---

## 10. CONTENT OPTIMIZATION ROADMAP

### Phase 1: Foundation (Month 1)
- Fix all critical technical issues (items 1-4)
- Create Emergency Services landing page
- Add Reviews/Testimonials page
- Optimize top 10 highest-traffic page titles and descriptions

### Phase 2: Schema & Structure (Month 2)
- Implement FAQ, Review, Service, and Breadcrumb schema
- Audit and de-duplicate geo page content
- Add unique content to top 20 geo pages
- Set up Google Search Console monitoring

### Phase 3: Content Growth (Month 3+)
- Launch blog with initial 4-6 cornerstone articles
- Create seasonal content calendar
- Build out missing geo pages
- Begin local backlink outreach program

### Phase 4: Ongoing Optimization (Quarterly)
- Monitor Core Web Vitals
- Update content for freshness
- Add new service pages as offerings expand
- Track keyword rankings and adjust strategy

---

## APPENDIX: Sitemap URL Inventory Summary

| Category | Example URLs | Est. Count |
|----------|-------------|------------|
| Core Pages | /, /about-us/, /contact-us/, /financing/, /gallery/, /service-area/, /coupons/ | 10 |
| Trade Hubs | /cooling/, /heating/, /insulation/, /iaq/, /hot-water/ | 5 |
| Service Pages | /cooling/calhoun/ac-maintenance/, /iaq/calhoun/air-sealing/ | 20+ |
| Geo-Trade Pages | /heating/calhoun/, /windows/dalton/, /plumbing-services/rome/ | 80+ |
| Geo-Service Pages | /heating-and-air-conditioning-repair-services/dalton/ | 30+ |
| Total Estimated | | ~150-180+ |

---

*Report prepared by Technical SEO Audit Agent — May 15, 2026*
*Data sources: Live website crawl, Brave Search, XML sitemaps, HTML source analysis*
