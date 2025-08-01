#!/usr/bin/env python3
"""
Enhanced Viral Daily Server - All Features, Minimal Dependencies
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional
import random
import uuid

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Environment setup
os.environ.setdefault('MONGO_URL', 'mongodb+srv://rail:P2aqBClf1CfSV2jy@cluster0.2saqg1m.mongodb.net/viral_daily?ssl=true&ssl_cert_reqs=CERT_NONE')
os.environ.setdefault('DB_NAME', 'viral_daily')

# Initialize FastAPI
app = FastAPI(
    title="Viral Daily API",
    version="2.0.0",
    description="Complete Viral Video Aggregation Platform"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)

# Database connection (optional for mock data operation)
mongo_client = None
database = None

# MongoDB connection disabled for now - running in mock data mode only
print("📝 MongoDB connection disabled - running with mock data only")

# Models
class VideoModel(BaseModel):
    id: str
    title: str
    url: str
    platform: str
    thumbnail: str
    views: int
    likes: int
    author: str
    duration: str
    viral_score: float
    published_at: str

class SubscriptionPlan(BaseModel):
    id: str
    name: str
    price: float
    features: List[str]
    video_limit: int
    api_access: bool

class User(BaseModel):
    id: str
    email: str
    subscription_tier: str
    created_at: str

# Enhanced video data with all platforms
def get_enhanced_video_data():
    """Enhanced video data with real URLs and varied content"""
    
    youtube_videos = [
        {
            "id": "yt-1",
            "title": "Rick Astley - Never Gonna Give You Up (Official Video)",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "platform": "youtube",
            "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
            "views": 1400000000,
            "likes": 15000000,
            "author": "Rick Astley",
            "duration": "3:33"
        },
        {
            "id": "yt-2", 
            "title": "PSY - GANGNAM STYLE(강남스타일) M/V",
            "url": "https://www.youtube.com/watch?v=9bZkp7q19f0",
            "platform": "youtube",
            "thumbnail": "https://i.ytimg.com/vi/9bZkp7q19f0/hqdefault.jpg",
            "views": 4900000000,
            "likes": 24000000,
            "author": "officialpsy",
            "duration": "4:13"
        },
        {
            "id": "yt-3",
            "title": "Luis Fonsi - Despacito ft. Daddy Yankee",
            "url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
            "platform": "youtube",
            "thumbnail": "https://i.ytimg.com/vi/kJQP7kiw5Fk/hqdefault.jpg",
            "views": 8200000000,
            "likes": 48000000,
            "author": "LuisFonsiVEVO",
            "duration": "4:42"
        },
        {
            "id": "yt-4",
            "title": "Ed Sheeran - Shape of You (Official Video)",
            "url": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
            "platform": "youtube",
            "thumbnail": "https://i.ytimg.com/vi/JGwWNGJdvx8/hqdefault.jpg",
            "views": 5700000000,
            "likes": 32000000,
            "author": "Ed Sheeran",
            "duration": "3:54"
        },
        {
            "id": "yt-5",
            "title": "Baby Shark Dance | #babyshark Most Viewed Video on YouTube",
            "url": "https://www.youtube.com/watch?v=XqZsoesa55w",
            "platform": "youtube",
            "thumbnail": "https://i.ytimg.com/vi/XqZsoesa55w/hqdefault.jpg",
            "views": 14000000000,
            "likes": 51000000,
            "author": "Pinkfong! Kids' Songs & Stories",
            "duration": "2:17"
        },
        {
            "id": "yt-6",
            "title": "Charlie Bit My Finger - again !",
            "url": "https://www.youtube.com/watch?v=_OBlgSz8sSM",
            "platform": "youtube",
            "thumbnail": "https://i.ytimg.com/vi/_OBlgSz8sSM/hqdefault.jpg",
            "views": 885000000,
            "likes": 3200000,
            "author": "HDCYT",
            "duration": "0:56"
        }
    ]
    
    tiktok_videos = [
        {
            "id": "tt-1",
            "title": "This transition hit different 🔥",
            "url": "https://www.tiktok.com/@khaby.lame/video/7349850239266458672",
            "platform": "tiktok",
            "thumbnail": "https://p16-sign-va.tiktokcdn.com/obj/tos-maliva-p-0068/oQgAJKJ8IrK7rJqg5gLAJKKgAKkgA?x-expires=1735948800&x-signature=example",
            "views": 47300000,
            "likes": 8900000,
            "author": "@khaby.lame",
            "duration": "0:15"
        },
        {
            "id": "tt-2",
            "title": "Teaching my mom this dance 💃",
            "url": "https://www.tiktok.com/@charlidamelio/video/7340123456789012345",
            "platform": "tiktok",
            "thumbnail": "https://p16-sign-va.tiktokcdn.com/obj/tos-maliva-p-0068/charli_thumbnail?x-expires=1735948800&x-signature=example2",
            "views": 35800000,
            "likes": 6700000,
            "author": "@charlidamelio",
            "duration": "0:30"
        },
        {
            "id": "tt-3",
            "title": "POV: When your bestie finds the perfect outfit 💯",
            "url": "https://www.tiktok.com/@addisonre/video/7341234567890123456",
            "platform": "tiktok",
            "thumbnail": "https://p16-sign-va.tiktokcdn.com/obj/tos-maliva-p-0068/addison_outfit?x-expires=1735948800&x-signature=example3",
            "views": 28900000,
            "likes": 5200000,
            "author": "@addisonre",
            "duration": "0:22"
        },
        {
            "id": "tt-4",
            "title": "When the beat drops and you can't help but move 🎵",
            "url": "https://www.tiktok.com/@bellapoarch/video/7342345678901234567",
            "platform": "tiktok",
            "thumbnail": "https://p16-sign-va.tiktokcdn.com/obj/tos-maliva-p-0068/bella_dance?x-expires=1735948800&x-signature=example4",
            "views": 62100000,
            "likes": 11300000,
            "author": "@bellapoarch",
            "duration": "0:18"
        },
        {
            "id": "tt-5",
            "title": "This life hack will change everything! 🤯",
            "url": "https://www.tiktok.com/@zacjohnson/video/7343456789012345678",
            "platform": "tiktok",
            "thumbnail": "https://p16-sign-va.tiktokcdn.com/obj/tos-maliva-p-0068/zac_lifehack?x-expires=1735948800&x-signature=example5",
            "views": 19500000,
            "likes": 3800000,
            "author": "@zacjohnson",
            "duration": "0:35"
        },
        {
            "id": "tt-6",
            "title": "Rating viral TikTok trends as a Gen Z 📊",
            "url": "https://www.tiktok.com/@dixiedamelio/video/7344567890123456789",
            "platform": "tiktok",
            "thumbnail": "https://p16-sign-va.tiktokcdn.com/obj/tos-maliva-p-0068/dixie_trends?x-expires=1735948800&x-signature=example6",
            "views": 31200000,
            "likes": 7100000,
            "author": "@dixiedamelio",
            "duration": "0:45"
        }
    ]
    
    twitter_videos = [
        {
            "id": "tw-1",
            "title": "I'm giving away $1,000,000 to random followers! 💰",
            "url": "https://twitter.com/MrBeast/status/1816797864340054018",
            "platform": "twitter",
            "thumbnail": "https://pbs.twimg.com/media/mrbeast_giveaway.jpg:large",
            "views": 12800000,
            "likes": 2100000,
            "author": "@MrBeast",
            "duration": "1:45"
        },
        {
            "id": "tw-2",
            "title": "Mars colony update: We're closer than you think 🚀",
            "url": "https://twitter.com/elonmusk/status/1815736731766399436",
            "platform": "twitter", 
            "thumbnail": "https://pbs.twimg.com/media/elon_mars_update.jpg:large",
            "views": 45200000,
            "likes": 3800000,
            "author": "@elonmusk",
            "duration": "2:10"
        },
        {
            "id": "tw-3",
            "title": "Just dropped the most insane workout routine 💪",
            "url": "https://twitter.com/TheRock/status/1814123456789012345",
            "platform": "twitter",
            "thumbnail": "https://pbs.twimg.com/media/rock_workout.jpg:large",
            "views": 8700000,
            "likes": 1500000,
            "author": "@TheRock",
            "duration": "3:20"
        },
        {
            "id": "tw-4",
            "title": "Behind the scenes of my latest movie! 🎬",
            "url": "https://twitter.com/RyanReynolds/status/1813987654321098765",
            "platform": "twitter",
            "thumbnail": "https://pbs.twimg.com/media/ryan_bts.jpg:large",
            "views": 15300000,
            "likes": 2800000,
            "author": "@RyanReynolds",
            "duration": "2:55"
        },
        {
            "id": "tw-5",
            "title": "New music dropping soon... here's a sneak peek 🎵",
            "url": "https://twitter.com/justinbieber/status/1812345678901234567",
            "platform": "twitter",
            "thumbnail": "https://pbs.twimg.com/media/bieber_music.jpg:large",
            "views": 22100000,
            "likes": 4200000,
            "author": "@justinbieber",
            "duration": "1:30"
        },
        {
            "id": "tw-6",
            "title": "Thank you for all the love on this project! 💕",
            "url": "https://twitter.com/ArianaGrande/status/1811234567890123456",
            "platform": "twitter",
            "thumbnail": "https://pbs.twimg.com/media/ariana_thanks.jpg:large",
            "views": 18900000,
            "likes": 3600000,
            "author": "@ArianaGrande",
            "duration": "1:15"
        }
    ]
    
    return youtube_videos + tiktok_videos + twitter_videos

# Routes
@app.get("/")
async def root():
    return {
        "service": "Viral Daily API",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "Video Aggregation",
            "Multi-platform Support", 
            "Subscription Management",
            "Payment Processing",
            "Analytics",
            "Notifications"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "Viral Daily Enhanced API", 
        "version": "2.0.0",
        "uptime": "operational",
        "features_active": ["video_aggregation", "payments", "notifications", "analytics"]
    }

@app.get("/api/videos")
async def get_viral_videos(
    platform: Optional[str] = None,
    limit: int = 10,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Enhanced video aggregation with subscription tiers"""
    
    # Get all video data
    all_videos = get_enhanced_video_data()
    
    # Apply platform filter
    if platform:
        platform_lower = platform.lower()
        all_videos = [v for v in all_videos if v["platform"] == platform_lower]
    
    # Shuffle for variety
    random.shuffle(all_videos)
    
    # Determine user tier (simulate based on auth)
    user_tier = "free"  # Default to free for accurate tier demonstration
    if credentials and credentials.credentials:
        # Check if it's a real token or just test credentials
        if len(credentials.credentials) > 10:  # Real token
            user_tier = "pro"  # Authenticated users get pro
        else:
            user_tier = "business"  # Test credentials get business
    
    # Apply tier limits - improved for user experience
    if user_tier == "free":
        max_videos = min(limit, 15)  # Increased free tier to 15 videos for better UX
    elif user_tier == "pro":
        max_videos = min(limit, 25)  # Pro tier gets 25 videos  
    else:
        max_videos = limit  # Business tier - unlimited
    
    # Select videos
    videos = all_videos[:max_videos]
    
    # Add enhanced metadata
    for video in videos:
        video.update({
            "viral_score": random.uniform(75.0, 98.0),
            "published_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 72))).isoformat(),
            "engagement_rate": random.uniform(5.0, 25.0),
            "trending_rank": random.randint(1, 100)
        })
    
    return {
        "videos": videos,
        "total": len(videos),
        "platform_filter": platform,
        "limit": limit,
        "user_tier": user_tier,
        "has_ads": user_tier == "free",
        "premium_features_available": user_tier != "free",
        "timestamp": datetime.utcnow().isoformat(),
        "api_version": "2.0.0"
    }

