# 🔧 Hướng dẫn Fix Lỗi OAuth "Connection Failed"

## 🐛 Nguyên nhân lỗi

Dựa vào ảnh chụp màn hình, lỗi xảy ra là **"Connection Failed"** tại callback URL: `localhost:8003/api/oauth/google/callback`

### Có 2 nguyên nhân chính:

1. **Redirect URI trong Google Console không khớp với .env**
2. **Backend service có lỗi khi xử lý callback**

---

## ✅ Bước 1: Kiểm tra Redirect URI trong Google Console

### 1.1. Mở Google Cloud Console
```
https://console.cloud.google.com/apis/credentials
```

### 1.2. Click vào OAuth 2.0 Client ID của bạn
- Tìm client có ID: `477173705324-j441dqvann275pkv6tnv8omt2kdg0rsu.apps.googleusercontent.com`

### 1.3. Kiểm tra "Authorized redirect URIs"
**PHẢI có URI này:**
```
http://localhost:8003/api/oauth/google/callback
```

**Nếu chỉ có URI cũ, XÓA và thêm URI mới:**
- ❌ Xóa: `http://localhost:8080/api/auth/google/callback`
- ✅ Thêm: `http://localhost:8003/api/oauth/google/callback`

### 1.4. Click **SAVE** (quan trọng!)

---

## ✅ Bước 2: Kiểm tra Backend Services

### 2.1. Kiểm tra OAuth Service (Port 8003)
Mở PowerShell và chạy:
```powershell
Invoke-RestMethod -Uri "http://localhost:8003/" -Method GET
```

**Kết quả mong đợi:**
```json
{
  "status": "running",
  "service": "Google OAuth Service",
  "oauth_configured": true
}
```

Nếu lỗi → OAuth service chưa chạy, chạy lại:
```powershell
cd backend\PythonService
python google_oauth_service.py
```

### 2.2. Kiểm tra log của OAuth service
Xem terminal đang chạy `google_oauth_service.py`, tìm lỗi khi callback.

---

## ✅ Bước 3: Kiểm tra Scopes trong OAuth Consent Screen

### 3.1. Mở OAuth Consent Screen
```
https://console.cloud.google.com/apis/credentials/consent
```

### 3.2. Kiểm tra Test Users
- Đảm bảo email `nguyenleduydhty@gmail.com` đã được thêm vào **Test users**
- Nếu chưa → Click **ADD USERS** → Thêm email → SAVE

### 3.3. Kiểm tra Scopes
App cần các scopes sau:
- `openid`
- `email`
- `profile`
- `https://www.googleapis.com/auth/cloud-platform`
- `https://www.googleapis.com/auth/cloud-vision`
- `https://www.googleapis.com/auth/cloud-translation`

---

## ✅ Bước 4: Restart Services và Test lại

### 4.1. Restart OAuth Service
```powershell
# Tìm process đang chạy trên port 8003
netstat -ano | findstr :8003

# Kill process (thay <PID> bằng số từ lệnh trên)
taskkill /PID <PID> /F

# Restart service
cd backend\PythonService
python google_oauth_service.py
```

### 4.2. Clear browser cache và cookies
- Mở Chrome DevTools (F12)
- Application → Storage → Clear site data
- Hoặc dùng Incognito mode

### 4.3. Test lại OAuth flow
1. Vào Settings → Google Integration
2. Click "Connect Google Account"
3. Đăng nhập Google
4. Cho phép các quyền
5. Kiểm tra xem có redirect về thành công không

---

## ✅ Bước 5: Debug chi tiết (nếu vẫn lỗi)

### 5.1. Kiểm tra response từ Google
Mở Chrome DevTools → Network tab

Khi click "Connect Google Account":
1. Request đến `/api/oauth/google/init` → Trả về `auth_url`
2. Redirect đến Google → Đăng nhập
3. Google redirect về `/api/oauth/google/callback?code=...&state=...`
4. Backend xử lý callback → Trả về HTML success hoặc error

**Nếu bước 4 fail:**
- Xem Console tab có error gì không
- Xem Network tab request `/api/oauth/google/callback` status code
- Xem Response body của request đó

### 5.2. Kiểm tra log chi tiết
Thêm logging vào `google_oauth_service.py`:

```python
@app.get("/api/oauth/google/callback", tags=["OAuth"])
async def oauth_callback(code: str, state: str):
    try:
        print(f"DEBUG: Received callback - code: {code[:20]}..., state: {state}")
        
        # ... existing code ...
        
    except Exception as e:
        print(f"ERROR in callback: {str(e)}")
        import traceback
        traceback.print_exc()
        # ... existing error handling ...
```

---

## 🔍 Common Issues

### Issue 1: "redirect_uri_mismatch"
→ **Fix:** URI trong Google Console phải 100% giống với `.env`

### Issue 2: "invalid_client"
→ **Fix:** Client ID hoặc Secret sai, kiểm tra lại `.env`

### Issue 3: "access_denied"
→ **Fix:** User từ chối quyền hoặc app chưa verified

### Issue 4: "Connection Failed" (như ảnh)
→ **Fix:** Backend callback handler bị lỗi
- Kiểm tra log của Python service
- Kiểm tra Spring Boot có chạy không (port 8080)
- Kiểm tra database connection

---

## 📞 Nếu vẫn lỗi

Cung cấp các thông tin sau:
1. Screenshot của Google Console → OAuth Client → Redirect URIs
2. Log từ terminal chạy `google_oauth_service.py`
3. Chrome DevTools → Network tab khi OAuth callback
4. File `.env` (che Client Secret)
