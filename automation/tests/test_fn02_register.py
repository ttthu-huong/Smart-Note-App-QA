"""Automation Test Suite for FN-02: Register with Email/Password.

Test Cases:
- TC-BB-001: Xác minh đăng ký thành công khi nhập thông tin hợp lệ (D01)
- TC-BB-002: Xác minh chặn đăng ký khi bỏ trống toàn bộ dữ liệu (D01)
- TC-BB-003: Xác minh ứng dụng từ chối các email không hợp lệ hoặc thuộc tên miền không được hỗ trợ (D01)
- TC-BB-004: Xác minh chặn đăng ký khi mật khẩu dưới 6 ký tự (D02)
- TC-BB-005: Xác minh thông báo khi đăng ký bằng Email đã tồn tại (D01)

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


class TestFN02Register:
    @classmethod
    def setup_class(cls):
        cls.driver = SmartNoteDriver()
        cls.d = cls.driver.device
        cls.ensure_register_screen()

    def setup_method(self, method):
        """Guarantee strict test isolation before each test."""
        print(f"\n[Test Setup] Ensuring RegisterScreen for {method.__name__}...")
        self.ensure_register_screen()
        self.clear_fields()

    def teardown_method(self, method):
        """Post-test cleanup to guarantee isolation between tests, best-effort."""
        try:
            print(f"\n[Test Teardown] Running isolation cleanup after {method.__name__}...")
            if self.is_in_verification():
                ret_btn = (
                    self.d(description="Quay lại đăng nhập")
                    or self.d(descriptionContains="Quay lại đăng nhập")
                    or self.d(text="Quay lại đăng nhập")
                    or self.d(textContains="Quay lại đăng nhập")
                    or self.d.xpath('//*[@text="Quay lại đăng nhập" or @content-desc="Quay lại đăng nhập"]')
                )
                if ret_btn.exists:
                    ret_btn.click()
                else:
                    self.d.click(540, 2140)
                for _ in range(12):
                    if not self.is_in_verification() and (self.is_in_login() or self.is_in_register()):
                        break
                    time.sleep(0.5)

            self.ensure_register_screen()
        except Exception as e:
            print(f"[Teardown Warning] Best-effort isolation cleanup encountered error: {e}")

    @classmethod
    def dismiss_keyboard(cls):
        """Dismiss keyboard safely without pressing back when keyboard is closed."""
        try:
            for pkg in [
                "com.samsung.android.honeyboard",
                "com.google.android.inputmethod.latin",
                "com.android.inputmethod.latin",
            ]:
                if cls.d(packageName=pkg).exists:
                    cls.d.press("back")
                    time.sleep(0.4)
                    return
        except Exception:
            pass

    @classmethod
    def is_in_register(cls) -> bool:
        """Check if currently on Register Screen (LoginScreen in Register mode)."""
        return (
            cls.d(descriptionContains="Tạo tài khoản mới").exists
            or cls.d(textContains="Tạo tài khoản mới").exists
            or "Tạo tài khoản mới" in cls.d.dump_hierarchy()
        )

    @classmethod
    def is_in_login(cls) -> bool:
        """Check if currently on LoginScreen in Login mode."""
        return (
            cls.d(descriptionContains="Chào mừng trở lại!").exists
            or cls.d(textContains="Chào mừng trở lại!").exists
            or cls.d(description="Đăng ký ngay").exists
            or cls.d(text="Đăng ký ngay").exists
            or "Chào mừng trở lại!" in cls.d.dump_hierarchy()
        )

    @classmethod
    def is_in_verification(cls) -> bool:
        """Check if currently on EmailVerificationScreen."""
        return (
            cls.d(descriptionContains="Quay lại đăng nhập").exists
            or cls.d(textContains="Quay lại đăng nhập").exists
            or cls.d(descriptionContains="Xác thực").exists
            or "Quay lại đăng nhập" in cls.d.dump_hierarchy()
        )

    @classmethod
    def is_in_home(cls) -> bool:
        """Check if currently on HomeScreen."""
        return (
            cls.driver.find_by_text("Tìm kiếm", contains=True) is not None
            or cls.driver.find_by_text("Search", contains=True) is not None
            or cls.driver.find_by_text("Chưa có ghi chú nào", contains=True) is not None
        )

    @classmethod
    def ensure_register_screen(cls):
        """Precondition: Ensure device is at Register Screen without minimizing app."""
        cls.driver.ensure_device_ready()
        cls.dismiss_keyboard()

        # Retry loop up to 8 iterations
        for iteration in range(8):
            cls.dismiss_keyboard()

            # 1. If already on RegisterScreen
            if cls.is_in_register():
                cls.reset_register_form()
                return True

            # 2. If on EmailVerificationScreen, tap 'Quay lại đăng nhập'
            if cls.is_in_verification():
                print(f"[Precondition] Detected EmailVerificationScreen at loop {iteration}, returning to Login...")
                ret_btn = (
                    cls.d(description="Quay lại đăng nhập")
                    or cls.d(descriptionContains="Quay lại đăng nhập")
                    or cls.d(text="Quay lại đăng nhập")
                    or cls.d(textContains="Quay lại đăng nhập")
                    or cls.d.xpath('//*[@text="Quay lại đăng nhập" or @content-desc="Quay lại đăng nhập"]')
                )
                if ret_btn.exists:
                    ret_btn.click()
                else:
                    cls.d.click(540, 2140)
                
                # Wait for transition out of EmailVerificationScreen
                for _ in range(12):
                    if not cls.is_in_verification() and (cls.is_in_login() or cls.is_in_register()):
                        break
                    time.sleep(0.5)
                continue

            # 3. If on HomeScreen, perform logout
            if cls.is_in_home():
                print(f"[Precondition] Detected HomeScreen at loop {iteration}, logging out...")
                # Tap Avatar (top right)
                cls.d.click(1006, 172)
                time.sleep(1.0)
                # Tap 'Quản lý tài khoản'
                manage_btn = (
                    cls.d(descriptionContains="Quản lý tài khoản")
                    or cls.d(textContains="Quản lý tài khoản")
                )
                if manage_btn.exists:
                    manage_btn.click()
                else:
                    cls.d.click(500, 750)
                time.sleep(1.0)
                # Tap 'Đăng xuất'
                logout_btn = (
                    cls.d(descriptionContains="Đăng xuất")
                    or cls.d(textContains="Đăng xuất")
                )
                if logout_btn.exists:
                    logout_btn.click()
                else:
                    cls.d.click(540, 1120)
                time.sleep(1.0)
                # Tap Confirm dialog
                confirm_btn = (
                    cls.d(descriptionContains="Đăng xuất tài khoản")
                    or cls.d(textContains="Đăng xuất tài khoản")
                )
                if confirm_btn.exists:
                    confirm_btn.click()
                else:
                    cls.d.click(672, 1324)
                time.sleep(2.0)
                continue

            # 4. If on LoginScreen in Login mode, switch to Register mode
            if cls.is_in_login():
                print(f"[Precondition] Detected LoginScreen in Login mode at loop {iteration}, switching to Register...")
                cls.dismiss_keyboard()
                switch_btn = (
                    cls.d(description="Đăng ký ngay")
                    or cls.d(descriptionContains="Đăng ký ngay")
                    or cls.d(text="Đăng ký ngay")
                    or cls.d(textContains="Đăng ký ngay")
                    or cls.d.xpath('//*[@text="Đăng ký ngay" or @content-desc="Đăng ký ngay"]')
                )
                if switch_btn.exists:
                    switch_btn.click()
                else:
                    cls.d.click(720, 1920)
                
                # Wait for transition to Register mode
                for _ in range(8):
                    if cls.is_in_register():
                        cls.reset_register_form()
                        return True
                    time.sleep(0.4)
                continue

            # 5. If unknown screen state, bring app to foreground
            print(f"[Precondition] Unknown screen state at loop {iteration}, ensuring device ready...")
            cls.driver.ensure_device_ready()
            time.sleep(1.0)

        assert cls.is_in_register(), "Precondition failed: Unable to navigate to Register Screen."
        return True

    @classmethod
    def reset_register_form(cls):
        """Reset register form and clear old error messages by toggling tab if needed."""
        cls.dismiss_keyboard()
        xml = cls.d.dump_hierarchy()
        has_error = any(
            k in xml
            for k in ["Vui lòng", "không hợp lệ", "yếu", "sử dụng cho một tài khoản", "rác"]
        )
        if has_error:
            # Switch to login then back to register to clear auth.error
            login_link = (
                cls.d(description="Đăng nhập")
                or cls.d(text="Đăng nhập")
                or cls.d.xpath('//*[@text="Đăng nhập" or @content-desc="Đăng nhập"]')
            )
            if login_link.exists:
                login_link.click()
                time.sleep(0.8)
            else:
                cls.d.click(720, 2100)
                time.sleep(0.8)

            reg_link = (
                cls.d(description="Đăng ký ngay")
                or cls.d(descriptionContains="Đăng ký ngay")
                or cls.d(text="Đăng ký ngay")
                or cls.d(textContains="Đăng ký ngay")
                or cls.d.xpath('//*[@text="Đăng ký ngay" or @content-desc="Đăng ký ngay"]')
            )
            if reg_link.exists:
                reg_link.click()
                time.sleep(0.8)
            else:
                cls.d.click(720, 1920)
                time.sleep(0.8)

    def get_input_fields(self):
        """Locate Email and Password fields reliably using accessibility attributes.
        
        Flutter sets password="true" on obscured TextFormField (Mật khẩu)
        and password="false" on the Email field.
        """
        pass_field = self.d.xpath('//android.widget.EditText[@password="true"]')
        email_field = self.d.xpath('//android.widget.EditText[@password="false"]')

        if not email_field.exists or not pass_field.exists:
            edits = self.d(className="android.widget.EditText")
            assert len(edits) >= 2, f"Expected at least 2 EditText fields on RegisterScreen, found {len(edits)}"
            email_field = edits[0]
            pass_field = edits[1]

        assert email_field.exists, "Email input field not found on RegisterScreen"
        assert pass_field.exists, "Password input field not found on RegisterScreen"
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
        expected_len = len(value)
        actual_len = len(current_txt)

        # For password or text fields where set_text did not register full length
        if expected_len > 0 and actual_len != expected_len:
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

        print(f"[{field_name}] Requested: {repr(value)}, UI text: {repr(current_txt)} (len={len(current_txt)})")

    def verify_fields_before_submit(self, expect_email: bool = True, expect_pass: bool = True):
        """Verify that both Email and Password fields match expectations before submit."""
        email_f, pass_f = self.get_input_fields()
        email_txt = self.get_field_text(email_f)
        pass_txt = self.get_field_text(pass_f)

        print(f"[Field Verification] Email: {repr(email_txt)}, Password: {repr(pass_txt)}")

        if expect_email:
            assert bool(email_txt), "[INPUT FAILURE] Email field is unexpectedly empty before submit!"
        if expect_pass:
            assert bool(pass_txt), "[INPUT FAILURE] Password field is unexpectedly empty before submit!"

    def submit_register(self):
        """Dismiss soft keyboard if open and tap the primary 'Đăng ký' button."""
        # 1. Dismiss soft keyboard safely if open so Register button is viewable
        self.dismiss_keyboard()

        # 2. Click Register button
        btn = (
            self.d(description="Đăng ký")
            or self.d(text="Đăng ký")
            or self.d.xpath('//*[@text="Đăng ký" or @content-desc="Đăng ký"]')
        )
        if btn.exists:
            btn.click()
        else:
            self.d.click(540, 1390)
        time.sleep(1.0)

    def extract_error_message(self, wait_seconds: float = 4.0) -> str:
        """Extract red error message displayed on RegisterScreen with polling."""
        start_time = time.time()
        while time.time() - start_time < wait_seconds:
            # If in-flight progress bar is still active, wait
            if self.d(className="android.widget.ProgressBar").exists:
                time.sleep(0.5)
                continue

            for el in self.d.xpath('//*').all():
                txt = el.attrib.get('text', '') or el.attrib.get('content-desc', '')
                if any(
                    k in txt
                    for k in [
                        "Email", "Mật khẩu", "mật khẩu", "Tài khoản", "lỗi",
                        "không chính xác", "kết nối", "tồn tại", "yếu", "rác", "hợp lệ"
                    ]
                ):
                    if txt not in [
                        "Tạo tài khoản mới", "Bắt đầu hành trình ghi chú thông minh của bạn",
                        "Đăng ký", "Đăng nhập", "Hoặc tiếp tục với", "Đăng nhập bằng Google",
                        "Đã có tài khoản? "
                    ]:
                        return txt
            time.sleep(0.5)
        return ""

    def clear_fields(self):
        """Clear both email and password input fields."""
        try:
            email_f, pass_f = self.get_input_fields()
            self.set_text(email_f, "", "Email")
            self.set_text(pass_f, "", "Password")
        except Exception:
            pass

    # =========================================================================
    # TEST CASES FOR FN-02
    # =========================================================================

    def test_tc_bb_001_register_success(self):
        """TC-BB-001 (D01): Xác minh đăng ký thành công khi nhập thông tin hợp lệ.
        
        Test Data:
        - Email: student_qa_<timestamp>@gmail.com (mới chưa từng đăng ký)
        - Mật khẩu: 123456
        
        Expected Result:
        - Ứng dụng chuyển sang màn hình Xác thực Email (EmailVerificationScreen) và hiển thị hướng dẫn kiểm tra email.
        """
        self.ensure_register_screen()
        self.clear_fields()

        timestamp = int(time.time())
        email = f"student_qa_{timestamp}@gmail.com"
        password = "123456"

        email_f, pass_f = self.get_input_fields()
        self.set_text(email_f, email, "Email")
        self.set_text(pass_f, password, "Password")
        self.verify_fields_before_submit(expect_email=True, expect_pass=True)

        try:
            self.submit_register()

            # Polling up to 12.0s for Firebase registration & screen transition
            transitioned = False
            for _ in range(24):
                if self.is_in_verification() or "Quay lại đăng nhập" in self.d.dump_hierarchy():
                    transitioned = True
                    break
                time.sleep(0.5)

            # Evidence Capture
            ev_file = self.driver.capture_evidence("evidence/fn02/FN02_TC-BB-001_D01_01.png")
            print(f"\n[TC-BB-001] Evidence saved: {ev_file}")

            print(f"[TC-BB-001] Transitioned to EmailVerificationScreen: {transitioned}")
            assert transitioned, (
                f"Expected app to navigate to EmailVerificationScreen after registering with valid email '{email}'."
            )
        finally:
            # Best-effort cleanup: Return to Register screen cleanly without failing BB-001
            try:
                if self.is_in_verification():
                    ret_btn = (
                        self.d(description="Quay lại đăng nhập")
                        or self.d(descriptionContains="Quay lại đăng nhập")
                        or self.d(text="Quay lại đăng nhập")
                        or self.d(textContains="Quay lại đăng nhập")
                        or self.d.xpath('//*[@text="Quay lại đăng nhập" or @content-desc="Quay lại đăng nhập"]')
                    )
                    if ret_btn.exists:
                        ret_btn.click()
                    else:
                        self.d.click(540, 2140)
                    for _ in range(12):
                        if not self.is_in_verification() and (self.is_in_login() or self.is_in_register()):
                            break
                        time.sleep(0.5)

                self.ensure_register_screen()
            except Exception as e:
                print(f"[TC-BB-001 Cleanup Warning] Best-effort return failed: {e}")

    def test_tc_bb_002_empty_fields(self):
        """TC-BB-002 (D01): Xác minh chặn đăng ký khi bỏ trống toàn bộ dữ liệu.
        
        Test Data:
        - Email: ""
        - Mật khẩu: ""
        
        Expected Result:
        - Ứng dụng không chuyển màn hình; xuất hiện khung thông báo lỗi màu đỏ:
          "Vui lòng nhập đầy đủ Email và Mật khẩu."
        """
        self.ensure_register_screen()
        self.clear_fields()

        email_f, pass_f = self.get_input_fields()
        self.set_text(email_f, "", "Email")
        self.set_text(pass_f, "", "Password")
        self.verify_fields_before_submit(expect_email=False, expect_pass=False)

        self.submit_register()

        err_msg = self.extract_error_message(wait_seconds=3.0)

        # Evidence Capture
        ev_file = self.driver.capture_evidence("evidence/fn02/FN02_TC-BB-002_D01_01.png")
        print(f"\n[TC-BB-002] Evidence saved: {ev_file}")
        print(f"[TC-BB-002] Actual Error Message: {repr(err_msg)}")

        expected = "Vui lòng nhập đầy đủ Email và Mật khẩu."
        assert self.is_in_register(), "App unexpectedly left RegisterScreen on empty submission."
        assert err_msg == expected, f"Expected error '{expected}', but got '{err_msg}'."

    def test_tc_bb_003_invalid_email_format(self):
        """TC-BB-003 (D01): Xác minh ứng dụng từ chối các email không hợp lệ (thiếu ký tự @).
        
        Test Data:
        - Email: nguoidung_gmail.com
        - Mật khẩu: 123456
        
        Expected Result:
        - Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ:
          "Định dạng email không hợp lệ."
        """
        self.ensure_register_screen()
        self.clear_fields()

        email = "nguoidung_gmail.com"
        password = "123456"

        email_f, pass_f = self.get_input_fields()
        self.set_text(email_f, email, "Email")
        self.set_text(pass_f, password, "Password")
        self.verify_fields_before_submit(expect_email=True, expect_pass=True)

        self.submit_register()

        err_msg = self.extract_error_message(wait_seconds=3.5)

        # Evidence Capture
        ev_file = self.driver.capture_evidence("evidence/fn02/FN02_TC-BB-003_D01_01.png")
        print(f"\n[TC-BB-003] Evidence saved: {ev_file}")
        print(f"[TC-BB-003] Actual Error Message: {repr(err_msg)}")

        expected = "Định dạng email không hợp lệ."
        assert self.is_in_register(), "App unexpectedly left RegisterScreen on invalid email."
        assert err_msg == expected, (
            f"[BUG-FN02-01] Expected error message '{expected}', but got '{err_msg}'."
        )

    def test_tc_bb_004_weak_password(self):
        """TC-BB-004 (D02): Xác minh chặn đăng ký khi mật khẩu dưới 6 ký tự.
        
        Test Data:
        - Email: student_bva_<timestamp>@gmail.com
        - Mật khẩu: 12345 (5 ký tự - điểm biên cận dưới không hợp lệ)
        
        Expected Result:
        - Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ:
          "Mật khẩu quá yếu (cần ít nhất 6 ký tự)."
        """
        self.ensure_register_screen()
        self.clear_fields()

        timestamp = int(time.time())
        email = f"student_bva_{timestamp}@gmail.com"
        password = "12345"

        email_f, pass_f = self.get_input_fields()
        self.set_text(email_f, email, "Email")
        self.set_text(pass_f, password, "Password")
        self.verify_fields_before_submit(expect_email=True, expect_pass=True)

        self.submit_register()

        err_msg = self.extract_error_message(wait_seconds=4.0)

        # Evidence Capture
        ev_file = self.driver.capture_evidence("evidence/fn02/FN02_TC-BB-004_D02_01.png")
        print(f"\n[TC-BB-004] Evidence saved: {ev_file}")
        print(f"[TC-BB-004] Actual Error Message: {repr(err_msg)}")

        expected = "Mật khẩu quá yếu (cần ít nhất 6 ký tự)."
        assert self.is_in_register(), "App unexpectedly left RegisterScreen on weak password."
        assert err_msg == expected, f"Expected error '{expected}', but got '{err_msg}'."

    def test_tc_bb_005_duplicate_email(self):
        """TC-BB-005 (D01): Xác minh thông báo khi đăng ký bằng Email đã tồn tại.
        
        Test Data:
        - Email: student_qa@gmail.com (tài khoản đã đăng ký trên hệ thống)
        - Mật khẩu: 123456
        
        Expected Result:
        - Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ:
          "Email này đã được sử dụng cho một tài khoản khác."
        """
        self.ensure_register_screen()
        self.clear_fields()

        email = "student_qa@gmail.com"
        password = "123456"

        email_f, pass_f = self.get_input_fields()
        self.set_text(email_f, email, "Email")
        self.set_text(pass_f, password, "Password")
        self.verify_fields_before_submit(expect_email=True, expect_pass=True)

        self.submit_register()

        err_msg = self.extract_error_message(wait_seconds=4.5)

        # Evidence Capture
        ev_file = self.driver.capture_evidence("evidence/fn02/FN02_TC-BB-005_D01_01.png")
        print(f"\n[TC-BB-005] Evidence saved: {ev_file}")
        print(f"[TC-BB-005] Actual Error Message: {repr(err_msg)}")

        expected = "Email này đã được sử dụng cho một tài khoản khác."
        assert self.is_in_register(), "App unexpectedly left RegisterScreen on duplicate email."
        assert err_msg == expected, f"Expected error '{expected}', but got '{err_msg}'."
