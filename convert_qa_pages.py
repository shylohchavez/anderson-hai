#!/usr/bin/env python3
"""Convert 60 Q&A markdown pages to HTML with Tailwind CSS, schema markup, and FAQ JSON-LD."""

import os
import re
import json
import html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QA_DIR = os.path.join(BASE_DIR, "qa-pages")
FAQ_DIR = os.path.join(BASE_DIR, "faq-schema")
OUT_DIR = BASE_DIR

# Service-specific configuration
SERVICE_CONFIG = {
    "AC Repair": {
        "emoji_hero": "❄️",
        "hero_badge": "24/7 EMERGENCY AC REPAIR",
        "hero_subtitle": "When You Need It Most",
        "keywords_base": "ac repair, air conditioning repair, emergency ac repair, hvac repair",
        "offer_catalog_name": "AC Repair Services",
        "offers": [
            "Emergency AC Repair (24/7)",
            "AC Not Cooling Diagnosis",
            "Refrigerant Leak Repair",
            "Capacitor & Fan Motor Replacement",
            "Ductwork Repairs & Custom Fabrication",
            "Thermostat Repair"
        ],
        "knows_about": ["AC Repair", "Air Conditioning", "Emergency HVAC", "Ductwork", "Refrigerant", "Thermostat Repair"],
        "service_cards": [
            ("🚨", "Emergency AC Repair (24/7)", "AC died at 2am? We're there. No extra charge for nights, weekends, or holidays."),
            ("❄️", "AC Not Cooling", "Expert diagnosis of why your AC isn't keeping up with Georgia heat."),
            ("🔊", "Strange Noises or Smells", "Unusual sounds or odors from your AC? We diagnose and fix the root cause."),
            ("💰", "High Energy Bills", "AC running constantly? We find efficiency problems and fix them."),
            ("🧊", "Refrigerant Leaks", "Leak detection, repair, and proper recharging by certified technicians."),
            ("⚙️", "Capacitor &amp; Fan Motor", "Common failures diagnosed and replaced on the spot — fully stocked trucks."),
        ],
        "breadcrumb_parent": ("HVAC Services", "calhoun-ga-hvac.html"),
        "cta_urgency": "Georgia summers don't wait. When your AC fails at 2am, we're there.",
    },
    "Duct Cleaning": {
        "emoji_hero": "🌬️",
        "hero_badge": "PROFESSIONAL DUCT CLEANING",
        "hero_subtitle": "Breathe Cleaner Air Today",
        "keywords_base": "duct cleaning, air duct cleaning, hvac duct cleaning, ductwork cleaning",
        "offer_catalog_name": "Duct Cleaning Services",
        "offers": [
            "Complete Air Duct Cleaning",
            "Dryer Vent Cleaning",
            "Duct Sanitization & Deodorizing",
            "Duct Inspection & Assessment",
            "Custom Ductwork Fabrication",
            "Duct Sealing & Repair"
        ],
        "knows_about": ["Duct Cleaning", "Air Quality", "HVAC Maintenance", "Ductwork", "Air Filtration", "Ventilation"],
        "service_cards": [
            ("🌬️", "Complete Duct Cleaning", "Full system cleaning removes dust, allergens, and debris from every vent and return."),
            ("🔥", "Dryer Vent Cleaning", "Prevent fire hazards and improve efficiency with professional dryer vent cleaning."),
            ("🦠", "Duct Sanitization", "Kill mold, bacteria, and allergens with professional-grade sanitization treatments."),
            ("🔍", "Duct Inspection", "Camera inspection reveals hidden problems — leaks, blockages, and contamination."),
            ("🔧", "Custom Ductwork", "Our in-house sheet metal shop fabricates perfect replacement ducts on-site."),
            ("💨", "Duct Sealing", "Seal leaky ducts to stop energy waste and improve airflow throughout your home."),
        ],
        "breadcrumb_parent": ("HVAC Services", "calhoun-ga-hvac.html"),
        "cta_urgency": "Dirty ducts mean dirty air. Get your home's air quality tested today.",
    },
    "Ductless Mini-Splits": {
        "emoji_hero": "🏠",
        "hero_badge": "DUCTLESS MINI-SPLIT EXPERTS",
        "hero_subtitle": "Zone Comfort Without Ductwork",
        "keywords_base": "ductless mini-splits, mini split installation, ductless ac, ductless heat pump",
        "offer_catalog_name": "Ductless Mini-Split Services",
        "offers": [
            "Mini-Split Installation",
            "Multi-Zone Mini-Split Systems",
            "Mini-Split Repair & Service",
            "MRCOOL Mini-Split Installation",
            "Samsung Mini-Split Installation",
            "Mini-Split Maintenance Plans"
        ],
        "knows_about": ["Ductless Mini-Splits", "MRCOOL", "Samsung", "Heat Pumps", "Zone Heating", "Zone Cooling"],
        "service_cards": [
            ("🏠", "Single-Zone Mini-Splits", "Perfect for additions, garages, sunrooms, or problem rooms that never get comfortable."),
            ("🏢", "Multi-Zone Systems", "Heat and cool multiple rooms independently with one outdoor unit — maximum control."),
            ("🔧", "Mini-Split Repair", "Expert service on all brands including MRCOOL, Samsung, Trane, and more."),
            ("❄️", "Heating &amp; Cooling", "Mini-splits provide both heating and cooling — one system, year-round comfort."),
            ("⚡", "Energy Efficient", "Up to 40% more efficient than traditional HVAC — lower bills, better comfort."),
            ("🛠️", "Professional Install", "Hundreds of mini-splits installed — we know the right size and placement for your space."),
        ],
        "breadcrumb_parent": ("HVAC Services", "calhoun-ga-hvac.html"),
        "cta_urgency": "Stop fighting with window units. Get real comfort with a ductless mini-split.",
    },
    "HVAC Installation": {
        "emoji_hero": "🏗️",
        "hero_badge": "EXPERT HVAC INSTALLATION",
        "hero_subtitle": "Done Right the First Time",
        "keywords_base": "hvac installation, ac installation, heating installation, new hvac system",
        "offer_catalog_name": "HVAC Installation Services",
        "offers": [
            "Central Air Conditioning Installation",
            "Heat Pump Installation",
            "Furnace Installation",
            "Complete HVAC System Replacement",
            "Custom Ductwork Design & Fabrication",
            "Whole-Home Energy Assessment"
        ],
        "knows_about": ["HVAC Installation", "Heat Pumps", "Air Conditioning", "Furnaces", "Ductwork Design", "Energy Efficiency"],
        "service_cards": [
            ("🏗️", "New HVAC Systems", "Complete system design and installation — we size it right the first time."),
            ("♻️", "System Replacement", "Upgrade your old system for better efficiency, lower bills, and reliable comfort."),
            ("🔥", "Heat Pump Install", "Year-round heating and cooling in one efficient system — our specialty."),
            ("🔧", "Custom Ductwork", "Our in-house sheet metal shop designs and fabricates perfect ductwork for your home."),
            ("📊", "Energy Assessment", "Free whole-home energy audit identifies the best system for YOUR home."),
            ("💰", "Financing Available", "Affordable payment plans make new HVAC systems accessible for every budget."),
        ],
        "breadcrumb_parent": ("HVAC Services", "calhoun-ga-hvac.html"),
        "cta_urgency": "A properly installed HVAC system saves thousands over its lifetime. Get it right.",
    },
    "Indoor Air Quality": {
        "emoji_hero": "🫁",
        "hero_badge": "INDOOR AIR QUALITY EXPERTS",
        "hero_subtitle": "Breathe Better at Home",
        "keywords_base": "indoor air quality, air quality testing, air purification, iaq, home air quality",
        "offer_catalog_name": "Indoor Air Quality Services",
        "offers": [
            "Air Quality Testing & Assessment",
            "Whole-Home Air Purification",
            "UV Light Air Treatment",
            "Humidity Control Systems",
            "Air Filtration Upgrades",
            "Ventilation Improvement"
        ],
        "knows_about": ["Indoor Air Quality", "Air Purification", "UV Treatment", "Humidity Control", "Air Filtration", "Ventilation"],
        "service_cards": [
            ("🫁", "Air Quality Testing", "Professional assessment identifies pollutants, allergens, and contaminants in your home."),
            ("✨", "Air Purification", "Whole-home air purifiers remove 99%+ of airborne particles, viruses, and bacteria."),
            ("☀️", "UV Light Treatment", "UV-C light systems kill mold and bacteria inside your HVAC system 24/7."),
            ("💧", "Humidity Control", "Too humid or too dry? We install systems that keep humidity in the healthy range."),
            ("🔬", "Advanced Filtration", "Upgrade from basic filters to HEPA-grade filtration for hospital-clean air."),
            ("🌬️", "Ventilation Solutions", "Proper ventilation removes stale air and brings in fresh, filtered outdoor air."),
        ],
        "breadcrumb_parent": ("HVAC Services", "calhoun-ga-hvac.html"),
        "cta_urgency": "Your family breathes 20,000+ times a day at home. Make every breath count.",
    },
    "Insulation & Air Sealing": {
        "emoji_hero": "🏡",
        "hero_badge": "INSULATION & AIR SEALING EXPERTS",
        "hero_subtitle": "Lower Bills, Better Comfort",
        "keywords_base": "insulation, air sealing, home insulation, attic insulation, energy efficiency",
        "offer_catalog_name": "Insulation & Air Sealing Services",
        "offers": [
            "Attic Insulation Installation",
            "Crawl Space Insulation",
            "Air Sealing & Weatherization",
            "Blown-In Insulation",
            "Spray Foam Insulation",
            "Free Energy Audit"
        ],
        "knows_about": ["Insulation", "Air Sealing", "Weatherization", "Energy Efficiency", "Attic Insulation", "Spray Foam"],
        "service_cards": [
            ("🏡", "Attic Insulation", "Proper attic insulation is the #1 way to reduce energy bills in Georgia homes."),
            ("🕳️", "Air Sealing", "We find and seal every gap, crack, and hole where conditioned air escapes your home."),
            ("💨", "Blown-In Insulation", "Fast, effective blown-in insulation fills every gap for complete coverage."),
            ("🧪", "Spray Foam", "Premium spray foam insulation provides the highest R-value and creates an air barrier."),
            ("📊", "Free Energy Audit", "BPI-certified auditors identify exactly where your home is losing energy and money."),
            ("🌡️", "Weatherization", "Complete weatherization packages that can cut energy bills by 20-40%."),
        ],
        "breadcrumb_parent": ("Home Services", "index.html"),
        "cta_urgency": "Most Georgia homes lose 30%+ of conditioned air through leaks. Stop paying to cool the outdoors.",
    },
}

