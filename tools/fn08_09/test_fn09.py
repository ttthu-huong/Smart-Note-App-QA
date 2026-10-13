import uiautomator2 as u2
import time
import re

d = u2.connect('R5CW82ECF6M')

# Find element with text or content-desc containing Hop Lab
for el in d.xpath('//*').all():
    txt = el.text or el.attrib.get('content-desc', '')
    if 'Hop' in txt or 'Họp' in txt:
        bounds_str = el.attrib.get('bounds')
        print(f"Found note: {bounds_str}")
        # Parse bounds [left,top][right,bottom]
        m = re.findall(r'\d+', bounds_str)
        if m:
            x = (int(m[0]) + int(m[2])) // 2
            y = (int(m[1]) + int(m[3])) // 2
            print(f"Clicking at ({x}, {y})")
            d.click(x, y)
            break

time.sleep(2)
# Click content area
d.click(300, 500)
time.sleep(0.5)
# In editor, add [Đã cập nhật lúc 10:00]
d.send_keys(" [Đã cập nhật lúc 10:00]")
time.sleep(1)

# Press back to exit editor
d.press('back') # closes keyboard if open
time.sleep(1)
d.click(74, 173) # tap back button on top bar
time.sleep(2)

d.screenshot('./screen_tc19_result.png')
print("TC-BB-019 finished")
