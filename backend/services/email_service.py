"""
Email Service for sending notifications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import List, Dict, Optional
from datetime import datetime


class EmailService:
    """Email service for sending notifications"""
    
    def __init__(self):
        """Initialize email service with SMTP configuration"""
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_user)
        self.from_name = os.getenv('FROM_NAME', 'Expense Risk Analyzer')
    
    def is_configured(self) -> bool:
        """Check if email service is properly configured"""
        # Check if credentials are set and not placeholder values
        return bool(
            self.smtp_user and 
            self.smtp_password and 
            self.smtp_user != 'your-email@gmail.com' and
            self.smtp_password != 'your-app-password' and
            '@' in self.smtp_user
        )
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send an email
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML body content
            text_content: Plain text fallback (optional)
        
        Returns:
            bool: True if email was sent successfully
        """
        if not self.is_configured():
            error_msg = "Email service not configured. Please set valid SMTP_USER and SMTP_PASSWORD in .env file"
            print(error_msg)
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Add plain text part
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                msg.attach(part1)
            
            # Add HTML part
            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)
            
            # Connect and send
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.from_email, to_email, msg.as_string())
            
            print(f"Email sent successfully to {to_email}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"SMTP Authentication failed: {e}")
            return False
        except smtplib.SMTPConnectError as e:
            print(f"SMTP Connection failed: {e}")
            return False
        except smtplib.SMTPException as e:
            print(f"SMTP Error: {e}")
            return False
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def send_recommendation_alert(
        self,
        user_email: str,
        user_name: str,
        recommendations: List[Dict]
    ) -> bool:
        """
        Send AI recommendation alert email
        
        Args:
            user_email: User's email address
            user_name: User's name for personalization
            recommendations: List of recommendation dictionaries
        
        Returns:
            bool: True if email was sent successfully
        """
        if not recommendations:
            return False
        
        # Filter high-priority recommendations (priority >= 7)
        high_priority_recs = [r for r in recommendations if r.get('priority', 0) >= 7]
        
        if not high_priority_recs:
            return False
        
        subject = "🚨 AI Financial Alert - Action Required"
        
        # Build HTML content
        html_content = self._build_recommendation_email_html(
            user_name, 
            high_priority_recs
        )
        
        # Build plain text content
        text_content = self._build_recommendation_email_text(
            user_name, 
            high_priority_recs
        )
        
        return self.send_email(user_email, subject, html_content, text_content)
    
    def _build_recommendation_email_html(
        self, 
        user_name: str, 
        recommendations: List[Dict]
    ) -> str:
        """Build HTML email content for recommendations"""
        
        rec_items = ""
        for rec in recommendations:
            priority_color = self._get_priority_color(rec.get('priority', 0))
            priority_label = self._get_priority_label(rec.get('priority', 0))
            
            rec_items += f"""
            <div style="background-color: #f8f9fa; border-left: 4px solid {priority_color}; padding: 16px; margin-bottom: 16px; border-radius: 4px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <h3 style="margin: 0; color: #333; font-size: 16px;">{rec.get('title', 'Recommendation')}</h3>
                    <span style="background-color: {priority_color}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{priority_label}</span>
                </div>
                <p style="margin: 8px 0; color: #555; font-size: 14px;">{rec.get('message', '')}</p>
                <p style="margin: 8px 0; color: {priority_color}; font-weight: 600; font-size: 14px;">
                    💰 {rec.get('impact', '')}
                </p>
            </div>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #1976d2, #42a5f5); padding: 30px; border-radius: 8px 8px 0 0; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 24px;">💡 AI Financial Recommendations</h1>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">Your personalized insights from Expense Risk Analyzer</p>
            </div>
            
            <div style="background-color: white; padding: 30px; border: 1px solid #e0e0e0; border-top: none; border-radius: 0 0 8px 8px;">
                <p style="font-size: 16px; color: #333;">Hi {user_name or 'there'},</p>
                
                <p style="font-size: 14px; color: #555;">
                    Our AI has analyzed your financial data and identified the following important recommendations that require your attention:
                </p>
                
                <div style="margin: 24px 0;">
                    {rec_items}
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="http://localhost:5173/dashboard" style="background-color: #1976d2; color: white; padding: 12px 30px; text-decoration: none; border-radius: 4px; font-weight: 600; display: inline-block;">
                        View Dashboard
                    </a>
                </div>
                
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 30px 0;">
                
                <p style="font-size: 12px; color: #888; text-align: center;">
                    This is an automated alert from Expense Risk Analyzer.<br>
                    Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
                </p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _build_recommendation_email_text(
        self, 
        user_name: str, 
        recommendations: List[Dict]
    ) -> str:
        """Build plain text email content for recommendations"""
        
        text = f"""
AI Financial Recommendations
============================

Hi {user_name or 'there'},

Our AI has analyzed your financial data and identified the following important recommendations:

"""
        for i, rec in enumerate(recommendations, 1):
            text += f"""
{i}. {rec.get('title', 'Recommendation')}
   {rec.get('message', '')}
   Impact: {rec.get('impact', '')}
   Priority: {self._get_priority_label(rec.get('priority', 0))}

"""
        
        text += f"""
---
View your dashboard: http://localhost:5173/dashboard

This is an automated alert from Expense Risk Analyzer.
Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
"""
        
        return text
    
    def _get_priority_color(self, priority: int) -> str:
        """Get color based on priority level"""
        if priority >= 9:
            return '#d32f2f'  # Red - Critical
        elif priority >= 7:
            return '#f57c00'  # Orange - High
        elif priority >= 5:
            return '#fbc02d'  # Yellow - Medium
        else:
            return '#388e3c'  # Green - Low
    
    def _get_priority_label(self, priority: int) -> str:
        """Get label based on priority level"""
        if priority >= 9:
            return 'Critical'
        elif priority >= 7:
            return 'High Priority'
        elif priority >= 5:
            return 'Medium'
        else:
            return 'Low'


# Global instance
email_service = EmailService()
