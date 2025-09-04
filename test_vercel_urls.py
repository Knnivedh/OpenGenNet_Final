#!/usr/bin/env python3
"""
Test Existing Vercel Deployments
Check the status of both Vercel URLs
"""

import requests
import json
import time

# Your Vercel URLs
PRODUCTION_URL = "https://opengennet-ai.vercel.app"
PREVIEW_URL = "https://opengennet-qhp6d797k-nivedhs-projects-ce31ae36.vercel.app"

def test_vercel_deployment(url, name):
    """Test a Vercel deployment URL"""
    print(f"\n🌐 Testing {name}")
    print(f"🔗 URL: {url}")
    print("-" * 60)
    
    # Test 1: Root endpoint
    print(f"1. 🏠 Testing Root Endpoint:")
    try:
        response = requests.get(f"{url}/", timeout=15)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ Service: {data.get('service', 'N/A')}")
                print(f"   ✅ Status: {data.get('status', 'N/A')}")
                print(f"   ✅ Version: {data.get('version', 'N/A')}")
                print(f"   🎉 ROOT ENDPOINT WORKING!")
                return True
            except:
                print(f"   ⚠️  Response not JSON: {response.text[:100]}...")
                return False
        elif response.status_code == 404:
            print(f"   ❌ 404 - Deployment not found or root route missing")
            print(f"   Response: {response.text[:200]}")
            return False
        else:
            print(f"   ❌ Error {response.status_code}: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection failed - deployment might not exist")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Health endpoint if root works
    print(f"2. 💊 Testing Health Endpoint:")
    try:
        response = requests.get(f"{url}/health", timeout=15)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health Status: {data.get('status', 'N/A')}")
            print(f"   🎉 HEALTH CHECK WORKING!")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Health check error: {e}")

def main():
    print("🧪 Testing Your Existing Vercel Deployments")
    print("=" * 70)
    
    # Test production URL
    prod_working = test_vercel_deployment(PRODUCTION_URL, "Production Deployment")
    
    # Test preview URL  
    preview_working = test_vercel_deployment(PREVIEW_URL, "Preview Deployment")
    
    print("\n" + "=" * 70)
    print("📊 DEPLOYMENT STATUS SUMMARY")
    print("=" * 70)
    
    print(f"🌍 Production ({PRODUCTION_URL.split('//')[1]}): {'✅ WORKING' if prod_working else '❌ NOT WORKING'}")
    print(f"🔄 Preview ({PREVIEW_URL.split('//')[1].split('-')[0]}): {'✅ WORKING' if preview_working else '❌ NOT WORKING'}")
    
    if not prod_working and not preview_working:
        print("\n🔧 RECOMMENDED ACTIONS:")
        print("1. ⚡ Trigger a redeploy from Vercel dashboard")
        print("2. 🔍 Check if latest code changes are deployed")
        print("3. 🔑 Verify environment variables are set")
        print("4. 📋 Check build logs for errors")
        
        print("\n🚀 QUICK REDEPLOY STEPS:")
        print("1. Go to Vercel dashboard")
        print("2. Find your opengennet-ai project")
        print("3. Click on latest deployment")
        print("4. Click three dots (⋯) menu")
        print("5. Select 'Redeploy without Build Cache'")
        
    elif prod_working or preview_working:
        print("\n🎉 GOOD NEWS: At least one deployment is working!")
        if prod_working:
            print(f"✅ Use production URL: {PRODUCTION_URL}")
        else:
            print(f"✅ Use preview URL: {PREVIEW_URL}")
            print("💡 Consider promoting preview to production")
    
    print("\n🎯 NEXT STEPS:")
    print("- If deployments work: Test API functionality")
    print("- If deployments fail: Redeploy with our fixes")
    print("- Our code fixes are ready and should work!")

if __name__ == "__main__":
    main()
