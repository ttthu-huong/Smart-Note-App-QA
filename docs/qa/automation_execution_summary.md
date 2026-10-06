# BÁO CÁO TỔNG HỢP KẾT QUẢ THỰC THI KIỂM THỬ TỰ ĐỘNG (AUTOMATION SUMMARY)
## Dự án: Smart Note App
**Branch kiểm thử:** `huong`  
**Ngày cập nhật:** 05/10/2026  
**Thiết bị thực thi:** Samsung Galaxy S21 FE 5G (SM-G990B / R5CW82ECF6M), Android 14 (API 34)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual / Automation Test Execution  

---

## 1. TỔNG QUAN TÌNH TRẠNG THỰC THI AUTOMATION

| Chỉ số đo lường | Số lượng | Tỷ lệ (%) | Ghi chú |
|---|---:|---:|---|
| **Tổng số Black-box Test Cases** | **31** | 100.00% | Theo đặc tả `black_box_test_cases.md` |
| **Test Cases đã có code tự động** | **20** | **64.52%** | FN-02 (5 TCs), FN-04 (4 TCs), FN-08 (3 TCs), FN-09 (2 TCs), FN-20 (2 TCs), FN-23 (4 TCs) |
| **Test Cases đã thực thi (Executed)** | **20** | **64.52%** | Chạy E2E hoàn chỉnh trên thiết bị thật |
| **Test Cases đạt yêu cầu (PASS)** | **16** | **80.00%** | Tính trên tổng số ca đã thực thi (16/20) |
| **Test Cases thất bại (FAIL)** | **4** | **20.00%** | Tính trên tổng số ca đã thực thi (4/20) |
| **Test Cases gặp lỗi script (ERROR)** | **0** | **0.00%** | Không có lỗi script / crash môi trường |
| **Test Cases chưa automation** | **11** | **35.48%** | Gồm 3 Planned + 8 Deferred (11/31) |
| **Test Cases tạm hoãn (Deferred)** | **8** | 25.81% | Do phụ thuộc OAuth, Sinh trắc học, Mạng đa thiết bị |
| **Test Cases đang lên kế hoạch (Planned)** | **3** | 9.68% | Nhóm FN-10/11/12 (3 TCs) |

---

## 2. BẢNG TIẾN ĐỘ VÀ KẾT QUẢ CHI TIẾT TỪNG TEST CASE (31 TCs)

