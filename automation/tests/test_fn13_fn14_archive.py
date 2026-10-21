
# -*- coding: utf-8 -*-
"""UI Automation Phase 3: FN-13 Archive / FN-14 Unarchive.

5 test cases:
- TC-BB-040 D01: Archive single note
- TC-BB-040B D01: Unarchive single note
- TC-BB-EXT-008 D01: Archive isolation
- TC-BB-EXT-006 D01: Archive persistence
- TC-BB-EXT-007 D01: Unarchive/Archive without duplicates

Framework: pytest + uiautomator2 + ADB + SQLite Oracle
Device: Samsung Galaxy S21 FE 5G, Android 14

Safety: No app reset, no deletion of existing notes.
"""

import json
import sqlite3
import subprocess
import time
import uuid
from datetime import datetime

from automation import config
from automation.core.device import SmartNoteDriver
from automation.core.qa_note_helper import QANoteHelper


class TestFN13FN14Archive:

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

    # ==========================================================
    # COMMON HELPERS
    # ==========================================================

    def _first(self, *selectors):
        for item in selectors:
            if item.exists:
                return item
        return None


    def _start(self, tc):
        marker = uuid.uuid4().hex[:10]
        folder = (
            f"evidence/fn13_14/automation_"
            f"{datetime.now():%Y%m%d_%H%M%S_%f}_{marker}/{tc}"
        )

        print(f"\n[START] {tc} | marker={marker}")

        # Open app without pressing Back repeatedly.
        self.driver.ensure_device_ready()
        self.driver.launch_app()
        time.sleep(1.0)

        current = self.d.app_current()
        assert current.get("package") == config.APP_PACKAGE, (
            f"Smart Note App not in foreground: {current}"
        )

        # Previous test may finish on ArchiveScreen.
        if not self.driver.is_on_home_screen():
            print(
                "[SETUP] Not on HomeScreen. "
                "Navigating through MainDrawer..."
            )

            # Use the existing safe navigation helper.
            self._goto("home", folder)

        # Verify correct precondition before creating QA notes.
        assert self.driver.is_on_home_screen(), (
            f"Cannot return to HomeScreen before {tc}"
        )

        print("[SETUP PASS] HomeScreen ready")

        return marker, folder


    def _shot(self, folder, tc, number):
        path = f"{folder}/{tc}_{number:02d}.png"
        self.driver.capture_evidence(path)
        print(f"[EVIDENCE] {path}")

    def _db(self):
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
            "Cannot read SQLite: "
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
    def _plain(raw):
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

        return (raw or "").strip()

    def _wait_row(self, rid, expected, title, content, timeout=25):
        end = time.monotonic() + timeout
        rows = {}

        while time.monotonic() < end:
            rows = self._db()
            row = rows.get(rid)

            if row and row["status"] == expected:
                assert row["title"] == title
                assert self._plain(row["content"]) == content

                count = sum(
                    r["title"] == title for r in rows.values()
                )
                assert count == 1, (
                    f"Duplicate QA note detected: {title}"
                )

                return row

            time.sleep(0.5)

        raise AssertionError(
            f"QA note {rid} did not reach status={expected}; "
            f"last row={rows.get(rid)}"
        )

    def _new(self, title, content):
        """Create a unique QA note and resolve its SQLite ID."""
        self.driver.ensure_home_screen()
        before = set(self._db())

        assert QANoteHelper.create_test_note(
            self.driver,
            title,
            content,
            poll_timeout=8.0,
        )

        rows = self._db()

        ids = [
            rid
            for rid, row in rows.items()
            if rid not in before
            and row["title"] == title
            and row["status"] == "normal"
        ]

        assert len(ids) == 1, (
            f"Cannot identify exactly one new QA note: {title}"
        )

        rid = ids[0]
        self._wait_row(rid, "normal", title, content)

        print(f"[QA CREATED] {title} | ID={rid}")
        return rid

    def _card(self, title, scroll=False):
        """Locate QA note by its unique title, never by list index."""
        width, height = self.d.window_size()

        attempts = 11 if scroll else 1

        for attempt in range(attempts):
            card = self._first(
                self.d(descriptionContains=title),
                self.d(textContains=title),
            )

            if card is not None:
                return card

            if scroll and attempt < attempts - 1:
                self.d.swipe(
                    int(width * 0.70),
                    int(height * 0.76),
                    int(width * 0.70),
                    int(height * 0.33),
                    steps=18,
                )
                time.sleep(0.4)

        return None

    def _visible(self, title, screen):
        assert self._card(title, scroll=True) is not None, (
            f"Note {title} not visible on {screen}"
        )

    def _absent(self, title, screen):
        assert self._card(title) is None, (
            f"Note {title} unexpectedly visible on {screen}"
        )

    # ==========================================================
    # SAFE NAVIGATION: HOME <-> ARCHIVE
    # ==========================================================

    def _goto(self, target, folder):
        """Navigate using the verified Drawer, never edge swipe."""

        labels = {
            "archive": ("Lưu trữ", "Archive"),
            "home": ("Ghi chú", "Notes"),
        }

        assert target in labels

        current = self.d.app_current()

        assert current.get("package") == config.APP_PACKAGE, (
            f"App is not in foreground: {current}"
        )

        # Verified menu location on Samsung Galaxy S21 FE.
        # Do not swipe from x=10: Android may interpret it as Back.
        self.d.click(75, 170)
        time.sleep(0.9)

        drawer_open = any((
            self.d(text="Smart Note").exists,
            self.d(descriptionContains="Smart Note").exists,
            self.d(text="Nhắc nhở").exists,
            self.d(text="Reminders").exists,
            self.d(text="Tạo nhãn mới").exists,
            self.d(text="Create new label").exists,
        ))

        if not drawer_open:
            self._shot(folder, "DRAWER_NOT_OPEN", 1)
            print("[DRAWER DEBUG]", self.driver.get_screen_texts())

            raise AssertionError(
                "Drawer not confirmed open. "
                "Stopped safely without edge swipe."
            )

        width, height = self.d.window_size()
        drawer_x = int(width * 0.23)

        label_vi, label_en = labels[target]
        item = None

        for attempt in range(10):
            item = self._first(
                self.d(text=label_vi),
                self.d(description=label_vi),
                self.d(text=label_en),
                self.d(description=label_en),
                self.d(descriptionContains=label_vi),
                self.d(descriptionContains=label_en),
            )

            if item is not None:
                print(
                    f"[DRAWER] Found {target} "
                    f"at attempt {attempt}"
                )
                break

            # Archive is below user labels.
            # Home is at the top of the Drawer.
            if target == "archive":
                y_from = int(height * 0.76)
                y_to = int(height * 0.29)
            else:
                y_from = int(height * 0.29)
                y_to = int(height * 0.76)

            self.d.swipe(
                drawer_x, y_from,
                drawer_x, y_to,
                steps=20,
            )
            time.sleep(0.5)

            assert (
                self.d.app_current().get("package")
                == config.APP_PACKAGE
            ), "App left foreground during Drawer scrolling"

        if item is None:
            self._shot(
                folder,
                f"DRAWER_{target.upper()}_MISSING",
                1,
            )
            print("[DRAWER DEBUG]", self.driver.get_screen_texts())

            raise AssertionError(
                f"Cannot find {target} in verified Drawer"
            )

        item.click()
        time.sleep(1.2)

        assert (
            self.d.app_current().get("package")
            == config.APP_PACKAGE
        ), "App left foreground during navigation"

        print(f"[NAVIGATE] {target}")

    # ==========================================================
    # ARCHIVE / UNARCHIVE ACTIONS
    # ==========================================================

    def _archive(self, rid, title, content):
        """Archive exactly one newly created QA note."""

        self.driver.ensure_home_screen()
        self._wait_row(rid, "normal", title, content)

        card = self._card(title, scroll=True)

        assert card is not None, (
            f"QA target not found on HomeScreen: {title}"
        )

        card.long_click(duration=1.2)
        time.sleep(0.7)

        archive_button = self._first(
            self.d(description="Lưu trữ"),
            self.d(description="Archive"),
            self.d(descriptionContains="Lưu trữ"),
            self.d(descriptionContains="Archive"),
        )

        assert archive_button is not None, (
            "Archive action not found in Selection AppBar"
        )

        archive_button.click()

        self._wait_row(rid, "archived", title, content)
        self._absent(title, "HomeScreen")

        print(f"[ARCHIVED] {title} | ID={rid}")


    def _unarchive(self, rid, title, content):
        """Unarchive QA note via ArchiveScreen BottomSheet."""

        self._wait_row(rid, "archived", title, content)

        card = self._card(title, scroll=True)
        assert card is not None, (
            f"QA note not found in Archive: {title}"
        )

        print(f"[UNARCHIVE] Opening BottomSheet for {title}")
        card.click()
        time.sleep(1.0)

        # Flutter may expose ListTile title/subtitle as
        # combined content-desc instead of separate text.
        button = None

        for _ in range(8):
            button = self._first(
                self.d(text="Bỏ lưu trữ"),
                self.d(textContains="Bỏ lưu trữ"),
                self.d(descriptionContains="Bỏ lưu trữ"),
                self.d(text="Unarchive"),
                self.d(descriptionContains="Unarchive"),
                self.d(textContains="Khôi phục về Trang chủ"),
                self.d(descriptionContains="Khôi phục về Trang chủ"),
                self.d(textContains="Restore to Home"),
                self.d(descriptionContains="Restore to Home"),
            )

            if button is not None:
                break

            time.sleep(0.5)

        if button is None:
            stamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S_%f"
            )
            debug_path = (
                "evidence/fn13_14/"
                f"unarchive_bottomsheet_debug_{stamp}.png"
            )

            self.driver.capture_evidence(debug_path)

            print("[UNARCHIVE DEBUG] Current app:")
            print(self.d.app_current())
            print("[UNARCHIVE DEBUG] Visible UI:")
            print(self.driver.get_screen_texts())
            print("[UNARCHIVE DEBUG] Screenshot:", debug_path)

            raise AssertionError(
                "Unarchive BottomSheet action not found. "
                "See debug screenshot and visible UI texts."
            )

        print("[UNARCHIVE] BottomSheet action found")
        button.click()

        self._wait_row(rid, "normal", title, content)
        self._absent(title, "ArchiveScreen")

        print(f"[UNARCHIVED] {title} | ID={rid}")


    def _restart(self):
        """Force-stop and relaunch without clearing app data."""

        result = subprocess.run(
            [
                "adb", "-s", self.driver.serial,
                "shell", "am", "force-stop",
                config.APP_PACKAGE,
            ],
            capture_output=True,
            timeout=20,
        )

        assert result.returncode == 0, (
            "Force-stop failed: "
            + result.stderr.decode(errors="replace")
        )

        self.driver.launch_app()
        self.driver.ensure_home_screen()

        print("[RESTART] App reopened; data preserved")

    # ==========================================================
    # FN-13 / TC-BB-040 D01
    # ==========================================================

    def test_tc_bb_040_d01_archive_single_note(self):
        """Archive a single QA note."""

        marker, folder = self._start("TC-BB-040")

        title = f"QA_ARC_040_{marker}"
        content = f"Noi dung luu tru QA {marker}"

        rid = self._new(title, content)
        self._shot(folder, "FN13_TC-BB-040_D01", 1)

        self._archive(rid, title, content)
        self._shot(folder, "FN13_TC-BB-040_D01", 2)

        self._goto("archive", folder)
        self._visible(title, "ArchiveScreen")

        self._wait_row(rid, "archived", title, content)
        self._shot(folder, "FN13_TC-BB-040_D01", 3)

        print("[PASS] TC-BB-040 D01")

    # ==========================================================
    # FN-14 / TC-BB-040B D01
    # ==========================================================

    def test_tc_bb_040b_d01_unarchive_single_note(self):
        """Unarchive a note from Archive back to Home."""

        marker, folder = self._start("TC-BB-040B")

        title = f"QA_ARC_040B_{marker}"
        content = f"Noi dung bo luu tru {marker}"

        rid = self._new(title, content)

        self._archive(rid, title, content)
        self._goto("archive", folder)

        self._shot(folder, "FN14_TC-BB-040B_D01", 1)

        self._unarchive(rid, title, content)
        self._shot(folder, "FN14_TC-BB-040B_D01", 2)

        self._goto("home", folder)
        self._visible(title, "HomeScreen")

        self._wait_row(rid, "normal", title, content)
        self._shot(folder, "FN14_TC-BB-040B_D01", 3)

        print("[PASS] TC-BB-040B D01")

    # ==========================================================
    # FN-13 / TC-BB-EXT-008 D01
    # ==========================================================

    def test_tc_bb_ext_008_d01_archive_isolation(self):
        """Archive TARGET without affecting CONTROL."""

        marker, folder = self._start("TC-BB-EXT-008")

        target = f"QA_ARC_TARGET_{marker}"
        control = f"QA_ARC_CONTROL_{marker}"

        target_content = f"Target QA {marker}"
        control_content = f"Control QA {marker}"

        target_id = self._new(target, target_content)
        control_id = self._new(control, control_content)

        assert target_id != control_id

        self._shot(folder, "FN13_TC-BB-EXT-008_D01", 1)

        self._archive(target_id, target, target_content)

        self._wait_row(
            control_id, "normal",
            control, control_content,
        )
        self._visible(control, "HomeScreen")

        self._shot(folder, "FN13_TC-BB-EXT-008_D01", 2)

        self._goto("archive", folder)

        self._visible(target, "ArchiveScreen")
        self._absent(control, "ArchiveScreen")

        self._wait_row(
            target_id, "archived",
            target, target_content,
        )
        self._wait_row(
            control_id, "normal",
            control, control_content,
        )

        self._shot(folder, "FN13_TC-BB-EXT-008_D01", 3)

        print("[PASS] TC-BB-EXT-008 D01")

    # ==========================================================
    # FN-13 / TC-BB-EXT-006 D01
    # ==========================================================

    def test_tc_bb_ext_006_d01_archive_persistence(self):
        """Archived note survives force-stop/relaunch."""

        marker, folder = self._start("TC-BB-EXT-006")

        title = f"QA_ARCHIVE_PERSIST_{marker}"
        content = (
            f"Dòng một: ghi chú lưu trữ {marker}\n"
            "Dòng hai: dữ liệu còn nguyên."
        )

        rid = self._new(title, content)
        self._shot(folder, "FN13_TC-BB-EXT-006_D01", 1)

        self._archive(rid, title, content)
        self._shot(folder, "FN13_TC-BB-EXT-006_D01", 2)

        self._restart()

        self._wait_row(rid, "archived", title, content)
        self._absent(title, "HomeScreen")

        self._shot(folder, "FN13_TC-BB-EXT-006_D01", 3)

        self._goto("archive", folder)

        self._visible(title, "ArchiveScreen")
        self._wait_row(rid, "archived", title, content)

        self._shot(folder, "FN13_TC-BB-EXT-006_D01", 4)

        print("[PASS] TC-BB-EXT-006 D01")

    # ==========================================================
    # FN-14 / TC-BB-EXT-007 D01
    # ==========================================================

    def test_tc_bb_ext_007_d01_unarchive_no_duplicates(self):
        """Unarchive -> Archive -> Unarchive; no duplicates."""

        marker, folder = self._start("TC-BB-EXT-007")

        title = f"QA_UNARCHIVE_{marker}"
        content = f"Vong doi khong nhan ban {marker}"

        rid = self._new(title, content)

        # Initial archive
        self._archive(rid, title, content)
        self._goto("archive", folder)

        self._shot(folder, "FN14_TC-BB-EXT-007_D01", 1)

        # First unarchive
        self._unarchive(rid, title, content)
        self._goto("home", folder)

        self._visible(title, "HomeScreen")
        self._shot(folder, "FN14_TC-BB-EXT-007_D01", 2)

        # Archive again, same immutable note ID
        self._archive(rid, title, content)
        self._goto("archive", folder)

        self._visible(title, "ArchiveScreen")
        self._shot(folder, "FN14_TC-BB-EXT-007_D01", 3)

        # Second unarchive
        self._unarchive(rid, title, content)
        self._goto("home", folder)

        self._visible(title, "HomeScreen")

        # Restart app and verify final state
        self._restart()

        self._wait_row(rid, "normal", title, content)
        self._visible(title, "HomeScreen")

        self._shot(folder, "FN14_TC-BB-EXT-007_D01", 4)

        # Final Archive check: QA note must not appear there.
        self._goto("archive", folder)
        self._absent(title, "ArchiveScreen")

        self._wait_row(rid, "normal", title, content)
        self._shot(folder, "FN14_TC-BB-EXT-007_D01", 5)

        print("[PASS] TC-BB-EXT-007 D01")
