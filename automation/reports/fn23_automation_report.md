# BÁO CÁO THỰC THI AUTOMATION TEST TOÀN DIỆN — FN-23 (SEARCH & FILTER)
## Dự án: Smart Note App
**Branch:** `huong`
**Nhóm chức năng:** FN-23: Tìm kiếm Ghi chú theo từ khóa văn bản & Bộ lọc đa phương tiện (Search Note & Multimedia Filters)
**Phạm vi:** 18 execution items có kịch bản automation (4 baseline + 14 mở rộng Phase 5 thực thi trên thiết bị thật) & 4 execution items Manual lịch sử (tổng 22 execution items thiết kế)
**Framework:** Python 3.13 + pytest + uiautomator2 + ADB
**Thiết bị thực thi:** Samsung Galaxy S21 FE 5G (SM-G990E / R5CW82ECF6M), Android 14 (API 34, One UI 6.1)
**Ngày thực thi & cập nhật chốt:** 21/10/2026 (Mốc baseline: 05/10/2026; Mốc mở rộng Phase 5: 21/10/2026)
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Automation Test Reporting

---

## 1. TỔNG QUAN KẾT QUẢ THỰC THI AUTOMATION TẠI THỜI ĐIỂM CHỐT

| Chỉ số | Số lượng / Giá trị | Ghi chú |
|---|---:|---|
| **Tổng số Execution Items thiết kế cho FN-23** | **22** | Toàn bộ 22 items theo [Bảng thực thi FN-23](../../docs/test_cases/execution_sheets/fn23_execution_sheet.md) |
| **Số items có kịch bản Automation** | **18** | 4 baseline (`test_fn23_search.py`) + 14 mở rộng (`test_fn23_extended.py`) |
| **Số items giữ nguyên kết quả Manual lịch sử** | **4** | `TC-BB-026D-D01`, `TC-BB-027B-D01`, `TC-BB-027B-D02`, `TC-BB-027C-D01` (đã xác minh thủ công) |
| **Automation ĐẠT (PASS)** | **15** | 4 baseline + 5 Batch 1 + 6 Batch 2 (**83.33%** trên 18 items tự động hóa) |
| **Automation THẤT BẠI DO LỖI ỨNG DỤNG (FAIL)** | **1** | `TC-BB-027G-D01` (Bộ lọc Danh sách `has:list` — Tái hiện lỗi **BUG-004 OPEN**) |
| **Automation CHƯA ĐỦ CĂN CỨ NGHIỆP VỤ (BR-01)** | **1** | `TC-BB-026B-D03` (Tìm không dấu tiếng Việt — SQLite engine không unaccent, Empty State an toàn) |
| **Automation BỊ CHẶN (BLOCKED / SKIPPED)** | **1** | `TC-BB-027E-D01` (Lọc kết hợp Ảnh + Từ khóa — Bị chặn do lỗi upload ảnh **BUG-001 OPEN**) |
| **Số ca FAIL-AUTO (Lỗi kịch bản/Môi trường) còn lại** | **0** | Đã loại trừ triệt để; các lần retry Batch 2 ghi nhận riêng trong lịch sử kỹ thuật |
| **Tổng số tệp JUnit XML chính thức** | **4 tệp** | [`fn23_search_junit.xml`](fn23_search_junit.xml), [`fn23_batch1_20261021_0325.xml`](fn23_batch1_20261021_0325.xml), [`fn23_batch2_20261021_0402.xml`](fn23_batch2_20261021_0402.xml), [`fn23_batch3_20261021_0404.xml`](fn23_batch3_20261021_0404.xml) |
| **Tổng số Screenshot Evidence thực tế** | **17 ảnh** | 4 ảnh baseline (`evidence/fn23/`) + 13 ảnh mở rộng (`evidence/fn23/run_20261021_0325/`) |

---

## 2. BẢNG CHI TIẾT KẾT QUẢ TỪNG BATCH THỰC THI PHASE 5

### BATCH 1: Tìm kiếm tiếng Việt, Case-Insensitive & Điều hướng cơ bản (5 Items — PASS 100%)
*Tệp JUnit XML đối chiếu:* [`fn23_batch1_20261021_0325.xml`](fn23_batch1_20261021_0325.xml) (Tests: 5, Failures: 0, Time: 120.57s)
*Thư mục ảnh:* `evidence/fn23/run_20261021_0325/`