| TC-ID | Chức năng (FN) | Tên kịch bản kiểm thử | Automated? | Script Path | Executed? | Result | Ghi chú phân loại / Bug ID |
|:--- |:--- |:--- |:---:|:--- |:---:|:---:|:--- |
| **TC-BB-001** | FN-02: Đăng ký tài khoản Email | Đăng ký tài khoản với Email và Mật khẩu hợp lệ | **Yes** | `automation/tests/test_fn02_register.py` | **Yes** | **PASS** | — |
| **TC-BB-002** | FN-02 | Để trống thông tin khi đăng ký | **Yes** | `automation/tests/test_fn02_register.py` | **Yes** | **PASS** | — |
| **TC-BB-003** | FN-02 | Đăng ký với định dạng Email không hợp lệ | **Yes** | `automation/tests/test_fn02_register.py` | **Yes** | **FAIL** | BUG-FN02-01 (Sai thông báo lỗi email) |
| **TC-BB-004** | FN-02 | Đăng ký với mật khẩu ngắn dưới 6 ký tự | **Yes** | `automation/tests/test_fn02_register.py` | **Yes** | **PASS** | — |
| **TC-BB-005** | FN-02 | Đăng ký với email đã tồn tại trên hệ thống | **Yes** | `automation/tests/test_fn02_register.py` | **Yes** | **PASS** | — |
| **TC-BB-006** | FN-04: Đăng nhập tài khoản Email/Password | Đăng nhập thành công với tài khoản Email hợp lệ | **Yes** | `automation/tests/test_fn04_login.py` | **Yes** | **FAIL** | Precondition Issue: Tài khoản test chưa verify email |
| **TC-BB-007** | FN-04 | Đăng nhập thất bại do sai Mật khẩu | **Yes** | `automation/tests/test_fn04_login.py` | **Yes** | **FAIL** | BUG-BB-003 (Thông báo Firebase gộp) |
| **TC-BB-008** | FN-04 | Đăng nhập thất bại do tài khoản không tồn tại | **Yes** | `automation/tests/test_fn04_login.py` | **Yes** | **FAIL** | BUG-BB-002 (Thông báo Firebase gộp) |
| **TC-BB-009** | FN-04 | Đăng nhập thất bại do để trống Mật khẩu | **Yes** | `automation/tests/test_fn04_login.py` | **Yes** | **PASS** | — |
| **TC-BB-010** | FN-05: Đăng nhập nhanh Google | Đăng nhập thành công qua tài khoản Google | No | — | No | — | — |
| **TC-BB-011** | FN-05 | Hủy quá trình đăng nhập Google | No | — | No | — | — |
| **TC-BB-012** | FN-29/FN-30: Khóa & Mở khóa Ghi chú bằng Sinh trắc học | Kích hoạt khóa sinh trắc học cho ghi chú | No | — | No | — | — |
| **TC-BB-013** | FN-29/FN-30 | Mở khóa ghi chú bằng sinh trắc học thành công | No | — | No | — | — |
| **TC-BB-014** | FN-29/FN-30 | Mở khóa ghi chú bằng sinh trắc học thất bại | No | — | No | — | — |
| **TC-BB-015** | FN-29/FN-30 | Tắt tính năng khóa sinh trắc học cho ghi chú | No | — | No | — | — |
| **TC-BB-016** | FN-08: Tạo Ghi chú văn bản mới | Tạo ghi chú văn bản có Tiêu đề và Nội dung | **Yes** | `automation/tests/test_fn08_create_note.py` | **Yes** | **PASS** | — |
| **TC-BB-017** | FN-08 | Tạo ghi chú không có tiêu đề nhưng có nội dung. | **Yes** | `automation/tests/test_fn08_create_note.py` | **Yes** | **PASS** | — |
| **TC-BB-018** | FN-08 | Tạo ghi chú với cả tiêu đề và nội dung để trống; xác minh ứng dụng không tạo ghi chú rỗng. | **Yes** | `automation/tests/test_fn08_create_note.py` | **Yes** | **PASS** | — |
| **TC-BB-019** | FN-09: Chỉnh sửa Ghi chú & Tự động lưu | Chỉnh sửa nội dung ghi chú. | **Yes** | `automation/tests/test_fn09_edit_note.py` | **Yes** | **PASS** | — |
| **TC-BB-020** | FN-09 | Kiểm tra tự động lưu nội dung sau khi chỉnh sửa và rời màn hình. | **Yes** | `automation/tests/test_fn09_edit_note.py` | **Yes** | **PASS** | — |
| **TC-BB-021** | FN-10/FN-11/FN-12: Xóa vào Thùng rác / Khôi phục / Xóa vĩnh viễn | Chuyển ghi chú vào Thùng rác | No | — | No | — | — |
| **TC-BB-022** | FN-10/FN-11/FN-12 | Khôi phục ghi chú từ Thùng rác về Trang chủ | No | — | No | — | — |
| **TC-BB-023** | FN-10/FN-11/FN-12 | Xóa vĩnh viễn ghi chú khỏi Thùng rác | No | — | No | — | — |
| **TC-BB-024** | FN-20: Ghim & Bỏ ghim Ghi chú | Ghim ghi chú lên đầu danh sách Trang chủ | **Yes** | `automation/tests/test_fn20_pin_note.py` | **Yes** | **PASS** | — |
| **TC-BB-025** | FN-20 | Bỏ ghim ghi chú trở về danh sách thông thường | **Yes** | `automation/tests/test_fn20_pin_note.py` | **Yes** | **PASS** | — |
| **TC-BB-026** | FN-23: Tìm kiếm Ghi chú theo từ khóa | Tìm kiếm ghi chú theo từ khóa Tiêu đề | **Yes** | `automation/tests/test_fn23_search.py` | **Yes** | **PASS** | — |
| **TC-BB-027** | FN-23 | Tìm kiếm ghi chú theo từ khóa Nội dung | **Yes** | `automation/tests/test_fn23_search.py` | **Yes** | **PASS** | — |
| **TC-BB-028** | FN-23 | Tìm kiếm với từ khóa không tồn tại | **Yes** | `automation/tests/test_fn23_search.py` | **Yes** | **PASS** | — |
| **TC-BB-029** | FN-23 | Tìm kiếm với chuỗi Ký tự đặc biệt / Robustness | **Yes** | `automation/tests/test_fn23_search.py` | **Yes** | **PASS** | — |
| **TC-BB-030** | FN-40/FN-41: Đồng bộ Offline/Online & Giải quyết xung đột LWW | Tạo ghi chú ngoại tuyến và tự động đồng bộ khi có mạng | No | — | No | — | — |
| **TC-BB-031** | FN-40/FN-41 | Giải quyết xung đột chỉnh sửa đồng thời theo nguyên tắc LWW | No | — | No | — | — |

---

## 3. PHÂN TÍCH CHI TIẾT CÁC CA KIỂM THỬ THẤT BẠI (FAIL ANALYSIS)

### A. Nhóm Application Bugs (Đã xác nhận lỗi ứng dụng)
1. **TC-BB-003 (BUG-FN02-01):**
   - **Mục tiêu:** Kiểm tra thông báo khi nhập email sai định dạng (thiếu `@`).
   - **Thực tế:** Email `nguoidung_gmail.com` thiếu ký tự `@`, nhưng ứng dụng hiển thị: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* thay vì *"Định dạng email không hợp lệ."*.
   - **Kỳ vọng:** Ứng dụng phải hiển thị *"Định dạng email không hợp lệ."* theo đặc tả.
   - **Nguyên nhân gốc:** Trong `auth_provider.dart`, hàm `_isValidDomain(email)` kiểm tra `email.split('@').length < 2` và trả về `false`, khiến hệ thống báo lỗi domain rác trước khi Firebase kiểm tra định dạng email hợp lệ.
   - **Kết luận:** **Application Bug**.

