# -*- coding: utf-8 -*-
"""
Script nạp dữ liệu tiền điều kiện chuẩn xác cho FN-23.
Sử dụng tọa độ chuẩn của màn hình Editor trên thiết bị Samsung Galaxy S21 FE 5G.
"""
import sys
import time
import subprocess
import uiautomator2 as u2
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

SERIAL = 'R5CW82ECF6M'
d = u2.connect(SERIAL)

def create_note_exact(title, content):
    print(f"\nCreating note: '{title}'...")
    
    # 1. Click FAB (+) button at center (964, 2185)
    d.click(964, 2185)
    time.sleep(1.2)
    
    # 2. Focus Title input field (bounds ~ 540, 350)
    d.click(540, 350)
    time.sleep(0.4)
    if title:
        d.send_keys(title)
        time.sleep(0.4)
        
    # 3. Focus Content input field (bounds ~ 540, 650)
    if content:
        d.click(540, 650)
        time.sleep(0.4)
        d.send_keys(content)
        time.sleep(0.4)

    # 4. Click Back button on AppBar (bounds ~ 70, 170) to save and exit to HomeScreen
    d.click(70, 170)
    time.sleep(1.5)

def main():
    print("=== POPULATING ALL FN-23 PRECONDITION NOTES ===")
    
    notes = [
        ("Báo cáo tiến độ", "Cập nhật tiến độ dự án QA kiểm thử phần mềm"),
        ("Họp Tuần", "Thảo luận kế hoạch kiểm thử"),
        ("Nghiên cứu", "Nghiên cứu tài liệu kiểm thử phần mềm"),
        ("Văn phòng phẩm", "mua thêm giấy in A4"),
        ("Tài nguyên kiểm thử", "Xem chi tiết tại https://example.com/docs"),
        ("Danh sách công việc", "Checklist công việc cần làm"),
    ]
    
    for title, content in notes:
        create_note_exact(title, content)

    # Screenshot HomeScreen to verify created notes
    d.screenshot('evidence_fn23_notes_populated_perfect.png')
    xml_str = d.dump_hierarchy()
    with open('populated_perfect_hierarchy.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)

    root = ET.fromstring(xml_str)
    print("\n=== VERIFYING CREATED NOTES ON HOMESCREEN ===")
    found_notes = []
    for node in root.iter('node'):
        desc = node.attrib.get('content-desc', '')
        text = node.attrib.get('text', '')
        val = (desc or text).strip()
        if val and any(k in val for k in ['Báo cáo', 'Họp', 'Nghiên cứu', 'giấy in A4', 'Tài nguyên', 'Danh sách']):
            found_notes.append(val)
            print(f"  --> Found note on UI: {val!r}")

    print(f"\n✅ Created {len(found_notes)} precondition notes successfully!")

if __name__ == '__main__':
    main()
