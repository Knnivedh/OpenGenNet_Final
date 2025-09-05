#!/usr/bin/env python3
"""
🧪 OpenGenNet 2.0 Local API Test
Comprehensive testing of all endpoints
"""

import requests
import json
import time

def test_local_api():
    """Test the local Flask API"""
    base_url = "http://localhost:8080"
    
    print("🧪 Testing OpenGenNet 2.0 Local API")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            print(f"📊 Version: {data['version']}")
            print(f"🤖 Providers: {data['providers']}")
            print(f"📚 Knowledge Base: {data['knowledge_base']}")
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
    
    # Test 2: Home Endpoint
    print("\n2. Testing Home Endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Home: {data['message']}")
            print(f"📊 Version: {data['version']}")
        else:
            print(f"❌ Home Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Home Error: {e}")
    
    # Test 3: Status Endpoint
    print("\n3. Testing Status Endpoint...")
    try:
        response = requests.get(f"{base_url}/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"🤖 AI Providers: {len(data['providers'])}")
            print(f"📚 Knowledge Categories: {data['knowledge_base']['categories']}")
        else:
            print(f"❌ Status Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Status Error: {e}")
    
    # Test 4: Knowledge Search
    print("\n4. Testing Knowledge Search...")
    try:
        search_data = {"query": "networking", "category": "networking"}
        response = requests.post(f"{base_url}/search", 
                               json=search_data, 
                               headers={'Content-Type': 'application/json'}, 
                               timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search Results: {data['count']} found")
            if data['results']:
                print(f"📝 First Result: {data['results'][0]['topic']}")
        else:
            print(f"❌ Search Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Search Error: {e}")
    
    # Test 5: AI Chat (without API keys)
    print("\n5. Testing AI Chat Endpoint...")
    try:
        chat_data = {"message": "Hello, test message", "use_context": False}
        response = requests.post(f"{base_url}/ask", 
                               json=chat_data, 
                               headers={'Content-Type': 'application/json'}, 
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI Chat: Response received")
            print(f"🤖 Provider: {data.get('provider', 'Unknown')}")
        elif response.status_code == 500:
            data = response.json()
            print(f"⚠️ AI Chat: Expected error (no API keys)")
            print(f"❌ Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ AI Chat Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ AI Chat Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 OpenGenNet 2.0 Local Testing Complete!")
    print("💡 To test with AI providers, add API keys to environment variables")

if __name__ == '__main__':
    test_local_api()
