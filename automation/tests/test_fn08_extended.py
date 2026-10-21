"""FN-08 extension: TC-BB-018B..018F (D01).

Use alongside the repository's existing test_fn08_create_note.py (016/017/018).
No application sources are modified. UI tests require the actual Android device.
Evidence uses a unique run directory so existing screenshots remain unchanged.

Usage from repository root:
    python -m pytest -v -s automation/tests/test_fn08_extended.py \
      --junitxml=automation/reports/fn08_extended_<run-id>.xml

WARNING: TC-018C and TC-018F intentionally force-stop only the test app.
Never execute these on a device with unrelated unsaved editing in progress.
"""

import json
import os
import sqlite3
import subprocess
import time
import unicodedata
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime

import pytest

from automation import config
from automation.core.device import SmartNoteDriver


RUN_ID = os.environ.get("FN08_RUN_ID") or datetime.now().strftime("%Y%m%d_%H%M%S_%f")
EVIDENCE_DIR = f"evidence/fn08/automation_{RUN_ID}"


def _semantics(d):
    """Collect decoded Android accessibility strings without XPath quoting issues."""
    try:
        root = ET.fromstring(d.dump_hierarchy())
    except Exception as exc:
        raise AssertionError(f"Cannot inspect Android UI semantics: {exc}") from exc
    return "\n".join(
        (node.attrib.get("content-desc", "") + "\n" + node.attrib.get("text", ""))
        for node in root.iter()
    )


def _clean_unicode(s: str) -> str:
    """Normalize Unicode (NFC), remove formatting/variation selectors and invisible characters."""
    if not s:
        return ""
    norm = unicodedata.normalize("NFC", s)
    return (
        norm.replace("\ufe0f", "")
        .replace("\ufe0e", "")
        .replace("\u200b", "")
        .replace("\u200c", "")
        .replace("\u200d", "")
    )


def _fetch_sqlite_notes(serial: str = None, package: str = None) -> list[dict]:
    """Retrieve all records from SQLite notes table using read-only ADB stream and Python sqlite3.

    This function acts as an internal state verification oracle (UI automation with complementary
    internal data verification, not pure black-box testing). It reads directly from the private
    application database without modifying device data.
    """
    serial = serial or config.DEVICE_SERIAL
    package = package or config.APP_PACKAGE
    cmd = ["adb"]
    if serial:
        cmd.extend(["-s", serial])
    cmd.extend(["exec-out", "run-as", package, "cat", "databases/smart_note.db"])

    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0 or not res.stdout:
        err = res.stderr.decode("utf-8", errors="replace") if res.stderr else "Empty database dump"
        raise RuntimeError(f"Failed to read SQLite db via adb exec-out run-as: {err}")

    conn = sqlite3.connect(":memory:")
    conn.deserialize(res.stdout)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, user_id, title, content, status, is_synced, is_locked, note_color, tags, "
        "image_urls, audio_urls, created_at, updated_at, reminder FROM notes"
    )
    cols = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(cols, row)) for row in rows]


def _extract_note_text(raw_content: str) -> str:
    """Extract plain text from note content (handling Quill Delta JSON format or raw text)."""
    if not raw_content:
        return ""
    try:
        data = json.loads(raw_content)
        if isinstance(data, list):
            parts = []
            for op in data:
                if isinstance(op, dict) and "insert" in op:
                    val = op["insert"]
                    if isinstance(val, str):
                        parts.append(val)
            return "".join(parts)
    except Exception:
        pass
    return raw_content


