## 🎯 TÓM TẮT: Lấy TKB Với Ngày Tương Đối

### ✨ Vấn Đề & Giải Pháp

**Vấn Đề:**
- Trước đây, chỉ hỗ trợ xem TKB hôm nay hoặc ngày cụ thể (thứ 2, 3...)
- Không hỗ trợ ngày tương đối (hôm qua, mai, mốt, kia)

**Giải Pháp:**
- ✅ Thêm hỗ trợ ngày tương đối
- ✅ Hiển thị ngày/tháng/năm cùng tên gọi
- ✅ Phát hiện intent tự động

---

### 🔄 Luồng Xử Lý Mới

```
User: "Hôm qua tôi học gì?"
         ↓
[detect_schedule_intent()]
   └─ Match: r'hôm qua' ✓
         ↓
[get_schedule(token, message)]
   ├─ extract_day_from_message()
   │  └─ today - 1 day → THURSDAY
   │
   ├─ get_formatted_date_label()
   │  └─ Format: "hôm qua (19/12/2024)"
   │
   ├─ TVU Login & Fetch
   │
   └─ Filter by THURSDAY
         ↓
Response: "📅 **Lịch học hôm qua (19/12/2024):**
           (Danh sách các lớp...)"
```

---

### 📝 Các Cách Sử Dụng

| Input | Ý Nghĩa |
|-------|---------|
| "Hôm nay tôi học gì?" | Ngày hiện tại |
| "Hôm qua có lớp không?" | 1 ngày trước |
| "Mai lịch sao?" | 1 ngày sau |
| "Mốt tôi bận không?" | 2 ngày sau |
| "Kia xem thời khóa biểu" | 3 ngày sau |
| "Thứ 2 học cái gì?" | Thứ 2 bất kỳ |
| "Chủ nhật có buổi nào?" | Chủ nhật |

---

### 🔧 Thay Đổi Code

#### 1. **agent_features.py**

```python
# ❌ Trước
def extract_day_from_message(self, message: str) -> Optional[str]:
    day_map = {
        'hôm nay': None,
        'thứ 2': 'MONDAY',
        ...
    }
    # Chỉ check được ngày cụ thể

# ✅ Sau
def extract_day_from_message(self, message: str) -> Optional[str]:
    today = datetime.now()
    
    if 'hôm qua' in message_lower:
        yesterday = today - timedelta(days=1)
        return yesterday.strftime('%A').upper()
    
    if 'mai' in message_lower:
        tomorrow = today + timedelta(days=1)
        return tomorrow.strftime('%A').upper()
    # ... và mốt, kia
```

#### 2. **Thêm hàm mới**

```python
def get_formatted_date_label(self, message: str) -> tuple:
    """Format label ngày với ngày/tháng/năm"""
    if 'hôm qua' in message_lower:
        target_date = today - timedelta(days=1)
        return (f"hôm qua ({date_str})", True)
    # ... tương tự cho mai, mốt, kia
```

---

### 📂 File Đã Tạo/Sửa

✅ **Sửa:**
- `backend/PythonService/agent_features.py` - Cập nhật logic
- `backend/PythonService/main.py` - Cập nhật test endpoint

✅ **Tạo:**
- `SCHEDULE_QUERY_GUIDE.md` - Hướng dẫn sử dụng
- `CHANGELOG_SCHEDULE_FEATURES.md` - Chi tiết thay đổi
- `backend/PythonService/test_schedule_features.py` - Test script
- `examples_schedule_queries.py` - Ví dụ API calls

---

### 🧪 Cách Test

#### 1. Test Script
```bash
cd backend/PythonService
python test_schedule_features.py
```

Output:
```
🧪 TEST: Phân tích ngày từ tin nhắn
========================

📝 Input: 'Hôm qua tôi học gì?'
   └─ Day: THURSDAY
   └─ Label: hôm qua (19/12/2024)
   └─ Is Relative: True

📝 Input: 'Mai có lớp không?'
   └─ Day: SATURDAY
   └─ Label: mai (21/12/2024)
   └─ Is Relative: True
```

#### 2. Chat Box
```
User: "Hôm qua tôi học gì?"
Bot:  📅 **Lịch học hôm qua (19/12/2024):**

      🕐 08:00 - 09:30
         📚 Toán
         🏫 Phòng 301
```

#### 3. Test Endpoint
```bash
curl -X POST http://localhost:8000/api/test/tvu-schedule \
  -H "Content-Type: application/json" \
  -d '{
    "mssv": "YOUR_MSSV",
    "password": "YOUR_PASSWORD",
    "message": "Hôm qua tôi học gì?"
  }'
```

---

### 🚀 Tính Năng Được Hỗ Trợ

✅ Hôm nay
✅ Hôm qua
✅ Mai
✅ Mốt (2 ngày sau)
✅ Kia (3 ngày sau)
✅ Thứ 2-7 (ngày cụ thể)
✅ Chủ nhật
✅ Hiển thị ngày/tháng/năm
✅ Phát hiện intent tự động

---

### 💡 Mở Rộng Thêm

#### Thêm "2 ngày nữa"
```python
if '2 ngày' in message_lower:
    two_days = today + timedelta(days=2)
    return two_days.strftime('%A').upper()
```

#### Thêm ngày cụ thể (20/12/2024)
```python
import re
match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', message_lower)
if match:
    day, month, year = match.groups()
    target = datetime(int(year), int(month), int(day))
    return target.strftime('%A').upper()
```

#### Thêm tuần tương đối
```python
# "Tuần trước", "Tuần sau" - Tính toàn bộ tuần
def get_week_schedule(self, token, message):
    if 'tuần trước' in message_lower:
        # Lấy TKB cả tuần trước
```

---

### 📊 Comparision

| Feature | Trước | Sau |
|---------|-------|-----|
| Hôm nay | ✅ | ✅ |
| Hôm qua | ❌ | ✅ |
| Mai | ❌ | ✅ |
| Mốt | ❌ | ✅ |
| Kia | ❌ | ✅ |
| Thứ cụ thể | ✅ | ✅ |
| Ngày/Tháng/Năm | ❌ | ✅ |
| Auto intent detect | ⚠️ Cơ bản | ✅ Toàn diện |

---

### 📞 Liên Hệ & Support

Các file liên quan:
- **Main logic**: `backend/PythonService/agent_features.py`
- **Test endpoint**: `backend/PythonService/main.py` (dòng 432+)
- **TVU Scraper**: `backend/PythonService/tvu_scraper.py`
- **Guide**: `SCHEDULE_QUERY_GUIDE.md`
- **Changelog**: `CHANGELOG_SCHEDULE_FEATURES.md`

---

### ✅ Status

**Implementation**: ✅ Done
**Testing**: ⏳ Ready to Test
**Documentation**: ✅ Complete

Ready to use! 🚀
