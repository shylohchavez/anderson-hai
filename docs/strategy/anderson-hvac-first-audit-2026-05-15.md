# Anderson HAI Website HVAC-First Categorization Audit
## Date: May 15, 2026

---

## OVERALL HVAC-FIRST COMPLIANCE SCORE: 6.5/10 ⚠️

**The site does many things right but has a systemic schema problem and several content signals that could confuse Google's categorization engine.**

---

## 🔴 CRITICAL ISSUES (Fix Immediately)

### 1. Schema Markup: `InsulationContractor` Type on 124 Pages
**Risk Level: HIGH — This is the #1 categorization threat**

124 out of 202 HTML pages use this triple @type:
```json
"@type": ["LocalBusiness", "HVACBusiness", "InsulationContractor"]
```

**Why this is dangerous:**
- Google treats multi-type arrays as equal-weight signals. By declaring `InsulationContractor` alongside `HVACBusiness`, you're literally telling Google "we are equally an insulation contractor."
- The `LocalBusiness` wrapper further dilutes the HVAC signal — Google may prioritize the more generic type.
- Google's Knowledge Graph can pick ANY of the declared types for categorization. You're giving it 3 choices when you want it to pick just 1.

**Fix:** Change ALL pages to:
```json
"@type": "HVACBusiness"
```
Remove `LocalBusiness` and `InsulationContractor` from the `@type` array on every page.

**Pages affected:** 124 pages (see appendix for full list)

### 2. `anderson-schema.jsonld` Contains Separate `InsulationContractor` Entity
**Risk Level: HIGH**

The standalone schema file at `anderson-schema.jsonld` contains:
```json
{
  "@type": "InsulationContractor",
  "@id": "https://johnandersonservice.com/#insulation",
  "parentOrganization": {"@id": "https://johnandersonservice.com/#organization"},
  "serviceType": "Home Insulation and Air Sealing"
}
```

Plus a separate `LocalBusiness` entity with `additionalType: HVACBusiness` — this is backwards. The primary type should BE `HVACBusiness`, not an additional type on `LocalBusiness`.

**Fix:** Remove the `InsulationContractor` entity entirely. Remove the `LocalBusiness` entity. Keep only the `HVACBusiness` entity.

### 3. `emergency-service-schema.jsonld` Uses `LocalBusiness` as Provider Type
**Risk Level: MEDIUM-HIGH**

```json
"provider": {
  "@type": "LocalBusiness",
  "name": "Anderson Heating, Air & Insulation"
}
```

**Fix:** Change to `"@type": "HVACBusiness"`

### 4. Review Count Inconsistency: 632 vs 513
**Risk Level: MEDIUM**

- Schema files (`anderson-schema.jsonld`, `authority-bridge-schema.json`) show `"reviewCount": "632"`
- On-page content shows "513+ Google Reviews"
- This mismatch could trigger Google's spam detection for review markup

**Fix:** Align all `reviewCount` values to the actual current Google review count.

---

## 🟠 HIGH-PRIORITY ISSUES

### 5. Homepage Meta Keywords Include "insulation contractor calhoun ga"
**Risk Level: MEDIUM**

Line 9 of `index.html`:
```html
<meta name="keywords" content="...insulation contractor calhoun ga...">
```

While meta keywords have minimal SEO weight in 2026, this still sends a categorization signal.

**Fix:** Replace with "hvac contractor calhoun ga" or remove entirely.

### 6. "Windows & Doors Installation" in Service Catalog on 118 Pages
**Risk Level: MEDIUM**

118 pages include this in the OfferCatalog schema:
```json
{"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Windows & Doors Installation"}}
```

Windows and doors installation is a classic "Building Contractor" / "General Contractor" signal. Having it listed as a service on most pages dilutes HVAC identity.

**Fix:** Remove "Windows & Doors Installation" from the OfferCatalog on all pages EXCEPT `windows-doors.html` itself. On that page, frame it as "Energy-Efficient Windows for HVAC Performance" or similar HVAC-adjacent language.