# Cities with their nearby cities for area served
CITIES = {
    "Calhoun": ["Adairsville", "Resaca", "Fairmount", "Dalton", "Cartersville", "Rome", "Chatsworth"],
    "Adairsville": ["Calhoun", "Cartersville", "Rome", "Fairmount", "Resaca", "Kingston", "Cassville"],
    "Cartersville": ["Adairsville", "Calhoun", "Rome", "Acworth", "Euharlee", "Kingston", "Cassville"],
    "Chatsworth": ["Dalton", "Calhoun", "Ellijay", "Eton", "Cisco", "Resaca", "Fairmount"],
    "Dalton": ["Chatsworth", "Calhoun", "Resaca", "Tunnel Hill", "Rocky Face", "Varnell", "Ringgold"],
    "Ellijay": ["Chatsworth", "Jasper", "Blue Ridge", "Cherry Log", "East Ellijay", "Calhoun", "Dalton"],
    "Fairmount": ["Calhoun", "Jasper", "Resaca", "Ranger", "Talking Rock", "Chatsworth", "Ellijay"],
    "Jasper": ["Ellijay", "Fairmount", "Ball Ground", "Talking Rock", "Tate", "Marble Hill", "Canton"],
    "Resaca": ["Calhoun", "Dalton", "Fairmount", "Adairsville", "Ranger", "Sugar Valley", "Chatsworth"],
    "Rome": ["Cartersville", "Adairsville", "Calhoun", "Cedartown", "Armuchee", "Silver Creek", "Shannon"],
}


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}, content
    fm_text = match.group(1)
    body = content[match.end():]
    fm = {}
    for line in fm_text.strip().split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip().strip('"')
    return fm, body


