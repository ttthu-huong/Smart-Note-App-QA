# BÁO CÁO THỰC THI AUTOMATION TEST PHASE 4 (PHASE 4 AUTOMATION EXECUTION REPORT)
## Dự án: Smart Note App
**Branch kiểm thử:** `huong`  
**Repository:** `ttt-huong/Smart-Note-App-QA`  
**Thiết bị thực thi chính:** Samsung Galaxy S21 FE 5G (Serial: `R5CW82ECF6M`, SM-G990E, Android 16 / SDK 36, Màn hình: 1080x2340)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Test Execution / Defect Reporting  
**Mục tiêu:** Ghi nhận tiến độ và kết quả triển khai tự động hóa thực tế cho từng AT-ID trong danh sách 61 "Recommended for Implementation" đã thống nhất tại Phase 3C.

---

## I. TỔNG QUAN TIẾN ĐỘ THỰC THI PHASE 4

- **Tổng số Test Cases trong kế hoạch tự động hóa (Recommended Suite):** **61 Test Cases**
- **Tổng số lượt thực thi theo kế hoạch (Planned Executions):** **74 Lượt**
- **Số Test Cases đã hoàn thành triển khai thực tế trong Phase 4 (Full Implementation):** **11 / 61 Test Cases** (~18.03%)
  - `AT-01` (`TC-BB-001`): **PASS** (3/3 executions: D01, D02, D03)
  - `AT-02` (`TC-BB-001B`): **PASS** (1/1 execution: D01)
  - `AT-03` (`TC-BB-002`): **PASS** (1/1 execution: D01)
  - `AT-04` (`TC-BB-002B`): **PASS** (1/1 execution: D01)
  - `AT-05` (`TC-BB-002C`): **PASS** (1/1 execution: D01)
  - `AT-06` (`TC-BB-003`): **COMPLETED** (2/2 executions: D01 [FAIL-APP do BUG-FN02-01], D02 [PASS])
  - `AT-07` (`TC-BB-003B`): **PASS** (1/1 execution: D01)
  - `AT-08` (`TC-BB-004`): **PASS** (2/2 executions: D01, D02)
  - `AT-09` (`TC-BB-004B`): **PASS** (2/2 executions: D01, D02)
  - `AT-10` (`TC-BB-005`): **PASS** (2/2 executions: D01, D02)
  - `AT-11` (`TC-BB-006`): **PASS** (1/1 execution: D01)
- **Tổng số lượt thực thi đã hoàn thành trong Phase 4 (Executions Completed):** **17 / 74 Executions** (~22.97%)
  - Phân loại kết quả thực thi: **16 PASS / 01 FAIL-APP** (Tỷ lệ PASS: 94.12%, 100% ca lỗi là lỗi ứng dụng đã xác nhận)
- **Số Test Cases còn lại cần triển khai tuần tự:** **50 / 61 Test Cases** (57 Lượt thực thi)
- **Ghi chú về giai đoạn Thăm dò khả thi (Pre-Phase 4 Feasibility Validation):**
  - Trước khi bước vào triển khai chính thức theo từng iteration, 03 Test Cases (`AT-21`, `AT-59`, `AT-60`) đã được thực hiện thăm dò khả thi kỹ thuật độc lập (Commit `21d66de`) với kết quả: `AT-21` (PASS), `AT-59` (PASS), `AT-60` (PASS WITH PRECONDITION).
  - *Nguyên tắc thống kê tiến độ:* Các ca Feasibility Validation không được tính gộp tự động vào số Test Cases hoàn thành chính thức của Phase 4; chúng được theo dõi riêng biệt và sẽ được tích hợp chính thức vào bộ test của hàm tương ứng khi lộ trình tuần tự đến các mã AT này.

---
## II. BẢNG TRUY VẾT & KẾT QUẢ THỰC THI CHI TIẾT TỪNG AT-ID (TRACEABILITY LOG)

