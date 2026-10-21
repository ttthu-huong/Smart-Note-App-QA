# -*- coding: utf-8 -*-
"""Shared QA Test Data and Note Lifecycle Helper for Automation Suites.

Provides reusable methods for:
- Creating QA test notes with title and content using the proven QuillEditor clipboard method.
- Verifying notes on HomeScreen and TrashScreen using resilient text/content-desc matching.
- Moving notes to Trash via Flutter Selection Mode.
- Navigating between HomeScreen and TrashScreen via the Main Drawer.
- Restoring notes from TrashScreen.
- Permanently deleting notes from TrashScreen with confirmation dialog handling.
- Best-effort safe cleanup.

Standards: IEEE 829 & ISTQB Automation Guidelines
Compatible with: Python 3.13, uiautomator2, Flutter accessibility trees
"""

import time
from automation.core.device import SmartNoteDriver


class QANoteHelper:
    """Centralized QA Note Helper for FN-10, FN-11, FN-12 and related suites."""

    @staticmethod
    def create_test_note(driver: SmartNoteDriver, title: str, content: str = "QA Test Content", poll_timeout: float = 6.0) -> bool:
        """Create a new note using the proven FN-08/09 Editor flow and verify on HomeScreen.

        Args:
            driver: Initialized SmartNoteDriver instance.
            title: Title of the note.
            content: Body text for QuillEditor.
            poll_timeout: Seconds to wait for note to render on HomeScreen.

        Returns:
            True if created and verified on HomeScreen.

        Raises:
            AssertionError if creation or HomeScreen verification fails.
        """
        d = driver.device
        driver.ensure_home_screen()
        time.sleep(0.5)

        # 1. Open Editor
        print(f"[QANoteHelper] Opening editor for note '{title}'...")
        driver.open_note_editor()
        time.sleep(0.5)

        # 2. Input Title
        print(f"[QANoteHelper] Inputting title: '{title}'...")
        driver.input_title(title)
        time.sleep(0.3)

        # 3. Input Content via QuillEditor clipboard helper
        if content:
            print(f"[QANoteHelper] Inputting content via clipboard JSON-RPC...")
            driver.input_content(content)
            time.sleep(0.5)

        # 4. Save and return to HomeScreen
        print(f"[QANoteHelper] Saving and exiting editor...")
        driver.save_and_exit_editor()

        # 5. Polling verification on HomeScreen
        print(f"[QANoteHelper] Verifying note '{title}' appears on HomeScreen (up to {poll_timeout}s)...")
        start_time = time.time()
        found = False

        while time.time() - start_time < poll_timeout:
            if (
                d(descriptionContains=title).exists
                or d(textContains=title).exists
                or driver.find_by_text(title, contains=True) is not None
                or d.xpath(f'//*[contains(@content-desc, "{title}") or contains(@text, "{title}")]').exists
            ):
                found = True
                break
            time.sleep(0.5)

        assert found, f"[QANoteHelper ERROR] Created note '{title}' not found on HomeScreen after {poll_timeout}s."
        print(f"[QANoteHelper SUCCESS] Note '{title}' successfully created and rendered on HomeScreen.")
        return True

    @staticmethod
    def move_note_to_trash_from_home(driver: SmartNoteDriver, title: str) -> bool:
        """Move a note to Trash via HomeScreen Selection Mode (TC-BB-021).

        Steps:
        1. Locate note card on HomeScreen.
        2. Long press (1.2s) to activate Selection Mode.
        3. Tap the Trash icon on the Selection AppBar.
        4. Verify note disappears from HomeScreen.
        """
        d = driver.device
        driver.ensure_home_screen()

        # 1. Locate card
        card = d(descriptionContains=title) or d(textContains=title)
        if not card.exists:
            card = driver.find_by_text(title, contains=True)
        assert card is not None and card.exists, f"[QANoteHelper] Note '{title}' not found on HomeScreen to move to trash."

        # 2. Long press to activate selection mode
        print(f"[QANoteHelper] Long-pressing note '{title}' to activate Selection Mode...")
        card.long_click(duration=1.2)
        time.sleep(0.8)

        # 3. Find and tap Trash icon on Selection AppBar
        trash_btn = (
            d(descriptionContains="thùng rác")
            or d(descriptionContains="Trash")
            or d(descriptionContains="trash")
            or d(textContains="thùng rác")
            or d.xpath('//*[contains(@content-desc, "thùng rác") or contains(@content-desc, "Trash")]')
        )
        assert trash_btn.exists, "[QANoteHelper] Trash button not found on Selection AppBar."
        print(f"[QANoteHelper] Tapping Trash button on Selection AppBar...")
        trash_btn.click()
        time.sleep(1.2)

        # 4. Verify note disappeared from HomeScreen
        absent = False
        for _ in range(8):
            still_exists = (
                d(descriptionContains=title).exists
                or d(textContains=title).exists
                or driver.find_by_text(title, contains=True) is not None
            )
            if not still_exists:
                absent = True
                break
            time.sleep(0.5)

        assert absent, f"[QANoteHelper ERROR] Note '{title}' is still visible on HomeScreen after moving to trash."
        print(f"[QANoteHelper SUCCESS] Note '{title}' successfully removed from HomeScreen into Trash.")
        return True

    @staticmethod
    def navigate_to_trash(driver: SmartNoteDriver) -> bool:
        """Navigate to TrashScreen via MainDrawer from HomeScreen."""
        d = driver.device
        driver.ensure_home_screen()
        time.sleep(0.5)

        # 1. Open Drawer (hamburger menu top-left or swipe right)
        print(f"[QANoteHelper] Opening MainDrawer...")
        menu_btn = (
            d(descriptionContains="menu")
            or d(descriptionContains="Menu")
            or d(descriptionContains="điều hướng")
            or d(descriptionContains="navigation")
        )
        if menu_btn.exists:
            menu_btn.click()
        else:
            # Fallback: click top-left AppBar area or swipe
            d.click(75, 170)
        time.sleep(0.8)

        # If drawer didn't open via click, swipe from left edge
        if not (d(text="Thùng rác").exists or d(description="Thùng rác").exists):
            print(f"[QANoteHelper] Fallback: Swiping left-to-right to open drawer...")
            d.swipe(10, 600, 800, 600, steps=15)
            time.sleep(0.8)

        # 2. Tap "Thùng rác" in Drawer
        trash_item = (
            d(text="Thùng rác")
            or d(description="Thùng rác")
            or d(textContains="Thùng rác")
            or d(descriptionContains="Thùng rác")
        )
        assert trash_item.exists, "[QANoteHelper ERROR] 'Thùng rác' option not found in MainDrawer."
        print(f"[QANoteHelper] Selecting 'Thùng rác' from Drawer...")
        trash_item.click()
        time.sleep(1.5)

        # 3. Verify on TrashScreen
        on_trash = (
            d(text="Thùng rác").exists
            or d(description="Thùng rác").exists
            or d(descriptionContains="Thùng rác").exists
            or d(textContains="Thùng rác trống").exists
            or d(descriptionContains="Thùng rác trống").exists
        )
        assert on_trash, "[QANoteHelper ERROR] Failed to navigate to TrashScreen."
        print(f"[QANoteHelper SUCCESS] Navigated to TrashScreen.")
        return True

    @staticmethod
    def navigate_from_trash_to_home(driver: SmartNoteDriver) -> bool:
        """Navigate back to HomeScreen from TrashScreen via Drawer."""
        d = driver.device
        time.sleep(0.5)

        # 1. Open Drawer from TrashScreen
        menu_btn = d(descriptionContains="menu") or d(descriptionContains="Menu")
        if menu_btn.exists:
            menu_btn.click()
        else:
            d.click(75, 170)
        time.sleep(0.8)

        if not (d(text="Ghi chú").exists or d(description="Ghi chú").exists):
            d.swipe(10, 600, 800, 600, steps=15)
            time.sleep(0.8)

        # 2. Tap "Ghi chú" in Drawer
        home_item = (
            d(text="Ghi chú")
            or d(description="Ghi chú")
            or d(textContains="Ghi chú")
            or d(descriptionContains="Ghi chú")
        )
        if home_item.exists:
            home_item.click()
            time.sleep(1.2)

        # 3. Ensure on HomeScreen
        driver.ensure_home_screen()
        return True

    @staticmethod
    def verify_note_in_trash(driver: SmartNoteDriver, title: str, poll_timeout: float = 5.0) -> bool:
        """Verify note appears in TrashScreen."""
        d = driver.device
        start_time = time.time()
        found = False

        while time.time() - start_time < poll_timeout:
            if (
                d(descriptionContains=title).exists
                or d(textContains=title).exists
                or driver.find_by_text(title, contains=True) is not None
                or d.xpath(f'//*[contains(@content-desc, "{title}") or contains(@text, "{title}")]').exists
            ):
                found = True
                break
            time.sleep(0.5)

        assert found, f"[QANoteHelper ERROR] Note '{title}' not found in TrashScreen."
        print(f"[QANoteHelper SUCCESS] Note '{title}' verified present in TrashScreen.")
        return True

    @staticmethod
    def verify_note_absent_in_trash(driver: SmartNoteDriver, title: str) -> bool:
        """Verify note is no longer present in TrashScreen."""
        d = driver.device
        absent = False
        for _ in range(6):
            if not (
                d(descriptionContains=title).exists
                or d(textContains=title).exists
                or driver.find_by_text(title, contains=True) is not None
            ):
                absent = True
                break
            time.sleep(0.5)

        assert absent, f"[QANoteHelper ERROR] Note '{title}' still visible in TrashScreen."
        print(f"[QANoteHelper SUCCESS] Note '{title}' verified absent in TrashScreen.")
        return True

    @staticmethod
    def verify_note_on_home(driver: SmartNoteDriver, title: str, poll_timeout: float = 6.0) -> bool:
        """Verify note is present on HomeScreen."""
        d = driver.device
        driver.ensure_home_screen()
        start_time = time.time()
        found = False

        while time.time() - start_time < poll_timeout:
            if (
                d(descriptionContains=title).exists
                or d(textContains=title).exists
                or driver.find_by_text(title, contains=True) is not None
            ):
                found = True
                break
            time.sleep(0.5)

        assert found, f"[QANoteHelper ERROR] Note '{title}' not found on HomeScreen."
        print(f"[QANoteHelper SUCCESS] Note '{title}' verified present on HomeScreen.")
        return True

    @staticmethod
    def verify_note_absent_on_home(driver: SmartNoteDriver, title: str) -> bool:
        """Verify note is absent on HomeScreen."""
        d = driver.device
        driver.ensure_home_screen()
        absent = False

        for _ in range(6):
            if not (
                d(descriptionContains=title).exists
                or d(textContains=title).exists
                or driver.find_by_text(title, contains=True) is not None
            ):
                absent = True
                break
            time.sleep(0.5)

        assert absent, f"[QANoteHelper ERROR] Note '{title}' is still visible on HomeScreen."
        print(f"[QANoteHelper SUCCESS] Note '{title}' verified absent on HomeScreen.")
        return True

    @staticmethod
    def restore_note_from_trash(driver: SmartNoteDriver, title: str) -> bool:
        """Restore a note from TrashScreen via bottom options sheet (TC-BB-022)."""
        d = driver.device

        # 1. Find note card in Trash
        card = d(descriptionContains=title) or d(textContains=title)
        if not card.exists:
            card = driver.find_by_text(title, contains=True)
        assert card is not None and card.exists, f"[QANoteHelper] Note '{title}' not found in TrashScreen to restore."

        # 2. Tap note card to open bottom sheet options
        print(f"[QANoteHelper] Tapping note '{title}' in TrashScreen to open options...")
        card.click()
        time.sleep(0.8)

        # 3. Tap "Khôi phục ghi chú"
        restore_opt = (
            d(text="Khôi phục ghi chú")
            or d(textContains="Khôi phục")
            or d(descriptionContains="Khôi phục")
            or d(description="Khôi phục ghi chú")
            or d.xpath('//*[contains(@text, "Khôi phục") or contains(@content-desc, "Khôi phục")]')
        )
        assert restore_opt.exists, "[QANoteHelper ERROR] 'Khôi phục ghi chú' option not found in bottom sheet."
        print(f"[QANoteHelper] Tapping 'Khôi phục ghi chú'...")
        restore_opt.click()
        time.sleep(1.2)

        # 4. Verify note is no longer in Trash
        return QANoteHelper.verify_note_absent_in_trash(driver, title)

    @staticmethod
    def permanently_delete_note_from_trash(driver: SmartNoteDriver, title: str) -> bool:
        """Permanently delete a note from TrashScreen (TC-BB-023).

        Handles both Single Note BottomSheet and Multi-Select Dialog confirmations.
        """
        d = driver.device

        # 1. Locate card in Trash
        card = d(descriptionContains=title) or d(textContains=title)
        if not card.exists:
            card = driver.find_by_text(title, contains=True)
        assert card is not None and card.exists, f"[QANoteHelper] Note '{title}' not found in TrashScreen to permanently delete."

        # 2. Tap note card to open bottom sheet
        print(f"[QANoteHelper] Tapping note '{title}' in TrashScreen to open bottom sheet...")
        card.click()
        time.sleep(0.8)

        # 3. Tap "Xóa vĩnh viễn"
        del_forever_opt = (
            d(text="Xóa vĩnh viễn")
            or d(textContains="Xóa vĩnh viễn")
            or d(descriptionContains="Xóa vĩnh viễn")
            or d(description="Xóa vĩnh viễn")
            or d.xpath('//*[contains(@text, "Xóa vĩnh viễn") or contains(@content-desc, "Xóa vĩnh viễn")]')
        )
        if del_forever_opt.exists:
            print(f"[QANoteHelper] Tapping 'Xóa vĩnh viễn' in bottom sheet...")
            del_forever_opt.click()
            time.sleep(0.8)
        else:
            # Fallback: long press to enter selection mode and tap delete forever icon on AppBar
            print(f"[QANoteHelper] Fallback: Long press note for selection mode...")
            d.press("back")
            time.sleep(0.5)
            card.long_click(duration=1.2)
            time.sleep(0.8)
            appbar_del = (
                d(descriptionContains="Xóa vĩnh viễn")
                or d(descriptionContains="delete_forever")
                or d.xpath('//*[contains(@content-desc, "Xóa vĩnh viễn")]')
            )
            if appbar_del.exists:
                appbar_del.click()
                time.sleep(0.8)

        # 4. Check if confirmation dialog ("Xóa vĩnh viễn?" / "Xóa") is displayed
        confirm_btn = (
            d(text="Xóa")
            or d(description="Xóa")
            or d(text="Xác nhận")
            or d(description="Xác nhận")
        )
        if confirm_btn.exists:
            print(f"[QANoteHelper] Confirmation dialog detected. Tapping 'Xóa'...")
            confirm_btn.click()
            time.sleep(1.2)

        # 5. Verify note is no longer in Trash
        return QANoteHelper.verify_note_absent_in_trash(driver, title)

    @staticmethod
    def cleanup_note_safely(driver: SmartNoteDriver, title: str):
        """Best-effort cleanup of test note on HomeScreen or TrashScreen."""
        try:
            d = driver.device
            driver.ensure_home_screen()
            time.sleep(0.5)
            # 1. Cleanup on Home if present
            driver.cleanup_note_via_selection(title)

            # 2. Cleanup in Trash if present
            QANoteHelper.navigate_to_trash(driver)
            card = d(descriptionContains=title) or d(textContains=title)
            if card.exists:
                QANoteHelper.permanently_delete_note_from_trash(driver, title)
            QANoteHelper.navigate_from_trash_to_home(driver)
        except Exception as e:
            print(f"[QANoteHelper Cleanup Notice] Ignored cleanup exception for '{title}': {e}")
            try:
                driver.ensure_home_screen()
            except Exception:
                pass
