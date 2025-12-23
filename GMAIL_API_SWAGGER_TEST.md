# 🧪 Test Gmail API qua Swagger

## 🚀 Quick Start

### 1. Start service

```powershell
.\start-gmail-api.ps1
```

hoặc

```bash
cd backend/PythonService
python gmail_api.py
```

### 2. Mở Swagger UI

```
http://localhost:8005/docs
```

---

## 📧 API Endpoints có sẵn

### 1. **Read Emails** - `POST /api/gmail/read`

Đọc emails từ inbox

**Request:**
```json
{
  "user_id": 1,
  "max_results": 5,
  "only_unread": false
}
```

**Response:**
```json
{
  "success": true,
  "emails": [
    {
      "id": "...",
      "subject": "Thông báo lịch học",
      "from": "teacher@tvu.edu.vn",
      "date": "2025-12-23",
      "snippet": "Lớp học ngày mai...",
      "isUnread": true
    }
  ],
  "count": 5
}
```

---

### 2. **Send Email** - `POST /api/gmail/send`

Gửi email

**Request:**
```json
{
  "user_id": 1,
  "to": "teacher@tvu.edu.vn",
  "subject": "Xin nghỉ học",
  "body": "Kính gửi thầy,\n\nEm xin phép nghỉ học ngày mai.\n\nTrân trọng,\nNguyễn Văn A"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email sent to teacher@tvu.edu.vn"
}
```

---

### 3. **Search Emails** - `POST /api/gmail/search`

Tìm kiếm emails

**Request:**
```json
{
  "user_id": 1,
  "query": "from:teacher@tvu.edu.vn",
  "max_results": 10
}
```

**Gmail Search Query Examples:**
- `from:teacher@tvu.edu.vn` - Từ người gửi
- `subject:thời khóa biểu` - Chủ đề
- `has:attachment` - Có đính kèm
- `is:unread` - Chưa đọc
- `after:2025/12/01` - Sau ngày

---

### 4. **Get Contacts** - `GET /api/gmail/contacts/{user_id}`

Lấy danh sách contacts (từ sent emails)

**Response:**
```json
{
  "success": true,
  "contacts": [
    {
      "name": "Nguyễn Văn A",
      "email": "teacher.a@tvu.edu.vn",
      "count": 5
    },
    {
      "name": "Phòng Đào Tạo",
      "email": "daotao@tvu.edu.vn",
      "count": 10
    }
  ],
  "total": 2
}
```

---

### 5. **Create Draft** - `POST /api/gmail/draft`

AI tạo draft email

**Request:**
```json
{
  "subject_keyword": "xin nghỉ học",
  "recipient_name": "thầy Nguyễn Văn A"
}
```

**Response:**
```json
{
  "success": true,
  "subject": "Xin phép nghỉ học",
  "body": "Kính gửi thầy Nguyễn Văn A,\n\nEm xin phép được nghỉ học...\n\nTrân trọng,\n[Tên bạn]",
  "recipient_name": "thầy Nguyễn Văn A"
}
```

---

### 6. **Compose Interactive** - `POST /api/gmail/compose/interactive`

Flow tương tác (suggest contacts)

**Request:**
```json
{
  "user_id": 1,
  "message": "gửi email xin nghỉ học đến thầy"
}
```

**Response:**
```json
{
  "success": true,
  "message": "📧 Gửi email: xin nghỉ học\n\n📋 Chọn người nhận:\n\n1. Nguyễn Văn A...",
  "action": "select_recipient",
  "contacts": [...],
  "awaiting_selection": true
}
```

---

### 7. **Get Labels** - `GET /api/gmail/labels/{user_id}`

Lấy labels/folders

**Response:**
```json
{
  "success": true,
  "labels": [
    {"id": "INBOX", "name": "INBOX", "type": "system"},
    {"id": "SENT", "name": "SENT", "type": "system"},
    ...
  ],
  "total": 10
}
```

---

### 8. **Get Profile** - `GET /api/gmail/profile/{user_id}`

Lấy Gmail profile

**Response:**
```json
{
  "success": true,
  "profile": {
    "emailAddress": "your-email@gmail.com",
    "messagesTotal": 1234,
    "threadsTotal": 567
  }
}
```

---

## ⚙️ Test trong Swagger UI

### Bước 1: Mở Swagger
```
http://localhost:8005/docs
```

### Bước 2: Test endpoint đơn giản

**Test GET /api/gmail/contacts/1**

1. Click vào endpoint
2. Click "Try it out"
3. Nhập `user_id = 1`
4. Click "Execute"
5. Xem response

### Bước 3: Test send email

**Test POST /api/gmail/send**

1. Click endpoint
2. "Try it out"
3. Nhập JSON:
```json
{
  "user_id": 1,
  "to": "test@example.com",
  "subject": "Test",
  "body": "Hello from Swagger!"
}
```
4. Execute
5. Check response

---

## 🔐 OAuth Required

**Lưu ý:** Trước khi test, user phải:

1. Vào frontend: http://localhost:5173
2. Vào Settings
3. Connect Google Account
4. Cấp quyền Gmail

Nếu không, API sẽ trả về:
```json
{
  "detail": "Please connect Google Account in Settings"
}
```

---

## 🐛 Troubleshooting

### Lỗi 401: Not connected

**Giải pháp:**
- Kết nối Google trong Settings
- Check OAuth service đang chạy (port 8003)

### Lỗi 500: Gmail service not available

**Giải pháp:**
- Check `gmail_service.py` có trong folder không
- Restart service

### Lỗi: Token expired

**Giải pháp:**
- Disconnect và connect lại Google
- OAuth service sẽ tự refresh token

---

## 📊 Test Flow Hoàn Chỉnh

### Scenario: Gửi email xin nghỉ học

**Step 1: Get contacts**
```
GET /api/gmail/contacts/1
→ Lấy list giáo viên
```

**Step 2: Create draft**
```
POST /api/gmail/draft
{
  "subject_keyword": "xin nghỉ học",
  "recipient_name": "thầy Nguyễn Văn A"
}
→ AI generate nội dung
```

**Step 3: Send email**
```
POST /api/gmail/send
{
  "user_id": 1,
  "to": "teacher.a@tvu.edu.vn",
  "subject": "Xin phép nghỉ học",
  "body": "[Nội dung từ draft]"
}
→ Email được gửi!
```

---

## 🎯 Quick Test Commands

### Test với curl

**Read emails:**
```bash
curl -X POST http://localhost:8005/api/gmail/read \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "max_results": 3}'
```

**Get contacts:**
```bash
curl http://localhost:8005/api/gmail/contacts/1
```

**Send email:**
```bash
curl -X POST http://localhost:8005/api/gmail/send \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "to": "test@example.com",
    "subject": "Test",
    "body": "Hello!"
  }'
```

---

## 📝 Notes

- **Port:** 8005 (khác với main AI service port 8000)
- **OAuth Service:** Port 8003 (phải chạy song song)
- **Frontend:** Port 5173 (để connect Google)
- **Auto-reload:** Service tự restart khi sửa code

---

**Happy Testing! 🎉**