| STT | AT-ID | Manual TC ID | Nhóm FN | Execution ID / Dataset | Automation Test Method | Kết quả | Thời gian | Bằng chứng kiểm thử (Evidence) | Khiếm khuyết (Defect/Bug) |
|:---:|:---:|:---:|:---:|:---:|:---|:---:|:---:|:---|:---:|
| 1 | **AT-01** | `TC-BB-001` | FN-02 | **D01** (Gmail hợp lệ) | `test_tc_bb_001_d01_gmail_success` | **PASS** | ~48s | [`evidence/fn02/FN02_TC-BB-001_D01_01.png`](../../evidence/fn02/FN02_TC-BB-001_D01_01.png) | Không |
| 2 | **AT-01** | `TC-BB-001` | FN-02 | **D02** (Outlook hợp lệ) | `test_tc_bb_001_d02_outlook_success` | **PASS** | ~49s | [`evidence/fn02/FN02_TC-BB-001_D02_01.png`](../../evidence/fn02/FN02_TC-BB-001_D02_01.png) | Không |
| 3 | **AT-01** | `TC-BB-001` | FN-02 | **D03** (Edu hợp lệ) | `test_tc_bb_001_d03_edu_success` | **PASS** | ~50s | [`evidence/fn02/FN02_TC-BB-001_D03_01.png`](../../evidence/fn02/FN02_TC-BB-001_D03_01.png) | Không |
| 4 | **AT-02** | `TC-BB-001B` | FN-02 | **D01** (Khoảng trắng đầu/cuối) | `test_tc_bb_001b_trim_whitespace` | **PASS** | ~54s | [`evidence/fn02/FN02_TC-BB-001B_D01_01.png`](../../evidence/fn02/FN02_TC-BB-001B_D01_01.png) | Không |
| 5 | **AT-03** | `TC-BB-002` | FN-02 | **D01** (Trống cả 2 ô) | `test_tc_bb_002_empty_fields` | **PASS** | ~45s | [`evidence/fn02/FN02_TC-BB-002_D01_01.png`](../../evidence/fn02/FN02_TC-BB-002_D01_01.png) | Không |
| 6 | **AT-04** | `TC-BB-002B` | FN-02 | **D01** (Chỉ email, trống pass) | `test_tc_bb_002b_missing_password` | **PASS** | ~48s | [`evidence/fn02/FN02_TC-BB-002B_D01_01.png`](../../evidence/fn02/FN02_TC-BB-002B_D01_01.png) | Không |
| 7 | **AT-05** | `TC-BB-002C` | FN-02 | **D01** (Chỉ pass, trống email) | `test_tc_bb_002c_missing_email` | **PASS** | ~42s | [`evidence/fn02/FN02_TC-BB-002C_D01_01.png`](../../evidence/fn02/FN02_TC-BB-002C_D01_01.png) | Không |
| 8 | **AT-06** | `TC-BB-003` | FN-02 | **D01** (Thiếu ký tự @) | `test_tc_bb_003_d01_missing_at_symbol` | **FAIL-APP** | ~41s | [`evidence/fn02/FN02_TC-BB-003_D01_01.png`](../../evidence/fn02/FN02_TC-BB-003_D01_01.png) | **BUG-FN02-01** |
| 9 | **AT-06** | `TC-BB-003` | FN-02 | **D02** (Thiếu tên miền) | `test_tc_bb_003_d02_missing_domain` | **PASS** | ~41s | [`evidence/fn02/FN02_TC-BB-003_D02_01.png`](../../evidence/fn02/FN02_TC-BB-003_D02_01.png) | Không |
| 10 | **AT-07** | `TC-BB-003B` | FN-02 | **D01** (Domain rác tempmail.com) | `test_tc_bb_003b_disposable_email` | **PASS** | ~39s | [`evidence/fn02/FN02_TC-BB-003B_D01_01.png`](../../evidence/fn02/FN02_TC-BB-003B_D01_01.png) | Không |
| 11 | **AT-08** | `TC-BB-004` | FN-02 | **D01** (Mật khẩu 1 ký tự) | `test_tc_bb_004_d01_min_1_char` | **PASS** | ~38s | [`evidence/fn02/FN02_TC-BB-004_D01_01.png`](../../evidence/fn02/FN02_TC-BB-004_D01_01.png) | Không |
| 12 | **AT-08** | `TC-BB-004` | FN-02 | **D02** (Mật khẩu 5 ký tự) | `test_tc_bb_004_d02_boundary_5_chars` | **PASS** | ~37s | [`evidence/fn02/FN02_TC-BB-004_D02_01.png`](../../evidence/fn02/FN02_TC-BB-004_D02_01.png) | Không |
| 13 | **AT-09** | `TC-BB-004B` | FN-02 | **D01** (Biên tối thiểu 6 ký tự) | `test_tc_bb_004b_d01_min_6_chars` | **PASS** | ~46s | [`evidence/fn02/FN02_TC-BB-004B_D01_01.png`](../../evidence/fn02/FN02_TC-BB-004B_D01_01.png) | Không |
| 14 | **AT-09** | `TC-BB-004B` | FN-02 | **D02** (Biên N+1 với 7 ký tự) | `test_tc_bb_004b_d02_boundary_7_chars` | **PASS** | ~47s | [`evidence/fn02/FN02_TC-BB-004B_D02_01.png`](../../evidence/fn02/FN02_TC-BB-004B_D02_01.png) | Không |
| 15 | **AT-10** | `TC-BB-005` | FN-02 | **D01** (Email đã tồn tại thường) | `test_tc_bb_005_d01_lowercase` | **PASS** | ~38s | [`evidence/fn02/FN02_TC-BB-005_D01_01.png`](../../evidence/fn02/FN02_TC-BB-005_D01_01.png) | Không |
| 16 | **AT-10** | `TC-BB-005` | FN-02 | **D02** (Email đã tồn tại chữ hoa) | `test_tc_bb_005_d02_uppercase` | **PASS** | ~39s | [`evidence/fn02/FN02_TC-BB-005_D02_01.png`](../../evidence/fn02/FN02_TC-BB-005_D02_01.png) | Không |
| 17 | **AT-11** | `TC-BB-006` | FN-04 | **D01** (Tài khoản chuẩn verified) | `test_tc_bb_006_valid_email_login` | **PASS** | ~51s | [`evidence/fn04/FN04_TC-BB-006_D01_01.png`](../../evidence/fn04/FN04_TC-BB-006_D01_01.png) | Không |
| 28 | **AT-21** | `TC-BB-011` | FN-05 | **D01** (Hủy Account Picker) | `test_at21_cancel_google_account_picker` | **PASS** | ~17s | [`evidence/fn05/FN05_TC-BB-011_D01_01.png`](../../evidence/fn05/FN05_TC-BB-011_D01_01.png), [`evidence/fn05/FN05_TC-BB-011_D01_02.png`](../../evidence/fn05/FN05_TC-BB-011_D01_02.png) | Không |
| 72 | **AT-59** | `TC-BB-015` | FN-29/30 | **D01** (Hủy Biometric Prompt) | `test_at59_cancel_biometric_prompt` | **PASS** | ~17s | [`evidence/fn29_30/FN29_30_TC-BB-015_D01_01.png`](../../evidence/fn29_30/FN29_30_TC-BB-015_D01_01.png), [`evidence/fn29_30/FN29_30_TC-BB-015_D01_02.png`](../../evidence/fn29_30/FN29_30_TC-BB-015_D01_02.png) | Không |
| 73 | **AT-60** | `TC-BB-015C` | FN-29/30 | **D01** (Back từ Locked Note) | `test_at60_back_navigation_from_locked_note` | **PASS WITH PRECONDITION** | ~19s | [`evidence/fn29_30/FN29_30_TC-BB-015C_D01_01.png`](../../evidence/fn29_30/FN29_30_TC-BB-015C_D01_01.png), [`evidence/fn29_30/FN29_30_TC-BB-015C_D01_02.png`](../../evidence/fn29_30/FN29_30_TC-BB-015C_D01_02.png) | Không |

