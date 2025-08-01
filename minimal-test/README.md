# Viral Daily - Video Aggregation Platform

A production-ready SaaS application for viral video aggregation.

## Features
- Multi-platform video aggregation (YouTube, TikTok, Twitter)
- User authentication and subscription management
- Payment processing integration
- Daily email notifications
- Responsive web interface

## Tech Stack
- **Backend**: FastAPI + MongoDB
- **Frontend**: React.js + Tailwind CSS
- **Payment**: PayPal integration
- **Notifications**: Email + SMS + Telegram

## Getting Started

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt

cd frontend  
npm install
```

2. Configure environment variables:
```bash
cp .env.example .env
# Fill in your API keys
```

3. Start the application:
```bash
# Backend
python backend/server.py

# Frontend
cd frontend
npm start
```

## Environment Variables

The application requires the following environment variables:
- `YOUTUBE_API_KEY` - YouTube Data API key
- `TWITTER_BEARER_TOKEN` - Twitter API bearer token
- `PAYPAL_CLIENT_ID` - PayPal client ID
- `PAYPAL_CLIENT_SECRET` - PayPal client secret
- `TELEGRAM_BOT_TOKEN` - Telegram bot token
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `SENDGRID_API_KEY` - SendGrid API key

## Deployment

The application is designed to be deployed on cloud platforms with environment variable support.