# -*- coding: utf-8 -*-
import sys
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
SERIAL = 'R5CW82ECF6M'
PKG = 'com.example.smart_note_app'
d = u2.connect(SERIAL)

def ensure_home_screen():
    # Make sure we are at HomeScreen
    d.app_start(PKG, use_monkey=False)
    time.sleep(2.0)
    xml_str = d.dump_hierarchy()
    if 'Tìm kiếm' not in xml_str and 'Tất cả ghi chú' not in xml_str:
        d.press('back')
        time.sleep(1.0)

def create_note(title, content, pin=False, tag=None, archive=False, trash=False):
    print(f"\n--- Creating Note: '{title}' ---")
    ensure_home_screen()
    
    # 1. Click FAB (+) at (964, 2185)
    d.click(964, 2185)
    time.sleep(1.5)
    
    # 2. Set Title (540, 350)
    d.click(540, 350)
    time.sleep(0.3)
    if title:
        d.send_keys(title)
        time.sleep(0.3)
        
    # 3. Set Content (540, 650)
    if content:
        d.click(540, 650)
        time.sleep(0.3)
        d.send_keys(content)
        time.sleep(0.3)
        
    if pin:
        print("  -> Pinning note...")
        # AppBar Pin icon at bounds [807,120][933,225] -> center (870, 172)
        d.click(870, 172)
        time.sleep(0.5)

    if tag:
        print(f"  -> Adding Tag '{tag}'...")
        # Click More (...) at bottom right (1006, 2196)
        d.click(1006, 2196)
        time.sleep(0.8)
        # Click 'Nhãn' item at bounds [0,1839][1080,1986] -> center (540, 1912)
        d.click(540, 1912)
        time.sleep(1.0)
        
        # Check if tag already exists in list or create new
        if d(text=tag).exists:
            d(text=tag).click()
            time.sleep(0.4)
        else:
            if d(text='Tạo nhãn mới').exists:
                d(text='Tạo nhãn mới').click()
                time.sleep(0.5)
                d.send_keys(tag)
                time.sleep(0.4)
                if d(text='Lưu').exists:
                    d(text='Lưu').click()
                    time.sleep(0.4)
                elif d(text='OK').exists:
                    d(text='OK').click()
                    time.sleep(0.4)
        time.sleep(0.5)
        d.press('back')
        time.sleep(0.5)

    if archive:
        print("  -> Archiving note...")
        # Click More (...) at bottom right (1006, 2196)
        d.click(1006, 2196)
        time.sleep(0.8)
        # Click 'Lưu trữ' at bounds [0,2133][1080,2280] -> center (540, 2200)
        d.click(540, 2200)
        time.sleep(1.5)
        return

    if trash:
        print("  -> Moving note to Trash...")
        # Click More (...) at bottom right (1006, 2196)
        d.click(1006, 2196)
        time.sleep(0.8)
        # Click 'Xóa ghi chú' at bounds [0,1692][1080,1839] -> center (540, 1765)
        d.click(540, 1765)
        time.sleep(1.5)
        return

    # Exit editor to save and return to HomeScreen
    d.click(70, 170)
    time.sleep(1.5)

def main():
    print("=== POPULATING ALL REQUIRED FN-23 PRECONDITION NOTES ===")
    
    # 1. Text Note titled "Báo cáo" (TC-BB-026 D01) -> Pinned (TC-BB-027D D01) & Tagged "Công việc" (TC-BB-027C D01)
    create_note("Báo cáo tiến độ", "Báo cáo tiến độ kiểm thử tự động FN-23", pin=True, tag="Công việc")

    # 2. Text Note containing "Thiết kế" (TC-BB-027E D01)
    create_note("Bản vẽ Thiết kế", "Tài liệu mô tả bản vẽ thiết kế hệ thống UI", tag="Công việc")

    # 3. Note in Trash containing "Tài liệu mật" (TC-BB-028B D01)
    create_note("Tài liệu mật", "Thông tin kiểm thử bảo mật không được tiết lộ", trash=True)

    # 4. Note in Archive (TC-BB-027D D02)
    create_note("Ghi chú cũ 2025", "Lưu trữ tài liệu dự án năm ngoái", archive=True)

    # 5. Checklist Note "Danh sách mua sắm" (TC-BB-027G D01)
    create_note("Danh sách công việc", "1. Kiểm thử FN-23\n2. Báo cáo kết quả\n3. Họp review")

    ensure_home_screen()
    d.screenshot('evidence_fn23_preconditions_populated.png')
    xml_str = d.dump_hierarchy()
    with open('populated_hierarchy_v3.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)
        
    print("\n✅ Precondition population completed successfully!")

if __name__ == '__main__':
    main()
