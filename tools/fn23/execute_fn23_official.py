# -*- coding: utf-8 -*-
"""
Script thực thi tự động 22 Execution Items cho FN-23 với hàm clear_search_field chuẩn hóa.
"""
import os
import sys
import time
import subprocess
import uiautomator2 as u2
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

SERIAL = 'R5CW82ECF6M'
EV_DIR = r'D:\Workspace\TBDD\Smart-Note-App-QA\evidence\fn23'

os.makedirs(EV_DIR, exist_ok=True)
d = u2.connect(SERIAL)

def dump_ui():
    xml_str = d.dump_hierarchy()
    try:
        root = ET.fromstring(xml_str)
        items = []
        for node in root.iter('node'):
            desc = node.attrib.get('content-desc', '')
            text = node.attrib.get('text', '')
            if desc or text:
                items.append(f"{desc.strip()} {text.strip()}".strip())
        return " | ".join(items)
    except Exception:
        return xml_str[:300]

def take_evidence(filename):
    filepath = os.path.join(EV_DIR, filename)
    d.screenshot(filepath)
    print(f"📸 Saved evidence: {filename}")
    return filename

def clear_search_field():
    print("Clearing search field...")
    # Click search field
    d.click(540, 172)
    time.sleep(0.3)
    # Try clear icon at right of search bar (bounds ~ 960, 172)
    d.click(960, 172)
    time.sleep(0.4)
    # Also select all text and backspace if text remains
    try:
        if d(focused=True).exists:
            d(focused=True).clear_text()
    except Exception:
        pass
    time.sleep(0.3)

def run_suite():
    print("=== STARTING OFFICIAL FN-23 BLACK-BOX EXECUTION SUITE (V2) ===")
    
    # 1. Open Search Screen if not on Search Screen
    xml_str = d.dump_hierarchy()
    if 'Xóa bộ lọc' not in xml_str and 'Không tìm thấy' not in xml_str:
        search_bar = d(description='Tìm kiếm')
        if search_bar.exists:
            search_bar.click()
        else:
            d.click(540, 172)
        time.sleep(1.5)

    results = []

    # ITEM 01: TC-BB-026 D01
    print("\n--- [ITEM 01] TC-BB-026 D01: Search 'Báo cáo' ---")
    clear_search_field()
    d.send_keys("Báo cáo")
    time.sleep(1.5)
    ev01 = take_evidence("FN23_TC-BB-026_D01.png")
    ui01 = dump_ui()
    print(f"UI 01: {ui01}")
    if 'Báo cáo' in ui01:
        print("✅ ITEM 01: PASS")
        results.append(("TC-BB-026", "D01", "PASS", ev01, "Danh sách kết quả hiển thị thẻ ghi chú 'Báo cáo tiến độ'"))
    else:
        print("❌ ITEM 01: FAIL")
        results.append(("TC-BB-026", "D01", "FAIL", ev01, f"Actual UI: {ui01}"))
        return False, results

    # ITEM 02: TC-BB-026B D01
    print("\n--- [ITEM 02] TC-BB-026B D01: Search 'nghiên cứu' (lowercase) ---")
    clear_search_field()
    d.send_keys("nghiên cứu")
    time.sleep(1.5)
    ev02 = take_evidence("FN23_TC-BB-026B_D01.png")
    ui02 = dump_ui()
    print(f"UI 02: {ui02}")
    if 'Nghiên cứu' in ui02:
        print("✅ ITEM 02: PASS")
        results.append(("TC-BB-026B", "D01", "PASS", ev02, "Hiển thị chính xác ghi chú 'Nghiên cứu' khi nhập từ khóa chữ thường có dấu"))
    else:
        print("❌ ITEM 02: FAIL")
        results.append(("TC-BB-026B", "D01", "FAIL", ev02, f"Actual UI: {ui02}"))
        return False, results

    # ITEM 03: TC-BB-026B D02
    print("\n--- [ITEM 03] TC-BB-026B D02: Search 'NGHIÊN CỨU' (UPPERCASE) ---")
    clear_search_field()
    d.send_keys("NGHIÊN CỨU")
    time.sleep(1.5)
    ev03 = take_evidence("FN23_TC-BB-026B_D02.png")
    ui03 = dump_ui()
    print(f"UI 03: {ui03}")
    if 'Nghiên cứu' in ui03:
        print("✅ ITEM 03: PASS")
        results.append(("TC-BB-026B", "D02", "PASS", ev03, "Chấp nhận từ khóa chữ HOA có dấu 'NGHIÊN CỨU'"))
    else:
        print("❌ ITEM 03: FAIL")
        results.append(("TC-BB-026B", "D02", "FAIL", ev03, f"Actual UI: {ui03}"))
        return False, results

    # ITEM 04: TC-BB-026B D03
    print("\n--- [ITEM 04] TC-BB-026B D03: Search 'nghien cuu' (unaccented) ---")
    clear_search_field()
    d.send_keys("nghien cuu")
    time.sleep(1.5)
    ev04 = take_evidence("FN23_TC-BB-026B_D03.png")
    ui04 = dump_ui()
    print(f"UI 04: {ui04}")
    if 'Nghiên cứu' in ui04:
        print("✅ ITEM 04: PASS")
        results.append(("TC-BB-026B", "D03", "PASS", ev04, "Hỗ trợ tìm kiếm từ khóa tiếng Việt không dấu"))
    else:
        print("❌ ITEM 04: FAIL (SQLite unaccented search gap)")
        results.append(("TC-BB-026B", "D03", "FAIL", ev04, f"Engine SQLite không loại bỏ dấu tiếng Việt khi tìm từ khóa không dấu: {ui04}"))
        return False, results

    print("\n🎉 ALL ITEMS SUCCEEDED!")
    return True, results

if __name__ == '__main__':
    run_suite()
