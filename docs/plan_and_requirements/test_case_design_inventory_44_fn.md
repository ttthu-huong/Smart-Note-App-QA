# BẢNG KIỂM KÊ VÀ ĐẶC TẢ THIẾT KẾ KIỂM THỬ TOÀN DIỆN 44 CHỨC NĂNG (GIAI ĐOẠN 3 – TEST CASE DESIGN)
## Dự án: Smart Note App
**Branch:** `huong`  
**Chiến lược áp dụng:** **THIẾT KẾ ĐẦY ĐỦ CHO TOÀN DỰ ÁN – THỰC THI THEO ƯU TIÊN**  
**Tiêu chuẩn áp dụng:** IEEE 829 (Test Design Specification) & ISTQB Advanced Test Design  
**Ngày lập:** 11/10/2026  
**Cam kết tuân thủ:** Bảo toàn nguyên vẹn 140 Black-box execution items, 18 Unit Tests PASS, 8 Firestore Rules tests, 8 Defect logs; không sửa `lib/`, không chạy test, không commit/push.

---

## I. BẢNG KIỂM KÊ CHI TIẾT 44 CHỨC NĂNG (FN-01 ĐẾN FN-44)

> **Ghi chú về Trạng thái thiết kế & thực thi:**
> - `DESIGNED (Reused)`: Test case đã có từ trước trong bộ tài liệu và được tái sử dụng nguyên vẹn.
> - `DESIGNED (New)`: Test case mới được thiết kế bổ sung trong đợt này để phủ kín chức năng.
> - `EXECUTED (PASS/FAIL/BLOCKED)`: Ca kiểm thử đã có mã/kịch bản thực thi và có bằng chứng ghi nhận.
> - `NOT RUN`: Ca kiểm thử đã thiết kế đầy đủ nhưng chưa thực thi trong lượt này (chờ kế hoạch thực thi theo mức ưu tiên).

