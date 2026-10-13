# White-Box Test Report: Note CRUD & Trash Lifecycle (NoteProvider)

## 1. Thông tin đợt chạy
- **Run ID**: `run_wb_trash_lifecycle_20261011_2155`
- **Thời gian**: 2026-10-11 21:58:00
- **Branch**: `huong`
- **Target File**: `lib/providers/note_provider.dart`
- **Test File**: `test/unit/note/note_trash_lifecycle_test.dart`
- **Phạm vi kiểm thử**: FN-29 / FN-30 (Note Deletion, Trash Lifecycle & Multi-select Trash Operations)

---

## 2. Kết quả thực thi tổng quan
- **Tổng số tests**: 15 tests
- **PASS**: 15 tests (100%)
- **FAIL**: 0 tests
- **BLOCKED**: 0 tests
- **Execution Log**: [test_execution.log](file:///d:/Workspace/TBDD/Smart-Note-App-QA/evidence/white_box/run_wb_trash_lifecycle_20261011_2155/test_execution.log)
- **LCOV File**: [lcov.info](file:///d:/Workspace/TBDD/Smart-Note-App-QA/evidence/white_box/run_wb_trash_lifecycle_20261011_2155/lcov.info)

---

## 3. Danh sách Test Cases & Kết quả chi tiết

| Mã Test Case | Nhóm chức năng | Tên bài kiểm thử / Mục tiêu kiểm thử | Kết quả |
| :--- | :--- | :--- | :---: |
| **TC-WB-TRASH-01** | `deleteNote` | Xóa ghi chú thường: chuyển status sang `trash`, cập nhật list, lưu repository, hủy reminder | **PASS** |
| **TC-WB-TRASH-02** | `deleteNote` | Xóa ghi chú ghim: loại bỏ khỏi `pinnedNotes`, chuyển sang `trashNotes`, lưu repository | **PASS** |
| **TC-WB-TRASH-03** | `deleteNote` | Xóa với ID không tồn tại: không biến đổi list, không gọi repository | **PASS** |
| **TC-WB-TRASH-04** | `restoreNote` | Khôi phục từ thùng rác về `normalNotes` với status `normal`, cập nhật repository | **PASS** |
| **TC-WB-TRASH-05** | `restoreNote` | Khôi phục với ID không nằm trong thùng rác: không thay đổi trạng thái | **PASS** |
| **TC-WB-TRASH-06** | `deleteNoteForever` | Xóa vĩnh viễn ghi chú khỏi thùng rác và gọi repo `deleteNoteForever` | **PASS** |
| **TC-WB-TRASH-07** | `deleteNoteForever` | Dọn dẹp ghi chú có đính kèm ảnh và âm thanh Cloudinary | **PASS** |
| **TC-WB-TRASH-08** | `fetchTrashNotes` | Thùng rác rỗng: không thực hiện xóa vĩnh viễn | **PASS** |
| **TC-WB-TRASH-09** | `fetchTrashNotes` | Giữ lại ghi chú chưa đủ 7 ngày (`daysInTrash < 7`) | **PASS** |
| **TC-WB-TRASH-10** | `fetchTrashNotes` | Tự động dọn dẹp ghi chú chạm mốc 7 ngày (`daysInTrash >= 7`) | **PASS** |
| **TC-WB-TRASH-11** | `fetchTrashNotes` | Tự động dọn dẹp ghi chú quá hạn 7 ngày (15 ngày và 30 ngày) | **PASS** |
| **TC-WB-TRASH-12** | Batch Operations | `restoreSelectedTrashNotes`: khôi phục tất cả ghi chú được chọn | **PASS** |
| **TC-WB-TRASH-13** | Batch Operations | `deleteForeverSelectedTrashNotes`: xóa vĩnh viễn tất cả ghi chú được chọn | **PASS** |
| **TC-WB-TRASH-14** | Robustness | Repository ném ngoại lệ khi `saveNote`: lan truyền lỗi an toàn cho caller | **PASS** |
| **TC-WB-TRASH-15** | Robustness | Platform channel ném ngoại lệ không làm sập `deleteNoteForever` | **PASS** |

---

## 4. Độ bao phủ mã nguồn (Code Coverage)
Đo lường bằng `flutter test --coverage` đối với production code:
- **`lib/providers/note_provider.dart`**:
  - Dòng được thực thi (LH): **94 dòng**
  - Tổng số dòng khả dụng (LF): **458 dòng**
  - Tỷ lệ bao phủ (Line Coverage): **20.52%**
- **Phương thức được bao phủ hoàn toàn các nhánh**:
  - `deleteNote(String id)` (100% branch: normal, pinned, not-found)
  - `restoreNote(String id)` (100% branch: found, not-found)
  - `deleteNoteForever(String id)` (100% branch: media check, list cleanup, repo call)
  - `fetchTrashNotes(String userId)` (100% branch: empty, <7 days, ==7 days, >7 days)
  - `restoreSelectedTrashNotes(List<String> ids)`
  - `deleteForeverSelectedTrashNotes(List<String> ids)`

---

## 5. Phát hiện kiến trúc & Lỗi logic tiềm ẩn (Architectural Defect Finding)

### DEFECT-WB-TRASH-01: Auto-purge trong `fetchTrashNotes` không dọn dẹp media Cloudinary do Note chưa có trong Memory
- **Vị trí**: [lib/providers/note_provider.dart:L463-L509](file:///d:/Workspace/TBDD/Smart-Note-App-QA/lib/providers/note_provider.dart#L463-L509)
- **Cơ chế**:
  1. Trong `fetchTrashNotes(userId)`, danh sách in-memory `_trashNotes` được reset rỗng: `_trashNotes = [];` (L466).
  2. Vòng lặp duyệt các note từ DB (`allTrash`), nếu `daysInTrash >= 7` thì gọi `await deleteNoteForever(note.id)` (L472).
  3. Bên trong `deleteNoteForever(id)`, hệ thống tìm kiếm `noteToDelete` trong các list bộ nhớ: `_trashNotes`, `_notes`, `_pinnedNotesList`, `_archivedNotes` (L487-L491).
  4. Do ghi chú quá hạn chưa từng được đưa vào bất kỳ list bộ nhớ nào (nó chỉ mới được load vào biến cục bộ `allTrash`), `noteToDelete` luôn nhận giá trị `null`!
  5. Hệ thống rơi vào nhánh rẽ:
     ```dart
     debugPrint('⚠️ deleteNoteForever: Không tìm thấy note $id trong memory — bỏ qua dọn Cloud, tiếp tục xóa DB.');
     ```
  6. Khối xóa file trên Cloudinary (`_cloudinaryService.deleteFile`) bị bỏ qua hoàn toàn đối với mọi ghi chú bị xóa tự động sau 7 ngày.
- **Hệ quả**: File ảnh và âm thanh đính kèm của các ghi chú hết hạn 7 ngày trong thùng rác bị **rò rỉ vĩnh viễn (orphaned cloud assets)** trên dịch vụ đám mây Cloudinary, tiêu tốn dung lượng lưu trữ cloud.
- **Tuân thủ quy định**: Không sửa production code trong đợt kiểm thử. Phát hiện được ghi nhận vào báo cáo bằng chứng phục vụ bug triage.
