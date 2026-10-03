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
| **Người kiểm thử (Tester)** | [Điền khi thực hiện] |
| **Ngày kiểm thử (Execution Date)** | [Điền khi thực hiện] (DD/MM/YYYY) |
| **Thiết bị kiểm thử (Device/Model)** | [Điền khi thực hiện] (VD: Pixel 7 / Samsung S22 / Android Emulator) |
| **Android Version** | [Điền khi thực hiện] (VD: Android 13, 14, 15) |
| **App Version / Build Number** | [Điền khi thực hiện] (VD: v1.0.0+1) |
| **Kết nối mạng** | [Wi-Fi / 4G / 5G] |
| **Ghi chú môi trường khác** | [Nếu có] |

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
| **TC-BB-006** | **D01** | • Email: `student_qa@gmail.com`<br>• Mật khẩu: `123456` | 1. Nhập đúng Email đã đăng ký.<br>2. Nhập đúng Mật khẩu.<br>3. Nhấn nút "Đăng nhập". | Ứng dụng hiển thị màn hình chờ đồng bộ, sau đó điều hướng vào Trang chủ. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |
| **TC-BB-007** | **D01** | • Email: `student_qa@gmail.com`<br>• Mật khẩu: `wrongpass` | 1. Nhập đúng Email đã đăng ký.<br>2. Nhập sai Mật khẩu.<br>3. Nhấn nút "Đăng nhập". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Mật khẩu không chính xác."* | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |
| **TC-BB-008** | **D01** | • Email: `ghost_user@gmail.com`<br>• Mật khẩu: `123456` | 1. Nhập Email chưa đăng ký trên hệ thống.<br>2. Nhập Mật khẩu bất kỳ.<br>3. Nhấn nút "Đăng nhập". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."* | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |
| **TC-BB-009** | **D01** | • Email: `student_qa@gmail.com`<br>• Mật khẩu: `""` | 1. Nhập Email hợp lệ.<br>2. Để trống ô Mật khẩu.<br>3. Nhấn nút "Đăng nhập". | Ứng dụng không thực hiện đăng nhập; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |

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
| *[Trống]* | *[Trống]* | *[Trống]* | *[Ghi nhận khi có bug]* | *[Tên file evidence]* | *[Critical / Major / Minor]* | *[Open / In Progress / Fixed]* |

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
| **Số lượng PASS** | [Điền sau khi test] | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng FAIL** | [Điền sau khi test] | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng BLOCKED** | [Điền sau khi test] | Các ca không thể chạy do lỗi môi trường/mạng |
| **Số Bug phát hiện** | [Điền sau khi test] | Tổng số lỗi ghi nhận trong bảng Bug Report |
| **Tỷ lệ thực thi (Execution Rate)** | [Điền sau khi test] % | `(PASS + FAIL) / 4 * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | [Điền sau khi test] % | `PASS / (PASS + FAIL) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [ ] Đã thực hiện đầy đủ 4 execution items của chức năng FN-04.
- [ ] Đã ghi nhận Actual Result trung thực và chi tiết.
- [ ] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [ ] Đã lưu trữ Evidence (ảnh/video) theo đúng quy tắc đặt tên.
- [ ] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report.
- [ ] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [ ] Đã điền đầy đủ thông tin môi trường kiểm thử trong Mục 1.
- [ ] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.
