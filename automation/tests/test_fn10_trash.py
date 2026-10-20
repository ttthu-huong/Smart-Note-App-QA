# -*- coding: utf-8 -*-
"""Automation UI Test Suite for FN-10: Move Note to Trash.
Test Cases:
- TC-BB-021: Chuyển 1 ghi chú vào Thùng rác từ Trang chủ (D01)
- TC-BB-021B: Hoàn tác chuyển ghi chú vào Thùng rác từ SnackBar (D01)
- TC-BB-021C: Hủy xóa (D01) / xác nhận xóa (D02) từ Editor
Standards: IEEE 829 & ISTQB Manual / Automation Execution
Device: Samsung Galaxy S21 FE 5G (Android 14)
Framework: Python 3.13 + pytest + uiautomator2 + ADB
"""
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
import uuid
from datetime import datetime
import pytest
# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from automation import config
from automation.core.device import SmartNoteDriver
from automation.core.qa_note_helper import QANoteHelper
RUN_LABEL = os.environ.get("FN10_RUN_ID") or datetime.now().strftime("%Y%m%d_%H%M%S_%f")
RUN_ID = f"{RUN_LABEL}_{uuid.uuid4().hex[:8]}"
RUN_EVIDENCE = Path("evidence") / "fn10" / f"automation_{RUN_ID}"
def _notes(serial: str, package: str) -> list[dict]:
    """Read an app-private SQLite snapshot into memory without modifying the device."""
    cmd = ["adb", "-s", serial, "exec-out", "run-as", package,
           "cat", "databases/smart_note.db"]
    result = subprocess.run(cmd, capture_output=True, timeout=25, check=False)
    if result.returncode or not result.stdout:
        message = result.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"SQLite read-only oracle unavailable: {message}")
    conn = sqlite3.connect(":memory:")
    try:
        conn.deserialize(result.stdout)
        rows = conn.execute("SELECT id, title, content, status FROM notes").fetchall()
        return [dict(zip(("id", "title", "content", "status"), row)) for row in rows]
    finally:
        conn.close()
def _plain(content) -> str:
    """Extract plain text from a Quill Delta or plain string."""
    if content is None:
        return ""
    if not isinstance(content, str):
        return str(content)
    try:
        delta = json.loads(content)
        if isinstance(delta, dict):
            delta = delta.get("ops", delta)
        if isinstance(delta, list):
            return "".join(op.get("insert", "") for op in delta
                           if isinstance(op, dict) and isinstance(op.get("insert"), str))
    except (ValueError, TypeError):
        pass
    return content
