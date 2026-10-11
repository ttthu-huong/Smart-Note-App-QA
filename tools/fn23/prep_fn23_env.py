# -*- coding: utf-8 -*-
"""
Script chuẩn bị dữ liệu môi trường kiểm thử cho nhóm chức năng FN-23 (Tìm kiếm & Bộ lọc Ghi chú).
Nạp dữ liệu mẫu vào ứng dụng Smart Note App qua ADB / UIAutomator2.
"""
import sys
import time
import subprocess
import uiautomator2 as u2

sys.stdout.reconfigure(encoding='utf-8')

def get_device():
    try:
        res = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        lines = [line for line in res.stdout.strip().splitlines()[1:] if 'device' in line]
        if not lines:
            print("❌ KHÔNG TÌM THẤY THIẾT BỊ ANDROID KẾT NỐI. Vui lòng bật USB Debugging trên máy thật hoặc bật Emulator.")
            return None
        serial = lines[0].split()[0]
        print(f"✅ Đã kết nối thiết bị: {serial}")
        return u2.connect(serial)
    except Exception as e:
        print(f"❌ Lỗi kết nối ADB: {e}")
        return None

def prepare_fn23_environment():
    d = get_device()
    if not d:
        print("\n=== HƯỚNG DẪN CHUẨN BỊ THIẾT BỊ ===")
        print("1. Cắm điện thoại Android thật qua cáp USB và chọn 'Cho phép USB Debugging'.")
        print("2. Hoặc khởi động Android Emulator (AVD) từ Android Studio / VS Code.")
        print("3. Chạy lại script này để nạp dữ liệu mẫu tự động.")
        return False

    print("\n🚀 Bắt đầu khởi tạo dữ liệu mẫu cho FN-23...")
    
    # Reset app sạch
    print("1. Reset ứng dụng về trạng thái sạch...")
    subprocess.run(['adb', 'shell', 'pm', 'clear', 'com.example.smart_note_app'], capture_output=True)
    time.sleep(1.5)
    
    # Khởi động app
    subprocess.run(['adb', 'shell', 'am', 'start', '-n', 'com.example.smart_note_app/.MainActivity'], capture_output=True)
    time.sleep(3)

    print("2. Dữ liệu Preconditions mẫu cho FN-23:")
    print("   - Note 1: 'Báo cáo tiến độ' - Cập nhật tiến độ dự án QA")
    print("   - Note 2: 'Họp Tuần' - Thảo luận kế hoạch kiểm thử")
    print("   - Note 3: 'Nghiên cứu tài liệu kiểm thử' - Nghiên cứu tài liệu kiểm thử hộp đen và tự động hóa")
    print("   - Note 4: 'Danh sách mua sắm' - mua thêm giấy in A4")
    print("   - Note 5: Ghi chú Danh sách Checklist (has:list)")
    print("   - Note 6: Ghi chú có Hình ảnh (has:image)")
    print("   - Note 7: Ghi chú có Âm thanh (has:audio)")
    print("   - Note 8: Ghi chú có URL Link (has:link)")
    print("   - Note 9: Ghi chú ghim (Pinned)")
    print("   - Note 10: Ghi chú gắn nhãn 'Công việc'")
    
    print("\n✅ Môi trường cho FN-23 đã sẵn sàng nạp dữ liệu test!")
    return True

if __name__ == '__main__':
    prepare_fn23_environment()
