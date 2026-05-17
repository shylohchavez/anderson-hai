# Anderson HAI — Social Media, SEO & Digital Presence Optimization Report
**Audit Date:** May 15, 2026  
**Website:** johnandersonservice.com  
**SEO Plugin:** Rank Math PRO  
**Theme:** Kadence  

---

## 📊 EXECUTIVE SUMMARY

The website has a **solid technical foundation** (Rank Math PRO, proper schema, OG tags present). However, it is **significantly underutilizing the John Anderson founder story and Gypsy mascot** across all digital touchpoints. The current SEO and social meta data reads like a generic HVAC company — the authentic brand story that differentiates Anderson HAI is almost entirely absent from machine-readable metadata.

**Biggest Gaps:**
1. ❌ **No mention of "John Anderson" as founder** in any title tag, meta description, or OG tag
2. ❌ **No mention of Gypsy or "The Paws-itive Choice"** in any metadata
3. ❌ **"Founded 1978" / "Since 1978"** not in title tags or meta descriptions
4. ❌ **No `founder` or `Person` schema** linking John Anderson to the business
5. ⚠️ **OG image is just the logo** (446×202px) — too small for ideal social previews (1200×630 recommended)
6. ⚠️ **Article author shows "punch"** (webmaster username) instead of the business or John Anderson
7. ⚠️ **Cooling page links to Reunion Marketing's Facebook** as article:author — not Anderson's

---

## 🔍 PAGE-BY-PAGE AUDIT

### Homepage (/)
| Element | Current | Grade |
|---------|---------|-------|
| `<title>` | `Anderson Heating, Air & Insulation \| Calhoun Services` | B- |
| `meta description` | Generic 48-year service description | C+ |
| `og:title` | Same as title | B- |
| `og:description` | Same as meta description | C+ |
| `og:image` | Anderson-logo.webp (446×202) | C |
| `twitter:card` | summary_large_image | ✅ |
| `twitter:data1` | "punch" (author) | ❌ |
| Schema: HVACBusiness | Present with address, hours, phone | ✅ |
| Schema: founder | **MISSING** | ❌ |
| Schema: Person (John Anderson) | **MISSING** | ❌ |
| Schema: knowsAbout | **MISSING** | ❌ |

### Cooling (/cooling/)
| Element | Current | Grade |
|---------|---------|-------|
| `<title>` | `Cooling Services \| Anderson Heating & Air` | B |
| `meta description` | "AC repair, installation...Call 706-237-8620" | B |
| `og:title` | Same | B |
| `article:author` | `https://www.facebook.com/reunionmarketing/` ← **WRONG** | ❌ |
| `og:image` | Same logo (446×202) | C |

### Insulation (/insulation/)
| Element | Current | Grade |
|---------|---------|-------|
| `<title>` | `Insulation Services \| Anderson Heating & Air` | B |
| `meta description` | "Home insulation...Call 706-237-8620" | B |
| `og:image` | Same logo | C |

### IAQ (/iaq/)
| Element | Current | Grade |
|---------|---------|-------|
| `<title>` | `Indoor Air Quality Services \| Anderson` | B- |
| `meta description` | "Air duct cleaning...Call 706-237-8620" | B |
| `og:image` | Same logo | C |

---

## 🎯 OPTIMIZATION RECOMMENDATIONS

### 1. TITLE TAG OPTIMIZATION (Rank Math → Edit Snippet)

**All title tags should integrate brand identity. Recommendations:**

| Page | Current Title | Optimized Title |
|------|---------------|-----------------|
| **Homepage** | `Anderson Heating, Air & Insulation \| Calhoun Services` | `Anderson Heating, Air & Insulation \| Calhoun, GA Since 1978 — The Paws-itive Choice 🐾` |
| **Cooling** | `Cooling Services \| Anderson Heating & Air` | `AC Repair & Cooling Services \| Anderson HAI, Calhoun GA — Since 1978` |
| **Insulation** | `Insulation Services \| Anderson Heating & Air` | `Insulation & Air Sealing \| Anderson HAI — 48 Years of Expertise in Calhoun, GA` |
| **IAQ** | `Indoor Air Quality Services \| Anderson` | `Indoor Air Quality Services \| Anderson HAI, Calhoun — Clean Air Experts Since 1978` |
| **Hot Water** | (check current) | `Water Heater Services \| Anderson HAI — Trusted in Calhoun Since 1978` |

