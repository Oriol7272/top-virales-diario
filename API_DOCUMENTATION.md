# Viral Daily API Documentation

## Overview

The Viral Daily API provides access to the world's most viral videos from YouTube, TikTok, and Twitter, aggregated daily with advanced filtering and analytics capabilities. Our API is designed for developers, content creators, and businesses who want to integrate viral content into their applications.

## Base URL
```
https://your-domain.com/api
```

## Authentication

### API Key Authentication
All API requests require authentication using an API key in the header:

```http
Authorization: Bearer YOUR_API_KEY
```

### Getting Your API Key
1. Sign up for a Pro or Business account at [Viral Daily](https://your-domain.com)
2. Navigate to your dashboard
3. Generate your API key in the Developer section
4. Use this key in all API requests

## Subscription Tiers & Limits

| Tier | Price | Videos/Day | API Calls/Month | Features |
|------|--------|------------|-----------------|----------|
| Free | $0 | 40 | 0 | Web access only |
| Pro | $9.99 | 100 | 1,000+ | API access, No ads |
| Business | $29.99 | Unlimited | 10,000+ | Full API, Analytics |

## Endpoints

### 1. Video Aggregation

#### Get Viral Videos
Retrieve the latest viral videos from all platforms or specific platforms.

```http
GET /videos
```

**Parameters:**
- `platform` (optional): Filter by platform (`youtube`, `tiktok`, `twitter`)
- `limit` (optional): Number of videos to return (default: based on subscription tier)
- `date` (optional): Date filter in YYYY-MM-DD format

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     "https://your-domain.com/api/videos?platform=youtube&limit=10"
```

**Example Response:**
```json
{
  "videos": [
    {
      "id": "video_123",
      "title": "Amazing Viral Video",
      "url": "https://youtube.com/watch?v=abc123",
      "thumbnail": "https://img.youtube.com/vi/abc123/maxresdefault.jpg",
      "platform": "youtube",
      "viral_score": 95.7,
      "engagement_rate": 12.3,
      "view_count": 2500000,
      "created_at": "2025-01-13T10:30:00Z",
      "description": "This video is going viral...",
      "creator": "Content Creator Name",
      "duration": 180
    }
  ],
  "total": 10,
  "user_tier": "pro",
  "has_ads": false,
  "premium_features_available": true
}
```

#### Get Platform-Specific Videos
Get videos from a specific platform only.

```http
GET /videos?platform={platform}
```

**Supported Platforms:**
- `youtube` - YouTube videos
- `tiktok` - TikTok videos  
- `twitter` - Twitter/X videos

### 2. Analytics (Business Tier Only)

#### Get Video Analytics
Retrieve detailed analytics for viral videos.

```http
GET /analytics/videos
```

**Example Response:**
```json
{
  "analytics": {
    "total_videos_tracked": 1250,
    "average_viral_score": 78.5,
    "platform_breakdown": {
      "youtube": { "count": 500, "avg_score": 82.1 },
      "tiktok": { "count": 400, "avg_score": 75.8 },
      "twitter": { "count": 350, "avg_score": 79.2 }
    },
    "trending_topics": ["viral dance", "tech news", "comedy"],
    "engagement_trends": {
      "daily_average": 125000,
      "peak_hour": "15:00",
      "top_engagement_platform": "youtube"
    }
  }
}
```

### 3. Subscription Management

#### Get Subscription Plans
Retrieve available subscription plans and pricing.

```http
GET /subscription/plans
```

**Example Response:**
```json
{
  "plans": [
    {
      "tier": "free",
      "price_monthly": 0,
      "price_yearly": 0,
      "max_videos_per_day": 40,
      "api_access": false,
      "features": [
        "40 viral videos per day",
        "Web access",
        "Platform filtering",
        "Basic search"
      ]
    },
    {
      "tier": "pro",
      "price_monthly": 9.99,
      "price_yearly": 99.99,
      "max_videos_per_day": 100,
      "api_access": true,
      "features": [
        "100 viral videos per day",
        "Full API access",
        "No advertisements",
        "Email notifications",
        "1,000+ API calls per month"
      ]
    },
    {
      "tier": "business",
      "price_monthly": 29.99,
      "price_yearly": 299.99,
      "max_videos_per_day": -1,
      "api_access": true,
      "features": [
        "Unlimited viral videos",
        "Full API access",
        "Advanced analytics",
        "Priority support",
        "10,000+ API calls per month",
        "Brand partnership opportunities"
      ]
    }
  ]
}
```

## Code Examples

### JavaScript/Node.js
```javascript
const axios = require('axios');

const apiKey = 'YOUR_API_KEY';
const baseURL = 'https://your-domain.com/api';

// Get viral videos
async function getViralVideos(platform = null, limit = 20) {
  try {
    const params = { limit };
    if (platform) params.platform = platform;
    
    const response = await axios.get(`${baseURL}/videos`, {
      headers: {
        'Authorization': `Bearer ${apiKey}`
      },
      params
    });
    
    return response.data;
  } catch (error) {
    console.error('Error fetching videos:', error.response?.data || error.message);
  }
}

// Usage
getViralVideos('youtube', 10).then(data => {
  console.log(`Found ${data.videos.length} viral YouTube videos`);
  data.videos.forEach(video => {
    console.log(`${video.title} - Score: ${video.viral_score}`);
  });
});
```

### Python
```python
import requests

class ViralDailyAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://your-domain.com/api'
        self.headers = {'Authorization': f'Bearer {api_key}'}
    
    def get_videos(self, platform=None, limit=20):
        params = {'limit': limit}
        if platform:
            params['platform'] = platform
            
        response = requests.get(
            f'{self.base_url}/videos',
            headers=self.headers,
            params=params
        )
        return response.json()
    
    def get_analytics(self):
        response = requests.get(
            f'{self.base_url}/analytics/videos',
            headers=self.headers
        )
        return response.json()

# Usage
api = ViralDailyAPI('YOUR_API_KEY')
videos = api.get_videos(platform='tiktok', limit=5)
print(f"Found {len(videos['videos'])} viral TikTok videos")
```

### PHP
```php
<?php
class ViralDailyAPI {
    private $apiKey;
    private $baseUrl = 'https://your-domain.com/api';
    
    public function __construct($apiKey) {
        $this->apiKey = $apiKey;
    }
    
    public function getVideos($platform = null, $limit = 20) {
        $url = $this->baseUrl . '/videos';
        $params = ['limit' => $limit];
        
        if ($platform) {
            $params['platform'] = $platform;
        }
        
        $url .= '?' . http_build_query($params);
        
        $context = stream_context_create([
            'http' => [
                'header' => "Authorization: Bearer " . $this->apiKey
            ]
        ]);
        
        $response = file_get_contents($url, false, $context);
        return json_decode($response, true);
    }
}

// Usage
$api = new ViralDailyAPI('YOUR_API_KEY');
$videos = $api->getVideos('youtube', 15);
echo "Found " . count($videos['videos']) . " viral YouTube videos\n";
?>
```

## Error Handling

The API uses conventional HTTP response codes to indicate success or failure:

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (invalid API key)
- `403` - Forbidden (insufficient subscription tier)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error

**Error Response Format:**
```json
{
  "error": {
    "code": 403,
    "message": "API access requires Pro or Business subscription",
    "details": "Upgrade at https://your-domain.com/pricing"
  }
}
```

## Rate Limiting

API calls are limited based on your subscription tier:

- **Pro Tier**: 1,000+ calls per month (≈33 per day)
- **Business Tier**: 10,000+ calls per month (≈333 per day)

Rate limit headers are included in all responses:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1673635200
```

## Webhooks (Business Tier)

Get real-time notifications when new viral videos are detected.

### Setup Webhook
```http
POST /webhooks
```

**Request Body:**
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["video.new", "video.viral_threshold"],
  "filters": {
    "platforms": ["youtube", "tiktok"],
    "min_viral_score": 80
  }
}
```

**Webhook Payload:**
```json
{
  "event": "video.new",
  "timestamp": "2025-01-13T10:30:00Z",
  "data": {
    "video": {
      "id": "video_456",
      "title": "Breaking: New Viral Sensation",
      "platform": "tiktok",
      "viral_score": 87.5,
      "url": "https://tiktok.com/@user/video/123"
    }
  }
}
```

## Best Practices

### 1. Optimize API Usage
- Cache responses when possible to reduce API calls
- Use appropriate `limit` parameters to avoid over-fetching
- Implement exponential backoff for retries

### 2. Handle Rate Limits
```javascript
async function makeAPICallWithRetry(apiCall, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await apiCall();
    } catch (error) {
      if (error.response?.status === 429) {
        const waitTime = Math.pow(2, i) * 1000; // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, waitTime));
        continue;
      }
      throw error;
    }
  }
}
```

### 3. Monitor Your Usage
Track your API usage to optimize costs:
```javascript
// Check remaining quota
function checkQuota(response) {
  const remaining = response.headers['x-ratelimit-remaining'];
  if (remaining < 100) {
    console.warn(`Low API quota: ${remaining} calls remaining`);
  }
}
```

## SDKs and Libraries

### Official SDKs
- **JavaScript/TypeScript**: `npm install viral-daily-sdk`
- **Python**: `pip install viral-daily-python`
- **PHP**: `composer require viral-daily/php-sdk`

### Community Libraries
- **Go**: `github.com/community/viral-daily-go`
- **Ruby**: `gem install viral-daily-ruby`
- **Java**: `maven: com.viral-daily:java-sdk`

## Support

- **Documentation**: [https://docs.viral-daily.com](https://docs.viral-daily.com)
- **API Status**: [https://status.viral-daily.com](https://status.viral-daily.com)
- **Developer Support**: [support@viral-daily.com](mailto:support@viral-daily.com)
- **Discord Community**: [https://discord.gg/viral-daily](https://discord.gg/viral-daily)

## Changelog

### v2.0 (January 2025)
- Added viral_score and engagement_rate to video responses
- Introduced Business tier with advanced analytics
- Added webhook support for real-time notifications
- Improved rate limiting with per-tier quotas

### v1.5 (December 2024)
- Added Twitter/X platform support
- Enhanced video metadata with creator information
- Implemented subscription-based access control

### v1.0 (October 2024)
- Initial API release
- YouTube and TikTok video aggregation
- Basic authentication and rate limiting

---

*Start building with viral content today! Sign up at [Viral Daily](https://your-domain.com) and get your API key.*