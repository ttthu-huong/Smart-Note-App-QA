# MA TRẬN TRUY VẾT YÊU CẦU KIỂM THỬ (REQUIREMENTS TRACEABILITY MATRIX - RTM)
## Dự án: Smart Note App
**Mục tiêu:** Ánh xạ hai chiều giữa Yêu cầu Nghiệp vụ / Yêu cầu Kỹ thuật (Requirements) với các Kịch bản kiểm thử Hộp đen, Hộp trắng, Tự động hóa và Phi chức năng
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Traceability Management

---

## 1. BẢNG MA TRẬN TRUY VẾT YÊU CẦU CHI TIẾT (REQUIREMENTS TRACEABILITY MATRIX)

| Mã Yêu cầu (REQ-ID) | Mô tả Yêu cầu hệ thống / Nghiệp vụ | Mã Test Case ánh xạ (Test Case IDs) | Loại kiểm thử (Test Type) | Trạng thái Đặc tả & Thiết k| **REQ-01** | **Đăng ký tài khoản mới** (Xác thực email, validate, lọc domain rác, cắt khoảng trắng, gửi email xác minh) | `TC-BB-001` .. `005` (19 items FN-02), `test_fn02_register.py`, `test/unit/auth/auth_provider_test.dart` (18 tests PASS, gồm 3 ca lọc domain rác phái sinh từ dung); `TC-BB-003C`, `003D` `[NOT RUN]` (FN-03) | Black-box / White-box / Auto | `DESIGNED` | **18 PASS / 1 FAIL** (Hộp đen `BUG-FN02-01`) + **18 PASS** (White-box contract & domain test); 2 ca mới `NOT RUN` | `evidence/fn02/`, `evidence/white_box/run_wb_final_closure_20261011_2330/` |
| **REQ-02** | **Đăng nhập hệ thống & Đăng xuất** (Email/Password, Google OAuth, trim khoảng trắng, case-insensitive email, chuyển hướng chưa verify, đăng xuất) | `TC-BB-006` .. `009G` (16 items FN-04), `TC-BB-010` .. `011G` (8 items FN-05), `test_fn04_login.py`, `test_fn05_google_oauth.py`, `TC-BB-007C` `[NOT RUN]` | Black-box / Auto | `DESIGNED` | **22 PASS / 2 FAIL** (`BUG-BB-002`, `003`) + **1 Evidence PASS** (FN-07); 1 ca mới `NOT RUN` | `evidence/fn04/`, `evidence/fn05/`, `auth01_logged_out.png` |
| **REQ-03** | **Quên & Đặt lại mật khẩu** (Gửi email khôi phục mật khẩu qua Firebase Auth) | `TC-BB-009E`, `TC-BB-011` .. `011C`, `TC-BB-011H` `[NOT RUN]` | Black-box / Manual | `DESIGNED` | **4 PASS / 0 FAIL** (100% PASS đã chạy); 1 ca mới `NOT RUN` | `evidence/fn05/FN05_TC-BB-011_D01_01.png`, `02.png` |
| **REQ-04** | **Tạo ghi chú mới & Tự động lưu** (Tạo ghi chú văn bản, checklist, tự động lưu SQLite, hủy bản nháp rỗng) | `TC-BB-016` .. `018F` (8 items FN-08), `test/unit/note/note_model_test.dart` (12 tests), `test/unit/note/note_model_whitebox_test.dart` (14 tests), `test/unit/note/note_parsing_defect_test.dart` (50 tests: 46 PASS / 4 FAIL `DEFECT-WB-01..04`) | Black-box / White-box / Auto | `DESIGNED` | **8 PASS / 0 FAIL** (Hộp đen) + **72 PASS / 4 FAIL** (White-box: `DEFECT-WB-01..04` phát hiện lỗi parsing/type robustness) | `evidence/fn08/`, `evidence/white_box/run_wb_final_closure_20261011_2330/` |
| **REQ-05** | **Chỉnh sửa Rich-text & Cập nhật ghi chú** (Rich-text, cập nhật `updatedAt`, tự động lưu thời gian thực, lưu khi back) | `TC-BB-019` .. `020D` (12 items FN-09), `test_fn09_edit_note.py` | Black-box / Auto | `DESIGNED` | **12 PASS / 0 FAIL** (1 Glitch `BUG-005`) | `evidence/fn09/`, video `overflow_th1.mp4` |
| **REQ-06** | **Quản lý Checklist** (Thêm mục, tick hoàn thành, bỏ tick, xóa mục, toàn vẹn checkbox) | `TC-BB-CHK-01` .. `06` (6 items FN-15..19), `test/unit/note/checklist_model_test.dart` (5 tests), `test/unit/note/checklist_copy_with_test.dart` (5 tests), `test/unit/note/checklist_whitebox_test.dart` (1 test UUID) | Black-box / White-box | `DESIGNED` | **6 PASS / 0 FAIL** (Hộp đen) + **11 PASS / 0 FAIL** (White-box Models) | `evidence/fn15_19_run_20261011_0005/`, `evidence/white_box/run_wb_final_closure_20261011_2330/` |
| **REQ-07** | **Ghim ghi chú (Pin Note)** (Ghim/bỏ ghim, tự động gom nhóm hiển thị lên đầu Trang chủ) | `TC-BB-024` .. `025F` (15 items FN-20), `test_fn20_pin_note.py`, `test_fn20_extended.py`, Provider `PV-REF-01`, `02` | Black-box / Auto | `DESIGNED` | **15 PASS / 0 FAIL** (UI Auto) + **2 PASS** (Provider) | `evidence/fn20/` (15 items xác minh: 2 baseline + 13 mở rộng Phase 4 có JUnit XML & ảnh chụp) |
| **REQ-08** | **Tìm kiếm & Bộ lọc ghi chú** (Từ khóa tiêu đề/nội dung SQL LIKE khớp có dấu theo `BR-01`, highlight, chip: `has:url`, `has:image`, `has:audio`, `has:list`, `is:pinned`, `is:archived`, `label`, loại trừ Thùng rác) | `TC-BB-026` .. `029` (22 items FN-23), `test_fn23_search.py`, `test_fn23_extended.py`, `test/unit/search/search_notes_whitebox_test.dart` (15 tests: 14 PASS / 1 FAIL `BUG-004`), Provider `PV-REF-08..10` (3 PASS) | Black-box / White-box / Auto | `DESIGNED` *(Đã chốt `BR-01`)* | **15 PASS / 1 FAIL / 1 BR-01 / 1 BLOCKED** (UI Auto: 18 items) + **4 PASS** (Manual lịch sử) + **14 PASS / 1 FAIL** (White-box: xác nhận triệt để `BUG-004` không parse token `has:list`) | `evidence/fn23/`, `evidence/white_box/run_wb_final_closure_20261011_2330/` |
| **REQ-09** | **Quản lý Thùng rác & Lưu trữ (Trash & Archive)** (Xóa mềm vào Trash, khôi phục, xóa vĩnh viễn, dọn rác 7 ngày, chuyển vào Archive và bỏ lưu trữ) | • **Trash (FN-10..12):** `TC-BB-021` .. `023C` (12 items), `test/unit/note/note_trash_lifecycle_test.dart` (17 tests: 15 PASS / 2 FAIL `DEFECT-WB-TRASH-01`, `DEFECT-WB-TRASH-02`)<br>• **Archive (FN-13..14):** `TC-BB-040`, `040B`, `EXT-006`, `EXT-007`, `EXT-008` (5 items: 5 PASS, `test_fn13_fn14_archive.py`), `arc01`, `arc02`, Provider `PV-REF-03`, `04` (2 PASS) | Black-box / White-box / Auto | `DESIGNED` | **12 PASS / 0 FAIL** (Hộp đen Trash) + **5 PASS / 0 FAIL** (UI Auto Archive) + **15 PASS / 2 FAIL** (White-box Trash: leak Cloudinary `TRASH-01` & reminder `TRASH-02`) | `evidence/fn10_11_12/`, `evidence/fn13_14/`, `evidence/white_box/run_wb_final_closure_20261011_2330/` |
| **REQ-10** | **Bảo mật sinh trắc học** (Khóa ghi chú riêng tư bằng vân tay/FaceID, tự động khóa khi vào background AppLifecycle) | `TC-BB-012` .. `015G` (12 items), `test_fn29_30_biometric.py`, `TC-NF-005` `[NOT RUN]` | Black-box / Auto / Non-functional | `DESIGNED` *(White-box unit mock bị BLOCKED do `BiometricService` thiếu DI constructor)* | **11 PASS / 0 FAIL / 1 BLOCKED** (`TC-BB-015G-D01` an toàn vân tay); `TC-NF-005`: `NOT RUN` | `evidence/fn29_30/` |
| **REQ-11** | **Đồng bộ Offline-First & Giải quyết xung đột LWW** (Lưu cục bộ khi offline, sync nền khi có mạng, phân xử LWW theo `updatedAt`, cô lập Firestore rules `NFR-03`) | `TC-BB-030` .. `031D` (10 items FN-40/41), `test/security/security_rules_test.dart` (15 tests PASS), `test/unit/sync/lww_timestamp_reference_test.dart` (7 tests PASS: LWW in-memory & reconciliation rules) | Black-box / White-box / Non-functional | `DESIGNED` *(Đã chốt `BR-02`; `BR-03` `NEEDS CONFIRMATION`)* | **7 PASS / 2 FAIL** (`BUG-002`, `003`) + **22 PASS** (15 Security Rules simulation + 7 LWW Decision tests) | `evidence/fn40_41_run_20261010_2125/`, `evidence/white_box/run_wb_final_closure_20261011_2330/` |
| **REQ-12** | **Tiện ích bổ trợ** (Nhãn dán, Xuất PDF, Vẽ tay, Tải ảnh Cloudinary, Đổi màu, Layout Grid/List, Lập lịch nhắc nhở) | • **Evidence:** `tag01/02`, `fn28`, `pdf01`, `draw01`, `image_note_home.png` (`BUG-001`), `fn37`, `rem01/02`<br>• **White-box:** `test/unit/services/cloudinary_whitebox_test.dart` (2 tests PASS - guard checks), `test/widget/empty_state_widget_test.dart` (2 tests PASS) | Black-box / White-box / Manual | `DESIGNED` | **10 Evidence PASS / 0 FAIL** (riêng FN-36 có `BUG-001`) + **4 White-box PASS** (2 Cloudinary guards + 2 EmptyState widget) | `evidence/fn13_14_21_22_run_20261011_0055/`, `evidence/white_box/run_wb_final_closure_20261011_2330/` |
| **REQ-13** | **Trợ lý thông minh Gemini AI** (Tóm tắt, gợi ý tiêu đề, bóc tách checklist) | • **Lịch sử thực thi:** Kịch bản 5 (`Testing_Report.md` / `black_box_execution_summary.md`)<br>• **Thiết kế mới:** `TC-BB-032` (FN-31), `TC-BB-032B` (FN-32), `TC-BB-032C` (FN-33) `[NOT RUN — Chờ gỡ BLOCKED]` | Black-box / Integration | `DESIGNED` | **Lịch sử Kịch bản 5: 3 BLOCKED** (lỗi UI máy thật); **3 ca mới (`TC-BB-032, 032B, 032C`): `NOT RUN`** (chưa có evidence riêng) | `black_box_execution_summary.md` |

