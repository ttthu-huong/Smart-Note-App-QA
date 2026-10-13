"""Automation Test Suite for FN-09: Edit Note & Auto-save.

Test Cases:
- TC-BB-019: Chỉnh sửa nội dung ghi chú thành công và cập nhật lên Trang chủ (D01)
- TC-BB-020: Xác minh cơ chế tự động lưu (Auto-save) sau khoảng thời gian ngừng nhập (D01)

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


class TestFN09EditNote:
    @classmethod
    def setup_class(cls):
        cls.driver = SmartNoteDriver()
        cls.d = cls.driver.device
        cls.ensure_home_screen()

    @classmethod
    def ensure_home_screen(cls):
        """Ensure HomeScreen via centralized SmartNoteDriver."""
        return cls.driver.ensure_home_screen()

    @classmethod
    def is_in_editor(cls) -> bool:
        """Check if in EditorScreen via centralized SmartNoteDriver."""
        return cls.driver.is_in_editor()

    def open_note_editor(self):
        """Open EditorScreen via centralized SmartNoteDriver."""
        return self.driver.open_note_editor()

    def open_existing_note(self, title_or_content: str):
        """Open existing note via centralized SmartNoteDriver."""
        return self.driver.open_existing_note(title_or_content)

    def get_title_field(self):
        return self.driver.get_title_field()

    def input_title(self, title: str):
        return self.driver.input_title(title)

    def input_content(self, content: str):
        return self.driver.input_content(content)

    def save_and_exit_editor(self):
        return self.driver.save_and_exit_editor()

    def ensure_base_note(self, title: str, base_content: str):
        """Ensure base note exists via centralized SmartNoteDriver."""
        return self.driver.ensure_test_note(title, base_content)

    def cleanup_note_via_selection(self, title_or_content: str):
        return self.driver.cleanup_note_via_selection(title_or_content)

    
    def test_tc_bb_019_edit_note_content(self):
        """TC-BB-019 (D01): Chỉnh sửa nội dung ghi chú và xác minh cập nhật thành công.
        
        Test Data:
        - Note ban đầu: Title = "Họp Lab", Content = "Nội dung ngắn gọn"
        - Nội dung thêm mới: "[Đã cập nhật lúc 10:00]"
        
        Expected Result:
        - Ứng dụng quay về Trang chủ; thẻ ghi chú phản ánh nội dung mới vừa chỉnh sửa.
        """
        title = "Họp Lab"
        base_content = "Nội dung ngắn gọn"
        update_text = "[Đã cập nhật lúc 10:00]"

        self.ensure_home_screen()
        # Chuẩn bị ghi chú ban đầu trên HomeScreen
        self.ensure_base_note(title, base_content)

        try:
            # 1. Chạm vào ghi chú để mở màn hình soạn thảo
            self.open_existing_note(title)

            # 2. Nhập thêm nội dung mới vào phần văn bản
            self.input_content(update_text)
            time.sleep(0.5)

            # 3. Nhấn nút Quay lại (Back)
            self.save_and_exit_editor()

            # Assertions: Verify note card on HomeScreen reflects updated content
            has_update = False
            for _ in range(12):  # Polling tối đa 6.0s
                # 1. Tìm thẻ qua contentDescription hoặc text chứa chuỗi cập nhật
                if (
                    self.d(descriptionContains=update_text).exists
                    or self.d(textContains=update_text).exists
                ):
                    has_update = True
                    break

                # 2. XPath tìm kiếm trên toàn bộ UI node
                xpath_update = f'//*[contains(@content-desc, "{update_text}") or contains(@text, "{update_text}")]'
                if self.d.xpath(xpath_update).exists:
                    has_update = True
                    break

                # 3. Driver fallback
                if self.driver.find_by_text(update_text, contains=True) is not None:
                    has_update = True
                    break

                time.sleep(0.5)

            # Evidence Capture
            ev_file = self.driver.capture_evidence("evidence/fn09/FN09_TC-BB-019_D01_01.png")
            print(f"\n[TC-BB-019] Evidence saved: {ev_file}")

            print(f"[TC-BB-019] Updated content visible on HomeScreen: {has_update}")
            assert has_update, (
                f"Expected updated content '{update_text}' to be reflected on HomeScreen NoteCard."
            )
        finally:
            # Cleanup test note
            try:
                if self.is_in_editor():
                    self.d.press("back")
                    time.sleep(1.0)
                self.cleanup_note_via_selection(title)
            except Exception as e:
                print(f"[TC-BB-019 Cleanup Notice] Ignored cleanup exception: {e}")

    def test_tc_bb_020_auto_save_after_delay(self):
        """TC-BB-020 (D01): Xác minh nội dung được tự động lưu sau khoảng thời gian ngừng nhập.
        
        Test Data:
        - Note ban đầu: Title = "Ghi chú Auto-save", Content = "Nội dung ban đầu"
        - Nội dung thêm: "- Nội dung kiểm tra tự động lưu"
        
        Expected Result:
        - Nội dung vừa nhập vẫn còn nguyên vẹn sau khi mở lại ghi chú.
        """
        title = "Ghi chú Auto-save"
        base_content = "Nội dung ban đầu"
        auto_save_text = "- Nội dung kiểm tra tự động lưu"

        self.ensure_home_screen()
        # Dọn dẹp note cũ nếu có từ lần chạy trước
        self.cleanup_note_via_selection(title)
        # Chuẩn bị ghi chú ban đầu trên HomeScreen
        self.ensure_base_note(title, base_content)

        try:
            # 1. Mở một ghi chú hiện có
            self.open_existing_note(title)

            # 2. Gõ thêm nội dung mới vào vùng soạn thảo
            self.input_content(auto_save_text)

            # 3. Ngừng nhập khoảng 1.5 giây - 2.0 giây để cơ chế tự động lưu (debounce timer 1000ms) kích hoạt
            print("[TC-BB-020] Pausing 2.0s to allow _autoSaveTimer (1000ms debounce) to fire...")
            time.sleep(2.0)

            # 4. Thoát màn hình ghi chú (nhấn Back thoát về HomeScreen)
            self.save_and_exit_editor()

            # 5. Mở lại ghi chú từ HomeScreen
            print("[TC-BB-020] Reopening note from HomeScreen to verify persisted auto-save content...")
            self.open_existing_note(title)

            # Assertion: Nội dung vừa nhập vẫn còn nguyên vẹn sau khi mở lại ghi chú
            content_retained = False
            for _ in range(12):  # Polling tối đa 6.0s trong EditorScreen
                hierarchy = self.d.dump_hierarchy()
                if (
                    auto_save_text in hierarchy
                    or self.d(descriptionContains=auto_save_text).exists
                    or self.d(textContains=auto_save_text).exists
                ):
                    content_retained = True
                    break
                time.sleep(0.5)

            # Evidence Capture
            ev_file = self.driver.capture_evidence("evidence/fn09/FN09_TC-BB-020_D01_01.png")
            print(f"\n[TC-BB-020] Evidence saved: {ev_file}")

            # Thoát Editor trở về HomeScreen an toàn
            self.save_and_exit_editor()

            print(f"[TC-BB-020] Auto-saved content retained in Editor: {content_retained}")
            assert content_retained, (
                f"Expected auto-saved content '{auto_save_text}' to be retained upon reopening note."
            )
        finally:
            # Cleanup test note
            try:
                if self.is_in_editor():
                    self.d.press("back")
                    time.sleep(1.0)
                self.cleanup_note_via_selection(title)
            except Exception as e:
                print(f"[TC-BB-020 Cleanup Notice] Ignored cleanup exception: {e}")


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
