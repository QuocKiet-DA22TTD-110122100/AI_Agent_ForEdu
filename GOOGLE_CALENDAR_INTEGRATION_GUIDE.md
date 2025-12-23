# 📅 Google Calendar Integration Guide

## ✅ Đã Hoàn Thành

Đã tích hợp **Google Calendar API** vào hệ thống! Bây giờ bạn có thể:
- Tạo sự kiện trên Google Calendar từ chatbot
- Xem lịch hôm nay
- Đồng bộ TKB lên Calendar
- Nhắc deadline và cuộc họp

---

## 🔧 Cấu Hình

### 1. OAuth Scopes Đã Thêm

Trong `google_oauth_service.py`:
```python
SCOPES = [
    # ... existing scopes ...
    # Calendar API
    "https://www.googleapis.com/auth/calendar",           # Full calendar access
    "https://www.googleapis.com/auth/calendar.events",    # Manage events
]
```

### 2. Backend Services

**Google Cloud Service** (`google_cloud_service_oauth.py`):
- Port: 8004
- Endpoints:
  - `POST /api/google-cloud/calendar/create-event` - Tạo event
  - `POST /api/google-cloud/calendar/list-events` - Lấy danh sách events
  - `GET /api/google-cloud/calendar/today-events/{user_id}` - Events hôm nay
  - `DELETE /api/google-cloud/calendar/delete-event/{event_id}` - Xóa event

---

## 🎯 Cách Sử Dụng

### A. Trong Chat (AI Agent)

Sau khi đã kết nối Google Account (như trong ảnh Settings), bạn có thể:

#### 1. Xem lịch hôm nay
```
"Lịch hôm nay của tôi là gì?"
"What's my schedule today?"
"Hôm nay tôi có event gì không?"
```

**Response:**
```
📅 Lịch hôm nay (3 sự kiện):

1. Stand-up Meeting
   ⏰ 09:00
   📍 Conference Room A

2. Client Presentation
   ⏰ 14:00
   📍 Zoom

3. Team Dinner
   ⏰ 18:30
   📍 ABC Restaurant
```

#### 2. Tạo sự kiện mới
```
"Tạo lịch: Meeting với client vào hôm nay lúc 15:00"
"Nhắc tôi: Nộp báo cáo vào ngày mai lúc 10:00"
"Thêm sự kiện: Họp team vào 14:30"
```

**Response:**
```
📅 Đã tạo sự kiện trên Google Calendar:

Tiêu đề: Meeting với client
Thời gian: 2025-12-22T15:00:00+07:00 → 2025-12-22T16:00:00+07:00

🔗 [Xem trên Calendar](https://calendar.google.com/...)
```

#### 3. Tạo với thời gian cụ thể
```
"Tạo lịch: Đi du lịch Đà Lạt ngày 25/12 lúc 08:00, kéo dài 3 giờ"
"Thêm deadline: Nộp luận văn vào 30/12/2025 lúc 23:59"
```

---

### B. API Direct Call

#### 1. Tạo Event

**Request:**
```http
POST http://localhost:8004/api/google-cloud/calendar/create-event
Content-Type: application/json

{
  "user_id": 1,
  "summary": "Sprint Planning Meeting",
  "description": "Plan for Sprint 15",
  "start_time": "2025-12-25T09:00:00+07:00",
  "end_time": "2025-12-25T10:30:00+07:00",
  "location": "Office - Room 301",
  "attendees": ["team@example.com", "manager@example.com"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "✅ Đã tạo sự kiện: Sprint Planning Meeting",
  "event": {
    "id": "abc123xyz",
    "summary": "Sprint Planning Meeting",
    "start": "2025-12-25T09:00:00+07:00",
    "end": "2025-12-25T10:30:00+07:00",
    "html_link": "https://calendar.google.com/event?eid=..."
  }
}
```

#### 2. Lấy Events Hôm Nay

**Request:**
```http
GET http://localhost:8004/api/google-cloud/calendar/today-events/1
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "events": [
    {
      "id": "event1",
      "summary": "Morning Standup",
      "description": "Daily team sync",
      "start": "2025-12-22T09:00:00+07:00",
      "end": "2025-12-22T09:30:00+07:00",
      "location": "Zoom",
      "html_link": "https://calendar.google.com/..."
    }
  ]
}
```

#### 3. Lấy Events Trong Khoảng Thời Gian

**Request:**
```http
POST http://localhost:8004/api/google-cloud/calendar/list-events
Content-Type: application/json

{
  "user_id": 1,
  "time_min": "2025-12-22T00:00:00+07:00",
  "time_max": "2025-12-25T23:59:59+07:00",
  "max_results": 20
}
```

#### 4. Xóa Event

**Request:**
```http
DELETE http://localhost:8004/api/google-cloud/calendar/delete-event/abc123xyz?user_id=1
```

---

## 🤖 Google Cloud Agent

File: `google_cloud_agent.py`

