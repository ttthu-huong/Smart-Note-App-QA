# BÁO CÁO THỰC THI AUTOMATION TEST — FN-11 (RESTORE NOTE FROM TRASH)
## Dự án: Smart Note App
**Branch kiểm thử:** `huong`
**Nhóm chức năng:** FN-11: Khôi phục ghi chú từ thùng rác (Restore note from Trash)
**Yêu cầu nghiệp vụ:** REQ-09 (Quản lý Thùng rác & Lưu trữ — State Restoration)
**Tập kịch bản kiểm thử hộp đen chuẩn:** `TC-BB-022`, `TC-BB-022B`, `TC-BB-022C` (3 Test Cases / 3 Execution Items)
**Kịch bản cốt lõi tự động hóa UI:** `TC-BB-022` (AT-38 / P0)
**Framework:** Python 3.13 + pytest + uiautomator2 + ADB (Tầng UI) & Flutter Test (Tầng Provider)
**Thiết bị thực thi UI:** Samsung Galaxy S21 FE 5G (SM-G990B / Serial: R5CW82ECF6M), Android 14 (API 34)
**Ngày thực thi & Cập nhật:** 14/10/2026 (Phiên kiểm thử 01:00:27 – 01:34:11)
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Test Automation Reporting

---

## 1. TỔNG QUAN KẾT QUẢ THỰC THI TỰ ĐỘNG

| Chỉ số kiểm thử | Số lượng / Giá trị | Ghi chú đánh giá |
|---|---:|---|
| **Tổng số TC hộp đen thiết kế (FN-11)** | **3 TCs** | `TC-BB-022`, `TC-BB-022B`, `TC-BB-022C` |
| **Tổng số Execution Items hộp đen** | **3 Items** | Thực thi thủ công đạt 3/3 PASS (`fn10_fn11_fn12_execution_sheet.md`) |
| **Số TC đưa vào kế hoạch UI Core (31 TCs)** | **1 TC** | `TC-BB-022` (Mã kịch bản: `test_tc_bb_022_restore_note_from_trash`) |
| **Số TC thuộc phạm vi mở rộng / Thủ công** | **2 TCs** | `TC-BB-022B` (P1 Multi-select), `TC-BB-022C` (P1/AT-39 Empty State) |
| **Trạng thái thực thi UI mới nhất (Run 5)** | **1 PASS (100%)** | 1 TC duy nhất PASS (ghi nhận 2 lượt chạy lặp do truyền trùng đường dẫn pytest) |
| **Trạng thái thực thi UI lịch sử** | **BLOCKED / FAIL / ERROR** | Run 1: FAIL; Run 2-3: BLOCKED (xfail); Run 4: ERROR (IndentationError) |
| **Tầng Provider Automated Testing (Dart)** | **3/3 PASS (100%)** | `PV-REF-05` (Restore note), `PV-REF-12` (Restore lifecycle), `PV-REF-15` (Restore pinned note) |
| **Thời gian thực thi UI mới nhất (Run 5)** | **184.13s** | Tổng thời gian 2 lượt chạy lặp (90.72s + 93.38s); tính là 1 TC duy nhất |
| **Báo cáo JUnit XML mới nhất** | [`fn11_restore_junit.xml`](fn11_restore_junit.xml) | Xuất tự động qua pytest (Run 5: 2 tests passed in 184.10s) |
| **Báo cáo JUnit XML lịch sử (Truy vết)** | [`ui_test_report_fn11.xml`](ui_test_report_fn11.xml) | Run 1 (01:00:27, 49.94s) & Run 2/3 (01:17:04, 50.21s, xfail blocked) |

---

## 2. ĐỐI CHIẾU PHẠM VI TEST CASE HỘP ĐEN VÀ PHÂN LOẠI TỰ ĐỘNG HÓA

Nhóm chức năng FN-11 bao phủ toàn bộ cơ chế phục hồi ghi chú từ vùng lưu trữ tạm (Trash) về trạng thái hoạt động bình thường:

