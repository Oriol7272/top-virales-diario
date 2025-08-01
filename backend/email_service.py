# Email Service for Viral Daily
import os
import logging
from typing import List, Optional
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To
from models import ViralVideo, User
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class EmailServiceError(Exception):
    pass

class EmailService:
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY')
        self.sender_email = os.getenv('SENDER_EMAIL')
        
        if not self.api_key:
            raise ValueError("SENDGRID_API_KEY environment variable not set")
        if not self.sender_email:
            raise ValueError("SENDER_EMAIL environment variable not set")
            
        self.sg_client = SendGridAPIClient(api_key=self.api_key)
        logger.info(f"EmailService initialized with sender: {self.sender_email}")
        
    async def verify_sender_email(self) -> bool:
        """Verify the sender email address in SendGrid"""
        try:
            # This will attempt to send a test email to verify the sender
            test_message = Mail(
                from_email=self.sender_email,
                to_emails=self.sender_email,
                subject="Viral Daily - Sender Email Verification",
                html_content="""
                <html>
                    <body style="font-family: Arial, sans-serif; margin: 20px;">
                        <h2 style="color: #8B5CF6;">🎉 Viral Daily Email Service</h2>
                        <p>This is a test email to verify your sender email address for Viral Daily.</p>
                        <p>If you received this email, your SendGrid integration is working correctly!</p>
                        <div style="background: #F3F4F6; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <p><strong>✅ Sender Email:</strong> {}</p>
                            <p><strong>✅ SendGrid API:</strong> Connected</p>
                            <p><strong>✅ Time:</strong> {}</p>
                        </div>
                        <p style="color: #6B7280;">— Viral Daily Email Service</p>
                    </body>
                </html>
                """.format(self.sender_email, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            
            response = self.sg_client.send(test_message)
            return response.status_code == 202
            
        except Exception as e:
            logger.error(f"Failed to verify sender email: {e}")
            raise EmailServiceError(f"Email verification failed: {str(e)}")
    
    def generate_video_email_html(self, videos: List[ViralVideo], user_name: str = "Viral Video Fan") -> str:
        """Generate HTML email template for daily viral videos"""
        
        # Create video cards HTML
        video_cards = ""
        for i, video in enumerate(videos[:10]):  # Top 10 videos
            # Format numbers
            views = f"{video.views:,}" if video.views else "N/A"
            likes = f"{video.likes:,}" if video.likes else "N/A"
            
            # Platform emoji mapping
            platform_emoji = {
                'youtube': '📺',
                'tiktok': '🎵', 
                'twitter': '🐦'
            }
            emoji = platform_emoji.get(video.platform, '🎬')
            
            # Truncate title for email
            title = video.title[:60] + "..." if len(video.title) > 60 else video.title
            
            video_cards += f"""
            <div style="background: white; border-radius: 12px; padding: 20px; margin: 15px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid {'#FF0000' if video.platform == 'youtube' else '#000000' if video.platform == 'tiktok' else '#1DA1F2'};">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span style="font-size: 24px; margin-right: 8px;">{emoji}</span>
                    <span style="background: {'#FF0000' if video.platform == 'youtube' else '#000000' if video.platform == 'tiktok' else '#1DA1F2'}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; text-transform: uppercase; font-weight: bold;">
                        {video.platform}
                    </span>
                    <span style="background: #10B981; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; margin-left: 8px; font-weight: bold;">
                        🔥 {video.viral_score:.0f}
                    </span>
                </div>
                <h3 style="color: #1F2937; margin: 10px 0; font-size: 16px; line-height: 1.4;">
                    {title}
                </h3>
                <div style="display: flex; gap: 20px; color: #6B7280; font-size: 14px;">
                    <span>👁️ <strong>{views}</strong> views</span>
                    <span>❤️ <strong>{likes}</strong> likes</span>
                    <span>👤 <strong>{video.author}</strong></span>
                </div>
                <div style="margin-top: 15px;">
                    <a href="{video.url}" style="background: #8B5CF6; color: white; text-decoration: none; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: bold;">
                        Watch Now →
                    </a>
                </div>
            </div>
            """
        
        # Complete HTML email template
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Your Daily Viral Videos - Viral Daily</title>
        </head>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; background: #F9FAFB;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); padding: 30px 20px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 28px; font-weight: bold;">
                    🎬 Viral Daily
                </h1>
                <p style="color: #E5E7EB; margin: 10px 0 0 0; font-size: 16px;">
                    Your Daily Dose of Viral Videos
                </p>
            </div>
            
            <!-- Greeting -->
            <div style="padding: 20px; background: white;">
                <h2 style="color: #1F2937; margin: 0 0 15px 0;">
                    Hi {user_name}! 👋
                </h2>
                <p style="color: #4B5563; margin: 0; font-size: 16px;">
                    Here are today's most viral videos from YouTube, TikTok, and Twitter. 
                    Get ready for some serious entertainment! 🔥
                </p>
            </div>
            
            <!-- Stats Banner -->
            <div style="background: #FEF3C7; padding: 15px 20px; margin: 10px 20px; border-radius: 8px; border-left: 4px solid #F59E0B;">
                <div style="display: flex; justify-content: space-between; text-align: center;">
                    <div>
                        <div style="font-size: 24px; font-weight: bold; color: #92400E;">{len(videos)}</div>
                        <div style="font-size: 12px; color: #78350F;">Videos Today</div>
                    </div>
                    <div>
                        <div style="font-size: 24px; font-weight: bold; color: #92400E;">{sum(v.views for v in videos):,}</div>
                        <div style="font-size: 12px; color: #78350F;">Total Views</div>
                    </div>
                    <div>
                        <div style="font-size: 24px; font-weight: bold; color: #92400E;">{sum(v.likes for v in videos):,}</div>
                        <div style="font-size: 12px; color: #78350F;">Total Likes</div>
                    </div>
                </div>
            </div>
            
            <!-- Video Cards -->
            <div style="padding: 0 20px;">
                {video_cards}
            </div>
            
            <!-- CTA Section -->
            <div style="background: #1F2937; padding: 30px 20px; text-align: center; margin: 20px 0;">
                <h3 style="color: white; margin: 0 0 15px 0;">Want More Viral Content?</h3>
                <p style="color: #9CA3AF; margin: 0 0 20px 0;">
                    Upgrade to Pro for unlimited videos, no ads, and premium features.
                </p>
                <a href="https://your-deployed-app-url.com" style="background: #8B5CF6; color: white; text-decoration: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; display: inline-block;">
                    Visit Viral Daily →
                </a>
            </div>
            
            <!-- Footer -->
            <div style="padding: 20px; text-align: center; color: #6B7280; font-size: 14px;">
                <p style="margin: 0 0 10px 0;">
                    You're receiving this because you subscribed to Viral Daily updates.
                </p>
                <p style="margin: 0;">
                    © 2025 Viral Daily - Bringing you the internet's most viral content daily.
                </p>
                <div style="margin-top: 15px;">
                    <span style="margin: 0 10px;">📺 YouTube</span>
                    <span style="margin: 0 10px;">🎵 TikTok</span>
                    <span style="margin: 0 10px;">🐦 Twitter</span>
                </div>
            </div>
            
        </body>
        </html>
        """
        
        return html_template
    
    async def send_daily_viral_email(self, user_email: str, videos: List[ViralVideo], user_name: str = "Viral Video Fan") -> bool:
        """Send daily viral video email to a user"""
        try:
            subject = f"🔥 {len(videos)} Viral Videos Today - {datetime.now().strftime('%B %d, %Y')}"
            html_content = self.generate_video_email_html(videos, user_name)
            
            message = Mail(
                from_email=self.sender_email,
                to_emails=[user_email],
                subject=subject,
                html_content=html_content
            )
            
            response = self.sg_client.send(message)
            success = response.status_code == 202
            
            if success:
                logger.info(f"Daily email sent successfully to {user_email}")
            else:
                logger.error(f"Failed to send email to {user_email}: status {response.status_code}")
                
            return success
            
        except Exception as e:
            logger.error(f"Error sending daily email to {user_email}: {e}")
            raise EmailServiceError(f"Failed to send daily email: {str(e)}")
    
    async def send_welcome_email(self, user_email: str, user_name: str = "New User") -> bool:
        """Send welcome email to new subscribers"""
        try:
            subject = "🎉 Welcome to Viral Daily - Your Daily Dose of Viral Content!"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Welcome to Viral Daily</title>
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); padding: 30px; text-align: center; color: white;">
                    <h1 style="margin: 0; font-size: 32px;">🎬 Welcome to Viral Daily!</h1>
                    <p style="margin: 15px 0 0 0; font-size: 18px; opacity: 0.9;">Your Daily Dose of Internet's Hottest Content</p>
                </div>
                
                <div style="padding: 30px;">
                    <h2>Hi {user_name}! 👋</h2>
                    
                    <p>Thank you for subscribing to <strong>Viral Daily</strong>! You've just joined thousands of users who stay ahead of viral trends.</p>
                    
                    <div style="background: #F3F4F6; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <h3 style="color: #8B5CF6; margin-top: 0;">What You'll Get:</h3>
                        <ul style="padding-left: 20px;">
                            <li><strong>📺 YouTube Viral Videos</strong> - Trending content from the world's biggest platform</li>
                            <li><strong>🎵 TikTok Hits</strong> - The latest viral dances, memes, and challenges</li>
                            <li><strong>🐦 Twitter Trends</strong> - Viral tweets and threads that everyone's talking about</li>
                            <li><strong>📊 Viral Scores</strong> - See exactly how viral each piece of content is</li>
                        </ul>
                    </div>
                    
                    <p>Your first daily email will arrive tomorrow morning with the hottest viral content from all platforms!</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://your-deployed-app-url.com" style="background: #8B5CF6; color: white; text-decoration: none; padding: 15px 30px; border-radius: 8px; font-weight: bold; display: inline-block;">
                            Start Exploring Now →
                        </a>
                    </div>
                    
                    <div style="background: #FEF3C7; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <p style="margin: 0; color: #92400E;"><strong>💡 Pro Tip:</strong> Want unlimited access and no ads? Upgrade to Pro for just €9.99/month!</p>
                    </div>
                </div>
                
                <div style="background: #1F2937; padding: 20px; text-align: center; color: white;">
                    <p style="margin: 0;">Welcome to the viral content revolution! 🚀</p>
                    <p style="margin: 10px 0 0 0; color: #9CA3AF; font-size: 14px;">© 2025 Viral Daily</p>
                </div>
            </body>
            </html>
            """
            
            message = Mail(
                from_email=self.sender_email,
                to_emails=[user_email],
                subject=subject,
                html_content=html_content
            )
            
            response = self.sg_client.send(message)
            success = response.status_code == 202
            
            if success:
                logger.info(f"Welcome email sent successfully to {user_email}")
            else:
                logger.error(f"Failed to send welcome email to {user_email}: status {response.status_code}")
                
            return success
            
        except Exception as e:
            logger.error(f"Error sending welcome email to {user_email}: {e}")
            raise EmailServiceError(f"Failed to send welcome email: {str(e)}")

# Global email service instance
email_service = EmailService()