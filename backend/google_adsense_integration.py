"""
Google AdSense Integration for Viral Daily
Maximize advertising revenue with strategic ad placement
"""

from typing import List, Dict, Any, Optional
import os
import logging
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import User, SubscriptionTier
import asyncio

logger = logging.getLogger(__name__)

class GoogleAdSenseService:
    """Service for Google AdSense ad management and optimization"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.adsense_publisher_id = os.getenv('GOOGLE_ADSENSE_PUBLISHER_ID', 'pub-YOUR_PUBLISHER_ID')
        self.adsense_client_id = os.getenv('GOOGLE_ADSENSE_CLIENT_ID')
        
    def generate_adsense_ad_units(self, page_type: str = "homepage", user: Optional[User] = None) -> List[Dict[str, Any]]:
        """Generate optimized AdSense ad units for maximum revenue"""
        
        # Premium users don't see ads
        if user and user.subscription_tier != SubscriptionTier.FREE:
            return []
        
        ad_units = []
        
        if page_type == "homepage":
            # High-revenue ad placements for homepage
            ad_units = [
                {
                    "placement": "header_banner",
                    "type": "display",
                    "size": "728x90",  # Leaderboard - highest CPM
                    "code": self._generate_adsense_code("header_banner_728x90", "728x90"),
                    "revenue_potential": "$2-8 CPM",
                    "position": "top"
                },
                {
                    "placement": "sidebar_rectangle", 
                    "type": "display",
                    "size": "300x250",  # Medium Rectangle - high performance
                    "code": self._generate_adsense_code("sidebar_rect_300x250", "300x250"),
                    "revenue_potential": "$1-5 CPM",
                    "position": "right_sidebar"
                },
                {
                    "placement": "in_content_native",
                    "type": "native", 
                    "size": "responsive",
                    "code": self._generate_adsense_native_code("in_content_native"),
                    "revenue_potential": "$3-12 CPM",  # Native ads perform best
                    "position": "between_videos"
                },
                {
                    "placement": "footer_banner",
                    "type": "display",
                    "size": "320x100",  # Mobile banner
                    "code": self._generate_adsense_code("footer_mobile_320x100", "320x100"),
                    "revenue_potential": "$1-4 CPM",
                    "position": "footer"
                }
            ]
        
        elif page_type == "video_detail":
            # Video page specific ads
            ad_units = [
                {
                    "placement": "pre_video",
                    "type": "video",
                    "size": "responsive", 
                    "code": self._generate_adsense_video_code("pre_video_ad"),
                    "revenue_potential": "$5-20 CPM",  # Video ads highest revenue
                    "position": "before_video"
                },
                {
                    "placement": "related_content",
                    "type": "native",
                    "size": "responsive",
                    "code": self._generate_adsense_native_code("related_content"),
                    "revenue_potential": "$2-8 CPM",
                    "position": "related_videos"
                }
            ]
        
        return ad_units
    
    def _generate_adsense_code(self, slot_name: str, size: str) -> str:
        """Generate AdSense display ad code"""
        slot_id = self._get_ad_slot_id(slot_name)
        
        return f'''
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={self.adsense_publisher_id}"
                crossorigin="anonymous"></script>
        <!-- {slot_name} -->
        <ins class="adsbygoogle"
             style="display:inline-block;width:{size.split('x')[0]}px;height:{size.split('x')[1]}px"
             data-ad-client="{self.adsense_publisher_id}"
             data-ad-slot="{slot_id}"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({{}});
        </script>
        '''
    
    def _generate_adsense_native_code(self, slot_name: str) -> str:
        """Generate native AdSense ad code (highest revenue)"""
        slot_id = self._get_ad_slot_id(slot_name)
        
        return f'''
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={self.adsense_publisher_id}"
                crossorigin="anonymous"></script>
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-format="fluid"
             data-ad-layout-key="-6t+ed+2i-1n-4w"
             data-ad-client="{self.adsense_publisher_id}"
             data-ad-slot="{slot_id}"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({{}});
        </script>
        '''
    
    def _generate_adsense_video_code(self, slot_name: str) -> str:
        """Generate video ad code (highest CPM)"""
        slot_id = self._get_ad_slot_id(slot_name)
        
        return f'''
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={self.adsense_publisher_id}"
                crossorigin="anonymous"></script>
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-format="autorelaxed"
             data-ad-client="{self.adsense_publisher_id}"
             data-ad-slot="{slot_id}"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({{}});
        </script>
        '''
    
    def _get_ad_slot_id(self, slot_name: str) -> str:
        """Get or generate ad slot IDs"""
        slot_mapping = {
            "header_banner_728x90": "1234567890",
            "sidebar_rect_300x250": "2345678901", 
            "in_content_native": "3456789012",
            "footer_mobile_320x100": "4567890123",
            "pre_video_ad": "5678901234",
            "related_content": "6789012345"
        }
        
        return slot_mapping.get(slot_name, "1234567890")  # Default slot
    
    async def track_adsense_performance(self, ad_placement: str, interaction_type: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Track AdSense performance for optimization"""
        
        performance_data = {
            "ad_placement": ad_placement,
            "interaction_type": interaction_type,  # impression, click
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "revenue_estimate": self._calculate_adsense_revenue(ad_placement, interaction_type)
        }
        
        # Store in database
        try:
            await self.db.adsense_performance.insert_one(performance_data.copy())
        except Exception as e:
            logging.error(f"Error storing AdSense performance: {e}")
        
        return {
            "status": "tracked",
            "ad_placement": ad_placement,
            "interaction_type": interaction_type,
            "revenue_estimate": performance_data["revenue_estimate"]
        }
    
    def _calculate_adsense_revenue(self, placement: str, interaction_type: str) -> Dict[str, float]:
        """Calculate estimated AdSense revenue"""
        
        # AdSense revenue rates (estimated)
        cpm_rates = {
            "header_banner": 2.5,      # $2.50 CPM
            "sidebar_rectangle": 3.0,   # $3.00 CPM
            "in_content_native": 6.0,   # $6.00 CPM (best performing)
            "footer_banner": 1.5,       # $1.50 CPM
            "pre_video": 12.0,          # $12.00 CPM (video ads)
            "related_content": 4.0      # $4.00 CPM
        }
        
        ctr_rates = {
            "header_banner": 0.5,       # 0.5% CTR
            "sidebar_rectangle": 0.8,   # 0.8% CTR
            "in_content_native": 1.2,   # 1.2% CTR
            "footer_banner": 0.3,       # 0.3% CTR
            "pre_video": 2.0,           # 2.0% CTR
            "related_content": 1.0      # 1.0% CTR
        }
        
        base_cpm = cpm_rates.get(placement, 2.0)
        base_ctr = ctr_rates.get(placement, 0.5)
        
        if interaction_type == "impression":
            revenue_per_impression = base_cpm / 1000
        elif interaction_type == "click":
            revenue_per_click = (base_cpm / 1000) / (base_ctr / 100)
        else:
            revenue_per_impression = 0
            revenue_per_click = 0
        
        return {
            "revenue_per_impression": revenue_per_impression,
            "revenue_per_click": revenue_per_click if interaction_type == "click" else revenue_per_impression * (base_ctr / 100),
            "estimated_daily": revenue_per_impression * 10000 if interaction_type == "impression" else revenue_per_click * 100,  # Estimated daily revenue
            "cpm": base_cpm,
            "ctr": base_ctr
        }
    
    async def get_adsense_optimization_report(self) -> Dict[str, Any]:
        """Generate AdSense optimization report"""
        
        # Get recent performance data
        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)
        
        performance_data = await self.db.adsense_performance.find({
            "timestamp": {"$gte": yesterday}
        }).to_list(length=None)
        
        # Analyze performance by placement
        placement_stats = {}
        total_impressions = 0
        total_clicks = 0
        total_revenue = 0
        
        for record in performance_data:
            placement = record["ad_placement"]
            interaction = record["interaction_type"]
            revenue = record["revenue_estimate"]["revenue_per_impression"]
            
            if placement not in placement_stats:
                placement_stats[placement] = {
                    "impressions": 0,
                    "clicks": 0,
                    "revenue": 0,
                    "ctr": 0
                }
            
            if interaction == "impression":
                placement_stats[placement]["impressions"] += 1
                total_impressions += 1
            elif interaction == "click":
                placement_stats[placement]["clicks"] += 1
                total_clicks += 1
            
            placement_stats[placement]["revenue"] += revenue
            total_revenue += revenue
        
        # Calculate CTR for each placement
        for placement in placement_stats:
            impressions = placement_stats[placement]["impressions"]
            clicks = placement_stats[placement]["clicks"]
            if impressions > 0:
                placement_stats[placement]["ctr"] = (clicks / impressions) * 100
        
        overall_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        
        return {
            "period": "last_24_hours",
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "total_revenue": f"${total_revenue:.2f}",
            "overall_ctr": f"{overall_ctr:.2f}%",
            "estimated_monthly_revenue": f"${total_revenue * 30:.2f}",
            "placement_performance": placement_stats,
            "optimization_recommendations": [
                "🎯 Native ads perform 2-3x better than display ads",
                "📱 Mobile ads have 40% higher CTR than desktop",
                "🎬 Video ads generate the highest revenue per impression",
                "⬆️ Above-the-fold placements get 5x more impressions",
                "🔄 A/B test ad placements weekly for optimization"
            ],
            "revenue_projections": {
                "conservative_monthly": f"${total_revenue * 30 * 0.8:.2f}",  # 80% of current rate
                "realistic_monthly": f"${total_revenue * 30:.2f}",
                "optimistic_monthly": f"${total_revenue * 30 * 1.5:.2f}"  # With optimization
            }
        }