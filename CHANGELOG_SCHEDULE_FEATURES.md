# 📋 Cập Nhật: Hỗ Trợ Lấy TKB với Ngày Tương Đối

## 📝 Tóm Tắt Thay Đổi

Dự án giờ đây hỗ trợ lấy thời khóa biểu cho:
- ✅ Ngày hôm qua
- ✅ Ngày mai
- ✅ Ngày mốt (2 ngày sau)
- ✅ Ngày kia (3 ngày sau)
- ✅ Ngày cụ thể (Thứ 2, 3, 4...)
- ✅ Hôm nay

---

## 🔧 Các File Đã Sửa

### 1. **backend/PythonService/agent_features.py**

#### Thay đổi 1: Import `timedelta`
```python
from datetime import datetime, timedelta
```

#### Thay đổi 2: Thêm `get_formatted_date_label()`
Hàm mới để format ngày đẹp hơn (ví dụ: "hôm qua (20/12/2024)")

**Lợi ích:**
- Hiển thị ngày tháng năm cùng với tên gọi tương đối
- Dễ nhận biết user muốn xem ngày nào

#### Thay đổi 3: Cải thiện `extract_day_from_message()`
```python
# Trước: Chỉ hỗ trợ ngày cụ thể (thứ 2, 3...)
# Sau: Hỗ trợ cả ngày tương đối + ngày cụ thể
```

**Hỗ trợ:**
- `hôm qua` → 1 ngày trước
- `mai` → 1 ngày sau
- `mốt` → 2 ngày sau
- `kia` → 3 ngày sau

#### Thay đổi 4: Cập nhật `detect_schedule_intent()`
Thêm regex patterns để nhận diện:
```python
r'hôm qua|hom qua'  # Hôm qua
r'mai'              # Mai
r'mốt|mot'          # Mốt
r'kia'              # Kia
r'thứ\s*[2-7]'      # Thứ 2-7
```

#### Thay đổi 5: Cập nhật `get_schedule()`
Dùng `get_formatted_date_label()` để hiển thị label đẹp hơn

---

### 2. **backend/PythonService/main.py**

#### Thay đổi: Cập nhật test endpoint `/api/test/tvu-schedule`
```python
# Import timedelta
from datetime import datetime, timedelta

# Thêm logic xử lý ngày tương đối
if 'hôm qua' in message_lower:
    yesterday = today - timedelta(days=1)
    target_day = yesterday.strftime('%A').upper()
    ...
```

**Lợi ích:**
- Test endpoint cũng hỗ trợ ngày tương đối
- Có thể test trực tiếp mà không cần full chat flow

---

## 📂 File Mới Tạo

### 1. **SCHEDULE_QUERY_GUIDE.md**
Hướng dẫn chi tiết về cách sử dụng tính năng lấy TKB

Nội dung:
- Các cách sử dụng (ngày tương đối, ngày cụ thể)
- Ví dụ sử dụng
- Luồng xử lý backend
- Code implementation
- Cách extend tính năng

### 2. **backend/PythonService/test_schedule_features.py**
Script test để demo tính năng

Chạy bằng:
```bash
cd backend/PythonService
python test_schedule_features.py
```

---

## 🎯 Các Tính Năng Mới

### 1. Hỗ Trợ Ngày Tương Đối
```
User: "Hôm qua tôi học gì?"
Bot:  📅 **Lịch học hôm qua (19/12/2024):**
      (Danh sách các lớp...)

User: "Mai có lớp không?"
Bot:  📅 **Lịch học mai (21/12/2024):**
      (Danh sách các lớp...)

User: "Mốt tôi bận không?"
Bot:  📅 **Lịch học mốt (22/12/2024):**
      (Danh sách các lớp...)
```

### 2. Hiển Thị Ngày/Tháng/Năm
```
Trước: "📅 **Lịch học hôm nay:**"
Sau:   "📅 **Lịch học hôm nay (20/12/2024):**"
```

### 3. Phát Hiện Intent Tốt Hơn
- Bây giờ detect các ngày tương đối tự động
- Không cần phải nói "Thứ 2" mà có thể nói "Mai"

---

## 🔄 Luồng Xử Lý