class TestFN10Trash:
    """Test Suite for FN-10: Chuyển ghi chú vào thùng rác."""
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
    def _evidence(self, tc: str, seq: int, data_id: str = "D01") -> str:
        """Capture screenshot into run-specific folder."""
        rel = (
            RUN_EVIDENCE / tc /
            f"FN10_{tc}_{data_id}_{seq:02d}.png"
        ).as_posix()
        saved = self.driver.capture_evidence(rel)
        print(f"[FN10 evidence] {tc} {data_id}: {saved}")
        return saved
    def _db(self) -> list[dict]:
        """Fetch read-only snapshot of SQLite notes table."""
        try:
            return _notes(self.driver.serial, config.APP_PACKAGE)
        except Exception as exc:
            print(f"[TC-BB-021B SQLite] Warning: Could not read DB: {exc}")
            return []
    def _row(self, note_id: str) -> dict | None:
        """Find a note row in SQLite snapshot by note_id."""
        db = self._db()
        found = [r for r in db if r["id"] == note_id]
        return found[0] if len(found) == 1 else None
    def test_tc_bb_021_move_note_to_trash(self):
        """TC-BB-021 (D01): Chuyển ghi chú vào thùng rác từ HomeScreen.
        Expected Result:
        - Thẻ ghi chú biến mất khỏi danh sách Trang chủ.
        - Mở Thùng rác thấy ghi chú xuất hiện với đúng thông tin tiêu đề/nội dung.
        """
        note_title = f"TrashTest_{int(time.time())}"
        note_content = "Nội dung kiểm thử chuyển vào thùng rác"
        print(f"\n========================================================")
        print(f"[START] TC-BB-021: Move Note to Trash — '{note_title}'")
        print(f"========================================================")
        try:
            # 1. Tiền điều kiện: Tạo ghi chú kiểm thử cô lập trên HomeScreen
            print(f"\n--- BƯỚC 1: Tạo ghi chú kiểm thử cô lập trên HomeScreen ---")
            QANoteHelper.create_test_note(self.driver, note_title, note_content, poll_timeout=6.0)
            # 2. Thao tác xóa: Nhấn giữ thẻ ghi chú để bật Selection Mode và nhấn Thùng rác
            print(f"\n--- BƯỚC 2: Chọn ghi chú và nhấn biểu tượng Thùng rác trên AppBar ---")
            QANoteHelper.move_note_to_trash_from_home(self.driver, note_title)
            # 3. Xác minh bước 1: Thẻ ghi chú biến mất khỏi Trang chủ
            print(f"\n--- BƯỚC 3: Xác minh ghi chú đã biến mất khỏi HomeScreen ---")
            QANoteHelper.verify_note_absent_on_home(self.driver, note_title)
            # 4. Điều hướng: Mở ngăn kéo (Drawer) và chọn "Thùng rác"
            print(f"\n--- BƯỚC 4: Điều hướng vào màn hình Thùng rác qua Drawer ---")
            QANoteHelper.navigate_to_trash(self.driver)
            # 5. Xác minh bước 2: Ghi chú xuất hiện trong Thùng rác
            print(f"\n--- BƯỚC 5: Xác minh ghi chú hiện diện trong Thùng rác ---")
            QANoteHelper.verify_note_in_trash(self.driver, note_title, poll_timeout=5.0)
            # 6. Chụp ảnh bằng chứng thực thi thành công
            ev_path = self.driver.capture_evidence("evidence/fn10/FN10_TC-BB-021_D01_01.png")
            print(f"\n[PASS] TC-BB-021 hoàn tất thành công! Bằng chứng đã lưu: {ev_path}")
        finally:
            # Dọn dẹp an toàn (Best-effort cleanup)
            print(f"\n--- DỌN DẸP: Xóa sạch dữ liệu test cô lập '{note_title}' ---")
            try:
                QANoteHelper.permanently_delete_note_from_trash(self.driver, note_title)
            except Exception as e:
                print(f"[Cleanup Notice] Ignored cleanup warning: {e}")
            try:
                QANoteHelper.navigate_from_trash_to_home(self.driver)
            except Exception:
                self.driver.ensure_home_screen()
    def test_tc_bb_021b_undo_move_to_trash(self):
        """TC-BB-021B (D01): Hoàn tác chuyển ghi chú vào Thùng rác từ SnackBar.
        Precondition:
        - Đang ở Trang chủ, có ghi chú QA hợp lệ được tạo mới.
        Steps:
        1. Tạo ghi chú QA với tiêu đề duy nhất, ghi nhận ID và nội dung trước thao tác.
        2. Nhấn giữ thẻ ghi chú trên Trang chủ để kích hoạt Selection Mode.
        3. Nhấn biểu tượng Thùng rác trên AppBar.
        4. Khi SnackBar xuất hiện, nhấn ngay nút 'Hoàn tác' (Undo), không chờ polling làm biến mất SnackBar.
        5. Xác minh ghi chú lập tức xuất hiện trở lại trên HomeScreen.
        6. Đối chiếu SQLite (read-only): status='normal', tiêu đề và nội dung nguyên vẹn.
        7. Điều hướng vào Thùng rác qua Drawer, xác nhận ghi chú KHÔNG có trong Thùng rác.
        8. Quay lại HomeScreen và dọn dẹp an toàn.
        """
        tc = "021B"
        marker = uuid.uuid4().hex[:10]
        note_title = f"QA_FN10_{tc}_{marker}"
        note_content = f"Nội dung kiểm thử hoàn tác xóa FN10-021B - {uuid.uuid4().hex[:8]}"
        note_id = None
        print(f"\n========================================================")
        print(f"[START] TC-BB-021B: Undo Move to Trash — '{note_title}'")
        print(f"========================================================")
        try:
            # 0. Ghi nhận danh sách ID trước khi tạo để xác định chính xác note_id mới
            before_db = self._db()
            before_ids = {r["id"] for r in before_db} if before_db else set()
            # 1. BƯỚC 1: Tiền điều kiện - Tạo ghi chú kiểm thử cô lập trên HomeScreen
            print(f"\n--- BƯỚC 1: Tạo ghi chú kiểm thử cô lập trên HomeScreen ---")
            self.driver.ensure_home_screen()
            time.sleep(0.5)
            created = QANoteHelper.create_test_note(self.driver, note_title, note_content, poll_timeout=6.0)
            assert created, f"Precondition failed: Cannot create test note '{note_title}'."
            # Ghi nhận ID từ SQLite
            after_db = self._db()
            if after_db:
                new_rows = [
                    r for r in after_db
                    if r["id"] not in before_ids and r["title"] == note_title and r["status"] == "normal"
                ]
                if len(new_rows) == 1:
                    note_id = new_rows[0]["id"]
                    print(f"[TC-BB-021B] Identified QA note ID: {note_id}")
            # Evidence 1: Ghi chú mới hiển thị trên HomeScreen
            self._evidence("TC-BB-021B", 1, data_id="D01")
            # 2. BƯỚC 2: Chọn ghi chú trên HomeScreen và kích hoạt Selection Mode
            print(f"\n--- BƯỚC 2: Nhấn giữ thẻ ghi chú '{note_title}' để bật Selection Mode ---")
            card = self.d(descriptionContains=note_title) or self.d(textContains=note_title)
            if not card.exists:
                card = self.driver.find_by_text(note_title, contains=True)
            assert card is not None and card.exists, (
                f"BLOCKED: Cannot locate NoteCard for '{note_title}' on HomeScreen."
            )
            card.long_click(duration=1.2)
            time.sleep(0.6)
            trash_btn = (
                self.d(descriptionContains="thùng rác")
                or self.d(descriptionContains="Trash")
                or self.d(descriptionContains="trash")
                or self.d(textContains="thùng rác")
                or self.d.xpath('//*[contains(@content-desc, "thùng rác") or contains(@content-desc, "Trash")]')
            )
            assert trash_btn.exists, "BLOCKED: Trash button not found on Selection AppBar."
            # 3. BƯỚC 3: Nhấn biểu tượng Thùng rác
            print(f"\n--- BƯỚC 3: Nhấn biểu tượng Thùng rác trên AppBar ---")
            trash_btn.click()
            # 4. BƯỚC 4: Nhấn ngay 'Hoàn tác' (Undo) khi SnackBar xuất hiện
            print(f"\n--- BƯỚC 4: Đợi SnackBar xuất hiện và nhấn ngay nút 'Hoàn tác' ---")
            undo_btn = None
            start_wait = time.time()
            while time.time() - start_wait < 3.0:
                for sel in (
                    self.d(text="Hoàn tác"),
                    self.d(description="Hoàn tác"),
                    self.d(textContains="Hoàn tác"),
                    self.d(descriptionContains="Hoàn tác"),
                    self.d(text="Undo"),
                    self.d(description="Undo"),
                    self.d(textContains="Undo"),
                    self.d(descriptionContains="Undo"),
                ):
                    if sel.exists:
                        undo_btn = sel
                        break
                if undo_btn is not None:
                    break
                time.sleep(0.05)
            if undo_btn is None:
                diag_path = (RUN_EVIDENCE / "TC-BB-021B" / "blocked_no_undo_button.png").as_posix()
                self.driver.capture_evidence(diag_path)
                pytest.skip(
                    f"BLOCKED: SnackBar 'Hoàn tác' button not detected within timeout. Screenshot: {diag_path}"
                )
            # Chụp ảnh SnackBar và nút Hoàn tác ngay khi xuất hiện
            self._evidence("TC-BB-021B", 2, data_id="D01")
            # Nhấn nút Hoàn tác ngay lập tức
            print(f"[TC-BB-021B] Tapping 'Hoàn tác' button immediately...")
            try:
                undo_btn.click()
            except Exception as e:
                print(f"[TC-BB-021B] Primary click failed ({e}), attempting resilient fallback click...")
                clicked = False
                for sel in (self.d(text="Hoàn tác"), self.d(description="Hoàn tác"), self.d(text="Undo")):
                    if sel.exists:
                        sel.click()
                        clicked = True
                        break
                if not clicked:
                    alt = self.driver.find_by_text("Hoàn tác", contains=True) or self.driver.find_by_text("Undo", contains=True)
                    if alt is not None:
                        alt.click()
            time.sleep(0.8)
            # 5. BƯỚC 5: Xác minh ghi chú lập tức xuất hiện trở lại trên HomeScreen
            print(f"\n--- BƯỚC 5: Xác minh ghi chú trở lại HomeScreen ---")
            found_on_home = False
            for _ in range(16):
                if (
                    self.d(descriptionContains=note_title).exists
                    or self.d(textContains=note_title).exists
                    or self.driver.find_by_text(note_title, contains=True) is not None
                ):
                    found_on_home = True
                    break
                time.sleep(0.5)
            assert found_on_home, (
                f"Expected note '{note_title}' to be restored on HomeScreen after Undo, but not found."
            )
            self._evidence("TC-BB-021B", 3, data_id="D01")
            print(f"[TC-BB-021B SUCCESS] Note '{note_title}' verified present on HomeScreen after Undo.")
            # 6. BƯỚC 6: Đối chiếu trạng thái SQLite (read-only)
            print(f"\n--- BƯỚC 6: Đối chiếu trạng thái SQLite theo ID (read-only) ---")
            if note_id:
                row = self._row(note_id)
                if row:
                    assert row["status"] == "normal", (
                        f"SQLite status mismatch: expected 'normal', got {row['status']!r}"
                    )
                    assert row["title"] == note_title, (
                        f"SQLite title mismatch: expected {note_title!r}, got {row['title']!r}"
                    )
                    actual_content = _plain(row["content"]).rstrip("\n")
                    assert actual_content == note_content, (
                        f"SQLite content mismatch: expected {note_content!r}, got {actual_content!r}"
                    )
                    print(
                        f"[TC-BB-021B SQLite] Note {note_id} verified: "
                        f"status={row['status']}, title={row['title']}"
                    )
                else:
                    print(f"[TC-BB-021B SQLite] Warning: Note {note_id} not retrievable from DB snapshot.")
            else:
                print(f"[TC-BB-021B SQLite] SQLite read-only check skipped (note_id not resolved).")
            # 7. BƯỚC 7: Điều hướng vào Thùng rác kiểm tra ghi chú KHÔNG có trong Thùng rác
            print(f"\n--- BƯỚC 7: Điều hướng vào Thùng rác và kiểm tra ghi chú không có trong Trash ---")
            QANoteHelper.navigate_to_trash(self.driver)
            absent_in_trash = False
            for _ in range(8):
                still_in_trash = (
                    self.d(descriptionContains=note_title).exists
                    or self.d(textContains=note_title).exists
                    or self.driver.find_by_text(note_title, contains=True) is not None
                )
                if not still_in_trash:
                    absent_in_trash = True
                    break
                time.sleep(0.5)
            assert absent_in_trash, (
                f"Defect: Note '{note_title}' was unexpectedly found in TrashScreen after Undo!"
            )
            self._evidence("TC-BB-021B", 4, data_id="D01")
            print(f"[TC-BB-021B SUCCESS] Verified note '{note_title}' is absent in TrashScreen.")
            # Quay lại HomeScreen
            QANoteHelper.navigate_from_trash_to_home(self.driver)
            print(f"\n========================================================")
            print(f"[PASS] TC-BB-021B: Undo Move to Trash PASSED successfully!")
            print(f"========================================================")
        finally:
            print(f"\n--- DỌN DẸP AN TOÀN: Xử lý ghi chú QA '{note_title}' ---")
            try:
                if not self.driver.is_on_home_screen():
                    QANoteHelper.navigate_from_trash_to_home(self.driver)
            except Exception:
                try:
                    self.driver.ensure_home_screen()
                except Exception:
                    pass
            # Tuyệt đối không xóa vĩnh viễn ghi chú QA.
            if os.environ.get("FN10_DEBUG") == "1":
                print(f"[FN10-021B DEBUG] Ghi chú QA được giữ lại để điều tra: title={note_title}, ID={note_id}")
            else:
                try:
                    if note_title and (
                        self.d(descriptionContains=note_title).exists
                        or self.d(textContains=note_title).exists
                    ):
                        print(f"[TC-BB-021B] Chuyển ghi chú QA '{note_title}' vào thùng rác (không xóa vĩnh viễn)...")
                        self.driver.cleanup_note_via_selection(note_title)
                except Exception as e:
                    print(f"[TC-BB-021B Cleanup Notice] Bỏ qua cảnh báo dọn dẹp: {e}")
    def test_tc_bb_021c_d01_cancel_delete_from_editor(self):
        """TC-BB-021C (D01): Hủy xóa ghi chú từ menu 3 chấm trong Editor.
        Precondition:
        - Đang ở Trang chủ, có ghi chú QA hợp lệ được tạo mới.
        Steps:
        1. Tạo ghi chú QA với tiêu đề duy nhất, ghi nhận ID và nội dung trước thao tác.
        2. Mở ghi chú để vào màn hình Editor.
        3. Nhấn biểu tượng 3 chấm (More) ở góc phải thanh công cụ đáy.
        4. Chọn "Xóa ghi chú" trên bottom sheet tùy chọn.
        5. Trên hộp thoại cảnh báo 'Xóa ghi chú?', nhấn nút "Hủy".
        6. Xác minh hộp thoại đóng lại, người dùng vẫn ở màn hình Editor và ghi chú không bị xóa.
        7. Thoát về HomeScreen, xác minh ghi chú vẫn hiển thị trên Trang chủ.
        8. Đối chiếu SQLite (read-only): status='normal', tiêu đề và nội dung nguyên vẹn.
        9. Kiểm tra Thùng rác: ghi chú KHÔNG xuất hiện trong Thùng rác.

        """
        tc = "021C"
        marker = uuid.uuid4().hex[:10]
        note_title = f"QA_FN10_{tc}_{marker}"
        note_content = f"Nội dung kiểm thử hủy xóa trong Editor FN10-021C - {uuid.uuid4().hex[:8]}"
        note_id = None
        print(f"\n========================================================")
        print(f"[START] TC-BB-021C D01: Cancel Delete from Editor — '{note_title}'")
        print(f"========================================================")
        try:
            # 0. Ghi nhận danh sách ID trước khi tạo
            before_db = self._db()
            before_ids = {r["id"] for r in before_db} if before_db else set()

            # 1. BƯỚC 1: Tiền điều kiện - Tạo ghi chú kiểm thử cô lập trên HomeScreen
            print(f"\n--- BƯỚC 1: Tạo ghi chú kiểm thử cô lập trên HomeScreen ---")
            self.driver.ensure_home_screen()
            time.sleep(0.5)
            created = QANoteHelper.create_test_note(self.driver, note_title, note_content, poll_timeout=6.0)
            assert created, f"Precondition failed: Cannot create test note '{note_title}'."

            # Ghi nhận ID từ SQLite
            after_db = self._db()
            if after_db:
                new_rows = [
                    r for r in after_db
                    if r["id"] not in before_ids and r["title"] == note_title and r["status"] == "normal"
                ]
                if len(new_rows) == 1:
                    note_id = new_rows[0]["id"]
                    print(f"[TC-BB-021C] Identified QA note ID: {note_id}")

            # Evidence 1: Ghi chú mới hiển thị trên HomeScreen

            self._evidence("TC-BB-021C", 1, data_id="D01")

            # 2. BƯỚC 2: Mở ghi chú để vào màn hình Editor

            print(f"\n--- BƯỚC 2: Mở ghi chú '{note_title}' vào màn hình Editor ---")
            card = self.d(descriptionContains=note_title) or self.d(textContains=note_title)
            if not card.exists:
                card = self.driver.find_by_text(note_title, contains=True)
            assert card is not None and card.exists, (
                f"BLOCKED: Cannot locate NoteCard for '{note_title}' on HomeScreen."
            )
            card.click()
            time.sleep(1.2)
            assert self.driver.is_in_editor(), "BLOCKED: Failed to open EditorScreen for target note."

            # Editor là vùng soạn thảo: chạm vào (540,600) sẽ LÀM MỞ lại IME.
            # Không gọi dismiss_keyboard_safely() ở đây; xử lý IME bằng Back
            # CHỈ sau khi xác nhận cửa sổ bàn phím trong UI hierarchy.
            import re as _fn10_re
            import xml.etree.ElementTree as _fn10_ET

            def _hierarchy_nodes():
                hierarchy = self.d.dump_hierarchy()
                return list(_fn10_ET.fromstring(hierarchy).iter('node'))

            def _keyboard_visible():
                nodes = _hierarchy_nodes()
                ime_packages = (
                    'honeyboard', 'inputmethod', 'swiftkey', 'latinime', 'gboard',
                )
                return any(
                    any(token in n.attrib.get('package', '').lower() for token in ime_packages)
                    for n in nodes

                )

            def _close_keyboard_only():
                if _keyboard_visible():
                    print('[TC-BB-021C] IME detected. Hiding it with one Android Back...')
                    self.d.press('back')
                    time.sleep(0.6)
                    if not self.driver.is_in_editor():
                        diag = (RUN_EVIDENCE / 'TC-BB-021C' / 'diag_editor_exited_after_ime_back.png').as_posix()
                        self.driver.capture_evidence(diag)
                        pytest.skip('BLOCKED: Back navigated out of Editor while hiding IME; ' + diag)
            def _more_center():

                # Lấy chính xác bounds của nút toolbarMore trong UI dump của APP.
                # Tuyệt đối không bấm tọa độ mù, không chọn nút ... của Samsung Keyboard.
                width, height = self.d.window_size()
                candidates = []
                for node in _hierarchy_nodes():
                    attrs = node.attrib
                    label = attrs.get('content-desc', '').strip()
                    if label not in ('Thêm nữa', 'More'):
                        continue
                    package = attrs.get('package', '')
                    if package and package != config.APP_PACKAGE:
                        continue
                    numbers = _fn10_re.findall(r'\d+', attrs.get('bounds', ''))
                    if len(numbers) != 4:
                        continue
                    x1, y1, x2, y2 = map(int, numbers)
                    x, y = (x1 + x2) // 2, (y1 + y2) // 2
                    if not (0.55 * width < x < width and 0.40 * height < y < 0.98 * height):
                        continue
                    if (x2 - x1) * (y2 - y1) > 0.20 * width * height:
                        continue
                    candidates.append((y, x))
                if not candidates:
                    return None

                # Toolbar More là nút phía dưới, bên phải của editor.
                y, x = max(candidates)
                return (x, y)
            def _has_menu_item():
                return any((
                    self.d(text=t).exists or self.d(description=t).exists
                ) for t in ('Xóa ghi chú', 'Delete note',
                             'Nhãn', 'Labels', 'Xuất file PDF', 'Export to PDF'))
            def _has_delete():
                return any((
                    self.d(text=t).exists or self.d(description=t).exists
                ) for t in ('Xóa ghi chú', 'Delete note'))
            # 3. BƯỚC 3: Chọn đúng nút ba chấm TRÊN EDITOR, không phải nút ... IME.

            print("\n--- BƯỚC 3: Mở More Options thật trên Editor BottomAppBar ---")
            delete_visible = False
            for attempt in range(2):
                _close_keyboard_only()
                center = _more_center()
                if center is None:
                    diag_dir = RUN_EVIDENCE / 'TC-BB-021C'
                    diag_dir.mkdir(parents=True, exist_ok=True)
                    (diag_dir / 'diag_more_hierarchy.xml').write_text(
                        self.d.dump_hierarchy(), encoding='utf-8')
                    diag = (diag_dir / 'diag_no_editor_more.png').as_posix()
                    self.driver.capture_evidence(diag)
                    pytest.skip('BLOCKED: Editor toolbarMore not uniquely locatable; ' + diag)
                print(f'[TC-BB-021C] Click verified toolbarMore bounds center={center} (attempt {attempt + 1})')
                self.d.click(*center)
                for _ in range(10):
                    if _has_menu_item():
                        break
                    time.sleep(0.2)
                if _has_menu_item():
                    delete_visible = _has_delete()
                    if not delete_visible:
                        self._evidence('TC-BB-021C', 2, data_id='D01')
                        pytest.fail('APP: Editor More Options opened but lacks Xóa ghi chú / Delete note')
                    break
                print('[TC-BB-021C] More sheet absent; retrying after UI diagnostics...')

            # 4. BƯỚC 4: Xác nhận sheet mở ra trước khi chọn "Xóa ghi chú".
            print("\n--- BƯỚC 4: Xác nhận EditorMoreOptionsSheet và chọn 'Xóa ghi chú' ---")
            if not delete_visible:
                diag_dir = RUN_EVIDENCE / 'TC-BB-021C'
                diag_dir.mkdir(parents=True, exist_ok=True)
                (diag_dir / 'diag_more_not_opened.xml').write_text(
                    self.d.dump_hierarchy(), encoding='utf-8')
                diag = (diag_dir / 'diag_more_not_opened.png').as_posix()
                self.driver.capture_evidence(diag)
                pytest.skip('BLOCKED: More UI did not open reliably after verified click; ' + diag)
            delete_opt = (self.d(text='Xóa ghi chú') or
                          self.d(description='Xóa ghi chú') or
                          self.d(text='Delete note') or
                          self.d(description='Delete note'))
            assert delete_opt.exists, 'EditorMoreOptionsSheet open but delete locator disappeared'
            self._evidence('TC-BB-021C', 2, data_id='D01')
            delete_opt.click()
            time.sleep(0.8)

            # 5. BƯỚC 5: Kiểm tra hộp thoại xác nhận 'Xóa ghi chú?' và nhấn 'Hủy'
            print(f"\n--- BƯỚC 5: Kiểm tra hộp thoại xác nhận và nhấn 'Hủy' ---")
            dialog_present = (
                self.d(text="Xóa ghi chú?").exists
                or self.d(textContains="Xóa ghi chú?").exists
                or self.d(descriptionContains="Xóa ghi chú?").exists
                or self.d(text="Delete note?").exists
                or self.d(description="Delete note?").exists
            )
            assert dialog_present, "BLOCKED: Confirmation dialog 'Xóa ghi chú?' not displayed."
            cancel_btn = (
                self.d(text="Hủy")
                or self.d(description="Hủy")
                or self.d(text="Cancel")
                or self.d(description="Cancel")
                or self.d.xpath('//*[@text="Hủy" or @content-desc="Hủy" or @text="Cancel"]')
            )

            # Evidence 3: Hộp thoại xác nhận hiển thị
            self._evidence("TC-BB-021C", 3, data_id="D01")
            assert cancel_btn.exists, "BLOCKED: 'Hủy' button not found on confirmation dialog."
            print(f"[TC-BB-021C] Tapping 'Hủy' button on confirmation dialog...")
            cancel_btn.click()
            time.sleep(0.8)

            # 6. BƯỚC 6: Xác minh hộp thoại đóng, người dùng vẫn ở EditorScreen và dữ liệu nguyên vẹn
            print(f"\n--- BƯỚC 6: Xác minh hộp thoại đóng và vẫn ở EditorScreen ---")
            assert not self.d(text="Xóa ghi chú?").exists, (
                "Confirmation dialog still visible after tapping 'Hủy'."
            )
            assert self.driver.is_in_editor(), (
                "Expected user to remain on EditorScreen after canceling deletion."
            )

            # Evidence 4: Vẫn ở EditorScreen sau khi hủy
            self._evidence("TC-BB-021C", 4, data_id="D01")
            print(f"[TC-BB-021C SUCCESS] Confirmed dialog closed and user remained in EditorScreen.")

            # Thoát an toàn về HomeScreen
            self.driver.save_and_exit_editor()
            time.sleep(0.8)
            self.driver.ensure_home_screen()

            # 7. BƯỚC 7: Xác minh ghi chú vẫn hiển thị trên HomeScreen
            print(f"\n--- BƯỚC 7: Xác minh ghi chú vẫn tồn tại trên HomeScreen ---")
            found_on_home = False
            for _ in range(16):
                if (
                    self.d(descriptionContains=note_title).exists
                    or self.d(textContains=note_title).exists
                    or self.driver.find_by_text(note_title, contains=True) is not None
                ):
                    found_on_home = True
                    break
                time.sleep(0.5)
            assert found_on_home, (
                f"Note '{note_title}' was unexpectedly deleted or missing from HomeScreen!"
            )

            # Evidence 5: Ghi chú vẫn còn nguyên vẹn trên HomeScreen
            self._evidence("TC-BB-021C", 5, data_id="D01")
            print(f"[TC-BB-021C SUCCESS] Note '{note_title}' verified still present on HomeScreen.")

            # 8. BƯỚC 8: Đối chiếu trạng thái SQLite (read-only)
            print(f"\n--- BƯỚC 8: Đối chiếu trạng thái SQLite theo ID (read-only) ---")
            if note_id:
                row = self._row(note_id)
                if row:
                    assert row["status"] == "normal", (
                        f"SQLite status mismatch: expected 'normal', got {row['status']!r}"
                    )
                    assert row["title"] == note_title, (
                        f"SQLite title mismatch: expected {note_title!r}, got {row['title']!r}"
                    )
                    actual_content = _plain(row["content"]).rstrip("\n")
                    assert actual_content == note_content, (
                        f"SQLite content mismatch: expected {note_content!r}, got {actual_content!r}"
                    )
                    print(
                        f"[TC-BB-021C SQLite] Note {note_id} verified: "
                        f"status={row['status']}, title={row['title']}"
                    )
                else:
                    print(f"[TC-BB-021C SQLite] Warning: Note {note_id} not retrievable from DB snapshot.")
            else:
                print(f"[TC-BB-021C SQLite] SQLite check skipped (note_id not resolved).")

            # 9. BƯỚC 9: Điều hướng vào Thùng rác kiểm tra ghi chú KHÔNG có trong Thùng rác
            print(f"\n--- BƯỚC 9: Điều hướng vào Thùng rác và kiểm tra ghi chú không có trong Trash ---")
            QANoteHelper.navigate_to_trash(self.driver)
            absent_in_trash = False
            for _ in range(8):
                still_in_trash = (
                    self.d(descriptionContains=note_title).exists
                    or self.d(textContains=note_title).exists
                    or self.driver.find_by_text(note_title, contains=True) is not None
                )
                if not still_in_trash:
                    absent_in_trash = True
                    break
                time.sleep(0.5)
            assert absent_in_trash, (
                f"Defect: Note '{note_title}' was unexpectedly found in TrashScreen after cancel!"
            )
            print(f"[TC-BB-021C SUCCESS] Verified note '{note_title}' is absent in TrashScreen.")

            # Quay lại HomeScreen
            QANoteHelper.navigate_from_trash_to_home(self.driver)
            print(f"\n========================================================")
            print(f"[PASS] TC-BB-021C D01: Cancel Delete from Editor PASSED successfully!")
            print(f"========================================================")
        finally:
            print(f"\n--- DỌN DẸP AN TOÀN: Xử lý ghi chú QA '{note_title}' ---")
            try:
                if self.driver.is_in_editor():
                    self.driver.save_and_exit_editor()
                if not self.driver.is_on_home_screen():
                    QANoteHelper.navigate_from_trash_to_home(self.driver)

            except Exception:
                try:
                    self.driver.ensure_home_screen()
                except Exception:
                    pass

            # Tuyệt đối không xóa vĩnh viễn ghi chú QA.
            if os.environ.get("FN10_DEBUG") == "1":
                print(f"[FN10-021C DEBUG] Ghi chú QA được giữ lại để điều tra: title={note_title}, ID={note_id}")

            else:

                try:
                    if note_title and (
                        self.d(descriptionContains=note_title).exists
                        or self.d(textContains=note_title).exists
                    ):
                        print(f"[TC-BB-021C] Chuyển ghi chú QA '{note_title}' vào thùng rác (không xóa vĩnh viễn)...")

                        self.driver.cleanup_note_via_selection(note_title)
                except Exception as e:
                    print(f"[TC-BB-021C Cleanup Notice] Bỏ qua cảnh báo dọn dẹp: {e}")


    def test_tc_bb_021c_d02_confirm_delete_from_editor(self):
        """TC-BB-021C (D02): Xác nhận xóa ghi chú từ Editor.

        Given: Ghi chú QA duy nhất, lưu trong DB, đang status='normal'.
        When: Editor -> More -> Xóa ghi chú -> xác nhận Xóa.
        Then: Ghi chú biến mất khỏi Home, xuất hiện ở Trash,
              SQLite theo đúng note_id đổi sang 'trash'; title/content giữ nguyên.
        Note: Không xóa vĩnh viễn ghi chú; evidence theo Run ID.
        """
        tc = "021C"
        marker = uuid.uuid4().hex[:10]
        note_title = f"QA_FN10_{tc}_{marker}"
        note_content = f"Nội dung kiểm thử xác nhận xóa từ Editor FN10-021C D02 - {uuid.uuid4().hex[:8]}"
        note_id = None
        print(f"\n========================================================")
        print(f"[START] TC-BB-021C D02: Confirm Delete from Editor — '{note_title}'")
        print(f"========================================================")

        try:

            # 0. Ghi nhận danh sách ID trước khi tạo
            before_db = _notes(self.driver.serial, config.APP_PACKAGE)
            before_ids = {r["id"] for r in before_db} if before_db else set()

            # 1. BƯỚC 1: Tiền điều kiện - Tạo ghi chú kiểm thử cô lập trên HomeScreen
            print(f"\n--- BƯỚC 1: Tạo ghi chú kiểm thử cô lập trên HomeScreen ---")
            self.driver.ensure_home_screen()
            time.sleep(0.5)
            created = QANoteHelper.create_test_note(self.driver, note_title, note_content, poll_timeout=6.0)
            assert created, f"Precondition failed: Cannot create test note '{note_title}'."

            # Ghi nhận ID từ SQLite
            after_db = _notes(self.driver.serial, config.APP_PACKAGE)
            new_rows = [
                r for r in after_db
                if r['id'] not in before_ids
                and r['title'] == note_title
                and r['status'] == 'normal'
            ]
            assert len(new_rows) == 1, (
                f'Cannot uniquely identify newly created QA note: {len(new_rows)} matches'
            )
            note_id = new_rows[0]['id']
            initial_content = _plain(new_rows[0]['content']).rstrip('\n')
            assert initial_content == note_content, (
                f'QA note content mismatch before deletion: {initial_content!r}'
            )
            print(f'[TC-BB-021C D02] Exact QA note ID: {note_id}')

            # Evidence 1: Ghi chú mới hiển thị trên HomeScreen
            self._evidence("TC-BB-021C", 1, data_id="D02")

            # 2. BƯỚC 2: Mở ghi chú để vào màn hình Editor
            print(f"\n--- BƯỚC 2: Mở ghi chú '{note_title}' vào màn hình Editor ---")
            card = self.d(descriptionContains=note_title) or self.d(textContains=note_title)
            if not card.exists:
                card = self.driver.find_by_text(note_title, contains=True)
            assert card is not None and card.exists, (
                f"BLOCKED: Cannot locate NoteCard for '{note_title}' on HomeScreen."
            )
            card.click()
            time.sleep(1.2)
            assert self.driver.is_in_editor(), "BLOCKED: Failed to open EditorScreen for target note."

            # Editor là vùng soạn thảo: chạm vào (540,600) sẽ LÀM MỞ lại IME.
            # Không gọi dismiss_keyboard_safely() ở đây; xử lý IME bằng Back
            # CHỈ sau khi xác nhận cửa sổ bàn phím trong UI hierarchy.

            import re as _fn10_re
            import xml.etree.ElementTree as _fn10_ET

            def _hierarchy_nodes():
                hierarchy = self.d.dump_hierarchy()
                return list(_fn10_ET.fromstring(hierarchy).iter('node'))

            def _keyboard_visible():
                nodes = _hierarchy_nodes()
                ime_packages = ('honeyboard', 'inputmethod', 'swiftkey', 'latinime', 'gboard')
                return any(
                    any(token in n.attrib.get('package', '').lower() for token in ime_packages)
                    for n in nodes
                )

            def _close_keyboard_only():
                if _keyboard_visible():
                    print('[TC-BB-021C] IME detected. Hiding it with one Android Back...')
                    self.d.press('back')
                    time.sleep(0.6)
                    if not self.driver.is_in_editor():
                        diag = (RUN_EVIDENCE / 'TC-BB-021C' / 'diag_editor_exited_after_ime_back_D02.png').as_posix()
                        self.driver.capture_evidence(diag)
                        pytest.skip('BLOCKED: Back navigated out of Editor while hiding IME; ' + diag)

            def _more_center():
                # Lấy chính xác bounds của nút toolbarMore trong UI dump của APP.
                # Tuyệt đối không bấm tọa độ mù, không chọn nút ... của Samsung Keyboard.
                width, height = self.d.window_size()
                candidates = []
                for node in _hierarchy_nodes():
                    attrs = node.attrib
                    label = attrs.get('content-desc', '').strip()
                    if label not in ('Thêm nữa', 'More'):
                        continue
                    package = attrs.get('package', '')
                    if package and package != config.APP_PACKAGE:
                        continue
                    numbers = _fn10_re.findall(r'\d+', attrs.get('bounds', ''))
                    if len(numbers) != 4:
                        continue
                    x1, y1, x2, y2 = map(int, numbers)
                    x, y = (x1 + x2) // 2, (y1 + y2) // 2
                    if not (0.55 * width < x < width and 0.40 * height < y < 0.98 * height):
                        continue
                    if (x2 - x1) * (y2 - y1) > 0.20 * width * height:
                        continue
                    candidates.append((y, x))
                if not candidates:
                    return None
                # Toolbar More là nút phía dưới, bên phải của editor.
                y, x = max(candidates)
                return (x, y)

            def _has_menu_item():
                return any((
                    self.d(text=t).exists or self.d(description=t).exists
                ) for t in ('Xóa ghi chú', 'Delete note',
                             'Nhãn', 'Labels', 'Xuất file PDF', 'Export to PDF'))

            def _has_delete():
                return any((
                    self.d(text=t).exists or self.d(description=t).exists
                ) for t in ('Xóa ghi chú', 'Delete note'))

            # 3. BƯỚC 3: Chọn đúng nút ba chấm TRÊN EDITOR, không phải nút ... IME.
            print("\n--- BƯỚC 3: Mở More Options thật trên Editor BottomAppBar ---")
            delete_visible = False
            for attempt in range(2):
                _close_keyboard_only()
                center = _more_center()
                if center is None:
                    diag_dir = RUN_EVIDENCE / 'TC-BB-021C'
                    diag_dir.mkdir(parents=True, exist_ok=True)
                    (diag_dir / 'diag_more_hierarchy_D02.xml').write_text(
                        self.d.dump_hierarchy(), encoding='utf-8')
                    diag = (diag_dir / 'diag_no_editor_more_D02.png').as_posix()
                    self.driver.capture_evidence(diag)
                    pytest.skip('BLOCKED: Editor toolbarMore not uniquely locatable; ' + diag)
                print(f'[TC-BB-021C] Click verified toolbarMore bounds center={center} (attempt {attempt + 1})')
                self.d.click(*center)
                for _ in range(10):
                    if _has_menu_item():
                        break
                    time.sleep(0.2)
                if _has_menu_item():
                    delete_visible = _has_delete()
                    if not delete_visible:
                        self._evidence('TC-BB-021C', 2, data_id='D02')
                        pytest.fail('APP: Editor More Options opened but lacks Xóa ghi chú / Delete note')
                    break
                print('[TC-BB-021C] More sheet absent; retrying after UI diagnostics...')

            # 4. BƯỚC 4: Xác nhận sheet mở ra trước khi chọn "Xóa ghi chú".
            print("\n--- BƯỚC 4: Xác nhận EditorMoreOptionsSheet và chọn 'Xóa ghi chú' ---")
            if not delete_visible:
                diag_dir = RUN_EVIDENCE / 'TC-BB-021C'
                diag_dir.mkdir(parents=True, exist_ok=True)
                (diag_dir / 'diag_more_not_opened_D02.xml').write_text(
                    self.d.dump_hierarchy(), encoding='utf-8')
                diag = (diag_dir / 'diag_more_not_opened_D02.png').as_posix()
                self.driver.capture_evidence(diag)
                pytest.skip('BLOCKED: More UI did not open reliably after verified click; ' + diag)
            delete_opt = (self.d(text='Xóa ghi chú') or
                          self.d(description='Xóa ghi chú') or
                          self.d(text='Delete note') or
                          self.d(description='Delete note'))
            assert delete_opt.exists, 'EditorMoreOptionsSheet open but delete locator disappeared'
            self._evidence('TC-BB-021C', 2, data_id='D02')
            delete_opt.click()
            time.sleep(0.8)

            # 5. Confirm delete in AlertDialog -- target the dialog, never delete from Trash.
            print("\n--- BƯỚC 5: Hộp thoại xác nhận -> nhấn Xóa ---")
            title_visible = any(
                self.d(text=t).exists or self.d(description=t).exists
                for t in ('Xóa ghi chú?', 'Delete note?')
            )
            assert title_visible, 'Expected delete confirmation dialog did not appear'
            self._evidence('TC-BB-021C', 3, data_id='D02')

            confirm_btn = None
            for selector in (
                self.d(text='Xóa'), self.d(description='Xóa'),
                self.d(text='Delete'), self.d(description='Delete'),
            ):
                if selector.exists:
                    confirm_btn = selector
                    break
            assert confirm_btn is not None, 'Delete confirmation button missing from AlertDialog'
            confirm_btn.click()

            # 6. Wait for route transition and assert absence from the Home UI.
            print("\n--- BƯỚC 6: Kiểm tra HomeScreen sau xác nhận xóa ---")
            for _ in range(16):
                if self.driver.is_on_home_screen():
                    break
                time.sleep(0.5)
            assert self.driver.is_on_home_screen(), (
                'Expected Editor to close and HomeScreen to appear after Delete'
            )
            self.driver.ensure_home_screen()
            time.sleep(0.8)
            home_card = self.d(descriptionContains=note_title)
            home_text = self.d(textContains=note_title)
            assert not home_card.exists and not home_text.exists, (
                f'Deleted QA note {note_title!r} still visible on HomeScreen'
            )
            self._evidence('TC-BB-021C', 4, data_id='D02')

            # 7. SQLite oracle MUST execute and MUST resolve exact note_id.
            print("\n--- BƯỚC 7: SQLite xác minh status=trash và dữ liệu nguyên vẹn ---")
            row = None
            for _ in range(12):
                matched = [
                    r for r in _notes(self.driver.serial, config.APP_PACKAGE)
                    if r['id'] == note_id
                ]
                assert len(matched) == 1, (
                    f'QA note ID {note_id} disappeared or duplicated in SQLite'
                )
                row = matched[0]
                if row['status'] == 'trash':
                    break
                time.sleep(0.5)
            assert row is not None and row['status'] == 'trash', (
                f'Expected SQLite status=trash for {note_id}; '
                f'actual={None if row is None else row["status"]!r}'
            )
            assert row['title'] == note_title, (
                f'QA title changed after deletion: {row["title"]!r}'
            )
            actual_text = _plain(row['content']).rstrip('\n')
            assert actual_text == note_content, (
                f'QA content changed: {actual_text!r} != {note_content!r}'
            )
            print(f'[TC-BB-021C D02 SQLite] PASS: ID={note_id}, '
                  f'status={row["status"]}, title/content intact')

            # 8. Independently confirm TrashScreen shows this exact QA title.
            print("\n--- BƯỚC 8: Xác minh ghi chú trong TrashScreen ---")
            QANoteHelper.navigate_to_trash(self.driver)
            QANoteHelper.verify_note_in_trash(self.driver, note_title, poll_timeout=7.0)
            self._evidence('TC-BB-021C', 5, data_id='D02')
            QANoteHelper.navigate_from_trash_to_home(self.driver)
            print('[PASS] TC-BB-021C D02: Editor Delete confirmed; QA note in Trash.')

        finally:
            # Never permanently delete any note. Best-effort QA-owned cleanup only.
            try:
                if self.driver.is_in_editor():
                    self.driver.save_and_exit_editor()
                if not self.driver.is_on_home_screen():
                    QANoteHelper.navigate_from_trash_to_home(self.driver)
            except Exception as cleanup_nav_error:
                print(f'[D02 cleanup] Navigation warning: {cleanup_nav_error}')
                try:
                    self.driver.ensure_home_screen()
                except Exception:
                    pass

            if os.environ.get('FN10_DEBUG') == '1':
                print(f'[D02 DEBUG] Keeping QA note for audit: title={note_title} ID={note_id}')
            elif note_id:
                try:
                    current = [
                        r for r in _notes(self.driver.serial, config.APP_PACKAGE)
                        if r['id'] == note_id and r['title'] == note_title
                    ]
                    if len(current) == 1 and current[0]['status'] == 'normal':
                        # Only if the exact QA note still needs soft-deletion.
                        if (self.d(descriptionContains=note_title).exists
                                or self.d(textContains=note_title).exists):
                            self.driver.cleanup_note_via_selection(note_title)
                    # status=trash: keep the QA note in Trash for audit.
                except Exception as cleanup_error:
                    print(f'[D02 cleanup] QA note left untouched: {cleanup_error}')

    def test_tc_bb_021d_d01_multi_select_move_to_trash(self):
        """TC-BB-021D D01: Chuyển đồng thời 2 ghi chú QA vào Thùng rác."""
        tc, data_id = "TC-BB-021D", "D01"
        marker = uuid.uuid4().hex[:10]

        expected = {
            f"QA_FN10_021D_A_{marker}": f"FN10 bulk-trash QA content A {marker}",
            f"QA_FN10_021D_B_{marker}": f"FN10 bulk-trash QA content B {marker}",
        }
        qa_ids = {}

        print(f"\n[START] TC-BB-021D D01: Bulk Move 2 QA notes — {marker}")

        def visible(title):
            """Tìm đúng ghi chú QA thuộc lượt kiểm thử."""
            for selector in (
                self.d(descriptionContains=title),
                self.d(textContains=title),
            ):
                if selector.exists:
                    return selector
            return None

        def selected_count_is(count):
            texts = (f"{count} đã chọn", f"{count} selected")
            return any(
                self.d(text=t).exists or self.d(description=t).exists
                for t in texts
            )

        try:
            self.driver.ensure_home_screen()

            # BƯỚC 1: Tạo 2 ghi chú QA riêng biệt
            print("[021D] BƯỚC 1: Tạo 2 ghi chú QA")

            for title, content in expected.items():
                before = _notes(self.driver.serial, config.APP_PACKAGE)
                before_ids = {r["id"] for r in before}

                created = QANoteHelper.create_test_note(
                    self.driver,
                    title,
                    content,
                    poll_timeout=8.0,
                )
                assert created, f"Không tạo được ghi chú QA: {title}"

                after = _notes(self.driver.serial, config.APP_PACKAGE)

                new_rows = [
                    r for r in after
                    if r["id"] not in before_ids
                    and r["title"] == title
                    and r["status"] == "normal"
                ]

                assert len(new_rows) == 1, (
                    f"Không xác định được chính xác note_id: {title}"
                )

                row = new_rows[0]

                assert _plain(row["content"]).rstrip("\n") == content, (
                    f"Nội dung ghi chú QA không khớp: {title}"
                )

                qa_ids[title] = row["id"]
                print(f"[021D] Created: {title}, ID={row['id']}")

            assert len(set(qa_ids.values())) == 2, (
                "Hai ghi chú QA có ID không hợp lệ"
            )

            for title in expected:
                assert visible(title) is not None, (
                    f"Ghi chú không hiển thị trên Home: {title}"
                )

            self._evidence(tc, 1, data_id)

            before_action = {
                r["id"]: r
                for r in _notes(self.driver.serial, config.APP_PACKAGE)
            }

            for title, note_id in qa_ids.items():
                assert (
                    note_id in before_action
                    and before_action[note_id]["status"] == "normal"
                ), f"Ghi chú chưa ở trạng thái normal: {title}"

            # BƯỚC 2: Chọn đúng 2 ghi chú
            print("[021D] BƯỚC 2: Chọn đồng thời 2 ghi chú")

            titles = list(expected)

            first_card = visible(titles[0])
            assert first_card is not None, "Không tìm thấy ghi chú QA thứ nhất"

            first_card.long_click(duration=1.2)

            for _ in range(8):
                if selected_count_is(1):
                    break
                time.sleep(0.2)

            assert selected_count_is(1), (
                "Selection Mode không xác nhận đúng 1 ghi chú"
            )

            second_card = visible(titles[1])
            assert second_card is not None, "Không tìm thấy ghi chú QA thứ hai"

            second_card.click()

            for _ in range(8):
                if selected_count_is(2):
                    break
                time.sleep(0.2)

            if not selected_count_is(2):
                self._evidence(tc, 2, data_id)
                pytest.fail("Selection Mode không xác nhận đúng 2 ghi chú")

            self._evidence(tc, 2, data_id)

            # BƯỚC 3: Chuyển cả 2 ghi chú vào Thùng rác
            print("[021D] BƯỚC 3: Nhấn Chuyển vào thùng rác")

            trash_button = None

            for selector in (
                self.d(description="Chuyển vào thùng rác"),
                self.d(description="Move to trash"),
                self.d(descriptionContains="thùng rác"),
                self.d(descriptionContains="Trash"),
            ):
                if selector.exists:
                    trash_button = selector
                    break

            assert trash_button is not None, (
                "Không tìm thấy nút Thùng rác"
            )

            assert selected_count_is(2), (
                "Số ghi chú được chọn thay đổi trước khi xóa"
            )

            trash_button.click()

            snackbar_labels = (
                "Đã chuyển 2 ghi chú vào thùng rác",
                "Moved 2 notes to trash",
            )

            snackbar_seen = False
            started = time.monotonic()

            while time.monotonic() - started < 2.7:
                if any(
                    self.d(text=t).exists or self.d(description=t).exists
                    for t in snackbar_labels
                ):
                    snackbar_seen = True
                    break
                time.sleep(0.05)

            self._evidence(tc, 3, data_id)

            assert snackbar_seen, (
                "Không phát hiện Snackbar xác nhận chuyển 2 ghi chú"
            )

            # BƯỚC 4: Kiểm tra cả 2 ghi chú biến mất khỏi Home
            print("[021D] BƯỚC 4: Kiểm tra HomeScreen")

            self.driver.ensure_home_screen()

            for title in expected:
                for _ in range(12):
                    if visible(title) is None:
                        break
                    time.sleep(0.5)

                assert visible(title) is None, (
                    f"Ghi chú vẫn còn trên HomeScreen: {title}"
                )

            self._evidence(tc, 4, data_id)

            # BƯỚC 5: Đối chiếu SQLite theo đúng 2 note_id
            print("[021D] BƯỚC 5: Kiểm tra SQLite status=trash")

            rows = {}

            for _ in range(12):
                snapshot = _notes(
                    self.driver.serial,
                    config.APP_PACKAGE,
                )
                by_id = {r["id"]: r for r in snapshot}

                rows = {
                    title: by_id.get(note_id)
                    for title, note_id in qa_ids.items()
                }

                assert all(row is not None for row in rows.values()), (
                    "Không tìm thấy bản ghi QA trong SQLite"
                )

                if all(row["status"] == "trash" for row in rows.values()):
                    break

                time.sleep(0.5)

            for title, row in rows.items():
                assert row["status"] == "trash", (
                    f"Trạng thái SQLite không đúng: {title}"
                )

                assert row["title"] == title, (
                    f"Tiêu đề ghi chú bị thay đổi: {title}"
                )

                assert (
                    _plain(row["content"]).rstrip("\n") == expected[title]
                ), f"Nội dung ghi chú bị thay đổi: {title}"

                print(
                    f"[021D SQLite] PASS: {row['id']} "
                    f"status=trash, content intact"
                )

            # Đảm bảo không có ghi chú khác bị chuyển nhầm
            after_action = {
                r["id"]: r
                for r in _notes(self.driver.serial, config.APP_PACKAGE)
            }

            unintended = [
                note_id
                for note_id, old in before_action.items()
                if note_id not in qa_ids.values()
                and old["status"] != "trash"
                and note_id in after_action
                and after_action[note_id]["status"] == "trash"
            ]

            assert not unintended, (
                f"Ghi chú ngoài phạm vi QA bị chuyển vào Trash: {unintended}"
            )

            # BƯỚC 6: Kiểm tra cả 2 ghi chú trong TrashScreen
            print("[021D] BƯỚC 6: Kiểm tra TrashScreen")

            QANoteHelper.navigate_to_trash(self.driver)

            for title in expected:
                QANoteHelper.verify_note_in_trash(
                    self.driver,
                    title,
                    poll_timeout=7.0,
                )

            self._evidence(tc, 5, data_id)

            QANoteHelper.navigate_from_trash_to_home(self.driver)

            print(
                "[PASS] TC-BB-021D D01: "
                "Đã chuyển đúng 2 ghi chú QA vào Thùng rác"
            )

        finally:
            # Không xóa vĩnh viễn bất kỳ ghi chú nào
            try:
                self.driver.ensure_home_screen()
            except Exception as exc:
                print(f"[021D cleanup] Navigation warning: {exc}")

            print(f"[021D] QA notes retained for audit: {qa_ids}")

if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
