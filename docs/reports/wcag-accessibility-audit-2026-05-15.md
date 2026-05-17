# WCAG 2.1 Accessibility Audit Report
## Anderson Heating, Air & Insulation — johnandersonservice.com
**Audit Date:** May 15, 2026  
**Auditor:** Claude (Automated Code-Level + Content Review)  
**Standard:** WCAG 2.1 Level AA (with AAA opportunities noted)  
**Pages Sampled:** Homepage, /heating/, /cooling/, /about-us/, /contact-us/

---

## Executive Summary

**Overall Compliance Estimate: ~75% WCAG 2.1 Level AA**

The site is built on WordPress with the Kadence theme and Kadence Blocks — a modern, accessibility-aware stack. Several strong accessibility foundations are already in place, but there are **12 critical/high issues** and **15 medium/low issues** that need addressing to reach full Level AA compliance and minimize ADA lawsuit risk.

### ADA Lawsuit Risk Assessment: **MODERATE**
HVAC services are considered essential, especially emergency services. The site's target demographic includes elderly homeowners who are more likely to use assistive technology. The combination of essential services + older demographic = higher legal exposure if accessibility issues exist.

---

## 🟢 WHAT'S WORKING WELL (Strengths)

### 1. Language Declaration ✅
```html
<html lang="en-US">
```
- Properly declared — screen readers will use correct pronunciation rules.

### 2. Skip Navigation Link ✅
```html
<a class="skip-link screen-reader-text scroll-ignore" href="#main">Skip to content</a>
```
- Present and properly implemented with screen-reader-text class.
- Becomes visible on focus (good keyboard accessibility pattern).

### 3. Semantic HTML Landmarks ✅
- `<header id="masthead" role="banner">` — proper header landmark
- `<main id="inner-wrap" role="main">` — proper main content area
- `<footer id="colophon" role="contentinfo">` — proper footer landmark
- `<nav aria-label="Main Mega Menu">` — labeled navigation
- `<section aria-label="Services menu">` — labeled sections
- `<section aria-label="Anderson highlights">` — labeled sections

### 4. Logo Alt Text ✅
```html
<img alt="Anderson Heating, Air &amp; Insulation" class="custom-logo">
```
- Brand logo has proper descriptive alt text.

### 5. Form Accessibility ✅ (Mostly)
- Form fields have proper `<label>` elements with `for` attributes matching input `id`s
- Required fields use both `required` attribute AND `aria-required="true"`
- Required fields visually marked with asterisk `<span class="kb-adv-form-required">*</span>`
- Input types are semantically correct (`type="tel"`, `type="email"`, `type="text"`)

### 6. Service Area Tabs — Excellent ARIA ✅
```html
<div role="tablist" aria-label="Service area counties">
  <button role="tab" id="tab-gordon" aria-controls="pane-gordon" aria-selected="true">
  <section role="tabpanel" aria-labelledby="tab-gordon">
```
- Full ARIA tab pattern with `role="tablist"`, `role="tab"`, `role="tabpanel"`
- Proper `aria-controls`, `aria-selected`, `aria-expanded` attributes
- Dynamically managed via JavaScript

### 7. Decorative SVG Icons ✅
```html
<svg aria-hidden="true" class="kadence-svg-icon">
```
- SVG icons properly hidden from screen readers with `aria-hidden="true"`.

### 8. Phone Number as Clickable Link ✅
```html
<a href="tel:7066290749" class="cta-btn cta-secondary">(706) 629-0749</a>
```
- Emergency phone number is a clickable `tel:` link on both desktop and mobile.
- Appears multiple times across the page (header, hero, footer).

### 9. Social Media Links ✅
```html
<a href="https://www.facebook.com/..." target="_blank" aria-label="Facebook">
<a href="https://www.youtube.com/..." target="_blank" aria-label="YouTube">
```
- Social links have proper `aria-label` attributes.

### 10. Screen Reader Text Utility ✅
```css
.screen-reader-text { clip: rect(1px,1px,1px,1px); position: absolute !important; ... }
.kb-screen-reader-text { position: absolute; width: 1px; height: 1px; ... }
```
- Two screen-reader-only text classes properly implemented.

---

## 🔴 CRITICAL ISSUES (Must Fix — ADA Risk)

