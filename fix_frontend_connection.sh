#!/bin/bash
# Quick fix for frontend-backend connection

echo "🔧 FIXING FRONTEND-BACKEND CONNECTION"
echo "====================================="

# Get Railway backend URL
echo "Enter your Railway backend URL (e.g., https://your-app.railway.app):"
read -r RAILWAY_URL

# Remove trailing slash
RAILWAY_URL=${RAILWAY_URL%/}

# Update frontend .env
echo "📝 Updating frontend/.env..."
cat > /app/frontend/.env << EOF
REACT_APP_BACKEND_URL=${RAILWAY_URL}
WDS_SOCKET_PORT=443
EOF

echo "✅ Updated frontend/.env:"
cat /app/frontend/.env

echo ""
echo "🚀 NEXT STEPS:"
echo "1. Push changes to GitHub"
echo "2. Vercel will auto-redeploy frontend"
echo "3. Test connection with debug script:"
echo "   python debug_connection.py ${RAILWAY_URL} https://your-vercel-app.vercel.app"

echo ""
echo "🧪 TEST BACKEND NOW:"
echo "curl ${RAILWAY_URL}/api/videos?limit=3"