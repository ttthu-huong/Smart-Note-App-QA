# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-23
## Dự án: Smart Note App
**Chức năng:** Tìm kiếm Ghi chú theo từ khóa văn bản & Bộ lọc đa phương tiện (FN-23)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng Tìm kiếm ghi chú theo tiêu đề, nội dung, bộ lọc đa phương tiện, nhãn dán, trạng thái và độ bền nhập liệu cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-23** |
| **Chức năng** | **Tìm kiếm Ghi chú theo từ khóa văn bản & Bộ lọc** |
| **Người kiểm thử (Tester)** | QA Tester (Manual Execution on Real Device) |
| **Ngày kiểm thử (Execution Date)** | 06/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (Android 14) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | v1.0.0+1 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | Thực thi kiểm thử thủ công trực tiếp trên thiết bị vật lý |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đang ở màn hình Trang chủ (`HomeScreen`) hoặc màn hình Tìm kiếm (`SearchScreen`).
2. **Dữ liệu chuẩn bị trước trên Trang chủ:**
   - Có ghi chú chứa tiêu đề `"Báo cáo tiến độ"`.
   - Có ghi chú chứa cụm từ `"Họp Tuần"`.
   - Có ghi chú tiếng Việt có dấu chứa đoạn `"Nghiên cứu tài liệu kiểm thử"`.
   - Có ghi chú chứa nội dung `"mua thêm giấy in A4"`.
   - Có ghi chú chứa danh sách công việc (Checklist / To-do list).
   - Có ghi chú chứa hình ảnh, ghi chú chứa âm thanh, ghi chú chứa liên kết URL.
   - Có ít nhất 1 ghi chú gắn nhãn dán (ví dụ: nhãn `"Công việc"`).
   - Có ít nhất 1 ghi chú đã ghim và 1 ghi chú đã đưa vào Lưu trữ (`Archive`).
   - Có 1 ghi chú chứa từ khóa `"Tài liệu mật"` nằm trong Thùng rác.

---

## 3. BẢNG THEO DÕI THỰC THI CHI TIẾT (22 EXECUTION ITEMS)