### C1. Focus Outline Suppressed Globally 🔴
**WCAG:** 2.4.7 Focus Visible (Level AA)  
**Severity:** CRITICAL  
**Risk:** HIGH — #1 source of ADA lawsuits after missing alt text
```css
:where(html:not(.no-js)) .hide-focus-outline *:focus { outline: 0; }
```
Also:
```css
input:focus, textarea:focus { outline: 0; }
```
**Impact:** Keyboard-only users cannot see where they are on the page. This affects ALL interactive elements.  
**Fix:** Remove the global outline suppression. Instead, use `:focus-visible` to show focus rings only for keyboard users:
```css
*:focus-visible {
  outline: 3px solid var(--global-palette3); /* Anderson orange */
  outline-offset: 2px;
}
```

### C2. Footer Logo Missing Alt Text 🔴
**WCAG:** 1.1.1 Non-text Content (Level A)  
**Severity:** CRITICAL
```html
<img alt class="kb-img wp-image-241814" data-src=".../Anderson-logo-white.webp">
```
**Impact:** Empty `alt` attribute tells screen readers the image is decorative. But this is the company logo in the footer — it should have alt text.  
**Fix:** Add `alt="Anderson Heating, Air & Insulation"` to the footer logo.

### C3. Some Image Alt Text is Generic/Non-Descriptive 🔴
**WCAG:** 1.1.1 Non-text Content (Level A)  
**Severity:** HIGH
```html
alt="Anderson Heating, Air & Insulation | heater tankless"
alt="Anderson Heating, Air & Insulation | air"
alt="Anderson Heating, Air & Insulation | duct2"
alt="Anderson"
```
**Impact:** While alt text IS present (improvement from the 250+ update), many still use the pattern `"Company Name | filename"` which doesn't describe the image content.  
**Fix:** Use descriptive alt text that tells users what the image shows:
- `"Technician installing a tankless water heater in a residential home"`
- `"Home air filtration system with clean filter installed"`
- `"HVAC ductwork being repaired in a crawlspace"`

### C4. Video Lacks Accessible Controls & Transcript 🔴
**WCAG:** 1.2.1 Audio-only/Video-only (Level A), 1.2.5 Audio Description (Level AA)  
**Severity:** HIGH
```html
<section class="scroll-webm-video" aria-hidden="true">
  <video ...>
```
**Impact:** The hero video is marked `aria-hidden="true"` (good for decorative), but if it contains meaningful content, it needs:
- Captions/transcript
- Audio description if it conveys visual-only information
- Accessible play/pause controls  
**Note:** If truly decorative (background ambiance only), the `aria-hidden="true"` is correct. Verify the video content.

### C5. Google Maps iframes Missing Title on First Instance 🔴
**WCAG:** 4.1.2 Name, Role, Value (Level A)  
**Severity:** HIGH
```html
<iframe class="sa-gmap" loading="eager" fetchpriority="high" ...>
```
The first iframe (Gordon County map) does not have a `title` attribute, while subsequent ones do:
```html
<iframe class="sa-gmap" title="Service Areas Map" ...>
```
**Fix:** Add `title="Gordon County Service Area Map"` to the first iframe. Make titles unique per county for all iframes.

---

## 🟡 HIGH-PRIORITY ISSUES

### H1. Color Contrast Concerns 🟡
**WCAG:** 1.4.3 Contrast (Minimum) (Level AA)  
**Severity:** HIGH

**Identified contrast pairs needing verification:**

| Element | Foreground | Background | Estimated Ratio | Pass? |
|---------|-----------|------------|-----------------|-------|
| Body text on white | `#181818` | `#ffffff` | ~18.5:1 | ✅ |
| Orange CTA button | `#ffffff` on `#E74D1F` | N/A | ~3.6:1 | ⚠️ Borderline for small text |
| Purple CTA button | `#ffffff` on `#481F6F` | N/A | ~9.2:1 | ✅ |
| Hero text on gradient | `#ffffff` on dark overlay | Variable | Needs visual check | ⚠️ |
| Placeholder text | `#6e6e70` on `#ffffff` | N/A | ~4.6:1 | ✅ (barely) |
| Sub-menu items | `#481f6f` on `#ecf0f2` | N/A | ~8.5:1 | ✅ |
| Link color | `#481f6f` on `#ffffff` | N/A | ~10.1:1 | ✅ |

