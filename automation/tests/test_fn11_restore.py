# -*- coding: utf-8 -*-
"""Automation UI Test Suite for FN-11: Restore Note from Trash.

Test Cases:
- TC-BB-022: Khôi phục 1 ghi chú từ Thùng rác về Trang chủ (D01)

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


class TestFN11Restore:
    """Test Suite for FN-11: Khôi phục ghi chú từ thùng rác."""

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

    def test_tc_bb_022_restore_note_from_trash(self):
        """TC-BB-022 (D01): Khôi phục ghi chú từ Thùng rác về Trang chủ.

        Expected Result:
        - Ghi chú biến mất khỏi màn hình Thùng rác.
        - Quay về Trang chủ thấy ghi chú đã xuất hiện lại đầy đủ và nguyên vẹn.
        """
        note_title = f"RestoreTest_{int(time.time())}"
        note_content = "Nội dung kiểm thử khôi phục từ thùng rác"

        print(f"\n========================================================")
        print(f"[START] TC-BB-022: Restore Note from Trash — '{note_title}'")
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

            # 2. Thao tác chính: Mở menu tùy chọn dưới đáy và bấm "Khôi phục ghi chú"
            print(f"\n--- BƯỚC 4: Chạm vào ghi chú trong Thùng rác và chọn 'Khôi phục ghi chú' ---")
            QANoteHelper.restore_note_from_trash(self.driver, note_title)

            # 3. Xác minh bước 1: Ghi chú biến mất khỏi Thùng rác
            print(f"\n--- BƯỚC 5: Xác minh ghi chú đã biến mất khỏi Thùng rác ---")
            QANoteHelper.verify_note_absent_in_trash(self.driver, note_title)

            # 4. Điều hướng: Quay lại Trang chủ
            print(f"\n--- BƯỚC 6: Điều hướng quay về Trang chủ qua Drawer ---")
            QANoteHelper.navigate_from_trash_to_home(self.driver)

            # 5. Xác minh bước 2: Ghi chú xuất hiện lại trên Trang chủ
            print(f"\n--- BƯỚC 7: Xác minh ghi chú tái xuất hiện trên HomeScreen ---")
            QANoteHelper.verify_note_on_home(self.driver, note_title, poll_timeout=6.0)

            # 6. Chụp ảnh bằng chứng thực thi thành công
            ev_path = self.driver.capture_evidence("evidence/fn11/FN11_TC-BB-022_D01_01.png")
            print(f"\n[PASS] TC-BB-022 hoàn tất thành công! Bằng chứng đã lưu: {ev_path}")

        finally:
            # Dọn dẹp an toàn ghi chú test sau khi khôi phục
            print(f"\n--- DỌN DẸP: Xóa ghi chú test cô lập '{note_title}' trên HomeScreen ---")
            try:
                self.driver.ensure_home_screen()
                self.driver.cleanup_note_via_selection(note_title)
            except Exception as e:
                print(f"[Cleanup Notice] Ignored cleanup warning: {e}")

    def test_tc_bb_022b_d01_multi_restore_from_trash(self):
        """TC-BB-022B D01: Khôi phục đúng 2 ghi chú QA bằng multi-select."""
        import json
        import sqlite3
        import subprocess
        import uuid
        from datetime import datetime
        from pathlib import Path
        from automation import config

        d = self.d
        marker = uuid.uuid4().hex[:10]
        samples = {
            f"QA_FN11_022B_A_{marker}": f"Noi dung QA FN11 A {marker}",
            f"QA_FN11_022B_B_{marker}": f"Noi dung QA FN11 B {marker}",
        }
        ids = {}
        folder = (Path("evidence/fn11") /
                  f"automation_{datetime.now():%Y%m%d_%H%M%S_%f}_{marker}" /
                  "TC-BB-022B")

        def db_rows():
            cmd = ["adb", "-s", self.driver.serial, "exec-out", "run-as",
                   config.APP_PACKAGE, "cat", "databases/smart_note.db"]
            out = subprocess.run(cmd, capture_output=True, timeout=25)
            assert out.returncode == 0 and out.stdout, (
                f"SQLite oracle unavailable: {out.stderr.decode(errors='replace')}")
            conn = sqlite3.connect(":memory:")
            try:
                conn.deserialize(out.stdout)
                rows = conn.execute("SELECT id, title, content, status FROM notes").fetchall()
                return {r[0]: dict(zip(("id", "title", "content", "status"), r))
                        for r in rows}
            finally:
                conn.close()

        def plain(raw):
            try:
                value = json.loads(raw)
                if isinstance(value, dict):
                    value = value.get("ops", value)
                if isinstance(value, list):
                    return "".join(op.get("insert", "") for op in value
                                   if isinstance(op, dict) and
                                   isinstance(op.get("insert"), str)).rstrip("\n")
            except (TypeError, ValueError):
                pass
            return (raw or "").rstrip("\n")

        def card(title):
            for item in (d(descriptionContains=title), d(textContains=title)):
                if item.exists:
                    return item
            return None

        def selected(n):
            return any(d(text=t).exists or d(description=t).exists
                       for t in (f"{n} đã chọn", f"{n} selected"))

        def screenshot(n):
            path = (folder / f"FN11_TC-BB-022B_D01_{n:02d}.png").as_posix()
            self.driver.capture_evidence(path)
            print(f"[022B Evidence] {path}")

        print(f"[START] TC-BB-022B D01 — QA marker {marker}")
        try:
            self.driver.ensure_home_screen()

            # BƯỚC 1: Tạo 2 ghi chú QA và chuyển vào Thùng rác
            for title, content in samples.items():
                before = set(db_rows())
                assert QANoteHelper.create_test_note(
                    self.driver, title, content, poll_timeout=8.0)
                rows = db_rows()
                created = [r for id_, r in rows.items()
                           if id_ not in before and r["title"] == title
                           and r["status"] == "normal"]
                assert len(created) == 1, f"Cannot uniquely identify QA note: {title}"
                row = created[0]
                assert plain(row["content"]) == content, f"Wrong initial content: {title}"
                ids[title] = row["id"]
                QANoteHelper.move_note_to_trash_from_home(self.driver, title)
                print(f"[022B] Prepared {title} / ID={row['id']}")

            assert len(set(ids.values())) == 2, "QA note IDs are not distinct"
            QANoteHelper.navigate_to_trash(self.driver)

            for title in samples:
                QANoteHelper.verify_note_in_trash(self.driver, title)
            for title, id_ in ids.items():
                assert db_rows()[id_]["status"] == "trash", (
                    f"Precondition: note is not in trash: {title}")
            screenshot(1)

            # BƯỚC 2: Chọn đúng 2 ghi chú trong TrashScreen
            titles = list(samples)
            first = card(titles[0])
            assert first is not None, "First QA card not visible in Trash"
            first.long_click(duration=1.2)

            for _ in range(10):
                if selected(1):
                    break
                time.sleep(0.2)
            assert selected(1), "Selection Mode did not select exactly one note"

            second = card(titles[1])
            assert second is not None, "Second QA card not visible in Trash"
            second.click()

            for _ in range(10):
                if selected(2):
                    break
                time.sleep(0.2)
            assert selected(2), "Selection Mode did not select exactly two notes"
            screenshot(2)

            # BƯỚC 3: Nhấn nút Khôi phục trên AppBar
            restore = None
            for item in (d(description="Khôi phục"), d(description="Restore")):
                if item.exists:
                    restore = item
                    break
            assert restore is not None, "Multi-select Restore AppBar button missing"
            restore.click()

            # BƯỚC 4: SQLite bắt buộc xác nhận cả 2 note đã khôi phục
            final = {}
            for _ in range(16):
                final = db_rows()
                if all(final.get(id_, {}).get("status") == "normal"
                       for id_ in ids.values()):
                    break
                time.sleep(0.5)

            for title, id_ in ids.items():
                row = final.get(id_)
                assert row is not None, f"QA note disappeared from SQLite: {id_}"
                assert row["status"] == "normal", f"Restore failed: {title}"
                assert row["title"] == title, f"Title changed: {id_}"
                assert plain(row["content"]) == samples[title], (
                    f"Content changed: {id_}")
                QANoteHelper.verify_note_absent_in_trash(self.driver, title)
            screenshot(3)

            # BƯỚC 5: Cả 2 ghi chú xuất hiện trên HomeScreen
            QANoteHelper.navigate_from_trash_to_home(self.driver)
            for title in samples:
                QANoteHelper.verify_note_on_home(
                    self.driver, title, poll_timeout=8.0)
            screenshot(4)

            print("[PASS] TC-BB-022B D01: 2/2 QA notes restored, SQLite intact")
        finally:
            # Giữ ghi chú QA để đối chiếu, không xóa vĩnh viễn
            print(f"[022B Audit] QA notes retained: {ids}")
            try:
                self.driver.ensure_home_screen()
            except Exception as exc:
                print(f"[022B Navigation warning] {exc}")


    def test_tc_bb_022c_d01_empty_trash_state(self):
        """TC-BB-022C D01: Kiểm tra giao diện Thùng rác trống."""
        import sqlite3
        import subprocess
        import uuid
        from datetime import datetime
        from automation import config

        run_id = f"{datetime.now():%Y%m%d_%H%M%S_%f}_{uuid.uuid4().hex[:8]}"
        folder = f"evidence/fn11/automation_{run_id}/TC-BB-022C"

        print("[START] TC-BB-022C D01: Empty Trash State")

        try:
            # Bước 1: Mở Thùng rác
            QANoteHelper.navigate_to_trash(self.driver)

            # Bước 2: Kiểm tra SQLite chỉ đọc
            result = subprocess.run(
                [
                    "adb", "-s", self.driver.serial,
                    "exec-out", "run-as", config.APP_PACKAGE,
                    "cat", "databases/smart_note.db"
                ],
                capture_output=True,
                timeout=25
            )

            assert result.returncode == 0 and result.stdout, (
                "Không đọc được SQLite"
            )

            conn = sqlite3.connect(":memory:")
            try:
                conn.deserialize(result.stdout)
                count = conn.execute(
                    "SELECT COUNT(*) FROM notes WHERE status = 'trash'"
                ).fetchone()[0]
            finally:
                conn.close()

            print(f"[022C] Số ghi chú trong Trash: {count}")

            # Không xóa dữ liệu để ép tiền điều kiện
            if count > 0:
                path = f"{folder}/precondition_not_empty.png"
                self.driver.capture_evidence(path)
                pytest.skip(
                    f"BLOCKED: Thùng rác còn {count} ghi chú. "
                    "Không tự động xóa dữ liệu."
                )

            # Bước 3: Xác minh Empty State
            found = False
            for _ in range(15):
                if (
                    self.d(text="Thùng rác trống").exists
                    or self.d(description="Thùng rác trống").exists
                    or self.d(text="Trash is empty").exists
                ):
                    found = True
                    break
                time.sleep(0.4)

            evidence = f"{folder}/FN11_TC-BB-022C_D01_01.png"
            self.driver.capture_evidence(evidence)

            assert found, (
                "Thùng rác có 0 ghi chú nhưng không hiển thị Empty State"
            )

            print("[PASS] TC-BB-022C D01: Empty State displayed")

        finally:
            try:
                QANoteHelper.navigate_from_trash_to_home(self.driver)
            except Exception as exc:
                print(f"[022C Navigation] {exc}")