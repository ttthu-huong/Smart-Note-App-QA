"""Automation test suite for FN-05: Google OAuth Authentication.

Covers AT-21 (TC-BB-011): Cancel Google Account Picker safely without app crash or freeze.
Standard: IEEE 829 and ISTQB Feasibility Validation.
"""
import time
import os
import pytest
from automation import config


class TestGoogleOAuth:
    """Feasibility Validation test suite for FN-05: Google OAuth Authentication."""

    def test_at21_cancel_google_account_picker(self, ensure_login, driver, device):
        """AT-21 / TC-BB-011 (D01): Cancel Google Account Picker.

        Precondition: App is on LoginScreen.
        Steps:
            1. Locate and click 'Đăng nhập bằng Google'.
            2. Detect System UI Google Account Picker (com.google.android.gms).
            3. Press system Back key to cancel account selection.
            4. Verify Account Picker is dismissed and app remains safely on LoginScreen.
        """
        # Step 1: Precondition check
        assert driver.is_in_login(), "Precondition failed: App is not on LoginScreen"

        # Step 2: Locate Google Login button
        google_btn = driver.find_by_text("Đăng nhập bằng Google") or device(textContains="Google")
        assert google_btn is not None and google_btn.exists, "Google login button not found on LoginScreen"

        # Step 3: Click Google button
        google_btn.click()

        # Step 4: Detect Google Account Picker (System UI)
        picker_opened = device(packageName="com.google.android.gms").wait(timeout=8.0)
        assert picker_opened, "System UI Google Account Picker (com.google.android.gms) did not appear within 8s"

        # Evidence 1: Account Picker displayed
        ev_dir = os.path.join(config.EVIDENCE_ROOT, "fn05")
        os.makedirs(ev_dir, exist_ok=True)
        ev1 = os.path.join(ev_dir, "FN05_TC-BB-011_D01_01.png")
        device.screenshot(ev1)

        # Step 5: Send Back key to cancel
        device.press("back")

        # Step 6: Wait for Account Picker to dismiss
        picker_gone = device(packageName="com.google.android.gms").wait_gone(timeout=5.0)
        assert picker_gone, "Google Account Picker did not dismiss after pressing Back key"

        # Step 7: Verify app returns safely to LoginScreen
        time.sleep(1.0)
        assert driver.is_in_login(), "App did not return to LoginScreen after canceling Google Account Picker"
        assert device.app_current().get("package") == config.APP_PACKAGE, "Smart Note App is not in foreground"

        # Evidence 2: Safely returned to LoginScreen
        ev2 = os.path.join(ev_dir, "FN05_TC-BB-011_D01_02.png")
        device.screenshot(ev2)
