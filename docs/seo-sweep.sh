#!/bin/bash
# ============================================================
# ANDERSON HAI FULL SEO SWEEP SCRIPT
# Executed: 2026-05-14
# ============================================================
set -e
cd ~/.hermes/shared/anderson-website

echo "=== PHASE 1: Title/Meta Optimization ==="

# --- Homepage ---
sed -i 's|<title>Anderson Heating, Air & Insulation | Anderson HAI</title>|<title>Anderson Heating, Air \&amp; Insulation Calhoun GA | #1 HVAC, AC Repair \&amp; Insulation Since 1978 | (706) 629-0749</title>|' index.html

# --- About ---
sed -i 's|<title>About Anderson Heating, Air & Insulation | Anderson HAI</title>|<title>About Anderson Heating, Air \&amp; Insulation | Family-Owned Since 1978 | Calhoun GA HVAC</title>|' about.html

# --- Contact ---
sed -i 's|<title>Contact Anderson Heating, Air & Insulation | Anderson HAI</title>|<title>Contact Anderson Heating, Air \&amp; Insulation | Call (706) 629-0749 | Calhoun GA</title>|' contact.html

# --- Reviews ---
sed -i 's|<title>632+ Google Reviews | Anderson HAI</title>|<title>632+ Google Reviews | Anderson Heating, Air \&amp; Insulation Calhoun GA | 4.8★ Rating</title>|' reviews.html

# --- Financing ---
sed -i 's|<title>Financing &amp; Discounts | Anderson HAI</title>|<title>HVAC Financing \&amp; Senior/Military Discounts | Anderson Heating, Air \&amp; Insulation Calhoun GA</title>|' financing.html

# --- Service Area ---
sed -i 's|<title>Service Area | Anderson HAI</title>|<title>HVAC Service Area | Calhoun, Dalton, Rome, Cartersville GA \&amp; NW Georgia | Anderson HAI</title>|' service-area.html

# --- Maintenance Plan ---
sed -i 's|<title>Maintenance Plans | Anderson HAI</title>|<title>HVAC Maintenance Plans Calhoun GA | Preventive AC \&amp; Heating Service | Anderson HAI</title>|' maintenance-plan.html

# --- Emergency AC Repair (generic) ---
sed -i 's|<title>Calhoun GA HVAC | Anderson HAI</title>|<title>Emergency AC Repair Calhoun GA | 24/7 Same-Day Service | Anderson Heating, Air \&amp; Insulation</title>|' emergency-ac-repair.html

# --- City pages: optimize titles with top keywords ---
# Calhoun (hvac calhoun ga: 50 vol, ac repair calhoun ga: 40 vol)
sed -i 's|<title>HVAC in Calhoun GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)</title>|<title>HVAC Calhoun GA | AC Repair, Heating \&amp; Insulation | 48 Years, 632+ Reviews | Anderson HAI</title>|' calhoun-ga.html

# Dalton (hvac dalton ga: 110 vol, ac repair dalton ga: 20 vol)
sed -i 's|<title>HVAC in Dalton GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)</title>|<title>HVAC Dalton GA | AC Repair \&amp; Heating Services | Same-Day Service | Anderson HAI (706) 629-0749</title>|' dalton-ga.html

# Rome (hvac rome ga: 140 vol, ac repair rome ga: 70 vol)
sed -i 's|<title>HVAC in Rome GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)</title>|<title>HVAC Rome GA | AC Repair \&amp; Furnace Service | 24/7 Emergency Available | Anderson HAI</title>|' rome-ga.html

# Cartersville (hvac cartersville ga: 110, air conditioning cartersville ga: 90)
sed -i 's|<title>HVAC in Cartersville GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)</title>|<title>HVAC Cartersville GA | Air Conditioning \&amp; Heating Repair | BPI Certified | Anderson HAI</title>|' cartersville-ga.html

# Adairsville
sed -i 's|<title>HVAC in Adairsville GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)</title>|<title>HVAC Adairsville GA | AC Repair \&amp; Heating | Trusted Since 1978 | Anderson HAI</title>|' adairsville-ga.html

# Chatsworth (ac repair chatsworth ga: 10 vol)
sed -i 's|<title>HVAC in Chatsworth GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)</title>|<title>HVAC Chatsworth GA | AC Repair, Heat Pumps \&amp; Insulation | Anderson Heating, Air \&amp; Insulation</title>|' chatsworth-ga.html

# Jasper (hvac jasper ga: 70, air conditioning jasper ga: 50, furnace repair jasper ga: 50)
sed -i 's|<title>HVAC in Jasper GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)</title>|<title>HVAC Jasper GA | Air Conditioning \&amp; Furnace Repair | 24/7 Emergency | Anderson HAI</title>|' jasper-ga.html

# Ellijay (hvac ellijay ga: 50, ac repair ellijay ga: 20)
sed -i 's|<title>HVAC in Ellijay GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)</title>|<title>HVAC Ellijay GA | AC Repair \&amp; Heat Pump Installation | Serving Gilmer County | Anderson HAI</title>|' ellijay-ga.html

# Fairmount
sed -i 's|<title>HVAC in Fairmount GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)</title>|<title>HVAC Fairmount GA | AC Repair \&amp; Heating Service | Family-Owned Since 1978 | Anderson HAI</title>|' fairmount-ga.html

# Resaca
sed -i 's|<title>HVAC in Resaca GA | AC Repair, Heating & Insulation | Anderson HAI (Formerly John Anderson Service Co.)</title>|<title>HVAC Resaca GA | AC Repair \&amp; Heating | Just Minutes From Our Shop | Anderson HAI</title>|' resaca-ga.html

echo "Titles updated on all key pages."

echo "=== PHASE 1b: Meta descriptions ==="
# Update meta descriptions with keyword-optimized versions for main pages

# Homepage
sed -i 's|<meta name="description" content="Anderson Heating, Air & Insulation since 1978 - BPI Certified HVAC, insulation, weatherization, duct cleaning & more in Calhoun, Dalton, Rome & NW Georgia. T...">|<meta name="description" content="Anderson Heating, Air \&amp; Insulation — Calhoun GA\x27s #1 HVAC company since 1978. AC repair, heat pumps, insulation, duct cleaning. BPI certified, 632+ reviews, 24/7 emergency. Call (706) 629-0749.">|' index.html

echo "Meta descriptions updated."
echo "Phase 1 complete."
