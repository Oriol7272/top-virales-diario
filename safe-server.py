"""
Viral Daily - Video Aggregation API
Sanitized version for GitHub
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List, Optional

app = FastAPI(title="Viral Daily API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic models
class VideoItem:
    def __init__(self, id: str, title: str, platform: str, views: int):
        self.id = id
        self.title = title
        self.platform = platform  
        self.views = views

class VideoAggregator:
    """Video aggregation service"""
    
    def __init__(self):
        self.api_configured = bool(os.getenv('VIDEO_API_KEY'))
    
    async def get_trending_videos(self, platform: str = None, limit: int = 10) -> List[VideoItem]:
        """Fetch trending videos from platforms"""
        videos = []
        
        # Sample video data structure
        sample_videos = [
            VideoItem("1", "Trending Video 1", "youtube", 1000000),
            VideoItem("2", "Viral Content 2", "tiktok", 2000000), 
            VideoItem("3", "Popular Post 3", "twitter", 500000),
        ]
        
        return sample_videos[:limit]

# Initialize services
aggregator = VideoAggregator()

@app.get("/")
async def root():
    return {"message": "Viral Daily API", "status": "active"}

@app.get("/api/videos")
async def get_videos(platform: str = None, limit: int = 10):
    """Get viral videos endpoint"""
    try:
        videos = await aggregator.get_trending_videos(platform, limit)
        return {
            "status": "success",
            "videos": [vars(v) for v in videos],
            "total": len(videos)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "api_configured": aggregator.api_configured}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)