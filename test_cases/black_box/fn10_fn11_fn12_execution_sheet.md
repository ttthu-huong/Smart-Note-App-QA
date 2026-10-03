# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-10 / FN-11 / FN-12
## Dự án: Smart Note App
**Chức năng:** Quản lý vòng đời Ghi chú (Xóa vào Thùng rác, Khôi phục, Xóa vĩnh viễn) (FN-10, FN-11, FN-12)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công vòng đời ghi chú (chuyển thùng rác, khôi phục, xóa vĩnh viễn) cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-10, FN-11, FN-12** |
| **Chức năng** | **Quản lý vòng đời Ghi chú (Xóa, Khôi phục, Xóa vĩnh viễn)** |
| **Người kiểm thử (Tester)** | Artemis QA Runner |
| **Ngày kiểm thử (Execution Date)** | 04/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990B) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | 1.0.0+1 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | [Nếu có] |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đang ở màn hình Trang chủ (`HomeScreen`).
2. **Dữ liệu chuẩn bị trước:**
   - Có ít nhất một ghi chú trên Trang chủ để thực hiện xóa vào Thùng rác (TC-BB-021).
   - Có ít nhất một ghi chú nằm trong Thùng rác (`TrashScreen`) để thực hiện Khôi phục (TC-BB-022) và Xóa vĩnh viễn (TC-BB-023).

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-021** | **D01** | Thao tác: Chọn xóa 1 ghi chú | 1. Nhấn giữ thẻ ghi chú để chọn (hoặc mở menu tùy chọn của ghi chú).<br>2. Nhấn biểu tượng Thùng rác trên thanh công cụ. | Ghi chú biến mất khỏi danh sách Trang chủ; xuất hiện thanh thông báo bên dưới: *"Đã chuyển 1 ghi chú vào thùng rác"* kèm nút *"Hoàn tác"*. | Nhấn giữ ghi chú trên Trang chủ và nhấn biểu tượng Thùng rác trên thanh công cụ. Ghi chú lập tức biến mất khỏi Trang chủ; xuất hiện thanh thông báo bên dưới: "Đã chuyển 1 ghi chú vào thùng rác" cùng nút "Hoàn tác". | PASS | FN10_11_12_TC-BB-021_D01_01.png | - |
| **TC-BB-022** | **D01** | Thao tác: Nhấn "Khôi phục" | 1. Mở ngăn kéo điều hướng (Drawer), chọn "Thùng rác".<br>2. Chọn ghi chú cần khôi phục.<br>3. Nhấn nút "Khôi phục". | Ghi chú biến mất khỏi màn hình Thùng rác; thanh thông báo hiển thị: *"Đã khôi phục ghi chú"*; quay về Trang chủ thấy ghi chú đã xuất hiện lại. | Mở Drawer vào Thùng rác, chọn ghi chú và nhấn "Khôi phục ghi chú". Ghi chú biến mất khỏi Thùng rác (hiển thị "Thùng rác trống"), xuất hiện thông báo "Đã khôi phục ghi chú"; quay về Trang chủ ghi chú đã xuất hiện lại đầy đủ. | PASS | FN10_11_12_TC-BB-022_D01_01.png | - |
| **TC-BB-023** | **D01** | Thao tác: Nhấn "Xóa" trên hộp thoại | 1. Vào màn hình Thùng rác.<br>2. Chọn ghi chú và nhấn biểu tượng "Xóa vĩnh viễn".<br>3. Trên hộp thoại cảnh báo 'Xóa vĩnh viễn?', nhấn nút "Xóa". | Hộp thoại đóng lại; ghi chú biến mất hoàn toàn khỏi danh sách Thùng rác; quay lại Trang chủ ghi chú cũng không còn tồn tại trên ứng dụng. | Vào Thùng rác, nhấn giữ chọn ghi chú và nhấn icon "Xóa vĩnh viễn". Hộp thoại xác nhận 'Xóa vĩnh viễn?' hiển thị với cảnh báo và nút "Xóa", "Hủy". Nhấn nút "Xóa", hộp thoại đóng lại, ghi chú bị xóa hoàn toàn khỏi Thùng rác ("Thùng rác trống") và vĩnh viễn không còn trên ứng dụng. | PASS | FN10_11_12_TC-BB-023_D01_01.png | - |

---

## 4. EVIDENCE NAMING CONVENTION

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN10_11_12_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Ví dụ:  
  • Thông báo chuyển ghi chú vào thùng rác: `FN10_11_12_TC-BB-021_D01_01.png`  
  • Ghi chú khôi phục thành công về Trang chủ: `FN10_11_12_TC-BB-022_D01_01.png`  
  • Hộp thoại xác nhận và kết quả xóa vĩnh viễn: `FN10_11_12_TC-BB-023_D01_01.png`
- **Video quay màn hình (Screen Recording):**  
  Cấu trúc: `FN10_11_12_[TC-ID]_[Data-ID].mp4`  
  Ví dụ: `FN10_11_12_TC-BB-021_D01.mp4`

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

- Sau khi kiểm thử vòng đời hoàn tất, kiểm tra dọn sạch các ghi chú rác còn sót lại trong Thùng rác nếu cần thiết.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **3** | TC-BB-021, TC-BB-022, TC-BB-023 |
| **Tổng Execution Items** | **3** | TC-BB-021 (1), TC-BB-022 (1), TC-BB-023 (1) |
| **Số lượng PASS** | 3 | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng FAIL** | 0 | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng BLOCKED** | 0 | Các ca không thể chạy do lỗi môi trường |
| **Số Bug phát hiện** | 0 | Tổng số lỗi ghi nhận trong bảng Bug Report |
| **Tỷ lệ thực thi (Execution Rate)** | 100% | `(PASS + FAIL) / 3 * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | 100% | `PASS / (PASS + FAIL) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 3 execution items của nhóm chức năng FN-10 / FN-11 / FN-12.
- [x] Đã ghi nhận Actual Result trung thực và chi tiết.
- [x] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [x] Đã lưu trữ Evidence (ảnh/video) theo đúng quy tắc đặt tên.
- [x] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report.
- [x] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [x] Đã điền đầy đủ thông tin môi trường kiểm thử trong Mục 1.
- [x] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.
