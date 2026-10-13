# RUN LOG — BLACK-BOX TEST EXECUTION RUN 2: SEARCH SUITE
**Thời điểm thực thi:** 10/10/2026 17:25 - 17:50 (GMT+7)  
**Phạm vi:** FN-23 (Tìm kiếm văn bản), FN-25 (Bộ lọc `has:url`), FN-27 (Bộ lọc `is:pinned` và `is:archived`)  
**Tài liệu tham chiếu:** [`test_cases/execution_sheets/fn23_execution_sheet.md`](../../test_cases/execution_sheets/fn23_execution_sheet.md)  
**Thiết bị thực tế:** Samsung Galaxy S21 FE 5G (`SM-G990E`, Serial: `R5CW82ECF6M`)  
**Hệ điều hành:** Android 14 (API 34, One UI 6.1)  
**Bản build:** `com.example.smart_note_app` (v1.0.0+1)  
**Môi trường mạng:** Offline / Local SQLite (bảo toàn ghi chú hiện có)  

---

## 1. DỮ LIỆU THỬ NGHIỆM ĐƯỢC CHUẨN BỊ (QUA UI)
- Tạo mới qua giao diện người dùng (UI) nhằm đảm bảo toàn vẹn dữ liệu SQLite và không ảnh hưởng đồng bộ:
  1. Ghi chú đã ghim (`status = 'pinned'`): `Ghi_chu_bao_mat_FN29_B`
  2. Ghi chú lưu trữ (`status = 'archived'`): `Ghi chú lưu trữ` (chứa `Lưu trữ tài liệu dự án năm ngoái`)
  3. Ghi chú trong thùng rác (`status = 'trash'`): `FN23_Tai_lieu_mat_Trash`
  4. Ghi chú chứa URL (`note.content` có link hợp lệ): `FN23_URL_Official` (`https://smartnote.app/docs`)
  5. Các ghi chú văn bản tiêu đề / nội dung phục vụ tìm kiếm: `Báo cáo tiến độ`, `Nghiên cứu tài liệu kiểm thử phần mềm`, `Họp Tuần` (chứa `kế hoạch kiểm thử`), `Văn phòng phẩm` (chứa `mua thêm giấy in A4`).

---

## 2. KẾT QUẢ THỰC THI CHI TIẾT THEO ITEM (17 ITEMS IN-SCOPE)