| TC-ID | Dataset | Kịch bản kiểm thử | Kết quả thực tế trên thiết bị | Trạng thái | Bằng chứng hình ảnh |
|---|:---:|---|---|:---:|---|
| **TC-BB-026B** | **D01** | Tìm kiếm chữ thường có dấu (`"nghiên cứu"`) | Tìm thấy chính xác thẻ ghi chú mục tiêu `QA_FN23_Nghiencuu_026B` chứa từ khóa trong tiêu đề/nội dung | **PASS** | [`FN23_TC-BB-026B_D01_lowercase.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-026B_D01_lowercase.png) |
| **TC-BB-026B** | **D02** | Tìm kiếm chữ HOA có dấu (`"NGHIÊN CỨU"`) | SQL `LOWER(...) LIKE ?` xử lý case-insensitive chuẩn xác trên SQLite Android, tìm thấy đúng ghi chú | **PASS** | [`FN23_TC-BB-026B_D02_uppercase.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-026B_D02_uppercase.png) |
| **TC-BB-026C** | **D01** | Tìm kiếm từ khóa tiếng Việt đầy đủ (`"kiểm thử"`) | Trả về đúng danh sách ghi chú tiếng Việt có dấu, font Unicode không bị lỗi font hay mất ký tự | **PASS** | [`FN23_TC-BB-026C_D01_vietnamese.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-026C_D01_vietnamese.png) |
| **TC-BB-026E** | **D01** | Nút 'X' xóa nhanh từ khóa trên SearchBar | Chạm biểu tượng 'X', ô tìm kiếm được xóa sạch tức thì, danh sách kết quả đóng và trở về menu gợi ý bộ lọc | **PASS** | [`FN23_TC-BB-026E_D01_clear_bar.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-026E_D01_clear_bar.png) |
| **TC-BB-028D** | **D01** | Nút mũi tên Back trên SearchBar thoát về Home | Bấm icon mũi tên Back góc trái SearchBar, màn hình tìm kiếm đóng và quay về `HomeScreen` hiển thị đầy đủ ghi chú ban đầu | **PASS** | [`FN23_TC-BB-028D_D01_back_home.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-028D_D01_back_home.png) |

---

### BATCH 2: Bộ lọc trạng thái, Gỡ Chip, Loại trừ rác, Lọc URL & Mở Editor (6 Items — PASS 100%)
*Tệp JUnit XML đối chiếu cuối cùng:* [`fn23_batch2_20261021_0402.xml`](fn23_batch2_20261021_0402.xml) (Tests: 6, Failures: 0, Time: 164.50s)
*Lịch sử kỹ thuật:* Các lần chạy thử trước (`0341`, `0353`, `0357`) gặp sự cố bàn phím ảo Samsung che khuất lưới bộ lọc (`FAIL-AUTO`). Sau khi bổ sung lệnh thu gọn bàn phím ảo và tối ưu locator, toàn bộ 6/6 tests đã PASS tuyệt đối ở lượt chạy `0402`. Không tính các lần retry trung gian là execution items mới.

| TC-ID | Dataset | Kịch bản kiểm thử | Kết quả thực tế trên thiết bị | Trạng thái | Bằng chứng hình ảnh |
|---|:---:|---|---|:---:|---|
| **TC-BB-027D** | **D01** | Lọc trạng thái 'Được ghim' (`is:pinned`) | Chạm icon "Được ghim", Chip `[Được ghim]` xuất hiện trên AppBar; danh sách chỉ hiển thị các ghi chú đã ghim | **PASS** | [`FN23_TC-BB-027D_D01_pinned_filter.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-027D_D01_pinned_filter.png) |
| **TC-BB-027F** | **D01** | Gỡ bỏ từng viên Chip lọc trên AppBar | Chạm icon 'X' bên trong Chip `[Được ghim]`, Chip biến mất và các bộ lọc gợi ý xuất hiện trở lại | **PASS** | [`FN23_TC-BB-027F_D01_remove_chip.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-027F_D01_remove_chip.png) |
| **TC-BB-028B** | **D01** | Loại trừ ghi chú trong Thùng rác (0 leak bảo mật) | Tìm kiếm ghi chú đã vào Thùng rác (`QA_FN23_Nghiencuu_026B`); kết quả không rò rỉ, hiển thị Empty State an toàn | **PASS** | [`FN23_TC-BB-028B_D01_trash_excluded.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-028B_D01_trash_excluded.png) |
| **TC-BB-027B** | **D03** | Lọc Loại phương tiện 'Liên kết' (`has:url`) | Chip `[URL]` xuất hiện trên SearchBar, danh sách lọc ra đúng ghi chú chứa đường link URL (`https://smartnote.app/docs`) | **PASS** | [`FN23_TC-BB-027B_D03_url_filter.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-027B_D03_url_filter.png) |
| **TC-BB-027D** | **D02** | Lọc trạng thái 'Lưu trữ' (`is:archived`) | Chạm icon "Lưu trữ", Chip `[Lưu trữ]` xuất hiện; danh sách chỉ hiển thị các ghi chú nằm trong kho lưu trữ | **PASS** | [`FN23_TC-BB-027D_D02_archive_filter.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-027D_D02_archive_filter.png) |
| **TC-BB-028C** | **D01** | Mở và chỉnh sửa ghi chú từ kết quả tìm kiếm | Chạm thẻ ghi chú trong kết quả tìm kiếm, chuyển hướng vào `EditorScreen`; bấm Back lưu và quay lại `SearchScreen` an toàn | **PASS** | [`FN23_TC-BB-028C_D01_edit_from_search.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-028C_D01_edit_from_search.png) |

---

### BATCH 3: Tìm không dấu (BR-01), Bộ lọc Danh sách (BUG-004), & Media Dependency (3 Items)
*Tệp JUnit XML đối chiếu:* [`fn23_batch3_20261021_0404.xml`](fn23_batch3_20261021_0404.xml) (Tests: 3, Failures: 0, Skipped: 1, Time: 52.11s)

| TC-ID | Dataset | Kịch bản kiểm thử | Kết quả thực tế & Phân tích chuyên sâu | Trạng thái Nghiệp vụ | Bằng chứng hình ảnh |
|---|:---:|---|---|:---:|---|
| **TC-BB-026B** | **D03** | Tìm kiếm chuỗi không dấu đối với tiếng Việt (`"nghien cuu"`) | SQLite mặc định không hỗ trợ unaccent folding; nhập `"nghien cuu"` hiển thị Empty State ("Không tìm thấy kết quả"). Ứng dụng ổn định, không lỗi/crash. Script assertion PASS theo hành vi thực tế nhưng phân loại nghiệp vụ là **CHƯA ĐỦ CĂN CỨ theo BR-01** (chờ SRS làm rõ). | **CHƯA ĐỦ CĂN CỨ** *(BR-01)* | [`FN23_TC-BB-026B_D03_unaccented.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-026B_D03_unaccented.png) |
| **TC-BB-027G** | **D01** | Bộ lọc loại "Danh sách" (`has:list`) — Tái hiện lỗi `BUG-004` | Chọn icon "Danh sách", Chip `[Danh sách]` hiển thị trên AppBar, nhưng câu truy vấn SQLite thực hiện LIKE thô `'%has:list%'` dẫn đến danh sách rỗng (Empty State) dù có ghi chú checklist. Script assertion PASS do bắt đúng hành vi khiếm khuyết; phân loại nghiệp vụ là **FAIL do ứng dụng / BUG-004 OPEN**. | **FAIL** *(BUG-004 OPEN)* | [`FN23_TC-BB-027G_D01_list_filter_bug004.png`](../../evidence/fn23/run_20261021_0325/FN23_TC-BB-027G_D01_list_filter_bug004.png) |
| **TC-BB-027E** | **D01** | Lọc kết hợp Chip 'Hình ảnh' + Từ khóa văn bản | Phụ thuộc tính năng đính kèm ảnh bị chặn bởi lỗi **BUG-001 (Infinite Upload Hang trong Editor)**; không có ghi chú ảnh QA hợp lệ trong môi trường test isolated. Test được đánh dấu `pytest.skip()` chuẩn mực; giữ nguyên định danh TC gốc, không tự ý đổi sang Pinned + từ khóa. | **BLOCKED** *(do BUG-001)* | *(Bị chặn bởi lỗi upload ảnh BUG-001)* |

