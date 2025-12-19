# 🔐 Hướng dẫn Tạo Google OAuth Credentials

## Bước 1: Truy cập Google Cloud Console

1. Vào: [https://console.cloud.google.com](https://console.cloud.google.com)
2. Đăng nhập bằng tài khoản Gmail

## Bước 2: Tạo Project (nếu chưa có)

1. Click **"Select a Project"** (góc trên cùng)
2. Click **"New Project"**
3. Nhập tên: `EduAgent OAuth`
4. Click **"Create"**
5. Chờ project được tạo xong (2-3 phút)

## Bước 3: Bật Google+ API

1. Ở sidebar trái, tìm **APIs & Services** → **Library**
2. Tìm kiếm: `Google+ API`
3. Click vào kết quả
4. Click **"Enable"** (nút xanh)

## Bước 4: Tạo OAuth 2.0 Credentials

1. Ở sidebar, click **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** (góc trên)
3. Chọn **"OAuth 2.0 Client ID"**
4. Nếu bị hỏi "Configure OAuth consent screen":
   - Click **"Configure Consent Screen"**
   - Chọn **External** → Click **"Create"**
   - Điền:
     - **App name**: `EduAgent`
     - **User support email**: your-email@gmail.com
     - Scroll xuống, click **"Add or Remove Scopes"**
     - Tìm và chọn:
       - `openid`
       - `email`
       - `profile`
     - Lưu lại
   - Quay lại **Credentials**, click **"+ CREATE CREDENTIALS"** → **"OAuth 2.0 Client ID"**

5. Chọn **Application type**: **Web application**

6. Nhập **Name**: `EduAgent Web Client`

7. Thêm **Authorized redirect URIs**:
   ```
   http://localhost:3000/api/auth/callback
   http://localhost:5173/api/auth/callback
   http://localhost:8003/api/oauth/google/callback
   http://localhost:8080/api/oauth/google/callback
   ```

8. Click **"Create"**

## Bước 5: Copy Client ID

Một dialog sẽ pop-up hiển thị:
- **Client ID**: `YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com`
- **Client Secret**: `YOUR_GOOGLE_CLIENT_SECRET`

📌 **QUAN TRỌNG**: Sao chép 2 cái này, bạn sẽ cần dùng!

## Bước 6: Cập nhật Config

### Frontend (.env hoặc vite.config.ts)
```env
VITE_GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
```

### Backend Python (PythonService/.env)
```env
GOOGLE_OAUTH_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
GOOGLE_OAUTH_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET
GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8003/api/oauth/google/callback
```

## Bước 7: Setup Email (Gmail SMTP)

1. Vào: [https://myaccount.google.com](https://myaccount.google.com)
2. Click **"Security"** (sidebar trái)
3. Bật **2-Step Verification** (nếu chưa)
4. Ở mục "App passwords":
   - Chọn **App**: `Mail`
   - Chọn **Device**: `Windows Computer`
   - Click **"Generate"**
   - Google sẽ tạo password 16 ký tự
   - Copy password này

5. Cập nhật `application.yaml`:
```yaml
spring:
  mail:
    host: smtp.gmail.com
    port: 587
    username: your-email@gmail.com
    password: your-app-password-16-char
```

## ✅ Xác nhận Setup

Chạy test script để kiểm tra:
```bash
python test-oauth-flow.py
```

