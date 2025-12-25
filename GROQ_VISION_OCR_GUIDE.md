# Groq Vision Support - OCR Image Reading

## Tổng quan

Groq models (Llama, Mixtral) không hỗ trợ vision natively. Để Groq có thể "hiểu" nội dung ảnh, tôi đã implement:

✅ **EasyOCR** - Đọc text từ ảnh (tiếng Anh + tiếng Việt)
⚠️ **BLIP** (Optional) - Mô tả tổng quan ảnh (disabled mặc định vì model nặng ~1GB)

## Cách hoạt động

### Khi user upload ảnh với Groq:

1. **Extract text** từ ảnh bằng EasyOCR
2. **Tạo context** từ text đã extract
3. **Gửi context + câu hỏi** cho Groq
4. Groq trả lời dựa trên text context

### Khi user upload ảnh với Gemini:

- Gemini Vision API xử lý trực tiếp (native vision support)

## Cài đặt

```bash
cd backend/PythonService
pip install easyocr
```

## Sử dụng trong Frontend

**Không cần thay đổi gì!** Frontend vẫn upload ảnh như bình thường:

```typescript
// ChatPage.tsx - Upload ảnh
const handleSend = async () => {
  await chatService.sendMessageWithActions(
    message,
    imageBase64,  // ← Base64 của ảnh
    imageMimeType // ← Mime type
  );
};
```

Backend tự động:
- **Nếu chọn Groq** → Dùng OCR extract text
- **Nếu chọn Gemini** → Dùng Vision API trực tiếp

## Ví dụ

### Test với PowerShell:

```powershell
.\test_groq_vision.ps1
```

### Test trong UI:

1. Mở http://localhost:5173
2. Settings → Chọn **Groq** (Llama 3.3 70B)
3. Click 📎 → Upload ảnh có text
4. Groq sẽ đọc text từ ảnh và trả lời!

## Giới hạn

### OCR Support:
- ✅ Text rõ ràng, cỡ chữ vừa đủ
- ✅ Tiếng Anh, tiếng Việt
- ⚠️ Chữ viết tay (kém chính xác)
- ⚠️ Text nhỏ hoặc bị mờ

### Không thể:
- ❌ Nhận diện đối tượng (vật, người, động vật)
- ❌ Phân tích màu sắc, bố cục
- ❌ Hiểu ngữ cảnh visual phức tạp

→ **Dùng Gemini** cho các trường hợp trên!

## Performance

- **OCR Loading**: ~2-3 giây lần đầu (load model)
- **OCR Processing**: ~1-2 giây/ảnh
- **Groq Response**: ~1-2 giây (rất nhanh!)

**Tổng**: ~3-7 giây (lần đầu), ~2-4 giây (lần sau)

## Tối ưu

### Kích hoạt BLIP (nếu cần mô tả ảnh):

1. Edit `main.py`:
```python
# Uncomment dòng này
from transformers import BlipProcessor, BlipForConditionalGeneration
IMAGE_CAPTION_AVAILABLE = True
```

2. Cài đặt:
```bash
pip install transformers torch
```

**Lưu ý**: BLIP model ~1GB, tốn ~3-5 giây load lần đầu!

## Code Reference

### Backend: `main.py`

```python
def extract_image_content(image_base64, image_mime_type):
    # OCR extract text
    ocr_reader = get_ocr_reader()
    ocr_results = ocr_reader.readtext(image_data)
    text_lines = [text for (bbox, text, prob) in ocr_results]
    
    return {
        "text_content": "\n".join(text_lines),
        "description": f"Image: {format}, {width}x{height}",
        "success": True
    }
```

### Groq Integration:

```python
if request.ai_provider == "groq" and has_image:
    image_content = extract_image_content(image_base64, mime_type)
    
    # Build context
    image_context = f"""
    📸 NỘI DUNG TỪ ẢNH:
    Text trong ảnh: {image_content['text_content']}
    """
    
    # Send to Groq with context
    groq_response = groq_client.generate_text(
        prompt=f"{image_context}\n\n{user_question}"
    )
```

## So sánh Groq vs Gemini

| Feature | Groq + OCR | Gemini Vision |
|---------|------------|---------------|
| **Đọc text** | ✅ Rất tốt | ✅ Excellent |
| **Nhận diện vật thể** | ❌ Không | ✅ Excellent |
| **Hiểu ngữ cảnh** | ⚠️ Giới hạn | ✅ Excellent |
| **Tốc độ** | ⚡ Rất nhanh | ⚡ Nhanh |
| **Cost** | 💰 Miễn phí | 💰 Có quota |

## Khi nào dùng gì?

### Dùng Groq + OCR:
- ✅ Ảnh có nhiều text (code, documents, slides)
- ✅ Cần tốc độ cao
- ✅ Đã hết quota Gemini

### Dùng Gemini Vision:
- ✅ Ảnh không có text
- ✅ Cần hiểu ngữ cảnh visual
- ✅ Nhận diện vật thể, người, cảnh

## Troubleshooting

### "OCR không khả dụng":
```bash
pip install easyocr
```

### "Không tìm thấy text trong ảnh":
- Kiểm tra ảnh có text rõ ràng không
- Text có đủ lớn không (>12pt)
- Ảnh có bị mờ/nghiêng không

### OCR chậm:
- Lần đầu load model (bình thường)
- Ảnh quá lớn → resize trước khi gửi

## API Endpoint

```http
POST /api/chat
Content-Type: application/json

{
  "message": "Explain this code",
  "ai_provider": "groq",
  "model": "llama-3.3-70b-versatile",
  "image_base64": "base64_string_here",
  "image_mime_type": "image/jpeg"
}
```

**Response**:
```json
{
  "response": "Groq's answer based on extracted text...",
  "model": "llama-3.3-70b-versatile (Groq)",
  "rag_enabled": true
}
```

## Future Enhancements

- [ ] Support PDF text extraction
- [ ] Support handwriting recognition
- [ ] Cache OCR results
- [ ] Parallel OCR + Groq processing
- [ ] Custom OCR confidence threshold

---

**Status**: ✅ Production Ready
**Last Updated**: December 24, 2025
