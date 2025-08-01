"""
Affiliate Marketing System for Viral Daily
Generate revenue through strategic affiliate partnerships
"""

from typing import List, Dict, Any, Optional
import os
import logging
from datetime import datetime, timedelta
import random
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import User, SubscriptionTier, ViralVideo, Platform

logger = logging.getLogger(__name__)

class AffiliateMarketingService:
    """Service for managing affiliate marketing campaigns"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        
    async def generate_contextual_affiliate_offers(self, videos: List[ViralVideo], user: Optional[User] = None) -> List[Dict[str, Any]]:
        """Generate contextual affiliate offers based on viral content"""
        
        affiliate_offers = []
        
        # High-converting affiliate categories for viral content audience
        affiliate_programs = [
            {
                "category": "content_creation_tools",
                "offers": [
                    {
                        "title": "🎬 Create Viral Videos with Filmora - 50% OFF",
                        "description": "Professional video editing made easy. Used by millions of content creators worldwide.",
                        "commission": "40%",  # $20-60 per sale
                        "price": "$49.99",
                        "affiliate_link": "https://viral-daily.com/aff/filmora",
                        "conversion_rate": "8%",
                        "avg_earnings": "$35/sale"
                    },
                    {
                        "title": "📱 Canva Pro - Design Like a Pro (30-Day Free Trial)",
                        "description": "Create stunning graphics, videos, and social media content. Perfect for viral content.",
                        "commission": "30%", 
                        "price": "$14.99/month",
                        "affiliate_link": "https://viral-daily.com/aff/canva-pro",
                        "conversion_rate": "12%",
                        "avg_earnings": "$5/signup"
                    }
                ]
            },
            {
                "category": "social_media_growth",
                "offers": [
                    {
                        "title": "🚀 Hootsuite - Manage All Your Social Media (Free Trial)",
                        "description": "Schedule posts, track performance, and grow your following across all platforms.",
                        "commission": "50%",
                        "price": "$99/month", 
                        "affiliate_link": "https://viral-daily.com/aff/hootsuite",
                        "conversion_rate": "6%",
                        "avg_earnings": "$50/sale"
                    },
                    {
                        "title": "📈 Later - Visual Social Media Scheduler (FREE Plan Available)",
                        "description": "Plan, schedule, and analyze your social media content for maximum viral potential.",
                        "commission": "35%",
                        "price": "$25/month",
                        "affiliate_link": "https://viral-daily.com/aff/later",
                        "conversion_rate": "10%",
                        "avg_earnings": "$8/signup"
                    }
                ]
            },
            {
                "category": "online_education",
                "offers": [
                    {
                        "title": "🎓 MasterClass - Learn from the Best (50% OFF Annual)",
                        "description": "Learn viral content creation from industry experts and celebrities.",
                        "commission": "25%",
                        "price": "$180/year",
                        "affiliate_link": "https://viral-daily.com/aff/masterclass",
                        "conversion_rate": "7%",
                        "avg_earnings": "$45/sale"
                    },
                    {
                        "title": "💡 Skillshare - Unlimited Creative Classes (2 Months FREE)",
                        "description": "Learn video editing, social media marketing, and content creation skills.",
                        "commission": "40%",
                        "price": "$168/year",
                        "affiliate_link": "https://viral-daily.com/aff/skillshare",
                        "conversion_rate": "9%",
                        "avg_earnings": "$25/signup"
                    }
                ]
            },
            {
                "category": "tech_gadgets",
                "offers": [
                    {
                        "title": "🎤 Blue Yeti Microphone - Professional Audio for Content Creators",
                        "description": "The #1 choice for YouTubers, podcasters, and content creators worldwide.",
                        "commission": "4%",
                        "price": "$99.99",
                        "affiliate_link": "https://viral-daily.com/aff/amazon-blue-yeti",
                        "conversion_rate": "5%",
                        "avg_earnings": "$4/sale"
                    },
                    {
                        "title": "💡 Ring Light Kit - Professional Lighting for Videos",
                        "description": "Create professional-looking videos with perfect lighting. Essential for viral content.",
                        "commission": "8%",
                        "price": "$79.99",
                        "affiliate_link": "https://viral-daily.com/aff/amazon-ring-light",
                        "conversion_rate": "7%",
                        "avg_earnings": "$6/sale"
                    }
                ]
            }
        ]
        
        # Select offers based on video content and platform
        for video in videos[:3]:  # Top 3 videos for context
            platform_category = self._get_platform_category(video.platform)
            relevant_programs = self._filter_programs_by_platform(affiliate_programs, platform_category)
            
            for program in relevant_programs[:2]:  # Top 2 most relevant
                for offer in program["offers"][:1]:  # Best offer from each program
                    affiliate_offer = {
                        "type": "affiliate_offer",
                        "id": f"aff_{datetime.now().timestamp()}_{random.randint(1000, 9999)}",
                        "title": offer["title"],
                        "description": offer["description"],
                        "thumbnail": self._generate_affiliate_thumbnail(program["category"], offer["title"]),
                        "affiliate_link": offer["affiliate_link"],
                        "commission": offer["commission"],
                        "price": offer["price"],
                        "conversion_rate": offer["conversion_rate"],
                        "avg_earnings": offer["avg_earnings"],
                        "context_platform": video.platform.value,
                        "context_video": video.title[:50],
                        "revenue_potential": "High",
                        "targeting": {
                            "audience": "viral_content_creators",
                            "interests": ["content_creation", "social_media", "video_editing"],
                            "platforms": [video.platform.value]
                        }
                    }
                    
                    affiliate_offers.append(affiliate_offer)
        
        # Remove duplicates and limit to top offers
        unique_offers = []
        seen_titles = set()
        
        for offer in affiliate_offers:
            if offer["title"] not in seen_titles:
                unique_offers.append(offer)
                seen_titles.add(offer["title"])
                
                if len(unique_offers) >= 6:  # Limit to 6 offers
                    break
        
        return unique_offers
    
    def _get_platform_category(self, platform: Platform) -> str:
        """Get affiliate category based on platform"""
        mapping = {
            Platform.YOUTUBE: "content_creation_tools",
            Platform.TIKTOK: "social_media_growth", 
            Platform.TWITTER: "social_media_growth"
        }
        return mapping.get(platform, "content_creation_tools")
    
    def _filter_programs_by_platform(self, programs: List[Dict], category: str) -> List[Dict]:
        """Filter affiliate programs by category"""
        return [p for p in programs if p["category"] == category]
    
    def _generate_affiliate_thumbnail(self, category: str, title: str) -> str:
        """Generate affiliate offer thumbnail"""
        from urllib.parse import quote
        
        colors = {
            "content_creation_tools": {"bg": "#FF6B35", "accent": "#FFA500"},
            "social_media_growth": {"bg": "#1DA1F2", "accent": "#4AB3F2"},
            "online_education": {"bg": "#28A745", "accent": "#5CBF2A"},
            "tech_gadgets": {"bg": "#6F42C1", "accent": "#8B5CF6"}
        }
        
        color_scheme = colors.get(category, {"bg": "#FF5722", "accent": "#FF7043"})
        
        # Extract emoji and first few words
        title_parts = title.split()
        emoji = title_parts[0] if title_parts[0].startswith(('🎬', '📱', '🚀', '🎓', '💡', '🎤')) else '💰'
        short_title = ' '.join(title_parts[1:4]) if len(title_parts) > 1 else 'Affiliate Offer'
        
        svg_content = f'''<svg width="400" height="225" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="225" fill="{color_scheme['bg']}"/>
            <rect x="0" y="0" width="400" height="225" fill="url(#affgrad)" opacity="0.9"/>
            <defs>
                <linearGradient id="affgrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:{color_scheme['accent']};stop-opacity:0.8" />
                    <stop offset="100%" style="stop-color:{color_scheme['bg']};stop-opacity:0.7" />
                </linearGradient>
            </defs>
            <text x="200" y="70" text-anchor="middle" fill="white" font-size="48" font-weight="bold">{emoji}</text>
            <text x="200" y="105" text-anchor="middle" fill="white" font-size="18" font-weight="bold">AFFILIATE OFFER</text>
            <rect x="20" y="120" width="360" height="40" fill="rgba(255,255,255,0.1)" rx="8"/>
            <text x="200" y="145" text-anchor="middle" fill="white" font-size="14" font-weight="bold" opacity="0.95">{short_title}</text>
            <text x="200" y="175" text-anchor="middle" fill="white" font-size="16" font-weight="bold">HIGH COMMISSION</text>
            <text x="200" y="200" text-anchor="middle" fill="white" font-size="12" opacity="0.8">Click to Earn Revenue</text>
        </svg>'''
        
        return f"data:image/svg+xml;charset=utf-8,{quote(svg_content)}"
    
    async def track_affiliate_performance(self, affiliate_id: str, action: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Track affiliate marketing performance"""
        
        performance_data = {
            "affiliate_id": affiliate_id,
            "action": action,  # view, click, conversion
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "estimated_earnings": self._calculate_affiliate_earnings(action)
        }
        
        try:
            await self.db.affiliate_performance.insert_one(performance_data.copy())
        except Exception as e:
            logging.error(f"Error storing affiliate performance: {e}")
        
        return {
            "status": "tracked",
            "affiliate_id": affiliate_id,
            "action": action,
            "estimated_earnings": performance_data["estimated_earnings"]
        }
    
    def _calculate_affiliate_earnings(self, action: str) -> Dict[str, float]:
        """Calculate estimated affiliate earnings"""
        
        earnings = {
            "view": 0.01,        # $0.01 per view (brand awareness)
            "click": 0.50,       # $0.50 per click (traffic value)
            "conversion": 25.00  # $25 average per conversion
        }
        
        base_earning = earnings.get(action, 0)
        
        return {
            "base_earning": base_earning,
            "daily_potential": base_earning * 100,    # Per 100 actions
            "monthly_potential": base_earning * 3000   # Scaled monthly
        }
    
    async def get_top_performing_offers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performing affiliate offers"""
        
        # Get recent performance data
        recent_performance = await self.db.affiliate_performance.find({
            "timestamp": {"$gte": datetime.utcnow() - timedelta(days=30)}
        }).to_list(length=None)
        
        # Aggregate by affiliate_id
        offer_stats = {}
        for record in recent_performance:
            affiliate_id = record["affiliate_id"]
            action = record["action"]
            earning = record["estimated_earnings"]["base_earning"]
            
            if affiliate_id not in offer_stats:
                offer_stats[affiliate_id] = {
                    "views": 0,
                    "clicks": 0, 
                    "conversions": 0,
                    "total_earnings": 0,
                    "ctr": 0,
                    "conversion_rate": 0
                }
            
            if action == "view":
                offer_stats[affiliate_id]["views"] += 1
            elif action == "click":
                offer_stats[affiliate_id]["clicks"] += 1
            elif action == "conversion":
                offer_stats[affiliate_id]["conversions"] += 1
            
            offer_stats[affiliate_id]["total_earnings"] += earning
        
        # Calculate performance metrics
        for affiliate_id in offer_stats:
            stats = offer_stats[affiliate_id]
            if stats["views"] > 0:
                stats["ctr"] = (stats["clicks"] / stats["views"]) * 100
            if stats["clicks"] > 0:
                stats["conversion_rate"] = (stats["conversions"] / stats["clicks"]) * 100
        
        # Sort by total earnings
        top_offers = sorted(offer_stats.items(), key=lambda x: x[1]["total_earnings"], reverse=True)
        
        return [
            {
                "affiliate_id": offer_id,
                "performance": stats,
                "ranking": i + 1
            }
            for i, (offer_id, stats) in enumerate(top_offers[:limit])
        ]