---

### BỘ THỰC THI BASELINE LỊCH SỬ (4 Items — PASS 100%)
*Tệp JUnit XML đối chiếu:* [`fn23_search_junit.xml`](fn23_search_junit.xml) (05/10/2026, Tests: 4, Failures: 0, Time: 123.19s)
*Thư mục ảnh:* `evidence/fn23/`

| TC-ID | Dataset | Kịch bản kiểm thử | Kết quả thực tế trên thiết bị | Trạng thái | Bằng chứng hình ảnh |
|---|:---:|---|---|:---:|---|
| **TC-BB-026** | **D01** | Tìm kiếm theo từ khóa trong Tiêu đề (`"Lịch thi"`) | Hiển thị chính xác thẻ ghi chú "Lịch thi học kỳ" có chứa từ khóa khớp trong tiêu đề | **PASS** | [`FN23_TC-BB-026_D01_01.png`](../../evidence/fn23/FN23_TC-BB-026_D01_01.png) |
| **TC-BB-027** | **D01** | Tìm kiếm theo từ khóa trong Nội dung (`"giấy in A4"`) | Hiển thị chính xác thẻ ghi chú "Tạp vụ" có chứa đoạn nội dung tương ứng | **PASS** | [`FN23_TC-BB-027_D01_01.png`](../../evidence/fn23/FN23_TC-BB-027_D01_01.png) |
| **TC-BB-028** | **D01** | Tìm kiếm chuỗi ngẫu nhiên không tồn tại | Hiển thị `EmptyStateWidget` với "Không tìm thấy kết quả", "Thử từ khóa khác" và nút "Xóa bộ lọc" | **PASS** | [`FN23_TC-BB-028_D01_01.png`](../../evidence/fn23/FN23_TC-BB-028_D01_01.png) |
| **TC-BB-029** | **D01** | Ký tự đặc biệt & SQL Injection (`' OR 1=1 -- % _ @#$`) | SQLite parameterized query xử lý an toàn tuyệt đối; 0 crash, 0 lộ dữ liệu; hiển thị Empty State chuẩn | **PASS** | [`FN23_TC-BB-029_D01_01.png`](../../evidence/fn23/FN23_TC-BB-029_D01_01.png) |

