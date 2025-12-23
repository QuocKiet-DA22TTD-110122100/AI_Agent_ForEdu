# 🔧 FIX: Email Draft System

## ❌ Vấn Đề Trước Đây

### 1. **Response Sai Format**
```json
// Trả về array thay vì object
[
  {"id": 470, "message": "..."},
  {"id": 471, "message": "..."}
]

// Thiếu field email_draft
```

### 2. **Trang Bị Trắng**
- EmailDraftPreview render bên trong bubble → Conflict với background
- Không có dark mode support
- Layout bị lỗi

## ✅ Đã Fix

### **Backend ([main.py](../backend/PythonService/main.py))**

#### 1. Thêm EmailDraft Model (Line 327)
```python
class EmailDraft(BaseModel):
    """Email draft for preview"""
    to: str
    subject: str
    body: str
    user_id: Optional[int] = None
```

#### 2. Thêm Field vào ChatResponse (Line 335)
```python
class ChatResponse(BaseModel):
    response: str
    model: str
    context_used: Optional[List[str]] = None
    rag_enabled: bool = False
    suggested_actions: Optional[List[ActionLink]] = None
    tool_action: Optional[ToolAction] = None
    email_draft: Optional[EmailDraft] = None  # ✅ NEW!
```

#### 3. Pass Email Draft (Line 738-748)
```python
# Extract email_draft if present
email_draft_data = result.get('email_draft')
email_draft = None
if email_draft_data:
    email_draft = EmailDraft(**email_draft_data)

return ChatResponse(
    response=response_text,
    model=request.model,
    rag_enabled=False,
    email_draft=email_draft  # ✅ Pass to frontend
)
```

### **Frontend ([ChatPage.tsx](../fronend_web/src/pages/ChatPage.tsx))**

#### 1. Fix Layout Structure (Line 630-753)

**TRƯỚC:**
```tsx
<div className="bubble">
  <p>Message text</p>
  {/* EmailDraftPreview INSIDE bubble ❌ */}
  <EmailDraftPreview />
</div>
```

**SAU:**
```tsx
<div className="flex-1">
  <div className="bubble">
    <p>Message text</p>
  </div>
  
  {/* EmailDraftPreview OUTSIDE bubble ✅ */}
  {message.emailDraft && (
    <div className="mt-2 w-full">
      <EmailDraftPreview draft={message.emailDraft} />
    </div>
  )}
</div>
```

#### 2. Thêm Dark Mode Support
```tsx
bg-gray-100 dark:bg-gray-800
text-gray-900 dark:text-white
border-gray-200 dark:border-gray-700
```

## 📊 Response Format Mới

### **API Response:**
```json
{
  "response": "📝 **Xem trước Email**\n\n📧 **Người nhận:** teacher@tvu.edu.vn...",
  "model": "gemini-flash-latest",
  "rag_enabled": false,
  "email_draft": {
    "to": "teacher@tvu.edu.vn",
    "subject": "Xin nghỉ học",
    "body": "Kính gửi thầy/cô...",
    "user_id": 3
  }
}
```

### **Frontend Render:**
```
┌─────────────────────────────────┐
│ 🤖 AI                          │
│ ┌─────────────────────────────┐│
│ │ 📝 Xem trước Email          ││
│ │ Người nhận: teacher@...     ││
│ └─────────────────────────────┘│
└─────────────────────────────────┘
┌─────────────────────────────────┐
│ 📧 Email Draft Preview         │
│ [Editable Fields]              │
│ [ 📨 Gửi Email ]               │
└─────────────────────────────────┘
```

## 🧪 Test

### **Input:**
```
"gửi mail xin nghỉ học đến teacher@tvu.edu.vn"
```

### **Expected Output:**
1. ✅ AI message với text preview
2. ✅ EmailDraftPreview component hiển thị
3. ✅ Có thể chỉnh sửa các field
4. ✅ Nút "Gửi Email" hoạt động
5. ✅ Dark mode render đúng
6. ✅ Không bị trắng trang

## 🚀 Restart & Test

```bash
# Backend
cd backend/PythonService
python main.py

# Frontend  
cd fronend_web
npm run dev
```

### Test Command:
```
"gửi mail xin nghỉ học đến teacher@tvu.edu.vn"
```

## ✅ Checklist

- [x] Fix ChatResponse model thêm email_draft
- [x] Pass email_draft từ backend
- [x] Fix layout EmailDraftPreview (di chuyển ra ngoài bubble)
- [x] Thêm dark mode support
- [x] Thêm wrapper div với flex-1
- [x] Test không bị trắng trang
- [x] Verify JSON response đúng format