| Mã FN | Tên chức năng gốc | REQ / NFR liên quan | Test Case đã tồn tại (Tái sử dụng) | Test Case thiết kế mới | Phương pháp kiểm thử phù hợp | Mức ưu tiên | Trạng thái Thiết kế | Trạng thái Thực thi |
|:---:|:---|:---:|:---|:---|:---|:---:|:---:|:---:|
| **FN-01** | Validate form đăng nhập | REQ-02, NFR-04 | `TC-BB-006C`, `006D`, `007B`, `008B`, `009B`, `009C`, `009D`, `TC-WB-001/002` | — | Black-box (EP, BVA), Automation (Python) | **P1** | `DESIGNED (Reused)` | **EXECUTED (PASS / FAIL BUG-BB-002, 003)** |
| **FN-02** | Đăng ký tài khoản | REQ-01, NFR-04 | `TC-BB-001` .. `005`, `001B`, `002B..F`, `003B`, `004B` (19 items) | — | Black-box (EP, BVA), Automation (Python) | **P1** | `DESIGNED (Reused)` | **EXECUTED (18 PASS / 1 FAIL BUG-FN02-01)** |
| **FN-03** | Xác thực email | REQ-01 | `TC-BB-001`, `TC-BB-006B` | `TC-BB-003C`, `TC-BB-003D` | Black-box (State Transition, UI Flow) | **P2** | `DESIGNED (Reused + New)` | **1 Reused EXECUTED / 2 New NOT RUN** |
| **FN-04** | Đăng nhập email/password | REQ-02 | `TC-BB-006` .. `009G` (16 items), `TC-WB-001..005` `[DESIGN ONLY]` | — | Black-box (EP), White-box, Automation | **P1** | `DESIGNED (Reused)` | **EXECUTED (14 PASS / 2 FAIL)** |
| **FN-05** | Đăng nhập Google OAuth | REQ-02 | `TC-BB-010` .. `011G` (8 items), `test_fn05_google_oauth.py` | — | Black-box (Third-party Integration), Auto | **P1** | `DESIGNED (Reused)` | **EXECUTED (8 PASS / 0 FAIL)** |
| **FN-06** | Đặt lại mật khẩu | REQ-03 | `TC-BB-009E`, `TC-BB-011` .. `011C` | `TC-BB-011H` | Black-box (Boundary, Negative Flow) | **P2** | `DESIGNED (Reused + New)` | **4 Reused EXECUTED / 1 New NOT RUN** |
| **FN-07** | Đăng xuất tài khoản | REQ-02 | `TC-BB-011E`, `TC-WB-003` `[DESIGN ONLY]`, `auth01_logged_out.png` | `TC-BB-007C` | Black-box (Session Lifecycle, Usability) | **P1** | `DESIGNED (Reused + New)` | **1 Reused EXECUTED / 1 New NOT RUN** |
| **FN-08** | Tạo ghi chú văn bản | REQ-04, NFR-01 | `TC-BB-016` .. `018F` (8 items), `test_fn08_create_note.py`, `test/note_model_test.dart` (9 unit tests), `TC-WB-020` `[DESIGN ONLY]` | — | Black-box (Autosave), White-box, Auto | **P1** | `DESIGNED (Reused)` | **EXECUTED (8 BB PASS + 9 WB PASS)** |
| **FN-09** | Cập nhật ghi chú | REQ-05, NFR-01 | `TC-BB-019` .. `020D` (12 items), `test_fn09_edit_note.py`, `TC-WB-016, 017, 019` `[DESIGN ONLY]` | — | Black-box (Rich-text, Back event), White-box | **P1** | `DESIGNED (Reused)` | **EXECUTED (12 PASS, 1 Glitch BUG-005)** |
| **FN-10** | Chuyển ghi chú vào thùng rác | REQ-09 | `TC-BB-021`, `021B`, `021C` (`D01`, `D02`), `021D`, `023C` (`fn10_fn11_fn12_execution_sheet.md`) | — | Black-box (Soft-delete), White-box | **P1** | `DESIGNED (Reused)` | **EXECUTED (PASS 100%)** |
| **FN-11** | Khôi phục ghi chú | REQ-09 | `TC-BB-022`, `022B`, `022C`, `023C` (`fn10_fn11_fn12_execution_sheet.md`) | — | Black-box (State Restore), White-box | **P1** | `DESIGNED (Reused)` | **EXECUTED (PASS 100%)** |
| **FN-12** | Xóa ghi chú vĩnh viễn | REQ-09 | `TC-BB-023`, `023B` (`D01`, `D02`), `023C` (`fn10_fn11_fn12_execution_sheet.md`), `TC-WB-006, 007` `[DESIGN ONLY]` *(Chính: `deleteNoteForever` $\rightarrow$ `deleteFile`)* | — | Black-box (Hard Delete, Clean Cloudinary) | **P1** | `DESIGNED (Reused)` | **EXECUTED (PASS 100%)** |
| **FN-13** | Lưu trữ ghi chú (Archive) | REQ-09 | `arc01_archive_screen.png` (bằng chứng có sẵn) | `TC-BB-040` *(Archive)* | Black-box (Status Transition, Filter Hide) | **P2** | `DESIGNED (Reused + New)` | **1 Evidence EXECUTED / 1 New NOT RUN** |
| **FN-14** | Bỏ lưu trữ ghi chú | REQ-09 | `arc02_unarchived_home.png` (bằng chứng có sẵn) | `TC-BB-040B` *(Unarchive)* | Black-box (Status Restore, Home Display) | **P2** | `DESIGNED (Reused + New)` | **1 Evidence EXECUTED / 1 New NOT RUN** |
| **FN-15** | Tạo ghi chú checklist | REQ-06 | `TC-BB-CHK-01`, `test/checklist_test.dart` (5 tests), `TC-WB-015, 022` `[DESIGN ONLY]` | — | Black-box (To-do Flow), White-box Unit | **P1** | `DESIGNED (Reused)` | **EXECUTED (1 BB PASS + 5 WB PASS)** |
| **FN-16** | Thêm mục checklist | REQ-06 | `TC-BB-CHK-02`, `test/checklist_test.dart` | — | Black-box (Dynamic List, Keyboard Next) | **P1** | `DESIGNED (Reused)` | **EXECUTED (PASS 100%)** |
| **FN-17** | Tick hoàn thành mục | REQ-06 | `TC-BB-CHK-03`, `test/checklist_copy_with_test.dart` (4 tests) | — | Black-box (State Toggle, Strike-through) | **P1** | `DESIGNED (Reused)` | **EXECUTED (1 BB PASS + 4 WB PASS)** |
| **FN-18** | Bỏ tick mục checklist | REQ-06 | `TC-BB-CHK-04`, `test/checklist_copy_with_test.dart` | — | Black-box (State Untick) | **P1** | `DESIGNED (Reused)` | **EXECUTED (PASS 100%)** |
| **FN-19** | Xóa mục checklist | REQ-06 | `TC-BB-CHK-05`, `TC-BB-CHK-06` | — | Black-box (Item Remove, Index Preservation) | **P1** | `DESIGNED (Reused)` | **EXECUTED (PASS 100%)** |
| **FN-20** | Ghim ghi chú (Pin) | REQ-07 | `TC-BB-024` .. `024H`, `TC-BB-025` .. `025F` (15 items), `test_fn20_pin_note.py` | — | Black-box (Sorting, Group Header), Auto | **P1** | `DESIGNED (Reused)` | **EXECUTED (15 PASS / 0 FAIL)** |
| **FN-21** | Tạo nhãn (Create Tag) | REQ-12 | `tag01_create_tag.png` (bằng chứng có sẵn) | `TC-BB-041` | Black-box (CRUD Tag, Color Assign) | **P2** | `DESIGNED (Reused + New)` | **1 Evidence EXECUTED / 1 New NOT RUN** |
| **FN-22** | Gắn nhãn vào ghi chú | REQ-12 | `tag02_note_tagged.png` (bằng chứng có sẵn) | `TC-BB-041B` | Black-box (Tag Attachment, Filter by Tag) | **P2** | `DESIGNED (Reused + New)` | **1 Evidence EXECUTED / 1 New NOT RUN** |
| **FN-23** | Tìm kiếm văn bản & lọc `has:list` | REQ-08, NFR-04 | `TC-BB-026` .. `029` (22 items trong `fn23_execution_sheet.md`, gồm `TC-BB-027G-D01` lọc `has:list` & `TC-BB-026B-D03` không dấu), `TC-NF-001, 007`, `test_fn23_search.py`, `TC-WB-016` `[DESIGN ONLY]` | — | Black-box (SQL LIKE, SQLi Robustness), Auto | **P1** | `DESIGNED (Reused)` | **EXECUTED (20 PASS / 1 FAIL BUG-004 / 1 CHƯA ĐỦ CĂN CỨ theo BR-01)** |
| **FN-24** | Lọc `has:image` | REQ-08 | `srch05_image_filter_result.png`, `TC-BB-027B-D01` (`fn23_execution_sheet.md`) | — | Black-box (Filter Chip, Token Parser) | **P2** | `DESIGNED (Reused)` | **EXECUTED (PASS 100%)** |
| **FN-25** | Lọc `has:url` | REQ-08 | `TC-BB-027B-D03` (`fn23_execution_sheet.md`) | — | Black-box (URL Regex Detection, Chip) | **P2** | `DESIGNED (Reused)` | **EXECUTED (PASS 100%)** |
| **FN-26** | Lọc `has:audio` | REQ-08 | `srch06_audio_filter_result.png`, `TC-BB-027B-D02` (`fn23_execution_sheet.md`) | — | Black-box (Audio Attachment Filter) | **P2** | `DESIGNED (Reused)` | **EXECUTED (PASS 100%)** |
| **FN-27** | Lọc Archive / Pinned | REQ-08 | `TC-BB-027D-D01` (`is:pinned`), `TC-BB-027D-D02` (`is:archived`), `TC-BB-028B-D01` (Trash) (`fn23_execution_sheet.md`) | — | Black-box (Status Attribute Filter Chip) | **P2** | `DESIGNED (Reused)` | **EXECUTED (PASS 100%)** |
| **FN-28** | Chuyển layout Grid/List | REQ-12 | `fn28_01_before_toggle.png`, `fn28_02_after_toggle_grid.png` | `TC-BB-042` | Black-box (View Toggle, Staggered Grid) | **P3** | `DESIGNED (Reused + New)` | **1 Evidence EXECUTED / 1 New NOT RUN** |
| **FN-29** | Bật khóa ghi chú | REQ-10, NFR-05 | `TC-BB-012` .. `012C`, `015G` (`fn29_fn30_execution_sheet.md`), `test_fn29_30_biometric.py` | — | Black-box (Biometric Enrolment, State Lock) | **P1** | `DESIGNED (Reused)` | **EXECUTED (PASS / 1 BLOCKED an toàn)** |
| **FN-30** | Mở khóa sinh trắc học | REQ-10, NFR-05 | `TC-BB-013` .. `015F` (`fn29_fn30_execution_sheet.md`), `test_fn29_30_biometric.py`, `TC-NF-005` `[NOT RUN]` | — | Black-box (Sensor Prompt, Resume Lifecycle) | **P1** | `DESIGNED (Reused)` | **EXECUTED (11 PASS / 0 FAIL / 1 BLOCKED ở FN-29/30)** |
| **FN-31** | Gemini AI tóm tắt | REQ-13 | Kịch bản 5 (`Testing_Report.md` / `black_box_execution_summary.md`) | `TC-BB-032` | Black-box (AI Prompt, Streaming, Error Catch) | **P2** | `DESIGNED (Reused + New)` | **Kịch bản 5: BLOCKED (Lỗi service UI) / `TC-BB-032`: NOT RUN (Chờ gỡ BLOCKED)** |
| **FN-32** | Gemini AI đề xuất tiêu đề | REQ-13 | Kịch bản 5 (`Testing_Report.md` / `black_box_execution_summary.md`) | `TC-BB-032B` | Black-box (AI Title Suggestion) | **P2** | `DESIGNED (Reused + New)` | **Kịch bản 5: BLOCKED (Lỗi service UI) / `TC-BB-032B`: NOT RUN (Chờ gỡ BLOCKED)** |
| **FN-33** | Gemini AI đề xuất nhãn / checklist | REQ-13 | Kịch bản 5 (`Testing_Report.md` / `black_box_execution_summary.md`) | `TC-BB-032C` | Black-box (AI Checklist Extraction) | **P2** | `DESIGNED (Reused + New)` | **Kịch bản 5: BLOCKED (Lỗi service UI) / `TC-BB-032C`: NOT RUN (Chờ gỡ BLOCKED)** |
| **FN-34** | Xuất PDF | REQ-12 | `pdf01_export_preview.png`, `pdf01_print_preview.png` | `TC-BB-034` | Black-box (Document Rendering, Print Dialog) | **P2** | `DESIGNED (Reused + New)` | **1 Evidence EXECUTED / 1 New NOT RUN** |
| **FN-35** | Lưu hình vẽ tay | REQ-12 | `draw01_drawing_attached.png`, `TC-WB-009` `[DESIGN ONLY]`, `TC-WB-006, 007` *(Phụ: `_replaceDrawing`)* | `TC-BB-035` | Black-box (Canvas Paint, PNG Export) | **P2** | `DESIGNED (Reused + New)` | **1 Evidence EXECUTED / 1 New NOT RUN** |
| **FN-36** | Tải ảnh lên Cloudinary | REQ-12, NFR-08 | `image_note_home.png`, `TC-WB-008..010` `[DESIGN ONLY]`, `TC-WB-006, 007` *(Phụ: thay thế media)*, `BUG-001` | `TC-BB-036` | Black-box (Multipart HTTP, Error Timeout) | **P1** | `DESIGNED (Reused + New)` | **EXECUTED (FAIL BUG-001 / 1 New NOT RUN)** |
| **FN-37** | Đổi màu nền ghi chú | REQ-12 | `fn37_home_note_colored.png` | `TC-BB-037` | Black-box (Palette Picker, Hex Mapping) | **P3** | `DESIGNED (Reused + New)` | **1 Evidence EXECUTED / 1 New NOT RUN** |
| **FN-38** | Thiết lập nhắc nhở | REQ-12 | `rem01_reminder_set.png`, `TC-WB-018` (`Note.copyWith(clearReminder)` — `[DESIGN ONLY]`) | `TC-BB-038` | Black-box (Alarm Clock, Local Notification) | **P2** | `DESIGNED (Reused + New)` | **1 Evidence EXECUTED / 1 New NOT RUN** |
| **FN-39** | Chạm thông báo mở đúng ghi chú | REQ-12 | `rem02_notification_tap_result.png` | `TC-BB-039` | Black-box (Notification Payload, Deep Route) | **P2** | `DESIGNED (Reused + New)` | **1 Evidence EXECUTED / 1 New NOT RUN** |
| **FN-40** | Bắt đầu đồng bộ khi có mạng | REQ-11, NFR-01/02/03 | `TC-BB-030` .. `030F-D01` (6 items), `check_sync_dbs.py`, `test/security_rules_test.dart` (8 tests PASS; `TC-WB-011..014`, `TC-NF-006` $\rightarrow$ `NFR-03`), `TC-NF-003, 004` | — | Black-box (Multi-device, Airplane mode), Auto | **P1** | `DESIGNED (Reused)` | **EXECUTED (4 PASS, 2 FAIL BUG-002, 003 + 8 Rules PASS)** |
| **FN-41** | Giải quyết xung đột LWW | REQ-11, NFR-02 | `TC-BB-031` .. `031D` (4 items), `TC-WB-019` `[DESIGN ONLY]`, `TC-WB-021` `[DESIGN ONLY]` *(quy tắc hòa BR-03: `NEEDS CONFIRMATION`)* | — | Black-box (Timestamp Tie-break), White-box | **P1** | `DESIGNED (Reused)` | **EXECUTED (3 PASS / 1 CHƯA ĐỦ CĂN CỨ giải tỏa theo BR-02; BR-03 OPEN)** |
| **FN-42** | Xử lý nội dung quá lớn | NFR-04 | — | `TC-NF-009` | Non-functional (Stress / Buffer Overflow) | **P3** | `DESIGNED (New)` | **NOT RUN** |
| **FN-43** | Xử lý ảnh dung lượng lớn | NFR-04 | — | `TC-NF-010` | Non-functional (Memory Leak / OOM Handling) | **P3** | `DESIGNED (New)` | **NOT RUN** |
| **FN-44** | Xử lý thiết bị hết dung lượng | NFR-01 | — | `TC-NF-011` | Non-functional (Fault Injection / SQLite Full) | **P3** | `DESIGNED (New)` | **BLOCKED (Ràng buộc an toàn máy thật)** |

