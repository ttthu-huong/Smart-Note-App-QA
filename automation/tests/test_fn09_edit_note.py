"""FN-09 / phase 1: UI/E2E tests on the real Samsung S21 FE.

TC-BB-019, TC-BB-019B, TC-BB-019C, TC-BB-020.
All editing is performed via UIAutomator2. SQLite is an additional READ-ONLY
oracle to establish record identity and persisted content (not pure black-box).

Run from repository root.  No application source files are changed.
A unique folder is used for each execution.  Set FN09_DEBUG=1 to retain QA
notes for investigation.  A failed/uncertain cleanup leaves the note intact.
"""

from _pytest import legacypath
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import time
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime

import pytest

from automation import config
from automation.core.device import SmartNoteDriver


RUN_LABEL = os.environ.get("FN09_RUN_ID") or datetime.now().strftime("%Y%m%d_%H%M%S_%f")
RUN_ID = f"{RUN_LABEL}_{uuid.uuid4().hex[:8]}"  # unique even when caller reuses a label
RUN_EVIDENCE = Path("evidence") / "fn09" / f"automation_{RUN_ID}"


def _notes(serial: str, package: str) -> list[dict]:
    """Read an app-private SQLite snapshot into memory without writing to device."""
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


def _ui_nodes(device) -> list[str]:
    root = ET.fromstring(device.dump_hierarchy())
    return [value for el in root.iter()
            if (value := (el.attrib.get("content-desc", "")
                          or el.attrib.get("text", "")))]


@dataclass
class OwnedNote:
    note_id: str
    title: str
    marker: str


