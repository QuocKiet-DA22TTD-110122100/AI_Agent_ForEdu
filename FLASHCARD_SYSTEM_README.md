# 🎴 FLASHCARD SYSTEM - COMPLETE README

## 📋 Tổng Quan

Hệ thống Flashcard học tập thông minh với **Spaced Repetition Algorithm (SM-2)** giống Anki, được tích hợp vào ứng dụng Agent For Edu.

### ✨ Tính Năng Chính

1. **📚 Quản lý Bộ Thẻ (Decks)**
   - Tạo/sửa/xóa bộ thẻ
   - Customize màu sắc và biểu tượng
   - Public/Private decks

2. **🎴 Flashcards**
   - Mặt trước (Question) / Mặt sau (Answer)
   - Hint và Explanation
   - Hỗ trợ hình ảnh và audio
   - Tags để phân loại

3. **🧠 Spaced Repetition (SM-2 Algorithm)**
   - Tự động tính toán lịch ôn tập
   - 5 mức độ: NEW → LEARNING → YOUNG → MATURE → RELEARNING
   - Quality ratings: 0-5 (Again/Hard/Good/Easy)
   - Ease Factor calculation (minimum 1.3)

4. **📊 Thống Kê Chi Tiết**
   - Progress tracking
   - Accuracy metrics
   - Study time tracking
   - Daily/Weekly/Monthly stats

5. **🤖 AI Auto-Generation** (Coming soon)
   - Tự động tạo flashcards từ tài liệu (PDF, DOC)
   - Gemini AI extract nội dung quan trọng

---

## 📁 Files Đã Tạo

### ✅ Backend (Spring Boot)

#### Database:
- `add_flashcard_system.sql` - Migration script với 7 bảng

#### Entity Classes (6 files):
- `FlashcardDeck.java` - Bộ thẻ
- `Flashcard.java` - Thẻ học
- `FlashcardReview.java` - Lịch sử review
- `FlashcardStats.java` - Thống kê tổng hợp
- `FlashcardStudySession.java` - Phiên học tập
- `FlashcardGenerationRequest.java` - AI generation

#### Repository Interfaces (6 files):
- `FlashcardDeckRepository.java`
- `FlashcardRepository.java`
- `FlashcardStatsRepository.java`
- `FlashcardReviewRepository.java`
- `FlashcardStudySessionRepository.java`
- `FlashcardGenerationRequestRepository.java`

#### Service Layer (2 files):
- `SpacedRepetitionService.java` - SM-2 algorithm
- `FlashcardService.java` - Business logic (CRUD + Study + Stats)

#### Controller:
- `FlashcardController.java` - REST API với 20+ endpoints

#### DTOs (6 files):
- `CreateDeckRequest.java`
- `CreateFlashcardRequest.java`
- `ReviewFlashcardRequest.java`
- `DeckResponse.java`
- `FlashcardResponse.java`
- `DeckStatsResponse.java`

### 📖 Documentation Files:
- `FLASHCARD_IMPLEMENTATION_GUIDE.md` - Hướng dẫn triển khai
- `FLASHCARD_FRONTEND_GUIDE.md` - Frontend components & API

---

## 🚀 Cài Đặt & Chạy

### 1. Database Migration

```bash
cd backend/SpringService/agentforedu
mysql -u root -p Agent_Db < add_flashcard_system.sql
```

**Output:**
```
✅ Flashcard system tables created successfully!
Tables: flashcard_decks, flashcards, flashcard_reviews, 
        flashcard_stats, flashcard_study_sessions, 
        flashcard_deck_shares, flashcard_generation_requests
```

### 2. Spring Boot Backend

```bash
cd backend/SpringService/agentforedu
./mvnw clean package
./mvnw spring-boot:run
```

**Verify:**
- API runs on: http://localhost:8080
- Swagger UI: http://localhost:8080/swagger-ui.html

### 3. Frontend (React)

