"""
Gmail API Service - FastAPI Endpoints
Expose Gmail functions qua REST API để test Swagger
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from dotenv import load_dotenv

# Import Gmail service
try:
    from gmail_service import (
        gmail_service, 
        ai_read_emails, 
        ai_send_email, 
        ai_search_emails,
        ai_get_contacts,
        ai_create_draft_email
    )
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False

load_dotenv()

app = FastAPI(
    title="Gmail API Service",
    description="Gmail integration với OAuth 2.0 - Test via Swagger",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# MODELS
# ============================================================================

class ReadEmailsRequest(BaseModel):
    user_id: int = 1
    max_results: int = 5
    only_unread: bool = False

class SendEmailRequest(BaseModel):
    user_id: int = 1
    to: str
    subject: str
    body: str
    html: bool = False

class SearchEmailsRequest(BaseModel):
    user_id: int = 1
    query: str
    max_results: int = 10

class GetContactsRequest(BaseModel):
    user_id: int = 1
    max_results: int = 20

class CreateDraftRequest(BaseModel):
    subject_keyword: str
    recipient_name: Optional[str] = None

class ComposeEmailRequest(BaseModel):
    user_id: int = 1
    message: str  # VD: "gửi email xin nghỉ học"

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Gmail API Service",
        "gmail_available": GMAIL_AVAILABLE,
        "oauth_required": True
    }

# ============================================================================
# GMAIL ENDPOINTS
# ============================================================================

@app.post("/api/gmail/read", tags=["Gmail"])
async def read_emails(request: ReadEmailsRequest):
    """
    📧 Đọc emails từ Gmail inbox
    
    **Yêu cầu:**
    - User đã kết nối Google Account trong Settings
    - OAuth token còn hiệu lực
    
    **Returns:**
    - List emails với subject, from, date, snippet
    """
    if not GMAIL_AVAILABLE:
        raise HTTPException(status_code=500, detail="Gmail service not available")
    
    result = ai_read_emails(
        user_id=request.user_id,
        max_results=request.max_results,
        only_unread=request.only_unread
    )
    
    if not result.get("success"):
        if result.get("need_auth"):
            raise HTTPException(
                status_code=401, 
                detail="Please connect Google Account in Settings"
            )
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    
    return {
        "success": True,
        "emails": result.get("emails", []),
        "count": len(result.get("emails", []))
    }


@app.post("/api/gmail/send", tags=["Gmail"])
async def send_email(request: SendEmailRequest):
    """
    📤 Gửi email qua Gmail
    
    **Ví dụ:**
    ```json
    {
      "user_id": 1,
      "to": "teacher@tvu.edu.vn",
      "subject": "Xin nghỉ học",
      "body": "Kính gửi thầy,\\n\\nEm xin phép nghỉ học..."
    }
    ```
    """
    if not GMAIL_AVAILABLE:
        raise HTTPException(status_code=500, detail="Gmail service not available")
    
    result = ai_send_email(
        user_id=request.user_id,
        to=request.to,
        subject=request.subject,
        body=request.body
    )
    
    if not result.get("success"):
        if result.get("need_auth"):
            raise HTTPException(status_code=401, detail="Need Google OAuth")
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to send"))
    
    return {
        "success": True,
        "message": f"Email sent to {request.to}"
    }


@app.post("/api/gmail/search", tags=["Gmail"])
async def search_emails(request: SearchEmailsRequest):
    """
    🔍 Tìm kiếm emails trong Gmail
    
    **Query examples:**
    - "from:teacher@tvu.edu.vn"
    - "subject:thời khóa biểu"
    - "has:attachment"
    """
    if not GMAIL_AVAILABLE:
        raise HTTPException(status_code=500, detail="Gmail service not available")
    
    result = ai_search_emails(
        user_id=request.user_id,
        query=request.query,
        max_results=request.max_results
    )
    
    if not result.get("success"):
        if result.get("need_auth"):
            raise HTTPException(status_code=401, detail="Need Google OAuth")
        raise HTTPException(status_code=400, detail=result.get("error", "Search failed"))
    
    return {
        "success": True,
        "emails": result.get("emails", []),
        "query": request.query,
        "count": len(result.get("emails", []))
    }


@app.get("/api/gmail/contacts/{user_id}", tags=["Contacts"])
async def get_contacts(user_id: int, max_results: int = 20):
    """
    👥 Lấy danh sách contacts từ sent emails
    
    **Returns:**
    - List contacts với name, email, và số lần gửi
    - Sắp xếp theo tần suất gửi email
    """
    if not GMAIL_AVAILABLE:
        raise HTTPException(status_code=500, detail="Gmail service not available")
    
    result = ai_get_contacts(user_id=user_id, max_results=max_results)
    
    if not result.get("success"):
        if result.get("need_auth"):
            raise HTTPException(status_code=401, detail="Need Google OAuth")
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to get contacts"))
    
    return {
        "success": True,
        "contacts": result.get("contacts", []),
        "total": len(result.get("contacts", []))
    }


@app.post("/api/gmail/draft", tags=["Compose"])
async def create_draft(request: CreateDraftRequest):
    """
    ✏️ Tạo draft email bằng AI
    
    **Ví dụ:**
    ```json
    {
      "subject_keyword": "xin nghỉ học",
      "recipient_name": "thầy Nguyễn Văn A"
    }
    ```
    
    **AI sẽ:**
    - Generate subject line phù hợp
    - Tạo nội dung email chuyên nghiệp
    - Điều chỉnh tone dựa trên recipient
    """
    if not GMAIL_AVAILABLE:
        raise HTTPException(status_code=500, detail="Gmail service not available")
    
    result = ai_create_draft_email(
        subject_keyword=request.subject_keyword,
        recipient_name=request.recipient_name
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to create draft"))
    
    return {
        "success": True,
        "subject": result.get("subject", ""),
        "body": result.get("body", ""),
        "recipient_name": request.recipient_name
    }


@app.post("/api/gmail/compose/interactive", tags=["Compose"])
async def compose_email_interactive(request: ComposeEmailRequest):
    """
    🎯 Compose email theo flow tương tác
    
    **Flow:**
    1. User: "gửi email xin nghỉ học"
    2. AI: Suggest contacts
    3. User chọn contact
    4. AI tạo draft
    5. User confirm/edit
    6. Send!
    
    **Ví dụ message:**
    - "gửi email xin nghỉ học đến thầy"
    - "soạn mail hỏi bài tập"
    - "viết email cảm ơn"
    """
    if not GMAIL_AVAILABLE:
        raise HTTPException(status_code=500, detail="Gmail service not available")
    
    try:
        from agent_features import AgentFeatures
        agent = AgentFeatures()
        
        # Call interactive email handler
        result = agent.handle_gmail_send(
            message=request.message,
            token="",  # Token will be fetched from OAuth service
            user_id=request.user_id
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.get("/api/gmail/labels/{user_id}", tags=["Utility"])
async def get_labels(user_id: int):
    """
    🏷️ Lấy danh sách labels/folders trong Gmail
    
    **Returns:**
    - INBOX, SENT, DRAFT, TRASH, etc.
    - Custom labels
    """
    if not GMAIL_AVAILABLE:
        raise HTTPException(status_code=500, detail="Gmail service not available")
    
    result = gmail_service.list_labels(user_id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed"))
    
    return result


@app.get("/api/gmail/profile/{user_id}", tags=["Utility"])
async def get_profile(user_id: int):
    """
    👤 Lấy Gmail profile của user
    
    **Returns:**
    - Email address
    - Total messages
    - Total threads
    """
    if not GMAIL_AVAILABLE:
        raise HTTPException(status_code=500, detail="Gmail service not available")
    
    try:
        access_token = gmail_service._get_access_token(user_id)
        if not access_token:
            raise HTTPException(status_code=401, detail="Not connected")
        
        import requests
        response = requests.get(
            f"{gmail_service.gmail_api}/users/me/profile",
            headers=gmail_service._get_headers(access_token),
            timeout=10
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get profile")
        
        return {
            "success": True,
            "profile": response.json()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("GMAIL_API_PORT", 8005))
    print("=" * 60)
    print("📧 Gmail API Service")
    print("=" * 60)
    print(f"📍 Server: http://localhost:{port}")
    print(f"📚 Swagger UI: http://localhost:{port}/docs")
    print(f"🔐 OAuth required: User must connect Google in Settings")
    print("=" * 60)
    uvicorn.run("gmail_api:app", host="0.0.0.0", port=port, reload=True)
