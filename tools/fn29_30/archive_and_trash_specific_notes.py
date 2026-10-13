# -*- coding: utf-8 -*-
import sys
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
d = u2.connect('R5CW82ECF6M')
PKG = 'com.example.smart_note_app'

def ensure_home():
    for _ in range(4):
        xml_str = d.dump_hierarchy()
        if 'Tìm kiếm' in xml_str or 'Tất cả ghi chú' in xml_str:
            return True
        d.press('back')
        time.sleep(1.0)
    return False

def archive_note_by_title(target_title):
    print(f"\n--- Archiving Note: {target_title!r} ---")
    ensure_home()
    if d(textContains=target_title).exists:
        d(textContains=target_title).click()
    elif d(descriptionContains=target_title).exists:
        d(descriptionContains=target_title).click()
    else:
        print(f"Note {target_title!r} not found on screen!")
        return False
    time.sleep(1.5)
    
    # Click More (...) bottom right (1006, 2196)
    d.click(1006, 2196)
    time.sleep(1.0)
    # Click 'Lưu trữ' at bounds [0,2133][1080,2280] -> center (540, 2200)
    d.click(540, 2200)
    time.sleep(1.5)
    ensure_home()
    print(f"✅ Archived {target_title!r}!")

def trash_note_by_title(target_title):
    print(f"\n--- Trashing Note: {target_title!r} ---")
    ensure_home()
    if d(textContains=target_title).exists:
        d(textContains=target_title).click()
    elif d(descriptionContains=target_title).exists:
        d(descriptionContains=target_title).click()
    else:
        print(f"Note {target_title!r} not found on screen!")
        return False
    time.sleep(1.5)
    
    # Click More (...) bottom right (1006, 2196)
    d.click(1006, 2196)
    time.sleep(1.0)
    # Click 'Xóa ghi chú' at bounds [0,1692][1080,1839] -> center (540, 1765)
    d.click(540, 1765)
    time.sleep(1.5)
    ensure_home()
    print(f"✅ Trashed {target_title!r}!")

def main():
    archive_note_by_title("Ghi chú lưu trữ FN23")
    archive_note_by_title("Ghi chú cũ 2025")
    trash_note_by_title("Tài liệu mật")

if __name__ == '__main__':
    main()
