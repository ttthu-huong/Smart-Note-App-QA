# BẢNG TIẾN ĐỘ VÀ TRẠNG THÁI AUTOMATION TESTING TỔNG THỂ
## Dự án: Smart Note App
**Branch kiểm thử:** `huong`  
**Repository duy nhất:** `ttt-huong/Smart-Note-App-QA`  
**Ngày cập nhật audit:** 05/10/2026  
**Thiết bị thực thi:** Samsung Galaxy S21 FE 5G (SM-G990B / R5CW82ECF6M), Android 14 (API 34)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual / Automation Test Execution  

---

## I. GIẢI ĐÁP CÁC CÂU HỎI QUAN TRỌNG

### A. Tôi đang tự động hóa những gì?
Hệ thống đang tập trung tự động hóa các kịch bản kiểm thử hộp đen (Black-box Test Cases) mức giao diện người dùng đầu cuối (Android UI/E2E Testing) trên thiết bị thật, ưu tiên các luồng chức năng độc lập, ổn định và có thể lặp lại mà không phụ thuộc vào dịch vụ OAuth bên thứ 3 hoặc tương tác phần cứng đặc thù.

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
- **TC-BB-003**: **FAIL** (16.7s) — Expected: *"Định dạng email không hợp lệ."*, Actual: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* (Application Bug BUG-FN02-01).
- **TC-BB-004**: **PASS** (16.4s) — Mật khẩu 5 ký tự bị chặn với thông báo lỗi đỏ: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."*
- **TC-BB-005**: **PASS** (17.2s) — Đăng ký bằng email đã tồn tại bị chặn với thông báo: *"Email này đã được sử dụng cho một tài khoản khác."*

**Nhóm FN-23 (4/4 PASS — 100%):**
- **TC-BB-026**: **PASS** (33.9s) — Danh sách kết quả hiển thị thẻ ghi chú "Lịch thi học kỳ" khớp từ khóa trong tiêu đề.
- **TC-BB-027**: **PASS** (36.9s) — Danh sách kết quả hiển thị thẻ ghi chú "Tạp vụ" khớp từ khóa nội dung "giấy in A4".
- **TC-BB-028**: **PASS** (28.2s) — Từ khóa không tồn tại "chuoi_khong_ton_tai_999" trả về Empty State "Không tìm thấy kết quả", gợi ý "Thử từ khóa khác".
- **TC-BB-029**: **PASS** (27.2s) — Chuỗi ký tự đặc biệt & SQL Injection `"' OR 1=1 -- % _ @#$"` được xử lý an toàn, app không crash, hiển thị màn hình rỗng "Không tìm thấy kết quả".
**Nhóm FN-20 (2/2 PASS — 100%):**
- **TC-BB-024**: **PASS** (24.2s) — Xuất hiện tiêu đề phân vùng "Được ghim" và thẻ ghi chú được chuyển lên khu vực ưu tiên phía trên cùng.
- **TC-BB-025**: **PASS** (18.5s) — Bỏ ghim đưa ghi chú về danh sách thông thường bên dưới, tiêu đề "Được ghim" tự động ẩn đi hoàn toàn.

**Nhóm FN-09 (2/2 PASS — 100%):**
- **TC-BB-019**: **PASS** — Thẻ ghi chú trên HomeScreen phản ánh chính xác chuỗi nội dung mới vừa chỉnh sửa `"[Đã cập nhật lúc 10:00]"`.
- **TC-BB-020**: **PASS** — Ngừng nhập 2.0s (> 1000ms debounce), thoát ra và mở lại ghi chú, toàn bộ nội dung mới `"- Nội dung kiểm tra tự động lưu"` vẫn còn nguyên vẹn trong EditorScreen.

