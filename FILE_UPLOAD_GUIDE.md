# 📁 Hướng Dẫn Upload File/Ảnh Trong Chatbox

## 🎯 Tính Năng

Ứng dụng hỗ trợ học tập của bạn giờ đây có thể:
- ✅ **Upload ảnh** (JPG, PNG, GIF, WebP) để AI phân tích
- ✅ **Upload file** (PDF, TXT) để AI đọc và giải thích
- ✅ **Gemini Vision API** tự động nhận diện và phân tích hình ảnh
- ✅ **Preview ảnh** trước khi gửi
- ✅ **Hiển thị file đính kèm** trong tin nhắn

## 🚀 Cách Sử Dụng

### 1. Upload Ảnh/File
1. Click vào nút **📎 (Paperclip)** bên trái ô nhập tin nhắn
2. Chọn file từ máy tính (tối đa 10MB)
3. Xem preview ảnh hoặc thông tin file
4. Nhập câu hỏi hoặc yêu cầu phân tích
5. Click **Send** để gửi

### 2. Ví Dụ Sử Dụng

**Phân tích bài toán:**
```
📎 Upload: ảnh bài toán
💬 "Giải thích cách làm bài toán này"
```

**Nhận diện chữ viết:**
```
📎 Upload: ảnh ghi chú tay
💬 "Đọc và tóm tắt nội dung trong ảnh"
```

**Phân tích biểu đồ:**
```
📎 Upload: ảnh biểu đồ/chart
💬 "Phân tích biểu đồ này và đưa ra nhận xét"
```

**Giải thích code:**
```
📎 Upload: ảnh code
💬 "Code này làm gì? Giải thích chi tiết"
```

**Đọc tài liệu:**
```
📎 Upload: file PDF
💬 "Tóm tắt nội dung tài liệu này"
```

## 📋 Loại File Được Hỗ Trợ

| Loại File | Định Dạng | Giới Hạn |
|-----------|-----------|----------|
| **Ảnh** | JPG, PNG, GIF, WebP | 10MB |
| **Tài liệu** | PDF, TXT | 10MB |

## 🔧 Chi Tiết Kỹ Thuật

### Frontend Changes

#### 1. **ChatPage.tsx**

**New States:**
```typescript
const [selectedFile, setSelectedFile] = useState<File | null>(null);
const [filePreview, setFilePreview] = useState<string | null>(null);
const fileInputRef = useRef<HTMLInputElement>(null);
```

**File Selection Handler:**
```typescript
const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0];
  // Validation: size, type
  // Create preview for images
  // Show toast notification
};
```

**Message Interface Updated:**
```typescript
interface Message {
  // ... existing fields
  attachment?: {
    type: 'image' | 'file';
    url: string;
    name: string;
    mimeType?: string;
  };
}
```

**UI Components:**
- Hidden file input with ref
- Paperclip button to trigger file selection
- File preview card with image/icon
- Remove file button
- Attachment display in message bubble

#### 2. **chatService.ts**

**Updated Function:**
```typescript
sendMessageWithActions: async (
  message: string, 
  useRag: boolean, 
  aiProvider: string, 
  groqModel?: string,
  imageBase64?: string,      // NEW
  imageMimeType?: string     // NEW
): Promise<any>
```

### Backend Changes

#### 1. **main.py - ChatRequest Model**

```python
class ChatRequest(BaseModel):
    message: str
    model: str = "gemini-flash-latest"
    ai_provider: str = "gemini"
    use_rag: bool = True
    image_base64: Optional[str] = None      # NEW
    image_mime_type: Optional[str] = None   # NEW
```

#### 2. **Gemini Vision API Integration**

```python
# Check if image is provided
if request.image_base64 and request.image_mime_type:
    # Decode base64
    image_data = base64.b64decode(request.image_base64)
    
    # Create multi-modal content
    content_parts = [
        {
            'mime_type': request.image_mime_type,
            'data': image_data
        },
        prompt
    ]
    
    # Use vision-capable model
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(content_parts)
```

## 🎨 UI/UX Features

### File Upload Button
```tsx
<button
  onClick={() => fileInputRef.current?.click()}
  className="flex items-center justify-center px-3 py-2 bg-gray-100 hover:bg-gray-200"
  title="Đính kèm file hoặc ảnh"
>
  <Paperclip className="w-5 h-5" />
</button>
```

