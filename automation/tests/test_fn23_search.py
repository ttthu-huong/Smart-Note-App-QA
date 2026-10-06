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
        """Precondition: Ensure device is at HomeScreen."""
        cls.driver.ensure_device_ready()

        # Retry loop to dismiss any open modals, keyboards, search screens, or editor screens
        for _ in range(6):
            if cls.is_in_search():
                cls.d.click(105, 192)
                time.sleep(1.0)
                if cls.is_in_search():
                    cls.d.press("back")
                    time.sleep(0.8)

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

            if (has_search or has_empty) and not_login and not cls.is_in_editor() and not cls.is_in_search():
                return True

            cls.d.press("back")
            time.sleep(0.8)

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
            or cls.d(description="Nhắc nhở").exists
            or cls.d(text="Tiêu đề").exists
            or cls.d(text="Title").exists
            or cls.d(description="Tiêu đề").exists
            or cls.d(description="Title").exists
        )

    @classmethod
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
        # Check if already present on HomeScreen with polling
        for _ in range(4):
            if (
                self.d(descriptionContains=title).exists
                or self.d(textContains=title).exists
                or title in self.d.dump_hierarchy()
            ):
                return
            time.sleep(0.5)

        print(f"[Precondition] Note '{title}' not found on HomeScreen. Creating it...")
        self.open_note_editor()
        self.input_title(title)
        self.input_content(content)
        self.save_and_exit_editor()

        # Polling wait for note to render on HomeScreen
        created = False
        for _ in range(12):  # Polling up to 6.0 seconds
            if (
                self.d(descriptionContains=title).exists
                or self.d(textContains=title).exists
                or title in self.d.dump_hierarchy()
            ):
                created = True
                break
            time.sleep(0.5)

        assert created, f"Failed to create test note '{title}'."

    def cleanup_note_via_selection(self, title_or_content: str):
        """Safely clean up test note from HomeScreen using Selection Mode (Long-press -> Trash)."""
        try:
            self.ensure_home_screen()

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
            elif self.is_in_editor() or self.is_in_search():
                self.d.press("back")
                time.sleep(1.0)
        except Exception as e:
            print(f"[Cleanup Notice] Cleanup for '{title_or_content}' skipped or error: {e}")
            try:
                if self.is_in_editor() or self.is_in_search():
                    self.d.press("back")
            except Exception:
                pass

    # =========================================================================
    # TEST CASES FOR FN-23
    # =========================================================================

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
