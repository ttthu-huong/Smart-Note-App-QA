# -*- coding: utf-8 -*-
"""Automation UI Test Suite for FN-11: Restore Note from Trash.

Test Cases:
- TC-BB-022: Khôi phục 1 ghi chú từ Thùng rác về Trang chủ (D01)

Standards: IEEE 829 & ISTQB Manual / Automation Execution
Device: Samsung Galaxy S21 FE 5G (Android 14)
Framework: Python 3.13 + pytest + uiautomator2 + ADB
"""

import sys
import os
import time
import pytest

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from automation.core.device import SmartNoteDriver
from automation.core.qa_note_helper import QANoteHelper


class TestFN11Restore:
    """Test Suite for FN-11: Khôi phục ghi chú từ thùng rác."""

    @classmethod
    def setup_class(cls):
        cls.driver = SmartNoteDriver()
        cls.d = cls.driver.device
        cls.driver.ensure_home_screen()

    @classmethod
    def teardown_class(cls):
        try:
            cls.driver.ensure_home_screen()
        except Exception as e:
            print(f"[Teardown] Warning: {e}")

    def setup_method(self, method):
        """Ensure clean HomeScreen before each test."""
        self.driver.ensure_home_screen()

    def teardown_method(self, method):
        """Safe post-test state reset."""
        try:
            self.driver.ensure_home_screen()
        except Exception:
            pass

    def test_tc_bb_022_restore_note_from_trash(self):
        """TC-BB-022 (D01): Khôi phục ghi chú từ Thùng rác về Trang chủ.

        Expected Result:
        - Ghi chú biến mất khỏi màn hình Thùng rác.
        - Quay về Trang chủ thấy ghi chú đã xuất hiện lại đầy đủ và nguyên vẹn.
        """
        note_title = f"RestoreTest_{int(time.time())}"
        note_content = "Nội dung kiểm thử khôi phục từ thùng rác"

        print(f"\n========================================================")
        print(f"[START] TC-BB-022: Restore Note from Trash — '{note_title}'")
        print(f"========================================================")

        try:
            # 1. Tiền điều kiện: Chuẩn bị 1 ghi chú kiểm thử nằm sẵn trong Thùng rác
            print(f"\n--- BƯỚC 1: Tạo ghi chú kiểm thử cô lập trên HomeScreen ---")
            QANoteHelper.create_test_note(self.driver, note_title, note_content, poll_timeout=6.0)

            print(f"\n--- BƯỚC 2: Chuyển ghi chú vào Thùng rác để tạo tiền điều kiện ---")
            QANoteHelper.move_note_to_trash_from_home(self.driver, note_title)

            print(f"\n--- BƯỚC 3: Mở Thùng rác và xác nhận ghi chú đã có trong Thùng rác ---")
            QANoteHelper.navigate_to_trash(self.driver)
            QANoteHelper.verify_note_in_trash(self.driver, note_title, poll_timeout=5.0)

            # 2. Thao tác chính: Mở menu tùy chọn dưới đáy và bấm "Khôi phục ghi chú"
            print(f"\n--- BƯỚC 4: Chạm vào ghi chú trong Thùng rác và chọn 'Khôi phục ghi chú' ---")
            QANoteHelper.restore_note_from_trash(self.driver, note_title)

            # 3. Xác minh bước 1: Ghi chú biến mất khỏi Thùng rác
            print(f"\n--- BƯỚC 5: Xác minh ghi chú đã biến mất khỏi Thùng rác ---")
            QANoteHelper.verify_note_absent_in_trash(self.driver, note_title)

            # 4. Điều hướng: Quay lại Trang chủ
            print(f"\n--- BƯỚC 6: Điều hướng quay về Trang chủ qua Drawer ---")
            QANoteHelper.navigate_from_trash_to_home(self.driver)

            # 5. Xác minh bước 2: Ghi chú xuất hiện lại trên Trang chủ
            print(f"\n--- BƯỚC 7: Xác minh ghi chú tái xuất hiện trên HomeScreen ---")
            QANoteHelper.verify_note_on_home(self.driver, note_title, poll_timeout=6.0)

            # 6. Chụp ảnh bằng chứng thực thi thành công
            ev_path = self.driver.capture_evidence("evidence/fn11/FN11_TC-BB-022_D01_01.png")
            print(f"\n[PASS] TC-BB-022 hoàn tất thành công! Bằng chứng đã lưu: {ev_path}")

        finally:
            # Dọn dẹp an toàn ghi chú test sau khi khôi phục
            print(f"\n--- DỌN DẸP: Xóa ghi chú test cô lập '{note_title}' trên HomeScreen ---")
            try:
                self.driver.ensure_home_screen()
                self.driver.cleanup_note_via_selection(note_title)
            except Exception as e:
                print(f"[Cleanup Notice] Ignored cleanup warning: {e}")