def _diagnose_accessibility_nodes(d, filter_tokens=("LongText", "Emoji", "2026", "🚀")):
    """Inspect and log text/content-desc of matching accessibility nodes with exact code points and representations."""
    try:
        root = ET.fromstring(d.dump_hierarchy())
    except Exception as exc:
        print(f"[Diagnostic] Cannot dump hierarchy: {exc}")
        return []

    def inspect_val(name, val):
        if not val:
            return
        escaped = val.encode("unicode_escape").decode("ascii")
        cps = " ".join(f"U+{ord(c):04X}" for c in val)
        is_nfc_equal_nfd = (unicodedata.normalize("NFC", val) == unicodedata.normalize("NFD", val))
        print(f"      {name}:")
        print(f"        repr:           {repr(val)}")
        print(f"        ascii:          {ascii(val)}")
        print(f"        unicode_escape: {escaped}")
        print(f"        code points:    {cps}")
        print(f"        NFC == NFD:     {is_nfc_equal_nfd}")
        hidden = []
        if "\ufe0f" in val: hidden.append("VS-16 (\\ufe0f)")
        if "\ufe0e" in val: hidden.append("VS-15 (\\ufe0e)")
        if "\u200b" in val: hidden.append("Zero-Width Space (\\u200b)")
        if "\n" in val: hidden.append("Newline (\\n)")
        if "\r" in val: hidden.append("CR (\\r)")
        if "\u2026" in val: hidden.append("Ellipsis (…)")
        if hidden:
            print(f"        special flags:  {', '.join(hidden)}")

    matching_nodes = []
    print("\n--- [TC-BB-018E ACCESSIBILITY DIAGNOSTIC REPORT] ---")
    for idx, node in enumerate(root.iter()):
        txt = node.attrib.get("text", "")
        desc = node.attrib.get("content-desc", "")
        cls_name = node.attrib.get("class", "")
        bounds = node.attrib.get("bounds", "")

        matches = any(tok in txt or tok in desc for tok in filter_tokens)
        if matches:
            matching_nodes.append((node, txt, desc))
            print(f"  [Match #{len(matching_nodes)}] Tag: <{node.tag}> Class: {cls_name} Bounds: {bounds}")
            inspect_val("text", txt)
            inspect_val("content-desc", desc)

    if not matching_nodes:
        print(f"  [Diagnostic] No nodes matched any of tokens {filter_tokens}!")
    else:
        print(f"  [Diagnostic] Total {len(matching_nodes)} matching node(s) found.")
    print("----------------------------------------------------\n")
    return matching_nodes


def _verify_complex_title(d, expected_title: str, prefix: str = "LongText_UTF8_Emoji_", log_diagnostic: bool = True) -> bool:
    """Verify presence of complex Unicode/Emoji title reliably, handling splitting, normalization, and line breaks."""
    raw_sem = _semantics(d)

    # 1. Exact string match
    if expected_title in raw_sem:
        print("[Title Verify] PASS: Exact title match in accessibility semantics.")
        return True

    # 2. Normalized match (NFC, strip emoji variation selector VS-16 and zero-width spaces)
    clean_expected = _clean_unicode(expected_title)
    clean_sem = _clean_unicode(raw_sem)
    if clean_expected in clean_sem:
        print("[Title Verify] PASS: Normalized match (Unicode NFC / VS-16 stripped).")
        return True

    # 3. Match after removing line-breaks / wrap whitespace (when title wraps across lines in NoteCard)
    nowrap_expected = clean_expected.replace(" ", "").replace("\n", "").replace("\r", "")
    nowrap_sem = clean_sem.replace(" ", "").replace("\n", "").replace("\r", "")
    if nowrap_expected in nowrap_sem:
        print("[Title Verify] PASS: Match after removing line-breaks / wrap whitespace.")
        return True

    # 4. Reconstructed container check (if Flutter split title into adjacent sub-nodes)
    try:
        root = ET.fromstring(d.dump_hierarchy())
        for node in root.iter():
            subtree_texts = []
            for sub in node.iter():
                t = sub.attrib.get("text", "")
                c = sub.attrib.get("content-desc", "")
                if t: subtree_texts.append(t)
                if c: subtree_texts.append(c)

            combined = "".join(subtree_texts)
            if prefix in combined:
                clean_combined = _clean_unicode(combined).replace(" ", "").replace("\n", "").replace("\r", "")
                if nowrap_expected in clean_combined:
                    print("[Title Verify] PASS: Match via reconstructed subtree/card container nodes.")
                    return True
                # Check mandatory elements together: prefix, emoji (🚀 or \U0001f680), and #2026
                has_prefix = prefix in combined
                has_rocket = ("🚀" in combined or "\U0001f680" in combined)
                has_suffix = ("#2026" in combined or "2026" in combined)
                if has_prefix and has_rocket and has_suffix:
                    print("[Title Verify] PASS: Container contains prefix, rocket emoji, and #2026 across sub-nodes.")
                    return True
    except Exception as exc:
        print(f"[Title Verify] Subtree inspection error: {exc}")

    if log_diagnostic:
        print(f"[Title Verify] FAIL: Expected title '{expected_title}' not matched by any strategy.")
        _diagnose_accessibility_nodes(d, [prefix, "🚀", "2026"])
    return False