| STT | Exec-ID | TC-ID | Thao tác / Dữ liệu | Kỳ vọng (Expected Result) | Thực tế (Actual Result) | Đánh giá | File minh chứng |
|:---:|---|---|---|---|---|:---:|---|
| 01 | **TC-BB-026-D01** | TC-BB-026 | Từ khóa: `"Báo cáo"` (Tiêu đề) | Trả về các note có tiêu đề chứa "Báo cáo" | Hiển thị 2 ghi chú khớp Tiêu đề (`Báo cáo tiến độ`, `Danh sách công việc... Báo cáo kết quả`), kèm thông báo `"TÌM THẤY 2 GHI CHÚ KHỚP"` | **PASS** | `01_tc_bb_026_d01_title_search.png` |
| 02 | **TC-BB-026B-D01** | TC-BB-026B | Từ khóa thường: `"nghiên cứu"` | Khớp chính xác ghi chú có chứa "Nghiên cứu" | Trả về đúng ghi chú `"Nghiên cứu tài liệu kiểm thử phần mềm"`, `"TÌM THẤY 1 GHI CHÚ KHỚP"` | **PASS** | `02_tc_bb_026b_d01_lowercase.png` |
| 03 | **TC-BB-026B-D02** | TC-BB-026B | Từ khóa hoa: `"NGHIÊN CỨU"` | Khớp chính xác (case-insensitive) | Trả về đúng ghi chú `"Nghiên cứu"`, SQLite `LOWER(?)` xử lý chính xác | **PASS** | `03_tc_bb_026b_d02_uppercase.png` |
| 04 | **TC-BB-026B-D03** | TC-BB-026B | Từ khóa không dấu: `"nghien cuu"` | Xác minh thực tế engine SQLite | Trả về Empty State (*"Không tìm thấy kết quả"*). Xác nhận SQLite Android không hỗ trợ bỏ dấu tiếng Việt mặc định; ứng dụng xử lý an toàn, không treo. Chưa có tiêu chí yêu cầu rõ ràng về bắt buộc tìm không dấu $\rightarrow$ Chưa đủ căn cứ kết luận PASS/FAIL | **CHƯA ĐỦ CĂN CỨ** | `04_tc_bb_026b_d03_unaccented.png` |
| 05 | **TC-BB-026C-D01** | TC-BB-026C | Từ khóa tiếng Việt: `"kiểm thử"` | Hiển thị đúng, không lỗi font Unicode | Trả về 5 ghi chú chứa từ khóa `"kiểm thử"`, font Unicode toàn vẹn | **PASS** | `05_tc_bb_026c_d01_vietnamese.png` |
| 06 | **TC-BB-026D-D01** | TC-BB-026D | Highlight từ khóa `"Kế hoạch"` | Từ khóa được bôi màu nổi bật | Tìm thấy ghi chú `"Họp Tuần"`, từ khóa `"kế hoạch"` được highlight màu nổi bật | **PASS** | `06_tc_bb_026d_d01_highlight.png` |
| 07 | **TC-BB-026E-D01** | TC-BB-026E | Bấm nút 'X' trên search bar | Xóa ô tìm kiếm, trở về menu gợi ý | Ô tìm kiếm xóa trống, kết quả đóng, trở về danh mục bộ lọc gợi ý ban đầu | **PASS** | `07_tc_bb_026e_d01_clear_bar.png` |
| 08 | **TC-BB-027-D01** | TC-BB-027 | Từ khóa `"giấy in A4"` (Nội dung) | Trả về note có preview nội dung khớp | Trả về thẻ ghi chú `"Văn phòng phẩm"` có nội dung preview chứa `"mua thêm giấy in A4"` | **PASS** | `08_tc_bb_027_d01_content_search.png` |
| 09 | **TC-BB-027B-D03** | TC-BB-027B | Bộ lọc "URL" (Liên kết) | Chip `[URL]` xuất hiện, chỉ hiện note có URL | Xuất hiện Chip `[URL (x)]` trên thanh tìm kiếm, danh sách trả về ghi chú chứa link `https://smartnote.app/docs` | **PASS** | `09_tc_bb_027b_d03_url_filter.png` |
| 10 | **TC-BB-027F-D01** | TC-BB-027F | Gỡ Chip lọc bằng icon 'X' | Chip biến mất, bộ lọc bị hủy | Chạm icon 'X' trong viên Chip, Chip biến mất ngay khỏi search bar, giao diện trở về menu gợi ý ban đầu | **PASS** | `10_tc_bb_027f_d01_remove_chip.png` |
| 11 | **TC-BB-027D-D01** | TC-BB-027D | Bộ lọc "Được ghim" | Chip `[Được ghim]`, chỉ hiện note ghim | Xuất hiện Chip `[Được ghim (x)]`, danh sách lọc ra đúng ghi chú đã ghim `Ghi_chu_bao_mat_FN29_B` | **PASS** | `11_tc_bb_027d_d01_pinned_filter.png` |
| 12 | **TC-BB-027D-D02** | TC-BB-027D | Bộ lọc "Lưu trữ" | Chip `[Lưu trữ]`, hiển thị note archived | Xuất hiện Chip `[Lưu trữ (x)]`, danh sách trả về đúng ghi chú đã đưa vào lưu trữ | **PASS** | `12_tc_bb_027d_d02_archive_filter.png` |
| 13 | **TC-BB-028-D01** | TC-BB-028 | Từ khóa không tồn tại: `tu_khoa_...` | Hiển thị giao diện Empty State | Hiển thị đầy đủ icon tìm kiếm rỗng, *"Không tìm thấy kết quả"*, *"Thử từ khóa khác"*, nút *"Xóa bộ lọc"* | **PASS** | `13_tc_bb_028_d01_empty_state.png` |
| 14 | **TC-BB-028B-D01** | TC-BB-028B | Tìm từ khóa trong Trash: `FN23_Tai_lieu_...` | Ghi chú Trash không xuất hiện (0 leak) | Ghi chú trong thùng rác bị loại trừ hoàn toàn trong kịch bản đã chạy, hiển thị an toàn màn hình Empty State (0 rò rỉ dữ liệu) | **PASS** | `14_tc_bb_028b_d01_trash_excluded.png` |
| 15 | **TC-BB-028C-D01** | TC-BB-028C | Mở note từ search $\rightarrow$ Sửa $\rightarrow$ Back | Cập nhật ngay kết quả trên search screen | Mở ghi chú trong Editor, sửa tiêu đề, bấm Back, kết quả tìm kiếm cập nhật ngay lập tức nội dung mới | **PASS** | `15_tc_bb_028c_d01_edit_from_search.png` |
| 16 | **TC-BB-028D-D01** | TC-BB-028D | Bấm mũi tên Back trên search bar | Thoát SearchScreen về HomeScreen | SearchScreen đóng lại, ứng dụng quay về Trang chủ (`HomeScreen`) hiển thị đầy đủ danh sách ghi chú ban đầu | **PASS** | `16_tc_bb_028d_d01_back_to_home.png` |
| 17 | **TC-BB-029-D01** | TC-BB-029 | SQL Injection: `"' OR '1'='1 -- % _ @#$ <script>"` | Ứng dụng ổn định, không lỗi/crash | Ứng dụng xử lý ổn định, không crash, không lỗi cú pháp SQL trong phạm vi chuỗi kiểm thử đã chạy, hiển thị an toàn Empty State | **PASS** | `17_tc_bb_029_d01_sql_injection.png` |