### 7. About Page Positions as "Whole-Home Energy Experts"
**Risk Level: MEDIUM**

- Meta description: "Whole-home energy experts"
- OG description: "why we became the whole-home energy experts in NW Georgia"
- Body: "the only company in Northwest Georgia that truly does it all — HVAC, insulation, weatherization, duct cleaning..."

This positions as an "energy company" rather than "HVAC specialist with energy expertise."

**Fix:** Reframe to "HVAC specialists with whole-home energy expertise" — HVAC must be the noun, energy must be the adjective.

### 8. `insulation-and-hvac-*.html` Pages (10 pages) — Insulation-First URL Structure
**Risk Level: MEDIUM**

10 pages named `insulation-and-hvac-[city].html` put insulation before HVAC in the URL slug. URLs are a ranking/categorization signal.

**Fix:** These can't easily be renamed without breaking links, but ensure their titles and H1s say "HVAC and Insulation" (HVAC first), not "Insulation and HVAC."

Current title example: "Insulation and HVAC in Calhoun GA" — **needs to be flipped**.

---

## 🟡 MODERATE ISSUES

### 9. Emergency Service Page Uses Triple Type
**Risk Level: LOW-MEDIUM**

`emergency-hvac-service.html` — an emergency HVAC page — declares `InsulationContractor` in its schema. This is semantically wrong. An emergency HVAC page has zero relationship to insulation contracting.

Same applies to all emergency pages that use the triple type.

### 10. Weatherization Pages Could Trigger Non-HVAC Categorization
**Risk Level: LOW-MEDIUM**

- `weatherization-coverage.html` — titled "Weatherization Coverage & Service Area"
- `weatherization-rebates.html` — focused on weatherization rebates
- Both use the triple type schema

Weatherization is more associated with "building performance" and "energy efficiency" contractors than HVAC.

**Fix:** Reframe as "HVAC Weatherization" or "HVAC + Weatherization" and ensure HVAC is primary in all content.

### 11. `crawlspace-encapsulation.html` Uses Triple Type
**Risk Level: LOW-MEDIUM**

