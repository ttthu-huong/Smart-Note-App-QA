# Báo Cáo Kiểm Thử Hộp Trắng Module Search (FN-23 / REQ-08)

**Dự án:** Smart-Note-App-QA  
**Branch:** `huong`  
**Thời gian thực hiện:** 2026-10-11 21:38  
**File kiểm thử:** [test/unit/search/search_notes_whitebox_test.dart](file:///d:/Workspace/TBDD/Smart-Note-App-QA/test/unit/search/search_notes_whitebox_test.dart)  
**Evidence directory:** [evidence/white_box/run_wb_search_20261011_2138/](file:///d:/Workspace/TBDD/Smart-Note-App-QA/evidence/white_box/run_wb_search_20261011_2138/)

---

## 1. Mục Tiêu & Cơ Chế Kiểm Thử

- **Mục tiêu:** Kiểm thử trực tiếp production code `LocalNoteService.searchNotes({required String userId, required String query})` trên branch `huong`.
- **Ràng buộc:** Không sửa đổi bất kỳ file nào trong `lib/`, không sửa `pubspec.yaml`, không thêm dependency mới, không merge `origin/dung`.
- **Cơ chế Test Database:**
  - Khởi tạo `databaseFactory = impl.sqfliteDatabaseFactory` kết hợp với `TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler` trên MethodChannel `'com.tekartik.sqflite'`.
  - Cơ chế này cho phép các lời gọi production database từ `LocalNoteService._initDb()` và `LocalNoteService.searchNotes()` thực thi tự nhiên trong môi trường headless unit test mà không cần native plugin channel thực của thiết bị.
  - Production code gọi trực tiếp câu lệnh SQL và logic client-side filtering thật 100%.

---

## 2. Kết Quả Kiểm Thử (15 Test Cases)

| Mã Test | Tên Test Case | Nhánh / Logic được kiểm thử | Kết quả | Ghi chú |
|---------|---------------|-----------------------------|:-------:|---------|
| `TC-WB-SRCH-01` | Query chuỗi rỗng / khoảng trắng | Gọi `getAllNotes(userId)` | **PASS** | Lấy toàn bộ note của `u1`, trừ `trash` |
| `TC-WB-SRCH-02` | Tìm kiếm theo Tiêu đề | SQL LIKE `LOWER(title) LIKE ?` | **PASS** | Khớp note `n1` có tiêu đề chứa 'Flutter' |
| `TC-WB-SRCH-03` | Tìm kiếm theo Nội dung | SQL LIKE `LOWER(content) LIKE ?` | **PASS** | Khớp note `n3` có nội dung chứa 'mccabe' |
| `TC-WB-SRCH-04` | Không phân biệt hoa/thường | Chuyển đổi query sang lowercase | **PASS** | `'FLUTTER'` và `'flutter'` trả kết quả giống hệt |
| `TC-WB-SRCH-05` | Loại trừ Thùng rác | Điều kiện `status != 'trash'` | **PASS** | Note `n7` trong thùng rác không bao giờ xuất hiện |
| `TC-WB-SRCH-06` | Token Filter `has:image` | Bóc tách token + `note.imageUrls.isNotEmpty` | **PASS** | Chỉ note `n2` có ảnh |
| `TC-WB-SRCH-07` | Token Filter `has:audio` | Bóc tách token + `note.audioUrls.isNotEmpty` | **PASS** | Chỉ note `n3` có audio |
| `TC-WB-SRCH-08` | Token Filter `has:url` | Bóc tách token + RegExp kiểm tra URL | **PASS** | Khớp note `n4` có link |
| `TC-WB-SRCH-09` | Token Filter `is:pinned` | Bóc tách token + `note.status == 'pinned'` | **PASS** | Khớp note `n5` được ghim |
| `TC-WB-SRCH-10` | Token Filter `is:archived` | Bóc tách token + lọc mặc định loại trừ archived | **PASS** | Có token lấy `n6`, không có token loại trừ `n6` |
| `TC-WB-SRCH-11` | Token Filter `label:"..."` | Bóc tách token bằng RegExp + kiểm tra `note.tags` | **PASS** | Khớp note `n2` có nhãn 'Thiết kế' |
| `TC-WB-SRCH-12` | Kết hợp Text + Token | Text query + Token Filter đồng thời | **PASS** | `'Figma has:image'` lọc chính xác `n2` |
| `TC-WB-SRCH-13` | Phân tách theo `userId` | Điều kiện SQL `user_id = ?` | **PASS** | `u1` không nhìn thấy note của `u2` |
| `TC-WB-SRCH-14` | Ký tự đặc biệt SQL LIKE | Kiểm tra an toàn ký tự `%` và `_` | **PASS** | Không gây exception crash |
| `TC-WB-SRCH-15` | **BUG-004:** Token Filter `has:list` | Bóc tách token `has:list` và lọc checklist notes | **FAIL** | **Tái hiện trực tiếp BUG-004** |

**Tổng cộng:** **14 PASS / 1 FAIL** (Tái hiện thành công BUG-004 mà không sửa logic test để ép PASS).

---

## 3. Phân Tích Lỗi BUG-004 Được Tái Hiện

- **Đặc tả nghiệp vụ (SRS REQ-08 & TC-BB-027G-D01):**
  Khi người dùng chọn bộ lọc loại "Danh sách" (`has:list`) trên UI tìm kiếm, hệ thống phải lọc và hiển thị danh sách các ghi chú công việc dạng checklist.
- **Đường đi mã nguồn (Source Path):**
  Tại [lib/services/local_note_service.dart](file:///d:/Workspace/TBDD/Smart-Note-App-QA/lib/services/local_note_service.dart#L175-L189):
  ```dart
  final hasImageToken = lowerQuery.contains('has:image');
  final hasAudioToken = lowerQuery.contains('has:audio');
  final hasUrlToken = lowerQuery.contains('has:url');
  final isPinnedToken = lowerQuery.contains('is:pinned');
  final isArchivedToken = lowerQuery.contains('is:archived');
  ```
  Token `has:list` **hoàn toàn bị bỏ quên**, không được bóc tách và không bị loại bỏ khỏi `cleanTextQuery`.
- **Thực tế xảy ra:**
  `cleanTextQuery` bị giữ nguyên chuỗi thô `"has:list"`. Hàm gửi câu truy vấn SQL:
  `LOWER(title) LIKE '%has:list%' OR LOWER(content) LIKE '%has:list%'`
  Do ghi chú checklist không có chuỗi văn bản `"has:list"` nên truy vấn trả về rỗng `[]` (`Actual: <0>`).
- **Kết luận:** Lỗi sản phẩm xác thực (**CONFIRMED PRODUCT DEFECT** - `BUG-004`).

---

## 4. Đo Lường Độ Bao Phủ Mã (LCOV Coverage)

Độ bao phủ đạt được trên `lib/services/local_note_service.dart`:
- **Lines Hit:** 49
- **Lines Found:** 157
- **Line Coverage:** **31.21%** (Tăng từ 0.00% lên 31.21% sau khi đưa vào kiểm thử hộp trắng Search).
