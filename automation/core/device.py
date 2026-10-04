"""Device driver and automation utilities wrapping uiautomator2 for Smart Note App."""
import os
import time
import uiautomator2 as u2
from automation import config

class SmartNoteDriver:
    """High-level test driver implementing Dynamic-First, Coordinate-Fallback design."""
    def __init__(self, serial: str = config.DEVICE_SERIAL):
        self.serial = serial
        self.device = u2.connect(serial)
        self.ensure_device_ready()

    def ensure_device_ready(self):
        """Wake up and unlock device."""
        self.device.screen_on()
        self.device.unlock()

    def launch_app(self):
        """Launch target application and wait for idle."""
        self.device.app_start(config.APP_PACKAGE)
        time.sleep(1.5)

    def find_by_text(self, text: str, contains: bool = False):
        """Find element dynamically by text or content-description (Flutter friendly)."""
        d = self.device
        if not contains:
            if d(text=text).exists:
                return d(text=text)
            if d(description=text).exists:
                return d(description=text)
        else:
            if d(textContains=text).exists:
                return d(textContains=text)
            if d(descriptionContains=text).exists:
                return d(descriptionContains=text)
        # XPath Fallback
        op = "=" if not contains else "contains"
        xpath = f'//*[@text="{text}" or @content-desc="{text}"]' if not contains else f'//*[contains(@text, "{text}") or contains(@content-desc, "{text}")]'
        nodes = d.xpath(xpath).all()
        if nodes:
            return nodes[0]
        return None

    def click_element_or_coordinate(self, text: str, fallback_x: int, fallback_y: int, timeout: float = 3.0):
        """Try dynamic click first, fallback to verified coordinates if locator fails."""
        d = self.device
        el = self.find_by_text(text)
        if el is not None:
            try:
                el.click(timeout=timeout)
                return True
            except Exception:
                pass
        # Fallback to verified coordinates
        d.click(fallback_x, fallback_y)
        return True

    def dismiss_keyboard_safely(self, touch_x: int = 540, touch_y: int = 600):
        """Dismiss keyboard by tapping safe neutral area without triggering Back exit."""
        self.device.click(touch_x, touch_y)
        time.sleep(0.5)

    def capture_evidence(self, relative_path: str) -> str:
        """Capture screen evidence and save to evidence folder."""
        full_path = os.path.join(config.PROJECT_ROOT, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        self.device.screenshot().save(full_path)
        return full_path

    def get_screen_texts(self):
        """Extract all visible texts and content descriptions."""
        texts = []
        for el in self.device.xpath('//*[@text!="" or @content-desc!=""]').all():
            t = el.attrib.get('text', '') or el.attrib.get('content-desc', '')
            if t and t not in texts:
                texts.append(t)
        return texts
