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
| **Người kiểm thử (Tester)** | QA Tester (Autonomous Execution) |
| **Ngày kiểm thử (Execution Date)** | 04/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990B / R5CW82ECF6M) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | v1.0.0+1 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | Google Play Services có sẵn tài khoản Google trên máy |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đang ở màn hình Đăng nhập (chưa đăng nhập tài khoản nào).
2. **Tài khoản Google trên thiết bị:** Thiết bị kiểm thử (hoặc máy ảo Android có Google Play Services) đã đăng nhập sẵn ít nhất một tài khoản Google hợp lệ.
3. **Kết nối mạng Internet:** Thiết bị có kết nối mạng Internet hoạt động ổn định.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-010** | **D01** | Thao tác: Chọn tài khoản Google hiển thị trên hộp thoại | 1. Nhấn nút "Đăng nhập bằng Google".<br>2. Trên hộp thoại hệ thống xuất hiện, chạm chọn tài khoản Google của bạn. | Hộp thoại chọn tài khoản đóng lại; ứng dụng hiển thị màn hình chờ đồng bộ, sau đó điều hướng vào Trang chủ. | Hộp thoại chọn tài khoản Google xuất hiện. Khi nhấn chọn tài khoản Google (Thu Hường - ht158713@gmail.com), hộp thoại đóng lại và ứng dụng điều hướng thành công vào Trang chủ, hiển thị danh sách ghi chú và nút thêm ghi chú (+). | PASS | `FN05_TC-BB-010_D01_01.png`<br>`FN05_TC-BB-010_D01_02.png` | [Không] |
| **TC-BB-011** | **D01** | Thao tác: Hủy chọn tài khoản trên hộp thoại | 1. Nhấn nút "Đăng nhập bằng Google".<br>2. Khi hộp thoại danh sách tài khoản hiện lên, chạm vào vùng ngoài hoặc nhấn nút Quay lại (Back). | Hộp thoại đóng lại; ứng dụng không bị đóng đột ngột, vẫn giữ nguyên tại màn hình Đăng nhập và không hiển thị lỗi. | Khi hộp thoại tài khoản Google xuất hiện, nhấn Back, hộp thoại đóng lại ngay lập tức; ứng dụng vẫn ở màn hình Đăng nhập ổn định, không crash, không hiển thị lỗi. | PASS | `FN05_TC-BB-011_D01_01.png` | [Không] |

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
| *[Không có lỗi]* | - | - | Không phát sinh lỗi trong quá trình kiểm thử FN-05 | - | - | - |

---

## 6. RETEST

| Bug ID | TC-ID | Kết quả lần đầu | Kết quả Retest | Evidence Retest | Ngày Retest |
|---|---|---|---|---|---|
| *[Không có]* | - | - | - | - | - |

---

## 7. TEST DATA CLEANUP

- Sau khi kiểm thử thành công TC-BB-010, tài khoản Google được duy trì đăng nhập để tiếp tục phục vụ kiểm thử các chức năng ghi chú (FN-08, FN-09, FN-10/11/12, FN-20, FN-23) trước khi thực hiện nhóm Đăng xuất (FN-29/FN-30).

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **2** | TC-BB-010, TC-BB-011 |
| **Tổng Execution Items** | **2** | TC-BB-010 (1), TC-BB-011 (1) |
| **Số lượng PASS** | **2** | Cả 2 ca đều hoạt động đúng thiết kế |
| **Số lượng FAIL** | **0** | Không có ca nào thất bại |
| **Số lượng BLOCKED** | **0** | Không có ca nào bị chặn |
| **Số Bug phát hiện** | **0** | Không có bug |
| **Tỷ lệ thực thi (Execution Rate)** | **100%** | `(2 / 2) * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | **100%** | `(2 / 2) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 2 execution items của chức năng FN-05.
- [x] Đã ghi nhận Actual Result trung thực và chi tiết.
- [x] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [x] Đã lưu trữ Evidence (ảnh/video) theo đúng quy tắc đặt tên.
- [x] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report (không có fail).
- [x] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [x] Đã điền đầy đủ thông tin môi trường kiểm thử trong Mục 1.
- [x] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.