#!/usr/bin/env python3
"""
URGENT VIDEO LINKS DIAGNOSIS TOOL
Comprehensive analysis of video URL generation and accessibility issues
"""

import requests
import sys
import json
from datetime import datetime
import uuid
import re
from urllib.parse import urlparse, parse_qs
import time

class VideoLinksDiagnosticTool:
    def __init__(self, base_url=None):
        # Use deployed backend URL from frontend/.env
        if base_url is None:
            try:
                with open('/app/frontend/.env', 'r') as f:
                    for line in f:
                        if line.startswith('REACT_APP_BACKEND_URL='):
                            base_url = line.split('=')[1].strip()
                            break
                if base_url is None:
                    base_url = "http://localhost:8001"
            except:
                base_url = "http://localhost:8001"
        
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.broken_urls = []
        self.url_analysis = {}

    def log_result(self, test_name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name}")
        else:
            print(f"❌ {test_name}")
        
        if details:
            print(f"   {details}")

    def analyze_url_format(self, url, platform):
        """Analyze URL format for platform-specific patterns"""
        if not url:
            return {"valid": False, "issue": "Empty URL"}
        
        parsed = urlparse(url)
        analysis = {
            "url": url,
            "platform": platform,
            "domain": parsed.netloc,
            "path": parsed.path,
            "valid": False,
            "issues": [],
            "expected_format": "",
            "accessibility": "unknown"
        }
        
        # Platform-specific URL validation
        if platform.lower() == 'youtube':
            analysis["expected_format"] = "https://www.youtube.com/watch?v=VIDEO_ID"
            
            if 'youtube.com' in parsed.netloc:
                if '/watch' in parsed.path:
                    query_params = parse_qs(parsed.query)
                    if 'v' in query_params:
                        video_id = query_params['v'][0]
                        if len(video_id) == 11:  # YouTube video IDs are 11 characters
                            analysis["valid"] = True
                            analysis["video_id"] = video_id
                        else:
                            analysis["issues"].append(f"Invalid video ID length: {len(video_id)}")
                    else:
                        analysis["issues"].append("Missing 'v' parameter in query")
                else:
                    analysis["issues"].append("Invalid YouTube path - should contain '/watch'")
            else:
                analysis["issues"].append(f"Invalid domain for YouTube: {parsed.netloc}")
                
        elif platform.lower() == 'twitter':
            analysis["expected_format"] = "https://twitter.com/username/status/TWEET_ID"
            
            if 'twitter.com' in parsed.netloc:
                path_parts = parsed.path.strip('/').split('/')
                if len(path_parts) >= 3 and path_parts[1] == 'status':
                    tweet_id = path_parts[2]
                    if tweet_id.isdigit() and len(tweet_id) >= 15:  # Twitter IDs are typically 18-19 digits
                        analysis["valid"] = True
                        analysis["tweet_id"] = tweet_id
                    else:
                        analysis["issues"].append(f"Invalid tweet ID format: {tweet_id}")
                elif '/i/status/' in parsed.path:
                    # Alternative Twitter URL format
                    tweet_id = parsed.path.split('/i/status/')[-1]
                    if tweet_id.isdigit() and len(tweet_id) >= 15:
                        analysis["valid"] = True
                        analysis["tweet_id"] = tweet_id
                    else:
                        analysis["issues"].append(f"Invalid tweet ID in /i/status/ format: {tweet_id}")
                else:
                    analysis["issues"].append("Invalid Twitter path format")
            else:
                analysis["issues"].append(f"Invalid domain for Twitter: {parsed.netloc}")
                
        elif platform.lower() == 'tiktok':
            analysis["expected_format"] = "https://www.tiktok.com/@username/video/VIDEO_ID"
            
            if 'tiktok.com' in parsed.netloc:
                if '/video/' in parsed.path:
                    video_id = parsed.path.split('/video/')[-1]
                    if video_id.isdigit() and len(video_id) >= 15:  # TikTok video IDs are long numbers
                        analysis["valid"] = True
                        analysis["video_id"] = video_id
                    else:
                        analysis["issues"].append(f"Invalid TikTok video ID: {video_id}")
                else:
                    analysis["issues"].append("Invalid TikTok path - should contain '/video/'")
            else:
                analysis["issues"].append(f"Invalid domain for TikTok: {parsed.netloc}")
        
        return analysis

    def test_url_accessibility(self, url, timeout=10):
        """Test if URL is accessible"""
        if not url or not url.startswith('http'):
            return {"accessible": False, "error": "Invalid URL format"}
        
        try:
            # Use HEAD request first to avoid downloading content
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            
            if response.status_code == 200:
                return {"accessible": True, "status_code": 200, "final_url": response.url}
            elif response.status_code in [301, 302, 303, 307, 308]:
                return {"accessible": True, "status_code": response.status_code, "redirected": True, "final_url": response.url}
            elif response.status_code == 405:  # Method not allowed, try GET
                response = requests.get(url, timeout=timeout, stream=True)
                response.close()  # Close immediately to avoid downloading content
                return {"accessible": True, "status_code": response.status_code, "method": "GET"}
            else:
                return {"accessible": False, "status_code": response.status_code, "error": f"HTTP {response.status_code}"}
                
        except requests.exceptions.Timeout:
            return {"accessible": False, "error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            return {"accessible": False, "error": "Connection error"}
        except requests.exceptions.RequestException as e:
            return {"accessible": False, "error": str(e)}

    def fetch_and_analyze_videos(self, platform=None, limit=20):
        """Fetch videos and analyze their URLs"""
        print(f"\n🔍 FETCHING AND ANALYZING VIDEO URLS...")
        
        # Build request URL
        url = f"{self.api_url}/videos"
        params = {'limit': limit}
        if platform:
            params['platform'] = platform
        
        try:
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code != 200:
                self.log_result(f"Fetch Videos API Call", False, f"HTTP {response.status_code}: {response.text[:200]}")
                return []
            
            data = response.json()
            videos = data.get('videos', [])
            
            self.log_result(f"Fetch Videos API Call", True, f"Retrieved {len(videos)} videos")
            
            return videos
            
        except Exception as e:
            self.log_result(f"Fetch Videos API Call", False, f"Error: {str(e)}")
            return []

    def analyze_platform_urls(self, platform):
        """Comprehensive URL analysis for a specific platform"""
        print(f"\n🎯 ANALYZING {platform.upper()} VIDEO URLS...")
        
        videos = self.fetch_and_analyze_videos(platform=platform, limit=15)
        
        if not videos:
            print(f"   ❌ No {platform} videos found for analysis")
            return
        
        print(f"   📊 Analyzing {len(videos)} {platform} videos...")
        
        valid_urls = 0
        broken_urls = 0
        mock_urls = 0
        accessible_urls = 0
        
        for i, video in enumerate(videos[:10]):  # Analyze first 10 videos
            title = video.get('title', 'No title')[:50]
            url = video.get('url', '')
            thumbnail = video.get('thumbnail', '')
            viral_score = video.get('viral_score', 0)
            
            print(f"\n   📹 Video {i+1}: {title}...")
            print(f"      URL: {url}")
            print(f"      Thumbnail: {thumbnail[:80]}{'...' if len(thumbnail) > 80 else ''}")
            print(f"      Viral Score: {viral_score}")
            
            # Analyze URL format
            url_analysis = self.analyze_url_format(url, platform)
            
            if url_analysis["valid"]:
                valid_urls += 1
                print(f"      ✅ URL Format: Valid {platform} URL")
                if "video_id" in url_analysis:
                    print(f"      🆔 Video ID: {url_analysis['video_id']}")
                elif "tweet_id" in url_analysis:
                    print(f"      🆔 Tweet ID: {url_analysis['tweet_id']}")
            else:
                broken_urls += 1
                print(f"      ❌ URL Format: Invalid - {', '.join(url_analysis['issues'])}")
                print(f"      📝 Expected: {url_analysis['expected_format']}")
                
                self.broken_urls.append({
                    "platform": platform,
                    "title": title,
                    "url": url,
                    "issues": url_analysis["issues"]
                })
            
            # Check if URL looks like mock data
            if any(mock_indicator in url.lower() for mock_indicator in ['viral', 'test', 'mock', 'sample', 'fake']):
                mock_urls += 1
                print(f"      ⚠️  URL appears to be MOCK DATA")
            
            # Test URL accessibility (for first 5 videos to avoid rate limits)
            if i < 5:
                print(f"      🌐 Testing accessibility...")
                accessibility = self.test_url_accessibility(url)
                
                if accessibility["accessible"]:
                    accessible_urls += 1
                    print(f"      ✅ Accessible (HTTP {accessibility.get('status_code', 'unknown')})")
                    if accessibility.get("redirected"):
                        print(f"      🔄 Redirected to: {accessibility.get('final_url', 'unknown')[:60]}...")
                else:
                    print(f"      ❌ Not Accessible: {accessibility.get('error', 'Unknown error')}")
        
        # Summary for platform
        print(f"\n   📊 {platform.upper()} URL ANALYSIS SUMMARY:")
        print(f"      Valid URLs: {valid_urls}/{len(videos[:10])}")
        print(f"      Broken URLs: {broken_urls}/{len(videos[:10])}")
        print(f"      Mock URLs: {mock_urls}/{len(videos[:10])}")
        print(f"      Accessible URLs: {accessible_urls}/5 (tested)")
        
        success_rate = (valid_urls / len(videos[:10])) * 100 if videos else 0
        print(f"      Success Rate: {success_rate:.1f}%")
        
        if success_rate < 50:
            print(f"      🚨 CRITICAL: {platform} has high URL failure rate!")
        elif success_rate < 80:
            print(f"      ⚠️  WARNING: {platform} has moderate URL issues")
        else:
            print(f"      ✅ {platform} URLs are mostly valid")

    def analyze_thumbnail_urls(self, platform):
        """Analyze thumbnail URLs for a platform"""
        print(f"\n🖼️  ANALYZING {platform.upper()} THUMBNAIL URLS...")
        
        videos = self.fetch_and_analyze_videos(platform=platform, limit=10)
        
        if not videos:
            print(f"   ❌ No {platform} videos found for thumbnail analysis")
            return
        
        valid_thumbnails = 0
        broken_thumbnails = 0
        svg_thumbnails = 0
        http_thumbnails = 0
        
        for i, video in enumerate(videos[:5]):  # Check first 5
            title = video.get('title', 'No title')[:40]
            thumbnail = video.get('thumbnail', '')
            
            print(f"\n   🖼️  Thumbnail {i+1}: {title}...")
            
            if not thumbnail:
                broken_thumbnails += 1
                print(f"      ❌ Empty thumbnail URL")
                continue
            
            if thumbnail.startswith('data:image/svg+xml'):
                svg_thumbnails += 1
                print(f"      ✅ SVG thumbnail (generated)")
                valid_thumbnails += 1
                
                # Decode SVG content for analysis
                try:
                    from urllib.parse import unquote
                    svg_content = unquote(thumbnail.split(',')[1])
                    if platform.lower() == 'tiktok' and '🎵' in svg_content:
                        print(f"      🎵 Contains TikTok music icon")
                    elif platform.lower() == 'twitter' and '🐦' in svg_content:
                        print(f"      🐦 Contains Twitter bird icon")
                except:
                    print(f"      ⚠️  Could not decode SVG content")
                    
            elif thumbnail.startswith('http'):
                http_thumbnails += 1
                print(f"      ✅ HTTP thumbnail URL")
                valid_thumbnails += 1
                
                # Test accessibility for HTTP thumbnails
                accessibility = self.test_url_accessibility(thumbnail)
                if accessibility["accessible"]:
                    print(f"      ✅ Thumbnail accessible")
                else:
                    print(f"      ❌ Thumbnail not accessible: {accessibility.get('error', 'Unknown')}")
                    
            else:
                broken_thumbnails += 1
                print(f"      ❌ Invalid thumbnail format: {thumbnail[:50]}...")
        
        print(f"\n   📊 {platform.upper()} THUMBNAIL SUMMARY:")
        print(f"      Valid: {valid_thumbnails}/5")
        print(f"      SVG: {svg_thumbnails}/5")
        print(f"      HTTP: {http_thumbnails}/5")
        print(f"      Broken: {broken_thumbnails}/5")

    def test_mock_vs_real_data(self):
        """Identify which platforms are using mock vs real data"""
        print(f"\n🎭 TESTING MOCK VS REAL DATA IDENTIFICATION...")
        
        platforms = ['youtube', 'tiktok', 'twitter']
        
        for platform in platforms:
            print(f"\n   🔍 Analyzing {platform.upper()} data authenticity...")
            
            videos = self.fetch_and_analyze_videos(platform=platform, limit=5)
            
            if not videos:
                print(f"      ❌ No {platform} videos found")
                continue
            
            mock_indicators = 0
            real_indicators = 0
            
            for video in videos:
                url = video.get('url', '')
                title = video.get('title', '')
                thumbnail = video.get('thumbnail', '')
                
                # Check for mock data indicators
                mock_patterns = ['viral', 'test', 'mock', 'sample', 'fake', 'demo']
                if any(pattern in url.lower() for pattern in mock_patterns):
                    mock_indicators += 1
                
                if any(pattern in title.lower() for pattern in mock_patterns):
                    mock_indicators += 1
                
                # Check for real data indicators
                if platform == 'youtube':
                    if 'ytimg.com' in thumbnail or 'youtube.com' in thumbnail:
                        real_indicators += 1
                    if re.match(r'https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}', url):
                        real_indicators += 1
                        
                elif platform == 'twitter':
                    if re.match(r'https://twitter\.com/.+/status/\d{15,}', url):
                        real_indicators += 1
                        
                elif platform == 'tiktok':
                    if re.match(r'https://www\.tiktok\.com/@.+/video/\d{15,}', url):
                        real_indicators += 1
            
            total_videos = len(videos)
            real_confidence = (real_indicators / (total_videos * 2)) * 100  # 2 checks per video
            
            print(f"      📊 Real data confidence: {real_confidence:.1f}%")
            print(f"      🎭 Mock indicators: {mock_indicators}")
            print(f"      ✅ Real indicators: {real_indicators}")
            
            if real_confidence > 70:
                print(f"      ✅ {platform.upper()} appears to use REAL data")
            elif real_confidence > 30:
                print(f"      ⚠️  {platform.upper()} uses MIXED data (real + mock)")
            else:
                print(f"      ❌ {platform.upper()} appears to use MOCK data")

    def comprehensive_url_diagnosis(self):
        """Run comprehensive URL diagnosis"""
        print("=" * 80)
        print("🚨 URGENT: COMPREHENSIVE VIDEO LINKS DIAGNOSIS")
        print("=" * 80)
        
        start_time = time.time()
        
        # Test 1: Analyze all platforms
        print("\n📋 STEP 1: PLATFORM-SPECIFIC URL ANALYSIS")
        platforms = ['youtube', 'tiktok', 'twitter']
        
        for platform in platforms:
            self.analyze_platform_urls(platform)
        
        # Test 2: Thumbnail URL analysis
        print("\n📋 STEP 2: THUMBNAIL URL ANALYSIS")
        for platform in platforms:
            self.analyze_thumbnail_urls(platform)
        
        # Test 3: Mock vs Real data identification
        print("\n📋 STEP 3: MOCK VS REAL DATA ANALYSIS")
        self.test_mock_vs_real_data()
        
        # Test 4: General video aggregation test
        print("\n📋 STEP 4: GENERAL VIDEO AGGREGATION TEST")
        all_videos = self.fetch_and_analyze_videos(limit=30)
        
        if all_videos:
            platform_distribution = {}
            total_broken = 0
            
            for video in all_videos:
                platform = video.get('platform', 'unknown')
                url = video.get('url', '')
                
                if platform not in platform_distribution:
                    platform_distribution[platform] = 0
                platform_distribution[platform] += 1
                
                # Quick URL validation
                if not url or not url.startswith('http'):
                    total_broken += 1
            
            print(f"   📊 Platform Distribution: {platform_distribution}")
            print(f"   ❌ Broken URLs: {total_broken}/{len(all_videos)}")
            
            broken_percentage = (total_broken / len(all_videos)) * 100
            if broken_percentage > 20:
                print(f"   🚨 CRITICAL: {broken_percentage:.1f}% of URLs are broken!")
            elif broken_percentage > 10:
                print(f"   ⚠️  WARNING: {broken_percentage:.1f}% of URLs have issues")
            else:
                print(f"   ✅ URL health is good ({broken_percentage:.1f}% broken)")
        
        # Final Summary
        print("\n" + "=" * 80)
        print("📋 DIAGNOSIS SUMMARY")
        print("=" * 80)
        
        print(f"⏱️  Total diagnosis time: {time.time() - start_time:.2f} seconds")
        print(f"🧪 Tests run: {self.tests_run}")
        print(f"✅ Tests passed: {self.tests_passed}")
        print(f"❌ Tests failed: {self.tests_run - self.tests_passed}")
        
        if self.broken_urls:
            print(f"\n🚨 BROKEN URLS FOUND ({len(self.broken_urls)}):")
            for i, broken in enumerate(self.broken_urls[:10]):  # Show first 10
                print(f"   {i+1}. {broken['platform'].upper()}: {broken['title']}")
                print(f"      URL: {broken['url']}")
                print(f"      Issues: {', '.join(broken['issues'])}")
        else:
            print(f"\n✅ No broken URLs detected in sample")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        if any('youtube' in broken['platform'] for broken in self.broken_urls):
            print("   🎬 YouTube: Check API key validity and video ID generation")
        
        if any('twitter' in broken['platform'] for broken in self.broken_urls):
            print("   🐦 Twitter: Verify tweet ID format and API integration")
        
        if any('tiktok' in broken['platform'] for broken in self.broken_urls):
            print("   📱 TikTok: Check video ID generation and URL construction")
        
        if len(self.broken_urls) > 5:
            print("   🔧 Consider implementing URL validation before returning to frontend")
            print("   🧪 Add automated URL accessibility testing")
            print("   📊 Monitor URL success rates in production")

def main():
    """Main execution function"""
    print("🚀 Starting Video Links Diagnostic Tool...")
    
    diagnostic_tool = VideoLinksDiagnosticTool()
    diagnostic_tool.comprehensive_url_diagnosis()
    
    print("\n🏁 Diagnosis complete!")

if __name__ == "__main__":
    main()