**Nhóm FN-08 (3/3 PASS — 100%):**
- **TC-BB-016**: **PASS** (31.8s) — Thẻ ghi chú hiển thị đầy đủ tiêu đề "Họp Lab" và nội dung "Nội dung ngắn gọn" trên HomeScreen.
- **TC-BB-017**: **PASS** (23.3s) — Ứng dụng tạo note thành công và hiển thị phần xem trước nội dung "Ý tưởng nhanh không tiêu đề" trên HomeScreen.
- **TC-BB-018**: **PASS** (15.7s) — Rời Editor để trống cả title và content, ứng dụng không tạo bất kỳ ghi chú rỗng nào trên HomeScreen.

**Nhóm FN-04 (1/4 PASS, 3/4 FAIL):**
- **TC-BB-009**: **PASS** (1.5s) — Client validation bắt chính xác: *"Vui lòng nhập đầy đủ Email và Mật khẩu."*
- **TC-BB-008**: **FAIL** (3.0s) — Expected: *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."*, Actual: *"Email hoặc mật khẩu không chính xác."*
- **TC-BB-007**: **FAIL** (3.0s) — Expected: *"Mật khẩu không chính xác."*, Actual: *"Email hoặc mật khẩu không chính xác."*
- **TC-BB-006**: **FAIL** (4.0s) — Credentials được nhập thành công, nhưng ứng dụng chuyển hướng sang `EmailVerificationScreen` vì tài khoản test chưa xác thực email (`emailVerified: false`).

### E. Phân loại lỗi và Bug ghi nhận
Tổng kết lỗi / thất bại từ automation ghi nhận rõ 3 nhóm:
- **Application Bugs (3 Bugs):**
  1. **BUG-FN02-01** (`TC-BB-003`): Khi nhập email thiếu ký tự `@` (`nguoidung_gmail.com`), ứng dụng hiển thị sai thông báo lỗi: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* thay vì *"Định dạng email không hợp lệ."* theo đặc tả.
  2. **BUG-BB-002** (`TC-BB-008`): Ứng dụng hiển thị thông báo gộp Firebase "Email hoặc mật khẩu không chính xác.", không chỉ rõ tài khoản không tồn tại theo đặc tả.
  3. **BUG-BB-003** (`TC-BB-007`): Ứng dụng hiển thị thông báo gộp Firebase "Email hoặc mật khẩu không chính xác.", không chỉ rõ sai mật khẩu theo đặc tả.
- **Test Data / Precondition Issue (1 Issue):**
  - `TC-BB-006`: Credentials được nhập thành công nhưng tài khoản test `student_qa@gmail.com` có trường `emailVerified: false` trên Firebase Authentication, khiến ứng dụng chuyển hướng sang màn hình xác thực email thay vì HomeScreen. Không khẳng định đây là application bug nếu chưa có precondition hợp lệ.
- **Automation Input Issue (Đã khắc phục hoàn toàn):**
  - Lỗi nhập QuillEditor ở FN-08, FN-09 và PasswordField ở FN-04 đã được xử lý triệt để bằng cơ chế native paste / accessibility `set_text`, xác minh UI trung gian trước khi submit.

### F. Evidence nằm ở đâu?
Toàn bộ ảnh chụp màn hình bằng chứng thực tế được lưu tại:
- **FN-02:**
  - [`evidence/fn02/FN02_TC-BB-001_D01_01.png`](../../evidence/fn02/FN02_TC-BB-001_D01_01.png)
  - [`evidence/fn02/FN02_TC-BB-002_D01_01.png`](../../evidence/fn02/FN02_TC-BB-002_D01_01.png)
  - [`evidence/fn02/FN02_TC-BB-003_D01_01.png`](../../evidence/fn02/FN02_TC-BB-003_D01_01.png)
  - [`evidence/fn02/FN02_TC-BB-004_D02_01.png`](../../evidence/fn02/FN02_TC-BB-004_D02_01.png)
  - [`evidence/fn02/FN02_TC-BB-005_D01_01.png`](../../evidence/fn02/FN02_TC-BB-005_D01_01.png)
  - Báo cáo chi tiết: [`automation/reports/fn02_automation_report.md`](../../automation/reports/fn02_automation_report.md)
  - JUnit XML: [`automation/reports/fn02_register_junit.xml`](../../automation/reports/fn02_register_junit.xml)
