# BẢNG TIẾN ĐỘ VÀ TRẠNG THÁI AUTOMATION TESTING TỔNG THỂ
## Dự án: Smart Note App
**Branch kiểm thử:** `huong`
**Repository duy nhất:** `ttt-huong/Smart-Note-App-QA`
**Ngày cập nhật:** 13/10/2026 (Đồng bộ theo hồ sơ baseline 12/10/2026)
**Commit tích hợp Provider:** `73514ad` (`test(qa): integrate 24 passing automated provider tests from thuong`)
**Commit tài liệu baseline:** `76df421`
**Thiết bị thực thi UI:** Samsung Galaxy S21 FE 5G (SM-G990B / API 34), Android 14
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual / Automation Test Execution

---

## I. GIẢI ĐÁP CÁC CÂU HỎI QUAN TRỌNG

### A. Tôi đang tự động hóa những gì?
Hệ thống áp dụng kiến trúc kiểm thử tự động hóa hai tầng bổ trợ lẫn nhau:
1. **Tầng 1 (Android UI/E2E Testing):** Tự động hóa các kịch bản kiểm thử hộp đen trên thiết bị thật (Samsung Galaxy S21 FE 5G) bằng Python 3.13 + uiautomator2 + pytest, tập trung các luồng giao diện người dùng độc lập (FN-02, FN-04, FN-08, FN-09, FN-20, FN-23).
2. **Tầng 2 (Flutter Provider Automated Testing):** Tự động hóa kiểm thử thành phần nội bộ và quản lý trạng thái (`NoteProvider`, `SyncProvider`) trong bộ nhớ bằng `flutter test`, bao phủ các chức năng cốt lõi và vòng đời đồng bộ/thùng rác khó can thiệp trên UI máy thật (FN-08, FN-09, FN-10, FN-11, FN-12, FN-13, FN-14, FN-20, FN-23, FN-40).

### B. Những Test Case nào đã có test code?
Hiện tại, **20/31 Test Cases** (độ bao phủ **64.52%**) thuộc 6 nhóm chức năng chính đã được cài đặt mã tự động hóa trong repository:
1. **FN-02: Đăng ký tài khoản Email/Password (5 TCs)** — file [`automation/tests/test_fn02_register.py`](../../automation/tests/test_fn02_register.py):
   - `TC-BB-001`: Đăng ký tài khoản với Email và Mật khẩu hợp lệ (D01)
   - `TC-BB-002`: Chặn đăng ký khi bỏ trống toàn bộ dữ liệu (D01)
   - `TC-BB-003`: Từ chối email không hợp lệ / thiếu ký tự @ (D01)
   - `TC-BB-004`: Chặn đăng ký khi mật khẩu dưới 6 ký tự (D02)
   - `TC-BB-005`: Thông báo lỗi khi đăng ký bằng Email đã tồn tại (D01)
2. **FN-04: Đăng nhập tài khoản Email/Password (4 TCs)** — file [`automation/tests/test_fn04_login.py`](../../automation/tests/test_fn04_login.py):
   - `TC-BB-006`: Đăng nhập thành công với tài khoản Email hợp lệ (D01)
   - `TC-BB-007`: Đăng nhập thất bại do sai Mật khẩu (D01)
   - `TC-BB-008`: Đăng nhập thất bại do tài khoản không tồn tại (D01)
   - `TC-BB-009`: Đăng nhập thất bại do để trống Mật khẩu (D01)
3. **FN-08: Tạo Ghi chú văn bản mới (3 TCs)** — file [`automation/tests/test_fn08_create_note.py`](../../automation/tests/test_fn08_create_note.py):
   - `TC-BB-016`: Tạo ghi chú văn bản có Tiêu đề và Nội dung (D01)
   - `TC-BB-017`: Tạo ghi chú không có tiêu đề nhưng có nội dung (D01)
   - `TC-BB-018`: Tạo ghi chú với cả tiêu đề và nội dung để trống; xác minh không tạo ghi chú rỗng (D01)
4. **FN-09: Chỉnh sửa Ghi chú & Tự động lưu (2 TCs)** — file [`automation/tests/test_fn09_edit_note.py`](../../automation/tests/test_fn09_edit_note.py):
   - `TC-BB-019`: Chỉnh sửa nội dung ghi chú và xác minh cập nhật thành công (D01)
   - `TC-BB-020`: Xác minh nội dung được tự động lưu sau khoảng thời gian ngừng nhập (D01)
