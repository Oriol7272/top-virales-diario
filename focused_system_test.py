#!/usr/bin/env python3
"""
Focused System Health Check for Viral Daily - Key Areas Only
"""

import requests
import json
from datetime import datetime
import uuid
from urllib.parse import unquote

class FocusedSystemTester:
    def __init__(self):
        # Use deployed backend URL from frontend/.env
        try:
            with open('/app/frontend/.env', 'r') as f:
                for line in f:
                    if line.startswith('REACT_APP_BACKEND_URL='):
                        self.base_url = line.split('=')[1].strip()
                        break
        except:
            self.base_url = "http://localhost:8001"
        
        self.api_url = f"{self.base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        
        print(f"🚀 FOCUSED SYSTEM HEALTH CHECK")
        print(f"   Base URL: {self.base_url}")
        print("="*60)

    def run_test(self, name, method, endpoint, expected_status, params=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
        
        self.tests_run += 1
        print(f"\n🔍 {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, params=params, timeout=10)
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Status: {response.status_code}")
                try:
                    return True, response.json()
                except:
                    return True, response.text
            else:
                print(f"❌ Expected {expected_status}, got {response.status_code}")
                return False, {}

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False, {}

    def test_video_aggregation(self):
        """Test mixed platform video aggregation"""
        print(f"\n🎯 VIDEO AGGREGATION HEALTH CHECK")
        print("-" * 40)
        
        success, response = self.run_test(
            "Mixed Platform Aggregation",
            "GET",
            "videos",
            200,
            {'limit': 20}
        )
        
        if not success:
            return False
        
        videos = response.get('videos', [])
        print(f"   📊 Total videos: {len(videos)}")
        
        # Check platforms
        platforms = {}
        for video in videos:
            platform = video.get('platform', 'unknown')
            platforms[platform] = platforms.get(platform, 0) + 1
        
        print(f"   🎭 Platforms: {platforms}")
        
        # Check for Instagram (should be removed)
        if 'instagram' in platforms:
            print("❌ CRITICAL: Instagram found!")
            return False
        
        print("✅ Instagram successfully removed")
        
        # Check required platforms
        expected = {'youtube', 'tiktok', 'twitter'}
        found = set(platforms.keys())
        valid_platforms = found.intersection(expected)
        
        if len(valid_platforms) >= 2:
            print(f"✅ Multi-platform working: {valid_platforms}")
        else:
            print(f"⚠️  Limited platforms: {valid_platforms}")
        
        return len(valid_platforms) >= 2

    def test_platform_filtering(self):
        """Test platform-specific endpoints"""
        print(f"\n🎯 PLATFORM-SPECIFIC ENDPOINTS")
        print("-" * 40)
        
        platforms = ['youtube', 'tiktok', 'twitter']
        results = {}
        
        for platform in platforms:
            success, response = self.run_test(
                f"{platform.title()} Filter",
                "GET",
                "videos",
                200,
                {'platform': platform, 'limit': 5}
            )
            
            if success:
                videos = response.get('videos', [])
                if videos:
                    # Check all videos are from requested platform
                    correct_platform = all(v.get('platform', '').lower() == platform for v in videos)
                    results[platform] = correct_platform
                    print(f"   {'✅' if correct_platform else '❌'} {len(videos)} {platform} videos")
                else:
                    results[platform] = False
                    print(f"   ⚠️  No {platform} videos")
            else:
                results[platform] = False
        
        success_count = sum(results.values())
        print(f"   📊 Platform filtering: {success_count}/{len(platforms)} working")
        
        return success_count >= 2

    def test_url_correctness(self):
        """Test URL correctness - no fake URLs"""
        print(f"\n🎯 URL CORRECTNESS VERIFICATION")
        print("-" * 40)
        
        success, response = self.run_test(
            "URL Analysis",
            "GET",
            "videos",
            200,
            {'limit': 15}
        )
        
        if not success:
            return False
        
        videos = response.get('videos', [])
        fake_patterns = ['viral001', 'viral002', 'example.com', 'test.com']
        
        real_urls = 0
        fake_urls = 0
        
        print(f"   🔍 Analyzing {len(videos)} video URLs...")
        
        for video in videos:
            url = video.get('url', '')
            platform = video.get('platform', '')
            title = video.get('title', 'No title')[:30]
            
            is_fake = any(pattern in url.lower() for pattern in fake_patterns)
            
            if is_fake:
                fake_urls += 1
                print(f"   ❌ FAKE: {platform} - {title}")
            else:
                real_urls += 1
        
        total = len(videos)
        real_pct = (real_urls / total) * 100 if total > 0 else 0
        
        print(f"   📊 Real URLs: {real_urls}/{total} ({real_pct:.1f}%)")
        
        # Check specific URL formats
        self._check_url_formats(videos)
        
        success = real_pct >= 85
        print(f"   {'✅' if success else '❌'} URL correctness: {'PASSED' if success else 'FAILED'}")
        
        return success

    def _check_url_formats(self, videos):
        """Check platform-specific URL formats"""
        youtube_videos = [v for v in videos if v.get('platform') == 'youtube']
        tiktok_videos = [v for v in videos if v.get('platform') == 'tiktok']
        twitter_videos = [v for v in videos if v.get('platform') == 'twitter']
        
        if youtube_videos:
            youtube_correct = sum(1 for v in youtube_videos[:3] if 'youtube.com/watch?v=' in v.get('url', ''))
            print(f"   📺 YouTube format: {youtube_correct}/{min(len(youtube_videos), 3)}")
        
        if tiktok_videos:
            tiktok_correct = sum(1 for v in tiktok_videos[:3] if 'tiktok.com/@' in v.get('url', ''))
            print(f"   📱 TikTok format: {tiktok_correct}/{min(len(tiktok_videos), 3)}")
        
        if twitter_videos:
            twitter_correct = sum(1 for v in twitter_videos[:3] if 'twitter.com/' in v.get('url', '') and '/status/' in v.get('url', ''))
            print(f"   🐦 Twitter format: {twitter_correct}/{min(len(twitter_videos), 3)}")

    def test_thumbnails(self):
        """Test thumbnail verification"""
        print(f"\n🎯 THUMBNAIL VERIFICATION")
        print("-" * 40)
        
        success, response = self.run_test(
            "Thumbnail Analysis",
            "GET",
            "videos",
            200,
            {'limit': 15}
        )
        
        if not success:
            return False
        
        videos = response.get('videos', [])
        
        empty_thumbnails = 0
        valid_thumbnails = 0
        
        platform_thumbnails = {'youtube': 0, 'tiktok': 0, 'twitter': 0}
        
        for video in videos:
            thumbnail = video.get('thumbnail', '')
            platform = video.get('platform', '').lower()
            
            if not thumbnail or thumbnail.strip() == '':
                empty_thumbnails += 1
                print(f"   ❌ EMPTY: {platform} - {video.get('title', 'No title')[:25]}")
            else:
                valid_thumbnails += 1
                if platform in platform_thumbnails:
                    platform_thumbnails[platform] += 1
        
        total = len(videos)
        valid_pct = (valid_thumbnails / total) * 100 if total > 0 else 0
        
        print(f"   📊 Valid thumbnails: {valid_thumbnails}/{total} ({valid_pct:.1f}%)")
        print(f"   🎭 By platform: {platform_thumbnails}")
        
        # Check platform-specific thumbnail types
        self._check_thumbnail_types(videos)
        
        success = empty_thumbnails == 0
        print(f"   {'✅' if success else '❌'} Thumbnail check: {'PASSED' if success else 'FAILED'}")
        
        return success

    def _check_thumbnail_types(self, videos):
        """Check thumbnail types by platform"""
        youtube_videos = [v for v in videos if v.get('platform') == 'youtube']
        tiktok_videos = [v for v in videos if v.get('platform') == 'tiktok']
        twitter_videos = [v for v in videos if v.get('platform') == 'twitter']
        
        if youtube_videos:
            http_count = sum(1 for v in youtube_videos if v.get('thumbnail', '').startswith('http'))
            ytimg_count = sum(1 for v in youtube_videos if 'ytimg.com' in v.get('thumbnail', ''))
            print(f"   📺 YouTube: {http_count} HTTP, {ytimg_count} ytimg.com")
        
        if tiktok_videos:
            svg_count = sum(1 for v in tiktok_videos if v.get('thumbnail', '').startswith('data:image/svg+xml'))
            print(f"   📱 TikTok: {svg_count} SVG thumbnails")
        
        if twitter_videos:
            svg_count = sum(1 for v in twitter_videos if v.get('thumbnail', '').startswith('data:image/svg+xml'))
            print(f"   🐦 Twitter: {svg_count} SVG thumbnails")

    def test_system_integration(self):
        """Test key system integration points"""
        print(f"\n🎯 SYSTEM INTEGRATION HEALTH")
        print("-" * 40)
        
        results = {}
        
        # Test subscription plans
        success, response = self.run_test(
            "Subscription Plans",
            "GET",
            "subscription/plans",
            200
        )
        results['subscriptions'] = success
        if success:
            plans = response.get('plans', [])
            print(f"   ✅ {len(plans)} subscription plans available")
        
        # Test PayPal integration
        success, response = self.run_test(
            "PayPal Integration",
            "GET",
            "payments/paypal/available",
            200
        )
        results['paypal'] = success
        if success:
            available = response.get('available', False)
            mode = response.get('mode', 'unknown')
            print(f"   {'✅' if available else '❌'} PayPal: {mode} mode")
        
        working = sum(results.values())
        total = len(results)
        print(f"   📊 Integration health: {working}/{total}")
        
        return working >= 1

    def run_focused_tests(self):
        """Run focused system tests"""
        print(f"\n🎯 RUNNING FOCUSED SYSTEM HEALTH CHECK")
        print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)
        
        # Run key tests
        test_results = {}
        test_results['video_aggregation'] = self.test_video_aggregation()
        test_results['platform_filtering'] = self.test_platform_filtering()
        test_results['url_correctness'] = self.test_url_correctness()
        test_results['thumbnails'] = self.test_thumbnails()
        test_results['system_integration'] = self.test_system_integration()
        
        # Generate report
        print(f"\n" + "="*60)
        print(f"🎯 FOCUSED SYSTEM HEALTH RESULTS")
        print("="*60)
        
        passed = sum(test_results.values())
        total = len(test_results)
        success_rate = (passed / total) * 100
        
        print(f"\n📊 RESULTS:")
        print(f"   API Tests: {self.tests_passed}/{self.tests_run} passed")
        print(f"   System Components: {passed}/{total} working ({success_rate:.1f}%)")
        
        print(f"\n🎯 KEY SYSTEM VERIFICATION:")
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status} {test_name.replace('_', ' ').title()}")
        
        if success_rate >= 80:
            print(f"\n🎉 SYSTEM STATUS: HEALTHY ({success_rate:.1f}%)")
        elif success_rate >= 60:
            print(f"\n⚠️  SYSTEM STATUS: FAIR ({success_rate:.1f}%)")
        else:
            print(f"\n❌ SYSTEM STATUS: NEEDS ATTENTION ({success_rate:.1f}%)")
        
        print("="*60)
        
        return test_results

if __name__ == "__main__":
    tester = FocusedSystemTester()
    results = tester.run_focused_tests()