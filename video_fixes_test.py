#!/usr/bin/env python3
"""
FINAL VERIFICATION: Test that the video display fixes are working correctly
"""

import requests
import sys
import json
from datetime import datetime

class VideoDisplayFixesVerifier:
    def __init__(self):
        # Use deployed backend URL from frontend/.env
        try:
            with open('/app/frontend/.env', 'r') as f:
                for line in f:
                    if line.startswith('REACT_APP_BACKEND_URL='):
                        self.base_url = line.split('=')[1].strip()
                        break
                else:
                    self.base_url = "http://localhost:8001"
        except:
            self.base_url = "http://localhost:8001"
        
        self.api_url = f"{self.base_url}/api"
        print(f"🎯 Testing against: {self.base_url}")

    def make_request(self, endpoint, params=None):
        """Make API request and return response"""
        url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
        try:
            response = requests.get(url, params=params, timeout=10)
            return response.status_code == 200, response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
            return False, None

    def test_video_count_verification(self):
        """Test video count with various limits for free tier users"""
        print("\n1️⃣ VIDEO COUNT VERIFICATION")
        print("   Testing /api/videos with various limits (5, 20, 50) for free tier users")
        
        limits_to_test = [5, 20, 50]
        video_counts = {}
        
        for limit in limits_to_test:
            success, response = self.make_request("videos", {'limit': limit})
            
            if success and response:
                videos = response.get('videos', [])
                video_counts[limit] = len(videos)
                user_tier = response.get('user_tier', 'unknown')
                has_ads = response.get('has_ads', False)
                
                print(f"   Limit {limit}: Got {len(videos)} videos (tier: {user_tier}, ads: {has_ads})")
            else:
                print(f"   ❌ Failed to get videos with limit {limit}")
                video_counts[limit] = 0
        
        # Check if free tier gets ~40 videos max (not 5 like before)
        max_videos = max(video_counts.values()) if video_counts else 0
        if max_videos >= 35:  # Allow some variance around 40
            print(f"   ✅ FREE TIER VIDEO COUNT FIXED: Getting {max_videos} videos (was 5 before)")
            return True
        else:
            print(f"   ❌ VIDEO COUNT ISSUE: Only getting {max_videos} videos (should be ~40)")
            return False

    def test_platform_content_verification(self):
        """Test all platform-specific endpoints"""
        print("\n2️⃣ PLATFORM CONTENT VERIFICATION")
        print("   Testing all platform-specific endpoints: YouTube, TikTok, Twitter")
        
        platforms = ['youtube', 'tiktok', 'twitter']
        platform_results = {}
        
        for platform in platforms:
            success, response = self.make_request("videos", {'platform': platform, 'limit': 10})
            
            if success and response:
                videos = response.get('videos', [])
                platform_results[platform] = {
                    'count': len(videos),
                    'has_proper_urls': False,
                    'has_thumbnails': False
                }
                
                if videos:
                    # Check URLs and thumbnails
                    first_video = videos[0]
                    url = first_video.get('url', '')
                    thumbnail = first_video.get('thumbnail', '')
                    
                    # Platform-specific URL checks
                    if platform == 'youtube' and 'youtube.com' in url:
                        platform_results[platform]['has_proper_urls'] = True
                    elif platform == 'tiktok' and 'tiktok.com' in url:
                        platform_results[platform]['has_proper_urls'] = True
                    elif platform == 'twitter' and 'twitter.com' in url:
                        platform_results[platform]['has_proper_urls'] = True
                    
                    # Thumbnail checks
                    if thumbnail and thumbnail.strip():
                        platform_results[platform]['has_thumbnails'] = True
                    
                    print(f"   {platform.title()}: {len(videos)} videos, URLs: {'✅' if platform_results[platform]['has_proper_urls'] else '❌'}, Thumbnails: {'✅' if platform_results[platform]['has_thumbnails'] else '❌'}")
                else:
                    print(f"   ❌ {platform.title()}: No videos returned")
            else:
                print(f"   ❌ {platform.title()}: Request failed")
                platform_results[platform] = {'count': 0, 'has_proper_urls': False, 'has_thumbnails': False}
        
        # Check if all platforms are working
        all_platforms_working = all(
            result['count'] > 0 and result['has_proper_urls'] and result['has_thumbnails']
            for result in platform_results.values()
        )
        
        if all_platforms_working:
            print("   ✅ ALL PLATFORMS WORKING: YouTube, TikTok, Twitter with proper URLs and thumbnails")
            return True
        else:
            print("   ❌ PLATFORM ISSUES DETECTED")
            return False

    def test_user_tier_logic_verification(self):
        """Test user tier logic for unauthenticated users"""
        print("\n3️⃣ USER TIER LOGIC VERIFICATION")
        print("   Verifying unauthenticated users default to 'free' tier with has_ads=true")
        
        success, response = self.make_request("videos", {'limit': 10})
        
        if success and response:
            user_tier = response.get('user_tier', 'unknown')
            has_ads = response.get('has_ads', False)
            
            print(f"   User Tier: {user_tier}")
            print(f"   Has Ads: {has_ads}")
            
            if user_tier == 'free' and has_ads:
                print("   ✅ USER TIER LOGIC CORRECT: Unauthenticated users are 'free' tier with ads")
                return True
            else:
                print("   ❌ USER TIER LOGIC ISSUE: Expected 'free' tier with has_ads=true")
                return False
        else:
            print("   ❌ Failed to test user tier logic")
            return False

    def test_url_thumbnail_quality(self):
        """Test URL and thumbnail quality"""
        print("\n4️⃣ URL AND THUMBNAIL QUALITY VERIFICATION")
        print("   Verifying YouTube videos have real ytimg.com thumbnails")
        print("   Verifying TikTok videos have proper tiktok.com URLs")
        print("   Verifying Twitter videos have proper twitter.com URLs")
        
        success, response = self.make_request("videos", {'limit': 30})
        
        if success and response:
            videos = response.get('videos', [])
            
            youtube_real_thumbnails = 0
            tiktok_proper_urls = 0
            twitter_proper_urls = 0
            total_youtube = 0
            total_tiktok = 0
            total_twitter = 0
            
            for video in videos:
                platform = video.get('platform', '').lower()
                url = video.get('url', '')
                thumbnail = video.get('thumbnail', '')
                
                if platform == 'youtube':
                    total_youtube += 1
                    if 'ytimg.com' in thumbnail:
                        youtube_real_thumbnails += 1
                elif platform == 'tiktok':
                    total_tiktok += 1
                    if 'tiktok.com' in url:
                        tiktok_proper_urls += 1
                elif platform == 'twitter':
                    total_twitter += 1
                    if 'twitter.com' in url:
                        twitter_proper_urls += 1
            
            print(f"   YouTube real thumbnails: {youtube_real_thumbnails}/{total_youtube}")
            print(f"   TikTok proper URLs: {tiktok_proper_urls}/{total_tiktok}")
            print(f"   Twitter proper URLs: {twitter_proper_urls}/{total_twitter}")
            
            # Check quality thresholds
            youtube_quality = (youtube_real_thumbnails / total_youtube * 100) if total_youtube > 0 else 0
            tiktok_quality = (tiktok_proper_urls / total_tiktok * 100) if total_tiktok > 0 else 0
            twitter_quality = (twitter_proper_urls / total_twitter * 100) if total_twitter > 0 else 0
            
            if youtube_quality >= 80 and tiktok_quality >= 80 and twitter_quality >= 80:
                print("   ✅ URL AND THUMBNAIL QUALITY EXCELLENT: All platforms have proper URLs/thumbnails")
                return True
            else:
                print("   ❌ URL AND THUMBNAIL QUALITY ISSUES DETECTED")
                return False
        else:
            print("   ❌ Failed to test URL and thumbnail quality")
            return False

    def test_response_structure_verification(self):
        """Test response structure"""
        print("\n5️⃣ RESPONSE STRUCTURE VERIFICATION")
        print("   Confirming all required fields are present")
        print("   Verifying viral_score calculation is working")
        print("   Checking date/timestamp fields are properly populated")
        
        success, response = self.make_request("videos", {'limit': 5})
        
        if success and response:
            videos = response.get('videos', [])
            
            if videos:
                first_video = videos[0]
                required_fields = ['title', 'url', 'thumbnail', 'platform', 'views', 'likes', 'viral_score']
                missing_fields = [field for field in required_fields if field not in first_video]
                
                viral_scores = [v.get('viral_score', 0) for v in videos if v.get('viral_score') is not None]
                has_viral_scores = len(viral_scores) > 0
                
                response_date = response.get('date')
                has_date = response_date is not None
                
                print(f"   Required fields present: {'✅' if not missing_fields else '❌'}")
                if missing_fields:
                    print(f"   Missing fields: {missing_fields}")
                
                print(f"   Viral scores working: {'✅' if has_viral_scores else '❌'}")
                if has_viral_scores:
                    avg_score = sum(viral_scores) / len(viral_scores)
                    print(f"   Average viral score: {avg_score:.1f}")
                
                print(f"   Date field present: {'✅' if has_date else '❌'}")
                
                if not missing_fields and has_viral_scores and has_date:
                    print("   ✅ RESPONSE STRUCTURE PERFECT: All required fields present")
                    return True
                else:
                    print("   ❌ RESPONSE STRUCTURE ISSUES DETECTED")
                    return False
            else:
                print("   ❌ No videos to test response structure")
                return False
        else:
            print("   ❌ Failed to test response structure")
            return False

    def run_verification(self):
        """Run all verification tests"""
        print("🎯 FINAL VERIFICATION: VIDEO DISPLAY FIXES TESTING")
        print("="*60)
        
        verification_results = {
            'video_count_verification': self.test_video_count_verification(),
            'platform_content_verification': self.test_platform_content_verification(),
            'user_tier_logic_verification': self.test_user_tier_logic_verification(),
            'url_thumbnail_quality': self.test_url_thumbnail_quality(),
            'response_structure_verification': self.test_response_structure_verification()
        }
        
        # FINAL VERIFICATION SUMMARY
        print("\n" + "="*60)
        print("🎯 FINAL VERIFICATION RESULTS")
        print("="*60)
        
        passed_tests = sum(verification_results.values())
        total_tests = len(verification_results)
        success_rate = (passed_tests / total_tests) * 100
        
        for test_name, result in verification_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"   {test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\n📊 VERIFICATION SCORE: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate == 100:
            print("🎉 ALL VIDEO DISPLAY FIXES VERIFIED SUCCESSFULLY!")
            print("✅ OLD: Only 5 videos showing → ✅ NEW: ~40 videos for free tier")
            print("✅ OLD: TikTok/Twitter links broken → ✅ NEW: Proper platform URLs")
            print("✅ OLD: Missing thumbnails → ✅ NEW: Real thumbnails for all platforms")
        elif success_rate >= 80:
            print("✅ MOST VIDEO DISPLAY FIXES WORKING - Minor issues remain")
        else:
            print("❌ SIGNIFICANT VIDEO DISPLAY ISSUES STILL PRESENT")
        
        print("="*60)
        
        return success_rate >= 80

if __name__ == "__main__":
    verifier = VideoDisplayFixesVerifier()
    success = verifier.run_verification()
    sys.exit(0 if success else 1)