---

## 3. CÁC ITEMS BẢO LƯU NGOÀI PHẠM VI (5 ITEMS)
Các items sau chưa chạy theo đúng yêu cầu phạm vi của lượt này (chưa chạy `has:image`, `has:audio`, Tag, `has:list`):
- `TC-BB-027B-D01`: Lọc hình ảnh (`has:image`)
- `TC-BB-027B-D02`: Lọc âm thanh (`has:audio`)
- `TC-BB-027C-D01`: Lọc nhãn dán (Tag)
- `TC-BB-027E-D01`: Kết hợp Chip hình ảnh + từ khóa text
- `TC-BB-027G-D01`: Lọc danh sách (`has:list`)

---

## 4. TỔNG KẾT METRICS
- **Tổng số Execution Items thiết kế (FN-23):** 22 items
- **Số items thuộc phạm vi lượt này:** 17 items
- **Số items ngoài phạm vi (bảo lưu):** 5 items
- **Kết quả thực thi phạm vi:**
  - **PASS:** 16 / 17 (94.1%)
  - **CHƯA ĐỦ CĂN CỨ KẾT LUẬN:** 1 / 17 (5.9%) — `TC-BB-026B-D03` (chờ làm rõ SRS về tìm không dấu)
  - **FAIL:** 0
  - **BLOCKED:** 0
- **Giới hạn kết luận an toàn:** Giới hạn chặt chẽ trong các tình huống thực tế và chuỗi ký tự đã chạy (0 crash, 0 rò rỉ dữ liệu thùng rác, 0 lỗi cú pháp SQL, 0 mất mát dữ liệu SQLite).

---

## 5. GHI CHÚ VỀ CÁC THAO TÁC RUNNER
- Các bước hiệu chỉnh trong quá trình chạy tự động hóa hoàn toàn chỉ nằm trong script runner Python/UIAutomator2 (điều chỉnh tọa độ nhấp chuột ảo theo bounding box của bàn phím và icon X bên trong viên Chip lọc).
- Tuyệt đối không can thiệp, không sửa đổi bất kỳ dòng mã nguồn nào của ứng dụng Flutter (`lib/`).