5. **FN-20: Ghim & Bỏ ghim Ghi chú (2 TCs)** — file [`automation/tests/test_fn20_pin_note.py`](../../automation/tests/test_fn20_pin_note.py):
   - `TC-BB-024`: Ghim ghi chú lên khu vực ưu tiên trên Trang chủ (D01)
   - `TC-BB-025`: Bỏ ghim đưa ghi chú trở về danh sách thông thường (D01)
6. **FN-23: Tìm kiếm Ghi chú (Search Note) (4 TCs)** — file [`automation/tests/test_fn23_search.py`](../../automation/tests/test_fn23_search.py):
   - `TC-BB-026`: Tìm kiếm ghi chú theo từ khóa Tiêu đề (D01)
   - `TC-BB-027`: Tìm kiếm ghi chú theo từ khóa Nội dung (D01)
   - `TC-BB-028`: Tìm kiếm với từ khóa không tồn tại, xác minh Empty State (D01)
   - `TC-BB-029`: Tìm kiếm với chuỗi Ký tự đặc biệt & SQL Injection, xác minh Robustness & Empty State (D01)

### C. Những Test Case nào đã thực sự chạy?
Toàn bộ **20 Test Cases** trên (20/31 = **64.52%**) đã được thực thi thực tế trên thiết bị Samsung Galaxy S21 FE 5G, đạt tỷ lệ PASS **80.00%** (16/20 PASS):
- FN-02: `pytest -v -s automation/tests/test_fn02_register.py --junitxml=automation/reports/fn02_register_junit.xml`
- FN-04: `pytest -v -s automation/tests/test_fn04_login.py --junitxml=automation/reports/fn04_login_junit.xml`
- FN-08: `pytest -v -s automation/tests/test_fn08_create_note.py --junitxml=automation/reports/fn08_create_note_junit.xml`
- FN-09: `pytest -v -s automation/tests/test_fn09_edit_note.py --junitxml=automation/reports/fn09_edit_note_junit.xml`
- FN-20: `pytest -v -s automation/tests/test_fn20_pin_note.py --junitxml=automation/reports/fn20_pin_note_junit.xml`
- FN-23: `pytest -v -s automation/tests/test_fn23_search.py --junitxml=automation/reports/fn23_search_junit.xml`

### D. Kết quả từng Test Case?
**Nhóm FN-02 (4/5 PASS, 1/5 FAIL — 80.00%):**
- **TC-BB-001**: **PASS** (19.4s) — Đăng ký email mới thành công và chuyển sang màn hình Xác thực Email (`EmailVerificationScreen`).
- **TC-BB-002**: **PASS** (17.1s) — Bỏ trống form đăng ký bị chặn với thông báo lỗi đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."*
- **TC-BB-003**: **FAIL** (16.7s) — Expected: *"Định dạng email không hợp lệ."*, Actual: *"Không hỗ trợ tên miền email rác này..."* (Lỗi thứ tự regex validation form đăng ký; nhãn báo cáo cũ `BUG-FN02-01`).
- **TC-BB-004**: **PASS** (16.4s) — Mật khẩu 5 ký tự bị chặn với thông báo lỗi đỏ: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."*
- **TC-BB-005**: **PASS** (17.2s) — Đăng ký bằng email đã tồn tại bị chặn với thông báo: *"Email này đã được sử dụng cho một tài khoản khác."*

**Nhóm FN-04 (1/4 PASS, 3/4 FAIL — 25.00%):**
- **TC-BB-009**: **PASS** (1.5s) — Client validation bắt chính xác: *"Vui lòng nhập đầy đủ Email và Mật khẩu."*
- **TC-BB-006**: **FAIL** (4.0s) — Tài khoản test `student_qa@gmail.com` có trường `emailVerified: false` trên Firebase Auth nên ứng dụng chuyển hướng sang màn hình Xác thực email thay vì HomeScreen. Đây là lỗi tiền điều kiện (Precondition Issue), không phải lỗi ứng dụng.
- **TC-BB-007**: **FAIL** (3.0s) — Expected: *"Mật khẩu không chính xác."*, Actual: *"Email hoặc mật khẩu không chính xác."* (Thông báo gộp Firebase; nhãn cũ `BUG-BB-003` xung đột với `BUG-003` Pull-to-refresh trong Defect Log).
- **TC-BB-008**: **FAIL** (3.0s) — Expected: *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."*, Actual: *"Email hoặc mật khẩu không chính xác."* (Thông báo gộp Firebase; nhãn cũ `BUG-BB-002` xung đột với `BUG-002` Tombstone trong Defect Log).

