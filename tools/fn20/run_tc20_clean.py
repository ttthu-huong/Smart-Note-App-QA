import uiautomator2 as u2
import time

d = u2.connect('R5CW82ECF6M')

# We are inside the note editor right now
# 1. Tap content field to focus
d.click(650, 210)
time.sleep(1)

# 2. Type text
d.send_keys(" - Nội dung kiểm tra tự động lưu")
# 3. Wait 2 seconds for auto-save
time.sleep(2)

# 4. Exit screen by clicking back arrow at top-left
d.click(74, 173)
time.sleep(2)

# Verify on Home screen, reopen note at (540, 2090)
d.click(540, 2090)
time.sleep(2)

# 5. Capture screenshot of reopened note
d.screenshot('./FN09_TC-BB-020_D01_01.png')
print("Captured FN09_TC-BB-020_D01_01.png successfully!")

# Exit note to Home
d.click(74, 173)
time.sleep(1)
