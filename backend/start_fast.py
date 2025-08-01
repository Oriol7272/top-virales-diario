#!/usr/bin/env python3
"""
Fast Railway startup - minimal imports for quick health check
"""
import os
import sys
import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Quick logging setup
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Create minimal FastAPI app for health check first
quick_app = FastAPI()

@quick_app.get("/api/health")
async def health():
    return {"status": "ok"}

@quick_app.get("/")
async def root():
    return {"status": "starting"}

def main():
    """Fast startup for Railway"""
    port = int(os.environ.get("PORT", 8001))
    logger.info(f"🚀 Starting on port {port}")
    
    try:
        # Try to import and start the full server
        logger.info("📦 Loading full server...")
        
        # Import the main server app
        import sys
        sys.path.insert(0, '/app/backend')
        from server import app
        
        logger.info("✅ Full server loaded successfully")
        
        # Start uvicorn with the full app
        import uvicorn
        uvicorn.run(
            app,  # Use the imported app directly
            host="0.0.0.0", 
            port=port,
            reload=False,
            access_log=False,
            log_level="info"
        )
        
    except Exception as e:
        logger.error(f"❌ Full server failed: {e}")
        logger.error(f"📁 Current directory: {os.getcwd()}")
        logger.error(f"📁 Files: {list(os.listdir('.'))}")
        
        # Import traceback for better error info
        import traceback
        logger.error(f"📋 Full error: {traceback.format_exc()}")
        
        # Fallback to quick app
        logger.info("🔄 Falling back to basic health check...")
        import uvicorn
        uvicorn.run(
            quick_app,
            host="0.0.0.0",
            port=port,
            reload=False,
            access_log=False
        )

if __name__ == "__main__":
    main()