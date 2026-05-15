#!/usr/bin/env python3
"""
Comprehensive content quality fix for Anderson HAI website.
Fixes: garbled FAQ text, wrong city content, incomplete testimonials,
wrong county assignments, duplicate city names.
"""
import os
import re

SITE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# CITY/COUNTY MAPPING - correct geographic data
# ============================================================

# City pages: filename -> (city_name, county_name, landmarks, neighborhoods)
CITY_PAGES = {
    'plainville-ga': {
        'city': 'Plainville',
        'county': 'Gordon County',
        'landmarks': 'New Echota State Historic Site, Salacoa Creek, and the scenic Gordon County countryside',
        'neighborhoods': 'Downtown Plainville, Highway 41 corridor, and surrounding Gordon County communities',
        'local_note': 'Just minutes from our Calhoun headquarters, Plainville homeowners get fast response times and the same whole-home approach we\'re known for across Gordon County.',
    },
    'trion-ga': {
        'city': 'Trion',
        'county': 'Chattooga County',
        'landmarks': 'Trion City Park, Chattooga River, and the historic Trion Factory area',
        'neighborhoods': 'Downtown Trion, Mill Village, and surrounding Chattooga County communities',
        'local_note': 'Trion\'s mix of historic mill homes and newer construction means we see every type of HVAC challenge — and our whole-home approach handles them all.',
    },
    'sugar-valley-ga': {
        'city': 'Sugar Valley',
        'county': 'Gordon County',
        'landmarks': 'Sugar Valley community center, Highway 411, and the rolling Gordon County farmland',
        'neighborhoods': 'Sugar Valley, Highway 411 corridor, and surrounding Gordon County communities',
        'local_note': 'Sugar Valley is right in our backyard — Gordon County homeowners here get priority service from our Calhoun shop just minutes away.',
    },
    'sonoraville-ga': {
        'city': 'Sonoraville',
        'county': 'Gordon County',
        'landmarks': 'Sonoraville community, Sonoraville High School, and the growing east Gordon County area',
        'neighborhoods': 'Sonoraville, east Gordon County, and surrounding communities',
        'local_note': 'Sonoraville is one of Gordon County\'s fastest-growing areas, and we\'ve been keeping these homes comfortable since long before the growth started.',
    },
    'armuchee-ga': {
        'city': 'Armuchee',
        'county': 'Floyd County',
        'landmarks': 'Armuchee Creek, Marshall Forest, and the scenic ridges of northwest Floyd County',
        'neighborhoods': 'Armuchee, Old Summerville Road area, and surrounding Floyd County communities',
        'local_note': 'Armuchee\'s rural Floyd County setting means homes here face unique energy challenges — our whole-home approach makes a real difference.',
    },
    'tunnel-hill-ga': {
        'city': 'Tunnel Hill',
        'county': 'Whitfield County',
        'landmarks': 'Western & Atlantic Railroad Tunnel, Tunnel Hill Heritage Center, and Clisby Austin House',
        'neighborhoods': 'Downtown Tunnel Hill, Varnell area, and surrounding Whitfield County communities',
        'local_note': 'Tunnel Hill\'s historic homes and newer developments both benefit from our comprehensive energy approach — we fix the whole house, not just the equipment.',
    },
    'tennga-ga': {
        'city': 'Tennga',
        'county': 'Murray County',
        'landmarks': 'The Cohutta Wilderness nearby, Holly Creek, and the scenic Murray County mountains',
        'neighborhoods': 'Tennga, Highway 411 corridor, and surrounding Murray County communities',
        'local_note': 'Tennga\'s mountain-area homes face unique heating and cooling challenges — our BPI-certified approach ensures year-round comfort.',
    },
    'ranger-ga': {
        'city': 'Ranger',
        'county': 'Gordon County',
        'landmarks': 'Ranger community area, scenic Gordon County ridgelines, and nearby Calhoun attractions',
        'neighborhoods': 'Ranger, Highway 411 area, and surrounding Gordon County communities',
        'local_note': 'Ranger is one of our closest communities to serve — Gordon County homeowners here enjoy fast response from our Pine Street headquarters.',
    },
    'lyerly-ga': {
        'city': 'Lyerly',
        'county': 'Chattooga County',
        'landmarks': 'Chattooga County countryside, the Lyerly community center, and nearby Cloudland Canyon',
        'neighborhoods': 'Downtown Lyerly, Highway 114 corridor, and surrounding Chattooga County communities',
        'local_note': 'Lyerly\'s charming Chattooga County homes deserve whole-home comfort solutions, and that\'s exactly what Anderson delivers.',
    },
    'chickamauga-ga': {
        'city': 'Chickamauga',
        'county': 'Walker County',
        'landmarks': 'Chickamauga & Chattanooga National Military Park, Gordon-Lee Mansion, and historic downtown',
        'neighborhoods': 'Downtown Chickamauga, Lee & Gordon\'s Mill area, and surrounding Walker County communities',
        'local_note': 'Chickamauga\'s historic homes and battlefield-area properties have unique comfort needs — our whole-home approach preserves character while maximizing efficiency.',
    },
    'lafayette-ga': {
        'city': 'LaFayette',
        'county': 'Walker County',
        'landmarks': 'Walker County Courthouse, Marsh House, LaFayette Square, and nearby Chickamauga Lake',
        'neighborhoods': 'Downtown LaFayette, Villanow area, and surrounding Walker County communities',
        'local_note': 'As the Walker County seat, LaFayette has a wonderful mix of historic and modern homes — all of which benefit from our whole-home energy solutions.',
    },
    'ringgold-ga': {
        'city': 'Ringgold',
        'county': 'Catoosa County',
        'landmarks': 'Historic Ringgold Depot, Ringgold Gap Battlefield, and the growing Catoosa County corridor',
        'neighborhoods': 'Downtown Ringgold, Boynton area, and surrounding Catoosa County communities',
        'local_note': 'Ringgold\'s growth along the I-75 corridor means plenty of new and existing homes need our whole-home energy approach.',
    },
    'summerville-ga': {
        'city': 'Summerville',
        'county': 'Chattooga County',
        'landmarks': 'Howard Finster\'s Paradise Garden, Chattooga County Courthouse, and James H. Floyd State Park',
        'neighborhoods': 'Downtown Summerville, Pennville area, and surrounding Chattooga County communities',
        'local_note': 'As the Chattooga County seat, Summerville has a rich heritage of homes that deserve modern comfort solutions with our whole-home approach.',
    },
    'redbud-ga': {
        'city': 'Redbud',
        'county': 'Gordon County',
        'landmarks': 'Redbud community, scenic Gordon County landscape, and proximity to Calhoun',
        'neighborhoods': 'Redbud, surrounding Gordon County communities, and nearby Calhoun areas',
        'local_note': 'Redbud is right in the heart of Gordon County — our closest neighbors get priority service from our Calhoun headquarters.',
    },
    'rocky-face-ga': {
        'city': 'Rocky Face',
        'county': 'Whitfield County',
        'landmarks': 'Rocky Face Ridge, Buzzard Roost trail, and the scenic Whitfield County ridgeline',
        'neighborhoods': 'Rocky Face, Mill Creek area, and surrounding Whitfield County communities',
        'local_note': 'Rocky Face\'s ridgetop and valley homes face distinct heating and cooling demands — our BPI-certified team knows exactly how to handle them.',
    },
}