---

## II. ĐẶC TẢ CHI TIẾT CÁC TEST CASE BỔ SUNG MỚI (NEW TEST CASE SPECIFICATIONS)

Toàn bộ các test case bổ sung dưới đây được thiết kế theo đúng quy chuẩn IEEE 829, có đầy đủ mục tiêu, điều kiện tiên quyết, dữ liệu đầu vào, các bước thực hiện và tiêu chuẩn chấp nhận, không trùng lặp với các ID đã có trong hệ thống:

### 1. Nhóm Xác thực tài khoản & Phiên làm việc (FN-03, FN-06, FN-07)

#### `TC-BB-003C` (FN-03): Gửi lại email xác thực tài khoản (Resend Verification Email)
* **Mục tiêu kiểm thử:** Xác minh ứng dụng cho phép người dùng yêu cầu gửi lại email kích hoạt khi chưa nhận được email ban đầu.
* **Điều kiện tiên quyết:** Đang ở màn hình "Xác thực Email" sau khi vừa hoàn tất đăng ký tài khoản mới; thiết bị có kết nối mạng.
* **Dữ liệu đầu vào:** Tài khoản vừa đăng ký `new_user_<timestamp>@gmail.com`.
* **Các bước thực hiện:**
  1. Trên màn hình Xác thực Email, tìm và chạm vào nút/liên kết "Gửi lại email xác thực".
  2. Quan sát phản hồi trên giao diện và kiểm tra hộp thư đến.
