# 🎴 Hướng Dẫn Test Hệ Thống Flashcard

## ✅ Đã Hoàn Thành

### Backend (Spring Boot)
- ✅ 7 Entity classes (FlashcardDeck, Flashcard, FlashcardReview, FlashcardStats, FlashcardStudySession, FlashcardGenerationRequest)
- ✅ 6 Repository interfaces  
- ✅ SpacedRepetitionService (SM-2 Algorithm)
- ✅ FlashcardService (Business Logic)
- ✅ FlashcardController (REST API với @AuthenticationPrincipal)
- ✅ 6 DTO classes
- ✅ Maven compile thành công

### Frontend (React + TypeScript)
- ✅ TypeScript types (flashcard.ts)
- ✅ API service layer (flashcardService.ts)
- ✅ DeckCard component
- ✅ FlashcardsPage (danh sách deck + modal tạo mới)
- ✅ FlashcardStudyPage (học thẻ với flip animation)
- ✅ Routes trong App.tsx
- ✅ Menu item trong Layout.tsx
- ✅ TypeScript compile không lỗi

### Database
- ✅ add_flashcard_system.sql (7 bảng với SM-2 fields)

---

## 🚀 Các Bước Để Chạy

### 1️⃣ Chạy Database Migration

```powershell
# Option 1: MySQL Command Line
mysql -u root -p
USE Agent_Db;
source C:/Users/canhn/Downloads/DACN/DACN/add_flashcard_system.sql;
exit;

# Option 2: MySQL Workbench
# - Mở file add_flashcard_system.sql
# - Chọn database Agent_Db
# - Execute (Ctrl+Shift+Enter)
```

### 2️⃣ Start Backend (Spring Boot)

```powershell
cd "c:\Users\canhn\Downloads\DACN\DACN\backend\SpringService\agentforedu"
./mvnw.cmd spring-boot:run
```

Backend sẽ chạy trên: http://localhost:8081

### 3️⃣ Start Frontend (React Vite)

```powershell
cd "c:\Users\canhn\Downloads\DACN\DACN\fronend_web"
npm run dev
```

Frontend đang chạy trên: http://localhost:5174

---

## 🧪 Test Flow

### A. Tạo Deck Mới
1. Đăng nhập vào hệ thống
2. Click menu "Flashcards" (icon thẻ bài)
3. Click nút "Create New Deck"
4. Nhập:
   - Name: "Tiếng Anh Cơ Bản"
   - Description: "Từ vựng tiếng Anh cơ bản"
   - Color: Chọn màu tùy thích
5. Click "Create Deck"

### B. Thêm Flashcards
1. Click vào deck vừa tạo
2. Click "Add Card"
3. Nhập:
   - Front: "Hello"
   - Back: "Xin chào"
4. Click "Add Card"
5. Thêm thêm vài thẻ nữa:
   - "Goodbye" → "Tạm biệt"
   - "Thank you" → "Cảm ơn"
   - "Good morning" → "Chào buổi sáng"

### C. Học Thẻ (Study Mode)
1. Click "Study Now" trên deck
2. Xem mặt trước của thẻ (Front)
3. Click thẻ hoặc nhấn Space để lật
4. Đánh giá độ khó (1-5):
   - **1 - Again**: Quên hoàn toàn
   - **2 - Hard**: Khó nhớ  
   - **3 - Good**: Nhớ được
   - **4 - Easy**: Dễ
   - **5 - Perfect**: Rất dễ

### D. Kiểm Tra Spaced Repetition
1. Sau khi học xong tất cả thẻ
2. Quay lại trang Flashcards
3. Xem stats:
   - Total Cards
   - New Cards (còn chưa học)
   - Due Cards (đến hạn ôn tập)
   - Mastered (đã thành thạo)

---

## 🎯 API Endpoints

### Deck Management
```
POST   /api/flashcards/decks          - Tạo deck mới
GET    /api/flashcards/decks          - Lấy danh sách decks
GET    /api/flashcards/decks/{id}     - Lấy chi tiết deck
PUT    /api/flashcards/decks/{id}     - Cập nhật deck
DELETE /api/flashcards/decks/{id}     - Xóa deck
```

