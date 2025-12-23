# 🔍 Debug OAuth Callback Error

## Vấn đề hiện tại

Từ ảnh chụp màn hình:
- Người dùng đã xác thực thành công với Google
- Google redirect về callback URL: `localhost:8003/api/oauth/google/callback?state=...`
- **Nhưng hiển thị "Connection Failed"**

## Nguyên nhân có thể

### 1. ❌ Redirect URI không khớp (QUAN TRỌNG NHẤT)

**Kiểm tra:**
```
File .env: http://localhost:8003/api/oauth/google/callback
Google Console: ??? (cần kiểm tra)
```

**Cách fix:**
1. Mở: https://console.cloud.google.com/apis/credentials
2. Click OAuth Client ID: `477173705324-j441dqvann275pkv6tnv8omt2kdg0rsu`
3. Tìm "Authorized redirect URIs"
4. **PHẢI có chính xác:** `http://localhost:8003/api/oauth/google/callback`
5. Click SAVE

### 2. ❌ Spring Boot API /api/users/{userId}/google-tokens lỗi

**Callback flow:**
```
1. Google → callback với code
2. Python service exchange code → tokens
3. Python gọi Spring Boot: POST /api/users/{userId}/google-tokens
4. Nếu step 3 fail → "Connection Failed"
```

**Kiểm tra:**
```powershell
# Test Spring Boot endpoint
$body = @{
    accessToken = "test"
    refreshToken = "test"
    expiryTime = "2025-12-19T00:00:00"
    connected = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/api/users/1/google-tokens" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

Nếu lỗi 403/401 → Cần token JWT!

### 3. ❌ Database lỗi

Kiểm tra database có bảng `google_oauth_tokens` không:
```sql
SHOW TABLES LIKE 'google_oauth_tokens';
DESCRIBE google_oauth_tokens;
```

Nếu không có → Chạy migration:
```powershell
cd backend\SpringService\agentforedu
mysql -u root -p Agent_Db < database_migration_google_oauth_mysql.sql
```

### 4. ❌ Exception trong callback handler

**Xem log của OAuth service:**
- Mở terminal đang chạy `python google_oauth_service.py`
- Tìm dòng `OAuth callback error:`
- Copy error message

## Hành động ngay

### Bước 1: Enable detailed logging

Sửa file `google_oauth_service.py`, tìm hàm `oauth_callback`, thay đổi:

```python
@app.get("/api/oauth/google/callback", tags=["OAuth"])
async def oauth_callback(code: str, state: str):
    try:
        print(f"DEBUG: Callback received")
        print(f"  Code: {code[:30]}...")
        print(f"  State: {state}")
        
        # Decode state
        decoded_state = base64.urlsafe_b64decode(state.encode()).decode()
        user_id = int(decoded_state.split(':')[0])
        print(f"  User ID: {user_id}")
        
        # Exchange code for tokens
        print("DEBUG: Exchanging code for tokens...")
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_OAUTH_CLIENT_ID,
                "client_secret": GOOGLE_OAUTH_CLIENT_SECRET,
                "redirect_uri": GOOGLE_OAUTH_REDIRECT_URI,
                "grant_type": "authorization_code"
            }
        )
        
        print(f"DEBUG: Token response status: {token_response.status_code}")
        
        if token_response.status_code != 200:
            error_detail = token_response.json()
            print(f"ERROR: Token exchange failed: {error_detail}")
            raise HTTPException(
                status_code=400, 
                detail=f"Token exchange failed: {error_detail.get('error', 'unknown')}"
            )
        
        tokens = token_response.json()
        print(f"DEBUG: Got tokens, access_token length: {len(tokens.get('access_token', ''))}")
        
        # Save tokens
        print("DEBUG: Saving tokens to Spring Boot...")
        success = save_user_tokens(
            user_id=user_id,
            access_token=tokens['access_token'],
            refresh_token=tokens.get('refresh_token'),
            expires_in=tokens['expires_in']
        )
        
        print(f"DEBUG: Save tokens result: {success}")
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save tokens to database")
        
        # Return success HTML
        # ... (giữ nguyên phần HTML)
        
    except Exception as e:
        print(f"!!! EXCEPTION in callback: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return error HTML with detailed message
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OAuth Error</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 2rem;
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    color: white;
                }}
                .error {{
                    background: rgba(255,255,255,0.1);
                    padding: 1rem;
                    border-radius: 8px;
                    margin-top: 1rem;
                }}
            </style>
        </head>
        <body>
            <h1>❌ Connection Failed</h1>
            <p>Error Type: {type(e).__name__}</p>
            <div class="error">
                <pre>{str(e)}</pre>
            </div>
            <p>Please close this window and check the console logs.</p>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
```

### Bước 2: Restart OAuth service

```powershell
# Kill process
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *oauth*"

# Restart
cd backend\PythonService
python google_oauth_service.py
```

### Bước 3: Test lại OAuth flow

1. Vào app → Settings → Connect Google Account
2. Đăng nhập Google
3. **QUAN TRỌNG:** Xem terminal đang chạy OAuth service
4. Copy tất cả log khi callback xảy ra
5. Phân tích lỗi từ log

## Các lỗi thường gặp

### Error: "redirect_uri_mismatch"
```
Error: redirect_uri_mismatch
The redirect URI in the request: http://localhost:8003/api/oauth/google/callback 
does not match the ones authorized for the OAuth client.
```

**Fix:** Thêm chính xác URI đó vào Google Console

### Error: "invalid_grant"
```
Error: invalid_grant
The authorization code has expired or was already used.
```

**Fix:** 
- Code chỉ dùng được 1 lần
- Thử lại OAuth flow từ đầu
- Đảm bảo time đồng bộ giữa máy và Google

### Error: Failed to save tokens
```
Failed to save tokens to database
```

**Fix:**
- Kiểm tra Spring Boot có chạy không: `netstat -ano | findstr :8080`
- Kiểm tra database migration đã chạy chưa
- Test endpoint Spring Boot trực tiếp

### Error: Connection refused (Spring Boot)
```
ConnectionError: Cannot connect to http://localhost:8080
```

**Fix:** Start Spring Boot:
```powershell
cd backend\SpringService\agentforedu
mvn spring-boot:run
```

## Next Steps

Sau khi có log chi tiết, sẽ biết chính xác lỗi ở đâu và fix được ngay!
