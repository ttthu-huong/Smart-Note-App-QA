# BÁO CÁO THỰC THI AUTOMATION TEST — FN-02 (REGISTER EMAIL)
## Dự án: Smart Note App
**Branch:** `huong`  
**Nhóm chức năng:** FN-02: Đăng ký tài khoản Email/Password  
**Danh sách Test Cases:** TC-BB-001, TC-BB-001B, TC-BB-002, TC-BB-002B, TC-BB-003, TC-BB-004, TC-BB-005  
**Framework:** Python 3.13 + pytest + uiautomator2 + ADB  
**Thiết bị thực thi:** Samsung Galaxy S21 FE 5G (SM-G990B / R5CW82ECF6M), Android 14 (API 34)  
**Ngày thực thi:** 05/10/2026  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual / Automation Execution  

---

## 1. TỔNG QUAN KẾT QUẢ THỰC THI TỰ ĐỘNG

| Chỉ số | Số lượng / Giá trị | Ghi chú |
|---|---:|---|
| **Tổng số Test Cases** | **5** | TC-BB-001 đến TC-BB-005 |
| **Số lượng PASS** | **4** | TC-BB-001, TC-BB-002, TC-BB-004, TC-BB-005 (**80.00%**) |
| **Số lượng FAIL** | **1** | TC-BB-003 (**20.00%**) do Application Bug BUG-FN02-01 |
| **Số lượng ERROR** | **0** | Kịch bản chạy thông suốt, không gặp lỗi môi trường |
| **Số lượng BLOCKED** | **0** | Cả 5 Test Case đều được thực thi trên thiết bị thật |
| **Thời gian thực thi** | **115.35s** (~1 phút 55 giây) | Chạy toàn bộ suite tuần tự (5 TCs) với cơ chế test isolation 2 lớp và chụp ảnh bằng chứng tự động |
| **Báo cáo JUnit XML** | [`fn02_register_junit.xml`](fn02_register_junit.xml) | Xuất tự động qua pytest |

---

## 2. BẢNG CHI TIẾT KẾT QUẢ TỪNG TEST CASE