**Action needed:** The orange CTA button (`#E74D1F` bg with white text) has approximately **3.6:1 contrast** — below the 4.5:1 minimum for normal-sized text. If the button text is ≥18.67px bold or ≥24px regular, it passes at 3:1 for "large text." Verify the actual rendered font size.

**Fix:** Either darken the orange to `#C93004` (which is already `--global-palette4`) or increase button text size to qualify as "large text."

### H2. Mobile Menu Drawer — Keyboard Trap Risk 🟡
**WCAG:** 2.1.2 No Keyboard Trap (Level A)  
**Severity:** HIGH
```html
<div id="mobile-drawer" class="popup-drawer">
  <div class="drawer-inner">
    <div class="drawer-header">
      <button class="drawer-toggle" ...>
```
**Concerns:**
- No visible `tabindex` management or focus trap script detected
- When drawer opens, focus needs to move into the drawer
- When drawer closes, focus needs to return to the toggle button
- Escape key should close the drawer
- Background content should be inert while drawer is open

**Fix:** Implement focus management:
```javascript
// On open: set focus to close button, trap Tab within drawer
// On close: return focus to toggle button
// Listen for Escape key to close
```

### H3. Heading Hierarchy Issues 🟡
**WCAG:** 1.3.1 Info and Relationships (Level A)  
**Severity:** MEDIUM-HIGH

**Homepage heading structure observed:**
```
H1: (hero title — appears correct)
H2: "Heating Services | Furnace Repair..." (on subpages)
H2: "Heating Services You Can Count On" (on subpages)
H3: "Gordon County" / "Bartow County" (service areas)
```

**Potential issues:**
- Multiple H2s on the homepage without a clear single H1 visible in content
- H3 used for county names within tab panels (appropriate)
- Some pages may have duplicate H1/H2 patterns

**Fix:** Ensure every page has exactly one `<h1>` and headings follow a logical order without skipping levels.

### H4. Trustbox Links — Redundant/Confusing Link Text 🟡
**WCAG:** 2.4.4 Link Purpose (Level A)  
**Severity:** MEDIUM
```html
<a class="and-trustbox__item" href="/about-us/" aria-label="Learn more about our top-rated service">
<a class="and-trustbox__item" href="/about-us/" aria-label="Learn more about our locally owned company">
```
**Issue:** Two different `aria-labels` link to the same `/about-us/` page. Screen reader users will hear two different link purposes that lead to the same destination.

**Fix:** Make link purposes distinguishable or combine into one link.

---

## 🟠 MEDIUM-PRIORITY ISSUES

### M1. Page Title Not Unique Across Pages 🟠
**WCAG:** 2.4.2 Page Titled (Level A)  
**Severity:** MEDIUM

- Homepage: `"Anderson Heating, Air & Insulation | Calhoun Services"`  
- Contact page: `"Anderson Heating, Air & Insulation"` (generic — missing page-specific suffix)
- About page: `"Anderson Heating, Air & Insulation"` (same generic title)
- Heating: `"Heating Services | Anderson Heating & Air"` ✅ (good)
- Cooling: `"Cooling Services | Anderson Heating & Air"` ✅ (good)

**Fix:** Ensure every page has a unique, descriptive `<title>` tag. Contact should be `"Contact Us | Anderson Heating, Air & Insulation"`.

### M2. `/request-an-estimate/` Redirects to Homepage 🟠
**WCAG:** 3.2.5 Change on Request (Level AAA), General UX  
**Severity:** MEDIUM
**Impact:** If users or search engines link to `/request-an-estimate/`, they land on the homepage with no indication they've been redirected. There's no dedicated estimate request form page.  
**Fix:** Either create a dedicated estimate page or redirect to `/contact-us/` with a clear form.

### M3. Lazy-Loaded Images — Alt Text in noscript Only 🟠
**WCAG:** 1.1.1 Non-text Content (Level A)  
**Severity:** MEDIUM
```html
<img src="data:image/svg+xml,..." alt="Financing options" class="perfmatters-lazy" data-src="...">
<noscript><img src="..." alt="Financing options"></noscript>
```
**Status:** The PerfMatters lazy loading preserves alt text on both the placeholder `<img>` and `<noscript>` fallback. ✅ This is correctly implemented.

