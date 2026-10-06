"""Automation test suite for FN-29 & FN-30: Note Lock & Biometric Authentication.

Covers:
- AT-59 (TC-BB-015): Cancel BiometricPrompt safely while maintaining lock overlay.
- AT-60 (TC-BB-015C): Safely exit from locked note overlay via Back navigation.
Standard: IEEE 829 and ISTQB Feasibility Validation.
"""
import time
import os
import pytest
from automation import config


class TestBiometricPrompt:
    """Feasibility Validation test suite for FN-29 / FN-30: Biometric Authentication."""

    def test_at59_cancel_biometric_prompt(self, ensure_home, driver, device):
        """AT-59 / TC-BB-015 (D01): Cancel system BiometricPrompt.

        Precondition: App is on HomeScreen with at least one locked note.
        Steps:
            1. Tap on the locked note card.
            2. Detect System UI BiometricPrompt (com.samsung.android.biometrics.app.setting).
            3. Dismiss BiometricPrompt by tapping 'Cancel' button (or pressing system Back).
            4. Verify BiometricPrompt is dismissed and note remains in locked state with overlay.
        """
        # Step 1: Precondition check - verify HomeScreen
        assert driver.is_on_home_screen(), "Precondition failed: App is not on HomeScreen"

        # Locate locked note card on HomeScreen
        locked_card = (
            driver.find_by_text("Ghi chú đã khóa", contains=True)
            or device(descriptionContains="Ghi chú đã khóa")
            or device(textContains="Ghi chú đã khóa")
        )
        if not locked_card or not locked_card.exists:
            nodes = device.xpath(
                '//*[contains(@text, "Ghi chú đã khóa") or contains(@content-desc, "Ghi chú đã khóa")]'
            ).all()
            assert len(nodes) > 0, "Precondition failed: No locked note found on HomeScreen"
            locked_card = nodes[0]

        # Step 2: Open locked note to trigger BiometricPrompt
        locked_card.click()

        # Step 3: Detect System UI BiometricPrompt
        biometric_pkg = "com.samsung.android.biometrics.app.setting"
        prompt_opened = (
            device(packageName=biometric_pkg).wait(timeout=6.0)
            or device(resourceIdMatches=".*biometrics.*").wait(timeout=3.0)
            or device(textMatches="(?i)(Cancel|Hủy)").wait(timeout=3.0)
        )
        assert prompt_opened, "System UI BiometricPrompt did not appear within 6s"

        # Evidence 1: BiometricPrompt displayed
        ev_dir = os.path.join(config.EVIDENCE_ROOT, "fn29_30")
        os.makedirs(ev_dir, exist_ok=True)
        ev1 = os.path.join(ev_dir, "FN29_30_TC-BB-015_D01_01.png")
        device.screenshot(ev1)

        # Step 4: Dismiss BiometricPrompt via Cancel button or Back key
        cancel_btn = (
            device(resourceId=f"{biometric_pkg}:id/button_negative")
            or device(text="Cancel")
            or device(text="Hủy")
            or device(description="Cancel")
            or device(description="Hủy")
        )
        if cancel_btn.exists:
            cancel_btn.click()
        else:
            device.press("back")

        # Step 5: Verify prompt is dismissed
        prompt_gone = device(packageName=biometric_pkg).wait_gone(timeout=5.0)
        assert prompt_gone, "BiometricPrompt did not dismiss after cancellation"

        # Step 6: Verify observable state in Smart Note App
        time.sleep(1.0)
        current_app = device.app_current()
        assert current_app.get("package") == config.APP_PACKAGE, (
            f"Smart Note App is not in foreground, got: {current_app}"
        )

        # Verify Lock Overlay is preserved
        screen_texts = driver.get_screen_texts()
        has_lock_overlay = any(
            ("Ghi chú đã" in t or "Xác thực ngay" in t or "khóa" in t.lower())
            for t in screen_texts
        )
        has_auth_btn = (
            device(text="Xác thực ngay").exists
            or device(description="Xác thực ngay").exists
            or any("Xác thực ngay" in t for t in screen_texts)
        )
        assert has_lock_overlay, f"Lock overlay not visible on screen. Visible texts: {screen_texts}"
        assert has_auth_btn, "Authenticate button ('Xác thực ngay') not found on lock screen"

        # Evidence 2: Lock overlay maintained after cancellation
        ev2 = os.path.join(ev_dir, "FN29_30_TC-BB-015_D01_02.png")
        device.screenshot(ev2)

        # Post-test Cleanup: Return to HomeScreen safely
        device.press("back")
        time.sleep(1.0)
        if not driver.is_on_home_screen():
            device.press("back")
            time.sleep(1.0)

    def test_at60_back_from_locked_note(self, ensure_home, driver, device):
        """AT-60 / TC-BB-015C (D01): Safely exit from locked note overlay via Back navigation.

        Precondition: App is on HomeScreen with a pre-existing locked note.
        (Note: Requires pre-existing locked note; cannot auto-generate without physical biometric scan).

        Steps:
            1. Locate locked note on HomeScreen.
            2. Tap locked note to enter EditorScreen.
            3. Dismiss System UI BiometricPrompt (Cancel button / Back key).
            4. Verify Lock Overlay is active (note content protected).
            5. Tap AppBar Back button (or press Back key).
            6. Verify navigation back to HomeScreen safely without data leak.
        """
        # Step 1: Precondition check
        assert driver.is_on_home_screen(), "Precondition failed: App is not on HomeScreen"

        locked_card = (
            driver.find_by_text("Ghi chú đã khóa", contains=True)
            or device(descriptionContains="Ghi chú đã khóa")
            or device(textContains="Ghi chú đã khóa")
        )
        if not locked_card or not locked_card.exists:
            nodes = device.xpath(
                '//*[contains(@text, "Ghi chú đã khóa") or contains(@content-desc, "Ghi chú đã khóa")]'
            ).all()
            assert len(nodes) > 0, (
                "Precondition failed: No locked note found on HomeScreen. "
                "AT-60 requires a pre-existing locked note on the test device."
            )
            locked_card = nodes[0]

        # Step 2: Open locked note
        locked_card.click()

        # Step 3: Dismiss System UI BiometricPrompt
        biometric_pkg = "com.samsung.android.biometrics.app.setting"
        prompt_opened = (
            device(packageName=biometric_pkg).wait(timeout=6.0)
            or device(resourceIdMatches=".*biometrics.*").wait(timeout=3.0)
            or device(textMatches="(?i)(Cancel|Hủy)").wait(timeout=3.0)
        )
        if prompt_opened:
            cancel_btn = (
                device(resourceId=f"{biometric_pkg}:id/button_negative")
                or device(text="Cancel")
                or device(text="Hủy")
            )
            if cancel_btn.exists:
                cancel_btn.click()
            else:
                device.press("back")
            device(packageName=biometric_pkg).wait_gone(timeout=5.0)

        time.sleep(1.0)

        # Step 4: Verify Lock Overlay is active
        ev_dir = os.path.join(config.EVIDENCE_ROOT, "fn29_30")
        os.makedirs(ev_dir, exist_ok=True)
        ev1 = os.path.join(ev_dir, "FN29_30_TC-BB-015C_D01_01.png")
        device.screenshot(ev1)

        screen_texts = driver.get_screen_texts()
        has_lock_overlay = any(
            ("Ghi chú đã" in t or "Xác thực ngay" in t or "khóa" in t.lower())
            for t in screen_texts
        )
        assert has_lock_overlay, f"Lock overlay not visible before Back navigation. Visible: {screen_texts}"

        # Step 5: Perform Back navigation via AppBar Back button or coordinate fallback
        appbar_back = device(descriptionContains="Quay lại") or device(descriptionContains="Back")
        if appbar_back.exists:
            appbar_back.click()
        else:
            # Verified coordinate for AppBar leading back icon (75, 170)
            device.click(75, 170)

        time.sleep(1.2)

        # Fallback to system Back if still on editor
        if not driver.is_on_home_screen():
            device.press("back")
            time.sleep(1.0)

        # Step 6: Verify navigation back to HomeScreen safely
        assert driver.is_on_home_screen(), "Failed to navigate back to HomeScreen from locked note overlay"
        assert device.app_current().get("package") == config.APP_PACKAGE, "App is not in foreground"

        # Evidence 2: Safely returned to HomeScreen
        ev2 = os.path.join(ev_dir, "FN29_30_TC-BB-015C_D01_02.png")
        device.screenshot(ev2)
