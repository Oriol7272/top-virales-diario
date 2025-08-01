"""
Premium Content & Features System
Monetize through exclusive content and advanced features
"""

from typing import List, Dict, Any, Optional
import os
import logging
from datetime import datetime, timedelta
import random
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import User, SubscriptionTier, ViralVideo, Platform

logger = logging.getLogger(__name__)

class PremiumContentService:
    """Service for managing premium content and features"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        
    async def generate_premium_content_offers(self, user: Optional[User] = None) -> List[Dict[str, Any]]:
        """Generate premium content and feature offers"""
        
        # Don't show premium offers to existing premium users
        if user and user.subscription_tier in [SubscriptionTier.PRO, SubscriptionTier.BUSINESS]:
            return []
        
        premium_offers = [
            {
                "type": "premium_analytics",
                "title": "🔥 Viral Score Analytics - See What Makes Content Go Viral",
                "description": "Get detailed analytics on viral patterns, trending hashtags, and optimal posting times across all platforms.",
                "features": [
                    "Real-time viral score tracking",
                    "Trending hashtag analysis", 
                    "Optimal posting time recommendations",
                    "Competitor content analysis",
                    "Platform-specific insights"
                ],
                "price": "$19.99/month",
                "savings": "Save $100/year with annual plan",
                "upgrade_url": "/upgrade/analytics",
                "thumbnail": self._generate_premium_thumbnail("analytics", "📊"),
                "revenue_potential": "$20-40/user/month"
            },
            {
                "type": "exclusive_content",
                "title": "⭐ Exclusive Viral Content - Before It Goes Viral",
                "description": "Access viral content 24-48 hours before it hits mainstream. Be the first to know what's trending.",
                "features": [
                    "Early access to trending content",
                    "Exclusive creator interviews",
                    "Behind-the-scenes viral content",
                    "Industry insider reports",
                    "Weekly trend predictions"
                ],
                "price": "$14.99/month", 
                "savings": "First month FREE",
                "upgrade_url": "/upgrade/exclusive",
                "thumbnail": self._generate_premium_thumbnail("exclusive", "🎬"),
                "revenue_potential": "$15-30/user/month"
            },
            {
                "type": "viral_toolkit",
                "title": "🚀 Viral Creator Toolkit - Turn Your Content Viral",
                "description": "Complete suite of tools and templates used by top content creators to create viral content.",
                "features": [
                    "Viral video templates",
                    "Trending audio library",
                    "Hashtag optimization tools",
                    "Content calendar planner",
                    "Cross-platform posting scheduler"
                ],
                "price": "$29.99/month",
                "savings": "60% OFF - Limited Time",
                "upgrade_url": "/upgrade/toolkit",
                "thumbnail": self._generate_premium_thumbnail("toolkit", "⚡"),
                "revenue_potential": "$30-60/user/month"
            },
            {
                "type": "personal_coaching",
                "title": "👨‍🏫 Personal Viral Coaching - 1-on-1 Strategy Sessions",
                "description": "Work directly with viral content experts to develop your personal viral content strategy.",
                "features": [
                    "Weekly 1-on-1 coaching calls",
                    "Personal content strategy development", 
                    "Account review and optimization",
                    "Custom viral content creation",
                    "Priority email support"
                ],
                "price": "$199.99/month",
                "savings": "Money-back guarantee",
                "upgrade_url": "/upgrade/coaching",
                "thumbnail": self._generate_premium_thumbnail("coaching", "🎯"),
                "revenue_potential": "$200-400/user/month"
            },
            {
                "type": "api_access",
                "title": "🔌 Viral Daily API - Integrate Our Data Into Your Apps",
                "description": "Access our viral content database and analytics through a powerful API for your applications.",
                "features": [
                    "Full API access to viral content",
                    "Real-time trend data",
                    "Custom webhooks",
                    "Advanced filtering options",
                    "Developer support"
                ],
                "price": "$99.99/month", 
                "savings": "Start with 1000 free API calls",
                "upgrade_url": "/upgrade/api",
                "thumbnail": self._generate_premium_thumbnail("api", "⚙️"),
                "revenue_potential": "$100-500/user/month"
            },
            {
                "type": "white_label",
                "title": "🏷️ White Label Solution - Your Brand, Our Technology",
                "description": "Launch your own viral content platform with our technology under your brand name.",
                "features": [
                    "Complete white-label platform",
                    "Custom branding and domain",
                    "Revenue sharing program",
                    "Technical support",
                    "Marketing materials"
                ],
                "price": "$999.99/month",
                "savings": "Revenue share opportunities", 
                "upgrade_url": "/upgrade/whitelabel",
                "thumbnail": self._generate_premium_thumbnail("whitelabel", "🏢"),
                "revenue_potential": "$1000-5000/client/month"
            }
        ]
        
        # Personalize offers based on user behavior if available
        if user:
            premium_offers = self._personalize_premium_offers(premium_offers, user)
        
        return premium_offers[:4]  # Show top 4 offers
    
    def _personalize_premium_offers(self, offers: List[Dict[str, Any]], user: User) -> List[Dict[str, Any]]:
        """Personalize premium offers based on user behavior"""
        
        # Simple personalization based on subscription tier
        if user.subscription_tier == SubscriptionTier.FREE:
            # Free users see all offers, prioritize lower-priced ones
            return sorted(offers, key=lambda x: float(x["price"].replace("$", "").split("/")[0]))
        
        return offers
    
    def _generate_premium_thumbnail(self, content_type: str, emoji: str) -> str:
        """Generate premium content thumbnail"""
        from urllib.parse import quote
        
        colors = {
            "analytics": {"bg": "#4285F4", "accent": "#66A3FF"},
            "exclusive": {"bg": "#FF6B35", "accent": "#FF8C55"}, 
            "toolkit": {"bg": "#28A745", "accent": "#4CBB69"},
            "coaching": {"bg": "#6F42C1", "accent": "#8B5FD6"},
            "api": {"bg": "#20C997", "accent": "#44D9B6"},
            "whitelabel": {"bg": "#495057", "accent": "#6C757D"}
        }
        
        color_scheme = colors.get(content_type, {"bg": "#FF5722", "accent": "#FF7043"})
        
        svg_content = f'''<svg width="400" height="225" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="225" fill="{color_scheme['bg']}"/>
            <rect x="0" y="0" width="400" height="225" fill="url(#premgrad)" opacity="0.9"/>
            <defs>
                <linearGradient id="premgrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:{color_scheme['accent']};stop-opacity:0.8" />
                    <stop offset="100%" style="stop-color:{color_scheme['bg']};stop-opacity:0.7" />
                </linearGradient>
            </defs>
            <text x="200" y="70" text-anchor="middle" fill="white" font-size="52" font-weight="bold">{emoji}</text>
            <text x="200" y="105" text-anchor="middle" fill="white" font-size="20" font-weight="bold">PREMIUM</text>
            <text x="200" y="130" text-anchor="middle" fill="white" font-size="16" opacity="0.9">{content_type.replace("_", " ").title()}</text>
            <rect x="30" y="150" width="340" height="30" fill="rgba(255,255,255,0.15)" rx="15"/>
            <text x="200" y="170" text-anchor="middle" fill="white" font-size="14" font-weight="bold">EXCLUSIVE ACCESS</text>
            <text x="200" y="200" text-anchor="middle" fill="white" font-size="12" opacity="0.8">Upgrade to Premium</text>
        </svg>'''
        
        return f"data:image/svg+xml;charset=utf-8,{quote(svg_content)}"
    
    async def track_premium_interest(self, offer_type: str, user_id: Optional[str] = None, action: str = "view") -> Dict[str, Any]:
        """Track user interest in premium content"""
        
        interest_data = {
            "offer_type": offer_type,
            "user_id": user_id,
            "action": action,  # view, click, upgrade
            "timestamp": datetime.utcnow().isoformat(),
            "conversion_value": self._calculate_premium_value(offer_type, action)
        }
        
        try:
            await self.db.premium_interest.insert_one(interest_data.copy())
        except Exception as e:
            logging.error(f"Error storing premium interest: {e}")
        
        return {
            "status": "tracked",
            "offer_type": offer_type,
            "action": action,
            "conversion_value": interest_data["conversion_value"]
        }
    
    def _calculate_premium_value(self, offer_type: str, action: str) -> Dict[str, float]:
        """Calculate premium content value"""
        
        # Monthly revenue potential for each premium offer
        monthly_values = {
            "premium_analytics": 25.00,
            "exclusive_content": 18.00, 
            "viral_toolkit": 35.00,
            "personal_coaching": 250.00,
            "api_access": 120.00,
            "white_label": 1500.00
        }
        
        conversion_rates = {
            "view": 0.02,      # 2% view to upgrade
            "click": 0.15,     # 15% click to upgrade  
            "upgrade": 1.0     # 100% upgrade
        }
        
        base_value = monthly_values.get(offer_type, 25.00)
        conversion_rate = conversion_rates.get(action, 0.02)
        expected_value = base_value * conversion_rate
        
        return {
            "monthly_value": base_value,
            "conversion_rate": conversion_rate,
            "expected_value": expected_value,
            "annual_potential": base_value * 12,
            "ltv": base_value * 18  # 18-month average customer lifetime
        }
    
    async def generate_upsell_campaigns(self, user: User) -> List[Dict[str, Any]]:
        """Generate personalized upsell campaigns"""
        
        campaigns = []
        
        if user.subscription_tier == SubscriptionTier.FREE:
            # Free to Pro upsell
            campaigns.append({
                "type": "tier_upgrade",
                "title": "🚀 Upgrade to Pro - Unlock 3x More Viral Content",
                "description": "Get access to exclusive viral content, advanced analytics, and premium features.",
                "current_plan": "Free",
                "upgrade_to": "Pro",
                "benefits": [
                    "10x more viral videos daily",
                    "Advanced viral score analytics",
                    "Priority customer support",
                    "Ad-free experience",
                    "Early access to new features"
                ],
                "pricing": {
                    "monthly": "$9.99",
                    "yearly": "$99.99",
                    "savings": "Save $20/year"
                },
                "cta": "Upgrade to Pro Now",
                "urgency": "Limited time: 50% OFF first month"
            })
        
        elif user.subscription_tier == SubscriptionTier.PRO:
            # Pro to Business upsell
            campaigns.append({
                "type": "tier_upgrade", 
                "title": "💼 Upgrade to Business - Dominate Your Competition",
                "description": "Get everything in Pro plus API access, white-label options, and business-level analytics.",
                "current_plan": "Pro",
                "upgrade_to": "Business", 
                "benefits": [
                    "Unlimited viral content access",
                    "Full API access for integrations",
                    "Custom branding options",
                    "Advanced business analytics",
                    "Priority phone support",
                    "Revenue sharing opportunities"
                ],
                "pricing": {
                    "monthly": "$29.99",
                    "yearly": "$299.99",
                    "savings": "Save $60/year"
                },
                "cta": "Upgrade to Business",
                "urgency": "Scale your business today"
            })
        
        # Add feature-specific upsells
        campaigns.extend([
            {
                "type": "feature_addon",
                "title": "🔥 Viral Prediction Engine - Know What Goes Viral Before It Does",
                "description": "AI-powered predictions of viral content 24-48 hours before it explodes.",
                "addon_price": "$14.99/month",
                "benefits": [
                    "AI viral predictions",
                    "Trend forecasting",
                    "Competitive intelligence",
                    "Early trend alerts"
                ],
                "trial": "7-day free trial",
                "cta": "Start Free Trial"
            },
            {
                "type": "coaching_addon",
                "title": "👨‍💼 Personal Viral Strategist - Your Success Coach",
                "description": "Work 1-on-1 with viral content experts to maximize your content performance.",
                "addon_price": "$99.99/month",
                "benefits": [
                    "Monthly strategy calls",
                    "Content review & optimization",
                    "Personal growth plans",
                    "Direct expert access"
                ],
                "guarantee": "30-day money-back guarantee",
                "cta": "Book Strategy Session"
            }
        ])
        
        return campaigns
    
    async def get_premium_revenue_report(self) -> Dict[str, Any]:
        """Generate premium content revenue report"""
        
        # Get recent interest data
        recent_interest = await self.db.premium_interest.find({
            "timestamp": {"$gte": datetime.utcnow() - timedelta(days=30)}
        }).to_list(length=None)
        
        # Calculate metrics
        total_views = len([r for r in recent_interest if r["action"] == "view"])
        total_clicks = len([r for r in recent_interest if r["action"] == "click"])
        total_upgrades = len([r for r in recent_interest if r["action"] == "upgrade"])
        
        total_revenue = sum(r["conversion_value"]["expected_value"] for r in recent_interest)
        
        # Analyze by offer type
        offer_performance = {}
        for record in recent_interest:
            offer_type = record["offer_type"]
            if offer_type not in offer_performance:
                offer_performance[offer_type] = {
                    "views": 0,
                    "clicks": 0,
                    "upgrades": 0,
                    "revenue": 0
                }
            
            offer_performance[offer_type][record["action"] + "s"] = offer_performance[offer_type].get(record["action"] + "s", 0) + 1
            offer_performance[offer_type]["revenue"] += record["conversion_value"]["expected_value"]
        
        return {
            "period": "last_30_days",
            "overview": {
                "total_views": total_views,
                "total_clicks": total_clicks, 
                "total_upgrades": total_upgrades,
                "total_revenue": f"${total_revenue:.2f}",
                "click_through_rate": f"{(total_clicks/max(total_views, 1)*100):.1f}%",
                "conversion_rate": f"{(total_upgrades/max(total_clicks, 1)*100):.1f}%"
            },
            "offer_performance": offer_performance,
            "projections": {
                "monthly_revenue": f"${total_revenue:.2f}",
                "annual_revenue": f"${total_revenue * 12:.2f}",
                "growth_potential": f"${total_revenue * 2:.2f}"  # With optimization
            },
            "top_offers": [
                "Personal Coaching ($250/month/user)",
                "White Label Solution ($1500/month/client)",
                "API Access ($120/month/developer)",
                "Viral Toolkit ($35/month/creator)"
            ],
            "recommendations": [
                "💡 Focus on high-value offers (Coaching, White Label)",
                "🎯 A/B test premium offer positioning", 
                "📊 Add more analytics features for Pro users",
                "🚀 Create tiered API pricing for developers"
            ]
        }