- **FN-23:**
  - [`evidence/fn23/FN23_TC-BB-026_D01_01.png`](../../evidence/fn23/FN23_TC-BB-026_D01_01.png)
  - [`evidence/fn23/FN23_TC-BB-027_D01_01.png`](../../evidence/fn23/FN23_TC-BB-027_D01_01.png)
  - [`evidence/fn23/FN23_TC-BB-028_D01_01.png`](../../evidence/fn23/FN23_TC-BB-028_D01_01.png)
  - [`evidence/fn23/FN23_TC-BB-029_D01_01.png`](../../evidence/fn23/FN23_TC-BB-029_D01_01.png)
  - Báo cáo chi tiết: [`automation/reports/fn23_automation_report.md`](../../automation/reports/fn23_automation_report.md)
  - JUnit XML: [`automation/reports/fn23_search_junit.xml`](../../automation/reports/fn23_search_junit.xml)
- **FN-20:**
  - [`evidence/fn20/FN20_TC-BB-024_D01_01.png`](../../evidence/fn20/FN20_TC-BB-024_D01_01.png)
  - [`evidence/fn20/FN20_TC-BB-025_D01_01.png`](../../evidence/fn20/FN20_TC-BB-025_D01_01.png)
  - Báo cáo chi tiết: [`automation/reports/fn20_automation_report.md`](../../automation/reports/fn20_automation_report.md)
  - JUnit XML: [`automation/reports/fn20_pin_note_junit.xml`](../../automation/reports/fn20_pin_note_junit.xml)
- **FN-09:**
  - [`evidence/fn09/FN09_TC-BB-019_D01_01.png`](../../evidence/fn09/FN09_TC-BB-019_D01_01.png)
  - [`evidence/fn09/FN09_TC-BB-020_D01_01.png`](../../evidence/fn09/FN09_TC-BB-020_D01_01.png)
  - Báo cáo chi tiết: [`automation/reports/fn09_automation_report.md`](../../automation/reports/fn09_automation_report.md)
  - JUnit XML: [`automation/reports/fn09_edit_note_junit.xml`](../../automation/reports/fn09_edit_note_junit.xml)
- **FN-08:**
  - [`evidence/fn08/FN08_TC-BB-016_D01_01.png`](../../evidence/fn08/FN08_TC-BB-016_D01_01.png)
  - [`evidence/fn08/FN08_TC-BB-017_D01_01.png`](../../evidence/fn08/FN08_TC-BB-017_D01_01.png)
  - [`evidence/fn08/FN08_TC-BB-018_D01_01.png`](../../evidence/fn08/FN08_TC-BB-018_D01_01.png)
  - Báo cáo chi tiết: [`automation/reports/fn08_automation_report.md`](../../automation/reports/fn08_automation_report.md)
  - JUnit XML: [`automation/reports/fn08_create_note_junit.xml`](../../automation/reports/fn08_create_note_junit.xml)
- **FN-04:**
  - [`evidence/fn04/FN04_TC-BB-009_D01_01.png`](../../evidence/fn04/FN04_TC-BB-009_D01_01.png)
  - [`evidence/fn04/FN04_TC-BB-008_D01_01.png`](../../evidence/fn04/FN04_TC-BB-008_D01_01.png)
  - [`evidence/fn04/FN04_TC-BB-007_D01_01.png`](../../evidence/fn04/FN04_TC-BB-007_D01_01.png)
  - [`evidence/fn04/FN04_TC-BB-006_D01_01.png`](../../evidence/fn04/FN04_TC-BB-006_D01_01.png)
  - Báo cáo chi tiết: [`automation/reports/fn04_automation_report.md`](../../automation/reports/fn04_automation_report.md)
  - JUnit XML: [`automation/reports/fn04_login_junit.xml`](../../automation/reports/fn04_login_junit.xml)

