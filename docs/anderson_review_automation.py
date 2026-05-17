#!/usr/bin/env python3
"""
Anderson HAI Review Automation System
Powered by Scrape.do API

Fetches ALL Google reviews, filters for quality, generates website data and case studies.
"""

import json
import requests
import time
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AndersonReviewAutomation:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.scrape.do/plugin/google/maps"
        self.anderson_place_id = "ChIJURzG3EsHYIgRirAdHMx9MlU"  # From our test
        
        # Output directories
        self.website_dir = "/home/shyloh/.hermes/shared/anderson-website/api-data"
        self.case_studies_dir = "/home/shyloh/.hermes/shared/anderson-website/case-studies"
        self.backup_dir = "/home/shyloh/.openclaw/workspace/anderson-reviews-backup"
        
        # Create directories if they don't exist
        os.makedirs(self.website_dir, exist_ok=True)
        os.makedirs(self.case_studies_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    def make_api_request(self, endpoint: str, params: Dict[str, Any], max_retries: int = 3) -> Dict:
        """Make API request with retry logic"""
        params['token'] = self.api_token
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(max_retries):
            try:
                logger.info(f"API Request: {endpoint} (attempt {attempt + 1}/{max_retries})")
                response = requests.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    wait_time = 2 ** attempt
                    logger.warning(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                elif response.status_code == 502:
                    logger.warning("Transient error (502), retrying...")
                    time.sleep(1)
                    continue
                else:
                    response.raise_for_status()
                    
            except requests.RequestException as e:
                logger.error(f"Request failed: {e}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(1)
        
        raise Exception(f"Failed to get response after {max_retries} attempts")

    def get_all_reviews(self, min_rating: int = 4, max_reviews: int = 1000) -> List[Dict]:
        """Fetch all Anderson HAI reviews with specified minimum rating"""
        logger.info(f"Fetching Anderson HAI reviews (min rating: {min_rating})")
        
        all_reviews = []
        start = 0
        page_size = 20
        
        while len(all_reviews) < max_reviews:
            try:
                params = {
                    'place_id': self.anderson_place_id,
                    'start': start,
                    'num': page_size,
                    'sort': 'newest'
                }
                
                data = self.make_api_request('reviews', params)
                
                if 'reviews' not in data or not data['reviews']:
                    logger.info("No more reviews found")
                    break
                
                # Filter for high-rating reviews
                high_rating_reviews = [
                    review for review in data['reviews'] 
                    if review.get('rating', 0) >= min_rating
                ]
                
                all_reviews.extend(high_rating_reviews)
                logger.info(f"Collected {len(all_reviews)} high-rating reviews so far...")
                
                # Check if more pages available
                if 'pagination' not in data or 'next_page_token' not in data['pagination']:
                    logger.info("Reached end of reviews")
                    break
                    
                start += page_size
                time.sleep(1)  # Be nice to the API
                
            except Exception as e:
                logger.error(f"Error fetching reviews at page {start}: {e}")
                break
        
        logger.info(f"✅ Collected {len(all_reviews)} total high-rating reviews")
        return all_reviews

    def select_website_reviews(self, all_reviews: List[Dict], count: int = 25) -> List[Dict]:
        """Select best reviews for website display"""
        logger.info(f"Selecting top {count} reviews for website")
        
        # Prioritize detailed 5-star reviews
        detailed_5_star = [
            r for r in all_reviews 
            if r.get('rating') == 5 and len(r.get('snippet', '')) > 100
        ]
        
        # Add some authentic 4-star reviews for credibility
        authentic_4_star = [
            r for r in all_reviews 
            if r.get('rating') == 4 and len(r.get('snippet', '')) > 80
        ][:5]
        
        # Combine and select best ones
        selected = detailed_5_star[:20] + authentic_4_star
        
        # Sort by date (newest first) and limit
        selected.sort(key=lambda x: x.get('iso_date', ''), reverse=True)
        return selected[:count]

    def select_case_study_reviews(self, all_reviews: List[Dict], count: int = 15) -> List[Dict]:
        """Select detailed reviews perfect for case studies"""
        logger.info(f"Selecting {count} reviews for case studies")
        
        # Look for reviews with specific criteria
        case_study_candidates = []
        
        for review in all_reviews:
            snippet = review.get('snippet', '')
            rating = review.get('rating', 0)
            
            # Must be 5-star and have substantial detail
            if rating != 5 or len(snippet) < 150:
                continue
                
            # Look for reviews mentioning specific services or outcomes
            service_keywords = [
                'installation', 'repair', 'insulation', 'hvac', 'thermostat', 
                'heating', 'cooling', 'air conditioning', 'emergency', 'professional',
                'weatherization', 'ductwork', 'maintenance'
            ]
            
            quality_indicators = [
                'recommend', 'excellent', 'professional', 'knowledgeable', 
                'thorough', 'explained', 'helpful', 'courteous', 'timely',
                'exceeded', 'impressed', 'satisfied', 'grateful'
            ]
            
            snippet_lower = snippet.lower()
            service_mentions = sum(1 for keyword in service_keywords if keyword in snippet_lower)
            quality_mentions = sum(1 for indicator in quality_indicators if indicator in snippet_lower)
            
            # Score based on length, service mentions, and quality indicators
            score = len(snippet) + (service_mentions * 20) + (quality_mentions * 15)
            
            case_study_candidates.append({
                'review': review,
                'score': score,
                'service_mentions': service_mentions,
                'quality_mentions': quality_mentions
            })
        
        # Sort by score and select top candidates
        case_study_candidates.sort(key=lambda x: x['score'], reverse=True)
        return [candidate['review'] for candidate in case_study_candidates[:count]]

    def generate_website_data(self, all_reviews: List[Dict], selected_reviews: List[Dict]) -> Dict:
        """Generate JSON data for website consumption"""
        logger.info("Generating website data JSON")
        
        # Calculate statistics
        total_reviews = len(all_reviews)
        ratings_breakdown = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for review in all_reviews:
            rating = review.get('rating', 0)
            if 1 <= rating <= 5:
                ratings_breakdown[rating] += 1
        
        average_rating = sum(rating * count for rating, count in ratings_breakdown.items()) / max(total_reviews, 1)
        
        # Format selected reviews for website
        formatted_reviews = []
        for review in selected_reviews:
            formatted_review = {
                'id': review.get('review_id', ''),
                'author': review.get('user', {}).get('name', 'Anonymous'),
                'rating': review.get('rating', 5),
                'date': review.get('date', ''),
                'iso_date': review.get('iso_date', ''),
                'text': review.get('snippet', ''),
                'service_type': self.extract_service_type(review.get('snippet', '')),
                'has_photos': len(review.get('images', [])) > 0,
                'photo_count': len(review.get('images', [])),
                'local_guide': review.get('user', {}).get('local_guide', False),
                'owner_response': review.get('response', {}).get('snippet', '') if review.get('response') else None
            }
            formatted_reviews.append(formatted_review)
        
        website_data = {
            'generated_at': datetime.now().isoformat(),
            'source': 'scrape.do API',
            'business_name': 'Anderson Heating, Air & Insulation',
            'total_reviews_analyzed': total_reviews,
            'average_rating': round(average_rating, 2),
            'ratings_breakdown': ratings_breakdown,
            'featured_reviews_count': len(formatted_reviews),
            'featured_reviews': formatted_reviews,
            'summary_stats': {
                'excellent_service_mentions': self.count_keyword_mentions(all_reviews, ['excellent', 'outstanding', 'exceptional']),
                'professional_mentions': self.count_keyword_mentions(all_reviews, ['professional', 'knowledgeable', 'expert']),
                'recommend_mentions': self.count_keyword_mentions(all_reviews, ['recommend', 'highly recommend']),
                'timely_service_mentions': self.count_keyword_mentions(all_reviews, ['quick', 'fast', 'prompt', 'timely', 'same day'])
            }
        }
        
        return website_data

    def extract_service_type(self, snippet: str) -> str:
        """Extract primary service type from review text"""
        snippet_lower = snippet.lower()
        
        if any(word in snippet_lower for word in ['install', 'installation', 'new unit', 'replace']):
            return 'Installation'
        elif any(word in snippet_lower for word in ['repair', 'fix', 'broken', 'not working']):
            return 'Repair'
        elif any(word in snippet_lower for word in ['insulation', 'insulate', 'weatherization']):
            return 'Insulation'
        elif any(word in snippet_lower for word in ['maintenance', 'service', 'tune up', 'check']):
            return 'Maintenance'
        elif any(word in snippet_lower for word in ['emergency', 'urgent', '24/7']):
            return 'Emergency Service'
        else:
            return 'HVAC Service'

    def count_keyword_mentions(self, reviews: List[Dict], keywords: List[str]) -> int:
        """Count mentions of specific keywords across all reviews"""
        count = 0
        for review in reviews:
            snippet = review.get('snippet', '').lower()
            for keyword in keywords:
                count += snippet.count(keyword.lower())
        return count

    def generate_case_studies(self, case_study_reviews: List[Dict]) -> None:
        """Generate individual case study files"""
        logger.info(f"Generating {len(case_study_reviews)} case studies")
        
        for i, review in enumerate(case_study_reviews, 1):
            case_study = self.create_case_study(review, i)
            
            # Generate filename from customer name and service type
            customer_name = review.get('user', {}).get('name', f'Customer_{i}')
            safe_name = ''.join(c for c in customer_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_').lower()
            
            filename = f"case_study_{i:02d}_{safe_name}.json"
            filepath = os.path.join(self.case_studies_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(case_study, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Generated case study: {filename}")

    def create_case_study(self, review: Dict, case_number: int) -> Dict:
        """Create a detailed case study from a review"""
        snippet = review.get('snippet', '')
        user = review.get('user', {})
        
        # Extract key details
        service_type = self.extract_service_type(snippet)
        
        # Identify problem and solution from review text
        problem, solution = self.extract_problem_solution(snippet)
        
        case_study = {
            'case_number': case_number,
            'title': f"{service_type} Success Story - {user.get('name', 'Anderson Customer')}",
            'customer': {
                'name': user.get('name', 'Anonymous'),
                'location': 'Calhoun, GA Area',  # Anderson's service area
                'local_guide': user.get('local_guide', False),
                'review_count': user.get('reviews', 0)
            },
            'service': {
                'type': service_type,
                'date': review.get('date', ''),
                'iso_date': review.get('iso_date', ''),
                'rating': review.get('rating', 5)
            },
            'challenge': problem,
            'solution': solution,
            'outcome': {
                'customer_satisfaction': review.get('rating', 5),
                'full_testimonial': snippet,
                'key_highlights': self.extract_highlights(snippet),
                'would_recommend': 'recommend' in snippet.lower()
            },
            'anderson_response': review.get('response', {}).get('snippet', '') if review.get('response') else None,
            'photos': review.get('images', []),
            'generated_at': datetime.now().isoformat(),
            'source_review_id': review.get('review_id', '')
        }
        
        return case_study

    def extract_problem_solution(self, snippet: str) -> tuple:
        """Extract problem and solution from review text"""
        snippet_lower = snippet.lower()
        
        # Common problem indicators
        problem_keywords = {
            'not working': 'HVAC system malfunction',
            'broken': 'Equipment failure', 
            'no heat': 'Heating system failure',
            'no air': 'Air conditioning failure',
            'strange odor': 'HVAC system odor issues',
            'high bills': 'Energy efficiency concerns',
            'old unit': 'Aging HVAC equipment replacement needed',
            'emergency': 'Emergency HVAC service required'
        }
        
        # Common solution indicators
        solution_keywords = {
            'install': 'Professional installation service',
            'repair': 'Expert repair service',
            'fix': 'Professional troubleshooting and repair',
            'insulation': 'Energy efficiency insulation service', 
            'maintenance': 'Preventive maintenance service',
            'explain': 'Customer education and consultation',
            'options': 'Comprehensive service options provided'
        }
        
        problem = "Customer HVAC service needs"
        solution = "Anderson Heating, Air & Insulation professional service"
        
        # Find most specific problem
        for keyword, description in problem_keywords.items():
            if keyword in snippet_lower:
                problem = description
                break
        
        # Find most specific solution  
        for keyword, description in solution_keywords.items():
            if keyword in snippet_lower:
                solution = description
                break
        
        return problem, solution

    def extract_highlights(self, snippet: str) -> List[str]:
        """Extract key highlights from review text"""
        highlights = []
        snippet_lower = snippet.lower()
        
        highlight_patterns = [
            ('professional', 'Professional service team'),
            ('knowledgeable', 'Knowledgeable technicians'),
            ('explain', 'Clear communication and education'),
            ('timely', 'Prompt and timely service'),
            ('clean', 'Clean and respectful work practices'),
            ('fair price', 'Fair and transparent pricing'),
            ('recommend', 'Customer would recommend Anderson HAI'),
            ('local', 'Locally owned and operated business'),
            ('satisfied', 'High customer satisfaction')
        ]
        
        for keyword, highlight in highlight_patterns:
            if keyword in snippet_lower:
                highlights.append(highlight)
        
        return highlights[:5]  # Limit to top 5 highlights

    def save_backup(self, all_reviews: List[Dict]) -> None:
        """Save complete backup of all reviews"""
        backup_data = {
            'generated_at': datetime.now().isoformat(),
            'total_reviews': len(all_reviews),
            'source': 'scrape.do API',
            'anderson_place_id': self.anderson_place_id,
            'reviews': all_reviews
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'anderson_reviews_backup_{timestamp}.json')
        
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Backup saved: {backup_file}")

    def run_full_sync(self) -> Dict:
        """Run complete review sync process"""
        start_time = datetime.now()
        logger.info("🚀 Starting Anderson HAI review automation...")
        
        try:
            # Step 1: Fetch all high-rating reviews
            all_reviews = self.get_all_reviews(min_rating=4, max_reviews=500)
            
            if not all_reviews:
                raise Exception("No reviews found!")
            
            # Step 2: Select reviews for different purposes
            website_reviews = self.select_website_reviews(all_reviews, count=25)
            case_study_reviews = self.select_case_study_reviews(all_reviews, count=15)
            
            # Step 3: Generate website data
            website_data = self.generate_website_data(all_reviews, website_reviews)
            
            # Step 4: Save website data
            website_file = os.path.join(self.website_dir, 'reviews.json')
            with open(website_file, 'w') as f:
                json.dump(website_data, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ Website data saved: {website_file}")
            
            # Step 5: Generate case studies
            self.generate_case_studies(case_study_reviews)
            
            # Step 6: Save backup
            self.save_backup(all_reviews)
            
            # Step 7: Generate summary
            duration = datetime.now() - start_time
            summary = {
                'success': True,
                'duration_seconds': duration.total_seconds(),
                'total_reviews_processed': len(all_reviews),
                'website_reviews_selected': len(website_reviews),
                'case_studies_generated': len(case_study_reviews),
                'generated_at': datetime.now().isoformat(),
                'files_created': {
                    'website_data': website_file,
                    'case_studies': f"{len(case_study_reviews)} files in {self.case_studies_dir}",
                    'backup': f"Backup in {self.backup_dir}"
                }
            }
            
            logger.info("✅ Anderson review automation completed successfully!")
            logger.info(f"📊 Processed {len(all_reviews)} reviews in {duration.total_seconds():.1f}s")
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Review automation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'generated_at': datetime.now().isoformat()
            }

def main():
    """Main entry point"""
    API_TOKEN = "SCRAPE_DO_TOKEN_REMOVED"
    
    automation = AndersonReviewAutomation(API_TOKEN)
    result = automation.run_full_sync()
    
    # Print summary
    print("\n" + "="*50)
    print("ANDERSON HAI REVIEW AUTOMATION SUMMARY")
    print("="*50)
    
    if result['success']:
        print(f"✅ SUCCESS!")
        print(f"📊 Reviews processed: {result['total_reviews_processed']}")
        print(f"🌐 Website reviews: {result['website_reviews_selected']}")  
        print(f"📝 Case studies: {result['case_studies_generated']}")
        print(f"⏱️  Duration: {result['duration_seconds']:.1f}s")
        print(f"📁 Files: {result['files_created']}")
    else:
        print(f"❌ FAILED: {result['error']}")

if __name__ == "__main__":
    main()