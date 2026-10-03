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
| **Người kiểm thử (Tester)** | QA Tester (Autonomous Execution) |
| **Ngày kiểm thử (Execution Date)** | 04/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990B / R5CW82ECF6M) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | v1.0.0+1 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | Tài khoản Google đang đăng nhập |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đã đăng nhập vào ứng dụng và đang ở màn hình Trang chủ.
2. **Giao diện sẵn sàng:** Nút Tạo mới (+) hoặc tùy chọn tạo ghi chú văn bản hiển thị rõ ràng trên Trang chủ.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-016** | **D01** | • Tiêu đề: `"Họp Lab"`<br>• Nội dung: `"Nội dung ngắn gọn"` | 1. Nhấn nút Tạo mới (+) hoặc chọn "Văn bản".<br>2. Nhập Tiêu đề.<br>3. Nhập Nội dung.<br>4. Nhấn nút Quay lại (Back) trên thanh tiêu đề. | Thẻ ghi chú hiển thị đầy đủ tiêu đề và nội dung; xuất hiện ở đầu danh sách Trang chủ. | Thẻ ghi chú hiển thị đầy đủ tiêu đề "Họp Lab" và nội dung "Nội dung ngắn gọn", xuất hiện ở đầu danh sách mục "Khác" trên Trang chủ. | PASS | `FN08_TC-BB-016_D01_01.png` | [Không] |
| **TC-BB-017** | **D01** | • Tiêu đề: `""`<br>• Nội dung: `"Ý tưởng nhanh không tiêu đề"` | 1. Mở màn hình soạn thảo ghi chú mới.<br>2. Để trống ô Tiêu đề.<br>3. Nhập nội dung văn bản.<br>4. Nhấn nút Quay lại (Back). | Ứng dụng quay về Trang chủ; ghi chú mới vẫn được tạo và xuất hiện trên danh sách với phần hiển thị xem trước là đoạn văn bản nội dung. | Ứng dụng quay về Trang chủ; ghi chú không tiêu đề được lưu thành công, hiển thị xem trước nội dung "Ý tưởng nhanh không tiêu đề" trên danh sách. | PASS | `FN08_TC-BB-017_D01_01.png` | [Không] |
| **TC-BB-018** | **D01** | • Tiêu đề: `""`<br>• Nội dung: `""` | 1. Mở màn hình soạn thảo ghi chú mới.<br>2. Không nhập bất kỳ ký tự nào vào cả ô Tiêu đề và ô Nội dung.<br>3. Nhấn nút Quay lại (Back). | Ứng dụng quay về Trang chủ; không có bất kỳ ghi chú trống nào xuất hiện thêm trên danh sách. | Ứng dụng quay về Trang chủ; không có bất kỳ ghi chú trống nào xuất hiện thêm trên danh sách Trang chủ. | PASS | `FN08_TC-BB-018_D01_01.png` | [Không] |

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
| *[Không có lỗi]* | - | - | Không phát sinh lỗi trong quá trình kiểm thử FN-08 | - | - | - |

---

## 6. RETEST

| Bug ID | TC-ID | Kết quả lần đầu | Kết quả Retest | Evidence Retest | Ngày Retest |
|---|---|---|---|---|---|
| *[Không có]* | - | - | - | - | - |

---

## 7. TEST DATA CLEANUP

- Các ghi chú vừa tạo sẽ được tiếp tục sử dụng để kiểm thử các chức năng tiếp theo: xem chi tiết, chỉnh sửa (FN-09), ghim, xóa vào thùng rác (FN-10/11/12), tìm kiếm (FN-23) trước khi dọn dẹp.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **3** | TC-BB-016, TC-BB-017, TC-BB-018 |
| **Tổng Execution Items** | **3** | TC-BB-016 (1), TC-BB-017 (1), TC-BB-018 (1) |
| **Số lượng PASS** | **3** | Toàn bộ 3 ca đều đạt yêu cầu |
| **Số lượng FAIL** | **0** | Không có ca nào thất bại |
| **Số lượng BLOCKED** | **0** | Không có ca nào bị chặn |
| **Số Bug phát hiện** | **0** | Không có bug |
| **Tỷ lệ thực thi (Execution Rate)** | **100%** | `(3 / 3) * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | **100%** | `(3 / 3) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 3 execution items của chức năng FN-08.
- [x] Đã ghi nhận Actual Result trung thực và chi tiết.
- [x] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [x] Đã lưu trữ Evidence (ảnh/video) theo đúng quy tắc đặt tên.
- [x] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report (không có fail).
- [x] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [x] Đã điền đầy đủ thông tin môi trường kiểm thử trong Mục 1.
- [x] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.