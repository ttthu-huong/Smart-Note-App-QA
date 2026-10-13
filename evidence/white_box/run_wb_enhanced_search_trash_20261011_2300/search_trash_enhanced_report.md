# White-Box Quality Enhancement Report: Search & Note Trash Lifecycle

## 1. Thông tin đợt chạy
- **Run ID**: `run_wb_enhanced_search_trash_20261011_2300`
- **Thời gian**: 2026-10-11 23:01:00
- **Branch**: `huong`
- **Các file test thực thi**:
  1. `test/unit/search/search_notes_whitebox_test.dart` (15 tests)
  2. `test/unit/note/note_trash_lifecycle_test.dart` (17 tests)
- **Tập tin lưu bằng chứng**:
  - Log thực thi: [test_execution.log](file:///d:/Workspace/TBDD/Smart-Note-App-QA/evidence/white_box/run_wb_enhanced_search_trash_20261011_2300/test_execution.log)
  - LCOV: [lcov.info](file:///d:/Workspace/TBDD/Smart-Note-App-QA/evidence/white_box/run_wb_enhanced_search_trash_20261011_2300/lcov.info)

---

## 2. Kết quả thực thi tổng quan
- **Tổng số tests thực thi**: **32 tests**
- **PASS**: **29 tests** (90.6%)
- **FAIL**: **3 tests** (9.4% — gồm 3 lỗi thực tế phát hiện trong production code)
- **SKIP / BLOCKED**: **0 tests**

---

## 3. Chi tiết kết quả kiểm thử theo từng Module

### A. Module Tìm kiếm (LocalNoteService Search — FN-23): 15 tests (14 PASS / 1 FAIL)
- **TC-WB-SRCH-01 .. TC-WB-SRCH-13**: **PASS** (Bao phủ query rỗng, title match, content match, case-insensitivity, exclude trash, token filters `has:image`, `has:audio`, `has:url`, `is:pinned`, `is:archived`, `label:"..."`, combination, multi-user isolation).
- **TC-WB-SRCH-14**: **PASS** (Đã cải tiến: Phân tích SQL Generator, kiểm chứng `lastCapturedArgs` nhận `['u1', 'trash', '%%%', '%%%']` và `['u1', 'trash', '%_%', '%_%']` xác minh production code đưa trực tiếp ký tự wildcard vào SQL mà không escape).
- **TC-WB-SRCH-15 (BUG-004)**: **FAIL** (Xác nhận lỗi sản phẩm: Token `has:list` không được bóc tách, sinh câu SQL `LIKE '%has:list%'` trả về 0 kết quả).

### B. Module Thùng rác & Vòng đời ghi chú (NoteProvider Trash Lifecycle — FN-29 / FN-30): 17 tests (15 PASS / 2 FAIL)
- **TC-WB-TRASH-01 .. TC-WB-TRASH-06**: **PASS** (Xóa thường, xóa ghim, xóa non-existent, khôi phục thường, khôi phục non-existent, xóa vĩnh viễn khỏi trash).
- **TC-WB-TRASH-07**: **PASS** (Đã chuẩn hóa tên và kỳ vọng: Xác minh `deleteNoteForever` gỡ sạch ghi chú có danh sách media khỏi in-memory và repository DB).
- **TC-WB-TRASH-08 .. TC-WB-TRASH-09**: **PASS** (Thùng rác rỗng, ghi chú 3 ngày chưa đủ hạn).
- **TC-WB-TRASH-10a**: **PASS** (Trường hợp cận biên dưới: Ghi chú 6 ngày 23 giờ 50 phút $\rightarrow$ `daysInTrash == 6 < 7` $\rightarrow$ Giữ lại trong thùng rác).
- **TC-WB-TRASH-10b**: **PASS** (Trường hợp chạm đúng mốc biên: Ghi chú 7 ngày 0 giờ 5 giây $\rightarrow$ `daysInTrash == 7 >= 7` $\rightarrow$ Tự động purge vĩnh viễn).
- **TC-WB-TRASH-11 .. TC-WB-TRASH-13**: **PASS** (Ghi chú quá hạn 15d & 30d, batch restore, batch purge).
- **TC-WB-TRASH-14**: **PASS** (Kiểm tra Repository `saveNote` ném ngoại lệ được lan truyền an toàn cho caller).
- **TC-WB-TRASH-15**: **FAIL** (Phát hiện lỗi Robustness: Platform channel `cancelReminder` ném ngoại lệ làm sập `deleteNoteForever`, không hoàn thành xóa in-memory và DB).
- **TC-WB-TRASH-16 (DEFECT-WB-TRASH-01)**: **FAIL** (Xác minh lỗi sản phẩm qua `HttpOverrides`: Tự động xóa ghi chú quá hạn 7 ngày bỏ qua yêu cầu dọn media Cloudinary do `noteToDelete` bị `null` trong memory).

---

## 4. Chi tiết 3 Defect phát hiện có bằng chứng thực thi độc lập

### 1. BUG-004: Token filter `has:list` bị truyền thô vào câu lệnh SQL LIKE
- **Test**: `TC-WB-SRCH-15`
- **File**: `lib/services/local_note_service.dart:L175-L189`
- **Bằng chứng**: Expected 1 checklist note, Actual 0 note do SQL `LIKE '%has:list%'`.

### 2. DEFECT-WB-TRASH-01: Auto-purge trong `fetchTrashNotes` không dọn dẹp media Cloudinary
- **Test**: `TC-WB-TRASH-16`
- **File**: `lib/providers/note_provider.dart:L468-L509`
- **Bằng chứng**: Chặn HTTP bằng `HttpOverrides`, ghi nhận 0 request destroy gửi đi (`Actual: <0>`) vì `noteToDelete == null`, trong khi Expected phải gửi ít nhất 1 request xóa ảnh (`greaterThan(0)`).

### 3. DEFECT-WB-TRASH-02 (Robustness): `deleteNoteForever` bị vỡ khi `ReminderService` gặp sự cố
- **Test**: `TC-WB-TRASH-15`
- **File**: `lib/providers/note_provider.dart:L483`
- **Bằng chứng**: `cancelReminder` ném `PlatformException(CANCEL_ERROR)`, `deleteNoteForever` không có try-catch bọc ngoài nên crash và hủy bỏ toàn bộ quá trình xóa ghi chú khỏi bộ nhớ và DB.

---

## 5. Thống kê Code Coverage (Line Coverage)
- `lib/services/local_note_service.dart`: **49 / 157 dòng (31.21%)**
- `lib/providers/note_provider.dart`: **94 / 458 dòng (20.52%)**
- `lib/services/cloudinary_service.dart`: **8 / 81 dòng (9.88%)**
