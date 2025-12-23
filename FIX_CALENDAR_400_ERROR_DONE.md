# ✅ Đã Fix Lỗi 400 Bad Request - Calendar API

## 🐛 Vấn đề
Lỗi **400 Bad Request** khi tạo Calendar event từ frontend:
```
POST http://localhost:8004/api/google-cloud/calendar/create-event
Status: 400 Bad Request
```

## 🔍 Nguyên nhân
Frontend gửi thời gian dạng `datetime-local` HTML:
```
start_time: "2025-12-23T14:30"    ❌ Thiếu timezone
end_time: "2025-12-23T15:30"      ❌ Thiếu timezone
```

Backend yêu cầu ISO 8601 **với timezone**:
```
start_time: "2025-12-23T14:30:00+07:00"  ✅ Đúng format
end_time: "2025-12-23T15:30:00+07:00"    ✅ Đúng format
```

## ✅ Giải pháp đã áp dụng

### 1. **Frontend Fix** - Thêm timezone vào datetime
File: `fronend_web/src/pages/GoogleCalendarPage.tsx`

```typescript
const handleCreateEvent = async (e: React.FormEvent) => {
  // Convert datetime-local to ISO 8601 with timezone
  const formatDateTime = (datetime: string) => {
    const withSeconds = datetime + ':00';
    return withSeconds + '+07:00';  // Vietnam timezone
  };

  const event = await calendarService.createEvent({
    user_id: user.id,
    summary,
    description,
    start_time: formatDateTime(startTime),  // ✅ Add timezone
    end_time: formatDateTime(endTime),      // ✅ Add timezone
    location,
  });
};
```

### 2. **Backend Validation** - Kiểm tra format ngay từ đầu
File: `backend/PythonService/google_cloud_service_oauth.py`

```python
@app.post("/api/google-cloud/calendar/create-event")
async def create_calendar_event(request: CalendarEventRequest):
    # Validate datetime format
    if '+' not in request.start_time and 'Z' not in request.start_time:
        raise HTTPException(
            status_code=400, 
            detail="Invalid format. Use ISO 8601 with timezone"
        )
```

### 3. **Auto-fill Default Time** - Tiện lợi hơn cho user
```typescript
// Khi mở form, tự động điền:
// - Start time: 1 giờ sau (làm tròn)
// - End time: 2 giờ sau
useEffect(() => {
  if (showCreateModal && !startTime) {
    const now = new Date();
    now.setHours(now.getHours() + 1, 0, 0, 0);
    setStartTime(now.toISOString().slice(0, 16));
    
    const end = new Date(now);
    end.setHours(end.getHours() + 1);
    setEndTime(end.toISOString().slice(0, 16));
  }
}, [showCreateModal]);
```

## 🧪 Test ngay

### 1. Restart frontend
```powershell
cd fronend_web
npm run dev
```

### 2. Test qua UI
1. Mở http://localhost:5173/calendar
2. Click nút **"+ Tạo Sự Kiện"**
3. Điền form (thời gian đã được auto-fill):
   - **Tiêu đề**: Test Event
   - **Start time**: (đã có sẵn)
   - **End time**: (đã có sẵn)
4. Click **Tạo**
5. ✅ Thành công!

### 3. Test qua API (Swagger)
```
http://localhost:8004/docs
```

Test với payload:
```json
{
  "user_id": 3,
  "summary": "Test Event",
  "description": "Testing calendar",
  "start_time": "2025-12-25T10:00:00+07:00",
  "end_time": "2025-12-25T11:00:00+07:00"
}
```

### 4. Xem Backend Logs
Backend giờ sẽ in ra:
```
🔍 DEBUG - Creating calendar event for user 3
📍 API URL: https://www.googleapis.com/calendar/v3/calendars/primary/events
📝 Event data: {...}
📊 Response status: 200
```

## 📊 Kết quả mong đợi

### ✅ Success Response (200)
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

### ❌ Error Cases

**400 - Missing timezone:**
```json
{
  "detail": "Invalid start_time format. Use ISO 8601 with timezone"
}
```

**401 - Not connected:**
```json
{
  "detail": "Please connect your Google account to use Calendar"
}
```

**403 - No permission:**
```json
{
  "detail": "Calendar API error: Insufficient Permission"
}
```
→ Xem [FIX_CALENDAR_403_ERROR.md](FIX_CALENDAR_403_ERROR.md)

## 🎯 Checklist

- [x] Frontend format datetime đúng ISO 8601 với timezone
- [x] Backend validate datetime format
- [x] Debug logging để dễ troubleshoot
- [x] Auto-fill default time cho UX tốt hơn
- [x] Clear error messages

## 📝 Notes

- **Timezone**: Hiện tại hardcode `+07:00` (Vietnam timezone)
- **Format**: ISO 8601 với timezone là bắt buộc cho Google Calendar API
- **Validation**: Backend kiểm tra format trước khi call Google API
- **User Experience**: Form tự động điền thời gian mặc định

## 🔗 Related Docs

- [Google Calendar API - Events](https://developers.google.com/calendar/api/v3/reference/events)
- [ISO 8601 DateTime Format](https://en.wikipedia.org/wiki/ISO_8601)
- [FIX_CALENDAR_403_ERROR.md](FIX_CALENDAR_403_ERROR.md) - Nếu gặp lỗi 403
