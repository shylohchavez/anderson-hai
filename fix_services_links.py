#!/usr/bin/env python3
import os
import re

# List of files that need fixing (excluding about.html and index.html which are already fixed)
files_to_fix = [
    "adairsville-ga.html", "armuchee-ga.html", "bartow-county-ga.html", "blog.html", 
    "calhoun-ga.html", "cartersville-ga.html", "catoosa-county-ga.html", "chatsworth-ga.html",
    "chickamauga-ga.html", "contact.html", "dalton-ga.html", "ellijay-ga.html", 
    "fairmount-ga.html", "floyd-county-ga.html", "gilmer-county-ga.html", "gordon-county-ga.html",
    "jasper-ga.html", "lafayette-ga.html", "lyerly-ga.html", "murray-county-ga.html",
    "pickens-county-ga.html", "plainville-ga.html", "ranger-ga.html", "redbud-ga.html",
    "resaca-ga.html", "ringgold-ga.html", "rocky-face-ga.html", "rome-ga.html",
    "sonoraville-ga.html", "sugar-valley-ga.html", "summerville-ga.html", "tennga-ga.html",
    "trion-ga.html", "tunnel-hill-ga.html", "walker-county-ga.html", "whitfield-county-ga.html"
]

# Pattern to match the Services div structure
old_pattern = '''                    <div class="space-y-1 text-xs">
                        <div>HVAC Repair & Install</div>
                        <div>Heat Pumps & Mini-Splits</div>
                        <div>Insulation & Weatherization</div>
                        <div>Duct Cleaning & IAQ</div>
                        <div>Custom Sheet Metal</div>
                        <div>Energy Audits</div>
                    </div>'''

# Replacement with clickable links
new_pattern = '''                    <div class="space-y-1 text-xs">
                        <a href="hvac-repair-install.html" class="block hover:text-white">HVAC Repair & Install</a>
                        <a href="heat-pump-mini-split.html" class="block hover:text-white">Heat Pumps & Mini-Splits</a>
                        <a href="insulation-air-sealing.html" class="block hover:text-white">Insulation & Weatherization</a>
                        <a href="duct-cleaning.html" class="block hover:text-white">Duct Cleaning & IAQ</a>
                        <a href="custom-sheet-metal.html" class="block hover:text-white">Custom Sheet Metal</a>
                        <a href="whole-home-energy-audits.html" class="block hover:text-white">Energy Audits</a>
                    </div>'''

fixed_count = 0
for filename in files_to_fix:
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_pattern in content:
                new_content = content.replace(old_pattern, new_pattern)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ Fixed {filename}")
                fixed_count += 1
            else:
                print(f"⚠️  Pattern not found in {filename}")
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

print(f"\n🎉 Fixed {fixed_count} files successfully!")
