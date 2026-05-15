#!/usr/bin/env python3
"""
CompanyCam Geo SEO Gallery Generator
Pulls geotagged photos via CompanyCam API and generates hidden SEO gallery
"""
import requests
import json
from datetime import datetime
import os

# CompanyCam API Configuration
COMPANYCAM_API_TOKEN = "YOUR_COMPANYCAM_API_TOKEN"  # Set in environment or replace
COMPANYCAM_BASE_URL = "https://api.companycam.com/v2"

def fetch_companycam_photos():
    """Fetch all photos with geotags from CompanyCam"""
    headers = {
        'Authorization': f'Bearer {COMPANYCAM_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    photos = []
    page = 1
    
    try:
        # First get all projects
        projects_response = requests.get(
            f"{COMPANYCAM_BASE_URL}/projects",
            headers=headers,
            params={'per_page': 100}
        )
        projects_response.raise_for_status()
        projects = projects_response.json().get('data', [])
        
        print(f"Found {len(projects)} projects")
        
        # Get photos from each project
        for project in projects:
            project_id = project['id']
            project_name = project.get('name', 'Unnamed Project')
            
            photos_response = requests.get(
                f"{COMPANYCAM_BASE_URL}/projects/{project_id}/photos",
                headers=headers,
                params={'per_page': 100}
            )
            
            if photos_response.status_code == 200:
                project_photos = photos_response.json().get('data', [])
                
                for photo in project_photos:
                    # Only include photos with GPS coordinates
                    if photo.get('latitude') and photo.get('longitude'):
                        photos.append({
                            'id': photo['id'],
                            'url': photo['uris']['large'],
                            'thumbnail': photo['uris']['medium'],
                            'latitude': photo['latitude'],
                            'longitude': photo['longitude'],
                            'created_at': photo['created_at'],
                            'project_name': project_name,
                            'project_address': project.get('address', {}).get('formatted', 'Georgia'),
                            'description': photo.get('annotation', 'HVAC project photo')
                        })
                
                print(f"Project '{project_name}': {len(project_photos)} photos")
        
        print(f"Total geotagged photos found: {len(photos)}")
        return photos
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return []

def generate_hidden_geo_gallery(photos):
    """Generate hidden HTML gallery with rich geo schema markup"""
    
    # Generate schema markup for each photo
    photo_schemas = []
    for photo in photos:
        photo_schema = {
            "@type": "ImageObject",
            "contentUrl": photo['url'],
            "thumbnailUrl": photo['thumbnail'],
            "description": f"HVAC project photo from {photo['project_address']}",
            "contentLocation": {
                "@type": "Place",
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": photo['latitude'],
                    "longitude": photo['longitude']
                },
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": photo['project_address'],
                    "addressRegion": "GA",
                    "addressCountry": "US"
                }
            },
            "dateCreated": photo['created_at'],
            "creator": {
                "@type": "Organization",
                "name": "Anderson Heating, Air & Insulation"
            }
        }
        photo_schemas.append(photo_schema)
    
    # Main schema markup
    main_schema = {
        "@context": "https://schema.org",
        "@type": "ImageGallery",
        "name": "Anderson HAI Service Area Photos",
        "description": "Geotagged photos from HVAC and energy efficiency projects across Northwest Georgia",
        "provider": {
            "@type": "HVACBusiness",
            "name": "Anderson Heating, Air & Insulation",
            "telephone": "(706) 629-0749",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "519 Pine Street",
                "addressLocality": "Calhoun",
                "addressRegion": "GA",
                "postalCode": "30701"
            }
        },
        "associatedMedia": photo_schemas,
        "areaServed": [
            {"@type": "City", "name": "Calhoun", "addressRegion": "GA"},
            {"@type": "City", "name": "Dalton", "addressRegion": "GA"},
            {"@type": "City", "name": "Rome", "addressRegion": "GA"},
            {"@type": "City", "name": "Cartersville", "addressRegion": "GA"}
        ]
    }
    
    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, follow">
    <title>Anderson HAI Service Area Photos - Internal</title>
    <meta name="description" content="Internal geotagged photo gallery for Anderson Heating, Air & Insulation service area mapping">
    <link rel="canonical" href="https://johnandersonservice.com/companycam-geo-seo.html">
    
    <!-- Rich Geo Schema for SEO -->
    <script type="application/ld+json">
    {json.dumps(main_schema, indent=2)}
    </script>
    
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .notice {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .gallery {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }}
        .photo-item {{ background: white; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .photo-item img {{ width: 100%; height: 180px; object-fit: cover; border-radius: 3px; }}
        .photo-info {{ margin-top: 8px; font-size: 0.9em; color: #555; }}
        .geo-info {{ background: #e3f2fd; padding: 5px; border-radius: 3px; font-size: 0.8em; color: #1565c0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="notice">
            <strong>Internal SEO Gallery:</strong> This page contains geotagged photos for search engine optimization and service area mapping. Not intended for public browsing.
        </div>
        
        <h1>Anderson Heating, Air & Insulation - Service Area Documentation</h1>
        <p>Geotagged project photos across Calhoun, Dalton, Rome, Cartersville, and surrounding Northwest Georgia areas.</p>
        
        <div class="gallery">
"""
    
    # Add each photo
    for photo in photos:
        html_content += f"""
            <div class="photo-item">
                <img src="{photo['thumbnail']}" alt="HVAC project photo from {photo['project_address']}" loading="lazy">
                <div class="photo-info">
                    <strong>Location:</strong> {photo['project_address']}<br>
                    <strong>Date:</strong> {datetime.fromisoformat(photo['created_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d')}<br>
                    <div class="geo-info">
                        📍 {photo['latitude']}, {photo['longitude']}
                    </div>
                </div>
            </div>
"""
    
    html_content += """
        </div>
        
        <footer style="margin-top: 40px; padding: 20px; background: white; text-align: center; border-radius: 5px;">
            <p><strong>Anderson Heating, Air & Insulation</strong><br>
            519 Pine Street, Calhoun, GA 30701<br>
            Phone: <a href="tel:(706)629-0749">(706) 629-0749</a></p>
            <p style="font-size: 0.9em; color: #666;">
                Serving Northwest Georgia since 1978 • BPI Certified Energy Auditors
            </p>
        </footer>
    </div>
</body>
</html>"""
    
    return html_content

def main():
    """Main execution"""
    print("CompanyCam Geo SEO Gallery Generator")
    print("=" * 40)
    
    # Check for API token
    if COMPANYCAM_API_TOKEN == "YOUR_COMPANYCAM_API_TOKEN":
        print("❌ Please set your CompanyCam API token in the script or environment variable")
        print("Get token from: https://app.companycam.com/access_tokens")
        return
    
    # Fetch photos
    print("Fetching geotagged photos from CompanyCam API...")
    photos = fetch_companycam_photos()
    
    if not photos:
        print("❌ No geotagged photos found or API error")
        return
    
    # Generate HTML gallery
    print(f"Generating hidden geo SEO gallery with {len(photos)} photos...")
    html_content = generate_hidden_geo_gallery(photos)
    
    # Save to website
    output_file = "companycam-geo-seo.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated: {output_file}")
    print(f"📊 Photos included: {len(photos)}")
    print("🔍 Page is hidden from humans (noindex) but crawlable for geo SEO")
    print("📍 Rich geo schema markup included for each photo location")

if __name__ == "__main__":
    main()