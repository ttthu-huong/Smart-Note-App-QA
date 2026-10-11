import sys
import os
import time
import uiautomator2 as u2

sys.stdout.reconfigure(encoding='utf-8')
d = u2.connect('R5CW82ECF6M')

QA_ROOT = r"d:\Workspace\TBDD\Smart-Note-App-QA"
if QA_ROOT not in sys.path:
    sys.path.insert(0, QA_ROOT)

from automation.core.device import SmartNoteDriver

driver = SmartNoteDriver()
driver.ensure_device_ready()
driver.launch_app()
time.sleep(1.0)

test_title = f"AUTO_LIFE_{int(time.time())}"
test_content = "Lifecycle test content"

print(f"1. Creating test note: {test_title}...")
# Tap FAB (964, 2185)
driver.d.click(964, 2185)
time.sleep(1.5)

# Input title
title_field = driver.find_by_text("Tiêu đề") or driver.find_by_text("Title") or driver.d(className="android.widget.EditText")[0]
if title_field:
    title_field.click()
    time.sleep(0.3)
    driver.d.send_keys(test_title)
    time.sleep(0.5)

# Press back to save
driver.d.press("back")
time.sleep(1.5)

# Verify note on HomeScreen
print(f"2. Checking if note {test_title} is on HomeScreen...")
xml = driver.d.dump_hierarchy()
has_note = test_title in xml
print(f"   Note on HomeScreen: {has_note}")
assert has_note, "Note was not created on HomeScreen!"

# Find note element bounds
note_bounds = None
for el in driver.d.xpath(f'//*[contains(@text, "{test_title}") or contains(@content-desc, "{test_title}")]').all():
    note_bounds = el.attrib.get('bounds')
    break

print(f"   Note bounds: {note_bounds}")
import re
m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', note_bounds)
cx = (int(m.group(1)) + int(m.group(3))) // 2
cy = (int(m.group(2)) + int(m.group(4))) // 2

# Test Long click to select
print(f"3. Long clicking note at ({cx}, {cy})...")
driver.d.long_click(cx, cy, duration=1.0)
time.sleep(1.0)

# Inspect Selection Mode AppBar
print("   Inspecting Selection Mode AppBar...")
for el in driver.d.xpath('//*[@text!="" or @content-desc!=""]').all():
    t = el.attrib.get('text', '') or el.attrib.get('content-desc', '')
    b = el.attrib.get('bounds', '')
    if any(k in t for k in ["chọn", "Chuyển", "thùng rác", "Thùng rác", "Ghim", "Đổi màu"]):
        print(f"   Selection bar item: {repr(t)}, bounds={b}")

# Find delete button in selection mode
del_btn = driver.find_by_text("Chuyển vào thùng rác") or driver.d(descriptionContains="thùng rác") or driver.d.xpath('//*[contains(@content-desc, "thùng rác")]')
print(f"   Delete button found: {del_btn is not None}")

# Tap delete
if del_btn:
    del_btn.click()
else:
    # Top right delete icon
    driver.d.click(980, 172)
time.sleep(1.0)

# Check SnackBar
xml_after_del = driver.d.dump_hierarchy()
has_undo = ("Hoàn tác" in xml_after_del) or ("Undo" in xml_after_del)
print(f"4. SnackBar with 'Hoàn tác' present: {has_undo}")

# Tap 'Hoàn tác'
if has_undo:
    undo_btn = driver.find_by_text("Hoàn tác") or driver.find_by_text("Undo")
    if undo_btn:
        undo_btn.click()
        time.sleep(1.0)
        print("   Tapped 'Hoàn tác'! Checking if note returned to Home...")
        print(f"   Note on Home after undo: {test_title in driver.d.dump_hierarchy()}")

print("Diagnostic finished successfully!")
