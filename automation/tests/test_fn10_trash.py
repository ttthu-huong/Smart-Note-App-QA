# -*- coding: utf-8 -*-
"""Automation UI Test Suite for FN-10: Move Note to Trash.

Test Cases:
- TC-BB-021: Chuyển 1 ghi chú vào Thùng rác từ Trang chủ (D01)

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


class TestFN10Trash:
    """Test Suite for FN-10: Chuyển ghi chú vào thùng rác."""

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

    def test_tc_bb_021_move_note_to_trash(self):
        """TC-BB-021 (D01): Chuyển ghi chú vào thùng rác từ HomeScreen.

        Expected Result:
        - Thẻ ghi chú biến mất khỏi danh sách Trang chủ.
        - Mở Thùng rác thấy ghi chú xuất hiện với đúng thông tin tiêu đề/nội dung.
        """
        note_title = f"TrashTest_{int(time.time())}"
        note_content = "Nội dung kiểm thử chuyển vào thùng rác"

        print(f"\n========================================================")
        print(f"[START] TC-BB-021: Move Note to Trash — '{note_title}'")
        print(f"========================================================")

        try:
            # 1. Tiền điều kiện: Tạo ghi chú kiểm thử cô lập trên HomeScreen
            print(f"\n--- BƯỚC 1: Tạo ghi chú kiểm thử cô lập trên HomeScreen ---")
            QANoteHelper.create_test_note(self.driver, note_title, note_content, poll_timeout=6.0)

            # 2. Thao tác xóa: Nhấn giữ thẻ ghi chú để bật Selection Mode và nhấn Thùng rác
            print(f"\n--- BƯỚC 2: Chọn ghi chú và nhấn biểu tượng Thùng rác trên AppBar ---")
            QANoteHelper.move_note_to_trash_from_home(self.driver, note_title)

            # 3. Xác minh bước 1: Thẻ ghi chú biến mất khỏi Trang chủ
            print(f"\n--- BƯỚC 3: Xác minh ghi chú đã biến mất khỏi HomeScreen ---")
            QANoteHelper.verify_note_absent_on_home(self.driver, note_title)

            # 4. Điều hướng: Mở ngăn kéo (Drawer) và chọn "Thùng rác"
            print(f"\n--- BƯỚC 4: Điều hướng vào màn hình Thùng rác qua Drawer ---")
            QANoteHelper.navigate_to_trash(self.driver)

            # 5. Xác minh bước 2: Ghi chú xuất hiện trong Thùng rác
            print(f"\n--- BƯỚC 5: Xác minh ghi chú hiện diện trong Thùng rác ---")
            QANoteHelper.verify_note_in_trash(self.driver, note_title, poll_timeout=5.0)

            # 6. Chụp ảnh bằng chứng thực thi thành công
            ev_path = self.driver.capture_evidence("evidence/fn10/FN10_TC-BB-021_D01_01.png")
            print(f"\n[PASS] TC-BB-021 hoàn tất thành công! Bằng chứng đã lưu: {ev_path}")

        finally:
            # Dọn dẹp an toàn (Best-effort cleanup)
            print(f"\n--- DỌN DẸP: Xóa sạch dữ liệu test cô lập '{note_title}' ---")
            try:
                QANoteHelper.permanently_delete_note_from_trash(self.driver, note_title)
            except Exception as e:
                print(f"[Cleanup Notice] Ignored cleanup warning: {e}")
            try:
                QANoteHelper.navigate_from_trash_to_home(self.driver)
            except Exception:
                self.driver.ensure_home_screen()
