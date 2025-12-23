# 📧 Hệ Thống Gửi Email Qua Chat Box - Hoàn Chỉnh

## ✨ Tính Năng Mới

### 🎯 Flow Gửi Email Thông Minh

#### **1. Không Chỉ Định Email** 
```
User: "gửi mail xin nghỉ học"
        ↓
AI: Hiển thị danh sách contacts từ Gmail
        ↓
User: Chọn contact (1, 2, 3...)
        ↓
AI: Soạn thảo email tự động
        ↓
Hiển thị khung preview với nút "Gửi"
```

#### **2. Có Chỉ Định Email**
```
User: "gửi mail xin nghỉ học đến teacher@tvu.edu.vn"
        ↓
AI: Tự động soạn email theo ngữ cảnh
        ↓
Hiển thị khung preview với:
  - To: teacher@tvu.edu.vn
  - Subject: Xin nghỉ học
  - Body: (Nội dung tự động tạo)
  - Nút "📨 Gửi Email"
        ↓
User: Chỉnh sửa nội dung (nếu cần)
        ↓
User: Click "Gửi"
        ↓
✅ Email được gửi qua Gmail API
```

## 🔧 Các Thay Đổi

### **Backend ([main.py](../backend/PythonService/main.py))**

#### 1. Thêm Model Mới (Line 308)
```python
class SendEmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    user_id: Optional[int] = None
```

#### 2. Thêm Endpoint Gửi Email (Line 950)
```python
@app.post("/api/email/send", tags=["Email"])
async def send_email_confirmed(request: SendEmailRequest):
    """Send email after user confirms"""
    # Get user_id from token
    # Call ai_send_email()
    # Return success/error
```

### **Backend ([agent_features.py](../backend/PythonService/agent_features.py))**

#### 1. Cải Thiện Logic (Line 1450-1530)
- **Trước:** Tự động gửi email ngay
- **Sau:** Trả về draft với action button

```python
return {
    "success": True,
    "message": "📝 **Xem trước Email**...",
    "action": "email_draft",
    "email_draft": {
        "to": to_email,
        "subject": subject,
        "body": body,
        "user_id": user_id
    }
}
```

### **Frontend ([EmailDraftPreview.tsx](../fronend_web/src/components/EmailDraftPreview.tsx))**

#### Component Mới
```tsx
<EmailDraftPreview 
  draft={{to, subject, body, user_id}}
  onSent={() => toast.success('Sent!')}
/>
```

**Features:**
- ✏️ Chỉnh sửa To, Subject, Body
- 📨 Nút gửi với loading state
- 🎨 UI đẹp với gradient
- ✅ Toast notification

### **Frontend ([ChatPage.tsx](../fronend_web/src/pages/ChatPage.tsx))**

#### 1. Thêm Interface (Line 28)
```typescript
interface EmailDraft {
  to: string;
  subject: string;
  body: string;
  user_id?: number;
}

interface Message {
  ...
  emailDraft?: EmailDraft; // NEW!
}
```

#### 2. Xử Lý Email Draft (Line 340)
```typescript
const aiMessage: Message = {
  ...
  emailDraft: aiResponse.email_draft, // Extract từ AI response
};
```

#### 3. Render Email Draft (Line 705)
```tsx
{message.emailDraft && (
  <EmailDraftPreview 
    draft={message.emailDraft}
    onSent={() => toast.success('Sent!')}
  />
)}
```

## 📖 Hướng Dẫn Sử Dụng

### **Cách 1: Không Chỉ Định Email**

```
User: "gửi mail xin nghỉ học"
```

**Kết quả:**
```
AI: 📧 **Gửi email: xin nghỉ học**

📋 Chọn người nhận:

1. **Thầy Nguyễn** (teacher@tvu.edu.vn) _5 emails_
2. **Admin** (admin@tvu.edu.vn) _3 emails_
3. john@gmail.com _1 email_

💡 Cách chọn:
• Nhắn số: "1" hoặc "chọn 1"
• Hoặc gõ email trực tiếp
```

