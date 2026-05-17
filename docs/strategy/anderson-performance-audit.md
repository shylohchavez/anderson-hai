# Anderson HAI Website — Performance & Core Web Vitals Audit
**Date:** May 15, 2026  
**Domain:** johnandersonservice.com  
**Hosting:** Apache (WordPress 6.9.4) — NOT GitHub Pages  
**Theme:** Kadence 1.4.5 + Kadence Blocks 3.6.7 + Kadence Blocks Pro 2.7.4  
**Performance Plugin:** Perfmatters 2.5.0  

---

## Executive Summary

The Anderson HAI website has **solid fundamentals** thanks to Perfmatters (used CSS extraction, delayed stylesheet loading, lazy loading) and proper image format usage (WebP throughout). However, there are **significant performance bottlenecks** that likely push Core Web Vitals into the orange/red zone — especially on mobile. The homepage weighs **~374 KB of HTML alone** (before images/scripts), with **93 KB of inline CSS** in the `<head>`, which is the single biggest performance killer.

### Estimated Core Web Vitals (Server-Side Analysis)

| Metric | Target | Estimated Desktop | Estimated Mobile | Status |
|--------|--------|-------------------|------------------|--------|
| **LCP** | < 2.5s | ~2.5–3.5s | ~4–6s | 🟡/🔴 |
| **FID/INP** | < 100ms | ~50–100ms | ~100–200ms | 🟡 |
| **CLS** | < 0.1 | ~0.05–0.1 | ~0.1–0.25 | 🟡/🔴 |
| **FCP** | < 1.8s | ~1.4–2.0s | ~2.5–4s | 🟡/🔴 |
| **TTFB** | < 800ms | ~1.4s | ~1.4s | 🔴 |

---

## 1. CRITICAL ISSUES (Fix First — Biggest Impact)

### 🔴 C1: Massive HTML Document Size — 374 KB
- **Homepage HTML:** 374 KB (uncompressed)
- **Cooling page:** 337 KB  
- **Insulation page:** 337 KB
- **Contact page:** 254 KB
- **No gzip/brotli compression detected on HTML responses**
- The HTML itself contains **~93 KB of inline CSS** from Perfmatters' "Used CSS" feature
- The Kadence blocks CSS inline block alone is enormous (~50 KB of page-specific layout rules)

**Impact:** Directly increases TTFB and FCP. The server must generate and transmit ~374 KB before the browser can begin parsing.

**Fix:** 
1. **Enable gzip/brotli compression on Apache** — this alone could reduce HTML transfer from 374 KB to ~60–80 KB (5x reduction)
2. Review if Perfmatters' "Used CSS" inline setting is optimal vs. a separate file with `preload`
3. Reduce Kadence blocks CSS bloat — many rules are for blocks not used on the page

**Expected Impact:** FCP improvement of 1–2 seconds on mobile

### 🔴 C2: No HTTP Caching Headers
- **HTML pages:** No `Cache-Control` or `Expires` headers
- **Static assets (images, CSS, JS):** No `Cache-Control` headers detected
- Only `ETag` present on some assets (CSS/JS)
- Images have NO caching headers at all

**Impact:** Every return visit re-downloads everything. Repeat visitors get zero benefit from browser cache.

**Fix:** Add to `.htaccess`:
```apache
# Cache static assets for 1 year
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresDefault "access plus 1 month"
</IfModule>

# Enable compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json
</IfModule>
```

**Expected Impact:** 50-80% faster repeat visits, Google PageSpeed improvement

### 🔴 C3: Slow Server Response (TTFB ~1.4s)
- **Time to First Byte:** 1.42s (homepage), 1.38s (cooling), 1.14s (insulation)
- Target: < 800ms (ideally < 200ms)
- Server: Apache (likely shared hosting or unoptimized VPS)
- WordPress is doing server-side geo-detection (CF GeoPlugin) on every request

**Impact:** Everything is delayed by 1.4 seconds before the browser even receives the first byte.

**Fix:**
1. Enable **page caching** (WP Super Cache, W3 Total Cache, or Perfmatters may have this)
2. Consider **Cloudflare CDN** (free tier) — would add edge caching + compression + HTTP/3
3. Investigate CF GeoPlugin — it's running server-side geo lookup on every page load
4. Check hosting plan — shared hosting is likely the bottleneck

**Expected Impact:** TTFB reduction to 200-500ms (2–7x faster)

---

## 2. HIGH-PRIORITY ISSUES