# County pages: filename -> (county_name, main_city)
COUNTY_PAGES = {
    'walker-county-ga': {'county': 'Walker County', 'main_city': 'LaFayette'},
    'floyd-county-ga': {'county': 'Floyd County', 'main_city': 'Rome'},
    'catoosa-county-ga': {'county': 'Catoosa County', 'main_city': 'Ringgold'},
    'gilmer-county-ga': {'county': 'Gilmer County', 'main_city': 'Ellijay'},
    'whitfield-county-ga': {'county': 'Whitfield County', 'main_city': 'Dalton'},
    'murray-county-ga': {'county': 'Murray County', 'main_city': 'Chatsworth'},
    'pickens-county-ga': {'county': 'Pickens County', 'main_city': 'Jasper'},
    'bartow-county-ga': {'county': 'Bartow County', 'main_city': 'Cartersville'},
}

def fix_garbled_faqs_county(content, county, main_city):
    """Fix garbled FAQ text in county pages."""
    
    # Fix "Do you offer do you offer same-day hvac repair in X county ga?"
    pattern = r'Do you offer do you offer same-day hvac repair in ' + re.escape(county.lower()) + r' ga\?'
    replacement = f'Do you offer same-day HVAC repair in {county}, GA?'
    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Fix "Yes — we prioritize Yes — we prioritize X County calls for emerge[n] for emergency..."
    pattern = r'Yes — we prioritize Yes — we prioritize ' + re.escape(county) + r' calls for emerge[n]? for emergency AC and heating repairs with 24/7 availability\.'
    replacement = f'Yes — we prioritize {county} calls for emergency AC and heating repairs with 24/7 availability.'
    content = re.sub(pattern, replacement, content)
    
    # Fix "What what communities in X county do you serve?"
    pattern = r'What what communities in ' + re.escape(county.lower()) + r' do you serve\?'
    replacement = f'What communities in {county} do you serve?'
    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Fix "Is your is your sheet metal shop available for X county customers?"
    pattern = r'Is your is your sheet metal shop available for ' + re.escape(county.lower()) + r' customers\?'
    replacement = f'Is your sheet metal shop available for {county} customers?'
    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Fix "Do you do do you do energy audits for X county homes?"
    pattern = r'Do you do do you do energy audits for ' + re.escape(county.lower()) + r' homes\?'
    replacement = f'Do you do energy audits for {county} homes?'
    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    # Fix "does this what makes anderson different for X county homeowners"
    pattern = r'does this what makes anderson different for ' + re.escape(county.lower()) + r' homeowners'
    replacement = f'does this for {county} homeowners'
    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Fix "We serve all of Calhoun including X and all Y County communities."
    old = f'We serve all of Calhoun including {main_city} and all {county} communities.'
    new = f'We serve {main_city}, and all {county} communities — from small towns to rural areas.'
    content = content.replace(old, new)
    
    return content