| TC-ID | Exec-ID | Test Input / Thao tác | Các bước thực hiện (Steps) | Kết quả kỳ vọng (Expected Result) | Kết quả thực tế (Actual Result) | Trạng thái (Status) | Evidence (Ảnh chụp) | Defect ID |
|---|---|---|---|---|---|---|---|---|
| **TC-BB-026** | **D01** | Từ khóa: `"Báo cáo"` (khớp Tiêu đề) | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa `"Báo cáo"`. | Danh sách kết quả hiển thị thông báo số lượng khớp và trả về thẻ ghi chú có Tiêu đề chứa từ khóa `"Báo cáo"`. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-026B** | **D01** | Note có `"Nghiên cứu"`, nhập chữ thường có dấu: `"nghiên cứu"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa chữ thường có dấu `"nghiên cứu"`. | Hiển thị chính xác ghi chú có chứa `"Nghiên cứu"`. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-026B** | **D02** | Note có `"Nghiên cứu"`, nhập chữ hoa có dấu: `"NGHIÊN CỨU"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa chữ HOA có dấu `"NGHIÊN CỨU"`. | Xác minh thực tế trên thiết bị kết quả trả về đúng ghi chú `"Nghiên cứu"` (kiểm tra hàm xử lý chữ hoa có dấu trên SQLite Android). | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-026B** | **D03** | Note có `"Nghiên cứu"`, nhập không dấu: `"nghien cuu"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa không dấu `"nghien cuu"`. | Xác minh thực tế trên thiết bị: Quan sát xem ứng dụng có tìm được ghi chú `"Nghiên cứu"` khi nhập `"nghien cuu"` hay không (không mặc định PASS, ghi nhận đúng hành vi thực tế của engine). | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-026C** | **D01** | Từ khóa tiếng Việt có dấu: `"kiểm thử"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa tiếng Việt có dấu `"kiểm thử"`. | Danh sách trả về đúng ghi chú có chứa đoạn văn bản `"kiểm thử"`, không bị lỗi font hay mất kết quả. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-026D** | **D01** | Note chứa `"Kế hoạch"`, tìm kiếm: `"Kế hoạch"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa `"Kế hoạch"`. | Đoạn chữ `"Kế hoạch"` trên thẻ ghi chú kết quả được bôi màu nền nổi bật (highlight vàng nhạt). | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-026E** | **D01** | Đang có từ khóa tìm kiếm $\rightarrow$ Bấm nút 'X' trên search bar | 1. Nhập từ khóa để hiển thị kết quả.<br>2. Chạm vào biểu tượng 'X' ở bên phải thanh tìm kiếm.<br>3. Quan sát màn hình. | Ô tìm kiếm được xóa trống; kết quả tìm kiếm đóng; màn hình trở về trạng thái gợi ý ban đầu. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-027** | **D01** | Từ khóa: `"giấy in A4"` (khớp trong Nội dung) | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa `"giấy in A4"`. | Danh sách kết quả hiển thị thẻ ghi chú có phần nội dung xem trước chứa đoạn văn bản `"giấy in A4"`. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-027B** | **D01** | Bấm chọn mục "Hình ảnh" trong Loại phương tiện | 1. Mở màn hình Tìm kiếm.<br>2. Bấm vào icon "Hình ảnh" trong mục Loại.<br>3. Quan sát thanh tìm kiếm và kết quả. | Viên Chip `[Hình ảnh]` xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú có chứa hình ảnh. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-027B** | **D02** | Bấm chọn mục "Âm thanh" trong Loại phương tiện | 1. Mở màn hình Tìm kiếm.<br>2. Bấm vào icon "Âm thanh" trong mục Loại.<br>3. Quan sát thanh tìm kiếm và kết quả. | Viên Chip `[Âm thanh]` xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú có chứa bản ghi âm. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-027B** | **D03** | Bấm chọn mục "Liên kết" trong Loại phương tiện | 1. Mở màn hình Tìm kiếm.<br>2. Bấm vào icon "Liên kết" trong mục Loại.<br>3. Quan sát thanh tìm kiếm và kết quả. | Viên Chip `[Liên kết]` xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú có chứa đường dẫn URL. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-027C** | **D01** | Bấm chọn nhãn dán trong danh mục Nhãn | 1. Mở màn hình Tìm kiếm.<br>2. Cuộn xuống phần "Nhãn", bấm chọn nhãn dán (ví dụ: `"Công việc"`).<br>3. Quan sát kết quả. | Viên Chip mang tên nhãn xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ lọc ra các ghi chú được gắn đúng nhãn dán đó. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-027D** | **D01** | Bấm chọn mục "Được ghim" trong Trạng thái | 1. Mở màn hình Tìm kiếm.<br>2. Bấm chọn mục "Được ghim" trong phần Trạng thái.<br>3. Quan sát kết quả. | Viên Chip `[Được ghim]` xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú đang được ghim. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-027D** | **D02** | Bấm chọn mục "Lưu trữ" trong Trạng thái | 1. Mở màn hình Tìm kiếm.<br>2. Bấm chọn mục "Lưu trữ" trong phần Trạng thái.<br>3. Quan sát kết quả. | Viên Chip `[Lưu trữ]` xuất hiện trên thanh tìm kiếm; danh sách kết quả lọc ra các ghi chú nằm trong kho lưu trữ. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-027E** | **D01** | Chip `[Hình ảnh]` + gõ từ khóa: `"Thiết kế"` | 1. Bấm chọn mục "Hình ảnh" để tạo Chip lọc.<br>2. Gõ tiếp từ khóa `"Thiết kế"` vào sau Chip.<br>3. Quan sát kết quả. | Danh sách chỉ hiển thị ghi chú vừa có chứa hình ảnh VỪA có tiêu đề/nội dung khớp từ khóa `"Thiết kế"`. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-027F** | **D01** | Đang có Chip lọc $\rightarrow$ Chạm icon 'X' nhỏ bên trong viên Chip | 1. Chọn 1 bộ lọc để viên Chip xuất hiện trên thanh tìm kiếm.<br>2. Chạm vào biểu tượng 'X' nằm bên trong viên Chip đó.<br>3. Quan sát giao diện. | Viên Chip biến mất khỏi thanh tìm kiếm; bộ lọc bị gỡ bỏ và danh sách kết quả cập nhật lại trạng thái không còn áp dụng filter đó. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-027G** | **D01** | Bấm chọn mục "Danh sách" trong Loại phương tiện | 1. Mở màn hình Tìm kiếm.<br>2. Bấm vào icon "Danh sách" trong mục Loại.<br>3. Quan sát thanh tìm kiếm và kết quả. | Xác minh thực tế trên thiết bị: Viên Chip `[Danh sách]` xuất hiện; kiểm tra xem danh sách có lọc đúng ghi chú checklist hay không (xác minh gap giữa UI và service). | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-028** | **D01** | Từ khóa ngẫu nhiên không tồn tại: `"tu_khoa_khong_co_thuc_999"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập chuỗi từ khóa ngẫu nhiên không có thật.<br>3. Quan sát giao diện. | Màn hình hiển thị hình biểu tượng tìm kiếm rỗng, tiêu đề *"Không tìm thấy kết quả"*, phụ đề *"Thử từ khóa khác"* và nút bấm *"Xóa bộ lọc"*. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-028B** | **D01** | Note chứa `"Tài liệu mật"` trong Trash $\rightarrow$ Tìm kiếm: `"Tài liệu mật"` | 1. Đưa ghi chú vào Thùng rác.<br>2. Mở màn hình Tìm kiếm, gõ từ khóa `"Tài liệu mật"`.<br>3. Quan sát kết quả. | Ghi chú nằm trong Thùng rác hoàn toàn không xuất hiện trong kết quả tìm kiếm; màn hình hiển thị trạng thái không tìm thấy kết quả. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-028C** | **D01** | Chạm thẻ ghi chú trong kết quả $\rightarrow$ Sửa nội dung $\rightarrow$ Back | 1. Chạm vào thẻ ghi chú trong danh sách kết quả tìm kiếm.<br>2. Màn hình Editor mở ra; thêm đoạn văn bản mới.<br>3. Bấm nút Back quay lại màn hình Tìm kiếm. | Ghi chú mở ra đúng nội dung; sau khi chỉnh sửa và quay lại, danh sách tìm kiếm cập nhật ngay nội dung mới của ghi chú. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-028D** | **D01** | Bấm icon mũi tên Back trên thanh tìm kiếm | 1. Tại màn hình Tìm kiếm, bấm vào biểu tượng mũi tên Back ở góc trái.<br>2. Quan sát màn hình. | Màn hình Tìm kiếm đóng lại; ứng dụng quay về Trang chủ và hiển thị đầy đủ danh sách ghi chú ban đầu. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-029** | **D01** | Chuỗi ký tự đặc biệt: `"' OR '1'='1 -- % _ @#$ <script>"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập chuỗi ký tự đặc biệt vào ô tìm kiếm.<br>3. Quan sát phản hồi ứng dụng. | Ứng dụng xử lý ổn định, không bị đơ, treo hay crash đột ngột; hiển thị an toàn giao diện không tìm thấy kết quả. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |

---

## 4. TỔNG KẾT METRICS THỰC THI (CHƯA THỰC THI)

| Chỉ số | Số lượng | Tỷ lệ (%) | Ghi chú |
|---|---|---|---|
| **Tổng số Test Cases chính thức** | **17** | — | TC-BB-026 -> TC-BB-029 (Bao gồm TC-BB-027G) |
| **Tổng số Execution Items** | **22** | **100%** | Bao gồm TC-BB-026B (3 items), TC-BB-027B (3 items), TC-BB-027D (2 items), TC-BB-027G (1 item) |
| **Tỷ lệ thực thi (Execution Rate)** | 0 / 22 | 0% | Thiết kế hoàn tất, sẵn sàng thực thi |
| **Số ca kiểm thử ĐẠT (PASS)** | 0 | 0% | Đang chờ Tester trực tiếp kiểm thử |
| **Số ca kiểm thử THẤT BẠI (FAIL)** | 0 | 0% | — |
| **Số ca kiểm thử BỊ CHẶN (BLOCKED)** | 0 | 0% | — |
| **Số ca GẶP LỖI MÔI TRƯỜNG (ERROR)** | 0 | 0% | — |
| **Tổng số lỗi phát hiện (Defects Found)** | 0 | — | Chưa ghi nhận |

---

## 5. BẢNG EVIDENCE MAPPING (CHỜ ĐIỀN)

| Exec-ID | TC-ID | Tên kịch bản | Trạng thái | Đường dẫn hình ảnh minh chứng | Ghi chú minh chứng |
|---|---|---|---|---|---|
| **TC-BB-026-D01** | TC-BB-026 | Tìm kiếm khớp từ khóa trong Tiêu đề ghi chú | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-026B-D01** | TC-BB-026B | Note có "Nghiên cứu", nhập chữ thường có dấu: "nghiên cứu" | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-026B-D02** | TC-BB-026B | Note có "Nghiên cứu", nhập chữ hoa có dấu: "NGHIÊN CỨU" | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-026B-D03** | TC-BB-026B | Note có "Nghiên cứu", nhập không dấu: "nghien cuu" | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-026C-D01** | TC-BB-026C | Tìm kiếm từ khóa tiếng Việt có dấu: "kiểm thử" | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-026D-D01** | TC-BB-026D | Làm nổi bật (Highlight) từ khóa tìm kiếm trên thẻ ghi chú | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-026E-D01** | TC-BB-026E | Xóa nhanh toàn bộ từ khóa tìm kiếm bằng nút X trên search bar | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-027-D01** | TC-BB-027 | Tìm kiếm khớp từ khóa trong Nội dung văn bản ghi chú | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-027B-D01** | TC-BB-027B | Lọc ghi chú có chứa Hình ảnh bằng Chip lọc | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-027B-D02** | TC-BB-027B | Lọc ghi chú có chứa Âm thanh (Voice) bằng Chip lọc | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-027B-D03** | TC-BB-027B | Lọc ghi chú có chứa Liên kết URL bằng Chip lọc | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-027C-D01** | TC-BB-027C | Lọc ghi chú theo Nhãn dán bằng Chip (Tags Filter) | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-027D-D01** | TC-BB-027D | Lọc ghi chú có trạng thái Được ghim bằng Chip lọc | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-027D-D02** | TC-BB-027D | Lọc ghi chú có trạng thái Đã lưu trữ bằng Chip lọc | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-027E-D01** | TC-BB-027E | Tìm kiếm kết hợp đồng thời Bộ lọc Chip và Từ khóa văn bản | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-027F-D01** | TC-BB-027F | Gỡ bỏ từng viên Chip lọc đơn lẻ trên thanh tìm kiếm | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-027G-D01** | TC-BB-027G | Kiểm tra bộ lọc "Danh sách" (has:list) trên UI so với implementation | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-028-D01** | TC-BB-028 | Không tìm thấy kết quả nào (Empty State) | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-028B-D01** | TC-BB-028B | Loại trừ hoàn toàn ghi chú trong Thùng rác khỏi kết quả | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-028C-D01** | TC-BB-028C | Mở và chỉnh sửa ghi chú trực tiếp từ kết quả tìm kiếm | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-028D-D01** | TC-BB-028D | Nút mũi tên Back trên AppBar thoát màn hình tìm kiếm | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-029-D01** | TC-BB-029 | Kiểm tra độ an toàn khi nhập ký tự đặc biệt (Input Robustness) | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |

---

## 6. HƯỚNG DẪN DÀNH CHO TESTER KHI BẮT ĐẦU THỰC THI THỰC TẾ

- [ ] Thực hiện đầy đủ 22 execution items của chức năng FN-23.
- [ ] Đánh giá trạng thái PASS / FAIL / BLOCKED cho cả 22 execution items.
- [ ] Chụp ảnh minh chứng rõ ràng cho từng bước hoặc màn hình kết quả tương ứng.
- [ ] Ghi chú rõ hành vi thực tế quan sát được vào cột `Actual Result`.