---

## III. CHI TIẾT TRIỂN KHAI TỪNG ITERATION

### Iteration 1: AT-01 / TC-BB-001 (Đăng ký tài khoản với thông tin hợp lệ)
- **Mã AT:** `AT-01`
- **Mã Manual TC:** `TC-BB-001`
- **Nhóm chức năng:** `FN-02` (Đăng ký tài khoản Email/Password)
- **Mức độ ưu tiên:** `P0`
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng ký (`RegisterScreen`); thiết bị có kết nối Internet ổn định; tài khoản đăng ký là tài khoản mới chưa từng tồn tại trên hệ thống Firebase Auth.
- **Dữ liệu kiểm thử (3 Executions):**
  - **D01:** Email `student_qa_<timestamp>@gmail.com`, Mật khẩu `123456`.
  - **D02:** Email `user_dev_<timestamp>@outlook.com`, Mật khẩu `Abc@2026!`.
  - **D03:** Email `sv_<timestamp>@hcmus.edu.vn`, Mật khẩu `MatKhauDai123`.
- **Hành vi quan sát được (Observable UI Behavior):** Ứng dụng gửi thông tin đăng ký lên Firebase Auth thành công, điều hướng sang màn hình Xác thực Email (`EmailVerificationScreen`) với tiêu đề "Xác thực email của bạn".
- **File mã nguồn test:** [`automation/tests/test_fn02_register.py`](../../automation/tests/test_fn02_register.py)
  - `test_tc_bb_001_d01_gmail_success`
  - `test_tc_bb_001_d02_outlook_success`
  - `test_tc_bb_001_d03_edu_success`
  - `test_tc_bb_001_register_success` (alias tương thích ngược)
