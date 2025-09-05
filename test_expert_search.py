#!/usr/bin/env python3
"""
🔍 Expert Knowledge Search Test - What topics are available?
"""

import requests
import json

def test_expert_knowledge():
    base_url = "https://opengennet-ai.vercel.app"
    
    print("🔍 EXPERT KNOWLEDGE AVAILABILITY TEST")
    print("=" * 50)
    
    # Test various technical terms
    search_terms = [
        "security", "network", "cloud", "protocol", "encryption",
        "TCP", "firewall", "VPN", "routing", "authentication",
        "python", "javascript", "database", "API", "server",
        "algorithm", "data structure", "performance", "optimization"
    ]
    
    for term in search_terms:
        try:
            response = requests.post(f"{base_url}/search", 
                                   json={"query": term}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = data.get('total_results', 0)
                print(f"🔍 '{term}': {results} expert cases")
                
                if results > 0:
                    for result in data.get('results', [])[:2]:
                        topic = result.get('topic', 'N/A')
                        category = result.get('category', 'N/A')
                        print(f"   📚 {topic} ({category})")
            else:
                print(f"❌ '{term}': Error {response.status_code}")
        except Exception as e:
            print(f"❌ '{term}': Error - {e}")
    
    # Get full status
    print(f"\n📊 SYSTEM STATUS:")
    try:
        response = requests.get(f"{base_url}/status")
        if response.status_code == 200:
            data = response.json()
            print(f"Expert Cases: {data.get('total_expert_cases', 0)}")
            print(f"Categories: {', '.join(data.get('expert_knowledge_categories', []))}")
        else:
            print(f"Status error: {response.status_code}")
    except Exception as e:
        print(f"Status error: {e}")

if __name__ == "__main__":
    test_expert_knowledge()
