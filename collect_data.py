#!/usr/bin/env python3
import requests
import json
import time
import re
from typing import Dict, List, Set
import math

# Search terms for nonprofits
SEARCH_TERMS = [
    "health", "wellness", "mental health", "workforce development", 
    "employment", "job training", "disability services", "youth services",
    "community health", "substance abuse", "housing assistance", 
    "food bank", "veterans services"
]

# Philadelphia metro cities to include
PHILLY_METRO_CITIES = {
    # PA cities
    'philadelphia', 'upper darby', 'chester', 'norristown', 'conshohocken', 
    'king of prussia', 'lansdale', 'doylestown', 'media', 'west chester',
    'drexel hill', 'yeadon', 'ardmore', 'bryn mawr', 'villanova', 'wayne',
    'berwyn', 'devon', 'malvern', 'paoli', 'downingtown', 'coatesville',
    'phoenixville', 'pottstown', 'collegeville', 'royersford', 'limerick',
    'schwenksville', 'harleysville', 'souderton', 'telford', 'hatfield',
    'north wales', 'ambler', 'fort washington', 'warminster', 'warrington',
    'newtown', 'richboro', 'holland', 'southampton', 'feasterville',
    'trevose', 'bensalem', 'bristol', 'levittown', 'morrisville',
    # NJ cities
    'camden', 'cherry hill', 'gloucester', 'deptford', 'washington township',
    'monroe township', 'williamstown', 'sicklerville', 'blackwood',
    'turnersville', 'sewell', 'pitman', 'wenonah', 'woodbury', 'glassboro'
}

# NTEE code categories
NTEE_CATEGORIES = {
    'Health & Wellness': ['E', 'G', 'H'],
    'Mental Health': ['F'],
    'Employment/Workforce': ['J'],
    'Youth Services': ['O'],
    'Disability Services': ['P8'],
    'Community Services': ['P', 'S'],
    'Housing': ['L'],
    'Food/Nutrition': ['K']
}

def get_ntee_category(ntee_code: str) -> str:
    if not ntee_code:
        return "Other"
    
    ntee_code = ntee_code.upper().strip()
    
    for category, codes in NTEE_CATEGORIES.items():
        for code in codes:
            if ntee_code.startswith(code):
                return category
    
    return "Other"

def estimate_distance_tier(city: str) -> int:
    """Estimate distance tier based on city name"""
    city = city.lower().strip()
    
    # Tier 1: Core Philadelphia area (0-10 miles)
    tier1_cities = {'philadelphia', 'upper darby', 'drexel hill', 'yeadon', 'camden'}
    
    # Tier 2: Inner suburbs (10-20 miles)  
    tier2_cities = {'chester', 'norristown', 'conshohocken', 'king of prussia', 
                   'ardmore', 'bryn mawr', 'villanova', 'wayne', 'media', 
                   'cherry hill', 'gloucester'}
    
    if city in tier1_cities:
        return 1
    elif city in tier2_cities:
        return 2
    else:
        return 3  # Tier 3: Outer suburbs (20-30 miles)

def query_propublica_api(query: str, page: int = 1) -> Dict:
    """Query ProPublica API for a search term"""
    base_url = "https://projects.propublica.org/nonprofits/api/v2/search.json"
    params = {
        'q': query,
        'state[id]': 'PA',
        'page': page
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error querying API for '{query}' page {page}: {e}")
        return {}

def get_org_details(ein: str) -> Dict:
    """Get detailed org info from ProPublica"""
    try:
        url = f"https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error getting details for EIN {ein}: {e}")
        return {}

def collect_all_data():
    all_orgs = {}  # Use dict to deduplicate by EIN
    
    print("Collecting nonprofit data from ProPublica API...")
    
    for term in SEARCH_TERMS:
        print(f"\nSearching for: {term}")
        page = 1
        
        while True:
            print(f"  Page {page}...")
            data = query_propublica_api(term, page)
            
            if not data or 'organizations' not in data:
                break
                
            orgs = data.get('organizations', [])
            if not orgs:
                break
                
            for org in orgs:
                ein = org.get('ein')
                city = org.get('city', '').lower().strip()
                
                # Filter to Philadelphia metro area
                if city in PHILLY_METRO_CITIES:
                    if ein not in all_orgs:
                        # Process and store org data
                        processed_org = {
                            'ein': ein,
                            'name': org.get('name', ''),
                            'city': org.get('city', ''),
                            'state': org.get('state', ''),
                            'ntee_code': org.get('ntee_code', ''),
                            'category': get_ntee_category(org.get('ntee_code', '')),
                            'distance_tier': estimate_distance_tier(city),
                            'income_amount': org.get('income_amount', 0),
                            'asset_amount': org.get('asset_amount', 0),
                            'search_term': term
                        }
                        all_orgs[ein] = processed_org
                        print(f"    Added: {processed_org['name']} ({city})")
            
            # Check if there are more pages
            if len(orgs) < 25:  # ProPublica returns 25 per page typically
                break
                
            page += 1
            time.sleep(0.5)  # Be nice to the API
    
    print(f"\nFound {len(all_orgs)} unique organizations in Philadelphia metro area")
    
    # Get detailed info for top organizations (Tier 1 priority)
    print("\nEnriching data with detailed information...")
    tier1_orgs = [org for org in all_orgs.values() if org['distance_tier'] == 1]
    tier1_orgs.sort(key=lambda x: x.get('income_amount', 0), reverse=True)
    
    # Enrich top 50 Tier 1 orgs with detailed data
    for i, org in enumerate(tier1_orgs[:50]):
        if i > 0 and i % 10 == 0:
            print(f"  Enriched {i} organizations...")
        
        details = get_org_details(org['ein'])
        if details and 'organization' in details:
            org_detail = details['organization']
            org.update({
                'mission': org_detail.get('mission', ''),
                'primary_purpose': org_detail.get('primary_purpose', ''),
                'website': org_detail.get('website', ''),
                'address': org_detail.get('address', ''),
                'zip_code': org_detail.get('zip_code', '')
            })
        
        time.sleep(0.3)  # Be nice to the API
    
    return list(all_orgs.values())

if __name__ == "__main__":
    nonprofit_data = collect_all_data()
    
    # Save raw data
    with open('nonprofit_data.json', 'w') as f:
        json.dump(nonprofit_data, f, indent=2)
    
    print(f"\nData collection complete! Found {len(nonprofit_data)} organizations")
    
    # Print some stats
    tier_counts = {}
    category_counts = {}
    
    for org in nonprofit_data:
        tier = org['distance_tier']
        category = org['category']
        
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print(f"\nDistance Tiers:")
    for tier in sorted(tier_counts.keys()):
        print(f"  Tier {tier}: {tier_counts[tier]} organizations")
    
    print(f"\nCategories:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count} organizations")