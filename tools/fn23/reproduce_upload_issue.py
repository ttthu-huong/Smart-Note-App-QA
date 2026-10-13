# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import uiautomator2 as u2
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

SERIAL = 'R5CW82ECF6M'
d = u2.connect(SERIAL)

print("1. Clearing logcat...")
subprocess.run(['adb', '-s', SERIAL, 'logcat', '-c'])

print("2. Starting background logcat capture...")
log_proc = subprocess.Popen(
    ['adb', '-s', SERIAL, 'logcat', '-v', 'time'],
    stdout=open('reproduce_logcat.txt', 'w', encoding='utf-8', errors='replace'),
    stderr=subprocess.DEVNULL
)

try:
    print("3. Clicking 'Thêm hình ảnh'...")
    if d(description='Thêm hình ảnh').exists:
        d(description='Thêm hình ảnh').click()
    elif d(text='Thêm hình ảnh').exists:
        d(text='Thêm hình ảnh').click()
    else:
        # Click by bounds from earlier screenshot: around (300, 1750)
        d.click(300, 1750)
    time.sleep(1.0)
    
    print("4. Clicking 'Chọn từ thư viện' / Gallery...")
    d.screenshot('choose_source.png')
    root = ET.fromstring(d.dump_hierarchy())
    clicked_gallery = False
    for n in root.iter('node'):
        desc = n.attrib.get('content-desc', '')
        text = n.attrib.get('text', '')
        val = desc or text
        if any(k in val.lower() for k in ['thư viện', 'gallery', 'ảnh']):
            bounds = n.attrib.get('bounds', '')
            import re
            m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
            if m:
                x1, y1, x2, y2 = map(int, m.groups())
                d.click((x1+x2)//2, (y1+y2)//2)
                clicked_gallery = True
                print(f"Clicked gallery option: {val} at bounds {bounds}")
                break
    if not clicked_gallery:
        # Fallback click
        d.click(400, 2050)
    
    time.sleep(2.0)
    print("5. In Android Photo Picker...")
    d.screenshot('photo_picker.png')
    
    # Pick first photo: usually around (180, 500) or similar
    root2 = ET.fromstring(d.dump_hierarchy())
    picked_photo = False
    for n in root2.iter('node'):
        cls = n.attrib.get('class', '')
        desc = n.attrib.get('content-desc', '')
        text = n.attrib.get('text', '')
        if 'ImageView' in cls or 'Photo' in desc or 'Ảnh' in desc:
            bounds = n.attrib.get('bounds', '')
            import re
            m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
            if m:
                x1, y1, x2, y2 = map(int, m.groups())
                if y1 > 300: # not header
                    d.click((x1+x2)//2, (y1+y2)//2)
                    picked_photo = True
                    print(f"Clicked photo at bounds {bounds}")
                    break
    if not picked_photo:
        print("Tapping default photo coordinates (180, 500)...")
        d.click(180, 500)
        
    print("6. Waiting for upload behavior (8 seconds)...")
    time.sleep(3.0)
    d.screenshot('upload_progress_3s.png')
    time.sleep(5.0)
    d.screenshot('upload_progress_8s.png')
    print("Screenshots taken.")

finally:
    print("7. Terminating logcat capture...")
    log_proc.terminate()
    log_proc.wait()

print("Reproduce script finished.")