### G. Những Test Case nào chưa làm?
**11 Test Cases** còn lại chưa có mã kiểm thử tự động (31 - 20 = 11, chiếm **35.48%**):
- 3 TCs trong kế hoạch triển khai tiếp theo (FN-10/11/12: 3 TCs).
- 8 TCs tạm hoãn do độ phức tạp ngoại vi (FN-05 OAuth, FN-29/30 Sinh trắc học, FN-40/41 Đồng bộ 2 thiết bị).

### H. Những Test Case nào đang Planned? (3 TCs)
- `TC-BB-021`, `TC-BB-022`, `TC-BB-023` (FN-10/FN-11/FN-12: Xóa vào Thùng rác / Khôi phục / Xóa vĩnh viễn)

### I. Những Test Case nào Deferred vì khó? (8 TCs)
- `TC-BB-010`, `TC-BB-011` (FN-05: Đăng nhập nhanh Google): Phụ thuộc Google OAuth Dialog.
- `TC-BB-012`, `TC-BB-013`, `TC-BB-014`, `TC-BB-015` (FN-29/FN-30: Khóa & Mở khóa Ghi chú bằng Sinh trắc học): Phụ thuộc phần cứng quét vân tay/khuôn mặt trên thiết bị thật.
- `TC-BB-030`, `TC-BB-031` (FN-40/FN-41: Đồng bộ Offline/Online & Giải quyết xung đột LWW): Yêu cầu phối hợp 2 thiết bị và can thiệp mạng phức tạp.

### J. Framework/công cụ đang sử dụng là gì?
- **Loại hình:** Android UI/E2E Testing (Black-box Automation).
- **Framework & Thư viện:** Python 3.13 + pytest + uiautomator2 + ADB.
- **Thiết kế locator:** Dynamic-First (hỗ trợ cả `text`, `content-description` và `xpath` của Flutter) kết hợp Coordinate-Fallback (tọa độ dự phòng).

---

## II. BẢNG TIẾN ĐỘ AUTOMATION TOÀN DIỆN (31 BLACK-BOX TEST CASES)

*Quy ước Status: `DONE` (Đã code & đã chạy), `IN PROGRESS` (Đang viết code), `PLANNED` (Trong kế hoạch triển khai), `DEFERRED` (Tạm hoãn do độ phức tạp ngoại vi), `BLOCKED` (Bị chặn).*