def fix_garbled_faqs_city(content, city, county):
    """Fix garbled FAQ text in city pages."""
    city_lower = city.lower()
    
    # Fix "Do you offer do you offer hvac repair in X ga?"
    pattern = r'Do you offer do you offer hvac repair in ' + re.escape(city_lower) + r' ga\?'
    replacement = f'Do you offer HVAC repair in {city}, GA?'
    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Fix "Yes — we prioritize Yes, we provide same-day HVAC repair and emergency service f for emergency..."
    pattern = r'Yes — we prioritize Yes, we provide same-day HVAC repair and emergency service f for emergency AC and heating repairs with 24/7 availability\.'
    replacement = f'Yes — we provide same-day HVAC repair and emergency service for {city} homeowners, with 24/7 availability.'
    content = re.sub(pattern, replacement, content)
    
    return content


def fix_calhoun_references_city(content, city, county, info):
    """Replace incorrect Calhoun references in city pages with correct city/county."""
    
    # ---- HYPER-LOCAL SECTION ----
    # "HYPER-LOCAL TO CALHOUN" -> "HYPER-LOCAL TO [CITY]"
    content = content.replace('HYPER-LOCAL TO CALHOUN', f'HYPER-LOCAL TO {city.upper()}')
    
    # "Proudly Serving Calhoun & Gordon County Neighborhoods"
    content = content.replace(
        'Proudly Serving Calhoun & Gordon County Neighborhoods',
        f'Proudly Serving {city} & {county} Neighborhoods'
    )
    
    # Hyper-local paragraph - replace the whole block
    old_local_block = '''<p class="text-lg text-gray-700 mb-6">From historic downtown Calhoun to the growing Eastside and Westside neighborhoods, we understand the unique heating and cooling challenges of Gordon County homes — older farmhouses, 1980s subdivisions, and new construction alike. Our whole-home approach fixes the house, not just the equipment.</p>
                <p class="text-lg text-gray-700 mb-6"><strong>Local landmarks we know well:</strong> New Echota State Historic Site, Calhoun Square, Gordon County Courthouse, and Lake Marvin.</p>
                <p class="text-lg text-gray-700 mb-6"><strong>Neighborhoods we serve daily:</strong> Downtown Calhoun, Park Place, East Calhoun, Westside, and surrounding Gordon County communities.</p>
                <p class="text-lg text-gray-700"><strong>The Anderson difference in Calhoun:</strong> As our home base since 1978, we know every street in Calhoun and Gordon County. Our custom sheet metal shop at 519 Pine Street means faster turnaround for local homeowners.</p>'''
    
    new_local_block = f'''<p class="text-lg text-gray-700 mb-6">We understand the unique heating and cooling challenges of {county} homes — older farmhouses, established subdivisions, and new construction alike. Our whole-home approach fixes the house, not just the equipment.</p>
                <p class="text-lg text-gray-700 mb-6"><strong>Local landmarks we know well:</strong> {info['landmarks']}.</p>
                <p class="text-lg text-gray-700 mb-6"><strong>Neighborhoods we serve daily:</strong> {info['neighborhoods']}.</p>
                <p class="text-lg text-gray-700"><strong>The Anderson difference in {city}:</strong> {info['local_note']} Our custom sheet metal shop at 519 Pine Street in Calhoun means faster turnaround for all our customers.</p>'''
    
    content = content.replace(old_local_block, new_local_block)
    
    # ---- WHY ANDERSON SECTION ----
    content = content.replace(
        f'Why Calhoun Homeowners Choose Anderson',
        f'Why {city} Homeowners Choose Anderson'
    )
    
    # ---- SERVICE DESCRIPTIONS ----
    # "That's the Anderson difference in Calhoun."
    content = content.replace(
        "That's the Anderson difference in Calhoun.",
        f"That's the Anderson difference in {city}."
    )
    
    # Service card text with "Calhoun" -> city
    content = content.replace(
        f'serving Calhoun and Gordon County',
        f'serving {city} and {county}'
    )
    content = content.replace(
        f'perfect for Calhoun homes',
        f'perfect for {city} homes'
    )
    content = content.replace(
        f"your home's envelope in Calhoun",
        f"your home's envelope in {city}"
    )
    content = content.replace(
        f'healthier air in Calhoun',
        f'healthier air in {city}'
    )
    content = content.replace(
        f'for Gordon County homeowners',
        f'for {county} homeowners'
    )
    content = content.replace(
        f'your Calhoun home is losing energy',
        f'your {city} home is losing energy'
    )
    
    # "for Calhoun families" -> "for [city] families"
    content = content.replace('for Calhoun families', f'for {city} families')
    # "for Calhoun projects" -> "for [city] projects"  
    content = content.replace('for Calhoun projects', f'for {city} projects')
    # "for every Calhoun customer"
    content = content.replace('for every Calhoun customer', f'for every {city} customer')
    # "in Calhoun." (general)
    # Be careful - some "in Calhoun" refs are correct (address, company location)
    
    # "energy picture in Calhoun"
    content = content.replace('energy picture in Calhoun', f'energy picture in {city}')
    
    # ---- FAQ SECTION ----
    content = content.replace(
        f'Questions Calhoun Homeowners Ask',
        f'Questions {city} Homeowners Ask'
    )
    
    # FAQ: "What communities in Gordon County do you serve?"
    content = content.replace(
        f'What communities in Gordon County do you serve?',
        f'What communities in {county} do you serve?'
    )
    content = content.replace(
        f'We serve all of Calhoun including {city} and nearby Gordon County areas.',
        f'We serve all of {city} and the surrounding {county} area, plus communities throughout Northwest Georgia.'
    )
    content = content.replace(
        f'We serve all of Calhoun including {city} and nearby areas.',
        f'We serve all of {city} and the surrounding {county} area, plus communities throughout Northwest Georgia.'
    )
    
    # FAQ: county references
    content = content.replace(
        f'Is your sheet metal shop available for Gordon County customers?',
        f'Is your sheet metal shop available for {county} customers?'
    )
    content = content.replace(
        f'Do you do energy audits for Gordon County homes?',
        f'Do you do energy audits for {county} homes?'
    )
    content = content.replace(
        f'What makes Anderson different for Gordon County homeowners?',
        f'What makes Anderson different for {county} homeowners?'
    )
    content = content.replace(
        f'We have served Gordon County since 1978.',
        f'We have served {county} since 1978.'
    )
    
    # ---- FINAL CTA ----
    content = content.replace(
        'Ready to Fix Your Whole House in Calhoun?',
        f'Ready to Fix Your Whole House in {city}?'
    )
    
    # ---- TESTIMONIALS ----
    content = content.replace(
        f'Real homeowners across Calhoun, Gordon County and NW Georgia.',
        f'Real homeowners across {city}, {county} and NW Georgia.'
    )
    
    # ---- FOOTER ----
    content = content.replace(
        f'519 Pine Street<br>Gordon County, GA 30701',
        f'519 Pine Street<br>Calhoun, GA 30701'
    )
    
    # Footer: Serving line
    content = content.replace(
        f'Serving Calhoun, Gordon County & NW Georgia since 1978',
        f'Serving {city}, {county} & NW Georgia since 1978'
    )
    
    # Console log
    content = content.replace(
        "console.log('%c[Anderson HAI] Calhoun city page loaded successfully.'",
        f"console.log('%c[Anderson HAI] {city} city page loaded successfully.'"
    )
    
    return content