---

## 2. THỐNG KÊ MỨC ĐỘ TRUY VẾT YÊU CẦU (REQUIREMENTS COVERAGE METRICS)

* **Tổng số Yêu cầu hệ thống (Total System Requirements)**: 13 Yêu cầu (REQ-01 đến REQ-13 theo Condensed SRS v1.0).
* **Tỷ lệ Yêu cầu đã được bao phủ bởi Test Cases (Test Design Coverage)**: **100%** (13/13 REQ đều có test cases ánh xạ trực tiếp).
* **Tỷ lệ Yêu cầu đã thực thi (Execution Coverage)**: **92,31%** (12/13 REQ đã có kết quả thực thi thực tế; REQ-13 chưa hoàn tất do các ca kiểm thử đang ở trạng thái BLOCKED / NOT RUN).


## 3. CẬP NHẬT TRUY VẾT AUTOMATION PHASE 2 — 20/10/2026

| Requirement | Chức năng | Automation execution | Trạng thái |
|---|---|---|---|
| REQ-04 | FN-08 — Tạo ghi chú | 8/8 PASS (3 baseline + 5 mở rộng) | Đã đối chiếu đầy đủ JUnit XML & Evidence |
| REQ-05 | FN-09 — Chỉnh sửa/Auto-save | 12/12 PASS (12 execution items mở rộng) | Đã đối chiếu 12 JUnit XML & Evidence; BUG-005 vẫn OPEN |
| REQ-09 | FN-10 — Chuyển vào Thùng rác | 5/5 PASS (1 baseline + 4 mở rộng) | Hoàn thành nhóm test (TC-BB-021B có evidence, chờ XML riêng) |
| REQ-09 | FN-11 — Khôi phục | 2 PASS, 1 BLOCKED (1 baseline + 1 mở rộng PASS, 1 BLOCKED) | TC-BB-022C D01 BLOCKED (chờ Trash rỗng để retest) |
| REQ-09 | FN-12 — Xóa vĩnh viễn | 4/4 PASS (1 baseline + 3 mở rộng) | Hoàn thành nhóm test (gồm kiểm tra bền vững TC-BB-023C) |