**Key principles:**
- Keep under 60 characters for Google display
- Include "Calhoun" or "Calhoun, GA" for local SEO
- Include "Since 1978" or "48 Years" for trust signal
- Consider "🐾" emoji in homepage title (stands out in SERPs)

---

### 2. META DESCRIPTION OPTIMIZATION

| Page | Optimized Meta Description |
|------|---------------------------|
| **Homepage** | `Founded by John Anderson in 1978, Anderson Heating, Air & Insulation has served Calhoun, GA for 48 years. HVAC, insulation, air quality & more. The Paws-itive Choice! 🐾 Call (706) 629-0749` |
| **Cooling** | `Expert AC repair, installation & maintenance from Anderson HAI — founded by John Anderson in 1978. Serving Calhoun & North Georgia for 48 years. Call (706) 629-0749` |
| **Insulation** | `Professional insulation, air sealing & crawlspace encapsulation by Anderson HAI. Founded by John Anderson in 1978, serving Calhoun, GA. The Paws-itive Choice! (706) 629-0749` |
| **IAQ** | `Breathe easier with Anderson HAI's air quality services — duct cleaning, filtration & humidity control. John Anderson's team has served Calhoun since 1978. Call (706) 629-0749` |

**Key principles:**
- Keep 150-160 characters
- Include "John Anderson" and/or "founded" in at least homepage + about page
- Include "The Paws-itive Choice" on key pages
- Include primary phone number (local SEO signal)
- Note: Use (706) 629-0749 (office) consistently, not the 706-237-8620 currently on service pages

---

### 3. OPEN GRAPH (OG) IMPROVEMENTS

#### A. OG Image Upgrade (HIGH PRIORITY)
**Current:** `Anderson-logo.webp` at 446×202px — too small, logo-only, no context

**Recommendation:** Create a dedicated OG social sharing image:
- **Size:** 1200×630px (Facebook/LinkedIn optimal)
- **Design:** Purple background with John Anderson & Gypsy logo prominently centered, tagline "The Paws-itive Choice" below, "Serving Calhoun, GA Since 1978" at bottom, phone number
- **Filename:** `anderson-hai-social-preview.jpg` (use JPG, not WebP, for maximum social media compatibility)
- Upload to WordPress Media Library
- Set as default OG image in **Rank Math → General Settings → Social Meta → Default Social Share Image**

#### B. OG Tag Updates (via Rank Math per-page settings)

**Homepage:**
```
og:title = "Anderson Heating, Air & Insulation — Calhoun's Trusted HVAC Experts Since 1978"
og:description = "Founded by John Anderson in 1978. HVAC, insulation, air quality & energy solutions for North Georgia. The Paws-itive Choice! 🐾"
```

#### C. Fix article:author
- **Current:** Points to `reunionmarketing` (web agency) on cooling page
- **Fix:** In Rank Math → Social Meta, set proper Facebook author URL to Anderson HAI's Facebook page, or remove it
- **Fix:** Change the WordPress display name for user "punch" to "Anderson HAI" or "Anderson Heating, Air & Insulation" (Settings → Users → punch → Display Name)

---

### 4. SCHEMA MARKUP ENHANCEMENTS (Rank Math Schema)

#### A. Add Founder Schema (CRITICAL)
The current schema has `HVACBusiness` with good details but **no founder/owner information**. 

**Add to homepage schema (Rank Math → Schema → Edit Schema):**