def fix_calhoun_references_county(content, county, main_city):
    """Replace incorrect Calhoun references in county pages."""
    
    # County pages have different wrong-content patterns
    # "HYPER-LOCAL TO CALHOUN"
    content = content.replace('HYPER-LOCAL TO CALHOUN', f'HYPER-LOCAL TO {county.upper()}')
    
    # "Proudly Serving Calhoun & Gordon County Neighborhoods"
    content = content.replace(
        'Proudly Serving Calhoun & Gordon County Neighborhoods',
        f'Proudly Serving {main_city} & {county} Neighborhoods'
    )
    
    # "Why Calhoun Homeowners Choose Anderson"
    content = content.replace(
        'Why Calhoun Homeowners Choose Anderson',
        f'Why {county} Homeowners Choose Anderson'
    )
    
    # "That's the Anderson difference in Calhoun."
    content = content.replace(
        "That's the Anderson difference in Calhoun.",
        f"That's the Anderson difference in {county}."
    )
    
    # Service card references
    content = content.replace(
        'serving Calhoun and Gordon County',
        f'serving {main_city} and {county}'
    )
    content = content.replace(
        'perfect for Calhoun homes',
        f'perfect for {county} homes'
    )
    content = content.replace(
        "your home's envelope in Calhoun",
        f"your home's envelope in {county}"
    )
    content = content.replace(
        'healthier air in Calhoun',
        f'healthier air in {county}'
    )
    content = content.replace(
        'for Gordon County homeowners',
        f'for {county} homeowners'
    )
    content = content.replace(
        'your Calhoun home is losing energy',
        f'your {county} home is losing energy'
    )
    content = content.replace('for Calhoun families', f'for {county} families')
    content = content.replace('for Calhoun projects', f'for {county} projects')
    content = content.replace('for every Calhoun customer', f'for every {county} customer')
    content = content.replace('energy picture in Calhoun', f'energy picture in {county}')
    
    # FAQ section
    content = content.replace(
        'Questions Calhoun Homeowners Ask',
        f'Questions {county} Homeowners Ask'
    )
    
    # Testimonials
    content = content.replace(
        'Real homeowners across Calhoun, Gordon County and NW Georgia.',
        f'Real homeowners across {main_city}, {county} and NW Georgia.'
    )
    
    # CTA
    content = content.replace(
        'Ready to Fix Your Whole House in Calhoun?',
        f'Ready to Fix Your Whole House in {county}?'
    )
    
    # Footer
    content = content.replace(
        '519 Pine Street<br>Gordon County, GA 30701',
        f'519 Pine Street<br>Calhoun, GA 30701'
    )
    content = content.replace(
        'Serving Calhoun, Gordon County & NW Georgia since 1978',
        f'Serving {main_city}, {county} & NW Georgia since 1978'
    )
    
    # Hyper-local section for county pages
    old_local = '''<p class="text-lg text-gray-700 mb-6">From historic downtown Calhoun to the growing Eastside and Westside neighborhoods, we understand the unique heating and cooling challenges of Gordon County homes — older farmhouses, 1980s subdivisions, and new construction alike. Our whole-home approach fixes the house, not just the equipment.</p>
                <p class="text-lg text-gray-700 mb-6"><strong>Local landmarks we know well:</strong> New Echota State Historic Site, Calhoun Square, Gordon County Courthouse, and Lake Marvin.</p>
                <p class="text-lg text-gray-700 mb-6"><strong>Neighborhoods we serve daily:</strong> Downtown Calhoun, Park Place, East Calhoun, Westside, and surrounding Gordon County communities.</p>
                <p class="text-lg text-gray-700"><strong>The Anderson difference in Calhoun:</strong> As our home base since 1978, we know every street in Calhoun and Gordon County. Our custom sheet metal shop at 519 Pine Street means faster turnaround for local homeowners.</p>'''
    
    new_local = f'''<p class="text-lg text-gray-700 mb-6">We understand the unique heating and cooling challenges of {county} homes — older farmhouses, established subdivisions, and new construction alike. Our whole-home approach fixes the house, not just the equipment.</p>
                <p class="text-lg text-gray-700 mb-6"><strong>Areas we serve in {county}:</strong> {main_city} and all surrounding {county} communities.</p>
                <p class="text-lg text-gray-700 mb-6"><strong>The Anderson difference:</strong> Based at 519 Pine Street in Calhoun since 1978, we serve all of {county} with the same whole-home energy approach that has earned us 632+ Google reviews.</p>
                <p class="text-lg text-gray-700"><strong>Custom sheet metal:</strong> Our in-house fabrication shop means faster turnaround on custom ductwork for {county} homeowners — no waiting on third-party suppliers.</p>'''
    
    content = content.replace(old_local, new_local)
    
    # Console log
    content = content.replace(
        "console.log('%c[Anderson HAI] Calhoun city page loaded successfully.'",
        f"console.log('%c[Anderson HAI] {county} page loaded successfully.'"
    )
    
    return content


