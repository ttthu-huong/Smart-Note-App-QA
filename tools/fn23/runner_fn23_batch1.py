# -*- coding: utf-8 -*-
import os
import sys
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

SERIAL = 'R5CW82ECF6M'
PKG = 'com.example.smart_note_app'
EV_DIR = r'D:\Workspace\TBDD\Smart-Note-App-QA\evidence\fn23'
os.makedirs(EV_DIR, exist_ok=True)

d = u2.connect(SERIAL)

def ensure_home():
    for _ in range(4):
        xml_str = d.dump_hierarchy()
        if 'Tìm kiếm' in xml_str or 'Tất cả ghi chú' in xml_str:
            return True
        d.press('back')
        time.sleep(1.0)
    return False

def take_evidence(name):
    path = os.path.join(EV_DIR, name)
    d.screenshot(path)
    print(f"📸 Captured evidence: {path}")
    return path

def open_search():
    ensure_home()
    # Click search bar
    d.click(540, 172)
    time.sleep(1.2)

def clear_search():
    # If clear button exists, tap it
    if d(description='Clear text').exists:
        d(description='Clear text').click()
    elif d(description='Xóa').exists:
        d(description='Xóa').click()
    elif d(description='Clear query').exists:
        d(description='Clear query').click()
    else:
        # Click search text area and clear
        d.click(540, 172)
        time.sleep(0.3)
        d.clear_text()
    time.sleep(0.8)

def dump_ui_texts():
    xml_str = d.dump_hierarchy()
    root = ET.fromstring(xml_str)
    items = []
    for node in root.iter('node'):
        desc = node.attrib.get('content-desc', '')
        text = node.attrib.get('text', '')
        val = (desc or text).strip()
        if val and not any(k in val for k in ['Wi-Fi', 'pin', '19:', 'Chuông', 'Thông báo', 'Bảng ở cạnh', ', 3 vạch.']):
            items.append(val)
    return items

def main():
    print("=== STARTING FN-23 EXECUTION (ITEMS 1 TO 4) ===")
    open_search()
    
    # ----------------------------------------------------
    # ITEM 1: TC-BB-026-D01: Search "Báo cáo" in Title
    # ----------------------------------------------------
    print("\n--- [ITEM 1] TC-BB-026-D01: Search 'Báo cáo' ---")
    clear_search()
    d.click(540, 172)
    time.sleep(0.3)
    d.send_keys("Báo cáo")
    time.sleep(1.5)
    
    ev01 = take_evidence("FN23_TC-BB-026_D01.png")
    texts01 = dump_ui_texts()
    print("UI Texts 01:", texts01)
    
    has_bao_cao = any("Báo cáo" in t for t in texts01)
    if has_bao_cao:
        print("✅ ITEM 1 PASS: Trả về thẻ ghi chú có Tiêu đề chứa 'Báo cáo'")
    else:
        print("❌ ITEM 1 FAIL: Không tìm thấy ghi chú 'Báo cáo'")
        sys.exit(1)
        
    # ----------------------------------------------------
    # ITEM 2: TC-BB-026B-D01: Search lowercase "nghiên cứu"
    # ----------------------------------------------------
    print("\n--- [ITEM 2] TC-BB-026B-D01: Search lowercase 'nghiên cứu' ---")
    clear_search()
    d.click(540, 172)
    time.sleep(0.3)
    d.send_keys("nghiên cứu")
    time.sleep(1.5)
    
    ev02 = take_evidence("FN23_TC-BB-026B_D01.png")
    texts02 = dump_ui_texts()
    print("UI Texts 02:", texts02)
    
    has_nghien_cuu = any("Nghiên cứu" in t for t in texts02)
    if has_nghien_cuu:
        print("✅ ITEM 2 PASS: Hiển thị chính xác ghi chú 'Nghiên cứu'")
    else:
        print("❌ ITEM 2 FAIL: Không tìm thấy ghi chú 'Nghiên cứu'")
        sys.exit(1)

    # ----------------------------------------------------
    # ITEM 3: TC-BB-026B-D02: Search uppercase "NGHIÊN CỨU"
    # ----------------------------------------------------
    print("\n--- [ITEM 3] TC-BB-026B-D02: Search uppercase 'NGHIÊN CỨU' ---")
    clear_search()
    d.click(540, 172)
    time.sleep(0.3)
    d.send_keys("NGHIÊN CỨU")
    time.sleep(1.5)
    
    ev03 = take_evidence("FN23_TC-BB-026B_D02.png")
    texts03 = dump_ui_texts()
    print("UI Texts 03:", texts03)
    
    has_upper = any("Nghiên cứu" in t for t in texts03)
    if has_upper:
        print("✅ ITEM 3 PASS: Trả về đúng ghi chú 'Nghiên cứu' với từ khóa chữ HOA có dấu")
    else:
        print("❌ ITEM 3 FAIL: Không tìm thấy ghi chú 'Nghiên cứu' với từ khóa chữ HOA")
        sys.exit(1)

    # ----------------------------------------------------
    # ITEM 4: TC-BB-026B-D03: Search unaccented "nghien cuu"
    # ----------------------------------------------------
    print("\n--- [ITEM 4] TC-BB-026B-D03: Search unaccented 'nghien cuu' ---")
    clear_search()
    d.click(540, 172)
    time.sleep(0.3)
    d.send_keys("nghien cuu")
    time.sleep(1.5)
    
    ev04 = take_evidence("FN23_TC-BB-026B_D03.png")
    texts04 = dump_ui_texts()
    print("UI Texts 04:", texts04)
    
    has_unaccented = any("Nghiên cứu" in t for t in texts04)
    print(f"Observation for unaccented search: found={has_unaccented}")
    # Note: TC-BB-026B D03 Expected Result says:
    # "Xác minh thực tế trên thiết bị: Quan sát xem ứng dụng có tìm được ghi chú 'Nghiên cứu' khi nhập 'nghien cuu' hay không (không mặc định PASS, ghi nhận đúng hành vi thực tế của engine)."
    
    print("\nBatch 1 completed successfully!")

if __name__ == '__main__':
    main()