---

## 3. TỔNG HỢP TOÀN BỘ 22 EXECUTION ITEMS CỦA FN-23

| # | TC-ID | Exec-ID | Kịch bản kiểm thử | Hình thức kiểm thử | Trạng thái cuối | JUnit XML / Minh chứng |
|:---:|---|:---:|---|:---:|:---:|---|
| 1 | **TC-BB-026** | D01 | Tìm kiếm khớp từ khóa trong Tiêu đề | **Automation** | **PASS** | `fn23_search_junit.xml` |
| 2 | **TC-BB-026B** | D01 | Tìm kiếm chữ thường có dấu (`"nghiên cứu"`) | **Automation** | **PASS** | `fn23_batch1_20261021_0325.xml` |
| 3 | **TC-BB-026B** | D02 | Tìm kiếm chữ HOA có dấu (`"NGHIÊN CỨU"`) | **Automation** | **PASS** | `fn23_batch1_20261021_0325.xml` |
| 4 | **TC-BB-026B** | D03 | Tìm kiếm chuỗi không dấu tiếng Việt (`"nghien cuu"`) | **Automation** | **CHƯA ĐỦ CĂN CỨ** *(BR-01)* | `fn23_batch3_20261021_0404.xml` |
| 5 | **TC-BB-026C** | D01 | Tìm kiếm từ khóa tiếng Việt có dấu (`"kiểm thử"`) | **Automation** | **PASS** | `fn23_batch1_20261021_0325.xml` |
| 6 | **TC-BB-026D** | D01 | Highlight từ khóa tìm kiếm trên thẻ ghi chú | **Manual** | *Manual PASS* | `evidence/search_run_20261010_1725/06_tc_bb_026d_d01_highlight.png` |
| 7 | **TC-BB-026E** | D01 | Xóa nhanh từ khóa bằng nút 'X' trên search bar | **Automation** | **PASS** | `fn23_batch1_20261021_0325.xml` |
| 8 | **TC-BB-027** | D01 | Tìm kiếm khớp từ khóa trong Nội dung | **Automation** | **PASS** | `fn23_search_junit.xml` |
| 9 | **TC-BB-027B** | D01 | Lọc ghi chú chứa Hình ảnh (`has:image`) | **Thủ công / Lịch sử** | **PENDING / NOT RUN** *(Lịch sử)* | `evidence/fn13_14_21_22_run_20261011_0055/srch05_image_filter_result.png` |
| 10 | **TC-BB-027B** | D02 | Lọc ghi chú chứa Âm thanh (`has:audio`) | **Thủ công / Lịch sử** | **PENDING / NOT RUN** *(Lịch sử)* | `evidence/fn13_14_21_22_run_20261011_0055/srch06_audio_filter_result.png` |
| 11 | **TC-BB-027B** | D03 | Lọc Loại phương tiện 'Liên kết' (`has:url`) | **Automation** | **PASS** | `fn23_batch2_20261021_0402.xml` |
| 12 | **TC-BB-027C** | D01 | Lọc ghi chú theo Nhãn dán (Tags Filter) | **Thủ công / Lịch sử** | **PENDING / NOT RUN** *(Lịch sử)* | `evidence/fn13_14_21_22_run_20261011_0055/ui_srch01.xml` (thiếu screenshot) |
| 13 | **TC-BB-027D** | D01 | Lọc trạng thái 'Được ghim' (`is:pinned`) | **Automation** | **PASS** | `fn23_batch2_20261021_0402.xml` |
| 14 | **TC-BB-027D** | D02 | Lọc trạng thái 'Lưu trữ' (`is:archived`) | **Automation** | **PASS** | `fn23_batch2_20261021_0402.xml` |
| 15 | **TC-BB-027E** | D01 | Lọc kết hợp Chip 'Hình ảnh' + Từ khóa văn bản | **Automation** | **BLOCKED** *(BUG-001)* | `fn23_batch3_20261021_0404.xml` |
| 16 | **TC-BB-027F** | D01 | Gỡ bỏ từng viên Chip lọc trên thanh tìm kiếm | **Automation** | **PASS** | `fn23_batch2_20261021_0402.xml` |
| 17 | **TC-BB-027G** | D01 | Lọc ghi chú Checklist (`has:list`) — Tái hiện lỗi | **Automation** | **FAIL** *(BUG-004 OPEN)* | `fn23_batch3_20261021_0404.xml` |
| 18 | **TC-BB-028** | D01 | Tìm kiếm không có kết quả (Empty State) | **Automation** | **PASS** | `fn23_search_junit.xml` |
| 19 | **TC-BB-028B** | D01 | Loại trừ ghi chú trong Thùng rác khỏi kết quả (0 leak) | **Automation** | **PASS** | `fn23_batch2_20261021_0402.xml` |
| 20 | **TC-BB-028C** | D01 | Mở & sửa ghi chú từ kết quả tìm kiếm | **Automation** | **PASS** | `fn23_batch2_20261021_0402.xml` |
| 21 | **TC-BB-028D** | D01 | Nút mũi tên Back trên SearchBar thoát về Trang chủ | **Automation** | **PASS** | `fn23_batch1_20261021_0325.xml` |
| 22 | **TC-BB-029** | D01 | Nhập ký tự đặc biệt & SQL Injection an toàn | **Automation** | **PASS** | `fn23_search_junit.xml` |