2. **TC-BB-007 (BUG-BB-003):**
   - **Mục tiêu:** Kiểm tra thông báo khi nhập sai mật khẩu.
   - **Thực tế:** Cả Email và Mật khẩu đều được nhập thành công trên giao diện (`student_qa@gmail.com` và `wrongpass`), nhưng ứng dụng hiển thị thông báo gộp Firebase: *"Email hoặc mật khẩu không chính xác."*.
   - **Kỳ vọng:** Ứng dụng phải chỉ rõ *"Mật khẩu không chính xác."* theo đặc tả.
   - **Kết luận:** Application Bug do mã nguồn ánh xạ Firebase exception `invalid-credential` sang thông báo chung chung.

3. **TC-BB-008 (BUG-BB-002):**
   - **Mục tiêu:** Kiểm tra thông báo khi đăng nhập tài khoản không tồn tại.
   - **Thực tế:** Cả Email và Mật khẩu đều được nhập thành công trên giao diện (`ghost_user@gmail.com` và `123456`), nhưng ứng dụng hiển thị thông báo gộp Firebase: *"Email hoặc mật khẩu không chính xác."*.
   - **Kỳ vọng:** Ứng dụng phải hiển thị *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."* theo đặc tả.
   - **Kết luận:** Application Bug do Firebase Auth v10+ trả về mã lỗi gộp để bảo mật, ứng dụng chưa xử lý phân tách theo đúng yêu cầu nghiệp vụ.

### B. Nhóm Precondition / Test Data Issue (Không khẳng định là Bug ứng dụng)
1. **TC-BB-006:**
   - **Mục tiêu:** Đăng nhập thành công và điều hướng vào Trang chủ (`HomeScreen`).
   - **Thực tế:** Credentials được nhập thành công (`student_qa@gmail.com` / `123456`), nhưng ứng dụng chuyển hướng sang `EmailVerificationScreen`.
   - **Nguyên nhân gốc:** Tài khoản test `student_qa@gmail.com` có trường `emailVerified: false` trong Firebase Authentication. Ứng dụng kiểm tra trạng thái này và chủ động chặn người dùng chưa xác thực email theo đúng luồng bảo vệ.
   - **Kết luận:** **Test Data / Precondition Issue**. Không kết luận đây là Application Bug nếu chưa cung cấp tài khoản test thỏa mãn tiền điều kiện `emailVerified: true`.

---

## 4. BẢNG TỔNG KẾT THEO NHÓM CHỨC NĂNG (AUTOMATION COVERAGE)

| Nhóm chức năng | Tên nhóm | Tổng TCs | Implemented | Executed | PASS | FAIL | ERROR | Tỷ lệ PASS/Executed |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **FN-02** | Đăng ký tài khoản Email | 5 | 5 | 5 | 4 | 1 | 0 | 80.00% |
| **FN-04** | Đăng nhập tài khoản Email/Password | 4 | 4 | 4 | 1 | 3 | 0 | 25.00% |
| **FN-08** | Tạo Ghi chú văn bản mới | 3 | 3 | 3 | 3 | 0 | 0 | 100.00% |
| **FN-09** | Chỉnh sửa Ghi chú & Tự động lưu | 2 | 2 | 2 | 2 | 0 | 0 | 100.00% |
| **FN-20** | Ghim & Bỏ ghim Ghi chú | 2 | 2 | 2 | 2 | 0 | 0 | 100.00% |
| **FN-23** | Tìm kiếm Ghi chú (Search Note) | 4 | 4 | 4 | 4 | 0 | 0 | 100.00% |
| **FN-10/11/12**| Quản lý Thùng rác | 3 | 0 | 0 | — | — | — | Planned |
| **FN-05** | Đăng nhập Google (OAuth) | 2 | 0 | 0 | — | — | — | Deferred |
| **FN-29/30** | Khóa sinh trắc học | 4 | 0 | 0 | — | — | — | Deferred |
| **FN-40/41** | Đồng bộ Offline/Online | 2 | 0 | 0 | — | — | — | Deferred |
| **Tổng cộng** | **Toàn bộ hệ thống** | **31** | **20** | **20** | **16** | **4** | **0** | **80.00%** |

*Số liệu tổng hợp chuẩn xác toàn hệ thống:*
- **Độ bao phủ automation (Coverage):** 20/31 = **64.52%**
- **Tỷ lệ PASS trên số ca đã thực thi:** 16/20 = **80.00%** (16 PASS / 4 FAIL / 0 ERROR)
- **Tổng số ca chưa automation:** 11/31 = **35.48%** (3 Planned + 8 Deferred)
