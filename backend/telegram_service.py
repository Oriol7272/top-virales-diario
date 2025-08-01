"""
Telegram Notification Service
Send daily video digest notifications via Telegram Bot
"""

from typing import List, Dict, Optional, Any
import asyncio
import os
import logging
from datetime import datetime
from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from models import ViralVideo, User, Platform
from motor.motor_asyncio import AsyncIOMotorDatabase


class TelegramNotificationService:
    """Service for sending video digest notifications via Telegram"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.webhook_secret = os.getenv('TELEGRAM_WEBHOOK_SECRET', 'secure_webhook_secret_2025')
        self.bot = None
        self.db = db
        self.logger = logging.getLogger(__name__)
        
        if self.bot_token:
            self.bot = Bot(token=self.bot_token)
            self.logger.info("Telegram bot initialized")
        else:
            self.logger.warning("Telegram bot token not provided")
    
    def escape_markdown_v2(self, text: str) -> str:
        """Escape special characters for MarkdownV2"""
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text
    
    async def send_daily_digest(self, chat_id: int, videos: List[ViralVideo], user_subscription: str = "free") -> bool:
        """Send daily video digest to a Telegram chat"""
        if not self.bot:
            self.logger.error("Telegram bot not initialized")
            return False
        
        try:
            # Create digest message
            message = self._format_daily_digest(videos, user_subscription)
            
            # Send message
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_web_page_preview=False
            )
            
            # Log successful delivery
            await self._log_notification(chat_id, "daily_digest", "sent", len(videos))
            
            self.logger.info(f"Daily digest sent to chat_id {chat_id}")
            return True
            
        except TelegramError as e:
            self.logger.error(f"Telegram error sending digest to {chat_id}: {e}")
            await self._log_notification(chat_id, "daily_digest", "failed", 0, str(e))
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error sending digest to {chat_id}: {e}")
            await self._log_notification(chat_id, "daily_digest", "failed", 0, str(e))
            return False
    
    def _format_daily_digest(self, videos: List[ViralVideo], subscription: str = "free") -> str:
        """Format videos into a Telegram-friendly digest message"""
        # Platform emojis
        platform_emojis = {
            Platform.YOUTUBE: '📺',
            Platform.TIKTOK: '🎵',
            Platform.TWITTER: '🐦'
        }
        
        # Header
        date_str = datetime.now().strftime('%B %d, %Y')
        message_parts = [
            f"*🔥 VIRAL DAILY \\- {self.escape_markdown_v2(date_str)}*",
            "",
            f"*Today's {len(videos)} Most Viral Videos*",
            ""
        ]
        
        # Add subscription info
        if subscription == "free":
            message_parts.append("_🆓 Free Plan \\- Limited to top viral videos_")
        elif subscription == "pro":
            message_parts.append("_⭐ Pro Plan \\- Premium viral content_")
        elif subscription == "business":
            message_parts.append("_💼 Business Plan \\- Full analytics access_")
        
        message_parts.append("")
        
        # Add videos
        for i, video in enumerate(videos, 1):
            platform_emoji = platform_emojis.get(video.platform, '🎬')
            
            # Format numbers
            views_formatted = self._format_number(video.views)
            likes_formatted = self._format_number(video.likes) if video.likes else "N/A"
            
            # Escape title and channel
            title_escaped = self.escape_markdown_v2(video.title[:80] + "..." if len(video.title) > 80 else video.title)
            channel_escaped = self.escape_markdown_v2(video.channel_name)
            
            video_section = [
                f"*{i}\\. {platform_emoji} {title_escaped}*",
                f"📊 *{self.escape_markdown_v2(views_formatted)} views* • ❤️ {self.escape_markdown_v2(likes_formatted)} likes",
                f"👤 {channel_escaped}",
                f"🔗 [Watch Video]({video.url})",
                ""
            ]
            
            message_parts.extend(video_section)
        
        # Footer
        message_parts.extend([
            "─" * 30,
            "_🚀 Want more viral content? Upgrade your plan\\!_",
            "",
            "💬 Reply with /help for commands",
            f"⏰ Next digest: {self.escape_markdown_v2('Tomorrow at 9:00 AM')}"
        ])
        
        return "\n".join(message_parts)
    
    def _format_number(self, num: int) -> str:
        """Format large numbers in a readable way"""
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        else:
            return str(num)
    
    async def send_instant_notification(self, chat_id: int, message: str) -> bool:
        """Send instant notification to a user"""
        if not self.bot:
            return False
        
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=self.escape_markdown_v2(message),
                parse_mode=ParseMode.MARKDOWN_V2
            )
            return True
        except Exception as e:
            self.logger.error(f"Error sending instant notification: {e}")
            return False
    
    async def handle_webhook_update(self, update_data: Dict[str, Any]) -> Dict[str, str]:
        """Handle incoming Telegram webhook updates"""
        try:
            update = Update.de_json(update_data, self.bot)
            
            if update.message:
                await self._handle_message(update.message)
            
            return {"status": "ok"}
        except Exception as e:
            self.logger.error(f"Webhook processing failed: {e}")
            return {"status": "error", "detail": str(e)}
    
    async def _handle_message(self, message):
        """Handle incoming messages and commands"""
        chat_id = message.chat_id
        text = message.text
        user_id = message.from_user.id
        
        # Log incoming message
        await self._log_message(chat_id, user_id, text, "incoming")
        
        if not text:
            return
        
        # Handle commands
        if text.startswith('/start'):
            await self._handle_start_command(chat_id)
        elif text.startswith('/help'):
            await self._handle_help_command(chat_id)
        elif text.startswith('/digest'):
            await self._handle_digest_command(chat_id)
        elif text.startswith('/subscribe'):
            await self._handle_subscribe_command(chat_id)
        elif text.startswith('/unsubscribe'):
            await self._handle_unsubscribe_command(chat_id)
        else:
            await self._handle_unknown_command(chat_id)
    
    async def _handle_start_command(self, chat_id: int):
        """Handle /start command"""
        welcome_message = """
