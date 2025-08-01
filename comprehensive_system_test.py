#!/usr/bin/env python3
"""
Comprehensive System Health Check for Viral Daily
Focus on video aggregation, URL correctness, thumbnails, and system integration
"""

import requests
import sys
import json
from datetime import datetime
import uuid
import time
from urllib.parse import urlparse, unquote

class ComprehensiveSystemTester:
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
        self.test_user = None
        self.test_api_key = None
        
        print(f"🚀 COMPREHENSIVE SYSTEM HEALTH CHECK")
        print(f"   Base URL: {self.base_url}")
        print(f"   API URL: {self.api_url}")
        print("="*80)

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
        request_headers = {'Content-Type': 'application/json'}
        
        if self.test_api_key:
            request_headers['Authorization'] = f'Bearer {self.test_api_key}'
        
        if headers:
            request_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=request_headers, params=params, timeout=15)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=request_headers, timeout=15)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    return True, response_data
                except:
                    return True, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout (>15s)")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def setup_test_user(self):
        """Create a test user for authenticated tests"""
        test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        test_name = f"Test User {datetime.now().strftime('%H%M%S')}"
        
        success, response = self.run_test(
            "User Registration for Testing",
            "POST",
            "users/register",
            200,
            data={"email": test_email, "name": test_name}
        )
        
        if success and isinstance(response, dict):
            self.test_user = response
            self.test_api_key = response['api_key']
            print(f"   ✅ Test user created: {response['email']}")
            return True
        return False

    def test_1_video_aggregation_health(self):
        """Test 1: Video Aggregation Health Check - Mixed platform aggregation"""
        print(f"\n🎯 TEST 1: VIDEO AGGREGATION HEALTH CHECK")
        print("="*60)
        
        success, response = self.run_test(
            "Mixed Platform Video Aggregation",
            "GET",
            "videos",
            200,
            params={'limit': 30}
        )
        
        if not success:
            print("❌ CRITICAL: Video aggregation endpoint failed")
            return False
        
        videos = response.get('videos', [])
        total = response.get('total', 0)
        
        print(f"   📊 Total videos returned: {total}")
        
        if not videos:
            print("❌ CRITICAL: No videos returned")
            return False
        
        # Check platform distribution
        platforms = {}
        for video in videos:
            platform = video.get('platform', 'unknown')
            platforms[platform] = platforms.get(platform, 0) + 1
        
        print(f"   🎭 Platform distribution: {platforms}")
        
        # Verify expected platforms (YouTube, TikTok, Twitter)
        expected_platforms = {'youtube', 'tiktok', 'twitter'}
        found_platforms = set(platforms.keys())
        
        # Check for forbidden Instagram
        if 'instagram' in found_platforms:
            print("❌ CRITICAL: Instagram videos found! Instagram should be removed.")
            return False
        
        print("✅ Instagram successfully removed - no Instagram videos found")
        
        # Check if we have videos from multiple platforms
        valid_platforms = found_platforms.intersection(expected_platforms)
        if len(valid_platforms) >= 2:
            print(f"✅ Multi-platform aggregation working: {valid_platforms}")
        else:
            print(f"⚠️  Limited platform diversity: {valid_platforms}")
        
        # Check video structure
        required_fields = ['title', 'url', 'thumbnail', 'platform', 'viral_score', 'views', 'author']
        sample_video = videos[0]
        missing_fields = [field for field in required_fields if field not in sample_video]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        print("✅ Video structure validation passed")
        
        # Check viral scores
        viral_scores = [v.get('viral_score', 0) for v in videos if v.get('viral_score')]
        if viral_scores:
            avg_score = sum(viral_scores) / len(viral_scores)
            score_range = f"{min(viral_scores):.1f}-{max(viral_scores):.1f}"
            print(f"   📈 Viral scores: avg {avg_score:.1f}, range {score_range}")
            
            if all(0 <= score <= 100 for score in viral_scores):
                print("✅ Viral scores in valid range (0-100)")
            else:
                print("⚠️  Some viral scores outside 0-100 range")
        
        return True

    def test_2_platform_specific_endpoints(self):
        """Test 2: Platform-Specific Endpoint Testing"""
        print(f"\n🎯 TEST 2: PLATFORM-SPECIFIC ENDPOINT TESTING")
        print("="*60)
        
        platforms = ['youtube', 'tiktok', 'twitter']
        all_passed = True
        
        for platform in platforms:
            print(f"\n   Testing {platform.upper()} platform filter...")
            
            success, response = self.run_test(
                f"Get {platform.title()} Videos Only",
                "GET",
                "videos",
                200,
                params={'platform': platform, 'limit': 10}
            )
            
            if not success:
                print(f"❌ {platform} endpoint failed")
                all_passed = False
                continue
            
            videos = response.get('videos', [])
            if not videos:
                print(f"⚠️  No {platform} videos returned")
                continue
            
            # Verify all videos are from requested platform
            platform_check = all(v.get('platform', '').lower() == platform for v in videos)
            if platform_check:
                print(f"✅ All {len(videos)} videos are from {platform}")
            else:
                mixed_platforms = set(v.get('platform', '') for v in videos)
                print(f"❌ Mixed platforms found: {mixed_platforms}")
                all_passed = False
            
            # Check URLs for platform-specific format
            self._verify_platform_urls(videos, platform)
        
        return all_passed

    def _verify_platform_urls(self, videos, expected_platform):
        """Verify URLs match expected platform format"""
        url_patterns = {
            'youtube': 'youtube.com/watch',
            'tiktok': 'tiktok.com/',
            'twitter': 'twitter.com/'
        }
        
        pattern = url_patterns.get(expected_platform)
        if not pattern:
            return
        
        valid_urls = 0
        total_urls = len(videos)
        
        for video in videos[:5]:  # Check first 5
            url = video.get('url', '')
            if pattern in url:
                valid_urls += 1
                print(f"      ✅ Valid {expected_platform} URL: {url[:50]}...")
            else:
                print(f"      ❌ Invalid {expected_platform} URL: {url[:50]}...")
        
        accuracy = (valid_urls / min(total_urls, 5)) * 100
        print(f"   📊 URL accuracy: {valid_urls}/{min(total_urls, 5)} ({accuracy:.1f}%)")

    def test_3_url_correctness_verification(self):
        """Test 3: URL Correctness Verification - Real URLs vs fake ones"""
        print(f"\n🎯 TEST 3: URL CORRECTNESS VERIFICATION")
        print("="*60)
        
        success, response = self.run_test(
            "URL Correctness Analysis",
            "GET",
            "videos",
            200,
            params={'limit': 25}
        )
        
        if not success:
            print("❌ CRITICAL: Cannot fetch videos for URL analysis")
            return False
        
        videos = response.get('videos', [])
        
        # Analyze URLs by platform
        url_analysis = {
            'youtube': {'real': 0, 'fake': 0, 'total': 0},
            'tiktok': {'real': 0, 'fake': 0, 'total': 0},
            'twitter': {'real': 0, 'fake': 0, 'total': 0},
            'other': {'real': 0, 'fake': 0, 'total': 0}
        }
        
        fake_patterns = ['viral001', 'viral002', 'viral003', 'example.com', 'test.com', 'fake.com']
        
        for video in videos:
            platform = video.get('platform', 'other').lower()
            url = video.get('url', '')
            title = video.get('title', 'No title')[:40]
            
            if platform not in url_analysis:
                platform = 'other'
            
            url_analysis[platform]['total'] += 1
            
            # Check for fake patterns
            is_fake = any(pattern in url.lower() for pattern in fake_patterns)
            
            if is_fake:
                url_analysis[platform]['fake'] += 1
                print(f"      ❌ FAKE URL detected: {platform} - {title} -> {url}")
            else:
                url_analysis[platform]['real'] += 1
        
        # Report results
        print(f"\n   📊 URL CORRECTNESS ANALYSIS:")
        total_real = 0
        total_fake = 0
        total_videos = 0
        
        for platform, stats in url_analysis.items():
            if stats['total'] > 0:
                real_pct = (stats['real'] / stats['total']) * 100
                print(f"   {platform.upper()}: {stats['real']}/{stats['total']} real URLs ({real_pct:.1f}%)")
                total_real += stats['real']
                total_fake += stats['fake']
                total_videos += stats['total']
        
        overall_real_pct = (total_real / total_videos) * 100 if total_videos > 0 else 0
        print(f"\n   🎯 OVERALL: {total_real}/{total_videos} real URLs ({overall_real_pct:.1f}%)")
        
        # Specific URL format checks
        self._check_youtube_url_format(videos)
        self._check_tiktok_url_format(videos)
        self._check_twitter_url_format(videos)
        
        # Success criteria: >90% real URLs
        success = overall_real_pct >= 90
        if success:
            print("✅ URL correctness verification PASSED")
        else:
            print("❌ URL correctness verification FAILED - too many fake URLs")
        
        return success

    def _check_youtube_url_format(self, videos):
        """Check YouTube URL format: https://www.youtube.com/watch?v={video_id}"""
        youtube_videos = [v for v in videos if v.get('platform', '').lower() == 'youtube']
        if not youtube_videos:
            return
        
        print(f"\n   🔍 YouTube URL Format Check ({len(youtube_videos)} videos):")
        valid_format = 0
        
        for video in youtube_videos[:3]:  # Check first 3
            url = video.get('url', '')
            title = video.get('title', 'No title')[:30]
            
            if 'youtube.com/watch?v=' in url and len(url.split('v=')[1].split('&')[0]) >= 10:
                valid_format += 1
                video_id = url.split('v=')[1].split('&')[0]
                print(f"      ✅ {title} -> Video ID: {video_id}")
            else:
                print(f"      ❌ {title} -> Invalid format: {url}")
        
        print(f"   YouTube format accuracy: {valid_format}/{min(len(youtube_videos), 3)}")

    def _check_tiktok_url_format(self, videos):
        """Check TikTok URL format: https://www.tiktok.com/@{username}/video/{id}"""
        tiktok_videos = [v for v in videos if v.get('platform', '').lower() == 'tiktok']
        if not tiktok_videos:
            return
        
        print(f"\n   🔍 TikTok URL Format Check ({len(tiktok_videos)} videos):")
        valid_format = 0
        
        for video in tiktok_videos[:3]:  # Check first 3
            url = video.get('url', '')
            title = video.get('title', 'No title')[:30]
            
            if 'tiktok.com/@' in url and '/video/' in url:
                valid_format += 1
                username = url.split('@')[1].split('/')[0]
                print(f"      ✅ {title} -> @{username}")
            else:
                print(f"      ❌ {title} -> Invalid format: {url}")
        
        print(f"   TikTok format accuracy: {valid_format}/{min(len(tiktok_videos), 3)}")

    def _check_twitter_url_format(self, videos):
        """Check Twitter URL format: https://twitter.com/{username}/status/{tweet_id}"""
        twitter_videos = [v for v in videos if v.get('platform', '').lower() == 'twitter']
        if not twitter_videos:
            return
        
        print(f"\n   🔍 Twitter URL Format Check ({len(twitter_videos)} videos):")
        valid_format = 0
        
        for video in twitter_videos[:3]:  # Check first 3
            url = video.get('url', '')
            title = video.get('title', 'No title')[:30]
            
            if 'twitter.com/' in url and '/status/' in url:
                valid_format += 1
                username = url.split('twitter.com/')[1].split('/')[0]
                print(f"      ✅ {title} -> @{username}")
            else:
                print(f"      ❌ {title} -> Invalid format: {url}")
        
        print(f"   Twitter format accuracy: {valid_format}/{min(len(twitter_videos), 3)}")

    def test_4_thumbnail_verification(self):
        """Test 4: Thumbnail Verification - All platforms should have proper thumbnails"""
        print(f"\n🎯 TEST 4: THUMBNAIL VERIFICATION")
        print("="*60)
        
        success, response = self.run_test(
            "Thumbnail Quality Analysis",
            "GET",
            "videos",
            200,
            params={'limit': 20}
        )
        
        if not success:
            print("❌ CRITICAL: Cannot fetch videos for thumbnail analysis")
            return False
        
        videos = response.get('videos', [])
        
        # Analyze thumbnails by platform
        thumbnail_analysis = {
            'youtube': {'http': 0, 'svg': 0, 'empty': 0, 'total': 0},
            'tiktok': {'http': 0, 'svg': 0, 'empty': 0, 'total': 0},
            'twitter': {'http': 0, 'svg': 0, 'empty': 0, 'total': 0}
        }
        
        for video in videos:
            platform = video.get('platform', '').lower()
            thumbnail = video.get('thumbnail', '')
            title = video.get('title', 'No title')[:30]
            
            if platform not in thumbnail_analysis:
                continue
            
            thumbnail_analysis[platform]['total'] += 1
            
            if not thumbnail or thumbnail.strip() == '':
                thumbnail_analysis[platform]['empty'] += 1
                print(f"      ❌ EMPTY thumbnail: {platform} - {title}")
            elif thumbnail.startswith('http'):
                thumbnail_analysis[platform]['http'] += 1
            elif thumbnail.startswith('data:image/svg+xml'):
                thumbnail_analysis[platform]['svg'] += 1
            else:
                print(f"      ⚠️  Unknown thumbnail format: {platform} - {thumbnail[:50]}")
        
        # Report results
        print(f"\n   📊 THUMBNAIL ANALYSIS:")
        all_good = True
        
        for platform, stats in thumbnail_analysis.items():
            if stats['total'] > 0:
                empty_pct = (stats['empty'] / stats['total']) * 100
                print(f"   {platform.upper()}: {stats['total']} videos, {stats['empty']} empty ({empty_pct:.1f}%)")
                print(f"      HTTP: {stats['http']}, SVG: {stats['svg']}")
                
                if stats['empty'] > 0:
                    all_good = False
        
        # Platform-specific checks
        self._verify_youtube_thumbnails(videos)
        self._verify_tiktok_thumbnails(videos)
        self._verify_twitter_thumbnails(videos)
        
        if all_good:
            print("✅ Thumbnail verification PASSED - no empty thumbnails")
        else:
            print("❌ Thumbnail verification FAILED - empty thumbnails found")
        
        return all_good

    def _verify_youtube_thumbnails(self, videos):
        """Verify YouTube videos have HTTP thumbnail URLs (preferably ytimg.com)"""
        youtube_videos = [v for v in videos if v.get('platform', '').lower() == 'youtube']
        if not youtube_videos:
            return
        
        print(f"\n   📺 YouTube Thumbnails ({len(youtube_videos)} videos):")
        ytimg_count = 0
        http_count = 0
        
        for video in youtube_videos[:3]:
            thumbnail = video.get('thumbnail', '')
            title = video.get('title', 'No title')[:25]
            
            if thumbnail.startswith('http'):
                http_count += 1
                if 'ytimg.com' in thumbnail:
                    ytimg_count += 1
                    print(f"      ✅ {title} -> ytimg.com CDN")
                else:
                    print(f"      ✅ {title} -> HTTP thumbnail")
            else:
                print(f"      ❌ {title} -> Non-HTTP: {thumbnail[:30]}")
        
        print(f"   YouTube HTTP thumbnails: {http_count}/{min(len(youtube_videos), 3)}")
        print(f"   YouTube ytimg.com CDN: {ytimg_count}/{min(len(youtube_videos), 3)}")

    def _verify_tiktok_thumbnails(self, videos):
        """Verify TikTok videos have SVG thumbnails with platform styling"""
        tiktok_videos = [v for v in videos if v.get('platform', '').lower() == 'tiktok']
        if not tiktok_videos:
            return
        
        print(f"\n   📱 TikTok Thumbnails ({len(tiktok_videos)} videos):")
        svg_count = 0
        
        for video in tiktok_videos[:3]:
            thumbnail = video.get('thumbnail', '')
            title = video.get('title', 'No title')[:25]
            
            if thumbnail.startswith('data:image/svg+xml'):
                svg_count += 1
                # Check for TikTok styling
                try:
                    svg_content = unquote(thumbnail.split(',')[1])
                    has_music_icon = '🎵' in svg_content
                    has_black_theme = '#000000' in svg_content
                    print(f"      ✅ {title} -> SVG (Music: {has_music_icon}, Black: {has_black_theme})")
                except:
                    print(f"      ✅ {title} -> SVG thumbnail")
            else:
                print(f"      ❌ {title} -> Non-SVG: {thumbnail[:30]}")
        
        print(f"   TikTok SVG thumbnails: {svg_count}/{min(len(tiktok_videos), 3)}")

    def _verify_twitter_thumbnails(self, videos):
        """Verify Twitter videos have SVG thumbnails with platform styling"""
        twitter_videos = [v for v in videos if v.get('platform', '').lower() == 'twitter']
        if not twitter_videos:
            return
        
        print(f"\n   🐦 Twitter Thumbnails ({len(twitter_videos)} videos):")
        svg_count = 0
        
        for video in twitter_videos[:3]:
            thumbnail = video.get('thumbnail', '')
            title = video.get('title', 'No title')[:25]
            
            if thumbnail.startswith('data:image/svg+xml'):
                svg_count += 1
                # Check for Twitter styling
                try:
                    svg_content = unquote(thumbnail.split(',')[1])
                    has_bird_icon = '🐦' in svg_content
                    has_blue_theme = '#1DA1F2' in svg_content
                    print(f"      ✅ {title} -> SVG (Bird: {has_bird_icon}, Blue: {has_blue_theme})")
                except:
                    print(f"      ✅ {title} -> SVG thumbnail")
            else:
                print(f"      ❌ {title} -> Non-SVG: {thumbnail[:30]}")
        
        print(f"   Twitter SVG thumbnails: {svg_count}/{min(len(twitter_videos), 3)}")

    def test_5_system_integration_health(self):
        """Test 5: System Integration Health - Authentication, PayPal, subscriptions"""
        print(f"\n🎯 TEST 5: SYSTEM INTEGRATION HEALTH")
        print("="*60)
        
        integration_results = {}
        
        # Test authentication endpoints
        print(f"\n   🔐 Authentication System:")
        if self.test_user:
            success, response = self.run_test(
                "Get Current User Info",
                "GET",
                "users/me",
                200
            )
            integration_results['auth'] = success
            if success:
                print("      ✅ Authentication working")
            else:
                print("      ❌ Authentication failed")
        else:
            print("      ⚠️  No test user available")
            integration_results['auth'] = False
        
        # Test PayPal integration
        print(f"\n   💳 PayPal Integration:")
        success, response = self.run_test(
            "PayPal Availability Check",
            "GET",
            "payments/paypal/available",
            200
        )
        integration_results['paypal'] = success
        if success and isinstance(response, dict):
            available = response.get('available', False)
            mode = response.get('mode', 'unknown')
            print(f"      {'✅' if available else '❌'} PayPal: {mode} mode, available: {available}")
        else:
            print("      ❌ PayPal integration failed")
        
        # Test subscription plans
        print(f"\n   📋 Subscription Plans:")
        success, response = self.run_test(
            "Get Subscription Plans",
            "GET",
            "subscription/plans",
            200
        )
        integration_results['subscriptions'] = success
        if success and isinstance(response, dict):
            plans = response.get('plans', [])
            tiers = [plan.get('tier') for plan in plans]
            print(f"      ✅ {len(plans)} plans available: {tiers}")
        else:
            print("      ❌ Subscription plans failed")
        
        # Calculate integration health
        working_systems = sum(integration_results.values())
        total_systems = len(integration_results)
        health_pct = (working_systems / total_systems) * 100 if total_systems > 0 else 0
        
        print(f"\n   📊 Integration Health: {working_systems}/{total_systems} ({health_pct:.1f}%)")
        
        return health_pct >= 75

    def test_6_performance_reliability(self):
        """Test 6: Performance & Reliability - Response times and error handling"""
        print(f"\n🎯 TEST 6: PERFORMANCE & RELIABILITY")
        print("="*60)
        
        # Test response times
        endpoints_to_test = [
            ("Root API", "", {}),
            ("All Videos", "videos", {'limit': 10}),
            ("YouTube Videos", "videos", {'platform': 'youtube', 'limit': 5}),
            ("Subscription Plans", "subscription/plans", {})
        ]
        
        response_times = []
        
        for name, endpoint, params in endpoints_to_test:
            start_time = time.time()
            
            success, response = self.run_test(
                f"Performance Test - {name}",
                "GET",
                endpoint,
                200,
                params=params
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            response_times.append(response_time)
            
            if success:
                if response_time < 5.0:
                    print(f"      ✅ Response time: {response_time:.2f}s (Good)")
                else:
                    print(f"      ⚠️  Response time: {response_time:.2f}s (Slow)")
            else:
                print(f"      ❌ Failed - Response time: {response_time:.2f}s")
        
        # Calculate average response time
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            print(f"\n   📊 Performance Summary:")
            print(f"      Average response time: {avg_response_time:.2f}s")
            print(f"      Maximum response time: {max_response_time:.2f}s")
            
            performance_good = avg_response_time < 5.0 and max_response_time < 10.0
        else:
            performance_good = False
        
        # Test error handling
        print(f"\n   🛡️  Error Handling Tests:")
        
        # Test invalid platform
        success, response = self.run_test(
            "Invalid Platform Error Handling",
            "GET",
            "videos",
            422,  # Should return validation error
            params={'platform': 'invalid_platform'}
        )
        
        error_handling_good = success
        if success:
            print("      ✅ Invalid platform properly rejected")
        else:
            print("      ⚠️  Invalid platform handling unclear")
        
        # Test invalid endpoint
        success, response = self.run_test(
            "Invalid Endpoint Error Handling",
            "GET",
            "nonexistent/endpoint",
            404
        )
        
        if success:
            print("      ✅ Invalid endpoint returns 404")
            error_handling_good = error_handling_good and True
        else:
            print("      ⚠️  Invalid endpoint handling unclear")
        
        overall_reliability = performance_good and error_handling_good
        
        if overall_reliability:
            print("✅ Performance & Reliability PASSED")
        else:
            print("⚠️  Performance & Reliability has issues")
        
        return overall_reliability

    def run_comprehensive_test(self):
        """Run all comprehensive system tests"""
        print(f"\n🎯 STARTING COMPREHENSIVE SYSTEM HEALTH CHECK")
        print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        # Setup test user
        print(f"\n👤 SETTING UP TEST USER")
        user_setup = self.setup_test_user()
        if not user_setup:
            print("⚠️  Continuing without authenticated user")
        
        # Run all tests
        test_results = {}
        
        test_results['video_aggregation'] = self.test_1_video_aggregation_health()
        test_results['platform_endpoints'] = self.test_2_platform_specific_endpoints()
        test_results['url_correctness'] = self.test_3_url_correctness_verification()
        test_results['thumbnails'] = self.test_4_thumbnail_verification()
        test_results['system_integration'] = self.test_5_system_integration_health()
        test_results['performance'] = self.test_6_performance_reliability()
        
        # Generate final report
        self.generate_final_report(test_results)
        
        return test_results

    def generate_final_report(self, test_results):
        """Generate comprehensive final report"""
        print(f"\n" + "="*80)
        print(f"🎯 COMPREHENSIVE SYSTEM HEALTH CHECK RESULTS")
        print(f"="*80)
        
        passed_tests = sum(test_results.values())
        total_tests = len(test_results)
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   Tests Run: {self.tests_run}")
        print(f"   Tests Passed: {self.tests_passed}")
        print(f"   Individual Test Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        print(f"   System Component Success Rate: {success_rate:.1f}%")
        
        print(f"\n🎯 CRITICAL SYSTEM VERIFICATION RESULTS:")
        
        status_icon = lambda x: "✅" if x else "❌"
        
        print(f"   {status_icon(test_results['video_aggregation'])} Video Aggregation Health Check")
        print(f"   {status_icon(test_results['platform_endpoints'])} Platform-Specific Endpoint Testing")
        print(f"   {status_icon(test_results['url_correctness'])} URL Correctness Verification")
        print(f"   {status_icon(test_results['thumbnails'])} Thumbnail Verification")
        print(f"   {status_icon(test_results['system_integration'])} System Integration Health")
        print(f"   {status_icon(test_results['performance'])} Performance & Reliability")
        
        # Overall system health
        if success_rate >= 90:
            print(f"\n🎉 SYSTEM STATUS: EXCELLENT ({success_rate:.1f}%)")
            print("   All critical systems are operational!")
        elif success_rate >= 75:
            print(f"\n✅ SYSTEM STATUS: GOOD ({success_rate:.1f}%)")
            print("   Most systems operational with minor issues")
        elif success_rate >= 50:
            print(f"\n⚠️  SYSTEM STATUS: FAIR ({success_rate:.1f}%)")
            print("   Some systems need attention")
        else:
            print(f"\n❌ SYSTEM STATUS: POOR ({success_rate:.1f}%)")
            print("   Critical systems need immediate attention")
        
        print(f"\n" + "="*80)

if __name__ == "__main__":
    tester = ComprehensiveSystemTester()
    results = tester.run_comprehensive_test()
    
    # Exit with appropriate code
    passed_tests = sum(results.values())
    total_tests = len(results)
    success_rate = (passed_tests / total_tests) * 100
    
    if success_rate >= 75:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Issues detected