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
os.makedirs(evidence_qa_dir, exist_ok=True)
os.makedirs(evidence_artemis_dir, exist_ok=True)

def save_screen(filename):
    raw = subprocess.check_output(f"adb -s {serial} exec-out screencap -p", shell=True)
    with open(f"{evidence_qa_dir}\\{filename}", "wb") as f:
        f.write(raw)
    with open(f"{evidence_artemis_dir}\\{filename}", "wb") as f:
        f.write(raw)
    return len(raw)

print("1. Tapping 'Đăng nhập bằng Google' at (540, 1912)...")
adb("shell input tap 540 1912")
time.sleep(2.5)

print("2. Capturing Google Account Chooser Dialog...")
save_screen("FN05_TC-BB-010_D01_01.png")
adb("shell uiautomator dump /sdcard/window_dump.xml")
dump = subprocess.check_output(['adb', '-s', serial, 'shell', 'cat', '/sdcard/window_dump.xml']).decode('utf-8', errors='ignore')

# Check which package is in focus
res_focus = adb("shell dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'")
print("Focus after tap:", res_focus)

print("3. Cancelling Google Sign-In via Back key (TC-BB-011)...")
adb("shell input keyevent 4")
time.sleep(1.5)

print("4. Capturing screen after cancel...")
save_screen("FN05_TC-BB-011_D01_01.png")

adb("shell uiautomator dump /sdcard/window_dump.xml")
dump_after = subprocess.check_output(['adb', '-s', serial, 'shell', 'cat', '/sdcard/window_dump.xml']).decode('utf-8', errors='ignore')
texts = re.findall(r'content-desc="([^"]+)"', dump_after)
print("Screen texts after cancel:")
for t in texts:
    print(" -", t)
