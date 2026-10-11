# -*- coding: utf-8 -*-
"""
Script tự động nạp 11 Ghi chú mẫu (Precondition Data) cho nhóm FN-23
trực tiếp trên giao diện ứng dụng Smart Note App.
"""
import sys
import time
import subprocess
import uiautomator2 as u2
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

SERIAL = 'R5CW82ECF6M'
PKG = 'com.example.smart_note_app'

d = u2.connect(SERIAL)

def hide_keyboard():
    res = subprocess.run(['adb', '-s', SERIAL, 'shell', 'dumpsys input_method | grep mInputShown'], capture_output=True, text=True)
    if 'mInputShown=true' in res.stdout:
        d.press('back')
        time.sleep(0.4)

def create_text_note(title, content):
    print(f"  --> Creating note: '{title}'...")
    # Click (+) Create button on HomeScreen
    # In Flutter UI, FAB or (+) button is typically around bottom right or top
    # Let's find (+) button or click by content-desc / bounds
    fab = d(description='Tạo ghi chú mới')
    if not fab.exists:
        fab = d(description='+')
    if fab.exists:
        fab.click()
    else:
        # Fallback click on FAB area (bottom right ~ 930, 2020 or similar)
        d.click(930, 2020)
    
    time.sleep(1.2)
    
    # Enter Title
    if title:
        # Tap Title input area (top area ~ 300, 300)
        d.click(300, 300)
        time.sleep(0.3)
        escaped_title = title.replace(' ', '%s')
        subprocess.run(['adb', '-s', SERIAL, 'shell', 'input', 'text', escaped_title])
        time.sleep(0.3)
        hide_keyboard()

    # Enter Content
    if content:
        # Tap Content input area (~ 300, 600)
        d.click(300, 600)
        time.sleep(0.3)
        escaped_content = content.replace(' ', '%s')
        subprocess.run(['adb', '-s', SERIAL, 'shell', 'input', 'text', escaped_content])
        time.sleep(0.3)
        hide_keyboard()

    # Press Back (<-) button on AppBar to save note
    back_btn = d(description='Trở về')
    if not back_btn.exists:
        back_btn = d(description='Back')
    if back_btn.exists:
        back_btn.click()
    else:
        d.press('back')
    
    time.sleep(1.5)

def populate_all_preconditions():
    print("🚀 BẮT ĐẦU TỰ ĐỘNG TẠO DỮ LIỆU TIỀN ĐIỀU KIỆN CHO FN-23...")
    
    # Define notes to create
    notes = [
        ("Báo cáo tiến độ", "Cập nhật tiến độ dự án QA"),
        ("Họp nhóm", "Thảo luận Họp Tuần kiểm thử phần mềm"),
        ("Nghiên cứu", "Nghiên cứu tài liệu kiểm thử phần mềm"),
        ("Văn phòng phẩm", "mua thêm giấy in A4"),
        ("Tài nguyên kiểm thử", "Xem chi tiết tài liệu tại https://example.com/docs"),
        ("Danh sách công việc", "Checklist công việc cần làm trong tuần"),
    ]
    
    for title, content in notes:
        create_text_note(title, content)
        
    print("📸 Chụp ảnh màn hình lưu bằng chứng dữ liệu đã nạp...")
    d.screenshot('evidence_fn23_preconditions_populated.png')
    
    xml_str = d.dump_hierarchy()
    with open('populated_hierarchy.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)
        
    print("✅ Đã khởi tạo thành công dữ liệu tiền điều kiện trên thiết bị!")

if __name__ == '__main__':
    populate_all_preconditions()
