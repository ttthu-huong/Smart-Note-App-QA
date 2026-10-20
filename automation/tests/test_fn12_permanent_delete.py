# -*- coding: utf-8 -*-
"""Automation UI Test Suite for FN-12: Permanent Delete Note from Trash.

Test Cases:
- TC-BB-023: Xóa vĩnh viễn 1 ghi chú khỏi Thùng rác kèm xác nhận (D01)
- TC-BB-023B D01: Chọn 2 ghi chú -> Xóa vĩnh viễn -> Hủy
- TC-BB-023B D02: Chọn 2 ghi chú -> Xóa vĩnh viễn -> Xác nhận

Standards: IEEE 829 & ISTQB Manual / Automation Execution
Device: Samsung Galaxy S21 FE 5G (Android 14)
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
from automation.core.qa_note_helper import QANoteHelper


class TestFN12DeleteForever:
    """Test Suite for FN-12: Xóa ghi chú vĩnh viễn."""

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

    def test_tc_bb_023_permanent_delete_from_trash(self):
        """TC-BB-023 (D01): Xóa vĩnh viễn ghi chú khỏi Thùng rác.

        Expected Result:
        - Ghi chú biến mất hoàn toàn khỏi danh sách Thùng rác.
        - Quay lại Trang chủ xác nhận ghi chú không còn tồn tại trên ứng dụng.
        """
        note_title = f"DeleteForever_{int(time.time())}"
        note_content = "Nội dung kiểm thử xóa vĩnh viễn khỏi hệ thống"

        print(f"\n========================================================")
        print(f"[START] TC-BB-023: Permanent Delete Note — '{note_title}'")
        print(f"========================================================")

        try:
            # 1. Tiền điều kiện: Chuẩn bị 1 ghi chú kiểm thử nằm sẵn trong Thùng rác
            print(f"\n--- BƯỚC 1: Tạo ghi chú kiểm thử cô lập trên HomeScreen ---")
            QANoteHelper.create_test_note(self.driver, note_title, note_content, poll_timeout=6.0)

            print(f"\n--- BƯỚC 2: Chuyển ghi chú vào Thùng rác để tạo tiền điều kiện ---")
            QANoteHelper.move_note_to_trash_from_home(self.driver, note_title)

            print(f"\n--- BƯỚC 3: Mở Thùng rác và xác nhận ghi chú đã có trong Thùng rác ---")
            QANoteHelper.navigate_to_trash(self.driver)
            QANoteHelper.verify_note_in_trash(self.driver, note_title, poll_timeout=5.0)

            # 2. Thao tác chính: Chọn "Xóa vĩnh viễn" và xác nhận hộp thoại nếu có
            print(f"\n--- BƯỚC 4: Chọn 'Xóa vĩnh viễn' và xác nhận trên hộp thoại ---")
            QANoteHelper.permanently_delete_note_from_trash(self.driver, note_title)

            # 3. Xác minh bước 1: Ghi chú biến mất hoàn toàn khỏi Thùng rác
            print(f"\n--- BƯỚC 5: Xác minh ghi chú đã biến mất khỏi Thùng rác ---")
            QANoteHelper.verify_note_absent_in_trash(self.driver, note_title)

            # 4. Điều hướng: Quay lại Trang chủ
            print(f"\n--- BƯỚC 6: Điều hướng quay về Trang chủ qua Drawer ---")
            QANoteHelper.navigate_from_trash_to_home(self.driver)

            # 5. Xác minh bước 2: Ghi chú không tồn tại trên Trang chủ
            print(f"\n--- BƯỚC 7: Xác minh ghi chú không tồn tại trên HomeScreen ---")
            QANoteHelper.verify_note_absent_on_home(self.driver, note_title)

            # 6. Chụp ảnh bằng chứng thực thi thành công
            ev_path = self.driver.capture_evidence("evidence/fn12/FN12_TC-BB-023_D01_01.png")
            print(f"\n[PASS] TC-BB-023 hoàn tất thành công! Bằng chứng đã lưu: {ev_path}")

        finally:
            # Dọn dẹp an toàn: Đảm bảo app ở Trang chủ
            print(f"\n--- DỌN DẸP: Đảm bảo trở về HomeScreen ---")
            try:
                self.driver.ensure_home_screen()
            except Exception as e:
                print(f"[Cleanup Notice] Ignored cleanup warning: {e}")


    def test_tc_bb_023b_d01_cancel_multi_permanent_delete(self):
        """TC-BB-023B D01: Chọn 2 ghi chú trong Trash, Xóa vĩnh viễn -> Hủy."""
        import json
        import sqlite3
        import subprocess
        import uuid
        from datetime import datetime
        from pathlib import Path
        from automation import config

        marker = uuid.uuid4().hex[:10]
        items = {
            f"QA_FN12_023B_A_{marker}": f"FN12 cancel delete QA A {marker}",
            f"QA_FN12_023B_B_{marker}": f"FN12 cancel delete QA B {marker}",
        }
        note_ids = {}
        saved_rows = {}
        folder = (Path("evidence/fn12") /
                  f"automation_{datetime.now():%Y%m%d_%H%M%S_%f}_{marker}" /
                  "TC-BB-023B")
        d = self.d

        def read_db():
            cmd = ["adb", "-s", self.driver.serial, "exec-out", "run-as",
                   config.APP_PACKAGE, "cat", "databases/smart_note.db"]
            result = subprocess.run(cmd, capture_output=True, timeout=25)
            assert result.returncode == 0 and result.stdout, (
                f"SQLite read-only unavailable: {result.stderr.decode(errors='replace')}")
            conn = sqlite3.connect(":memory:")
            try:
                conn.deserialize(result.stdout)
                rows = conn.execute(
                    "SELECT id, title, content, status FROM notes").fetchall()
                return {r[0]: dict(zip(("id", "title", "content", "status"), r))
                        for r in rows}
            finally:
                conn.close()

        def as_text(raw):
            try:
                delta = json.loads(raw)
                if isinstance(delta, dict):
                    delta = delta.get("ops", delta)
                if isinstance(delta, list):
                    return "".join(x.get("insert", "") for x in delta
                                   if isinstance(x, dict) and
                                   isinstance(x.get("insert"), str)).rstrip("\n")
            except (ValueError, TypeError):
                pass
            return (raw or "").rstrip("\n")

        def card(title):
            for sel in (d(descriptionContains=title), d(textContains=title)):
                if sel.exists:
                    return sel
            return None

        def selected(n):
            return any(d(text=t).exists or d(description=t).exists
                       for t in (f"{n} đã chọn", f"{n} selected"))

        def has_label(value):
            return (
                d(textContains=value).exists
                or d(descriptionContains=value).exists
            )

        def dialog_open():
            return any(has_label(s) for s in (
                "Xóa vĩnh viễn?",
                "Delete permanently?",
                "Hành động này không thể hoàn tác",
                "This action cannot be undone",
            ))

        def cancel_button():
            # Chỉ trả về nút Hủy; tuyệt đối không tìm hoặc bấm nút Xóa.
            for sel in (
                d(text="Hủy"), d(description="Hủy"),
                d(text="Cancel"), d(description="Cancel"),
            ):
                if sel.exists:
                    return sel
            return None

        def evidence(number):
            path = (folder / f"FN12_TC-BB-023B_D01_{number:02d}.png").as_posix()
            self.driver.capture_evidence(path)
            print(f"[023B D01 evidence] {path}")

        print(f"[START] TC-BB-023B D01: Cancel multi permanent delete {marker}")

        try:
            self.driver.ensure_home_screen()

            # BƯỚC 1: Tạo đúng 2 ghi chú QA, chuyển vào Thùng rác.
            for title, content in items.items():
                before_ids = set(read_db())
                assert QANoteHelper.create_test_note(
                    self.driver, title, content, poll_timeout=8.0)

                new_rows = [r for id_, r in read_db().items()
                            if id_ not in before_ids and r["title"] == title
                            and r["status"] == "normal"]

                assert len(new_rows) == 1, f"QA note ID not unique: {title}"
                note_ids[title] = new_rows[0]["id"]
                assert as_text(new_rows[0]["content"]) == content

                QANoteHelper.move_note_to_trash_from_home(self.driver, title)

            assert len(set(note_ids.values())) == 2
            QANoteHelper.navigate_to_trash(self.driver)

            for title, note_id in note_ids.items():
                QANoteHelper.verify_note_in_trash(self.driver, title)
                row = read_db().get(note_id)

                assert row is not None and row["status"] == "trash"
                assert row["title"] == title
                assert as_text(row["content"]) == items[title]
                saved_rows[title] = row

            evidence(1)

            # BƯỚC 2: Chọn đúng 2 ghi chú QA.
            titles = list(items)
            first = card(titles[0])
            assert first is not None, "First QA card missing in Trash"
            first.long_click(duration=1.2)

            for _ in range(10):
                if selected(1):
                    break
                time.sleep(0.2)

            assert selected(1), "Expected exactly one selected Trash note"

            second = card(titles[1])
            assert second is not None, "Second QA card missing in Trash"
            second.click()

            for _ in range(10):
                if selected(2):
                    break
                time.sleep(0.2)

            assert selected(2), "Expected exactly two selected Trash notes"
            evidence(2)

            # BƯỚC 3: Mở hộp thoại Xóa vĩnh viễn.
            # Không nhấn nút xác nhận Xóa.
            action = None
            for sel in (d(description="Xóa vĩnh viễn"),
                        d(description="Delete forever")):
                if sel.exists:
                    action = sel
                    break

            assert action is not None, "Delete-forever AppBar control missing"
            assert selected(2), "Selection changed before opening dialog"

            action.click()

            for _ in range(12):
                if dialog_open():
                    break
                time.sleep(0.25)

            if not dialog_open():
                # Chụp đúng thời điểm lỗi, không thử click tọa độ mù.
                evidence(3)
                import re
                xml = d.dump_hierarchy()
                labels = re.findall(r'(?:text|content-desc)="([^"]*)"', xml)
                relevant = [
                    value for value in labels
                    if any(k in value.lower() for k in (
                        "xóa", "hủy", "delete", "cancel", "chọn", "selected"
                    ))
                ]
                print("[023B DEBUG] Visible UI labels:", relevant[:40])
                pytest.fail(
                    "Không nhận diện được hộp thoại xác nhận. "
                    "Kiểm tra evidence 03 và [023B DEBUG]."
                )

            assert (
                has_label("2 ghi chú đã chọn")
                or has_label("2 selected notes")
            ), "Dialog does not confirm deletion of exactly 2 notes"

            evidence(3)

            # BƯỚC 4: Chỉ nhấn HỦY.
            cancel = cancel_button()
            assert cancel is not None, "Cancel button missing from confirmation"
            cancel.click()

            for _ in range(10):
                if not dialog_open():
                    break
                time.sleep(0.2)

            assert not dialog_open(), (
                "Confirmation dialog stayed open after Cancel"
            )
            evidence(4)

            # BƯỚC 5: SQLite và Trash phải giữ nguyên cả 2 ghi chú.
            rows = read_db()

            for title, note_id in note_ids.items():
                assert rows.get(note_id) == saved_rows[title], (
                    f"Note changed/deleted despite Cancel: {note_id}"
                )
                QANoteHelper.verify_note_in_trash(self.driver, title)
                print(f"[023B D01 SQLite] PASS: {note_id} still in trash")

            evidence(5)

            print("[PASS] TC-BB-023B D01: Cancel preserved both QA notes")

        finally:
            # Nếu hộp thoại còn mở, chỉ được nhấn Hủy.
            # Không xóa vĩnh viễn bất kỳ ghi chú nào.
            if dialog_open():
                safe_cancel = cancel_button()
                if safe_cancel is not None:
                    safe_cancel.click()

            print(
                f"[023B D01 Audit] QA notes retained "
                f"(no permanent deletion): {note_ids}"
            )
    def test_tc_bb_023b_d02_confirm_multi_permanent_delete(self):
        """TC-BB-023B D02: Chỉ xóa vĩnh viễn 2 ghi chú QA mới tạo."""
        import json
        import sqlite3
        import subprocess
        import uuid
        from datetime import datetime
        from pathlib import Path
        from automation import config

        marker = uuid.uuid4().hex[:10]
        notes = {
            f"QA_FN12_023B_D02_A_{marker}": f"FN12 confirm delete QA A {marker}",
            f"QA_FN12_023B_D02_B_{marker}": f"FN12 confirm delete QA B {marker}",
        }
        note_ids = {}
        folder = (Path("evidence/fn12") /
                  f"automation_{datetime.now():%Y%m%d_%H%M%S_%f}_{marker}" /
                  "TC-BB-023B")
        d = self.d
        confirmed = False

        def read_db():
            cmd = ["adb", "-s", self.driver.serial, "exec-out", "run-as",
                   config.APP_PACKAGE, "cat", "databases/smart_note.db"]
            result = subprocess.run(cmd, capture_output=True, timeout=25)
            assert result.returncode == 0 and result.stdout, (
                "SQLite read-only unavailable: " +
                result.stderr.decode(errors="replace"))
            conn = sqlite3.connect(":memory:")
            try:
                conn.deserialize(result.stdout)
                rows = conn.execute(
                    "SELECT id, title, content, status FROM notes").fetchall()
                return {r[0]: dict(zip(("id", "title", "content", "status"), r))
                        for r in rows}
            finally:
                conn.close()

        def as_text(raw):
            try:
                delta = json.loads(raw)
                if isinstance(delta, dict):
                    delta = delta.get("ops", delta)
                if isinstance(delta, list):
                    return "".join(x.get("insert", "") for x in delta
                                   if isinstance(x, dict) and
                                   isinstance(x.get("insert"), str)).rstrip("\n")
            except (TypeError, ValueError):
                pass
            return (raw or "").rstrip("\n")

        def card(title):
            for sel in (d(descriptionContains=title), d(textContains=title)):
                if sel.exists:
                    return sel
            return None

        def selected(n):
            return any(d(text=t).exists or d(description=t).exists
                       for t in (f"{n} đã chọn", f"{n} selected"))

        def has_label(value):
            return (d(textContains=value).exists or
                    d(descriptionContains=value).exists)

        def dialog_open():
            return any(has_label(text) for text in (
                "Xóa vĩnh viễn?", "Delete permanently?",
                "Hành động này không thể hoàn tác",
                "This action cannot be undone",
            ))

        def evidence(number):
            path = (folder / f"FN12_TC-BB-023B_D02_{number:02d}.png").as_posix()
            self.driver.capture_evidence(path)
            print(f"[023B D02 evidence] {path}")

        print(f"[START] TC-BB-023B D02: Confirm multi delete QA {marker}")
        try:
            self.driver.ensure_home_screen()

            # B1: Tạo 2 note QA mới; xác định ID thực từ SQLite.
            for title, content in notes.items():
                before_ids = set(read_db())
                assert QANoteHelper.create_test_note(
                    self.driver, title, content, poll_timeout=8.0)
                created = [r for id_, r in read_db().items()
                           if id_ not in before_ids
                           and r["title"] == title and r["status"] == "normal"]
                assert len(created) == 1, f"Cannot uniquely identify QA note: {title}"
                row = created[0]
                assert as_text(row["content"]) == content, (
                    f"Initial QA content mismatch: {title}")
                note_ids[title] = row["id"]
                QANoteHelper.move_note_to_trash_from_home(self.driver, title)
                print(f"[023B D02] Prepared {title}: {row['id']}")

            assert len(set(note_ids.values())) == 2, "QA note IDs not distinct"
            QANoteHelper.navigate_to_trash(self.driver)
            for title in notes:
                QANoteHelper.verify_note_in_trash(self.driver, title)

            # B2: Tiền điều kiện và dữ liệu đối chứng của những note khác.
            baseline = read_db()
            qa_ids = set(note_ids.values())
            assert len(qa_ids) == 2
            for title, note_id in note_ids.items():
                row = baseline.get(note_id)
                assert row is not None and row["status"] == "trash"
                assert row["title"] == title
                assert as_text(row["content"]) == notes[title]
            other_notes = {id_: row for id_, row in baseline.items()
                           if id_ not in qa_ids}
            evidence(1)

            # B3: Chọn chính xác 2 thẻ QA, xác nhận số lượng = 2.
            titles = list(notes)
            first = card(titles[0])
            assert first is not None, "First QA card not visible"
            first.long_click(duration=1.2)
            for _ in range(12):
                if selected(1):
                    break
                time.sleep(0.25)
            assert selected(1), "Expected exactly 1 selected item"

            second = card(titles[1])
            assert second is not None, "Second QA card not visible"
            second.click()
            for _ in range(12):
                if selected(2):
                    break
                time.sleep(0.25)
            assert selected(2), "Expected exactly 2 selected items"
            evidence(2)

            # B4: Mở dialog, dừng nếu thiếu bằng chứng chọn đúng 2 mục.
            action = next((sel for sel in (
                d(description="Xóa vĩnh viễn"),
                d(description="Delete forever"),
            ) if sel.exists), None)
            assert action is not None, "Delete-forever AppBar button not found"
            assert selected(2), "Selection changed unexpectedly"
            action.click()
            for _ in range(12):
                if dialog_open():
                    break
                time.sleep(0.25)
            evidence(3)
            assert dialog_open(), "Permanent-delete dialog missing"
            assert (has_label("2 ghi chú đã chọn") or
                    has_label("2 selected notes")), (
                "Confirmation dialog does not specify exactly 2 notes")

            # B5: Chỉ khi đã xác minh note IDs, chọn đúng 2 và dialog
            # xác nhận 2 note, mới được nhấn nút 'Xóa' chính xác.
            delete_button = next((sel for sel in (
                d(text="Xóa"), d(description="Xóa"),
                d(text="Delete"), d(description="Delete"),
            ) if sel.exists), None)
            assert delete_button is not None, "Dialog Delete button not found"
            assert dialog_open(), "Dialog closed before confirmation"
            delete_button.click()
            confirmed = True
            print("[023B D02] Confirmed permanent deletion of selected 2 QA notes")

            # B6: SQLite phải không còn đúng 2 ID QA; các note khác nguyên vẹn.
            after = {}
            for _ in range(40):
                after = read_db()
                if all(note_id not in after for note_id in qa_ids):
                    break
                time.sleep(1.0)
            assert all(note_id not in after for note_id in qa_ids), (
                f"QA note IDs still in SQLite: {qa_ids.intersection(after)}")
            evidence(4)

            # So sánh cả dữ liệu, trạng thái của mọi note không thuộc test.
            # Nếu dữ liệu ngoài phạm vi thay đổi, đánh dấu FAIL để điều tra.
            for note_id, expected in other_notes.items():
                assert after.get(note_id) == expected, (
                    f"Unrelated note changed/removed: {note_id}")
            print(f"[023B D02] Unrelated notes preserved: {len(other_notes)}")

            for title in notes:
                QANoteHelper.verify_note_absent_in_trash(self.driver, title)
            evidence(5)

            QANoteHelper.navigate_from_trash_to_home(self.driver)
            for title in notes:
                QANoteHelper.verify_note_absent_on_home(self.driver, title)
            evidence(6)

            print("[PASS] TC-BB-023B D02: 2 QA notes permanently deleted; "
                  "unrelated notes unchanged")
        finally:
            # Nếu chưa nhấn xác nhận mà dialog vẫn mở, chỉ bấm Hủy.
            # Không dọn/xóa ghi chú nào khác.
            if not confirmed:
                try:
                    if dialog_open():
                        cancel = next((sel for sel in (
                            d(text="Hủy"), d(description="Hủy"),
                            d(text="Cancel"), d(description="Cancel"),
                        ) if sel.exists), None)
                        if cancel is not None:
                            cancel.click()
                except Exception as exc:
                    print(f"[023B D02] Safe cancel warning: {exc}")
            print(f"[023B D02 Audit] confirmed={confirmed}; QA IDs={note_ids}")



    def test_tc_bb_023c_d01_lifecycle_survives_restart(self):
        """TC-BB-023C D01: Trash / permanent delete persists after force-stop + relaunch.

        Chỉ tạo và thao tác với 2 ghi chú QA mang marker riêng:
        - QA_TRASH giữ trong Thùng rác sau khởi động lại.
        - QA_DELETED xóa vĩnh viễn trước khởi động lại và không được xuất hiện lại.
        """
        import json
        import sqlite3
        import subprocess
        import uuid
        from datetime import datetime
        from pathlib import Path
        from automation import config

        marker = uuid.uuid4().hex[:10]
        trash_title = f"QA_FN12_023C_TRASH_{marker}"
        deleted_title = f"QA_FN12_023C_DELETED_{marker}"
        notes = {
            trash_title: f"QA 023C preserved in trash {marker}",
            deleted_title: f"QA 023C permanently deleted {marker}",
        }
        note_ids = {}
        folder = (Path("evidence/fn12") /
                  f"automation_{datetime.now():%Y%m%d_%H%M%S_%f}_{marker}" /
                  "TC-BB-023C")
        d = self.d
        was_force_stopped = False

        def read_db():
            result = subprocess.run(
                ["adb", "-s", self.driver.serial, "exec-out", "run-as",
                 config.APP_PACKAGE, "cat", "databases/smart_note.db"],
                capture_output=True, timeout=25,
            )
            assert result.returncode == 0 and result.stdout, (
                "SQLite oracle unavailable: " +
                result.stderr.decode(errors="replace")
            )
            conn = sqlite3.connect(":memory:")
            try:
                conn.deserialize(result.stdout)
                rows = conn.execute(
                    "SELECT id, title, content, status FROM notes"
                ).fetchall()
                return {
                    row[0]: dict(zip(("id", "title", "content", "status"), row))
                    for row in rows
                }
            finally:
                conn.close()

        def as_text(raw):
            try:
                delta = json.loads(raw)
                if isinstance(delta, dict):
                    delta = delta.get("ops", delta)
                if isinstance(delta, list):
                    return "".join(
                        op.get("insert", "") for op in delta
                        if isinstance(op, dict) and
                        isinstance(op.get("insert"), str)
                    ).rstrip("\n")
            except (ValueError, TypeError):
                pass
            return (raw or "").rstrip("\n")

        def capture(number):
            name = (folder / f"FN12_TC-BB-023C_D01_{number:02d}.png").as_posix()
            self.driver.capture_evidence(name)
            print(f"[023C Evidence] {name}")

        def check_trash_row(rows):
            row = rows.get(note_ids[trash_title])
            assert row is not None, "QA_TRASH disappeared from SQLite"
            assert row["title"] == trash_title, "QA_TRASH title changed"
            assert row["status"] == "trash", "QA_TRASH status is not trash"
            assert as_text(row["content"]) == notes[trash_title], (
                "QA_TRASH content changed"
            )

        print(f"[START] TC-BB-023C D01: Persistence after restart {marker}")
        try:
            self.driver.ensure_home_screen()

            # B1. Tạo đúng hai note QA mới, đọc note_id thật từ SQLite.
            for title, content in notes.items():
                before_ids = set(read_db())
                assert QANoteHelper.create_test_note(
                    self.driver, title, content, poll_timeout=8.0
                )
                created = [
                    row for note_id, row in read_db().items()
                    if note_id not in before_ids and row["title"] == title
                    and row["status"] == "normal"
                ]
                assert len(created) == 1, (
                    f"Cannot uniquely identify new QA note: {title}"
                )
                assert as_text(created[0]["content"]) == content, (
                    f"Initial QA content mismatch: {title}"
                )
                note_ids[title] = created[0]["id"]
                QANoteHelper.move_note_to_trash_from_home(self.driver, title)
                print(f"[023C] Prepared QA note {title}: {note_ids[title]}")

            assert len(set(note_ids.values())) == 2, "QA IDs are not unique"
            QANoteHelper.navigate_to_trash(self.driver)

            for title in notes:
                QANoteHelper.verify_note_in_trash(self.driver, title)

            before_delete = read_db()
            check_trash_row(before_delete)

            deleted_id = note_ids[deleted_title]
            assert before_delete.get(deleted_id, {}).get("status") == "trash"
            assert before_delete[deleted_id]["title"] == deleted_title
            assert as_text(before_delete[deleted_id]["content"]) == notes[deleted_title]

            capture(1)

            # B2. Chỉ xóa vĩnh viễn note QA_DELETED đã xác minh ID.
            # Không dùng select nhiều, tọa độ mù hay xóa toàn bộ Trash.
            delete_card = next((item for item in (
                d(descriptionContains=deleted_title),
                d(textContains=deleted_title),
            ) if item.exists), None)

            assert delete_card is not None, "QA_DELETED card not found in Trash"

            delete_card.click()
            time.sleep(0.7)

            # Xác minh đúng BottomSheet của 1 ghi chú, rồi mới xóa.
            restore_option = next((item for item in (
                d(text="Khôi phục ghi chú"),
                d(description="Khôi phục ghi chú"),
                d(text="Restore note"),
                d(description="Restore note"),
            ) if item.exists), None)

            assert restore_option is not None, (
                "Expected single-note options sheet; refusing to delete"
            )

            delete_option = next((item for item in (
                d(text="Xóa vĩnh viễn"),
                d(description="Xóa vĩnh viễn"),
                d(text="Delete forever"),
                d(description="Delete forever"),
            ) if item.exists), None)

            assert delete_option is not None, (
                "Single-note permanent-delete option not found; refusing to delete"
            )

            capture(2)

            assert read_db().get(deleted_id, {}).get("status") == "trash", (
                "QA_DELETED changed unexpectedly before delete"
            )

            delete_option.click()

            # B3. Xác minh note B đã xóa, note A vẫn còn trước khi khởi động lại.
            after_delete = {}

            for _ in range(40):
                after_delete = read_db()
                if deleted_id not in after_delete:
                    break
                time.sleep(1.0)

            assert deleted_id not in after_delete, (
                "QA_DELETED still in SQLite before restart"
            )

            check_trash_row(after_delete)

            QANoteHelper.verify_note_absent_in_trash(self.driver, deleted_title)
            QANoteHelper.verify_note_in_trash(self.driver, trash_title)

            capture(3)

            # B4. Force-stop, KHÔNG xóa dữ liệu / reset / uninstall ứng dụng.
            stop = subprocess.run(
                ["adb", "-s", self.driver.serial, "shell", "am", "force-stop",
                 config.APP_PACKAGE],
                capture_output=True, timeout=20,
            )

            assert stop.returncode == 0, (
                "Force-stop failed: " + stop.stderr.decode(errors="replace")
            )

            was_force_stopped = True
            print("[023C] ADB force-stop OK; app data preserved")

            time.sleep(1.0)

            # Mở lại app và đợi HomeScreen.
            self.driver.launch_app()
            self.driver.ensure_home_screen()
            was_force_stopped = False

            time.sleep(2.0)

            # B5. Trên Home cả 2 QA note đều không được xuất hiện.
            QANoteHelper.verify_note_absent_on_home(self.driver, trash_title)
            QANoteHelper.verify_note_absent_on_home(self.driver, deleted_title)

            capture(4)

            # B6. Trash còn QA_TRASH; QA_DELETED không tái xuất hiện.
            QANoteHelper.navigate_to_trash(self.driver)

            QANoteHelper.verify_note_in_trash(self.driver, trash_title)
            QANoteHelper.verify_note_absent_in_trash(self.driver, deleted_title)

            capture(5)

            # Oracle cuối cùng theo đúng note_id, title và content.
            final_rows = read_db()

            check_trash_row(final_rows)

            assert deleted_id not in final_rows, (
                "QA_DELETED reappeared in SQLite after force-stop/relaunch"
            )

            print(
                "[PASS] TC-BB-023C D01: Trash and permanent-delete "
                "states persist after app restart"
            )

        finally:
            # Giữ lại QA_TRASH để kiểm tra/audit.
            # Tuyệt đối không tự động xóa ghi chú khác.
            print(f"[023C Audit] retained/deleted QA IDs: {note_ids}")

            if was_force_stopped:
                try:
                    self.driver.launch_app()
                    self.driver.ensure_home_screen()
                except Exception as exc:
                    print(f"[023C Recovery warning] {exc}")
