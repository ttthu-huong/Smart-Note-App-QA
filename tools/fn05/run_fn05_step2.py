import subprocess
import time
import os
import re
import sys
import io

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

serial = "R5CW82ECF6M"

def adb(cmd):
    full_cmd = f"adb -s {serial} {cmd}"
    res = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

evidence_qa_dir = r"D:\Workspace\TBDD\Smart-Note-App-QA\evidence\fn05"
evidence_artemis_dir = r"d:\Workspace\TBDD\artemis\evidence\fn05"

def save_screen(filename):
    raw = subprocess.check_output(f"adb -s {serial} exec-out screencap -p", shell=True)
    with open(f"{evidence_qa_dir}\\{filename}", "wb") as f:
        f.write(raw)
    with open(f"{evidence_artemis_dir}\\{filename}", "wb") as f:
        f.write(raw)
    return len(raw)

print("1. Finding 'Đăng nhập bằng Google' button and tapping...")
adb("shell uiautomator dump /sdcard/window_dump.xml")
dump = subprocess.check_output(['adb', '-s', serial, 'shell', 'cat', '/sdcard/window_dump.xml']).decode('utf-8', errors='ignore')
btn_match = re.search(r'<node [^>]*content-desc="Đăng nhập bằng Google"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', dump)
if btn_match:
    x1, y1, x2, y2 = map(int, btn_match.groups())
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    adb(f"shell input tap {cx} {cy}")
else:
    adb("shell input tap 540 1721")

time.sleep(2.5)

print("2. Tapping first Google account (Thu Hường) in chooser dialog...")
# First account row in Google Chooser is around X=500, Y=285
adb("shell input tap 500 285")
time.sleep(6.0) # Wait for Google auth & cloud sync

print("3. Capturing Evidence 2 after Google Login...")
save_screen("FN05_TC-BB-010_D01_02.png")

print("4. Dumping UI hierarchy to verify Home screen...")
adb("shell uiautomator dump /sdcard/window_dump.xml")
dump_home = subprocess.check_output(['adb', '-s', serial, 'shell', 'cat', '/sdcard/window_dump.xml']).decode('utf-8', errors='ignore')
texts = re.findall(r'content-desc="([^"]+)"', dump_home)
print("Screen texts on Home:")
for t in texts:
    print(" -", t)