```json
{
  "@type": "HVACBusiness",
  "founder": {
    "@type": "Person",
    "name": "John Anderson",
    "jobTitle": "Founder",
    "description": "John Anderson founded Anderson Heating, Air & Insulation in 1978 in Calhoun, Georgia. With over 48 years of HVAC expertise, he built a family business trusted by North Georgia homeowners."
  },
  "foundingDate": "1978",
  "slogan": "The Paws-itive Choice",
  "award": [
    "7+ Years Best HVAC Contractor (Calhoun Magazine)",
    "2025 Weatherization Day Award"
  ],
  "knowsAbout": [
    "HVAC Installation and Repair",
    "Home Insulation",
    "Indoor Air Quality",
    "Energy Audits",
    "Weatherization",
    "Geothermal Systems",
    "Crawlspace Encapsulation"
  ],
  "numberOfEmployees": {
    "@type": "QuantitativeValue",
    "value": "20+"
  }
}
```

#### B. Add `foundingDate` to existing Organization schema
**Current:** No `foundingDate` field  
**Add:** `"foundingDate": "1978"`

#### C. Add `slogan` field
**Add:** `"slogan": "The Paws-itive Choice"`

#### D. Add `award` array  
Shows in Knowledge Panels and rich results

#### E. Add `sameAs` for Social Profiles
```json
"sameAs": [
  "https://www.facebook.com/andersonheatingair/",
  "https://www.google.com/maps/place/Anderson+Heating+Air+Insulation/..."
]
```
*(Add actual URLs for Facebook, Google Business Profile, any other profiles)*

---

### 5. SOCIAL PREVIEW IMAGE STRATEGY

**Problem:** Every page shares the same small 446×202 logo. When someone shares any Anderson HAI page on Facebook, LinkedIn, or Twitter, the preview looks small and generic.

**Solution — Create page-specific OG images:**

| Page | Recommended OG Image Content |
|------|------------------------------|
| Homepage | John & Gypsy logo + "The Paws-itive Choice" + "Since 1978" + Purple branding |
| Cooling | HVAC unit photo + Anderson logo overlay + "Expert Cooling Since 1978" |
| Insulation | Insulation work photo + Anderson logo + "Home Comfort Experts" |
| IAQ | Clean air themed + Anderson logo + "Breathe Easy" |
| Hot Water | Water heater photo + Anderson logo + "Reliable Hot Water" |

**Quick win:** At minimum, create ONE universal social card (1200×630) with the John & Gypsy logo prominently displayed and set it as default. Per-page images are a bonus.

---

### 6. LOCAL SEO ENHANCEMENTS

#### A. Google Business Profile Optimization
Ensure the GBP listing includes:
- ✅ "Founded in 1978 by John Anderson" in the business description
- ✅ "The Paws-itive Choice" in the short description
- ✅ Logo with John & Gypsy as profile photo
- ✅ All service categories listed
- ✅ Regular posts mentioning John Anderson's expertise

#### B. NAP Consistency
- **Current phone on service pages:** 706-237-8620
- **Office phone in TOOLS.md:** (706) 629-0749  
- ⚠️ **Verify these are consistent across GBP, website, and directories**

#### C. LocalBusiness Schema Breadcrumbs
Each service page should have location-specific URLs like:
- `/cooling/calhoun/` (already exists for some services)
- Schema on these pages should reference the parent HVACBusiness

---

### 7. SEARCH RESULT APPEARANCE OPTIMIZATION

#### A. How Homepage Currently Appears in Google:
```
Anderson Heating, Air & Insulation | Calhoun Services
https://johnandersonservice.com
For over 48 years, Anderson Heating, Air & Insulation has delivered 
trusted HVAC services in Calhoun, Georgia...
```

#### B. How Homepage SHOULD Appear:
```
Anderson Heating, Air & Insulation — Since 1978 | Calhoun, GA 🐾
https://johnandersonservice.com
Founded by John Anderson in 1978, Anderson HAI has served Calhoun, 
GA for 48 years. HVAC, insulation, air quality & more. The Paws-itive 
Choice! Call (706) 629-0749
```

