# -*- coding: utf-8 -*-
"""
Script tự động nạp 11 Ghi chú mẫu (Precondition Data) cho nhóm FN-23
dùng uiautomator2 send_keys an toàn.
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
d.set_fastinput_ime(True)

def create_note_v2(title, content):
    print(f"Creating note: title='{title}' | content='{content}'...")
    
    # 1. Tap Create (+) FAB on HomeScreen (FAB center is usually 936, 2012 on S21 FE)
    fab = d(description='+')
    if not fab.exists:
        fab = d(description='Tạo ghi chú mới')
    if fab.exists:
        fab.click()
    else:
        d.click(936, 2012)
        
    time.sleep(1.5)
    
    # 2. Type Title
    if title:
        # Title field is top field
        d.click(350, 320)
        time.sleep(0.4)
        d.send_keys(title)
        time.sleep(0.4)

    # 3. Type Content
    if content:
        # Content field is lower area
        d.click(350, 650)
        time.sleep(0.4)
        d.send_keys(content)
        time.sleep(0.4)

    # 4. Save & Back
    back_btn = d(description='Trở về')
    if not back_btn.exists:
        back_btn = d(description='Back')
    if back_btn.exists:
        back_btn.click()
    else:
        d.press('back')
        
    time.sleep(1.5)

def main():
    print("=== POPULATING FN-23 PRECONDITION NOTES ===")
    
    notes = [
        ("Báo cáo tiến độ", "Cập nhật tiến độ dự án QA kiểm thử phần mềm"),
        ("Họp nhóm", "Thảo luận Họp Tuần kiểm thử"),
        ("Nghiên cứu", "Nghiên cứu tài liệu kiểm thử phần mềm"),
        ("Văn phòng phẩm", "mua thêm giấy in A4"),
        ("Tài nguyên kiểm thử", "Xem chi tiết tại https://example.com/docs"),
        ("Danh sách công việc", "Checklist công việc cần thực hiện"),
    ]
    
    for title, content in notes:
        create_note_v2(title, content)
        
    d.set_fastinput_ime(False)
    
    d.screenshot('evidence_fn23_preconditions_v2.png')
    xml_str = d.dump_hierarchy()
    with open('populated_hierarchy_v2.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)
        
    print("📸 Saved evidence_fn23_preconditions_v2.png and populated_hierarchy_v2.xml")
    
    # Read visible elements on HomeScreen
    root = ET.fromstring(xml_str)
    print("\n=== POPULATED NOTES ON HOMESCREEN ===")
    for node in root.iter('node'):
        desc = node.attrib.get('content-desc', '')
        text = node.attrib.get('text', '')
        if desc or text:
            print(f"desc='{desc}' | text='{text}'")

if __name__ == '__main__':
    main()
