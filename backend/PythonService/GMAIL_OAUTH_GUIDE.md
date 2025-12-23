# 📧 Gmail API Integration với OAuth 2.0

## 🎯 Tổng quan

Tích hợp Gmail API cho phép AI Assistant:
- 📬 **Đọc email** trong inbox của người dùng
- ✉️ **Gửi email** thay mặt người dùng
- 🔍 **Tìm kiếm email** theo từ khóa, người gửi, ngày...

## 🔐 OAuth 2.0 là gì?

OAuth 2.0 (Open Authorization) là giao thức ủy quyền chuẩn công nghiệp, cho phép ứng dụng truy cập tài nguyên của người dùng mà không cần lưu mật khẩu.

### Flow hoạt động:

```
┌─────────────┐     1. Request Auth      ┌──────────────┐
│   User      │  ─────────────────────>  │   AI App     │
│ (Browser)   │                          │              │
└─────────────┘                          └──────────────┘
       │                                        │
       │                                        │ 2. Redirect to Google
       │                                        │
       ▼                                        ▼
┌─────────────┐     3. User Login        ┌──────────────┐
│   Google    │  <─────────────────────  │   Google     │
│   Login     │                          │   OAuth      │
│   Page      │  ─────────────────────>  │   Server     │
└─────────────┘     4. Authorization     └──────────────┘
                         Code                   │
       │                                        │
       │                                        │ 5. Exchange Code
       │                                        │    for Tokens
       ▼                                        ▼
┌─────────────┐     6. Access Token      ┌──────────────┐
│   AI can    │  <─────────────────────  │   Token      │
│   access    │                          │   Response   │
│   Gmail     │                          │              │
└─────────────┘                          └──────────────┘
```

### Các thành phần:
1. **Authorization Code**: Mã tạm thời dùng để đổi lấy token
2. **Access Token**: Token ngắn hạn (1 giờ) để gọi API
3. **Refresh Token**: Token dài hạn để lấy access token mới

## 📁 Cấu trúc Files

```
PythonService/
├── google_oauth_service.py   # OAuth server (port 8003)
├── gmail_service.py          # Gmail API wrapper
├── agent_features.py         # AI intent detection & handlers
└── main.py                   # Main API server
```

## 🔧 Cấu hình Google Cloud

### 1. Tạo Project trên Google Cloud Console

1. Truy cập [Google Cloud Console](https://console.cloud.google.com)
2. Tạo project mới hoặc chọn project có sẵn
3. Vào **APIs & Services > Library**
4. Bật **Gmail API**

### 2. Tạo OAuth Credentials

1. Vào **APIs & Services > Credentials**
2. Click **Create Credentials > OAuth client ID**
3. Chọn **Web application**
4. Thêm Authorized redirect URIs:
   ```
   http://localhost:8003/auth/callback/google
   http://localhost:3000/oauth/callback
   ```
5. Copy **Client ID** và **Client Secret**

### 3. Cấu hình OAuth Consent Screen

1. Vào **OAuth consent screen**
2. Chọn **External** (cho testing)
3. Thêm scopes:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/gmail.compose`
   - `https://www.googleapis.com/auth/gmail.modify`

### 4. File .env

```env
# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
OAUTH_REDIRECT_URI=http://localhost:8003/auth/callback/google
OAUTH_SERVICE_URL=http://localhost:8003

# Gmail API
GMAIL_API_ENABLED=true
```

## 💬 Cách sử dụng với AI

### Đọc Email
```
User: "Đọc email của tôi"
User: "Xem hộp thư đến"
User: "Tôi có email mới không?"
User: "Đọc email chưa đọc"
```

### Gửi Email
```
User: "Gửi email cho teacher@tvu.edu.vn chủ đề Xin nghỉ học nội dung Em xin phép nghỉ học ngày mai"
```

### Tìm kiếm Email
```
User: "Tìm email từ teacher@tvu.edu.vn"
User: "Tìm email về thời khóa biểu"
```

## 🚀 Chạy Service

### 1. Start OAuth Service
```powershell
cd backend/PythonService
python google_oauth_service.py
# Running on port 8003
```

### 2. Start Main AI Service
```powershell
python main.py
# Running on port 8000
```

### 3. Kết nối Google Account

1. Truy cập: `http://localhost:8003/auth/google?user_id=1`
2. Đăng nhập Google và cấp quyền
3. Callback sẽ lưu token

## 🔒 Bảo mật

### Token Storage
- Tokens được lưu trong file `oauth_tokens.json` (development)
- Production nên dùng database với encryption

### Token Refresh
- Access token tự động refresh khi expired
- Refresh token có thể bị thu hồi nếu:
  - User thu hồi quyền
  - Token không sử dụng 6 tháng
  - Password Google thay đổi

### Scopes tối thiểu
Chỉ request scopes thực sự cần:
- `gmail.readonly` - Chỉ đọc
- `gmail.send` - Chỉ gửi
- `gmail.modify` - Đọc + sửa + xóa

## 🧪 Testing

```python
# Test đọc email
import requests

# 1. Get token
token_resp = requests.get("http://localhost:8003/api/oauth/google/token/1")
access_token = token_resp.json()['access_token']

# 2. Call Gmail API
headers = {"Authorization": f"Bearer {access_token}"}
inbox = requests.get(
    "https://gmail.googleapis.com/gmail/v1/users/me/messages",
    headers=headers,
    params={"maxResults": 5}
)
print(inbox.json())
```

## ❓ Troubleshooting

### "Token expired"
- Tự động refresh bằng refresh token
- Nếu refresh thất bại, yêu cầu user đăng nhập lại

### "Insufficient permission"
- Kiểm tra scopes trong OAuth consent screen
- User cần re-authorize với scopes mới

### "Access blocked: This app's request is invalid"
- Redirect URI không khớp
- Client ID/Secret sai

## 📚 Tài liệu tham khảo

- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [Gmail API Reference](https://developers.google.com/gmail/api/reference/rest)
- [OAuth 2.0 Scopes for Gmail](https://developers.google.com/gmail/api/auth/scopes)