**Lưu ý:** Kết quả automation REQ-09 không thay thế kết quả Black-box thủ công, White-box hoặc các hạng mục Archive chưa thực thi. TC-BB-023C D01 kiểm tra tính bền vững vòng đời ghi chú và có liên quan đến FN-10, FN-11, FN-12.


## 4. CẬP NHẬT TRUY VẾT AUTOMATION PHASE 3 — 20/10/2026

| Requirement | Chức năng | Automation execution | Trạng thái |
|---|---|---|---|
| REQ-09 | FN-13 — Lưu trữ ghi chú (Archive Note) | 3/3 PASS (TC-BB-040 D01, EXT-006 D01, EXT-008 D01) | Đã đối chiếu đầy đủ JUnit XML & Evidence |
| REQ-09 | FN-14 — Bỏ lưu trữ ghi chú (Unarchive Note) | 2/2 PASS (TC-BB-040B D01, EXT-007 D01) | Đã đối chiếu đầy đủ JUnit XML & Evidence (040B retry PASS sau khi chỉnh precondition) |

**Lưu ý REQ-09:**
- Phân hệ Lưu trữ (FN-13 & FN-14) của REQ-09 đã hoàn thành tự động hóa 100% với 5/5 execution items PASS trên thiết bị thật.
- Kết hợp Phase 2 (Thùng rác: 11 PASS, 1 BLOCKED) và Phase 3 (Lưu trữ: 5 PASS), toàn bộ yêu cầu **REQ-09 đạt 16 items PASS / 1 BLOCKED / 0 FAIL** trên 17 execution items tự động hóa UI/E2E.
- Kết quả automation không thay thế các bộ test White-box hoặc bằng chứng thủ công trước đây.

