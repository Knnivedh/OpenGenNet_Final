#!/usr/bin/env python3
"""
Test Deployed Enhanced API
Verifies the enhanced API is working on Vercel with expert knowledge integration
"""

import requests
import json
import time

# Your deployed API URL
API_BASE = "https://opengennet-final.vercel.app"

def test_deployed_api():
    """Test the deployed enhanced API"""
    print("🌐 Testing Deployed Enhanced OpenGenNet API")
    print("=" * 60)
    print(f"🔗 API URL: {API_BASE}")
    
    # Test 1: Root endpoint - Check enhancement status
    print("\n1. Testing Enhanced Root Endpoint:")
    try:
        response = requests.get(f"{API_BASE}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data.get('status', 'N/A')}")
            print(f"   🚀 Version: {data.get('version', 'N/A')}")
            print(f"   ✨ Enhancement: {data.get('enhancement', 'N/A')}")
            print(f"   📚 Expert Cases: {data.get('expert_knowledge_cases', 'N/A')}")
            
            features = data.get('features', [])
            if features:
                print("   🎯 Features:")
                for feature in features[:3]:  # Show first 3
                    print(f"     - {feature}")
        else:
            print(f"   ❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Health check with expert knowledge
    print("\n2. Testing Enhanced Health Check:")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data.get('status', 'N/A')}")
            print(f"   📈 Integration Level: {data.get('integration_level', 'N/A')}")
            print(f"   📚 Expert Cases: {data.get('expert_knowledge_cases', 'N/A')}")
            print(f"   🐍 Python: {data.get('python_version', 'N/A')}")
        else:
            print(f"   ❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: System status with expert details
    print("\n3. Testing Enhanced System Status:")
    try:
        response = requests.get(f"{API_BASE}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data.get('status', 'N/A')}")
            print(f"   🚀 Version: {data.get('version', 'N/A')}")
            
            expert_knowledge = data.get('expert_knowledge', {})
            print(f"   📚 Total Cases: {expert_knowledge.get('total_cases', 'N/A')}")
            print(f"   🎯 Enhancement Level: {expert_knowledge.get('enhancement_level', 'N/A')}")
            
            categories = expert_knowledge.get('categories', {})
            if categories:
                print(f"   📋 Categories: {len(categories)} types")
        else:
            print(f"   ❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Debug endpoint
    print("\n4. Testing Debug Endpoint:")
    try:
        response = requests.get(f"{API_BASE}/debug", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Expert Knowledge Loaded: {data.get('expert_knowledge_loaded', 'N/A')}")
            print(f"   🔧 Integration Status: {data.get('integration_status', 'N/A')}")
            print(f"   🌍 Environment: {data.get('environment', 'N/A')}")
        else:
            print(f"   ❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Enhanced search
    print("\n5. Testing Enhanced Expert Search:")
    try:
        search_data = {"query": "OSPF routing protocol", "max_results": 3}
        response = requests.post(f"{API_BASE}/search", json=search_data, timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Search Type: {data.get('search_type', 'N/A')}")
            print(f"   📊 Results Found: {data.get('total_results', 'N/A')}")
            
            results = data.get('results', [])
            if results:
                best = results[0]
                print(f"   🎯 Best Match: {best.get('title', 'N/A')[:50]}...")
                print(f"   📋 Category: {best.get('category', 'N/A')}")
                print(f"   ⭐ Quality Score: {best.get('quality_score', 'N/A')}")
        else:
            print(f"   ❌ HTTP {response.status_code}: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Enhanced AI chat (if API keys are configured)
    print("\n6. Testing Enhanced AI Chat:")
    try:
        chat_data = {"message": "Explain OSPF routing protocol configuration"}
        response = requests.post(f"{API_BASE}/ask", json=chat_data, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Provider: {data.get('provider', 'N/A')}")
            
            enhancement = data.get('enhancement', {})
            print(f"   🎯 Expert Context Used: {enhancement.get('expert_context_used', 'N/A')}")
            print(f"   🔧 Knowledge Integration: {enhancement.get('knowledge_integration', 'N/A')}")
            print(f"   📈 Response Level: {enhancement.get('response_level', 'N/A')}")
            
            response_text = data.get('response', '')
            print(f"   📝 Response Length: {len(response_text)} characters")
            print(f"   📖 Preview: {response_text[:150]}...")
        else:
            print(f"   ❌ HTTP {response.status_code}: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 DEPLOYED API TESTING COMPLETE!")
    print("✨ Enhanced OpenGenNet API with Expert Knowledge Integration!")

if __name__ == "__main__":
    test_deployed_api()