- **Kết quả thực thi:** **PASS (3/3 Executions)**
- **Thời gian thực thi:** 147.71s (toàn bộ 3 executions kèm teardown cách ly màn hình).
- **Minh chứng thực tế:**
  - `evidence/fn02/FN02_TC-BB-001_D01_01.png`
  - `evidence/fn02/FN02_TC-BB-001_D02_01.png`
  - `evidence/fn02/FN02_TC-BB-001_D03_01.png`
- **Kết quả kiểm thử hồi quy (Smoke Regression):** `pytest automation/tests/test_fn05_google_oauth.py -v -s` $\rightarrow$
ightarrow$\rightarrow$ **1 PASSED in 17.45s** (không làm ảnh hưởng các luồng automation khác).

### Iteration 2: AT-02 / TC-BB-001B (Đăng ký thành công với Email chứa khoảng trắng đầu/cuối - Whitespace Trimming)
- **Mã AT:** `AT-02`
- **Mã Manual TC:** `TC-BB-001B`
- **Nhóm chức năng:** `FN-02` (Đăng ký tài khoản Email/Password)
- **Mức độ ưu tiên:** `P1`
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng ký (`RegisterScreen`); thiết bị có kết nối Internet ổn định; email sau khi cắt tỉa chưa từng tồn tại trên hệ thống Firebase Auth.
- **Dữ liệu kiểm thử (1 Execution):**
  - **D01:** Email `"   student_trim_<timestamp>@gmail.com   "` (chuỗi có khoảng trắng thừa đầu và cuối), Mật khẩu `123456`.
- **Hành vi quan sát được (Observable UI Behavior):** Hệ thống tự động cắt tỉa khoảng trắng (`trim()`), gửi yêu cầu đăng ký lên Firebase Auth thành công và điều hướng sang màn hình Xác thực Email (`EmailVerificationScreen`) hiển thị địa chỉ đã cắt tỉa `student_trim_<timestamp>@gmail.com`.
- **File mã nguồn test:** [`automation/tests/test_fn02_register.py`](../../automation/tests/test_fn02_register.py)
  - `test_tc_bb_001b_trim_whitespace`
- **Kết quả thực thi:** **PASS (1/1 Execution)**
- **Thời gian thực thi:** 54.15s (chạy trên Samsung Galaxy S21 FE 5G với teardown cách ly an toàn).
- **Minh chứng thực tế:**
  - `evidence/fn02/FN02_TC-BB-001B_D01_01.png`
- **Kết quả kiểm thử hồi quy (Smoke Regression):** `pytest automation/tests/test_fn02_register.py -k test_tc_bb_001_d01 -v -s` $\rightarrow$
ightarrow$\rightarrow$ **1 PASSED in 54.61s** (không làm ảnh hưởng các luồng automation khác).

### Iteration 3: AT-03 / TC-BB-002 (Bỏ trống cả 2 ô Email và Mật khẩu khi Đăng ký)
- **Mã AT:** `AT-03`
- **Mã Manual TC:** `TC-BB-002`
- **Nhóm chức năng:** `FN-02` (Đăng ký tài khoản Email/Password)
- **Mức độ ưu tiên:** `P0`
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng ký (`RegisterScreen`).
- **Dữ liệu kiểm thử (1 Execution):**
  - **D01:** Email `""`, Mật khẩu `""` (để trống hoàn toàn cả hai trường).
- **Hành vi quan sát được (Observable UI Behavior):** Ứng dụng không chuyển màn hình; xuất hiện khung thông báo lỗi màu đỏ ngay trên form: *"Vui lòng nhập đầy đủ Email và Mật khẩu."*
- **File mã nguồn test:** [`automation/tests/test_fn02_register.py`](../../automation/tests/test_fn02_register.py)
  - `test_tc_bb_002_empty_fields`
- **Kết quả thực thi:** **PASS (1/1 Execution)**
- **Thời gian thực thi:** 44.64s (chạy trên Samsung Galaxy S21 FE 5G với teardown cách ly an toàn).
- **Minh chứng thực tế:**
  - `evidence/fn02/FN02_TC-BB-002_D01_01.png`
- **Kết quả kiểm thử hồi quy (Smoke Regression):** `pytest automation/tests/test_fn02_register.py -k test_tc_bb_001b -v -s` $\rightarrow$ **1 PASSED in 51.61s** (không làm ảnh hưởng các luồng automation khác).