* **Kết quả mong đợi:** Ứng dụng hiển thị thông báo: *"Đã gửi lại email xác thực. Vui lòng kiểm tra hộp thư."*; Firebase Auth phát sinh lệnh gửi email mới thành công; nút gửi lại có thời gian chờ (cooldown 30-60s) để tránh spam.
* **Kỹ thuật thiết kế:** Luồng tương tác giao diện (UI Interaction) & Phân lớp tương đương.
* **Mức ưu tiên:** **P2** | **Trạng thái:** `NOT RUN`.

#### `TC-BB-003D` (FN-03): Kiểm tra trạng thái kích hoạt tài khoản từ màn hình Xác thực
* **Mục tiêu kiểm thử:** Xác minh ứng dụng cập nhật trạng thái `emailVerified` khi người dùng nhấn nút xác nhận đã kích hoạt.
* **Điều kiện tiên quyết:** Đang ở màn hình Xác thực Email; người dùng đã click liên kết xác thực trong hộp thư Gmail trên trình duyệt ngoài.
* **Dữ liệu đầu vào:** Tài khoản đã click link xác nhận (`emailVerified == true` trên Firebase).
* **Các bước thực hiện:**
  1. Sau khi click link xác thực từ Gmail, quay lại ứng dụng Smart Note.
  2. Chạm vào nút "Tôi đã xác thực" hoặc "Tiếp tục".
* **Kết quả mong đợi:** Ứng dụng gọi `user.reload()`, nhận diện trạng thái `emailVerified == true`, tự động điều hướng người dùng vào màn hình Trang chủ ghi chú.
* **Kỹ thuật thiết kế:** Kiểm thử chuyển đổi trạng thái (State Transition Testing).
* **Mức ưu tiên:** **P2** | **Trạng thái:** `NOT RUN`.

#### `TC-BB-011H` (FN-06): Yêu cầu đặt lại mật khẩu với Email không tồn tại hoặc sai định dạng
* **Mục tiêu kiểm thử:** Xác minh ứng dụng xử lý an toàn và thông báo lỗi rõ ràng khi người dùng yêu cầu khôi phục mật khẩu với email không hợp lệ.
* **Điều kiện tiên quyết:** Mở hộp thoại "Quên mật khẩu?" từ màn hình Đăng nhập; thiết bị có kết nối mạng.
* **Dữ liệu đầu vào:**
  - Ca D01: Email sai cú pháp `invalid_email_format`.
  - Ca D02: Email chưa từng đăng ký `non_existent_user_999@gmail.com`.
* **Các bước thực hiện:**
  1. Nhập email theo dữ liệu D01 / D02 vào ô nhập của hộp thoại Quên mật khẩu.
  2. Nhấn nút "Gửi liên kết".
* **Kết quả mong đợi:**
  - Ca D01: Ứng dụng chặn gửi, báo lỗi: *"Định dạng email không hợp lệ."*.
  - Ca D02: Ứng dụng thông báo lỗi: *"Không tìm thấy tài khoản với email này."* hoặc thông báo an toàn, không làm crash ứng dụng.
* **Kỹ thuật thiết kế:** Phân tích giá trị biên & Ca phủ định (Negative Testing).
* **Mức ưu tiên:** **P2** | **Trạng thái:** `NOT RUN`.

#### `TC-BB-007C` (FN-07): Đăng xuất tài khoản từ màn hình Cài đặt / Hồ sơ người dùng
* **Mục tiêu kiểm thử:** Xác minh thao tác đăng xuất xóa sạch phiên làm việc cục bộ và đưa người dùng an toàn về màn hình Đăng nhập.
* **Điều kiện tiên quyết:** Người dùng đang đăng nhập hợp lệ và ở màn hình Trang chủ.
* **Dữ liệu đầu vào:** Thao tác chạm nút "Đăng xuất" trong menu Cài đặt/Hồ sơ.
* **Các bước thực hiện:**
  1. Từ Trang chủ, chạm mở Menu điều hướng (Drawer) hoặc Avatar góc trên $\rightarrow$ chọn "Cài đặt" / "Hồ sơ".
  2. Cuộn xuống cuối và chạm nút "Đăng xuất".
  3. Trên hộp thoại xác nhận "Bạn có chắc chắn muốn đăng xuất?", chọn "Đồng ý".
* **Kết quả mong đợi:** Firebase Auth hủy phiên đăng nhập (`signOut()`); toàn bộ bộ nhớ tạm phiên người dùng được giải phóng; ứng dụng điều hướng ngay lập tức về màn hình Đăng nhập; nhấn nút Back của Android không thể quay trở lại Trang chủ.
* **Kỹ thuật thiết kế:** Quản lý vòng đời phiên làm việc (Session Lifecycle Testing).
* **Mức ưu tiên:** **P1** | **Trạng thái:** `NOT RUN`.

---

### 2. Nhóm Lưu trữ & Quản lý Nhãn (FN-13, FN-14, FN-21, FN-22, FN-28)

#### `TC-BB-040` (FN-13): Chuyển ghi chú vào mục Lưu trữ (Archive Note)
* **Mục tiêu kiểm thử:** Xác minh chức năng Lưu trữ ẩn ghi chú khỏi Trang chủ và chuyển vào màn hình Archive mà không xóa dữ liệu.
* **Điều kiện tiên quyết:** Có ít nhất một ghi chú hợp lệ đang hiển thị trên Trang chủ.
* **Dữ liệu đầu vào:** Ghi chú `Note_Archive_Test_01`.
* **Các bước thực hiện:**
  1. Nhấn giữ thẻ ghi chú trên Trang chủ hoặc mở Editor $\rightarrow$ chọn biểu tượng "Lưu trữ" (Archive).
  2. Quan sát Trang chủ.
  3. Mở menu điều hướng $\rightarrow$ chọn màn hình "Lưu trữ" (Archive Screen).
* **Kết quả mong đợi:** Ghi chú biến mất khỏi danh sách Trang chủ; cờ `status` trong SQLite cập nhật thành `'archived'`; khi mở màn hình Lưu trữ, ghi chú xuất hiện đầy đủ với toàn vẹn nội dung.
* **Kỹ thuật thiết kế:** Chuyển đổi trạng thái dữ liệu (State Transition: `normal` $\rightarrow$ `archived`).
* **Mức ưu tiên:** **P2** | **Trạng thái:** `NOT RUN`.

