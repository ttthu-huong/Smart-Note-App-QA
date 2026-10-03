# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-23
## Dự án: Smart Note App
**Chức năng:** Tìm kiếm Ghi chú theo từ khóa văn bản (FN-23)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng Tìm kiếm ghi chú theo tiêu đề, nội dung và ký tự đặc biệt cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-23** |
| **Chức năng** | **Tìm kiếm Ghi chú theo từ khóa văn bản** |
| **Người kiểm thử (Tester)** | Artemis QA Runner |
| **Ngày kiểm thử (Execution Date)** | 04/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990B) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | 1.0.0+1 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | [Nếu có] |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đang ở màn hình Trang chủ hoặc đã mở màn hình Tìm kiếm.
2. **Dữ liệu chuẩn bị trước trên Trang chủ:**
   - Ghi chú 1: Tiêu đề `"Kế hoạch"`, nội dung bất kỳ.
   - Ghi chú 2: Tiêu đề `"Tạp vụ"`, nội dung chứa đoạn: `"mua thêm giấy in A4"`.
   - Đảm bảo **không** có ghi chú nào chứa chuỗi từ khóa `"chuoi_khong_ton_tai_999"`.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-026** | **D01** | Từ khóa: `"Kế hoạch"` | 1. Chạm vào thanh "Tìm kiếm" ở đầu Trang chủ.<br>2. Nhập từ khóa có dấu `"Kế hoạch"`. | Danh sách tìm kiếm hiển thị các ghi chú có tiêu đề chứa chữ "Kế hoạch". | Chạm thanh Tìm kiếm trên Trang chủ, nhập từ khóa "Kế hoạch". Danh sách hiển thị "TÌM THẤY 1 GHI CHÚ KHỚP" và trả về đúng ghi chú có tiêu đề chứa chữ "Kế hoạch". | PASS | FN23_TC-BB-026_D01_01.png | - |
| **TC-BB-027** | **D01** | Từ khóa: `"giấy in A4"` | 1. Mở màn hình tìm kiếm.<br>2. Nhập từ khóa `"giấy in A4"`. | Danh sách kết quả hiển thị thẻ ghi chú "Tạp vụ" có chứa đoạn văn bản tương ứng trong phần nội dung. | Nhập từ khóa "giấy in A4" vào ô tìm kiếm. Danh sách kết quả hiển thị "TÌM THẤY 1 GHI CHÚ KHỚP" với thẻ ghi chú "Tạp vụ" có chứa đoạn "mua thêm giấy in A4" trong nội dung. | PASS | FN23_TC-BB-027_D01_01.png | - |
| **TC-BB-028** | **D01** | Từ khóa: `"chuoi_khong_ton_tai_999"` | 1. Mở màn hình tìm kiếm.<br>2. Nhập chuỗi từ khóa ngẫu nhiên không có thật. | Danh sách không có ghi chú nào; màn hình hiển thị biểu tượng tìm kiếm rỗng kèm thông báo: *"Không tìm thấy kết quả"* và *"Thử từ khóa khác"*. | Nhập từ khóa ngẫu nhiên không tồn tại "chuoi_khong_ton_tai_999". Không có ghi chú nào hiển thị; màn hình hiển thị biểu tượng tìm kiếm rỗng kèm thông báo "Không tìm thấy kết quả" và "Thử từ khóa khác". | PASS | FN23_TC-BB-028_D01_01.png | - |
| **TC-BB-029** | **D01** | Từ khóa: `'" OR '1'='1"` | 1. Mở màn hình tìm kiếm.<br>2. Nhập chuỗi ký tự đặc biệt dạng logic mệnh đề. | Ứng dụng không bị đóng đột ngột, hiển thị trạng thái tìm kiếm rỗng an toàn (*"Không tìm thấy kết quả"*). | Nhập chuỗi ký tự đặc biệt dạng logic mệnh đề ' OR '1'='1. Ứng dụng xử lý an toàn, không bị crash, hiển thị trạng thái tìm kiếm rỗng an toàn ("Không tìm thấy kết quả", "Thử từ khóa khác"). | PASS | FN23_TC-BB-029_D01_01.png | - |

---

## 4. EVIDENCE NAMING CONVENTION

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN23_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Ví dụ:  
  • Kết quả tìm kiếm từ khóa có dấu: `FN23_TC-BB-026_D01_01.png`  
  • Kết quả tìm kiếm khớp phần nội dung: `FN23_TC-BB-027_D01_01.png`  
  • Giao diện tìm kiếm rỗng khi không có kết quả: `FN23_TC-BB-028_D01_01.png`  
  • Giao diện tìm kiếm ký tự logic an toàn: `FN23_TC-BB-029_D01_01.png`
- **Video quay màn hình (Screen Recording):**  
  Cấu trúc: `FN23_[TC-ID]_[Data-ID].mp4`  
  Ví dụ: `FN23_TC-BB-026_D01.mp4`

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

- Xóa các ghi chú test dữ liệu tìm kiếm (`Kế hoạch`, `Tạp vụ`) nếu không còn phục vụ cho các ca kiểm thử khác.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **4** | TC-BB-026, TC-BB-027, TC-BB-028, TC-BB-029 |
| **Tổng Execution Items** | **4** | TC-BB-026 (1), TC-BB-027 (1), TC-BB-028 (1), TC-BB-029 (1) |
| **Số lượng PASS** | 4 |
| **Số lượng FAIL** | 0 |
| **Số lượng BLOCKED** | 0 |
| **Số Bug phát hiện** | 0 |
| **Tỷ lệ thực thi (Execution Rate)** | 100% |
| **Tỷ lệ đạt (Pass Rate)** | 100% |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 4 execution items của chức năng FN-23.
- [x] Đã ghi nhận Actual Result trung thực và chi tiết.
- [x] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [x] Đã lưu trữ Evidence (ảnh/video) theo đúng quy tắc đặt tên.
- [x] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report.
- [x] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [x] Đã điền đầy đủ thông tin môi trường kiểm thử trong Mục 1.
- [x] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.