### Iteration 4: AT-04 / TC-BB-002B (Chặn đăng ký khi chỉ nhập Email và bỏ trống Mật khẩu)
- **Mã AT:** `AT-04`
- **Mã Manual TC:** `TC-BB-002B`
- **Nhóm chức năng:** `FN-02` (Đăng ký tài khoản Email/Password)
- **Mức độ ưu tiên:** `P1`
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng ký (`RegisterScreen`).
- **Dữ liệu kiểm thử (1 Execution):**
  - **D01:** Email `student_valid_<timestamp>@gmail.com`, Mật khẩu `""` (chỉ nhập email hợp lệ, để trống trường mật khẩu).
- **Hành vi quan sát được (Observable UI Behavior):** Ứng dụng không chuyển màn hình; xuất hiện khung thông báo lỗi màu đỏ ngay trên form: *"Vui lòng nhập đầy đủ Email và Mật khẩu."*
- **File mã nguồn test:** [`automation/tests/test_fn02_register.py`](../../automation/tests/test_fn02_register.py)
  - `test_tc_bb_002b_missing_password`
- **Kết quả thực thi:** **PASS (1/1 Execution)**
- **Thời gian thực thi:** 47.63s (chạy trên Samsung Galaxy S21 FE 5G với teardown cách ly an toàn).
- **Minh chứng thực tế:**
  - `evidence/fn02/FN02_TC-BB-002B_D01_01.png`
- **Kết quả kiểm thử hồi quy (Smoke Regression):** `pytest automation/tests/test_fn02_register.py -k test_tc_bb_002_empty_fields -v -s` -> **1 PASSED in 43.61s** (không làm ảnh hưởng các luồng automation khác).

### Iteration 5: AT-05 / TC-BB-002C (Chặn đăng ký khi chỉ nhập Mật khẩu và bỏ trống Email)
- **Mã AT:** `AT-05`
- **Mã Manual TC:** `TC-BB-002C`
- **Nhóm chức năng:** `FN-02` (Đăng ký tài khoản Email/Password)
- **Mức độ ưu tiên:** `P1`
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng ký (`RegisterScreen`).
- **Dữ liệu kiểm thử (1 Execution):**
  - **D01:** Email `""`, Mật khẩu `"123456"` (để trống ô email, nhập mật khẩu hợp lệ).
- **Hành vi quan sát được (Observable UI Behavior):** Ứng dụng không chuyển màn hình; xuất hiện khung thông báo lỗi màu đỏ ngay trên form: *"Vui lòng nhập đầy đủ Email và Mật khẩu."*
- **File mã nguồn test:** [`automation/tests/test_fn02_register.py`](../../automation/tests/test_fn02_register.py)
  - `test_tc_bb_002c_missing_email`
- **Kết quả thực thi:** **PASS (1/1 Execution)**
- **Thời gian thực thi:** 41.74s (chạy trên Samsung Galaxy S21 FE 5G với teardown cách ly an toàn).
- **Minh chứng thực tế:**
  - `evidence/fn02/FN02_TC-BB-002C_D01_01.png`
- **Kết quả kiểm thử hồi quy (Smoke Regression):** `pytest automation/tests/test_fn02_register.py -k "test_tc_bb_002b_missing_password or test_tc_bb_002_empty_fields" -v -s` -> **2 PASSED in 73.32s** (các ca kiểm thử rỗng liên quan trong FN-02 đều hoạt động ổn định).

### Iteration 6: AT-06 / TC-BB-003 (Từ chối email không hợp lệ & Bắt lỗi ứng dụng BUG-FN02-01)
- **Mã AT:** `AT-06`
- **Mã Manual TC:** `TC-BB-003`
- **Nhóm chức năng:** `FN-02` (Đăng ký tài khoản Email/Password)
- **Mức độ ưu tiên:** `P0`
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng ký (`RegisterScreen`).
- **Dữ liệu kiểm thử (2 Executions):**
  - **D01:** Email `nguoidung_gmail.com` (thiếu ký tự `@`), Mật khẩu `123456`.
  - **D02:** Email `nguoidung@` (thiếu tên miền sau `@`), Mật khẩu `123456`.
- **Hành vi quan sát được (Observable UI Behavior):**
  - **D01:** Ứng dụng không chuyển màn hình; xuất hiện khung lỗi đỏ hiển thị: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* (Trái với đặc tả kỳ vọng *"Định dạng email không hợp lệ."* $
ightarrow$ Xác nhận lỗi ứng dụng **BUG-FN02-01**).
  - **D02:** Ứng dụng không chuyển màn hình; xuất hiện khung lỗi đỏ hiển thị chính xác: *"Định dạng email không hợp lệ."*.
