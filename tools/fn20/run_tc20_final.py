import uiautomator2 as u2
import time

d = u2.connect('R5CW82ECF6M')

# We are currently in the note editor
# Tap at (650, 210) to focus at end of line
d.click(650, 210)
time.sleep(1)

# Type text
d.send_keys(" - Nội dung kiểm tra tự động lưu")
# Wait 3s for auto-save
time.sleep(3)

# Dismiss keyboard and click back arrow on top bar to return to Home
d.press('back') # closes keyboard
time.sleep(1)
d.click(74, 173) # click back arrow on top bar
time.sleep(2)

# Screenshot on Home
d.screenshot('./screen_home_after_tc20_save.png')

# Now reopen the note: find and click 'Ý tưởng' or at (540, 2090)
d.click(540, 2090)
time.sleep(2)

# Capture screenshot inside the reopened note
d.screenshot('./FN09_TC-BB-020_D01_01.png')
print("Successfully captured FN09_TC-BB-020_D01_01.png")

# Exit note to Home
d.click(74, 173)
time.sleep(1)
