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
- **Tổng số lượt thực thi (Planned Executions):** **74 Lượt**
- **Số Test Cases đã hoàn thành triển khai & xác thực thực tế:** **05 / 61 Test Cases**
  - `AT-21` (`TC-BB-011`): PASS (Feasibility Validation)
  - `AT-59` (`TC-BB-015`): PASS (Feasibility Validation)
  - `AT-60` (`TC-BB-015C`): PASS WITH PRECONDITION (Feasibility Validation)
  - `AT-01` (`TC-BB-001`): **PASS (Full Implementation: D01, D02, D03 — 3/3 executions)**
- **Số Test Cases còn lại cần triển khai tuần tự:** **56 Test Cases**

---

## II. BẢNG TRUY VẾT & KẾT QUẢ THỰC THI CHI TIẾT TỪNG AT-ID (TRACEABILITY LOG)

| STT | AT-ID | Manual TC ID | Nhóm FN | Execution ID / Dataset | Automation Test Method | Kết quả | Thời gian | Bằng chứng kiểm thử (Evidence) | Khiếm khuyết (Defect/Bug) |
|:---:|:---:|:---:|:---:|:---:|:---|:---:|:---:|:---|:---:|
| 1 | **AT-01** | `TC-BB-001` | FN-02 | **D01** (Gmail hợp lệ) | `test_tc_bb_001_d01_gmail_success` | **PASS** | ~48s | [`evidence/fn02/FN02_TC-BB-001_D01_01.png`](../../evidence/fn02/FN02_TC-BB-001_D01_01.png) | Không |
| 2 | **AT-01** | `TC-BB-001` | FN-02 | **D02** (Outlook hợp lệ) | `test_tc_bb_001_d02_outlook_success` | **PASS** | ~49s | [`evidence/fn02/FN02_TC-BB-001_D02_01.png`](../../evidence/fn02/FN02_TC-BB-001_D02_01.png) | Không |
| 3 | **AT-01** | `TC-BB-001` | FN-02 | **D03** (Edu hợp lệ) | `test_tc_bb_001_d03_edu_success` | **PASS** | ~50s | [`evidence/fn02/FN02_TC-BB-001_D03_01.png`](../../evidence/fn02/FN02_TC-BB-001_D03_01.png) | Không |
| 4 | **AT-02** | `TC-BB-001B` | FN-02 | **D01** (Khoảng trắng đầu/cuối) | `test_tc_bb_001b_trim_whitespace` | **PASS** | ~54s | [`evidence/fn02/FN02_TC-BB-001B_D01_01.png`](../../evidence/fn02/FN02_TC-BB-001B_D01_01.png) | Không |
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