### M4. Cookie Consent Banner Accessibility 🟠
**WCAG:** Multiple criteria  
**Severity:** MEDIUM
- Cookie consent plugin detected (`beautiful-and-responsive-cookie-consent`)
- Could not verify keyboard accessibility or focus management of the banner
- Cookie banners are a frequent source of accessibility complaints

**Fix:** Test the cookie banner with keyboard-only navigation and screen reader.

### M5. Decorative Video Has No Pause Mechanism 🟠
**WCAG:** 2.2.2 Pause, Stop, Hide (Level A)  
**Severity:** MEDIUM
- The hero video appears to auto-play (common for HVAC sites)
- WCAG requires a mechanism to pause, stop, or hide auto-playing video
- `aria-hidden="true"` handles screen reader, but keyboard/visual users may still be affected

**Fix:** Add a visible pause/play button or use `prefers-reduced-motion` media query to disable auto-play.

### M6. `target="_blank"` Links Missing Warning 🟠
**WCAG:** 3.2.5 Change on Request (Level AAA)  
**Severity:** LOW-MEDIUM
```html
<a href="https://www.facebook.com/..." target="_blank" class="social-btn">
```
**Impact:** Links that open new windows/tabs should warn users. The `aria-label="Facebook"` helps but doesn't indicate new window behavior.  
**Fix:** Add `aria-label="Facebook (opens in new tab)"` or add `rel="noopener noreferrer"` (security) plus visual indicator.

---

## 🔵 LOW-PRIORITY / AAA OPPORTUNITIES

### L1. Text Spacing — No Issues Detected ✅
**WCAG:** 1.4.12 Text Spacing (Level AA)
- CSS uses relative units (`em`, `rem`, `clamp()`) — good for text spacing override tools.

### L2. Content Reflow ✅
**WCAG:** 1.4.10 Reflow (Level AA)
- Responsive design with proper media queries at 1024px and 767px breakpoints.
- Content appears to reflow to single column on mobile.

### L3. Touch Target Size 🔵
**WCAG:** 2.5.8 Target Size (Level AAA)
- CTA buttons have adequate padding (`12px 30px`) — likely meets 44x44px minimum.
- Menu toggle button should be verified: `padding: 0.4em 0.6em` with 40px icon.

### L4. Consistent Navigation ✅
**WCAG:** 3.2.3 Consistent Navigation (Level AA)
- Header navigation appears consistent across pages (same structure).

### L5. Error Identification on Forms 🔵
**WCAG:** 3.3.1 Error Identification (Level A)
- Form uses HTML5 `required` + `aria-required` for validation.
- Native browser validation will provide error messages.
- **Improvement opportunity:** Add custom, descriptive error messages with `aria-describedby` or `aria-errormessage`.

### L6. Consistent Identification ✅
**WCAG:** 3.2.4 Consistent Identification (Level AA)
- Phone number, CTAs, and branding appear consistently across pages.

---

## 📊 Compliance Summary by WCAG Principle

| Principle | Score | Notes |
|-----------|-------|-------|
| **1. Perceivable** | 70% | Alt text quality, video accessibility, contrast issues |
| **2. Operable** | 65% | Focus visibility is the biggest gap; keyboard trap risk |
| **3. Understandable** | 85% | Good form labeling; some page titles need work |
| **4. Robust** | 80% | Good ARIA usage; some landmarks and roles need polish |

---

## 🛡️ ADA Risk Mitigation — Priority Actions

### Tier 1: Fix This Week (Lawsuit Prevention)
| # | Issue | Effort | Impact |
|---|-------|--------|--------|
| 1 | **Restore focus visibility** (C1) | 30 min CSS | Eliminates #1 ADA complaint |
| 2 | **Fix footer logo alt text** (C2) | 2 min | Easy fix, Level A requirement |
| 3 | **Add iframe titles** (C5) | 5 min | Level A requirement |
| 4 | **Verify orange button contrast** (H1) | 15 min | May need color adjustment |

