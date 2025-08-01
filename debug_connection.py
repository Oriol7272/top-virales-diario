#!/usr/bin/env python3
"""
Debug Frontend-Backend Connection Issues
"""
import requests
import json
import sys

def test_backend_connection(backend_url):
    """Test if backend is accessible and working"""
    print(f"🔍 Testing Backend: {backend_url}")
    
    # Test 1: Basic connectivity
    try:
        response = requests.get(f"{backend_url}/api/", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is accessible")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Backend returned {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False
    
    # Test 2: Health check
    try:
        response = requests.get(f"{backend_url}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check working")
        else:
            print(f"⚠️  Health check returned {response.status_code}")
    except Exception as e:
        print(f"⚠️  Health check failed: {e}")
    
    # Test 3: Videos endpoint (main issue)
    try:
        response = requests.get(f"{backend_url}/api/videos?limit=5", timeout=15)
        if response.status_code == 200:
            data = response.json()
            videos = data.get('videos', [])
            print(f"✅ Videos endpoint working: {len(videos)} videos")
            if videos:
                print(f"   Sample video: {videos[0].get('title', 'No title')}")
                print(f"   Platforms: {list(set(v.get('platform') for v in videos))}")
            else:
                print("❌ No videos returned")
                return False
        else:
            print(f"❌ Videos endpoint failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Videos endpoint error: {e}")
        return False
    
    # Test 4: CORS headers
    try:
        response = requests.options(f"{backend_url}/api/videos")
        cors_headers = {k: v for k, v in response.headers.items() if 'access-control' in k.lower()}
        if cors_headers:
            print("✅ CORS headers present:")
            for header, value in cors_headers.items():
                print(f"   {header}: {value}")
        else:
            print("⚠️  No CORS headers found")
    except Exception as e:
        print(f"⚠️  CORS check failed: {e}")
    
    return True

def test_frontend_config(frontend_url):
    """Test frontend configuration"""
    print(f"\n🔍 Testing Frontend: {frontend_url}")
    
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            
            # Check if React app is loading
            content = response.text.lower()
            if 'viral daily' in content or 'react' in content:
                print("✅ Frontend appears to be loading correctly")
            else:
                print("⚠️  Frontend may not be loading properly")
                
        else:
            print(f"❌ Frontend returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to frontend: {e}")
        return False
    
    return True

def main():
    print("🚀 VIRAL DAILY CONNECTION DEBUGGER")
    print("=" * 50)
    
    # Get URLs
    if len(sys.argv) >= 3:
        backend_url = sys.argv[1].rstrip('/')
        frontend_url = sys.argv[2].rstrip('/')
    else:
        backend_url = input("Enter Railway Backend URL: ").strip().rstrip('/')
        frontend_url = input("Enter Vercel Frontend URL: ").strip().rstrip('/')
    
    # Test backend
    backend_ok = test_backend_connection(backend_url)
    
    # Test frontend
    frontend_ok = test_frontend_config(frontend_url)
    
    # Summary and recommendations
    print("\n" + "=" * 50)
    print("📋 DIAGNOSIS & RECOMMENDATIONS")
    print("=" * 50)
    
    if not backend_ok:
        print("❌ BACKEND ISSUE DETECTED")
        print("🔧 FIXES:")
        print("   1. Check Railway deployment logs")
        print("   2. Verify environment variables are set")
        print("   3. Test health check manually")
        print("   4. Check if server is starting properly")
        
    elif not frontend_ok:
        print("❌ FRONTEND ISSUE DETECTED")
        print("🔧 FIXES:")
        print("   1. Check Vercel deployment logs")
        print("   2. Verify build completed successfully")
        print("   3. Check if React app is building correctly")
        
    else:
        print("✅ BOTH SERVICES ACCESSIBLE")
        print("🔧 FRONTEND CONNECTION ISSUE:")
        print("   1. Update frontend/.env with correct backend URL:")
        print(f"      REACT_APP_BACKEND_URL={backend_url}")
        print("   2. Redeploy frontend to Vercel")
        print("   3. Check browser developer console for errors")
        print("   4. Verify CORS is working (no browser blocking)")
    
    print(f"\n🔧 QUICK FIXES:")
    print(f"   Frontend .env should contain:")
    print(f"   REACT_APP_BACKEND_URL={backend_url}")
    print(f"   \n   Test backend directly:")
    print(f"   curl {backend_url}/api/videos?limit=3")

if __name__ == "__main__":
    main()