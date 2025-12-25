# 🚀 LangChain Quick Start - 5 Phút

## ✨ Tích Hợp Xong Rồi!

Dự án của bạn đã có **LangChain AI Agent**! Chỉ cần 3 bước để chạy:

---

## 📦 **Bước 1: Cài Đặt (2 phút)**

```cmd
cd backend\PythonService
install-langchain.cmd
```

Hoặc manual:
```bash
pip install langchain langchain-google-genai langchain-community
```

---

## 🚀 **Bước 2: Chạy Service (1 phút)**

```bash
cd backend/PythonService
python main.py
```

Xem log:
```
✅ LangChain Agent initialized
✅ 6 tools available
Server running on http://localhost:8000
```

---

## 🧪 **Bước 3: Test (2 phút)**

### **Option 1: Test Script**
```bash
python test_langchain_agent.py
```

### **Option 2: cURL**
```bash
curl -X POST http://localhost:8000/api/chat/langchain \
  -H "Content-Type: application/json" \
  -d '{"message": "Xin chào!", "user_id": 1}'
```

### **Option 3: Swagger UI**
Mở: http://localhost:8000/docs

Tìm: `POST /api/chat/langchain`

Test với:
```json
{
  "message": "Hôm nay tôi học gì?",
  "user_id": 1
}
```

---

## 🎯 **Thử Ngay**

### **Test 1: Simple Chat**
```json
{
  "message": "Xin chào! Bạn là ai?",
  "user_id": 1
}
```

### **Test 2: Schedule Query**
```json
{
  "message": "Hôm nay tôi học gì?",
  "user_id": 1
}
```

### **Test 3: Multi-Step**
```json
{
  "message": "Gửi email xin nghỉ cho thầy và thêm vào lịch",
  "user_id": 1
}
```

### **Test 4: Memory**
```json
// Message 1
{"message": "Tên tôi là Minh", "user_id": 1}

// Message 2 (agent sẽ nhớ!)
{"message": "Tên tôi là gì?", "user_id": 1}
```

---

## 📊 **Check Status**

```bash
curl http://localhost:8000/api/chat/langchain/status
```

Response:
```json
{
  "available": true,
  "tools": ["GetSchedule", "SendEmail", "GetContacts", ...],
  "tool_count": 6,
  "memory_enabled": true
}
```

---

## 🎉 **Xong!**

Bây giờ bạn có:
- ✅ AI Agent thông minh (không còn if/else)
- ✅ 6 tools tích hợp sẵn
- ✅ Conversation memory
- ✅ ReAct reasoning

**Đọc thêm:** `LANGCHAIN_INTEGRATION_GUIDE.md`

---

## 🐛 **Lỗi Thường Gặp**

### **"LangChain not available"**
→ Chạy: `install-langchain.cmd`

### **"Agent not initialized"**
→ Check `.env` có `GEMINI_API_KEY`

### **"Tool execution failed"**
→ Check logs trong console

---

## 📞 **Support**

- Full guide: `LANGCHAIN_INTEGRATION_GUIDE.md`
- Test script: `test_langchain_agent.py`
- API docs: http://localhost:8000/docs

**Happy coding!** 🚀
