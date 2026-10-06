"""Automation Test Suite for FN-04: Login with Email/Password.

Test Cases:
- TC-BB-006: Đăng nhập thành công với tài khoản Email hợp lệ (D01)
- TC-BB-007: Đăng nhập thất bại do sai Mật khẩu (D01)
- TC-BB-008: Đăng nhập thất bại do tài khoản không tồn tại (D01)
- TC-BB-009: Đăng nhập thất bại do để trống Mật khẩu (D01)

Standards: IEEE 829 & ISTQB Manual / Automation Test Execution
Device: Samsung Galaxy S21 FE 5G (Android 14)
"""
import sys
import os
import time
import pytest

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from automation.core.device import SmartNoteDriver

class TestFN04Login:
    @classmethod
    def setup_class(cls):
        cls.driver = SmartNoteDriver()
        cls.d = cls.driver.device
        cls.ensure_login_screen()

    @classmethod
    def ensure_login_screen(cls):
        """Precondition: Ensure device is at Login Screen."""
        cls.driver.ensure_device_ready()
        cls.driver.launch_app()
        time.sleep(2)

        # Check if already on login screen
        if cls.driver.find_by_text("Đăng nhập") and (cls.driver.find_by_text("Quên mật khẩu?") or cls.driver.find_by_text("Đăng ký ngay")):
            return True

        # If on EmailVerificationScreen, tap 'Quay lại đăng nhập'
        ret_btn = cls.driver.find_by_text("Quay lại đăng nhập")
        if ret_btn:
            try:
                ret_btn.click()
            except Exception:
                cls.d.click(540, 2140)
            time.sleep(2)
            return True

        # If on Home screen, log out
        if cls.driver.find_by_text("Tìm kiếm"):
            cls.d.click(1006, 172) # Avatar
            time.sleep(1)
            cls.d.click(500, 750) # Quản lý tài khoản
            time.sleep(1)
            cls.d.click(540, 1120) # Đăng xuất tài khoản
            time.sleep(1)
            cls.d.click(672, 1324) # Confirm dialog
            time.sleep(2)

        return True

    def get_input_fields(self):
        """Locate Email and Password fields reliably using accessibility attributes.
        
        Flutter sets password="true" on obscured TextFormField (Mật khẩu)
        and password="false" on the Email field.
        """
        pass_field = self.d.xpath('//android.widget.EditText[@password="true"]')
        email_field = self.d.xpath('//android.widget.EditText[@password="false"]')

        if not email_field.exists or not pass_field.exists:
            edits = self.d(className="android.widget.EditText")
            assert len(edits) >= 2, f"Expected at least 2 EditText fields on LoginScreen, found {len(edits)}"
            email_field = edits[0]
            pass_field = edits[1]

        assert email_field.exists, "Email input field not found on LoginScreen"
        assert pass_field.exists, "Password input field not found on LoginScreen"
        return email_field, pass_field

    def get_field_text(self, field) -> str:
        """Safely retrieve text from either XPathElement or UiObject."""
        try:
            if hasattr(field, "get_text"):
                return field.get_text() or ""
            if hasattr(field, "attrib"):
                return field.attrib.get("text", "") or ""
            if hasattr(field, "info"):
                return field.info.get("text", "") or ""
        except Exception:
            pass
        return ""

    def set_text(self, field, value: str, field_name: str = "Field"):
        """Input text into field and verify text was received."""
        if hasattr(field, "set_text"):
            field.set_text(value)
            time.sleep(0.4)
        else:
            field.click()
            time.sleep(0.3)
            field.clear_text()
            time.sleep(0.3)
            if value:
                field.send_keys(value)
                time.sleep(0.3)

        current_txt = self.get_field_text(field)
        if value and not current_txt:
            # Fallback retry via clipboard paste if set_text didn't register
            field.click()
            time.sleep(0.2)
            self.d.set_clipboard(value)
            time.sleep(0.2)
            try:
                self.d.jsonrpc.pasteClipboard()
            except Exception:
                pass
            time.sleep(0.4)
            current_txt = self.get_field_text(field)

        print(f"[{field_name}] Requested value: {repr(value)}, UI current text: {repr(current_txt)} (len={len(current_txt)})")

    def verify_fields_before_submit(self, expect_email: bool = True, expect_pass: bool = True):
        """Verify that both Email and Password fields actually have data before submit."""
        email_f, pass_f = self.get_input_fields()
        email_txt = self.get_field_text(email_f)
        pass_txt = self.get_field_text(pass_f)

        print(f"[Field Verification Before Submit] Email: {repr(email_txt)} (len={len(email_txt)}), Password: {repr(pass_txt)} (len={len(pass_txt)})")

        if expect_email:
            assert bool(email_txt), "[INPUT FAILURE] Email field is unexpectedly empty before submit!"
        if expect_pass:
            assert bool(pass_txt), "[INPUT FAILURE] Password field is unexpectedly empty before submit!"

    def submit_login(self):
        # 1. Dismiss soft keyboard if open so Login button is not covered
        btn = (
            self.d(description="Đăng nhập")
            or self.d(text="Đăng nhập")
            or self.d.xpath('//*[@text="Đăng nhập" or @content-desc="Đăng nhập"]')
        )
        if not btn.exists:
            self.d.press("back")
            time.sleep(0.5)

        # 2. Click Login button
        btn = (
            self.d(description="Đăng nhập")
            or self.d(text="Đăng nhập")
            or self.d.xpath('//*[@text="Đăng nhập" or @content-desc="Đăng nhập"]')
        )
        if btn.exists:
            btn.click()
        else:
            self.d.press("back")
            time.sleep(0.3)
            self.d.click(540, 1600)

    def extract_error_message(self, wait_seconds: float = 2.5):
        time.sleep(wait_seconds)
        for el in self.d.xpath('//*').all():
            txt = el.attrib.get('text', '') or el.attrib.get('content-desc', '')
            if any(k in txt for k in ["Email", "Mật khẩu", "mật khẩu", "Tài khoản", "lỗi", "không chính xác", "kết nối", "tồn tại"]):
                if txt not in ["Đăng nhập", "Quên mật khẩu?", "Đăng ký ngay", "Chưa có tài khoản? ", "Hoặc tiếp tục với"]:
                    return txt
        return None

    def test_tc_bb_009_empty_password(self):
        """TC-BB-009 (D01): Đăng nhập thất bại do để trống Mật khẩu."""
        self.ensure_login_screen()
        email_f, pass_f = self.get_input_fields()
        self.set_text(email_f, "student_qa@gmail.com", "Email")
        self.set_text(pass_f, "", "Password")
        self.verify_fields_before_submit(expect_email=True, expect_pass=False)
        self.submit_login()

        actual_msg = self.extract_error_message(wait_seconds=1.5)
        ev_file = self.driver.capture_evidence("evidence/fn04/FN04_TC-BB-009_D01_01.png")
        print(f"\n[TC-BB-009] Evidence: {ev_file}")
        print(f"[TC-BB-009] Actual: {repr(actual_msg)}")

        expected_msg = "Vui lòng nhập đầy đủ Email và Mật khẩu."
        assert actual_msg == expected_msg, f"Expected '{expected_msg}', but got '{actual_msg}'"

    def test_tc_bb_008_non_existent_account(self):
        """TC-BB-008 (D01): Đăng nhập thất bại do tài khoản không tồn tại."""
        self.ensure_login_screen()
        email_f, pass_f = self.get_input_fields()
        self.set_text(email_f, "ghost_user@gmail.com", "Email")
        self.set_text(pass_f, "123456", "Password")
        self.verify_fields_before_submit(expect_email=True, expect_pass=True)
        self.submit_login()

        actual_msg = self.extract_error_message(wait_seconds=3.0)
        ev_file = self.driver.capture_evidence("evidence/fn04/FN04_TC-BB-008_D01_01.png")
        print(f"\n[TC-BB-008] Evidence: {ev_file}")
        print(f"[TC-BB-008] Actual: {repr(actual_msg)}")

        expected_msg = "Tài khoản không tồn tại. Vui lòng kiểm tra lại email."
        assert actual_msg == expected_msg, f"[BUG-BB-002] Expected '{expected_msg}', but application displayed '{actual_msg}'"

    def test_tc_bb_007_wrong_password(self):
        """TC-BB-007 (D01): Đăng nhập thất bại do sai Mật khẩu."""
        self.ensure_login_screen()
        email_f, pass_f = self.get_input_fields()
        self.set_text(email_f, "student_qa@gmail.com", "Email")
        self.set_text(pass_f, "wrongpass", "Password")
        self.verify_fields_before_submit(expect_email=True, expect_pass=True)
        self.submit_login()

        actual_msg = self.extract_error_message(wait_seconds=3.0)
        ev_file = self.driver.capture_evidence("evidence/fn04/FN04_TC-BB-007_D01_01.png")
        print(f"\n[TC-BB-007] Evidence: {ev_file}")
        print(f"[TC-BB-007] Actual: {repr(actual_msg)}")

        expected_msg = "Mật khẩu không chính xác."
        assert actual_msg == expected_msg, f"[BUG-BB-003] Expected '{expected_msg}', but application displayed '{actual_msg}'"

    def test_tc_bb_006_valid_email_login(self):
        """TC-BB-006 (D01): Đăng nhập thành công với tài khoản Email hợp lệ."""
        self.ensure_login_screen()
        email_f, pass_f = self.get_input_fields()
        self.set_text(email_f, "student_qa@gmail.com", "Email")
        self.set_text(pass_f, "123456", "Password")
        self.verify_fields_before_submit(expect_email=True, expect_pass=True)
        self.submit_login()

        time.sleep(4.0)
        ev_file = self.driver.capture_evidence("evidence/fn04/FN04_TC-BB-006_D01_01.png")
        print(f"\n[TC-BB-006] Evidence: {ev_file}")

        is_home = bool(self.driver.find_by_text("Tìm kiếm") or self.driver.find_by_text("Ghi chú"))
        is_verification = bool(self.driver.find_by_text("Quay lại đăng nhập") or self.driver.find_by_text("Tôi đã xác thực"))

        if is_verification:
            # Cleanup: return back to login screen
            ret_btn = self.driver.find_by_text("Quay lại đăng nhập")
            if ret_btn:
                try: ret_btn.click()
                except Exception: self.d.click(540, 2140)
            assert False, "[BUG-BB-004] Expected navigation to HomeScreen, but application redirected to EmailVerificationScreen because emailVerified is false."

        assert is_home, "Application did not navigate to HomeScreen after login."

if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
