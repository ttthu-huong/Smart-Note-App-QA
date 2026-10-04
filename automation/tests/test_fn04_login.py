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
        email_field = self.d(className="android.widget.EditText", instance=0)
        pass_field = self.d(className="android.widget.EditText", instance=1)
        assert email_field.exists, "Email input field not found"
        assert pass_field.exists, "Password input field not found"
        return email_field, pass_field

    def set_text(self, field, value: str):
        field.click()
        time.sleep(0.3)
        field.clear_text()
        time.sleep(0.3)
        if value:
            field.send_keys(value)
            time.sleep(0.3)

    def submit_login(self):
        # Dismiss keyboard safely
        self.driver.dismiss_keyboard_safely(540, 600)
        btn = self.driver.find_by_text("Đăng nhập")
        if btn is not None:
            try:
                btn.click()
            except Exception:
                self.d.click(540, 1600)
        else:
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
        self.set_text(email_f, "student_qa@gmail.com")
        self.set_text(pass_f, "")
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
        self.set_text(email_f, "ghost_user@gmail.com")
        self.set_text(pass_f, "123456")
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
        self.set_text(email_f, "student_qa@gmail.com")
        self.set_text(pass_f, "wrongpass")
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
        self.set_text(email_f, "student_qa@gmail.com")
        self.set_text(pass_f, "123456")
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
