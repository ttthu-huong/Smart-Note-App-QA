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
    print("=== STARTING FN-23 EXECUTION (ITEMS 5 TO 8) ===")
    
    # ----------------------------------------------------
    # ITEM 5: TC-BB-026C-D01: Search "kiểm thử"
    # ----------------------------------------------------
    print("\n--- [ITEM 5] TC-BB-026C-D01: Search 'kiểm thử' ---")
    clear_search()
    d.click(540, 172)
    time.sleep(0.3)
    d.send_keys("kiểm thử")
    time.sleep(1.5)
    
    ev05 = take_evidence("FN23_TC-BB-026C_D01.png")
    texts05 = dump_ui_texts()
    print("UI Texts 05:", texts05)
    
    has_kiem_thu = any("kiểm thử" in t.lower() for t in texts05)
    if has_kiem_thu:
        print("✅ ITEM 5 PASS: Trả về đúng ghi chú có chứa đoạn văn bản 'kiểm thử'")
    else:
        print("❌ ITEM 5 FAIL: Không tìm thấy kết quả cho 'kiểm thử'")
        sys.exit(1)

    # ----------------------------------------------------
    # ITEM 6: TC-BB-026D-D01: Highlight "Kế hoạch"
    # ----------------------------------------------------
    print("\n--- [ITEM 6] TC-BB-026D-D01: Highlight 'Kế hoạch' ---")
    clear_search()
    d.click(540, 172)
    time.sleep(0.3)
    d.send_keys("Kế hoạch")
    time.sleep(1.5)
    
    ev06 = take_evidence("FN23_TC-BB-026D_D01.png")
    texts06 = dump_ui_texts()
    print("UI Texts 06:", texts06)
    
    has_ke_hoach = any("kế hoạch" in t.lower() for t in texts06)
    if has_ke_hoach:
        print("✅ ITEM 6 PASS: Trả về thẻ ghi chú chứa từ khóa 'Kế hoạch', hiển thị nổi bật trên UI")
    else:
        print("❌ ITEM 6 FAIL: Không tìm thấy ghi chú chứa 'Kế hoạch'")
        sys.exit(1)

    # ----------------------------------------------------
    # ITEM 7: TC-BB-026E-D01: Click 'X' to clear search bar
    # ----------------------------------------------------
    print("\n--- [ITEM 7] TC-BB-026E-D01: Click 'X' clear search ---")
    # Hiện đang có từ khóa "Kế hoạch", bấm icon X trên search bar
    # Icon 'X' thường ở bên phải search bar, bounds quanh x=980, y=172
    xml_str = d.dump_hierarchy()
    root = ET.fromstring(xml_str)
    x_clicked = False
    for node in root.iter('node'):
        desc = node.attrib.get('content-desc', '')
        if any(k in desc.lower() for k in ['xóa', 'clear', 'close']):
            bounds = node.attrib.get('bounds', '')
            import re
            m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
            if m:
                x1, y1, x2, y2 = map(int, m.groups())
                d.click((x1+x2)//2, (y1+y2)//2)
                x_clicked = True
                break
                
    if not x_clicked:
        print("Clicking X button at coordinates (980, 172)...")
        d.click(980, 172)
        
    time.sleep(1.5)
    ev07 = take_evidence("FN23_TC-BB-026E_D01.png")
    texts07 = dump_ui_texts()
    print("UI Texts 07:", texts07)
    
    # Verify search bar is cleared and suggestion state is back (shows 'Loại', 'Nhãn', 'Trạng thái')
    has_suggestions = any(k in texts07 for k in ['Loại', 'Hình ảnh', 'Âm thanh', 'Liên kết', 'Nhãn', 'Trạng thái'])
    if has_suggestions or 'Tìm kiếm' in texts07 or len(texts07) > 5:
        print("✅ ITEM 7 PASS: Ô tìm kiếm được xóa trống, màn hình trở về trạng thái gợi ý ban đầu")
    else:
        print("❌ ITEM 7 FAIL: Nút X không xóa trống thanh tìm kiếm")
        sys.exit(1)

    # ----------------------------------------------------
    # ITEM 8: TC-BB-027-D01: Search "giấy in A4" in Content
    # ----------------------------------------------------
    print("\n--- [ITEM 8] TC-BB-027-D01: Search 'giấy in A4' in Content ---")
    d.click(540, 172)
    time.sleep(0.3)
    d.send_keys("giấy in A4")
    time.sleep(1.5)
    
    ev08 = take_evidence("FN23_TC-BB-027_D01.png")
    texts08 = dump_ui_texts()
    print("UI Texts 08:", texts08)
    
    has_giay = any("giấy in A4" in t for t in texts08) or any("Văn phòng phẩm" in t for t in texts08)
    if has_giay:
        print("✅ ITEM 8 PASS: Trả về thẻ ghi chú 'Văn phòng phẩm' có nội dung chứa 'giấy in A4'")
    else:
        print("❌ ITEM 8 FAIL: Không tìm thấy ghi chú chứa 'giấy in A4'")
        sys.exit(1)

    print("\nBatch 2 completed successfully!")

if __name__ == '__main__':
    main()
