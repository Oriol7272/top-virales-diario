#!/usr/bin/env python3
"""
Simple test to check if video endpoints work without database dependencies
"""
import requests
import sys

def test_video_endpoints():
    """Test video endpoints without database dependencies"""
    base_url = "https://cc945f70-93e3-4a62-a0e6-c6de7d225df0.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("🧪 Testing Video Endpoints Without Database Dependencies")
    print("=" * 60)
    
    # Test 1: Root API endpoint (should work)
    print("\n1. Testing Root API Endpoint...")
    try:
        response = requests.get(f"{api_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root API: {data.get('message', 'No message')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
        else:
            print(f"❌ Root API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root API error: {e}")
    
    # Test 2: Subscription plans (should work without database)
    print("\n2. Testing Subscription Plans...")
    try:
        response = requests.get(f"{api_url}/subscription/plans", timeout=10)
        if response.status_code == 200:
            data = response.json()
            plans = data.get('plans', [])
            print(f"✅ Subscription Plans: {len(plans)} plans found")
            for plan in plans:
                tier = plan.get('tier', 'unknown')
                price = plan.get('price_monthly', 0)
                videos = plan.get('max_videos_per_day', 0)
                print(f"   {tier.upper()}: ${price}/month, {videos} videos/day")
        else:
            print(f"❌ Subscription Plans failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Subscription Plans error: {e}")
    
    # Test 3: PayPal configuration (should work)
    print("\n3. Testing PayPal Configuration...")
    try:
        response = requests.get(f"{api_url}/payments/paypal/config", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ PayPal Config: Mode={data.get('mode')}, Currency={data.get('currency')}")
        else:
            print(f"❌ PayPal Config failed: {response.status_code}")
    except Exception as e:
        print(f"❌ PayPal Config error: {e}")
    
    # Test 4: PayPal availability (should work)
    print("\n4. Testing PayPal Availability...")
    try:
        response = requests.get(f"{api_url}/payments/paypal/available", timeout=10)
        if response.status_code == 200:
            data = response.json()
            available = data.get('available', False)
            mode = data.get('mode', 'unknown')
            print(f"✅ PayPal Available: {available} (Mode: {mode})")
        else:
            print(f"❌ PayPal Availability failed: {response.status_code}")
    except Exception as e:
        print(f"❌ PayPal Availability error: {e}")
    
    # Test 5: Video endpoints (currently failing due to database)
    print("\n5. Testing Video Endpoints (Expected to fail due to database issues)...")
    try:
        response = requests.get(f"{api_url}/videos", params={'limit': 5}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            videos = data.get('videos', [])
            print(f"✅ Videos: {len(videos)} videos returned")
            if videos:
                first_video = videos[0]
                print(f"   Sample: {first_video.get('title', 'No title')[:50]}...")
        else:
            print(f"❌ Videos failed: {response.status_code}")
            print(f"   Error: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ Videos error: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 Simple Video Test Complete")

if __name__ == "__main__":
    test_video_endpoints()