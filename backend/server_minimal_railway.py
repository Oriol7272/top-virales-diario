#!/usr/bin/env python3
"""
Ultra-minimal FastAPI server for Railway - starts instantly
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Viral Daily API Quick Start")

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
        "message": "Viral Daily API - Quick Start Mode",
        "status": "healthy",
        "note": "Full features loading..."
    }

@app.get("/api/videos")
async def get_videos_minimal():
    """Minimal video endpoint for testing"""
    mock_videos = [
        {
            "id": "quick-1",
            "title": "Sample Video 1",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "platform": "youtube",
            "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
            "views": 1000000,
            "likes": 50000,
            "author": "Test Channel",
            "viral_score": 85.0
        },
        {
            "id": "quick-2", 
            "title": "Sample Video 2",
            "url": "https://www.tiktok.com/@test/video/123",
            "platform": "tiktok",
            "thumbnail": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzAwMCI+PHRleHQgeD0iMTUwIiB5PSIxMDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IndoaXRlIj5UaWtUb2s8L3RleHQ+PC9zdmc+",
            "views": 2000000,
            "likes": 100000,
            "author": "@testuser",
            "viral_score": 92.0
        }
    ]
    
    return {
        "videos": mock_videos,
        "total": len(mock_videos),
        "user_tier": "free",
        "has_ads": True,
        "note": "Minimal mode - full features loading in background"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    print(f"🚀 Starting minimal server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, access_log=False)