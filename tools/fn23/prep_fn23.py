import sys
import time
import uiautomator2 as u2

sys.stdout.reconfigure(encoding='utf-8')

d = u2.connect('R5CW82ECF6M')

def create_note(title, body):
    print(f"Creating note: {title}...")
    # Click FAB (+) at (960, 2180)
    d.click(960, 2180)
    time.sleep(1.5)
    
    # Enter title at (300, 360)
    d.click(300, 360)
    time.sleep(0.5)
    d.send_keys(title)
    time.sleep(0.5)
    
    # Enter body at (300, 500)
    d.click(300, 500)
    time.sleep(0.5)
    d.send_keys(body)
    time.sleep(0.5)
    
    # Click back arrow at (74, 160) to auto-save and exit
    d.click(74, 160)
    time.sleep(1.5)

# Create Note 1
create_note("Kế hoạch", "Kế hoạch công việc tuần mới")

# Create Note 2
create_note("Tạp vụ", "mua thêm giấy in A4")

print("Preconditions ready! Checking Home:")
for el in d.xpath('//*').all():
    txt = el.attrib.get('text', '') or el.attrib.get('content-desc', '')
    bounds = el.attrib.get('bounds', '')
    if txt in ['Kế hoạch', 'Tạp vụ', 'Quay video tiếng anh', 'Ta3']:
        print(f"{bounds}: {txt}")
