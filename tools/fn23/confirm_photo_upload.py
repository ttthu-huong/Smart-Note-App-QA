# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import uiautomator2 as u2

sys.stdout.reconfigure(encoding='utf-8')

SERIAL = 'R5CW82ECF6M'
d = u2.connect(SERIAL)

print("1. Clearing logcat...")
subprocess.run(['adb', '-s', SERIAL, 'logcat', '-c'])

print("2. Starting background logcat capture...")
log_proc = subprocess.Popen(
    ['adb', '-s', SERIAL, 'logcat', '-v', 'time'],
    stdout=open('upload_realtime_logcat.txt', 'w', encoding='utf-8', errors='replace'),
    stderr=subprocess.DEVNULL
)

try:
    print("3. Clicking 'Xong' button in Photo Picker...")
    if d(text='Xong').exists:
        d(text='Xong').click()
    else:
        d.click(830, 2120)
        
    print("4. Observing editor screen for 10 seconds...")
    for t in range(1, 11):
        time.sleep(1.0)
        if t in [2, 5, 10]:
            path = f"editor_uploading_{t}s.png"
            d.screenshot(path)
            print(f"Captured {path}")

finally:
    print("5. Terminating logcat...")
    log_proc.terminate()
    log_proc.wait()

print("Logcat saved to upload_realtime_logcat.txt")
