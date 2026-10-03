# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-20
## Dự án: Smart Note App
**Chức năng:** Ghim & Bỏ ghim Ghi chú (Pin Note) (FN-20)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng Ghim và Bỏ ghim ghi chú ưu tiên cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-20** |
| **Chức năng** | **Ghim & Bỏ ghim Ghi chú (Pin Note)** |
| **Người kiểm thử (Tester)** | [Điền khi thực hiện] |
| **Ngày kiểm thử (Execution Date)** | [Điền khi thực hiện] (DD/MM/YYYY) |
| **Thiết bị kiểm thử (Device/Model)** | [Điền khi thực hiện] (VD: Pixel 7 / Samsung S22 / Android Emulator) |
| **Android Version** | [Điền khi thực hiện] (VD: Android 13, 14, 15) |
| **App Version / Build Number** | [Điền khi thực hiện] (VD: v1.0.0+1) |
| **Kết nối mạng** | [Wi-Fi / 4G / 5G / Không bắt buộc] |
| **Ghi chú môi trường khác** | [Nếu có] |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đang ở màn hình Trang chủ (`HomeScreen`).
2. **Dữ liệu chuẩn bị trước:**
   - Có ít nhất một ghi chú nằm ở phần danh sách thông thường trên Trang chủ (chưa được ghim) để thực hiện TC-BB-024.
   - Có ít nhất một ghi chú đang nằm trong phân vùng "Được ghim" để thực hiện TC-BB-025.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-024** | **D01** | Thao tác: Ghim ghi chú | 1. Nhấn giữ thẻ ghi chú hoặc mở màn hình soạn thảo.<br>2. Nhấn biểu tượng Ghim (📌). | Trang chủ xuất hiện tiêu đề phân vùng *"Được ghim"*; thẻ ghi chú di chuyển lên nằm trong khu vực *"Được ghim"* ở phía trên cùng. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |
| **TC-BB-025** | **D01** | Thao tác: Bỏ ghim ghi chú | 1. Nhấn biểu tượng Bỏ ghim trên thẻ ghi chú đang được ghim. | Thẻ ghi chú chuyển xuống phân vùng ghi chú thông thường bên dưới; nếu không còn ghi chú nào được ghim, tiêu đề *"Được ghim"* tự động ẩn đi. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |

---

## 4. EVIDENCE NAMING CONVENTION

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN20_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Ví dụ:  
  • Ghi chú chuyển lên phân vùng 'Được ghim': `FN20_TC-BB-024_D01_01.png`  
  • Bỏ ghim đưa ghi chú về danh sách thường: `FN20_TC-BB-025_D01_01.png`
- **Video quay màn hình (Screen Recording):**  
  Cấu trúc: `FN20_[TC-ID]_[Data-ID].mp4`  
  Ví dụ: `FN20_TC-BB-024_D01.mp4`

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

- Đưa các ghi chú về trạng thái ghim/bỏ ghim mong muốn sau khi hoàn thành phiên kiểm thử.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **2** | TC-BB-024, TC-BB-025 |
| **Tổng Execution Items** | **2** | TC-BB-024 (1), TC-BB-025 (1) |
| **Số lượng PASS** | [Điền sau khi test] | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng FAIL** | [Điền sau khi test] | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng BLOCKED** | [Điền sau khi test] | Các ca không thể chạy do lỗi môi trường |
| **Số Bug phát hiện** | [Điền sau khi test] | Tổng số lỗi ghi nhận trong bảng Bug Report |
| **Tỷ lệ thực thi (Execution Rate)** | [Điền sau khi test] % | `(PASS + FAIL) / 2 * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | [Điền sau khi test] % | `PASS / (PASS + FAIL) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [ ] Đã thực hiện đầy đủ 2 execution items của chức năng FN-20.
- [ ] Đã ghi nhận Actual Result trung thực và chi tiết.
- [ ] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [ ] Đã lưu trữ Evidence (ảnh/video) theo đúng quy tắc đặt tên.
- [ ] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report.
- [ ] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [ ] Đã điền đầy đủ thông tin môi trường kiểm thử trong Mục 1.
- [ ] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.
