#!/usr/bin/env python3
"""
Fixed API Deployment Test
Tests the deployed API with the Vercel fixes
"""

import requests
import json
import time

# API URL
API_BASE = "https://opengennet-final.vercel.app"

def test_deployment():
    """Test the fixed deployment"""
    print("🔧 Testing Fixed OpenGenNet API Deployment")
    print("=" * 60)
    print(f"🌐 API URL: {API_BASE}")
    
    # Wait a moment for deployment
    print("\n⏳ Waiting for Vercel deployment to complete...")
    time.sleep(10)
    
    # Test 1: Root endpoint (most important)
    print("\n1. 🏠 Testing Root Endpoint (Critical Fix):")
    try:
        response = requests.get(f"{API_BASE}/", timeout=15)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service: {data.get('service', 'N/A')}")
            print(f"   ✅ Status: {data.get('status', 'N/A')}")
            print(f"   ✅ Version: {data.get('version', 'N/A')}")
            print(f"   ✅ Endpoints: {len(data.get('endpoints', []))} available")
            print("   🎉 ROOT ROUTE FIXED!")
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    # Test 2: Health check
    print("\n2. 💊 Testing Health Endpoint:")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=15)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service: {data.get('service', 'N/A')}")
            print(f"   ✅ Status: {data.get('status', 'N/A')}")
            print("   🎉 HEALTH CHECK WORKING!")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    # Test 3: Status endpoint
    print("\n3. 📊 Testing Status Endpoint:")
    try:
        response = requests.get(f"{API_BASE}/status", timeout=15)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service: {data.get('service', 'N/A')}")
            print(f"   ✅ Status: {data.get('status', 'N/A')}")
            print("   🎉 STATUS ENDPOINT WORKING!")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    # Test 4: Debug endpoint
    print("\n4. 🐛 Testing Debug Endpoint:")
    try:
        response = requests.get(f"{API_BASE}/debug", timeout=15)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Environment: {data.get('environment', 'N/A')}")
            print("   🎉 DEBUG ENDPOINT WORKING!")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    # Test 5: Search endpoint with POST
    print("\n5. 🔍 Testing Search Endpoint (POST):")
    try:
        search_data = {"query": "networking"}
        response = requests.post(f"{API_BASE}/search", json=search_data, timeout=15)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Query: {data.get('query', 'N/A')}")
            print(f"   ✅ Results: {data.get('total_results', 'N/A')}")
            print("   🎉 SEARCH ENDPOINT WORKING!")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    # Test 6: Ask endpoint with POST  
    print("\n6. 💬 Testing Ask Endpoint (POST):")
    try:
        ask_data = {"message": "Hello, how are you?"}
        response = requests.post(f"{API_BASE}/ask", json=ask_data, timeout=30)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Provider: {data.get('provider', 'N/A')}")
            response_text = data.get('response', '')
            print(f"   ✅ Response Length: {len(response_text)} characters")
            print("   🎉 ASK ENDPOINT WORKING!")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 DEPLOYMENT TEST COMPLETE!")
    print("🔧 Fixed Issues:")
    print("   ✅ Added missing root route")
    print("   ✅ Created vercel.json configuration")
    print("   ✅ Simplified requirements.txt")
    print("   ✅ Added CORS OPTIONS handlers")
    print("🚀 API should now be accessible!")

if __name__ == "__main__":
    test_deployment()
