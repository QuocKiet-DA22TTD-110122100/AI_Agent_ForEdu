# 🧪 Test Google Calendar API

## Prerequisites
Đảm bảo các services đang chạy:
- ✅ OAuth Service (port 8003)
- ✅ Google Cloud Service (port 8004)
- ✅ AI Service (port 8000)
- ✅ Spring Boot (port 8080 hoặc 8081)

---

## Test 1: Lấy Events Hôm Nay

### PowerShell
```powershell
# Replace user_id with your actual user ID (from database)
$userId = 1

$response = Invoke-RestMethod -Uri "http://localhost:8004/api/google-cloud/calendar/today-events/$userId" -Method Get -ContentType "application/json"
$response | ConvertTo-Json -Depth 10
```

### Curl (Git Bash/WSL)
```bash
curl -X GET "http://localhost:8004/api/google-cloud/calendar/today-events/1" \
  -H "Content-Type: application/json"
```

### Expected Response
```json
{
  "success": true,
  "count": 2,
  "events": [
    {
      "id": "abc123",
      "summary": "Team Meeting",
      "description": "Weekly sync",
      "start": "2025-12-22T09:00:00+07:00",
      "end": "2025-12-22T10:00:00+07:00",
      "location": "Conference Room A",
      "html_link": "https://calendar.google.com/..."
    }
  ]
}
```

---

## Test 2: Tạo Event Mới

### PowerShell
```powershell
$userId = 1
$eventData = @{
    user_id = $userId
    summary = "Test Calendar Event"
    description = "Testing Google Calendar API integration"
    start_time = "2025-12-23T14:00:00+07:00"
    end_time = "2025-12-23T15:00:00+07:00"
    location = "Test Location"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8004/api/google-cloud/calendar/create-event" `
    -Method Post `
    -Body $eventData `
    -ContentType "application/json"

$response | ConvertTo-Json -Depth 10
```

### Curl
```bash
curl -X POST "http://localhost:8004/api/google-cloud/calendar/create-event" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "summary": "Test Calendar Event",
    "description": "Testing API",
    "start_time": "2025-12-23T14:00:00+07:00",
    "end_time": "2025-12-23T15:00:00+07:00",
    "location": "Test Room"
  }'
```

### Expected Response
```json
{
  "success": true,
  "message": "✅ Đã tạo sự kiện: Test Calendar Event",
  "event": {
    "id": "xyz789",
    "summary": "Test Calendar Event",
    "start": "2025-12-23T14:00:00+07:00",
    "end": "2025-12-23T15:00:00+07:00",
    "html_link": "https://calendar.google.com/calendar/event?eid=..."
  }
}
```

---

## Test 3: Lấy Events Trong Khoảng Thời Gian

### PowerShell
```powershell
$userId = 1
$requestData = @{
    user_id = $userId
    time_min = "2025-12-22T00:00:00+07:00"
    time_max = "2025-12-25T23:59:59+07:00"
    max_results = 20
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8004/api/google-cloud/calendar/list-events" `
    -Method Post `
    -Body $requestData `
    -ContentType "application/json"

Write-Host "Found $($response.count) events:" -ForegroundColor Green
$response.events | ForEach-Object {
    Write-Host "  - $($_.summary) at $($_.start)" -ForegroundColor Cyan
}
```

### Curl
```bash
curl -X POST "http://localhost:8004/api/google-cloud/calendar/list-events" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "time_min": "2025-12-22T00:00:00+07:00",
    "time_max": "2025-12-25T23:59:59+07:00",
    "max_results": 20
  }'
```

---

## Test 4: Xóa Event

### PowerShell
```powershell
$eventId = "xyz789"  # Replace with actual event ID from create response
$userId = 1

$response = Invoke-RestMethod -Uri "http://localhost:8004/api/google-cloud/calendar/delete-event/${eventId}?user_id=$userId" `
    -Method Delete `
    -ContentType "application/json"

$response | ConvertTo-Json
```

### Curl
```bash
curl -X DELETE "http://localhost:8004/api/google-cloud/calendar/delete-event/xyz789?user_id=1" \
  -H "Content-Type: application/json"
