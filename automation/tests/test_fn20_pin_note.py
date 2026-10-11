"""Automation Test Suite for FN-20: Pin / Unpin Note.

Test Cases:
- TC-BB-024: Ghim ghi chú lên khu vực ưu tiên trên Trang chủ (D01)
- TC-BB-025: Bỏ ghim đưa ghi chú trở về danh sách thông thường (D01)

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


class TestFN20PinNote:
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

    def get_title_field(self):
        return self.driver.get_title_field()

    def input_title(self, title: str):
        return self.driver.input_title(title)

    def input_content(self, content: str):
        return self.driver.input_content(content)

    def save_and_exit_editor(self):
        return self.driver.save_and_exit_editor()

    def ensure_test_note(self, title: str, content: str):
        return self.driver.ensure_test_note(title, content)

    def select_note_by_long_press(self, title_or_content: str) -> bool:
        return self.driver.select_note_by_long_press(title_or_content)

    
    def toggle_pin_via_toolbar(self):
        """Click the Pin/Unpin action button on Selection Mode AppBar."""
        pin_btn = (
            self.d(descriptionContains="Ghim/Bỏ ghim hàng loạt")
            or self.d(descriptionContains="Pin/Unpin")
            or self.d(description="Ghim/Bỏ ghim hàng loạt")
        )
        assert pin_btn.exists, "Cannot find 'Ghim/Bỏ ghim hàng loạt' button in Selection Mode AppBar."
        pin_btn.click()
        time.sleep(1.2)

    def is_pinned_section_visible(self) -> bool:
        """Check if 'Được ghim' / 'Pinned' section header is visible on HomeScreen."""
        return (
            self.d(text="Được ghim").exists
            or self.d(description="Được ghim").exists
            or self.d(text="Pinned").exists
            or self.d(description="Pinned").exists
            or self.d.xpath('//*[@text="Được ghim" or @content-desc="Được ghim"]').exists
        )

    def cleanup_note_via_selection(self, title_or_content: str):
        return self.driver.cleanup_note_via_selection(title_or_content)

    
    def test_tc_bb_024_pin_note(self):
        """TC-BB-024 (D01): Ghim ghi chú lên khu vực ưu tiên trên Trang chủ.
        
        Test Data:
        - Note: Title = "Ghi chú Test Ghim", Content = "Nội dung kiểm tra ghim"
        - Thao tác: Ghim ghi chú qua thanh công cụ
        
        Expected Result:
        - Trang chủ xuất hiện tiêu đề phân vùng 'Được ghim';
        - Thẻ ghi chú di chuyển lên nằm trong khu vực 'Được ghim' ở phía trên cùng.
        """
        title = "Ghi chú Test Ghim"
        content = "Nội dung kiểm tra ghim"

        self.ensure_home_screen()
        # 1. Đảm bảo ghi chú test tồn tại trên HomeScreen
        self.ensure_test_note(title, content)

        # Nếu note đang bị ghim từ trước, bỏ ghim để chuẩn bị precondition chuẩn
        if self.is_pinned_section_visible():
            # Kiểm tra xem có phải chính note này đang ghim không
            pinned_header = self.d(text="Được ghim") or self.d(description="Được ghim")
            pinned_y = pinned_header.info.get("bounds", {}).get("top", 0) if pinned_header.exists else 0
            card = self.d(descriptionContains=title) or self.d(textContains=title)
            card_y = card.info.get("bounds", {}).get("top", 0) if card.exists else 0
            others_header = self.d(text="Khác") or self.d(description="Khác") or self.d(text="Others")
            others_top = others_header.info.get("bounds", {}).get("top", 9999) if others_header.exists else 9999
            if card_y > pinned_y and card_y < others_top:
                print("[Precondition] Note is currently pinned. Unpinning first...")
                if self.select_note_by_long_press(title):
                    self.toggle_pin_via_toolbar()
                    time.sleep(1.0)

        try:
            # 1. Nhấn giữ thẻ ghi chú để kích hoạt Selection Mode
            is_selected = self.select_note_by_long_press(title)
            assert is_selected, f"Failed to activate Selection Mode for note '{title}'."

            # 2. Nhấn biểu tượng Ghim (Ghim/Bỏ ghim hàng loạt) trên thanh công cụ
            self.toggle_pin_via_toolbar()

            # Assertions:
            # 1. Trang chủ xuất hiện tiêu đề phân vùng "Được ghim"
            has_pinned_section = False
            for _ in range(10):  # Polling tối đa 5.0s
                if self.is_pinned_section_visible():
                    has_pinned_section = True
                    break
                time.sleep(0.5)

            # 2. Thẻ ghi chú nằm trong khu vực "Được ghim" ở phía trên cùng
            card_in_pinned_section = False
            if has_pinned_section:
                pinned_header = (
                    self.d(text="Được ghim")
                    or self.d(description="Được ghim")
                    or self.d(text="Pinned")
                    or self.d(description="Pinned")
                )
                ph_bounds = pinned_header.info.get("bounds", {})
                ph_bottom = ph_bounds.get("bottom", 0)

                card = self.d(descriptionContains=title) or self.d(textContains=title)
                if card.exists:
                    card_bounds = card.info.get("bounds", {})
                    card_top = card_bounds.get("top", 0)
                    # Thẻ ghi chú nằm bên dưới header "Được ghim" và nằm ở khu vực phía trên
                    if card_top >= ph_bottom - 20:
                        # Nếu có header "Khác", thẻ ghi chú phải nằm trên header "Khác"
                        others_header = self.d(text="Khác") or self.d(description="Khác") or self.d(text="Others")
                        if others_header.exists:
                            others_top = others_header.info.get("bounds", {}).get("top", 9999)
                            card_in_pinned_section = card_top < others_top
                        else:
                            card_in_pinned_section = True

            # Evidence Capture
            ev_file = self.driver.capture_evidence("evidence/fn20/FN20_TC-BB-024_D01_01.png")
            print(f"\n[TC-BB-024] Evidence saved: {ev_file}")

            print(f"[TC-BB-024] 'Được ghim' header visible: {has_pinned_section}")
            print(f"[TC-BB-024] Note is inside pinned section: {card_in_pinned_section}")

            assert has_pinned_section, "Expected 'Được ghim' section header to appear on HomeScreen."
            assert card_in_pinned_section, f"Expected note '{title}' to be located inside 'Được ghim' section."
        except Exception as e:
            # Dismiss selection mode if error occurred while in selection
            cancel_btn = self.d(descriptionContains="Hủy chọn") or self.d(descriptionContains="Cancel")
            if cancel_btn.exists:
                try:
                    cancel_btn.click()
                except Exception:
                    pass
            raise e

    def test_tc_bb_025_unpin_note(self):
        """TC-BB-025 (D01): Bỏ ghim đưa ghi chú trở về danh sách thông thường.
        
        Test Data:
        - Note: Title = "Ghi chú Test Ghim", Content = "Nội dung kiểm tra ghim"
        - Thao tác: Bỏ ghim ghi chú qua thanh công cụ
        
        Expected Result:
        - Thẻ ghi chú chuyển xuống phân vùng ghi chú thông thường bên dưới;
        - Nếu không còn ghi chú nào được ghim, tiêu đề 'Được ghim' tự động ẩn đi.
        """
        title = "Ghi chú Test Ghim"
        content = "Nội dung kiểm tra ghim"

        self.ensure_home_screen()
        # Precondition: Đảm bảo note tồn tại
        self.ensure_test_note(title, content)

        # Precondition: Đảm bảo note đang nằm trong phân vùng "Được ghim"
        if not self.is_pinned_section_visible():
            print("[Precondition] Note is not yet pinned for TC-BB-025. Pinning it first...")
            if self.select_note_by_long_press(title):
                self.toggle_pin_via_toolbar()
                time.sleep(1.0)
            assert self.is_pinned_section_visible(), (
                "Precondition failed: Unable to pin note for TC-BB-025."
            )

        try:
            # 1. Nhấn giữ chọn thẻ ghi chú đang được ghim
            is_selected = self.select_note_by_long_press(title)
            assert is_selected, f"Failed to activate Selection Mode for pinned note '{title}'."

            # 2. Nhấn biểu tượng Bỏ ghim (Ghim/Bỏ ghim hàng loạt) trên thanh công cụ
            self.toggle_pin_via_toolbar()

            # Assertions:
            # 1. Thẻ ghi chú vẫn tồn tại trên HomeScreen
            has_note_on_home = False
            for _ in range(8):
                card = self.d(descriptionContains=title) or self.d(textContains=title)
                if card.exists:
                    has_note_on_home = True
                    break
                time.sleep(0.5)

            # 2. Tiêu đề "Được ghim" tự động ẩn đi hoàn toàn (vì đây là note duy nhất được ghim)
            pinned_header_disappeared = False
            for _ in range(8):
                if not self.is_pinned_section_visible():
                    pinned_header_disappeared = True
                    break
                time.sleep(0.5)

            # Evidence Capture
            ev_file = self.driver.capture_evidence("evidence/fn20/FN20_TC-BB-025_D01_01.png")
            print(f"\n[TC-BB-025] Evidence saved: {ev_file}")

            print(f"[TC-BB-025] Note exists on HomeScreen: {has_note_on_home}")
            print(f"[TC-BB-025] 'Được ghim' header disappeared: {pinned_header_disappeared}")

            assert has_note_on_home, f"Expected note '{title}' to remain on HomeScreen after unpinning."
            assert pinned_header_disappeared, (
                "Expected 'Được ghim' section header to disappear when no notes remain pinned."
            )
        finally:
            # Cleanup test note
            try:
                self.cleanup_note_via_selection(title)
            except Exception as e:
                print(f"[TC-BB-025 Cleanup Notice] Ignored cleanup exception: {e}")


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