### Flashcard CRUD
```
POST   /api/flashcards/decks/{deckId}/cards  - Tạo thẻ mới
GET    /api/flashcards/decks/{deckId}/cards  - Lấy thẻ trong deck
GET    /api/flashcards/cards/{cardId}        - Lấy chi tiết thẻ
PUT    /api/flashcards/cards/{cardId}        - Cập nhật thẻ
DELETE /api/flashcards/cards/{cardId}        - Xóa thẻ
```

### Study Mode
```
GET    /api/flashcards/study/due       - Lấy thẻ đến hạn ôn tập
GET    /api/flashcards/study/new       - Lấy thẻ mới
POST   /api/flashcards/study/review    - Submit đánh giá thẻ
```

### Statistics
```
GET    /api/flashcards/stats/deck/{deckId}  - Thống kê deck
GET    /api/flashcards/stats/overview       - Tổng quan toàn bộ
```

---

## 🔍 Test với Postman/Thunder Client

### 1. Login để lấy token
```http
POST http://localhost:8081/api/auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

Lấy `token` từ response.

### 2. Tạo deck
```http
POST http://localhost:8081/api/flashcards/decks
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "name": "Japanese N5",
  "description": "Basic Japanese vocabulary",
  "color": "#FF6B6B"
}
```

### 3. Tạo flashcard
```http
POST http://localhost:8081/api/flashcards/decks/{deckId}/cards
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "front": "こんにちは",
  "back": "Hello / Xin chào"
}
```

### 4. Lấy thẻ mới để học
```http
GET http://localhost:8081/api/flashcards/study/new?limit=10
Authorization: Bearer YOUR_TOKEN_HERE
```

### 5. Submit review
```http
POST http://localhost:8081/api/flashcards/study/review
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "flashcardId": 1,
  "quality": 4
}
```

---

## 🐛 Troubleshooting

### Lỗi: "Cannot load frontend"
✅ **Đã fix**: Sửa type imports từ `import { Type }` thành `import type { Type }`

### Lỗi: "JwtTokenProvider not found"
✅ **Đã fix**: Thay bằng `@AuthenticationPrincipal User user` pattern

### Lỗi: Tables không tồn tại
➡️ Chạy migration: `source add_flashcard_system.sql`

### Lỗi: CORS
➡️ Controller đã có `@CrossOrigin(origins = "*")`

---

## 📊 SM-2 Algorithm Info

### Công Thức
```
EF' = EF + (0.1 - (5 - q) × (0.08 + (5 - q) × 0.02))
```

- `q`: Quality rating (0-5)
- `EF`: Ease Factor (min 1.3)
- `I(1) = 1 day`
- `I(2) = 6 days`
- `I(n) = I(n-1) × EF`

### Maturity Levels
- **NEW**: Chưa học lần nào
- **LEARNING**: Đang học (EF < 2.5)
- **YOUNG**: Đã thuộc nhưng còn non (repetitions < 5)
- **MATURE**: Thành thạo (repetitions ≥ 5, EF ≥ 2.5)
- **RELEARNING**: Đang học lại (sau khi quên)

---

## 🎨 Frontend Features

### FlashcardsPage
- Grid view của tất cả decks
- Create deck modal với color picker
- Stats overview (total/new/due cards)
- Search và filter decks

### FlashcardStudyPage
- 3D flip animation (Framer Motion)
- Keyboard shortcuts:
  - `Space` - Flip card
  - `1-5` - Rate quality
  - `Esc` - Exit study
- Progress bar
- Auto-load next card
- Confetti effect khi hoàn thành

---

## 🔮 Future Enhancements

### Phase 2 (AI Integration)
- [ ] Auto-generate flashcards from PDF
- [ ] Auto-generate flashcards from lecture notes
- [ ] Auto-generate flashcards from DOC/DOCX
- [ ] AI suggests optimal study schedule

### Phase 3 (Social Features)
- [ ] Share decks với classmates
- [ ] Public deck library
- [ ] Collaborative decks

### Phase 4 (Advanced Features)
- [ ] Image/Audio support on flashcards
- [ ] Cloze deletion
- [ ] Multiple choice mode
- [ ] Daily streak tracking
- [ ] Study statistics dashboard với charts

---

## ✨ Hoàn Tất!

Hệ thống Flashcard giờ đã:
- ✅ Backend API hoàn chỉnh
- ✅ Frontend UI với animations
- ✅ SM-2 Spaced Repetition Algorithm
- ✅ Statistics tracking
- ✅ Mobile responsive

**Sẵn sàng để test và sử dụng!** 🎉