### File Preview Card
```tsx
{selectedFile && (
  <div className="flex items-center space-x-2 p-2 bg-blue-50 rounded-lg">
    <img src={filePreview} alt="Preview" className="w-12 h-12" />
    <div>
      <p className="text-sm">{selectedFile.name}</p>
      <p className="text-xs">{(selectedFile.size / 1024).toFixed(1)} KB</p>
    </div>
    <button onClick={handleRemoveFile}>
      <X className="w-4 h-4" />
    </button>
  </div>
)}
```

### Message Attachment Display
```tsx
{message.attachment && (
  <div className="mt-3">
    {message.attachment.type === 'image' ? (
      <img 
        src={message.attachment.url} 
        alt={message.attachment.name}
        className="max-w-xs rounded-lg shadow-md"
        onClick={() => window.open(message.attachment!.url, '_blank')}
      />
    ) : (
      <a href={message.attachment.url} download>
        <Paperclip /> {message.attachment.name}
      </a>
    )}
  </div>
)}
```

## 🔐 Bảo Mật & Giới Hạn

- **Kích thước tối đa:** 10MB mỗi file
- **Định dạng được phép:** Chỉ ảnh và tài liệu text
- **Validation:** Client-side và server-side
- **Base64 encoding:** Dữ liệu được mã hóa an toàn
- **Không lưu file:** File được xử lý tức thì, không lưu trên server

## 📊 Gemini Vision Capabilities

Gemini Vision API có thể:
- ✅ Nhận diện chữ viết (OCR)
- ✅ Phân tích biểu đồ và đồ thị
- ✅ Giải thích hình ảnh khoa học
- ✅ Đọc công thức toán học
- ✅ Phân tích code trong ảnh
- ✅ Mô tả hình ảnh chi tiết
- ✅ Trả lời câu hỏi về ảnh

## 🎯 Use Cases Cho Học Tập

### 1. **Giải Bài Tập**
- Upload ảnh đề bài
- AI đọc và giải thích từng bước

### 2. **Học Ngôn Ngữ**
- Upload ảnh văn bản ngoại ngữ
- AI dịch và giải thích

### 3. **Khoa Học**
- Upload ảnh thí nghiệm, công thức
- AI phân tích và giải thích

### 4. **Lập Trình**
- Upload ảnh code/error
- AI debug và giải thích

### 5. **Tóm Tắt Tài Liệu**
- Upload PDF bài giảng
- AI tóm tắt nội dung chính

## 🐛 Troubleshooting

### Lỗi: "File quá lớn"
**Giải pháp:** Nén ảnh hoặc chọn file nhỏ hơn 10MB

### Lỗi: "Loại file không được hỗ trợ"
**Giải pháp:** Chỉ upload JPG, PNG, GIF, WebP, PDF, TXT

### Ảnh không hiển thị
**Giải pháp:** 
- Kiểm tra định dạng file
- Thử chọn lại file
- Refresh trang

### AI không phân tích được ảnh
**Giải pháp:**
- Đảm bảo ảnh rõ ràng
- Viết câu hỏi cụ thể
- Thử với ảnh khác

## 🚀 Next Steps / Future Enhancements

- [ ] Hỗ trợ nhiều file cùng lúc
- [ ] Drag & drop upload
- [ ] Hỗ trợ file Word, Excel
- [ ] Lưu history file đã upload
- [ ] Compress ảnh tự động
- [ ] Audio/Video analysis
- [ ] OCR riêng biệt

## 📝 Notes

- **Groq API** không hỗ trợ vision → tự động chuyển sang Gemini khi upload ảnh
- **Gemini 2.0 Flash** được sử dụng cho vision (nhanh và chính xác)
- File được encode base64 trước khi gửi API
- Preview ảnh sử dụng FileReader API
- Không cần lưu file trên server

## 🎉 Kết Luận

Tính năng upload file/ảnh giúp ứng dụng học tập của bạn trở nên mạnh mẽ hơn! 

Học sinh có thể:
- Upload bài tập để được hướng dẫn
- Phân tích hình ảnh khoa học
- Đọc tài liệu nhanh chóng
- Học qua hình ảnh trực quan

**Happy Learning! 🚀📚**
