# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-05
## Dự án: Smart Note App
**Chức năng:** Đăng nhập nhanh Google (Google Sign-In) (FN-05)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng đăng nhập tài khoản Google cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-05** |
| **Chức năng** | **Đăng nhập nhanh Google (Google Sign-In)** |
| **Người kiểm thử (Tester)** | [Điền khi thực hiện] |
| **Ngày kiểm thử (Execution Date)** | [Điền khi thực hiện] (DD/MM/YYYY) |
| **Thiết bị kiểm thử (Device/Model)** | [Điền khi thực hiện] (VD: Pixel 7 / Samsung S22 / Android Emulator) |
| **Android Version** | [Điền khi thực hiện] (VD: Android 13, 14, 15) |
| **App Version / Build Number** | [Điền khi thực hiện] (VD: v1.0.0+1) |
| **Kết nối mạng** | [Wi-Fi / 4G / 5G] |
| **Ghi chú môi trường khác** | [Nếu có] |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đang ở màn hình Đăng nhập (chưa đăng nhập tài khoản nào).
2. **Tài khoản Google trên thiết bị:** Thiết bị kiểm thử (hoặc máy ảo Android có Google Play Services) đã đăng nhập sẵn ít nhất một tài khoản Google hợp lệ.
3. **Kết nối mạng Internet:** Thiết bị có kết nối mạng Internet hoạt động ổn định.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-010** | **D01** | Thao tác: Chọn tài khoản Google hiển thị trên hộp thoại | 1. Nhấn nút "Đăng nhập bằng Google".<br>2. Trên hộp thoại hệ thống xuất hiện, chạm chọn tài khoản Google của bạn. | Hộp thoại chọn tài khoản đóng lại; ứng dụng hiển thị màn hình chờ đồng bộ, sau đó điều hướng vào Trang chủ. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |
| **TC-BB-011** | **D01** | Thao tác: Hủy chọn tài khoản trên hộp thoại | 1. Nhấn nút "Đăng nhập bằng Google".<br>2. Khi hộp thoại danh sách tài khoản hiện lên, chạm vào vùng ngoài hoặc nhấn nút Quay lại (Back). | Hộp thoại đóng lại; ứng dụng không bị đóng đột ngột, vẫn giữ nguyên tại màn hình Đăng nhập và không hiển thị lỗi. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |

---

## 4. EVIDENCE NAMING CONVENTION

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN05_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Ví dụ:  
  • Hộp thoại chọn Google Account: `FN05_TC-BB-010_D01_01.png`  
  • Đăng nhập thành công vào Trang chủ: `FN05_TC-BB-010_D01_02.png`  
  • Giao diện sau khi hủy chọn tài khoản Google: `FN05_TC-BB-011_D01_01.png`
- **Video quay màn hình (Screen Recording):**  
  Cấu trúc: `FN05_[TC-ID]_[Data-ID].mp4`  
  Ví dụ: `FN05_TC-BB-010_D01.mp4`

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

- Sau khi kiểm thử thành công TC-BB-010, Tester thực hiện **Đăng xuất** tài khoản Google để trả ứng dụng về màn hình Đăng nhập ban đầu.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **2** | TC-BB-010, TC-BB-011 |
| **Tổng Execution Items** | **2** | TC-BB-010 (1), TC-BB-011 (1) |
| **Số lượng PASS** | [Điền sau khi test] | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng FAIL** | [Điền sau khi test] | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng BLOCKED** | [Điền sau khi test] | Các ca không thể chạy do lỗi môi trường/mạng |
| **Số Bug phát hiện** | [Điền sau khi test] | Tổng số lỗi ghi nhận trong bảng Bug Report |
| **Tỷ lệ thực thi (Execution Rate)** | [Điền sau khi test] % | `(PASS + FAIL) / 2 * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | [Điền sau khi test] % | `PASS / (PASS + FAIL) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [ ] Đã thực hiện đầy đủ 2 execution items của chức năng FN-05.
- [ ] Đã ghi nhận Actual Result trung thực và chi tiết.
- [ ] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [ ] Đã lưu trữ Evidence (ảnh/video) theo đúng quy tắc đặt tên.
- [ ] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report.
- [ ] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [ ] Đã điền đầy đủ thông tin môi trường kiểm thử trong Mục 1.
- [ ] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.
