# Q&A Pages — How to Make Them Actually Different (Not Just City-Name Swaps)

## The honest problem

You have 60 Q&A pages (six service types × ten cities — `qa-ac-repair-calhoun-ga.html`, `qa-ac-repair-dalton-ga.html`, and so on). Right now they are ~94% identical. Only the city name changes. There's even a templating bug — the Dalton AC repair page says "Our service area includes **Dalton, Dalton,** Rome, Cartersville..." because the template doesn't notice when the city already appears in the service list.

Google's "Helpful Content" system and AI search engines (ChatGPT, Perplexity, Claude) both penalize this pattern. They call it "scaled content" — pages produced at scale with little human value. The result is "Discovered, not indexed" in Google Search Console: the pages are seen but never shown to users.

Your instinct that "we differentiated them a little but not enough" is exactly right. The fix isn't to delete these pages — they're great SEO real estate **if** they earn it. The fix is to put real local knowledge in each one.

---

## What "real differentiation" looks like

For each city, every Q&A page should reference at least 2-3 things that are **only true of that city**. Examples:

### Calhoun, GA
- Sits in the Oostanaula River valley — higher summer humidity than mountain communities, drives oversized AC selection mistakes
- Older housing stock along Court Street and historic district often has retrofitted HVAC with undersized return ducts
- Newer subdivisions (e.g., near GA-225) tend to be 1990s-2010s spec homes with envelope leakage issues
- Gordon County building code specifics
- Mention nearby landmarks: Anderson HQ is at 519 Pine Street, walking distance from downtown Calhoun

### Dalton, GA
- Carpet capital of the world — high indoor dust loads from carpet manufacturing residue affect filter life and IAQ
- Mill homes (older) vs. newer subdivisions east of I-75 have very different HVAC needs
- Whitfield County's higher commercial density means more drive-by service competition (mention "local, family-owned" hard)
- Distance from Calhoun HQ: 20 minutes north on I-75

### Rome, GA
- Three-river city (Etowah + Oostanaula + Coosa) — extremely humid summers, dehumidification matters more here than other markets
- Lots of historic homes (Between the Rivers, Battery Hill) with retrofitted HVAC, often undersized ductwork
- Berry College and Shorter University area: high-end homes, often want zoning systems
- Floyd County propane is more common in rural areas — fuel-flexible HVAC matters
- Distance from Calhoun: 30 minutes south-southwest

### Cartersville, GA
- Closer to Atlanta sprawl — much more new construction (2010s+ subdivisions like Allatoona Landing, Aviary)
- These newer homes often have 2-stage AC undersized for the actual cooling load due to envelope leakage
- Bartow County permit requirements
- Distance from Calhoun: 35 minutes south
- Local mention: Allatoona Lake area has many vacation/second homes with seasonal HVAC quirks

### Jasper, GA / Pickens County
- Mountain elevation (~1,500 ft) — significantly cooler summers than valley markets, **cold-climate heat pump territory**
- Cold-snap winters (sub-20°F nights) require careful heat pump sizing or dual-fuel systems
- Many vacation homes / part-time occupancy → freeze-protection winterization matters
- Distance from Calhoun: 45 minutes east

### Ellijay, GA / Gilmer County
- Mountains, similar to Jasper but more remote
- Higher elevation = ice/snow events; HVAC outdoor units need elevated pads
- Lots of cabins and second homes
- Apple country — agricultural humidity patterns differ
- Distance from Calhoun: 60 minutes east

### Adairsville, GA
- Bartow County, just south of Calhoun on I-75
- Rural-to-suburban transition zone
- Historic Western & Atlantic Railroad town — older central business district with 1900s commercial buildings
- Distance from Calhoun: 15 minutes south

### Chatsworth, GA / Murray County
- Murray County, north of Dalton
- Mountain proximity (Cohutta range) — cooler summers
- Less commercial development = longer travel for service
- Distance from Calhoun: 25 minutes northeast

### Fairmount, GA
- Small Gordon County town
- Rural homes, often older, propane heat common
- Distance from Calhoun: 15 minutes east

### Resaca, GA
- Battlefield town, Gordon/Whitfield county line
- Mix of older homes and new construction along I-75 corridor
- Distance from Calhoun: 10 minutes north

