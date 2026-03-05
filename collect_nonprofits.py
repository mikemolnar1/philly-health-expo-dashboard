#!/usr/bin/env python3
import requests
import json
import time
import sys
from typing import Dict, List

# Search terms for nonprofits
SEARCH_TERMS = [
    "health", "wellness", "mental health", "workforce development", 
    "employment", "job training", "disability services", "youth services",
    "community health", "substance abuse", "housing assistance", 
    "food bank", "veterans services"
]

# Philadelphia metro cities and surrounding areas
PHILLY_METRO_AREAS = {
    # Core Philadelphia
    'philadelphia', 'phila', 'upper darby', 'drexel hill', 'yeadon',
    
    # Close suburbs (Tier 1-2)
    'chester', 'norristown', 'conshohocken', 'king of prussia', 'lansdale',
    'ardmore', 'bryn mawr', 'villanova', 'wayne', 'berwyn', 'devon',
    'media', 'west chester', 'malvern', 'paoli', 'downingtown',
    
    # Extended suburbs (Tier 2-3)  
    'coatesville', 'phoenixville', 'pottstown', 'collegeville', 'royersford',
    'harleysville', 'souderton', 'telford', 'hatfield', 'north wales',
    'ambler', 'fort washington', 'warminster', 'warrington', 'newtown',
    'doylestown', 'richboro', 'holland', 'southampton', 'feasterville',
    'trevose', 'bensalem', 'bristol', 'levittown', 'morrisville',
    
    # NJ metro
    'camden', 'cherry hill', 'gloucester', 'deptford', 'washington township',
    'monroe township', 'williamstown', 'sicklerville', 'blackwood',
    'turnersville', 'sewell', 'pitman', 'woodbury', 'glassboro'
}

def categorize_by_ntee(ntee_code: str) -> str:
    """Categorize organization by NTEE code"""
    if not ntee_code:
        return "Other"
    
    ntee = ntee_code.upper().strip()
    
    if ntee.startswith('E'):
        return "Health & Wellness"
    elif ntee.startswith('F'):
        return "Mental Health" 
    elif ntee.startswith('G') or ntee.startswith('H'):
        return "Health & Wellness"
    elif ntee.startswith('J'):
        return "Employment/Workforce"
    elif ntee.startswith('O'):
        return "Youth Services"
    elif ntee.startswith('P8'):
        return "Disability Services"
    elif ntee.startswith('P') or ntee.startswith('S'):
        return "Community Services"
    elif ntee.startswith('L'):
        return "Housing"
    elif ntee.startswith('K'):
        return "Food/Nutrition"
    else:
        return "Other"

def estimate_distance_tier(city: str) -> int:
    """Estimate distance tier based on city"""
    city_clean = city.lower().strip()
    
    # Tier 1: 0-10 miles (core Philadelphia area)
    tier1 = {'philadelphia', 'phila', 'upper darby', 'drexel hill', 'camden'}
    
    # Tier 2: 10-20 miles
    tier2 = {'chester', 'norristown', 'conshohocken', 'king of prussia',
             'ardmore', 'bryn mawr', 'villanova', 'wayne', 'media', 
             'cherry hill', 'gloucester'}
    
    if city_clean in tier1:
        return 1
    elif city_clean in tier2:
        return 2
    else:
        return 3  # Tier 3: 20-30 miles

def is_philly_metro(city: str) -> bool:
    """Check if city is in Philadelphia metro area"""
    return city.lower().strip() in PHILLY_METRO_AREAS

def collect_data():
    """Collect nonprofit data from ProPublica API"""
    all_orgs = {}  # Dict to deduplicate by EIN
    
    print("🔍 Collecting nonprofit data from ProPublica API...")
    
    for i, term in enumerate(SEARCH_TERMS):
        print(f"\n📊 Search {i+1}/{len(SEARCH_TERMS)}: '{term}'")
        
        page = 1
        term_count = 0
        
        while page <= 10:  # Limit to 10 pages per search term
            try:
                url = "https://projects.propublica.org/nonprofits/api/v2/search.json"
                params = {
                    'q': term,
                    'state[id]': 'PA',
                    'page': page
                }
                
                response = requests.get(url, params=params, timeout=15)
                response.raise_for_status()
                data = response.json()
                
                orgs = data.get('organizations', [])
                if not orgs:
                    break
                    
                page_additions = 0
                for org in orgs:
                    city = org.get('city', '').strip()
                    
                    if is_philly_metro(city):
                        ein = org.get('ein')
                        if ein and ein not in all_orgs:
                            all_orgs[ein] = {
                                'ein': ein,
                                'name': org.get('name', ''),
                                'city': city,
                                'state': org.get('state', 'PA'),
                                'ntee_code': org.get('ntee_code', ''),
                                'category': categorize_by_ntee(org.get('ntee_code', '')),
                                'distance_tier': estimate_distance_tier(city),
                                'income_amount': org.get('income_amount', 0) or 0,
                                'asset_amount': org.get('asset_amount', 0) or 0,
                                'found_via': term,
                                'subseccd': org.get('subseccd'),
                                'has_filings': org.get('have_filings', False)
                            }
                            page_additions += 1
                            term_count += 1
                
                print(f"   Page {page}: +{page_additions} orgs (total for '{term}': {term_count})")
                
                if len(orgs) < 25:  # ProPublica returns 25 per page
                    break
                    
                page += 1
                time.sleep(0.3)  # Rate limiting
                
            except requests.RequestException as e:
                print(f"   ⚠️  Error on page {page}: {e}")
                break
            except Exception as e:
                print(f"   ⚠️  Unexpected error: {e}")
                break
    
    print(f"\n✅ Found {len(all_orgs)} unique organizations in Philadelphia metro")
    return list(all_orgs.values())

def save_data(orgs: List[Dict]):
    """Save data and print summary statistics"""
    # Save to JSON
    with open('nonprofit_data.json', 'w') as f:
        json.dump(orgs, f, indent=2)
    
    # Calculate and display stats
    total = len(orgs)
    tier_counts = {1: 0, 2: 0, 3: 0}
    category_counts = {}
    
    for org in orgs:
        tier = org['distance_tier']
        category = org['category']
        
        tier_counts[tier] += 1
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print(f"\n📈 SUMMARY STATISTICS")
    print(f"Total Organizations: {total}")
    print(f"\n📍 Distance Tiers:")
    print(f"   Tier 1 (0-10 miles):  {tier_counts[1]:3d} orgs")
    print(f"   Tier 2 (10-20 miles): {tier_counts[2]:3d} orgs")  
    print(f"   Tier 3 (20-30 miles): {tier_counts[3]:3d} orgs")
    
    print(f"\n🏷️  Categories:")
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {category:20s}: {count:3d} orgs")
    
    # Top organizations by revenue
    print(f"\n💰 Top 10 by Revenue (Tier 1 priority):")
    tier1_orgs = [org for org in orgs if org['distance_tier'] == 1]
    tier1_orgs.sort(key=lambda x: x['income_amount'], reverse=True)
    
    for i, org in enumerate(tier1_orgs[:10]):
        revenue = org['income_amount']
        revenue_str = f"${revenue:,.0f}" if revenue > 0 else "N/A"
        print(f"   {i+1:2d}. {org['name'][:50]:<50s} {revenue_str}")

if __name__ == "__main__":
    try:
        nonprofit_data = collect_data()
        save_data(nonprofit_data)
        print(f"\n🎉 Data collection complete! Saved to nonprofit_data.json")
        
    except KeyboardInterrupt:
        print("\n⏹️  Collection stopped by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)