| Nhóm chức năng | TC-ID | Automation Type | Tool | Code | Executed | Result | Phân loại / Bug | Status |
|---|---|---|---|:---:|:---:|:---:|---|:---:|
| **FN-02: Đăng ký tài khoản Email** | **TC-BB-001** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-02 | **TC-BB-002** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-02 | **TC-BB-003** | Android UI/E2E | Python + u2 | **Có** | **Có** | **FAIL** | BUG-FN02-01 (Sai thông báo lỗi email) | **DONE** |
| FN-02 | **TC-BB-004** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-02 | **TC-BB-005** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| **FN-04: Đăng nhập tài khoản Email/Password** | **TC-BB-006** | Android UI/E2E | Python + u2 | **Có** | **Có** | **FAIL** | Precondition Issue (Tài khoản chưa verify email) | **DONE** |
| FN-04 | **TC-BB-007** | Android UI/E2E | Python + u2 | **Có** | **Có** | **FAIL** | BUG-BB-003 (Thông báo Firebase gộp) | **DONE** |
| FN-04 | **TC-BB-008** | Android UI/E2E | Python + u2 | **Có** | **Có** | **FAIL** | BUG-BB-002 (Thông báo Firebase gộp) | **DONE** |
| FN-04 | **TC-BB-009** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| **FN-05: Đăng nhập nhanh Google** | TC-BB-010 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | — | **DEFERRED** |
| FN-05 | TC-BB-011 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | — | **DEFERRED** |
| **FN-29/FN-30: Khóa & Mở khóa Ghi chú bằng Sinh trắc học** | TC-BB-012 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | — | **DEFERRED** |
| FN-29/FN-30 | TC-BB-013 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | — | **DEFERRED** |
| FN-29/FN-30 | TC-BB-014 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | — | **DEFERRED** |
| FN-29/FN-30 | TC-BB-015 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | — | **DEFERRED** |
| **FN-08: Tạo Ghi chú văn bản mới** | **TC-BB-016** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-08 | **TC-BB-017** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-08 | **TC-BB-018** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| **FN-09: Chỉnh sửa Ghi chú & Tự động lưu** | **TC-BB-019** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-09 | **TC-BB-020** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| **FN-10/FN-11/FN-12: Xóa vào Thùng rác / Khôi phục / Xóa vĩnh viễn** | TC-BB-021 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | — | **PLANNED** |
| FN-10/FN-11/FN-12 | TC-BB-022 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | — | **PLANNED** |
| FN-10/FN-11/FN-12 | TC-BB-023 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | — | **PLANNED** |
| **FN-20: Ghim & Bỏ ghim Ghi chú** | **TC-BB-024** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-20 | **TC-BB-025** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| **FN-23: Tìm kiếm Ghi chú theo từ khóa** | **TC-BB-026** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-23 | **TC-BB-027** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-23 | **TC-BB-028** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| FN-23 | **TC-BB-029** | Android UI/E2E | Python + u2 | **Có** | **Có** | **PASS** | — | **DONE** |
| **FN-40/FN-41: Đồng bộ Offline/Online & Giải quyết xung đột LWW** | TC-BB-030 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | — | **DEFERRED** |
| FN-40/FN-41 | TC-BB-031 | Android UI/E2E | Python + u2 | Chưa | Chưa | — | — | **DEFERRED** |

---

## III. BẢNG TỔNG HỢP SỐ LIỆU AUTOMATION TOÀN HỆ THỐNG

| Nhóm chức năng | Tên nhóm | Tổng TCs | Đã Code & Chạy | PASS | FAIL | ERROR | Tỷ lệ PASS | Trạng thái |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **FN-02** | Đăng ký tài khoản Email/Password | **5** | 5 | 4 | 1 | 0 | 80.00% | DONE |
| **FN-04** | Đăng nhập Email/Password | **4** | 4 | 1 | 3 | 0 | 25.00% | DONE |
| **FN-08** | Tạo Ghi chú văn bản mới | **3** | 3 | 3 | 0 | 0 | 100.00% | DONE |
| **FN-09** | Chỉnh sửa Ghi chú & Auto-save | **2** | 2 | 2 | 0 | 0 | 100.00% | DONE |
| **FN-20** | Ghim & Bỏ ghim Ghi chú | **2** | 2 | 2 | 0 | 0 | 100.00% | DONE |
| **FN-23** | Tìm kiếm Ghi chú (Search Note) | **4** | 4 | 4 | 0 | 0 | 100.00% | DONE |
| *Chưa automation* | FN-10/11/12 (3) | **3** | 0 | — | — | — | — | PLANNED |
| *Chưa automation* | FN-05 (2), FN-29/30 (4), FN-40/41 (2) | **8** | 0 | — | — | — | — | DEFERRED |
| **Tổng cộng** | **Toàn bộ hệ thống** | **31** | **20** | **16** | **4** | **0** | **80.00%** | — |

*Số liệu tổng hợp chuẩn xác toàn hệ thống:*
- **Độ bao phủ automation (Coverage):** 20/31 = **64.52%**
- **Tỷ lệ PASS trên số ca đã thực thi:** 16/20 = **80.00%** (16 PASS / 4 FAIL / 0 ERROR)
- **Tổng số ca chưa automation:** 11/31 = **35.48%** (3 Planned + 8 Deferred)
