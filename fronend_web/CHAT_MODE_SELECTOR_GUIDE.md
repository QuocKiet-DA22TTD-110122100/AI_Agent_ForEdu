# 🎯 Chat Mode Selector - Hướng dẫn sử dụng

## Tổng quan

Chatbox giờ có **4 chế độ** để bạn chọn tùy theo nhu cầu:

```
🤖 Normal  |  🌐 Cloud  |  📚 RAG  |  🎓 Agent
```

Chuyển đổi dễ dàng bằng cách click vào các nút ở header chatbox.

---

## 📋 Các Mode chi tiết

### 🤖 **Normal Chat Mode**

**Công dụng:** Trò chuyện tự nhiên với AI, hỏi đáp chung

**Khi nào dùng:**
- Hỏi kiến thức chung
- Giải thích khái niệm
- Tư vấn học tập
- Trò chuyện thông thường

**Ví dụ:**
```
- "Giải thích về lập trình hướng đối tượng"
- "Cách học tiếng Anh hiệu quả?"
- "Lập trình Python là gì?"
```

---

### 🌐 **Google Cloud Mode**

**Công dụng:** Sử dụng Google Cloud APIs đã kết nối

**Khi nào dùng:**
- Cần dịch thuật
- Phân tích cảm xúc văn bản
- Nhận diện nội dung ảnh
- Chuyển text thành giọng nói

**Các lệnh có thể dùng:**

#### 1. Dịch thuật
```
Dịch sang tiếng Anh: Xin chào
Dịch sang tiếng Việt: Hello world
Translate to English: Hôm nay trời đẹp
```

#### 2. Phân tích cảm xúc
```
Phân tích cảm xúc: This product is amazing!
Analyze sentiment: Tôi rất thất vọng về dịch vụ này
```

#### 3. Nhận diện ảnh
```
Phân tích ảnh này: https://example.com/cat.jpg
What's in this image: [URL]
```

#### 4. Text-to-Speech
```
Đọc cho tôi: Hello world
Text to speech: Chào mừng bạn đến với hệ thống
```

---

### 📚 **RAG Mode** (Retrieval-Augmented Generation)

**Công dụng:** Tìm kiếm trong knowledge base để trả lời chính xác

**Khi nào dùng:**
- Hỏi về tài liệu đã upload
- Cần câu trả lời dựa trên nguồn cụ thể
- Ôn tập kiến thức đã học

**Ví dụ:**
```
- "Định lý Pythagoras là gì?" (nếu đã upload tài liệu toán)
- "Các loại sorting algorithm"
- "Khái niệm về React Hooks"
```

**Lưu ý:** Cần upload documents vào Knowledge Base trước

---

### 🎓 **Agent Mode**

**Công dụng:** Thực hiện các tác vụ tự động (schedule, grades, credentials)

**Khi nào dùng:**
- Xem thời khóa biểu
- Kiểm tra điểm số
- Quản lý tài khoản

**Các lệnh có thể dùng:**

#### 1. Thời khóa biểu
```
Xem thời khóa biểu
Hôm nay tôi học gì?
Lịch học tuần này
Thứ 2 có lớp gì?
```

#### 2. Điểm số
```
Xem điểm
Điểm của tôi
Kết quả học tập
```

#### 3. Email
```
Gửi email cho giáo viên
Email thông báo nghỉ học
```

**Lưu ý:** Cần cấu hình tài khoản trường trong Settings → Credentials

---

## 🎨 Giao diện Mode Selector

### Header Buttons
```
┌─────────────────────────────────────────────────┐
│  🤖 Normal | 🌐 Cloud | 📚 RAG | 🎓 Agent       │
│  (active button có background trắng + shadow)    │
└─────────────────────────────────────────────────┘
```

### Mode Helper (dưới input box)
Mỗi mode hiển thị:
- Icon + Tên mode
- Hướng dẫn ngắn gọn
- Ví dụ lệnh (nếu có)

---

## 💡 Tips sử dụng

### Auto-switching (tương lai)
Chatbox sẽ tự động nhận diện intent và gợi ý mode phù hợp:
- Nhập "Dịch sang..." → Gợi ý: "Switch to Cloud Mode?"
- Nhập "Xem thời khóa biểu" → Gợi ý: "Switch to Agent Mode?"

### Keyboard Shortcuts (tương lai)
```
Ctrl + 1 → Normal Mode
Ctrl + 2 → Cloud Mode
Ctrl + 3 → RAG Mode
Ctrl + 4 → Agent Mode
```

---

## 🔧 Technical Implementation

**State:**
```typescript
type ChatMode = 'normal' | 'google-cloud' | 'rag' | 'agent';
const [chatMode, setChatMode] = useState<ChatMode>('normal');
```

**Auto RAG:**
- RAG Mode → `useRag = true`
- Other modes → `useRag = false`

**Backend routing:**
- Backend tự động detect intent
- Google Cloud mode priority cao nhất
- Agent features check tiếp theo
- Normal chat là fallback

---

## 📝 Example Workflow

### Workflow 1: Dịch + Học
1. Click **🌐 Cloud Mode**
2. "Dịch sang tiếng Anh: Tôi đang học lập trình"
3. Nhận translation: "I am learning programming"
4. Switch sang **🤖 Normal Mode**
5. "Giải thích cách học lập trình hiệu quả"

### Workflow 2: Xem lịch + Học
1. Click **🎓 Agent Mode**
2. "Xem thời khóa biểu hôm nay"
3. Nhận schedule
4. Switch sang **📚 RAG Mode**
5. "Ôn tập về chương 3 môn Toán"

---

## ✅ Checklist triển khai

- [x] UI Mode Selector với 4 nút
- [x] Mode Helper Text động
- [x] Auto-adjust RAG based on mode
- [ ] Auto-suggest mode dựa vào input
- [ ] Keyboard shortcuts
- [ ] Mode history/analytics
- [ ] Save preferred mode per user

---

**Mode selector giúp bạn:**
✅ Biết rõ đang dùng chức năng gì
✅ Dễ dàng chuyển đổi giữa các mode
✅ Có gợi ý lệnh cho từng mode
✅ Tối ưu trải nghiệm chat

Giờ bạn có thể chat thông minh hơn! 🚀
