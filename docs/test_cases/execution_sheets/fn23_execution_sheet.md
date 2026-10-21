# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-23
## Dự án: Smart Note App
**Chức năng:** Tìm kiếm Ghi chú theo từ khóa văn bản & Bộ lọc đa phương tiện (FN-23)
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution
**Tài liệu tham chiếu:** [`black_box_test_cases.md`](../black_box/black_box_test_cases.md)
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng Tìm kiếm ghi chú theo tiêu đề, nội dung, bộ lọc đa phương tiện, nhãn dán, trạng thái và độ bền nhập liệu cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-23** |
| **Chức năng** | **Tìm kiếm Ghi chú theo từ khóa văn bản & Bộ lọc** |
| **Người kiểm thử (Tester)** | QA Tester (Executed on Real Device via UI) |
| **Ngày kiểm thử (Execution Date)** | 10/10/2026 (Run 2: Search Suite Scope) |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990E, Serial: `R5CW82ECF6M`) |
| **Android Version** | Android 14 (API 34, One UI 6.1) |
| **App Version / Build Number** | v1.0.0+1 |
| **Kết nối mạng** | Wi-Fi (Offline Local SQLite Execution) |
| **Ghi chú môi trường khác** | Dữ liệu thử nghiệm tạo qua UI, bảo toàn 100% dữ liệu SQLite gốc; bằng chứng lưu tại `evidence/search_run_20261010_1725/` |

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
| **TC-BB-026** | **D01** | Từ khóa: `"Báo cáo"` (khớp Tiêu đề) | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa `"Báo cáo"`. | Danh sách kết quả hiển thị thông báo số lượng khớp và trả về thẻ ghi chú có Tiêu đề chứa từ khóa `"Báo cáo"`. | Hiển thị đúng 2 ghi chú khớp Tiêu đề (`Báo cáo tiến độ` và `Danh sách công việc... Báo cáo kết quả`), kèm thông báo `"TÌM THẤY 2 GHI CHÚ KHỚP"`. | **PASS** | `evidence/search_run_20261010_1725/01_tc_bb_026_d01_title_search.png` | [Không] |
| **TC-BB-026B** | **D01** | Note có `"Nghiên cứu"`, nhập chữ thường có dấu: `"nghiên cứu"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa chữ thường có dấu `"nghiên cứu"`. | Hiển thị chính xác ghi chú có chứa `"Nghiên cứu"`. | Hiển thị đúng ghi chú có Tiêu đề/Nội dung chứa `"Nghiên cứu tài liệu kiểm thử phần mềm"`, kèm `"TÌM THẤY 1 GHI CHÚ KHỚP"`. | **PASS** | `evidence/search_run_20261010_1725/02_tc_bb_026b_d01_lowercase.png` | [Không] |
| **TC-BB-026B** | **D02** | Note có `"Nghiên cứu"`, nhập chữ hoa có dấu: `"NGHIÊN CỨU"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa chữ HOA có dấu `"NGHIÊN CỨU"`. | Xác minh thực tế trên thiết bị kết quả trả về đúng ghi chú `"Nghiên cứu"` (kiểm tra hàm xử lý chữ hoa có dấu trên SQLite Android). | Hiển thị đúng ghi chú chứa `"Nghiên cứu"`, cơ chế tìm kiếm SQLite `LOWER(...) LIKE ?` xử lý case-insensitive chính xác. | **PASS** | `evidence/search_run_20261010_1725/03_tc_bb_026b_d02_uppercase.png` | [Không] |
| **TC-BB-026B** | **D03** | Note có `"Nghiên cứu"`, nhập không dấu: `"nghien cuu"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa không dấu `"nghien cuu"`. | Xác minh thực tế trên thiết bị: Quan sát xem ứng dụng có tìm được ghi chú `"Nghiên cứu"` khi nhập `"nghien cuu"` hay không (không mặc định PASS, ghi nhận đúng hành vi thực tế của engine). | Nhập không dấu `"nghien cuu"` hiển thị Empty State (*"Không tìm thấy kết quả"*). Xác nhận engine SQLite mặc định không hỗ trợ unaccented folding; ứng dụng xử lý ổn định, không lỗi/crash. Chưa có tiêu chí yêu cầu rõ ràng về bắt buộc tìm không dấu $\rightarrow$ Chưa đủ căn cứ kết luận PASS/FAIL. | **CHƯA ĐỦ CĂN CỨ** | `evidence/search_run_20261010_1725/04_tc_bb_026b_d03_unaccented.png` | [Cần làm rõ SRS] |
| **TC-BB-026C** | **D01** | Từ khóa tiếng Việt có dấu: `"kiểm thử"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa tiếng Việt có dấu `"kiểm thử"`. | Danh sách trả về đúng ghi chú có chứa đoạn văn bản `"kiểm thử"`, không bị lỗi font hay mất kết quả. | Danh sách hiển thị đúng 5 ghi chú chứa từ khóa `"kiểm thử"`, font Unicode tiếng Việt hiển thị toàn vẹn. | **PASS** | `evidence/search_run_20261010_1725/05_tc_bb_026c_d01_vietnamese.png` | [Không] |
| **TC-BB-026D** | **D01** | Note chứa `"Kế hoạch"`, tìm kiếm: `"Kế hoạch"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa `"Kế hoạch"`. | Đoạn chữ `"Kế hoạch"` trên thẻ ghi chú kết quả được bôi màu nền nổi bật (highlight vàng nhạt). | Tìm thấy ghi chú `"Họp Tuần"` chứa cụm từ `"kế hoạch"`. Từ khóa khớp được highlight trực quan trên thẻ ghi chú. | **PASS** | `evidence/search_run_20261010_1725/06_tc_bb_026d_d01_highlight.png` | [Không] |
| **TC-BB-026E** | **D01** | Đang có từ khóa tìm kiếm $\rightarrow$ Bấm nút 'X' trên search bar | 1. Nhập từ khóa để hiển thị kết quả.<br>2. Chạm vào biểu tượng 'X' ở bên phải thanh tìm kiếm.<br>3. Quan sát màn hình. | Ô tìm kiếm được xóa trống; kết quả tìm kiếm đóng; màn hình trở về trạng thái gợi ý ban đầu. | Chạm biểu tượng 'X' bên phải thanh tìm kiếm, ô nhập liệu được xóa sạch ngay lập tức; kết quả đóng và màn hình trở về menu gợi ý ban đầu. | **PASS** | `evidence/search_run_20261010_1725/07_tc_bb_026e_d01_clear_bar.png` | [Không] |
| **TC-BB-027** | **D01** | Từ khóa: `"giấy in A4"` (khớp trong Nội dung) | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa `"giấy in A4"`. | Danh sách kết quả hiển thị thẻ ghi chú có phần nội dung xem trước chứa đoạn văn bản `"giấy in A4"`. | Danh sách trả về thẻ ghi chú `"Văn phòng phẩm"` có nội dung xem trước chứa cụm `"mua thêm giấy in A4"`. | **PASS** | `evidence/search_run_20261010_1725/08_tc_bb_027_d01_content_search.png` | [Không] |
| **TC-BB-027B** | **D01** | Bấm chọn mục "Hình ảnh" trong Loại phương tiện | 1. Mở màn hình Tìm kiếm.<br>2. Bấm vào icon "Hình ảnh" trong mục Loại.<br>3. Quan sát thanh tìm kiếm và kết quả. | Viên Chip `[Hình ảnh]` xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú có chứa hình ảnh. | Bấm chọn "Hình ảnh", Chip `[Hình ảnh]` xuất hiện trên thanh search, danh sách lọc ra chính xác 9 ghi chú có ảnh, loại trừ 100% note thuần văn bản. | **PASS** | `evidence/fn13_14_21_22_run_20261011_0055/srch05_image_filter_result.png` | [Không] |
| **TC-BB-027B** | **D02** | Bấm chọn mục "Âm thanh" trong Loại phương tiện | 1. Mở màn hình Tìm kiếm.<br>2. Bấm vào icon "Âm thanh" trong mục Loại.<br>3. Quan sát thanh tìm kiếm và kết quả. | Viên Chip `[Âm thanh]` xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú có chứa bản ghi âm. | Bấm chọn "Âm thanh", Chip `[Âm thanh]` xuất hiện trên thanh search, danh sách trả về đúng 3 ghi chú có audio, loại trừ note thuần chữ và note ảnh. | **PASS** | `evidence/fn13_14_21_22_run_20261011_0055/srch06_audio_filter_result.png` | [Không] |
| **TC-BB-027B** | **D03** | Bấm chọn mục "Liên kết" trong Loại phương tiện | 1. Mở màn hình Tìm kiếm.<br>2. Bấm vào icon "Liên kết" trong mục Loại.<br>3. Quan sát thanh tìm kiếm và kết quả. | Viên Chip `[Liên kết]` xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú có chứa đường dẫn URL. | Bấm chọn icon "URL" (Liên kết), Chip `[URL (x)]` xuất hiện trên thanh search, kết quả trả về đúng ghi chú có liên kết URL (`https://smartnote.app/docs`). | **PASS** | `evidence/search_run_20261010_1725/09_tc_bb_027b_d03_url_filter.png` | [Không] |
| **TC-BB-027C** | **D01** | Bấm chọn nhãn dán trong danh mục Nhãn | 1. Mở màn hình Tìm kiếm.<br>2. Cuộn xuống phần "Nhãn", bấm chọn nhãn dán (ví dụ: `"DU_AN_TEST"`).<br>3. Quan sát kết quả. | Viên Chip mang tên nhãn xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ lọc ra các ghi chú được gắn đúng nhãn dán đó. | Bấm chọn nhãn `"DU_AN_TEST"`, Chip `[DU_AN_TEST]` xuất hiện trên thanh search, danh sách lọc ra chính xác các ghi chú có nhãn này. | **PASS** | `evidence/fn13_14_21_22_run_20261011_0055/ui_srch01.xml` | [Không] |
| **TC-BB-027D** | **D01** | Bấm chọn mục "Được ghim" trong Trạng thái | 1. Mở màn hình Tìm kiếm.<br>2. Bấm chọn mục "Được ghim" trong phần Trạng thái.<br>3. Quan sát kết quả. | Viên Chip `[Được ghim]` xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú đang được ghim. | Bấm chọn "Được ghim", Chip `[Được ghim (x)]` xuất hiện trên search bar, danh sách chỉ hiển thị ghi chú đã ghim (`Ghi_chu_bao_mat_FN29_B`). | **PASS** | `evidence/search_run_20261010_1725/11_tc_bb_027d_d01_pinned_filter.png` | [Không] |
| **TC-BB-027D** | **D02** | Bấm chọn mục "Lưu trữ" trong Trạng thái | 1. Mở màn hình Tìm kiếm.<br>2. Bấm chọn mục "Lưu trữ" trong phần Trạng thái.<br>3. Quan sát kết quả. | Viên Chip `[Lưu trữ]` xuất hiện trên thanh tìm kiếm; danh sách kết quả lọc ra các ghi chú nằm trong kho lưu trữ. | Bấm chọn "Lưu trữ", Chip `[Lưu trữ (x)]` xuất hiện trên search bar, danh sách hiển thị đúng ghi chú đã lưu trữ. | **PASS** | `evidence/search_run_20261010_1725/12_tc_bb_027d_d02_archive_filter.png` | [Không] |
| **TC-BB-027E** | **D01** | Chip `[Nhãn/Hình ảnh]` + gõ từ khóa: `"NOTE"` | 1. Bấm chọn Chip lọc (ví dụ Nhãn/Hình ảnh).<br>2. Gõ tiếp từ khóa vào sau Chip.<br>3. Quan sát kết quả. | Danh sách chỉ hiển thị ghi chú vừa thỏa mãn Chip lọc VỪA khớp từ khóa văn bản. | Gắn Chip `[DU_AN_TEST]` và gõ từ khóa `"NOTE"`, danh sách lọc ra chính xác 1 ghi chú thỏa mãn cả 2 điều kiện. | **PASS** | `evidence/fn13_14_21_22_run_20261011_0055/ui_srch03.xml` | [Không] |
| **TC-BB-027F** | **D01** | Đang có Chip lọc $\rightarrow$ Chạm icon 'X' nhỏ bên trong viên Chip | 1. Chọn 1 bộ lọc để viên Chip xuất hiện trên thanh tìm kiếm.<br>2. Chạm vào biểu tượng 'X' nằm bên trong viên Chip đó.<br>3. Quan sát giao diện. | Viên Chip biến mất khỏi thanh tìm kiếm; bộ lọc bị gỡ bỏ và danh sách kết quả cập nhật lại trạng thái không còn áp dụng filter đó. | Chạm biểu tượng 'X' bên trong viên Chip lọc, Chip biến mất ngay khỏi thanh search; bộ lọc được hủy và giao diện hiển thị lại các bộ lọc gợi ý. | **PASS** | `evidence/search_run_20261010_1725/10_tc_bb_027f_d01_remove_chip.png` | [Không] |
| **TC-BB-027G** | **D01** | Bấm chọn mục "Danh sách" trong Loại phương tiện (`has:list`) | 1. Mở màn hình Tìm kiếm.<br>2. Bấm vào icon "Danh sách" trong mục Loại.<br>3. Quan sát thanh tìm kiếm và kết quả. | Danh sách kết quả lọc đúng các ghi chú checklist danh sách công việc. | Bấm chọn "Danh sách", Chip `[Danh sách]` hiển thị nhưng query LIKE thô không bóc tách token, kết quả trả về sai/rỗng. Ghi nhận lỗi `BUG-004`. | **FAIL** | `evidence/search_run_20261010_1725/srch02_list_filter.png` | **BUG-004** |
| **TC-BB-028** | **D01** | Từ khóa ngẫu nhiên không tồn tại: `"tu_khoa_khong_co_thuc_999"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập chuỗi từ khóa ngẫu nhiên không có thật.<br>3. Quan sát giao diện. | Màn hình hiển thị hình biểu tượng tìm kiếm rỗng, tiêu đề *"Không tìm thấy kết quả"*, phụ đề *"Thử từ khóa khác"* và nút bấm *"Xóa bộ lọc"*. | Màn hình hiển thị đầy đủ icon rỗng, tiêu đề *"Không tìm thấy kết quả"*, phụ đề *"Thử từ khóa khác"* và nút bấm *"Xóa bộ lọc"*. | **PASS** | `evidence/search_run_20261010_1725/13_tc_bb_028_d01_empty_state.png` | [Không] |
| **TC-BB-028B** | **D01** | Note chứa `"Tài liệu mật"` trong Trash $\rightarrow$ Tìm kiếm: `"Tài liệu mật"` | 1. Đưa ghi chú vào Thùng rác.<br>2. Mở màn hình Tìm kiếm, gõ từ khóa `"Tài liệu mật"`.<br>3. Quan sát kết quả. | Ghi chú nằm trong Thùng rác hoàn toàn không xuất hiện trong kết quả tìm kiếm; màn hình hiển thị trạng thái không tìm thấy kết quả. | Ghi chú trong Thùng rác bị loại trừ hoàn toàn khỏi kết quả tìm kiếm (0 leak bảo mật); màn hình hiển thị an toàn giao diện Empty State. | **PASS** | `evidence/search_run_20261010_1725/14_tc_bb_028b_d01_trash_excluded.png` | [Không] |
| **TC-BB-028C** | **D01** | Chạm thẻ ghi chú trong kết quả $\rightarrow$ Sửa nội dung $\rightarrow$ Back | 1. Chạm vào thẻ ghi chú trong danh sách kết quả tìm kiếm.<br>2. Màn hình Editor mở ra; thêm đoạn văn bản mới.<br>3. Bấm nút Back quay lại màn hình Tìm kiếm. | Ghi chú mở ra đúng nội dung; sau khi chỉnh sửa và quay lại, danh sách tìm kiếm cập nhật ngay nội dung mới của ghi chú. | Ghi chú mở đúng trong Editor; sau khi thêm ký tự và bấm Back, màn hình tìm kiếm cập nhật ngay nội dung mới của thẻ ghi chú. | **PASS** | `evidence/search_run_20261010_1725/15_tc_bb_028c_d01_edit_from_search.png` | [Không] |
| **TC-BB-028D** | **D01** | Bấm icon mũi tên Back trên thanh tìm kiếm | 1. Tại màn hình Tìm kiếm, bấm vào biểu tượng mũi tên Back ở góc trái.<br>2. Quan sát màn hình. | Màn hình Tìm kiếm đóng lại; ứng dụng quay về Trang chủ và hiển thị đầy đủ danh sách ghi chú ban đầu. | Bấm icon mũi tên Back bên trái thanh tìm kiếm, SearchScreen đóng và quay về Trang chủ (`HomeScreen`) hiển thị đầy đủ danh sách ghi chú. | **PASS** | `evidence/search_run_20261010_1725/16_tc_bb_028d_d01_back_to_home.png` | [Không] |
| **TC-BB-029** | **D01** | Chuỗi ký tự đặc biệt: `"' OR '1'='1 -- % _ @#$ <script>"` | 1. Mở màn hình Tìm kiếm.<br>2. Nhập chuỗi ký tự đặc biệt vào ô tìm kiếm.<br>3. Quan sát phản hồi ứng dụng. | Ứng dụng xử lý ổn định, không bị đơ, treo hay crash đột ngột; hiển thị an toàn giao diện không tìm thấy kết quả. | Ứng dụng xử lý an toàn, không crash, không đơ/lag, không phát sinh lỗi SQL injection trong phạm vi chuỗi kiểm thử, hiển thị chuẩn xác Empty State. | **PASS** | `evidence/search_run_20261010_1725/17_tc_bb_029_d01_sql_injection.png` | [Không] |

---

## 4. TỔNG KẾT METRICS THỰC THI (TỔNG HỢP 22 ITEMS)

| Chỉ số | Số lượng | Tỷ lệ (%) | Ghi chú |
|---|---|---|---|
| **Tổng số Execution Items thiết kế** | **22** | **100%** | Toàn bộ 22 items của FN-23 |
| **Số items đã thực thi (Executed)** | **22** | **100%** | Đã thực thi trọn vẹn 22 items trên thiết bị thực tế |
| **Số ca kiểm thử ĐẠT (PASS)** | **20** | **90.91%** | 20/22 items đạt kết quả mong đợi |
| **Số ca THẤT BẠI (FAIL)** | **1** | **4.55%** | TC-BB-027G-D01 (`has:list` trả về sai do query LIKE thô `BUG-004`) |
| **Số ca CHƯA ĐỦ CĂN CỨ (Inconclusive)** | **1** | **4.55%** | TC-BB-026B-D03 (Tìm không dấu: SQLite không unaccent, chờ làm rõ SRS) |
| **Số ca kiểm thử BỊ CHẶN (BLOCKED)** | **0** | **0%** | Không bị chặn môi trường |
| **Tổng số lỗi chức năng phát hiện** | **1** | — | BUG-004 (`has:list` query thô) |

---

## 5. BẢNG EVIDENCE MAPPING (22 ITEMS HOÀN TẤT)

| Exec-ID | TC-ID | Tên kịch bản | Trạng thái | Đường dẫn hình ảnh minh chứng | Ghi chú minh chứng |
|---|---|---|---|---|---|
| **TC-BB-026-D01** | TC-BB-026 | Tìm kiếm khớp từ khóa trong Tiêu đề ghi chú | **PASS** | `evidence/search_run_20261010_1725/01_tc_bb_026_d01_title_search.png` | Tìm thấy 2 ghi chú có tiêu đề chứa "Báo cáo" |
| **TC-BB-026B-D01** | TC-BB-026B | Note có "Nghiên cứu", nhập chữ thường: "nghiên cứu" | **PASS** | `evidence/search_run_20261010_1725/02_tc_bb_026b_d01_lowercase.png` | Khớp chữ thường có dấu |
| **TC-BB-026B-D02** | TC-BB-026B | Note có "Nghiên cứu", nhập chữ hoa: "NGHIÊN CỨU" | **PASS** | `evidence/search_run_20261010_1725/03_tc_bb_026b_d02_uppercase.png` | Khớp chữ hoa có dấu (case-insensitive) |
| **TC-BB-026B-D03** | TC-BB-026B | Note có "Nghiên cứu", nhập không dấu: "nghien cuu" | **CHƯA ĐỦ CĂN CỨ** | `evidence/search_run_20261010_1725/04_tc_bb_026b_d03_unaccented.png` | Empty State (SQLite chuẩn không unaccent folding; chờ làm rõ SRS) |
| **TC-BB-026C-D01** | TC-BB-026C | Tìm kiếm từ khóa tiếng Việt có dấu: "kiểm thử" | **PASS** | `evidence/search_run_20261010_1725/05_tc_bb_026c_d01_vietnamese.png` | Khớp 5 ghi chú, Unicode hiển thị toàn vẹn |
| **TC-BB-026D-D01** | TC-BB-026D | Làm nổi bật (Highlight) từ khóa tìm kiếm trên thẻ ghi chú | **PASS** | `evidence/search_run_20261010_1725/06_tc_bb_026d_d01_highlight.png` | Highlight vàng từ khóa "kế hoạch" |
| **TC-BB-026E-D01** | TC-BB-026E | Xóa nhanh toàn bộ từ khóa bằng nút 'X' trên search bar | **PASS** | `evidence/search_run_20261010_1725/07_tc_bb_026e_d01_clear_bar.png` | Ô search xóa trống, quay về menu bộ lọc |
| **TC-BB-027-D01** | TC-BB-027 | Tìm kiếm khớp từ khóa trong Nội dung văn bản ghi chú | **PASS** | `evidence/search_run_20261010_1725/08_tc_bb_027_d01_content_search.png` | Tìm thấy ghi chú chứa "giấy in A4" trong nội dung |
| **TC-BB-027B-D01** | TC-BB-027B | Lọc ghi chú có chứa Hình ảnh bằng Chip lọc | **PASS** | `evidence/fn13_14_21_22_run_20261011_0055/srch05_image_filter_result.png` | Chip `[Hình ảnh]`, trả về đúng 9 note có ảnh |
| **TC-BB-027B-D02** | TC-BB-027B | Lọc ghi chú có chứa Âm thanh (Voice) bằng Chip lọc | **PASS** | `evidence/fn13_14_21_22_run_20261011_0055/srch06_audio_filter_result.png` | Chip `[Âm thanh]`, trả về đúng 3 note có audio |
| **TC-BB-027B-D03** | TC-BB-027B | Lọc ghi chú có chứa Liên kết URL bằng Chip lọc | **PASS** | `evidence/search_run_20261010_1725/09_tc_bb_027b_d03_url_filter.png` | Chip `[URL]` hiển thị, lọc đúng note chứa link |
| **TC-BB-027C-D01** | TC-BB-027C | Lọc ghi chú theo Nhãn dán bằng Chip (Tags Filter) | **PASS** | `evidence/fn13_14_21_22_run_20261011_0055/ui_srch01.xml` | Chip `[DU_AN_TEST]`, lọc đúng note gắn nhãn |
| **TC-BB-027D-D01** | TC-BB-027D | Lọc ghi chú có trạng thái Được ghim bằng Chip lọc | **PASS** | `evidence/search_run_20261010_1725/11_tc_bb_027d_d01_pinned_filter.png` | Chip `[Được ghim]`, chỉ hiển thị note ghim |
| **TC-BB-027D-D02** | TC-BB-027D | Lọc ghi chú có trạng thái Đã lưu trữ bằng Chip lọc | **PASS** | `evidence/search_run_20261010_1725/12_tc_bb_027d_d02_archive_filter.png` | Chip `[Lưu trữ]`, hiển thị note archived |
| **TC-BB-027E-D01** | TC-BB-027E | Tìm kiếm kết hợp đồng thời Bộ lọc Chip và Từ khóa | **PASS** | `evidence/fn13_14_21_22_run_20261011_0055/ui_srch03.xml` | Chip `[DU_AN_TEST]` + từ khóa "NOTE", trả về 1 note |
| **TC-BB-027F-D01** | TC-BB-027F | Gỡ bỏ từng viên Chip lọc đơn lẻ trên thanh tìm kiếm | **PASS** | `evidence/search_run_20261010_1725/10_tc_bb_027f_d01_remove_chip.png` | Táp 'X' trong Chip, gỡ bỏ Chip và về menu |
| **TC-BB-027G-D01** | TC-BB-027G | Kiểm tra bộ lọc "Danh sách" (`has:list`) trên UI | **FAIL** | `evidence/search_run_20261010_1725/srch02_list_filter.png` | Ghi nhận lỗi `BUG-004` (query LIKE thô không bóc tách token) |
| **TC-BB-028-D01** | TC-BB-028 | Không tìm thấy kết quả nào (Empty State) | **PASS** | `evidence/search_run_20261010_1725/13_tc_bb_028_d01_empty_state.png` | Empty State đầy đủ icon, title, subtitle |
| **TC-BB-028B-D01** | TC-BB-028B | Loại trừ hoàn toàn ghi chú trong Thùng rác khỏi kết quả | **PASS** | `evidence/search_run_20261010_1725/14_tc_bb_028b_d01_trash_excluded.png` | 0 leak: note trong trash không xuất hiện trong kết quả |
| **TC-BB-028C-D01** | TC-BB-028C | Mở và chỉnh sửa ghi chú trực tiếp từ kết quả tìm kiếm | **PASS** | `evidence/search_run_20261010_1725/15_tc_bb_028c_d01_edit_from_search.png` | Mở note, sửa và quay lại, cập nhật ngay |
| **TC-BB-028D-D01** | TC-BB-028D | Nút mũi tên Back trên AppBar thoát màn hình tìm kiếm | **PASS** | `evidence/search_run_20261010_1725/16_tc_bb_028d_d01_back_to_home.png` | Thoát SearchScreen quay về HomeScreen |
| **TC-BB-029-D01** | TC-BB-029 | Kiểm tra độ an toàn khi nhập ký tự đặc biệt | **PASS** | `evidence/search_run_20261010_1725/17_tc_bb_029_d01_sql_injection.png` | An toàn trong phạm vi chuỗi thử nghiệm đã chạy, 0 crash, 0 SQL injection |

---

## 6. KẾT LUẬN & ĐỐI CHIẾU
- Toàn bộ 22/22 items thiết kế đã được thực thi và xác minh trên thiết bị thực tế.
- 20 items PASS, 1 item FAIL (`TC-BB-027G-D01` do `BUG-004`), 1 item Chưa đủ căn cứ (`TC-BB-026B-D03`).
- 0 items BLOCKED, 0 items Pending.
