"""Device driver and automation utilities wrapping uiautomator2 for Smart Note App.

Centralizes shared UI helpers that were previously duplicated across test files,
following the Dynamic-First, Coordinate-Fallback design principle.
"""
import os
import time
import uiautomator2 as u2
from automation import config


class SmartNoteDriver:
    """High-level test driver implementing Dynamic-First, Coordinate-Fallback design.

    Provides centralized helpers for screen navigation, note lifecycle,
    and test cleanup to eliminate duplication across test suites.
    """
    def __init__(self, serial: str = config.DEVICE_SERIAL):
        self.serial = serial
        self.device = u2.connect(serial)
        self.ensure_device_ready()

    def ensure_device_ready(self):
        """Wake up and unlock device."""
        self.device.screen_on()
        self.device.unlock()

    def launch_app(self):
        """Launch target application and wait for idle."""
        self.device.app_start(config.APP_PACKAGE)
        time.sleep(1.5)

    # =========================================================================
    # ELEMENT FINDING (Dynamic-First, Coordinate-Fallback)
    # =========================================================================

    def find_by_text(self, text: str, contains: bool = False):
        """Find element dynamically by text or content-description (Flutter friendly)."""
        d = self.device
        if not contains:
            if d(text=text).exists:
                return d(text=text)
            if d(description=text).exists:
                return d(description=text)
        else:
            if d(textContains=text).exists:
                return d(textContains=text)
            if d(descriptionContains=text).exists:
                return d(descriptionContains=text)
        # XPath Fallback
        if not contains:
            xpath = f'//*[@text="{text}" or @content-desc="{text}"]'
        else:
            xpath = f'//*[contains(@text, "{text}") or contains(@content-desc, "{text}")]'
        nodes = d.xpath(xpath).all()
        if nodes:
            return nodes[0]
        return None

    def click_element_or_coordinate(self, text: str, fallback_x: int, fallback_y: int, timeout: float = 3.0):
        """Try dynamic click first, fallback to verified coordinates if locator fails."""
        d = self.device
        el = self.find_by_text(text)
        if el is not None:
            try:
                el.click(timeout=timeout)
                return True
            except Exception:
                pass
        d.click(fallback_x, fallback_y)
        return True

    def dismiss_keyboard_safely(self, touch_x: int = 540, touch_y: int = 600):
        """Dismiss keyboard by tapping safe neutral area without triggering Back exit."""
        self.device.click(touch_x, touch_y)
        time.sleep(0.5)

    # =========================================================================
    # EVIDENCE & SCREEN EXTRACTION
    # =========================================================================

    def capture_evidence(self, relative_path: str) -> str:
        """Capture screen evidence and save to evidence folder."""
        full_path = os.path.join(config.PROJECT_ROOT, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        self.device.screenshot().save(full_path)
        return full_path

    def get_screen_texts(self):
        """Extract all visible texts and content descriptions."""
        texts = []
        for el in self.device.xpath('//*[@text!="" or @content-desc!=""]').all():
            t = el.attrib.get('text', '') or el.attrib.get('content-desc', '')
            if t and t not in texts:
                texts.append(t)
        return texts

    # =========================================================================
    # SCREEN STATE DETECTION (centralized from test files)
    # =========================================================================

    def is_in_editor(self) -> bool:
        """Check if currently on EditorScreen via robust Flutter semantics."""
        d = self.device
        return (
            d(description="Ghi ch\u00fa").exists
            or d(description="Note").exists
            or d(description="AI Tr\u1ee3 l\u00fd").exists
            or d(description="AI Assistant").exists
            or d(description="\u0110\u1ecbnh d\u1ea1ng").exists
            or d(description="Format").exists
            or d(description="M\u00e0u s\u1eafc").exists
            or d(description="Color").exists
            or d(description="Kh\u00f3a ghi ch\u00fa").exists
            or d(description="Lock note").exists
            or d(description="M\u1edf kh\u00f3a ghi ch\u00fa").exists
            or d(description="Ghim").exists
            or d(description="Nh\u1eafc nh\u1edf").exists
            or d(text="Ti\u00eau \u0111\u1ec1").exists
            or d(text="Title").exists
            or d(description="Ti\u00eau \u0111\u1ec1").exists
            or d(description="Title").exists
        )

    def is_on_home_screen(self) -> bool:
        """Check if currently on HomeScreen."""
        has_search = (
            self.find_by_text("T\u00ecm ki\u1ebfm", contains=True) is not None
            or self.find_by_text("Search", contains=True) is not None
        )
        has_empty = (
            self.find_by_text("Ch\u01b0a c\u00f3 ghi ch\u00fa n\u00e0o", contains=True) is not None
            or self.find_by_text("No notes yet", contains=True) is not None
        )
        not_login = (
            self.find_by_text("\u0110\u0103ng k\u00fd ngay") is None
            and self.find_by_text("Qu\u00ean m\u1eadt kh\u1ea9u?") is None
        )
        return (has_search or has_empty) and not_login and not self.is_in_editor()

    def is_in_login(self) -> bool:
        """Check if currently on LoginScreen in Login mode."""
        d = self.device
        return (
            d(descriptionContains="Ch\u00e0o m\u1eebng tr\u1edf l\u1ea1i!").exists
            or d(textContains="Ch\u00e0o m\u1eebng tr\u1edf l\u1ea1i!").exists
            or d(description="\u0110\u0103ng k\u00fd ngay").exists
            or d(text="\u0110\u0103ng k\u00fd ngay").exists
            or "Ch\u00e0o m\u1eebng tr\u1edf l\u1ea1i!" in d.dump_hierarchy()
        )

    def is_in_register(self) -> bool:
        """Check if currently on Register Screen."""
        d = self.device
        return (
            d(descriptionContains="T\u1ea1o t\u00e0i kho\u1ea3n m\u1edbi").exists
            or d(textContains="T\u1ea1o t\u00e0i kho\u1ea3n m\u1edbi").exists
            or "T\u1ea1o t\u00e0i kho\u1ea3n m\u1edbi" in d.dump_hierarchy()
        )

    def is_in_verification(self) -> bool:
        """Check if currently on EmailVerificationScreen."""
        d = self.device
        return (
            d(descriptionContains="Quay l\u1ea1i \u0111\u0103ng nh\u1eadp").exists
            or d(textContains="Quay l\u1ea1i \u0111\u0103ng nh\u1eadp").exists
            or d(descriptionContains="X\u00e1c th\u1ef1c").exists
            or "Quay l\u1ea1i \u0111\u0103ng nh\u1eadp" in d.dump_hierarchy()
        )

    # =========================================================================
    # SCREEN NAVIGATION (centralized from test files)
    # =========================================================================

    def ensure_home_screen(self):
        """Precondition: Ensure app is at HomeScreen, recovering from any lingering state.
        
        Self-healing recovery:
        - Dismisses any active Selection Mode, Modal Bottom Sheets, EditorScreen, or Scrim.
        - If app is currently on Login/Register screen, automatically logs in via Google account.
        """
        self.ensure_device_ready()
        self.launch_app()
        time.sleep(1.0)

        d = self.device

        # If already on home screen, return immediately
        if self.is_on_home_screen():
            return True

        # Recovery loop: dismiss selection mode, modals, editor
        for _ in range(5):
            cancel_btn = (
                self.find_by_text("Hủy chọn", contains=True)
                or self.find_by_text("Cancel selection", contains=True)
            )
            if cancel_btn is not None:
                try:
                    cancel_btn.click()
                    time.sleep(0.5)
                except Exception:
                    pass

            if self.is_on_home_screen():
                return True

            if self.is_in_login() or self.is_in_register():
                break

            d.press("back")
            time.sleep(0.8)

        # If on RegisterScreen, switch to Login mode
        if self.is_in_register():
            login_tab = self.find_by_text("Đăng nhập")
            if login_tab:
                try:
                    login_tab.click()
                    time.sleep(1.0)
                except Exception:
                    pass

        # If on LoginScreen, log in via Google to restore HomeScreen
        if self.is_in_login():
            google_btn = self.find_by_text("Đăng nhập bằng Google")
            if google_btn:
                try:
                    google_btn.click()
                    time.sleep(2.5)
                    # Pick account on Google Accounts dialog
                    acct = self.find_by_text("ht158713@gmail.com") or self.find_by_text("Thu Hường")
                    if acct:
                        acct.click()
                        time.sleep(4.0)
                    else:
                        # Tap first account in list
                        d.click(540, 600)
                        time.sleep(4.0)
                except Exception:
                    pass

        # Final verification loop with sync wait (allow up to 15s for Firestore cloud sync)
        for _ in range(15):
            if self.is_on_home_screen():
                return True
            time.sleep(1.0)

        assert self.is_on_home_screen(), (
            "Precondition failed: App is not on HomeScreen. "
            "Please ensure user is logged in and app is launched to HomeScreen."
        )
        return True
    def ensure_login_screen(self):
        """Precondition: Ensure device is at Login Screen.
        
        Follows Dynamic-First, Coordinate-Fallback design:
        - Tries dynamic accessibility / semantics locators first.
        - Falls back to verified coordinates only when Flutter lacks semantics in current build.
        """
        self.ensure_device_ready()
        self.launch_app()
        time.sleep(2)

        d = self.device

        if self.is_in_login():
            return True

        if self.is_in_verification():
            ret_btn = self.find_by_text("Quay lại đăng nhập")
            if ret_btn:
                try:
                    ret_btn.click()
                except Exception:
                    # Coordinate Fallback: (540, 2140)
                    # Reason: Bottom button on EmailVerificationScreen when semantics tree lag occurs
                    # Resolution dependency: 1080x2340 (Samsung Galaxy S21 FE 5G)
                    d.click(540, 2140)
            time.sleep(2)
            return True

        if self.is_on_home_screen():
            # Dynamic locator: Avatar on AppBar
            avatar = (
                d(descriptionContains="Tài khoản")
                or d(descriptionContains="Account")
                or d(descriptionContains="avatar")
            )
            if avatar.exists:
                avatar.click()
            else:
                # Coordinate Fallback: (1006, 172)
                # Reason: Flutter CircleAvatar lacks semantics label in current build
                # Resolution dependency: 1080x2340 (Samsung Galaxy S21 FE 5G, top-right AppBar)
                d.click(1006, 172)
            time.sleep(1)

            # Dynamic locator: "Quản lý tài khoản" option
            acct_btn = (
                self.find_by_text("Quản lý tài khoản", contains=True)
                or self.find_by_text("Account", contains=True)
            )
            if acct_btn:
                try:
                    acct_btn.click()
                except Exception:
                    # Coordinate Fallback: (500, 750)
                    # Reason: Account BottomSheet item when semantics lag occurs
                    # Resolution dependency: 1080x2340 (Samsung Galaxy S21 FE 5G)
                    d.click(500, 750)
            else:
                d.click(500, 750)
            time.sleep(1)

            # Dynamic locator: "Đăng xuất" button
            logout_btn = (
                self.find_by_text("Đăng xuất", contains=True)
                or self.find_by_text("Logout", contains=True)
            )
            if logout_btn:
                try:
                    logout_btn.click()
                except Exception:
                    # Coordinate Fallback: (540, 1120)
                    # Reason: Logout button on Account Profile page
                    # Resolution dependency: 1080x2340 (Samsung Galaxy S21 FE 5G)
                    d.click(540, 1120)
            else:
                d.click(540, 1120)
            time.sleep(1)

            # Dynamic locator: Confirmation button on dialog
            confirm_btn = (
                self.find_by_text("Đăng xuất tài khoản", contains=True)
                or self.find_by_text("Đăng xuất", contains=True)
                or self.find_by_text("Xác nhận", contains=True)
                or self.find_by_text("Đồng ý", contains=True)
                or self.find_by_text("OK")
                or self.find_by_text("Confirm")
            )
            if confirm_btn:
                try:
                    confirm_btn.click()
                except Exception:
                    # Coordinate Fallback: (672, 1324)
                    # Reason: Confirm button on AlertDialog
                    # Resolution dependency: 1080x2340 (Samsung Galaxy S21 FE 5G)
                    d.click(672, 1324)
            else:
                d.click(672, 1324)
            time.sleep(2)

        if self.is_in_register():
            # On Register mode, the toggle link to switch back to Login mode is "Đăng nhập" at the bottom
            login_link = None
            for el in d(className="android.view.View", clickable=True):
                try:
                    desc = el.info.get("contentDescription", "") or ""
                    if desc == "Đăng nhập":
                        b = el.info.get("bounds", {})
                        if b.get("bottom", 0) > 2000:
                            login_link = el
                            break
                except Exception:
                    pass
            if login_link is not None:
                try:
                    login_link.click()
                except Exception:
                    # Fallback coordinate for toggle link on RegisterScreen (bottom row)
                    # Resolution dependency: 1080x2340 (Samsung Galaxy S21 FE 5G)
                    d.click(745, 2160)
            else:
                d.click(745, 2160)
            time.sleep(1.5)

        for _ in range(10):
            if self.is_in_login():
                return True
            if self.is_in_register():
                link = self.find_by_text("Đăng nhập")
                if link:
                    try:
                        link.click()
                    except Exception:
                        d.click(745, 2160)
            time.sleep(0.5)

        assert self.is_in_login(), "Precondition failed: Unable to navigate to Login Screen."
        return True

    def ensure_register_screen(self):
        """Precondition: Ensure device is at Register Screen."""
        self.ensure_device_ready()
        self.launch_app()
        time.sleep(1.0)

        d = self.device

        if self.is_on_home_screen():
            self.ensure_login_screen()

        if self.is_in_verification():
            ret_btn = self.find_by_text("Quay l\u1ea1i \u0111\u0103ng nh\u1eadp")
            if ret_btn:
                try:
                    ret_btn.click()
                except Exception:
                    d.click(540, 2140)
            time.sleep(2)

        if self.is_in_login():
            reg_link = self.find_by_text("\u0110\u0103ng k\u00fd ngay")
            if reg_link:
                try:
                    reg_link.click()
                except Exception:
                    pass
                time.sleep(1)

        if self.is_in_register():
            return True

        for _ in range(3):
            d.press("back")
            time.sleep(1)
            if self.is_in_login() or self.is_in_register():
                if self.is_in_login():
                    reg_link = self.find_by_text("\u0110\u0103ng k\u00fd ngay")
                    if reg_link:
                        try:
                            reg_link.click()
                        except Exception:
                            pass
                        time.sleep(1)
                if self.is_in_register():
                    return True

        assert self.is_in_register(), "Precondition failed: Cannot navigate to RegisterScreen."
        return True

    # =========================================================================
    # NOTE EDITOR HELPERS (centralized from test files)
    # =========================================================================

    def open_note_editor(self):
        """Locate FAB in bottom-right corner and open EditorScreen for a new note."""
        d = self.device

        cancel_btn = (
            self.find_by_text("H\u1ee7y ch\u1ecdn", contains=True)
            or self.find_by_text("Cancel selection", contains=True)
        )
        if cancel_btn is not None:
            try:
                cancel_btn.click()
                time.sleep(0.5)
            except Exception:
                pass

        fab_btn = None
        candidates = []
        for btn in d(className="android.widget.Button"):
            try:
                info = btn.info
                desc = (info.get("contentDescription", "") or "").strip()
                if "Ho\u00e0n t\u00e1c" in desc or "Undo" in desc:
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
            d.click(964, 2185)

        for _ in range(8):
            time.sleep(0.5)
            if self.is_in_editor():
                return

        d.click(964, 2185)
        time.sleep(1.5)
        assert self.is_in_editor(), "Failed to open EditorScreen after tapping FAB."

    def open_existing_note(self, title_or_content: str):
        """Locate and tap an existing NoteCard on HomeScreen to open EditorScreen."""
        d = self.device

        cancel_btn = (
            d(descriptionContains="H\u1ee7y ch\u1ecdn")
            or d(descriptionContains="Cancel")
            or d(textContains="H\u1ee7y ch\u1ecdn")
        )
        if cancel_btn is not None:
            try:
                cancel_btn.click()
                time.sleep(0.5)
            except Exception:
                pass

        card = None
        for _ in range(8):
            card = (
                d(descriptionContains=title_or_content)
                or d(textContains=title_or_content)
            )
            if card.exists:
                break
            xpath_expr = f'//*[contains(@content-desc, "{title_or_content}") or contains(@text, "{title_or_content}")]'
            if d.xpath(xpath_expr).exists:
                card = d.xpath(xpath_expr)
                break
            time.sleep(0.5)

        assert card is not None and card.exists, (
            f"Cannot locate NoteCard with '{title_or_content}' on HomeScreen."
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
            if self.is_in_editor():
                time.sleep(0.5)
                return

        assert self.is_in_editor(), f"Failed to open EditorScreen for note '{title_or_content}'."

    def get_title_field(self):
        """Locate Title input field dynamically."""
        el = self.find_by_text("Ti\u00eau \u0111\u1ec1") or self.find_by_text("Title")
        if el is not None:
            return el
        for field in self.device(className="android.widget.EditText"):
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
            self.device.click(200, 290)
            time.sleep(0.3)
            focused = self.device(focused=True)
            if focused.exists:
                focused.set_text(title)
            else:
                edits = self.device(className="android.widget.EditText")
                if edits.exists:
                    edits[0].set_text(title)

    def input_content(self, content: str):
        """Input content into QuillEditor via native pasteClipboard."""
        if not content:
            return
        d = self.device

        content_placeholder = d(description="Ghi ch\u00fa") or d(text="Ghi ch\u00fa")
        if content_placeholder.exists:
            content_placeholder.click()
        else:
            d.click(540, 520)
        time.sleep(0.5)

        d.set_clipboard(content)
        time.sleep(0.3)
        try:
            d.jsonrpc.pasteClipboard()
        except Exception:
            time.sleep(0.3)
            d.jsonrpc.pasteClipboard()
        time.sleep(0.5)

        # Input content via clipboard with retries
        content_in_editor = False
        for _ in range(12):
            if d(descriptionContains=content).exists or content in d.dump_hierarchy():
                content_in_editor = True
                break
            time.sleep(1)
        # If still not detected, try an additional fallback click and paste
        if not content_in_editor:
            d.click(540, 520)
            time.sleep(0.5)
            d.set_clipboard(content)
            time.sleep(0.3)
            try:
                d.jsonrpc.pasteClipboard()
            except Exception:
                pass
            time.sleep(1)
            if d(descriptionContains=content).exists or content in d.dump_hierarchy():
                content_in_editor = True
        assert content_in_editor, (
            f"[INPUT FAILURE] Content '{content}' was not entered into QuillEditor."
        )

    def save_and_exit_editor(self):
        """Save note and return to HomeScreen via AppBar back button or system back."""
        d = self.device
        d.click(75, 170)
        time.sleep(1.5)
        if self.is_in_editor():
            d.press("back")
            time.sleep(1.5)
        if self.is_in_editor():
            d.press("back")
            time.sleep(1.5)

    # =========================================================================
    # NOTE LIFECYCLE HELPERS
    # =========================================================================

    def ensure_test_note(self, title: str, content: str):
        """Ensure a test note exists on HomeScreen. If not found, create it."""
        d = self.device
        card = d(descriptionContains=title) or d(textContains=title)
        if not card.exists:
            xpath_expr = f'//*[contains(@content-desc, "{title}") or contains(@text, "{title}")]'
            if not d.xpath(xpath_expr).exists:
                print(f"[Precondition] Note '{title}' not found. Creating...")
                self.open_note_editor()
                self.input_title(title)
                self.input_content(content)
                self.save_and_exit_editor()
                found = False
                for _ in range(12):
                    if (
                        d(descriptionContains=title).exists
                        or d(textContains=title).exists
                        or d.xpath(xpath_expr).exists
                        or self.find_by_text(title, contains=True) is not None
                    ):
                        found = True
                        break
                    time.sleep(0.5)
                assert found, f"Failed to create precondition note '{title}' on HomeScreen."

    def cleanup_note_via_selection(self, title_or_content: str):
        """Safely clean up test note using Selection Mode. Best-effort, never raises."""
        d = self.device
        try:
            if self.is_in_editor():
                d.press("back")
                time.sleep(1.0)

            card = d(descriptionContains=title_or_content) or d(textContains=title_or_content)
            if not card.exists:
                return

            card.long_click(duration=1.2)
            time.sleep(0.8)

            is_selection_mode = (
                d(descriptionContains="H\u1ee7y ch\u1ecdn").exists
                or d(descriptionContains="Cancel").exists
                or d(textContains="H\u1ee7y ch\u1ecdn").exists
                or d(descriptionContains="th\u00f9ng r\u00e1c").exists
                or d(descriptionContains="Trash").exists
            )

            if is_selection_mode:
                trash_btn = (
                    d(descriptionContains="th\u00f9ng r\u00e1c")
                    or d(descriptionContains="Trash")
                    or d(descriptionContains="trash")
                )
                if trash_btn.exists:
                    trash_btn.click()
                    time.sleep(1.2)
                else:
                    cancel_btn = d(descriptionContains="H\u1ee7y ch\u1ecdn") or d(descriptionContains="Cancel")
                    if cancel_btn.exists:
                        cancel_btn.click()
                    time.sleep(0.5)
            elif self.is_in_editor():
                d.press("back")
                time.sleep(1.0)
        except Exception as e:
            print(f"[Cleanup Notice] Cleanup for '{title_or_content}' skipped: {e}")
            try:
                if self.is_in_editor():
                    d.press("back")
            except Exception:
                pass

    def select_note_by_long_press(self, title_or_content: str) -> bool:
        """Long-press a NoteCard to activate Selection Mode."""
        d = self.device
        card = d(descriptionContains=title_or_content) or d(textContains=title_or_content)
        if not card.exists:
            return False
        card.long_click(duration=1.2)
        time.sleep(0.8)
        return (
            d(descriptionContains="H\u1ee7y ch\u1ecdn").exists
            or d(descriptionContains="Cancel").exists
            or d(textContains="H\u1ee7y ch\u1ecdn").exists
        )

    def get_home_notes_state(self) -> dict:
        """Capture the current note items state on HomeScreen."""
        is_empty = (
            self.find_by_text("Ch\u01b0a c\u00f3 ghi ch\u00fa n\u00e0o", contains=True) is not None
            or self.find_by_text("No notes yet", contains=True) is not None
        )
        ignored_ui_texts = {
            "T\u00ecm ki\u1ebfm", "Search",
            "\u0110\u01b0\u1ee3c ghim", "Pinned",
            "Kh\u00e1c", "Others",
            "Ch\u01b0a c\u00f3 ghi ch\u00fa n\u00e0o", "No notes yet",
            "Nh\u1ea5n + \u0111\u1ec3 t\u1ea1o ghi ch\u00fa \u0111\u1ea7u ti\u00ean",
            "Qu\u1ea3n l\u00fd nh\u00e3n", "Manage labels"
        }
        note_items = []
        for el in self.device.xpath('//*[@text!="" or @content-desc!=""]').all():
            txt = (el.attrib.get('text', '') or el.attrib.get('content-desc', '')).strip()
            if not txt or txt in ignored_ui_texts:
                continue
            if (":" in txt or "%" in txt) and len(txt) <= 6:
                continue
            note_items.append(txt)
        return {"is_empty": is_empty, "note_items": note_items, "count": len(note_items)}