def md_to_html_sections(body, city, service):
    """Parse markdown body into Q&A pairs."""
    questions = []
    current_q = None
    current_a_lines = []

    for line in body.split('\n'):
        if line.startswith('### '):
            if current_q:
                questions.append((current_q, '\n'.join(current_a_lines).strip()))
            current_q = line[4:].strip()
            current_a_lines = []
        elif current_q is not None and not line.startswith('## ') and not line.startswith('# '):
            current_a_lines.append(line)
        elif line.startswith('## ') and current_q:
            questions.append((current_q, '\n'.join(current_a_lines).strip()))
            current_q = None
            current_a_lines = []

    if current_q:
        questions.append((current_q, '\n'.join(current_a_lines).strip()))

    return questions


def load_faq_schema(service_slug, city_slug):
    """Load FAQ JSON-LD from faq-schema directory."""
    faq_file = os.path.join(FAQ_DIR, f"{service_slug}-{city_slug}-faq.json")
    if os.path.exists(faq_file):
        with open(faq_file, 'r') as f:
            return json.load(f)
    return None


def service_to_slug(service):
    """Convert service name to URL slug."""
    return service.lower().replace(' & ', '-').replace(' ', '-')


def generate_html(fm, body, faq_schema):
    """Generate full HTML page from parsed markdown data."""
    city = fm.get('city', 'Calhoun')
    service = fm.get('service', 'AC Repair')
    title = fm.get('title', f'{service} in {city} GA')
    meta_desc = fm.get('meta_description', f'Expert {service.lower()} in {city} GA.')

    service_slug = service_to_slug(service)
    city_slug = city.lower().replace(' ', '-')
    filename = f"qa-{service_slug}-{city_slug}-ga.html"
    canonical_url = f"https://johnandersonservice.com/{filename}"

    config = SERVICE_CONFIG.get(service, SERVICE_CONFIG["AC Repair"])
    nearby = CITIES.get(city, ["Calhoun", "Dalton", "Rome", "Cartersville"])
    keywords = ", ".join([f"{kw} {city.lower()} ga" for kw in config["keywords_base"].split(", ")])

    # Parse Q&A from markdown
    questions = md_to_html_sections(body, city, service)

    # Build Q&A HTML
    qa_html = ""
    for q, a in questions:
        # Convert markdown formatting in answer
        a_html = a.replace('\n\n', '</p><p class="text-gray-600 mt-2">')
        a_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', a_html)
        a_html = a_html.replace('{city}', city)
        if a_html.strip():
            qa_html += f"""            <div class="border rounded-2xl p-6">
                <h3 class="font-bold text-lg mb-2">{html.escape(q)}</h3>
                <p class="text-gray-600">{a_html}</p>
            </div>
"""

    # Build service cards HTML
    cards_html = ""
    for emoji, card_title, card_desc in config["service_cards"]:
        cards_html += f"""                <div class="service-card p-8 bg-white border rounded-3xl">
                    <div class="text-3xl mb-4">{emoji}</div>
                    <h3 class="font-bold text-xl mb-2">{card_title}</h3>
                    <p class="text-sm text-gray-600">{card_desc}</p>
                </div>
"""

    # Build area served schema
    area_served = [{"@type": "City", "name": city, "addressRegion": "GA"}]
    for nc in nearby[:6]:
        area_served.append({"@type": "City", "name": nc, "addressRegion": "GA"})

    # Build offers
    offers = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": o}} for o in config["offers"]]

    # Business schema
    business_schema = {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "HVACBusiness"],
        "name": "Anderson Heating, Air & Insulation",
        "alternateName": "John Anderson Service Company, Inc.",
        "legalName": "John Anderson Service Company, Inc.",
        "slogan": "The Paws-itive Choice",
        "description": f"Expert {service.lower()} in {city} GA. BPI Certified, 48 years of trusted service. Call (706) 629-0749.",
        "url": canonical_url,
        "telephone": "(706) 629-0749",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "519 Pine Street",
            "addressLocality": "Calhoun",
            "addressRegion": "GA",
            "postalCode": "30701",
            "addressCountry": "US"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "34.5029",
            "longitude": "-84.9511"
        },
        "openingHours": "Mo-Fr 07:00-17:00, Sa 08:00-12:00",
        "priceRange": "$$",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": "632"
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": config["offer_catalog_name"],
            "itemListElement": offers
        },
        "foundingDate": "1978-01",
        "founder": {"@type": "Person", "name": "John Anderson"},
        "knowsAbout": config["knows_about"],
        "areaServed": area_served,
        "sameAs": [
            "https://www.facebook.com/AndersonHeatAirCo/",
            "https://www.instagram.com/andersonheatairco/",
            "https://www.youtube.com/@AndersonHeatAirCo",
            "https://www.linkedin.com/company/anderson-heating-air-insulation"
        ],
        "potentialAction": {
            "@type": "CallAction",
            "target": "tel:+17066290749"
        },
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://johnandersonservice.com"},
                {"@type": "ListItem", "position": 2, "name": config["breadcrumb_parent"][0], "item": f"https://johnandersonservice.com/{config['breadcrumb_parent'][1]}"},
                {"@type": "ListItem", "position": 3, "name": f"{service} {city} GA", "item": canonical_url}
            ]
        }
    }

    # FAQ schema - use pre-built or generate from Q&A
    if faq_schema:
        faq_json = json.dumps(faq_schema, indent=6)
    else:
        faq_entities = []
        for q, a in questions[:8]:
            a_clean = re.sub(r'\*\*(.+?)\*\*', r'\1', a).replace('{city}', city).replace('\n', ' ').strip()
            if a_clean:
                faq_entities.append({
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a_clean
                    }
                })
        faq_schema_gen = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities
        }
        faq_json = json.dumps(faq_schema_gen, indent=6)

    # Nearby cities links
    nearby_links = ""
    for nc in nearby[:5]:
        nc_slug = nc.lower().replace(' ', '-')
        nearby_links += f'<a href="{nc_slug}-ga-hvac.html" class="text-anderson-purple hover:underline">{nc} GA</a>, '
    nearby_links = nearby_links.rstrip(', ')

    # Service-specific internal links
    internal_links_html = ""
    other_services = [s for s in SERVICE_CONFIG.keys() if s != service]
    for os_name in other_services[:4]:
        os_slug = service_to_slug(os_name)
        internal_links_html += f'                <a href="qa-{os_slug}-{city_slug}-ga.html" class="text-anderson-purple hover:underline">{os_name} in {city} GA</a>\n'

    service_escaped = html.escape(service)
    city_escaped = html.escape(city)

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="canonical" href="{canonical_url}" />
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(meta_desc)}">
    <meta name="keywords" content="{html.escape(keywords)}">
    <meta property="og:title" content="{html.escape(title)}">
    <meta property="og:description" content="{html.escape(meta_desc)}">
    <meta property="og:image" content="https://shylohchavez.github.io/anderson-hai/images/logo.png">
    <meta property="og:url" content="{canonical_url}">
    <meta name="twitter:card" content="summary_large_image">
    <style>
        .brand-purple {{ color: #4A1C6B; }}
        .brand-orange {{ color: #FF6B00; }}
        .nav-link {{ transition: color 0.2s; }}
        .nav-link:hover {{ color: #FF6B00; }}
        .cta-button {{ transition: all 0.3s ease; }}
        .cta-button:hover {{ transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1); }}
        .service-card {{ transition: transform 0.3s ease, box-shadow 0.3s ease; }}
        .service-card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1); }}
    </style>
    <!-- HVACBusiness + LocalBusiness Schema -->
    <script type="application/ld+json">
    {json.dumps(business_schema, indent=4)}
    </script>
    <!-- FAQ Schema -->
    <script type="application/ld+json">
    {faq_json}
    </script>
</head>
<body class="bg-white text-gray-900 font-sans">
    <!-- Navigation -->
    <nav class="bg-white border-b sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-20">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-anderson-purple rounded-full flex items-center justify-center text-white text-xl">🐾</div>
                    <div>
                        <div class="font-bold text-xl brand-purple">Anderson HAI</div>
                        <div class="text-xs text-gray-500 -mt-1">The Paws-itive Choice</div>
                    </div>
                </div>
                <div class="hidden md:flex items-center gap-8 text-sm font-medium">
                    <a href="index.html" class="nav-link">Home</a>
                    <a href="service-area.html" class="nav-link">Service Area</a>
                    <a href="about.html" class="nav-link">About Us</a>
                    <a href="reviews.html" class="nav-link">Reviews (632+)</a>
                    <a href="contact.html" class="nav-link">Contact</a>
                </div>
                <div class="flex items-center gap-4">
                    <a href="tel:+17066290749" class="hidden sm:block text-anderson-purple font-semibold hover:underline">(706) 629-0749</a>
                    <a href="contact.html" class="bg-anderson-purple text-white px-6 py-2 rounded-xl text-sm font-semibold cta-button">Get Free Estimate</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero -->
    <section class="bg-gradient-to-br from-anderson-purple to-anderson-purple/90 text-white py-20">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div class="inline-flex items-center gap-2 bg-white/20 px-4 py-1 rounded-full text-sm mb-6">
                <span class="w-2 h-2 bg-anderson-orange rounded-full animate-pulse"></span>
                {config["hero_badge"]} IN {city_escaped.upper()} GA
            </div>
            <h1 class="text-5xl md:text-6xl font-bold tracking-tight mb-6">
                {service_escaped} in {city_escaped}, Georgia — {config["hero_subtitle"]}
            </h1>
            <p class="text-xl max-w-3xl mx-auto mb-8 text-white/90">
                Anderson Heating, Air &amp; Insulation has been the trusted name for {service_escaped.lower()} in {city_escaped} and Northwest Georgia since 1978. Fast, honest, expert service — not a sales pitch.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="tel:+17066290749" class="inline-flex items-center justify-center gap-3 bg-anderson-orange text-white px-10 py-4 rounded-2xl font-bold text-lg cta-button">
                    📞 Call Now: (706) 629-0749
                </a>
                <a href="contact.html" class="inline-flex items-center justify-center gap-3 bg-white text-anderson-purple px-10 py-4 rounded-2xl font-bold text-lg border-2 border-white cta-button">
                    Request Free Estimate
                </a>
            </div>
            <p class="mt-6 text-sm text-white/70">Available 24/7 for emergencies • Same-day service available 🐾</p>
        </div>
    </section>

    <!-- Trust Bar -->
    <div class="bg-gray-50 border-b py-4">
        <div class="max-w-6xl mx-auto px-4 flex flex-wrap justify-center gap-x-8 gap-y-2 text-sm text-center">
            <div class="flex items-center gap-2"><span class="text-anderson-orange">★</span> <strong>632+ Google Reviews (4.8 Stars)</strong></div>
            <div>BPI Certified Technicians</div>
            <div>48 Years in Business (Since 1978)</div>
            <div>In-House Custom Sheet Metal Shop</div>
            <div>Serving {city_escaped} &amp; NW Georgia</div>
        </div>
    </div>

    <!-- Q&A Section -->
    <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="text-center mb-12">
            <div class="text-anderson-orange font-semibold tracking-widest text-sm mb-3">YOUR QUESTIONS ANSWERED</div>
            <h2 class="text-4xl font-bold">{service_escaped} Questions from {city_escaped} Homeowners</h2>
            <p class="text-gray-600 mt-3 max-w-2xl mx-auto">Get answers to the most common {service_escaped.lower()} questions from homeowners in {city_escaped}, GA.</p>
        </div>
        <div class="space-y-6 max-w-3xl mx-auto">
{qa_html}        </div>
    </section>

    <!-- Services -->
    <section class="bg-white py-16 border-t">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-12">
                <div class="text-anderson-orange font-semibold tracking-widest text-sm mb-3">COMPREHENSIVE {service_escaped.upper()}</div>
                <h2 class="text-4xl font-bold">Our {service_escaped} Services in {city_escaped}</h2>
                <p class="text-gray-600 mt-3 max-w-2xl mx-auto">Anderson Heating, Air &amp; Insulation provides complete {service_escaped.lower()} services for {city_escaped} and all of Northwest Georgia.</p>
            </div>
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
{cards_html}            </div>
        </div>
    </section>

    <!-- Why Choose Anderson -->
    <section class="bg-gray-50 py-16">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div>
                    <div class="text-anderson-orange font-semibold tracking-widest text-sm mb-3">WHY ANDERSON</div>
                    <h2 class="text-4xl font-bold tracking-tight mb-6">Why {city_escaped} Homeowners Choose Anderson</h2>
                    <div class="prose prose-lg text-gray-600">
                        <p>Most companies just swap the box. <strong>We diagnose the real problem and fix the whole house.</strong> Our BPI-certified team looks at insulation, air sealing, and HVAC together — because they all work as one system.</p>
                    </div>
                    <ul class="mt-6 space-y-3 text-sm">
                        <li class="flex gap-3"><span class="text-anderson-orange font-bold">→</span> <strong>48 Years Local Expertise</strong> — Serving NW Georgia since 1978</li>
                        <li class="flex gap-3"><span class="text-anderson-orange font-bold">→</span> <strong>In-House Custom Sheet Metal Shop</strong> — Perfect ductwork fabricated on-site</li>
                        <li class="flex gap-3"><span class="text-anderson-orange font-bold">→</span> <strong>Whole-Home Approach</strong> — We don't just "swap the box"</li>
                        <li class="flex gap-3"><span class="text-anderson-orange font-bold">→</span> <strong>BPI Certified</strong> — Only BPI-certified HVAC company in the area</li>
                        <li class="flex gap-3"><span class="text-anderson-orange font-bold">→</span> <strong>632+ Five-Star Reviews</strong> — Real customers, real results</li>
                        <li class="flex gap-3"><span class="text-anderson-orange font-bold">→</span> <strong>Same-Day Service</strong> — Most jobs completed same day</li>
                    </ul>
                </div>
                <div class="bg-white p-8 rounded-3xl border text-center">
                    <div class="text-6xl mb-4">{config["emoji_hero"]}</div>
                    <div class="font-bold text-xl mb-2">Get {service_escaped} in {city_escaped} Today</div>
                    <p class="text-sm text-gray-600">{config["cta_urgency"]}</p>
                    <div class="mt-6">
                        <a href="tel:+17066290749" class="inline-flex items-center justify-center bg-anderson-purple text-white px-8 py-3 rounded-xl font-bold text-sm cta-button">Call (706) 629-0749 Now</a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Service Area -->
    <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="grid md:grid-cols-2 gap-12 items-center">
            <div>
                <h2 class="text-3xl font-bold mb-4">{service_escaped} Service Area</h2>
                <p class="text-gray-600 mb-6">We provide {service_escaped.lower()} service throughout {city_escaped} and all of Northwest Georgia, including {', '.join(nearby[:5])}, and surrounding communities.</p>
                <div class="bg-white p-6 rounded-2xl border">
                    <div class="font-semibold mb-2">📍 Our Home Base</div>
                    <div class="text-sm">519 Pine Street<br>Calhoun, GA 30701</div>
                    <div class="mt-3 text-sm"><strong>Hours:</strong> 7am-5pm Mon-Fri | 8am-12pm Sat | 24/7 Emergency</div>
                    <a href="https://maps.google.com/?q=519+Pine+Street+Calhoun+GA+30701" target="_blank" class="mt-4 inline-block text-anderson-orange text-sm font-semibold hover:underline">Open in Google Maps →</a>
                </div>
            </div>
            <div class="bg-gray-50 p-8 rounded-3xl border text-center">
                <div class="text-anderson-orange text-5xl mb-4">★★★★★</div>
                <div class="font-bold text-2xl mb-2">4.8 Stars</div>
                <div class="text-gray-600 mb-4">632+ Verified Google Reviews</div>
                <a href="reviews.html" class="text-anderson-purple font-semibold hover:underline text-sm">Read Our Reviews →</a>
            </div>
        </div>
    </section>

    <!-- Final CTA -->
    <section class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center border-t">
        <h2 class="text-4xl font-bold tracking-tight mb-4">Need {service_escaped} in {city_escaped} GA?</h2>
        <p class="text-xl text-gray-600 mb-8">Call the local experts who have been serving {city_escaped} and Northwest Georgia since 1978. Same-day service available.</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="tel:+17066290749" class="inline-flex items-center justify-center gap-3 bg-anderson-purple text-white px-10 py-4 rounded-2xl font-bold text-lg cta-button">
                Call (706) 629-0749 Now
            </a>
            <a href="contact.html" class="inline-flex items-center justify-center gap-3 border-2 border-anderson-purple text-anderson-purple px-10 py-4 rounded-2xl font-bold text-lg hover:bg-anderson-purple hover:text-white cta-button">
                Request Free Estimate
            </a>
        </div>
        <p class="mt-8 text-sm text-gray-500">Anderson Heating, Air &amp; Insulation — The Paws-itive Choice 🐾<br>
        Trade name of John Anderson Service Company, Inc. • Est. 1978 • Serving {city_escaped} and NW Georgia</p>
    </section>

    <!-- Internal Links -->
    <div class="max-w-5xl mx-auto px-4 pb-12">
        <div class="p-6 bg-gray-50 rounded-lg">
            <h3 class="text-xl font-bold mb-4">More Services in {city_escaped} GA</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm mb-6">
{internal_links_html}            </div>
            <h3 class="text-xl font-bold mb-4">We Also Serve Nearby Cities</h3>
            <p class="text-gray-700">Anderson Heating, Air &amp; Insulation proudly serves {nearby_links} and all of Northwest Georgia. <a href="service-area.html" class="text-anderson-purple hover:underline">View full service area</a>.</p>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-anderson-purple text-white/80 text-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-y-10">
                <div>
                    <div class="flex items-center gap-3 mb-4">
                        <div class="w-9 h-9 bg-white/20 rounded-full flex items-center justify-center text-lg">🐾</div>
                        <div class="font-bold text-white">Anderson HAI</div>
                    </div>
                    <p class="text-xs">The Paws-itive Choice for home comfort since 1978.</p>
                </div>
                <div>
                    <div class="font-semibold text-white mb-3">Contact</div>
                    <div>519 Pine Street<br>Calhoun, GA 30701</div>
                    <a href="tel:+17066290749" class="block mt-1 text-white font-medium">(706) 629-0749</a>
                    <a href="contact.html" class="block text-anderson-orange hover:underline">Request Estimate</a>
                </div>
                <div>
                    <div class="font-semibold text-white mb-3">Services</div>
                    <div class="space-y-1 text-xs">
                        <div>HVAC Repair &amp; Install</div>
                        <div>Heat Pumps &amp; Mini-Splits</div>
                        <div>Insulation &amp; Weatherization</div>
                        <div>Duct Cleaning &amp; IAQ</div>
                        <div>Custom Sheet Metal</div>
                        <div>Energy Audits</div>
                    </div>
                </div>
                <div>
                    <div class="font-semibold text-white mb-3">Company</div>
                    <div class="space-y-1 text-xs">
                        <a href="about.html" class="block hover:text-white">About Us</a>
                        <a href="reviews.html" class="block hover:text-white">632+ Google Reviews</a>
                        <a href="financing.html" class="block hover:text-white">Financing &amp; Discounts</a>
                        <a href="service-area.html" class="block hover:text-white">Service Area</a>
                        <a href="careers.html" class="block hover:text-white">Careers</a>
                    </div>
                </div>
            </div>
            <div class="mt-8 flex justify-center gap-6 text-sm">
                <a href="https://www.facebook.com/AndersonHeatAirCo/" class="hover:text-white">Facebook</a>
                <a href="https://www.instagram.com/andersonheatairco/" class="hover:text-white">Instagram</a>
                <a href="https://www.youtube.com/@AndersonHeatAirCo" class="hover:text-white">YouTube</a>
                <a href="https://www.linkedin.com/company/anderson-heating-air-insulation" class="hover:text-white">LinkedIn</a>
            </div>
            <div class="border-t border-white/20 mt-12 pt-8 text-xs flex flex-col md:flex-row justify-between items-center gap-4">
                <div>&copy; 2026 Anderson Heating, Air &amp; Insulation. John Anderson Service Company, Inc. est. January 1978. All rights reserved.</div>
                <div class="text-anderson-orange">The Paws-itive Choice 🐾</div>
            </div>
        </div>
    </footer>
</body>
</html>"""

    return filename, page_html


def update_sitemap(new_files):
    """Add new URLs to sitemap.xml."""
    sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
    with open(sitemap_path, 'r') as f:
        content = f.read()

    # Build new entries
    new_entries = ""
    for filename in sorted(new_files):
        new_entries += f"""  <url>
    <loc>https://johnandersonservice.com/{filename}</loc>
    <lastmod>2026-05-15</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
"""

    # Insert before closing tag
    content = content.replace("</urlset>", new_entries + "</urlset>")

    with open(sitemap_path, 'w') as f:
        f.write(content)


def main():
    md_files = sorted([f for f in os.listdir(QA_DIR) if f.endswith('.md')])
    print(f"Found {len(md_files)} markdown files to convert")

    new_files = []
    for md_file in md_files:
        md_path = os.path.join(QA_DIR, md_file)
        with open(md_path, 'r') as f:
            content = f.read()

        fm, body = parse_frontmatter(content)
        city = fm.get('city', 'Unknown')
        service = fm.get('service', 'Unknown')

        # Load FAQ schema
        service_slug = service_to_slug(service)
        city_slug = city.lower().replace(' ', '-')
        faq_schema = load_faq_schema(service_slug, city_slug)

        filename, page_html = generate_html(fm, body, faq_schema)

        out_path = os.path.join(OUT_DIR, filename)
        with open(out_path, 'w') as f:
            f.write(page_html)

        new_files.append(filename)
        print(f"  ✅ {md_file} → {filename}")

    # Update sitemap
    update_sitemap(new_files)
    print(f"\n✅ Sitemap updated with {len(new_files)} new URLs")
    print(f"✅ All {len(new_files)} Q&A pages converted successfully!")


if __name__ == "__main__":
    main()