| TC-ID | Data ID | Tên kịch bản & Mục tiêu kiểm thử | Mức độ ưu tiên | Phân loại trong Kế hoạch Automation | Tình trạng kịch bản kiểm thử | Trạng thái thực thi |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **TC-BB-022** | **D01** | **Khôi phục 1 ghi chú từ Thùng rác về Trang chủ:** Vào Thùng rác qua Drawer, chạm nhẹ vào ghi chú chọn "Khôi phục ghi chú"; ghi chú biến mất khỏi Thùng rác, có SnackBar thông báo và xuất hiện lại trên HomeScreen. | **P0** | **ĐÃ CHỌN (Core UI Suite)**<br>(Mã AT-38 trong Phase 3C) | Đã viết script (`test_fn11_restore.py`) | **PASS** (184.13s / 1 TC duy nhất)<br>(Lịch sử: BLOCKED, ERROR) |
| **TC-BB-022B** | **D01** | **Khôi phục nhiều ghi chú đồng thời (Multi-select Restore):** Vào Thùng rác, nhấn giữ chọn nhiều ghi chú, nhấn icon Khôi phục trên AppBar; toàn bộ ghi chú đã chọn quay về Trang chủ đầy đủ. | **P1** | **KIỂM THỬ THỦ CÔNG**<br>(Chưa chọn đưa vào scope automation) | Chưa có script UI riêng | **NOT RUN (Manual PASS)** |
| **TC-BB-022C** | **D01** | **Kiểm tra trạng thái rỗng khi Thùng rác trống (Empty State):** Mở Thùng rác khi không có ghi chú nào; hiển thị hình minh họa và thông báo *"Thùng rác trống"*. | **P1** | **ĐỀ XUẤT MỞ RỘNG (Phase 3C)**<br>(Mã AT-39, khuyến nghị triển khai sau) | Chưa có script UI riêng | **NOT RUN (Manual PASS)** |

---

## 3. LỊCH SỬ THỰC THI UI AUTOMATION VÀ KẾT QUẢ CHI TIẾT

### 3.1. Bảng đối chiếu các lần chạy thực tế (Execution Runs History)

| Lần chạy (Run) | Thời điểm | Thời gian | Trạng thái | Mã lỗi / Hiện tượng quan sát được | Bằng chứng lưu trữ |
| :---: | :---: | :---: | :---: | :--- | :--- |
| **Run 1** | 14/10/2026 01:00:27 | 49.94s | **FAIL** | Script cũ gọi `open_note_editor()` gặp `AssertionError: Failed to open EditorScreen after tapping FAB`. | `ui_test_report_fn11.xml` (bản lưu 01:00) |
| **Run 2** | 14/10/2026 01:09:24 | 51.72s | **BLOCKED (xfail)** | Bổ sung fallback mở Editor, nhưng bị chặn ở bước nhập liệu do không tìm thấy `android.widget.EditText`. Kích hoạt `pytest.xfail` an toàn. | `ui_test_report_fn11_updated.xml` |
| **Run 3** | 14/10/2026 01:17:04 | 50.21s | **BLOCKED (xfail)** | Duy trì cơ chế bảo vệ xfail; xác nhận giao diện QuillEditor không tương thích với bộ tìm kiếm `EditText`. | [`editor_missing_fields.png`](../../evidence/fn11/editor_missing_fields.png) |
| **Run 4** | 14/10/2026 01:34:11 | 0.38s | **ERROR** | Lỗi cú pháp trong file kịch bản: `IndentationError: expected an indented block after function definition on line 47` tại `automation/tests/test_fn11_restore.py`. Pytest dừng tại collection phase. | [`fn11_restore_junit.xml`](fn11_restore_junit.xml) (0.375s) |
| **Run 5** | 14/10/2026 02:48:22 | 184.13s | **PASS** | Đã sửa lỗi IndentationError và sử dụng `QANoteHelper`: tạo note QA, đưa vào Thùng rác, vào TrashScreen nhấn Khôi phục, ghi chú biến mất khỏi Trash và xuất hiện lại trên HomeScreen (chạy lặp 2 lượt: 90.72s + 93.38s, tính 1 TC duy nhất). | [`FN11_TC-BB-022_D01_01.png`](../../evidence/fn11/FN11_TC-BB-022_D01_01.png), [`fn11_restore_junit.xml`](fn11_restore_junit.xml) |

### 3.2. Bảng chi tiết kết quả Test Case cốt lõi `TC-BB-022`