### 🟠 H1: Hero Background Image is 410 KB
- `hero_colorgraded-1-1.webp` — **410 KB** (used as CSS background-image)
- This is the LCP element on desktop
- It's referenced in inline CSS, so it can't be discovered until CSS is parsed
- No `preload` hint for this critical image

**Fix:**
1. **Add preload hint:** `<link rel="preload" as="image" href="...hero_colorgraded-1-1.webp" fetchpriority="high">`
2. **Compress/resize** — a background image at 85% coverage doesn't need to be full resolution. Target ~100-150 KB
3. Consider serving different sizes via `srcset` or media queries for tablet/mobile

**Expected Impact:** LCP improvement of 0.5–1.5 seconds

### 🟠 H2: Large Images Without Responsive Sizing
| Image | Size | Purpose |
|-------|------|---------|
| hero_colorgraded-1-1.webp | 410 KB | Hero background (desktop) |
| AndersonHAI-055-scaled.webp | 357 KB | Content image |
| refri-1.webp | 312 KB | Service image |
| anderson-back-mobile.webp | 81 KB | Hero background (mobile) ✅ |
| Anderson-logo.webp | 54 KB | Logo (OG share) |
| Anderson-logo-white.webp | 44 KB | Footer logo |
| duct2.webp | 50 KB | Content image |
| Anderson-figure-1.webp | 23 KB | Content image ✅ |

**Total image weight:** ~1.33 MB (before lazy loading helps)

**Fix:**
1. **AndersonHAI-055-scaled.webp** — the "-scaled" suffix means WordPress served the full-resolution version. Generate proper thumbnails (800px wide for content areas)
2. **refri-1.webp** — 312 KB for what's likely a card image. Should be under 50 KB at proper display size
3. Add `width` and `height` attributes to all images to prevent CLS

### 🟠 H3: Too Many Render-Blocking/Deferred Resources
- **31 script tags** in the document
- **73 stylesheet references** (inline + link tags)
- **18 delayed stylesheets** via Perfmatters' data-pmdelayedstyle
- Perfmatters is helping by delaying non-critical CSS, but the sheer volume is excessive

**Key third-party scripts:**
1. **Google reCAPTCHA** (`www.google.com/recaptcha/api.js`) — loaded on EVERY page even if form isn't visible
2. **Google Tag Manager** — loading synchronously in `<head>`
3. **Sassy Social Share** — loaded on every page
4. **CF GeoPlugin** — inline JS with server-side data (~2 KB)
5. **Cookie Consent plugin** — loaded on every page

**Fix:**
1. **Load reCAPTCHA only on pages with forms** (contact page) — saves ~500 KB of third-party downloads on other pages
2. **Defer GTM loading** — use `defer` or load after user interaction
3. **Remove Sassy Social Share if not needed** — adds CSS + JS on every page
4. **Evaluate CF GeoPlugin necessity** — it serializes 1.2 KB of geo data into every page

### 🟠 H4: Video File on Homepage (1.25 MB)
- `AndersonVideo-1.webm` — **1.25 MB** referenced in OG/schema markup
- The video tag may be loaded on the homepage
- No `preload="none"` attribute detected

**Fix:**
1. Add `preload="none"` to video element — don't download until user initiates playback
2. Use a poster image instead of auto-loading video
3. Consider lazy-loading the video below the fold

---

## 3. MEDIUM-PRIORITY ISSUES

### 🟡 M1: Five Font Files Preloaded
Preloading 5 font files (Poppins 400/500/700, Sora 700, Urbanist 400):
- Each ~10-25 KB = ~75-100 KB total
- All preloaded in `<head>` — competing with critical resources
- Fonts self-hosted (good!) with `font-display: swap` (good!)

**Fix:** 
1. Reduce to 2-3 fonts max. Do you really need Poppins AND Sora AND Urbanist?
2. Remove preload for fonts used only below the fold
3. Consider using system fonts for body text

### 🟡 M2: Perfmatters Used CSS is Very Large (50 KB inline)
- The `perfmatters-used-css` style block is ~50 KB inline in `<head>`
- Contains CSS for Kadence theme, blocks, forms, sliders, navigation, etc.
- This must all be parsed before any rendering begins

**Fix:**
1. Review Perfmatters settings — the "Used CSS" feature may be capturing too much
2. Consider if some CSS can be moved to deferred loading
3. Audit unused CSS — the Splide slider CSS, advanced form CSS, and icon list CSS may not be needed above the fold

### 🟡 M3: jQuery Still Loaded (Render-Blocking)
- jQuery 3.7.1 (86 KB uncompressed, ~30 KB gzipped) loaded in `<head>` as a preloaded script
- Many modern sites have moved away from jQuery
- Kadence theme still depends on it

