#!/usr/bin/env python3
"""
Monitor Vercel Deployment Status
Check every 30 seconds if deployment is ready
"""

import requests
import time
import json

URLS = [
    "https://opengennet-ai.vercel.app",
    "https://opengennet-qhp6d797k-nivedhs-projects-ce31ae36.vercel.app"
]

def check_deployment(url):
    """Check if deployment is working"""
    try:
        response = requests.get(f"{url}/", timeout=10)
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('service') and 'OpenGenNet' in str(data.get('service')):
                    return True, data
            except:
                pass
        return False, f"Status: {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"

def monitor_deployments():
    """Monitor deployment status"""
    print("🔄 Monitoring Vercel Deployment Status")
    print("=" * 60)
    print("⏳ Checking every 30 seconds for successful deployment...")
    print("💡 This will run for 10 minutes maximum")
    
    for attempt in range(20):  # 20 attempts = 10 minutes
        print(f"\n📍 Check #{attempt + 1}/20 - {time.strftime('%H:%M:%S')}")
        
        any_working = False
        for i, url in enumerate(URLS):
            name = "Production" if i == 0 else "Preview"
            working, result = check_deployment(url)
            
            if working:
                print(f"   ✅ {name}: DEPLOYMENT SUCCESSFUL!")
                print(f"   🎉 URL: {url}")
                if isinstance(result, dict):
                    print(f"   📊 Service: {result.get('service', 'N/A')}")
                    print(f"   📊 Version: {result.get('version', 'N/A')}")
                any_working = True
            else:
                print(f"   ⏳ {name}: Still deploying... ({result})")
        
        if any_working:
            print(f"\n🎊 SUCCESS! At least one deployment is now working!")
            print(f"🚀 Your API with expert knowledge integration is live!")
            break
        
        if attempt < 19:  # Don't sleep on last attempt
            print("   💤 Waiting 30 seconds before next check...")
            time.sleep(30)
    else:
        print(f"\n⏰ Monitoring timeout reached.")
        print(f"💡 Manual check: Go to Vercel dashboard to see build status")

    print(f"\n🔗 Test your working deployment:")
    for url in URLS:
        print(f"   {url}")

if __name__ == "__main__":
    monitor_deployments()