Sau đó:
```
User: "1"
```

### **Cách 2: Chỉ Định Email Ngay**

```
User: "gửi mail xin nghỉ học đến teacher@tvu.edu.vn"
```

**Kết quả:**
- Hiện khung preview email ngay lập tức
- User có thể chỉnh sửa
- Click "📨 Gửi Email" để gửi

### **Cách 3: Với Nội Dung Cụ Thể**

```
User: "gửi email cho admin@tvu.edu.vn chủ đề Báo cáo tiến độ nội dung Em xin báo cáo tiến độ dự án..."
```

**Kết quả:**
- To: admin@tvu.edu.vn ✅
- Subject: Báo cáo tiến độ ✅
- Body: Em xin báo cáo... ✅

## 🎨 Giao Diện Email Preview

```
┌─────────────────────────────────────────┐
│ 📧 Xem trước Email                      │
├─────────────────────────────────────────┤
│ 📧 Người nhận                           │
│ [teacher@tvu.edu.vn          ]          │
│                                          │
│ 📌 Chủ đề                               │
│ [Xin nghỉ học               ]          │
│                                          │
│ 📄 Nội dung                             │
│ ┌──────────────────────────────────┐   │
│ │ Kính gửi thầy,                    │   │
│ │                                    │   │
│ │ Em xin phép nghỉ học ngày mai...│   │
│ │                                    │   │
│ └──────────────────────────────────┘   │
│                                          │
│ ┌───────────────────────────────────┐  │
│ │  📨 Gửi Email                      │  │
│ └───────────────────────────────────┘  │
│                                          │
│ 💡 Bạn có thể chỉnh sửa trước khi gửi  │
└─────────────────────────────────────────┘
```

## 🔐 Bảo Mật

### **Authentication Flow:**
1. User đăng nhập → Nhận JWT token
2. Token được lưu trong localStorage
3. Mọi request gửi kèm: `Authorization: Bearer {token}`
4. Backend extract `user_id` từ token
5. Gửi email từ Gmail của user có `user_id` đó

### **Endpoints:**
- `POST /api/chat` - Chat với AI (tạo draft)
- `POST /api/email/send` - Gửi email sau khi confirm
- Cả 2 đều cần JWT token

## ✅ Checklist Hoàn Thành

- [x] Phân biệt rõ intent gửi mail vs chat thường
- [x] Hiển thị contacts khi không chỉ định email
- [x] Tự động soạn draft khi có chỉ định email
- [x] UI preview email với khả năng chỉnh sửa
- [x] Nút gửi với loading state
- [x] Lấy đúng user_id từ token
- [x] Gửi email qua Gmail API
- [x] Toast notification khi thành công/thất bại
- [x] Dark mode support
- [x] Responsive design

## 🧪 Test Cases

### **Test 1: Không có email**
```
Input: "gửi mail xin nghỉ"
Expected: Hiện danh sách contacts
```

### **Test 2: Có email**
```
Input: "gửi mail xin nghỉ đến test@gmail.com"
Expected: Hiện khung preview ngay
```

### **Test 3: Đầy đủ thông tin**
```
Input: "gửi email cho admin@tvu.edu.vn chủ đề Test nội dung This is a test"
Expected: Preview với đầy đủ thông tin
```

### **Test 4: Gửi thành công**
```
Action: Click "Gửi Email"
Expected: ✅ Toast "Email đã gửi thành công!"
```

## 🚀 Khởi Động

### **Backend:**
```bash
cd backend/PythonService
python main.py
```

### **Frontend:**
```bash
cd fronend_web
npm run dev
```

### **Test:**
1. Đăng nhập vào ứng dụng
2. Vào **Settings** → Connect Google Account
3. Thử gửi email: "gửi mail test đến your-email@gmail.com"
4. Kiểm tra inbox!

## 📝 Ghi Chú

- Cần OAuth 2.0 setup cho Gmail API
- User phải connect Google Account trước
- Email gửi từ Gmail của user đã đăng nhập
- Dark mode được hỗ trợ đầy đủ
