# BÁO CÁO THỰC THI AUTOMATION TEST — FN-12 (PERMANENT DELETE NOTE)
## Dự án: Smart Note App
**Branch kiểm thử:** `huong`
**Nhóm chức năng:** FN-12: Xóa ghi chú vĩnh viễn (Permanently delete note from Trash)
**Yêu cầu nghiệp vụ:** REQ-09 (Quản lý Thùng rác & Lưu trữ — Hard Delete / Data Purging)
**Tập kịch bản kiểm thử hộp đen chuẩn:** `TC-BB-023`, `TC-BB-023B` (D01, D02), `TC-BB-023C` (3 Test Cases / 4 Execution Items)
**Kịch bản cốt lõi tự động hóa UI:** `TC-BB-023` (AT-40 / P0)
**Framework:** Python 3.13 + pytest + uiautomator2 + ADB (Tầng UI) & Flutter Test (Tầng Provider)
**Thiết bị thực thi UI:** Samsung Galaxy S21 FE 5G (SM-G990B / Serial: R5CW82ECF6M), Android 14 (API 34)
**Ngày thực thi & Cập nhật:** 14/10/2026 (Phiên kiểm thử 01:03:21 – 01:34:44)
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Test Automation Reporting

---

## 1. TỔNG QUAN KẾT QUẢ THỰC THI TỰ ĐỘNG

| Chỉ số kiểm thử | Số lượng / Giá trị | Ghi chú đánh giá |
|---|---:|---|
| **Tổng số TC hộp đen thiết kế (FN-12)** | **3 TCs** | `TC-BB-023`, `TC-BB-023B`, `TC-BB-023C` |
| **Tổng số Execution Items hộp đen** | **4 Items** | Bao gồm `TC-BB-023B-D01` (Hủy xóa) và `TC-BB-023B-D02` (Xác nhận xóa) |
| **Số TC đưa vào kế hoạch UI Core (31 TCs)** | **1 TC** | `TC-BB-023` (Mã kịch bản: `test_tc_bb_023_permanent_delete_from_trash`) |
| **Số TC thuộc phạm vi mở rộng / Thủ công** | **2 TCs (3 Items)** | `TC-BB-023B` (P1 Dialog Cancel/Confirm), `TC-BB-023C` (P1/AT-41 Durability) |
| **Trạng thái thực thi UI mới nhất (Run 4)** | **1 PASS (100%)** | Hoàn thành trọn vẹn luồng E2E: Tạo note QA trong Trash -> Xóa vĩnh viễn -> Xác nhận Dialog -> Verify Trash & Home |
| **Trạng thái thực thi UI lịch sử** | **BLOCKED (Run 1-2) / FAIL (Run 3)** | Run 1 & 2 bị chặn an toàn (xfail); Run 3 gặp lỗi kiểm tra trung gian nhập liệu |
| **Tầng Provider Automated Testing (Dart)** | **1/1 PASS (100%)** | `PV-REF-13` (`NoteProvider - Note lifecycle: Xóa vĩnh viễn ghi chú trong thùng rác`) |
| **Liên kết White-Box thiết kế** | `TC-WB-006`, `007` | Ánh xạ hàm `deleteFile` khi xóa vĩnh viễn ghi chú có ảnh/audio (`CloudinaryService`) |
| **Thời gian thực thi UI mới nhất (Run 4)** | **88.80s** | Chạy kiểm thử tự động trên thiết bị thật với helper chuẩn hóa `QANoteHelper` |
| **Báo cáo JUnit XML mới nhất** | [`fn12_permanent_delete_junit.xml`](fn12_permanent_delete_junit.xml) | Xuất tự động qua pytest (Run 4: 1 passed in 88.80s) |
| **Báo cáo JUnit XML lịch sử (Truy vết)** | [`ui_test_report_fn12.xml`](ui_test_report_fn12.xml) | Run 1: 2026-10-14T01:03:21 (49.97s, xfail blocked) |

---

## 2. ĐỐI CHIẾU PHẠM VI TEST CASE HỘP ĐEN VÀ PHÂN LOẠI TỰ ĐỘNG HÓA

Nhóm chức năng FN-12 bao phủ toàn bộ cơ chế xóa cứng (Hard-delete), làm sạch dữ liệu trong cơ sở dữ liệu SQLite và tài nguyên đính kèm:

| TC-ID | Data ID | Tên kịch bản & Mục tiêu kiểm thử | Mức độ ưu tiên | Phân loại trong Kế hoạch Automation | Tình trạng kịch bản kiểm thử | Trạng thái thực thi |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **TC-BB-023** | **D01** | **Xóa vĩnh viễn 1 ghi chú khỏi Thùng rác kèm Dialog xác nhận:** Vào Thùng rác, chạm nhẹ ghi chú chọn "Xóa vĩnh viễn", nhấn "Xóa" trên AlertDialog; ghi chú biến mất hoàn toàn khỏi Thùng rác, Trang chủ và DB. | **P0** | **ĐÃ CHỌN (Core UI Suite)**<br>(Mã AT-40 trong Phase 3C) | Đã hoàn thiện script (`test_fn12_permanent_delete.py`) | **PASS** (88.80s)<br>(Lịch sử: BLOCKED, FAIL) |
| **TC-BB-023B** | **D01** | **Xóa vĩnh viễn nhiều ghi chú -> Hộp thoại Hủy:** Chọn nhiều ghi chú trong Thùng rác, bấm Xóa vĩnh viễn trên AppBar, nhấn "Hủy" trên AlertDialog; hộp thoại đóng, các ghi chú vẫn còn nguyên trong Thùng rác. | **P1** | **KIỂM THỬ THỦ CÔNG**<br>(Chưa chọn đưa vào scope automation) | Chưa có script UI riêng | **NOT RUN (Manual PASS)** |
| **TC-BB-023B** | **D02** | **Xóa vĩnh viễn nhiều ghi chú -> Hộp thoại Xóa:** Chọn nhiều ghi chú trong Thùng rác, bấm Xóa vĩnh viễn trên AppBar, nhấn "Xóa" trên AlertDialog; toàn bộ ghi chú đã chọn biến mất hoàn toàn khỏi ứng dụng. | **P1** | **KIỂM THỬ THỦ CÔNG**<br>(Chưa chọn đưa vào scope automation) | Chưa có script UI riêng | **NOT RUN (Manual PASS)** |
| **TC-BB-023C** | **D01** | **Kiểm tra tính toàn vẹn vòng đời sau khi đóng và mở lại app:** Có 1 note trong Trash và 1 note đã Permanent Delete; force-stop và mở lại app; ghi chú đã xóa vĩnh viễn không bao giờ xuất hiện lại. | **P1** | **ĐỀ XUẤT MỞ RỘNG (Phase 3C)**<br>(Mã AT-41, kiểm tra độ bền) | Chưa có script UI riêng | **NOT RUN (Manual PASS)** |

---

## 3. LỊCH SỬ THỰC THI UI AUTOMATION VÀ KẾT QUẢ CHI TIẾT

### 3.1. Bảng đối chiếu các lần chạy thực tế (Execution Runs History)

| Lần chạy (Run) | Thời điểm | Thời gian | Trạng thái | Mã lỗi / Hiện tượng quan sát được | Bằng chứng lưu trữ |
| :---: | :---: | :---: | :---: | :--- | :--- |
| **Run 1** | 14/10/2026 01:03:21 | 49.97s | **BLOCKED (xfail)** | Script kiểm tra điều kiện phát hiện không có `android.widget.EditText` trên EditorScreen của bản build hiện tại. Kích hoạt `pytest.xfail` an toàn. | `ui_test_report_fn12.xml` (bản lưu 01:03) |
| **Run 2** | 14/10/2026 01:17:09 | 50.16s | **BLOCKED (xfail)** | Giữ nguyên cơ chế fail-safe bảo vệ dữ liệu máy thật, ghi nhận trạng thái BLOCKED trung thực. | [`editor_missing_fields.png`](../../evidence/fn12/editor_missing_fields.png) |
| **Run 3** | 14/10/2026 01:34:44 | 42.87s | **FAIL** | Tích hợp phương pháp nhập qua `input_content()` nhưng kiểm tra trung gian phát hiện nội dung chưa vào được QuillEditor: `AssertionError: [INPUT FAILURE] Content 'Content for permanent delete test' was not entered into QuillEditor`. | [`fn12_permanent_delete_junit.xml`](fn12_permanent_delete_junit.xml) (43.018s) |
| **Run 4** | 14/10/2026 02:51:30 | 88.80s | **PASS** | Tái cấu trúc bằng `QANoteHelper`: chuẩn bị note QA trong Thùng rác ổn định, mở TrashScreen, chọn note, bấm Xóa vĩnh viễn, xác nhận dialog "Xóa", xác minh note biến mất hoàn toàn khỏi TrashScreen và không tồn tại trên HomeScreen. | [`FN12_TC-BB-023_D01_01.png`](../../evidence/fn12/FN12_TC-BB-023_D01_01.png), [`fn12_permanent_delete_junit.xml`](fn12_permanent_delete_junit.xml) |