#### `TC-BB-040B` (FN-14): Bỏ lưu trữ ghi chú (Unarchive Note)
* **Mục tiêu kiểm thử:** Xác minh khôi phục ghi chú từ màn hình Lưu trữ trở lại danh sách Trang chủ.
* **Điều kiện tiên quyết:** Có ít nhất một ghi chú đang nằm trong màn hình Lưu trữ (`ArchiveScreen`).
* **Dữ liệu đầu vào:** Ghi chú đang lưu trữ `Note_Archive_Test_01`.
* **Các bước thực hiện:**
  1. Mở màn hình Lưu trữ từ menu điều hướng.
  2. Nhấn giữ hoặc mở ghi chú $\rightarrow$ chọn biểu tượng "Bỏ lưu trữ" (Unarchive).
  3. Quay trở lại màn hình Trang chủ.
* **Kết quả mong đợi:** Ghi chú biến mất khỏi màn hình Lưu trữ; cờ `status` trở về `'normal'`; ghi chú xuất hiện trở lại trên danh sách Trang chủ tại đúng vị trí mốc thời gian cập nhật.
* **Kỹ thuật thiết kế:** Chuyển đổi trạng thái dữ liệu (State Transition: `archived` $\rightarrow$ `normal`).
* **Mức ưu tiên:** **P2** | **Trạng thái:** `NOT RUN`.

#### `TC-BB-041` (FN-21): Tạo nhãn mới trong màn hình Quản lý Nhãn (Create Tag/Label)
* **Mục tiêu kiểm thử:** Xác minh người dùng có thể tạo nhãn phân loại mới với tên và màu sắc tùy chọn.
* **Điều kiện tiên quyết:** Đang ở màn hình Trang chủ.
* **Dữ liệu đầu vào:** Tên nhãn: `"Học tập"`, chọn màu nhãn: Xanh lam.
* **Các bước thực hiện:**
  1. Mở menu điều hướng $\rightarrow$ chọn "Quản lý nhãn" (Manage Labels).
  2. Nhập tên nhãn `"Học tập"` vào ô nhập liệu $\rightarrow$ chọn màu $\rightarrow$ nhấn dấu tick (Lưu).
* **Kết quả mong đợi:** Nhãn mới xuất hiện trong danh sách nhãn; dữ liệu lưu thành công vào bảng SQLite `tags`; nhãn mới hiển thị trong danh sách lựa chọn khi soạn thảo ghi chú.
* **Kỹ thuật thiết kế:** Phân lớp tương đương & Kiểm thử CRUD.
* **Mức ưu tiên:** **P2** | **Trạng thái:** `NOT RUN`.

#### `TC-BB-041B` (FN-22): Gắn nhãn vào ghi chú và hiển thị thẻ chip nhãn
* **Mục tiêu kiểm thử:** Xác minh gán một hoặc nhiều nhãn vào ghi chú và hiển thị chip nhãn tương ứng trên thẻ Trang chủ.
* **Điều kiện tiên quyết:** Đã có sẵn nhãn `"Học tập"`; mở màn hình Editor của một ghi chú.
* **Dữ liệu đầu vào:** Chọn nhãn `"Học tập"`.
* **Các bước thực hiện:**
  1. Trong màn hình Editor, chạm vào biểu tượng "Nhãn" hoặc menu 3 chấm $\rightarrow$ chọn "Thêm nhãn".
  2. Tick chọn nhãn `"Học tập"` $\rightarrow$ nhấn Xong.
  3. Bấm Back quay về Trang chủ.
* **Kết quả mong đợi:** Trên thẻ ghi chú ở Trang chủ xuất hiện Chip nhãn nhỏ màu xanh có chữ `"Học tập"`; khi chạm vào chip nhãn hoặc tìm kiếm theo cú pháp `label:Học tập`, chỉ những ghi chú có gắn nhãn này được lọc ra.
* **Kỹ thuật thiết kế:** Tương tác dữ liệu quan hệ (Tag-Note Mapping).
* **Mức ưu tiên:** **P2** | **Trạng thái:** `NOT RUN`.

#### `TC-BB-042` (FN-28): Chuyển đổi chế độ hiển thị Trang chủ (Toggle Grid / List View)
* **Mục tiêu kiểm thử:** Xác minh chuyển đổi linh hoạt giữa giao diện lưới 2 cột (Staggered Grid) và danh sách 1 cột (List View).
* **Điều kiện tiên quyết:** Trang chủ có ít nhất 4 ghi chú với độ dài nội dung khác nhau.
* **Dữ liệu đầu vào:** Thao tác chạm biểu tượng Grid/List trên AppBar.
* **Các bước thực hiện:**
  1. Quan sát bố cục hiện tại trên Trang chủ (mặc định là lưới 2 cột).
  2. Chạm vào biểu tượng chuyển đổi chế độ xem trên AppBar.
  3. Quan sát giao diện chuyển sang danh sách 1 cột.
  4. Chạm lại biểu tượng một lần nữa để quay về dạng lưới.
* **Kết quả mong đợi:** Giao diện chuyển đổi mượt mà không bị giật hay vỡ layout; trạng thái hiển thị được lưu lại trong `SharedPreferences` để duy trì khi mở lại app.
* **Kỹ thuật thiết kế:** Kiểm thử giao diện và độ khả dụng (Usability & Layout Integrity).
* **Mức ưu tiên:** **P3** | **Trạng thái:** `NOT RUN`.

---

### 3. Nhóm Trợ lý Gemini AI (FN-31, FN-32, FN-33)

#### `TC-BB-032` (FN-31): Tóm tắt nội dung ghi chú bằng Trợ lý Gemini AI
* **Mục tiêu kiểm thử:** Xác minh tính năng gọi API Gemini AI để tạo đoạn tóm tắt ngắn từ văn bản ghi chú dài.
* **Điều kiện tiên quyết:** Thiết bị có kết nối mạng ổn định; mở Editor một ghi chú có nội dung văn bản dài (> 100 từ).
* **Dữ liệu đầu vào:** Văn bản cuộc họp 200 từ.
* **Các bước thực hiện:**
  1. Trong màn hình Editor, chạm vào biểu tượng Trợ lý AI (ngôi sao lấp lánh).
  2. Chọn tính năng "Tóm tắt ghi chú" (Summarize).
  3. Quan sát tiến trình loading và kết quả trả về.
* **Kết quả mong đợi:** Hiển thị shimmer loading trong khi chờ model phản hồi; sau 3-5 giây, xuất hiện hộp thoại/bottom sheet hiển thị đoạn tóm tắt súc tích; cung cấp nút "Chèn vào ghi chú" hoặc "Sao chép". Nếu lỗi mạng, hiển thị thông báo thân thiện bắt lỗi từ `_friendlyAiError`.
* **Kỹ thuật thiết kế:** Kiểm thử tích hợp AI (AI Service Integration).
* **Mức ưu tiên:** **P2** | **Trạng thái thiết kế mới:** `NOT RUN` *(Chưa có evidence thực thi riêng cho mã `TC-BB-032`; lịch sử thực thi Kịch bản 5 của `FN-31` đang `BLOCKED` do lỗi service UI máy thật)*.

