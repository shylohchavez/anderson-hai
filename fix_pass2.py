#!/usr/bin/env python3
"""Second pass: fix hero text and remaining template issues."""
import os

SITE_DIR = os.path.dirname(os.path.abspath(__file__))

CITY_PAGES = {
    'plainville-ga': ('Plainville', 'Gordon County'),
    'trion-ga': ('Trion', 'Chattooga County'),
    'sugar-valley-ga': ('Sugar Valley', 'Gordon County'),
    'sonoraville-ga': ('Sonoraville', 'Gordon County'),
    'armuchee-ga': ('Armuchee', 'Floyd County'),
    'tunnel-hill-ga': ('Tunnel Hill', 'Whitfield County'),
    'tennga-ga': ('Tennga', 'Murray County'),
    'ranger-ga': ('Ranger', 'Gordon County'),
    'lyerly-ga': ('Lyerly', 'Chattooga County'),
    'chickamauga-ga': ('Chickamauga', 'Walker County'),
    'lafayette-ga': ('LaFayette', 'Walker County'),
    'ringgold-ga': ('Ringgold', 'Catoosa County'),
    'summerville-ga': ('Summerville', 'Chattooga County'),
    'redbud-ga': ('Redbud', 'Gordon County'),
    'rocky-face-ga': ('Rocky Face', 'Whitfield County'),
}

COUNTY_PAGES = {
    'walker-county-ga': ('Walker County', 'LaFayette'),
    'floyd-county-ga': ('Floyd County', 'Rome'),
    'catoosa-county-ga': ('Catoosa County', 'Ringgold'),
    'gilmer-county-ga': ('Gilmer County', 'Ellijay'),
    'whitfield-county-ga': ('Whitfield County', 'Dalton'),
    'murray-county-ga': ('Murray County', 'Chatsworth'),
    'pickens-county-ga': ('Pickens County', 'Jasper'),
    'bartow-county-ga': ('Bartow County', 'Cartersville'),
}

OLD_HERO = 'Anderson Heating, Air & Insulation (formerly John Anderson Service Company, est. January 1978) delivers BPI-certified HVAC repair, installation, insulation, and whole-home energy solutions to Calhoun and all of Gordon County. The Paws-itive Choice for families who want real comfort, not just a new box.'

fixed = 0

# Fix city pages
for slug, (city, county) in CITY_PAGES.items():
    filepath = os.path.join(SITE_DIR, f'{slug}.html')
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    new_hero = f'Anderson Heating, Air & Insulation (formerly John Anderson Service Company, est. January 1978) delivers BPI-certified HVAC repair, installation, insulation, and whole-home energy solutions to {city} and all of {county}. The Paws-itive Choice for families who want real comfort, not just a new box.'
    content = content.replace(OLD_HERO, new_hero)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Fixed hero: {slug}.html')
        fixed += 1

# Fix county pages
for slug, (county, main_city) in COUNTY_PAGES.items():
    filepath = os.path.join(SITE_DIR, f'{slug}.html')
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    new_hero = f'Anderson Heating, Air & Insulation (formerly John Anderson Service Company, est. January 1978) delivers BPI-certified HVAC repair, installation, insulation, and whole-home energy solutions to {main_city} and all of {county}. The Paws-itive Choice for families who want real comfort, not just a new box.'
    content = content.replace(OLD_HERO, new_hero)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Fixed hero: {slug}.html')
        fixed += 1

print(f'\nTotal hero fixes: {fixed}')