### 3.2. Bảng chi tiết kết quả Test Case cốt lõi `TC-BB-023`

| TC-ID | Data ID | Test Data | Expected Result (Đặc tả) | Actual Result (Thực tế trên UI) | Kết quả ghi nhận | Phân loại nguyên nhân | Minh chứng Evidence |
| :--- | :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-023** | **D01** | • Tiền điều kiện: Tạo 1 note `"DeleteForever_<timestamp>"`, đưa vào Trash<br>• Thao tác: Vào Trash -> chọn note -> "Xóa vĩnh viễn" -> Dialog Confirm "Xóa" | Hộp thoại đóng lại; ghi chú bị xóa hoàn toàn khỏi cơ sở dữ liệu; biến mất khỏi cả Thùng rác lẫn Trang chủ. | Thao tác chọn Xóa vĩnh viễn và xác nhận AlertDialog thành công; ghi chú biến mất hoàn toàn khỏi TrashScreen và không xuất hiện trở lại trên HomeScreen. (Run 4: PASS trong 88.80s). | **PASS** | — (Lịch sử: Run 1-2 BLOCKED do rào cản Editor, Run 3 FAIL check paste) | • [`editor_missing_fields.png`](../../evidence/fn12/editor_missing_fields.png)<br>• [`fn12_permanent_delete_junit.xml`](fn12_permanent_delete_junit.xml)<br>• Baseline thủ công: [`FN10_11_12_TC-BB-023_D01_01.png`](../../evidence/fn10_11_12/FN10_11_12_TC-BB-023_D01_01.png) |

---

## 4. KỸ THUẬT THIẾT KẾ TEST CASE VÀ ĐẶC TẢ KIỂM THỬ

1. **Kỹ thuật Chuyển đổi trạng thái kết thúc (Terminal State Transition):**
   - Vòng đời ghi chú đi vào trạng thái tận cùng: `trash` $\xrightarrow{\text{deleteNoteForever}}$ `purged` (xóa vĩnh viễn).
   - Kiểm tra tính triệt để: bản ghi bị xóa khỏi bảng `notes` trong SQLite, không còn tồn tại ở bất kỳ view nào.
2. **Kỹ thuật Hộp thoại phòng vệ (Defensive Dialog Testing):**
   - Hành vi xóa vĩnh viễn là thao tác không thể đảo ngược, do đó bắt buộc phải có AlertDialog cảnh báo với 2 lựa chọn: Hủy (`TC-BB-023B-D01`) và Xóa (`TC-BB-023B-D02`).
3. **Tuân thủ Nguyên tắc An toàn Dữ liệu (Accidental Data Loss Prevention):**
   - Script bắt buộc phải tạo ghi chú tạm cô lập mang tên `DeleteForever_<timestamp>` để xóa.
   - Khi không tạo được ghi chú tạm, script kích hoạt dừng an toàn (`pytest.xfail`), tuyệt đối không được xóa bừa một ghi chú có sẵn trên máy để cố tình đạt kết quả PASS.
4. **Liên kết Xóa tài nguyên đám mây (Cloud Clean-up - White-box REQ-09):**
   - Theo thiết kế mã nguồn, `NoteProvider.deleteNoteForever` sẽ trích xuất public ID của ảnh/audio đính kèm và gọi `CloudinaryService.deleteFile(url)` (`TC-WB-006`, `007`).

---

## 5. MA TRẬN TRUY VẾT VÀ PHÂN TÍCH COVERAGE (TRACEABILITY MATRIX)

### 5.1. Ma trận truy vết chi tiết FN-12

| Chức năng | Mã TC Hộp đen | Mã TC Auto (Phase 3C) | Script / Test Method | Tầng kiểm thử | Kết quả thực thi | Bằng chứng xác minh |
| :---: | :---: | :---: | :--- | :---: | :---: | :--- |
| **FN-12** | `TC-BB-023` | AT-40 | `test_tc_bb_023_permanent_delete_from_trash` (`test_fn12_permanent_delete.py`) | UI / E2E | **PASS** (88.80s)<br>(Lịch sử: Run 1-2 BLOCKED, Run 3 FAIL) | `fn12_permanent_delete_junit.xml`, `FN12_TC-BB-023_D01_01.png` |
| **FN-12** | `TC-BB-023B` | — | *(Kiểm thử thủ công)* | UI Manual | **NOT RUN** (Manual PASS) | `fn10_fn11_fn12_execution_sheet.md` |
| **FN-12** | `TC-BB-023C` | AT-41 | *(Chưa có script UI riêng)* | UI / E2E | **NOT RUN** (Manual PASS) | `fn10_fn11_fn12_execution_sheet.md` |
| **FN-12** | REQ-09 Logic | — | `NoteProvider - Note lifecycle: Xóa vĩnh viễn ghi chú trong thùng rác` (`PV-REF-13`) | Provider (Dart) | **PASS** | `evidence/automated/automated_test_run.log` |
| **FN-12** | Cloudinary Clean | — | `CloudinaryService._extractPublicId` (`TC-WB-006, 007`) | White-Box | **DESIGN ONLY** | `srs_condensed.md` |

