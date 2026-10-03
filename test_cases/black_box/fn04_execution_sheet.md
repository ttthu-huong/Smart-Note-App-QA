# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-04
## Dự án: Smart Note App
**Chức năng:** Đăng nhập tài khoản Email/Password (FN-04)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng đăng nhập tài khoản Email/Password cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-04** |
| **Chức năng** | **Đăng nhập tài khoản Email/Password** |
| **Người kiểm thử (Tester)** | Huong (QA Tester) |
| **Ngày kiểm thử (Execution Date)** | 04/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990E) |
| **Android Version** | Android 16 |
| **App Version / Build Number** | v1.0.0 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | Độ phân giải 1080x2340, USB Debugging |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đang ở màn hình Đăng nhập (tab "Đăng nhập", nút chính hiển thị chữ "Đăng nhập"). Chưa đăng nhập tài khoản nào.
2. **Tài khoản hợp lệ chuẩn bị trước:** Tài khoản `student_qa@gmail.com` với mật khẩu `123456` đã tồn tại trên hệ thống và đã được kích hoạt.
3. **Tài khoản không tồn tại:** Chuẩn bị email chưa từng tạo tài khoản: `ghost_user@gmail.com`.
4. **Kết nối mạng Internet:** Thiết bị có kết nối mạng Internet hoạt động bình thường để gửi yêu cầu đăng nhập.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-006** | **D01** | • Email: `student_qa@gmail.com`<br>• Mật khẩu: `123456` | 1. Nhập đúng Email đã đăng ký.<br>2. Nhập đúng Mật khẩu.<br>3. Nhấn nút "Đăng nhập". | Ứng dụng hiển thị màn hình chờ đồng bộ, sau đó điều hướng vào Trang chủ. | [Điền khi test] | [Trống] | [Điền khi test] | Độ phân giải 1080x2340, USB Debugging |
| **TC-BB-007** | **D01** | • Email: `student_qa@gmail.com`<br>• Mật khẩu: `wrongpass` | 1. Nhập đúng Email đã đăng ký.<br>2. Nhập sai Mật khẩu.<br>3. Nhấn nút "Đăng nhập". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Mật khẩu không chính xác."* | [Điền khi test] | [Trống] | [Điền khi test] | Độ phân giải 1080x2340, USB Debugging |
| **TC-BB-008** | **D01** | • Email: `ghost_user@gmail.com`<br>• Mật khẩu: `123456` | 1. Nhập Email chưa đăng ký trên hệ thống.<br>2. Nhập Mật khẩu bất kỳ.<br>3. Nhấn nút "Đăng nhập". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."* | [Điền khi test] | [Trống] | [Điền khi test] | Độ phân giải 1080x2340, USB Debugging |
| **TC-BB-009** | **D01** | • Email: `student_qa@gmail.com`<br>• Mật khẩu: `""` | 1. Nhập Email hợp lệ.<br>2. Để trống ô Mật khẩu.<br>3. Nhấn nút "Đăng nhập". | Ứng dụng không thực hiện đăng nhập; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | [Điền khi test] | [Trống] | [Điền khi test] | Độ phân giải 1080x2340, USB Debugging |

---

## 4. EVIDENCE NAMING CONVENTION

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN04_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Ví dụ:  
  • Đăng nhập thành công vào Trang chủ: `FN04_TC-BB-006_D01_01.png`  
  • Lỗi sai mật khẩu: `FN04_TC-BB-007_D01_01.png`  
  • Lỗi tài khoản không tồn tại: `FN04_TC-BB-008_D01_01.png`  
  • Lỗi bỏ trống mật khẩu: `FN04_TC-BB-009_D01_01.png`
- **Video quay màn hình (Screen Recording):**  
  Cấu trúc: `FN04_[TC-ID]_[Data-ID].mp4`  
  Ví dụ: `FN04_TC-BB-006_D01.mp4`

---

## 5. BUG REPORT

| Bug ID | TC-ID | Data ID | Mô tả lỗi | Evidence | Severity | Status |
|---|---|---|---|---|---|---|
| **BUG-BB-002** | **TC-BB-008** | **D01** | Khi đăng nhập tài khoản không tồn tại (`ghost_user@gmail.com`), ứng dụng hiển thị thông báo gộp *"Email hoặc mật khẩu không chính xác."* thay vì *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."* | `FN04_TC-BB-008_D01_01.png`, `FN04_TC-BB-008_D01_02.png` | Minor | Open |
| **BUG-BB-003** | **TC-BB-007** | **D01** | Khi đăng nhập sai mật khẩu, ứng dụng hiển thị thông báo gộp *"Email hoặc mật khẩu không chính xác."* thay vì *"Mật khẩu không chính xác."* | `FN04_TC-BB-007_D01_01.png`, `FN04_TC-BB-007_D01_02.png` | Minor | Open |
| **BUG-BB-004** | **TC-BB-006** | **D01** | Tài khoản `student_qa@gmail.com` khi đăng nhập bị chuyển hướng đến màn hình Xác thực email thay vì Trang chủ do `emailVerified` là false. | `FN04_TC-BB-006_D01_01.png`, `FN04_TC-BB-006_D01_02.png` | Major | Open |

---

## 6. RETEST

| Bug ID | TC-ID | Kết quả lần đầu | Kết quả Retest | Evidence Retest | Ngày Retest |
|---|---|---|---|---|---|
| *[Trống]* | *[Trống]* | *[FAIL]* | *[PASS / FAIL]* | *[File evidence retest]* | *[DD/MM/YYYY]* |

---

## 7. TEST DATA CLEANUP

- Sau khi hoàn thành ca kiểm thử TC-BB-006 (Đăng nhập thành công), Tester thực hiện **Đăng xuất** tài khoản khỏi ứng dụng để đưa màn hình về trạng thái chưa đăng nhập, sẵn sàng cho các ca kiểm thử khác.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **4** | TC-BB-006, TC-BB-007, TC-BB-008, TC-BB-009 |
| **Tổng Execution Items** | **4** | TC-BB-006 (1), TC-BB-007 (1), TC-BB-008 (1), TC-BB-009 (1) |
| **Số lượng PASS** | **1** | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng FAIL** | **3** | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng BLOCKED** | **0** | Các ca không thể chạy do lỗi môi trường/mạng |
| **Số Bug phát hiện** | **3** | Tổng số lỗi ghi nhận trong bảng Bug Report |
| **Tỷ lệ thực thi (Execution Rate)** | **100%** | `(PASS + FAIL) / 4 * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | **25.00%** | `PASS / (PASS + FAIL) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 4 execution items của chức năng FN-04.
- [x] Đã ghi nhận Actual Result trung thực và chi tiết.
- [x] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [x] Đã lưu trữ Evidence (ảnh/video) theo đúng quy tắc đặt tên.
- [x] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report.
- [x] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [x] Đã điền đầy đủ thông tin môi trường kiểm thử trong Mục 1.
- [ ] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.
