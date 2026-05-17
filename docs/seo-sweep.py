#!/usr/bin/env python3
"""
Anderson HAI Full SEO Sweep — 2026-05-14
Handles: title/meta optimization, FAQPage schema injection, emergency pages,
partners page, 404 redirects, internal linking, and schema verification.
"""
import os, re, sys

SITE = os.path.expanduser("~/.hermes/shared/anderson-website")

def read_file(path):
    with open(os.path.join(SITE, path), 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(os.path.join(SITE, path), 'w', encoding='utf-8') as f:
        f.write(content)

def replace_title(filename, old_title, new_title):
    content = read_file(filename)
    old = f"<title>{old_title}</title>"
    new = f"<title>{new_title}</title>"
    if old in content:
        content = content.replace(old, new)
        write_file(filename, content)
        return True
    return False

# ============================================================
# PHASE 1: Title/Meta Optimization
# ============================================================
print("=== PHASE 1: Title/Meta Optimization ===")

title_updates = {
    'index.html': (
        'Anderson Heating, Air & Insulation | Anderson HAI',
        '#1 HVAC Company Calhoun GA | AC Repair, Heating & Insulation Since 1978 | Anderson HAI'
    ),
    'about.html': (
        'About Anderson Heating, Air & Insulation | Anderson HAI',
        'About Anderson Heating, Air & Insulation | Family-Owned Since 1978 | Calhoun GA'
    ),
    'contact.html': (
        'Contact Anderson Heating, Air & Insulation | Anderson HAI',
        'Contact Anderson HAI | Call (706) 629-0749 | Free HVAC Estimates Calhoun GA'
    ),
    'reviews.html': (
        '632+ Google Reviews | Anderson HAI',
        '632+ Google Reviews ★4.8 | Anderson Heating, Air & Insulation | Calhoun GA HVAC'
    ),
    'financing.html': (
        'Financing &amp; Discounts | Anderson HAI',
        'HVAC Financing & Senior/Military Discounts | Anderson HAI Calhoun GA'
    ),
    'service-area.html': (
        'Service Area | Anderson HAI',
        'HVAC Service Area | Calhoun, Dalton, Rome, Cartersville & NW Georgia | Anderson HAI'
    ),
    'maintenance-plan.html': (
        'Maintenance Plans | Anderson HAI',
        'HVAC Maintenance Plans Calhoun GA | Preventive AC & Heating Service | Anderson HAI'
    ),
    'emergency-ac-repair.html': (
        'Calhoun GA HVAC | Anderson HAI',
        'Emergency AC Repair Calhoun GA | 24/7 Same-Day Service | Anderson HAI (706) 629-0749'
    ),
    # City pages optimized with top Semrush keywords
    'calhoun-ga.html': (
        'HVAC in Calhoun GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)',
        'HVAC Calhoun GA | AC Repair, Heating & Insulation | 48 Years, 632+ Reviews | Anderson HAI'
    ),
    'dalton-ga.html': (
        'HVAC in Dalton GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)',
        'HVAC Dalton GA | AC Repair & Heating Services | Same-Day Service | Anderson HAI (706) 629-0749'
    ),
    'rome-ga.html': (
        'HVAC in Rome GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)',
        'HVAC Rome GA | AC Repair & Furnace Service | 24/7 Emergency Available | Anderson HAI'
    ),
    'cartersville-ga.html': (
        'HVAC in Cartersville GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)',
        'HVAC Cartersville GA | Air Conditioning & Heating Repair | BPI Certified | Anderson HAI'
    ),
    'adairsville-ga.html': (
        'HVAC in Adairsville GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)',
        'HVAC Adairsville GA | AC Repair & Heating | Trusted Since 1978 | Anderson HAI'
    ),
    'chatsworth-ga.html': (
        'HVAC in Chatsworth GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)',
        'HVAC Chatsworth GA | AC Repair, Heat Pumps & Insulation | Anderson HAI (706) 629-0749'
    ),
    'jasper-ga.html': (
        'HVAC in Jasper GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)',
        'HVAC Jasper GA | Air Conditioning & Furnace Repair | 24/7 Emergency | Anderson HAI'
    ),
    'ellijay-ga.html': (
        'HVAC in Ellijay GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)',
        'HVAC Ellijay GA | AC Repair & Heat Pump Installation | Serving Gilmer County | Anderson HAI'
    ),
    'fairmount-ga.html': (
        'HVAC in Fairmount GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)',
        'HVAC Fairmount GA | AC Repair & Heating Service | Family-Owned Since 1978 | Anderson HAI'
    ),
    'resaca-ga.html': (
        'HVAC in Resaca GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)',
        'HVAC Resaca GA | AC Repair & Heating | Minutes From Our Calhoun Shop | Anderson HAI'
    ),
}

title_count = 0
for fname, (old, new) in title_updates.items():
    if replace_title(fname, old, new):
        title_count += 1
        print(f"  ✓ {fname}")
    else:
        print(f"  ⚠ {fname} - title not found (may already be updated)")

print(f"  Updated {title_count} titles.\n")

# ============================================================
# PHASE 2: FAQPage Schema Injection on city pages
# ============================================================
print("=== PHASE 2: FAQPage Schema Injection ===")

city_faqs = {
    'chatsworth-ga.html': {
        'city': 'Chatsworth',
        'county': 'Murray County',
        'faqs': [
            ("Do you offer same-day HVAC repair in Chatsworth GA?", "Yes — Anderson provides priority same-day AC and heating repair service to Chatsworth and Murray County homes. Call (706) 629-0749 for emergency service."),
            ("How far is Anderson from Chatsworth?", "Our Calhoun shop is just 20 minutes from Chatsworth. We serve Murray County daily with fast response times."),
            ("Does Anderson install mini-splits in Chatsworth?", "Absolutely. We specialize in ductless mini-split and heat pump installations perfect for Chatsworth mountain homes and additions."),
            ("Are you BPI certified for Chatsworth homes?", "Yes — our BPI-certified technicians perform whole-home energy audits and insulation upgrades for Chatsworth homeowners."),
            ("What HVAC brands do you install in Chatsworth?", "We install Trane, MRCOOL, Samsung, and other top brands. Our in-house sheet metal shop means custom ductwork fabricated locally."),
        ]
    },
    'jasper-ga.html': {
        'city': 'Jasper',
        'county': 'Pickens County',
        'faqs': [
            ("Do you provide HVAC service in Jasper GA?", "Yes — Anderson serves Jasper and all of Pickens County with AC repair, furnace repair, heat pump installation, and insulation. Call (706) 629-0749."),
            ("How quickly can you get to Jasper for an emergency?", "We typically respond to Jasper emergency HVAC calls the same day. Our 24/7 emergency line is (706) 629-0749."),
            ("What is the cost of AC repair in Jasper GA?", "AC repair costs in Jasper typically range from $150-$500 for common repairs. We provide free estimates and upfront pricing."),
            ("Do you offer air conditioning installation in Jasper?", "Yes — we install high-efficiency air conditioning systems, heat pumps, and ductless mini-splits in Jasper homes. Financing available."),
            ("Can you do furnace repair in Jasper GA?", "Absolutely. Our technicians handle all furnace brands — gas, electric, and heat pump systems — serving Jasper and Pickens County."),
        ]
    },
    'ellijay-ga.html': {
        'city': 'Ellijay',
        'county': 'Gilmer County',
        'faqs': [
            ("Does Anderson serve Ellijay GA for HVAC?", "Yes — we provide full HVAC service to Ellijay and Gilmer County including AC repair, heat pump installation, and insulation. Call (706) 629-0749."),
            ("What HVAC services do you offer in Ellijay?", "We offer AC repair, furnace repair, heat pump and mini-split installation, duct cleaning, insulation, and whole-home energy audits in Ellijay."),
            ("Do you handle mountain home HVAC in Ellijay?", "Yes — we specialize in mountain home comfort challenges including zoning, insulation, and efficient heat pump systems perfect for Ellijay's climate."),
            ("Are you licensed to work in Gilmer County?", "Yes — Anderson is fully licensed (CN:003636), BPI certified, and insured. We've served Northwest Georgia since 1978."),
            ("Do you offer plumbing services in Ellijay?", "Yes — we provide plumbing services in Ellijay including water heater installation, tankless systems, and plumbing repairs."),
        ]
    },
    'fairmount-ga.html': {
        'city': 'Fairmount',
        'county': 'Gordon County',
        'faqs': [
            ("Do you serve Fairmount GA?", "Absolutely — Fairmount is in Gordon County, our home base. We provide HVAC, insulation, and energy services to Fairmount homeowners daily."),
            ("How close is Anderson to Fairmount?", "Our shop at 519 Pine Street in Calhoun is just 10-15 minutes from Fairmount. Same-day service is standard."),
            ("What heating and cooling services are available in Fairmount?", "We offer AC repair, furnace repair, heat pump installation, insulation, air sealing, duct cleaning, and whole-home energy audits in Fairmount."),
            ("Do you offer free estimates in Fairmount?", "Yes — we provide free in-home estimates for all HVAC, insulation, and energy improvement projects in Fairmount."),
            ("Can you help reduce energy bills in Fairmount homes?", "Yes — our BPI-certified whole-home approach addresses HVAC, insulation, air sealing, and ductwork to dramatically reduce energy costs."),
        ]
    },
    'resaca-ga.html': {
        'city': 'Resaca',
        'county': 'Gordon County',
        'faqs': [
            ("Does Anderson service Resaca GA?", "Yes — Resaca is just minutes from our Calhoun headquarters. We provide HVAC repair, installation, insulation, and energy services in Resaca."),
            ("Can I get same-day HVAC repair in Resaca?", "Yes — Resaca's proximity to our shop means fast response times. Call (706) 629-0749 for same-day or emergency HVAC service."),
            ("What makes Anderson different for Resaca homeowners?", "We're your neighbors — located just down the road in Calhoun. BPI certified, custom sheet metal shop, and whole-home energy approach since 1978."),
            ("Do you offer emergency HVAC service in Resaca?", "Yes — our 24/7 emergency line at (706) 629-0749 covers Resaca and all of Gordon County with same-day response."),
            ("Does Anderson do insulation work in Resaca?", "Absolutely. We install attic, wall, and crawlspace insulation with air sealing to make your Resaca home comfortable year-round."),
        ]
    },
}

faq_schema_count = 0
for fname, data in city_faqs.items():
    content = read_file(fname)
    if 'FAQPage' in content:
        print(f"  ⏭ {fname} already has FAQPage schema")
        continue

    # Build FAQPage schema
    faq_items = []
    for q, a in data['faqs']:
        faq_items.append(f'''        {{
          "@type": "Question",
          "name": "{q}",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{a}"
          }}
        }}''')

    faq_schema = f'''
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
{",\\n".join(faq_items)}
      ]
    }}
    </script>'''

    # Also add Service schema
    service_schema = f'''
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Service",
      "serviceType": "HVAC Services",
      "name": "HVAC Repair & Installation in {data['city']}, GA",
      "description": "Professional HVAC repair, AC installation, heat pump service, insulation, and whole-home energy solutions in {data['city']}, {data['county']}, Georgia.",
      "provider": {{
        "@type": "LocalBusiness",
        "name": "Anderson Heating, Air & Insulation",
        "telephone": "(706) 629-0749",
        "address": {{
          "@type": "PostalAddress",
          "streetAddress": "519 Pine Street",
          "addressLocality": "Calhoun",
          "addressRegion": "GA",
          "postalCode": "30701"
        }}
      }},
      "areaServed": {{
        "@type": "City",
        "name": "{data['city']}",
        "addressRegion": "GA"
      }},
      "hasOfferCatalog": {{
        "@type": "OfferCatalog",
        "name": "HVAC Services in {data['city']}",
        "itemListElement": [
          {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "AC Repair" }} }},
          {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Furnace Repair" }} }},
          {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Heat Pump Installation" }} }},
          {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Insulation & Air Sealing" }} }},
          {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Duct Cleaning" }} }},
          {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Whole Home Energy Audits" }} }}
        ]
      }}
    }}
    </script>'''

    # Inject before </head>
    content = content.replace('</head>', faq_schema + service_schema + '\n</head>')
    write_file(fname, content)
    faq_schema_count += 1
    print(f"  ✓ {fname} — FAQPage + Service schema added")

print(f"  Added FAQPage schema to {faq_schema_count} city pages.\n")

# ============================================================
# PHASE 3: Emergency HVAC Landing Pages
# ============================================================
print("=== PHASE 3: Emergency HVAC Landing Pages ===")

# Check which emergency pages need to be created
emergency_cities = {
    'emergency-hvac-chatsworth-ga.html': {
        'city': 'Chatsworth',
        'county': 'Murray County',
        'distance': '20 minutes',
        'keywords': 'emergency hvac chatsworth ga, 24/7 ac repair chatsworth, emergency heating repair chatsworth ga',
    },
    'emergency-hvac-adairsville-ga.html': {
        'city': 'Adairsville',
        'county': 'Bartow County',
        'distance': '15 minutes',
        'keywords': 'emergency hvac adairsville ga, 24/7 ac repair adairsville, emergency heating repair adairsville ga',
    },
}

emergency_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-XXXXXXXXXX');
    </script>
    <meta name="google-site-verification" content="REPLACE_WITH_VERIFICATION_CODE">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>24/7 Emergency HVAC Repair {city} GA | Same-Day AC & Heating | Anderson HAI (706) 629-0749</title>
    <meta name="description" content="Need emergency HVAC repair in {city}, GA? Anderson provides 24/7 same-day AC repair, furnace repair, and heating service. 48 years experience, 632+ reviews. Call (706) 629-0749 now!">
    <meta name="keywords" content="{keywords}">
    <link rel="canonical" href="https://shylohchavez.github.io/anderson-hai/{filename}">
    <meta property="og:title" content="24/7 Emergency HVAC Repair {city} GA | Anderson HAI">
    <meta property="og:description" content="Emergency HVAC repair in {city}, GA. 24/7 availability, same-day service. 48 years experience. Call (706) 629-0749.">
    <meta property="og:image" content="https://shylohchavez.github.io/anderson-hai/images/logo.png">
    <meta property="og:url" content="https://shylohchavez.github.io/anderson-hai/{filename}">
    <meta name="twitter:card" content="summary_large_image">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        'anderson-purple': '#4A1C6B',
                        'anderson-orange': '#FF6B00',
                    }}
                }}
            }}
        }}
    </script>
    <style>
        .brand-purple {{ color: #4A1C6B; }}
        .brand-orange {{ color: #FF6B00; }}
        .nav-link {{ transition: color 0.2s; }}
        .nav-link:hover {{ color: #FF6B00; }}
        .cta-button {{ transition: all 0.3s ease; }}
        .cta-button:hover {{ transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1); }}
        .pulse-emergency {{ animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.7; }} }}
    </style>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": ["LocalBusiness", "HVACBusiness"],
      "name": "Anderson Heating, Air & Insulation",
      "alternateName": "John Anderson Service Company, Inc.",
      "slogan": "The Paws-itive Choice",
      "description": "24/7 Emergency HVAC repair serving {city}, {county}, Georgia. BPI Certified, family-owned since 1978.",
      "url": "https://johnandersonservice.com/{filename}",
      "telephone": "(706) 629-0749",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "519 Pine Street",
        "addressLocality": "Calhoun",
        "addressRegion": "GA",
        "postalCode": "30701",
        "addressCountry": "US"
      }},
      "geo": {{ "@type": "GeoCoordinates", "latitude": "34.5029", "longitude": "-84.9511" }},
      "openingHours": "Mo-Su 00:00-23:59",
      "priceRange": "$$",
      "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "632" }},
      "areaServed": {{ "@type": "City", "name": "{city}", "addressRegion": "GA" }},
      "foundingDate": "1978-01",
      "sameAs": [
        "https://www.facebook.com/AndersonHeatAirCo/",
        "https://www.instagram.com/andersonheatairco/"
      ],
      "potentialAction": {{ "@type": "CallAction", "target": "tel:+17066290749" }},
      "breadcrumb": {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://johnandersonservice.com" }},
          {{ "@type": "ListItem", "position": 2, "name": "Emergency HVAC", "item": "https://johnandersonservice.com/emergency-hvac-repair.html" }},
          {{ "@type": "ListItem", "position": 3, "name": "Emergency HVAC {city} GA", "item": "https://johnandersonservice.com/{filename}" }}
        ]
      }}
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Service",
      "serviceType": "Emergency HVAC Repair",
      "name": "24/7 Emergency HVAC Repair in {city}, GA",
      "description": "Round-the-clock emergency AC repair, furnace repair, and heating service in {city}, {county}. Same-day response guaranteed.",
      "provider": {{
        "@type": "LocalBusiness",
        "name": "Anderson Heating, Air & Insulation",
        "telephone": "(706) 629-0749"
      }},
      "areaServed": {{ "@type": "City", "name": "{city}", "addressRegion": "GA" }},
      "availableChannel": {{
        "@type": "ServiceChannel",
        "servicePhone": {{ "@type": "ContactPoint", "telephone": "(706) 629-0749", "contactType": "emergency" }}
      }}
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "Does Anderson offer 24/7 emergency HVAC service in {city} GA?",
          "acceptedAnswer": {{ "@type": "Answer", "text": "Yes — Anderson provides 24/7 emergency HVAC repair service to {city} and {county}. Call (706) 629-0749 any time, day or night." }}
        }},
        {{
          "@type": "Question",
          "name": "How fast can you respond to an HVAC emergency in {city}?",
          "acceptedAnswer": {{ "@type": "Answer", "text": "We typically respond to {city} emergency calls within 1-2 hours. Our Calhoun shop is just {distance} away with technicians on call 24/7." }}
        }},
        {{
          "@type": "Question",
          "name": "What does emergency HVAC repair cost in {city} GA?",
          "acceptedAnswer": {{ "@type": "Answer", "text": "Emergency HVAC repair in {city} typically ranges from $150-$500 for common issues. We provide upfront pricing before any work begins — no surprise charges." }}
        }},
        {{
          "@type": "Question",
          "name": "Do you repair all HVAC brands in {city}?",
          "acceptedAnswer": {{ "@type": "Answer", "text": "Yes — our BPI and NATE certified technicians repair all major brands including Trane, Carrier, Lennox, Goodman, Rheem, and more in {city}." }}
        }},
        {{
          "@type": "Question",
          "name": "Can you fix my AC on weekends or holidays in {city}?",
          "acceptedAnswer": {{ "@type": "Answer", "text": "Absolutely. Anderson has been answering the phone at night and on weekends since 1978. We never charge extra for after-hours emergency calls to {city}." }}
        }}
      ]
    }}
    </script>
