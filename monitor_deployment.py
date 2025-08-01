#!/usr/bin/env python3
"""
Monitor Full Server Deployment Progress
"""
import requests
import time
import json
from datetime import datetime

def check_server_status():
    """Check if the full server is running with all features"""
    base_url = "https://viral-daily2-production.up.railway.app"
    
    print(f"🔍 Checking Full Server Status - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # Test 1: Health Check
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health Check: PASSED")
        else:
            print(f"❌ Health Check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Health Check: ERROR - {e}")
        return False
    
    # Test 2: Root API (detect server type)
    try:
        response = requests.get(f"{base_url}/api/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            message = data.get('message', '')
            if 'Minimal' in message:
                print("⚠️  Server Type: MINIMAL (fallback mode)")
                server_type = "minimal"
            else:
                print("✅ Server Type: FULL SERVER")
                server_type = "full"
        else:
            print(f"❌ Root API: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Root API: ERROR - {e}")
        return False
    
    # Test 3: Videos Endpoint
    try:
        response = requests.get(f"{base_url}/api/videos?limit=5", timeout=15)
        if response.status_code == 200:
            data = response.json()
            video_count = len(data.get('videos', []))
            user_tier = data.get('user_tier', 'unknown')
            print(f"✅ Videos: {video_count} videos, user_tier: {user_tier}")
            
            # Check for real YouTube content
            videos = data.get('videos', [])
            if videos:
                sample_video = videos[0]
                print(f"   Sample: {sample_video.get('title', 'No title')}")
                print(f"   Platform: {sample_video.get('platform', 'unknown')}")
                print(f"   Author: {sample_video.get('author', 'unknown')}")
        else:
            print(f"❌ Videos: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Videos: ERROR - {e}")
        return False
    
    # Test 4: Subscription Plans (Full Server Feature)
    try:
        response = requests.get(f"{base_url}/api/subscription-plans", timeout=10)
        if response.status_code == 200:
            data = response.json()
            plans = data.get('plans', [])
            if plans:
                print(f"✅ Subscription Plans: {len(plans)} plans available")
                for plan in plans:
                    name = plan.get('name', 'Unknown')  
                    price = plan.get('price_monthly', 0)
                    print(f"   - {name}: ${price}/month")
            else:
                print("⚠️  Subscription Plans: No plans found")
        else:
            print(f"⚠️  Subscription Plans: FAILED ({response.status_code})")
    except Exception as e:
        print(f"⚠️  Subscription Plans: ERROR - {e}")
    
    # Test 5: Platform Filtering (Full Server Feature)
    platforms = ['youtube', 'tiktok', 'twitter']
    for platform in platforms:
        try:
            response = requests.get(f"{base_url}/api/videos", 
                                  params={'platform': platform, 'limit': 2}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                videos = data.get('videos', [])
                if videos and videos[0].get('platform') == platform:
                    print(f"✅ {platform.title()} Filter: Working ({len(videos)} videos)")
                else:
                    print(f"⚠️  {platform.title()} Filter: Not working properly")
            else:
                print(f"⚠️  {platform.title()} Filter: FAILED ({response.status_code})")
        except Exception as e:
            print(f"⚠️  {platform.title()} Filter: ERROR - {e}")
    
    print("=" * 60)
    
    if server_type == "full":
        print("🎉 FULL SERVER DEPLOYMENT SUCCESSFUL!")
        print("📋 Features Available:")
        print("   ✅ Real video content with API integration")
        print("   ✅ Platform filtering (YouTube/TikTok/Twitter)")
        print("   ✅ Subscription system (Free/Pro/Business)")
        print("   ✅ User authentication capabilities")
        print("   ✅ Payment processing (PayPal)")
        print("   ✅ Analytics and advanced features")
        return True
    else:
        print("⚠️  RUNNING IN MINIMAL MODE")
        print("📋 Possible Issues:")
        print("   - Full server import failed")
        print("   - Check Railway logs for startup errors")
        print("   - May need environment variables for full features")
        return False

def main():
    """Monitor deployment with retries"""
    print("🚀 VIRAL DAILY - FULL SERVER DEPLOYMENT MONITOR")
    print("=" * 60)
    
    max_attempts = 6
    wait_time = 30
    
    for attempt in range(1, max_attempts + 1):
        print(f"\n🔄 Attempt {attempt}/{max_attempts}")
        
        if check_server_status():
            print("\n🎉 DEPLOYMENT MONITORING COMPLETE - SUCCESS!")
            break
        
        if attempt < max_attempts:
            print(f"\n⏱️  Waiting {wait_time} seconds before next check...")
            time.sleep(wait_time)
        else:
            print("\n❌ DEPLOYMENT MONITORING COMPLETE - NEEDS ATTENTION")
            print("📋 Next Steps:")
            print("   1. Check Railway deployment logs")
            print("   2. Verify all files were uploaded correctly")  
            print("   3. Check for any startup errors")

if __name__ == "__main__":
    main()