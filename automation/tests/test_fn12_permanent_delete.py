# -*- coding: utf-8 -*-
"""Automation UI Test Suite for FN-12: Permanent Delete Note from Trash.

Test Cases:
- TC-BB-023: Xóa vĩnh viễn 1 ghi chú khỏi Thùng rác kèm xác nhận (D01)

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


class TestFN12DeleteForever:
    """Test Suite for FN-12: Xóa ghi chú vĩnh viễn."""

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

    def test_tc_bb_023_permanent_delete_from_trash(self):
        """TC-BB-023 (D01): Xóa vĩnh viễn ghi chú khỏi Thùng rác.

        Expected Result:
        - Ghi chú biến mất hoàn toàn khỏi danh sách Thùng rác.
        - Quay lại Trang chủ xác nhận ghi chú không còn tồn tại trên ứng dụng.
        """
        note_title = f"DeleteForever_{int(time.time())}"
        note_content = "Nội dung kiểm thử xóa vĩnh viễn khỏi hệ thống"

        print(f"\n========================================================")
        print(f"[START] TC-BB-023: Permanent Delete Note — '{note_title}'")
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

            # 2. Thao tác chính: Chọn "Xóa vĩnh viễn" và xác nhận hộp thoại nếu có
            print(f"\n--- BƯỚC 4: Chọn 'Xóa vĩnh viễn' và xác nhận trên hộp thoại ---")
            QANoteHelper.permanently_delete_note_from_trash(self.driver, note_title)

            # 3. Xác minh bước 1: Ghi chú biến mất hoàn toàn khỏi Thùng rác
            print(f"\n--- BƯỚC 5: Xác minh ghi chú đã biến mất khỏi Thùng rác ---")
            QANoteHelper.verify_note_absent_in_trash(self.driver, note_title)

            # 4. Điều hướng: Quay lại Trang chủ
            print(f"\n--- BƯỚC 6: Điều hướng quay về Trang chủ qua Drawer ---")
            QANoteHelper.navigate_from_trash_to_home(self.driver)

            # 5. Xác minh bước 2: Ghi chú không tồn tại trên Trang chủ
            print(f"\n--- BƯỚC 7: Xác minh ghi chú không tồn tại trên HomeScreen ---")
            QANoteHelper.verify_note_absent_on_home(self.driver, note_title)

            # 6. Chụp ảnh bằng chứng thực thi thành công
            ev_path = self.driver.capture_evidence("evidence/fn12/FN12_TC-BB-023_D01_01.png")
            print(f"\n[PASS] TC-BB-023 hoàn tất thành công! Bằng chứng đã lưu: {ev_path}")

        finally:
            # Dọn dẹp an toàn: Đảm bảo app ở Trang chủ
            print(f"\n--- DỌN DẸP: Đảm bảo trở về HomeScreen ---")
            try:
                self.driver.ensure_home_screen()
            except Exception as e:
                print(f"[Cleanup Notice] Ignored cleanup warning: {e}")