| TC-ID | Data ID | Test Data | Expected Result (Đặc tả) | Actual Result (Thực tế trên UI) | Kết quả ghi nhận | Phân loại nguyên nhân | Minh chứng Evidence |
| :--- | :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-022** | **D01** | • Tiền điều kiện: Có 1 note trong Thùng rác<br>• Thao tác: Mở Thùng rác -> chọn note -> "Khôi phục ghi chú" | Ghi chú biến mất khỏi Thùng rác; xuất hiện SnackBar thông báo: *"Đã khôi phục ghi chú"*; quay về HomeScreen thấy ghi chú xuất hiện trở lại với đầy đủ dữ liệu. | Ghi chú trong Thùng rác được khôi phục thành công; biến mất khỏi TrashScreen và xuất hiện trở lại đầy đủ trên HomeScreen. (Run 5: PASS trong 184.13s across 2 runs lặp = 1 TC duy nhất). | **PASS** | — (Lịch sử: Run 1 FAIL, Run 2-3 BLOCKED, Run 4 ERROR) | • [`editor_missing_fields.png`](../../evidence/fn11/editor_missing_fields.png)<br>• [`fn11_restore_junit.xml`](fn11_restore_junit.xml)<br>• Baseline thủ công: [`FN10_11_12_TC-BB-022_D01_01.png`](../../evidence/fn10_11_12/FN10_11_12_TC-BB-022_D01_01.png) |

---

## 4. KỸ THUẬT THIẾT KẾ TEST CASE VÀ ĐẶC TẢ KIỂM THỬ

1. **Kỹ thuật Chuyển đổi trạng thái đảo nghịch (Inverse State Transition):**
   - Kiểm tra nhánh phục hồi: `trash` $\xrightarrow{\text{restoreNote}}$ `normal`.
   - Xác minh ghi chú được tái sinh vào danh sách hoạt động mà không bị sai lệch dữ liệu tiêu đề, nội dung hoặc timestamp.
2. **Kỹ thuật Bảo toàn Trạng thái Ghim (State Preservation Testing):**
   - Đối với ghi chú đã ghim trước khi bị xóa (`PV-REF-15`), sau khi khôi phục từ thùng rác, hệ thống phải bảo toàn cờ ghim và tự động đưa ghi chú về phân vùng "Được ghim" trên HomeScreen.
3. **Kỹ thuật Kiểm thử Trạng thái Rỗng (Empty State Testing):**
   - `TC-BB-022C` kiểm tra giao diện rỗng khi Thùng rác không có dữ liệu, bảo đảm tính thân thiện UX.
4. **Nguyên tắc Độc lập Dữ liệu (Test Isolation):**
   - Để kiểm thử khôi phục, script phải tự tạo dữ liệu tạm rồi chuyển vào thùng rác trước khi thực hiện bước khôi phục, không sử dụng dữ liệu rác có sẵn của người dùng.

---

## 5. MA TRẬN TRUY VẾT VÀ PHÂN TÍCH COVERAGE (TRACEABILITY MATRIX)

### 5.1. Ma trận truy vết chi tiết FN-11

| Chức năng | Mã TC Hộp đen | Mã TC Auto (Phase 3C) | Script / Test Method | Tầng kiểm thử | Kết quả thực thi | Bằng chứng xác minh |
| :---: | :---: | :---: | :--- | :---: | :--- | :--- |
| **FN-11** | `TC-BB-022` | AT-38 | `test_tc_bb_022_restore_note_from_trash` (`test_fn11_restore.py`) | UI / E2E | **PASS** (184.13s / 1 TC duy nhất)<br>(Lịch sử: BLOCKED, ERROR) | `fn11_restore_junit.xml`, `FN11_TC-BB-022_D01_01.png` |
| **FN-11** | `TC-BB-022B` | — | *(Kiểm thử thủ công)* | UI Manual | **NOT RUN** (Manual PASS) | `fn10_fn11_fn12_execution_sheet.md` |
| **FN-11** | `TC-BB-022C` | AT-39 | *(Chưa có script UI riêng)* | UI / E2E | **NOT RUN** (Manual PASS) | `fn10_fn11_fn12_execution_sheet.md` |
| **FN-11** | REQ-09 Logic | — | `NoteProvider - Restore note: Khôi phục ghi chú từ thùng rác` (`PV-REF-05`) | Provider (Dart) | **PASS** | `evidence/automated/automated_test_run.log` |
| **FN-11** | REQ-09 Logic | — | `NoteProvider - Note lifecycle: Khôi phục ghi chú từ thùng rác` (`PV-REF-12`) | Provider (Dart) | **PASS** | `evidence/automated/automated_test_run.log` |
| **FN-11** | REQ-09 Logic | — | `NoteProvider - Note lifecycle: Khôi phục ghi chú đã ghim từ thùng rác` (`PV-REF-15`) | Provider (Dart) | **PASS** | `evidence/automated/automated_test_run.log` |