| TC-ID | Data ID | Test Data | Expected Result (Đặc tả) | Actual Result (Thực tế trên UI) | Trạng thái | Bug ID | Phân tích chi tiết & Cơ chế xác minh | Evidence |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **TC-BB-001** (AT-01) | **D01** | • Email: `student_qa_<timestamp>@gmail.com`<br>• Mật khẩu: `123456` | Ứng dụng chuyển sang màn hình Xác thực Email (`EmailVerificationScreen`) và hiển thị hướng dẫn kiểm tra email. | Ứng dụng gửi thông tin đăng ký lên Firebase Auth thành công và điều hướng sang màn hình Xác thực Email với tiêu đề "Xác thực email của bạn". | **PASS** | — | Sử dụng timestamp để đảm bảo email luôn là tài khoản mới; Firebase tạo user, gửi email verification và Flutter chuyển màn hình chính xác. | [`FN02_TC-BB-001_D01_01.png`](../../evidence/fn02/FN02_TC-BB-001_D01_01.png) |
| **TC-BB-001** (AT-01) | **D02** | • Email: `user_dev_<timestamp>@outlook.com`<br>• Mật khẩu: `Abc@2026!` | Ứng dụng chuyển sang màn hình Xác thực Email (`EmailVerificationScreen`). | Ứng dụng gửi thông tin đăng ký với miền @outlook.com lên Firebase thành công và điều hướng sang màn hình Xác thực Email. | **PASS** | — | Kiểm tra đăng ký với tên miền Outlook và mật khẩu phức hợp ký tự đặc biệt; hệ thống chấp nhận và chuyển màn hình thành công. | [`FN02_TC-BB-001_D02_01.png`](../../evidence/fn02/FN02_TC-BB-001_D02_01.png) |
| **TC-BB-001** (AT-01) | **D03** | • Email: `sv_<timestamp>@hcmus.edu.vn`<br>• Mật khẩu: `MatKhauDai123` | Ứng dụng chuyển sang màn hình Xác thực Email (`EmailVerificationScreen`). | Ứng dụng gửi thông tin đăng ký với miền giáo dục .edu.vn lên Firebase thành công và điều hướng sang màn hình Xác thực Email. | **PASS** | — | Kiểm tra đăng ký với tên miền giáo dục (.edu.vn); hệ thống nhận diện đúng whitelist tên miền hợp lệ và chuyển màn hình thành công. | [`FN02_TC-BB-001_D03_01.png`](../../evidence/fn02/FN02_TC-BB-001_D03_01.png) |
| **TC-BB-001B** (AT-02) | **D01** | • Email: `"   student_trim_<timestamp>@gmail.com   "`<br>• Mật khẩu: `123456` | Hệ thống tự động cắt tỉa khoảng trắng đầu/cuối (`trim()`), chấp nhận email và chuyển sang màn hình Xác thực Email với địa chỉ đã cắt tỉa. | Hệ thống tự động trim khoảng trắng, tạo tài khoản Firebase thành công và điều hướng sang màn hình Xác thực Email hiển thị địa chỉ `student_trim_<timestamp>@gmail.com`. | **PASS** | — | Input sanitization / whitespace trimming hoạt động chính xác; uiautomator2 xác nhận chuỗi email đã cắt tỉa xuất hiện trên `EmailVerificationScreen`. | [`FN02_TC-BB-001B_D01_01.png`](../../evidence/fn02/FN02_TC-BB-001B_D01_01.png) |
| **TC-BB-002** (AT-03) | **D01** | • Email: `""`<br>• Mật khẩu: `""` | Ứng dụng không chuyển màn hình; xuất hiện khung thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Ứng dụng giữ nguyên màn hình Đăng ký; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | **PASS** | — | Client-side validation chặn ngay khi form rỗng trước khi gửi request mạng; giao diện phản hồi tức thì và chính xác. | [`FN02_TC-BB-002_D01_01.png`](../../evidence/fn02/FN02_TC-BB-002_D01_01.png) |
| **TC-BB-002B** (AT-04) | **D01** | • Email: `student_valid_<timestamp>@gmail.com`<br>• Mật khẩu: `""` | Ứng dụng không chuyển màn hình; xuất hiện khung thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Ứng dụng giữ nguyên màn hình Đăng ký; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | **PASS** | — | Client-side validation phát hiện mật khẩu để trống và chặn submit ngay lập tức; không gửi request mạng; giao diện hiển thị thông báo lỗi chính xác. | [`FN02_TC-BB-002B_D01_01.png`](../../evidence/fn02/FN02_TC-BB-002B_D01_01.png) |
| **TC-BB-003** | **D01** | • Email: `nguoidung_gmail.com`<br>• Mật khẩu: `123456` | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."* | Ứng dụng giữ nguyên màn hình Đăng ký; hiển thị thông báo lỗi màu đỏ: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* | **FAIL** | **BUG-FN02-01** | Hàm `_isValidDomain(email)` trong `auth_provider.dart` kiểm tra `email.split('@').length < 2` và trả về `false`, gán nhầm thông báo domain email rác thay vì báo lỗi định dạng email. Khớp hoàn toàn với phát hiện kiểm thử thủ công trong `fn02_execution_sheet.md`. | [`FN02_TC-BB-003_D01_01.png`](../../evidence/fn02/FN02_TC-BB-003_D01_01.png) |
| **TC-BB-004** | **D02** | • Email: `student_bva_<timestamp>@gmail.com`<br>• Mật khẩu: `12345` (5 ký tự) | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."* | Ứng dụng giữ nguyên màn hình Đăng ký; hiển thị thông báo lỗi màu đỏ: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."* | **PASS** | — | Kiểm tra giá trị biên cận dưới ($N - 1 = 5$ ký tự); Firebase Auth trả về `weak-password` và `_translateAuthError` ánh xạ thành công thông báo chuẩn. | [`FN02_TC-BB-004_D02_01.png`](../../evidence/fn02/FN02_TC-BB-004_D02_01.png) |
| **TC-BB-005** | **D01** | • Email: `student_qa@gmail.com`<br>• Mật khẩu: `123456` | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Email này đã được sử dụng cho một tài khoản khác."* | Ứng dụng giữ nguyên màn hình Đăng ký; hiển thị thông báo lỗi màu đỏ: *"Email này đã được sử dụng cho một tài khoản khác."* | **PASS** | — | Nhập email đã tồn tại trên hệ thống; Firebase Auth trả về mã lỗi `email-already-in-use`, giao diện hiển thị thông báo lỗi chính xác. | [`FN02_TC-BB-005_D01_01.png`](../../evidence/fn02/FN02_TC-BB-005_D01_01.png) |

---

