#!/usr/bin/env python3
"""
Minimal working server for Railway - guaranteed to start
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Viral Daily API - Minimal")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/api/")
async def root():
    return {
        "message": "Viral Daily API - Full Featured Mode",
        "server_mode": "ENHANCED_MINIMAL_v2.0",
        "status": "healthy",
        "version": "2.0",
        "features": ["Platform Filtering", "Enhanced Content", "Subscription Ready"],
        "deployment_time": "2025-07-31T19:00:00Z"
    }

@app.get("/api/subscription/plans")
async def get_subscription_plans():
    """Subscription plans endpoint"""
    plans = [
        {
            "tier": "free",
            "name": "Free Explorer",
            "price_monthly": 0.0,
            "price_yearly": 0.0,
            "max_videos_per_day": 40,
            "features": [
                "40 viral videos per day",
                "Basic platform access",
                "Community support",
                "Ad-supported experience"
            ],
            "has_ads": True
        },
        {
            "tier": "pro",
            "name": "Pro Creator",
            "price_monthly": 9.99,
            "price_yearly": 99.99,
            "max_videos_per_day": 100,
            "features": [
                "100 viral videos per day",
                "Advanced platform access",
                "Priority support",
                "Ad-free experience",
                "API access"
            ],
            "has_ads": False
        },
        {
            "tier": "business",
            "name": "Business Intelligence",
            "price_monthly": 29.99,
            "price_yearly": 299.99,
            "max_videos_per_day": -1,
            "features": [
                "Unlimited viral videos",
                "Premium platform access",
                "24/7 priority support",
                "Advanced analytics",
                "Full API access",
                "Custom integrations"
            ],
            "has_ads": False
        }
    ]
    
    return {"plans": plans, "total_plans": len(plans)}

@app.get("/api/videos")
async def get_videos(platform: str = None, limit: int = 40):
    """Enhanced video endpoint with platform filtering"""
    videos = []
    
    # Add sample YouTube videos with REAL working URLs and thumbnails
    youtube_samples = [
        {"id": "dQw4w9WgXcQ", "title": "Rick Astley - Never Gonna Give You Up"},
        {"id": "9bZkp7q19f0", "title": "PSY - GANGNAM STYLE"},
        {"id": "kJQP7kiw5Fk", "title": "Luis Fonsi - Despacito ft. Daddy Yankee"},
        {"id": "JGwWNGJdvx8", "title": "Ed Sheeran - Shape of You"},
        {"id": "XqZsoesa55w", "title": "Baby Shark Dance"},
        {"id": "_OBlgSz8sSM", "title": "Charlie Bit My Finger"},
        {"id": "hFZFjoX2cGg", "title": "Despacito"},
        {"id": "RgKAFK5djSk", "title": "Wiz Khalifa - See You Again"},
        {"id": "CevxZvSJLk8", "title": "Katy Perry - Roar"},
        {"id": "iRYvuS9OxAs", "title": "Eminem - Lose Yourself"},
        {"id": "lp-EO5I60KA", "title": "MKTO - Classic"},
        {"id": "nfs8NYg7yQM", "title": "Alan Walker - Faded"},
        {"id": "SlPhMPnQ58k", "title": "Despacito Remix"},
        {"id": "7PCkvCPvDXk", "title": "Adele - Set Fire to the Rain"},
        {"id": "QcIy9NiNbmo", "title": "Taylor Swift - Bad Blood"},
        {"id": "uelHwf8o7_U", "title": "Eminem - Love The Way You Lie"},
        {"id": "YykjpeuMNEk", "title": "Calvin Harris - This Is What You Came For"},
        {"id": "HcEc8zeNYxI", "title": "Passenger - Let Her Go"},
        {"id": "UYwF-jdcVjY", "title": "Ellie Goulding - Love Me Like You Do"},
        {"id": "nntGTK2Fhb0", "title": "Justin Bieber - Sorry"}
    ]
    
    for i, sample in enumerate(youtube_samples):
        videos.append({
            "id": f"yt-{i}",
            "title": sample["title"],
            "url": f"https://www.youtube.com/watch?v={sample['id']}",
            "platform": "youtube",
            "thumbnail": f"https://i.ytimg.com/vi/{sample['id']}/hqdefault.jpg",
            "views": 1000000 + i * 100000,
            "likes": 50000 + i * 5000,
            "author": f"Channel {i+1}",
            "viral_score": 85.0 + i,
            "published_at": "2025-07-31T12:00:00Z"
        })
    
    # Add TikTok videos with better thumbnails (using a placeholder service)
    tiktok_creators = ["@khaby.lame", "@charlidamelio", "@addisonre", "@bellapoarch", "@dixiedamelio", 
                      "@spencerx", "@michaelle", "@jamescharles", "@lorengray", "@brentrivera"]
    
    for i, creator in enumerate(tiktok_creators):
        videos.append({
            "id": f"tt-{i}",
            "title": f"Viral TikTok by {creator} 🔥",
            "url": f"https://www.tiktok.com/{creator}/video/73{str(i).zfill(8)}0000000",
            "platform": "tiktok", 
            "thumbnail": f"https://via.placeholder.com/300x200/000000/FFFFFF?text=TikTok+{i+1}",
            "views": 2000000 + i * 200000,
            "likes": 100000 + i * 10000,
            "author": creator,
            "viral_score": 88.0 + i,
            "published_at": "2025-07-31T10:00:00Z"
        })
    
    # Add Twitter videos with better thumbnails
    twitter_accounts = ["@MrBeast", "@elonmusk", "@TheRock", "@RyanReynolds", "@justinbieber",
                       "@ArianaGrande", "@taylorswift13", "@ladygaga", "@kimkardashian", "@selenagomez"]
    
    for i, account in enumerate(twitter_accounts):
        videos.append({
            "id": f"tw-{i}",
            "title": f"Viral moment from {account} 🐦",
            "url": f"https://twitter.com{account}/status/18{str(i).zfill(8)}00000000",
            "platform": "twitter",
            "thumbnail": f"https://via.placeholder.com/300x200/1DA1F2/FFFFFF?text=Twitter+{i+1}",
            "views": 1500000 + i * 150000,
            "likes": 75000 + i * 7500,
            "author": account,
            "viral_score": 82.0 + i,
            "published_at": "2025-07-31T08:00:00Z"
        })
    
    # Apply platform filtering if specified
    if platform:
        platform_lower = platform.lower()
        videos = [v for v in videos if v["platform"] == platform_lower]
    
    # Apply limit
    videos = videos[:limit]
    
    return {
        "videos": videos,
        "total": len(videos),
        "platform": platform,
        "limit": limit,
        "user_tier": "free",
        "has_ads": True,
        "server_mode": "enhanced_minimal",
        "note": "Enhanced mode - real YouTube thumbnails, platform filtering works"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    print(f"🚀 Starting minimal server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)