## 5. CẬP NHẬT TRUY VẾT AUTOMATION PHASE 4 — 20/10/2026

| Requirement | Chức năng | Automation execution | Trạng thái |
|---|---|---|---|
| REQ-07 | FN-20 — Ghim và Bỏ ghim ghi chú (Pin/Unpin Note) | 15/15 PASS (2 baseline + 13 mở rộng Phase 4) | Đã đối chiếu đầy đủ JUnit XML & Evidence trên thiết bị thật |

**Lưu ý REQ-07:**
- Toàn bộ yêu cầu **REQ-07 (Ghim ghi chú)** đã hoàn thành tự động hóa 100% với **15/15 execution items PASS** trên thiết bị thật (bao gồm Editor, Batch Pin/Unpin, phân vùng giao diện Pinned/Others, bảo toàn dữ liệu và tính bền vững sau restart).
- Trong đó, kiểm thử `TC-BB-024G` (Giao diện khi toàn bộ ghi chú được ghim) được thiết kế chạy an toàn bằng tài khoản QA cô lập với đúng 3 ghi chú, bảo đảm không làm ảnh hưởng đến dữ liệu của các tài khoản khác trên máy.
- Tầng Provider có 2 tests `PV-REF-01` và `PV-REF-02` đã được đối chiếu trong log máy lịch sử.
## 6. CẬP NHẬT TRUY VẾT AUTOMATION PHASE 5 — 21/10/2026