def fix_testimonials(content, city_or_county):
    """Fix incomplete testimonial fragments."""
    # "The Johnsons in Calhoun " fragment
    old_testimonial = '''"The Johnsons in Calhoun "</p>
                <div class="mt-6 text-sm font-semibold">—  "Anderson fixed our AC and showed us how poor insulation was spiking our bills. They sealed everything and our power bill dropped 30%. Best decision we made."</div>'''
    
    new_testimonial = f'''"Anderson fixed our AC and showed us how poor insulation was spiking our bills. They sealed everything and our power bill dropped 30%. Best decision we made."</p>
                <div class="mt-6 text-sm font-semibold">— The Johnson Family, {city_or_county}</div>'''
    
    content = content.replace(old_testimonial, new_testimonial)
    return content


def fix_wrong_county_assignments():
    """Fix wrong county in energy-rebates, hvac-repair-cost, insulation-and-hvac pages."""
    county_fixes = {
        'chatsworth': 'Murray County',
        'ellijay': 'Gilmer County',
        'fairmount': 'Gordon County',
        'jasper': 'Pickens County',
        'resaca': 'Gordon County',
    }
    
    prefixes = ['energy-rebates-hvac-', 'hvac-repair-cost-', 'insulation-and-hvac-']
    fixed = 0
    
    for city, correct_county in county_fixes.items():
        for prefix in prefixes:
            filepath = os.path.join(SITE_DIR, f'{prefix}{city}.html')
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    content = f.read()
                
                old = f'deep roots in Floyd County'
                new = f'deep roots in {correct_county}'
                
                if old in content:
                    content = content.replace(old, new)
                    with open(filepath, 'w') as f:
                        f.write(content)
                    fixed += 1
                    print(f'  Fixed county: {prefix}{city}.html → {correct_county}')
    
    return fixed