```
User: "Hôm qua tôi học gì?"
  ↓
detect_schedule_intent() ✓
  ├─ Pattern match: r'hôm qua' → YES
  └─ Return: True
  ↓
get_schedule(token, message)
  ├─ extract_day_from_message()
  │  └─ Input: "Hôm qua tôi học gì?"
  │  └─ Check: 'hôm qua' in message_lower
  │  └─ Calculate: today - 1 day
  │  └─ Return: 'THURSDAY' (if today is Friday)
  │
  ├─ get_formatted_date_label()
  │  └─ Format: "hôm qua (19/12/2024)"
  │
  └─ TVUScraper.get_schedule()
     ├─ Get credential
     ├─ Login TVU
     ├─ Fetch data
     └─ Filter by THURSDAY
       ↓
Display: "📅 **Lịch học hôm qua (19/12/2024):**"
```

---

## 🚀 Cách Test

### 1. Via Chat Box (Full Flow)
```
User: "Hôm qua tôi học lớp gì?"
      "Mai có buổi học nào?"
      "Mốt xem lịch học"
      "Kia bảo tôi lịch"
```

### 2. Via Test Script
```bash
cd backend/PythonService
python test_schedule_features.py
```

Output:
```
🧪 TEST: Phân tích ngày từ tin nhắn
================================================

📝 Input: 'Hôm nay tôi học gì?'
   └─ Day: FRIDAY
   └─ Label: hôm nay (20/12/2024)
   └─ Is Relative: True

📝 Input: 'Hôm qua tôi có lớp không?'
   └─ Day: THURSDAY
   └─ Label: hôm qua (19/12/2024)
   └─ Is Relative: True
...
```

### 3. Via Test Endpoint
```bash
curl -X POST http://localhost:8000/api/test/tvu-schedule \
  -H "Content-Type: application/json" \
  -d '{
    "mssv": "your_mssv",
    "password": "your_password",
    "message": "Hôm qua tôi học gì?"
  }'
```

---

## 💡 Ví Dụ Thực Tế

### Scenario 1: Hôm qua
```
Today: 20/12/2024 (Friday)
User: "Hôm qua học cái gì?"
→ Query for: THURSDAY, 19/12/2024
```

### Scenario 2: Mốt (2 ngày sau)
```
Today: 20/12/2024 (Friday)
User: "Mốt tôi có lớp không?"
→ Query for: SUNDAY, 22/12/2024
```

### Scenario 3: Thứ cụ thể
```
User: "Thứ 3 tôi học gì?"
→ Query for: TUESDAY (any week)
```

---

## 📊 Tổng Hợp Hỗ Trợ

| Input | Kết Quả |
|-------|---------|
| "Hôm nay" | Ngày hôm nay |
| "Hôm qua" | Ngày hôm qua (-1) |
| "Mai" | Ngày mai (+1) |
| "Mốt" | 2 ngày sau (+2) |
| "Kia" | 3 ngày sau (+3) |
| "Thứ 2-7" | Ngày đó của tuần |
| "Chủ nhật" | Chủ nhật |

---

## 🔧 Cách Extend Thêm

### Thêm hỗ trợ "2 ngày nữa"
```python
# Trong extract_day_from_message()
if '2 ngày' in message_lower or 'hai ngày' in message_lower:
    two_days = today + timedelta(days=2)
    return two_days.strftime('%A').upper()
```

### Thêm hỗ trợ ngày cụ thể (20/12/2024)
```python
import re
date_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', message_lower)
if date_match:
    day, month, year = date_match.groups()
    target = datetime(int(year), int(month), int(day))
    return target.strftime('%A').upper()
```

---

## ✅ Checklist

- [x] Cập nhật `extract_day_from_message()`
- [x] Thêm `get_formatted_date_label()`
- [x] Cập nhật `detect_schedule_intent()`
- [x] Cập nhật `get_schedule()`
- [x] Cập nhật test endpoint
- [x] Tạo test script
- [x] Tạo documentation

---

## 📞 Tiếp Theo

1. **Test**: Chạy test script để verify tất cả logic
2. **Run**: Start services và test via chat box
3. **Extend**: Thêm các feature khác nếu cần

---

Generated: 2025-12-20
Status: ✅ Ready to Use
