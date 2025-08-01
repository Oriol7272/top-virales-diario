#!/usr/bin/env python3
"""
Railway-optimized startup for full Viral Daily server with detailed debugging
"""
import os
import sys
import logging
import time

# Setup detailed logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def test_full_server_import():
    """Test if we can import the full server"""
    try:
        logger.info("🧪 Testing full server import...")
        
        # Test individual imports
        logger.info("📦 Testing core dependencies...")
        import fastapi
        logger.info(f"   ✅ FastAPI: {fastapi.__version__}")
        
        import uvicorn
        logger.info(f"   ✅ Uvicorn: {uvicorn.__version__}")
        
        import pydantic
        logger.info(f"   ✅ Pydantic: {pydantic.__version__}")
        
        # Test our modules
        logger.info("📦 Testing application modules...")
        
        import models
        logger.info("   ✅ Models imported")
        
        import subscription_plans
        logger.info("   ✅ Subscription plans imported")
        
        # Import the main server
        logger.info("📦 Importing main server application...")
        from server import app
        logger.info("   ✅ Server app imported successfully")
        
        # Test app properties
        logger.info(f"   📊 App routes: {len(app.routes)}")
        logger.info(f"   📊 App middleware: {len(app.user_middleware)}")
        
        return app
        
    except Exception as e:
        logger.error(f"❌ Full server import failed: {e}")
        import traceback
        logger.error(f"📋 Full traceback:\n{traceback.format_exc()}")
        return None

def main():
    """Start the full Viral Daily server with extensive debugging"""
    try:
        # Get port from Railway
        port = int(os.environ.get("PORT", 8001))
        logger.info(f"🚀 Starting Full Viral Daily Server on port {port}")
        
        # Environment info
        logger.info(f"📁 Working directory: {os.getcwd()}")
        logger.info(f"📁 Python executable: {sys.executable}")
        logger.info(f"📁 Python version: {sys.version}")
        logger.info(f"📁 Python path: {sys.path[:3]}...")  # First 3 entries
        
        # List available Python files
        py_files = [f for f in os.listdir('.') if f.endswith('.py')]
        logger.info(f"📁 Available Python files: {py_files}")
        
        # Set working directory
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        if os.getcwd() != backend_dir:
            os.chdir(backend_dir)
            logger.info(f"📁 Changed to: {os.getcwd()}")
        
        # Add to Python path
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
            logger.info(f"📁 Added to Python path: {backend_dir}")
        
        # Test full server import
        app = test_full_server_import()
        
        if app is None:
            logger.error("❌ Full server import failed, falling back to minimal server")
            raise ImportError("Full server import failed")
        
        # Success! Start the full server
        logger.info("🎯 Full server loaded successfully!")
        logger.info("🎯 Features available:")
        logger.info("   - Real YouTube API integration")
        logger.info("   - Platform filtering (YouTube/TikTok/Twitter)")
        logger.info("   - User authentication & subscriptions")
        logger.info("   - PayPal payment integration")
        logger.info("   - Analytics & advertising system")
        logger.info("   - Email notifications")
        
        # Start uvicorn
        logger.info("🔧 Starting uvicorn with full server...")
        import uvicorn
        
        # Give it a moment to initialize
        time.sleep(2)
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True,
            timeout_keep_alive=60
        )
        
    except ImportError as ie:
        logger.error(f"❌ Import error in full server: {ie}")
        logger.error("📋 Falling back to minimal server...")
        
        # Fallback to minimal server
        try:
            logger.info("🔄 Loading minimal server as fallback...")
            from server_minimal import app as minimal_app
            logger.info("✅ Minimal server loaded successfully")
            
            import uvicorn
            uvicorn.run(
                minimal_app, 
                host="0.0.0.0", 
                port=port,
                log_level="info"
            )
        except Exception as fe:
            logger.error(f"❌ Fallback to minimal server failed: {fe}")
            logger.error("🆘 Complete system failure - exiting")
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        import traceback
        logger.error(f"📋 Full traceback:\n{traceback.format_exc()}")
        
        # Last resort fallback
        logger.info("🆘 Attempting emergency minimal server startup...")
        try:
            from server_minimal import app as minimal_app
            import uvicorn
            uvicorn.run(minimal_app, host="0.0.0.0", port=port)
        except:
            logger.error("🆘 Emergency startup failed - system unusable")
            sys.exit(1)

if __name__ == "__main__":
    main()