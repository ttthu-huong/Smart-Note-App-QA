# BÁO CÁO CHỐT GIAI ĐOẠN 5 — FN-23: TÌM KIẾM GHI CHÚ & BỘ LỌC ĐA PHƯƠNG TIỆN

**Dự án:** Smart-Note-App-QA
**Nhánh làm việc:** `huong`
**Ngày chốt kết quả:** 21/10/2026 (UTC+7)
**Kỹ thuật:** UI/E2E — pytest + Python 3.13 + uiautomator2 + ADB
**Thiết bị:** Samsung Galaxy S21 FE 5G (SM-G990E, Serial: `R5CW82ECF6M`), Android 14 (API 34, One UI 6.1)
**Phạm vi:** 18 execution items có kịch bản automation (4 baseline + 14 mở rộng Phase 5) & 4 items Manual lịch sử; tổng 22 execution items của FN-23.

---

## 1. Kết quả thực thi cuối cùng

| Chỉ số | Kết quả thực tế | Ghi chú |
|---|---:|---|
| **Tổng số execution items trong phạm vi thiết kế** | **22** | [Bảng thực thi chi tiết FN-23](../test_cases/execution_sheets/fn23_execution_sheet.md) |
| **Execution items có mã nguồn Automation** | **18** | 4 baseline + 14 mở rộng Phase 5 |
| **Execution items ngoài phạm vi Automation (Thủ công / Lịch sử)** | **4** | 1 Manual PASS (`026D-D01`), 3 ca giữ PENDING/NOT RUN theo lịch sử (`027B-D01`, `027B-D02`, `027C-D01` do thiếu căn cứ xác nhận độc lập hoặc thiếu screenshot) |
| **PASS cuối cùng** | **15** | 4 baseline + 5 Batch 1 + 6 Batch 2 (**83.33%** trên tập automation) |
| **FAIL do lỗi ứng dụng (Defect xác nhận)** | **1** | `TC-BB-027G-D01` — Tái hiện lỗi **BUG-004 OPEN** (bộ lọc `has:list` query LIKE thô) |
| **CHƯA ĐỦ CĂN CỨ nghiệp vụ (BR-01)** | **1** | `TC-BB-026B-D03` — Tìm không dấu tiếng Việt (SQLite không unaccent, Empty State) |
| **BLOCKED do lỗi phụ thuộc môi trường** | **1** | `TC-BB-027E-D01` — Bị chặn do lỗi upload ảnh **BUG-001 OPEN** trong Editor |
| **FAIL-AUTO (Lỗi kịch bản/môi trường)** | **0** | Đã xử lý triệt để trong các lượt chỉnh locator và keyboard |

**Quy tắc đếm và chốt số liệu:**
- Kết quả được **tổng hợp độc lập từ các tệp JUnit XML thực tế và cây screenshot tương ứng**, không chạy lại toàn bộ suite và không đếm trùng các lần retry kỹ thuật.
- 4 ca baseline lịch sử (`TC-BB-026`, `027`, `028`, `029`) được bảo toàn từ `fn23_search_junit.xml` (05/10/2026).
- 14 ca mở rộng Phase 5 được thực thi độc lập theo 3 Batch trong `automation/tests/test_fn23_extended.py`.

---

## 2. Bảng đối chiếu 18 Execution Items Automation & Evidence