class TestFN08Extended:
    @classmethod
    def setup_class(cls):
        cls.driver = SmartNoteDriver()
        cls.d = cls.driver.device
        cls.driver.launch_app()
        for _ in range(30):
            if cls.driver.is_on_home_screen():
                break
            time.sleep(0.5)
        else:
            pytest.skip(
                "BLOCKED – app is not on HomeScreen. Log in with a QA account "
                "and open HomeScreen manually; no automatic account selection is performed."
            )

    def _home(self, relaunch=False):
        """Check HomeScreen without invoking driver's automatic Google login flow."""
        if relaunch:
            self.driver.launch_app()
        for _ in range(30):
            if self.driver.is_on_home_screen():
                return
            time.sleep(0.5)
        pytest.skip("BLOCKED – HomeScreen unavailable; login/navigation required")

    def _visible(self, token: str, attempts: int = 12):
        for _ in range(attempts):
            if token in _semantics(self.d):
                return True
            time.sleep(0.5)
        return False

    def _evidence(self, tc: str, seq: int = 1):
        path = f"{EVIDENCE_DIR}/FN08_{tc}_D01_{seq:02d}.png"
        saved = self.driver.capture_evidence(path)
        print(f"[FN-08 evidence] {tc}: {saved}")
        return saved

    def _check_not_existing(self, token: str):
        self._home()
        if self._visible(token, attempts=2):
            pytest.skip(
                f"Test-data collision: a note containing '{token}' exists. "
                "Refusing to delete or reuse an unrelated note."
            )

    def _cleanup_only_own_note(self, token: str, created: bool):
        if not created:
            return
        try:
            if self.driver.is_in_editor():
                self.driver.save_and_exit_editor()
            if self.driver.is_on_home_screen():
                self.driver.cleanup_note_via_selection(token)
            else:
                print("[Cleanup notice] Not on HomeScreen; leaving QA note intact")
        except Exception as exc:
            print(f"[Cleanup notice] Could not clean QA note '{token}': {exc}")

    def _clear_title(self):
        field = self.driver.get_title_field()
        if field is None:
            pytest.skip("BLOCKED – cannot locate editable title field to clear")
        field.click()
        field.set_text("")
        time.sleep(0.3)

    def _clear_quill(self):
        """Select-all + delete in Quill, with an accessibility-based verification.

        If this installation does not expose a keyboard-editable Quill view,
        do not pretend the note was cleared: mark this run as SKIPPED/BLOCKED.
        """
        d = self.d
        # This coordinate is the verified Editor body region on S21 FE 1080x2340.
        # Verify actual input after actions, rather than trusting the coordinate.
        d.click(540, 520)
        time.sleep(0.3)
        try:
            # KEYCODE_A=29 with META_CTRL_ON=0x1000; KEYCODE_DEL=67.
            d.jsonrpc.pressKeyCode(29, 0x1000)
            d.jsonrpc.pressKeyCode(67)
        except Exception:
            try:
                focused = d(className="android.widget.EditText", focused=True)
                if not focused.exists:
                    pytest.skip("BLOCKED – Quill has no editable accessibility element")
                focused.clear_text()
            except Exception as exc:
                pytest.skip(f"BLOCKED – cannot clear Quill text safely: {exc}")
        time.sleep(0.4)

    def _paste_complex_quill(self, content: str):
        """Paste multiline content once without relying on a full visible XML match.

        Rich-text accessibility can virtualize long paragraphs, so a full XML
        string match *at input time* can reject a successful clipboard paste.
        Actual persisted content is checked again after reopening the note.
        """
        placeholder = self.d(description="Ghi chú") or self.d(text="Ghi chú")
        if placeholder.exists:
            placeholder.click()
        else:
            self.d.click(540, 520)
        time.sleep(0.4)
        self.d.set_clipboard(content)
        time.sleep(0.3)
        try:
            self.d.jsonrpc.pasteClipboard()
        except Exception as exc:
            pytest.skip(f"BLOCKED – cannot paste multiline Quill content: {exc}")
        time.sleep(1.1)

    def test_tc_bb_018b_title_only(self):
        title = "Nhắc nhở họp gấp"
        created = False
        self._check_not_existing(title)
        try:
            self.driver.open_note_editor()
            created = True
            self.driver.input_title(title)
            self.driver.save_and_exit_editor()
            assert self._visible(title), "Title-only note was not shown on HomeScreen"
            self.driver.open_existing_note(title)
            semantic = _semantics(self.d)
            assert title in semantic, "Reopened note title differs"
            # Content remains untouched; no input_content() is called in this TC.
            self.driver.save_and_exit_editor()
        finally:
            self._evidence("TC-BB-018B")
            self._cleanup_only_own_note(title, created)

    def test_tc_bb_018c_autosave_without_back(self):
        title = "Ghi chú autosave kiểm chứng"
        content = "Dữ liệu này được tự động lưu ngầm không cần bấm nút Back"
        created = False
        self._check_not_existing(title)
        try:
            self.driver.open_note_editor()
            created = True
            self.driver.input_title(title)
            self.driver.input_content(content)
            assert self.driver.is_in_editor(), "Editor closed before force-stop"
            time.sleep(3.0)  # >= 2.5 s after finished input; no Back
            self.d.app_stop(config.APP_PACKAGE)
            self._home(relaunch=True)
            assert self._visible(title), "Autosaved note absent after force-stop"
            self.driver.open_existing_note(title)
            assert self._visible(content), "Autosaved content not retained after app restart"
            self.driver.save_and_exit_editor()
        finally:
            self._evidence("TC-BB-018C")
            self._cleanup_only_own_note(title, created)

    def test_tc_bb_018d_empty_draft_is_discarded(self):
        # Exact source data: title='Tạm', content='Tạm'. Avoid touching an older note.
        title = "Tạm"
        self._check_not_existing(title)
        initial = self.driver.get_home_notes_state()
        self.driver.open_note_editor()
        try:
            self.driver.input_title(title)
            self.driver.input_content(title)
            time.sleep(1.8)
            self._clear_title()
            self._clear_quill()
            # If text is still present, this is automation/precondition trouble,
            # not proof that the application failed its empty-draft behavior.
            if title in _semantics(self.d):
                pytest.skip("BLOCKED – clear operation not verified; cannot test empty-draft rule")
            self.driver.save_and_exit_editor()
            assert not self._visible(title, attempts=8), "Cleared draft still exists"
            after = self.driver.get_home_notes_state()
            assert after["count"] == initial["count"], (
                f"Empty draft changed HomeScreen item count: {initial['count']} -> {after['count']}"
            )
        finally:
            self._evidence("TC-BB-018D")
            if self.driver.is_in_editor():
                self.driver.save_and_exit_editor()
            # No blind cleanup of title='Tạm': it may be unrelated if test crashed.

    def _open_complex_note(self, expected_title: str, prefix: str = "LongText_UTF8_Emoji_"):
        """Locate and open NoteCard with complex title, using prefix locator as resilient fallback."""
        d = self.d
        cancel_btn = (
            d(descriptionContains="Hủy chọn")
            or d(descriptionContains="Cancel")
            or d(textContains="Hủy chọn")
        )
        if cancel_btn.exists:
            try:
                cancel_btn.click()
                time.sleep(0.5)
            except Exception:
                pass

        card = None
        # Strategy 1: Try exact title
        for _ in range(3):
            card = d(descriptionContains=expected_title) or d(textContains=expected_title)
            if card.exists:
                break
            time.sleep(0.3)

        # Strategy 2: Resilient fallback to unique prefix
        if card is None or not card.exists:
            card = d(descriptionContains=prefix) or d(textContains=prefix)
            if not card.exists:
                xpath_expr = f'//*[contains(@content-desc, "{prefix}") or contains(@text, "{prefix}")]'
                if d.xpath(xpath_expr).exists:
                    card = d.xpath(xpath_expr)

        assert card is not None and card.exists, (
            f"Cannot locate NoteCard with title/prefix '{prefix}' on HomeScreen."
        )

        try:
            b = card.info.get("bounds", {})
            if b:
                cx = (b.get("left", 0) + b.get("right", 0)) // 2
                cy = (b.get("top", 0) + b.get("bottom", 0)) // 2
                d.click(cx, cy)
            else:
                card.click()
        except Exception:
            card.click()

        for _ in range(8):
            time.sleep(0.5)
            if self.driver.is_in_editor():
                time.sleep(0.5)
                return

        assert self.driver.is_in_editor(), f"Failed to open EditorScreen for note with prefix '{prefix}'."

    def _cleanup_complex_note(self, title: str, prefix: str, created: bool):
        if not created:
            return
        try:
            if self.driver.is_in_editor():
                self.driver.save_and_exit_editor()
            if self.driver.is_on_home_screen():
                card = self.d(descriptionContains=title) or self.d(textContains=title)
                if card.exists:
                    self.driver.cleanup_note_via_selection(title)
                else:
                    self.driver.cleanup_note_via_selection(prefix)
            else:
                print("[Cleanup notice] Not on HomeScreen; leaving QA note intact")
        except Exception as exc:
            print(f"[Cleanup notice] Could not clean QA note: {exc}")

    def test_tc_bb_018e_complex_unicode_note(self):
        """TC-BB-018E: Tạo ghi chú chứa Unicode phức tạp, tiếng Việt, emoji, ký tự đặc biệt, HTML-like text.

        Phương pháp kiểm thử:
        - UI Automation (UIAutomator2): Thao tác giao diện tạo ghi chú, nhập tiêu đề, dán nội dung,
          lưu/thoát về HomeScreen, và mở lại ghi chú trên HomeScreen.
        - Internal State Verification Oracle (SQLite chỉ đọc):
          Do Android Accessibility XML thay thế emoji ngoài BMP (như 🚀 U+1F680) bằng hai dấu chấm '..',
          việc kiểm tra emoji qua tầng accessibility UI không phản ánh đúng dữ liệu thực tế đã lưu.
          Kịch bản sử dụng cơ chế kiểm chứng dữ liệu nội bộ bổ sung (internal state verification oracle)
          bằng cách đọc trực tiếp SQLite qua `adb exec-out run-as` và `sqlite3` của Python ở chế độ
          chỉ đọc. Đây là UI automation có kiểm chứng dữ liệu nội bộ bổ sung, không gọi là kiểm thử
          hộp đen thuần túy.
        - Định danh bản ghi và chống xung đột:
          So sánh snapshot trạng thái SQLite trước và sau khi tạo để xác định chính xác bản ghi sinh ra
          trong lần chạy hiện tại; tuyệt đối không lấy bản ghi cũ làm bằng chứng PASS.
          Không tự động xóa 4 ghi chú hiện có. Nếu dữ liệu trùng lặp khiến không thể xác định an toàn
          ghi chú qua giao diện, kịch bản báo BLOCKED rõ ràng.
        """
        title = "LongText_UTF8_Emoji_🚀_#2026"
        prefix = "LongText_UTF8_Emoji_"
        marker_end = "FINAL_FN08_018E_2026"
        # 11 dòng dữ liệu kiểm thử
        lines = [
            "L01 Tiếng Việt: ắ ằ ẳ ẵ ặ ấ ầ ẩ ẫ ậ ê ô ơ ư đ",
            "L02 Biểu tượng: 😀 😁 😂 🤣 😃 😄",
            "L03 Biểu tượng: 😅 😆 😉 😊 😋 😎 😍",
            "L04 Biểu tượng: 😘 😗 😙 😚 ☺️ 😇 🔥",
            "L05 Biểu tượng: 🚀 🌟 💡 📌 📝 📅",
            "L06 Special: !@#$%^&*()_+~|}{[]:;?><,./-=",
            'L07 HTML: <div><span style="color:red">Test Content</span></div>',
            "L08 HTML entity: &lt;script&gt;",
            'L09 Quotes: \'Single quote\', "Double quote", `Backtick`',
            "L10 Indent:\tTab 1\t\tTab 2",
            "L11 End marker: FINAL_FN08_018E_2026",
        ]
        content = "\n".join(lines)
        created = False

        self._home()

        # Step 0: Đọc snapshot SQLite ban đầu để xác định baseline và kiểm tra collision
        initial_notes = _fetch_sqlite_notes(self.driver.serial, config.APP_PACKAGE)
        initial_ids = {n["id"] for n in initial_notes}

        # Yêu cầu 5: Không tự động xóa 4 ghi chú hiện có.
        # Nếu đã có ghi chú active (status == 'normal') trùng tiêu đề hoặc tiền tố,
        # giao diện HomeScreen sẽ bị nhiễu do tồn tại nhiều thẻ trùng lặp -> Báo BLOCKED.
        active_duplicates = [
            n for n in initial_notes
            if n.get("status") == "normal" and (
                n.get("title") == title or n.get("title", "").startswith(prefix)
            )
        ]
        if active_duplicates:
            pytest.skip(
                f"BLOCKED – Test-data collision: Có {len(active_duplicates)} ghi chú trùng tiêu đề/tiền tố "
                f"'{prefix}' đang ở trạng thái active (normal) trên HomeScreen/SQLite. "
                "Không tự động xóa 4 ghi chú hiện có; cần dọn dẹp môi trường trước khi chạy lại."
            )

        if self._visible(prefix, attempts=2):
            pytest.skip(
                f"BLOCKED – Test-data collision: Thẻ ghi chú chứa tiền tố '{prefix}' đã hiển thị trên HomeScreen. "
                "Không tự động xóa dữ liệu hiện có; báo BLOCKED để tránh thao tác sai thẻ qua giao diện."
            )

        try:
            # 1. Thao tác UI: Mở EditorScreen và nhập tiêu đề
            self.driver.open_note_editor()
            created = True
            self.driver.input_title(title)
            print("\n[TC-BB-018E Step 1] Đã nhập tiêu đề vào EditorScreen.")
            self._evidence("TC-BB-018E", 1)

            # 2. Thao tác UI: Dán nội dung 11 dòng vào Quill Editor
            self._paste_complex_quill(content)
            print("[TC-BB-018E Step 2] Đã dán nội dung 11 dòng vào Quill Editor.")
            self._evidence("TC-BB-018E", 2)

            # 3. Thao tác UI: Lưu và thoát Editor về HomeScreen
            self.driver.save_and_exit_editor()
            on_home = self.driver.is_on_home_screen()
            assert on_home, "Failed to return to HomeScreen after saving complex note"
            print("[TC-BB-018E Step 3] Đã lưu ghi chú và xác nhận quay về HomeScreen thành công.")
            self._evidence("TC-BB-018E", 3)

            # 4. Xác minh dữ liệu qua SQLite Verification Oracle (UI automation có kiểm chứng dữ liệu nội bộ bổ sung)
            # Yêu cầu 4: So sánh snapshot trước và sau khi tạo để xác định chính xác bản ghi của lần chạy này.
            post_notes = _fetch_sqlite_notes(self.driver.serial, config.APP_PACKAGE)
            new_notes = [
                n for n in post_notes
                if n["id"] not in initial_ids and n.get("title", "").startswith(prefix)
            ]
            assert len(new_notes) == 1, (
                f"Expected exactly 1 newly created note in current run, but found {len(new_notes)}. "
                f"New IDs: {[n.get('id') for n in new_notes]}. Không lấy bản ghi cũ làm bằng chứng PASS."
            )
            target_note = new_notes[0]
            print(f"[TC-BB-018E Oracle] Xác định duy nhất bản ghi mới tạo trong lần chạy này: id={target_note['id']}")

            # Yêu cầu 3 & 6: Xác minh chính xác tiêu đề, emoji, tiếng Việt, ký tự đặc biệt, HTML-like text và đủ 11 dòng
            # a) Tiêu đề và emoji 🚀
            assert target_note["title"] == title, (
                f"Title mismatch in SQLite! Expected: {title!r}, Actual: {target_note['title']!r}"
            )
            assert "🚀" in target_note["title"], "Emoji '🚀' was lost or corrupted in SQLite title."
            assert target_note["title"].endswith("#2026"), "Title suffix '#2026' was lost in SQLite."

            # b) Trích xuất văn bản nội dung từ Quill Delta JSON trong SQLite
            raw_content = target_note.get("content", "")
            extracted_text = _extract_note_text(raw_content)
            extracted_lines = [line for line in extracted_text.split("\n") if line.strip()]

            # c) Xác minh đủ 11 dòng
            assert len(extracted_lines) == 11, (
                f"Expected exactly 11 lines in saved note, but found {len(extracted_lines)}. "
                f"Extracted lines: {extracted_lines}"
            )

            # d) Xác minh từng dòng và các thành phần dữ liệu đặc biệt
            # Dòng 1: Tiếng Việt đầy đủ thanh điệu
            assert "ắ ằ ẳ ẵ ặ ấ ầ ẩ ẫ ậ ê ô ơ ư đ" in extracted_text, "Vietnamese characters were corrupted or lost in SQLite."
            # Dòng 2..5: Emojis
            assert "😀" in extracted_text, "Emoji '😀' was lost in SQLite."
            assert "🔥" in extracted_text, "Emoji '🔥' was lost in SQLite."
            assert "🚀" in extracted_text, "Emoji '🚀' was lost in SQLite content."
            # Dòng 6: Ký tự đặc biệt
            assert "!@#$%^&*()_+~|}{[]:;?><,./-=" in extracted_text, "Special characters were corrupted or lost in SQLite."
            # Dòng 7..8: HTML-like tags và entity
            assert '<div><span style="color:red">Test Content</span></div>' in extracted_text, "HTML-like tag content was lost or transformed."
            assert "Test Content" in extracted_text, "'Test Content' text was lost in SQLite."
            assert "&lt;script&gt;" in extracted_text, "HTML entity was lost or transformed."
            # Dòng 9: Quotes
            assert "'Single quote'" in extracted_text and '"Double quote"' in extracted_text, "Quotes were corrupted or stripped."
            # Dòng 10: Tabs/Indent
            assert "\tTab 1\t\tTab 2" in extracted_text, "Tab indents were stripped or lost."
            # Dòng 11: End marker
            assert marker_end in extracted_text, f"End marker '{marker_end}' was lost in SQLite."

            # Đối sánh 1-1 từng dòng với dữ liệu gốc
            for idx, (exp_line, act_line) in enumerate(zip(lines, extracted_lines), 1):
                assert exp_line == act_line, (
                    f"Line {idx:02d} mismatch in SQLite! Expected: {exp_line!r}, Actual: {act_line!r}"
                )
            print("[TC-BB-018E Oracle] SQLite xác minh thành công toàn bộ 11 dòng, emoji, tiếng Việt, ký tự đặc biệt, HTML-like.")
            self._evidence("TC-BB-018E", 4)

            # 5. Thao tác UI: Mở lại đúng ghi chú trên HomeScreen qua UIAutomator2 để hoàn tất kiểm thử giao diện
            # Lưu ý: Android Accessibility XML thay 🚀 bằng '..', hàm `_open_complex_note` sử dụng prefix
            # định danh an toàn để click mở thẻ NoteCard mới tạo.
            self._open_complex_note(title, prefix)
            print("[TC-BB-018E Step 5] Đã mở lại ghi chú trên UI HomeScreen.")
            collected = _semantics(self.d)
            for _ in range(6):
                self.d.swipe(550, 1710, 550, 720, 0.35)
                time.sleep(0.35)
                collected += "\n" + _semantics(self.d)
            self._evidence("TC-BB-018E", 5)

            # Kiểm tra UI sanity: các markers cơ bản xuất hiện trên giao diện Editor khi mở lại
            assert "Test Content" in collected or "L01" in collected, (
                "Reopened note in Editor did not show expected content on UI."
            )
            print("[TC-BB-018E Step 5] Kiểm tra UI mở lại ghi chú thành công.")
        finally:
            self._evidence("TC-BB-018E", 6)
            if os.environ.get("FN08_DEBUG") == "1":
                print(
                    "[TC-BB-018E DEBUG] FN08_DEBUG=1: Bỏ qua cleanup để bảo tồn trạng thái thiết bị phục vụ điều tra."
                )
            else:
                self._cleanup_complex_note(title, prefix, created)

    def test_tc_bb_018f_persistence_after_restart(self):
        title = f"QA_FN08_018F_{uuid.uuid4().hex[:10]}"
        content = f"Persistence check {title}"
        created = False
        self._check_not_existing(title)
        try:
            self.driver.open_note_editor()
            created = True
            self.driver.input_title(title)
            self.driver.input_content(content)
            self.driver.save_and_exit_editor()
            assert self._visible(title), "Note was not created before restart"
            self.d.app_stop(config.APP_PACKAGE)
            self._home(relaunch=True)
            assert self._visible(title), "Created note did not survive app restart"
            self.driver.open_existing_note(title)
            assert self._visible(content), "Reopened note content changed after restart"
            self.driver.save_and_exit_editor()
        finally:
            self._evidence("TC-BB-018F")
            self._cleanup_only_own_note(title, created)