Crawlspace encapsulation is a building/insulation service, not HVAC. Having `HVACBusiness` as a type is fine (it's your business), but having `InsulationContractor` alongside it on this page reinforces the non-HVAC signal.

---

## ✅ WHAT'S WORKING WELL

### Homepage Content Hierarchy: EXCELLENT
- **H2: "HVAC is King. Everything Else Supports It."** — Perfect HVAC-first positioning
- Service cards order: HVAC → Heat Pumps → Insulation → Duct Cleaning → Sheet Metal → Energy Audits — correct hierarchy
- Emergency HVAC bar is prominent above other content
- Insulation is properly framed as supporting HVAC performance ("because your HVAC is only as good as your home's envelope")

### QA Pages: EXCELLENT HVAC-First Positioning
- `hvac-qa-*.html` pages explicitly differentiate HVAC contractors from general contractors
- Content like "Not general contractors. HVAC-first experts" is exactly right
- FAQ about "HVAC contractors vs general contractors" reinforces specialist identity

### BPI Certified Page: EXCELLENT (Model for Other Pages)
- Uses pure `"@type": "HVACBusiness"` — no LocalBusiness, no InsulationContractor
- Title: "BPI Certified HVAC Contractor Georgia" — BPI framed as HVAC credential
- Service catalog: "BPI-Certified HVAC Services" — energy expertise enhancing HVAC

### HVAC Energy Rebates Authority Page: EXCELLENT
- Uses pure `"@type": "HVACBusiness"`
- Frames rebates through HVAC lens

### Emergency Domination Pages: GOOD
- Pure HVACBusiness schema type
- HVAC emergency specialist positioning

### Nav Menu Order: GOOD
- HVAC Repair & Install is first service listed
- Heat Pumps & Mini-Splits second
- Insulation third (appropriate supporting position)

---

## ZERO-COMPETITION PAGES AUDIT

| Page | Schema Type | HVAC-First? | Notes |
|------|-------------|-------------|-------|
| `bpi-certified-hvac-contractor.html` | ✅ `HVACBusiness` only | ✅ Excellent | Model page — copy this schema to others |
| `same-day-hvac-repair-calhoun.html` | ❌ Triple type | ⚠️ Good content, bad schema | Why does a same-day HVAC repair page declare InsulationContractor? |
| `hvac-energy-rebates-authority.html` | ✅ `HVACBusiness` only | ✅ Excellent | Properly frames rebates through HVAC lens |
| `companycam-geotagged-gallery.html` | ❌ Triple type | ⚠️ Neutral content | Photo gallery — should use HVACBusiness only |
| `custom-sheet-metal.html` | ⚠️ `[LocalBusiness, HVACBusiness]` | ✅ Good | Better than triple type, but should be HVACBusiness only |

---

## PRIORITY FIX LIST (Ranked)

### Phase 1: Schema Fixes (Highest Impact — Do This Week)
1. **Change ALL 124 pages** with triple type to `"@type": "HVACBusiness"` only
2. **Change ALL remaining pages** with `["LocalBusiness", "HVACBusiness"]` to `"@type": "HVACBusiness"` only  
3. **Fix `anderson-schema.jsonld`**: Remove InsulationContractor entity, remove LocalBusiness entity
4. **Fix `emergency-service-schema.jsonld`**: Change provider type to HVACBusiness
5. **Fix `authority-bridge-schema.json`**: Verify HVACBusiness type (it's correct)
6. **Align review counts** across all schema (513 or actual current count)

### Phase 2: Content Fixes (High Impact — Next 2 Weeks)
7. **Remove "Windows & Doors Installation"** from OfferCatalog on all pages except windows-doors.html
8. **Fix `insulation-and-hvac-*.html` titles** to say "HVAC and Insulation" (HVAC first)
9. **Fix About page** meta/OG descriptions: "HVAC specialists" not "energy experts"
10. **Remove "insulation contractor"** from homepage meta keywords
11. **Reframe weatherization pages** as HVAC + weatherization

### Phase 3: Monitoring (Ongoing)
12. Audit any new pages for schema compliance before publishing
13. Monitor Google Business Profile category weekly for 30 days after fixes
14. Check Google Search Console for how Google categorizes pages

---

## APPENDIX: Page Categories

### Pages Using ✅ Pure HVACBusiness (68 pages) — NO CHANGES NEEDED
- bpi-certified-hvac-contractor.html
- hvac-energy-rebates-authority.html
- emergency-hvac-calhoun-domination.html
- emergency-hvac-dalton-ga-domination.html
- emergency-hvac-rome-ga-domination.html
- All QA pages (qa-*.html) — approximately 60 pages
- Various emergency repair pages

### Pages Using ⚠️ [LocalBusiness, HVACBusiness] (10 pages) — REMOVE LocalBusiness
- custom-sheet-metal.html
- Various other pages

### Pages Using ❌ [LocalBusiness, HVACBusiness, InsulationContractor] (124 pages) — CRITICAL FIX
- index.html (HOMEPAGE!)
- about.html
- services.html
- contact.html
- All city pages (calhoun-ga.html, dalton-ga.html, etc.)
- All emergency-hvac-*.html (non-domination)
- All energy-rebates-hvac-*.html
- All insulation-and-hvac-*.html
- All hvac-repair-cost-*.html
- emergency-hvac-service.html
- weatherization-coverage.html
- weatherization-rebates.html
- windows-doors.html
- And many more

---

## BOTTOM LINE

**The content is largely HVAC-first. The schema is NOT.** 

You have 124 pages telling Google you're equally an InsulationContractor, and 118 pages listing "Windows & Doors Installation" as a service. That's enough signal for Google to potentially categorize you as "Building Contractor" or "General Contractor."

The fix is mechanical — it's a find-and-replace operation across 124 files to change the schema types, plus removing Windows & Doors from the service catalog on most pages. Total effort: ~2-3 hours of careful scripting.

**After these fixes, compliance score would jump to 9/10.** The remaining 1 point is the insulation-and-hvac URL structure which can't be easily changed without redirect risk.
