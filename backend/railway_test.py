#!/usr/bin/env python3
"""
Railway deployment test - minimal working server
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Set required environment variables
os.environ.setdefault('MONGO_URL', 'mongodb+srv://rail:P2aqBClf1CfSV2jy@cluster0.2saqg1m.mongodb.net/viral_daily')
os.environ.setdefault('DB_NAME', 'viral_daily')

app = FastAPI(title="Viral Daily Test")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Viral Daily API is running"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "dependencies": "minimal"}

@app.get("/api/videos")
async def get_videos():
    # Return mock data that works
    mock_videos = [
        {
            "id": "test-1",
            "title": "Rick Astley - Never Gonna Give You Up",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
            "platform": "youtube",
            "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
            "views": 1400000000,
            "likes": 15000000,
            "author": "Rick Astley",
            "viral_score": 95.0
        },
        {
            "id": "test-2", 
            "title": "This transition hit different 🔥",
            "url": "https://www.tiktok.com/@khaby.lame/video/7349850239266458672",
            "platform": "tiktok",
            "thumbnail": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCI+PC9zdmc+",
            "views": 47300000,
            "likes": 8900000,
            "author": "@khaby.lame",
            "viral_score": 88.0
        },
        {
            "id": "test-3",
            "title": "I'm giving away $1,000,000 to random followers! 💰", 
            "url": "https://twitter.com/MrBeast/status/1816797864340054018",
            "platform": "twitter",
            "thumbnail": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCI+PC9zdmc+",
            "views": 12800000,
            "likes": 2100000,
            "author": "@MrBeast",
            "viral_score": 92.0
        }
    ]
    
    return {
        "videos": mock_videos,
        "total": len(mock_videos),
        "has_ads": True,
        "user_tier": "free"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)