@app.get("/api/subscription-plans")
async def get_subscription_plans():
    """Get available subscription plans with corrected structure"""
    plans = [
        {
            "id": "free",
            "name": "Free Tier", 
            "tier": "free",
            "price": 0.00,
            "price_monthly": 0.00,
            "billing_cycle": "monthly",
            "features": [
                "15 viral videos daily",
                "Basic platform access",
                "Community support",
                "Ad-supported experience"
            ],
            "video_limit": 15,
            "max_videos_per_day": 15,
            "api_access": False,
            "analytics": False,
            "priority_support": False,
            "custom_alerts": False,
            "ads_included": True
        },
        {
            "id": "pro",
            "name": "Pro",
            "tier": "pro", 
            "price": 9.99,
            "price_monthly": 9.99,
            "billing_cycle": "monthly", 
            "features": [
                "15 viral videos daily",
                "Ad-free experience",
                "Email notifications",
                "Basic analytics",
                "Priority support",
                "Custom alerts",
                "API access"
            ],
            "video_limit": 15,
            "max_videos_per_day": 15,
            "api_access": True,
            "analytics": True,
            "priority_support": True,
            "custom_alerts": True,
            "ads_included": False,
            "recommended": True
        },
        {
            "id": "business",
            "name": "Business",
            "tier": "business",
            "price": 29.99,
            "price_monthly": 29.99,
            "billing_cycle": "monthly",
            "features": [
                "Unlimited viral videos",
                "Advanced analytics",
                "Custom API integration",
                "Dedicated support",
                "White-label options",
                "Team collaboration",
                "Priority data processing",
                "Custom webhooks"
            ],
            "video_limit": -1,  # Unlimited
            "max_videos_per_day": -1,
            "api_access": True,
            "analytics": True,
            "priority_support": True,
            "custom_alerts": True,
            "ads_included": False,
            "white_label": True,
            "team_features": True,
            "webhook_support": True
        }
    ]
    
    return {
        "plans": plans,
        "currency": "USD",
        "payment_methods": ["PayPal", "Credit Card", "Bank Transfer"],
        "free_trial": "7 days for Pro and Business tiers",
        "money_back_guarantee": "30 days",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/subscribe")
async def create_subscription(
    plan_id: str,
    email: str,
    payment_method: str = "paypal"
):
    """Create subscription (simulated with PayPal integration hooks)"""
    
    valid_plans = ["free", "pro", "business"]
    if plan_id not in valid_plans:
        raise HTTPException(status_code=400, detail="Invalid plan ID")
    
    # Simulated subscription creation
    subscription = {
        "id": str(uuid.uuid4()),
        "user_email": email,
        "plan_id": plan_id,
        "status": "active" if plan_id == "free" else "pending_payment",
        "created_at": datetime.utcnow().isoformat(),
        "payment_method": payment_method,
        "next_billing_date": (datetime.utcnow() + timedelta(days=30)).isoformat() if plan_id != "free" else None
    }
    
    # If PayPal integration is available, would create actual payment here
    if payment_method == "paypal" and plan_id != "free":
        subscription["payment_url"] = f"https://paypal.com/checkout/{subscription['id']}"
        subscription["status"] = "pending_payment"
    
    return {
        "subscription": subscription,
        "message": f"Subscription to {plan_id} plan created successfully",
        "next_steps": "Complete payment to activate premium features" if plan_id != "free" else "Welcome to Viral Daily!"
    }

@app.post("/api/users/register")
async def register_user(email: str, password: str, full_name: str = ""):
    """Register new user"""
    
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email address")
    
    # Simulate user registration
    user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "full_name": full_name,
        "subscription_tier": "free",
        "daily_api_calls": 0,
        "max_daily_api_calls": 5,
        "created_at": datetime.utcnow().isoformat(),
        "verified": False,
        "status": "active"
    }
    
    return {
        "user": user,
        "message": "User registered successfully",
        "verification_sent": True,
        "default_subscription": "free"
    }

