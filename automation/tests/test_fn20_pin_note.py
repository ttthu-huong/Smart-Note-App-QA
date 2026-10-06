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
        """Precondition: Ensure device is at HomeScreen."""
        cls.driver.ensure_device_ready()

        # Retry loop to dismiss any open modals, keyboards, or editor screens
        for _ in range(5):
            # Dismiss selection mode if active
            cancel_btn = (
                cls.driver.find_by_text("Hủy chọn", contains=True)
                or cls.driver.find_by_text("Cancel selection", contains=True)
            )
            if cancel_btn is not None:
                try:
                    cancel_btn.click()
                    time.sleep(0.5)
                except Exception:
                    pass

            # Check if HomeScreen is visible via primary anchors
            has_search = (
                cls.driver.find_by_text("Tìm kiếm", contains=True) is not None
                or cls.driver.find_by_text("Search", contains=True) is not None
            )
            has_empty = (
                cls.driver.find_by_text("Chưa có ghi chú nào", contains=True) is not None
                or cls.driver.find_by_text("No notes yet", contains=True) is not None
            )
            not_login = (
                cls.driver.find_by_text("Đăng ký ngay") is None
                and cls.driver.find_by_text("Quên mật khẩu?") is None
            )

            if (has_search or has_empty) and not_login and not cls.is_in_editor():
                return True

            # If inside editor, modal sheet, or scrim, press back to dismiss
            cls.d.press("back")
            time.sleep(1.0)

        is_home = (
            cls.driver.find_by_text("Tìm kiếm", contains=True) is not None
            or cls.driver.find_by_text("Search", contains=True) is not None
            or cls.driver.find_by_text("Chưa có ghi chú nào", contains=True) is not None
            or cls.driver.find_by_text("No notes yet", contains=True) is not None
        )
        assert is_home, (
            "Precondition failed: App is not on HomeScreen. "
            "Please ensure user is logged in and app is launched to HomeScreen."
        )

    @classmethod
    def is_in_editor(cls) -> bool:
        """Check if currently on EditorScreen via robust Flutter semantics."""
        return (
            cls.d(description="Ghi chú").exists
            or cls.d(description="Note").exists
            or cls.d(description="AI Trợ lý").exists
            or cls.d(description="AI Assistant").exists
            or cls.d(description="Định dạng").exists
            or cls.d(description="Format").exists
            or cls.d(description="Màu sắc").exists
            or cls.d(description="Color").exists
            or cls.d(description="Khóa ghi chú").exists
            or cls.d(description="Lock note").exists
            or cls.d(description="Mở khóa ghi chú").exists
            or cls.d(description="Ghim").exists
            or cls.d(description="Nhắc nhở").exists
            or cls.d(text="Tiêu đề").exists
            or cls.d(text="Title").exists
            or cls.d(description="Tiêu đề").exists
            or cls.d(description="Title").exists
        )

    def open_note_editor(self):
        """Locate FAB in bottom-right corner and open EditorScreen."""
        cancel_btn = (
            self.driver.find_by_text("Hủy chọn", contains=True)
            or self.driver.find_by_text("Cancel selection", contains=True)
        )
        if cancel_btn is not None:
            try:
                cancel_btn.click()
                time.sleep(0.5)
            except Exception:
                pass

        fab_btn = None
        candidates = []
        for btn in self.d(className="android.widget.Button"):
            try:
                info = btn.info
                desc = (info.get("contentDescription", "") or "").strip()
                if "Hoàn tác" in desc or "Undo" in desc:
                    continue
                b = info.get("bounds", {})
                if b.get("right", 0) > 700 and b.get("bottom", 0) > 1800:
                    candidates.append((b.get("bottom", 0), b, btn))
            except Exception:
                pass

        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            fab_btn = candidates[0][2]

        if fab_btn is not None:
            fab_btn.click()
        else:
            self.d.click(964, 2185)

        for _ in range(8):
            time.sleep(0.5)
            if self.is_in_editor():
                return

        self.d.click(964, 2185)
        time.sleep(1.5)
        assert self.is_in_editor(), "Failed to open EditorScreen after tapping FAB."

    def get_title_field(self):
        """Locate Title input field dynamically."""
        el = self.driver.find_by_text("Tiêu đề") or self.driver.find_by_text("Title")
        if el is not None:
            return el

        for field in self.d(className="android.widget.EditText"):
            try:
                top = field.info.get("bounds", {}).get("top", 9999)
                if top < 500:
                    return field
            except Exception:
                pass
        return None

    def input_title(self, title: str):
        """Input title text into the Title TextField."""
        title_el = self.get_title_field()
        if title_el is not None:
            title_el.click()
            time.sleep(0.3)
            title_el.set_text(title)
        else:
            self.d.click(200, 290)
            time.sleep(0.3)
            focused = self.d(focused=True)
            if focused.exists:
                focused.set_text(title)
            else:
                edits = self.d(className="android.widget.EditText")
                if edits.exists:
                    edits[0].set_text(title)

    def input_content(self, content: str):
        """Input content text into QuillEditor via native pasteClipboard."""
        if not content:
            return

        content_placeholder = self.d(description="Ghi chú") or self.d(text="Ghi chú")
        if content_placeholder.exists:
            content_placeholder.click()
        else:
            self.d.click(540, 520)
        time.sleep(0.5)

        self.d.set_clipboard(content)
        time.sleep(0.3)
        try:
            self.d.jsonrpc.pasteClipboard()
        except Exception:
            time.sleep(0.3)
            self.d.jsonrpc.pasteClipboard()
        time.sleep(0.5)

        content_in_editor = False
        for _ in range(6):
            if self.d(descriptionContains=content).exists or content in self.d.dump_hierarchy():
                content_in_editor = True
                break
            time.sleep(0.5)

        if not content_in_editor:
            self.d.click(540, 520)
            time.sleep(0.3)
            self.d.set_clipboard(content)
            time.sleep(0.2)
            try:
                self.d.jsonrpc.pasteClipboard()
            except Exception:
                pass
            time.sleep(0.5)
            if self.d(descriptionContains=content).exists or content in self.d.dump_hierarchy():
                content_in_editor = True

        assert content_in_editor, (
            f"[INPUT FAILURE] Content '{content}' was not entered into QuillEditor."
        )

    def save_and_exit_editor(self):
        """Save note and return to HomeScreen via AppBar leading back button or system back."""
        self.d.click(75, 170)
        time.sleep(1.5)

        if self.is_in_editor():
            self.d.press("back")
            time.sleep(1.5)

        if self.is_in_editor():
            self.d.press("back")
            time.sleep(1.5)

    def ensure_test_note(self, title: str, content: str):
        """Ensure a test note exists on HomeScreen. If not, create via UI."""
        card = self.d(descriptionContains=title) or self.d(textContains=title)
        xpath_expr = f'//*[contains(@content-desc, "{title}") or contains(@text, "{title}")]'
        if not card.exists and not self.d.xpath(xpath_expr).exists:
            print(f"[Precondition] Note '{title}' not found on HomeScreen. Creating it...")
            self.open_note_editor()
            self.input_title(title)
            self.input_content(content)
            self.save_and_exit_editor()
            time.sleep(1.0)
            assert (
                self.d(descriptionContains=title).exists
                or self.d(textContains=title).exists
                or self.d.xpath(xpath_expr).exists
            ), f"Failed to create test note '{title}'."

    def select_note_by_long_press(self, title_or_content: str) -> bool:
        """Long press a NoteCard to enter Selection Mode."""
        # Dismiss existing selection mode if any
        cancel_btn = (
            self.d(descriptionContains="Hủy chọn")
            or self.d(descriptionContains="Cancel")
            or self.d(textContains="Hủy chọn")
        )
        if cancel_btn.exists:
            try:
                cancel_btn.click()
                time.sleep(0.5)
            except Exception:
                pass

        card = (
            self.d(descriptionContains=title_or_content)
            or self.d(textContains=title_or_content)
        )
        if not card.exists:
            xpath_expr = f'//*[contains(@content-desc, "{title_or_content}") or contains(@text, "{title_or_content}")]'
            if self.d.xpath(xpath_expr).exists:
                card = self.d.xpath(xpath_expr)

        assert card.exists, f"Cannot find NoteCard '{title_or_content}' to select."

        b = card.info.get("bounds", {})
        cx = (b.get("left", 0) + b.get("right", 0)) // 2
        cy = (b.get("top", 0) + b.get("bottom", 0)) // 2

        self.d.touch.down(cx, cy)
        time.sleep(1.2)
        self.d.touch.up(cx, cy)
        time.sleep(0.8)

        is_selection = (
            self.d(descriptionContains="Hủy chọn").exists
            or self.d(descriptionContains="Cancel").exists
            or self.d(descriptionContains="đã chọn").exists
            or self.d(descriptionContains="selected").exists
        )
        return is_selection

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
        """Safely clean up test note from HomeScreen using Selection Mode (Long-press -> Trash)."""
        try:
            if self.is_in_editor():
                self.d.press("back")
                time.sleep(1.0)

            cancel_btn = (
                self.d(descriptionContains="Hủy chọn")
                or self.d(descriptionContains="Cancel")
                or self.d(textContains="Hủy chọn")
            )
            if cancel_btn.exists:
                try:
                    cancel_btn.click()
                    time.sleep(0.5)
                except Exception:
                    pass

            card = (
                self.d(descriptionContains=title_or_content)
                or self.d(textContains=title_or_content)
            )
            if not card.exists:
                return

            b = card.info.get("bounds", {})
            if b:
                cx = (b.get("left", 0) + b.get("right", 0)) // 2
                cy = (b.get("top", 0) + b.get("bottom", 0)) // 2
                self.d.touch.down(cx, cy)
                time.sleep(1.2)
                self.d.touch.up(cx, cy)
                time.sleep(0.8)

            is_selection_mode = (
                self.d(descriptionContains="Hủy chọn").exists
                or self.d(descriptionContains="Cancel").exists
                or self.d(descriptionContains="đã chọn").exists
                or self.d(descriptionContains="selected").exists
            )

            if is_selection_mode:
                trash_btn = (
                    self.d(descriptionContains="thùng rác")
                    or self.d(descriptionContains="Trash")
                    or self.d(descriptionContains="trash")
                )
                if trash_btn.exists:
                    trash_btn.click()
                    time.sleep(1.2)
                else:
                    cancel_btn = self.d(descriptionContains="Hủy chọn") or self.d(descriptionContains="Cancel")
                    if cancel_btn.exists:
                        cancel_btn.click()
                    time.sleep(0.5)
            elif self.is_in_editor():
                self.d.press("back")
                time.sleep(1.0)
        except Exception as e:
            print(f"[Cleanup Notice] Cleanup for '{title_or_content}' skipped or error: {e}")
            try:
                if self.is_in_editor():
                    self.d.press("back")
            except Exception:
                pass

    # =========================================================================
    # TEST CASES FOR FN-20
    # =========================================================================

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
            if card_y > pinned_y and card_y < 1200:
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