- **File mã nguồn test:** [`automation/tests/test_fn02_register.py`](../../automation/tests/test_fn02_register.py)
  - `test_tc_bb_003_d01_missing_at_symbol`
  - `test_tc_bb_003_d02_missing_domain`
- **Kết quả thực thi (2/2 Executions):**
  - **D01:** **FAIL-APP** (Bắt lỗi ứng dụng BUG-FN02-01 theo đúng mục tiêu của AT-06 trong Phase 3C).
  - **D02:** **PASS** (41.39s).
- **Minh chứng thực tế:**
  - `evidence/fn02/FN02_TC-BB-003_D01_01.png`
  - `evidence/fn02/FN02_TC-BB-003_D02_01.png`
- **Khiếm khuyết ứng dụng (Application Bug):**
  - **BUG-FN02-01** (Confirmed): Hàm `_isValidDomain(email)` trong `auth_provider.dart` kiểm tra `email.split('@').length < 2` trả về `false`, gán nhầm thông báo domain email rác thay vì báo lỗi định dạng email. Khớp hoàn toàn với kết quả kiểm thử thủ công trước đó.
- **Kết quả kiểm thử hồi quy (Smoke Regression):** `pytest automation/tests/test_fn02_register.py -k "test_tc_bb_002b_missing_password or test_tc_bb_002c_missing_email" -v -s` -> **2 PASSED in 75.47s** (các ca kiểm thử trước đó hoạt động ổn định).

### Iteration 7: AT-07 / TC-BB-003B (Chặn đăng ký với Email thuộc danh sách đen tên miền rác)
- **Mã AT:** `AT-07`
- **Mã Manual TC:** `TC-BB-003B`
- **Nhóm chức năng:** `FN-02` (Đăng ký tài khoản Email/Password)
- **Mức độ ưu tiên:** `P1`
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng ký (`RegisterScreen`); thiết bị có kết nối Internet ổn định.
- **Dữ liệu kiểm thử (1 Execution):**
  - **D01:** Email `test_user_01@tempmail.com` (thuộc danh sách đen tên miền rác), Mật khẩu `123456`.
- **Hành vi quan sát được (Observable UI Behavior):** Ứng dụng không chuyển màn hình; hiển thị khung lỗi đỏ trên form: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* — khớp hoàn toàn với đặc tả kỳ vọng.
- **File mã nguồn test:** [`automation/tests/test_fn02_register.py`](../../automation/tests/test_fn02_register.py)
  - `test_tc_bb_003b_disposable_email`
- **Kết quả thực thi:** **PASS (1/1 Execution)**
- **Thời gian thực thi:** 39.46s (chạy trên Samsung Galaxy S21 FE 5G với teardown cách ly an toàn).
- **Minh chứng thực tế:**
  - `evidence/fn02/FN02_TC-BB-003B_D01_01.png`
- **Kết quả kiểm thử hồi quy (Smoke Regression):** `pytest automation/tests/test_fn02_register.py -k "test_tc_bb_003_d01 or test_tc_bb_003_d02" -v -s` $\rightarrow$ **D01: FAIL-APP (BUG-FN02-01 xác nhận lại), D02: PASS** — tổng hợp: 1 PASSED + 1 FAILED-APP (ổn định, khớp với kết quả AT-06).

### Iteration 8: AT-08 / TC-BB-004 (Xác minh chặn đăng ký khi mật khẩu dưới 6 ký tự - Cực tiểu và Biên N-1)
- **Mã AT:** `AT-08`
- **Mã Manual TC:** `TC-BB-004`
- **Nhóm chức năng:** `FN-02` (Đăng ký tài khoản Email/Password)
- **Mức độ ưu tiên:** `P1`
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng ký (`RegisterScreen`); thiết bị có kết nối Internet ổn định.
- **Dữ liệu kiểm thử (2 Executions):**
  - **D01:** Email `student_bva_<timestamp>@gmail.com`, Mật khẩu `1` (1 ký tự - điểm cực tiểu không hợp lệ).
  - **D02:** Email `student_bva_<timestamp>@gmail.com`, Mật khẩu `12345` (5 ký tự - điểm biên cận dưới $N-1$ không hợp lệ).