**Nhóm FN-08 (3/3 PASS — 100%):**
- **TC-BB-016**: **PASS** (31.8s) — Thẻ ghi chú hiển thị đầy đủ tiêu đề "Họp Lab" và nội dung "Nội dung ngắn gọn" trên HomeScreen.
- **TC-BB-017**: **PASS** (23.3s) — Ứng dụng tạo note thành công và hiển thị phần xem trước nội dung "Ý tưởng nhanh không tiêu đề" trên HomeScreen.
- **TC-BB-018**: **PASS** (15.7s) — Rời Editor để trống cả title và content, ứng dụng không tạo bất kỳ ghi chú rỗng nào trên HomeScreen.

**Nhóm FN-09 (2/2 PASS — 100%):**
- **TC-BB-019**: **PASS** — Thẻ ghi chú trên HomeScreen phản ánh chính xác chuỗi nội dung mới vừa chỉnh sửa `"[Đã cập nhật lúc 10:00]"`.
- **TC-BB-020**: **PASS** — Ngừng nhập 2.0s (> 1000ms debounce), thoát ra và mở lại ghi chú, toàn bộ nội dung mới `"- Nội dung kiểm tra tự động lưu"` vẫn còn nguyên vẹn trong EditorScreen.

**Nhóm FN-20 (2/2 PASS — 100%):**
- **TC-BB-024**: **PASS** (24.2s) — Xuất hiện tiêu đề phân vùng "Được ghim" và thẻ ghi chú được chuyển lên khu vực ưu tiên phía trên cùng.
- **TC-BB-025**: **PASS** (18.5s) — Bỏ ghim đưa ghi chú về danh sách thông thường bên dưới, tiêu đề "Được ghim" tự động ẩn đi hoàn toàn.

**Nhóm FN-23 (4/4 PASS — 100%):**
- **TC-BB-026**: **PASS** (33.9s) — Danh sách kết quả hiển thị thẻ ghi chú "Lịch thi học kỳ" khớp từ khóa trong tiêu đề.
- **TC-BB-027**: **PASS** (36.9s) — Danh sách kết quả hiển thị thẻ ghi chú "Tạp vụ" khớp từ khóa nội dung "giấy in A4".
- **TC-BB-028**: **PASS** (28.2s) — Từ khóa không tồn tại "chuoi_khong_ton_tai_999" trả về Empty State "Không tìm thấy kết quả", gợi ý "Thử từ khóa khác".
- **TC-BB-029**: **PASS** (27.2s) — Chuỗi ký tự đặc biệt & SQL Injection `"' OR 1=1 -- % _ @#$"` được xử lý an toàn, app không crash, hiển thị màn hình rỗng "Không tìm thấy kết quả".

### E. Phân loại lỗi và Đối chiếu Defect Log
1. **Lỗi ứng dụng (Application Bug - 1 ca):**
   - `TC-BB-003` (`FN-02`): Form đăng ký kích hoạt bộ lọc Disposable Email trước Regex format email, trả về sai thông báo lỗi (báo cáo cũ tạm ghi nhãn `BUG-FN02-01`).
2. **Lỗi tiền điều kiện dữ liệu kiểm thử (Precondition Issue - 1 ca):**
   - `TC-BB-006` (`FN-04`): Tài khoản test chưa được verify email (`emailVerified: false`) khiến app điều hướng sang màn hình Xác thực email. Đây là hành vi đúng của ứng dụng, không phải lỗi sản phẩm.
