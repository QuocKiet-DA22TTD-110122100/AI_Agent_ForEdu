# 📅 Hướng Dẫn Lấy Thời Khóa Biểu (TKB) Trong Chat

## ✨ Các Cách Sử Dụng

### 1. **Ngày Tương Đối (Relative Dates)**

| Cách Nói | Ví Dụ | Ý Nghĩa |
|---------|-------|---------|
| **Hôm nay** | "Hôm nay tôi học gì?" | Ngày hiện tại |
| **Hôm qua** | "Hôm qua tôi học lớp gì?" | 1 ngày trước |
| **Mai** | "Mai tôi có lớp nào?" | Ngày tiếp theo |
| **Mốt** | "Mốt lịch học sao?" | 2 ngày sau |
| **Kia** | "Kia bạn bảo tôi lịch học" | 3 ngày sau |

---

### 2. **Ngày Cụ Thể (Specific Days)**

| Cách Nói | Tương Đương |
|---------|-----------|
| **Thứ 2** | Thứ hai, Monday, t2 |
| **Thứ 3** | Thứ ba, Tuesday, t3 |
| **Thứ 4** | Thứ tư, Wednesday, t4 |
| **Thứ 5** | Thứ năm, Thursday, t5 |
| **Thứ 6** | Thứ sáu, Friday, t6 |
| **Thứ 7** | Thứ bảy, Saturday, t7 |
| **Chủ nhật** | Sunday, CN |

#### Ví Dụ:
- "Thứ 2 tôi học gì?"
- "Tôi có lớp thứ 5 không?"
- "Xem lịch thứ 6"

---

### 3. **Các Keyword Khích Hoạt**

Những từ khóa này sẽ tích hoạt tính năng lấy TKB:
- `thời khóa biểu`
- `tkb`
- `lịch học`
- `schedule`
- `có lớp`
- `học gì`

---

## 🎯 Ví Dụ Sử Dụng

```
User: "Hôm nay tôi học gì?"
Bot:  📅 **Lịch học hôm nay (20/12/2024):**
      
      🕐 08:00 - 09:30
         📚 Toán
         🏫 Phòng 301
         👨‍🏫 Thầy Nguyễn
      
      🕐 10:00 - 11:30
         📚 Tiếng Anh
         🏫 Phòng 305
```

---

## 🔄 Luồng Xử Lý Trong Backend

```
User nhập tin nhắn
    ↓
detect_schedule_intent() → Check keywords
    ↓
extract_day_from_message() → Parse ngày
    ↓
get_tvu_credential() → Lấy tài khoản từ DB
    ↓
TVUScraper.login() → Đăng nhập TVU
    ↓
TVUScraper.get_schedule() → Lấy dữ liệu từ API TVU
    ↓
_parse_single_schedule() → Parse mỗi lớp
    ↓
Format message → Trả về cho Frontend
    ↓
Display in Chat
```

---

## 📝 Code Implementation

### `extract_day_from_message()`
Chức năng: Phân tích tin nhắn để lấy ngày nào
- Hỗ trợ ngày tương đối (hôm qua, mai, mốt, kia)
- Hỗ trợ ngày cụ thể (thứ 2, 3, 4...)
- Return: Ngày theo format `'MONDAY'`, `'TUESDAY'`, ...

### `get_formatted_date_label()`
Chức năng: Format label ngày để hiển thị đẹp
- Input: Tin nhắn từ user
- Output: Label có ngày tháng năm (ví dụ: "hôm nay (20/12/2024)")

### `detect_schedule_intent()`
Chức năng: Kiểm tra xem user có muốn xem TKB hay không
- Dùng regex patterns để match keywords
- Include cả ngày tương đối và ngày cụ thể

---

## 🚀 Features Hiện Tại

✅ Hôm nay, hôm qua, mai, mốt, kia
✅ Thứ 2 đến Chủ nhật
✅ Tiếng Anh và Tiếng Việt
✅ Hiển thị ngày tháng năm
✅ Auto-login TVU portal
✅ Format đẹp với emoji

---

## 📋 Một Số Câu Hỏi Thường Gặp

**Q: Tôi nói "xem tuần này" có được không?**
A: Có! Đó là intent cho `get_week_schedule()` - hiển thị cả tuần

**Q: Có hỗ trợ "2 ngày nữa" không?**
A: Chưa. Hiện tại chỉ hỗ trợ: hôm qua (-1), mai (+1), mốt (+2), kia (+3)

**Q: Liệt kê tất cả lớp của tuần được không?**
A: Có! Hãy nói "xem lịch tuần này" hoặc "tkb tuần này"

**Q: Có hỗ trợ ngày cụ thể (20/12/2024) không?**
A: Hiện tại chưa. Nhưng bạn có thể extend `extract_day_from_message()` để hỗ trợ

---

## 🔧 Cách Extend Tính Năng

Để thêm hỗ trợ "2 ngày nữa", thêm vào `extract_day_from_message()`:

```python
if '2 ngày' in message_lower or 'hai ngày' in message_lower:
    two_days_later = today + timedelta(days=2)
    return two_days_later.strftime('%A').upper()
```

Để hỗ trợ ngày cụ thể (20/12/2024), thêm:

```python
import re
date_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', message_lower)
if date_match:
    day, month, year = date_match.groups()
    specific_date = datetime(int(year), int(month), int(day))
    return specific_date.strftime('%A').upper()
```

---

## 📞 Liên Hệ

Nếu có lỗi hoặc muốn extend, check file:
- `backend/PythonService/agent_features.py` - Main logic
- `backend/PythonService/tvu_scraper.py` - Lấy dữ liệu từ TVU