### Intent Detection
```python
def detect_calendar_intent(self, message: str) -> bool:
    """Phát hiện intent liên quan đến lịch"""
    patterns = [
        r'tạo.*lịch',
        r'thêm.*sự kiện',
        r'nhắc.*tôi',
        r'calendar.*event',
        r'lịch.*hôm nay',
        r'meeting',
        r'cuộc họp',
        r'deadline'
    ]
    return any(re.search(pattern, message.lower()) for pattern in patterns)
```

### Auto Parse Request
Agent tự động phân tích message để:
- Trích xuất tên sự kiện
- Phát hiện thời gian (hôm nay, ngày mai, specific date)
- Xác định duration (mặc định 1 giờ)

**Ví dụ:**
```python
message = "Tạo lịch: Meeting với khách vào hôm nay lúc 14:30, kéo dài 2 giờ"

# Agent tự parse thành:
{
    "summary": "Meeting với khách",
    "start_time": "2025-12-22T14:30:00+07:00",
    "end_time": "2025-12-22T16:30:00+07:00",
    "description": None
}
```

---

## 🚀 Chạy Services

### 1. Start OAuth Service
```powershell
cd backend\PythonService
python google_oauth_service.py
```
→ Port 8003

### 2. Start Google Cloud Service
```powershell
python google_cloud_service_oauth.py
```
→ Port 8004

### 3. Start AI Service
```powershell
python main.py
```
→ Port 8000

---

## 📝 Use Cases

### 1. Đồng Bộ TKB Lên Calendar

Khi người dùng hỏi "TKB tuần này", AI có thể:
1. Lấy TKB từ TVU Portal
2. Tự động tạo events trên Google Calendar
3. Set reminder trước mỗi lớp 30 phút

**Flow:**
```python
# 1. Get TKB
schedules = tvu_scraper.get_weekly_schedule(mssv, password)

# 2. Create Calendar events
for schedule in schedules:
    google_cloud_agent.create_calendar_event(
        user_id=user.id,
        summary=schedule['subject'],
        start_time=schedule['start_datetime'],
        end_time=schedule['end_datetime'],
        location=schedule['room']
    )
```

### 2. Smart Reminders

"Nhắc tôi nộp báo cáo vào 25/12"
→ Tạo event với reminder

### 3. Meeting Scheduler

"Đặt lịch meeting với team vào thứ 6 tuần sau lúc 2 giờ"
→ Parse date → Create event → Invite attendees

### 4. Study Planning

"Tạo lịch học: Toán Cao Cấp vào thứ 2-4-6 lúc 7:00 sáng"
→ Recurring events

---

## 🔐 Bảo Mật

- **OAuth 2.0**: User phải kết nối Google Account
- **Access Token**: Được mã hóa và lưu trong MySQL
- **Auto Refresh**: Token tự động refresh khi hết hạn
- **Per-User**: Mỗi user có token riêng

---

## 📊 Benefits

✅ **Tiện lợi**: Tạo lịch bằng ngôn ngữ tự nhiên
✅ **Đồng bộ**: Tự động sync TKB lên Google Calendar
✅ **Nhắc nhở**: Notification trên phone/email
✅ **Chia sẻ**: Dễ dàng share events với bạn bè
✅ **Cross-platform**: Truy cập mọi lúc mọi nơi

---

## 🎯 Test Flow

### Bước 1: Kết Nối Google Account
1. Vào Settings trong app
2. Click "Connect Google"
3. Authorize các permissions (bao gồm Calendar)
4. Xác nhận "Google Account Connected" ✅

### Bước 2: Test Trong Chat
```
User: "Lịch hôm nay của tôi là gì?"
AI: [Shows today's events from Google Calendar]

User: "Tạo lịch: Họp team vào 15:00 hôm nay"
AI: "✅ Đã tạo sự kiện: Họp team"

User: "Nhắc tôi nộp báo cáo vào ngày mai lúc 10:00"
AI: "✅ Đã tạo sự kiện trên Calendar với reminder"
```

### Bước 3: Verify Trên Google Calendar
- Mở Google Calendar (calendar.google.com)
- Kiểm tra events đã được tạo
- Click vào event để xem details

---

## 🔮 Future Enhancements

### Phase 2
- [ ] Recurring events (repeat daily/weekly)
- [ ] Smart scheduling (find free slots)
- [ ] Calendar color coding by subject
- [ ] Integration with Google Meet (auto create meeting links)

### Phase 3
- [ ] Share calendar with classmates
- [ ] Group study planning
- [ ] Exam countdown on calendar
- [ ] Auto-suggest study schedule based on exam dates

---

## ✨ Summary

**Google Calendar API đã sẵn sàng sử dụng!** 🎉

Người dùng có thể:
1. ✅ Xem lịch hôm nay từ chat
2. ✅ Tạo events bằng ngôn ngữ tự nhiên
3. ✅ Đồng bộ TKB lên Calendar
4. ✅ Nhận notifications trên mọi thiết bị
5. ✅ Quản lý deadline và meetings

**Test ngay bây giờ trong chatbot!** 🚀