---

## The recommended rewrite pattern for each Q&A page

Each Q&A page has six question/answer pairs. For each city, rewrite the answers so that:

1. **At least 2 answers reference something city-specific** from the list above (climate, building stock, neighborhood, landmark, distance from HQ)
2. **The "Is service available in [City]?" answer** mentions the actual driving time and a real route (e.g., "We're 20 minutes south on I-75 from Dalton — most Dalton service calls are dispatched same morning")
3. **The "best company near [City]" answer** mentions at least one specific local thing — a neighborhood, a project, a local building characteristic — instead of generic "we serve the area"
4. **The pricing answer** can stay general (don't fabricate prices) but should mention that travel/parts costs may differ slightly in farther markets (Ellijay, Jasper) due to drive time

### Example: "How long does AC repair take in [City]?"

**Current (template, same on every page):**
> Most ac repair jobs in Calhoun take 2-6 hours depending on complexity. Simple repairs are often completed the same day...

**Differentiated for Dalton:**
> Most AC repair jobs in Dalton take 2-6 hours. Because Dalton is 20 minutes north of our Calhoun headquarters on I-75, we dispatch the same morning for most calls — our trucks roll out by 8 AM. Older mill homes in central Dalton sometimes take longer because of cramped utility closets and original 1960s-70s ductwork; newer subdivisions east of I-75 are usually quicker. Simple capacitor or contactor swaps are typically same-day...

**Differentiated for Jasper:**
> Most AC repair jobs in Jasper take 2-6 hours. We're 45 minutes east in the mountains from our Calhoun HQ, so we batch Pickens County calls in the morning to keep travel efficient. Mountain homes often have heat pumps rather than straight AC, which adds diagnostic complexity — we carry the right heat pump parts on every Jasper-bound truck. Vacation homes in the area sometimes need an extra hour for system commissioning because they sit unused for months between visits...

---

## Order of operations to rewrite all 60 pages

You can't rewrite all 60 at once without it becoming a content sweatshop. Here's the order that gets the most SEO value fastest:

### Wave 1 (week 1-2 after launch): Top 4 cities × 6 services = 24 pages
Calhoun, Dalton, Rome, Cartersville. These are your highest-search-volume markets.

### Wave 2 (week 3-4): Mountain markets × 6 services = 12 pages
Jasper, Ellijay. Cold-climate heat pump content is distinctive — easy wins here.

### Wave 3 (week 5+): Smaller markets × 6 services = 24 pages
Adairsville, Chatsworth, Fairmount, Resaca.

---

## Honest tradeoff

If you don't want to write all 60, you have two cleaner options:

### Option A: Keep only the top 4 cities' Q&A pages
Delete `qa-*-jasper-ga.html`, `qa-*-ellijay-ga.html`, `qa-*-adairsville-ga.html`, `qa-*-chatsworth-ga.html`, `qa-*-fairmount-ga.html`, `qa-*-resaca-ga.html`. Redirect them to the main service page for that service. That's 36 pages gone, 24 remain — focus the content investment.

### Option B: Consolidate to one "FAQ" page per service
Instead of 10 cities × 6 services = 60 pages, have 6 pages — one per service — with a "Frequently Asked Questions" section that handles all cities by listing city-specific notes inline. Loses some long-tail SEO but eliminates duplicate content risk entirely.

### Option C (most work, most reward)
Rewrite all 60 with real local content per the pattern above. This is what gets you the SEO dominance in every city.

---

## What I'd recommend

**Option C, prioritized by Wave 1.** Here's why: the duplicate-content risk on the current pages is real and gets worse as the site ages. But the URL slugs (`qa-ac-repair-calhoun-ga.html`) are perfect long-tail SEO real estate that you don't want to delete. The right move is to invest in the content.

Realistically that means hiring a content writer (or me, if you want — I can rewrite them with the local knowledge above as input) for ~30-60 minutes per page once the local-knowledge research is done.

Want me to rewrite the Wave 1 set (24 pages: AC repair, duct cleaning, ductless mini-splits, HVAC installation, indoor air quality, insulation & air sealing — across Calhoun, Dalton, Rome, Cartersville) as a starting point? That would prove out the pattern before committing to the whole 60.