</head>
<body class="font-sans bg-white text-gray-900">
    <!-- Header -->
    <header class="bg-white border-b sticky top-0 z-50">
        <div class="mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-20">
                <a href="index.html" class="flex items-center gap-3">
                    <img src="images/logo.png" alt="Anderson Heating, Air & Insulation logo" class="w-12 h-12 object-contain">
                    <div>
                        <div class="font-bold text-2xl brand-purple">Anderson</div>
                        <div class="text-sm -mt-1 text-gray-600">Heating, Air & Insulation</div>
                    </div>
                </a>
                <nav class="hidden md:flex items-center gap-6 text-sm font-medium">
                    <a href="index.html" class="nav-link">Home</a>
                    <a href="services.html" class="nav-link">Services</a>
                    <a href="service-area.html" class="nav-link">Service Area</a>
                    <a href="reviews.html" class="nav-link">Reviews</a>
                    <a href="contact.html" class="nav-link">Contact</a>
                </nav>
                <div class="flex items-center gap-4">
                    <a href="tel:+17066290749" class="hidden sm:flex items-center gap-2 bg-red-600 text-white px-5 py-2.5 rounded-xl font-semibold text-sm pulse-emergency">
                        🚨 (706) 629-0749
                    </a>
                    <a href="contact.html" class="bg-anderson-orange text-white px-5 py-2.5 rounded-xl font-semibold text-sm cta-button">
                        Free Estimate
                    </a>
                </div>
            </div>
        </div>
    </header>

    <!-- Emergency Hero -->
    <section class="bg-gradient-to-br from-red-700 to-red-900 text-white py-16 md:py-24">
        <div class="mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div class="inline-flex items-center gap-2 bg-white/20 px-4 py-1.5 rounded-full text-sm mb-6 pulse-emergency">
                🚨 <span class="font-bold">24/7 EMERGENCY SERVICE</span> — Available Now
            </div>
            <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight tracking-tighter mb-6">
                Emergency HVAC Repair in {city}, Georgia
            </h1>
            <p class="text-xl md:text-2xl mx-auto mb-8 opacity-90 max-w-3xl">
                AC stopped working? Furnace won't start? Anderson has been answering emergency calls since 1978. Our Calhoun shop is just {distance} from {city} — we'll have a BPI-certified technician at your door fast.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="tel:+17066290749" class="inline-flex items-center justify-center gap-3 bg-white text-red-700 px-10 py-5 rounded-2xl font-bold text-xl cta-button">
                    📞 Call Now: (706) 629-0749
                </a>
                <a href="contact.html" class="inline-flex items-center justify-center gap-3 border-2 border-white/70 text-white px-8 py-5 rounded-2xl font-bold text-lg cta-button">
                    Request Emergency Service
                </a>
            </div>
            <div class="mt-8 flex items-center justify-center gap-8 text-sm opacity-75">
                <div>⭐ 632+ Reviews</div>
                <div>48 Years Experience</div>
                <div>No Extra After-Hours Fees</div>
            </div>
        </div>
    </section>

    <!-- Trust Bar -->
    <div class="bg-anderson-purple text-white py-4">
        <div class="mx-auto px-4 flex flex-wrap justify-center items-center gap-x-10 gap-y-3 text-sm">
            <div>🔧 All Brands Serviced</div>
            <div>⚡ Same-Day Response to {city}</div>
            <div>📜 Licensed CN:003636</div>
            <div>🏆 BPI + NATE Certified</div>
            <div>💰 Upfront Pricing</div>
        </div>
    </div>

    <!-- Emergency Services -->
    <section class="mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="text-center mb-12">
            <div class="text-red-600 font-semibold tracking-widest text-sm mb-3">EMERGENCY SERVICES</div>
            <h2 class="text-4xl font-bold tracking-tight brand-purple">What We Fix — Day or Night in {city}</h2>
        </div>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-white border rounded-3xl p-8">
                <div class="text-4xl mb-4">❄️</div>
                <h3 class="font-bold text-xl mb-3">Emergency AC Repair</h3>
                <p class="text-gray-600">AC blowing warm? Compressor failure? Refrigerant leak? We diagnose and fix it fast — no matter the hour in {city}.</p>
            </div>
            <div class="bg-white border rounded-3xl p-8">
                <div class="text-4xl mb-4">🔥</div>
                <h3 class="font-bold text-xl mb-3">Emergency Furnace Repair</h3>
                <p class="text-gray-600">No heat in winter? Furnace making strange noises? We handle gas, electric, and heat pump emergencies in {city}.</p>
            </div>
            <div class="bg-white border rounded-3xl p-8">
                <div class="text-4xl mb-4">🌡️</div>
                <h3 class="font-bold text-xl mb-3">Heat Pump Emergencies</h3>
                <p class="text-gray-600">Heat pump frozen, not switching modes, or short-cycling? Our NATE-certified techs handle all heat pump brands in {city}.</p>
            </div>
            <div class="bg-white border rounded-3xl p-8">
                <div class="text-4xl mb-4">💧</div>
                <h3 class="font-bold text-xl mb-3">Water Heater Emergencies</h3>
                <p class="text-gray-600">No hot water or leaking water heater? We repair and replace tank and tankless systems for {city} homes.</p>
            </div>
            <div class="bg-white border rounded-3xl p-8">
                <div class="text-4xl mb-4">💨</div>
                <h3 class="font-bold text-xl mb-3">Ductwork Emergencies</h3>
                <p class="text-gray-600">Collapsed duct, disconnected ductwork, or air flow problems? Our in-house sheet metal shop fabricates custom replacements.</p>
            </div>
            <div class="bg-white border rounded-3xl p-8">
                <div class="text-4xl mb-4">⚡</div>
                <h3 class="font-bold text-xl mb-3">Electrical & Thermostat</h3>
                <p class="text-gray-600">Thermostat failures, electrical issues, or tripped breakers from HVAC systems — we troubleshoot and resolve in {city}.</p>
            </div>
        </div>
    </section>

    <!-- Why Choose Anderson for Emergencies -->
    <section class="bg-gray-50 py-16">
        <div class="mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-12">
                <h2 class="text-4xl font-bold tracking-tight brand-purple">Why {city} Chooses Anderson for Emergencies</h2>
            </div>
            <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                <div class="flex gap-4">
                    <div class="text-3xl">⏰</div>
                    <div>
                        <h3 class="font-bold text-lg mb-2">True 24/7 Availability</h3>
                        <p class="text-gray-600">We've been answering the phone at night since 1978. No answering service — real technicians, real solutions.</p>
                    </div>
                </div>
                <div class="flex gap-4">
                    <div class="text-3xl">💰</div>
                    <div>
                        <h3 class="font-bold text-lg mb-2">No After-Hours Upcharge</h3>
                        <p class="text-gray-600">Same fair pricing whether it's 2 PM or 2 AM. Upfront quotes before any work begins.</p>
                    </div>
                </div>
                <div class="flex gap-4">
                    <div class="text-3xl">🏭</div>
                    <div>
                        <h3 class="font-bold text-lg mb-2">Parts On Hand</h3>
                        <p class="text-gray-600">Our trucks are stocked with common parts. Our sheet metal shop can fabricate custom ductwork the same day.</p>
                    </div>
                </div>
                <div class="flex gap-4">
                    <div class="text-3xl">📜</div>
                    <div>
                        <h3 class="font-bold text-lg mb-2">48 Years of Trust</h3>
                        <p class="text-gray-600">632+ Google reviews, BPI + NATE certified. The most experienced HVAC team serving {city}.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- FAQ Section -->
    <section class="mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="text-center mb-12">
            <div class="text-anderson-orange font-semibold tracking-widest text-sm mb-3">FREQUENTLY ASKED QUESTIONS</div>
            <h2 class="text-4xl font-bold tracking-tight brand-purple">Emergency HVAC Questions from {city} Homeowners</h2>
        </div>
        <div class="space-y-4 max-w-3xl mx-auto">
            <div class="bg-white border rounded-3xl p-6">
                <h3 class="font-semibold text-lg mb-2">Does Anderson offer 24/7 emergency HVAC service in {city} GA?</h3>
                <p class="text-gray-600">Yes — Anderson provides 24/7 emergency HVAC repair service to {city} and {county}. Call (706) 629-0749 any time, day or night.</p>
            </div>
            <div class="bg-white border rounded-3xl p-6">
                <h3 class="font-semibold text-lg mb-2">How fast can you respond to an HVAC emergency in {city}?</h3>
                <p class="text-gray-600">We typically respond to {city} emergency calls within 1-2 hours. Our Calhoun shop is just {distance} away with technicians on call 24/7.</p>
            </div>
            <div class="bg-white border rounded-3xl p-6">
                <h3 class="font-semibold text-lg mb-2">What does emergency HVAC repair cost in {city} GA?</h3>
                <p class="text-gray-600">Emergency HVAC repair in {city} typically ranges from $150-$500 for common issues. We provide upfront pricing before any work begins.</p>
            </div>
            <div class="bg-white border rounded-3xl p-6">
                <h3 class="font-semibold text-lg mb-2">Do you repair all HVAC brands in {city}?</h3>
                <p class="text-gray-600">Yes — our BPI and NATE certified technicians repair all major brands including Trane, Carrier, Lennox, Goodman, Rheem, and more.</p>
            </div>
            <div class="bg-white border rounded-3xl p-6">
                <h3 class="font-semibold text-lg mb-2">Can you fix my AC on weekends or holidays in {city}?</h3>
                <p class="text-gray-600">Absolutely. Anderson has been answering the phone at night and on weekends since 1978. No extra charge for after-hours calls to {city}.</p>
            </div>
        </div>
    </section>

    <!-- Service Area Links -->
    <section class="bg-gray-50 py-12">
        <div class="mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 class="text-2xl font-bold brand-purple mb-6">Emergency HVAC Service Across NW Georgia</h2>
            <div class="flex flex-wrap justify-center gap-3">
                <a href="emergency-hvac-repair-calhoun-ga.html" class="bg-white border px-4 py-2 rounded-full text-sm hover:border-anderson-orange">Calhoun</a>
                <a href="emergency-hvac-dalton-ga.html" class="bg-white border px-4 py-2 rounded-full text-sm hover:border-anderson-orange">Dalton</a>
                <a href="emergency-hvac-rome-ga.html" class="bg-white border px-4 py-2 rounded-full text-sm hover:border-anderson-orange">Rome</a>
                <a href="emergency-hvac-cartersville-ga.html" class="bg-white border px-4 py-2 rounded-full text-sm hover:border-anderson-orange">Cartersville</a>
                <a href="emergency-hvac-adairsville-ga.html" class="bg-white border px-4 py-2 rounded-full text-sm hover:border-anderson-orange">Adairsville</a>
                <a href="emergency-hvac-chatsworth-ga.html" class="bg-white border px-4 py-2 rounded-full text-sm hover:border-anderson-orange">Chatsworth</a>
            </div>
        </div>
    </section>

    <!-- Final CTA -->
    <section class="bg-red-700 text-white py-16 text-center">
        <div class="mx-auto px-4">
            <h2 class="text-4xl font-bold mb-4">Don't Sweat It — Call Anderson Now</h2>
            <p class="text-xl opacity-90 mb-8">48 years of answering emergency calls in {city} and Northwest Georgia.</p>
            <a href="tel:+17066290749" class="inline-flex items-center gap-3 bg-white text-red-700 px-10 py-5 rounded-2xl font-bold text-xl cta-button">
                📞 (706) 629-0749
            </a>
            <p class="mt-6 text-sm opacity-75">Anderson Heating, Air & Insulation — The Paws-itive Choice 🐾 | Licensed CN:003636</p>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-anderson-purple text-white/80 text-sm">
        <div class="mx-auto px-4 sm:px-6 lg:px-8 py-12">
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
                    <div class="text-xs mt-1 text-white/70">Licensed: CN:003636</div>
                </div>
                <div>
                    <div class="font-semibold text-white mb-3">Services</div>
                    <div class="space-y-1 text-xs">
                        <a href="hvac-repair-install.html" class="block hover:text-white">HVAC Repair & Install</a>
                        <a href="heat-pump-mini-split.html" class="block hover:text-white">Heat Pumps & Mini-Splits</a>
                        <a href="insulation-air-sealing.html" class="block hover:text-white">Insulation & Air Sealing</a>
                        <a href="duct-cleaning.html" class="block hover:text-white">Duct Cleaning</a>
                        <a href="water-heaters.html" class="block hover:text-white">Water Heaters</a>
                    </div>
                </div>
                <div>
                    <div class="font-semibold text-white mb-3">Service Areas</div>
                    <div class="space-y-1 text-xs">
                        <a href="calhoun-ga.html" class="block hover:text-white">Calhoun</a>
                        <a href="dalton-ga.html" class="block hover:text-white">Dalton</a>
                        <a href="rome-ga.html" class="block hover:text-white">Rome</a>
                        <a href="cartersville-ga.html" class="block hover:text-white">Cartersville</a>
                        <a href="chatsworth-ga.html" class="block hover:text-white">Chatsworth</a>
                        <a href="service-area.html" class="block hover:text-white">All Service Areas →</a>
                    </div>
                </div>
            </div>
            <div class="border-t border-white/20 mt-12 pt-8 text-xs text-center">
                © 2026 Anderson Heating, Air & Insulation. Est. January 1978. All rights reserved.
            </div>
        </div>
    </footer>
</body>
</html>'''

emergency_count = 0
for fname, data in emergency_cities.items():
    fpath = os.path.join(SITE, fname)
    if os.path.exists(fpath):
        print(f"  ⏭ {fname} already exists")
        continue
    content = emergency_template.format(
        city=data['city'],
        county=data['county'],
        distance=data['distance'],
        keywords=data['keywords'],
        filename=fname,
    )
    write_file(fname, content)
    emergency_count += 1
    print(f"  ✓ Created {fname}")

print(f"  Created {emergency_count} new emergency pages.\n")

print("Phase 3 complete.")