#### `TC-BB-032B` (FN-32): Đề xuất tiêu đề tự động bằng Gemini AI
* **Mục tiêu kiểm thử:** Xác minh Gemini AI đọc nội dung ghi chú và đề xuất tiêu đề phù hợp khi tiêu đề đang để trống.
* **Điều kiện tiên quyết:** Mở ghi chú có nội dung chi tiết nhưng ô Tiêu đề để trống; có kết nối mạng.
* **Dữ liệu đầu vào:** Nội dung về danh sách đồ dùng cần mua cho chuyến dã ngoại.
* **Các bước thực hiện:**
  1. Chạm biểu tượng Gemini AI $\rightarrow$ chọn "Gợi ý tiêu đề" (Suggest Title).
  2. Quan sát kết quả.
* **Kết quả mong đợi:** Trả về 2-3 gợi ý tiêu đề ngắn gọn liên quan (ví dụ: *"Kế hoạch dã ngoại"*); người dùng chạm vào gợi ý nào thì tiêu đề đó được tự động điền vào ô Tiêu đề ghi chú.
* **Kỹ thuật thiết kế:** Kiểm thử tích hợp AI & Tiện ích thông minh.
* **Mức ưu tiên:** **P2** | **Trạng thái thiết kế mới:** `NOT RUN` *(Chưa có evidence thực thi riêng cho mã `TC-BB-032B`; lịch sử thực thi Kịch bản 5 của `FN-32` đang `BLOCKED` do lỗi service UI máy thật)*.

#### `TC-BB-032C` (FN-33): Bóc tách nội dung văn bản thành Checklist việc cần làm
* **Mục tiêu kiểm thử:** Xác minh Gemini AI phân tích đoạn văn bản thô và tự động chuyển đổi thành các mục việc cần làm (Checklist to-do items).
* **Điều kiện tiên quyết:** Ghi chú có nội dung mô tả các công việc cần làm dạng văn xuôi; có kết nối mạng.
* **Dữ liệu đầu vào:** Văn bản: `"Hôm nay cần chuẩn bị báo cáo kiểm thử, gửi email cho giảng viên và họp nhóm lúc 3 giờ chiều."`
* **Các bước thực hiện:**
  1. Chạm biểu tượng Gemini AI $\rightarrow$ chọn "Tạo Checklist công việc".
  2. Quan sát kết quả bóc tách.
* **Kết quả mong đợi:** AI phân tích và trả về danh sách các checkbox riêng biệt: `[ ] Chuẩn bị báo cáo kiểm thử`, `[ ] Gửi email cho giảng viên`, `[ ] Họp nhóm lúc 3h chiều`; cho phép người dùng xác nhận chuyển đổi toàn bộ ghi chú sang định dạng Checklist.
* **Kỹ thuật thiết kế:** Xử lý ngôn ngữ tự nhiên (NLP / Transformation Testing).
* **Mức ưu tiên:** **P2** | **Trạng thái thiết kế mới:** `NOT RUN` *(Chưa có evidence thực thi riêng cho mã `TC-BB-032C`; lịch sử thực thi Kịch bản 5 của `FN-33` đang `BLOCKED` do lỗi service UI máy thật)*.

---

### 4. Nhóm Đa phương tiện & Tiện ích nâng cao (FN-34, FN-35, FN-36, FN-37, FN-38, FN-39)

#### `TC-BB-034` (FN-34): Xuất nội dung ghi chú thành tệp PDF (Export to PDF)
* **Mục tiêu kiểm thử:** Xác minh chuyển đổi toàn bộ tiêu đề, nội dung rich-text và hình ảnh thành tài liệu định dạng PDF chuẩn.
* **Điều kiện tiên quyết:** Đang mở một ghi chú có đầy đủ Tiêu đề, Nội dung và ngày tạo.
* **Dữ liệu đầu vào:** Thao tác chọn "Xuất PDF" trong menu tùy chọn của Editor.
* **Các bước thực hiện:**
  1. Mở ghi chú $\rightarrow$ chạm menu 3 chấm góc phải AppBar.
  2. Chọn "Xuất PDF".
  3. Quan sát màn hình xem trước bản in (Print Preview).
* **Kết quả mong đợi:** Thư viện `pdf` biên dịch thành công; màn hình xem trước bản in hiển thị chính xác tiêu đề, nội dung văn bản có căn lề chuẩn, font tiếng Việt không bị lỗi font (Unicode UTF-8); cho phép lưu tệp vào thư mục `Download` của máy.
* **Kỹ thuật thiết kế:** Kiểm thử xuất định dạng tài liệu (Document Export & Rendering).
* **Mức ưu tiên:** **P2** | **Trạng thái:** `NOT RUN`.

#### `TC-BB-035` (FN-35): Vẽ tay trên Bảng vẽ và đính kèm nét vẽ vào ghi chú (Drawing Board)
* **Mục tiêu kiểm thử:** Xác minh người dùng vẽ tự do trên màn hình Drawing, hỗ trợ đổi màu/nét bút và lưu ảnh đính kèm vào ghi chú.
* **Điều kiện tiên quyết:** Đang ở màn hình Editor của ghi chú.
* **Dữ liệu đầu vào:** Nét vẽ tự do bằng ngón tay màu đỏ, nét dày 4px.
* **Các bước thực hiện:**
  1. Trong Editor, chạm biểu tượng Bút vẽ (Drawing) trên thanh công cụ.
  2. Vẽ một hình minh họa bất kỳ trên canvas.
  3. Chạm nút "Lưu" (Save Drawing).
  4. Quan sát Editor.
* **Kết quả mong đợi:** Ứng dụng xuất nét vẽ thành tệp ảnh PNG cục bộ; ảnh vẽ tay xuất hiện ngay lập tức trong vùng nội dung của Editor; thẻ ghi chú ngoài Trang chủ hiển thị thumbnail nét vẽ.
* **Kỹ thuật thiết kế:** Tương tác đồ họa cảm ứng (Touch Drawing & Canvas Export).
* **Mức ưu tiên:** **P2** | **Trạng thái:** `NOT RUN`.

#### `TC-BB-036` (FN-36): Đính kèm hình ảnh từ Thư viện và xử lý tải lên Cloudinary
* **Mục tiêu kiểm thử:** Xác minh chọn ảnh từ thư viện thiết bị, hiển thị thanh tiến độ tải lên và bắt lỗi timeout an toàn khi mạng yếu (Xác minh bug `BUG-001`).
* **Điều kiện tiên quyết:** Đang mở Editor; thiết bị có kết nối mạng Internet.
* **Dữ liệu đầu vào:** 1 tệp ảnh định dạng JPG dung lượng 2MB từ thư viện ảnh máy.
* **Các bước thực hiện:**
  1. Chạm biểu tượng Đính kèm ảnh $\rightarrow$ chọn ảnh từ thư viện.
  2. Quan sát thanh tiến trình tải lên (Upload Progress Bar).
  3. Giả lập ngắt kết nối mạng giữa chừng khi ảnh đang tải.
