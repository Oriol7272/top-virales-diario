# 🌐 Viral Daily Domain & Deployment Guide

## 🎯 STEP 1: REGISTER YOUR DOMAIN

### **Recommended Domain Names:**
- `viraldaily.com` ⭐ **BEST CHOICE**
- `viral-daily.com` 
- `viralvids.com`
- `dailyviral.com`
- `trendingnow.com`
- `viralwatch.com`

### **Best Domain Registrars (Cheapest 2025):**

| Registrar | .com Price | Features | Link |
|-----------|------------|----------|------|
| **Porkbun** ⭐ | $8.69/year | Free WHOIS privacy, best value | https://porkbun.com |
| **Namecheap** | $9.48/year | Easy to use, reliable | https://namecheap.com |
| **Cloudflare** | $9.95/year | At-cost pricing, no markup | https://cloudflare.com |
| **Google Domains** | $12/year | Google integration, transparent | https://domains.google |

**⭐ RECOMMENDED: Porkbun** (cheapest + free privacy protection)

## 🚀 STEP 2: DEPLOYMENT OPTIONS

### **OPTION A: VERCEL + HEROKU (Recommended)**

#### **Frontend (React) → Vercel:**
**Cost:** FREE for your needs
**Features:** 
- ✅ Automatic deployments from GitHub
- ✅ Custom domain support
- ✅ Free SSL certificate
- ✅ CDN worldwide
- ✅ Perfect for React apps

**Setup Commands:**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from your frontend folder
cd /app/frontend
vercel --prod

# Connect custom domain in Vercel dashboard
```

#### **Backend (FastAPI) → Heroku:**
**Cost:** $7/month (Eco dynos)
**Features:**
- ✅ Python/FastAPI support
- ✅ Environment variables
- ✅ Database connections
- ✅ Custom domain support

**Setup Files:**
```bash
# Create Procfile in /app/backend/
echo "web: uvicorn server:app --host=0.0.0.0 --port=\$PORT" > Procfile

# Create runtime.txt
echo "python-3.11" > runtime.txt

# Deploy to Heroku
git init
heroku create your-viral-daily-api
git add .
git commit -m "Deploy FastAPI backend"
git push heroku main
```

### **OPTION B: NETLIFY + RAILWAY (Alternative)**

#### **Frontend → Netlify:**
**Cost:** FREE
**Similar features to Vercel**

#### **Backend → Railway:**
**Cost:** $5/month
**Easy FastAPI deployment**

### **OPTION C: FULL STACK ON RENDER (Simplest)**

**Cost:** $7/month for backend, FREE for frontend
**Features:**
- ✅ Deploy both frontend and backend
- ✅ Automatic HTTPS
- ✅ Environment variables
- ✅ Database hosting

## 🎯 STEP 3: QUICK DEPLOYMENT CHECKLIST

### **Pre-Deployment Setup:**

#### **1. Update Frontend Environment:**
```javascript
// Update /app/frontend/.env
REACT_APP_BACKEND_URL=https://your-api-domain.herokuapp.com
```

#### **2. Update Backend for Production:**
```python
# Add to /app/backend/server.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Your actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### **3. Environment Variables Setup:**
```bash
# Set these on your hosting platform:
YOUTUBE_API_KEY=your_key
TWITTER_BEARER_TOKEN=your_token
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_secret
MONGO_URL=your_mongodb_connection
```

### **Deployment Steps:**

#### **Day 1: Get Domain & Setup**
1. ✅ Register domain on Porkbun ($8.69)
2. ✅ Create Vercel account
3. ✅ Create Heroku account
4. ✅ Push code to GitHub

#### **Day 2: Deploy Backend**
1. ✅ Deploy FastAPI to Heroku
2. ✅ Configure environment variables
3. ✅ Test API endpoints

#### **Day 3: Deploy Frontend** 
1. ✅ Update frontend config
2. ✅ Deploy React to Vercel
3. ✅ Connect custom domain
4. ✅ Configure DNS

#### **Day 4: Final Testing**
1. ✅ Test complete application
2. ✅ Verify all features work
3. ✅ Apply for Google AdSense!

## 💰 TOTAL DEPLOYMENT COST

### **Monthly Costs:**
- **Domain:** $0.72/month ($8.69/year)
- **Backend Hosting:** $7/month (Heroku)
- **Frontend Hosting:** $0 (Vercel free)
- **Total:** ~$8/month

### **One-Time Setup:**
- **Domain Registration:** $8.69
- **Setup Time:** 2-3 hours

## 🎯 RECOMMENDED QUICK START

### **FASTEST DEPLOYMENT: 1-Day Setup**

**Use This Exact Plan:**

1. **Morning:** Register `viraldaily.com` on Porkbun
2. **Afternoon:** Deploy backend to Heroku 
3. **Evening:** Deploy frontend to Vercel + connect domain

**By tomorrow, you'll have:**
- ✅ `https://viraldaily.com` fully functional
- ✅ Custom domain for AdSense approval
- ✅ Professional deployment
- ✅ Ready to apply for AdSense immediately

## 🚀 ALTERNATIVE: EMERGENCY QUICK DOMAIN

**If you want to start TODAY:**

### **Use GitHub Pages + Custom Domain:**
1. Buy domain now: Porkbun.com
2. Deploy to GitHub Pages (free)
3. Connect domain immediately
4. Apply for AdSense today!

**Total time:** 2 hours
**Total cost:** $8.69 domain only

---

## 📞 NEED HELP?

Choose your deployment strategy:
1. **Professional** (Vercel + Heroku) = Best performance
2. **Budget** (GitHub Pages) = Fastest & cheapest  
3. **Easiest** (Render) = Simplest setup

**Ready to get your domain and deploy? Pick your strategy!** 🚀