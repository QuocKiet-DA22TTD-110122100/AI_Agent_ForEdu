#!/usr/bin/env python3
"""
Ví dụ: Cách gọi API chat để lấy TKB với ngày khác nhau
"""

import requests
import json
from datetime import datetime

# API endpoints
CHAT_API = "http://localhost:8000/api/chat"
TEST_API = "http://localhost:8000/api/test/tvu-schedule"

# Headers
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}

# Test data (MSSV và password TVU)
TEST_CREDENTIALS = {
    "mssv": "your_mssv",
    "password": "your_tvu_password"
}

def test_chat_schedule(message: str):
    """
    Test lấy TKB qua chat endpoint
    
    Args:
        message: Tin nhắn từ user (ví dụ: "Hôm qua tôi học gì?")
    """
    print("\n" + "=" * 70)
    print(f"📨 Testing Chat: '{message}'")
    print("=" * 70)
    
    payload = {
        "message": message,
        "use_rag": False,
        "ai_provider": "gemini",
        "model": "gemini-2.5-flash"
    }
    
    try:
        response = requests.post(CHAT_API, json=payload, headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Response:")
            print(f"   Message: {data.get('response', 'N/A')[:200]}...")
            if 'schedules' in data:
                print(f"   Schedules found: {len(data['schedules'])} items")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_tvu_schedule(message: str):
    """
    Test lấy TKB qua TVU test endpoint (direct)
    
    Args:
        message: Tin nhắn mô tả ngày (ví dụ: "Hôm qua")
    """
    print("\n" + "=" * 70)
    print(f"🧪 Testing TVU Direct: '{message}'")
    print("=" * 70)
    
    payload = {
        "mssv": TEST_CREDENTIALS["mssv"],
        "password": TEST_CREDENTIALS["password"],
        "message": message
    }
    
    try:
        response = requests.post(TEST_API, json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Response:")
            print(f"   Success: {data.get('success')}")
            print(f"   Message: {data.get('message', 'N/A')[:300]}...")
            if 'schedules' in data:
                print(f"   Schedules found: {len(data['schedules'])} items")
                for i, schedule in enumerate(data['schedules'][:3]):
                    print(f"\n   Schedule {i+1}:")
                    print(f"     - Subject: {schedule.get('subject')}")
                    print(f"     - Time: {schedule.get('start_time')} - {schedule.get('end_time')}")
                    print(f"     - Room: {schedule.get('room')}")
                    print(f"     - Teacher: {schedule.get('teacher')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    print("\n" + "📚" * 35)
    print("DEMO: Lấy TKB với Ngày Khác Nhau")
    print("📚" * 35)
    
    # Test messages
    test_cases = [
        ("Hôm nay tôi học gì?", "Lấy TKB hôm nay"),
        ("Hôm qua tôi có lớp không?", "Lấy TKB hôm qua"),
        ("Mai lịch sao?", "Lấy TKB ngày mai"),
        ("Mốt xem lịch", "Lấy TKB mốt (2 ngày sau)"),
        ("Kia bảo tôi thời khóa biểu", "Lấy TKB kia (3 ngày sau)"),
        ("Thứ 2 tôi học gì?", "Lấy TKB thứ 2"),
        ("Xem lịch thứ 5", "Lấy TKB thứ 5"),
        ("Chủ nhật có buổi học nào?", "Lấy TKB chủ nhật"),
    ]
    
    print("\n" + "─" * 70)
    print("🔍 Hướng dẫn:")
    print("─" * 70)
    print("""
    1. Trước tiên, cập nhật:
       - HEADERS["Authorization"] = "Bearer YOUR_TOKEN"
       - TEST_CREDENTIALS["mssv"] = "YOUR_MSSV"
       - TEST_CREDENTIALS["password"] = "YOUR_PASSWORD"
    
    2. Chạy script:
       python examples_schedule_queries.py
    
    3. Xem kết quả từ API
    """)
    
    print("\n" + "=" * 70)
    print("📋 TEST CASES")
    print("=" * 70)
    
    for message, description in test_cases:
        print(f"\n[{description}]")
        print(f"Input: '{message}'")
        
        # Uncomment để test via API
        # test_tvu_schedule(message)
        # hoặc
        # test_chat_schedule(message)
        
        # Tạm thời chỉ in ra expected output
        print("Expected: 📅 **Lịch học [ngày]:**")
        print("         (Danh sách các lớp...)")

def example_response():
    """
    Ví dụ response từ API
    """
    print("\n" + "=" * 70)
    print("📤 Ví Dụ Response")
    print("=" * 70)
    
    example = {
        "success": True,
        "message": """📅 **Lịch học hôm qua (19/12/2024):**

🕐 **08:00 - 09:30** (Thứ 4)
   📚 Toán Cao Cấp 1
   🏫 Phòng 301
   👨‍🏫 Thầy Nguyễn Văn A

🕐 **10:00 - 11:30** (Thứ 4)
   📚 Tiếng Anh 2
   🏫 Phòng 305
   👨‍🏫 Cô Trần Thị B

🕐 **13:30 - 15:00** (Thứ 4)
   📚 Lập Trình Python
   🏫 Phòng 201
   👨‍🏫 Thầy Lê Văn C
""",
        "schedules": [
            {
                "day_of_week": "WEDNESDAY",
                "start_time": "08:00",
                "end_time": "09:30",
                "subject": "Toán Cao Cấp 1",
                "room": "301",
                "teacher": "Thầy Nguyễn Văn A"
            },
            {
                "day_of_week": "WEDNESDAY",
                "start_time": "10:00",
                "end_time": "11:30",
                "subject": "Tiếng Anh 2",
                "room": "305",
                "teacher": "Cô Trần Thị B"
            },
            {
                "day_of_week": "WEDNESDAY",
                "start_time": "13:30",
                "end_time": "15:00",
                "subject": "Lập Trình Python",
                "room": "201",
                "teacher": "Thầy Lê Văn C"
            }
        ]
    }
    
    print("\nJSON Response:")
    print(json.dumps(example, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
    example_response()
    
    print("\n" + "=" * 70)
    print("💡 Ghi Chú:")
    print("=" * 70)
    print("""
    - Hỗ trợ ngày tương đối: hôm qua, mai, mốt, kia
    - Hỗ trợ ngày cụ thể: thứ 2-7, chủ nhật
    - API tự động phát hiện intent từ tin nhắn
    - Kết quả bao gồm danh sách chi tiết các lớp
    - Cần TVU credential để lấy dữ liệu
    """)
    print("=" * 70 + "\n")
