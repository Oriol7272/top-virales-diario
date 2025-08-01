#!/usr/bin/env python3
"""
Railway-optimized startup script for Viral Daily backend
"""
import os
import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for Railway deployment"""
    try:
        logger.info("🚀 Starting Viral Daily backend for Railway...")
        
        # Check environment
        port = int(os.environ.get("PORT", 8001))
        logger.info(f"📡 Port: {port}")
        
        # Log current directory and files
        logger.info(f"📁 Current directory: {os.getcwd()}")
        logger.info(f"📁 Files: {list(Path('.').glob('*.py'))[:10]}")
        
        # Import the FastAPI app
        logger.info("📦 Importing FastAPI app...")
        from server import app
        logger.info("✅ FastAPI app imported successfully")
        
        # Import and run uvicorn
        logger.info("🔧 Starting uvicorn server...")
        import uvicorn
        uvicorn.run(
            "server:app", 
            host="0.0.0.0", 
            port=port, 
            reload=False,
            access_log=True,
            log_level="info"
        )
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error(f"📁 Python path: {sys.path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()