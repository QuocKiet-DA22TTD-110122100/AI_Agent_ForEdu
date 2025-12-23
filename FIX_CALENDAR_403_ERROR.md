# 🔧 Fix Calendar 403 Forbidden Error

## 📋 Vấn đề
Lỗi **403 Forbidden** khi tạo sự kiện Calendar qua endpoint:
```
POST http://localhost:8004/api/google-cloud/calendar/create-event
```

## 🔍 Nguyên nhân có thể
1. **OAuth token thiếu quyền Calendar** - User đã kết nối Google nhưng không có scope Calendar
2. **Calendar API chưa được bật** trong Google Cloud Console
3. **Token đã hết hạn hoặc không hợp lệ**
4. **User chưa kết nối Google Account**

## ✅ Các bước khắc phục

### Bước 1: Kiểm tra trạng thái token
```bash
# Test endpoint mới để kiểm tra token
curl http://localhost:8004/api/google-cloud/debug/token-info/{user_id}
```

Hoặc mở trình duyệt:
```
http://localhost:8004/api/google-cloud/debug/token-info/1
```

Kết quả sẽ cho biết:
- ✅ Token có hợp lệ không
- ✅ Có quyền truy cập Calendar không
- ❌ Lỗi cụ thể nếu có

### Bước 2: Kích hoạt Calendar API trong Google Cloud Console

1. Mở [Google Cloud Console](https://console.cloud.google.com)
2. Chọn project của bạn
3. Vào **APIs & Services** > **Library**
4. Tìm "Google Calendar API"
5. Click **ENABLE** nếu chưa bật

### Bước 3: Kiểm tra OAuth Scopes

File `google_oauth_service.py` phải có các scope sau:
```python
SCOPES = [
    "https://www.googleapis.com/auth/calendar",           # Full calendar access
    "https://www.googleapis.com/auth/calendar.events",    # Manage events
]
```

✅ **ĐÃ ĐƯỢC CẤU HÌNH** - Scopes đã có trong code

### Bước 4: Ngắt kết nối và kết nối lại Google Account

Nếu user đã kết nối Google trước khi thêm Calendar scope:

1. **Trong frontend:**
   - Vào Settings/Profile
   - Disconnect Google Account
   - Connect lại

2. **Hoặc qua Google:**
   - Vào https://myaccount.google.com/permissions
   - Xóa quyền truy cập của app
   - Đăng nhập lại trong app

### Bước 5: Kiểm tra console logs

Sau khi fix code, backend sẽ in ra logs chi tiết:
```
🔍 DEBUG - Creating calendar event for user 1
📍 API URL: https://www.googleapis.com/calendar/v3/calendars/primary/events
📝 Event data: {...}
🔑 Token (first 20 chars): ya29.a0AfB_byBi...
📊 Response status: 403
📄 Response body: {"error": {...}}
```

Xem logs để biết lỗi cụ thể từ Google Calendar API.

## 🧪 Test nhanh

### 1. Test với Swagger UI
```
http://localhost:8004/docs
```

1. Vào endpoint `/api/google-cloud/debug/token-info/{user_id}`
2. Nhập `user_id` (thường là 1)
3. Click "Execute"
4. Xem kết quả:
   - `calendar_access_success: true` → OK ✅
   - `calendar_access_success: false` → Có vấn đề ❌

### 2. Test tạo event đơn giản
```json
POST http://localhost:8004/api/google-cloud/calendar/create-event
Content-Type: application/json

{
  "user_id": 1,
  "summary": "Test Event",
  "description": "Testing calendar API",
  "start_time": "2025-12-25T10:00:00+07:00",
  "end_time": "2025-12-25T11:00:00+07:00"
}
```

## 🔄 Restart services sau khi fix

```powershell
# Restart Python service
.\restart-ai-service.ps1

# Hoặc manual
Get-Process python | Stop-Process -Force
cd backend\PythonService
python google_cloud_service_oauth.py
```

## 📞 Nếu vẫn lỗi

Kiểm tra các điều sau:

1. **Google Cloud Console:**
   - Calendar API đã enable chưa?
   - OAuth consent screen đã publish chưa?
   - Có thông báo lỗi gì không?

2. **Database:**
   ```sql
   -- Kiểm tra user có OAuth token không
   SELECT id, username, google_connected, token_expiry 
   FROM users WHERE id = 1;
   
   -- Nếu có OAuth tokens table
   SELECT user_id, scope, expires_at 
   FROM oauth_tokens WHERE user_id = 1;
   ```

3. **Environment variables:**
   ```bash
   GOOGLE_OAUTH_CLIENT_ID=...
   GOOGLE_OAUTH_CLIENT_SECRET=...
   GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8080/api/auth/google/callback
   ```

## 🎯 Kết quả mong muốn

Sau khi fix xong, API sẽ trả về:
```json
{
  "success": true,
  "message": "✅ Đã tạo sự kiện: Test Event",
  "event": {
    "id": "abc123...",
    "summary": "Test Event",
    "start": "2025-12-25T10:00:00+07:00",
    "end": "2025-12-25T11:00:00+07:00",
    "html_link": "https://calendar.google.com/..."
  }
}
```

## 📚 Tài liệu tham khảo

- [Google Calendar API Documentation](https://developers.google.com/calendar/api/v3/reference)
- [OAuth 2.0 Scopes for Google APIs](https://developers.google.com/identity/protocols/oauth2/scopes#calendar)
- [Troubleshooting 403 Errors](https://cloud.google.com/storage/docs/troubleshooting#403)