| # | TC-ID / Data set | Kịch bản kiểm thử | Batch | Kết quả cuối | Tệp JUnit XML đối chiếu | Ảnh Screenshot minh chứng |
|---:|---|---|:---:|:---:|---|---|
| 1 | **TC-BB-026 / D01** | Tìm kiếm theo từ khóa trong Tiêu đề | Baseline | **PASS** | `fn23_search_junit.xml` | `evidence/fn23/FN23_TC-BB-026_D01_01.png` |
| 2 | **TC-BB-027 / D01** | Tìm kiếm theo từ khóa trong Nội dung | Baseline | **PASS** | `fn23_search_junit.xml` | `evidence/fn23/FN23_TC-BB-027_D01_01.png` |
| 3 | **TC-BB-028 / D01** | Tìm kiếm chuỗi ngẫu nhiên không tồn tại | Baseline | **PASS** | `fn23_search_junit.xml` | `evidence/fn23/FN23_TC-BB-028_D01_01.png` |
| 4 | **TC-BB-029 / D01** | Nhập ký tự đặc biệt & SQL Injection an toàn | Baseline | **PASS** | `fn23_search_junit.xml` | `evidence/fn23/FN23_TC-BB-029_D01_01.png` |
| 5 | **TC-BB-026B / D01** | Tìm kiếm chữ thường có dấu (`"nghiên cứu"`) | Batch 1 | **PASS** | `fn23_batch1_20261021_0325.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-026B_D01_lowercase.png` |
| 6 | **TC-BB-026B / D02** | Tìm kiếm chữ HOA có dấu (`"NGHIÊN CỨU"`) | Batch 1 | **PASS** | `fn23_batch1_20261021_0325.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-026B_D02_uppercase.png` |
| 7 | **TC-BB-026C / D01** | Tìm kiếm từ khóa tiếng Việt có dấu (`"kiểm thử"`) | Batch 1 | **PASS** | `fn23_batch1_20261021_0325.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-026C_D01_vietnamese.png` |
| 8 | **TC-BB-026E / D01** | Nút 'X' xóa nhanh từ khóa trên SearchBar | Batch 1 | **PASS** | `fn23_batch1_20261021_0325.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-026E_D01_clear_bar.png` |
| 9 | **TC-BB-028D / D01** | Nút mũi tên Back trên SearchBar thoát về Home | Batch 1 | **PASS** | `fn23_batch1_20261021_0325.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-028D_D01_back_home.png` |
| 10 | **TC-BB-027D / D01** | Lọc trạng thái 'Được ghim' (`is:pinned`) | Batch 2 | **PASS** | `fn23_batch2_20261021_0402.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-027D_D01_pinned_filter.png` |
| 11 | **TC-BB-027F / D01** | Gỡ bỏ từng viên Chip lọc trên AppBar | Batch 2 | **PASS** | `fn23_batch2_20261021_0402.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-027F_D01_remove_chip.png` |
| 12 | **TC-BB-028B / D01** | Loại trừ ghi chú trong Thùng rác (0 leak bảo mật) | Batch 2 | **PASS** | `fn23_batch2_20261021_0402.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-028B_D01_trash_excluded.png` |
| 13 | **TC-BB-027B / D03** | Lọc Loại phương tiện 'Liên kết' (`has:url`) | Batch 2 | **PASS** | `fn23_batch2_20261021_0402.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-027B_D03_url_filter.png` |
| 14 | **TC-BB-027D / D02** | Lọc trạng thái 'Lưu trữ' (`is:archived`) | Batch 2 | **PASS** | `fn23_batch2_20261021_0402.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-027D_D02_archive_filter.png` |
| 15 | **TC-BB-028C / D01** | Mở & chỉnh sửa ghi chú từ kết quả tìm kiếm | Batch 2 | **PASS** | `fn23_batch2_20261021_0402.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-028C_D01_edit_from_search.png` |
| 16 | **TC-BB-026B / D03** | Tìm kiếm chuỗi không dấu đối với tiếng Việt | Batch 3 | **CHƯA ĐỦ CĂN CỨ** *(BR-01)* | `fn23_batch3_20261021_0404.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-026B_D03_unaccented.png` |
| 17 | **TC-BB-027G / D01** | Bộ lọc loại "Danh sách" (`has:list`) — Tái hiện lỗi | Batch 3 | **FAIL** *(BUG-004 OPEN)* | `fn23_batch3_20261021_0404.xml` | `evidence/fn23/run_20261021_0325/FN23_TC-BB-027G_D01_list_filter_bug004.png` |
| 18 | **TC-BB-027E / D01** | Lọc kết hợp Chip 'Hình ảnh' + Từ khóa văn bản | Batch 3 | **BLOCKED** *(BUG-001)* | `fn23_batch3_20261021_0404.xml` | *(Bị chặn do lỗi upload ảnh BUG-001 trong Editor)* |

---

## 3. Phân tích nguyên nhân và xử lý sự cố trong từng Batch

### 3.1. Batch 1: Thực thi thành công 5/5 ngay ở lượt đầu
- Không gặp bất kỳ sự cố nào về locator hay môi trường.
- Kịch bản xác thực chính xác tính toàn vẹn của Unicode tiếng Việt và tính năng case-insensitive của SQLite (`LOWER(title) LIKE ?`).

### 3.2. Batch 2: Xử lý sự cố tương tác bàn phím ảo (Samsung Honeyboard)
- **Hiện tượng tại các lượt chạy sơ bộ (`0341`, `0353`, `0357`):** Khi mở `SearchScreen`, ô `EditText` tự động focus khiến bàn phím ảo Samsung đẩy lên, che khuất lưới icon bộ lọc ("Được ghim", "Gỡ Chip", "URL"). Do đó locator tìm icon báo lỗi (`FAIL-AUTO`).
- **Khắc phục kỹ thuật:** Script bổ sung kiểm tra gói bàn phím `com.samsung.android.honeyboard`, nhấn `back` thu gọn bàn phím trước khi định vị các nút lọc.
- **Kết quả chốt (`0402`):** Toàn bộ 6/6 tests chạy mượt mà, đạt 100% PASS. Lịch sử retry được ghi nhận rõ ràng, không tính là lỗi ứng dụng.

### 3.3. Batch 3: Kỷ luật QA trong phân loại kết quả
- **TC-BB-026B-D03:** Test assertion pass vì app trả về Empty State an toàn, không crash. Tuy nhiên, theo quyết định `BR-01`, do SRS chưa quy định rõ tính năng unaccent folding, kết quả được bảo toàn ở trạng thái **CHƯA ĐỦ CĂN CỨ**, tuyệt đối không tự nâng thành PASS.
- **TC-BB-027G-D01:** Test kịch bản pass vì bắt đúng lỗi; kết quả ứng dụng được phân loại đúng nghĩa là **FAIL do lỗi BUG-004 OPEN** (query LIKE thô không bóc tách token).
- **TC-BB-027E-D01:** Do phụ thuộc vào tính năng đính kèm ảnh đang bị lỗi **BUG-001**, test được bỏ qua có chủ đích qua `pytest.skip()` và ghi nhận trạng thái **BLOCKED**, không đổi sang fixture Pinned.

---

## 4. An toàn dữ liệu kiểm thử & Môi trường

- Tất cả các kịch bản thực thi trên tài khoản QA đã xác minh (`student_qa@gmail.com`).
- Các ghi chú phục vụ kiểm thử được cô lập với tiền tố `QA_FN23_*` và `QA_PIN_*`.
- Tuyệt đối không reset app, không thực hiện `pm clear`, không xóa tài khoản, bảo toàn 100% dữ liệu SQLite và cấu trúc thư mục trên máy thật.

---

## 5. Kết luận

**Chức năng FN-23 đã chính thức khép lại Phase 5 — Phase cuối cùng của kế hoạch kiểm thử tự động hóa dự án Smart Note App.** Toàn bộ 5 Phase đã hoàn thành với đầy đủ bằng chứng JUnit XML, ảnh screenshot thực tế và sự đồng bộ tuyệt đối trên toàn bộ tài liệu QA dự án.
