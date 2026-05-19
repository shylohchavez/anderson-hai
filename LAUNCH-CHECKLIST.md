# Anderson HAI — Launch Day Checklist

Things that **must** happen on the day this site goes live at johnandersonservice.com. Right now the site is in staging — search engines and AI tools are intentionally blocked so they don't index work-in-progress.

Read top to bottom on launch day. None of these are optional.

---

## 1. Unblock crawlers (the most important one)

The file `robots.txt` currently has this content:

```
User-agent: *
Disallow: /
```

That means "no search engine or AI tool is allowed to read anything." Correct for staging. Wrong for production.

**Replace the file content with:**

```
# Anderson Heating, Air & Insulation
# robots.txt — production

User-agent: *
Allow: /
Disallow: /404.html
Disallow: /reviews-section.html
Disallow: /reviews-schema.html
Disallow: /reviews-page.html
Disallow: /companycam-geo-seo.html
Disallow: /emergency-hvac-calhoun-domination.html
Disallow: /emergency-hvac-dalton-ga-domination.html
Disallow: /emergency-hvac-rome-ga-domination.html

# Explicitly welcome AI search engines (they sometimes ignore wildcards)
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

Sitemap: https://johnandersonservice.com/sitemap.xml
```

Until this swap happens, **everything else on this list is wasted effort.** The site simply will not appear in any search results.

---

## 2. Fix the staging-only URL in the schema

The file `authority-bridge-schema.json` references `https://shylohchavez.github.io/anderson-hai/` (the staging URL). On launch day, replace every occurrence of that URL with `https://johnandersonservice.com` in that one file.

---

## 3. Verify the site actually works on the new domain

Open these pages in a browser at the new domain (not staging):

- https://johnandersonservice.com/
- https://johnandersonservice.com/about.html
- https://johnandersonservice.com/contact.html
- https://johnandersonservice.com/services.html
- https://johnandersonservice.com/calhoun-ga.html
- https://johnandersonservice.com/dalton-ga.html
- https://johnandersonservice.com/rome-ga.html

For each: phone number visible? Logo loads? Free Estimate button clicks through? Footer shows correct address?

---

## 4. Submit sitemap to search engines

Go to:

- **Google Search Console** — https://search.google.com/search-console
  - Add property: `https://johnandersonservice.com`
  - Verify ownership (DNS, HTML tag, or Google Analytics)
  - Submit sitemap: `https://johnandersonservice.com/sitemap.xml`
- **Bing Webmaster Tools** — https://www.bing.com/webmasters
  - Add site, verify, submit same sitemap

These two steps tell Google and Bing "we exist, please come crawl us." Without them, indexing takes weeks instead of days.

---

## 5. Verify the AI summary file

After launch, visit https://johnandersonservice.com/llms.txt in a browser. You should see a markdown document starting with `# Anderson Heating, Air & Insulation`. This file is what ChatGPT, Perplexity, Claude, etc. read to understand your business. If it 404s, the file didn't deploy.

---

## 6. Google Business Profile

Make sure your Google Business Profile (the listing that appears in Google Maps results) points its website link to **https://johnandersonservice.com** — not the staging URL, not a Facebook page, not a phone-number-only listing.

Same name and same address and same phone as the website — Google compares these to confirm you're a real business. Any mismatch hurts local rankings.

---

## 7. Update the 24-hour smoke-test list

About 24 hours after launch, search Google for these exact phrases (in an incognito window so your personal results don't bias it):

- `site:johnandersonservice.com` — should return your pages. If it returns "no results," indexing hasn't started yet; wait another 24-48 hours. If results never appear, recheck step 1.
- `Anderson Heating Air Insulation Calhoun` — should show your site in the first page.
- `HVAC Calhoun GA` — long-term goal: top 3 results. Won't happen immediately, but worth watching.

---

## 8. After 7 days

- Look at Google Search Console → Coverage. Pages should be "Indexed." If many are "Discovered, not indexed," it usually means duplicate content or thin pages — see the **Known Issues** section below.
- Look at Performance tab. You'll see what searches are showing your site. This is gold.

---

## Known issues that need product decisions (not launch blockers)

These are things that will not stop launch, but should be tackled in the first weeks after launch.

### 1. Duplicate city/service pages
For each city we have up to 3 near-identical pages (e.g., `calhoun-ga.html`, `calhoun-ga-hvac.html`, `calhoun-hvac-service.html`). Google sees these as competing copies of each other; it sometimes refuses to show any of them because it can't decide which is "real."

**The decision needed:** for each city, pick the one canonical page and either delete the others or redirect them to the canonical. We chose to keep all three at staging time because they were doing programmatic SEO experiments, but at production scale they will fight each other.

### 2. Q&A pages need real local content
The 60 city Q&A pages (e.g., `qa-ac-repair-calhoun-ga.html` vs `qa-ac-repair-dalton-ga.html`) are currently ~94% identical text with only the city name swapped. Google's "helpful content" system and AI search engines both demote pages that look templated like this. See the separate **Q&A Differentiation Plan** for what to do.

### 3. services.html is on a different design template
This one page renders in a different visual style than the rest of the site. A visitor clicking "Services" in the nav will feel like they left the site. Needs to be rebuilt on the standard template. Not a launch blocker, but visible.

### 4. CTA copy fragmentation
The "click here" buttons across the site say six different things: "Book a Free Estimate," "Request Estimate," "Get Free Estimate," "Free Estimate," "Get Custom Quote," "Contact & Free Estimate." A visitor sees this as inconsistent. Pick one phrase. **Recommendation: "Get a Free Estimate" sitewide.**

### 5. 136 pages don't show the phone number in the desktop header
For an HVAC business, the phone is the conversion. Currently the homepage and most service pages only show "Free Estimate" in the header — no phone. Should add a `(706) 629-0749` call-button next to the Free Estimate button on every page header.

---

## Quick reference

- **Live URL (eventually):** https://johnandersonservice.com
- **Staging URL (current):** https://shylohchavez.github.io/anderson-hai/
- **Repository:** https://github.com/shylohchavez/anderson-hai
- **Sitemap:** /sitemap.xml (197 URLs)
- **AI search summary:** /llms.txt
- **Phone:** (706) 629-0749
- **Address:** 519 Pine Street, Calhoun, GA 30701
- **Hours:** Mon–Fri 7:30 AM – 5:00 PM ET
