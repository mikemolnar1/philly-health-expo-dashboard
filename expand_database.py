#!/usr/bin/env python3

import requests
import json
import time
import csv
from typing import List, Dict, Set
from urllib.parse import quote_plus

# Target cities/counties for Philadelphia metro area
PHILADELPHIA_METRO_CITIES = {
    # PA counties: Philadelphia, Montgomery, Delaware, Chester, Bucks  
    'philadelphia', 'upper darby', 'chester', 'norristown', 'conshohocken', 
    'king of prussia', 'lansdale', 'doylestown', 'media', 'west chester',
    'phoenixville', 'coatesville', 'wayne', 'bryn mawr', 'ardmore', 'villanova',
    'elkins park', 'cheltenham', 'warminster', 'warrington', 'newtown square',
    'plymouth meeting', 'exton', 'downingtown', 'newtown', 'yardley',
    'fallsington', 'levittown', 'bensalem', 'trevose', 'bristol',
    # NJ counties: Camden, Burlington, Gloucester
    'camden', 'cherry hill', 'trenton', 'burlington', 'moorestown',
    'mount laurel', 'marlton', 'voorhees', 'gloucester',
    # Delaware area
    'wilmington'
}

# Search terms organized by category
SEARCH_CATEGORIES = {
    # Legal Aid & Advocacy
    'Legal Aid & Advocacy': [
        'legal aid', 'legal services', 'advocacy', 'legal clinic', 'civil rights',
        'immigration legal', 'tenant rights', 'consumer protection'
    ],
    
    # Financial Literacy & Benefits
    'Financial Literacy & Benefits': [
        'financial literacy', 'tax preparation', 'VITA', 'benefits enrollment',
        'financial counseling', 'economic empowerment', 'credit counseling'
    ],
    
    # Education & Literacy
    'Education & Literacy': [
        'adult literacy', 'GED program', 'ESL english', 'education',
        'literacy', 'english learners', 'basic education', 'workforce training'
    ],
    
    # Veterans Services
    'Veterans Services': [
        'veterans', 'veteran services', 'military families', 'veteran support'
    ],
    
    # Senior & Elder Services
    'Senior & Elder Services': [
        'senior services', 'elder', 'aging', 'seniors', 'elderly',
        'senior center', 'eldercare', 'senior support'
    ],
    
    # Substance Abuse & Recovery
    'Substance Abuse & Recovery': [
        'addiction', 'recovery', 'substance abuse', 'drug treatment',
        'alcohol treatment', 'rehabilitation', 'addiction recovery'
    ],
    
    # Domestic Violence & Crisis
    'Domestic Violence & Crisis': [
        'domestic violence', 'crisis services', 'crisis intervention',
        'domestic abuse', 'shelter', 'crisis center', 'emergency services'
    ],
    
    # Re-Entry & Returning Citizens
    'Re-Entry & Returning Citizens': [
        'reentry', 'returning citizens', 'formerly incarcerated',
        'prisoner reentry', 'criminal justice', 'second chance'
    ],
    
    # Childcare & Early Childhood
    'Childcare & Early Childhood': [
        'childcare', 'early childhood', 'head start', 'daycare',
        'preschool', 'child development', 'early learning'
    ],
    
    # Housing & Homelessness
    'Housing & Homelessness': [
        'homelessness', 'housing', 'homeless services', 'affordable housing',
        'housing assistance', 'homeless shelter', 'transitional housing'
    ],
    
    # Immigrant & Refugee Services
    'Immigrant & Refugee Services': [
        'immigrant', 'refugee', 'resettlement', 'immigration',
        'refugee services', 'asylum', 'new americans'
    ],
    
    # Digital Inclusion & Tech Access
    'Digital Inclusion & Tech Access': [
        'digital inclusion', 'technology', 'computer literacy',
        'digital divide', 'computer access', 'tech training'
    ],
    
    # Employment & Workforce Development
    'Employment & Workforce Development': [
        'employment', 'workforce development', 'job training',
        'career services', 'vocational training', 'entrepreneurship',
        'small business', 'mentorship', 'job placement'
    ],
    
    # Transportation
    'Transportation': [
        'transportation assistance', 'medical transportation',
        'transit', 'transportation services'
    ],
    
    # Disability Services
    'Disability Services': [
        'disability', 'autism', 'developmental disabilities',
        'disability services', 'special needs', 'accessible'
    ],
    
    # Specialized Health Services
    'Health & Wellness': [
        'HIV AIDS', 'dental health', 'vision eye care', 'nutrition',
        'diabetes', 'cancer support', 'maternal health', 'family planning',
        'healthcare navigation', 'insurance enrollment', 'community health'
    ]
}

# Category to Expo Zone mapping
EXPO_ZONES = {
    'Wellness Zone': [
        'Health & Wellness', 'Mental Health & Counseling', 
        'Substance Abuse & Recovery', 'Disability Services'
    ],
    'Career Zone': [
        'Employment & Workforce Development', 'Education & Literacy',
        'Financial Literacy & Benefits'
    ],
    'Family Resource Hub': [
        'Youth Services', 'Senior & Elder Services', 'Childcare & Early Childhood',
        'Domestic Violence & Crisis', 'Housing & Homelessness', 'Food & Nutrition'
    ],
    'Community Partners Pavilion': [
        'Legal Aid & Advocacy', 'Immigrant & Refugee Services',
        'Veterans Services', 'Re-Entry & Returning Citizens',
        'Digital Inclusion & Tech Access', 'Transportation', 'Community Services'
    ]
}

