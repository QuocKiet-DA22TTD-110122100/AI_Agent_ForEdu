# 📧 Hướng Dẫn Gửi Email Thông Minh Qua Chatbox

## 🎯 Tính năng mới

Giờ đây bạn có thể **gửi email trực tiếp từ chatbox** với sự hỗ trợ của AI:

1. ✅ **Suggest contacts tự động** từ Gmail của bạn
2. ✅ **AI tạo nội dung email** dựa trên chủ đề
3. ✅ **Chỉnh sửa trước khi gửi**
4. ✅ **Gửi ngay trong chatbox**

## 🚀 Cách sử dụng

### Bước 1: Kết nối Gmail

Trước tiên, cần kết nối Google Account:

1. Vào **Settings** (trang cài đặt)
2. Tìm mục **"Google Cloud Integration"**
3. Click nút **"Connect Google"**
4. Đăng nhập và cấp quyền

### Bước 2: Gửi email qua chatbox

#### **Cách 1: AI suggest contacts (RECOMMENDED)**

Chỉ cần nói chủ đề email, AI sẽ gợi ý người nhận:

```
User: "gửi email xin nghỉ học đến thầy"
```

**AI sẽ:**
1. Lấy danh sách contacts từ Gmail của bạn
2. Hiển thị top 10 người bạn thường gửi email
3. Cho bạn chọn bằng số

```
📧 Gửi email: xin nghỉ học

📋 Chọn người nhận:

1. Nguyễn Văn A (teacher.a@tvu.edu.vn) _5 emails_
2. Trần Thị B (teacher.b@tvu.edu.vn) _3 emails_
3. Phòng Đào Tạo (daotao@tvu.edu.vn) _10 emails_
...

💡 Cách chọn:
• Nhắn số: "1" hoặc "chọn 1"
• Hoặc gõ email trực tiếp: "teacher@tvu.edu.vn"
```

#### **Bước 3: Chọn người nhận**

```
User: "1"
hoặc
User: "chọn 1"
```

**AI sẽ:**
1. Tạo draft email tự động bằng AI (Groq/Gemini)
2. Hiển thị preview để bạn xem trước

```
📝 Draft Email đã tạo:

📧 Người nhận: Nguyễn Văn A (teacher.a@tvu.edu.vn)
📌 Chủ đề: Xin phép nghỉ học

📄 Nội dung:
---
Kính gửi thầy Nguyễn Văn A,

Em là [Tên của bạn], sinh viên lớp [Lớp]. 
Em xin phép được nghỉ học buổi học ngày mai 
vì lý do sức khỏe.

Em xin cảm ơn thầy!

Trân trọng,
[Tên của bạn]
---

✅ Nếu đồng ý: nhắn "gửi" hoặc "ok"
✏️ Chỉnh sửa: nhắn "sửa [phần cần sửa]"
❌ Hủy: nhắn "hủy"
```

#### **Bước 4: Xác nhận hoặc chỉnh sửa**

**Option A: Gửi luôn**
```
User: "gửi"
hoặc
User: "ok"
```

**Option B: Chỉnh sửa**
```
User: "sửa nội dung: Em xin nghỉ học vì có việc gia đình đột xuất"
```

AI sẽ cập nhật draft và cho bạn xem lại.

**Option C: Hủy**
```
User: "hủy"
```

#### **Bước 5: Email được gửi!**

```
✅ Email đã gửi thành công!

📧 Người nhận: teacher.a@tvu.edu.vn
📝 Chủ đề: Xin phép nghỉ học
📅 Thời gian: 14:30 23/12/2025
```

---

## 📝 Ví dụ Use Cases

### Use Case 1: Xin nghỉ học

```
User: "gửi email xin nghỉ học đến thầy"
AI: [Hiển thị list giáo viên]
User: "1"
AI: [Tạo draft email xin nghỉ]
User: "gửi"
AI: ✅ Đã gửi!
```

### Use Case 2: Hỏi bài

```
User: "gửi mail hỏi bài tập về nhà"
AI: [Suggest contacts]
User: "chọn 2"
AI: [Draft email hỏi bài]
User: "sửa: em muốn hỏi bài tập chương 3"
AI: [Update draft]
User: "ok"
AI: ✅ Gửi thành công!
```

### Use Case 3: Liên hệ phòng ban

```
User: "soạn email hỏi về thủ tục xin giấy chứng nhận"
AI: [Suggest: Phòng Đào Tạo, VP Khoa,...]
User: "3"
AI: [Draft chuyên nghiệp]
User: "gửi"
```

---

## 🎨 Cách 2: Gửi trực tiếp (Không cần suggest)

