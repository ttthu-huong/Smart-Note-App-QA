# BÁO CÁO THỰC THI AUTOMATION TEST — FN-04 (LOGIN)
## Dự án: Smart Note App
**Branch:** `huong`  
**Nhóm chức năng:** FN-04: Đăng nhập tài khoản Email/Password  
**Danh sách Test Cases:** TC-BB-006 → TC-BB-009 (tổng 4 items)  
**Framework:** Python 3.13 + pytest + uiautomator2 + ADB  
**Thiết bị thực thi:** Samsung Galaxy S21 FE 5G (SM-G990E / R5CW82ECF6M), Android 16 (API 36)  
**Ngày thực thi & Cập nhật:** 05/10/2026  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual / Automation Execution  

---

## 1. TỔNG QUAN KẾT QUẢ THỰC THI TỰ ĐỘNG

| Chỉ số | Số lượng / Giá trị | Ghi chú |
|---|---:|---|
| **Tổng số Test Cases** | **4** | TC-BB-006, TC-BB-007, TC-BB-008, TC-BB-009 |
| **Số lượng PASS** | **2** | TC-BB-006, TC-BB-009 (50.00%) |
| **Số lượng FAIL** | **2** | TC-BB-007, TC-BB-008 (50.00%) |
| **Số lượng ERROR** | **0** | Toàn bộ 4 ca chạy trọn vẹn từ đầu đến cuối kịch bản |
| **Số lượng BLOCKED** | **0** | Cả 4 Test Case đều được thực thi trên thiết bị thật |
| **Thời gian thực thi** | **65.89s** | Chạy tuần tự và chụp ảnh screenshot tự động |
| **Phân loại thất bại** | **Application Bugs** | 2 Application Bugs (BUG-BB-002, BUG-BB-003) |

---

## 2. BẢNG CHI TIẾT KẾT QUẢ TỪNG TEST CASE

| TC-ID | Data ID | Test Data | Expected Result (Đặc tả) | Actual Result (Thực tế trên UI) | Trạng thái | Phân loại / Bug ID | Nguyên nhân / Phân tích chi tiết | Evidence |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **TC-BB-009** | **D01** | • Email: `student_qa@gmail.com`<br>• Password: `""` | Ứng dụng hiển thị thông báo lỗi: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Ứng dụng hiển thị chính xác: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | **PASS** | — | Validation client bắt đúng lỗi bỏ trống mật khẩu khi để trống Password. | [`FN04_TC-BB-009_D01_01.png`](../../evidence/fn04/FN04_TC-BB-009_D01_01.png) |
| **TC-BB-008** | **D01** | • Email: `ghost_user@gmail.com`<br>• Password: `123456` | Ứng dụng hiển thị thông báo lỗi: *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."* | Ứng dụng hiển thị thông báo gộp: *"Email hoặc mật khẩu không chính xác."* | **FAIL** | **BUG-BB-002** (Application Bug) | Cả Email và Mật khẩu đều đã được xác minh nhập đầy đủ vào giao diện trước khi submit (`len=20` và `len=6`). Ứng dụng trả về thông báo gộp Firebase `invalid-credential`, khác với Expected Result chi tiết của Test Case. | [`FN04_TC-BB-008_D01_01.png`](../../evidence/fn04/FN04_TC-BB-008_D01_01.png) |
| **TC-BB-007** | **D01** | • Email: `student_qa@gmail.com`<br>• Password: `wrongpass` | Ứng dụng hiển thị thông báo lỗi: *"Mật khẩu không chính xác."* | Ứng dụng hiển thị thông báo gộp: *"Email hoặc mật khẩu không chính xác."* | **FAIL** | **BUG-BB-003** (Application Bug) | Cả Email và Mật khẩu đều đã được xác minh nhập đầy đủ vào giao diện trước khi submit (`len=20` và `len=9`). Ứng dụng trả về thông báo gộp Firebase `invalid-credential`, khác với Expected Result chi tiết của Test Case. | [`FN04_TC-BB-007_D01_01.png`](../../evidence/fn04/FN04_TC-BB-007_D01_01.png) |
| **TC-BB-006** (AT-11) | **D01** | • Email: `student_qa@gmail.com`<br>• Password: `123456` | Ứng dụng điều hướng vào Trang chủ (HomeScreen); không xuất hiện thông báo lỗi. | Ứng dụng đăng nhập thành công, hoàn tất tải dữ liệu và điều hướng thẳng vào màn hình Trang chủ (`HomeScreen`). | **PASS** | — | Tài khoản chuẩn hợp lệ đã kích hoạt (`emailVerified = true`); kịch bản tự động hóa xác minh chuyển trang thành công và thực hiện teardown đăng xuất cách ly an toàn. | [`FN04_TC-BB-006_D01_01.png`](../../evidence/fn04/FN04_TC-BB-006_D01_01.png) |

---

## 3. CƠ CHẾ TỰ ĐỘNG HÓA VÀ ĐỘ ỔN ĐỊNH
- **Accessibility-First Selector:** Định danh chính xác trường Email qua `@password="false"` và trường Password qua `@password="true"` trên cây Accessibility của Flutter, tránh trượt focus do dùng index hay instance.
- **Direct Synchronous Input:** Nhập liệu bằng `set_text` trực tiếp qua Android Accessibility `ACTION_SET_TEXT`, đảm bảo đồng bộ vào `TextEditingController` của Flutter mà không phụ thuộc FastInputIME.
- **Xác minh trường trước khi Submit:** Kịch bản kiểm tra độ dài và giá trị thực tế của cả 2 field trước khi bấm Đăng nhập, loại trừ hoàn toàn rủi ro Automation Input Failure.
- **Auto-Teardown & Recovery:** Nếu test case điều hướng sang màn hình Xác thực email, kịch bản tự động nhấn *"Quay lại đăng nhập"* để khôi phục trạng thái Login Screen cho các lần chạy tiếp theo.