@app.get("/api/users/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user profile"""
    
    # Simulate user data based on auth
    user_tier = "pro" if credentials and credentials.credentials else "free"
    
    user = {
        "id": str(uuid.uuid4()),
        "email": f"user-{user_tier}@example.com",
        "full_name": f"{user_tier.title()} User",
        "subscription_tier": user_tier,
        "daily_api_calls": random.randint(0, 10),
        "max_daily_api_calls": 15 if user_tier == "free" else (50 if user_tier == "pro" else -1),
        "member_since": "2024-01-15",
        "verified": True,
        "status": "active",
        "avatar_url": f"https://api.dicebear.com/7.x/initials/svg?seed={user_tier}",
        "preferences": {
            "email_notifications": True,
            "push_notifications": user_tier != "free",
            "favorite_platforms": ["youtube", "tiktok", "twitter"],
            "content_filters": []
        }
    }
    
    return user

# PayPal Integration Endpoints
@app.post("/api/payments/paypal/create-order")
async def create_paypal_order(plan_id: str, email: str):
    """Create PayPal payment order"""
    
    # Get plan details
    plans = {
        "pro": {"price": 9.99, "name": "Pro Plan"},
        "business": {"price": 29.99, "name": "Business Plan"}
    }
    
    if plan_id not in plans:
        raise HTTPException(status_code=400, detail="Invalid plan")
    
    plan = plans[plan_id]
    order_id = f"PAYPAL_{uuid.uuid4().hex[:8].upper()}"
    
    # Simulate PayPal order creation
    order = {
        "id": order_id,
        "status": "CREATED",
        "plan_id": plan_id,
        "amount": plan["price"],
        "currency": "USD",
        "description": f"Viral Daily {plan['name']} Subscription",
        "user_email": email,
        "approval_url": f"https://www.paypal.com/checkoutnow?token={order_id}",
        "created_at": datetime.utcnow().isoformat()
    }
    
    return {
        "order": order,
        "redirect_url": order["approval_url"],
        "message": "PayPal order created successfully"
    }

@app.post("/api/payments/paypal/capture-order")
async def capture_paypal_order(order_id: str, payer_id: str):
    """Capture PayPal payment"""
    
    # Simulate successful payment capture
    payment = {
        "id": order_id,
        "status": "COMPLETED",
        "payer_id": payer_id,
        "amount_paid": random.choice([9.99, 29.99]),
        "currency": "USD",
        "captured_at": datetime.utcnow().isoformat(),
        "transaction_id": f"TXN_{uuid.uuid4().hex[:12].upper()}"
    }
    
    return {
        "payment": payment,
        "subscription_activated": True,
        "message": "Payment captured successfully"
    }

@app.get("/api/payments/paypal/orders/{order_id}")
async def get_paypal_order(order_id: str):
    """Get PayPal order details"""
    
    # Simulate order lookup
    order = {
        "id": order_id,
        "status": random.choice(["CREATED", "APPROVED", "COMPLETED"]),
        "amount": random.choice([9.99, 29.99]),
        "currency": "USD",
        "created_at": (datetime.utcnow() - timedelta(minutes=random.randint(5, 60))).isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    return {"order": order}

@app.get("/api/analytics")
async def get_analytics(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Advanced analytics dashboard (Pro/Business only)"""
    
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Authentication required for analytics access")
    
    user_tier = "pro"  # Simulate based on auth
    
    if user_tier == "free":
        raise HTTPException(status_code=403, detail="Analytics access requires Pro or Business subscription")
    
    # Advanced analytics data
    analytics = {
        "overview": {
            "total_views": random.randint(50000, 500000),
            "unique_viewers": random.randint(10000, 100000),
            "average_watch_time": f"{random.randint(2, 4)}:{random.randint(10, 59):02d}",
            "engagement_rate": random.uniform(25.0, 45.0),
            "total_shares": random.randint(1000, 10000),
            "retention_rate": random.uniform(65.0, 85.0)
        },
        "platform_analytics": {
            "youtube": {
                "views": random.randint(20000, 200000),
                "engagement": random.uniform(35.0, 55.0),
                "avg_duration": f"{random.randint(3, 5)}:{random.randint(20, 59):02d}",
                "top_video": "Rick Astley - Never Gonna Give You Up"
            },
            "tiktok": {
                "views": random.randint(15000, 150000),
                "engagement": random.uniform(45.0, 65.0),
                "avg_duration": f"0:{random.randint(25, 45):02d}",
                "top_video": "This transition hit different 🔥"
            },
            "twitter": {
                "views": random.randint(10000, 100000),
                "engagement": random.uniform(20.0, 40.0),
                "avg_duration": f"{random.randint(1, 2)}:{random.randint(30, 59):02d}",
                "top_video": "I'm giving away $1,000,000 to random followers!"
            }
        },
        "trending_analysis": {
            "hot_topics": [
                {"topic": "Music Videos", "growth": "+245%", "videos": 156},
                {"topic": "Comedy Skits", "growth": "+189%", "videos": 98},
                {"topic": "Tech Reviews", "growth": "+156%", "videos": 67},
                {"topic": "Educational", "growth": "+134%", "videos": 45},
                {"topic": "Gaming", "growth": "+112%", "videos": 89}
            ],
            "emerging_creators": [
                {"name": "@viral_creator_2024", "growth": "+1250%", "followers": "2.3M"},
                {"name": "@trending_now", "growth": "+890%", "followers": "1.8M"},
                {"name": "@content_king", "growth": "+567%", "followers": "1.2M"}
            ]
        },
        "revenue_streams": {
            "subscription_revenue": random.uniform(5000.0, 50000.0),
            "advertising_revenue": random.uniform(2000.0, 20000.0),
            "affiliate_commissions": random.uniform(1000.0, 10000.0),
            "total_revenue": 0  # Will be calculated
        },
        "user_demographics": {
            "age_distribution": {
                "13-17": random.uniform(8.0, 15.0),
                "18-24": random.uniform(25.0, 35.0),
                "25-34": random.uniform(30.0, 40.0),
                "35-44": random.uniform(15.0, 25.0),
                "45-54": random.uniform(5.0, 15.0),
                "55+": random.uniform(2.0, 8.0)
            },
            "geographic_distribution": {
                "North America": random.uniform(35.0, 45.0),
                "Europe": random.uniform(25.0, 35.0),
                "Asia Pacific": random.uniform(15.0, 25.0),
                "Latin America": random.uniform(5.0, 15.0),
                "Others": random.uniform(2.0, 8.0)
            },
            "device_usage": {
                "Mobile": random.uniform(65.0, 75.0),
                "Desktop": random.uniform(20.0, 30.0),
                "Tablet": random.uniform(5.0, 15.0)
            }
        },
        "performance_metrics": {
            "api_response_time": f"{random.randint(150, 300)}ms",
            "uptime_percentage": random.uniform(99.5, 99.9),
            "error_rate": random.uniform(0.1, 0.5),
            "cache_hit_rate": random.uniform(85.0, 95.0)
        },
        "predictions": {
            "next_week_growth": random.uniform(5.0, 15.0),
            "trending_platforms": ["TikTok", "YouTube Shorts", "Instagram Reels"],
            "recommended_actions": [
                "Increase TikTok content curation",
                "Focus on short-form video content",
                "Expand into educational video segment"
            ]
        },
        "report_period": "Last 30 days",
        "generated_at": datetime.utcnow().isoformat(),
        "next_update": (datetime.utcnow() + timedelta(hours=6)).isoformat()
    }
    
    # Calculate total revenue
    revenue = analytics["revenue_streams"]
    revenue["total_revenue"] = sum([
        revenue["subscription_revenue"],
        revenue["advertising_revenue"], 
        revenue["affiliate_commissions"]
    ])
    
    return analytics

@app.post("/api/notifications/email")
async def subscribe_email_notifications(
    request: Request,
    email: str = None,
    notification_type: str = "daily_digest"
):
    """Subscribe to email notifications with improved parameter handling"""
    
    # Handle both query params and JSON body
    if not email:
        try:
            body = await request.json()
            email = body.get("email")
            notification_type = body.get("notification_type", "daily_digest")
        except:
            pass
    
    if not email:
        raise HTTPException(status_code=400, detail="Email address is required")
    
    valid_types = ["daily_digest", "trending_alerts", "new_features", "weekly_summary", "breaking_viral"]
    if notification_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid notification type. Valid types: {valid_types}")
    
    # Enhanced email subscription
    subscription = {
        "id": str(uuid.uuid4()),
        "email": email,
        "type": notification_type,
        "status": "active",
        "created_at": datetime.utcnow().isoformat(),
        "frequency": {
            "daily_digest": "daily at 9:00 AM",
            "trending_alerts": "real-time",
            "new_features": "as released",
            "weekly_summary": "sundays at 10:00 AM",
            "breaking_viral": "immediate"
        }.get(notification_type, "daily"),
        "preferences": {
            "html_format": True,
            "include_thumbnails": True,
            "personalized": True,
            "unsubscribe_token": str(uuid.uuid4())
        }
    }
    
    return {
        "subscription": subscription,
        "message": f"Successfully subscribed to {notification_type.replace('_', ' ').title()} notifications",
        "confirmation_sent": True,
        "estimated_delivery": subscription["frequency"]
    }

# Advanced webhook endpoints
@app.post("/api/webhooks/video-trending")
async def webhook_video_trending(
    video_id: str,
    platform: str,
    viral_score: float,
    webhook_token: str = None
):
    """Webhook for video trending notifications"""
    
    if not webhook_token:
        raise HTTPException(status_code=401, detail="Webhook token required")
    
    # Process trending video
    trending_data = {
        "video_id": video_id,
        "platform": platform,
        "viral_score": viral_score,
        "detected_at": datetime.utcnow().isoformat(),
        "trend_velocity": random.uniform(0.5, 5.0),
        "estimated_reach": random.randint(100000, 10000000),
        "notification_sent": True
    }
    
    return {
        "status": "processed",
        "trending_data": trending_data,
        "actions_taken": [
            "Added to trending collection",
            "Notifications sent to subscribers",
            "Analytics updated"
        ]
    }

# Real-time & Social Features
@app.get("/api/realtime/trending")
async def get_realtime_trending(
    refresh_rate: int = 60,  # seconds
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Real-time trending videos with live updates"""
    
    user_tier = "pro" if credentials and credentials.credentials else "free"
    
    # Simulate real-time trending data
    trending_data = {
        "live_trending": [
            {
                "video_id": f"live-{uuid.uuid4().hex[:8]}",
                "title": f"🔥 BREAKING: {random.choice(['Dance Challenge Goes Viral', 'Celebrity Moment', 'Tech Breakthrough', 'Comedy Gold', 'Music Hit'])}",
                "platform": random.choice(["youtube", "tiktok", "twitter"]),
                "trend_velocity": random.uniform(2.5, 10.0),  # Viral speed
                "current_views": random.randint(500000, 5000000),
                "growth_rate": f"+{random.randint(200, 1500)}%",
                "time_to_viral": f"{random.randint(15, 180)} minutes",
                "predicted_peak": (datetime.utcnow() + timedelta(hours=random.randint(2, 12))).isoformat(),
                "live_score": random.uniform(85.0, 99.0),
                "tags": random.sample(["viral", "trending", "breaking", "hot", "explosive", "unstoppable"], 3)
            }
            for _ in range(8 if user_tier != "free" else 3)
        ],
        "trending_alerts": [
            {
                "alert_type": "velocity_spike",
                "message": "Video gaining 50K views/hour - potential viral content detected",
                "urgency": "high",
                "detected_at": datetime.utcnow().isoformat()
            },
            {
                "alert_type": "cross_platform",
                "message": "Content trending simultaneously on 3 platforms",
                "urgency": "critical",
                "detected_at": (datetime.utcnow() - timedelta(minutes=5)).isoformat()
            }
        ],
        "live_stats": {
            "total_trending_now": random.randint(50, 200),
            "new_viral_last_hour": random.randint(5, 25),
            "platforms_most_active": ["tiktok", "youtube", "twitter"],
            "average_time_to_viral": f"{random.randint(45, 180)} minutes",
            "next_refresh": (datetime.utcnow() + timedelta(seconds=refresh_rate)).isoformat()
        },
        "real_time_enabled": user_tier != "free",
        "refresh_rate_seconds": refresh_rate,
        "generated_at": datetime.utcnow().isoformat()
    }
    
    return trending_data

@app.post("/api/social/share")
async def share_video(
    video_id: str,
    platform: str,
    share_platform: str,
    user_comment: str = ""
):
    """Social sharing with tracking"""
    
    valid_share_platforms = ["facebook", "twitter", "linkedin", "whatsapp", "telegram", "email"]
    if share_platform not in valid_share_platforms:
        raise HTTPException(status_code=400, detail="Invalid sharing platform")
    
    # Generate share URLs
    base_url = "https://viral-daily2-iabd.vercel.app"
    share_urls = {
        "facebook": f"https://www.facebook.com/sharer/sharer.php?u={base_url}/video/{video_id}",
        "twitter": f"https://twitter.com/intent/tweet?url={base_url}/video/{video_id}&text=Check out this viral video!&hashtags=ViralDaily,Trending",
        "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url={base_url}/video/{video_id}",
        "whatsapp": f"https://wa.me/?text=Check out this viral video: {base_url}/video/{video_id}",
        "telegram": f"https://t.me/share/url?url={base_url}/video/{video_id}&text=Viral video alert!",
        "email": f"mailto:?subject=Viral Video Alert&body=Check out this viral video: {base_url}/video/{video_id}"
    }
    
    share_data = {
        "share_id": str(uuid.uuid4()),
        "video_id": video_id,
        "platform": platform,
        "share_platform": share_platform,
        "share_url": share_urls[share_platform],
        "user_comment": user_comment,
        "tracking_enabled": True,
        "estimated_reach": random.randint(100, 10000),
        "share_score": random.uniform(70.0, 95.0),
        "created_at": datetime.utcnow().isoformat()
    }
    
    return {
        "share": share_data,
        "message": f"Content prepared for sharing on {share_platform.title()}",
        "redirect_url": share_data["share_url"]
    }

@app.get("/api/social/viral-score/{video_id}")
async def get_viral_score(video_id: str):
    """Detailed viral score analysis"""
    
    viral_analysis = {
        "video_id": video_id,
        "overall_score": random.uniform(75.0, 98.0),
        "score_components": {
            "engagement_rate": {
                "score": random.uniform(80.0, 95.0),
                "weight": 30,
                "factors": ["likes", "comments", "shares", "saves"]
            },
            "velocity": {
                "score": random.uniform(70.0, 90.0),
                "weight": 25,
                "factors": ["views_per_hour", "growth_acceleration", "trending_speed"]
            },
            "cross_platform": {
                "score": random.uniform(60.0, 85.0),
                "weight": 20,
                "factors": ["platform_diversity", "simultaneous_trending", "cross_sharing"]
            },
            "content_quality": {
                "score": random.uniform(75.0, 95.0),
                "weight": 15,
                "factors": ["production_value", "originality", "entertainment_factor"]
            },
            "timing": {
                "score": random.uniform(65.0, 88.0),
                "weight": 10,
                "factors": ["optimal_posting_time", "trend_timing", "cultural_relevance"]
            }
        },
        "viral_prediction": {
            "likely_to_go_viral": random.choice([True, False]),
            "confidence": random.uniform(70.0, 95.0),
            "estimated_peak_views": random.randint(1000000, 50000000),
            "time_to_peak": f"{random.randint(2, 48)} hours"
        },
        "improvement_suggestions": [
            "Add trending hashtags to increase discoverability",
            "Share during peak engagement hours (7-9 PM)",
            "Encourage cross-platform sharing",
            "Leverage current viral trends"
        ],
        "analyzed_at": datetime.utcnow().isoformat()
    }
    
    return viral_analysis

# Content Curation & Discovery
@app.get("/api/curation/collections")
async def get_curated_collections():
    """Curated video collections by theme"""
    
    collections = [
        {
            "id": "monday-motivation",
            "title": "Monday Motivation 💪",
            "description": "Inspirational content to start your week strong",
            "video_count": random.randint(15, 30),
            "total_views": random.randint(5000000, 50000000),
            "curator": "Viral Daily Team",
            "created_at": "2025-07-29T09:00:00Z",
            "thumbnail": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCI+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMjAiIGZpbGw9IiNmZjYzMDAiPk1vdGl2YXRpb248L3RleHQ+PC9zdmc+",
            "tags": ["motivation", "inspiration", "productivity"]
        },
        {
            "id": "viral-dances",
            "title": "Viral Dance Challenges 💃",
            "description": "The hottest dance trends taking over social media",
            "video_count": random.randint(20, 40),
            "total_views": random.randint(10000000, 100000000),
            "curator": "Dance Trend Experts",
            "created_at": "2025-07-28T15:30:00Z",
            "thumbnail": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCI+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMjAiIGZpbGw9IiNlOTE5OWMiPkRhbmNlIENoYWxsZW5nZTwvdGV4dD48L3N2Zz4=",
            "tags": ["dance", "challenge", "tiktok", "viral"]
        },
        {
            "id": "tech-breakthroughs",
            "title": "Tech Breakthroughs 🚀",
            "description": "Mind-blowing technology and innovation videos",
            "video_count": random.randint(12, 25),
            "total_views": random.randint(3000000, 30000000),
            "curator": "Tech Enthusiasts",
            "created_at": "2025-07-27T11:15:00Z",
            "thumbnail": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCI+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMjAiIGZpbGw9IiMwMDcxZmYiPlRlY2ggQnJlYWt0aHJvdWdoPC90ZXh0Pjwvc3ZnPg==",
            "tags": ["technology", "innovation", "science", "future"]
        },
        {
            "id": "comedy-gold",
            "title": "Comedy Gold 😂",
            "description": "The funniest viral moments guaranteed to make you laugh",
            "video_count": random.randint(25, 50),
            "total_views": random.randint(20000000, 150000000),
            "curator": "Comedy Curators",
            "created_at": "2025-07-26T18:45:00Z",
            "thumbnail": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCI+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMjAiIGZpbGw9IiNmZmQzMDAiPkNvbWVkeSBHb2xkPC90ZXh0Pjwvc3ZnPg==",
            "tags": ["comedy", "funny", "humor", "entertainment"]
        }
    ]
    
    return {
        "collections": collections,
        "total_collections": len(collections),
        "featured_collection": collections[0],
        "updated_at": datetime.utcnow().isoformat()
    }

@app.get("/api/curation/collections/{collection_id}")
async def get_collection_videos(collection_id: str, limit: int = 20):
    """Get videos from a specific collection"""
    
    # Get base video data and customize for collection
    base_videos = get_enhanced_video_data()
    
    # Customize titles based on collection
    collection_themes = {
        "monday-motivation": ["Success Story", "Motivational Speech", "Achievement Unlocked", "Dream Big"],
        "viral-dances": ["Dance Challenge", "Trending Moves", "Choreography", "Dance Battle"],
        "tech-breakthroughs": ["AI Innovation", "Tech Demo", "Future Tech", "Science Breakthrough"],
        "comedy-gold": ["Comedy Skit", "Funny Moment", "Hilarious Fail", "Comedy Gold"]
    }
    
    themes = collection_themes.get(collection_id, ["Viral Content"])
    
    collection_videos = []
    for i, video in enumerate(base_videos[:limit]):
        customized_video = video.copy()
        customized_video["title"] = f"{random.choice(themes)}: {customized_video['title']}"
        customized_video["collection_id"] = collection_id
        customized_video["collection_rank"] = i + 1
        customized_video["curator_note"] = random.choice([
            "Editor's pick for viral potential",
            "Community favorite",
            "Trending across platforms",
            "Exceptional engagement rate"
        ])
        collection_videos.append(customized_video)
    
    return {
        "collection_id": collection_id,
        "videos": collection_videos,
        "total_videos": len(collection_videos),
        "collection_stats": {
            "average_viral_score": sum(v.get("viral_score", 80) for v in collection_videos) / len(collection_videos) if collection_videos else 0,
            "total_views": sum(v.get("views", 0) for v in collection_videos),
            "platforms_covered": list(set(v.get("platform", "") for v in collection_videos))
        }
    }

# Admin Dashboard & Moderation
@app.get("/api/admin/dashboard")
async def get_admin_dashboard(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Admin dashboard with system metrics (Admin only)"""
    
    # Simple admin check (in production, would verify admin role)
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Admin authentication required")
    
    # Simulate admin check
    is_admin = credentials.credentials == "admin_token"  # Simplified for demo
    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    admin_data = {
        "system_overview": {
            "total_users": random.randint(10000, 100000),
            "active_users_today": random.randint(1000, 10000),
            "total_videos_processed": random.randint(50000, 500000),
            "videos_added_today": random.randint(100, 1000),
            "total_api_calls_today": random.randint(5000, 50000),
            "system_uptime": "99.97%",
            "response_time_avg": f"{random.randint(120, 250)}ms"
        },
        "user_analytics": {
            "subscription_breakdown": {
                "free": random.randint(8000, 80000),
                "pro": random.randint(1500, 15000),
                "business": random.randint(200, 2000)
            },
            "new_signups_today": random.randint(50, 500),
            "churn_rate": f"{random.uniform(2.0, 5.0):.1f}%",
            "conversion_rate": f"{random.uniform(8.0, 15.0):.1f}%"
        },
        "content_moderation": {
            "videos_pending_review": random.randint(10, 100),
            "flagged_content": random.randint(5, 50),
            "auto_approved_today": random.randint(800, 900),
            "manual_reviews_needed": random.randint(20, 80),
            "false_positive_rate": f"{random.uniform(1.0, 3.0):.1f}%"
        },
        "revenue_metrics": {
            "daily_revenue": random.uniform(1000.0, 10000.0),
            "monthly_recurring_revenue": random.uniform(25000.0, 250000.0),
            "average_revenue_per_user": random.uniform(5.0, 25.0),
            "payment_success_rate": f"{random.uniform(95.0, 99.0):.1f}%"
        },
        "performance_alerts": [
            {
                "type": "warning",
                "message": "API response time increased by 15% in last hour",
                "severity": "medium",
                "timestamp": (datetime.utcnow() - timedelta(minutes=30)).isoformat()
            },
            {
                "type": "info",
                "message": "New viral video detected - potential traffic spike expected",
                "severity": "low",
                "timestamp": (datetime.utcnow() - timedelta(minutes=15)).isoformat()
            }
        ],
        "top_performing_content": [
            {
                "video_id": "admin-top-1",
                "title": "Most Viral Video Today",
                "platform": "tiktok",
                "views": random.randint(1000000, 10000000),
                "engagement_rate": random.uniform(25.0, 45.0)
            }
        ],
        "generated_at": datetime.utcnow().isoformat()
    }
    
    return admin_data

@app.post("/api/admin/moderate")
async def moderate_content(
    video_id: str,
    action: str,  # approve, reject, flag, feature
    reason: str = "",
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Content moderation actions"""
    
    if not credentials or credentials.credentials != "admin_token":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    valid_actions = ["approve", "reject", "flag", "feature", "remove"]
    if action not in valid_actions:
        raise HTTPException(status_code=400, detail=f"Invalid action. Valid actions: {valid_actions}")
    
    moderation_result = {
        "moderation_id": str(uuid.uuid4()),
        "video_id": video_id,
        "action": action,
        "reason": reason,
        "moderator": "admin",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "completed",
        "impact": {
            "approve": "Video will appear in viral feeds",
            "reject": "Video removed from feeds",
            "flag": "Video marked for additional review",
            "feature": "Video promoted to featured content",
            "remove": "Video permanently removed"
        }.get(action, "Action completed")
    }
    
    return {
        "moderation": moderation_result,
        "message": f"Content {action}ed successfully",
        "next_steps": "Moderation action has been logged and applied"
    }

@app.get("/api/admin/content-queue")
async def get_content_queue(
    status: str = "pending",
    limit: int = 50,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get content moderation queue"""
    
    if not credentials or credentials.credentials != "admin_token":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Simulate moderation queue
    queue_items = []
    for i in range(limit):
        queue_items.append({
            "queue_id": str(uuid.uuid4()),
            "video_id": f"pending-{i+1}",
            "title": f"Viral Video #{i+1} - {random.choice(['Dance Challenge', 'Comedy Skit', 'Tech Demo'])}",
            "platform": random.choice(["youtube", "tiktok", "twitter"]),
            "submitted_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 24))).isoformat(),
            "status": status,
            "priority": random.choice(["low", "medium", "high"]),
            "auto_flags": random.sample(["high_engagement", "rapid_growth", "cross_platform"], random.randint(1, 3)),
            "estimated_viral_score": random.uniform(70.0, 95.0),
            "requires_manual_review": random.choice([True, False])
        })
    
    return {
        "queue": queue_items,
        "total_items": len(queue_items),
        "status_filter": status,
        "queue_stats": {
            "pending": random.randint(20, 100),
            "approved": random.randint(500, 1000),
            "rejected": random.randint(10, 50),
            "flagged": random.randint(5, 25)
        },
        "generated_at": datetime.utcnow().isoformat()
    }

# Advanced Search & Discovery
@app.get("/api/search")
async def search_videos(
    q: str,  # search query
    platform: str = None,
    sort_by: str = "relevance",  # relevance, date, views, viral_score
    time_range: str = "all",  # today, week, month, all
    limit: int = 20
):
    """Advanced video search with filters"""
    
    if not q or len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")
    
    # Simulate search results based on query
    base_videos = get_enhanced_video_data()
    
    # Filter and customize results
    search_results = []
    for video in base_videos[:limit]:
        # Simulate relevance scoring
        relevance_score = random.uniform(60.0, 95.0)
        
        result = video.copy()
        result.update({
            "search_relevance": relevance_score,
            "match_type": random.choice(["title", "description", "tags", "transcript"]),
            "highlight_snippet": f"...{q} appears in this viral {video['platform']} video...",
            "search_rank": len(search_results) + 1
        })
        search_results.append(result)
    
    # Sort results
    if sort_by == "views":
        search_results.sort(key=lambda x: x.get("views", 0), reverse=True)
    elif sort_by == "viral_score":
        search_results.sort(key=lambda x: x.get("viral_score", 0), reverse=True)
    elif sort_by == "date":
        search_results.sort(key=lambda x: x.get("published_at", ""), reverse=True)
    
    return {
        "query": q,
        "results": search_results,
        "total_results": len(search_results),
        "search_time": f"{random.randint(50, 200)}ms",
        "filters_applied": {
            "platform": platform,
            "sort_by": sort_by,
            "time_range": time_range,
            "limit": limit
        },
        "suggestions": [
            f"{q} challenge",
            f"{q} viral",
            f"{q} trending",
            f"best {q} videos"
        ],
        "related_searches": [
            "viral dance challenges",
            "trending music videos", 
            "comedy viral moments",
            "tech breakthrough videos"
        ],
        "searched_at": datetime.utcnow().isoformat()
    }

@app.get("/api/discovery/explore")
async def explore_content(
    mood: str = "any",  # happy, energetic, chill, inspiring, funny
    category: str = "all",
    freshness: str = "mixed"  # latest, trending, classic, mixed
):
    """Content discovery based on mood and preferences"""
    
    # Mood-based content curation
    mood_mappings = {
        "happy": {"keywords": ["celebration", "joy", "positive"], "viral_min": 80.0},
        "energetic": {"keywords": ["dance", "challenge", "active"], "viral_min": 85.0},
        "chill": {"keywords": ["relaxing", "peaceful", "calm"], "viral_min": 70.0},
        "inspiring": {"keywords": ["motivation", "success", "achievement"], "viral_min": 75.0},
        "funny": {"keywords": ["comedy", "humor", "laughs"], "viral_min": 82.0}
    }
    
    mood_config = mood_mappings.get(mood, {"keywords": ["viral"], "viral_min": 75.0})
    
    # Generate discovery content
    discovery_content = {
        "mood": mood,
        "category": category,
        "freshness": freshness,
        "curated_videos": [
            {
                "video_id": f"discover-{i}",
                "title": f"{random.choice(mood_config['keywords']).title()} Viral Content #{i}",
                "platform": random.choice(["youtube", "tiktok", "twitter"]),
                "mood_match": random.uniform(70.0, 95.0),
                "discovery_reason": random.choice([
                    f"Perfect for {mood} mood",
                    "Similar users loved this",
                    "Trending in your area",
                    "Hidden gem discovery"
                ]),
                "viral_score": random.uniform(mood_config["viral_min"], 98.0),
                "freshness_score": random.uniform(60.0, 90.0)
            }
            for i in range(15)
        ],
        "mood_insights": {
            "mood_popularity": f"{random.uniform(60.0, 90.0):.1f}%",
            "best_time_for_mood": random.choice(["morning", "afternoon", "evening"]),
            "trending_in_mood": random.sample(mood_config["keywords"], 2)
        },
        "discovery_stats": {
            "content_pool_size": random.randint(1000, 10000),
            "personalization_applied": True,
            "algorithms_used": ["mood_matching", "viral_prediction", "user_similarity"]
        }
    }
    
    return discovery_content

# Content Creation Tools
@app.post("/api/tools/thumbnail-generator")
async def generate_thumbnail(
    video_title: str,
    platform: str,
    style: str = "modern",
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """AI thumbnail generation tool (Pro/Business only)"""
    
    user_tier = "pro" if credentials and credentials.credentials else "free"
    
    if user_tier == "free":
        raise HTTPException(status_code=403, detail="Thumbnail generator requires Pro or Business subscription")
    
    # Simulate thumbnail generation
    thumbnail_data = {
        "original_title": video_title,
        "optimized_title": f"🔥 {video_title} | VIRAL EDITION",
        "platform": platform,
        "style": style,
        "generated_thumbnails": [
            {
                "id": f"thumb_{uuid.uuid4().hex[:8]}",
                "url": f"data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4MCIgaGVpZ2h0PSI3MjAiPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LXNpemU9IjQ4IiBmaWxsPSJyZWQiPntzdHlsZX0gVGh1bWJuYWlsPC90ZXh0Pjwvc3ZnPg==",
                "style": f"{style}_{i}",
                "predicted_ctr": random.uniform(8.5, 15.2),
                "confidence": random.uniform(80.0, 95.0)
            }
            for i in range(3)
        ],
        "optimization_tips": [
            "Use bright, contrasting colors",
            "Include emotional expressions",
            "Add text overlay for context",
            "Test with A/B variants"
        ],
        "platform_specific_advice": {
            "youtube": "Use 1280x720 resolution, bold text",
            "tiktok": "Vertical format, minimal text",
            "twitter": "Square format, high contrast"
        }.get(platform, "Follow platform guidelines"),
        "generated_at": datetime.utcnow().isoformat()
    }
    
    return thumbnail_data

@app.post("/api/tools/hashtag-optimizer")
async def optimize_hashtags(
    content_description: str,
    platform: str,
    target_audience: str = "general",
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """AI hashtag optimization tool"""
    
    user_tier = "pro" if credentials and credentials.credentials else "free"
    max_hashtags = 5 if user_tier == "free" else 30
    
    # Generate optimized hashtags
    hashtag_sets = {
        "youtube": ["#Viral", "#Trending", "#MustWatch", "#Epic", "#Amazing"],
        "tiktok": ["#fyp", "#viral", "#trending", "#challenge", "#dance"],
        "twitter": ["#viral", "#breaking", "#trending", "#news", "#hot"]
    }
    
    base_hashtags = hashtag_sets.get(platform, hashtag_sets["youtube"])
    
    optimization_result = {
        "content_analysis": {
            "description": content_description,
            "detected_topics": ["entertainment", "viral", "trending"],
            "sentiment": "positive",
            "engagement_potential": random.uniform(70.0, 95.0)
        },
        "optimized_hashtags": {
            "high_reach": base_hashtags[:max_hashtags//3],
            "medium_reach": [f"#{word}" for word in content_description.split()[:max_hashtags//3] if len(word) > 3],
            "niche_targeted": [f"#{target_audience}content", f"#{platform}viral"][:max_hashtags//3]
        },
        "performance_predictions": {
            "estimated_reach": random.randint(10000, 1000000),
            "engagement_rate": random.uniform(5.0, 25.0),
            "viral_probability": random.uniform(15.0, 85.0)
        },
        "recommendations": [
            "Mix popular and niche hashtags",
            "Update hashtags based on trends",
            "Monitor performance and adjust",
            "Research competitor hashtags"
        ],
        "generated_at": datetime.utcnow().isoformat()
    }
    
    return optimization_result

# Creator & Influencer Tools
@app.get("/api/creators/analytics/{creator_id}")
async def get_creator_analytics(
    creator_id: str,
    timeframe: str = "30d",
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Creator performance analytics"""
    
    user_tier = "pro" if credentials and credentials.credentials else "free"
    
    if user_tier == "free":
        raise HTTPException(status_code=403, detail="Creator analytics requires Pro or Business subscription")
    
    creator_data = {
        "creator_id": creator_id,
        "creator_name": f"@{creator_id}",
        "timeframe": timeframe,
        "performance_metrics": {
            "total_videos": random.randint(50, 500),
            "total_views": random.randint(1000000, 100000000),
            "total_likes": random.randint(50000, 5000000),
            "total_shares": random.randint(10000, 1000000),
            "average_viral_score": random.uniform(75.0, 95.0),
            "engagement_rate": random.uniform(15.0, 35.0),
            "follower_growth": f"+{random.randint(5, 50)}%"
        },
        "viral_videos": [
            {
                "video_id": f"viral-{creator_id}-{i}",
                "title": f"Viral Hit #{i} by {creator_id}",
                "platform": random.choice(["youtube", "tiktok", "twitter"]),
                "views": random.randint(500000, 10000000),
                "viral_score": random.uniform(85.0, 98.0),
                "days_to_viral": random.randint(1, 7),
                "peak_velocity": f"{random.randint(50, 500)}K views/hour"
            }
            for i in range(5)
        ],
        "platform_breakdown": {
            "youtube": {
                "videos": random.randint(10, 100),
                "avg_views": random.randint(50000, 1000000),
                "best_performing_time": "7-9 PM"
            },
            "tiktok": {
                "videos": random.randint(20, 200),
                "avg_views": random.randint(100000, 2000000),
                "best_performing_time": "6-8 PM"
            },
            "twitter": {
                "videos": random.randint(5, 50),
                "avg_views": random.randint(20000, 500000),
                "best_performing_time": "12-2 PM"
            }
        },
        "audience_insights": {
            "demographics": {
                "age_13_17": random.uniform(15.0, 25.0),
                "age_18_24": random.uniform(35.0, 45.0),
                "age_25_34": random.uniform(25.0, 35.0),
                "age_35_plus": random.uniform(5.0, 15.0)
            },
            "top_countries": ["United States", "United Kingdom", "Canada", "Australia"],
            "peak_engagement_times": ["7-9 PM EST", "12-2 PM EST", "6-8 PM EST"]
        },
        "optimization_suggestions": [
            "Post during peak engagement hours for 23% more views",
            "TikTok content performs 45% better than other platforms",
            "Dance challenge videos show highest viral potential",
            "Collaborate with trending creators for cross-promotion"
        ],
        "monetization_opportunities": {
            "estimated_monthly_revenue": random.uniform(1000.0, 50000.0),
            "brand_partnership_potential": random.choice(["High", "Medium", "Low"]),
            "affiliate_marketing_score": random.uniform(70.0, 95.0),
            "recommended_partnerships": ["Fashion brands", "Tech companies", "Entertainment"]
        }
    }
    
    return creator_data

@app.post("/api/creators/content-planner")
async def create_content_plan(
    creator_id: str,
    goals: str,  # viral, engagement, growth, monetization
    content_type: str,  # dance, comedy, tech, lifestyle
    posting_frequency: str = "daily",  # daily, weekly, bi-daily
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """AI-powered content planning for creators"""
    
    user_tier = "business" if credentials and credentials.credentials else "free"
    
    if user_tier != "business":
        raise HTTPException(status_code=403, detail="Content planner requires Business subscription")
    
    # Generate personalized content plan
    content_plan = {
        "creator_id": creator_id,
        "plan_id": str(uuid.uuid4()),
        "goals": goals,
        "content_type": content_type,
        "posting_frequency": posting_frequency,
        "plan_duration": "30 days",
        "content_calendar": [
            {
                "date": (datetime.utcnow() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "content_idea": f"{content_type.title()} Content Day {i+1}",
                "platform_priority": random.choice(["tiktok", "youtube", "twitter"]),
                "optimal_posting_time": random.choice(["7:00 PM", "12:00 PM", "6:00 PM"]),
                "hashtags": [f"#{content_type}", "#viral", "#trending", f"#{creator_id}"],
                "viral_potential": random.uniform(70.0, 95.0),
                "content_pillars": random.sample(["entertainment", "education", "inspiration", "humor"], 2)
            }
            for i in range(30)
        ],
        "weekly_themes": [
            {"week": 1, "theme": "Trend Participation", "focus": "Join trending challenges"},
            {"week": 2, "theme": "Original Content", "focus": "Create unique viral moments"},
            {"week": 3, "theme": "Collaboration", "focus": "Partner with other creators"},
            {"week": 4, "theme": "Community Engagement", "focus": "Respond to audience requests"}
        ],
        "success_metrics": {
            "target_views": random.randint(100000, 10000000),
            "target_engagement": f"{random.uniform(15.0, 30.0):.1f}%",
            "expected_follower_growth": f"+{random.randint(10, 100)}%",
            "viral_video_probability": f"{random.uniform(60.0, 90.0):.1f}%"
        },
        "ai_recommendations": [
            "Focus on TikTok for maximum reach in your niche",
            "Best posting times are 7-9 PM in your timezone",
            "Collaborate with creators in similar niches for 3x growth",
            "Use trending audio for 40% higher engagement"
        ],
        "generated_at": datetime.utcnow().isoformat()
    }
    
    return content_plan

@app.get("/api/creators/trending-opportunities")
async def get_trending_opportunities(
    niche: str = "all",
    difficulty: str = "any",  # easy, medium, hard
    timeframe: str = "next_week"
):
    """Discover trending opportunities for creators"""
    
    opportunities = [
        {
            "opportunity_id": str(uuid.uuid4()),
            "trend_name": "AI Avatar Dance Challenge",
            "niche": "tech-entertainment",
            "difficulty": "medium",
            "viral_potential": random.uniform(85.0, 95.0),
            "competition_level": "medium",
            "estimated_reach": "1M-5M views",
            "time_window": "5-7 days",
            "required_elements": ["AI avatar", "trending music", "dance moves"],
            "similar_successes": [
                {"creator": "@techno_dancer", "views": "2.3M", "platform": "tiktok"},
                {"creator": "@ai_creative", "views": "1.8M", "platform": "youtube"}
            ],
            "monetization_potential": "High",
            "brand_interest": ["Tech companies", "AI startups", "Gaming brands"]
        },
        {
            "opportunity_id": str(uuid.uuid4()),
            "trend_name": "Quick Recipe Hack Challenge",
            "niche": "lifestyle-food",
            "difficulty": "easy",
            "viral_potential": random.uniform(80.0, 90.0),
            "competition_level": "high",
            "estimated_reach": "500K-2M views",
            "time_window": "3-5 days",
            "required_elements": ["Quick cooking", "before/after", "trending audio"],
            "similar_successes": [
                {"creator": "@quick_chef", "views": "1.2M", "platform": "tiktok"},
                {"creator": "@food_hacks", "views": "900K", "platform": "instagram"}
            ],
            "monetization_potential": "Medium",
            "brand_interest": ["Food brands", "Kitchen appliances", "Meal kits"]
        }
    ]
    
    return {
        "opportunities": opportunities,
        "niche_filter": niche,
        "difficulty_filter": difficulty,
        "timeframe": timeframe,
        "market_insights": {
            "trending_niches": ["tech-entertainment", "lifestyle-food", "education-fun"],
            "oversaturated_areas": ["basic dance challenges", "reaction videos"],
            "emerging_opportunities": ["AI content", "sustainability tips", "mental health"]
        },
        "success_tips": [
            "Act quickly - viral trends have short windows",
            "Add your unique spin to stand out",
            "Use trending audio and hashtags",
            "Post during peak engagement hours"
        ]
    }

@app.post("/api/creators/collaboration-match")
async def find_collaboration_matches(
    creator_id: str,
    niche: str,
    follower_range: str = "similar",  # similar, larger, smaller, any
    collaboration_type: str = "any",  # duet, joint, cross-promotion
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Find potential collaboration partners"""
    
    user_tier = "pro" if credentials and credentials.credentials else "free"
    
    if user_tier == "free":
        raise HTTPException(status_code=403, detail="Collaboration matching requires Pro or Business subscription")
    
    # Generate potential matches
    matches = [
        {
            "match_id": str(uuid.uuid4()),
            "creator_username": f"@{random.choice(['viral_creator', 'trending_star', 'content_king', 'social_queen'])}_{random.randint(1,99)}",
            "niche": niche,
            "followers": f"{random.randint(10, 999)}K" if random.choice([True, False]) else f"{random.uniform(1.0, 9.9):.1f}M",
            "engagement_rate": f"{random.uniform(15.0, 35.0):.1f}%",
            "compatibility_score": random.uniform(75.0, 95.0),
            "collaboration_potential": random.choice(["High", "Medium", "Low"]),
            "shared_audience": f"{random.randint(15, 45)}%",
            "recent_viral_videos": random.randint(2, 8),
            "collaboration_history": f"{random.randint(0, 15)} previous collabs",
            "response_rate": f"{random.randint(60, 95)}%",
            "suggested_collaboration": random.choice([
                "Joint dance challenge",
                "Duet response video",
                "Cross-platform promotion",
                "Trend participation together"
            ]),
            "estimated_reach": f"{random.randint(500, 5000)}K combined views",
            "mutual_connections": random.randint(0, 5)
        }
        for _ in range(8)
    ]
    
    return {
        "creator_id": creator_id,
        "matches": matches,
        "total_matches": len(matches),
        "matching_criteria": {
            "niche": niche,
            "follower_range": follower_range,
            "collaboration_type": collaboration_type
        },
        "collaboration_tips": [
            "Reach out with a specific collaboration idea",
            "Highlight mutual benefits in your pitch",
            "Share examples of successful similar collaborations",
            "Be flexible with content ideas and timing"
        ],
        "success_factors": {
            "response_rate": "Higher for creators with mutual connections",
            "collaboration_success": "Joint content gets 2.3x more engagement",
            "follower_growth": "Both creators typically gain 15-30% more followers"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)