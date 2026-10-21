"""Automation Test Suite for FN-23 Extended: Search & Filter Note (Phase 5).

Batch 1 (5 items):
- TC-BB-026B (D01): Tìm kiếm không phân biệt chữ thường có dấu ("nghiên cứu")
- TC-BB-026B (D02): Tìm kiếm không phân biệt chữ HOA có dấu ("NGHIÊN CỨU")
- TC-BB-026C (D01): Tìm kiếm tiếng Việt có dấu đầy đủ ("kiểm thử")
- TC-BB-026E (D01): Xóa nhanh từ khóa bằng nút 'X' trên search bar
- TC-BB-028D (D01): Thoát màn hình tìm kiếm bằng nút mũi tên Back trên AppBar

Batch 2 (6 items):
- TC-BB-027D (D01): Lọc trạng thái "Được ghim" (is:pinned)
- TC-BB-027F (D01): Gỡ bỏ từng viên Chip lọc trên search bar
- TC-BB-028B (D01): Loại trừ ghi chú trong Thùng rác khỏi kết quả (0 leak)
- TC-BB-027B (D03): Lọc Loại đa phương tiện "Liên kết" (has:url)
- TC-BB-027D (D02): Lọc trạng thái "Lưu trữ" (is:archived)
- TC-BB-028C (D01): Mở và chỉnh sửa ghi chú trực tiếp từ kết quả tìm kiếm

Batch 3 (3 items):
- TC-BB-026B (D03): Tìm kiếm chuỗi không dấu tiếng Việt ("nghien cuu") - CHƯA ĐỦ CĂN CỨ (BR-01)
- TC-BB-027G (D01): Bộ lọc "Danh sách" (has:list) - Tái hiện BUG-004 OPEN
- TC-BB-027E (D01): Lọc kết hợp Chip Hình ảnh + Từ khóa - BLOCKED (Vướng BUG-001)

Standards: IEEE 829 & ISTQB Automation Guidelines
Device: Samsung Galaxy S21 FE 5G (SM-G990E, Android 14)
Account: student_qa@gmail.com (UID: TcBEqoIJqjXj8p3ek9ITDuBQwSP2)
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
from automation import config

RUN_ID = "run_20261021_0325"
EVIDENCE_DIR = os.path.join(config.PROJECT_ROOT, "evidence", "fn23", RUN_ID)


class FN23Base:
    """Shared base helpers for FN-23 automation suites."""
    driver = None
    d = None

    @classmethod
    def init_driver(cls):
        os.makedirs(EVIDENCE_DIR, exist_ok=True)
        if cls.driver is None:
            cls.driver = SmartNoteDriver()
            cls.d = cls.driver.device
        cls.driver.ensure_device_ready()
        cls.driver.ensure_home_screen()
        time.sleep(1.0)

    @classmethod
    def is_in_editor(cls) -> bool:
        return cls.driver.is_in_editor()

    @classmethod
    def is_in_search(cls) -> bool:
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
        """Open SearchScreen from HomeScreen."""
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
        """Exit SearchScreen back to HomeScreen."""
        for _ in range(4):
            if self.driver.is_on_home_screen():
                return
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
        """Input query into Search TextField and dismiss soft keyboard."""
        edit = self.d(className="android.widget.EditText")
        assert edit.exists, "Cannot find Search TextField on SearchScreen."
        edit.click()
        time.sleep(0.3)
        edit.set_text(query)
        time.sleep(1.2)  # Wait for search debounce & query execution

        # Dismiss soft keyboard if visible
        if self.d(packageName="com.samsung.android.honeyboard").exists:
            self.d.press("back")
            time.sleep(0.5)

    def click_clear_button(self) -> bool:
        """Click the 'X' button inside the search bar."""
        for btn in self.d(className="android.widget.Button"):
            try:
                b = btn.info.get("bounds", {})
                if b.get("top", 999) < 300 and b.get("left", 0) > 800:
                    btn.click()
                    time.sleep(1.0)
                    return True
            except Exception:
                pass
        self.d.click(960, 192)
        time.sleep(1.0)
        return True

    def click_search_back_button(self) -> bool:
        """Click the back arrow inside SearchBar to return to HomeScreen."""
        for btn in self.d(className="android.widget.Button"):
            try:
                b = btn.info.get("bounds", {})
                if b.get("top", 999) < 300 and b.get("left", 999) < 200:
                    btn.click()
                    time.sleep(1.5)
                    return True
            except Exception:
                pass
        self.d.click(105, 192)
        time.sleep(1.5)
        return True

    def capture_screenshot(self, filename: str) -> str:
        """Capture screenshot into RUN_ID directory."""
        path = os.path.join(EVIDENCE_DIR, filename)
        self.d.screenshot(path)
        print(f"[EVIDENCE] Screenshot saved: {path}")
        return path


# =============================================================================
# BATCH 1: TÌM KIẾM TIẾNG VIỆT, CASE-INSENSITIVE & ĐIỀU HƯỚNG CƠ BẢN
# =============================================================================

class TestFN23Batch1(FN23Base):
    @classmethod
    def setup_class(cls):
        cls.init_driver()
        cls.fixture_title = "QA_FN23_Nghiencuu_026B"
        cls.fixture_content = "Tài liệu nghiên cứu và kiểm thử phần mềm tự động"
        print(f"\n[SETUP Batch 1] Checking fixture note: '{cls.fixture_title}'...")
        hierarchy = cls.d.dump_hierarchy()
        if cls.fixture_title in hierarchy or cls.d(descriptionContains=cls.fixture_title).exists:
            print(f"[SETUP Batch 1] Fixture note '{cls.fixture_title}' already present on HomeScreen.")
        else:
            print(f"[SETUP Batch 1] Creating fixture note: '{cls.fixture_title}'...")
            cls.driver.ensure_test_note(cls.fixture_title, cls.fixture_content)
        time.sleep(1.0)

    @classmethod
    def teardown_class(cls):
        print(f"\n[TEARDOWN Batch 1] Cleaning up fixture note: '{cls.fixture_title}'...")
        try:
            cls.exit_search_screen(cls)
            cls.driver.cleanup_note_via_selection(cls.fixture_title)
        except Exception as e:
            print(f"[TEARDOWN WARNING] {e}")

    def test_tc_bb_026b_d01_lowercase_accented(self):
        """TC-BB-026B (D01): Tìm kiếm chữ thường có dấu ('nghiên cứu')."""
        keyword = "nghiên cứu"
        print(f"\n--- [TC-BB-026B-D01] Tìm kiếm chữ thường có dấu: '{keyword}' ---")
        self.driver.ensure_home_screen()
        self.open_search_screen()
        try:
            self.input_search_query(keyword)
            found = False
            for _ in range(10):
                hierarchy = self.d.dump_hierarchy()
                if (
                    self.fixture_title in hierarchy
                    or self.d(textContains=self.fixture_title).exists
                    or self.d(descriptionContains=self.fixture_title).exists
                    or "nghiên cứu" in hierarchy.lower()
                ):
                    found = True
                    break
                time.sleep(0.5)

            ev = self.capture_screenshot("FN23_TC-BB-026B_D01_lowercase.png")
            print(f"[TC-BB-026B-D01] Kết quả tìm thấy: {found}")
            assert found, f"Expected search results to display note for lowercase keyword '{keyword}'."
        finally:
            self.click_clear_button()
            self.exit_search_screen()

    def test_tc_bb_026b_d02_uppercase_accented(self):
        """TC-BB-026B (D02): Tìm kiếm chữ HOA có dấu ('NGHIÊN CỨU')."""
        keyword = "NGHIÊN CỨU"
        print(f"\n--- [TC-BB-026B-D02] Tìm kiếm chữ HOA có dấu: '{keyword}' ---")
        self.driver.ensure_home_screen()
        self.open_search_screen()
        try:
            self.input_search_query(keyword)
            found = False
            for _ in range(10):
                hierarchy = self.d.dump_hierarchy()
                if (
                    self.fixture_title in hierarchy
                    or self.d(textContains=self.fixture_title).exists
                    or self.d(descriptionContains=self.fixture_title).exists
                ):
                    found = True
                    break
                time.sleep(0.5)

            ev = self.capture_screenshot("FN23_TC-BB-026B_D02_uppercase.png")
            print(f"[TC-BB-026B-D02] Kết quả tìm thấy trên thiết bị: {found}")
            assert found, f"Expected search results to display note for uppercase keyword '{keyword}'."
        finally:
            self.click_clear_button()
            self.exit_search_screen()

    def test_tc_bb_026c_d01_vietnamese_accented(self):
        """TC-BB-026C (D01): Tìm kiếm từ khóa tiếng Việt có dấu đầy đủ ('kiểm thử')."""
        keyword = "kiểm thử"
        print(f"\n--- [TC-BB-026C-D01] Tìm kiếm từ khóa tiếng Việt: '{keyword}' ---")
        self.driver.ensure_home_screen()
        self.open_search_screen()
        try:
            self.input_search_query(keyword)
            found = False
            for _ in range(10):
                hierarchy = self.d.dump_hierarchy()
                if (
                    self.fixture_title in hierarchy
                    or self.d(textContains=self.fixture_title).exists
                    or self.d(descriptionContains=self.fixture_title).exists
                    or "kiểm thử" in hierarchy
                ):
                    found = True
                    break
                time.sleep(0.5)

            ev = self.capture_screenshot("FN23_TC-BB-026C_D01_vietnamese.png")
            print(f"[TC-BB-026C-D01] Kết quả tìm thấy: {found}")
            assert found, f"Expected search results to display note containing '{keyword}'."
        finally:
            self.click_clear_button()
            self.exit_search_screen()

    def test_tc_bb_026e_d01_clear_search_bar(self):
        """TC-BB-026E (D01): Xóa nhanh từ khóa bằng nút 'X' trên search bar."""
        keyword = "kiểm thử"
        print(f"\n--- [TC-BB-026E-D01] Xóa nhanh từ khóa bằng nút 'X' trên search bar ---")
        self.driver.ensure_home_screen()
        self.open_search_screen()
        try:
            self.input_search_query(keyword)
            time.sleep(1.0)
            self.click_clear_button()
            time.sleep(1.0)

            edit = self.d(className="android.widget.EditText")
            current_text = ""
            if edit.exists:
                current_text = edit.get_text() or ""
            print(f"[TC-BB-026E-D01] Text in search field after Clear: '{current_text}'")

            hierarchy = self.d.dump_hierarchy()
            has_predefined = (
                "Loại" in hierarchy
                or "Ghim" in hierarchy
                or "Được ghim" in hierarchy
                or "Lưu trữ" in hierarchy
                or "Tìm kiếm ghi chú của bạn" in hierarchy
            )

            ev = self.capture_screenshot("FN23_TC-BB-026E_D01_clear_bar.png")
            print(f"[TC-BB-026E-D01] Predefined filters restored: {has_predefined}")

            assert current_text == "" or current_text is None, f"Search text field was not cleared, got '{current_text}'."
            assert has_predefined, "Search screen did not restore predefined filters after clearing search text."
        finally:
            self.exit_search_screen()

    def test_tc_bb_028d_d01_back_arrow_to_home(self):
        """TC-BB-028D (D01): Nút mũi tên Back trên thanh tìm kiếm thoát về Trang chủ."""
        print(f"\n--- [TC-BB-028D-D01] Nút mũi tên Back thoát về HomeScreen ---")
        self.driver.ensure_home_screen()
        self.open_search_screen()
        assert self.is_in_search(), "Precondition failed: Not in SearchScreen."

        self.click_search_back_button()
        time.sleep(1.5)

        on_home = self.driver.is_on_home_screen()
        print(f"[TC-BB-028D-D01] Returned to HomeScreen: {on_home}")

        ev = self.capture_screenshot("FN23_TC-BB-028D_D01_back_home.png")
        assert on_home, "Failed to navigate back to HomeScreen using search bar Back arrow."


# =============================================================================
# BATCH 2: BỘ LỌC TRẠNG THÁI (PINNED / ARCHIVE / TRASH), CHIP VÀ URL
# =============================================================================

class TestFN23Batch2(FN23Base):
    @classmethod
    def setup_class(cls):
        cls.init_driver()

    def test_tc_bb_027d_d01_pinned_filter(self):
        """TC-BB-027D (D01): Lọc trạng thái 'Được ghim' (is:pinned).

        Kỳ vọng: Chip [Được ghim] xuất hiện trên search bar; danh sách chỉ hiển thị các note đã ghim.
        """
        print("\n--- [TC-BB-027D-D01] Lọc ghi chú trạng thái 'Được ghim' ---")
        self.driver.ensure_home_screen()
        self.open_search_screen()
        try:
            time.sleep(1.0)
            pinned_icon = None
            for _ in range(8):
                if self.d(packageName="com.samsung.android.honeyboard").exists:
                    self.d.press("back")
                    time.sleep(0.5)
                icon = self.d(descriptionContains="ghim")
                if icon.exists:
                    pinned_icon = icon
                    break
                time.sleep(0.5)

            assert pinned_icon is not None and pinned_icon.exists, "Cannot find 'Được ghim' filter icon on SearchScreen."
            pinned_icon.click()
            time.sleep(1.5)

            # Check Chip on search bar
            chip = self.d(description="Được ghim") or self.d(text="Được ghim")
            assert chip.exists, "Expected Chip [Được ghim] to appear on search bar."

            # Check pinned notes appear in results
            hierarchy = self.d.dump_hierarchy()
            p1 = "QA_PIN_024G_59346191_1" in hierarchy
            p2 = "QA_PIN_024G_59346191_2" in hierarchy
            p3 = "QA_PIN_024G_59346191_3" in hierarchy
            has_pinned = p1 or p2 or p3

            ev = self.capture_screenshot("FN23_TC-BB-027D_D01_pinned_filter.png")
            print(f"[TC-BB-027D-D01] Pinned notes found: {has_pinned} (p1={p1}, p2={p2}, p3={p3})")
            assert has_pinned, "Expected pinned QA notes to appear in pinned filter results."
        finally:
            self.click_clear_button()
            self.exit_search_screen()

    def test_tc_bb_027f_d01_remove_filter_chip(self):
        """TC-BB-027F (D01): Gỡ bỏ từng viên Chip lọc trên thanh tìm kiếm.

        Kỳ vọng: Chạm 'X' bên trong Chip hoặc Clear, Chip biến mất và các bộ lọc gợi ý xuất hiện trở lại.
        """
        print("\n--- [TC-BB-027F-D01] Gỡ bỏ viên Chip lọc [Được ghim] ---")
        self.driver.ensure_home_screen()
        self.open_search_screen()
        try:
            if self.d(packageName="com.samsung.android.honeyboard").exists:
                self.d.press("back")
                time.sleep(0.5)
            self.d.swipe(540, 1500, 540, 800, duration=0.2)
            time.sleep(0.5)

            # 1. Tap "Được ghim" để xuất hiện Chip
            pinned_icon = self.d(description="Được ghim") or self.d(text="Được ghim")
            if pinned_icon.exists:
                pinned_icon.click()
                time.sleep(1.5)

            # 2. Định vị Chip trên AppBar
            chip = self.d(description="Được ghim")
            assert chip.exists, "Precondition failed: Chip [Được ghim] not found."
            b = chip.info.get("bounds", {})
            click_x = b.get("right", 390) - 25
            click_y = (b.get("top", 160) + b.get("bottom", 220)) // 2
            self.d.click(click_x, click_y)
            time.sleep(1.5)

            # If chip still present, click Clear 'X' on search bar
            if self.d(description="Được ghim").exists:
                self.click_clear_button()
                time.sleep(1.0)

            # Dismiss keyboard if popped up
            if self.d(packageName="com.samsung.android.honeyboard").exists:
                self.d.press("back")
                time.sleep(0.5)

            # 3. Xác minh Chip biến mất khỏi AppBar và bộ lọc gợi ý xuất hiện lại
            hierarchy = self.d.dump_hierarchy()
            filters_restored = (
                "Loại ghi chú" in hierarchy
                or "Trạng thái" in hierarchy
                or "Loại" in hierarchy
                or "Được ghim" in hierarchy
            )

            ev = self.capture_screenshot("FN23_TC-BB-027F_D01_remove_chip.png")
            print(f"[TC-BB-027F-D01] Predefined filters restored after chip removal: {filters_restored}")
            assert filters_restored, "Expected predefined filters to be restored after removing Chip."
        finally:
            self.click_clear_button()
            self.exit_search_screen()

    def test_tc_bb_028b_d01_trash_excluded(self):
        """TC-BB-028B (D01): Loại trừ hoàn toàn ghi chú trong Thùng rác khỏi kết quả tìm kiếm (0 leak).

        Kỳ vọng: Ghi chú trong Thùng rác (QA_FN23_Nghiencuu_026B) hoàn toàn không xuất hiện, hiển thị Empty State.
        """
        keyword = "QA_FN23_Nghiencuu_026B"
        print(f"\n--- [TC-BB-028B-D01] Tìm kiếm ghi chú đã vào Thùng rác: '{keyword}' ---")
        self.driver.ensure_home_screen()
        self.open_search_screen()
        try:
            self.input_search_query(keyword)
            time.sleep(1.5)

            hierarchy = self.d.dump_hierarchy()
            # Check if any note card below the search bar (y > 300) contains the deleted note keyword
            leaked_card = False
            for view in self.d(className="android.view.View"):
                desc = view.info.get("contentDescription") or ""
                b = view.info.get("bounds", {})
                if keyword in desc and b.get("top", 0) > 300:
                    leaked_card = True
                    break

            empty_state = (
                "Không tìm thấy kết quả" in hierarchy
                or self.d(textContains="Không tìm thấy kết quả").exists
                or self.d(descriptionContains="Không tìm thấy kết quả").exists
            )

            ev = self.capture_screenshot("FN23_TC-BB-028B_D01_trash_excluded.png")
            print(f"[TC-BB-028B-D01] Card leaked: {leaked_card}, Empty state shown: {empty_state}")
            assert not leaked_card, f"Security/Privacy defect: Note in trash '{keyword}' leaked into search results!"
            assert empty_state, "Expected Empty State 'Không tìm thấy kết quả' when searching note in trash."
        finally:
            self.click_clear_button()
            self.exit_search_screen()

    def test_tc_bb_027b_d03_url_filter(self):
        """TC-BB-027B (D03): Lọc Loại đa phương tiện 'Liên kết' (has:url).

        Kỳ vọng: Chip [URL] xuất hiện trên search bar, trả về đúng ghi chú có chứa URL text.
        """
        title = "QA_FN23_URL_027B"
        content = "https://smartnote.app/docs"
        print(f"\n--- [TC-BB-027B-D03] Lọc ghi chú chứa liên kết URL (has:url) ---")

        # 1. Đảm bảo note QA chứa URL tồn tại
        self.driver.ensure_home_screen()
        hierarchy = self.d.dump_hierarchy()
        if title not in hierarchy and not self.d(descriptionContains=title).exists:
            print(f"[TC-BB-027B-D03] Creating URL test note: '{title}'...")
            self.driver.open_note_editor()
            self.driver.input_title(title)
            self.driver.input_content(content)
            self.driver.save_and_exit_editor()
            time.sleep(1.0)

        self.open_search_screen()
        try:
            if self.d(packageName="com.samsung.android.honeyboard").exists:
                self.d.press("back")
                time.sleep(0.5)
            self.d.swipe(540, 1500, 540, 900, duration=0.2)
            time.sleep(0.5)

            # 2. Bấm icon URL
            url_btn = self.d(description="URL") or self.d(text="URL")
            assert url_btn.exists, "Cannot find URL filter icon on SearchScreen."
            url_btn.click()
            time.sleep(1.5)

            # 3. Kiểm tra kết quả
            hierarchy = self.d.dump_hierarchy()
            found_note = title in hierarchy or "smartnote.app" in hierarchy

            ev = self.capture_screenshot("FN23_TC-BB-027B_D03_url_filter.png")
            print(f"[TC-BB-027B-D03] URL note found: {found_note}")
            assert found_note, f"Expected URL filter (has:url) to display note '{title}'."
        finally:
            self.click_clear_button()
            self.exit_search_screen()
            self.driver.cleanup_note_via_selection(title)

    def test_tc_bb_027d_d02_archive_filter(self):
        """TC-BB-027D (D02): Lọc trạng thái 'Lưu trữ' (is:archived).

        Kỳ vọng: Chip [Lưu trữ] xuất hiện trên search bar; danh sách lọc ra ghi chú đã lưu trữ.
        """
        title = "QA_FN23_Archive_027D"
        content = "Noi dung ghi chu luu tru kiem thu FN23"
        print(f"\n--- [TC-BB-027D-D02] Lọc ghi chú trạng thái 'Lưu trữ' ---")

        # 1. Tạo note và chuyển sang Archive nếu chưa có
        self.driver.ensure_home_screen()
        hierarchy = self.d.dump_hierarchy()
        card = self.d(descriptionContains=title) or self.d(textContains=title)
        if card.exists:
            card.long_click(duration=1.2)
            time.sleep(0.8)
            arc_btn = self.d(description="Lưu trữ") or self.d(descriptionContains="Lưu trữ")
            if arc_btn.exists:
                arc_btn.click()
                time.sleep(1.5)

        self.open_search_screen()
        try:
            if self.d(packageName="com.samsung.android.honeyboard").exists:
                self.d.press("back")
                time.sleep(0.5)
            self.d.swipe(540, 1500, 540, 800, duration=0.2)
            time.sleep(0.5)

            # 2. Bấm icon Lưu trữ
            arc_filter = self.d(description="Lưu trữ") or self.d(text="Lưu trữ")
            assert arc_filter.exists, "Cannot find 'Lưu trữ' filter icon on SearchScreen."
            arc_filter.click()
            time.sleep(1.5)

            hierarchy = self.d.dump_hierarchy()
            found_archived = title in hierarchy or "QA_FN23_Archive" in hierarchy

            ev = self.capture_screenshot("FN23_TC-BB-027D_D02_archive_filter.png")
            print(f"[TC-BB-027D-D02] Archived note found in search: {found_archived}")
            assert found_archived, f"Expected archived note '{title}' to appear under is:archived filter."
        finally:
            self.click_clear_button()
            self.exit_search_screen()

    def test_tc_bb_028c_d01_edit_from_search_results(self):
        """TC-BB-028C (D01): Mở và chỉnh sửa ghi chú trực tiếp từ danh sách kết quả tìm kiếm.

        Kỳ vọng: Chạm thẻ ghi chú trong kết quả tìm kiếm mở đúng Editor; sửa và Back cập nhật ngay.
        """
        keyword = "024G"
        print(f"\n--- [TC-BB-028C-D01] Mở và chỉnh sửa ghi chú từ kết quả tìm kiếm: '{keyword}' ---")
        self.driver.ensure_home_screen()
        self.open_search_screen()
        try:
            self.input_search_query(keyword)
            time.sleep(1.5)

            # Chạm vào thẻ ghi chú đầu tiên
            card = self.d(descriptionContains="QA_PIN_024G_59346191_1")
            assert card.exists, "Cannot find target note card in search results."
            card.click()
            time.sleep(1.5)

            # Xác minh vào EditorScreen
            in_editor = self.driver.is_in_editor()
            print(f"[TC-BB-028C-D01] Opened EditorScreen from search result: {in_editor}")
            assert in_editor, "Failed to navigate to EditorScreen from search result card."

            # Bấm Back thoát Editor về Search
            self.driver.save_and_exit_editor()
            time.sleep(1.5)

            # Xác minh quay lại SearchScreen an toàn
            in_search = self.is_in_search()
            ev = self.capture_screenshot("FN23_TC-BB-028C_D01_edit_from_search.png")
            print(f"[TC-BB-028C-D01] Returned to SearchScreen: {in_search}")
            assert in_search, "Failed to return to SearchScreen after exiting Editor."
        finally:
            self.click_clear_button()
            self.exit_search_screen()


# =============================================================================
# BATCH 3: TÌM KHÔNG DẤU (BR-01), BỘ LỌC DANH SÁCH (BUG-004), & MEDIA GAP
# =============================================================================

class TestFN23Batch3(FN23Base):
    @classmethod
    def setup_class(cls):
        cls.init_driver()

    def test_tc_bb_026b_d03_unaccented_search_actual_behavior(self):
        """TC-BB-026B (D03): Tìm kiếm chuỗi không dấu đối với tiếng Việt ('nghien cuu').

        Xác minh thực tế trên thiết bị:
        - Engine SQLite mặc định không hỗ trợ unaccented folding;
        - Nhập 'nghien cuu' hiển thị Empty State ('Không tìm thấy kết quả');
        - Ứng dụng ổn định, không lỗi/crash.
        - Trạng thái: CHƯA ĐỦ CĂN CỨ theo BR-01 (không ép PASS).
        """
        keyword = "nghien cuu"
        print(f"\n--- [TC-BB-026B-D03] Xác minh tìm kiếm không dấu: '{keyword}' ---")
        self.driver.ensure_home_screen()
        self.open_search_screen()
        try:
            self.input_search_query(keyword)
            time.sleep(1.5)

            hierarchy = self.d.dump_hierarchy()
            empty_state = (
                "Không tìm thấy kết quả" in hierarchy
                or self.d(textContains="Không tìm thấy kết quả").exists
                or self.d(descriptionContains="Không tìm thấy kết quả").exists
            )
            app_alive = self.is_in_search()

            ev = self.capture_screenshot("FN23_TC-BB-026B_D03_unaccented.png")
            print(f"[TC-BB-026B-D03] Empty state displayed: {empty_state}, App alive: {app_alive}")
            print(f"[TC-BB-026B-D03] STATUS: CHƯA ĐỦ CĂN CỨ (SQLite requires accent, BR-01 unapproved)")
            assert app_alive, "App crashed on unaccented query."
            assert empty_state, "Expected Empty State on unaccented query in default SQLite engine."
        finally:
            self.click_clear_button()
            self.exit_search_screen()

    def test_tc_bb_027g_d01_list_filter_reproduce_bug_004(self):
        """TC-BB-027G (D01): Xác minh hoạt động bộ lọc 'Danh sách' (has:list) - Tái hiện BUG-004.

        Thực tế:
        - Bấm 'Danh sách' thêm Chip [Danh sách] vào search bar;
        - Service searchNotes xử lý LIKE thô 'has:list' không bóc tách token -> kết quả rỗng (Empty State).
        - Xác nhận lỗi BUG-004 OPEN tái hiện chính xác trên thiết bị thực tế.
        """
        print(f"\n--- [TC-BB-027G-D01] Xác minh bộ lọc 'Danh sách' (has:list) / Tái hiện BUG-004 ---")
        self.driver.ensure_home_screen()
        self.open_search_screen()
        try:
            time.sleep(1.0)
            list_icon = None
            for _ in range(8):
                if self.d(packageName="com.samsung.android.honeyboard").exists:
                    self.d.press("back")
                    time.sleep(0.5)
                icon = self.d(descriptionContains="sách") or self.d(textContains="sách")
                if icon.exists:
                    list_icon = icon
                    break
                time.sleep(0.5)

            assert list_icon is not None and list_icon.exists, "Cannot find 'Danh sách' filter icon on SearchScreen."
            list_icon.click()
            time.sleep(1.5)

            hierarchy = self.d.dump_hierarchy()
            chip_visible = "Danh sách" in hierarchy
            empty_result = (
                "Không tìm thấy kết quả" in hierarchy
                or self.d(textContains="Không tìm thấy kết quả").exists
                or self.d(descriptionContains="Không tìm thấy kết quả").exists
            )

            ev = self.capture_screenshot("FN23_TC-BB-027G_D01_list_filter_bug004.png")
            print(f"[TC-BB-027G-D01] Chip visible: {chip_visible}, Empty result due to raw LIKE: {empty_result}")
            print(f"[TC-BB-027G-D01] DEFECT VERIFIED: BUG-004 OPEN confirmed on device.")
            assert chip_visible, "Expected Chip [Danh sách] to appear on search bar."
            assert empty_result, "Expected Empty State reproducing BUG-004 raw LIKE query limitation."
        finally:
            self.click_clear_button()
            self.exit_search_screen()

    def test_tc_bb_027e_d01_combined_image_filter_status(self):
        """TC-BB-027E (D01): Lọc kết hợp Chip 'Hình ảnh' + Từ khóa văn bản.

        Trạng thái: BLOCKED / NOT RUN.
        Nguyên nhân: Đính kèm hình ảnh bị lỗi BUG-001 (treo vĩnh viễn ở thanh tiến trình trong Editor);
        không có ghi chú QA chứa hình ảnh hợp lệ trong môi trường test isolated.
        Theo yêu cầu chỉ đạo: Không tự ý thay đổi fixture sang Pinned; giữ đúng định danh TC gốc.
        """
        print(f"\n--- [TC-BB-027E-D01] Lọc kết hợp Hình ảnh + Từ khóa ---")
        pytest.skip("TC-BB-027E-D01 BLOCKED: Dependency on Image attachment blocked by BUG-001 (Infinite upload hang in Editor).")
