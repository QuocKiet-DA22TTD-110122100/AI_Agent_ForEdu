"""
Gmail Service with OAuth 2.0
Cho phép AI đọc, gửi và quản lý Gmail của người dùng

Yêu cầu:
- User đã kết nối Google OAuth với Gmail scopes
- OAuth service đang chạy (port 8003)

NOTE: Using synchronous requests library (not async) for compatibility
"""

import requests
import base64
from typing import Dict, List, Optional
from datetime import datetime
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
OAUTH_SERVICE_URL = os.getenv("OAUTH_SERVICE_URL", "http://localhost:8003")
GMAIL_API_URL = "https://gmail.googleapis.com/gmail/v1"


class GmailService:
    """
    Gmail Service - Quản lý email thông qua Gmail API
    Sử dụng OAuth 2.0 tokens từ OAuth Service
    """
    
    def __init__(self, oauth_service_url: str = OAUTH_SERVICE_URL):
        self.oauth_service_url = oauth_service_url
        self.gmail_api = GMAIL_API_URL
    
    def _get_access_token(self, user_id: int) -> Optional[str]:
        """
        Lấy access token từ OAuth service
        Tự động refresh nếu expired
        """
        try:
            response = requests.get(
                f"{self.oauth_service_url}/api/oauth/google/token/{user_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('access_token')
            
            logger.error(f"Failed to get token: {response.status_code} - {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting access token: {e}")
            return None
    
    def _get_headers(self, access_token: str) -> Dict:
        """Tạo headers cho Gmail API request"""
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    # =========================================================================
    # READ EMAILS
    # =========================================================================
    
    def list_emails(
        self, 
        user_id: int, 
        max_results: int = 10,
        label_ids: List[str] = None,
        query: str = None
    ) -> Dict:
        """
        Liệt kê emails trong inbox
        
        Args:
            user_id: ID của user
            max_results: Số lượng email tối đa (default: 10)
            label_ids: Lọc theo labels (INBOX, SENT, DRAFT, etc.)
            query: Gmail search query (vd: "from:example@gmail.com")
        
        Returns:
            Dict với list emails và metadata
        """
        try:
            access_token = self._get_access_token(user_id)
            if not access_token:
                return {"success": False, "error": "Chưa kết nối Google. Vui lòng kết nối trong Settings."}
            
            # Build query params
            params = {"maxResults": max_results}
            if label_ids:
                params["labelIds"] = ",".join(label_ids)
            if query:
                params["q"] = query
            
            # Call Gmail API
            response = requests.get(
                f"{self.gmail_api}/users/me/messages",
                headers=self._get_headers(access_token),
                params=params,
                timeout=15
            )
            
            if response.status_code != 200:
                logger.error(f"Gmail API error: {response.status_code} - {response.text}")
                return {"success": False, "error": f"Lỗi Gmail API: {response.status_code}"}
            
            data = response.json()
            messages = data.get("messages", [])
            
            # Get details for each message
            emails = []
            for msg in messages[:max_results]:
                email_detail = self.get_email(user_id, msg["id"])
                if email_detail.get("success"):
                    emails.append(email_detail["email"])
            
            return {
                "success": True,
                "emails": emails,
                "total": len(emails),
                "resultSizeEstimate": data.get("resultSizeEstimate", 0)
            }
            
        except Exception as e:
            logger.error(f"Error listing emails: {e}")
            return {"success": False, "error": str(e)}
    
    def get_email(self, user_id: int, message_id: str) -> Dict:
        """
        Lấy chi tiết một email
        
        Args:
            user_id: ID của user
            message_id: ID của email
        
        Returns:
            Dict với thông tin email
        """
        try:
            access_token = self._get_access_token(user_id)
            if not access_token:
                return {"success": False, "error": "Chưa kết nối Google"}
            
            response = requests.get(
                f"{self.gmail_api}/users/me/messages/{message_id}",
                headers=self._get_headers(access_token),
                params={"format": "full"},
                timeout=15
            )
            
            if response.status_code != 200:
                return {"success": False, "error": f"Lỗi: {response.status_code}"}
            
            data = response.json()
            
            # Parse email
            headers = {h["name"]: h["value"] for h in data.get("payload", {}).get("headers", [])}
            
            # Get body
            body = self._extract_body(data.get("payload", {}))
            
            email = {
                "id": data["id"],
                "threadId": data.get("threadId"),
                "from": headers.get("From", ""),
                "to": headers.get("To", ""),
                "subject": headers.get("Subject", "(Không có tiêu đề)"),
                "date": headers.get("Date", ""),
                "snippet": data.get("snippet", ""),
                "body": body,
                "labelIds": data.get("labelIds", []),
                "isUnread": "UNREAD" in data.get("labelIds", [])
            }
            
            return {"success": True, "email": email}
            
        except Exception as e:
            logger.error(f"Error getting email: {e}")
            return {"success": False, "error": str(e)}
    
    def _extract_body(self, payload: Dict) -> str:
        """Extract email body from payload"""
        body = ""
        
        if "body" in payload and payload["body"].get("data"):
            body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")
        
        elif "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain" and part.get("body", {}).get("data"):
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
                    break
                elif part["mimeType"] == "text/html" and not body and part.get("body", {}).get("data"):
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
                # Recursive for multipart
                elif "parts" in part:
                    body = self._extract_body(part)
                    if body:
                        break
        
        return body
    
    # =========================================================================
    # SEND EMAILS
    # =========================================================================
    
    def send_email(
        self, 
        user_id: int, 
        to: str, 
        subject: str, 
        body: str,
        cc: str = None,
        bcc: str = None,
        html: bool = False
    ) -> Dict:
        """
        Gửi email
        
        Args:
            user_id: ID của user
            to: Địa chỉ người nhận (có thể nhiều, ngăn cách bằng dấu phẩy)
            subject: Tiêu đề email
            body: Nội dung email
            cc: CC (optional)
            bcc: BCC (optional)
            html: True nếu body là HTML
        
        Returns:
            Dict với kết quả gửi
        """
        try:
            access_token = self._get_access_token(user_id)
            if not access_token:
                return {"success": False, "error": "Chưa kết nối Google. Vui lòng kết nối trong Settings."}
            
            # Get sender email from profile
            profile_response = requests.get(
                f"{self.gmail_api}/users/me/profile",
                headers=self._get_headers(access_token),
                timeout=10
            )
            
            if profile_response.status_code != 200:
                return {"success": False, "error": "Không thể lấy thông tin email"}
            
            sender_email = profile_response.json().get("emailAddress")
            
            # Create message
            if html:
                message = MIMEMultipart("alternative")
                message.attach(MIMEText(body, "html"))
            else:
                message = MIMEText(body)
            
            message["to"] = to
            message["from"] = sender_email
            message["subject"] = subject
            
            if cc:
                message["cc"] = cc
            if bcc:
                message["bcc"] = bcc
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send via Gmail API
            response = requests.post(
                f"{self.gmail_api}/users/me/messages/send",
                headers=self._get_headers(access_token),
                json={"raw": raw_message},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Email sent successfully: {data.get('id')}")
                return {
                    "success": True,
                    "message": f"✅ Đã gửi email đến {to}",
                    "messageId": data.get("id"),
                    "threadId": data.get("threadId")
                }
            else:
                logger.error(f"Send email error: {response.status_code} - {response.text}")
                return {"success": False, "error": f"Lỗi gửi email: {response.text}"}
                
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return {"success": False, "error": str(e)}
    
    def reply_email(
        self,
        user_id: int,
        message_id: str,
        body: str,
        html: bool = False
    ) -> Dict:
        """
        Trả lời email
        
        Args:
            user_id: ID của user  
            message_id: ID của email cần reply
            body: Nội dung reply
            html: True nếu body là HTML
        """
        try:
            # Get original email
            original = self.get_email(user_id, message_id)
            if not original.get("success"):
                return original
            
            email = original["email"]
            
            # Build reply
            to = email["from"]
            subject = email["subject"]
            if not subject.lower().startswith("re:"):
                subject = f"Re: {subject}"
            
            # Send reply with thread reference
            access_token = self._get_access_token(user_id)
            if not access_token:
                return {"success": False, "error": "Chưa kết nối Google"}
            
            # Get sender email
            profile_response = requests.get(
                f"{self.gmail_api}/users/me/profile",
                headers=self._get_headers(access_token),
                timeout=10
            )
            sender_email = profile_response.json().get("emailAddress", "")
            
            # Create message
            if html:
                message = MIMEMultipart("alternative")
                message.attach(MIMEText(body, "html"))
            else:
                message = MIMEText(body)
            
            message["to"] = to
            message["from"] = sender_email
            message["subject"] = subject
            message["In-Reply-To"] = message_id
            message["References"] = message_id
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            response = requests.post(
                f"{self.gmail_api}/users/me/messages/send",
                headers=self._get_headers(access_token),
                json={
                    "raw": raw_message,
                    "threadId": email["threadId"]
                },
                timeout=15
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": f"✅ Đã trả lời email từ {to}"
                }
            else:
                return {"success": False, "error": f"Lỗi: {response.text}"}
                
        except Exception as e:
            logger.error(f"Error replying email: {e}")
            return {"success": False, "error": str(e)}
    
    # =========================================================================
    # EMAIL MANAGEMENT
    # =========================================================================
    
    def mark_as_read(self, user_id: int, message_id: str) -> Dict:
        """Đánh dấu email đã đọc"""
        return self._modify_labels(user_id, message_id, remove_labels=["UNREAD"])
    
    def mark_as_unread(self, user_id: int, message_id: str) -> Dict:
        """Đánh dấu email chưa đọc"""
        return self._modify_labels(user_id, message_id, add_labels=["UNREAD"])
    
    def archive_email(self, user_id: int, message_id: str) -> Dict:
        """Archive email (xóa khỏi inbox)"""
        return self._modify_labels(user_id, message_id, remove_labels=["INBOX"])
    
    def star_email(self, user_id: int, message_id: str) -> Dict:
        """Đánh dấu sao"""
        return self._modify_labels(user_id, message_id, add_labels=["STARRED"])
    
    def trash_email(self, user_id: int, message_id: str) -> Dict:
        """Chuyển email vào thùng rác"""
        try:
            access_token = self._get_access_token(user_id)
            if not access_token:
                return {"success": False, "error": "Chưa kết nối Google"}
            
            response = requests.post(
                f"{self.gmail_api}/users/me/messages/{message_id}/trash",
                headers=self._get_headers(access_token),
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True, "message": "✅ Đã chuyển vào thùng rác"}
            return {"success": False, "error": f"Lỗi: {response.status_code}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _modify_labels(
        self, 
        user_id: int, 
        message_id: str,
        add_labels: List[str] = None,
        remove_labels: List[str] = None
    ) -> Dict:
        """Modify labels của email"""
        try:
            access_token = self._get_access_token(user_id)
            if not access_token:
                return {"success": False, "error": "Chưa kết nối Google"}
            
            body = {}
            if add_labels:
                body["addLabelIds"] = add_labels
            if remove_labels:
                body["removeLabelIds"] = remove_labels
            
            response = requests.post(
                f"{self.gmail_api}/users/me/messages/{message_id}/modify",
                headers=self._get_headers(access_token),
                json=body,
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True, "message": "✅ Cập nhật thành công"}
            return {"success": False, "error": f"Lỗi: {response.status_code}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # =========================================================================
    # SEARCH & FILTER
    # =========================================================================
    
    def search_emails(
        self,
        user_id: int,
        query: str,
        max_results: int = 10
    ) -> Dict:
        """
        Tìm kiếm emails với Gmail query syntax
        
        Examples:
            - from:example@gmail.com
            - subject:meeting
            - is:unread
            - after:2025/01/01
            - has:attachment
            - label:important
        """
        return self.list_emails(user_id, max_results=max_results, query=query)
    
    def get_unread_emails(self, user_id: int, max_results: int = 10) -> Dict:
        """Lấy danh sách email chưa đọc"""
        return self.list_emails(
            user_id, 
            max_results=max_results, 
            label_ids=["INBOX", "UNREAD"]
        )
    
    def get_inbox(self, user_id: int, max_results: int = 10) -> Dict:
        """Lấy inbox"""
        return self.list_emails(
            user_id,
            max_results=max_results,
            label_ids=["INBOX"]
        )
    
    def get_sent_emails(self, user_id: int, max_results: int = 10) -> Dict:
        """Lấy email đã gửi"""
        return self.list_emails(
            user_id,
            max_results=max_results,
            label_ids=["SENT"]
        )
    
    # =========================================================================
    # LABELS
    # =========================================================================
    
    def list_labels(self, user_id: int) -> Dict:
        """Liệt kê tất cả labels của user"""
        try:
            access_token = self._get_access_token(user_id)
            if not access_token:
                return {"success": False, "error": "Chưa kết nối Google"}
            
            response = requests.get(
                f"{self.gmail_api}/users/me/labels",
                headers=self._get_headers(access_token),
                timeout=10
            )
            
            if response.status_code == 200:
                labels = response.json().get("labels", [])
                return {
                    "success": True,
                    "labels": labels,
                    "total": len(labels)
                }
            return {"success": False, "error": f"Lỗi: {response.status_code}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}


# Singleton instance
gmail_service = GmailService()


# ============================================================================
# HELPER FUNCTIONS FOR AI INTEGRATION
# ============================================================================

def ai_read_emails(user_id: int, count: int = 5, unread_only: bool = False) -> str:
    """
    Hàm helper để AI đọc emails
    Returns: String mô tả emails cho AI respond
    """
    if unread_only:
        result = await gmail_service.get_unread_emails(user_id, max_results=count)
    else:
        result = await gmail_service.get_inbox(user_id, max_results=count)
    
    if not result.get("success"):
        return f"❌ {result.get('error', 'Không thể đọc email')}"
    
    emails = result.get("emails", [])
    
    if not emails:
        return "📭 Không có email mới trong hộp thư."
    
    response = f"📬 **Bạn có {len(emails)} email:**\n\n"
    
    for i, email in enumerate(emails, 1):
        unread_icon = "🔵" if email.get("isUnread") else "⚪"
        response += f"{unread_icon} **{i}. {email['subject']}**\n"
        response += f"   📧 Từ: {email['from']}\n"
        response += f"   📅 {email['date']}\n"
        response += f"   💬 {email['snippet'][:100]}...\n\n"
    
    return response


def ai_send_email(user_id: int, to: str, subject: str, body: str) -> str:
    """
    Hàm helper để AI gửi email
    Returns: String kết quả
    """
    result = await gmail_service.send_email(user_id, to, subject, body)
    
    if result.get("success"):
        return f"✅ Đã gửi email đến **{to}** với tiêu đề \"**{subject}**\""
    else:
        return f"❌ Gửi email thất bại: {result.get('error')}"


def ai_search_emails(user_id: int, query: str) -> str:
    """
    Hàm helper để AI tìm kiếm email
    """
    result = await gmail_service.search_emails(user_id, query)
    
    if not result.get("success"):
        return f"❌ {result.get('error')}"
    
    emails = result.get("emails", [])
    
    if not emails:
        return f"🔍 Không tìm thấy email nào với từ khóa \"{query}\""
    
    response = f"🔍 **Tìm thấy {len(emails)} email:**\n\n"
    
    for i, email in enumerate(emails, 1):
        response += f"**{i}. {email['subject']}**\n"
        response += f"   Từ: {email['from']}\n"
        response += f"   {email['snippet'][:80]}...\n\n"
    
    return response


# =========================================================================
# SYNC WRAPPERS for non-async callers
# =========================================================================
import asyncio

def _run_async(coro):
    """Helper to run async functions in sync context"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If already in async context, use nest_asyncio or create task
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        # No event loop, create new one
        return asyncio.run(coro)
    except ImportError:
        # nest_asyncio not available, try new loop
        return asyncio.run(coro)


def ai_read_emails_sync(user_id: int = 1, max_results: int = 5, only_unread: bool = False) -> Dict:
    """
    Sync wrapper for reading emails
    Used by agent_features.py
    """
    try:
        def _read():
            if only_unread:
                result = await gmail_service.get_unread_emails(user_id, max_results)
            else:
                result = await gmail_service.get_inbox(user_id, max_results)
            return result
        
        result = _run_async(_read())
        
        if result.get("success"):
            return {
                "success": True,
                "emails": result.get("emails", [])
            }
        else:
            # Check if need auth
            error_msg = result.get("error", "")
            if "kết nối" in error_msg.lower() or "token" in error_msg.lower():
                return {
                    "success": False,
                    "need_auth": True,
                    "auth_url": f"{OAUTH_SERVICE_URL}/auth/google"
                }
            return result
            
    except Exception as e:
        logger.error(f"ai_read_emails_sync error: {e}")
        return {
            "success": False,
            "error": str(e),
            "need_auth": True,
            "auth_url": f"{OAUTH_SERVICE_URL}/auth/google"
        }


def ai_send_email_sync(user_id: int, to: str, subject: str, body: str) -> Dict:
    """
    Sync wrapper for sending email
    """
    try:
        result = _run_async(gmail_service.send_email(user_id, to, subject, body))
        
        if result.get("success"):
            return {"success": True}
        else:
            error_msg = result.get("error", "")
            if "kết nối" in error_msg.lower() or "token" in error_msg.lower():
                return {
                    "success": False,
                    "need_auth": True,
                    "auth_url": f"{OAUTH_SERVICE_URL}/auth/google"
                }
            return result
            
    except Exception as e:
        logger.error(f"ai_send_email_sync error: {e}")
        return {"success": False, "error": str(e)}


def ai_search_emails_sync(user_id: int, query: str, max_results: int = 10) -> Dict:
    """
    Sync wrapper for searching emails
    """
    try:
        result = _run_async(gmail_service.search_emails(user_id, query, max_results))
        
        if result.get("success"):
            return {
                "success": True,
                "emails": result.get("emails", [])
            }
        else:
            error_msg = result.get("error", "")
            if "kết nối" in error_msg.lower() or "token" in error_msg.lower():
                return {
                    "success": False,
                    "need_auth": True,
                    "auth_url": f"{OAUTH_SERVICE_URL}/auth/google"
                }
            return result
            
    except Exception as e:
        logger.error(f"ai_search_emails_sync error: {e}")
        return {"success": False, "error": str(e)}


# Export sync wrappers with simpler names for agent_features
ai_read_emails = ai_read_emails_sync
ai_send_email = ai_send_email_sync  
ai_search_emails = ai_search_emails_sync


# Test
if __name__ == "__main__":
    import asyncio
    
    def test():
        # Test with user_id = 1
        print("Testing Gmail Service...")
        
        # Test list labels
        labels = await gmail_service.list_labels(1)
        print(f"Labels: {labels}")
        
        # Test inbox
        inbox = await gmail_service.get_inbox(1, max_results=3)
        print(f"Inbox: {inbox}")
    
    asyncio.run(test())

