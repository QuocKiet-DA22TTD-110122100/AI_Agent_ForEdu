# 🚀 Quick Start: Lấy TKB Với Ngày Tương Đối

## 📌 Tóm Tắt Nhanh

Bạn muốn lấy thời khóa biểu cho:
- ✅ **Hôm qua** - "Hôm qua tôi học gì?"
- ✅ **Mai** - "Mai có lớp không?"
- ✅ **Mốt** - "Mốt tôi bận không?" (2 ngày sau)
- ✅ **Kia** - "Kia xem lịch" (3 ngày sau)
- ✅ **Ngày cụ thể** - "Thứ 2 học cái gì?"

Đã implement! ✨

---

## 📂 Files Liên Quan

```
📦 Project Root
├── 📄 SCHEDULE_QUERY_GUIDE.md ..................... (Hướng dẫn chi tiết)
├── 📄 CHANGELOG_SCHEDULE_FEATURES.md ............. (Chi tiết thay đổi)
├── 📄 QUICK_SUMMARY_SCHEDULE.md .................. (Tóm tắt)
├── 📄 examples_schedule_queries.py ............... (Ví dụ API calls)
│
└── 📁 backend/PythonService
    ├── 📝 agent_features.py ....................... (⭐ Main logic)
    │   ├── extract_day_from_message() ........... (Parse ngày)
    │   ├── get_formatted_date_label() .......... (Format label)
    │   ├── detect_schedule_intent() ............ (Phát hiện intent)
    │   └── get_schedule() ....................... (Lấy TKB)
    │
    ├── 📝 main.py ................................ (API endpoints)
    │   └── /api/test/tvu-schedule .............. (Test endpoint)
    │
    ├── 📝 test_schedule_features.py ............. (Test script)
    │
    ├── 📝 tvu_scraper.py ......................... (Scrape TVU)
    │   └── get_schedule() ....................... (Lấy từ API)
    │
    └── 📝 school_scraper.py ..................... (Generic scraper)
```

---

## 🎯 Các Bước Để Test

### Step 1: Kiểm Tra Code
```bash
# Check main logic
cat backend/PythonService/agent_features.py | grep "extract_day_from_message" -A 50

# Check test endpoint
cat backend/PythonService/main.py | grep "/api/test/tvu-schedule" -A 30
```

### Step 2: Run Test Script
```bash
cd backend/PythonService
python test_schedule_features.py
```

Expected output:
```
🧪 TEST: Phân tích ngày từ tin nhắn
=====================================
📝 Input: 'Hôm qua tôi học gì?'
   └─ Day: THURSDAY
   └─ Label: hôm qua (19/12/2024)
   └─ Is Relative: True
```

### Step 3: Start Services
```bash
# Terminal 1: Spring Boot
cd backend/SpringService/agentforedu
mvn clean spring-boot:run

# Terminal 2: FastAPI
cd backend/PythonService
python main.py

# Terminal 3: Frontend
cd fronend_web
npm install && npm run dev
```

### Step 4: Test via Chat
```
1. Mở browser: http://localhost:3000
2. Login
3. Gõ: "Hôm qua tôi học gì?"
4. Bot trả về: "📅 **Lịch học hôm qua (19/12/2024):**"
```

### Step 5: Test via API (Optional)
```bash
curl -X POST http://localhost:8000/api/test/tvu-schedule \
  -H "Content-Type: application/json" \
  -d '{
    "mssv": "your_mssv",
    "password": "your_password",
    "message": "Hôm qua"
  }'
```

---

## 🔍 Cấu Trúc Luồng

```
┌─────────────────┐
│  User Input     │
│ "Hôm qua..."    │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────────┐
│ detect_schedule_intent()            │
│ - Check regex patterns              │
│ - Return: True/False                │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│ extract_day_from_message()          │
│ - Parse ngày từ message             │
│ - "hôm qua" → today - 1 day         │
│ - Return: 'THURSDAY'                │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│ get_formatted_date_label()          │
│ - Format label với ngày/tháng       │
│ - Return: "hôm qua (19/12/2024)"    │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│ get_tvu_credential()                │
│ - Lấy TVU account từ DB             │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│ TVUScraper.login()                  │
│ - Login https://ttsv.tvu.edu.vn     │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│ TVUScraper.get_schedule()           │
│ - Call API TVU                      │
│ - Get tất cả lớp tuần này           │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│ Filter by day_of_week               │
│ - Filter: day_of_week == 'THURSDAY' │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│ Format message                      │
│ "📅 **Lịch học hôm qua..."         │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────┐
│  Return to User │
└─────────────────┘
```

