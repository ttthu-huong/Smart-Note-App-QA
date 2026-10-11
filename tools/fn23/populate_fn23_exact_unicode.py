# -*- coding: utf-8 -*-
"""
Script nạp dữ liệu tiếng Việt có dấu chuẩn xác qua Clipboard dán ADB
cho nhóm FN-23.
"""
import sys
import time
import subprocess
import uiautomator2 as u2
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

SERIAL = 'R5CW82ECF6M'
d = u2.connect(SERIAL)

def type_unicode_text(text):
    if not text:
        return
    # Set text to Android clipboard
    d.set_clipboard(text)
    time.sleep(0.3)
    # Long click or paste / send_keys
    # In uiautomator2, d.send_keys(text) or paste works
    try:
        # Broadcast clipboard paste or input via u2
        d.send_keys(text)
    except Exception:
        # Fallback to clip broadcast
        subprocess.run(['adb', '-s', SERIAL, 'shell', 'input', 'keyevent', '279'], capture_output=True) # KEYCODE_PASTE
    time.sleep(0.3)

def create_note_unicode(title, content):
    print(f"Creating note: '{title}'...")
    # Click (+) FAB
    d.click(936, 2012)
    time.sleep(1.5)
    
    # Title input
    if title:
        d.click(350, 320)
        time.sleep(0.3)
        type_unicode_text(title)

    # Content input
    if content:
        d.click(350, 650)
        time.sleep(0.3)
        type_unicode_text(content)

    # Save & Back
    d.press('back')
    time.sleep(1.5)

def main():
    print("=== POPULATING EXACT ACCENTED VIETNAMESE NOTES FOR FN-23 ===")
    
    notes = [
        ("Báo cáo tiến độ", "Cập nhật tiến độ dự án QA kiểm thử phần mềm"),
        ("Họp Tuần", "Thảo luận kế hoạch kiểm thử"),
        ("Nghiên cứu", "Nghiên cứu tài liệu kiểm thử phần mềm"),
        ("Văn phòng phẩm", "mua thêm giấy in A4"),
        ("Tài nguyên kiểm thử", "Xem chi tiết tại https://example.com/docs"),
        ("Danh sách công việc", "Checklist công việc cần làm"),
    ]
    
    for title, content in notes:
        create_note_unicode(title, content)

    # Ensure back to HomeScreen
    for _ in range(2):
        xml_str = d.dump_hierarchy()
        if 'Tìm kiếm' in xml_str:
            break
        d.press('back')
        time.sleep(1.0)
        
    d.screenshot('evidence_fn23_unicode_populated.png')
    xml_str = d.dump_hierarchy()
    with open('populated_unicode_hierarchy.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)

    print("📸 Saved evidence_fn23_unicode_populated.png and populated_unicode_hierarchy.xml")

if __name__ == '__main__':
    main()