* **Kết quả mong đợi:** Khi có mạng: Ảnh tải lên Cloudinary thành công, nhận URL trả về và nhúng vào ghi chú. Khi mất mạng: Ứng dụng phải có cơ chế Timeout (30s) và hiển thị thông báo lỗi thân thiện thay vì bị treo đơ vĩnh viễn (kiểm tra khắc phục `BUG-001`).
* **Kỹ thuật thiết kế:** Kiểm thử tải lên mạng & Bắt lỗi ngoại lệ (Network Resilience).
* **Mức ưu tiên:** **P1** | **Trạng thái:** `NOT RUN` (Dành cho Retest `BUG-001`).

#### `TC-BB-037` (FN-37): Đổi màu nền ghi chú từ Bảng màu (Note Color Palette)
* **Mục tiêu kiểm thử:** Xác minh chọn màu nền cho ghi chú và đảm bảo màu nền hiển thị đồng nhất ở cả Editor và Trang chủ.
* **Điều kiện tiên quyết:** Đang mở một ghi chú trong Editor.
* **Dữ liệu đầu vào:** Chọn màu Vàng pastel (`#FFF9C4`) từ bảng màu.
* **Các bước thực hiện:**
  1. Chạm vào biểu tượng Bảng màu trên thanh công cụ Editor.
  2. Chọn màu Vàng pastel từ danh mục các màu có sẵn.
  3. Quan sát màu nền Editor thay đổi.
  4. Thoát về Trang chủ và quan sát thẻ ghi chú.
* **Kết quả mong đợi:** Nền của màn hình Editor và thẻ ghi chú trên Trang chủ lập tức chuyển sang màu Vàng pastel; màu chữ và icon tự động điều chỉnh độ tương phản để đảm bảo dễ đọc; giá trị màu lưu bền vững vào trường `note_color` của SQLite.
* **Kỹ thuật thiết kế:** Giao diện người dùng & Độ tương phản trực quan (Visual & Usability).
* **Mức ưu tiên:** **P3** | **Trạng thái:** `NOT RUN`.

#### `TC-BB-038` (FN-38): Thiết lập thông báo nhắc nhở theo thời gian (Schedule Reminder)
* **Mục tiêu kiểm thử:** Xác minh thiết lập ngày và giờ nhắc nhở cho ghi chú thông qua hộp thoại chọn ngày/giờ hệ thống.
* **Điều kiện tiên quyết:** Đang ở màn hình Editor; thiết bị đã cấp quyền thông báo (`POST_NOTIFICATIONS`).
* **Dữ liệu đầu vào:** Thiết lập nhắc nhở vào thời điểm 5 phút sau thời điểm hiện tại.
* **Các bước thực hiện:**
  1. Trong Editor, chạm biểu tượng Chiếc chuông (Nhắc nhở).
  2. Chọn ngày hôm nay và chọn giờ: hiện tại + 5 phút.
  3. Nhấn "Lưu nhắc nhở" $\rightarrow$ bấm Back về Trang chủ.
* **Kết quả mong đợi:** Thẻ ghi chú hiển thị chip nhắc nhở có icon chuông kèm thời gian hẹn; dịch vụ `ReminderService` đăng ký thành công một notification ID với hệ điều hành Android qua `flutter_local_notifications`.
* **Kỹ thuật thiết kế:** Lập lịch sự kiện thời gian thực (Scheduled Event Testing).
* **Mức ưu tiên:** **P2** | **Trạng thái:** `NOT RUN`.

#### `TC-BB-039` (FN-39): Chạm thông báo nhắc nhở mở chính xác ghi chú tương ứng
* **Mục tiêu kiểm thử:** Xác minh khi hệ điều hành kích hoạt thông báo nhắc nhở, người dùng chạm vào thông báo thì ứng dụng tự khởi động và mở đúng ghi chú.
* **Điều kiện tiên quyết:** Đã thiết lập nhắc nhở (từ `TC-BB-038`); ứng dụng đang tắt hoàn toàn hoặc chạy ngầm.
* **Dữ liệu đầu vào:** Thông báo nhắc nhở hiển thị trên khay thông báo Android với Tiêu đề và Nội dung ghi chú.
* **Các bước thực hiện:**
  1. Chờ đến đúng giờ hẹn thông báo.
  2. Kéo thanh thông báo của Android xuống, quan sát banner thông báo của Smart Note.
  3. Chạm trực tiếp vào banner thông báo.
* **Kết quả mong đợi:** Ứng dụng tự động mở lên, điều hướng thẳng qua màn hình Editor của chính xác ghi chú đã đặt nhắc nhở đó (Payload matching); nếu ghi chú đang bị khóa sinh trắc học thì yêu cầu quét vân tay trước khi hiển thị nội dung.
* **Kỹ thuật thiết kế:** Kiểm thử điều hướng Intent / Deep Link nội bộ (Notification Action Flow).
* **Mức ưu tiên:** **P2** | **Trạng thái:** `NOT RUN`.

---

## III. KIỂM KÊ TEST SUITE ĐA CHIỀU (MULTI-DIMENSIONAL TEST SUITE INVENTORY)

Nhằm đáp ứng yêu cầu phân định minh bạch các loại kiểm thử, toàn bộ tài nguyên kiểm thử của dự án được phân loại theo bảng dưới đây:

### 1. Kiểm thử Hộp trắng (White-box Testing Suite)
* **Các Unit Test đã có mã thực thi và có bằng chứng PASS (18 tests baseline):**
  - `test/checklist_test.dart`: 5 tests PASS (`ChecklistItem` defaults, custom, JSON serialization, plain text extraction).
  - `test/checklist_copy_with_test.dart`: 4 tests PASS (`copyWith` immutability, field update, checked toggle).
  - `test/note_model_test.dart`: 9 tests PASS (`toMap`/`fromMap` roundtrip, null/default fallback, camelCase fallback, CSV/JSON decoding, boolean parser).
  - *Bằng chứng đối chiếu:* `evidence/white_box/note_model_run_20261010_0945/test_execution.log`.
* **Các bài test Firestore Security Rules đã có mã thực thi (8 tests PASS — Truy vết `REQ-11 / NFR-03 / FN-40`):**
  - `test/security_rules_test.dart`: 8 tests PASS (xác thực cô lập dữ liệu người dùng `users/{userId}/notes` theo `NFR-03`, đối ứng `TC-WB-011..014` và `TC-NF-006`).