Nếu bạn đã biết email người nhận:

```
User: "gửi email cho teacher@tvu.edu.vn chủ đề Xin nghỉ học nội dung Em xin phép nghỉ học ngày mai vì ốm"
```

AI sẽ gửi ngay mà không cần qua bước suggest.

---

## ⚙️ Công nghệ sử dụng

### Backend
- **Gmail API (OAuth 2.0)**: Truy cập Gmail an toàn
- **Groq AI / Gemini**: Generate nội dung email thông minh
- **Contact Analysis**: Phân tích sent emails để suggest

### Flow Architecture

```
User Message
    ↓
Detect Send Email Intent
    ↓
Has recipient email?
    ├─ YES → Parse & Send directly
    └─ NO → Get contacts from Gmail
        ↓
    Display contacts list
        ↓
    Wait for user selection
        ↓
    AI generate draft email
        ↓
    Show preview
        ↓
    Wait for confirm/edit
        ↓
    Send email via Gmail API
```

---

## 🔒 Bảo mật & Quyền riêng tư

### ✅ An toàn tuyệt đối

1. **OAuth 2.0**: Không lưu mật khẩu Gmail
2. **Token encrypted**: Access tokens được mã hóa trong database
3. **User control**: Bạn có toàn quyền với emails của mình
4. **No storage**: Không lưu nội dung email của bạn

### Quyền truy cập Gmail

Khi connect Google, app xin các quyền:

- ✅ **gmail.readonly**: Đọc emails (để lấy contacts)
- ✅ **gmail.send**: Gửi email thay bạn
- ✅ **gmail.compose**: Tạo draft
- ✅ **gmail.modify**: Đánh dấu đã đọc/chưa đọc

👉 **Bạn có thể thu hồi quyền bất cứ lúc nào** tại: https://myaccount.google.com/permissions

---

## 🐛 Troubleshooting

### Lỗi: "Chưa kết nối Gmail"

**Giải pháp:**
1. Vào Settings
2. Click "Connect Google"
3. Đăng nhập và cấp quyền

### Lỗi: "Không tìm thấy contacts"

**Nguyên nhân:** Bạn chưa từng gửi email nào qua Gmail

**Giải pháp:**
- Sử dụng cách 2: Gửi trực tiếp với email address
- Hoặc gửi vài email thủ công trước để tạo contact list

### Lỗi: Token expired

**Giải pháp:**
1. Disconnect Google trong Settings
2. Connect lại
3. Token sẽ tự động refresh

---

## 🎯 Roadmap (Coming Soon)

- [ ] **Attach files**: Đính kèm tài liệu từ Google Drive
- [ ] **Templates**: Lưu mẫu email thường dùng
- [ ] **Scheduled send**: Hẹn giờ gửi email
- [ ] **CC/BCC support**: Gửi CC cho nhiều người
- [ ] **Email signatures**: Tự động thêm chữ ký
- [ ] **Smart reply**: AI suggest câu trả lời nhanh

---

## 💡 Tips & Tricks

### 1. Context-aware AI

AI sẽ điều chỉnh tone dựa trên người nhận:
- Giáo viên → **Trang trọng, lịch sự**
- Bạn bè → **Thân thiện, casual**
- Phòng ban → **Chuyên nghiệp, súc tích**

### 2. Smart keywords

Bạn có thể dùng nhiều từ khóa:
- "gửi email xin nghỉ" ✅
- "soạn mail hỏi bài" ✅
- "viết email cảm ơn" ✅
- "draft email report" ✅

### 3. Multi-language

AI hiểu cả tiếng Việt và tiếng Anh:
- "send email to teacher about homework"
- "gửi mail cho thầy về bài tập"

---

## 📚 API Documentation

### Endpoints mới

#### `GET /api/gmail/contacts/{user_id}`
Lấy danh sách contacts từ sent emails

#### `POST /api/gmail/draft`
Tạo draft email bằng AI

```json
{
  "subject_keyword": "xin nghỉ học",
  "recipient_name": "thầy Nguyễn Văn A"
}
```

#### `POST /api/gmail/send`
Gửi email

```json
{
  "user_id": 1,
  "to": "teacher@tvu.edu.vn",
  "subject": "Xin nghỉ học",
  "body": "..."
}
```

---

## 🆘 Support

Nếu gặp vấn đề:

1. **Check logs**: Backend terminal sẽ hiển thị errors
2. **Re-connect**: Thử disconnect và connect lại Google
3. **Check permissions**: Xem quyền tại Google Account settings

---

**Happy emailing! 📧✨**
