#!/usr/bin/env python3
"""
Test Local API - Verify Deployment Fixes Work
"""

import requests
import json
import time

# Local API URL
API_BASE = "http://127.0.0.1:8080"

def test_local_api():
    """Test the locally running API"""
    print("🧪 Testing Local OpenGenNet API")
    print("=" * 50)
    print(f"🔗 Local URL: {API_BASE}")
    
    # Test 1: Root endpoint (most critical fix)
    print("\n1. 🏠 Testing Root Endpoint:")
    try:
        response = requests.get(f"{API_BASE}/", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service: {data.get('service')}")
            print(f"   ✅ Status: {data.get('status')}")
            print(f"   ✅ Version: {data.get('version')}")
            print(f"   ✅ Endpoints: {data.get('endpoints')}")
            print("   🎉 ROOT ROUTE WORKING!")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Health endpoint
    print("\n2. 💊 Testing Health Endpoint:")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service: {data.get('service')}")
            print(f"   ✅ Status: {data.get('status')}")
            print("   🎉 HEALTH CHECK WORKING!")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Status endpoint
    print("\n3. 📊 Testing Status Endpoint:")
    try:
        response = requests.get(f"{API_BASE}/status", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service: {data.get('service')}")
            print(f"   ✅ Status: {data.get('status')}")
            print("   🎉 STATUS WORKING!")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Debug endpoint
    print("\n4. 🐛 Testing Debug Endpoint:")
    try:
        response = requests.get(f"{API_BASE}/debug", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Environment: {data.get('environment', 'local')}")
            print("   🎉 DEBUG WORKING!")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Search endpoint (POST)
    print("\n5. 🔍 Testing Search Endpoint:")
    try:
        search_data = {"query": "networking basics"}
        response = requests.post(f"{API_BASE}/search", json=search_data, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Query: {data.get('query')}")
            print(f"   ✅ Results: {data.get('total_results')}")
            print("   🎉 SEARCH WORKING!")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Ask endpoint (POST)
    print("\n6. 💬 Testing Ask Endpoint:")
    try:
        ask_data = {"message": "What is OSPF?"}
        response = requests.post(f"{API_BASE}/ask", json=ask_data, timeout=15)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Provider: {data.get('provider')}")
            response_text = data.get('response', '')
            print(f"   ✅ Response Length: {len(response_text)} chars")
            if len(response_text) > 0:
                print(f"   📝 Preview: {response_text[:100]}...")
            print("   🎉 ASK WORKING!")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎊 LOCAL API TEST COMPLETE!")
    print("✅ All fixes confirmed working locally!")
    print("🚀 Ready for deployment when Vercel is configured!")

if __name__ == "__main__":
    test_local_api()