* **Các Test Case Hộp trắng ở mức Thiết kế (Chưa chạy mã - 22 test cases):**
  - `TC-WB-001` .. `TC-WB-005` (AuthProvider logic trong `test_cases/white_box/white_box_test_cases.md`).
  - `TC-WB-006` .. `TC-WB-010` (CloudinaryService logic trong `test_cases/white_box/white_box_test_cases.md`: `TC-WB-006, 007` kiểm thử `_extractPublicId` phục vụ `deleteFile` — ánh xạ chính `REQ-09 / FN-12`, ánh xạ phụ `REQ-12 / FN-35, 36`; `TC-WB-008..010` kiểm thử `uploadImage` — ánh xạ `REQ-12 / FN-35, 36`).
  - `TC-WB-011` .. `TC-WB-014` (Security Rules logic trong `test_cases/white_box/white_box_test_cases.md` — truy vết `REQ-11 / NFR-03 / FN-40`).
  - `TC-WB-015` .. `TC-WB-022` (8 ca mở rộng trong `docs/plan_and_requirements/white_box_test_plan.md`: đếm checklist `pendingChecklistCount`, bóc tách Quill Delta `plainTextContent`, cờ `clearReminder`, sinh `updatedAt`, fallback SQLite thiếu thời gian, so sánh mốc LWW bộ nhớ).

### 2. Kiểm thử Tự động hóa (Automation Testing Suite)
* **Kịch bản tự động đã có mã nguồn trong `automation/tests/`:**
  - `test_fn02_register.py` (AT-01 đến AT-10: 10 kịch bản bao phủ đăng ký tài khoản).
  - `test_fn04_login.py` (AT-11 đến AT-20: 10 kịch bản bao phủ đăng nhập).
  - `test_fn05_google_oauth.py` (Kịch bản hủy account picker).
  - `test_fn08_create_note.py` (Tự động hóa luồng tạo ghi chú).
  - `test_fn09_edit_note.py` (Tự động hóa luồng sửa ghi chú).
  - `test_fn20_pin_note.py` (Tự động hóa kiểm tra vị trí ghi chú ghim).
  - `test_fn23_search.py` (Tự động hóa chuỗi tìm kiếm từ khóa SQL LIKE).
  - `test_fn29_30_biometric.py` (Tự động hóa kích hoạt khóa ghi chú).
* **Trạng thái thực thi tự động hóa:** Các ca smoke/regression test đã được chạy thực tế trong Phase 4 và lưu báo cáo tại `docs/qa/phase_4_automation_execution_report.md`.

### 3. Kiểm thử Phi chức năng (Non-Functional Testing Suite)
Toàn bộ 11 kịch bản phi chức năng trong `test_cases/non_functional/non_functional_test_cases.md`:
* **Đã thiết kế & Có bằng chứng xác minh (3 ca):**
  - `TC-NF-006` (Bảo mật cô lập dữ liệu người dùng — `NFR-03`) $\rightarrow$ Đạt qua Security Rules test suite (`test/security_rules_test.dart` & `TC-WB-011..014`).
  - `TC-NF-007` (Độ bền nhập liệu payload SQL Injection `' OR '1'='1`) $\rightarrow$ Đạt qua `TC-BB-029` trong `fn23_execution_sheet.md`.
  - `TC-NF-008` (Khả năng chịu lỗi timeout mạng) $\rightarrow$ Đã phát hiện và ghi nhận lỗi `BUG-001`.
* **Đã thiết kế & Chưa thực thi / Chờ điều kiện (8 ca):**
  - `TC-NF-001` (Hiệu năng tìm kiếm < 500ms khi có 100+ ghi chú) $\rightarrow$ `NOT RUN`.
  - `TC-NF-002` (Độ trễ autosave < 300ms khi nội dung dài 2.000 từ) $\rightarrow$ `NOT RUN`.
  - `TC-NF-003` (Độ tin cậy Offline-First khi mất mạng đột ngột) $\rightarrow$ `NOT RUN`.
  - `TC-NF-004` (Độ tin cậy tự khôi phục Offline-to-Online Sync) $\rightarrow$ `NOT RUN`.
  - `TC-NF-005` (Tự động khóa bảo mật khi app vào background > 30s) $\rightarrow$ `NOT RUN`.
  - `TC-NF-009` (Tải nội dung văn bản cực lớn 50.000 ký tự - FN-42) $\rightarrow$ `NOT RUN`.
  - `TC-NF-010` (Đính kèm và nén an toàn hình ảnh dung lượng lớn 15MB - FN-43) $\rightarrow$ `NOT RUN`.
  - `TC-NF-011` (Xử lý an toàn khi bộ nhớ thiết bị cạn kiệt < 1MB - FN-44) $\rightarrow$ `BLOCKED` (Do ràng buộc an toàn thiết bị thật).

---

## IV. BẢO TOÀN BASELINE VÀ CÁC ĐIỂM CHỜ XÁC NHẬN (BASELINE & OPEN ISSUES)

1. **Bảo toàn kết quả kiểm thử Hộp đen:**
   - 140 execution items chính thức trên 11 nhóm có execution sheet: **131 PASS, 6 FAIL, 2 giải tỏa theo BR, 1 BLOCKED**.
   - 8 lỗi phần mềm trong `docs/bugs/defect_log.md` (`BUG-001` đến `BUG-005`, `BUG-FN02-01`, `BUG-BB-002`, `BUG-BB-003`) giữ nguyên hiện trạng `OPEN`.
2. **Quy tắc phân xử hòa timestamp BR-03 (Tie-break Rule):**
   - Tiếp tục giữ nguyên trạng thái **`NEEDS CONFIRMATION`**.
   - Không tự ý áp đặt quy tắc Cloud thắng hay Local thắng; chờ quyết định chính thức từ Product Owner / Giảng viên hướng dẫn.
3. **Các ca BỊ CHẶN (BLOCKED Cases):**
   - `TC-BB-015G-D01` (FN-30): Bị chặn vĩnh viễn do nguyên tắc bảo vệ phần cứng máy thật của tester.
   - `FN-31, FN-32, FN-33` (Gemini AI): Lịch sử thực thi Kịch bản 5 trên máy thật ghi nhận **3 trường hợp `BLOCKED`** do lỗi service hiển thị khung đỏ trên UI (nguyên nhân gốc chưa xác định do thiếu log HTTP); 3 ca thiết kế chính thức mới (`TC-BB-032`, `TC-BB-032B`, `TC-BB-032C`) giữ trạng thái **`NOT RUN` (Chờ gỡ `BLOCKED` của dịch vụ Gemini AI)**.
   - `FN-44` (`TC-NF-011`): Bị chặn do nguyên tắc không làm đầy bộ nhớ máy thật; chỉ thực thi khi có máy ảo sandbox.
