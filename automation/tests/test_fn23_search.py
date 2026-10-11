"""Automation Test Suite for FN-23: Search Note.

Test Cases:
- TC-BB-026: Tìm kiếm ghi chú theo từ khóa Tiêu đề (D01)
- TC-BB-027: Tìm kiếm ghi chú theo từ khóa Nội dung (D01)
- TC-BB-028: Tìm kiếm với từ khóa không tồn tại / Giao diện rỗng (D01)
- TC-BB-029: Tìm kiếm với chuỗi ký tự đặc biệt / SQL injection pattern / Robustness (D01)

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


class TestFN23Search:
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

    
    def is_in_search(cls) -> bool:
        """Check if currently on SearchScreen."""
        if cls.is_in_editor():
            return False
        return (
            cls.d(descriptionContains="Tìm kiếm ghi chú của bạn").exists
            or cls.d(textContains="Tìm kiếm ghi chú của bạn").exists
            or cls.d(text="Không tìm thấy kết quả").exists
            or cls.d(description="Không tìm thấy kết quả").exists
            or (cls.d(className="android.widget.EditText").exists and not cls.is_in_editor())
        )

    def open_search_screen(self):
        """Open SearchScreen from HomeScreen by tapping the search bar."""
        if self.is_in_search():
            return

        search_bar = (
            self.d(textContains="Tìm kiếm")
            or self.d(descriptionContains="Tìm kiếm")
        )
        if search_bar.exists:
            search_bar.click()
        else:
            self.d.click(540, 260)

        for _ in range(8):
            time.sleep(0.5)
            if self.is_in_search():
                time.sleep(0.5)
                return

        assert self.is_in_search(), "Failed to open SearchScreen from HomeScreen."

    def exit_search_screen(self):
        """Return to HomeScreen from SearchScreen, ensuring search state is cleared."""
        for _ in range(4):
            if not self.is_in_search() and not self.is_in_editor():
                return
            # Tap the back button inside the SearchBar (bounds [42, 129][168, 255])
            # This triggers NoteProvider.clearSearch() so HomeScreen returns to normal mode.
            clicked = False
            for btn in self.d(className="android.widget.Button"):
                try:
                    b = btn.info.get("bounds", {})
                    if b.get("top", 999) < 300 and b.get("left", 999) < 200:
                        btn.click()
                        time.sleep(1.0)
                        clicked = True
                        break
                except Exception:
                    pass
            if not clicked and self.is_in_search():
                self.d.click(105, 192)
                time.sleep(1.0)
            if self.is_in_search():
                self.d.press("back")
                time.sleep(1.0)

    def input_search_query(self, query: str):
        """Input query string into SearchScreen's search TextField."""
        edit = self.d(className="android.widget.EditText")
        assert edit.exists, "Cannot find Search TextField on SearchScreen."
        edit.click()
        time.sleep(0.3)
        edit.set_text(query)
        time.sleep(1.2)  # Wait for search debounce & async DB query

        # Dismiss soft keyboard if visible so results are fully viewable
        if self.d(packageName="com.samsung.android.honeyboard").exists:
            self.d.press("back")
            time.sleep(0.5)

    def open_note_editor(self):
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

    def cleanup_note_via_selection(self, title_or_content: str):
        return self.driver.cleanup_note_via_selection(title_or_content)

    
    def test_tc_bb_026_search_by_title(self):
        """TC-BB-026 (D01): Xác minh tìm kiếm trả kết quả chính xác theo từ khóa Tiêu đề.
        
        Test Data:
        - Note: Title = "Lịch thi học kỳ", Content = "Ôn tập các môn cuối kỳ"
        - Từ khóa: "Lịch thi"
        
        Expected Result:
        - Danh sách tìm kiếm hiển thị thẻ ghi chú có tiêu đề "Lịch thi học kỳ".
        """
        title = "Lịch thi học kỳ"
        content = "Ôn tập các môn cuối kỳ"
        keyword = "Lịch thi"

        self.ensure_home_screen()
        # 1. Đảm bảo note tồn tại trên HomeScreen
        self.ensure_test_note(title, content)

        try:
            # 2. Mở SearchScreen
            self.open_search_screen()

            # 3. Nhập từ khóa tìm kiếm
            self.input_search_query(keyword)

            # Assertions:
            # - Danh sách tìm kiếm hiển thị ghi chú có tiêu đề "Lịch thi học kỳ"
            found_card = False
            for _ in range(10):  # Polling tối đa 5.0s
                if (
                    self.d(descriptionContains=title).exists
                    or self.d(textContains=title).exists
                    or title in self.d.dump_hierarchy()
                ):
                    found_card = True
                    break
                time.sleep(0.5)

            # Evidence Capture
            ev_file = self.driver.capture_evidence("evidence/fn23/FN23_TC-BB-026_D01_01.png")
            print(f"\n[TC-BB-026] Evidence saved: {ev_file}")

            print(f"[TC-BB-026] Note '{title}' found in search results: {found_card}")
            assert found_card, f"Expected search results to display note with title '{title}' for keyword '{keyword}'."
        finally:
            self.exit_search_screen()
            self.cleanup_note_via_selection(title)

    def test_tc_bb_027_search_by_content(self):
        """TC-BB-027 (D01): Xác minh tìm kiếm trả kết quả chính xác theo từ khóa Nội dung.
        
        Test Data:
        - Note: Title = "Tạp vụ", Content = "mua thêm giấy in A4"
        - Từ khóa: "giấy in A4"
        
        Expected Result:
        - Danh sách kết quả hiển thị thẻ ghi chú "Tạp vụ" có chứa đoạn văn bản tương ứng trong phần nội dung.
        """
        title = "Tạp vụ"
        content = "mua thêm giấy in A4"
        keyword = "giấy in A4"

        self.ensure_home_screen()
        # 1. Đảm bảo note tồn tại trên HomeScreen
        self.ensure_test_note(title, content)

        try:
            # 2. Mở SearchScreen
            self.open_search_screen()

            # 3. Nhập từ khóa tìm kiếm
            self.input_search_query(keyword)

            # Assertions:
            # - Danh sách tìm kiếm hiển thị thẻ ghi chú "Tạp vụ" có chứa đoạn text "giấy in A4"
            found_card = False
            for _ in range(10):  # Polling tối đa 5.0s
                hierarchy = self.d.dump_hierarchy()
                if (
                    (self.d(descriptionContains=title).exists or self.d(textContains=title).exists or title in hierarchy)
                    and keyword in hierarchy
                ):
                    found_card = True
                    break
                time.sleep(0.5)

            # Evidence Capture
            ev_file = self.driver.capture_evidence("evidence/fn23/FN23_TC-BB-027_D01_01.png")
            print(f"\n[TC-BB-027] Evidence saved: {ev_file}")

            print(f"[TC-BB-027] Note '{title}' with content '{content}' found: {found_card}")
            assert found_card, f"Expected search results to display note '{title}' containing '{keyword}'."
        finally:
            self.exit_search_screen()
            self.cleanup_note_via_selection(title)

    def test_tc_bb_028_search_non_existent(self):
        """TC-BB-028 (D01): Xác minh giao diện khi tìm kiếm với từ khóa không tồn tại.
        
        Test Data:
        - Từ khóa: "chuoi_khong_ton_tai_999"
        
        Expected Result:
        - Danh sách không có ghi chú nào;
        - Màn hình hiển thị biểu tượng tìm kiếm rỗng kèm thông báo: "Không tìm thấy kết quả" và "Thử từ khóa khác".
        """
        keyword = "chuoi_khong_ton_tai_999"

        self.ensure_home_screen()

        try:
            # 1. Mở SearchScreen
            self.open_search_screen()

            # 2. Nhập từ khóa không tồn tại
            self.input_search_query(keyword)

            # Assertions:
            # - Màn hình hiển thị "Không tìm thấy kết quả"
            empty_title_found = False
            for _ in range(10):  # Polling tối đa 5.0s
                if (
                    self.d(textContains="Không tìm thấy kết quả").exists
                    or self.d(descriptionContains="Không tìm thấy kết quả").exists
                    or "Không tìm thấy kết quả" in self.d.dump_hierarchy()
                ):
                    empty_title_found = True
                    break
                time.sleep(0.5)

            # - Màn hình hiển thị "Thử từ khóa khác"
            hierarchy = self.d.dump_hierarchy()
            empty_subtitle_found = (
                "Thử từ khóa khác" in hierarchy
                or self.d(textContains="Thử từ khóa khác").exists
                or self.d(descriptionContains="Thử từ khóa khác").exists
            )

            # Evidence Capture
            ev_file = self.driver.capture_evidence("evidence/fn23/FN23_TC-BB-028_D01_01.png")
            print(f"\n[TC-BB-028] Evidence saved: {ev_file}")

            print(f"[TC-BB-028] Empty search title visible: {empty_title_found}")
            print(f"[TC-BB-028] Empty search subtitle visible: {empty_subtitle_found}")

            assert empty_title_found, "Expected empty search title 'Không tìm thấy kết quả' to be displayed."
            assert empty_subtitle_found, "Expected empty search subtitle 'Thử từ khóa khác' to be displayed."
        finally:
            self.exit_search_screen()

    def test_tc_bb_029_search_special_characters(self):
        """TC-BB-029 (D01): Kiểm tra khả năng xử lý chuỗi chứa ký tự đặc biệt / SQL injection pattern.
        
        Test Data:
        - Từ khóa: "' OR 1=1 -- % _ @#$"
        
        Expected Result:
        - Ứng dụng hoạt động ổn định, không bị đơ hoặc đóng đột ngột;
        - Hiển thị giao diện "Không tìm thấy kết quả" nếu không có ghi chú khớp.
        """
        keyword = "' OR 1=1 -- % _ @#$"

        self.ensure_home_screen()

        try:
            # 1. Mở SearchScreen
            self.open_search_screen()

            # 2. Nhập chuỗi ký tự đặc biệt
            self.input_search_query(keyword)

            # Assertions:
            # 1. Ứng dụng vẫn chạy bình thường, không crash, vẫn ở SearchScreen
            is_alive = self.is_in_search()
            assert is_alive, "Application crashed or closed SearchScreen upon entering special characters."

            # 2. Hiển thị giao diện rỗng an toàn: "Không tìm thấy kết quả"
            empty_state_found = False
            for _ in range(10):  # Polling tối đa 5.0s
                hierarchy = self.d.dump_hierarchy()
                if (
                    "Không tìm thấy kết quả" in hierarchy
                    or self.d(textContains="Không tìm thấy kết quả").exists
                    or self.d(descriptionContains="Không tìm thấy kết quả").exists
                ):
                    empty_state_found = True
                    break
                time.sleep(0.5)

            # Evidence Capture
            ev_file = self.driver.capture_evidence("evidence/fn23/FN23_TC-BB-029_D01_01.png")
            print(f"\n[TC-BB-029] Evidence saved: {ev_file}")

            print(f"[TC-BB-029] App remained alive: {is_alive}")
            print(f"[TC-BB-029] Empty state safely displayed: {empty_state_found}")

            assert empty_state_found, (
                "Expected application to safely display empty state 'Không tìm thấy kết quả' "
                "for special character query."
            )
        finally:
            self.exit_search_screen()


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