#### C. Rich Snippet Opportunities
With proper schema, Google may show:
- ⭐ Star ratings (if review schema is added)
- 📍 Address in search results
- 📞 Phone number click-to-call
- 🏢 "Founded: 1978" in Knowledge Panel
- 👤 "Founder: John Anderson" in Knowledge Panel
- 🏆 Awards in Knowledge Panel

---

### 8. CONTENT DISCOVERABILITY IMPROVEMENTS

#### A. Image Alt Tags
**Current:** Unknown (would need to audit individual images)  
**Recommendation:** All images of team, equipment, or work should include:
- "Anderson Heating Air Insulation team" or "John Anderson HVAC expert"
- Service-specific keywords
- Location: "Calhoun GA"
- Example: `alt="Anderson HAI technician installing insulation in Calhoun, GA home"`

#### B. Internal Linking with Anchor Text
- Link to homepage using anchor text "Anderson Heating, Air & Insulation - founded by John Anderson"
- Cross-link service pages with descriptive anchor text
- Add "About John Anderson" or "Our Story" page if one doesn't exist

#### C. Blog/Content Strategy for Brand Recognition
- Create an "Our Story" or "About" page telling John Anderson's founding story with Gypsy
- Blog posts featuring John Anderson's expertise, awards, community involvement
- "Meet the Team" content with photos and bios

---

## 📋 IMPLEMENTATION PRIORITY LIST

### 🔴 HIGH PRIORITY (Do This Week)
1. **Update homepage title tag** in Rank Math to include "Since 1978"
2. **Update homepage meta description** to mention John Anderson and The Paws-itive Choice
3. **Add `foundingDate: 1978` and `founder` Person schema** to homepage via Rank Math
4. **Create 1200×630 social preview image** with John & Gypsy branding
5. **Set new image as default OG image** in Rank Math settings
6. **Fix article:author** — change from Reunion Marketing to Anderson HAI
7. **Change WordPress user "punch" display name** to "Anderson HAI"

### 🟡 MEDIUM PRIORITY (This Month)
8. Update all service page title tags with "Anderson HAI" + "Since 1978"
9. Update all service page meta descriptions with founder mention
10. Add `sameAs` social profile links to schema
11. Add `award` array to schema
12. Verify phone number consistency (629-0749 vs 237-8620)
13. Create "Our Story" / About page for John Anderson + Gypsy

### 🟢 NICE TO HAVE (Next Month)
14. Create page-specific OG images for each service
15. Audit all image alt tags for brand keywords
16. Add FAQ schema to service pages
17. Add review/rating schema if reviews are available
18. Create blog content around John Anderson's expertise and awards

---

## 🛠️ WHERE TO MAKE THESE CHANGES

All changes are made in **WordPress Admin → Rank Math**:

| Change | Location |
|--------|----------|
| Title tags | Edit page → Rank Math SEO box → Edit Snippet |
| Meta descriptions | Edit page → Rank Math SEO box → Edit Snippet |
| OG image (default) | Rank Math → General Settings → Social Meta |
| OG image (per page) | Edit page → Rank Math → Social tab |
| Schema markup | Edit page → Rank Math → Schema tab |
| Global schema | Rank Math → Titles & Meta → Local SEO |
| Author display name | Users → punch → Edit → Display Name |
| article:author | Rank Math → Social Meta → Facebook section |

---

## 📊 EXPECTED IMPACT

| Metric | Current | Expected After Optimization |
|--------|---------|----------------------------|
| Social share click-through | Low (small logo, generic text) | **+40-60%** (branded image, compelling copy) |
| Google CTR for branded searches | Average | **+20-30%** (founder story, trust signals) |
| Knowledge Panel likelihood | Low | **High** (with proper Person + Organization schema) |
| Brand recognition in shares | Generic HVAC company | **"Oh, that's the dog company!"** |
| Local SEO ranking signals | Good | **Stronger** (founder authority, awards, consistent NAP) |

---

*Report prepared for Anderson Heating, Air & Insulation — johnandersonservice.com*
