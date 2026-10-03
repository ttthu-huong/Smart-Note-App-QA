# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-08
## Dự án: Smart Note App
**Chức năng:** Tạo Ghi chú văn bản mới (FN-08)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng tạo ghi chú văn bản mới cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-08** |
| **Chức năng** | **Tạo Ghi chú văn bản mới** |
| **Người kiểm thử (Tester)** | [Điền khi thực hiện] |
| **Ngày kiểm thử (Execution Date)** | [Điền khi thực hiện] (DD/MM/YYYY) |
| **Thiết bị kiểm thử (Device/Model)** | [Điền khi thực hiện] (VD: Pixel 7 / Samsung S22 / Android Emulator) |
| **Android Version** | [Điền khi thực hiện] (VD: Android 13, 14, 15) |
| **App Version / Build Number** | [Điền khi thực hiện] (VD: v1.0.0+1) |
| **Kết nối mạng** | [Wi-Fi / 4G / 5G / Offline] |
| **Ghi chú môi trường khác** | [Nếu có] |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đã đăng nhập vào ứng dụng và đang ở màn hình Trang chủ.
2. **Giao diện sẵn sàng:** Nút Tạo mới (+) hoặc tùy chọn tạo ghi chú văn bản hiển thị rõ ràng trên Trang chủ.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-016** | **D01** | • Tiêu đề: `"Họp Lab"`<br>• Nội dung: `"Nội dung ngắn gọn"` | 1. Nhấn nút Tạo mới (+) hoặc chọn "Văn bản".<br>2. Nhập Tiêu đề.<br>3. Nhập Nội dung.<br>4. Nhấn nút Quay lại (Back) trên thanh tiêu đề. | Thẻ ghi chú hiển thị đầy đủ tiêu đề và nội dung; xuất hiện ở đầu danh sách Trang chủ. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |
| **TC-BB-017** | **D01** | • Tiêu đề: `""`<br>• Nội dung: `"Ý tưởng nhanh không tiêu đề"` | 1. Mở màn hình soạn thảo ghi chú mới.<br>2. Để trống ô Tiêu đề.<br>3. Nhập nội dung văn bản.<br>4. Nhấn nút Quay lại (Back). | Ứng dụng quay về Trang chủ; ghi chú mới vẫn được tạo và xuất hiện trên danh sách với phần hiển thị xem trước là đoạn văn bản nội dung. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |
| **TC-BB-018** | **D01** | • Tiêu đề: `""`<br>• Nội dung: `""` | 1. Mở màn hình soạn thảo ghi chú mới.<br>2. Không nhập bất kỳ ký tự nào vào cả ô Tiêu đề và ô Nội dung.<br>3. Nhấn nút Quay lại (Back). | Ứng dụng quay về Trang chủ; không có bất kỳ ghi chú trống nào xuất hiện thêm trên danh sách. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |

---

## 4. EVIDENCE NAMING CONVENTION

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN08_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Ví dụ:  
  • Ghi chú văn bản ngắn tại Trang chủ: `FN08_TC-BB-016_D01_01.png`  
  • Ghi chú không tiêu đề hiển thị nội dung xem trước: `FN08_TC-BB-017_D01_01.png`  
  • Danh sách Trang chủ không xuất hiện note trống: `FN08_TC-BB-018_D01_01.png`
- **Video quay màn hình (Screen Recording):**  
  Cấu trúc: `FN08_[TC-ID]_[Data-ID].mp4`  
  Ví dụ: `FN08_TC-BB-016_D01.mp4`

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

- Sau khi hoàn thành kiểm thử, Tester chuyển các ghi chú được tạo trong quá trình kiểm thử vào Thùng rác để đưa dữ liệu kiểm thử về trạng thái phù hợp.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **3** | TC-BB-016, TC-BB-017, TC-BB-018 |
| **Tổng Execution Items** | **3** | TC-BB-016 (1), TC-BB-017 (1), TC-BB-018 (1) |
| **Số lượng PASS** | [Điền sau khi test] | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng FAIL** | [Điền sau khi test] | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng BLOCKED** | [Điền sau khi test] | Các ca không thể chạy do lỗi môi trường |
| **Số Bug phát hiện** | [Điền sau khi test] | Tổng số lỗi ghi nhận trong bảng Bug Report |
| **Tỷ lệ thực thi (Execution Rate)** | [Điền sau khi test] % | `(PASS + FAIL) / 3 * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | [Điền sau khi test] % | `PASS / (PASS + FAIL) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [ ] Đã thực hiện đầy đủ 3 execution items của chức năng FN-08.
- [ ] Đã ghi nhận Actual Result trung thực và chi tiết.
- [ ] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [ ] Đã lưu trữ Evidence (ảnh/video) theo đúng quy tắc đặt tên.
- [ ] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report.
- [ ] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [ ] Đã điền đầy đủ thông tin môi trường kiểm thử trong Mục 1.
- [ ] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.