3. **Khác biệt Expected Result / Chính sách bảo mật (2 ca):**
   - `TC-BB-007` & `TC-BB-008` (`FN-04`): Ứng dụng trả về thông báo lỗi gộp an toàn của Firebase (*"Email hoặc mật khẩu không chính xác."*) để chống User Enumeration.
   - **Xử lý xung đột mã lỗi:** Các mã `BUG-BB-002` và `BUG-BB-003` chỉ là nhãn nội bộ trong báo cáo Automation cũ, **tuyệt đối không nhầm lẫn với `BUG-002` (Offline Tombstone) và `BUG-003` (Pull-to-refresh) trong Defect Log chính thức toàn dự án (`docs/bugs/defect_log.md`)**.

### F. Evidence nằm ở đâu?
- **Ảnh chụp màn hình UI:** Toàn bộ lưu tại `evidence/fn02/`, `evidence/fn04/`, `evidence/fn08/`, `evidence/fn09/`, `evidence/fn20/`, `evidence/fn23/`.
- **Báo cáo JUnit XML:** Lưu tại `automation/reports/` (6 tệp JUnit tương ứng 6 nhóm FN).
- **Log Provider:** Lưu tại `evidence/automated/automated_test_run.log` (24/24 PASS).

### G. Những Test Case nào chưa làm? (11 Test Cases UI)
- 3 TCs trong kế hoạch triển khai tiếp theo (FN-10/11/12 Thùng rác: `TC-BB-021`, `TC-BB-022`, `TC-BB-023`).
- 8 TCs tạm hoãn do phụ thuộc ngoại vi:
  - `TC-BB-010`, `TC-BB-011` (FN-05: Google OAuth Dialog).
  - `TC-BB-012` (FN-29: Kích hoạt khóa vân tay).
  - `TC-BB-013`, `TC-BB-014`, `TC-BB-015` (FN-30: Mở khóa và duy trì bảo vệ vân tay).
  - `TC-BB-030` (FN-40: Tạo ghi chú offline rồi sync).
  - `TC-BB-031` (FN-41: Xung đột LWW giữa 2 máy).

---

## II. BẢNG TIẾN ĐỘ AUTOMATION TOÀN DIỆN (31 BLACK-BOX TEST CASES)

*Quy ước Code Status: `DONE` (Đã code), `PLANNED` (Trong kế hoạch), `DEFERRED` (Tạm hoãn).*
*Quy ước Result: `PASS`, `FAIL`, `NOT RUN`.*

| Nhóm FN | TC-ID | Automation Type | Tool | Code | Executed | Result | Phân loại / Bug ghi nhận | Status |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **FN-02** | **TC-BB-001** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-02 | **TC-BB-002** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-02 | **TC-BB-003** | Android UI/E2E | Python + u2 | **Có** | **Có** | **FAIL** | Application Bug (Lỗi thứ tự validate email) | **DONE** |
| FN-02 | **TC-BB-004** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-02 | **TC-BB-005** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| **FN-04** | **TC-BB-006** | Android UI/E2E | Python + u2 | **Có** | **Có** | **FAIL** | Precondition Issue (`emailVerified: false`) | **DONE** |
| FN-04 | **TC-BB-007** | Android UI/E2E | Python + u2 | **Có** | **Có** | **FAIL** | Khác biệt Expected / Thông báo Firebase gộp | **DONE** |
| FN-04 | **TC-BB-008** | Android UI/E2E | Python + u2 | **Có** | **Có** | **FAIL** | Khác biệt Expected / Thông báo Firebase gộp | **DONE** |
| FN-04 | **TC-BB-009** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| **FN-05** | TC-BB-010 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | Phụ thuộc Google OAuth Dialog | **DEFERRED** |
| FN-05 | TC-BB-011 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | Phụ thuộc Google OAuth Dialog | **DEFERRED** |
| **FN-08** | **TC-BB-016** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-08 | **TC-BB-017** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-08 | **TC-BB-018** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| **FN-09** | **TC-BB-019** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-09 | **TC-BB-020** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| **FN-10** | TC-BB-021 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | Kế hoạch Phase 2 UI (Provider đã PASS) | **PLANNED** |
| **FN-11** | TC-BB-022 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | Kế hoạch Phase 2 UI (Provider đã PASS) | **PLANNED** |
| **FN-12** | TC-BB-023 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | Kế hoạch Phase 2 UI (Provider đã PASS) | **PLANNED** |
| **FN-20** | **TC-BB-024** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-20 | **TC-BB-025** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| **FN-23** | **TC-BB-026** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-23 | **TC-BB-027** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-23 | **TC-BB-028** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-23 | **TC-BB-029** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| **FN-29** | TC-BB-012 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | Phụ thuộc phần cứng quét vân tay | **DEFERRED** |
| **FN-30** | TC-BB-013 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | Phụ thuộc Biometric Prompt hệ thống | **DEFERRED** |
| FN-30 | TC-BB-014 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | Phụ thuộc Biometric Prompt hệ thống | **DEFERRED** |
| FN-30 | TC-BB-015 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | Duy trì bảo vệ khi hủy Biometric Prompt | **DEFERRED** |
| **FN-40** | TC-BB-030 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | Điều khiển mạng máy thật (Provider đã PASS) | **DEFERRED** |
| **FN-41** | TC-BB-031 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | Yêu cầu 2 thiết bị vật lý; quy tắc BR-03 | **DEFERRED** |

