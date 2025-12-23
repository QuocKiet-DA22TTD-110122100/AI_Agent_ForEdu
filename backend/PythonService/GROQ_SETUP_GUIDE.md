# ⚡ Hướng dẫn sử dụng Groq AI (LPU Inference)

## ✅ Đã cấu hình

### 1. Groq API Key đã thêm vào `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
DEFAULT_AI_MODEL=gemini  # hoặc "groq"
```

**Lấy API key:** https://console.groq.com/keys

### 2. Code đã support:
- ✅ `groq_helper.py` - Client để gọi Groq API
- ✅ `main.py` - Đã import và khởi tạo Groq client
- ✅ Tự động chọn AI model dựa vào `DEFAULT_AI_MODEL`

---

## 🔄 Cách chuyển sang Groq

### Option 1: Chuyển mặc định sang Groq

Sửa file `.env`:
```env
DEFAULT_AI_MODEL=groq
```

Restart AI service:
```powershell
.\restart-ai-service.ps1
```

### Option 2: Cho phép user chọn model khi chat

**Frontend** - Thêm dropdown chọn model:
```typescript
<select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
  <option value="gemini">Gemini 2.5 Flash</option>
  <option value="groq">Groq LPU</option>
</select>
```

**Backend** - API nhận model parameter:
```python
@app.post("/chat")
async def chat(request: ChatRequest):
    # request.ai_provider = "gemini" hoặc "groq"
    if request.ai_provider == "groq" and groq_client:
        response = groq_client.generate_text(...)
    else:
        # Use Gemini
        model = genai.GenerativeModel(request.model)
        response = model.generate_content(...)
```

---

## 🆚 So sánh Gemini vs Groq

| Feature | Gemini 2.5 Flash | Groq LPU |
|---------|------------------|-----------|
| **Tốc độ** | ⚡ Cực nhanh | 🚀 Siêu nhanh (LPU) |
| **Miễn phí** | 1500 requests/ngày | 14,400 req/day (free) |
| **Độ thông minh** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Kiến thức** | Cập nhật | Llama 3.1, Mixtral |
| **Multimodal** | ✅ Vision, Audio | ❌ Text only |
| **Giá** | FREE | FREE tier generous |

---

## 📝 Groq Models

### Available Models:
```
llama-3.1-70b-versatile  - Best overall (recommended)
llama-3.1-8b-instant     - Fastest inference
mixtral-8x7b-32768       - Long context (32K tokens)
gemma2-9b-it            - Lightweight & fast
```

### Example Request:
```python
from groq_helper import GroqClient

client = GroqClient(api_key="gsk_...")
response = client.generate_text(
    prompt="Explain quantum computing",
    system_prompt="You are a helpful assistant",
    model="llama-3.1-70b-versatile"
)
print(response)
```

---

## 🛠️ TODO: Tích hợp Groq vào Chat endpoint

Cần update hàm `/chat` trong `main.py`:

```python
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, authorization: str = Header(None)):
    """
    Chat endpoint với support cả Gemini và Groq
    """
    # Extract AI provider từ request hoặc dùng DEFAULT
    ai_provider = getattr(request, 'ai_provider', DEFAULT_AI_MODEL)
    
    # System prompt
    system_prompt = """🎓 Bạn là AI Learning Assistant..."""
    
    # Generate response dựa vào AI provider
    if ai_provider == "groq" and groq_client:
        # Use Groq LPU
        ai_response = groq_client.generate_text(
            prompt=full_prompt,
            system_prompt=system_prompt,
            model="llama-3.1-70b-versatile"
        )
    else:
        # Use Gemini (default)
        gemini_model = genai.GenerativeModel(request.model)
        result = gemini_model.generate_content(full_prompt)
        ai_response = result.text
    
    return ChatResponse(
        response=ai_response,
        model=ai_provider,
        rag_enabled=request.use_rag
    )
```

---

## 🎯 Next Steps

### 1. Test Groq helper trực tiếp:
```powershell
cd backend\PythonService
python groq_helper.py
```

### 2. Update ChatRequest model:
```python
class ChatRequest(BaseModel):
    message: str
    model: str = "gemini-flash-latest"
    ai_provider: str = "gemini"  # NEW: "gemini" or "groq"
    use_rag: bool = True
```

### 3. Thêm Groq vào Mode Selector:
```tsx
<button onClick={() => setAiProvider('groq')}>
  ⚡ Groq
</button>
```

### 4. Show AI provider trong chat:
```tsx
<span className="text-xs text-gray-500">
  Powered by {aiProvider === 'groq' ? '⚡ Groq LPU' : '✨ Gemini'}
</span>
```

---

## 💡 Use Cases

### Khi nào dùng Groq:
- ✅ Cần tốc độ inference cực nhanh (LPU)
- ✅ Chạy Llama 3.1 70B hoặc Mixtral
- ✅ Token limit lớn (32K với Mixtral)
- ✅ Miễn phí 14,400 requests/ngày

### Khi nào dùng Gemini:
- ✅ Cần xử lý ảnh/video (Vision)
- ✅ Miễn phí 1,500 requests/ngày
- ✅ Tốc độ cực nhanh
- ✅ Multimodal capabilities

---

## 🔐 Security Note

⚠️ **QUAN TRỌNG:** API keys trong `.env` không được commit lên Git!

Đảm bảo `.env` đã có trong `.gitignore`:
```
backend/PythonService/.env
```

---

**Grok đã sẵn sàng! Giờ chỉ cần tích hợp vào chat endpoint.** 🚀
