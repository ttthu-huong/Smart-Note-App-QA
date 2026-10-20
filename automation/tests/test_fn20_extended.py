# -*- coding: utf-8 -*-
# FN20-V9: account-scoped all-pinned test 024G; no changes to app lib.
"""Automation Phase 4 Suite for FN-20 (Pin / Unpin Note) Extended.

Covers the 13 previously unautomated execution items for FN-20:
- Editor (3 items):
  - TC-BB-024B D01: Ghim ghi chú trực tiếp từ AppBar màn hình soạn thảo (Editor)
  - TC-BB-024B D02: Bỏ ghim ghi chú trực tiếp từ AppBar màn hình soạn thảo (Editor)
  - TC-BB-024C D01: Ràng buộc không cho phép ghim ghi chú mới khi chưa nhập nội dung
- Batch (4 items):
  - TC-BB-024D D01: Ghim đồng thời nhiều ghi chú từ Trang chủ (Batch Pin)
  - TC-BB-024H D01: Đảo trạng thái độc lập khi chọn đồng thời ghi chú đã ghim và chưa ghim (Mixed Toggle)
  - TC-BB-025D D01: Bỏ ghim đồng thời nhiều ghi chú từ Trang chủ (Batch Unpin)
  - TC-BB-025E D01: Phân vùng 'Được ghim' vẫn duy trì khi chỉ bỏ ghim 1 trong số nhiều note ghim (Mixed State)
- Layout & Dữ liệu (3 items):
  - TC-BB-024E D01: Hiển thị phân vùng 'Được ghim' và 'Khác' khi có đồng thời cả 2 loại ghi chú
  - TC-BB-024F D01: Tính toàn vẹn dữ liệu (Tiêu đề, Nội dung) qua chu kỳ Pin/Unpin
  - TC-BB-024G D01: Giao diện khi toàn bộ các ghi chú đều ở trạng thái được ghim (All Notes Pinned)
- Persistence & Edit (3 items):
  - TC-BB-025B D01: Tính bền vững trạng thái Ghim sau khi khởi động lại ứng dụng (Pinned Persistence)
  - TC-BB-025C D01: Ghi chú đã ghim vẫn duy trì trạng thái ghim sau khi chỉnh sửa nội dung
  - TC-BB-025F D01: Tính bền vững trạng thái Bỏ ghim sau khi khởi động lại ứng dụng (Unpin Persistence)

Standards: IEEE 829 & ISTQB Test Execution
Platform: Android (uiautomator2 + ADB + SQLite Read-Only Oracle)
Device: Samsung Galaxy S21 FE 5G (Android 14)
Safety:
- Isolated test data per test case using unique UUID markers.
- Non-destructive execution: no note deletions, no moving to Trash for cleanup.
- Safe precondition verification on TC-BB-024G with pytest.skip fallback.
"""

import json
import os
import sqlite3
import subprocess
import sys
import time
import uuid
from datetime import datetime

import pytest

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from automation import config
from automation.core.device import SmartNoteDriver
from automation.core.qa_note_helper import QANoteHelper