```

---

## Test 5: Test Qua Chat (AI Agent)

### PowerShell - Chat API
```powershell
$chatData = @{
    message = "Lịch hôm nay của tôi là gì?"
    use_rag = $false
    ai_provider = "gemini"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/chat" `
    -Method Post `
    -Body $chatData `
    -ContentType "application/json" `
    -Headers @{Authorization = "Bearer YOUR_JWT_TOKEN"}

Write-Host $response.response
```

### Test Messages
```
1. "Lịch hôm nay của tôi là gì?"
2. "Tạo lịch: Meeting với team vào 15:00 hôm nay"
3. "Nhắc tôi nộp báo cáo vào ngày mai lúc 10:00"
4. "Thêm sự kiện: Họp khách hàng vào thứ 6 tuần sau lúc 14:00"
```

---

## Full Test Script

Lưu file này: `test_calendar_api.ps1`

```powershell
# Test Google Calendar API Integration
Write-Host "================================" -ForegroundColor Cyan
Write-Host "🧪 TESTING GOOGLE CALENDAR API" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

$userId = 1  # Change to your user ID

# Test 1: Get Today's Events
Write-Host "`n📅 Test 1: Getting today's events..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8004/api/google-cloud/calendar/today-events/$userId" `
        -Method Get -ContentType "application/json"
    
    if ($response.success) {
        Write-Host "✅ Success! Found $($response.count) events" -ForegroundColor Green
        $response.events | ForEach-Object {
            Write-Host "  - $($_.summary) at $($_.start)" -ForegroundColor White
        }
    } else {
        Write-Host "❌ Failed: $($response.message)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

# Test 2: Create New Event
Write-Host "`n📝 Test 2: Creating new event..." -ForegroundColor Yellow
try {
    $tomorrow = (Get-Date).AddDays(1)
    $startTime = $tomorrow.ToString("yyyy-MM-ddT10:00:00+07:00")
    $endTime = $tomorrow.ToString("yyyy-MM-ddT11:00:00+07:00")
    
    $eventData = @{
        user_id = $userId
        summary = "API Test Event - $(Get-Date -Format 'HH:mm:ss')"
        description = "Created via PowerShell test script"
        start_time = $startTime
        end_time = $endTime
        location = "Test Location"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:8004/api/google-cloud/calendar/create-event" `
        -Method Post -Body $eventData -ContentType "application/json"
    
    if ($response.success) {
        Write-Host "✅ Success! Event created: $($response.event.summary)" -ForegroundColor Green
        Write-Host "   ID: $($response.event.id)" -ForegroundColor Gray
        Write-Host "   Link: $($response.event.html_link)" -ForegroundColor Blue
        
        # Save event ID for deletion test
        $script:createdEventId = $response.event.id
    } else {
        Write-Host "❌ Failed: $($response.message)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

# Test 3: List Events (Next 7 days)
Write-Host "`n📋 Test 3: Listing events for next 7 days..." -ForegroundColor Yellow
try {
    $now = Get-Date
    $timeMin = $now.ToString("yyyy-MM-ddTHH:mm:ss+07:00")
    $timeMax = $now.AddDays(7).ToString("yyyy-MM-ddTHH:mm:ss+07:00")
    
    $listData = @{
        user_id = $userId
        time_min = $timeMin
        time_max = $timeMax
        max_results = 10
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:8004/api/google-cloud/calendar/list-events" `
        -Method Post -Body $listData -ContentType "application/json"
    
    if ($response.success) {
        Write-Host "✅ Success! Found $($response.count) upcoming events" -ForegroundColor Green
        $response.events | ForEach-Object {
            $date = ([DateTime]$_.start).ToString("dd/MM HH:mm")
            Write-Host "  - $date : $($_.summary)" -ForegroundColor White
        }
    } else {
        Write-Host "❌ Failed: $($response.message)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

# Test 4: Delete Event (if created)
if ($script:createdEventId) {
    Write-Host "`n🗑️  Test 4: Deleting created event..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod `
            -Uri "http://localhost:8004/api/google-cloud/calendar/delete-event/$($script:createdEventId)?user_id=$userId" `
            -Method Delete -ContentType "application/json"
        
        if ($response.success) {
            Write-Host "✅ Success! Event deleted" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed: $($response.message)" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
    }
} else {
    Write-Host "`n⏭️  Test 4: Skipped (no event to delete)" -ForegroundColor Gray
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "✅ ALL TESTS COMPLETED" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
```

---

## Chạy Test Script

```powershell
# Lưu script ở trên vào file
Set-Location "C:\Users\canhn\Downloads\DACN\DACN"

# Chạy test
.\test_calendar_api.ps1
```

---

## Troubleshooting

### Error: "Connection refused" hoặc "Unable to connect"
➡️ Service chưa chạy. Start services:
```powershell
# Terminal 1: OAuth Service
cd backend\PythonService
python google_oauth_service.py

# Terminal 2: Google Cloud Service  
python google_cloud_service_oauth.py

# Terminal 3: AI Service
python main.py
```

### Error: "Please connect your Google account"
➡️ User chưa kết nối Google:
1. Vào Settings trong web app
2. Click "Connect Google"
3. Authorize Calendar permissions

### Error: "Token expired"
➡️ Token hết hạn:
1. Disconnect Google account
2. Reconnect để lấy token mới

### Error: "User ID not found"
➡️ Kiểm tra user_id trong database:
```sql
SELECT id, username, email FROM users;
```

---

## Check Services Health

```powershell
# Check all services
$ports = @(8003, 8004, 8000, 8080)
foreach ($port in $ports) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$port" -TimeoutSec 2 -UseBasicParsing
        Write-Host "✅ Port $port is running" -ForegroundColor Green
    } catch {
        Write-Host "❌ Port $port is NOT running" -ForegroundColor Red
    }
}
```

---

## Verify On Google Calendar

Sau khi test:
1. Mở https://calendar.google.com
2. Đăng nhập với tài khoản đã connect
3. Kiểm tra events vừa tạo có xuất hiện không
4. Click vào event để xem details

---

## 🎯 Quick Test Commands

### Tạo event nhanh
```powershell
Invoke-RestMethod -Uri "http://localhost:8004/api/google-cloud/calendar/create-event" `
  -Method Post -ContentType "application/json" -Body '{
    "user_id": 1,
    "summary": "Quick Test",
    "start_time": "2025-12-23T15:00:00+07:00",
    "end_time": "2025-12-23T16:00:00+07:00"
  }' | ConvertTo-Json
```

### Xem lịch hôm nay
```powershell
Invoke-RestMethod "http://localhost:8004/api/google-cloud/calendar/today-events/1" | ConvertTo-Json
```
