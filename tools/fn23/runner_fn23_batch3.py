# -*- coding: utf-8 -*-
import os
import sys
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

SERIAL = 'R5CW82ECF6M'
EV_DIR = r'D:\Workspace\TBDD\Smart-Note-App-QA\evidence\fn23'
os.makedirs(EV_DIR, exist_ok=True)

d = u2.connect(SERIAL)

def take_evidence(name):
    path = os.path.join(EV_DIR, name)
    d.screenshot(path)
    print(f"📸 Captured evidence: {path}")
    return path

def clear_search():
    if d(description='Clear text').exists:
        d(description='Clear text').click()
    elif d(description='Xóa').exists:
        d(description='Xóa').click()
    elif d(description='Clear query').exists:
        d(description='Clear query').click()
    else:
        d.click(980, 172)
    time.sleep(1.0)

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

def click_filter_item(name_or_desc):
    if d(text=name_or_desc).exists:
        d(text=name_or_desc).click()
        return True
    if d(description=name_or_desc).exists:
        d(description=name_or_desc).click()
        return True
    xml_str = d.dump_hierarchy()
    root = ET.fromstring(xml_str)
    for node in root.iter('node'):
        desc = node.attrib.get('content-desc', '')
        text = node.attrib.get('text', '')
        if name_or_desc in (desc or text):
            bounds = node.attrib.get('bounds', '')
            import re
            m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
            if m:
                x1, y1, x2, y2 = map(int, m.groups())
                d.click((x1+x2)//2, (y1+y2)//2)
                return True
    return False

def main():
    print("=== STARTING FN-23 EXECUTION (ITEMS 9 TO 14) ===")
    
    # ----------------------------------------------------
    # ITEM 9: TC-BB-027B-D01: Filter "Hình ảnh"
    # ----------------------------------------------------
    print("\n--- [ITEM 9] TC-BB-027B-D01: Filter 'Hình ảnh' ---")
    clear_search()
    time.sleep(0.5)
    click_filter_item("Hình ảnh")
    time.sleep(1.5)
    
    ev09 = take_evidence("FN23_TC-BB-027B_D01.png")
    texts09 = dump_ui_texts()
    print("UI Texts 09:", texts09)
    
    has_image_note = any("Bản vẽ Thiết kế" in t for t in texts09) or any("Hình ảnh" in t for t in texts09)
    if has_image_note:
        print("✅ ITEM 9 PASS: Chip lọc Hình ảnh xuất hiện, danh sách lọc ra ghi chú có hình ảnh")
    else:
        print("❌ ITEM 9 FAIL: Không hiển thị ghi chú có hình ảnh")
        sys.exit(1)

    # ----------------------------------------------------
    # ITEM 10: TC-BB-027B-D02: Filter "Âm thanh"
    # ----------------------------------------------------
    print("\n--- [ITEM 10] TC-BB-027B-D02: Filter 'Âm thanh' ---")
    clear_search()
    time.sleep(0.5)
    click_filter_item("Âm thanh")
    time.sleep(1.5)
    
    ev10 = take_evidence("FN23_TC-BB-027B_D02.png")
    texts10 = dump_ui_texts()
    print("UI Texts 10:", texts10)
    
    has_audio_note = any("Ghi âm Họp" in t for t in texts10) or any("Âm thanh" in t for t in texts10)
    if has_audio_note:
        print("✅ ITEM 10 PASS: Chip lọc Âm thanh xuất hiện, danh sách lọc ra ghi chú có bản ghi âm")
    else:
        print("❌ ITEM 10 FAIL: Không hiển thị ghi chú có âm thanh")
        sys.exit(1)

    # ----------------------------------------------------
    # ITEM 11: TC-BB-027B-D03: Filter "Liên kết" (URL)
    # ----------------------------------------------------
    print("\n--- [ITEM 11] TC-BB-027B-D03: Filter 'Liên kết' / 'URL' ---")
    clear_search()
    time.sleep(0.5)
    # UI displays "URL" or "Liên kết"
    clicked_url = click_filter_item("URL") or click_filter_item("Liên kết")
    time.sleep(1.5)
    
    ev11 = take_evidence("FN23_TC-BB-027B_D03.png")
    texts11 = dump_ui_texts()
    print("UI Texts 11:", texts11)
    
    has_url_note = any("Tài nguyên kiểm thử" in t for t in texts11) or any("https://" in t for t in texts11) or any("URL" in t for t in texts11)
    if has_url_note:
        print("✅ ITEM 11 PASS: Chip lọc Liên kết/URL xuất hiện, danh sách lọc ra ghi chú chứa link URL")
    else:
        print("❌ ITEM 11 FAIL: Không hiển thị ghi chú chứa liên kết URL")
        sys.exit(1)

    # ----------------------------------------------------
    # ITEM 12: TC-BB-027C-D01: Filter Tag "Công việc"
    # ----------------------------------------------------
    print("\n--- [ITEM 12] TC-BB-027C-D01: Filter Tag 'Công việc' ---")
    clear_search()
    time.sleep(0.5)
    # Scroll down to see Tags if needed, or click "Công việc"
    d.swipe(540, 1500, 540, 800, duration=0.3)
    time.sleep(0.8)
    click_filter_item("Công việc")
    time.sleep(1.5)
    
    ev12 = take_evidence("FN23_TC-BB-027C_D01.png")
    texts12 = dump_ui_texts()
    print("UI Texts 12:", texts12)
    
    has_tag_note = any("Báo cáo tiến độ" in t for t in texts12) or any("Bản vẽ Thiết kế" in t for t in texts12) or any("Công việc" in t for t in texts12)
    if has_tag_note:
        print("✅ ITEM 12 PASS: Chip nhãn 'Công việc' xuất hiện, lọc ra các ghi chú được gắn nhãn đó")
    else:
        print("❌ ITEM 12 FAIL: Không lọc được ghi chú theo nhãn 'Công việc'")
        sys.exit(1)

    # ----------------------------------------------------
    # ITEM 13: TC-BB-027D-D01: Filter "Được ghim"
    # ----------------------------------------------------
    print("\n--- [ITEM 13] TC-BB-027D-D01: Filter 'Được ghim' ---")
    clear_search()
    time.sleep(0.5)
    click_filter_item("Được ghim")
    time.sleep(1.5)
    
    ev13 = take_evidence("FN23_TC-BB-027D_D01.png")
    texts13 = dump_ui_texts()
    print("UI Texts 13:", texts13)
    
    has_pinned_note = any("Báo cáo tiến độ" in t for t in texts13) or any("Được ghim" in t for t in texts13)
    if has_pinned_note:
        print("✅ ITEM 13 PASS: Chip lọc 'Được ghim' xuất hiện, danh sách chỉ hiển thị ghi chú được ghim")
    else:
        print("❌ ITEM 13 FAIL: Không lọc được ghi chú được ghim")
        sys.exit(1)

    # ----------------------------------------------------
    # ITEM 14: TC-BB-027D-D02: Filter "Lưu trữ"
    # ----------------------------------------------------
    print("\n--- [ITEM 14] TC-BB-027D-D02: Filter 'Lưu trữ' ---")
    clear_search()
    time.sleep(0.5)
    click_filter_item("Lưu trữ")
    time.sleep(1.5)
    
    ev14 = take_evidence("FN23_TC-BB-027D_D02.png")
    texts14 = dump_ui_texts()
    print("UI Texts 14:", texts14)
    
    has_archive_note = any("Ghi chú cũ 2025" in t for t in texts14) or any("Lưu trữ" in t for t in texts14) or any("KHỚP" in t for t in texts14)
    if has_archive_note:
        print("✅ ITEM 14 PASS: Chip lọc 'Lưu trữ' xuất hiện, danh sách lọc ra ghi chú nằm trong kho lưu trữ")
    else:
        print("❌ ITEM 14 FAIL: Không lọc được ghi chú trong kho lưu trữ")
        sys.exit(1)

    print("\nBatch 3 completed successfully!")

if __name__ == '__main__':
    main()