| Requirement | Chức năng | Automation execution | Trạng thái |
|---|---|---|---|
| REQ-08 | FN-23 — Tìm kiếm ghi chú & Bộ lọc đa phương tiện | 18 items tự động hóa: 15 PASS, 1 FAIL (`BUG-004`), 1 CHƯA ĐỦ CĂN CỨ (`BR-01`), 1 BLOCKED (`BUG-001`); 4 items giữ nguyên Manual lịch sử | Đã đối chiếu đầy đủ JUnit XML & Evidence trên thiết bị thật Samsung Galaxy S21 FE 5G |

**Lưu ý REQ-08 (FN-23 Search & Filter):**
- Chức năng **FN-23** là Phase Automation cuối cùng của dự án, đạt độ bao phủ tự động hóa trên **18/22 execution items** (4 baseline lịch sử + 14 items mở rộng thực thi trên thiết bị thật):
  - **15 items PASS:** Tìm kiếm tiêu đề (`026`), nội dung (`027`), chuỗi rỗng Empty State (`028`), SQL injection an toàn (`029`), chữ thường có dấu (`026B D01`), chữ HOA có dấu case-insensitive (`026B D02`), tiếng Việt có dấu (`026C D01`), nút X xóa nhanh (`026E D01`), nút Back thoát về Home (`028D D01`), lọc Pinned (`027D D01`), lọc Archive (`027D D02`), gỡ Chip (`027F D01`), lọc URL (`027B D03`), loại trừ Thùng rác 0 leak (`028B D01`), mở & sửa từ kết quả tìm kiếm (`028C D01`).
  - **1 item CHƯA ĐỦ CĂN CỨ:** `TC-BB-026B-D03` (Tìm kiếm không dấu tiếng Việt). SQLite không unaccent folding, trả về Empty State an toàn, giữ nguyên trạng thái theo quyết định `BR-01`, không tự ép PASS.
  - **1 item FAIL (Tái hiện BUG-004 OPEN):** `TC-BB-027G-D01` (Bộ lọc Danh sách `has:list`). SQLite thực hiện query LIKE thô không bóc tách token, tái hiện chính xác defect, không hợp thức hóa thành PASS.
  - **1 item BLOCKED:** `TC-BB-027E-D01` (Lọc kết hợp Hình ảnh + Từ khóa). Bị chặn bởi lỗi treo upload ảnh trong Editor (`BUG-001`), không thay thế fixture sang Pinned.
  - **4 items ngoài phạm vi Automation:** 1 Manual PASS (`TC-BB-026D-D01` Highlight có đủ ảnh), 3 items (`TC-BB-027B-D01` Ảnh, `TC-BB-027B-D02` Audio, `TC-BB-027C-D01` Nhãn dán) giữ PENDING / NOT RUN theo lịch sử do thiếu căn cứ xác nhận độc lập hoặc thiếu screenshot trực tiếp.
- Toàn bộ 5 Phase Automation của dự án đã hoàn thành thắng lợi theo kế hoạch.