```bash
cd fronend_web

# Install dependencies (if not already)
npm install framer-motion lucide-react

# Run dev server
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Flashcards page: http://localhost:5173/flashcards

---

## 📡 API Endpoints

### Deck Management
```
POST   /api/flashcards/decks           # Tạo bộ thẻ
GET    /api/flashcards/decks           # Danh sách bộ thẻ
GET    /api/flashcards/decks/{id}      # Chi tiết bộ thẻ
PUT    /api/flashcards/decks/{id}      # Cập nhật bộ thẻ
DELETE /api/flashcards/decks/{id}      # Xóa bộ thẻ
```

### Flashcard CRUD
```
POST   /api/flashcards/decks/{deckId}/cards    # Tạo thẻ mới
GET    /api/flashcards/decks/{deckId}/cards    # Danh sách thẻ
GET    /api/flashcards/cards/{id}              # Chi tiết thẻ
PUT    /api/flashcards/cards/{id}              # Cập nhật thẻ
DELETE /api/flashcards/cards/{id}              # Xóa thẻ
```

### Study Mode
```
GET    /api/flashcards/study/due               # Thẻ cần ôn hôm nay
GET    /api/flashcards/study/due?deckId=1      # Thẻ cần ôn (deck cụ thể)
GET    /api/flashcards/study/new?deckId=1      # Thẻ mới chưa học
POST   /api/flashcards/study/review            # Submit review
```

### Statistics
```
GET    /api/flashcards/stats/deck/{deckId}     # Thống kê bộ thẻ
GET    /api/flashcards/stats/overview          # Tổng quan toàn bộ
```

---

## 🎯 Cách Sử Dụng

### 1. Tạo Bộ Thẻ Mới

**Request:**
```bash
POST /api/flashcards/decks
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Toán Cao Cấp",
  "description": "Các khái niệm quan trọng",
  "color": "#10B981",
  "icon": "📐",
  "isPublic": false
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Toán Cao Cấp",
  "totalCards": 0,
  "newCards": 0,
  "dueCards": 0,
  "createdAt": "2025-12-22T10:30:00"
}
```

### 2. Thêm Thẻ Vào Bộ

**Request:**
```bash
POST /api/flashcards/decks/1/cards
Authorization: Bearer {token}

{
  "front": "Đạo hàm của sin(x) là gì?",
  "back": "cos(x)",
  "hint": "Nhớ công thức lượng giác cơ bản",
  "explanation": "Đạo hàm của sin(x) là cos(x). Đây là công thức cơ bản trong giải tích.",
  "tags": "[\"toán\", \"đạo hàm\"]"
}
```

### 3. Học Hàng Ngày

**Bước 1: Lấy thẻ cần ôn**
```bash
GET /api/flashcards/study/due?deckId=1&limit=20
```

**Response:**
```json
[
  {
    "id": 1,
    "front": "Đạo hàm của sin(x) là gì?",
    "back": "cos(x)",
    "totalReviews": 3,
    "accuracy": 0.67,
    "maturityLevel": "LEARNING",
    "nextReviewDate": "2025-12-22T10:00:00"
  }
]
```

**Bước 2: Review và submit**
```bash
POST /api/flashcards/study/review

{
  "flashcardId": 1,
  "quality": 3,         # 0=Again, 1-2=Hard, 3-4=Good, 5=Easy
  "timeTakenSeconds": 12
}
```

**SM-2 Algorithm tự động tính:**
- Quality 3 (Good) → Next review in 6 days
- Ease Factor updated: 2.5 → 2.36
- Maturity: LEARNING → YOUNG

### 4. Xem Thống Kê

```bash
GET /api/flashcards/stats/overview
```

**Response:**
```json
{
  "totalDecks": 3,
  "totalCards": 150,
  "newCards": 30,
  "dueCards": 15,
  "studyStreak": 7,
  "decks": [...]
}
```

---

## 🧠 SM-2 Algorithm Explained

### Thuật toán hoạt động:

1. **Initial State:**
   - Ease Factor (EF) = 2.5
   - Interval = 0 days
   - Repetitions = 0

2. **User reviews card with quality (0-5):**

   **Quality < 3 (Wrong answer):**
   - Interval = 1 day
   - Repetitions = 0 (reset)
   - EF unchanged

   **Quality ≥ 3 (Correct answer):**
   - Repetitions += 1
   - Update EF: `EF' = EF + (0.1 - (5-q)*(0.08 + (5-q)*0.02))`
   - EF minimum = 1.3
   
   **Calculate interval:**
   - If repetitions = 1: interval = 1 day
   - If repetitions = 2: interval = 6 days
   - If repetitions ≥ 3: interval = previous_interval * EF

3. **Quality modifiers:**
   - Quality 0 (Again): 1 day
   - Quality 1-2 (Hard): 50%-70% of calculated
   - Quality 3-4 (Good): 100%-120%
   - Quality 5 (Easy): 150%

