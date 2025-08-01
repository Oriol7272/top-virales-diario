"""
Twilio Notification Service
Send daily video digest notifications via SMS and WhatsApp
"""

from typing import List, Dict, Optional, Any
import asyncio
import os
import logging
from datetime import datetime, timedelta
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from models import ViralVideo, Platform
from motor.motor_asyncio import AsyncIOMotorDatabase


class TwilioNotificationService:
    """Service for sending video digest notifications via SMS and WhatsApp"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.whatsapp_number = os.getenv('WHATSAPP_PHONE_NUMBER')
        self.client = None
        self.db = db
        self.logger = logging.getLogger(__name__)
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
            self.logger.info("Twilio client initialized")
        else:
            self.logger.warning("Twilio credentials not provided")
    
    async def send_sms_digest(self, to_number: str, videos: List[ViralVideo], user_subscription: str = "free") -> bool:
        """Send daily video digest via SMS"""
        if not self.client or not self.phone_number:
            self.logger.error("Twilio SMS not properly configured")
            return False
        
        try:
            # Create SMS message
            message_body = self._format_sms_digest(videos, user_subscription)
            
            # Send SMS
            message = self.client.messages.create(
                body=message_body,
                from_=self.phone_number,
                to=to_number
            )
            
            # Log successful delivery
            await self._log_notification(to_number, "sms_digest", "sent", len(videos), message.sid)
            
            self.logger.info(f"SMS digest sent to {to_number}, SID: {message.sid}")
            return True
            
        except TwilioException as e:
            self.logger.error(f"Twilio SMS error for {to_number}: {e}")
            await self._log_notification(to_number, "sms_digest", "failed", 0, error=str(e))
            return False
        except Exception as e:
            self.logger.error(f"Unexpected SMS error for {to_number}: {e}")
            await self._log_notification(to_number, "sms_digest", "failed", 0, error=str(e))
            return False
    
    def _format_sms_digest(self, videos: List[ViralVideo], subscription: str = "free") -> str:
        """Format videos into SMS-friendly digest"""
        # Platform emojis
        platform_emojis = {
            Platform.YOUTUBE: '📺',
            Platform.TIKTOK: '🎵',
            Platform.TWITTER: '🐦'
        }
        
        # Header
        date_str = datetime.now().strftime('%m/%d')
        message_parts = [
            f"🔥 VIRAL DAILY - {date_str}",
            ""
        ]
        
        # Add top videos (limit for SMS length)
        max_videos = 3 if subscription == "free" else 5
        for i, video in enumerate(videos[:max_videos], 1):
            platform_emoji = platform_emojis.get(video.platform, '🎬')
            views_formatted = self._format_number(video.views)
            
            # Truncate title for SMS
            title = video.title[:40] + "..." if len(video.title) > 40 else video.title
            
            message_parts.append(f"{i}. {platform_emoji} {title}")
            message_parts.append(f"   {views_formatted} views")
            message_parts.append("")
        
        # Footer
        message_parts.append("More at viral-daily.com")
        message_parts.append("Reply STOP to unsubscribe")
        
        return "\n".join(message_parts)
    
    def _format_number(self, num: int) -> str:
        """Format large numbers in a readable way"""
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        else:
            return str(num)
    
    async def send_verification_code(self, to_number: str) -> Dict[str, Any]:
        """Send SMS verification code for phone verification"""
        if not self.client:
            return {"success": False, "error": "Twilio not configured"}
        
        try:
            # Generate 6-digit code
            import random
            code = str(random.randint(100000, 999999))
            
            # Send verification SMS
            message = self.client.messages.create(
                body=f"Your Viral Daily verification code is: {code}",
                from_=self.phone_number,
                to=to_number
            )
            
            # Store verification code in database (with expiration)
            expiry = datetime.utcnow() + timedelta(minutes=10)
            await self.db.phone_verifications.update_one(
                {"phone_number": to_number},
                {
                    "$set": {
                        "phone_number": to_number,
                        "verification_code": code,
                        "expires_at": expiry,
                        "verified": False,
                        "created_at": datetime.utcnow(),
                        "message_sid": message.sid
                    }
                },
                upsert=True
            )
            
            return {
                "success": True,
                "message_sid": message.sid,
                "expires_at": expiry
            }
            
        except Exception as e:
            self.logger.error(f"Error sending verification code: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_sms_subscribers(self) -> List[str]:
        """Get list of phone numbers subscribed to SMS digest"""
        try:
            cursor = self.db.sms_subscriptions.find({"subscribed": True})
            subscribers = await cursor.to_list(length=None)
            return [sub["phone_number"] for sub in subscribers]
        except Exception as e:
            self.logger.error(f"Error fetching SMS subscribers: {e}")
            return []
    
    async def subscribe_sms(self, phone_number: str, user_id: Optional[str] = None) -> bool:
        """Subscribe a phone number to SMS digest"""
        try:
            await self.db.sms_subscriptions.update_one(
                {"phone_number": phone_number},
                {
                    "$set": {
                        "phone_number": phone_number,
                        "user_id": user_id,
                        "subscribed": True,
                        "subscribed_at": datetime.utcnow(),
                        "subscription_type": "daily_digest"
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            self.logger.error(f"Error subscribing to SMS: {e}")
            return False
    
    async def send_bulk_sms_digest(self, videos: List[ViralVideo]) -> Dict[str, int]:
        """Send SMS digest to all subscribers"""
        subscribers = await self.get_sms_subscribers()
        
        results = {
            "total_subscribers": len(subscribers),
            "successful_deliveries": 0,
            "failed_deliveries": 0
        }
        
        for phone_number in subscribers:
            success = await self.send_sms_digest(phone_number, videos)
            if success:
                results["successful_deliveries"] += 1
            else:
                results["failed_deliveries"] += 1
            
            # Add delay to avoid rate limiting
            await asyncio.sleep(1)  # Twilio has stricter rate limits
        
        self.logger.info(f"Bulk SMS digest sent: {results}")
        return results
    
    async def _log_notification(self, to_number: str, notification_type: str, status: str, video_count: int, message_sid: str = None, error: str = None):
        """Log notification delivery"""
        try:
            await self.db.twilio_notifications.insert_one({
                "to_number": to_number,
                "type": notification_type,
                "status": status,
                "video_count": video_count,
                "message_sid": message_sid,
                "error": error,
                "timestamp": datetime.utcnow()
            })
        except Exception as e:
            self.logger.error(f"Error logging Twilio notification: {e}")