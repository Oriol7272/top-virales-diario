#!/usr/bin/env python3
"""
Reliable Railway startup for Viral Daily
"""
import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Start the Viral Daily server"""
    try:
        # Get port from Railway
        port = int(os.environ.get("PORT", 8001))
        logger.info(f"🚀 Starting Viral Daily on port {port}")
        
        # Change to the correct directory
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(backend_dir)
        
        logger.info(f"📁 Working directory: {os.getcwd()}")
        logger.info(f"📁 Files available: {[f for f in os.listdir('.') if f.endswith('.py')]}")
        
        # Add current directory to Python path
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        # Import the server app
        logger.info("📦 Importing server app...")
        from server import app
        logger.info("✅ Server app imported successfully")
        
        # Start uvicorn
        logger.info("🔧 Starting uvicorn server...")
        import uvicorn
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
        
    except ImportError as ie:
        logger.error(f"❌ Import error: {ie}")
        logger.error(f"📋 Python path: {sys.path}")
        logger.error(f"📋 Available modules: {[f[:-3] for f in os.listdir('.') if f.endswith('.py')]}")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"❌ Failed to start: {e}")
        import traceback
        logger.error(f"📋 Full traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()