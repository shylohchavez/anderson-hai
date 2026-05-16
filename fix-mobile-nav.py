#!/usr/bin/env python3
"""Fix mobile navigation issues across ALL pages:
1. Fix skip-to-content link (index.html uses wrong approach)
2. Remove harmful inline !important style from hamburger buttons
3. Normalize hamburger button classes to include border
"""

import os
import re
import glob

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
fixed_files = []
errors = []

# Get all HTML files (not backups)
html_files = glob.glob(os.path.join(SITE_DIR, '**/*.html'), recursive=True)
html_files = [f for f in html_files if not f.endswith(('.bak-seo', '.backup', '.good'))]

for filepath in sorted(html_files):
    relpath = os.path.relpath(filepath, SITE_DIR)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # FIX 1: Skip-to-content link on index.html
        # Replace the old absolute/-top-10 approach with sr-only
        old_skip = '<a href="#main-content" class="absolute -top-10 focus:top-2 focus:left-2 focus:z-[100] focus:bg-white focus:text-anderson-purple focus:px-4 focus:py-2 focus:rounded-lg focus:shadow-lg focus:font-semibold" style="position: absolute; top: -40px;" id="skip-to-content">Skip to main content</a>'
        new_skip = '<a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[100] focus:bg-white focus:text-anderson-purple focus:px-4 focus:py-2 focus:rounded-lg focus:shadow-lg focus:font-semibold" id="skip-to-content">Skip to main content</a>'
        
        if old_skip in content:
            content = content.replace(old_skip, new_skip)
            changes.append('fixed skip-to-content (absolute→sr-only)')
        
        # FIX 2: Hamburger button - remove inline style, normalize classes
        # Pattern: button with id="mobile-menu-btn" and the problematic inline style
        
        # Variant A: Has border border-gray-300 in class + inline style
        old_btn_a = 'class="md:hidden inline-flex items-center justify-center p-2 rounded-lg hover:bg-gray-100 border border-gray-300" style="display: inline-flex !important; padding: 8px; border: 1px solid #d1d5db; border-radius: 8px;"'
        new_btn = 'class="md:hidden inline-flex items-center justify-center p-2 rounded-lg hover:bg-gray-100 border border-gray-300"'
        
        if old_btn_a in content:
            content = content.replace(old_btn_a, new_btn)
            changes.append('removed inline !important from hamburger (variant A)')
        
        # Variant B: Missing border classes in class + inline style  
        old_btn_b = 'class="md:hidden inline-flex items-center justify-center p-2 rounded-lg hover:bg-gray-100" style="display: inline-flex !important; padding: 8px; border: 1px solid #d1d5db; border-radius: 8px;"'
        
        if old_btn_b in content:
            content = content.replace(old_btn_b, new_btn)
            changes.append('removed inline !important + added border classes (variant B)')
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_files.append((relpath, changes))
    except Exception as e:
        errors.append((relpath, str(e)))

print(f"\n{'='*60}")
print(f"MOBILE NAV FIX RESULTS")
print(f"{'='*60}")
print(f"Files scanned: {len(html_files)}")
print(f"Files modified: {len(fixed_files)}")
print(f"Errors: {len(errors)}")
print()

if fixed_files:
    print("MODIFIED FILES:")
    for path, changes in fixed_files:
        print(f"  ✅ {path}")
        for c in changes:
            print(f"     → {c}")

if errors:
    print("\nERRORS:")
    for path, err in errors:
        print(f"  ❌ {path}: {err}")

# Verify: check no inline !important remains
print(f"\n{'='*60}")
print("VERIFICATION:")
remaining_important = 0
remaining_old_skip = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'display: inline-flex !important' in content:
        remaining_important += 1
        print(f"  ⚠️  Still has !important: {os.path.relpath(filepath, SITE_DIR)}")
    if 'top: -40px' in content and 'skip-to-content' in content:
        remaining_old_skip += 1
        print(f"  ⚠️  Still has old skip link: {os.path.relpath(filepath, SITE_DIR)}")

if remaining_important == 0 and remaining_old_skip == 0:
    print("  ✅ All pages clean - no inline !important, no old skip links")
print(f"{'='*60}")