*🔥 Welcome to Viral Daily\\!*

Get the hottest viral videos from YouTube, TikTok, and Twitter delivered daily\\!

*Available Commands:*
/digest \\- Get today's viral videos
/subscribe \\- Enable daily notifications
/unsubscribe \\- Disable notifications  
/help \\- Show this help message

_Ready to go viral? Type /digest to see today's trending videos\\!_
        """
        
        await self.bot.send_message(
            chat_id=chat_id,
            text=welcome_message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def _handle_help_command(self, chat_id: int):
        """Handle /help command"""
        help_message = """
*🤖 Viral Daily Bot Commands*

*Main Commands:*
/digest \\- Get today's top viral videos
/subscribe \\- Enable daily digest notifications
/unsubscribe \\- Disable daily notifications
/help \\- Show this help message

*About Viral Daily:*
We aggregate the most viral videos from:
📺 YouTube \\- Trending videos
🎵 TikTok \\- Viral content  
🐦 Twitter \\- Popular video posts

*Subscription Plans:*
🆓 *Free* \\- Top 3 viral videos daily
⭐ *Pro* \\- Top 10 videos \\+ analytics
💼 *Business* \\- Unlimited access \\+ API

_Visit our website to upgrade your plan\\!_
        """
        
        await self.bot.send_message(
            chat_id=chat_id,
            text=help_message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def _handle_digest_command(self, chat_id: int):
        """Handle /digest command - send current viral videos"""
        await self.bot.send_message(
            chat_id=chat_id,
            text="*🔄 Fetching today's viral videos\\.\\.\\.*",
            parse_mode=ParseMode.MARKDOWN_V2
        )
        
        # This would typically fetch videos from the main aggregator
        # For now, send a placeholder
        message = """
*🔥 Today's Viral Videos*

_This feature requires integration with the main video aggregator\\._

Use /subscribe to get automatic daily digests\\!
        """
        
        await self.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def _handle_subscribe_command(self, chat_id: int):
        """Handle /subscribe command"""
        # Store subscription in database
        await self.db.telegram_subscriptions.update_one(
            {"chat_id": chat_id},
            {
                "$set": {
                    "chat_id": chat_id,
                    "subscribed": True,
                    "subscribed_at": datetime.utcnow(),
                    "subscription_type": "daily_digest"
                }
            },
            upsert=True
        )
        
        message = """
*✅ Successfully subscribed\\!*

You'll now receive daily viral video digests every morning at 9:00 AM\\.

_To unsubscribe, use /unsubscribe_
        """
        
        await self.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def _handle_unsubscribe_command(self, chat_id: int):
        """Handle /unsubscribe command"""
        await self.db.telegram_subscriptions.update_one(
            {"chat_id": chat_id},
            {"$set": {"subscribed": False, "unsubscribed_at": datetime.utcnow()}},
            upsert=True
        )
        
        message = """
*🔕 Successfully unsubscribed*

You'll no longer receive daily viral video digests\\.

_To resubscribe, use /subscribe_
        """
        
        await self.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def _handle_unknown_command(self, chat_id: int):
        """Handle unknown commands"""
        message = """
*🤔 Command not recognized*

Type /help to see available commands
        """
        
        await self.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def get_subscribed_users(self) -> List[int]:
        """Get list of chat IDs subscribed to daily digest"""
        try:
            cursor = self.db.telegram_subscriptions.find({"subscribed": True})
            subscribers = await cursor.to_list(length=None)
            return [sub["chat_id"] for sub in subscribers]
        except Exception as e:
            self.logger.error(f"Error fetching subscribers: {e}")
            return []
    
    async def _log_notification(self, chat_id: int, notification_type: str, status: str, video_count: int, error: str = None):
        """Log notification delivery"""
        try:
            await self.db.telegram_notifications.insert_one({
                "chat_id": chat_id,
                "type": notification_type,
                "status": status,
                "video_count": video_count,
                "error": error,
                "timestamp": datetime.utcnow()
            })
        except Exception as e:
            self.logger.error(f"Error logging notification: {e}")
    
    async def _log_message(self, chat_id: int, user_id: int, message: str, direction: str):
        """Log incoming/outgoing messages"""
        try:
            await self.db.telegram_messages.insert_one({
                "chat_id": chat_id,
                "user_id": user_id,
                "message": message,
                "direction": direction,
                "timestamp": datetime.utcnow()
            })
        except Exception as e:
            self.logger.error(f"Error logging message: {e}")
    
    async def send_bulk_digest(self, videos: List[ViralVideo]) -> Dict[str, int]:
        """Send daily digest to all subscribers"""
        subscribers = await self.get_subscribed_users()
        
        results = {
            "total_subscribers": len(subscribers),
            "successful_deliveries": 0,
            "failed_deliveries": 0
        }
        
        for chat_id in subscribers:
            success = await self.send_daily_digest(chat_id, videos)
            if success:
                results["successful_deliveries"] += 1
            else:
                results["failed_deliveries"] += 1
            
            # Add small delay to avoid rate limiting
            await asyncio.sleep(0.1)
        
        self.logger.info(f"Bulk digest sent: {results}")
        return results