**Fix:**
1. Move jQuery to footer if possible (check Perfmatters settings for "Defer JavaScript")
2. Long-term: evaluate if jQuery can be eliminated

### 🟡 M4: Potential CLS from Lazy Loading
- 10 images with `loading="lazy"` and 1 with `loading="eager"`
- All images also use Perfmatters lazy loading (`data-src` pattern)
- Double lazy loading (native + JS) can cause flash/reflow issues
- Need `width`/`height` attributes on all images for CLS prevention

### 🟡 M5: No CDN Detected
- All assets served from origin Apache server
- No CDN headers (no `cf-cache-status`, `x-cache`, etc.)
- Every request goes to origin, adding latency

**Fix:** Implement Cloudflare (free tier) for:
- Edge caching of static assets
- Automatic compression (Brotli)
- HTTP/3 support
- Global CDN distribution
- Free SSL optimization

---

## 4. LOW-PRIORITY / NICE-TO-HAVE

### 🟢 L1: HTTP/2 is Enabled ✅
Good — multiplexing helps with the large number of requests.

### 🟢 L2: Images in WebP Format ✅
All images are already in WebP — this is correct and optimal.

### 🟢 L3: Fonts Self-Hosted ✅
Good — no external Google Fonts calls. All served from own domain with proper `font-display: swap`.

### 🟢 L4: Perfmatters CSS Delay Working ✅
18 non-critical stylesheets properly deferred via `data-pmdelayedstyle`. Good optimization.

### 🟢 L5: Mobile Hero Image is Small (81 KB) ✅
Separate, smaller background image for mobile devices — good practice.

### 🔵 L6: Viewport Meta Tag
Current: `width=device-width, initial-scale=1, minimum-scale=1`
The `minimum-scale=1` prevents users from zooming out, which is fine but could be an accessibility concern for some users.

### 🔵 L7: Button/Touch Target Sizes
Buttons use `padding: 3px 6px` — this is very small for mobile touch targets.
Google recommends minimum 48×48px touch targets.

**Fix:** Increase mobile button padding to at least `padding: 12px 24px` for CTAs.

---

## 5. PAGE-BY-PAGE ANALYSIS

### Homepage (`/`)
| Metric | Value |
|--------|-------|
| HTML Size | 374 KB |
| TTFB | 1.42s |
| Time to Complete | 1.53s (HTML only) |
| Images | 6 unique images (~1.33 MB total) |
| Scripts | 31 |
| Stylesheets | 73 |
| Video | 1 (1.25 MB WebM) |
| Hero Image | 410 KB (CSS background) |
| LCP Element | Hero background image (likely) |

### Cooling (`/cooling/`)
| Metric | Value |
|--------|-------|
| HTML Size | 337 KB |
| TTFB | 1.38s |

### Insulation (`/insulation/`)
| Metric | Value |
|--------|-------|
| HTML Size | 337 KB |
| TTFB | 1.14s |

### Contact Us (`/contact-us/`)
| Metric | Value |
|--------|-------|
| HTML Size | 254 KB |
| TTFB | 0.71s |

### About Us (`/about-us/`)
| Metric | Value |
|--------|-------|
| Text Content | Minimal (771 chars extracted) |
| Very thin content page |

---

## 6. MOBILE vs. DESKTOP PERFORMANCE GAP

### Desktop Advantages
- Larger bandwidth handles the 374 KB HTML faster
- Hero image loads as CSS background at 85% width — visually fills above-fold
- Multiple connections handle parallel resource downloads

### Mobile Disadvantages
- **374 KB HTML on 3G/4G = 2-4 seconds just for HTML download** (no compression!)
- Hero image swaps to mobile version (81 KB — good), but fallback to large image can happen
- 93 KB of inline CSS parsed on mobile CPU = significant delay
- reCAPTCHA + GTM + jQuery all load on mobile
- Button touch targets at `3px 6px` padding are too small
- Mobile drawer menu loads additional CSS/JS

### Estimated Mobile vs Desktop Gap
| Metric | Desktop | Mobile | Gap |
|--------|---------|--------|-----|
| FCP | ~1.5–2s | ~3–4s | 2x slower |
| LCP | ~2.5–3.5s | ~4–6s | 2x slower |
| Total Page Load | ~4–6s | ~8–12s | 2x slower |

---

## 7. PRIORITY-RANKED OPTIMIZATION PLAN

### 🔥 Quick Wins (< 1 hour, biggest impact)

