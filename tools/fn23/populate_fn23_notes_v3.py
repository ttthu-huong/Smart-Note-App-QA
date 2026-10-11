# -*- coding: utf-8 -*-
"""
Script v3 nạp Dữ liệu Tiền điều kiện cho FN-23 không dùng FastInputIME.
"""
import sys
import time
import subprocess
import uiautomator2 as u2
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

SERIAL = 'R5CW82ECF6M'
d = u2.connect(SERIAL)

def input_text_adb(text):
    if not text:
        return
    # Use adb shell input text with escaped space %s
    escaped = text.replace(' ', '%s')
    subprocess.run(['adb', '-s', SERIAL, 'shell', 'input', 'text', escaped], capture_output=True)
    time.sleep(0.3)

def create_note(title, content):
    print(f"  --> Creating note: '{title}'...")
    # Click (+) button (bounds ~ 936, 2012)
    d.click(936, 2012)
    time.sleep(1.5)
    
    # Title
    if title:
        d.click(350, 320)
        time.sleep(0.3)
        input_text_adb(title)
        
    # Content
    if content:
        d.click(350, 650)
        time.sleep(0.3)
        input_text_adb(content)

    # Press Back (<-) button
    d.press('back')
    time.sleep(1.2)

def main():
    print("=== POPULATING FN-23 PRECONDITIONS (V3) ===")
    notes = [
        ("Bao_cao_tien_do", "Cap_nhat_tien_do_du_an_QA"),
        ("Hop_nhom", "Thao_luan_Hop_Tuan_kiem_thu"),
        ("Nghien_cuu", "Nghien_cuu_tai_lieu_kiem_thu_phan_mem"),
        ("Nghiên_cứu_tài_liệu_kiểm_thử", "Nội_dung_nghiên_cứu_tiếng_Việt_có_dấu"),
        ("Van_phong_pham", "mua_them_giay_in_A4"),
        ("Tai_nguyen", "Xem_chi_tiet_tai_https://example.com/docs"),
        ("Danh_sach_cong_viec", "Checklist_cong_viec_can_lam"),
    ]
    
    for title, content in notes:
        create_note(title, content)
        
    d.screenshot('evidence_fn23_preconditions_v3.png')
    xml_str = d.dump_hierarchy()
    with open('populated_hierarchy_v3.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)
        
    print("📸 Saved evidence_fn23_preconditions_v3.png")

if __name__ == '__main__':
    main()