- **Hành vi quan sát được (Observable UI Behavior):**
  - **D01:** Ứng dụng không chuyển màn hình; xuất hiện khung lỗi đỏ hiển thị: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."* — khớp hoàn toàn với đặc tả kỳ vọng.
  - **D02:** Ứng dụng không chuyển màn hình; xuất hiện khung lỗi đỏ hiển thị: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."* — khớp hoàn toàn với đặc tả kỳ vọng.
- **File mã nguồn test:** [`automation/tests/test_fn02_register.py`](../../automation/tests/test_fn02_register.py)
  - `test_tc_bb_004_d01_min_1_char`
  - `test_tc_bb_004_d02_boundary_5_chars`
  - `test_tc_bb_004_weak_password` (alias tương thích ngược)
- **Kết quả thực thi:** **PASS (2/2 Executions)**
- **Thời gian thực thi:** 75.24s (chạy cả 2 executions trên Samsung Galaxy S21 FE 5G với teardown cách ly an toàn).
- **Minh chứng thực tế:**
  - `evidence/fn02/FN02_TC-BB-004_D01_01.png`
  - `evidence/fn02/FN02_TC-BB-004_D02_01.png`
- **Kết quả kiểm thử hồi quy (Smoke Regression):** `pytest automation/tests/test_fn02_register.py -k "test_tc_bb_003b_disposable_email or test_tc_bb_002c_missing_email" -v -s` $\rightarrow$ **2 PASSED in 81.52s** (các ca kiểm thử trước đó trong FN-02 đều hoạt động ổn định).

### Iteration 9: AT-09 / TC-BB-004B (Kiểm tra mật khẩu biên 6 ký tự và 7 ký tự - Điểm biên hợp lệ N và N+1)
- **Mã AT:** `AT-09`
- **Mã Manual TC:** `TC-BB-004B`
- **Nhóm chức năng:** `FN-02` (Đăng ký tài khoản Email/Password)
- **Mức độ ưu tiên:** `P1`
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng ký (`RegisterScreen`); thiết bị có kết nối Internet ổn định.
- **Dữ liệu kiểm thử (2 Executions):**
  - **D01:** Email `student_bva_min6_<timestamp>@gmail.com`, Mật khẩu `123456` (đúng 6 ký tự - điểm biên $N$).
  - **D02:** Email `student_bva_7char_<timestamp>@gmail.com`, Mật khẩu `1234567` (7 ký tự - điểm biên $N+1$).
- **Hành vi quan sát được (Observable UI Behavior):**
  - **D01:** Ứng dụng chấp nhận thông tin đăng ký, hoàn tất gửi yêu cầu và chuyển màn hình thành công sang màn hình Xác thực Email (`EmailVerificationScreen`) với tiêu đề "Xác thực email của bạn" và nút "Quay lại đăng nhập".
  - **D02:** Ứng dụng chấp nhận thông tin đăng ký, hoàn tất gửi yêu cầu và chuyển màn hình thành công sang màn hình Xác thực Email (`EmailVerificationScreen`) với tiêu đề "Xác thực email của bạn" và nút "Quay lại đăng nhập".
- **File mã nguồn test:** [`automation/tests/test_fn02_register.py`](../../automation/tests/test_fn02_register.py)
  - `test_tc_bb_004b_d01_min_6_chars`
  - `test_tc_bb_004b_d02_boundary_7_chars`
- **Kết quả thực thi:** **PASS (2/2 Executions)**
- **Thời gian thực thi:** 92.94s (chạy cả 2 executions trên Samsung Galaxy S21 FE 5G với teardown cách ly an toàn).
- **Minh chứng thực tế:**
  - `evidence/fn02/FN02_TC-BB-004B_D01_01.png`
  - `evidence/fn02/FN02_TC-BB-004B_D02_01.png`
- **Kết quả kiểm thử hồi quy (Smoke Regression):** `pytest automation/tests/test_fn02_register.py -k "test_tc_bb_004_d01_min_1_char or test_tc_bb_004_d02_boundary_5_chars" -v -s` $\rightarrow$ **2 PASSED in 80.55s** (các ca kiểm thử mật khẩu yếu trước đó trong FN-02 đều hoạt động ổn định).