---

## III. BẢNG TỔNG HỢP SỐ LIỆU AUTOMATION TOÀN HỆ THỐNG

| Nhóm chức năng | Tên nhóm | Tổng TCs | Đã Code & Chạy | PASS | FAIL | ERROR | Tỷ lệ PASS | Trạng thái |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **FN-02** | Đăng ký tài khoản Email/Password | **5** | 5 | 4 | 1 | 0 | 80.00% | DONE |
| **FN-04** | Đăng nhập tài khoản Email/Password | **4** | 4 | 1 | 3 | 0 | 25.00% | DONE |
| **FN-08** | Tạo Ghi chú văn bản mới | **3** | 3 | 3 | 0 | 0 | 100.00% | DONE |
| **FN-09** | Chỉnh sửa Ghi chú & Auto-save | **2** | 2 | 2 | 0 | 0 | 100.00% | DONE |
| **FN-20** | Ghim & Bỏ ghim Ghi chú | **2** | 2 | 2 | 0 | 0 | 100.00% | DONE |
| **FN-23** | Tìm kiếm Ghi chú (Search Note) | **4** | 4 | 4 | 0 | 0 | 100.00% | DONE |
| *Chưa automation UI* | FN-10/11/12 (3 TCs) | **3** | 0 | — | — | — | — | PLANNED |
| *Chưa automation UI* | FN-05 (2), FN-29 (1), FN-30 (3), FN-40 (1), FN-41 (1) | **8** | 0 | — | — | — | — | DEFERRED |
| **Tổng cộng UI** | **Toàn bộ 31 Test Cases UI** | **31** | **20** | **16** | **4** | **0** | **80.00%** | — |

*Chỉ số đo lường chuẩn xác Tầng 1 (Android UI/E2E):*
- **Độ bao phủ cài đặt mã UI (Coverage):** 20/31 = **64.52%**
- **Tỷ lệ PASS trên số ca đã thực thi:** 16/20 = **80.00%** (16 PASS / 4 FAIL / 0 ERROR)
- **Tổng số ca chưa automation UI:** 11/31 = **35.48%** (3 Planned + 8 Deferred)

---

## IV. TIẾN ĐỘ VÀ KẾT QUẢ FLUTTER PROVIDER AUTOMATED TESTING (24 TESTS — COMMIT 73514ad)

Nhánh `huong` đã tích hợp bộ **24 Automated Provider Tests** từ nhánh `thuong` tại commit `73514ad`:

### A. Thông tin kiểm thử & Bằng chứng
- **Mã nguồn:**
  - `test/automated/note_provider_test.dart` (15 tests)
  - `test/automated/sync_provider_test.dart` (9 tests)
- **Kết quả thực thi:** **24/24 PASS (100.00%)** trong ~00:01s.
- **Tệp bằng chứng log:** [`evidence/automated/automated_test_run.log`](../../evidence/automated/automated_test_run.log)

