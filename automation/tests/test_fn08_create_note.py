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
        """Precondition: Ensure app is at HomeScreen, recovering from any lingering modal/editor."""
        cls.driver.ensure_device_ready()
        cls.driver.launch_app()
        time.sleep(1.0)

        # Recovery loop: Dismiss any open modal bottom sheets, Scrim, Selection Mode, or EditorScreen
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

        # Final check
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
        # 1. Dismiss any residual Selection Mode if active
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

        # 2. Locate FAB button, strictly excluding SnackBar Action buttons ('Hoàn tác' / 'Undo')
        fab_btn = None
        candidates = []
        for btn in self.d(className="android.widget.Button"):
            try:
                info = btn.info
                desc = (info.get("contentDescription", "") or "").strip()
                # Exclude SnackBar action button (Undo/Hoàn tác)
                if "Hoàn tác" in desc or "Undo" in desc:
                    continue
                b = info.get("bounds", {})
                if b.get("right", 0) > 700 and b.get("bottom", 0) > 1800:
                    candidates.append((b.get("bottom", 0), b, btn))
            except Exception:
                pass

        if candidates:
            # Pick the bottom-most candidate (the FAB at bottom: ~2259)
            candidates.sort(key=lambda x: x[0], reverse=True)
            fab_btn = candidates[0][2]

        if fab_btn is not None:
            fab_btn.click()
        else:
            # Fallback to verified S21 FE FAB center coordinate (x=964, y=2185)
            self.d.click(964, 2185)

        # 3. Wait for EditorScreen with a polling loop (up to 4.0s)
        for _ in range(8):
            time.sleep(0.5)
            if self.is_in_editor():
                return

        # Safe retry tap if still not in editor after initial wait
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
        """Input content text into the QuillEditor via uiautomator2 native pasteClipboard.
        
        flutter_quill QuillController requires input via IME / clipboard events
        to trigger document.changes listeners and mark _isDirty = true. Using
        accessibility ACTION_SET_TEXT changes the visual label but does not dispatch deltas
        to QuillController, causing empty-title notes to be treated as empty and not saved.
        Calling d.jsonrpc.pasteClipboard() triggers native clipboard paste into the active
        QuillEditor text client, properly updating QuillController.document.
        """
        if not content:
            return

        # 1. Tap content area to focus QuillEditor
        content_placeholder = self.d(description="Ghi chú") or self.d(text="Ghi chú")
        if content_placeholder.exists:
            content_placeholder.click()
        else:
            self.d.click(540, 520)  # Middle of QuillEditor area
        time.sleep(0.5)

        # 2. Input text via system clipboard and uiautomator2 native pasteClipboard JSON-RPC
        self.d.set_clipboard(content)
        time.sleep(0.3)
        try:
            self.d.jsonrpc.pasteClipboard()
        except Exception:
            time.sleep(0.3)
            self.d.jsonrpc.pasteClipboard()
        time.sleep(0.5)

        # 3. Intermediate verification: verify content actually appeared in QuillEditor before exiting
        content_in_editor = False
        for _ in range(6):  # Polling up to 3.0 seconds
            if self.d(descriptionContains=content).exists or content in self.d.dump_hierarchy():
                content_in_editor = True
                break
            time.sleep(0.5)

        if not content_in_editor:
            # Fallback retry focus and native paste once if not registered immediately
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
            f"[INPUT FAILURE] Content '{content}' was not entered into QuillEditor. "
            f"Content did not appear in EditorScreen UI hierarchy after paste."
        )

    def save_and_exit_editor(self):
        """Save note and return to HomeScreen via AppBar back button or system back."""
        # Tap top-left AppBar leading back button (Icons.arrow_back at bounds [0, 120][150, 225])
        self.d.click(75, 170)
        time.sleep(1.5)

        # If still in editor (e.g. soft keyboard intercepted the tap), press back to trigger PopScope
        if self.is_in_editor():
            self.d.press("back")
            time.sleep(1.5)

        # If still in editor, press back once more to exit
        if self.is_in_editor():
            self.d.press("back")
            time.sleep(1.5)

    def get_home_notes_state(self) -> dict:
        """Capture the current note items state on HomeScreen without relying on volatile system texts."""
        is_empty = (
            self.driver.find_by_text("Chưa có ghi chú nào", contains=True) is not None
            or self.driver.find_by_text("No notes yet", contains=True) is not None
        )

        ignored_ui_texts = {
            "Tìm kiếm", "Search",
            "Được ghim", "Pinned",
            "Khác", "Others",
            "Chưa có ghi chú nào", "No notes yet",
            "Nhấn + để tạo ghi chú đầu tiên",
            "Quản lý nhãn", "Manage labels"
        }

        note_items = []
        for el in self.d.xpath('//*[@text!="" or @content-desc!=""]').all():
            txt = (el.attrib.get('text', '') or el.attrib.get('content-desc', '')).strip()
            if not txt or txt in ignored_ui_texts:
                continue
            # Ignore transient system clocks, timestamps, or battery percentage
            if (":" in txt or "%" in txt) and len(txt) <= 6:
                continue
            note_items.append(txt)

        return {
            "is_empty": is_empty,
            "note_items": note_items,
            "count": len(note_items),
        }

    def cleanup_note_via_selection(self, title_or_content: str):
        """Safely clean up test note from HomeScreen using Selection Mode (Long-press -> Trash).
        
        Best-effort cleanup: never raises exceptions, never clicks unrelated buttons (e.g. Reminder),
        and never fails the functional test.
        """
        try:
            # 1. Ensure we are on HomeScreen, not inside editor or any overlay
            if self.is_in_editor():
                self.d.press("back")
                time.sleep(1.0)

            # 2. Dismiss any existing Selection Mode if active
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

            # 3. Locate the card on HomeScreen
            card = (
                self.d(descriptionContains=title_or_content)
                or self.d(textContains=title_or_content)
            )
            if not card.exists:
                return

            # 4. Long press on card center for 1.2s to trigger Flutter onLongPress (Selection Mode)
            b = card.info.get("bounds", {})
            if b:
                cx = (b.get("left", 0) + b.get("right", 0)) // 2
                cy = (b.get("top", 0) + b.get("bottom", 0)) // 2
                self.d.touch.down(cx, cy)
                time.sleep(1.2)
                self.d.touch.up(cx, cy)
                time.sleep(0.8)

            # 5. Check if Selection Mode is active
            is_selection_mode = (
                self.d(descriptionContains="Hủy chọn").exists
                or self.d(descriptionContains="Cancel").exists
                or self.d(descriptionContains="đã chọn").exists
                or self.d(descriptionContains="selected").exists
            )

            if is_selection_mode:
                # Find and click trash button in selection AppBar
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
                # If long press accidentally opened EditorScreen instead of selection,
                # press back to return to HomeScreen without clicking anything else (no Reminder/Schedule)
                self.d.press("back")
                time.sleep(1.0)
        except Exception as e:
            print(f"[Cleanup Notice] Cleanup for '{title_or_content}' skipped or error: {e}")
            try:
                if self.is_in_editor():
                    self.d.press("back")
                    time.sleep(0.5)
            except Exception:
                pass

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
