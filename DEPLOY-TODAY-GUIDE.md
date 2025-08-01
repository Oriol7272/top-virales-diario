# 🚨 EMERGENCY DEPLOYMENT: GET VIRALDAILY.COM ONLINE TODAY

## ⚡ STEP 1: REGISTER DOMAIN (5 minutes)

### **Register viraldaily.com NOW:**
1. **Go to Porkbun**: https://porkbun.com
2. **Search**: "viraldaily.com"
3. **Add to cart** ($8.69/year)
4. **Checkout** with free WHOIS privacy
5. **Complete purchase**

**⏰ Time: 5 minutes | Cost: $8.69**

---

## 🚀 STEP 2: PREPARE CODE FOR DEPLOYMENT (10 minutes)

### **Update Frontend Configuration:**
```bash
# Update frontend/.env
REACT_APP_BACKEND_URL=https://viral-daily-api.up.railway.app
```

### **Create Deployment Files:**

**Create /app/backend/Procfile:**
```
web: uvicorn server:app --host=0.0.0.0 --port=$PORT
```

**Create /app/backend/railway.json:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn server:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## 🎯 STEP 3: DEPLOY BACKEND (15 minutes)

### **Railway Deployment:**
1. **Go to Railway**: https://railway.app
2. **Sign up** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Connect** your viral-daily repo
5. **Select backend folder** as root
6. **Add Environment Variables**:
   ```
   YOUTUBE_API_KEY=AIzaSyDyuMNfrJXOMk4lCwJ7GV70zEP6iwrISuY
   TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAHvz3AEAAAAAJw0iwGwsf9pfwVgck2PfPPgzyw4%3DJsAxonP1Ro3704DcVsoXd2mwiD95EdAPuYWGtDiltkhPBjXVRM
   PAYPAL_CLIENT_ID=BAAjUw1nb84moRC0rrJOZtICaamy0n3pn_wL_qsvsw7w8fE8P6bKNU9cmWVmnkzwj5DJHkYU-nyM2wZtqI
   PAYPAL_CLIENT_SECRET=EH-bT6nhSkK6BC108r5FZtNlj7Aco84tpSdltaHxPvvpG8l9ltTdgpsJtx_4J2IOPknVbN-EB6URfUMd
   MONGO_URL=mongodb+srv://your-connection-string
   ```
7. **Deploy** and get your API URL

**⏰ Time: 15 minutes | Cost: $5/month**

---

## 🎨 STEP 4: DEPLOY FRONTEND (10 minutes)

### **Vercel Deployment:**
1. **Go to Vercel**: https://vercel.com
2. **Sign up** with GitHub
3. **Import Project** from GitHub
4. **Select** viral-daily repo
5. **Set root directory** to `frontend`
6. **Add Environment Variable**:
   ```
   REACT_APP_BACKEND_URL=https://your-railway-api-url.railway.app
   ```
7. **Deploy**

**⏰ Time: 10 minutes | Cost: FREE**

---

## 🌐 STEP 5: CONNECT DOMAIN (15 minutes)

### **Connect viraldaily.com to Vercel:**

1. **In Vercel Dashboard**:
   - Go to your project
   - Click **Settings** → **Domains**
   - Add **viraldaily.com**
   - Add **www.viraldaily.com**

2. **In Porkbun Dashboard**:
   - Go to **DNS** for your domain
   - Delete existing A records
   - Add these records:
   ```
   Type: A     Name: @     Value: 76.76.19.19
   Type: A     Name: www   Value: 76.76.19.19
   Type: CNAME Name: @     Value: cname.vercel-dns.com
   ```

3. **Wait 10-30 minutes** for DNS propagation

**⏰ Time: 15 minutes | Wait: 30 minutes for DNS**

---

## ✅ STEP 6: VERIFY & TEST (5 minutes)

### **Test Your Live Site:**
1. **Visit**: https://viraldaily.com
2. **Check**: All videos load correctly
3. **Test**: Platform filtering works
4. **Verify**: Subscription system functional
5. **Confirm**: AdSense placeholders visible

---

## 🎯 TOTAL TIMELINE TODAY:

- ✅ **Register Domain**: 5 minutes
- ✅ **Prepare Code**: 10 minutes  
- ✅ **Deploy Backend**: 15 minutes
- ✅ **Deploy Frontend**: 10 minutes
- ✅ **Connect Domain**: 15 minutes
- ⏳ **DNS Wait**: 30 minutes
- ✅ **Testing**: 5 minutes

**TOTAL: 1.5 hours + 30 min DNS wait = 2 hours**

---

## 💰 COSTS:

- **Domain**: $8.69/year
- **Railway**: $5/month
- **Vercel**: FREE
- **Total**: $8.69 today, then $5/month

---

## 🚨 EMERGENCY BACKUP PLAN:

**If Railway is slow, use Render:**
1. **Render.com** - Same process
2. **Deploy backend** in 10 minutes
3. **Same frontend setup**

---

## 📞 WHAT TO DO RIGHT NOW:

1. **REGISTER DOMAIN**: Go to Porkbun.com immediately
2. **Create accounts**: Railway.app and Vercel.com
3. **Follow steps above** in order
4. **By tonight**: Your site will be live at https://viraldaily.com

**🎉 TOMORROW: Apply for Google AdSense with your real domain!**

---

## ✅ SUCCESS CRITERIA:

By end of today you will have:
- ✅ viraldaily.com registered and owned by you
- ✅ Backend API running on Railway
- ✅ Frontend running on Vercel  
- ✅ Custom domain connected
- ✅ All features working (videos, payments, ads)
- ✅ Ready for AdSense application tomorrow!

**GO REGISTER THE DOMAIN NOW! 🚀**