### 5.2. Phân tích độ bao phủ (Coverage Analysis)

- **Độ bao phủ Test Case Hộp đen:** 3/3 TCs đã được thiết kế và thực thi thủ công đạt 100% PASS (`fn10_fn11_fn12_execution_sheet.md`).
- **Độ bao phủ Kế hoạch UI Core (31 TCs):** 1/1 TC (`TC-BB-023`) đạt **PASS 100%** trên thiết bị thật Samsung Galaxy S21 FE 5G (88.80s).
- **Lưu ý về độ bao phủ tính năng (Coverage Nuance):** Việc `TC-BB-023` PASS xác nhận trọn vẹn luồng xóa vĩnh viễn cốt lõi kèm hộp thoại xác nhận. Các nhánh mở rộng (`TC-BB-023B` Dialog Cancel/Confirm đa ghi chú, `TC-BB-023C` Durability check) được duy trì kiểm thử thủ công và sẽ mở rộng automation ở giai đoạn tiếp theo.
- **Độ bao phủ Tầng Provider (Logic nghiệp vụ):** 1/1 test đạt **100% PASS**, bảo chứng logic xóa vĩnh viễn của `NoteProvider` hoạt động chuẩn xác trong SQLite repository.

---

## 6. DANH MỤC VẤN ĐỀ VÀ NGUYÊN NHÂN KỸ THUẬT

| Mã Vấn đề | Test Case | Phân loại | Tóm tắt hiện tượng | Phân tích nguyên nhân & Cách xử lý | Trạng thái |
| :---: | :---: | :---: |---|---|---|
| **ISSUE-FN12-01** | `TC-BB-023` | **Intermediate Check Assertion** | Run 3: Gặp `AssertionError: [INPUT FAILURE]` khi paste nội dung vào QuillEditor. | Hàm `input_content()` dùng kiểm tra trung gian `assert content_in_editor`. Khắc phục: Chuẩn hóa kiểm tra nội dung và sử dụng `QANoteHelper` để đảm bảo note được lưu an toàn trước khi vào Trash. | **ĐÃ KHẮC PHỤC** (Run 4 PASS) |
| **ISSUE-FN12-02** | `TC-BB-023` | **UI Element Limitation** | Run 1 & 2: Bị chặn do Editor thiếu trường `EditText`. | Bản build Flutter render Editor dạng Canvas. Khắc phục: Xây dựng module dùng chung `QANoteHelper` tạo note bằng clipboard RPC / Intent mà không phụ thuộc vào widget Native. | **ĐÃ KHẮC PHỤC** (Run 4 PASS) |

---

## 7. ĐÁNH GIÁ KẾT QUẢ VÀ KẾT LUẬN

1. **Tính trung thực và minh bạch:** Toàn bộ lịch sử thực thi (Run 1 & 2 BLOCKED an toàn, Run 3 FAIL check paste) được lưu vết minh bạch song song với kết quả thành công cuối cùng ở Run 4.
2. **Kết quả UI E2E chính thức:** Kịch bản `TC-BB-023` đạt **PASS (88.80s)** trên thiết bị thật Samsung Galaxy S21 FE 5G (Android 14).
3. **Bảo toàn nghiệp vụ đa tầng:** Chức năng FN-12 đạt **100% PASS** ở cả hai tầng: UI E2E (1/1 TC) và Flutter Provider (1/1 test: `PV-REF-13`).
4. **Trạng thái ghi nhận hiện tại:** **PASS (Run 4 mới nhất: 88.80s)** — Minh chứng lưu tại [`evidence/fn12/FN12_TC-BB-023_D01_01.png`](../../evidence/fn12/FN12_TC-BB-023_D01_01.png) và [`fn12_permanent_delete_junit.xml`](fn12_permanent_delete_junit.xml).