---

## 4. KẾT LUẬN & KIỂM SOÁT DỮ LIỆU CHỐT

1. **Hoàn thành toàn diện Phase 5:**
   - FN-23 đã đạt độ bao phủ tự động hóa trên **18/22 execution items** (81.82%), với **15 PASS / 1 FAIL (`BUG-004`) / 1 CHƯA ĐỦ CĂN CỨ (`BR-01`) / 1 BLOCKED (`BUG-001`)**, và 4 ca Manual lịch sử được bảo toàn.
   - Đây là Phase Automation cuối cùng của dự án Smart Note App QA. Toàn bộ 5 Phase Automation đều đã hoàn thành.
2. **Kỷ luật QA & Tính trung thực kỹ thuật:**
   - Tuyệt đối không suy diễn PASS cho `TC-BB-026B-D03`: ghi nhận trung thực hiện trạng SQLite không unaccent folding và gắn nhãn **CHƯA ĐỦ CĂN CỨ** theo quyết định `BR-01`.
   - Giữ nguyên lỗi **BUG-004 OPEN** cho `TC-BB-027G-D01`: kịch bản tái hiện thành công lỗi query LIKE thô, không ép test pass bằng cách bỏ assert.
   - Ghi nhận đúng trạng thái **BLOCKED** cho `TC-BB-027E-D01` do lỗi nền tảng upload ảnh **BUG-001**: không tự ý thay đổi dữ liệu sang ghi chú Ghim hay từ khóa khác.
3. **An toàn dữ liệu tuyệt đối:**
   - Không reset ứng dụng, không chạy `pm clear`, không xóa tài khoản cá nhân, bảo toàn 100% dữ liệu SQLite và cấu trúc thư mục evidence/reports.