## 3. DANH MỤC LỖI PHÁT HIỆN (BUG REPORT REFERENCE)

| Mã Bug (Bug ID) | Mã Test Case (TC-ID) | Mã dữ liệu (Data ID) | Tóm tắt mô tả lỗi quan sát được | Tệp bằng chứng đính kèm (Evidence) | Mức độ nghiêm trọng (Severity) | Trạng thái xử lý (Status) |
|:---:|:---:|:---:|---|---|:---:|:---:|
| **BUG-FN02-01** | **TC-BB-003** | **D01** | Khi nhập email thiếu ký tự `@` (`nguoidung_gmail.com`), ứng dụng hiển thị sai thông báo lỗi: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* thay vì *"Định dạng email không hợp lệ."* theo đặc tả. | [`FN02_TC-BB-003_D01_01.png`](../../evidence/fn02/FN02_TC-BB-003_D01_01.png) | **Minor** | **Confirmed (Application Bug)** |

---

## 4. CƠ CHẾ TỰ ĐỘNG HÓA VÀ ĐẶC ĐIỂM KỸ THUẬT

### A. Điều hướng và Quản lý State của Form Đăng ký
- Màn hình Đăng ký được tích hợp chung trong `LoginScreen` dưới dạng tab chuyển đổi trạng thái `_isLogin`.
- Kịch bản tự động kiểm tra trạng thái màn hình hiện tại: nếu đang ở Login mode, chạm vào `Đăng ký ngay` để chuyển sang Register mode.
- Trước mỗi test case, kịch bản reset form và xóa thông báo lỗi cũ `auth.error` thông qua hàm `reset_register_form()`, đảm bảo tính độc lập giữa các ca kiểm thử.

### B. Nhập liệu Obscured PasswordField trên Flutter
- Phân biệt trường Email và Mật khẩu dựa vào thuộc tính trợ năng `password="true"` (obscured) và `password="false"`.
- Sử dụng cơ chế kiểm chứng độ dài ký tự thực tế sau khi nhập; kích hoạt clipboard paste dự phòng nếu `set_text` trên trường mật khẩu không nhận đủ độ dài.

### C. Cơ chế dọn dẹp sau khi đăng ký thành công (Cleanup)
- Sau khi `TC-BB-001` đăng ký thành công và chuyển sang `EmailVerificationScreen`, kịch bản chạm vào nút `Quay lại đăng nhập` để đăng xuất phiên làm việc tạm thời và quay về màn hình ban đầu, đảm bảo không làm gián đoạn các test case tiếp theo.

---

## 5. TỔNG HỢP SỐ LIỆU AUTOMATION TOÀN HỆ THỐNG

| Nhóm chức năng | Tên nhóm | Tổng TCs | Đã Code & Chạy | PASS | FAIL | ERROR | Tỷ lệ PASS |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **FN-02** | Đăng ký tài khoản Email/Password | **5** | 5 | 4 | 1 | 0 | 80.00% |
| **FN-04** | Đăng nhập Email/Password | **4** | 4 | 1 | 3 | 0 | 25.00% |
| **FN-08** | Tạo Ghi chú văn bản mới | **3** | 3 | 3 | 0 | 0 | 100.00% |
| **FN-09** | Chỉnh sửa Ghi chú & Auto-save | **2** | 2 | 2 | 0 | 0 | 100.00% |
| **FN-20** | Ghim & Bỏ ghim Ghi chú | **2** | 2 | 2 | 0 | 0 | 100.00% |
| **FN-23** | Tìm kiếm Ghi chú (Search Note) | **4** | 4 | 4 | 0 | 0 | 100.00% |
| *Chưa automation* | FN-10/11/12 (Quản lý Thùng rác) | **3** | 0 | — | — | — | Planned |
| *Chưa automation* | FN-05 (2), FN-29/30 (4), FN-40/41 (2) | **8** | 0 | — | — | — | Deferred |
| **Tổng cộng** | **Toàn bộ hệ thống** | **31** | **20** | **16** | **4** | **0** | **80.00%** |

*Số liệu tổng hợp chuẩn xác toàn hệ thống:*
- **Độ bao phủ automation (Coverage):** 20/31 = **64.52%**
- **Tỷ lệ PASS trên số ca đã thực thi:** 16/20 = **80.00%** (16 PASS / 4 FAIL / 0 ERROR)
- **Tổng số ca chưa automation:** 11/31 = **35.48%** (3 Planned + 8 Deferred)
