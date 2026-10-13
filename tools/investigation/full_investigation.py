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

print("Starting full upload investigation...")

# 1. Start logcat
log_file = open("full_investigation_logcat.txt", "w", encoding="utf-8", errors="replace")
log_proc = subprocess.Popen(
    ['adb', '-s', SERIAL, 'logcat', '-v', 'time'],
    stdout=log_file,
    stderr=subprocess.DEVNULL
)

try:
    # 2. Tap [+]
    print("Clicking [+] button...")
    d(description='Thêm').click()
    time.sleep(1.0)
    
    # 3. Tap Thêm hình ảnh
    print("Clicking 'Thêm hình ảnh'...")
    if d(description='Thêm hình ảnh').exists:
        d(description='Thêm hình ảnh').click()
    elif d(text='Thêm hình ảnh').exists:
        d(text='Thêm hình ảnh').click()
    else:
        d.click(300, 1750)
    time.sleep(1.0)
    
    # 4. Tap Chọn từ thư viện
    print("Clicking 'Chọn từ thư viện'...")
    d(text='Chọn từ thư viện').click()
    time.sleep(2.0)
    
    # 5. In photo picker, select a photo
    print("Selecting photo...")
    d.click(180, 500)
    time.sleep(1.0)
    if d(text='Xong').exists:
        print("Clicking 'Xong'...")
        d(text='Xong').click()
    else:
        d.click(830, 2120)
        
    print("6. Photo confirmed! Now monitoring UI and network every second...")
    start_time = time.time()
    
    for sec in range(1, 91):
        time.sleep(1.0)
        elapsed = int(time.time() - start_time)
        
        # Check UI hierarchy for spinner or image
        xml_str = d.dump_hierarchy()
        has_spinner = 'ProgressBar' in xml_str or 'CircularProgressIndicator' in xml_str or 'đang tải' in xml_str.lower()
        has_broken = 'broken_image' in xml_str
        
        # Check network connections of app
        net_out = subprocess.run(
            ['adb', '-s', SERIAL, 'shell', 'netstat -n -p 2>/dev/null || ss -t -p 2>/dev/null'],
            stdout=subprocess.PIPE,
            text=True
        ).stdout
        cloudinary_net = [line for line in net_out.splitlines() if '443' in line or 'cloudinary' in line]
        
        print(f"[{elapsed:02d}s] Spinner: {has_spinner} | Broken: {has_broken} | Net lines: {len(cloudinary_net)}")
        if cloudinary_net:
            for nl in cloudinary_net[:2]:
                print(f"       -> {nl.strip()}")
                
        # Take periodic screenshots
        if sec in [3, 10, 20, 30, 45, 60]:
            d.screenshot(f"investigate_{sec}s.png")
            
        # Check if snackbar appeared
        if 'SnackBar' in xml_str or 'Lỗi' in xml_str or 'không thể' in xml_str.lower() or 'upload' in xml_str.lower():
            print(f"[{elapsed:02d}s] ⚠️ Notice/Error detected on UI!")
            d.screenshot(f"investigate_notice_{sec}s.png")
            
        # If spinner stopped and it's been at least 15s, check result
        if not has_spinner and sec > 10:
            print(f"[{elapsed:02d}s] Spinner is NO LONGER visible!")
            d.screenshot(f"investigate_final_{sec}s.png")
            break

finally:
    print("Terminating logcat capture...")
    log_proc.terminate()
    log_proc.wait()
    log_file.close()

print("Full investigation script completed.")