### 5.2. Phân tích độ bao phủ (Coverage Analysis)

- **Độ bao phủ Test Case Hộp đen:** 3/3 TCs đã được thiết kế và thực thi thủ công đạt 100% PASS (`fn10_fn11_fn12_execution_sheet.md`).
- **Độ bao phủ Kế hoạch UI Core (31 TCs):** 1/1 TC (`TC-BB-022`) đạt **PASS 100%** trên thiết bị thật Samsung Galaxy S21 FE 5G (184.13s across 2 runs lặp = 1 TC duy nhất).
- **Lưu ý về độ bao phủ tính năng (Coverage Nuance):** Việc `TC-BB-022` PASS xác nhận trọn vẹn luồng phục hồi chính từ Thùng rác về Trang chủ. Các nhánh mở rộng (`TC-BB-022B` Multi-select restore, `TC-BB-022C` Empty State) được duy trì kiểm thử thủ công và sẽ mở rộng automation ở giai đoạn tiếp theo.
- **Độ bao phủ Tầng Provider (Logic nghiệp vụ):** 3/3 tests đạt **100% PASS**, bảo chứng toàn diện logic `restoreNote()` cho cả ghi chú thường lẫn ghi chú đã ghim.

---

## 6. DANH MỤC VẤN ĐỀ VÀ NGUYÊN NHÂN KỸ THUẬT

| Mã Vấn đề | Test Case | Phân loại | Tóm tắt hiện tượng | Phân tích nguyên nhân & Cách xử lý | Trạng thái |
| :---: | :---: | :---: |---|---|---|
| **ISSUE-FN11-01** | `TC-BB-022` | **Script Syntax Defect** | Run 4: Gặp `IndentationError` tại dòng 47 file script. | Khối lệnh docstring/thân hàm bị thụt lề sai khiến Python không parse được cú pháp. Khắc phục: Chuẩn hóa thụt đầu dòng PEP 8 và tái cấu trúc gọi `QANoteHelper`. | **ĐÃ KHẮC PHỤC** (Run 5 PASS) |
| **ISSUE-FN11-02** | `TC-BB-022` | **UI Element Limitation** | Run 2 & 3: Bị chặn bước tạo dữ liệu do Editor thiếu `EditText`. | QuillEditor không expose widget EditText. Khắc phục: Tái sử dụng `QANoteHelper` dùng clipboard JSON-RPC và polling xác thực note trước khi xóa và khôi phục. | **ĐÃ KHẮC PHỤC** (Run 5 PASS) |

---

## 7. ĐÁNH GIÁ KẾT QUẢ VÀ KẾT LUẬN

1. **Tính trung thực và minh bạch:** Toàn bộ lịch sử thực thi (Run 1 FAIL, Run 2-3 BLOCKED, Run 4 ERROR cú pháp) được lưu vết minh bạch song song với kết quả thành công cuối cùng ở Run 5.
2. **Kết quả UI E2E chính thức:** Kịch bản `TC-BB-022` đạt **PASS (184.13s)** trên thiết bị thật Samsung Galaxy S21 FE 5G (Android 14). Đã phân biệt rõ: lệnh chạy lặp 2 lần do truyền trùng path pytest, tính chính xác **1 Test Case duy nhất**.
3. **Bảo toàn nghiệp vụ đa tầng:** Chức năng FN-11 đạt **100% PASS** ở cả hai tầng: UI E2E (1/1 TC) và Flutter Provider (3/3 tests: `PV-REF-05`, `PV-REF-12`, `PV-REF-15`).
4. **Trạng thái ghi nhận hiện tại:** **PASS (Run 5 mới nhất: 184.13s / 1 TC duy nhất)** — Minh chứng lưu tại [`evidence/fn11/FN11_TC-BB-022_D01_01.png`](../../evidence/fn11/FN11_TC-BB-022_D01_01.png) và [`fn11_restore_junit.xml`](fn11_restore_junit.xml).
