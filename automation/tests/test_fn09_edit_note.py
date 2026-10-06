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
        """Locate FAB in bottom-right corner and open EditorScreen for new note."""
        # Dismiss any residual Selection Mode if active
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

    def open_existing_note(self, title_or_content: str):
        """Locate and tap an existing NoteCard on HomeScreen to open EditorScreen."""
        # Dismiss Selection Mode if accidentally active
        cancel_btn = (
            self.d(descriptionContains="Hủy chọn")
            or self.d(descriptionContains="Cancel")
            or self.d(textContains="Hủy chọn")
        )
        if cancel_btn is not None:
            try:
                cancel_btn.click()
                time.sleep(0.5)
            except Exception:
                pass

        card = None
        for _ in range(8):
            # Dynamic locator via contentDescription or text
            card = (
                self.d(descriptionContains=title_or_content)
                or self.d(textContains=title_or_content)
            )
            if card.exists:
                break
            # Try XPath locator
            xpath_expr = f'//*[contains(@content-desc, "{title_or_content}") or contains(@text, "{title_or_content}")]'
            if self.d.xpath(xpath_expr).exists:
                card = self.d.xpath(xpath_expr)
                break
            time.sleep(0.5)

        assert card is not None and card.exists, (
            f"Cannot locate NoteCard with title or content '{title_or_content}' on HomeScreen."
        )

        # Tap the card to open EditorScreen
        try:
            b = card.info.get("bounds", {})
            if b:
                cx = (b.get("left", 0) + b.get("right", 0)) // 2
                cy = (b.get("top", 0) + b.get("bottom", 0)) // 2
                self.d.click(cx, cy)
            else:
                card.click()
        except Exception:
            card.click()

        # Polling wait for EditorScreen
        for _ in range(8):
            time.sleep(0.5)
            if self.is_in_editor():
                time.sleep(0.5)
                return

        assert self.is_in_editor(), f"Failed to open EditorScreen for note '{title_or_content}'."

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
        """Input content text into QuillEditor via native pasteClipboard.
        
        Using uiautomator2 native pasteClipboard guarantees delta event dispatch to
        QuillController.document, setting _isDirty = true and triggering _autoSaveTimer.
        """
        if not content:
            return

        # 1. Focus QuillEditor
        content_placeholder = self.d(description="Ghi chú") or self.d(text="Ghi chú")
        if content_placeholder.exists:
            content_placeholder.click()
        else:
            self.d.click(540, 520)
        time.sleep(0.5)

        # 2. Input text via system clipboard and native pasteClipboard JSON-RPC
        self.d.set_clipboard(content)
        time.sleep(0.3)
        try:
            self.d.jsonrpc.pasteClipboard()
        except Exception:
            time.sleep(0.3)
            self.d.jsonrpc.pasteClipboard()
        time.sleep(0.5)

        # 3. Intermediate verification: verify content actually appeared in EditorScreen
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
            f"[INPUT FAILURE] Content '{content}' was not entered into QuillEditor. "
            f"Content did not appear in EditorScreen UI hierarchy after paste."
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

    def ensure_base_note(self, title: str, base_content: str):
        """Ensure a base note exists on HomeScreen for editing. If not found, create it."""
        card = self.d(descriptionContains=title) or self.d(textContains=title)
        if not card.exists:
            xpath_expr = f'//*[contains(@content-desc, "{title}") or contains(@text, "{title}")]'
            if not self.d.xpath(xpath_expr).exists:
                print(f"[Precondition] Base note '{title}' not found on HomeScreen. Creating it...")
                self.open_note_editor()
                self.input_title(title)
                self.input_content(base_content)
                self.save_and_exit_editor()
                time.sleep(1.0)
                # Verify base note created
                assert (
                    self.d(descriptionContains=title).exists
                    or self.d(textContains=title).exists
                    or self.d.xpath(xpath_expr).exists
                ), f"Failed to create precondition base note '{title}'."

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
    # TEST CASES FOR FN-09
    # =========================================================================

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