### Example progression:

```
Review 1: Quality 3 (Good)  → Next: 1 day    (EF: 2.5)
Review 2: Quality 3 (Good)  → Next: 6 days   (EF: 2.36)
Review 3: Quality 4 (Good)  → Next: 14 days  (EF: 2.46)
Review 4: Quality 5 (Easy)  → Next: 51 days  (EF: 2.6)
Review 5: Quality 1 (Hard)  → Next: 1 day    (EF: 2.6, Repetitions reset!)
```

---

## 📊 Maturity Levels

- **NEW** - Chưa học lần nào
- **LEARNING** - Đang học (interval < 7 days)
- **YOUNG** - Thẻ non (7 ≤ interval < 21 days)
- **MATURE** - Thẻ chín (interval ≥ 21 days)
- **RELEARNING** - Học lại (sau khi quên)

---

## 🎨 Frontend Components

### Main Pages:
1. **FlashcardsPage** - List tất cả bộ thẻ
2. **FlashcardDeckPage** - Quản lý thẻ trong bộ
3. **FlashcardStudyPage** - Chế độ học (flip animation)

### Key Features:
- ✨ 3D flip animation (framer-motion)
- ⌨️ Keyboard shortcuts (Space, 1-4)
- 📱 Mobile swipe gestures
- 📊 Real-time progress bar
- 🎯 Review buttons (Again/Hard/Good/Easy)

**See:** `FLASHCARD_FRONTEND_GUIDE.md` for complete code

---

## 🔮 Future Enhancements

### Phase 2 (Coming):
- [ ] AI auto-generation from materials
- [ ] Deck sharing & community decks
- [ ] Image occlusion (hide parts of images)
- [ ] Audio pronunciation (TTS)
- [ ] Advanced statistics dashboard
- [ ] Study reminders & notifications
- [ ] Import/Export (Anki format compatible)
- [ ] Collaborative decks
- [ ] Gamification (achievements, streaks)

---

## 🐛 Troubleshooting

### Issue: Database tables not created
```bash
# Check if Agent_Db exists
mysql -u root -p -e "SHOW DATABASES;"

# Run migration again
mysql -u root -p Agent_Db < add_flashcard_system.sql
```

### Issue: Spring Boot can't find entities
```bash
# Check package structure
# Entities should be in: aiagent.dacn.agentforedu.entity

# Clean and rebuild
./mvnw clean package
```

### Issue: Frontend API calls fail (CORS)
```java
// Add @CrossOrigin to controller
@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/api/flashcards")
public class FlashcardController { ... }
```

---

## 📚 References

- [SuperMemo SM-2 Algorithm](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2)
- [Anki Manual](https://docs.ankiweb.net/)
- [Spaced Repetition Research](https://en.wikipedia.org/wiki/Spaced_repetition)

---

## 📞 Support

Nếu có vấn đề:
1. Kiểm tra logs: `backend/SpringService/agentforedu/logs/`
2. Test API với Swagger: http://localhost:8080/swagger-ui.html
3. Check database: `SELECT * FROM flashcard_decks;`

---

## ✅ Implementation Status

| Component | Status | Files |
|-----------|--------|-------|
| Database Schema | ✅ Complete | `add_flashcard_system.sql` |
| Entity Classes | ✅ Complete | 6 files |
| Repositories | ✅ Complete | 6 files |
| SM-2 Algorithm | ✅ Complete | `SpacedRepetitionService.java` |
| Service Layer | ✅ Complete | `FlashcardService.java` |
| REST API | ✅ Complete | `FlashcardController.java` |
| DTOs | ✅ Complete | 6 files |
| Frontend Guide | ✅ Complete | `FLASHCARD_FRONTEND_GUIDE.md` |
| Sample Components | ✅ Complete | React code samples |
| AI Generation | 🔨 Pending | Need Python integration |

---

## 🎉 Conclusion

Hệ thống Flashcard đã được implement hoàn chỉnh với:
- ✅ Backend API đầy đủ (20+ endpoints)
- ✅ SM-2 Spaced Repetition Algorithm
- ✅ Database schema với 7 bảng
- ✅ Frontend components guide + sample code

**Bắt đầu ngay:**
1. Run database migration
2. Start Spring Boot
3. Create your first deck
4. Add cards & start studying!

**Happy Learning! 📚🎓**
