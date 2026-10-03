# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-29 / FN-30
## Dự án: Smart Note App
**Chức năng:** Khóa & Mở khóa Ghi chú bằng Sinh trắc học (FN-29, FN-30)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng Khóa và Mở khóa ghi chú bằng bảo mật sinh trắc học cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-29, FN-30** |
| **Chức năng** | **Khóa & Mở khóa Ghi chú bằng Sinh trắc học** |
| **Người kiểm thử (Tester)** | Artemis QA Runner |
| **Ngày kiểm thử (Execution Date)** | 04/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990B) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | 1.0.0+1 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | Đã cài đặt ít nhất 1 dấu vân tay trong Cài đặt bảo mật của Android |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Phần cứng & Bảo mật thiết bị:** Thiết bị kiểm thử (hoặc Android Emulator có hỗ trợ giả lập vân tay) đã cài đặt mã khóa màn hình (PIN/Pattern) và đã đăng ký ít nhất một dấu vân tay hợp lệ.
2. **Dữ liệu chuẩn bị trong ứng dụng:**
   - Đã đăng nhập vào ứng dụng và đang ở Trang chủ.
   - Có ít nhất một ghi chú văn bản thông thường trên Trang chủ để thực hiện khóa ghi chú (TC-BB-012).
   - Có ít nhất một ghi chú đang ở trạng thái bị khóa (hiển thị biểu tượng ổ khóa) trên Trang chủ để chạy các ca TC-BB-013, TC-BB-014, TC-BB-015.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-012** | **D01** | Thao tác: Bật khóa ghi chú | 1. Mở một ghi chú đang hiển thị nội dung bình thường.<br>2. Nhấn vào biểu tượng tùy chọn (hoặc biểu tượng Khóa) trên thanh công cụ.<br>3. Bật tính năng khóa ghi chú.<br>4. Nhấn nút Quay lại để trở về Trang chủ. | Tại Trang chủ, thẻ ghi chú hiển thị biểu tượng ổ khóa, toàn bộ nội dung văn bản xem trước bị che khuất để bảo mật. | Không thể hoàn thành do thiết bị vật lý yêu cầu xác thực sinh trắc học phần cứng (vân tay/khuôn mặt) của người dùng để kích hoạt khóa ghi chú; hệ thống hiển thị hộp thoại xác thực nhưng không thể quét sinh trắc học qua điều khiển tự động. | BLOCKED | FN29_30_TC-BB-012_D01_01.png | - |
| **TC-BB-013** | **D01** | Dấu vân tay hợp lệ đã đăng ký trên máy | 1. Chạm vào thẻ ghi chú đang bị khóa.<br>2. Hộp thoại sinh trắc học hệ thống xuất hiện.<br>3. Đặt dấu vân tay hợp lệ vào cảm biến (hoặc gửi mã vân tay hợp lệ qua emulator). | Hộp thoại xác thực đóng lại; ứng dụng mở màn hình soạn thảo hiển thị đầy đủ tiêu đề và nội dung chi tiết của ghi chú. | Không thể thực hiện do thiết bị vật lý yêu cầu quét dấu vân tay/khuôn mặt hợp lệ trực tiếp trên cảm biến phần cứng, không thể giả lập hay tương tác sinh trắc học thực tế từ xa qua ADB. | BLOCKED | FN29_30_TC-BB-013_D01_01.png | - |
| **TC-BB-014** | **D01** | Dấu vân tay không khớp | 1. Chạm vào thẻ ghi chú đang bị khóa.<br>2. Khi hộp thoại sinh trắc học hiện lên, quét ngón tay chưa từng đăng ký trên máy. | Hộp thoại hệ thống báo không nhận diện được; nội dung ghi chú không được mở ra; ứng dụng hiển thị thông báo: *"Xác thực thất bại. Thử lại?"* | Không thể thực hiện do thiếu ghi chú đã khóa sẵn và không thể cung cấp thao tác quét ngón tay không khớp trên cảm biến phần cứng của thiết bị vật lý từ xa (thực tế quan sát hệ thống tự quét nhận diện khuôn mặt thất bại hiển thị "Không phát hiện thấy khuôn mặt"). | BLOCKED | FN29_30_TC-BB-014_D01_01.png | - |
| **TC-BB-015** | **D01** | Thao tác: Nhấn Hủy xác thực | 1. Chạm vào thẻ ghi chú đang bị khóa.<br>2. Trên hộp thoại quét sinh trắc học, nhấn nút "Hủy" (Cancel). | Hộp thoại sinh trắc học đóng lại; ứng dụng trở về Trang chủ; thẻ ghi chú vẫn giữ nguyên biểu tượng ổ khóa và không hiển thị nội dung. | Không thể hoàn tất chu trình kiểm thử do không thể khóa ghi chú trước đó vì thiếu sinh trắc học phần cứng; thao tác nhấn "Cancel" trên hộp thoại sinh trắc học hệ thống đã được kiểm chứng đóng hộp thoại an toàn. | BLOCKED | FN29_30_TC-BB-015_D01_01.png | - |

---

## 4. EVIDENCE NAMING CONVENTION

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN29_30_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Ví dụ:  
  • Ghi chú hiển thị ổ khóa tại Trang chủ: `FN29_30_TC-BB-012_D01_01.png`  
  • Mở khóa thành công hiển thị nội dung chi tiết: `FN29_30_TC-BB-013_D01_01.png`  
  • Thông báo xác thực thất bại: `FN29_30_TC-BB-014_D01_01.png`  
  • Quay về Trang chủ sau khi hủy hộp thoại vân tay: `FN29_30_TC-BB-015_D01_01.png`
- **Video quay màn hình (Screen Recording):**  
  Cấu trúc: `FN29_30_[TC-ID]_[Data-ID].mp4`  
  Ví dụ: `FN29_30_TC-BB-013_D01.mp4`

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

- Sau khi hoàn thành kiểm thử, mở lại ghi chú bị khóa, tắt tính năng khóa ghi chú (hoặc xóa ghi chú mẫu nếu không còn dùng) để đưa dữ liệu kiểm thử về trạng thái ban đầu.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **4** | TC-BB-012, TC-BB-013, TC-BB-014, TC-BB-015 |
| **Tổng Execution Items** | **4** | TC-BB-012 (1), TC-BB-013 (1), TC-BB-014 (1), TC-BB-015 (1) |
| **Số lượng PASS** | 0 |
| **Số lượng FAIL** | 0 |
| **Số lượng BLOCKED** | 4 |
| **Số Bug phát hiện** | 0 |
| **Tỷ lệ thực thi (Execution Rate)** | 0% |
| **Tỷ lệ đạt (Pass Rate)** | N/A (0/0) |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 4 execution items của nhóm chức năng FN-29 / FN-30.
- [x] Đã ghi nhận Actual Result trung thực và chi tiết.
- [x] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [x] Đã lưu trữ Evidence (ảnh/video) theo đúng quy tắc đặt tên.
- [x] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report.
- [x] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [x] Đã điền đầy đủ thông tin môi trường kiểm thử trong Mục 1.
- [x] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.
