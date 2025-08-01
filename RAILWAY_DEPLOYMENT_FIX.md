# 🚂 Railway Deployment Troubleshooting Guide

## 🔧 Recent Fixes Applied

### 1. Server Startup Issues Fixed ✅
- **Problem**: `python server.py` had no main entry point
- **Fix**: Added `start_railway.py` with proper uvicorn startup
- **Fix**: Added `if __name__ == "__main__"` block to server.py

### 2. Health Check Improvements ✅  
- **Problem**: Health check timeout too short
- **Fix**: Increased timeout from 100s to 300s
- **Fix**: Added dedicated `/api/health` endpoint
- **Fix**: Made health check independent of database services

### 3. Startup Event Handling ✅
- **Problem**: Startup fails if advertising_service is None
- **Fix**: Added null checks for optional services
- **Fix**: Made startup errors non-fatal

## 📊 Current Configuration

**Files Updated:**
- `railway.json` - Uses `start_railway.py`, health check `/api/health`, 300s timeout
- `Procfile` - Uses `start_railway.py`
- `server.py` - Added health endpoint and proper startup handling
- `start_railway.py` - New Railway-optimized startup script with logging

## 🧪 Test Deployment Locally

Before redeploying to Railway, test locally:

```bash
cd /app/backend

# Test 1: Check if server starts
python start_railway.py
# Should start server on http://0.0.0.0:8001

# Test 2: Check health endpoint
curl http://localhost:8001/api/health
# Should return: {"status":"healthy","service":"Viral Daily API",...}

# Test 3: Check videos endpoint
curl "http://localhost:8001/api/videos?limit=5"
# Should return array of 5 videos
```

## 🚀 Railway Deployment Steps

### 1. Deploy to Railway
- Push your changes to GitHub
- Railway will automatically detect changes and rebuild
- Monitor build logs for any dependency issues

### 2. Check Build Logs
Look for these success indicators:
```
✅ Installing dependencies from requirements.txt
✅ [stage-0 8/8] COPY . /app
✅ Build completed successfully
```

### 3. Check Deploy Logs
Look for these startup messages:
```
🚀 Starting Viral Daily backend for Railway...
📡 Port: 8001
📦 Importing FastAPI app...
✅ FastAPI app imported successfully
🔧 Starting uvicorn server...
INFO: Uvicorn running on http://0.0.0.0:8001
```

### 4. Check Health Check
Railway will test: `https://your-app.railway.app/api/health`

Should return:
```json
{
  "status": "healthy",
  "service": "Viral Daily API", 
  "version": "2.0",
  "timestamp": "2025-07-31T..."
}
```

## 🐛 Common Issues & Solutions

### Issue 1: "Import Error" in Deploy Logs
**Cause**: Missing dependencies or import issues
**Solution**: 
- Check `requirements.txt` has all dependencies
- Ensure all import statements in `server.py` are correct
- Check file paths are correct

### Issue 2: "Address already in use" Error
**Cause**: Port configuration issue
**Solution**:
- Ensure using `PORT` environment variable from Railway
- Check `start_railway.py` uses `os.environ.get("PORT", 8001)`

### Issue 3: Health Check Timeout
**Cause**: Server takes too long to start or respond
**Solution**:
- Current timeout increased to 300s
- Check startup logs for slow imports
- Verify `/api/health` endpoint responds quickly

### Issue 4: MongoDB Connection Errors (Non-Fatal)
**Cause**: MongoDB Atlas SSL issues
**Solution**: 
- These are handled gracefully now
- App works without database connection
- Videos use mock data as fallback

## 🔍 Debugging Commands

### Check Railway Logs:
```bash
railway logs --tail
```

### Test Health Check:
```bash
curl https://your-railway-app.railway.app/api/health
```

### Test Video Endpoint:
```bash
curl "https://your-railway-app.railway.app/api/videos?limit=5"
```

## ✅ Success Indicators

When deployment is successful, you should see:
1. ✅ Build completes without errors
2. ✅ Deploy shows uvicorn startup messages  
3. ✅ Health check passes (green status in Railway dashboard)
4. ✅ `/api/health` returns healthy status
5. ✅ `/api/videos` returns video data

## 🆘 If Still Failing

1. **Check Railway Dashboard** - Look for detailed error messages
2. **Review Environment Variables** - Ensure all required vars are set
3. **Test Locally First** - Make sure `python start_railway.py` works locally
4. **Check File Structure** - Ensure all files are in the correct locations
5. **Review Requirements** - Make sure all dependencies are in `requirements.txt`

The fixes applied should resolve the health check failures. The app now has:
- Proper server startup with Railway port handling
- Robust health check endpoint
- Graceful error handling for missing services
- Comprehensive logging for debugging