class TestFN20Extended:
    """Phase 4 Extended Automation Test Suite for FN-20 (Pin/Unpin Note)."""

    driver: SmartNoteDriver
    d: object

    @classmethod
    def setup_class(cls):
        cls.driver = SmartNoteDriver()
        cls.d = cls.driver.device
        cls.driver.ensure_home_screen()

    @classmethod
    def teardown_class(cls):
        try:
            cls.driver.ensure_home_screen()
        except Exception as exc:
            print(f"[TEARDOWN WARNING] {exc}")

    # =========================================================================
    # COMMON HELPERS: SELECTORS, DB ORACLE, SCREENSHOTS, RESTART
    # =========================================================================

    def _first(self, *selectors):
        """Return the first existing selector or None."""
        for item in selectors:
            try:
                if item is not None and item.exists:
                    return item
            except Exception:
                pass
        return None

    def _start(self, tc: str):
        """Prepare clean HomeScreen state and generate unique run marker & folder."""
        marker = uuid.uuid4().hex[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = f"evidence/fn20/run_{timestamp}_{marker}/{tc}"

        print(f"\n{'='*70}")
        print(f"[START] {tc} | marker={marker}")
        print(f"{'='*70}")

        self.driver.ensure_device_ready()
        self.driver.launch_app()
        time.sleep(1.0)

        current = self.d.app_current()
        assert current.get("package") == config.APP_PACKAGE, (
            f"Smart Note App not in foreground: {current}"
        )

        self.driver.ensure_home_screen()
        assert self.driver.is_on_home_screen(), (
            f"Precondition failed: Cannot return to HomeScreen before {tc}"
        )

        return marker, folder

    def _shot(self, folder: str, tc: str, number: int):
        """Capture screenshot evidence with deterministic naming."""
        path = f"{folder}/{tc}_{number:02d}.png"
        full_path = self.driver.capture_evidence(path)
        print(f"[EVIDENCE] {path} -> {full_path}")
        return full_path

    def _db(self) -> dict:
        """Read SQLite database via ADB run-as into memory (strictly read-only)."""
        result = subprocess.run(
            [
                "adb", "-s", self.driver.serial,
                "exec-out", "run-as",
                config.APP_PACKAGE,
                "cat", "databases/smart_note.db",
            ],
            capture_output=True,
            timeout=25,
        )

        assert result.returncode == 0 and result.stdout, (
            "Cannot read SQLite database via ADB: "
            + result.stderr.decode(errors="replace")
        )

        conn = sqlite3.connect(":memory:")
        try:
            conn.deserialize(result.stdout)
            rows = conn.execute(
                "SELECT id, title, content, status FROM notes"
            ).fetchall()

            return {
                rid: {
                    "title": title,
                    "content": content,
                    "status": status,
                }
                for rid, title, content, status in rows
            }
        finally:
            conn.close()

    @staticmethod
    def _plain(raw: str) -> str:
        """Extract plain text from Quill delta JSON or return raw trimmed string."""
        if not raw:
            return ""
        try:
            value = json.loads(raw)
            if isinstance(value, dict):
                value = value.get("ops", [])
            if isinstance(value, list):
                return "".join(
                    item["insert"]
                    for item in value
                    if isinstance(item, dict)
                    and isinstance(item.get("insert"), str)
                ).strip()
        except (ValueError, TypeError):
            pass
        return raw.strip()

    def _wait_row(self, rid: str, expected_status: str, title: str = None, content: str = None, timeout: float = 25.0):
        """Poll SQLite until QA note reaches expected status and verify data."""
        end = time.monotonic() + timeout
        last_row = None

        while time.monotonic() < end:
            rows = self._db()
            row = rows.get(rid)
            last_row = row

            if row and row["status"] == expected_status:
                if title is not None:
                    assert row["title"] == title, (
                        f"Title mismatch for note {rid}: expected '{title}', got '{row['title']}'"
                    )
                if content is not None:
                    plain_db = self._plain(row["content"])
                    assert content.strip() and content.strip() in plain_db, (
                        f"Content mismatch for note {rid}: expected to contain '{content}', got '{plain_db}'"
                    )
                return row

            time.sleep(0.5)

        raise AssertionError(
            f"QA note {rid} did not reach status='{expected_status}' within {timeout}s; "
            f"last row={last_row}"
        )

    def _find_note_in_home_by_scrolling(self, title: str, max_swipes: int = 24):
        """Find a note outside the visible Home viewport without modifying any note.

        Scan down first (past long pinned sections), then back up if the
        HomeScreen retained an old scroll position. Both directions are bounded.
        Leave the desired card visible for the next Editor/selection action.
        """
        assert self.driver.is_on_home_screen(), (
            f"Cannot search HomeScreen for '{title}': not on HomeScreen."
        )
        card = self._card(title, scroll=False)
        if card is not None and card.exists:
            return card

        width, height = self.d.window_size()
        x = int(width * 0.70)  # Away from Android Back gesture edge.
        for direction in ("down", "up"):
            unchanged = 0
            for attempt in range(max_swipes):
                before = self.d.dump_hierarchy()
                if direction == "down":
                    self.d.swipe(x, int(height * 0.77), x, int(height * 0.33), steps=16)
                else:
                    self.d.swipe(x, int(height * 0.33), x, int(height * 0.77), steps=16)
                time.sleep(0.4)

                assert self.driver.is_on_home_screen(), (
                    f"HomeScreen changed unexpectedly while finding '{title}'."
                )
                card = self._card(title, scroll=False)
                if card is not None and card.exists:
                    print(f"[UI SEARCH] Found '{title}' after {direction} scroll #{attempt + 1}")
                    return card

                after = self.d.dump_hierarchy()
                unchanged = unchanged + 1 if after == before else 0
                if unchanged >= 2:
                    print(f"[UI SEARCH] Reached {direction} scroll boundary")
                    break

        return None

    def _new(self, title: str, content: str) -> str:
        """Create exactly one QA note; recover from UI-only verification timeout.

        The existing shared QANoteHelper may raise *after saving* because the
        new normal note is below a long pinned section. Never call it again
        after that timeout: resolve the saved note by its new SQLite ID, then
        require it to be visible via bounded HomeScreen scrolling.
        """
        self.driver.ensure_home_screen()
        before_rows = self._db()
        before_ids = set(before_rows)
        assert not any(row["title"] == title for row in before_rows.values()), (
            f"Test title already exists; refusing to create a duplicate: '{title}'"
        )

        missed_ui_timeout = False
        try:
            created = QANoteHelper.create_test_note(
                self.driver, title, content, poll_timeout=10.0
            )
            assert created, f"QANoteHelper returned False for '{title}'."
        except AssertionError as exc:
            # Only recover the known post-save UI timeout; all other errors
            # (including Editor/save errors) must propagate unchanged.
            expected_prefix = (
                f"[QANoteHelper ERROR] Created note '{title}' "
                "not found on HomeScreen after "
            )
            if not str(exc).startswith(expected_prefix):
                raise
            missed_ui_timeout = True
            print(f"[UI VERIFY TIMEOUT] '{title}' not visible yet; checking SQLite. No retry creation.")

        rows = self._db()
        new_ids = [
            rid for rid, row in rows.items()
            if rid not in before_ids
            and row["title"] == title
            and row["status"] == "normal"
        ]
        assert len(new_ids) == 1, (
            f"Cannot uniquely identify newly created normal QA note '{title}' "
            f"after save. New IDs: {new_ids}; all title matches: "
            f"{[rid for rid, row in rows.items() if row['title'] == title]}. "
            "Not creating the note again."
        )

        rid = new_ids[0]
        self._wait_row(rid, "normal", title, content)

        if missed_ui_timeout:
            card = self._find_note_in_home_by_scrolling(title)
            if card is None:
                debug_path = (
                    "evidence/fn20/"
                    f"debug_card_missing_{title}_{datetime.now():%Y%m%d_%H%M%S}.png"
                )
                try:
                    print(f"[UI DEBUG SCREENSHOT] {self.driver.capture_evidence(debug_path)}")
                    print(f"[UI DEBUG TEXTS] {self.driver.get_screen_texts()}")
                except Exception as debug_exc:
                    print(f"[UI DEBUG ERROR] {debug_exc}")
                raise AssertionError(
                    f"Note '{title}' (SQLite id={rid}, status=normal) was saved, "
                    "but its card was not found on HomeScreen after bounded scrolling. "
                    "This is FAIL-AUTO in setup, not a Pin/Unpin result."
                )

        print(f"[QA CREATED] {title} | SQLite ID={rid}")
        return rid

    def _card(self, title: str, scroll: bool = False):
        """Locate note card on HomeScreen by exact or partial unique title."""
        width, height = self.d.window_size()
        attempts = 6 if scroll else 1

        for attempt in range(attempts):
            card = self._first(
                self.d(descriptionContains=title),
                self.d(textContains=title),
            )
            if card is not None:
                return card

            # XPath check
            xpath_expr = f'//*[contains(@content-desc, "{title}") or contains(@text, "{title}")]'
            if self.d.xpath(xpath_expr).exists:
                return self.d.xpath(xpath_expr)

            if scroll and attempt < attempts - 1:
                self.d.swipe(
                    int(width * 0.70),
                    int(height * 0.75),
                    int(width * 0.70),
                    int(height * 0.35),
                    steps=16,
                )
                time.sleep(0.4)

        return None

    def _open_existing_note_with_scroll(self, title: str):
        """Open a specific QA note even when its card is outside the viewport.

        After Pin/Unpin the card moves between Home sections. The shared
        SmartNoteDriver.open_existing_note() searches only the visible area;
        use bounded, read-only scrolling here without changing shared code.
        """
        assert self.driver.is_on_home_screen(), (
            f"Expected HomeScreen before opening QA note '{title}'."
        )
        card = self._find_note_in_home_by_scrolling(title)
        if card is None or not card.exists:
            path = (
                f"evidence/fn20/debug_open_missing_{title}_"
                f"{datetime.now():%Y%m%d_%H%M%S}.png"
            )
            try:
                print(f"[OPEN NOTE DEBUG] Screenshot: {self.driver.capture_evidence(path)}")
                print(f"[OPEN NOTE DEBUG] Visible texts: {self.driver.get_screen_texts()}")
            except Exception as exc:
                print(f"[OPEN NOTE DEBUG] Could not save diagnostics: {exc}")
            raise AssertionError(
                f"Cannot find QA NoteCard '{title}' on Home after bounded scrolling. "
                "FAIL-AUTO: Editor was not opened."
            )

        # Click the visible note card by its actual element bounds; never use
        # coordinates for an unrelated note or an absolute card index.
        bounds = card.info.get("bounds", {})
        if bounds and bounds.get("right", 0) > bounds.get("left", 0) and bounds.get("bottom", 0) > bounds.get("top", 0):
            x = (bounds["left"] + bounds["right"]) // 2
            y = (bounds["top"] + bounds["bottom"]) // 2
            self.d.click(x, y)
        else:
            card.click()

        for _ in range(12):
            if self.driver.is_in_editor():
                print(f"[OPEN NOTE] Editor opened for '{title}'")
                return
            time.sleep(0.5)

        raise AssertionError(
            f"Tapped NoteCard '{title}' but EditorScreen did not open. "
            f"Visible UI: {self.driver.get_screen_texts()}"
        )

    def _restart(self):
        """Force-stop and relaunch app cleanly, testing persistence."""
        print("[LIFECYCLE] Force-stopping app via ADB...")
        subprocess.run(
            [
                "adb", "-s", self.driver.serial,
                "shell", "am", "force-stop",
                config.APP_PACKAGE,
            ],
            check=True,
            timeout=10,
        )
        time.sleep(1.0)

        print("[LIFECYCLE] Relaunching app...")
        self.driver.ensure_device_ready()
        self.driver.launch_app()
        time.sleep(1.5)
        self.driver.ensure_home_screen()
        time.sleep(0.8)
        assert self.driver.is_on_home_screen(), (
            "App failed to return to HomeScreen after restart."
        )

    # =========================================================================
    # PIN / UNPIN INTERACTION HELPERS
    # =========================================================================

    def _toggle_pin_toolbar(self):
        """Click 'Ghim/Bỏ ghim hàng loạt' icon button on Selection Mode AppBar."""
        pin_btn = self._first(
            self.d(description="Ghim/Bỏ ghim hàng loạt"),
            self.d(descriptionContains="Ghim/Bỏ ghim"),
            self.d(description="Pin/Unpin notes"),
            self.d(descriptionContains="Pin/Unpin"),
        )
        if pin_btn is None:
            xpath_btn = self.d.xpath(
                '//*[contains(@content-desc, "Ghim/Bỏ ghim") or contains(@content-desc, "Pin/Unpin")]'
            )
            if xpath_btn.exists:
                pin_btn = xpath_btn

        assert pin_btn is not None and pin_btn.exists, (
            "Cannot locate 'Ghim/Bỏ ghim hàng loạt' button on Selection Mode AppBar."
        )
        pin_btn.click()
        time.sleep(1.2)

    def _click_editor_pin_button(self, expect_pinned: bool = False):
        """Click Pin/Unpin icon button on EditorScreen AppBar.

        Dynamic-First, Coordinate-Fallback:
        - When note is normal: tooltip is 'Ghim' (Icons.push_pin_outlined).
        - When note is pinned: tooltip is 'Bỏ ghim' (Icons.push_pin).
        """
        tooltip = "Bỏ ghim" if expect_pinned else "Ghim"
        alt_tooltip = "Unpin" if expect_pinned else "Pin"

        btn = self._first(
            self.d(description=tooltip),
            self.d(description=alt_tooltip),
            self.d(descriptionContains=tooltip),
            self.d(descriptionContains=alt_tooltip),
        )
        if btn is None:
            xpath_btn = self.d.xpath(
                f'//*[contains(@content-desc, "{tooltip}") or contains(@content-desc, "{alt_tooltip}")]'
            )
            if xpath_btn.exists:
                btn = xpath_btn

        if btn is not None and btn.exists:
            btn.click()
        else:
            # Coordinate Fallback: Pin action button is located in the top-right AppBar
            # Resolution: 1080x2340 (Samsung Galaxy S21 FE 5G) -> x=860, y=170
            print(f"[FALLBACK] Tapping Editor Pin button via coordinate (860, 170)...")
            self.d.click(860, 170)

        time.sleep(1.2)

    def _pin_note_via_home(self, title: str):
        """Pin a single note via HomeScreen Selection Mode."""
        # Ensure the exact QA card is visible before calling the shared
        # long-press helper (which intentionally does not scroll).
        if self._card(title, scroll=False) is None:
            assert self._find_note_in_home_by_scrolling(title) is not None, (
                f"Cannot find QA note '{title}' for Pin/Unpin."
            )
        assert self.driver.select_note_by_long_press(title), (
            f"Failed to activate Selection Mode for note '{title}'."
        )
        self._toggle_pin_toolbar()

    def _unpin_note_via_home(self, title: str):
        """Unpin a single note via HomeScreen Selection Mode."""
        # Ensure the exact QA card is visible before calling the shared
        # long-press helper (which intentionally does not scroll).
        if self._card(title, scroll=False) is None:
            assert self._find_note_in_home_by_scrolling(title) is not None, (
                f"Cannot find QA note '{title}' for Pin/Unpin."
            )
        assert self.driver.select_note_by_long_press(title), (
            f"Failed to activate Selection Mode for pinned note '{title}'."
        )
        self._toggle_pin_toolbar()

    def _is_pinned_section_visible(self) -> bool:
        """Check if 'Được ghim' / 'Pinned' section header is visible on HomeScreen."""
        return (
            self.d(text="Được ghim").exists
            or self.d(description="Được ghim").exists
            or self.d(text="Pinned").exists
            or self.d(description="Pinned").exists
            or self.d.xpath('//*[@text="Được ghim" or @content-desc="Được ghim"]').exists
        )

    def _is_others_section_visible(self) -> bool:
        """Check if 'Khác' / 'Others' section header is visible on HomeScreen."""
        return (
            self.d(text="Khác").exists
            or self.d(description="Khác").exists
            or self.d(text="Others").exists
            or self.d(description="Others").exists
            or self.d.xpath('//*[@text="Khác" or @content-desc="Khác"]').exists
        )

    def _scroll_home_to_pinned_header(self, max_swipes: int = 65) -> bool:
        """Return to the pinned-section anchor, regardless of retained scroll.

        Use small central swipes as in the previously PASSed 024E V7. A
        scroll boundary inferred from an unchanged hierarchy is not reliable
        for Flutter CustomScrollView, so never stop for that reason.
        """
        assert self.d.app_current().get("package") == config.APP_PACKAGE
        assert self.driver.is_on_home_screen(), "Not on Smart Note HomeScreen"
        width, height = self.d.window_size()
        x = int(width * .58)
        for n in range(max_swipes + 1):
            if self._is_pinned_section_visible():
                print(f"[SECTION V8] Reached pinned heading after {n} upward swipes")
                return True
            if n == max_swipes:
                break
            # Finger moves DOWN => list moves UP.
            self.d.swipe(x, int(height * .42), x, int(height * .76), steps=20)
            time.sleep(.4)
            if n % 4 == 3:
                assert self.d.app_current().get("package") == config.APP_PACKAGE, (
                    "FAIL-AUTO: Left Smart Note while looking for Pinned header"
                )
                assert self.driver.is_on_home_screen(), (
                    "FAIL-AUTO: Home marker absent while looking for Pinned header"
                )
        return False

    def _assert_card_in_section(self, title: str, expected: str):
        """Verify UI section membership across *successive* Home viewports.

        Requires the Pinned header as the starting anchor. A pinned card must
        precede the 'Khác' header, while a normal card must follow it. Never
        silently PASS a normal card without witnessing the section boundary.
        UI is the oracle for placement; SQLite is used ONLY to distinguish
        the app's intentional no-pinned flat-list layout.
        """
        assert expected in ("pinned", "normal")
        assert self.d.app_current().get("package") == config.APP_PACKAGE
        assert self.driver.is_on_home_screen(), "Not on Smart Note HomeScreen"

        pinned_start = self._scroll_home_to_pinned_header()
        if not pinned_start:
            # When there are no pinned notes the app intentionally renders a
            # flat normal list with no 'Được ghim' or 'Khác' heading.
            pinned_count = sum(
                row["status"] == "pinned" for row in self._db().values()
            )
            assert expected == "normal" and pinned_count == 0, (
                f"Pinned heading not reachable while checking {title!r} "
                f"in {expected} section; pinned DB count={pinned_count}. "
                "FAIL-AUTO / UI not verified."
            )
            card = self._find_note_in_home_by_scrolling(title)
            assert card is not None and card.exists, (
                f"Flat normal-list UI did not show {title!r}"
            )
            assert not self._is_pinned_section_visible(), (
                "Unexpected Pinned heading in flat normal-list layout"
            )
            print(f"[SECTION V8] Flat normal list: card={title!r} visible")
            return

        width, height = self.d.window_size()
        x = int(width * .58)
        others_seen = False
        # Overlapping swipes prevent skipping the section heading while
        # traversing the virtualized Flutter slivers.
        for step in range(65):
            card = self._card(title, scroll=False)
            others = self._first(
                self.d(text="Khác"), self.d(description="Khác"),
                self.d(text="Others"), self.d(description="Others"),
            )
            card_bounds = card.info.get("bounds", {}) if card is not None and card.exists else {}
            others_bounds = others.info.get("bounds", {}) if others is not None and others.exists else {}
            card_y = card_bounds.get("top", -1)
            others_y = others_bounds.get("top", -1)
            card_visible = (
                0 <= card_y < height and card_bounds.get("bottom", -1) > card_y
            )
            others_visible = (
                0 <= others_y < height and others_bounds.get("bottom", -1) > others_y
            )

            if expected == "pinned":
                if card_visible:
                    assert not others_seen, (
                        f"Card {title!r} appeared after 'Khác'; not in Pinned section"
                    )
                    if others_visible:
                        assert card_y < others_y, (
                            f"Card {title!r} (y={card_y}) below 'Khác' (y={others_y})"
                        )
                    heading = self._first(
                        self.d(text="Được ghim"), self.d(description="Được ghim"),
                        self.d(text="Pinned"), self.d(description="Pinned"),
                    )
                    if heading is not None and heading.exists:
                        heading_bottom = heading.info.get("bounds", {}).get("bottom", -1)
                        assert card_y >= heading_bottom - 20, (
                            f"Card {title!r} is above Pinned header on same viewport"
                        )
                    print(f"[SECTION V8] PINNED UI verified at step={step}: {title}")
                    return
                if others_visible:
                    raise AssertionError(
                        f"Reached 'Khác' before seeing pinned card {title!r}. "
                        "Card not verified in Pinned section."
                    )
            else:
                if card_visible:
                    assert others_seen or others_visible, (
                        f"Card {title!r} appeared before 'Khác'; not in normal section"
                    )
                    if others_visible:
                        assert card_y >= others_bounds.get("bottom", 0) - 20, (
                            f"Card {title!r} (y={card_y}) above 'Khác' "
                            f"(bottom={others_bounds.get('bottom')})"
                        )
                    print(f"[SECTION V8] NORMAL UI verified at step={step}: {title}")
                    return

            if others_visible:
                others_seen = True
                if step == 0 or step % 8 == 0:
                    print(f"[SECTION V8] 'Khác' heading seen at step {step}")
            if step % 12 == 0:
                print(f"[SECTION V8] scanning {expected}: step={step}/65, others_seen={others_seen}")

            # Finger moves UP => scroll list DOWN, with viewport overlap.
            self.d.swipe(x, int(height * .74), x, int(height * .37), steps=23)
            time.sleep(.55)
            if step % 4 == 3:
                assert self.d.app_current().get("package") == config.APP_PACKAGE, (
                    "FAIL-AUTO: Left Smart Note during section check"
                )
                assert self.driver.is_on_home_screen(), (
                    "FAIL-AUTO: Home marker absent during section check"
                )

        debug_path = (
            "evidence/fn20/"
            f"debug_section_{expected}_{title}_{datetime.now():%Y%m%d_%H%M%S}.png"
        )
        try:
            print(f"[SECTION V8 DEBUG] Screenshot: {self.driver.capture_evidence(debug_path)}")
            print(f"[SECTION V8 DEBUG] Visible UI texts: {self.driver.get_screen_texts()}")
        except Exception as exc:
            print(f"[SECTION V8 DEBUG] Screenshot unavailable: {exc}")
        raise AssertionError(
            f"FAIL-AUTO: Card {title!r} not found in {expected} section "
            f"after 65 overlapping swipes; others_seen={others_seen}. "
            "No UI PASS can be inferred from SQLite alone."
        )

    def _assert_card_in_pinned_section(self, title: str):
        """Assert title card is rendered in Pinned UI section (scroll-safe)."""
        self._assert_card_in_section(title, "pinned")

    def _assert_card_in_others_section(self, title: str):
        """Assert title card is rendered after 'Khác' heading (scroll-safe)."""
        self._assert_card_in_section(title, "normal")

    # =========================================================================
    # NHÓM 1: MÀN HÌNH SOẠN THẢO (EDITOR) (3 ITEMS)
    # =========================================================================

    def test_tc_bb_024b_d01_editor_pin_note(self):
        """TC-BB-024B (D01): Editor -> mở note thường -> Bấm biểu tượng Pin trên AppBar.

        Expected Result:
        - Ứng dụng tự động lưu trạng thái ghim và quay về Trang chủ.
        - Thẻ ghi chú di chuyển lên phân vùng 'Được ghim'.
        - SQLite ghi nhận status='pinned'.
        """
        tc = "TC-BB-024B_D01"
        marker, folder = self._start(tc)
        title = f"QA_PIN_024B_D01_{marker}"
        content = "Test ghim ghi chu truc tiep tu AppBar man hinh Editor."

        # 1. Tạo ghi chú QA thường
        rid = self._new(title, content)
        self._shot(folder, tc, 1)

        # 2. Mở ghi chú để vào EditorScreen
        self._open_existing_note_with_scroll(title)
        assert self.driver.is_in_editor(), "Expected to enter EditorScreen."
        self._shot(folder, tc, 2)

        # 3. Bấm icon Ghim trên AppBar (note đang normal -> icon push_pin_outlined)
        self._click_editor_pin_button(expect_pinned=False)

        # 4. Kiểm tra ứng dụng tự động pop về HomeScreen
        for _ in range(10):
            if self.driver.is_on_home_screen():
                break
            time.sleep(0.5)
        assert self.driver.is_on_home_screen(), (
            "Expected Editor to automatically pop back to HomeScreen after pinning."
        )

        # 5. Xác minh SQLite status='pinned'
        self._wait_row(rid, "pinned", title, content)

        # 6. Xác minh giao diện: note nằm trong mục 'Được ghim'
        self._assert_card_in_pinned_section(title)
        self._shot(folder, tc, 3)
        print(f"[{tc} PASS] Note successfully pinned from Editor AppBar.")

    def test_tc_bb_024b_d02_editor_unpin_note(self):
        """TC-BB-024B (D02): Editor -> mở note đã ghim -> Bấm biểu tượng Unpin trên AppBar.

        Expected Result:
        - Ứng dụng tự động lưu trạng thái bỏ ghim và quay về Trang chủ.
        - Thẻ ghi chú chuyển về danh sách thường (mục 'Khác').
        - SQLite ghi nhận status='normal'.
        """
        tc = "TC-BB-024B_D02"
        marker, folder = self._start(tc)
        title = f"QA_PIN_024B_D02_{marker}"
        content = "Test bo ghim ghi chu truc tiep tu AppBar man hinh Editor."

        # 1. Tạo ghi chú và ghim trước trên HomeScreen
        rid = self._new(title, content)
        self._pin_note_via_home(title)
        self._wait_row(rid, "pinned", title, content)
        self._shot(folder, tc, 1)

        # 2. Mở ghi chú đã ghim để vào EditorScreen
        self._open_existing_note_with_scroll(title)
        assert self.driver.is_in_editor(), "Expected to enter EditorScreen."
        self._shot(folder, tc, 2)

        # 3. Bấm icon Bỏ ghim trên AppBar (note đang pinned -> icon push_pin)
        self._click_editor_pin_button(expect_pinned=True)

        # 4. Kiểm tra ứng dụng tự động pop về HomeScreen
        for _ in range(10):
            if self.driver.is_on_home_screen():
                break
            time.sleep(0.5)
        assert self.driver.is_on_home_screen(), (
            "Expected Editor to automatically pop back to HomeScreen after unpinning."
        )

        # 5. Xác minh SQLite status='normal'
        self._wait_row(rid, "normal", title, content)

        # 6. Xác minh giao diện: note chuyển về danh sách thường
        self._assert_card_in_others_section(title)
        self._shot(folder, tc, 3)
        print(f"[{tc} PASS] Note successfully unpinned from Editor AppBar.")

    def test_tc_bb_024c_d01_editor_pin_empty_note_validation(self):
        """TC-BB-024C (D01): Tạo note mới để trống -> Bấm biểu tượng Pin trên AppBar.

        Expected Result:
        - Xuất hiện thanh thông báo SnackBar: 'Vui lòng nhập nội dung để có thể ghim ghi chú này'.
        - Ghi chú không bị ghim và không tự thoát màn hình.
        - SQLite không sinh ra ghi chú rác ở trạng thái pinned.
        """
        tc = "TC-BB-024C_D01"
        marker, folder = self._start(tc)
        before_db = self._db()

        # 1. Bấm nút '+' để tạo ghi chú mới
        self.driver.open_note_editor()
        assert self.driver.is_in_editor(), "Expected to enter EditorScreen for new note."
        self._shot(folder, tc, 1)

        # 2. Không nhập Tiêu đề hay Nội dung, nhấn ngay vào biểu tượng Ghim trên AppBar
        self._click_editor_pin_button(expect_pinned=False)

        # 3. Xác minh SnackBar cảnh báo xuất hiện
        snack_msg = self._first(
            self.d(textContains="Vui lòng nhập nội dung để có thể ghim ghi chú này"),
            self.d(descriptionContains="Vui lòng nhập nội dung để có thể ghim ghi chú này"),
            self.d(textContains="Vui lòng nhập nội dung"),
            self.d(descriptionContains="Vui lòng nhập nội dung"),
            self.d(textContains="enter content to pin"),
            self.d(descriptionContains="enter content to pin"),
        )
        assert snack_msg is not None and snack_msg.exists, (
            "Expected SnackBar validation message 'Vui lòng nhập nội dung để có thể ghim ghi chú này' to appear."
        )

        # 4. Xác minh màn hình soạn thảo không bị đóng
        assert self.driver.is_in_editor(), (
            "Editor screen should remain open when attempting to pin an empty note."
        )
        self._shot(folder, tc, 2)

        # 5. Thoát Editor an toàn mà không lưu
        self.d.press("back")
        time.sleep(1.0)
        if self.driver.is_in_editor():
            self.d.press("back")
            time.sleep(1.0)

        assert self.driver.is_on_home_screen(), "Failed to return to HomeScreen."

        # 6. Xác minh SQLite không có ghi chú mới nào được tạo
        after_db = self._db()
        new_active = [
            rid for rid in after_db
            if rid not in before_db and after_db[rid]["status"] in ("normal", "pinned")
        ]
        assert len(new_active) == 0, (
            f"Unexpected notes created in SQLite during empty pin attempt: {new_active}"
        )
        self._shot(folder, tc, 3)
        print(f"[{tc} PASS] Empty note pin restriction validated successfully.")

    # =========================================================================
    # NHÓM 2: THAO TÁC HÀNG LOẠT (BATCH) (4 ITEMS)
    # =========================================================================

    def test_tc_bb_024d_d01_batch_pin_notes(self):
        """TC-BB-024D (D01): HomeScreen -> multi-select 2 note thường -> Bấm nút Pin.

        Expected Result:
        - Cả 2 ghi chú được chọn đồng thời chuyển lên phân vùng 'Được ghim'.
        - Phân vùng 'Được ghim' hiển thị đầy đủ cả 2 ghi chú.
        - SQLite cập nhật status='pinned' cho cả 2 ghi chú.
        """
        tc = "TC-BB-024D_D01"
        marker, folder = self._start(tc)
        title1 = f"QA_PIN_024D_A_{marker}"
        content1 = "Noi dung ghi chu hang loat A de kiem tra Batch Pin."
        title2 = f"QA_PIN_024D_B_{marker}"
        content2 = "Noi dung ghi chu hang loat B de kiem tra Batch Pin."

        # 1. Tạo 2 ghi chú QA thường
        rid1 = self._new(title1, content1)
        rid2 = self._new(title2, content2)
        self._shot(folder, tc, 1)

        # 2. Multi-select: Nhấn giữ note 1, chạm tiếp note 2
        assert self.driver.select_note_by_long_press(title1), (
            f"Failed to long-press note 1 '{title1}'."
        )
        card2 = self._card(title2, scroll=False)
        assert card2 is not None and card2.exists, f"Card 2 '{title2}' not found."
        card2.click()
        time.sleep(0.6)
        self._shot(folder, tc, 2)

        # 3. Bấm icon Ghim/Bỏ ghim hàng loạt trên AppBar
        self._toggle_pin_toolbar()

        # 4. Xác minh SQLite: cả 2 note đều có status='pinned'
        self._wait_row(rid1, "pinned", title1, content1)
        self._wait_row(rid2, "pinned", title2, content2)

        # 5. Xác minh giao diện: cả 2 note đều nằm trong 'Được ghim'
        self._assert_card_in_pinned_section(title1)
        self._assert_card_in_pinned_section(title2)
        self._shot(folder, tc, 3)
        print(f"[{tc} PASS] Batch pin 2 notes verified successfully.")

    def test_tc_bb_024h_d01_mixed_batch_toggle(self):
        """TC-BB-024H (D01): Chọn đồng thời 1 note Pinned + 1 note Normal -> Bấm Pin/Unpin.

        Yêu cầu bắt buộc: Phải kiểm tra cả hai trạng thái đảo chiều độc lập.
        Expected Result:
        - Cả 2 ghi chú đảo trạng thái độc lập:
          + Ghi chú đang ghim chuyển xuống danh sách thường ('Khác').
          + Ghi chú thường chuyển lên mục 'Được ghim'.
        - SQLite: Note 1 chuyển từ pinned -> normal, Note 2 chuyển từ normal -> pinned.
        """
        tc = "TC-BB-024H_D01"
        marker, folder = self._start(tc)
        title_pinned = f"QA_PIN_024H_P_{marker}"
        content_pinned = "Ghi chu ban dau dang duoc ghim."
        title_normal = f"QA_PIN_024H_N_{marker}"
        content_normal = "Ghi chu ban dau dang o danh sach thuong."

        # 1. Tạo 2 ghi chú QA
        rid_p = self._new(title_pinned, content_pinned)
        rid_n = self._new(title_normal, content_normal)

        # 2. Đưa note 1 vào mục 'Được ghim', note 2 giữ nguyên ở danh sách thường
        self._pin_note_via_home(title_pinned)
        self._wait_row(rid_p, "pinned", title_pinned, content_pinned)
        self._wait_row(rid_n, "normal", title_normal, content_normal)
        self._shot(folder, tc, 1)

        # 3. Chọn đồng thời: Long-press note đang ghim, chạm tiếp note thường
        assert self.driver.select_note_by_long_press(title_pinned), (
            f"Failed to long-press pinned note '{title_pinned}'."
        )
        card_normal = self._card(title_normal, scroll=False)
        assert card_normal is not None and card_normal.exists, (
            f"Normal card '{title_normal}' not found for selection."
        )
        card_normal.click()
        time.sleep(0.6)
        self._shot(folder, tc, 2)

        # 4. Bấm Ghim/Bỏ ghim hàng loạt trên AppBar
        self._toggle_pin_toolbar()

        # 5. Xác minh độc lập đảo chiều cả 2 trạng thái trong SQLite:
        # Note ban đầu Pinned -> giờ thành Normal
        self._wait_row(rid_p, "normal", title_pinned, content_pinned)
        # Note ban đầu Normal -> giờ thành Pinned
        self._wait_row(rid_n, "pinned", title_normal, content_normal)

        # 6. Xác minh giao diện:
        # Note 2 nằm trong mục 'Được ghim'
        self._assert_card_in_pinned_section(title_normal)
        # Note 1 nằm trong mục danh sách thường ('Khác')
        self._assert_card_in_others_section(title_pinned)
        self._shot(folder, tc, 3)
        print(f"[{tc} PASS] Independent reversal of mixed batch toggle verified.")

    def test_tc_bb_025d_d01_batch_unpin_notes(self):
        """TC-BB-025D (D01): HomeScreen -> multi-select 2 note ghim -> Bấm nút Pin/Unpin.

        Expected Result:
        - Cả 2 ghi chú được chọn đồng thời chuyển xuống danh sách thường.
        - SQLite cập nhật status='normal' cho cả 2 ghi chú.
        - Tiêu đề 'Được ghim' tự động ẩn đi nếu không còn ghi chú ghim nào khác.
        """
        tc = "TC-BB-025D_D01"
        marker, folder = self._start(tc)
        title1 = f"QA_PIN_025D_A_{marker}"
        content1 = "Noi dung note A de kiem tra Batch Unpin."
        title2 = f"QA_PIN_025D_B_{marker}"
        content2 = "Noi dung note B de kiem tra Batch Unpin."

        # 1. Tạo 2 ghi chú và ghim cả hai
        rid1 = self._new(title1, content1)
        rid2 = self._new(title2, content2)

        assert self.driver.select_note_by_long_press(title1)
        card2 = self._card(title2, scroll=False)
        assert card2 is not None and card2.exists
        card2.click()
        time.sleep(0.5)
        self._toggle_pin_toolbar()

        self._wait_row(rid1, "pinned", title1, content1)
        self._wait_row(rid2, "pinned", title2, content2)
        self._shot(folder, tc, 1)

        # 2. Multi-select cả 2 note đang ghim
        assert self.driver.select_note_by_long_press(title1), (
            f"Failed to select pinned note '{title1}'."
        )
        card2 = self._card(title2, scroll=False)
        assert card2 is not None and card2.exists
        card2.click()
        time.sleep(0.6)
        self._shot(folder, tc, 2)

        # 3. Bấm icon Ghim/Bỏ ghim hàng loạt trên AppBar
        self._toggle_pin_toolbar()

        # 4. Xác minh SQLite: cả 2 note đều trở về status='normal'
        self._wait_row(rid1, "normal", title1, content1)
        self._wait_row(rid2, "normal", title2, content2)

        # 5. Xác minh giao diện: cả 2 note nằm ở danh sách thường
        self._assert_card_in_others_section(title1)
        self._assert_card_in_others_section(title2)
        self._shot(folder, tc, 3)
        print(f"[{tc} PASS] Batch unpin 2 notes verified successfully.")

    def test_tc_bb_025e_d01_unpin_one_of_multiple_pinned(self):
        """TC-BB-025E (D01): Có 2 note ghim -> chỉ chọn bỏ ghim 1 note -> Bấm Pin/Unpin.

        Expected Result:
        - Ghi chú được chọn chuyển xuống danh sách thường.
        - Phân vùng 'Được ghim' vẫn tiếp tục hiển thị cùng với ghi chú đã ghim còn lại.
        - SQLite: Note được chọn có status='normal', Note còn lại vẫn status='pinned'.
        """
        tc = "TC-BB-025E_D01"
        marker, folder = self._start(tc)
        title_unpin = f"QA_PIN_025E_U_{marker}"
        content_unpin = "Ghi chu se duoc bo ghim."
        title_stay = f"QA_PIN_025E_S_{marker}"
        content_stay = "Ghi chu se tiep tuc duoc duy tri ghim."

        # 1. Tạo 2 ghi chú và ghim cả 2
        rid_u = self._new(title_unpin, content_unpin)
        rid_s = self._new(title_stay, content_stay)

        assert self.driver.select_note_by_long_press(title_unpin)
        card_s = self._card(title_stay, scroll=False)
        assert card_s is not None and card_s.exists
        card_s.click()
        time.sleep(0.5)
        self._toggle_pin_toolbar()

        self._wait_row(rid_u, "pinned", title_unpin, content_unpin)
        self._wait_row(rid_s, "pinned", title_stay, content_stay)
        self._shot(folder, tc, 1)

        # 2. Chỉ chọn duy nhất 1 note để bỏ ghim (long-press title_unpin)
        assert self.driver.select_note_by_long_press(title_unpin), (
            f"Failed to select note '{title_unpin}' for unpinning."
        )
        self._shot(folder, tc, 2)

        # 3. Bấm nút Bỏ ghim trên AppBar
        self._toggle_pin_toolbar()

        # 4. Xác minh SQLite:
        # Note chọn -> status='normal'
        self._wait_row(rid_u, "normal", title_unpin, content_unpin)
        # Note còn lại -> vẫn status='pinned'
        self._wait_row(rid_s, "pinned", title_stay, content_stay)

        # 5. Xác minh giao diện:
        # Phân vùng 'Được ghim' vẫn hiển thị và chứa note_stay
        assert self._is_pinned_section_visible(), (
            "Expected 'Được ghim' section header to remain visible for the remaining pinned note."
        )
        self._assert_card_in_pinned_section(title_stay)
        # Note_unpin đã chuyển xuống mục thường ('Khác')
        self._assert_card_in_others_section(title_unpin)
        self._shot(folder, tc, 3)
        print(f"[{tc} PASS] Unpin 1 of 2 pinned notes verified successfully.")

    # =========================================================================
    # NHÓM 3: BỐ CỤC GIAO DIỆN & TOÀN VẸN DỮ LIỆU (3 ITEMS)
    # =========================================================================

    def test_tc_bb_024e_d01_layout_pinned_and_others_sections(self):
        """TC-BB-024E D01: Verify section order across virtualized Home viewports.

        HOME_GUARD_V7: Diagnose app foreground and Home marker separately;
        only collapse when SystemUI really has foreground. Never identify a
        shade by generic notification text or a missing Home marker.
        """
        tc = "TC-BB-024E_D01"
        marker, folder = self._start(tc)
        # Optional read-only retest of this test's own notes from an earlier
        # run. This avoids creating more QA notes during locator debugging.
        reuse = os.getenv("FN20_LAYOUT_REUSE_MARKER", "").strip().lower()
        if reuse:
            assert len(reuse) == 8 and all(ch in "0123456789abcdef" for ch in reuse), (
                "Invalid FN20_LAYOUT_REUSE_MARKER: expected 8 hex characters"
            )
        data_marker = reuse or marker
        title_p = f"QA_PIN_024E_P_{data_marker}"
        content_p = "Noi dung note ghim phan vung tren."
        title_n = f"QA_PIN_024E_N_{data_marker}"
        content_n = "Noi dung note thuong phan vung duoi."

        if reuse:
            rows = self._db()
            pinned_ids = [rid for rid, r in rows.items() if r["title"] == title_p]
            normal_ids = [rid for rid, r in rows.items() if r["title"] == title_n]
            assert len(pinned_ids) == 1 and len(normal_ids) == 1, (
                "Cannot uniquely reuse old 024E QA dataset. No data was modified. "
                f"Pinned IDs={pinned_ids}; normal IDs={normal_ids}"
            )
            rid_p, rid_n = pinned_ids[0], normal_ids[0]
            self._wait_row(rid_p, "pinned", title_p, content_p)
            self._wait_row(rid_n, "normal", title_n, content_n)
            print(f"[LAYOUT V7] Reusing existing 024E data marker={reuse} "
                  "(read-only: no new notes, no pin/unpin)")
        else:
            rid_p = self._new(title_p, content_p)
            rid_n = self._new(title_n, content_n)
            self._pin_note_via_home(title_p)
            self._wait_row(rid_p, "pinned", title_p, content_p)
            self._wait_row(rid_n, "normal", title_n, content_n)

        width, height = self.d.window_size()
        x = int(width * 0.58)  # Inner list area, not the right-hand Samsung Edge Panel
        recoveries = 0

        def ensure_actual_home(where):
            """Guard UI with explicit diagnostics, never assume a failed Home
            locator is an Android notification shade.

            - Smart Note foreground + Home locator missing => fail with evidence;
              do NOT collapse/launch or mutate navigation state.
            - SystemUI foreground => attempt a bounded, reversible collapse.
            - Another foreground app => fail; no speculative auto-navigation.
            """
            nonlocal recoveries
            current = self.d.app_current()
            foreground = current.get("package")
            is_home = self.driver.is_on_home_screen()
            if foreground == config.APP_PACKAGE and is_home:
                return

            print(f"[LAYOUT V7] HOME GUARD FAILED at {where}: "
                  f"foreground={foreground!r}, is_home={is_home}, "
                  f"app_current={current}")
            self._shot(folder, tc, 90 + min(recoveries, 8))
            print(f"[LAYOUT V7] Visible texts on failed guard: "
                  f"{self.driver.get_screen_texts()}")

            if foreground == config.APP_PACKAGE:
                raise AssertionError(
                    f"FAIL-AUTO: Smart Note is foreground at {where} but "
                    f"is_on_home_screen() is False. Inspect screenshot "
                    "and Home semantics; NOT assuming notification shade."
                )

            if foreground != "com.android.systemui":
                raise AssertionError(
                    f"FAIL-AUTO: unexpected foreground package "
                    f"{foreground!r} at {where}, not Smart Note/SystemUI. "
                    "No automatic relaunch to avoid changing test position."
                )

            if recoveries >= 3:
                raise AssertionError(
                    f"FAIL-AUTO: SystemUI overlay recurred after "
                    f"{recoveries} successful recoveries; stop safely."
                )

            recoveries += 1
            result = subprocess.run(
                ["adb", "-s", self.driver.serial,
                 "shell", "cmd", "statusbar", "collapse"],
                capture_output=True, text=True, timeout=12,
            )
            if result.returncode != 0:
                raise AssertionError(
                    f"FAIL-AUTO: statusbar collapse command failed: "
                    f"{result.stderr.strip()}"
                )

            time.sleep(0.8)
            current = self.d.app_current()
            foreground = current.get("package")
            is_home = self.driver.is_on_home_screen()
            print(f"[LAYOUT V7] SystemUI recovery #{recoveries} at {where}: "
                  f"foreground={foreground!r}, is_home={is_home}")
            if foreground == config.APP_PACKAGE and is_home:
                return
            self._shot(folder, tc, 90 + min(recoveries, 8))
            raise AssertionError(
                f"FAIL-AUTO: after collapsing SystemUI, screen still not "
                f"Smart Note Home at {where}: "
                f"foreground={foreground!r}, is_home={is_home}."
            )

        def viewport_fingerprint():
            img = self.d.screenshot()
            return img.crop((
                int(width * .10), int(height * .26),
                int(width * .90), int(height * .80)
            )).convert("L").resize((48, 48)).tobytes()

        ensure_actual_home("after setup")
        # First locate the actual start of the pinned section, regardless of
        # the scroll position retained from other tests.
        for attempt in range(45):
            if self._is_pinned_section_visible():
                print(f"[LAYOUT V7] Pinned header reached after {attempt} up swipes")
                break
            self.d.swipe(x, int(height * .42), x, int(height * .76), steps=20)
            time.sleep(.4)
            ensure_actual_home(f"up swipe {attempt + 1}")
        else:
            self._shot(folder, tc, 1)
            raise AssertionError(
                "FAIL-AUTO: Could not navigate to Pinned header; "
                "expected pinned note exists in SQLite"
            )

        order = ("pinned_header", "pinned_note", "others_header", "normal_note")
        seen = {}
        previous = viewport_fingerprint()
        stationary = 0

        for step in range(60):
            ensure_actual_home(f"scan step {step}")
            elements = {
                "pinned_header": self._first(
                    self.d(text="Được ghim"), self.d(description="Được ghim"),
                    self.d(text="Pinned"), self.d(description="Pinned")),
                "pinned_note": self._card(title_p, scroll=False),
                "others_header": self._first(
                    self.d(text="Khác"), self.d(description="Khác"),
                    self.d(text="Others"), self.d(description="Others")),
                "normal_note": self._card(title_n, scroll=False),
            }
            for label in order:
                obj = elements[label]
                if label in seen or obj is None or not obj.exists:
                    continue
                bounds = obj.info.get("bounds", {})
                top, bottom = bounds.get("top", -1), bounds.get("bottom", -1)
                if 0 <= top < height and bottom > top:
                    seen[label] = (step, top)
                    print(f"[LAYOUT V6] {label}: step={step}, y={top}")
                    if label == "pinned_header":
                        self._shot(folder, tc, 1)
                    if label == "others_header":
                        self._shot(folder, tc, 2)

            if len(seen) == 4:
                break
            if step % 5 == 0:
                print(f"[LAYOUT V7] Scan {step}/60; found={list(seen)}")

            # Swipe UP (finger from lower middle to upper middle) to scroll DOWN
            # the list, with overlap so sliver headers aren't skipped.
            self.d.swipe(x, int(height * .74), x, int(height * .37), steps=23)
            time.sleep(.60)  # Let Flutter lazy-loading / rebuild settle
            ensure_actual_home(f"down swipe {step + 1}")

            current_image = viewport_fingerprint()
            stationary = stationary + 1 if current_image == previous else 0
            previous = current_image
            # Only declare a list boundary after a LONG stationary run and
            # while the app is confirmed foreground, not the notification shade.
            if stationary >= 6:
                print(f"[LAYOUT V7] 6 unchanged actual-app viewports at step {step}")
                break

        self._shot(folder, tc, 3)
        missing = [name for name in order if name not in seen]
        if missing:
            current = self.d.app_current()
            print(f"[LAYOUT V7 DEBUG] Missing={missing}; seen={seen}; app={current}")
            print(f"[LAYOUT V7 DEBUG] UI texts={self.driver.get_screen_texts()}")
            raise AssertionError(
                f"Layout not verified: missing {missing}. "
                "Review UI evidence; do not classify as app defect until confirmed."
            )

        actual_order = tuple(sorted(seen, key=seen.get))
        assert actual_order == order, (
            f"UI section order incorrect: actual={actual_order}; "
            f"expected={order}; positions={seen}"
        )
        print(f"[{tc} PASS] Verified Home UI order {actual_order}; {seen}")

    def test_tc_bb_024f_d01_data_integrity_pin_unpin_cycle(self):
        """TC-BB-024F (D01): Note có Title & Content -> Pin -> kiểm tra -> Unpin -> kiểm tra.

        Expected Result:
        - Tiêu đề và nội dung vẫn hiển thị đúng như trước khi Pin/Unpin, không bị mất hoặc thay đổi.
        - SQLite bảo toàn toàn vẹn dữ liệu qua toàn bộ chu kỳ.
        """
        tc = "TC-BB-024F_D01"
        marker, folder = self._start(tc)
        title = f"QA_PIN_024F_{marker}"
        content = "Dong 1: Toan ven du lieu khi Pin va Unpin.\nDong 2: Noi dung chi tiet khong bi mat mat ky tu."

        # 1. Tạo ghi chú QA hoàn chỉnh
        rid = self._new(title, content)
        self._shot(folder, tc, 1)

        # 2. Ghim ghi chú từ Home
        self._pin_note_via_home(title)
        self._wait_row(rid, "pinned", title, content)

        # 3. Mở ghi chú kiểm tra Tiêu đề và Nội dung trong EditorScreen
        self._open_existing_note_with_scroll(title)
        assert self.driver.is_in_editor(), "Expected to open EditorScreen."

        title_el = self.driver.get_title_field()
        if title_el is not None:
            actual_title = title_el.get_text() or title_el.info.get("text", "")
            if actual_title:
                assert title in actual_title or actual_title in title

        screen_texts = self.driver.get_screen_texts()
        assert any("Toan ven du lieu" in t for t in screen_texts) or "Toan ven du lieu" in self.d.dump_hierarchy(), (
            "Content verification failed in EditorScreen while pinned."
        )
        self._shot(folder, tc, 2)

        # Thoát Editor về Home
        self.driver.save_and_exit_editor()
        self.driver.ensure_home_screen()

        # 4. Bỏ ghim ghi chú từ Home
        self._unpin_note_via_home(title)
        self._wait_row(rid, "normal", title, content)

        # 5. Mở lại ghi chú kiểm tra Tiêu đề và Nội dung lần 2
        self._open_existing_note_with_scroll(title)
        assert self.driver.is_in_editor(), "Expected to open EditorScreen after unpin."

        screen_texts2 = self.driver.get_screen_texts()
        assert any("Toan ven du lieu" in t for t in screen_texts2) or "Toan ven du lieu" in self.d.dump_hierarchy(), (
            "Content verification failed in EditorScreen after unpinning."
        )
        self._shot(folder, tc, 3)

        self.driver.save_and_exit_editor()
        self.driver.ensure_home_screen()
        print(f"[{tc} PASS] Title and content data integrity verified across Pin/Unpin cycle.")

    def test_tc_bb_024g_d01_all_notes_pinned_layout(self):
        """TC-BB-024G D01: all active notes of *this login* are pinned.

        QA_ACCOUNT_SCOPED_V9:
        - No pm clear / account switching / bulk pin / cleanup of existing notes.
        - Require visibly empty Home at test start.
        - Create exactly 3 QA notes and identify the current owner from their
          persisted SQLite user_id. Ignore records belonging to other users.
        - Stop if any unexpected active note exists for this owner.
        - Verify all 3 card titles and absence of 'Khác' over the entire list,
          not just the current viewport. Evidence and JUnit on PASS / failure.
        """
        tc = "TC-BB-024G_D01"
        marker, folder = self._start(tc)

        def owned_db():
            """Read local SQLite including user_id; never modify app storage."""
            proc = subprocess.run(
                ["adb", "-s", self.driver.serial, "exec-out", "run-as",
                 config.APP_PACKAGE, "cat", "databases/smart_note.db"],
                capture_output=True, timeout=25,
            )
            assert proc.returncode == 0 and proc.stdout, (
                "Cannot read SQLite for owner-scoped validation: "
                + proc.stderr.decode(errors="replace")
            )
            conn = sqlite3.connect(":memory:")
            try:
                conn.deserialize(proc.stdout)
                columns = {x[1] for x in conn.execute("PRAGMA table_info(notes)")}
                assert "user_id" in columns, (
                    "DB schema lacks user_id; cannot safely isolate QA account"
                )
                rows = conn.execute(
                    "SELECT id, user_id, title, status FROM notes"
                ).fetchall()
                return {rid: {"user_id": owner, "title": title, "status": status}
                        for rid, owner, title, status in rows}
            finally:
                conn.close()

        def assert_home(where):
            actual = self.d.app_current()
            assert actual.get("package") == config.APP_PACKAGE, (
                f"FAIL-AUTO: Left Smart Note at {where}: {actual}"
            )
            assert self.driver.is_on_home_screen(), (
                f"FAIL-AUTO: Home not recognized at {where}; "
                "stop rather than trusting UI absence"
            )

        def screen_empty():
            return self._first(
                self.d(textContains="Chưa có ghi chú nào"),
                self.d(descriptionContains="Chưa có ghi chú nào"),
                self.d(textContains="No notes yet"),
                self.d(descriptionContains="No notes yet"),
            ) is not None

        # UI-only precondition, while account UID is not yet known. We also
        # verify existing SQLite records for the new note's UID before pinning.
        assert_home("initial Home")
        for _ in range(12):
            if screen_empty():
                break
            time.sleep(.5)
        if not screen_empty():
            self._shot(folder, tc, 90)
            pytest.skip(
                "BLOCKED: Current QA account's Home is not visibly empty. "
                "No existing notes were changed; do not reset app data."
            )
        before = owned_db()
        self._shot(folder, tc, 1)
        print(f"[024G V9] Home empty; SQLite has {len(before)} rows "
              "from all accounts combined (not treated as current account)")

        titles = [f"QA_PIN_024G_{marker}_{i}" for i in range(1, 4)]
        contents = [f"QA 024G all-pinned note {i}" for i in range(1, 4)]
        created = []
        owner = None

        for title, content in zip(titles, contents):
            rid = self._new(title, content)
            rows = owned_db()
            assert rid in rows, f"New QA note {rid} not found in owner-scoped DB"
            new_owner = rows[rid]["user_id"]
            assert new_owner, "New QA note has empty user_id; unsafe to continue"
            if owner is None:
                owner = new_owner
                prior_active = [key for key, row in before.items()
                                if row["user_id"] == owner
                                and row["status"] in ("normal", "pinned")]
                if prior_active:
                    pytest.skip(
                        "BLOCKED: Account had pre-existing active notes despite "
                        "an empty Home. Created one QA note but did not pin or "
                        f"change any existing note; count={len(prior_active)}."
                    )
            assert new_owner == owner, (
                "Firebase account/owner changed during the test; stop safely"
            )
            created.append(rid)
            active_now = {key for key, row in rows.items()
                          if row["user_id"] == owner
                          and row["status"] in ("normal", "pinned")}
            assert active_now == set(created), (
                "Unexpected active notes appeared in this account before Pin. "
                f"expected QA IDs={created}, actual active IDs={sorted(active_now)}. "
                "Stopping to avoid changing unrelated notes."
            )
            self._wait_row(rid, "normal", title, content)
            print(f"[024G V9] Created QA-owned note {len(created)}/3; id={rid}")

        self._shot(folder, tc, 2)

        # Toggle only exact unique QA titles. Never mass-pin existing notes.
        for title, content, rid in zip(titles, contents, created):
            rows = owned_db()
            active_now = {key for key, row in rows.items()
                          if row["user_id"] == owner
                          and row["status"] in ("normal", "pinned")}
            assert active_now == set(created), (
                "Unexpected notes appeared before Pin; refusing to proceed"
            )
            assert rows[rid]["status"] == "normal", (
                f"QA note {title} no longer normal before Pin"
            )
            self._pin_note_via_home(title)
            self._wait_row(rid, "pinned", title, content)
            print(f"[024G V9] Pinned {title}")

        after = owned_db()
        active_after = {key: row for key, row in after.items()
                        if row["user_id"] == owner
                        and row["status"] in ("normal", "pinned")}
        assert set(active_after) == set(created), (
            f"Account must have exactly 3 active QA notes, found {list(active_after)}"
        )
        assert all(row["status"] == "pinned" for row in active_after.values()), (
            f"Not all QA account notes are pinned: {active_after}"
        )
        # Detect changes to pre-existing rows, including other accounts.
        modified_old = [rid for rid, old in before.items()
                        if rid not in after or after[rid]["status"] != old["status"]]
        assert not modified_old, (
            "Unexpected state change to pre-existing notes. "
            f"IDs={modified_old}. No automatic cleanup attempted."
        )
        print("[024G V9] SQLite: exactly 3/3 pinned for this account; "
              "old account rows ignored for count and unchanged")

        assert_home("after pinning")
        assert self._scroll_home_to_pinned_header(max_swipes=35), (
            "FAIL-AUTO: Pinned heading not reachable after 3 notes were pinned"
        )
        self._shot(folder, tc, 3)

        width, height = self.d.window_size()
        x = int(width * .58)

        def viewport_fingerprint():
            # Crop away status bar / nav bar clocks and overlay text.
            im = self.d.screenshot()
            return im.crop((int(width * .12), int(height * .25),
                            int(width * .88), int(height * .80))) \
                     .convert("L").resize((64, 64)).tobytes()

        seen_cards = set()
        stationary = 0
        reached_bottom = False
        for step in range(24):
            assert_home(f"viewport {step}")
            # Assert absence in EVERY scanned viewport (not one screenshot).
            assert not self._is_others_section_visible(), (
                f"APP / UI FAIL: 'Khác' was visible at viewport {step} "
                "even though current account has no normal notes"
            )
            for title in titles:
                card = self._card(title, scroll=False)
                if card is None or not card.exists:
                    continue
                b = card.info.get("bounds", {})
                if 0 <= b.get("top", -1) < height and b.get("bottom", -1) > b["top"]:
                    seen_cards.add(title)
            if step % 3 == 0:
                print(f"[024G V9] UI step={step}; seen={len(seen_cards)}/3; "
                      f"stable={stationary}")
            before_image = viewport_fingerprint()
            self.d.swipe(x, int(height * .74), x, int(height * .37), steps=23)
            time.sleep(.65)
            assert_home(f"after swipe {step}")
            after_image = viewport_fingerprint()
            stationary = stationary + 1 if after_image == before_image else 0
            if stationary >= 3:
                reached_bottom = True
                print(f"[024G V9] Bottom confirmed after {step + 1} swipes")
                break

        self._shot(folder, tc, 4)
        assert reached_bottom, (
            "FAIL-AUTO: Could not establish end of Home list in 24 swipes; "
            "cannot prove 'Khác' absent throughout the whole list"
        )
        assert seen_cards == set(titles), (
            "FAIL-AUTO: Not all three QA cards were seen in Pinned UI section: "
            f"missing={set(titles) - seen_cards}"
        )
        print(f"[{tc} PASS] All 3 account-owned notes pinned; "
              "Pinned section present, Others absent across full UI list.")

    def test_tc_bb_025b_d01_pinned_persistence_restart(self):
        """TC-BB-025B (D01): Có note đã ghim -> Force-stop app -> Mở lại app.

        Expected Result:
        - Ứng dụng khởi động lại bình thường.
        - Ghi chú đã ghim vẫn nằm nguyên vẹn trong phân vùng 'Được ghim', trạng thái ghim không bị mất.
        - SQLite duy trì status='pinned'.
        """
        tc = "TC-BB-025B_D01"
        marker, folder = self._start(tc)
        reuse = os.getenv("FN20_025B_REUSE_MARKER", "").strip().lower()
        if reuse:
            assert len(reuse) == 8 and all(c in "0123456789abcdef" for c in reuse), (
                "Invalid FN20_025B_REUSE_MARKER: expected 8 hex chars"
            )
        data_marker = reuse or marker
        title = f"QA_PIN_025B_{data_marker}"
        content = "Kiem tra tinh ben vung cua trang thai ghim sau app restart."

        # 1. Create/pin once; for a retry, reuse ONLY the exact QA note
        # previously created by TC-BB-025B. Never create a duplicate.
        if reuse:
            candidates = [(rid, row) for rid, row in self._db().items()
                          if row["title"] == title]
            assert len(candidates) == 1, (
                f"Cannot uniquely reuse existing 025B note {title!r}: "
                f"found {len(candidates)}. No data was changed."
            )
            rid = candidates[0][0]
            self._wait_row(rid, "pinned", title, content)
            print(f"[025B V8] Reusing QA note {title} | SQLite ID={rid}; "
                  "no new note, no pin toggle")
        else:
            rid = self._new(title, content)
            self._pin_note_via_home(title)
            self._wait_row(rid, "pinned", title, content)
        self._assert_card_in_pinned_section(title)
        self._shot(folder, tc, 1)

        # 2. Khởi động lại ứng dụng (force-stop -> reopen)
        self._restart()
        self._shot(folder, tc, 2)

        # 3. Xác minh sau restart:
        # SQLite status vẫn là 'pinned'
        self._wait_row(rid, "pinned", title, content)
        # Giao diện: vẫn hiển thị mục 'Được ghim' và note nằm trong đó
        self._assert_card_in_pinned_section(title)
        self._shot(folder, tc, 3)
        print(f"[{tc} PASS] Pinned persistence verified after app restart.")

    def test_tc_bb_025c_d01_pinned_note_edit_preserves_pin(self):
        """TC-BB-025C (D01): Mở note đã ghim -> Chỉnh sửa nội dung -> Back về Home.

        Expected Result:
        - Ghi chú cập nhật nội dung mới.
        - Ghi chú vẫn tiếp tục nằm trong phân vùng 'Được ghim', không bị rớt xuống danh sách thường.
        - SQLite cập nhật nội dung mới và duy trì status='pinned'.
        """
        tc = "TC-BB-025C_D01"
        marker, folder = self._start(tc)
        title = f"QA_PIN_025C_{marker}"
        original_content = "Noi dung goc ban dau cua note ghim."
        append_content = " [DA CHINH SUA NOI DUNG BO SUNG]"

        # 1. Tạo note và ghim
        rid = self._new(title, original_content)
        self._pin_note_via_home(title)
        self._wait_row(rid, "pinned", title, original_content)
        self._shot(folder, tc, 1)

        # 2. Mở note đã ghim trong EditorScreen
        self._open_existing_note_with_scroll(title)
        assert self.driver.is_in_editor(), "Expected to open EditorScreen."

        # 3. Chỉnh sửa thêm nội dung văn bản
        self.driver.input_content(append_content)
        self._shot(folder, tc, 2)

        # 4. Bấm Back trên AppBar để lưu và thoát về HomeScreen
        self.driver.save_and_exit_editor()
        self.driver.ensure_home_screen()

        # 5. Xác minh SQLite: status='pinned' và nội dung đã cập nhật
        # Wait for the edit to be durably stored while status remains pinned.
        updated_row = self._wait_row(rid, "pinned", title, append_content.strip(), timeout=35)
        plain_updated = self._plain(updated_row["content"])
        assert "DA CHINH SUA NOI DUNG" in plain_updated or append_content.strip() in plain_updated, (
            f"Content in SQLite was not updated: '{plain_updated}'"
        )

        # 6. Xác minh giao diện: note vẫn nằm trong phân vùng 'Được ghim'
        self._assert_card_in_pinned_section(title)
        self._shot(folder, tc, 3)
        print(f"[{tc} PASS] Pinned note maintains pinned status after editing content.")

    def test_tc_bb_025f_d01_unpinned_persistence_restart(self):
        """TC-BB-025F (D01): Bỏ ghim note -> Force-stop app -> Mở lại app.

        Expected Result:
        - Sau khi khởi động lại, ghi chú vẫn duy trì ở danh sách thường; không bị tái kích hoạt trạng thái ghim.
        - SQLite duy trì status='normal'.
        """
        tc = "TC-BB-025F_D01"
        marker, folder = self._start(tc)
        title = f"QA_PIN_025F_{marker}"
        content = "Kiem tra tinh ben vung cua trang thai bo ghim sau restart."

        # 1. Tạo note, ghim, rồi bỏ ghim về normal
        rid = self._new(title, content)
        self._pin_note_via_home(title)
        self._wait_row(rid, "pinned", title, content)

        self._unpin_note_via_home(title)
        self._wait_row(rid, "normal", title, content)
        self._shot(folder, tc, 1)

        # 2. Khởi động lại ứng dụng
        self._restart()
        self._shot(folder, tc, 2)

        # 3. Xác minh sau restart:
        # SQLite status vẫn là 'normal'
        self._wait_row(rid, "normal", title, content)
        # Giao diện: note nằm ở danh sách thường (mục 'Khác' hoặc flat list)
        self._assert_card_in_others_section(title)
        self._shot(folder, tc, 3)
        print(f"[{tc} PASS] Unpinned persistence verified after app restart.")


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
