#!/usr/bin/env python3
"""
Full Server Direct Startup - All Advanced Features Enabled
"""
import os
import sys
import logging

# Setup comprehensive logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Launch the complete Viral Daily full server with all features"""
    try:
        port = int(os.environ.get("PORT", 8001))
        logger.info(f"🚀 LAUNCHING FULL VIRAL DAILY SERVER - PORT {port}")
        
        # Set working directory
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(backend_dir)
        
        # Add to Python path
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        logger.info("🎯 FULL SERVER FEATURES LOADING:")
        logger.info("   ⚡ Real YouTube API Integration")
        logger.info("   ⚡ Real Twitter API Integration") 
        logger.info("   ⚡ User Authentication System")
        logger.info("   ⚡ MongoDB Database Integration")
        logger.info("   ⚡ PayPal Payment Processing")
        logger.info("   ⚡ SendGrid Email Notifications")
        logger.info("   ⚡ Advanced Analytics Dashboard")
        logger.info("   ⚡ AI-Powered Recommendations")
        logger.info("   ⚡ Creator Tools & Brand Partnerships")
        
        # Import the complete server
        logger.info("📦 Importing full server application...")
        from server import app
        logger.info("✅ FULL SERVER LOADED SUCCESSFULLY")
        
        # Start with all features
        logger.info("🔧 Starting uvicorn with complete feature set...")
        import uvicorn
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True,
            timeout_keep_alive=120
        )
        
    except Exception as e:
        logger.error(f"❌ Full server startup failed: {e}")
        import traceback
        logger.error(f"📋 Full traceback:\n{traceback.format_exc()}")
        
        # Emergency fallback - keep the hybrid server running
        logger.info("🔄 EMERGENCY FALLBACK - Starting hybrid server...")
        try:
            from server_hybrid import app as hybrid_app
            import uvicorn
            uvicorn.run(hybrid_app, host="0.0.0.0", port=port, log_level="info")
        except Exception as fe:
            logger.error(f"❌ Emergency fallback failed: {fe}")
            sys.exit(1)

if __name__ == "__main__":
    main()