def fix_duplicate_city_names():
    """Fix 'Rome, Dalton, Rome, Cartersville' → 'Rome, Dalton, Cartersville'."""
    fixed = 0
    for filename in os.listdir(SITE_DIR):
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(SITE_DIR, filename)
        with open(filepath, 'r') as f:
            content = f.read()
        
        if 'Rome, Dalton, Rome, Cartersville' in content:
            content = content.replace('Rome, Dalton, Rome, Cartersville', 'Rome, Dalton, Cartersville')
            with open(filepath, 'w') as f:
                f.write(content)
            fixed += 1
            print(f'  Fixed duplicate cities: {filename}')
    
    return fixed


def main():
    total_fixed = 0
    
    # ---- FIX CITY PAGES ----
    print("=== FIXING CITY PAGES ===")
    for slug, info in CITY_PAGES.items():
        filepath = os.path.join(SITE_DIR, f'{slug}.html')
        if not os.path.exists(filepath):
            print(f'  SKIP (not found): {slug}.html')
            continue
        
        with open(filepath, 'r') as f:
            original = f.read()
        
        content = original
        city = info['city']
        county = info['county']
        
        # Fix garbled FAQs
        content = fix_garbled_faqs_city(content, city, county)
        
        # Fix Calhoun/Gordon County references
        content = fix_calhoun_references_city(content, city, county, info)
        
        # Fix testimonials
        content = fix_testimonials(content, city)
        
        if content != original:
            with open(filepath, 'w') as f:
                f.write(content)
            calhoun_count = content.count('Calhoun')
            print(f'  Fixed: {slug}.html (remaining Calhoun refs: {calhoun_count})')
            total_fixed += 1
        else:
            print(f'  No changes: {slug}.html')
    
    # ---- FIX COUNTY PAGES ----
    print("\n=== FIXING COUNTY PAGES ===")
    for slug, info in COUNTY_PAGES.items():
        filepath = os.path.join(SITE_DIR, f'{slug}.html')
        if not os.path.exists(filepath):
            print(f'  SKIP (not found): {slug}.html')
            continue
        
        with open(filepath, 'r') as f:
            original = f.read()
        
        content = original
        county = info['county']
        main_city = info['main_city']
        
        # Fix garbled FAQs
        content = fix_garbled_faqs_county(content, county, main_city)
        
        # Fix Calhoun/Gordon County references
        content = fix_calhoun_references_county(content, county, main_city)
        
        # Fix testimonials
        content = fix_testimonials(content, county)
        
        if content != original:
            with open(filepath, 'w') as f:
                f.write(content)
            calhoun_count = content.count('Calhoun')
            print(f'  Fixed: {slug}.html (remaining Calhoun refs: {calhoun_count})')
            total_fixed += 1
        else:
            print(f'  No changes: {slug}.html')
    
    # ---- FIX WRONG COUNTY ASSIGNMENTS ----
    print("\n=== FIXING WRONG COUNTY ASSIGNMENTS ===")
    county_fixes = fix_wrong_county_assignments()
    total_fixed += county_fixes
    
    # ---- FIX DUPLICATE CITY NAMES ----
    print("\n=== FIXING DUPLICATE CITY NAMES ===")
    dup_fixes = fix_duplicate_city_names()
    total_fixed += dup_fixes
    
    print(f"\n=== TOTAL FILES MODIFIED: {total_fixed} ===")


if __name__ == '__main__':
    main()
