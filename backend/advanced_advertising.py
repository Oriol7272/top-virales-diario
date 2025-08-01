"""
Advanced Advertising Monetization System
High-revenue advertising integrations for Viral Daily
"""

from typing import List, Optional, Dict, Any
import asyncio
import os
import logging
from datetime import datetime, timedelta
import random
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import ViralVideo, Platform, User, SubscriptionTier

logger = logging.getLogger(__name__)

class AdvancedAdvertisingService:
    """Enhanced advertising service for maximum revenue"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.google_adsense_id = os.getenv('GOOGLE_ADSENSE_ID')
        self.video_ad_network = os.getenv('VIDEO_AD_NETWORK_KEY')
        
    async def inject_video_ads(self, videos: List[ViralVideo], user: Optional[User] = None) -> List[Dict[str, Any]]:
        """Inject high-revenue video ads between viral videos"""
        
        # Premium users don't see ads
        if user and user.subscription_tier != SubscriptionTier.FREE:
            return [self._video_to_dict(v) for v in videos]
        
        enhanced_content = []
        ad_frequency = 3  # Show ad every 3 videos
        
        for i, video in enumerate(videos):
            # Add the actual video
            enhanced_content.append(self._video_to_dict(video))
            
            # Inject ad after every 3rd video
            if (i + 1) % ad_frequency == 0 and i < len(videos) - 1:
                ad_content = await self._generate_video_ad(video.platform)
                enhanced_content.append(ad_content)
        
        return enhanced_content
    
    async def _generate_video_ad(self, context_platform: Platform) -> Dict[str, Any]:
        """Generate contextual video advertisement"""
        
        # Get high-performing ad based on platform context
        ad_data = await self._get_contextual_ad(context_platform)
        
        return {
            "type": "advertisement",
            "id": f"ad_{datetime.now().timestamp()}",
            "title": "🎯 Sponsored Content",
            "description": ad_data["description"],
            "thumbnail": ad_data["thumbnail"],
            "click_url": ad_data["click_url"],
            "platform": "advertisement",
            "ad_type": "video_interstitial",
            "revenue_potential": "$0.50-5.00",  # Revenue per click
            "targeting": {
                "context_platform": context_platform.value,
                "content_type": "viral_videos",
                "audience": "entertainment_seekers"
            }
        }
    
    async def _get_contextual_ad(self, platform: Platform) -> Dict[str, Any]:
        """Get contextual ad based on platform and user behavior"""
        
        # Platform-specific high-revenue ad categories
        ad_templates = {
            Platform.YOUTUBE: {
                "description": "🎬 Create Viral Videos with AI - 90% Easier Than Traditional Editing!",
                "thumbnail": self._generate_ad_thumbnail("video_creation", "YouTube-style content creation"),
                "click_url": "https://filmora.wondershare.com/",  # Real Filmora URL
                "category": "content_creation"
            },
            Platform.TIKTOK: {
                "description": "💃 Trending Dance Moves Course - Go Viral in 7 Days!",
                "thumbnail": self._generate_ad_thumbnail("dance_course", "TikTok dance tutorial"),
                "click_url": "https://www.skillshare.com/browse/video",  # Real Skillshare URL
                "category": "skills_training"
            },
            Platform.TWITTER: {
                "description": "📈 Grow Your Following 10x - Social Media Automation Tools",
                "thumbnail": self._generate_ad_thumbnail("social_growth", "Twitter growth analytics"),
                "click_url": "https://hootsuite.com/",  # Real Hootsuite URL
                "category": "marketing_tools"
            }
        }
        
        # Fallback to real working ads
        default_ads = [
            {
                "description": "🎮 Top Viral Mobile Games - Download Free & Play Now!",
                "thumbnail": self._generate_ad_thumbnail("mobile_games", "Popular mobile games"),
                "click_url": "https://play.google.com/store/games",  # Real Google Play
                "category": "gaming"
            },
            {
                "description": "🛍️ Viral Fashion Trends - 50% Off Today Only!",
                "thumbnail": self._generate_ad_thumbnail("fashion", "Trending fashion items"),
                "click_url": "https://www.amazon.com/fashion",  # Real Amazon Fashion
                "category": "shopping"
            },
            {
                "description": "🎧 Unlimited Music Streaming - 3 Months Free Trial!",
                "thumbnail": self._generate_ad_thumbnail("music", "Music streaming service"),
                "click_url": "https://open.spotify.com/",  # Real Spotify
                "category": "entertainment"
            }
        ]
        
        return ad_templates.get(platform, random.choice(default_ads))
    
    def _generate_ad_thumbnail(self, category: str, description: str) -> str:
        """Generate attractive ad thumbnail"""
        from urllib.parse import quote
        
        colors = {
            "video_creation": {"bg": "#FF4444", "accent": "#FF6B6B"},
            "dance_course": {"bg": "#FF3B9A", "accent": "#FF6BB5"}, 
            "social_growth": {"bg": "#1DA1F2", "accent": "#4AB3F2"},
            "mobile_games": {"bg": "#4CAF50", "accent": "#66BB6A"},
            "fashion": {"bg": "#E91E63", "accent": "#F06292"},
            "music": {"bg": "#9C27B0", "accent": "#BA68C8"}
        }
        
        color_scheme = colors.get(category, {"bg": "#FF5722", "accent": "#FF7043"})
        
        svg_content = f'''<svg width="400" height="225" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="225" fill="{color_scheme['bg']}"/>
            <rect x="0" y="0" width="400" height="225" fill="url(#adgrad)" opacity="0.8"/>
            <defs>
                <linearGradient id="adgrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:{color_scheme['accent']};stop-opacity:0.9" />
                    <stop offset="100%" style="stop-color:{color_scheme['bg']};stop-opacity:0.7" />
                </linearGradient>
            </defs>
            <text x="200" y="80" text-anchor="middle" fill="white" font-size="42" font-weight="bold">🎯</text>
            <text x="200" y="115" text-anchor="middle" fill="white" font-size="24" font-weight="bold">SPONSORED</text>
            <text x="200" y="145" text-anchor="middle" fill="white" font-size="18" opacity="0.9">{category.replace('_', ' ').title()}</text>
            <text x="200" y="175" text-anchor="middle" fill="white" font-size="14" opacity="0.8">High Revenue Ad</text>
            <rect x="10" y="195" width="380" height="25" fill="rgba(255,255,255,0.2)" rx="12"/>
            <text x="200" y="212" text-anchor="middle" fill="white" font-size="12" opacity="0.9">Click for More Info</text>
        </svg>'''
        
        return f"data:image/svg+xml;charset=utf-8,{quote(svg_content)}"
    
    def _video_to_dict(self, video: ViralVideo) -> Dict[str, Any]:
        """Convert video object to dictionary"""
        return {
            "type": "video",
            "id": video.id,
            "title": video.title,
            "url": video.url,
            "thumbnail": video.thumbnail,
            "views": video.views,
            "likes": video.likes,
            "platform": video.platform.value,
            "published_at": video.published_at.isoformat() if video.published_at else None,
            "channel_name": video.channel_name,
            "duration": video.duration,
            "viral_score": video.viral_score
        }
    
    async def generate_sponsored_content(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Generate high-revenue sponsored viral content"""
        
        sponsored_content = []
        
        # High-value sponsored content templates with REAL URLs
        sponsors = [
            {
                "title": "🎬 AI Video Generator Goes VIRAL - Creates Hollywood-Quality Videos in Minutes!",
                "description": "This new AI tool is breaking the internet! Content creators are making $10K+ monthly",
                "category": "tech_viral",
                "revenue_per_view": 0.25,
                "click_url": "https://filmora.wondershare.com/"  # Real Filmora URL
            },
            {
                "title": "💰 22-Year-Old Makes $50K/Month with This Viral TikTok Strategy",
                "description": "The secret strategy that TikTok stars don't want you to know about",
                "category": "business_viral", 
                "revenue_per_view": 0.35,
                "click_url": "https://www.skillshare.com/browse/video"  # Real Skillshare URL
            },
            {
                "title": "🔥 This Viral Dance Move is Making People MILLIONS - Learn it in 5 Minutes",
                "description": "Celebrities are paying big money to learn this move. Now you can too!",
                "category": "entertainment_viral",
                "revenue_per_view": 0.20,
                "click_url": "https://www.udemy.com/courses/music/"  # Real Udemy URL
            },
            {
                "title": "🚨 VIRAL: New App Pays $100/Day Just for Scrolling - But There's a Catch",
                "description": "Over 2 million people are using this app, but it might not be available much longer",
                "category": "opportunity_viral",
                "revenue_per_view": 0.45,
                "click_url": "https://play.google.com/store/apps"  # Real Google Play URL
            },
            {
                "title": "🎯 This Viral Marketing Trick Gets 1M Views Guaranteed - Brands Pay $5K to Learn It",
                "description": "The viral marketing secret that made Wendy's famous on social media",
                "category": "marketing_viral",
                "revenue_per_view": 0.30,
                "click_url": "https://hootsuite.com/"  # Real Hootsuite URL
            }
        ]
        
        for i, sponsor in enumerate(sponsors[:limit]):
            content_id = f"sponsor_{datetime.now().timestamp()}_{i}"
            
            sponsored_item = {
                "type": "sponsored_video",
                "id": content_id,
                "title": sponsor["title"],
                "description": sponsor["description"],
                "thumbnail": self._generate_sponsored_thumbnail(sponsor["category"], sponsor["title"]),
                "click_url": sponsor["click_url"],  # Use real URL from sponsor data
                "platform": "sponsored",
                "views": random.randint(100000, 5000000),  # Realistic view counts
                "viral_score": random.randint(75, 95),  # High viral scores
                "revenue_data": {
                    "type": "sponsored_content",
                    "revenue_per_view": sponsor["revenue_per_view"],
                    "estimated_daily_revenue": "$50-500",
                    "advertiser_budget": "premium"
                },
                "targeting": {
                    "audience": "viral_content_consumers",
                    "interests": ["viral_videos", "trending_content", "entertainment"],
                    "age_range": "18-45"
                }
            }
            
            sponsored_content.append(sponsored_item)
        
        return sponsored_content
    
    def _generate_sponsored_thumbnail(self, category: str, title: str) -> str:
        """Generate eye-catching sponsored content thumbnail"""
        from urllib.parse import quote
        
        # Extract key words from title for thumbnail
        key_words = title.split()[:3]
        display_text = " ".join(key_words).replace("🎬", "").replace("💰", "").replace("🔥", "").strip()
        
        svg_content = f'''<svg width="400" height="225" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="225" fill="#000000"/>
            <rect x="0" y="0" width="400" height="225" fill="url(#sponsorgrad)" opacity="0.9"/>
            <defs>
                <linearGradient id="sponsorgrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#ff6b35;stop-opacity:0.8" />
                    <stop offset="50%" style="stop-color:#f7931e;stop-opacity:0.6" />
                    <stop offset="100%" style="stop-color:#ffd23f;stop-opacity:0.8" />
                </linearGradient>
            </defs>
            <text x="200" y="60" text-anchor="middle" fill="white" font-size="36" font-weight="bold">💰</text>
            <text x="200" y="95" text-anchor="middle" fill="white" font-size="20" font-weight="bold">SPONSORED</text>
            <text x="200" y="120" text-anchor="middle" fill="white" font-size="16" opacity="0.9">VIRAL CONTENT</text>
            <rect x="20" y="140" width="360" height="40" fill="rgba(255,255,255,0.1)" rx="8"/>
            <text x="200" y="165" text-anchor="middle" fill="white" font-size="14" font-weight="bold" opacity="0.95">{display_text}</text>
            <text x="200" y="200" text-anchor="middle" fill="white" font-size="12" opacity="0.7">High Revenue Content - Click to View</text>
        </svg>'''
        
        return f"data:image/svg+xml;charset=utf-8,{quote(svg_content)}"
    
    async def track_ad_performance(self, ad_id: str, interaction_type: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Track ad performance for revenue optimization"""
        
        performance_data = {
            "ad_id": ad_id,
            "interaction_type": interaction_type,  # view, click, conversion
            "user_id": user_id,
            "timestamp": datetime.utcnow(),
            "revenue_impact": self._calculate_revenue_impact(interaction_type)
        }
        
        # Store in database for analytics
        await self.db.ad_performance.insert_one(performance_data)
        
        return performance_data
    
    def _calculate_revenue_impact(self, interaction_type: str) -> Dict[str, float]:
        """Calculate revenue impact of different interactions"""
        revenue_rates = {
            "impression": 0.001,  # $0.001 per impression
            "view": 0.01,         # $0.01 per view
            "click": 0.25,        # $0.25 per click
            "conversion": 5.00    # $5.00 per conversion
        }
        
        return {
            "base_revenue": revenue_rates.get(interaction_type, 0),
            "estimated_daily": revenue_rates.get(interaction_type, 0) * 1000,  # Per 1000 interactions
            "monthly_potential": revenue_rates.get(interaction_type, 0) * 30000  # Per month
        }