def search_nonprofits(query: str, state: str = 'PA', max_pages: int = 3) -> List[Dict]:
    """Search ProPublica Nonprofit Explorer API for organizations"""
    organizations = []
    base_url = "https://projects.propublica.org/nonprofits/api/v2/search.json"
    
    for page in range(1, max_pages + 1):
        try:
            params = {
                'q': query,
                'state[id]': state,
                'page': page
            }
            
            # Build URL manually for proper encoding
            url = f"{base_url}?q={quote_plus(query)}&state%5Bid%5D={state}&page={page}"
            
            print(f"Searching: {query} (page {page})")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'organizations' in data and data['organizations']:
                organizations.extend(data['organizations'])
            
            # Check if there are more pages
            if page >= data.get('num_pages', 1):
                break
                
            # Rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error searching '{query}' page {page}: {e}")
            continue
    
    return organizations

def is_in_target_area(city: str) -> bool:
    """Check if city is in Philadelphia metro area"""
    if not city:
        return False
    return city.lower() in PHILADELPHIA_METRO_CITIES

def calculate_distance_tier(city: str) -> int:
    """Calculate distance tier based on city location (simplified)"""
    if not city:
        return 3
    
    city_lower = city.lower()
    
    # Tier 1: Philadelphia and immediate suburbs (0-10 miles)
    tier1_cities = {
        'philadelphia', 'upper darby', 'elkins park', 'cheltenham', 
        'ardmore', 'bryn mawr', 'wayne', 'plymouth meeting'
    }
    
    # Tier 2: Closer suburbs (10-20 miles)  
    tier2_cities = {
        'norristown', 'media', 'king of prussia', 'conshohocken',
        'newtown square', 'phoenixville', 'camden', 'cherry hill'
    }
    
    if city_lower in tier1_cities:
        return 1
    elif city_lower in tier2_cities:
        return 2
    else:
        return 3

def get_expo_zone(category: str) -> str:
    """Get expo zone for a category"""
    for zone, categories in EXPO_ZONES.items():
        if category in categories:
            return zone
    return 'Community Partners Pavilion'

def collect_all_organizations():
    """Collect organizations from all search categories"""
    all_organizations = []
    seen_eins = set()
    
    for category, search_terms in SEARCH_CATEGORIES.items():
        print(f"\n=== Searching {category} ===")
        
        for term in search_terms:
            organizations = search_nonprofits(term, max_pages=2)
            
            for org in organizations:
                # Skip if we've seen this EIN already
                if org.get('ein') in seen_eins:
                    continue
                
                # Filter for Philadelphia metro area
                if not is_in_target_area(org.get('city', '')):
                    continue
                
                # Add our metadata
                org['category'] = category
                org['distance_tier'] = calculate_distance_tier(org.get('city', ''))
                org['found_via'] = term
                org['expo_zone'] = get_expo_zone(category)
                
                all_organizations.append(org)
                seen_eins.add(org.get('ein'))
                
                print(f"  Found: {org.get('name')} ({org.get('city')})")
    
    print(f"\nTotal organizations found: {len(all_organizations)}")
    return all_organizations

def load_existing_organizations() -> List[Dict]:
    """Load existing organizations from the dashboard"""
    # Read current dashboard to extract existing data
    try:
        with open('/Users/matrixmolnar/.openclaw/workspace/philly-health-expo/index.html', 'r') as f:
            content = f.read()
            
        # Extract the nonprofitData JavaScript array
        start = content.find('const nonprofitData = [')
        if start == -1:
            return []
            
        start += len('const nonprofitData = ')
        end = content.find('];', start)
        if end == -1:
            return []
            
        data_str = content[start:end+1]
        
        # Parse as JSON (this is a simplified approach)
        # In practice, we'd use a proper JS parser, but this works for the current format
        import ast
        # Remove JS-style comments and fix format for Python
        data_str = data_str.replace('null', 'None')
        
        try:
            existing_data = eval(data_str)
            print(f"Loaded {len(existing_data)} existing organizations")
            return existing_data
        except:
            print("Could not parse existing data, starting fresh")
            return []
            
    except Exception as e:
        print(f"Error loading existing data: {e}")
        return []

def merge_and_deduplicate(existing: List[Dict], new: List[Dict]) -> List[Dict]:
    """Merge existing and new organizations, removing duplicates by EIN"""
    seen_eins = set()
    merged = []
    
    # Add existing organizations first
    for org in existing:
        ein = org.get('ein')
        if ein and ein not in seen_eins:
            # Ensure all new fields exist
            if 'expo_zone' not in org:
                org['expo_zone'] = get_expo_zone(org.get('category', 'Community Services'))
            
            merged.append(org)
            seen_eins.add(ein)
    
    # Add new organizations
    for org in new:
        ein = org.get('ein')
        if ein and ein not in seen_eins:
            merged.append(org)
            seen_eins.add(ein)
    
    return merged

if __name__ == "__main__":
    print("Starting comprehensive nonprofit search for Philadelphia Health Expo...")
    
    # Load existing organizations
    existing_orgs = load_existing_organizations()
    
    # Collect new organizations
    new_orgs = collect_all_organizations()
    
    # Merge and deduplicate
    all_orgs = merge_and_deduplicate(existing_orgs, new_orgs)
    
    # Save to JSON file for dashboard rebuild
    with open('/Users/matrixmolnar/.openclaw/workspace/philly-health-expo/expanded_data.json', 'w') as f:
        json.dump(all_orgs, f, indent=2)
    
    print(f"\nFinal count: {len(all_orgs)} organizations")
    print(f"Saved to expanded_data.json")
    
    # Show category breakdown
    print("\nCategory breakdown:")
    category_counts = {}
    for org in all_orgs:
        cat = org.get('category', 'Unknown')
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for cat, count in sorted(category_counts.items()):
        print(f"  {cat}: {count}")