### B. Phân bổ chức năng của 24 Provider Tests (Bao phủ 10 FNs, 26 lượt liên kết)
*Ghi chú: Bộ kiểm thử gồm chính xác **24 bài test duy nhất**, tạo ra **26 lượt liên kết Test → FN** do 2 bài test đa chức năng liên kết cả Thùng rác lẫn Ghim:*
1. `FN-08`: Tạo ghi chú văn bản (1 test: `PV-REF-06`)
2. `FN-09`: Cập nhật ghi chú (1 test: `PV-REF-07`)
3. `FN-10`: Chuyển ghi chú vào thùng rác (2 tests: `PV-REF-11`, `PV-REF-14`)
4. `FN-11`: Khôi phục ghi chú từ thùng rác (3 tests: `PV-REF-05`, `PV-REF-12`, `PV-REF-15`)
5. `FN-12`: Xóa ghi chú vĩnh viễn (1 test: `PV-REF-13`)
6. `FN-13`: Lưu trữ ghi chú (1 test: `PV-REF-03`)
7. `FN-14`: Bỏ lưu trữ ghi chú (1 test: `PV-REF-04`)
8. `FN-20`: Ghim & Bỏ ghim ghi chú (4 lượt liên kết: 2 tests chuyên biệt `PV-REF-01..02` + 2 tests đa chức năng `PV-REF-14..15`)
9. `FN-23`: Tìm kiếm ghi chú & Xóa tìm kiếm (3 tests: `PV-REF-08..10`)
10. `FN-40`: Bắt đầu đồng bộ & Vòng đời đồng bộ (9 tests: `PV-REF-16..24`)

### C. Đối chiếu toàn diện 44 FN và Phân loại Trạng thái Tự động hóa
1. **Automation chạy thành công chính thức (12 FNs — 27.27%):**
   - Danh sách: `FN-02`, `FN-04`, `FN-08`, `FN-09`, `FN-10`, `FN-11`, `FN-12`, `FN-13`, `FN-14`, `FN-20`, `FN-23`, `FN-40`.
2. **Chỉ có script thăm dò khả thi UI (3 FNs — 6.82%):**
   - Danh sách: `FN-05` (Google OAuth), `FN-29` (Kích hoạt khóa vân tay), `FN-30` (Mở khóa vân tay).
3. **Bị BLOCKED không thể tự động hóa (4 FNs — 9.09%):**
   - Danh sách: `FN-31`, `FN-32`, `FN-33` (Gemini AI — lỗi khung đỏ service UI trên máy thật); `FN-44` (Xử lý hết bộ nhớ — an toàn thiết bị tester).
4. **Chưa tự động hóa (25 FNs — 56.82%):**
   - Danh sách: `FN-01`, `FN-03`, `FN-06`, `FN-07`, `FN-15`, `FN-16`, `FN-17`, `FN-18`, `FN-19`, `FN-21`, `FN-22`, `FN-24`, `FN-25`, `FN-26`, `FN-27`, `FN-28`, `FN-34`, `FN-35`, `FN-36`, `FN-37`, `FN-38`, `FN-39`, `FN-41`, `FN-42`, `FN-43`.

**Cân bằng số liệu 44 FN:**
- **Đã bao phủ tự động:** **12 / 44 FNs (27.27%)** (Nhóm 1)
- **Chưa bao phủ tự động:** **32 / 44 FNs (72.73%)** (Nhóm 2 + 3 + 4: $3 + 4 + 25 = 32$)
- **Tổng cộng:** $\mathbf{12 + 32 = 44\ \text{FNs}\ (100.00\%)}$.

### D. Ranh giới số liệu và Nguyên tắc chốt phạm vi (FROZEN)
1. **Tầng 1 (Android UI/E2E):** Chính xác **20 Test Cases** đã thực thi (16 PASS / 4 FAIL).
2. **Tầng 2 (Flutter Provider):** Chính xác **24 Tests** đã thực thi (24 PASS / 0 FAIL).
3. **Tổng kịch bản tự động hóa chính thức:** **44 kịch bản** (40 PASS / 4 FAIL).
4. **Cô lập với White-box & Black-box thủ công:** Không cộng dồn 18 Unit Tests White-box hay 140 execution items kiểm thử thủ công vào số lượng kịch bản của bộ Automated Testing.
5. **Chi tiết đối chiếu đầy đủ:** Xem tại [`docs/qa/automation_execution_summary.md`](automation_execution_summary.md) và [`docs/qa/automation_test_cases.md`](automation_test_cases.md).
