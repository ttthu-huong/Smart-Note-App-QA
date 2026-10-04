# BÁO CÁO THỰC THI AUTOMATION TEST — FN-04 (LOGIN)
## Dự án: Smart Note App
**Branch:** `huong`  
**Nhóm chức năng:** FN-04: Đăng nhập tài khoản Email/Password  
**Framework:** pytest + uiautomator2 (ARTEMIS Mobile Automation)  
**Thiết bị thực thi:** Samsung Galaxy S21 FE 5G (SM-G990E), Android 14 (API 34)  
**Ngày thực thi:** 04/10/2026  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual / Automation Execution  

---

## 1. TỔNG QUAN KẾT QUẢ THỰC THI TỰ ĐỘNG

| Chỉ số | Số lượng / Giá trị | Ghi chú |
|---|---:|---|
| **Tổng số Test Cases** | **4** | TC-BB-006, TC-BB-007, TC-BB-008, TC-BB-009 |
| **Số lượng PASS** | **1** | TC-BB-009 (25.00%) |
| **Số lượng FAIL** | **3** | TC-BB-006, TC-BB-007, TC-BB-008 (75.00%) |
| **Số lượng BLOCKED** | **0** | Đã tháo gỡ, chạy 100% trên thiết bị thật |
| **Thời gian thực thi** | **65.89s** | Chạy tuần tự và chụp ảnh screenshot tự động |
| **Phân loại thất bại** | **100% Application Bugs** | Không có lỗi do Test Setup hay Môi trường |

---

## 2. BẢNG CHI TIẾT KẾT QUẢ TỪNG TEST CASE

| TC-ID | Data ID | Test Data | Expected Result | Actual Result | Trạng thái | Bug ID | Nguyên nhân / Phân tích | Evidence |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **TC-BB-009** | **D01** | • Email: `student_qa@gmail.com`<br>• Password: `""` | Ứng dụng hiển thị thông báo lỗi: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Ứng dụng hiển thị chính xác: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | **PASS** | — | Validation client bắt đúng lỗi bỏ trống mật khẩu. | [`FN04_TC-BB-009_D01_01.png`](../../evidence/fn04/FN04_TC-BB-009_D01_01.png) |
| **TC-BB-008** | **D01** | • Email: `ghost_user@gmail.com`<br>• Password: `123456` | Ứng dụng hiển thị thông báo lỗi: *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."* | Ứng dụng hiển thị thông báo gộp: *"Email hoặc mật khẩu không chính xác."* | **FAIL** | **BUG-BB-002** | Firebase Auth trả về mã lỗi gộp `invalid-credential` nhằm bảo mật chống dò quét tài khoản, ứng dụng hiển thị thông báo chung thay vì thông báo riêng biệt theo đặc tả. | [`FN04_TC-BB-008_D01_01.png`](../../evidence/fn04/FN04_TC-BB-008_D01_01.png) |
| **TC-BB-007** | **D01** | • Email: `student_qa@gmail.com`<br>• Password: `wrongpass` | Ứng dụng hiển thị thông báo lỗi: *"Mật khẩu không chính xác."* | Ứng dụng hiển thị thông báo gộp: *"Email hoặc mật khẩu không chính xác."* | **FAIL** | **BUG-BB-003** | Firebase Auth phiên bản mới trả về `invalid-credential` khi sai mật khẩu, ứng dụng chưa phân biệt chi tiết theo đặc tả IEEE. | [`FN04_TC-BB-007_D01_01.png`](../../evidence/fn04/FN04_TC-BB-007_D01_01.png) |
| **TC-BB-006** | **D01** | • Email: `student_qa@gmail.com`<br>• Password: `123456` | Ứng dụng điều hướng vào Trang chủ (HomeScreen). | Ứng dụng điều hướng vào Màn hình xác thực email (`EmailVerificationScreen`). | **FAIL** | **BUG-BB-004** | Tài khoản `student_qa@gmail.com` có trường `emailVerified` là `false` trong Firebase Authentication, nên logic chuyển trang chặn vào Trang chủ. | [`FN04_TC-BB-006_D01_01.png`](../../evidence/fn04/FN04_TC-BB-006_D01_01.png) |

---

## 3. CƠ CHẾ TỰ ĐỘNG HÓA VÀ ĐỘ ỔN ĐỊNH
- **Dynamic-First Selector:** Tìm kiếm phần tử thông minh hỗ trợ Flutter thông qua cả `text`, `content-description` và `xpath`.
- **Coordinate-Fallback:** Bổ sung tọa độ click dự phòng trong trường hợp phần tử bị bàn phím ảo che khuất hoặc layout thay đổi.
- **Auto-Teardown & Recovery:** Nếu test case điều hướng sang màn hình Xác thực email, kịch bản tự động nhấn "Quay lại đăng nhập" để khôi phục trạng thái Login Screen cho các lần chạy tiếp theo.
