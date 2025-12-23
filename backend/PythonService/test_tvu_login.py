"""
Test TVU Login và lấy TKB
"""
from tvu_scraper import TVUScraper

def main():
    scraper = TVUScraper()
    
    # Nhập thông tin
    print("=" * 50)
    print("🎓 TEST TVU LOGIN & TKB")
    print("=" * 50)
    
    username = input("Nhập MSSV: ")
    password = input("Nhập mật khẩu: ")
    
    print(f"\n🔑 Đang đăng nhập với MSSV: {username}...")
    result = scraper.login(username, password)
    
    if result:
        print("✅ Đăng nhập thành công!")
        if scraper.token:
            print(f"Token: {scraper.token[:50]}...")
        
        # Thử lấy học kỳ
        print("\n📅 Đang lấy danh sách học kỳ...")
        hoc_ky_list = scraper.get_hoc_ky_list()
        if hoc_ky_list:
            print(f"Tìm thấy {len(hoc_ky_list)} học kỳ:")
            for hk in hoc_ky_list[:3]:
                print(f"  - {hk}")
        else:
            print("Không tìm thấy học kỳ")
        
        # Thử lấy TKB
        print("\n📚 Đang lấy thời khóa biểu...")
        schedules = scraper.get_schedule()
        if schedules:
            print(f"Tìm thấy {len(schedules)} lịch học:")
            for s in schedules[:10]:
                print(f"  - {s['day_of_week']}: {s['subject']}")
                print(f"    ⏰ {s['start_time']} - {s['end_time']}")
                print(f"    🏫 Phòng: {s['room']}")
                print(f"    👨‍🏫 GV: {s['teacher']}")
                print()
        else:
            print("Không tìm thấy lịch học")
            
        # Test lấy TKB hôm nay
        print("\n📆 Lịch học hôm nay:")
        today_schedules = scraper.get_schedule_for_today()
        if today_schedules:
            for s in today_schedules:
                print(f"  - {s['start_time']}: {s['subject']} (Phòng {s['room']})")
        else:
            print("  Hôm nay không có lớp")
    else:
        print("❌ Đăng nhập thất bại!")
        print("Kiểm tra lại MSSV và mật khẩu")

if __name__ == "__main__":
    main()