class TestFN09EditNote:
    @classmethod
    def _current_qa_editor_title(cls) -> str | None:
        """Read the *actual* top title input; never guess from a Home NoteCard.

        Only a uniquely identified QA_FN09_ title allows automatic Editor exit.
        An ordinary/personal note must be left untouched.
        """
        if not cls.driver.is_in_editor():
            return None
        candidates = []
        try:
            for field in cls.d(className="android.widget.EditText"):
                info = field.info
                bounds = info.get("bounds", {})
                title = (info.get("text") or "").strip()
                if (bounds.get("top", 9999) < 500
                        and title.startswith("QA_FN09_")
                        and title not in candidates):
                    candidates.append(title)
        except Exception as exc:
            print(f"[FN09 precondition] Cannot inspect Editor title: {exc}")
            return None
        return candidates[0] if len(candidates) == 1 else None

    @classmethod
    def _return_from_verified_qa_editor(cls) -> bool:
        """Exit only an active FN09 QA Editor whose title is unique in SQLite.

        Keep the note; do not delete, reset, log out or navigate from user notes.
        """
        title = cls._current_qa_editor_title()
        if title is None:
            return False
        try:
            candidates = [r for r in _notes(cls.driver.serial, config.APP_PACKAGE)
                          if r["title"] == title and r["status"] == "normal"]
        except Exception as exc:
            print(f"[FN09 precondition] QA title DB verification unavailable: {exc}")
            return False
        if len(candidates) != 1:
            print(f"[FN09 precondition] QA title {title!r} has {len(candidates)} active DB matches; no navigation")
            return False
        print(f"[FN09 precondition] Returning from owned QA Editor: {title!r}")
        cls.driver.save_and_exit_editor()
        return True

    @classmethod
    def setup_class(cls):
        serial = os.environ.get("DEVICE_SERIAL") or config.DEVICE_SERIAL
        cls.driver = SmartNoteDriver(serial=serial)
        cls.d = cls.driver.device
        cls.driver.launch_app()
        for _ in range(12):
            if cls.driver.is_on_home_screen():
                return
            time.sleep(0.5)

        # FN09_DEBUG=1 preserves the note, but an earlier run can leave its
        # Editor open. Recover only if the Editor title/DB identify an FN09 QA
        # note. Never press Back blindly or change the account/session.
        if cls._return_from_verified_qa_editor():
            for _ in range(16):
                if cls.driver.is_on_home_screen():
                    return
                time.sleep(0.5)

        # Save a real screenshot for troubleshooting without changing app state.
        diagnostic_path = (RUN_EVIDENCE / "PRECONDITION" / "blocked_screen.png").as_posix()
        try:
            cls.driver.capture_evidence(diagnostic_path)
            print(f"[FN09 precondition] Screenshot: {diagnostic_path}")
        except Exception as exc:
            print(f"[FN09 precondition] Screenshot unavailable: {exc}")
        try:
            flags = (f"home={cls.driver.is_on_home_screen()}, "
                     f"editor={cls.driver.is_in_editor()}, "
                     f"login={cls.driver.is_in_login()}, "
                     f"register={cls.driver.is_in_register()}")
        except Exception as exc:
            flags = f"state-detection-error={exc}"
        print(f"[FN09 precondition] {flags}")
        pytest.skip(f"BLOCKED: HomeScreen not confirmed ({flags}). "
                    f"See {diagnostic_path}; personal notes/session were not changed")

    def _home(self):
        # Đợi UI ổn định, không tự nhấn Back
        for _ in range(40):
            if self.driver.is_on_home_screen():
                return
            time.sleep(0.5)
        home = self.driver.is_on_home_screen()
        editor = self.driver.is_in_editor()
        login = self.driver.is_in_login()
        current_app = self.d.app_current()
        path = (
            "evidence/fn09/diagnostics/"
            f"home_timeout_{uuid.uuid4().hex[:12]}.png"
        )
        self.driver.capture_evidence(path)
        print(
            f"[FN09 HOME ERROR] home={home}, "
            f"editor={editor}, login={login}, "
            f"app={current_app}"
        )
        print(f"[FN09 HOME ERROR] Screenshot: {path}")
        pytest.fail(
            "HomeScreen not confirmed after waiting. "
            "Inspect diagnostic screenshot before retrying."
        )

    def _evidence(self, tc: str, seq: int, data_id: str = "D01"):
        rel = (
            RUN_EVIDENCE / tc /
            f"FN09_{tc}_{data_id}_{seq:02d}.png"
        ).as_posix()

        saved = self.driver.capture_evidence(rel)
        print(f"[FN09 evidence] {tc} {data_id}: {saved}")
        return saved

    def _db(self):
        return _notes(self.driver.serial, config.APP_PACKAGE)

    def _row(self, note: OwnedNote) -> dict:
        found = [r for r in self._db() if r["id"] == note.note_id]
        assert len(found) == 1, f"DB: expected ID {note.note_id} exactly once, got {len(found)}"
        return found[0]

    def _active_home_card(self, title: str) -> str:
        """Return the semantics of the *same* NoteCard, not generic Home text."""
        self._home()
        for _ in range(12):
            matches = [value for value in _ui_nodes(self.d)
                       if value == title or value.startswith(title + "\n")]
            # Flutter NoteCard typically has one combined content-description:
            # '<title>\n<preview>'. Prefer the longest node containing the title.
            if matches:
                return max(matches, key=len)
            time.sleep(0.5)
        pytest.fail(f"Home NoteCard not found for {title!r}")

    def _unique_home_locator(self, title: str):
        """Pick exactly one matching NoteCard; never blindly click a broad selector."""
        for selector in (self.d(descriptionContains=title), self.d(textContains=title)):
            if selector.count == 1:
                return selector
        pytest.skip(f"BLOCKED: cannot uniquely locate Home NoteCard for {title!r}")

    def _open(self, title: str, note: OwnedNote):
        assert self._row(note)["title"] == title, "Note title/ID mismatch before UI open"
        self._active_home_card(title)
        # Avoid the shared driver's cancel-selection fallback: it can try to
        # click a non-existing UiObject because selectors are not existence tests.
        self._unique_home_locator(title).click()
        for _ in range(12):
            if self.driver.is_in_editor():
                break
            time.sleep(0.5)
        assert self.driver.is_in_editor(), "Not in Editor after opening target NoteCard"
        assert title in "\n".join(_ui_nodes(self.d)), "Editor title does not match target note"

    def _create(self, tc: str, base_content: str, data_id: str = "D01") -> OwnedNote:
        """Create and identify a fresh QA note using before/after DB ID difference."""
        self._home()
        marker = uuid.uuid4().hex[:12]  # 48-bit random suffix for short UI-safe titles
        title = f"QA_FN09_{tc}_{marker}"
        before = self._db()
        before_ids = {r["id"] for r in before}
        if any(r["title"] == title and r["status"] == "normal" for r in before):
            pytest.skip("BLOCKED: unexpected collision with this run's unique QA title")

        # If this creation fails before ID is known, do NOT delete by title alone.
        self.driver.open_note_editor()
        self.driver.input_title(title)
        self.driver.input_content(base_content)
        self.driver.save_and_exit_editor()
        self._home()

        rows = [r for r in self._db() if r["id"] not in before_ids
                and r["title"] == title and r["status"] == "normal"]
        assert len(rows) == 1, (
            f"Creation oracle: expected exactly one NEW note with {title}, "
            f"found {len(rows)}; manual QA data review may be required"
        )
        note = OwnedNote(rows[0]["id"], title, marker)
        actual = _plain(rows[0]["content"])
        assert actual.rstrip("\n") == base_content, (
            f"Invalid QA precondition: base content differs or is duplicated: {actual!r}"
        )
        self._evidence(f"TC-BB-{tc}", 1, data_id=data_id)
        print(f"[FN09 owned note] TC-BB-{tc} ID={note.note_id} title={title}")
        return note

    def _edit_title(self, new_title: str):
        """Only edit the verified top TextField. No blind coordinate fallback."""
        candidates = []
        for item in self.d(className="android.widget.EditText"):
            try:
                info = item.info
                b = info.get("bounds", {})
                if 0 < b.get("bottom", 0) and b.get("top", 9999) < 500:
                    candidates.append(item)
            except Exception:
                continue
        if len(candidates) != 1:
            pytest.skip(f"BLOCKED: cannot uniquely identify title TextField ({len(candidates)} candidates)")
        field = candidates[0]
        field.click()
        field.set_text(new_title)
        time.sleep(0.5)
        if new_title not in "\n".join(_ui_nodes(self.d)):
            pytest.fail("New title not visible in Editor immediately after editing")

    def _quill_focus(self):
        """Tap the known S21 FE body area, reject an observable Title focus."""
        self.d.click(540, 520)
        time.sleep(0.4)
        focused = self.d(className="android.widget.EditText", focused=True)
        if focused.exists:
            top = focused.info.get("bounds", {}).get("top", 9999)
            if top < 400:
                self.d.click(540, 650)
                time.sleep(0.4)
                focused = self.d(className="android.widget.EditText", focused=True)
                if focused.exists and focused.info.get("bounds", {}).get("top", 9999) < 400:
                    pytest.skip("BLOCKED: Quill tap still focuses Title, refusing to edit")

    def _paste(self, value: str):
        self.d.set_clipboard(value)
        time.sleep(0.25)
        try:
            self.d.jsonrpc.pasteClipboard()
        except Exception as exc:
            pytest.skip(f"BLOCKED: Quill clipboard paste not available: {exc}")
        time.sleep(0.8)

    def _append(self, original_title: str, value: str):
        self._quill_focus()
        try:
            self.d.jsonrpc.pressKeyCode(123)  # KEYCODE_MOVE_END
        except Exception as exc:
            pytest.skip(f"BLOCKED: cannot move Quill cursor to end: {exc}")
        # Xác nhận vẫn ở Editor trước khi dán
        assert self.driver.is_in_editor(), (
            "Editor closed unexpectedly before Quill append"
        )
        # Dán nội dung mới vào Quill
        self._paste(value)
        # Không kiểm tra Title bằng Accessibility XML khi bàn phím mở.
        # SQLite sẽ xác minh đúng Title và Content sau khi lưu.

    def _replace_quill(self, title: str, old_text: str, new_text: str):
        self._quill_focus()
        try:
            self.d.jsonrpc.pressKeyCode(123)  # Đưa con trỏ về cuối Quill
            for _ in range(len(old_text) + 2):
                self.d.jsonrpc.pressKeyCode(67)  # Backspace
                time.sleep(0.04)
        except Exception as exc:
            pytest.skip(f"BLOCKED: cannot select/clear Quill text: {exc}")
        time.sleep(0.5)
        ui = "\n".join(_ui_nodes(self.d))
        if title not in ui:
            pytest.fail("Title disappeared during Quill clear: wrong focus/input target")
        if old_text in ui:
            pytest.skip("BLOCKED: old Quill text still visible after Backspace")
        # Retain the verified Quill focus when pasting; driver.input_content()
        # may re-focus based on a generic 'Ghi chú' element.
        if new_text:
            self._paste(new_text)
        assert title in "\n".join(_ui_nodes(self.d)), "Title changed during Quill replacement"

    def _assert_db_edit(self, note: OwnedNote, title: str, original: str,
                        added: str, *, replacement: bool = False):
        row = self._row(note)
        assert row["status"] == "normal", "Edited note is no longer active"
        assert row["title"] == title, f"DB title changed unexpectedly: {row['title']!r}"
        actual = _plain(row["content"]).rstrip("\n")
        if replacement:
            assert actual == added, f"Content replacement mismatch: {actual!r}"
            assert original not in actual, "Old content remains after replacement"
        elif added:
            assert actual.startswith(original), f"Original content lost: {actual!r}"
            assert actual.endswith(added.strip()), f"Appended content not at end: {actual!r}"
            assert actual.count(added.strip()) == 1, "Appended content duplicated"
        else:
            assert actual == original, f"Title-only edit modified note content: {actual!r}"

    def _assert_reopen(self, note: OwnedNote, title: str, *expected_parts: str):
        self._open(title, note)
        ui = "\n".join(_ui_nodes(self.d))
        assert title in ui, "Editor lost new title on reopen"
        for part in expected_parts:
            assert part in ui, f"Editor missing persisted content: {part!r}"

    def _cleanup_owned(self, note: OwnedNote | None, current_title: str):
        if note is None:
            print("[FN09 cleanup] No verified new ID; leaving uncertain data untouched")
            return
        if os.environ.get("FN09_DEBUG") == "1":
            # Debug mode preserves QA data, not the transient Editor screen.
            # A successful test can finish after reopening the Editor. Exit
            # *only* the same verified test-owned note so the next pytest run
            # starts from HomeScreen without changing user notes.
            if self.driver.is_in_editor():
                try:
                    current = self._row(note)
                    editor_title = self._current_qa_editor_title()
                    if (current["status"] == "normal"
                            and current["title"] == current_title
                            and editor_title == current_title):
                        self.driver.save_and_exit_editor()
                        print("[FN09 DEBUG] Closed QA Editor safely; note preserved")
                    else:
                        print("[FN09 DEBUG] STOP: Editor/DB identity mismatch; preserving current screen")
                except Exception as exc:
                    print(f"[FN09 DEBUG] STOP: Cannot verify safe Editor exit: {exc}")
            print(f"[FN09 DEBUG] Preserve QA note ID={note.note_id} title={current_title!r}")
            return
        if not current_title.startswith("QA_FN09_") or note.marker not in current_title:
            print("[FN09 cleanup] STOP: target title lost own marker; leaving intact")
            return
        try:
            current = self._row(note)
            if current["status"] != "normal" or current["title"] != current_title:
                print("[FN09 cleanup] STOP: target ID/title/status mismatch; leaving intact")
                return
            if self.driver.is_in_editor():
                self.driver.save_and_exit_editor()
            if not self.driver.is_on_home_screen():
                print("[FN09 cleanup] STOP: not HomeScreen; leaving intact")
                return
            # Require a unique accessibility NoteCard before using shared UI helper.
            locator = self.d(descriptionContains=current_title)
            if locator.count != 1:
                print(f"[FN09 cleanup] STOP: {locator.count} matching description cards; leaving intact")
                return
            self.driver.cleanup_note_via_selection(current_title)
            time.sleep(0.8)
            status = self._row(note)["status"]
            print(f"[FN09 cleanup] ID={note.note_id} status={status}")
            if status != "trash":
                print("[FN09 cleanup] WARNING: not confirmed in Trash; inspect manually")
        except Exception as exc:
            print(f"[FN09 cleanup] STOP, no further deletion: {exc}")

    def test_tc_bb_019_edit_note_content(self):
        """TC-BB-019: append content, verify Home preview and reopened Editor."""
        tc = "019"
        original = "Nội dung ban đầu của Họp Lab."
        appended = "\n[Cập nhật: Đã hoàn tất phase 1]"
        note = None
        title = ""
        try:
            note = self._create(tc, original)
            title = note.title
            self._open(title, note)
            self._append(title, appended)
            self.driver.save_and_exit_editor()
            card = self._active_home_card(title)
            self._evidence("TC-BB-019", 2)
            assert appended.strip() in card, "Updated content missing from this Home NoteCard preview"
            self._assert_db_edit(note, title, original, appended)
            self._assert_reopen(note, title, original, appended.strip())
            self._evidence("TC-BB-019", 3)
        finally:
            self._cleanup_owned(note, title)

    def test_tc_bb_019b_edit_title_only(self):
        """TC-BB-019B: change title, preserve exactly the original content."""
        tc = "019B"
        original = "Nội dung ghi chú cần giữ nguyên vẹn không đổi."
        note = None
        title = ""
        try:
            note = self._create(tc, original)
            old_title = note.title
            title = old_title
            title = f"QA_FN09_019B_Kế hoạch tuần - Đã duyệt_{note.marker}"
            self._open(old_title, note)
            self._edit_title(title)
            self.driver.save_and_exit_editor()
            card = self._active_home_card(title)
            assert original in card, "Original preview missing after title-only edit"
            assert old_title not in card, "Old title still present in edited NoteCard"
            self._evidence("TC-BB-019B", 2)
            self._assert_db_edit(note, title, original, "")
            self._assert_reopen(note, title, original)
            self._evidence("TC-BB-019B", 3)
        finally:
            self._cleanup_owned(note, title)

    def test_tc_bb_019c_edit_title_and_content(self):
        """TC-BB-019C: replace both fields; verify no old body remains."""
        tc = "019C"
        original = "Nội dung cũ của tháng 10."
        updated = "Triển khai kiểm thử hồi quy toàn bộ hệ thống"
        note = None
        title = ""
        try:
            note = self._create(tc, original)
            old_title = note.title
            title = old_title
            title = f"QA_FN09_019C_Kế hoạch tháng 11_{note.marker}"
            self._open(old_title, note)
            self._edit_title(title)
            self._replace_quill(title, original, updated)
            self.driver.save_and_exit_editor()
            card = self._active_home_card(title)
            assert updated in card, "New content missing from this Home NoteCard preview"
            assert old_title not in card, "Old title still appears in edited NoteCard"
            self._evidence("TC-BB-019C", 2)
            self._assert_db_edit(note, title, original, updated, replacement=True)
            self._assert_reopen(note, title, updated)
            self._evidence("TC-BB-019C", 3)
        finally:
            self._cleanup_owned(note, title)

    def test_tc_bb_019d_clear_title_keep_content(self):
        """TC-BB-019D: Xóa tiêu đề, giữ nguyên nội dung."""
        tc = "019D"
        original = f"Nội dung FN09-019D-{uuid.uuid4().hex[:8]}"
        note = None
        try:
            note = self._create(tc, original)
            old_title = note.title

            self._open(old_title, note)
            self._edit_title("")
            self._evidence("TC-BB-019D", 2)
            self.driver.save_and_exit_editor()
            self._home()
            row = self._row(note)
            assert row["status"] == "normal", (
                "Ghi chú bị mất sau khi xóa tiêu đề"
            )
            assert row["title"] == "", (
                f"Tiêu đề chưa được xóa: {row['title']!r}"
            )
            assert _plain(row["content"]).rstrip("\n") == original, (
                "Nội dung đã bị thay đổi"
            )
            matches = [
                value for value in _ui_nodes(self.d)
                if original in value
            ]
            assert matches, (
                "Không thấy nội dung ghi chú trên HomeScreen"
            )
            assert all(old_title not in value for value in matches), (
                "Tiêu đề cũ vẫn hiển thị trên NoteCard"
            )
            self._evidence("TC-BB-019D", 3)
            card = self.d(descriptionContains=original)

            if card.count != 1:
                pytest.skip(
                    "BLOCKED: Không xác định duy nhất được "
                    "NoteCard không có tiêu đề"
                )
            card.click()
            for _ in range(12):
                if self.driver.is_in_editor():
                    break
                time.sleep(0.5)
            assert self.driver.is_in_editor(), (
                "Không mở lại được ghi chú"
            )
            assert original in "\n".join(_ui_nodes(self.d)), (
                "Nội dung bị mất khi mở lại"
            )
            assert self._row(note)["title"] == "", (
                "Tiêu đề thay đổi sau khi mở lại"
            )
            self._evidence("TC-BB-019D", 4)
            self.driver.save_and_exit_editor()
            self._home()
        finally:
            if note is not None:
                print(
                    f"[FN09-019D] QA note preserved: "
                    f"ID={note.note_id}"
                )


    def test_tc_bb_020_auto_save_after_delay(self):
        """TC-BB-020: Kiểm tra Autosave độc lập khi force-stop tại Editor."""
        tc = "020"
        original = "Nội dung ban đầu của ghi chú Autosave."
        appended = "\n[Autosave: Đang xử lý tự động]"
        note = None
        title = ""

        try:
            # 1. Tạo ghi chú QA riêng
            note = self._create(tc, original)
            title = note.title

            # 2. Mở ghi chú và bổ sung nội dung
            self._open(title, note)
            self._append(title, appended)
            self._evidence("TC-BB-020", 2)

            # 3. Chờ Autosave tự động thực hiện
            time.sleep(2.8)

            assert self.driver.is_in_editor(), (
                "Editor closed unexpectedly before force-stop"
            )

            # 4. Force-stop trực tiếp, KHÔNG nhấn Back
            self.d.app_stop(config.APP_PACKAGE)
            time.sleep(0.7)

            # 5. Kiểm tra SQLite trước khi khởi động lại
            self._assert_db_edit(note, title, original, appended)
            print(
                "[FN09 TC-BB-020] Saved content proven "
                "immediately after force-stop"
            )

            # 6. Khởi động lại ứng dụng
            self.driver.launch_app()
            self._home()

            # 7. Kiểm tra nội dung trên HomeScreen
            card = self._active_home_card(title)

            assert appended.strip() in card, (
                "Autosave missing from NoteCard after restart"
            )

            # 8. Đối chiếu dữ liệu SQLite
            self._assert_db_edit(note, title, original, appended)
            self._evidence("TC-BB-020", 3)

            # 9. Mở lại ghi chú và kiểm tra nội dung
            self._assert_reopen(
                note, title, original, appended.strip()
            )
            self._evidence("TC-BB-020", 4)

        finally:
            self._cleanup_owned(note, title)


    def test_tc_bb_019e_clear_content_keep_title(self):
        """TC-BB-019E: Xóa nội dung, giữ nguyên tiêu đề."""
        tc = "019E"
        original = f"Noi dung cu FN09-019E-{uuid.uuid4().hex[:8]}"
        note = None
        title = ""

        try:
            # 1. Tạo ghi chú QA
            note = self._create(tc, original)
            title = note.title

            # 2. Mở ghi chú và xóa nội dung
            self._open(title, note)
            self._replace_quill(title, original, "")

            # Evidence: kiểm tra lỗi RenderFlex Overflow
            self._evidence("TC-BB-019E", 2)

            # 3. Thoát về HomeScreen
            self.driver.save_and_exit_editor()
            self._home()

            # 4. Kiểm tra đúng bản ghi trong SQLite
            row = self._row(note)

            assert row["status"] == "normal", (
                "Ghi chú đã bị mất"
            )

            assert row["title"] == title, (
                "Tiêu đề bị thay đổi"
            )

            assert _plain(row["content"]).strip() == "", (
                "Nội dung chưa được xóa hoàn toàn"
            )

            # 5. Kiểm tra NoteCard
            card = self._active_home_card(title)

            assert original not in card, (
                "HomeScreen vẫn hiển thị nội dung cũ"
            )

            self._evidence("TC-BB-019E", 3)

            # 6. Mở lại ghi chú
            self._assert_reopen(note, title)

            ui = "\n".join(_ui_nodes(self.d))

            assert original not in ui, (
                "Nội dung cũ vẫn tồn tại trong Editor"
            )

            assert _plain(
                self._row(note)["content"]
            ).strip() == "", (
                "SQLite vẫn còn nội dung sau khi mở lại"
            )

            self._evidence("TC-BB-019E", 4)

        finally:
            self._cleanup_owned(note, title)



    def test_tc_bb_019f_clear_both_removes_note(self):
        """TC-BB-019F: Xóa cả Title và Content, ghi chú rỗng biến mất."""
        tc = "019F"
        original = f"FN09-019F-content-{uuid.uuid4().hex[:8]}"
        note = None
        try:
            # 1. Tạo ghi chú QA độc lập
            note = self._create(tc, original)
            title = note.title
            # 2. Mở đúng ghi chú QA
            self._open(title, note)
            # 3. Xóa nội dung trước, giữ lại tiêu đề
            self._replace_quill(title, original, "")
            # 4. Xóa toàn bộ tiêu đề
            self._edit_title("")
            # Chụp giao diện để đối chiếu BUG-BB-FN09-01
            self._evidence("TC-BB-019F", 2)
            # 5. Thoát Editor, nếu ứng dụng chưa tự thoát
            if self.driver.is_in_editor():
                self.driver.save_and_exit_editor()
            self._home()
            # 6. Kiểm tra ghi chú biến mất khỏi HomeScreen
            for _ in range(12):
                ui = "\n".join(_ui_nodes(self.d))
                if title not in ui and original not in ui:
                    break
                time.sleep(0.5)
            assert title not in ui, (
                "Ghi chú rỗng vẫn xuất hiện với tiêu đề cũ"
            )
            assert original not in ui, (
                "Ghi chú rỗng vẫn xuất hiện với nội dung cũ"
            )
            self._evidence("TC-BB-019F", 3)
            # 7. SQLite Oracle: đối chiếu đúng ID bản ghi
            rows = [
                r for r in self._db()
                if r["id"] == note.note_id
            ]
            if rows:
                print(
                    "[FN09-019F] DB record status:",
                    rows[0]["status"]
                )
                assert rows[0]["status"] != "normal", (
                    "Ghi chú rỗng vẫn active trong SQLite"
                )
            else:
                print(
                    "[FN09-019F] DB record removed:",
                    note.note_id
                )
            print("[FN09-019F] Empty note removed successfully")
        finally:
            # Không xóa theo Title vì sau test Title đã rỗng.
            # Giữ nguyên hiện trường nếu có lỗi.
            if note is not None:
                print(
                    "[FN09-019F] Checked QA note ID:",
                    note.note_id
                )




    def test_tc_bb_019g_d01_system_back(self):
        """TC-BB-019G D01: Lưu nội dung khi thoát bằng System Back."""
        tc = "019G"
        original = "Nội dung ban đầu kiểm tra System Back."
        appended = "\n[Thoát bằng System Back]"
        note = None
        title = ""

        try:
            # 1. Tạo và mở ghi chú QA riêng
            note = self._create(tc, original)
            title = note.title

            self._open(title, note)
            self._append(title, appended)
            self._evidence("TC-BB-019G", 2)

            assert self.driver.is_in_editor(), (
                "Không còn ở Editor trước System Back"
            )

            # 2. Sử dụng Android System Back, không dùng AppBar Back
            # Back lần đầu có thể chỉ ẩn bàn phím.
            for attempt in range(2):
                self.d.press("back")
                time.sleep(1.0)

                if self.driver.is_on_home_screen():
                    break

                if not self.driver.is_in_editor():
                    pytest.skip(
                        "BLOCKED: System Back chuyển sang màn hình "
                        "không xác định"
                    )

            # 3. Xác minh về HomeScreen
            self._home()

            # 4. Kiểm tra nội dung cập nhật trên NoteCard
            card = self._active_home_card(title)

            assert appended.strip() in card, (
                "Nội dung cập nhật không hiển thị trên HomeScreen"
            )

            self._evidence("TC-BB-019G", 3)

            # 5. SQLite oracle: đúng bản ghi và nội dung
            self._assert_db_edit(note, title, original, appended)

            # 6. Mở lại ghi chú để kiểm tra dữ liệu
            self._assert_reopen(
                note, title, original, appended.strip()
            )

            self._evidence("TC-BB-019G", 4)

        finally:
            self._cleanup_owned(note, title)



    def test_tc_bb_019g_d02_gesture_back(self):
        """TC-BB-019G D02: Lưu thay đổi khi thoát bằng Gesture Back."""
        tc = "019G"
        original = "Nội dung ban đầu kiểm tra Gesture Back."
        appended = "\n[Thoát bằng Gesture Back]"
        note = None
        title = ""

        try:
            # 1. Tạo ghi chú QA mới
            note = self._create(tc, original, data_id="D02")
            title = note.title

            # 2. Mở và chỉnh sửa
            self._open(title, note)
            self._append(title, appended)
            self._evidence("TC-BB-019G", 2, data_id="D02")

            assert self.driver.is_in_editor(), (
                "Editor đóng trước thao tác Gesture Back"
            )

            # 3. Vuốt từ mép trái màn hình vào trong
            # Lần đầu có thể chỉ ẩn bàn phím.
            for attempt in range(2):
                self.d.swipe(5, 1100, 430, 1100, 0.25)
                time.sleep(1.2)

                if self.driver.is_on_home_screen():
                    break

                if not self.driver.is_in_editor():
                    pytest.skip(
                        "BLOCKED: Gesture chuyển sang màn hình "
                        "không xác định"
                    )

            if not self.driver.is_on_home_screen():
                pytest.skip(
                    "BLOCKED: Gesture Back không đưa ứng dụng "
                    "về HomeScreen sau tối đa 2 lần vuốt"
                )

            # 4. Kiểm tra nội dung trên Home
            card = self._active_home_card(title)

            assert appended.strip() in card, (
                "Nội dung mới không hiển thị trên NoteCard"
            )

            self._evidence("TC-BB-019G", 3, data_id="D02")

            # 5. Kiểm tra đúng ID và nội dung SQLite
            self._assert_db_edit(note, title, original, appended)

            # 6. Mở lại và xác minh
            self._assert_reopen(
                note, title, original, appended.strip()
            )

            self._evidence("TC-BB-019G", 4, data_id="D02")

        finally:
            self._cleanup_owned(note, title)



    def test_tc_bb_020b_sequential_edits(self):
        """TC-BB-020B: Hai lần chỉnh sửa liên tiếp không mất dữ liệu."""
        tc = "020B"
        original = "Ghi chú kiểm thử tuần tự"
        part1 = "- Giai đoạn 1"
        part2 = "\n- Giai đoạn 2"
        note = None
        title = ""

        try:
            # Tạo ghi chú QA riêng
            note = self._create(tc, original)
            title = note.title

            # Lần chỉnh sửa thứ nhất
            self._open(title, note)
            self._append(title, part1)
            self._evidence("TC-BB-020B", 2)

            self.driver.save_and_exit_editor()
            self._home()

            expected1 = original + part1
            card1 = self._active_home_card(title)
            assert part1 in card1, "Home thiếu Giai đoạn 1"

            row1 = self._row(note)
            assert row1["status"] == "normal"
            assert row1["title"] == title
            assert _plain(row1["content"]).rstrip("\n") == expected1, (
                "Dữ liệu sau lần chỉnh sửa thứ nhất không chính xác"
            )
            self._evidence("TC-BB-020B", 3)

            # Lần chỉnh sửa thứ hai trên cùng note_id
            self._open(title, note)
            self._append(title, part2)
            self.driver.save_and_exit_editor()
            self._home()

            expected2 = expected1 + part2
            card2 = self._active_home_card(title)
            assert part1 in card2, "Home mất Giai đoạn 1"
            assert part2.strip() in card2, "Home thiếu Giai đoạn 2"

            row2 = self._row(note)
            assert row2["status"] == "normal"
            assert row2["title"] == title
            assert _plain(row2["content"]).rstrip("\n") == expected2, (
                "Hai lần chỉnh sửa không được lưu nguyên vẹn"
            )
            self._evidence("TC-BB-020B", 4)

            # Mở lại: xác minh sau hai lần lưu
            self._assert_reopen(
                note, title, original, part1, part2.strip()
            )
            self._evidence("TC-BB-020B", 5)

        finally:
            self._cleanup_owned(note, title)



    def test_tc_bb_020c_unicode_emoji_special(self):
        """TC-BB-020C: Giữ nguyên Unicode, emoji và ký tự đặc biệt."""
        tc = "020C"
        original = "Ghi chú gốc kiểm tra Unicode."
        appended = "\n[Cập nhật 🚀: Đạt 100% mục tiêu! @QA #2026]"
        note = None
        title = ""

        try:
            # 1. Tạo ghi chú QA riêng
            note = self._create(tc, original)
            title = note.title

            # 2. Mở và bổ sung nội dung Unicode
            self._open(title, note)
            self._append(title, appended)
            self._evidence("TC-BB-020C", 2)

            # 3. Lưu và về HomeScreen
            self.driver.save_and_exit_editor()
            self._home()

            # 4. Kiểm tra NoteCard trên Home
            card = self._active_home_card(title)
            assert "Cập nhật" in card, (
                "Home không hiển thị tiếng Việt có dấu"
            )
            assert "@QA #2026" in card, (
                "Home thiếu ký tự đặc biệt"
            )

            self._evidence("TC-BB-020C", 3)

            # 5. SQLite: kiểm tra chính xác, gồm cả emoji 🚀
            row = self._row(note)
            assert row["status"] == "normal", (
                "Trạng thái ghi chú bị thay đổi"
            )
            assert row["title"] == title, (
                "Tiêu đề ghi chú bị thay đổi"
            )

            actual = _plain(row["content"]).rstrip("\n")
            expected = original + appended

            assert actual == expected, (
                f"Unicode không được lưu chính xác:\n"
                f"Expected: {expected!r}\n"
                f"Actual:   {actual!r}"
            )

            assert actual.count(appended) == 1, (
                "Nội dung Unicode bị lặp"
            )

            # 6. Mở lại kiểm tra nội dung đã lưu
            self._assert_reopen(
                note, title, original, "@QA #2026"
            )

            self._evidence("TC-BB-020C", 4)

            # Xác minh dữ liệu vẫn đúng sau khi mở lại
            persisted = _plain(
                self._row(note)["content"]
            ).rstrip("\n")

            assert persisted == expected, (
                "Dữ liệu Unicode thay đổi sau khi mở lại"
            )

        finally:
            self._cleanup_owned(note, title)



    def test_tc_bb_020d_persistence_after_restart(self):
        """TC-BB-020D: Dữ liệu chỉnh sửa tồn tại sau khởi động lại."""
        tc = "020D"
        original = "Ghi chú gốc kiểm tra khởi động lại."
        appended = "\n[Nội dung đã chỉnh sửa trước khi khởi động lại]"
        note = None
        title = ""

        try:
            # 1. Tạo ghi chú QA độc lập
            note = self._create(tc, original)
            title = note.title

            # 2. Mở và chỉnh sửa
            self._open(title, note)
            self._append(title, appended)
            self._evidence("TC-BB-020D", 2)

            # 3. Lưu và trở về HomeScreen
            self.driver.save_and_exit_editor()
            self._home()

            before_card = self._active_home_card(title)
            assert appended.strip() in before_card, (
                "Home không hiển thị nội dung trước khi restart"
            )

            # Xác minh đúng nội dung và ID trước khi restart
            self._assert_db_edit(
                note, title, original, appended
            )
            self._evidence("TC-BB-020D", 3)

            # 4. Đóng hẳn ứng dụng khi đang ở HomeScreen
            assert self.driver.is_on_home_screen(), (
                "Không ở HomeScreen trước khi restart"
            )

            self.d.app_stop(config.APP_PACKAGE)
            time.sleep(1.0)

            # 5. Khởi động lại ứng dụng
            self.driver.launch_app()
            self._home()

            # 6. Kiểm tra dữ liệu sau restart
            after_card = self._active_home_card(title)
            assert appended.strip() in after_card, (
                "Nội dung chỉnh sửa bị mất sau restart"
            )

            self._assert_db_edit(
                note, title, original, appended
            )
            self._evidence("TC-BB-020D", 4)

            # 7. Mở lại đúng ghi chú, kiểm tra nội dung
            self._assert_reopen(
                note, title, original, appended.strip()
            )

            # Kiểm tra dữ liệu cuối cùng trong SQLite
            actual = _plain(
                self._row(note)["content"]
            ).rstrip("\n")

            assert actual == original + appended, (
                "Dữ liệu không được bảo toàn sau restart"
            )

            self._evidence("TC-BB-020D", 5)

        finally:
            self._cleanup_owned(note, title)


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
