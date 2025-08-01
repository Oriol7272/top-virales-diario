#!/usr/bin/env python3
"""
Comprehensive Monetization System Testing
Focus on Google AdSense, Affiliate Marketing, Premium Content, Brand Partnerships, Analytics
"""

import requests
import json
import sys
from datetime import datetime

class MonetizationTester:
    def __init__(self):
        # Get backend URL from frontend/.env
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
        self.tests_run = 0
        self.tests_passed = 0
        
    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=15)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=15)
            
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
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}
    
    def test_google_adsense_integration(self):
        """Test Google AdSense Integration endpoints"""
        print("\n" + "="*60)
        print("🎯 GOOGLE ADSENSE INTEGRATION TESTING")
        print("="*60)
        
        # Test AdSense setup endpoint
        success, response = self.run_test(
            "Google AdSense Setup",
            "GET",
            "monetization/adsense/setup",
            200
        )
        
        if success and isinstance(response, dict):
            print(f"   AdSense Setup Response Keys: {list(response.keys())}")
            
            # Check for ad units
            ad_units = response.get('ad_units', [])
            if ad_units:
                print(f"   ✅ Generated {len(ad_units)} ad units")
                for i, unit in enumerate(ad_units[:3]):  # Show first 3
                    print(f"      Unit {i+1}: {unit.get('type', 'Unknown')} - {unit.get('slot_id', 'No ID')}")
            
            # Check revenue projections
            revenue = response.get('revenue_projection', {})
            if revenue:
                monthly_min = revenue.get('monthly_min', 0)
                monthly_max = revenue.get('monthly_max', 0)
                print(f"   💰 Revenue Projection: ${monthly_min}-${monthly_max}/month")
                
                # Check if meets target ($500-2000/month)
                if monthly_min >= 500 and monthly_max <= 2000:
                    print("   ✅ Revenue projection meets target range!")
                else:
                    print(f"   ⚠️  Revenue projection outside target range ($500-2000)")
            
            return True
        return False
    
    def test_affiliate_marketing_system(self):
        """Test Affiliate Marketing System"""
        print("\n" + "="*60)
        print("🤝 AFFILIATE MARKETING SYSTEM TESTING")
        print("="*60)
        
        # Test affiliate offers endpoint
        success, response = self.run_test(
            "Affiliate Marketing Offers",
            "GET",
            "monetization/affiliate/offers",
            200
        )
        
        if success and isinstance(response, dict):
            print(f"   Affiliate Response Keys: {list(response.keys())}")
            
            # Check offers
            offers = response.get('offers', [])
            if offers:
                print(f"   ✅ Generated {len(offers)} affiliate offers")
                for i, offer in enumerate(offers[:3]):  # Show first 3
                    title = offer.get('title', 'Unknown')
                    commission = offer.get('commission_rate', 0)
                    print(f"      Offer {i+1}: {title} - {commission}% commission")
            
            # Check revenue potential
            revenue = response.get('revenue_potential', {})
            if revenue:
                monthly_estimate = revenue.get('monthly_estimate', 0)
                print(f"   💰 Monthly Revenue Estimate: ${monthly_estimate}")
                
                # Check if meets target ($3000-15000/month)
                if monthly_estimate >= 3000:
                    print("   ✅ Revenue estimate meets minimum target!")
                else:
                    print(f"   ⚠️  Revenue estimate below target ($3000+ needed)")
            
            return True
        return False
    
    def test_premium_content_system(self):
        """Test Premium Content & Features System"""
        print("\n" + "="*60)
        print("⭐ PREMIUM CONTENT SYSTEM TESTING")
        print("="*60)
        
        # Test premium content endpoint
        success, response = self.run_test(
            "Premium Content Offers",
            "GET",
            "monetization/premium/content",
            200
        )
        
        if success and isinstance(response, dict):
            print(f"   Premium Content Response Keys: {list(response.keys())}")
            
            # Check premium offers
            offers = response.get('premium_offers', [])
            if offers:
                print(f"   ✅ Generated {len(offers)} premium offers")
                for i, offer in enumerate(offers[:3]):  # Show first 3
                    title = offer.get('title', 'Unknown')
                    price = offer.get('monthly_price', 0)
                    print(f"      Offer {i+1}: {title} - ${price}/month")
            
            # Check upsell campaigns
            upsells = response.get('upsell_campaigns', [])
            if upsells:
                print(f"   ✅ Generated {len(upsells)} upsell campaigns")
            
            # Check revenue potential
            revenue = response.get('revenue_potential', {})
            if revenue:
                monthly_min = revenue.get('monthly_min', 0)
                monthly_max = revenue.get('monthly_max', 0)
                print(f"   💰 Revenue Potential: ${monthly_min}-${monthly_max}/month")
                
                # Check if meets target ($2000-10000/month)
                if monthly_min >= 2000 and monthly_max <= 10000:
                    print("   ✅ Revenue potential meets target range!")
                else:
                    print(f"   ⚠️  Revenue potential outside target range ($2000-10000)")
            
            return True
        return False
    
    def test_brand_partnerships_system(self):
        """Test Brand Partnership Opportunities"""
        print("\n" + "="*60)
        print("🏢 BRAND PARTNERSHIPS SYSTEM TESTING")
        print("="*60)
        
        # Test brand partnerships endpoint (requires Business tier)
        success, response = self.run_test(
            "Brand Partnership Opportunities",
            "GET",
            "monetization/partnerships/opportunities",
            200
        )
        
        if success and isinstance(response, dict):
            print(f"   Brand Partnerships Response Keys: {list(response.keys())}")
            
            # Check partnership opportunities
            opportunities = response.get('opportunities', [])
            if opportunities:
                print(f"   ✅ Generated {len(opportunities)} partnership opportunities")
                for i, opp in enumerate(opportunities[:3]):  # Show first 3
                    company = opp.get('company_type', 'Unknown')
                    revenue_min = opp.get('revenue_potential', {}).get('monthly_min', 0)
                    revenue_max = opp.get('revenue_potential', {}).get('monthly_max', 0)
                    print(f"      Partnership {i+1}: {company} - ${revenue_min}-${revenue_max}/month")
            
            # Check if any partnerships meet high-value target ($10,000-50,000/month)
            high_value_partnerships = []
            for opp in opportunities:
                revenue = opp.get('revenue_potential', {})
                if revenue.get('monthly_max', 0) >= 10000:
                    high_value_partnerships.append(opp)
            
            if high_value_partnerships:
                print(f"   ✅ Found {len(high_value_partnerships)} high-value partnerships ($10K+/month)")
            else:
                print("   ⚠️  No high-value partnerships found")
            
            return True
        else:
            # May require Business tier access
            print("   ℹ️  Brand partnerships may require Business tier subscription")
            return True  # Not a failure, just access control
    
    def test_interaction_tracking_system(self):
        """Test Interaction Tracking for monetization"""
        print("\n" + "="*60)
        print("📊 INTERACTION TRACKING SYSTEM TESTING")
        print("="*60)
        
        # Test interaction tracking endpoint
        success, response = self.run_test(
            "Monetization Interaction Tracking",
            "POST",
            "monetization/track-interaction",
            200,
            data={
                "interaction_type": "ad_impression",
                "monetization_channel": "adsense",
                "user_tier": "free",
                "revenue_impact": 0.001
            }
        )
        
        if success and isinstance(response, dict):
            print(f"   Interaction Tracking Response Keys: {list(response.keys())}")
            
            # Check tracking confirmation
            if response.get('status') == 'success':
                print("   ✅ Interaction tracking working")
                
                # Check revenue attribution
                revenue_impact = response.get('revenue_impact', 0)
                if revenue_impact > 0:
                    print(f"   💰 Revenue impact tracked: ${revenue_impact}")
                
                return True
            else:
                print("   ⚠️  Interaction tracking response unclear")
                return False
        return False
    
    def test_comprehensive_analytics_system(self):
        """Test Comprehensive Analytics & Reporting"""
        print("\n" + "="*60)
        print("📈 COMPREHENSIVE ANALYTICS SYSTEM TESTING")
        print("="*60)
        
        # Test comprehensive analytics endpoint (requires Business tier)
        success, response = self.run_test(
            "Comprehensive Analytics Report",
            "GET",
            "monetization/analytics/comprehensive",
            200
        )
        
        if success and isinstance(response, dict):
            print(f"   Analytics Response Keys: {list(response.keys())}")
            
            # Check revenue streams analysis
            revenue_streams = response.get('revenue_streams', {})
            if revenue_streams:
                print("   ✅ Revenue streams analysis available:")
                for stream, data in revenue_streams.items():
                    if isinstance(data, dict) and 'monthly_revenue' in data:
                        monthly = data['monthly_revenue']
                        print(f"      {stream.title()}: ${monthly}/month")
            
            # Check total revenue potential
            total_revenue = response.get('total_revenue_potential', {})
            if total_revenue:
                monthly_total = total_revenue.get('monthly', 0)
                annual_total = total_revenue.get('annual', 0)
                print(f"   💰 Total Revenue Potential: ${monthly_total}/month, ${annual_total}/year")
                
                # Check if meets overall target ($15,000-75,000+/month)
                if monthly_total >= 15000:
                    print("   ✅ Total revenue potential meets target!")
                else:
                    print(f"   ⚠️  Total revenue below target ($15,000+/month needed)")
            
            return True
        else:
            # May require Business tier access
            print("   ℹ️  Comprehensive analytics may require Business tier subscription")
            return True  # Not a failure, just access control
    
    def test_revenue_optimization_system(self):
        """Test Revenue Optimization & Projections"""
        print("\n" + "="*60)
        print("💰 REVENUE OPTIMIZATION SYSTEM TESTING")
        print("="*60)
        
        # Test revenue optimization endpoint
        success, response = self.run_test(
            "Revenue Optimization Analysis",
            "GET",
            "monetization/optimization/analysis",
            200
        )
        
        if success and isinstance(response, dict):
            print(f"   Revenue Optimization Response Keys: {list(response.keys())}")
            
            # Check optimization recommendations
            recommendations = response.get('optimization_recommendations', [])
            if recommendations:
                print(f"   ✅ Generated {len(recommendations)} optimization recommendations")
                for i, rec in enumerate(recommendations[:3]):  # Show first 3
                    title = rec.get('title', 'Unknown')
                    impact = rec.get('revenue_impact', 'Unknown')
                    print(f"      Recommendation {i+1}: {title} - Impact: {impact}")
            
            # Check performance metrics
            performance = response.get('performance_metrics', {})
            if performance:
                print("   📊 Performance metrics available:")
                for metric, value in performance.items():
                    print(f"      {metric}: {value}")
            
            return True
        return False
    
    def test_api_key_authentication_tiers(self):
        """Test API Key Authentication for different tiers"""
        print("\n" + "="*60)
        print("🔐 API KEY AUTHENTICATION TESTING")
        print("="*60)
        
        # Test API access without key (should work for basic endpoints)
        success, response = self.run_test(
            "API Access Without Key",
            "GET",
            "videos",
            200,
            params={'limit': 5}
        )
        
        if success and isinstance(response, dict):
            user_tier = response.get('user_tier', 'unknown')
            has_ads = response.get('has_ads', False)
            videos = response.get('videos', [])
            
            print(f"   User Tier: {user_tier}")
            print(f"   Has Ads: {has_ads}")
            print(f"   Videos Returned: {len(videos)}")
            
            # Check free tier characteristics
            if user_tier == 'free' and has_ads:
                print("   ✅ Free tier access control working")
            else:
                print("   ⚠️  Free tier access control may have issues")
            
            return True
        return False
    
    def test_video_count_limits_by_tier(self):
        """Test video count limits by subscription tier"""
        print("\n" + "="*60)
        print("📹 VIDEO COUNT LIMITS BY TIER TESTING")
        print("="*60)
        
        # Test free tier limit (should be 40 videos)
        success, response = self.run_test(
            "Free Tier Video Limit Test",
            "GET",
            "videos",
            200,
            params={'limit': 50}  # Request more than free tier limit
        )
        
        if success and isinstance(response, dict):
            videos = response.get('videos', [])
            user_tier = response.get('user_tier', 'unknown')
            
            print(f"   User Tier: {user_tier}")
            print(f"   Videos Returned: {len(videos)}")
            
            # Check if free tier limit is enforced (should be around 40)
            if user_tier == 'free':
                if len(videos) <= 40:
                    print(f"   ✅ Free tier limit enforced (≤40 videos)")
                else:
                    print(f"   ⚠️  Free tier limit may not be enforced ({len(videos)} > 40)")
            
            return True
        return False
    
    def run_all_monetization_tests(self):
        """Run all monetization system tests"""
        print("🚀 STARTING COMPREHENSIVE MONETIZATION SYSTEM TESTING")
        print("="*80)
        print(f"Testing against: {self.base_url}")
        print("Focus: Google AdSense, PayPal, Premium Content, Brand Partnerships, Analytics")
        print("="*80)
        
        # Run all monetization tests
        tests = [
            self.test_google_adsense_integration,
            self.test_affiliate_marketing_system,
            self.test_premium_content_system,
            self.test_brand_partnerships_system,
            self.test_interaction_tracking_system,
            self.test_comprehensive_analytics_system,
            self.test_revenue_optimization_system,
            self.test_api_key_authentication_tiers,
            self.test_video_count_limits_by_tier
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with error: {e}")
        
        # Final summary
        print("\n" + "="*80)
        print("🏁 MONETIZATION SYSTEM TESTING COMPLETE")
        print("="*80)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        print("="*80)
        
        return self.tests_passed, self.tests_run

if __name__ == "__main__":
    tester = MonetizationTester()
    passed, total = tester.run_all_monetization_tests()
    
    # Exit with appropriate code
    if passed == total:
        sys.exit(0)  # All tests passed
    else:
        sys.exit(1)  # Some tests failed