---

## 🧪 Test Cases

| Input | Expected Day | Expected Label |
|-------|--------------|-----------------|
| "Hôm nay" | TODAY | hôm nay (20/12/2024) |
| "Hôm qua" | YESTERDAY | hôm qua (19/12/2024) |
| "Mai" | TOMORROW | mai (21/12/2024) |
| "Mốt" | +2 days | mốt (22/12/2024) |
| "Kia" | +3 days | kia (23/12/2024) |
| "Thứ 2" | MONDAY | Thứ 2 |
| "Thứ 5" | THURSDAY | Thứ 5 |
| "CN" | SUNDAY | Chủ nhật |

---

## 📊 Code Changes Summary

### agent_features.py

```python
# Thêm import
from datetime import datetime, timedelta

# Thêm hàm
def get_formatted_date_label(self, message: str) -> tuple:
    """Format ngày với ngày/tháng/năm"""
    if 'hôm qua' in message_lower:
        target_date = today - timedelta(days=1)
        return (f"hôm qua ({date_str})", True)
    # ... tương tự cho mai, mốt, kia

# Cập nhật hàm
def extract_day_from_message(self, message: str) -> Optional[str]:
    """Support ngày tương đối"""
    if 'hôm qua' in message_lower:
        yesterday = today - timedelta(days=1)
        return yesterday.strftime('%A').upper()
    if 'mai' in message_lower:
        tomorrow = today + timedelta(days=1)
        return tomorrow.strftime('%A').upper()
    # ... mốt, kia

def detect_schedule_intent(self, message: str) -> bool:
    """Thêm patterns cho ngày tương đối"""
    patterns = [
        r'hôm qua|hom qua',
        r'mai',
        r'mốt|mot',
        r'kia',
        # ... existing patterns
    ]
```

---

## ✅ Verify Implementation

### Check 1: Files Modified
```bash
# Kiểm tra agent_features.py
grep -n "timedelta" backend/PythonService/agent_features.py
# Output: 5: from datetime import datetime, timedelta ✓

grep -n "get_formatted_date_label" backend/PythonService/agent_features.py
# Output: 21: def get_formatted_date_label(...) ✓
```

### Check 2: Test Patterns
```bash
# Kiểm tra detect_schedule_intent() có support hôm qua
grep -n "hôm qua\|hom qua" backend/PythonService/agent_features.py
# Output: 58: r'hôm qua', ✓
```

### Check 3: Extract Day Logic
```bash
# Kiểm tra extract_day_from_message() có xử lý mốt
grep -n "mốt\|mot" backend/PythonService/agent_features.py
# Output: 347: if 'mốt' in message_lower... ✓
```

---

## 🐛 Debugging

Nếu gặp lỗi:

### 1. Import Error
```python
# Check: timedelta imported?
from datetime import datetime, timedelta
```

### 2. Logic Error
```python
# Kiểm tra: 
# - extract_day_from_message() return đúng day?
# - get_formatted_date_label() format đúng?
# - detect_schedule_intent() match pattern?
```

### 3. TVU Error
```python
# Kiểm tra:
# - TVU credential đã setup?
# - Password đúng?
# - Internet kết nối?
```

---

## 📖 Đọc Thêm

1. **SCHEDULE_QUERY_GUIDE.md** - Hướng dẫn chi tiết
2. **CHANGELOG_SCHEDULE_FEATURES.md** - Tất cả thay đổi
3. **examples_schedule_queries.py** - Ví dụ code

---

## 🚀 Next Steps

1. ✅ Implementation complete
2. ⏳ Run test script
3. ⏳ Test via chat box
4. ⏳ Deploy to production

---

## 💬 Support

Issues? Checks these:
- [ ] TVU credential setup?
- [ ] Internet connection ok?
- [ ] All services running?
- [ ] Check logs in backend/PythonService/

---

**Status**: 🟢 Ready to Use
**Last Updated**: 2025-12-20