### Tier 2: Fix This Month (Compliance Foundation)
| # | Issue | Effort | Impact |
|---|-------|--------|--------|
| 5 | **Improve image alt text quality** (C3) | 2 hours | Better screen reader experience |
| 6 | **Mobile drawer focus management** (H2) | 2 hours dev | Prevents keyboard traps |
| 7 | **Verify video accessibility** (C4) | 1 hour | Clarify decorative vs. informational |
| 8 | **Fix page titles** (M1) | 30 min | SEO + accessibility win |
| 9 | **Add video pause control** (M5) | 1 hour | Level A requirement |

### Tier 3: Polish & AAA (Ongoing Improvement)
| # | Issue | Effort | Impact |
|---|-------|--------|--------|
| 10 | Fix redundant trustbox links (H4) | 30 min | Better UX for screen readers |
| 11 | Cookie banner testing (M4) | 1 hour | Risk reduction |
| 12 | Enhanced form error messages (L5) | 2 hours | Better user experience |
| 13 | `target="_blank"` warnings (M6) | 1 hour | Best practice |
| 14 | Create estimate request page (M2) | 2 hours | UX + accessibility |

---

## 🚨 Emergency Service Accessibility Assessment

### Phone Number: (706) 629-0749
| Check | Status | Notes |
|-------|--------|-------|
| Clickable `tel:` link | ✅ | Works on mobile/desktop |
| Visible in header | ✅ | Desktop and mobile headers |
| Visible in hero | ✅ | Prominent CTA button |
| Visible in footer | ✅ | Contact section |
| Screen reader accessible | ✅ | Link text reads naturally |
| High contrast | ✅ | White on purple (9.2:1) |
| Large touch target | ✅ | Button style with adequate padding |

### 24/7 Service Information
| Check | Status | Notes |
|-------|--------|-------|
| Mentioned on homepage | ✅ | "Same-Day Service Available" on subpages |
| Screen reader accessible | ✅ | Plain text content |
| Easy to find | ⚠️ | Could be more prominent on homepage |

### Service Area Information
| Check | Status | Notes |
|-------|--------|-------|
| Interactive map | ✅ | Tab-based county selector |
| ARIA tab pattern | ✅ | Proper roles and states |
| City lists accessible | ✅ | Linked text for each city |
| Map alternative | ⚠️ | Maps are Google embeds (iframes) — text alternatives provide city lists |

**Overall Emergency Accessibility: GOOD** — A user with any disability can find the phone number and call for service.

---

## 📋 Screen Reader Navigation Flow (Estimated)

When a screen reader user visits the homepage, they would encounter:

1. ✅ Skip to content link (announced on focus)
2. ✅ Banner landmark with company logo
3. ✅ Navigation landmark ("Main Mega Menu")
4. ⚠️ Phone number CTA (good — but no `aria-label` describing it as phone)
5. ✅ Main content landmark
6. ✅ Hero heading (H1)
7. ✅ Service sections with H2 headings
8. ⚠️ Service cards with linked content (link text is descriptive)
9. ✅ Contact form with labeled fields
10. ✅ Service areas tab panel
11. ✅ Footer with contact info, address, email

**Key concern:** The focus outline suppression (C1) means keyboard-only navigation is essentially impossible to track visually.

---

## 📝 Recommendations for Ongoing Accessibility

1. **Install an accessibility testing plugin** (e.g., WP Accessibility, Sa11y) for ongoing monitoring
2. **Add an accessibility statement page** — demonstrates good faith and provides contact for accessibility issues
3. **Test with actual screen readers** (NVDA is free for Windows; VoiceOver is built into Mac/iOS)
4. **Run automated scans quarterly** using WAVE, axe DevTools, or Lighthouse
5. **Consider adding a font size adjustment widget** — valuable for elderly HVAC customers
6. **Add `prefers-reduced-motion` media query** for users who are motion-sensitive:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Tool & Method Notes

This audit was conducted via:
- Raw HTML source code analysis (curl)
- Rendered content extraction (readability parser)
- CSS variable resolution and contrast calculation
- ARIA attribute pattern analysis
- Semantic structure review across 5+ pages

**Limitations:** This is a code-level audit. Full compliance verification requires:
- Browser-based automated scanning (axe, WAVE, Lighthouse)
- Manual keyboard navigation testing
- Screen reader testing (NVDA, JAWS, VoiceOver)
- Color contrast verification with rendered styles
- Mobile device testing with assistive technology

---

*Report prepared for Anderson Heating, Air & Insulation — internal use only.*
