"""Automation Test Suite for FN-08: Create New Text Note.

Test Cases:
- TC-BB-016: Tạo ghi chú văn bản có Tiêu đề và Nội dung (D01)
- TC-BB-017: Tạo ghi chú không có tiêu đề nhưng có nội dung (D01)
- TC-BB-018: Tạo ghi chú với cả tiêu đề và nội dung để trống; xác minh ứng dụng không tạo ghi chú rỗng (D01)

Standards: IEEE 829 & ISTQB Manual / Automation Test Execution
Device: Samsung Galaxy S21 FE 5G (Android 14, 1080x2340)
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
from automation import config

class TestFN08CreateNote:
    """Test Suite for FN-08: Tạo Ghi chú văn bản mới."""

    @classmethod
    def setup_class(cls):
        cls.driver = SmartNoteDriver()
        cls.d = cls.driver.device
        cls.ensure_home_screen()

    @classmethod
    def teardown_class(cls):
        pass

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

    def get_home_notes_state(self) -> dict:
        return self.driver.get_home_notes_state()

    def cleanup_note_via_selection(self, title_or_content: str):
        return self.driver.cleanup_note_via_selection(title_or_content)

    
    def test_tc_bb_016_create_note_with_title_and_content(self):
        """TC-BB-016 (D01): Tạo ghi chú văn bản có Tiêu đề và Nội dung.
        
        Test Data:
        - Tiêu đề: "Họp Lab"
        - Nội dung: "Nội dung ngắn gọn"
        
        Expected Result:
        - Thẻ ghi chú hiển thị đầy đủ tiêu đề và nội dung; xuất hiện ở đầu danh sách Trang chủ.
        """
        title = "Họp Lab"
        content = "Nội dung ngắn gọn"

        self.ensure_home_screen()
        # Clean up stale test note if present from previous run
        self.cleanup_note_via_selection(title)

        try:
            # 1. Nhấn nút Tạo mới (+)
            self.open_note_editor()

            # 2. Nhập Tiêu đề
            self.input_title(title)
            time.sleep(0.5)

            # 3. Nhập Nội dung vào QuillEditor
            self.input_content(content)
            time.sleep(0.5)

            # 4. Nhấn nút Quay lại (Back) trên thanh tiêu đề để lưu
            self.save_and_exit_editor()

            # Evidence Capture
            ev_file = self.driver.capture_evidence("evidence/fn08/FN08_TC-BB-016_D01_01.png")
            print(f"\n[TC-BB-016] Evidence saved: {ev_file}")

            # Assertions:
            # Trên Flutter NoteCard (note_card.dart), tiêu đề và nội dung preview được gộp
            # chung trong một semantic container duy nhất dưới dạng:
            # contentDescription = f"{displayTitle}\n{displayContent}" ('Họp Lab\nNội dung ngắn gọn').
            # Polling chờ NoteProvider tải xong dữ liệu từ DB và render thẻ lên HomeScreen.
            has_title = False
            has_content = False

            for _ in range(10):  # Polling tối đa 5.0 giây
                # 1. Tìm thẻ NoteCard chứa đồng thời cả Tiêu đề và Nội dung
                xpath_both = f'//*[contains(@content-desc, "{title}") and contains(@content-desc, "{content}")]'
                if self.d.xpath(xpath_both).exists:
                    has_title = True
                    has_content = True
                    break

                # 2. Tìm thẻ ghi chú theo title và kiểm tra content trong cùng thẻ đó
                card = self.driver.find_by_text(title, contains=True)
                if card is not None and card.exists:
                    has_title = True
                    card_desc = card.info.get("contentDescription", "") or ""
                    card_text = card.info.get("text", "") or ""
                    if content in card_desc or content in card_text:
                        has_content = True
                        break

                time.sleep(0.5)

            # Fallback kiểm tra độc lập nếu cần
            if not has_content:
                has_content = self.driver.find_by_text(content, contains=True) is not None

            print(f"[TC-BB-016] Title visible: {has_title}, Content visible: {has_content}")
            assert has_title, f"Expected note title '{title}' to be visible on HomeScreen."
            assert has_content, f"Expected note content '{content}' to be visible on HomeScreen."
        finally:
            # Post-cleanup: Best-effort cleanup, never fails functional test
            try:
                if self.is_in_editor():
                    self.d.press("back")
                    time.sleep(1.0)
                self.cleanup_note_via_selection(title)
            except Exception as e:
                print(f"[TC-BB-016 Cleanup Notice] Ignored cleanup exception: {e}")

    def test_tc_bb_017_create_note_without_title(self):
        """TC-BB-017 (D01): Tạo ghi chú không có tiêu đề nhưng có nội dung.
        
        Test Data:
        - Tiêu đề: ""
        - Nội dung: "Ý tưởng nhanh không tiêu đề"
        
        Expected Result:
        - Ứng dụng quay về Trang chủ; ghi chú mới vẫn được tạo và xuất hiện trên
          danh sách với phần hiển thị xem trước là đoạn văn bản nội dung.
        """
        content = "Ý tưởng nhanh không tiêu đề"

        self.ensure_home_screen()
        # Clean up stale test note if present from previous run
        self.cleanup_note_via_selection(content)

        try:
            # 1. Mở màn hình soạn thảo ghi chú mới
            self.open_note_editor()

            # 2. Để trống ô Tiêu đề (không nhập gì vào title)

            # 3. Nhập nội dung văn bản vào QuillEditor
            self.input_content(content)
            time.sleep(0.5)

            # 4. Nhấn nút Quay lại (Back)
            self.save_and_exit_editor()

            # Assertions: Verify note is created with content preview on HomeScreen
            # Trên Flutter NoteCard (note_card.dart), khi ghi chú không có tiêu đề,
            # toàn bộ phần preview hiển thị chính là đoạn nội dung văn bản:
            # contentDescription = f"{displayContent}" ('Ý tưởng nhanh không tiêu đề') trên node android.view.View.
            # Dữ liệu được lưu vào SQLite và load lại qua Provider.refreshNotes() bất đồng bộ,
            # do đó áp dụng polling đa tầng (tối đa 6.0s) để đảm bảo thẻ ghi chú đã render hoàn tất.
            has_content = False
            for _ in range(12):  # Polling tối đa 6.0 giây (12 * 0.5s)
                # 1. Tìm trực tiếp qua contentDescription của thẻ ghi chú
                if self.d(descriptionContains=content).exists or self.d(description=content).exists:
                    has_content = True
                    break

                # 2. Tìm qua XPath hỗ trợ cả content-desc và text
                xpath_content = f'//*[contains(@content-desc, "{content}") or contains(@text, "{content}")]'
                if self.d.xpath(xpath_content).exists:
                    has_content = True
                    break

                # 3. Fallback qua driver.find_by_text
                if self.driver.find_by_text(content, contains=True) is not None:
                    has_content = True
                    break

                time.sleep(0.5)

            # Evidence Capture (chụp sau khi danh sách đã tải xong để có hình ảnh NoteCard rõ ràng)
            ev_file = self.driver.capture_evidence("evidence/fn08/FN08_TC-BB-017_D01_01.png")
            print(f"\n[TC-BB-017] Evidence saved: {ev_file}")

            print(f"[TC-BB-017] Content preview visible: {has_content}")
            assert has_content, f"Expected note preview with content '{content}' on HomeScreen."
        finally:
            # Post-cleanup: Best-effort cleanup, never fails functional test
            try:
                if self.is_in_editor():
                    self.d.press("back")
                    time.sleep(1.0)
                self.cleanup_note_via_selection(content)
            except Exception as e:
                print(f"[TC-BB-017 Cleanup Notice] Ignored cleanup exception: {e}")

    def test_tc_bb_018_empty_note_not_created(self):
        """TC-BB-018 (D01): Tạo ghi chú với cả tiêu đề và nội dung để trống;
        xác minh ứng dụng không tạo ghi chú rỗng.
        
        Test Data:
        - Tiêu đề: ""
        - Nội dung: ""
        
        Expected Result:
        - Ứng dụng quay về Trang chủ; không có bất kỳ ghi chú trống nào xuất hiện thêm trên danh sách.
        
        Lưu ý:
        - Auto-save KHÔNG thuộc TC-BB-018 (Auto-save thuộc TC-BB-020).
        """
        self.ensure_home_screen()

        # Capture exact note state on HomeScreen prior to opening editor
        before_state = self.get_home_notes_state()
        print(f"[TC-BB-018] Before state: is_empty={before_state['is_empty']}, note_count={before_state['count']}")

        # 1. Mở màn hình soạn thảo ghi chú mới
        self.open_note_editor()

        # 2. Không nhập bất kỳ ký tự nào vào cả ô Tiêu đề và ô Nội dung
        time.sleep(0.5)

        # 3. Nhấn nút Quay lại (Back)
        self.save_and_exit_editor()

        # Capture exact note state on HomeScreen after returning
        after_state = self.get_home_notes_state()
        print(f"[TC-BB-018] After state: is_empty={after_state['is_empty']}, note_count={after_state['count']}")

        # Evidence Capture
        ev_file = self.driver.capture_evidence("evidence/fn08/FN08_TC-BB-018_D01_01.png")
        print(f"\n[TC-BB-018] Evidence saved: {ev_file}")

        # Assertions:
        # 1. Xác nhận ứng dụng đã thoát Editor và trở về HomeScreen thành công
        not_in_editor = not self.is_in_editor()
        is_back_home = (
            self.driver.find_by_text("Tìm kiếm", contains=True) is not None
            or self.driver.find_by_text("Search", contains=True) is not None
            or self.driver.find_by_text("Chưa có ghi chú nào", contains=True) is not None
            or self.driver.find_by_text("No notes yet", contains=True) is not None
        )
        assert not_in_editor and is_back_home, (
            "Expected application to return to HomeScreen after leaving empty editor."
        )

        # 2. Xác minh không tạo ghi chú rỗng:
        if before_state["is_empty"]:
            # Trường hợp 1: Ban đầu chưa có ghi chú nào -> Trạng thái Empty State phải giữ nguyên
            assert after_state["is_empty"], (
                "Expected empty state placeholder to remain, but it disappeared (an empty note may have been created)."
            )
        else:
            # Trường hợp 2: Ban đầu đã có ghi chú -> Danh sách note không được thêm bất kỳ note mới nào
            assert not after_state["is_empty"], "Unexpected empty state after exiting editor."
            assert after_state["note_items"] == before_state["note_items"], (
                f"Expected note list to be unchanged, but found difference: "
                f"before={before_state['note_items']}, after={after_state['note_items']}"
            )
            assert after_state["count"] == before_state["count"], (
                f"Expected note count to remain {before_state['count']}, but got {after_state['count']}."
            )

        print("[TC-BB-018] Verified: Application did not create any empty note.")

if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
