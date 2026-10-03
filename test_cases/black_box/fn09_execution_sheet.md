# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-09
## Dự án: Smart Note App
**Chức năng:** Chỉnh sửa Ghi chú & Tự động lưu (FN-09)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng chỉnh sửa ghi chú và tự động lưu (auto-save) cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-09** |
| **Chức năng** | **Chỉnh sửa Ghi chú & Tự động lưu** |
| **Người kiểm thử (Tester)** | [Điền khi thực hiện] |
| **Ngày kiểm thử (Execution Date)** | [Điền khi thực hiện] (DD/MM/YYYY) |
| **Thiết bị kiểm thử (Device/Model)** | [Điền khi thực hiện] (VD: Pixel 7 / Samsung S22 / Android Emulator) |
| **Android Version** | [Điền khi thực hiện] (VD: Android 13, 14, 15) |
| **App Version / Build Number** | [Điền khi thực hiện] (VD: v1.0.0+1) |
| **Kết nối mạng** | [Wi-Fi / 4G / 5G / Offline] |
| **Ghi chú môi trường khác** | [Nếu có] |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đã đăng nhập và đang ở màn hình Trang chủ.
2. **Dữ liệu chuẩn bị trước:** Có ít nhất một ghi chú văn bản sẵn có trên Trang chủ để tiến hành mở ra chỉnh sửa.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-019** | **D01** | Nhập thêm chuỗi: `"[Đã cập nhật lúc 10:00]"` | 1. Chạm vào ghi chú để mở màn hình soạn thảo.<br>2. Nhập thêm nội dung mới vào phần văn bản.<br>3. Nhấn nút Quay lại (Back). | Ứng dụng quay về Trang chủ; thẻ ghi chú phản ánh nội dung mới vừa chỉnh sửa. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |
| **TC-BB-020** | **D01** | Đoạn văn bản: `"Nội dung kiểm tra tự động lưu"` | 1. Mở một ghi chú hiện có.<br>2. Gõ thêm nội dung mới vào vùng soạn thảo.<br>3. Ngừng nhập khoảng 1 giây (để cơ chế tự động lưu kích hoạt).<br>4. Thoát màn hình ghi chú (nhấn Back hoặc phím Home/Recent).<br>5. Mở lại ghi chú. | Nội dung vừa nhập vẫn còn nguyên vẹn sau khi mở lại ghi chú. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |

---

## 4. EVIDENCE NAMING CONVENTION

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN09_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Ví dụ:  
  • Thẻ ghi chú phản ánh nội dung đã cập nhật: `FN09_TC-BB-019_D01_01.png`  
  • Ghi chú mở lại vẫn giữ nguyên nội dung tự động lưu: `FN09_TC-BB-020_D01_01.png`
- **Video quay màn hình (Screen Recording):**  
  Cấu trúc: `FN09_[TC-ID]_[Data-ID].mp4`  
  Ví dụ: `FN09_TC-BB-020_D01.mp4`

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

- Khôi phục nội dung ghi chú về trạng thái ban đầu hoặc xóa ghi chú thử nghiệm sau khi hoàn thành chuỗi test.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **2** | TC-BB-019, TC-BB-020 |
| **Tổng Execution Items** | **2** | TC-BB-019 (1), TC-BB-020 (1) |
| **Số lượng PASS** | [Điền sau khi test] | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng FAIL** | [Điền sau khi test] | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng BLOCKED** | [Điền sau khi test] | Các ca không thể chạy do lỗi môi trường |
| **Số Bug phát hiện** | [Điền sau khi test] | Tổng số lỗi ghi nhận trong bảng Bug Report |
| **Tỷ lệ thực thi (Execution Rate)** | [Điền sau khi test] % | `(PASS + FAIL) / 2 * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | [Điền sau khi test] % | `PASS / (PASS + FAIL) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [ ] Đã thực hiện đầy đủ 2 execution items của chức năng FN-09.
- [ ] Đã ghi nhận Actual Result trung thực và chi tiết.
- [ ] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [ ] Đã lưu trữ Evidence (ảnh/video) theo đúng quy tắc đặt tên.
- [ ] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report.
- [ ] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [ ] Đã điền đầy đủ thông tin môi trường kiểm thử trong Mục 1.
- [ ] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.