### Iteration 10: AT-10 / TC-BB-005 (Xác minh từ chối đăng ký với Email đã tồn tại & Không phân biệt hoa/thường)
- **Mã AT:** `AT-10`
- **Mã Manual TC:** `TC-BB-005`
- **Nhóm chức năng:** `FN-02` (Đăng ký tài khoản Email/Password)
- **Mức độ ưu tiên:** `P1`
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng ký (`RegisterScreen`); thiết bị có kết nối Internet ổn định; tài khoản `student_qa@gmail.com` đã tồn tại trên Firebase Auth.
- **Dữ liệu kiểm thử (2 Executions):**
  - **D01:** Email `student_qa@gmail.com` (chữ thường đã tồn tại), Mật khẩu `123456`.
  - **D02:** Email `STUDENT_QA@GMAIL.COM` (chữ IN HOA của tài khoản đã tồn tại), Mật khẩu `123456`.
- **Hành vi quan sát được (Observable UI Behavior):**
  - **D01:** Ứng dụng không chuyển màn hình; giữ nguyên tại màn hình Đăng ký và hiển thị khung thông báo lỗi màu đỏ trên form: *"Email này đã được sử dụng cho một tài khoản khác."* — khớp hoàn toàn với đặc tả kỳ vọng.
  - **D02:** Ứng dụng không chuyển màn hình; giữ nguyên tại màn hình Đăng ký và hiển thị khung thông báo lỗi màu đỏ trên form: *"Email này đã được sử dụng cho một tài khoản khác."* (xác nhận hệ thống chuẩn hóa không phân biệt hoa/thường đối với email) — khớp hoàn toàn với đặc tả kỳ vọng.
- **File mã nguồn test:** [`automation/tests/test_fn02_register.py`](../../automation/tests/test_fn02_register.py)
  - `test_tc_bb_005_d01_lowercase`
  - `test_tc_bb_005_d02_uppercase`
  - `test_tc_bb_005_duplicate_email` (alias tương thích ngược)
- **Kết quả thực thi:** **PASS (2/2 Executions)**
- **Thời gian thực thi:** 77.26s (chạy cả 2 executions trên Samsung Galaxy S21 FE 5G với teardown cách ly an toàn).
- **Minh chứng thực tế:**
  - `evidence/fn02/FN02_TC-BB-005_D01_01.png`
  - `evidence/fn02/FN02_TC-BB-005_D02_01.png`
- **Kết quả kiểm thử hồi quy (Smoke Regression):** `pytest automation/tests/test_fn02_register.py -k "test_tc_bb_004b_d01_min_6_chars" -v -s` $\rightarrow$ **1 PASSED in 47.11s** (ca kiểm thử biên hợp lệ AT-09 trước đó hoạt động hoàn toàn ổn định).

### Iteration 11: AT-11 / TC-BB-006 (Đăng nhập tài khoản chuẩn đã kích hoạt vào HomeScreen)
- **Mã AT:** `AT-11`
- **Mã Manual TC:** `TC-BB-006`
- **Nhóm chức năng:** `FN-04` (Đăng nhập Email/Password)
- **Mức độ ưu tiên:** `P0`
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng nhập (`LoginScreen`); thiết bị có kết nối Internet ổn định; tài khoản `student_qa@gmail.com` tồn tại trên Firebase Auth và đã kích hoạt (`emailVerified = true`).
- **Dữ liệu kiểm thử (1 Execution):**
  - **D01:** Email `student_qa@gmail.com`, Mật khẩu `123456`.
- **Hành vi quan sát được (Observable UI Behavior):** Ứng dụng hiển thị chỉ báo tải trong giây lát, hoàn tất xác thực Firebase Auth và điều hướng thẳng vào màn hình Trang chủ ghi chú (`HomeScreen`) với thanh tìm kiếm và danh sách ghi chú; không xuất hiện thông báo lỗi nào trên màn hình — khớp hoàn toàn với đặc tả kỳ vọng.
- **File mã nguồn test:** [`automation/tests/test_fn04_login.py`](../../automation/tests/test_fn04_login.py)
  - `test_tc_bb_006_valid_email_login`
  - `test_tc_bb_006_d01_verified_account` (alias)
- **Kết quả thực thi:** **PASS (1/1 Execution)**
- **Thời gian thực thi:** 51.13s (chạy trên Samsung Galaxy S21 FE 5G với teardown đăng xuất tự động khôi phục LoginScreen).
- **Minh chứng thực tế:**
  - `evidence/fn04/FN04_TC-BB-006_D01_01.png`
- **Kết quả kiểm thử hồi quy (Smoke Regression):** `pytest automation/tests/test_fn04_login.py -k "test_tc_bb_009_empty_password" -v -s` $\rightarrow$ **1 PASSED in 22.64s** (ca kiểm thử thiếu mật khẩu trong FN-04 hoạt động hoàn toàn ổn định).