| # | Action | Expected Impact | Effort |
|---|--------|-----------------|--------|
| 1 | **Enable gzip/brotli compression** on Apache (.htaccess) | FCP -1–2s, all pages | 15 min |
| 2 | **Add Cache-Control headers** for static assets | Repeat visits 50-80% faster | 15 min |
| 3 | **Preload hero image** with fetchpriority="high" | LCP -0.5–1s | 5 min |
| 4 | **Add preload="none" to video** | Save 1.25 MB on initial load | 5 min |
| 5 | **Load reCAPTCHA only on contact page** | Save ~500 KB on non-form pages | 15 min |

### 📈 Medium-Term (1–4 hours, significant impact)

| # | Action | Expected Impact | Effort |
|---|--------|-----------------|--------|
| 6 | **Set up Cloudflare CDN** (free tier) | TTFB → <500ms, auto compression, HTTP/3 | 1 hr |
| 7 | **Enable WordPress page caching** | TTFB → <200ms for cached pages | 30 min |
| 8 | **Optimize hero image** to ~100-150 KB | LCP -0.5s | 30 min |
| 9 | **Generate proper image thumbnails** for scaled images | Save ~500 KB+ per page | 1 hr |
| 10 | **Increase mobile CTA button sizes** | Better mobile UX + CWV | 30 min |

### 🔧 Long-Term (strategic improvements)

| # | Action | Expected Impact | Effort |
|---|--------|-----------------|--------|
| 11 | **Audit/reduce CSS bloat** — 50 KB inline is too much | FCP -0.5s | 2-4 hrs |
| 12 | **Consolidate fonts** — 3 families is excessive | Save ~40 KB + faster render | 2 hrs |
| 13 | **Remove/replace Sassy Social Share** | Less CSS/JS on every page | 30 min |
| 14 | **Evaluate CF GeoPlugin** — adds weight to every page | Cleaner HTML, faster parse | 1 hr |
| 15 | **Defer GTM loading** until after user interaction | Better FCP/LCP scores | 30 min |

---

## 8. EMERGENCY SERVICE PAGE IMPACT ASSESSMENT

**Critical concern:** A homeowner with a broken AC in July in Calhoun, GA searching on their phone.

### Current Experience (estimated)
1. Google shows result → click → **1.4s waiting for server** (TTFB)
2. **2–3 more seconds** downloading/parsing 374 KB uncompressed HTML + 93 KB inline CSS
3. **1–2 more seconds** for hero image + fonts + scripts
4. **Total: 5–7 seconds before the page is usable on mobile**
5. Google benchmark: **53% of mobile users abandon after 3 seconds**

### After Recommended Fixes
1. TTFB: **0.2–0.5s** (with caching + CDN)
2. HTML download: **0.3–0.5s** (with gzip compression)
3. Hero rendering: **0.5–1s** (with preload hint)
4. **Total: 1.5–2.5 seconds to usable page on mobile**

### Revenue Impact Estimate
- Every 1 second of load time = ~7% decrease in conversions (Google data)
- Current 5–7s load → potential 35–50% conversion loss vs. optimized competitor
- For emergency HVAC services ($200–500+ per call), even 1 additional conversion/month from faster pages could mean **$2,400–6,000/year** in additional revenue

---

## 9. WHAT'S ALREADY WORKING WELL ✅

1. **Perfmatters plugin** — delayed CSS loading, lazy loading, used CSS extraction
2. **WebP images throughout** — modern, efficient format
3. **Self-hosted fonts** with `font-display: swap` — no FOIT (flash of invisible text)
4. **HTTP/2 enabled** — multiplexed connections
5. **Mobile-specific hero image** — smaller file for mobile
6. **Responsive images** with `loading="lazy"` on below-fold content
7. **Structured data/Schema.org** — properly implemented for local business
8. **Separate mobile background** — 81 KB vs 410 KB desktop version

---

## Summary of Top 5 Recommendations

1. **🔴 Enable gzip compression** — single biggest win, zero cost, 5x HTML reduction
2. **🔴 Add Cache-Control headers** — makes every repeat visit dramatically faster
3. **🔴 Set up Cloudflare CDN** (free) — fixes TTFB, adds compression, HTTP/3
4. **🟠 Enable WordPress page caching** — eliminates server-side processing time
5. **🟠 Preload hero image + optimize to <150 KB** — directly improves LCP

Implementing just these 5 changes should bring Core Web Vitals from red/orange to solid green for most pages, and reduce mobile load time from 5–7s to under 2.5s.
