# KẾ HOẠCH KIỂM THỬ HỘP TRẮNG CHỌN LỌC (SELECTIVE WHITE-BOX TEST PLAN)
## Dự án: Smart Note App
**Branch:** `huong`  
**Giai đoạn:** Chuẩn bị mở rộng kiểm thử Hộp trắng (White-box Unit Test Phase)  
**Tiêu chuẩn áp dụng:** IEEE 829 Test Planning & ISTQB Unit Testing  
**Trạng thái kế hoạch:** **ĐÃ LẬP KẾ HOẠCH — CHƯA VIẾT THÊM TEST, CHƯA CHẠY TEST**  
**Cam kết tuân thủ:** Không sửa đổi mã nguồn `lib/`, không chạy lệnh `flutter test` / `flutter pub get`, không commit / push git. Giữ nguyên toàn bộ bằng chứng kiểm thử hộp đen đã chốt.

---

## I. BỐI CẢNH & HIỆN TRẠNG BASELINE (18/18 UNIT TESTS PASS)

### 1.1. Đối chiếu hiện trạng từ bằng chứng kiểm thử đã lưu
Dựa trên bằng chứng log thực thi tại `evidence/white_box/note_model_run_20261010_0945/test_execution.log` và báo cáo độ bao phủ `evidence/white_box/note_model_run_20261010_0945/lcov.info`, hệ thống hiện có chính xác **18/18 Unit Tests đã đạt trạng thái PASS**:

| STT | Tệp kiểm thử | Tên kịch bản Unit Test | Đối tượng / Hàm kiểm thử | Kết quả baseline | Bằng chứng đối chiếu |
|:---:|:---|:---|:---|:---:|:---|
| 1 | `test/checklist_test.dart` | should create ChecklistItem with default values | `ChecklistItem()` | **PASS** | `test_execution.log` (00:00 +0) |
| 2 | `test/checklist_test.dart` | should create ChecklistItem with custom values | `ChecklistItem(id, text, checked)` | **PASS** | `test_execution.log` (00:00 +1) |
| 3 | `test/checklist_test.dart` | should convert ChecklistItem to JSON and from JSON | `toJson()` / `fromJson()` | **PASS** | `test_execution.log` (00:00 +2) |
| 4 | `test/checklist_test.dart` | should identify non-checklist content | `Note.isChecklist`, `checklistPlainText` | **PASS** | `test_execution.log` (00:00 +3) |
| 5 | `test/checklist_test.dart` | should identify checklist content and extract plain text | `Note.isChecklist`, `checklistPlainText` | **PASS** | `test_execution.log` (00:00 +4) |
| 6 | `test/checklist_copy_with_test.dart` | should retain all existing properties when no changes are passed | `ChecklistItem.copyWith()` | **PASS** | `test_execution.log` (00:02 +5) |
| 7 | `test/checklist_copy_with_test.dart` | should update supported fields when new values are provided | `ChecklistItem.copyWith(text, checked)` | **PASS** | `test_execution.log` (00:02 +6) |
| 8 | `test/checklist_copy_with_test.dart` | should allow toggling checked from true to false | `ChecklistItem.copyWith(checked: false)` | **PASS** | `test_execution.log` (00:02 +7) |
| 9 | `test/checklist_copy_with_test.dart` | should preserve original object unmodified after creating copy | `ChecklistItem` immutability check | **PASS** | `test_execution.log` (00:02 +8) |
| 10 | `test/note_model_test.dart` | should serialize toMap and deserialize fromMap with full data round-trip | `Note.toMap()`, `Note.fromMap()` | **PASS** | `test_execution.log` (00:04 +9) |
| 11 | `test/note_model_test.dart` | should apply default values when minimal map is provided to fromMap | `Note.fromMap()` minimal payload | **PASS** | `test_execution.log` (00:04 +10) |
| 12 | `test/note_model_test.dart` | should serialize toMap with null reminder and false booleans correctly | `Note.toMap()` null/false mapping | **PASS** | `test_execution.log` (00:04 +11) |
| 13 | `test/note_model_test.dart` | should support noteColor fallback when note_color key is absent in fromMap | `Note.fromMap()` camelCase fallback | **PASS** | `test_execution.log` (00:04 +12) |
| 14 | `test/note_model_test.dart` | should decode string lists when values are null or empty string in fromMap | `Note._decodeStringList()` null/empty | **PASS** | `test_execution.log` (00:04 +13) |
| 15 | `test/note_model_test.dart` | should decode string lists from valid JSON encoded arrays in fromMap | `Note._decodeStringList()` JSON array | **PASS** | `test_execution.log` (00:04 +14) |
| 16 | `test/note_model_test.dart` | should fallback to comma-separated values (CSV) when JSON decode fails | `Note._decodeStringList()` CSV fallback | **PASS** | `test_execution.log` (00:04 +15) |
| 17 | `test/note_model_test.dart` | should safely return empty list for non-list JSON strings and non-string inputs | `Note._decodeStringList()` type safety | **PASS** | `test_execution.log` (00:04 +16) |
| 18 | `test/note_model_test.dart` | should correctly parse boolean flag integer variants in fromMap | `Note.fromMap()` integer flag parser | **PASS** | `test_execution.log` (00:04 +17) |

*(Ghi chú: Các module `SearchService` và `EncryptionService` hoàn toàn không có trong danh mục 18 test trên do chưa có log thực thi tương ứng).*

### 1.2. Phân tích khoảng trống mã nguồn (Coverage Gaps)
Theo phân tích chi tiết từ `lcov.info` của baseline:
- `lib/models/checklist_item.dart`: Đã đạt **14/14 dòng lệnh (100.0% Line Coverage)**.
- `lib/models/note_model.dart`: Đạt **55/124 dòng lệnh (44.35% Line Coverage)**. Còn **69 dòng lệnh chưa được kiểm thử**, tập trung tại các vùng logic nghiệp vụ:
  1. Getter `pendingChecklistCount` (dòng 33–42): Chưa có bất kỳ ca kiểm thử nào.
  2. Getter `plainTextContent` (dòng 45–69): Logic bóc tách Quill Delta JSON `[{"insert": "..."}]` và xử lý chuỗi rỗng / lỗi chưa có ca kiểm thử nào.
  3. Phương thức `Note.copyWith()` (dòng 200–229): Logic tạo bản sao, xử lý cờ `clearReminder` và cơ chế sinh tự động `updatedAt` chưa được kiểm thử.
  4. Phương thức `Note.fromMap()` (dòng 149–157): Nhánh xử lý khi SQLite map thiếu trường thời gian `created_at` / `updated_at` chưa được xác minh.
  5. Logic phân xử Last-Write-Wins (LWW) dựa trên `updatedAt` (`lib/repositories/sync_repository.dart` dòng 67, 104, 121): Chưa có unit test độc lập so sánh mốc thời gian giữa bản ghi Local và Cloud.

---

## II. ĐỀ XUẤT PHẠM VI NHỎ & DANH SÁCH 8 TEST CASES MỚI DỰ KIẾN

Nhằm tối ưu hóa hiệu quả kiểm thử mà không dàn trải toàn bộ ứng dụng, kế hoạch giới hạn **chính xác 8 ca kiểm thử mới**. Các ca kiểm thử này tập trung vào xử lý dữ liệu thiếu / sai định dạng của `NoteModel`, phân tích nội dung Checklist / Rich-text, và kiểm tra logic so sánh `updatedAt` của thuật toán LWW trong bộ nhớ mà không cần phụ thuộc điện thoại thật hay Firebase.

Mã số Test Case được đặt tiếp nối từ **`TC-WB-015`** đến **`TC-WB-022`** (đảm bảo không trùng với `TC-WB-001` $\rightarrow$ `TC-WB-014` đã thiết kế trước đây).

| Mã TC | Tên kịch bản dự kiến | Tệp nguồn & Hàm kiểm thử | Cấu trúc luồng / Nhánh logic kiểm tra (Control Flow) | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected Output) | Căn cứ yêu cầu | Mức ưu tiên |
|:---:|:---|:---|:---|:---|:---|:---:|:---:|
| **TC-WB-015** | Đếm số lượng công việc chưa hoàn thành trong ghi chú Checklist | `lib/models/note_model.dart`<br>Hàm: `pendingChecklistCount` | • Nhánh 1: `!isChecklist` $\rightarrow$ trả về `0`.<br>• Nhánh 2: `isChecklist == true` $\rightarrow$ lọc đếm các mục có `checked != true`.<br>• Nhánh 3: Khối `catch (_)` khi `items` rỗng hoặc JSON lỗi $\rightarrow$ trả về `0`. | Note A: `content` văn bản thuần.<br>Note B: `content` checklist có 3 items (1 item `checked: true`, 2 items `checked: false`).<br>Note C: checklist có item thiếu key `checked`. | • Note A: `pendingChecklistCount == 0`.<br>• Note B: `pendingChecklistCount == 2`.<br>• Note C: tính là chưa hoàn thành $\rightarrow$ `pendingChecklistCount == 1`. Không phát sinh crash. | REQ-04<br>(FN-15 Checklist Counter) | **HIGH** |
| **TC-WB-016** | Trích xuất văn bản thuần (plain text) từ cấu trúc Quill Delta JSON | `lib/models/note_model.dart`<br>Hàm: `plainTextContent` | • Điều kiện: `isChecklist == false` và chuỗi JSON dạng mảng Delta `[{"insert": "..."}]`.<br>• Vòng lặp: Duyệt qua các phần tử mảng, kiểm tra `item is Map && item.containsKey('insert')`.<br>• Nhánh `val is String`: Nối chuỗi vào buffer; bỏ qua các insert dạng object (như embed ảnh). | `content = jsonEncode([`<br>`{"insert": "Tiêu đề ghi chú\n"},`<br>`{"insert": {"image": "https://img.com/p.png"}},`<br>`{"insert": "Đoạn văn bản chi tiết"}`<br>`])` | `plainTextContent` trả về chuỗi đã nối các đoạn string: `"Tiêu đề ghi chú\nĐoạn văn bản chi tiết"`. Đoạn embed ảnh dạng Map bị bỏ qua an toàn. | REQ-03<br>(FN-09 / FN-23 Text Extraction) | **HIGH** |
| **TC-WB-017** | Xử lý dữ liệu rỗng, văn bản thuần và JSON malformed trong plainTextContent | `lib/models/note_model.dart`<br>Hàm: `plainTextContent` | • Nhánh 1: `content.isEmpty` $\rightarrow$ trả về `''`.<br>• Nhánh 2: Chuỗi bắt đầu bằng `[` hoặc `{` nhưng JSON lỗi cú pháp $\rightarrow$ rơi vào `catch (_)` và fallback về `trimmed`.<br>• Nhánh 3: Chuỗi văn bản thuần túy không bắt đầu bằng `[` hay `{` $\rightarrow$ trả về trực tiếp `trimmed`. | Payload 1: `content = ""` (chuỗi rỗng).<br>Payload 2: `content = "[{invalid_json_format"` (JSON lỗi).<br>Payload 3: `content = "   Ghi chú thuần túy không định dạng   "`. | • Payload 1: trả về `""`.<br>• Payload 2: rơi vào fallback an toàn, trả về `"[{invalid_json_format"`.<br>• Payload 3: trả về chuỗi đã trim `"Ghi chú thuần túy không định dạng"`. | REQ-03<br>(Data Integrity & Robustness) | **HIGH** |
| **TC-WB-018** | Cơ chế xóa nhắc nhở thông qua cờ clearReminder trong Note.copyWith | `lib/models/note_model.dart`<br>Hàm: `Note.copyWith()` | • Điều kiện ternary: `clearReminder ? null : (reminder ?? this.reminder)`.<br>• Nhánh 1: `clearReminder == true` $\rightarrow$ xóa nhắc nhở về `null`.<br>• Nhánh 2: `clearReminder == false` và không truyền `reminder` $\rightarrow$ giữ nguyên `this.reminder`.<br>• Nhánh 3: Truyền `reminder` mới $\rightarrow$ cập nhật mốc thời gian mới. | Note ban đầu có `reminder = DateTime(2026, 10, 20)`.<br>Thao tác 1: `note.copyWith(clearReminder: true)`.<br>Thao tác 2: `note.copyWith(title: "New Title")`.<br>Thao tác 3: `note.copyWith(reminder: DateTime(2026, 11, 1))`. | • Thao tác 1: `result1.reminder == null`.<br>• Thao tác 2: `result2.reminder` vẫn giữ ngày `2026-10-20`.<br>• Thao tác 3: `result3.reminder` mang ngày `2026-11-01`. | REQ-08<br>(FN-38 Nhắc nhở) | **MEDIUM** |
| **TC-WB-019** | Hành vi cập nhật mốc thời gian updatedAt trong Note.copyWith | `lib/models/note_model.dart`<br>Hàm: `Note.copyWith()` | • Điều kiện gán: `updatedAt: updatedAt ?? DateTime.now()`.<br>• Nhánh 1: Không truyền `updatedAt` $\rightarrow$ tự động sinh `DateTime.now()` (mới hơn note gốc).<br>• Nhánh 2: Truyền giá trị `updatedAt` cụ thể $\rightarrow$ gán chính xác giá trị được truyền (phục vụ đồng bộ dữ liệu). | Note gốc có `updatedAt = DateTime(2026, 10, 1, 10, 0, 0)`.<br>Trường hợp 1: `note.copyWith(title: "Sửa nội dung")` (không truyền `updatedAt`).<br>Trường hợp 2: `note.copyWith(updatedAt: DateTime(2026, 10, 5, 12, 0, 0))`. | • Trường hợp 1: `result1.updatedAt` có mốc thời gian tại thời điểm test chạy ($\ge$ note gốc).<br>• Trường hợp 2: `result2.updatedAt` bằng chính xác `2026-10-05 12:00:00`. | REQ-05<br>(FN-40/41 LWW Timestamp Tracking) | **HIGH** |
| **TC-WB-020** | Khả năng phòng thủ khi SQLite map thiếu trường thời gian trong Note.fromMap | `lib/models/note_model.dart`<br>Hàm: `Note.fromMap()` | • Nhánh fallback: `m['created_at'] ?? DateTime.now().millisecondsSinceEpoch`.<br>• Nhánh fallback: `m['updated_at'] ?? DateTime.now().millisecondsSinceEpoch`.<br>• Nhánh null: `m['reminder'] != null ? ... : null`. | Map SQLite khuyết thiếu:<br>`{`<br>`  'id': 'note-legacy-001',`<br>`  'title': 'Bản ghi cũ',`<br>`  'content': 'Nội dung',`<br>`  'created_at': null,`<br>`  'updated_at': null,`<br>`  'reminder': null`<br>`}` | • Đối tượng `Note` được khởi tạo thành công không bị ném ngoại lệ `TypeError` hoặc crash.<br>• `note.createdAt` và `note.updatedAt` nhận mốc thời gian fallback hợp lệ.<br>• `note.reminder` bằng `null`. | REQ-07<br>(Database Robustness) | **MEDIUM** |
| **TC-WB-021** | So sánh thứ tự ưu tiên Last-Write-Wins (LWW) độc lập trên cặp bản ghi Note | Mô phỏng logic so sánh `updatedAt.isAfter()` từ `lib/repositories/sync_repository.dart` | • Nhánh 1: `local.updatedAt.isAfter(cloud.updatedAt) == true` $\rightarrow$ Local thắng (cần đẩy lên Cloud).<br>• Nhánh 2: `cloud.updatedAt.isAfter(local.updatedAt) == true` $\rightarrow$ Cloud thắng (cần ghi đè xuống Local).<br>• Nhánh 3: `local.updatedAt.isAtSameMomentAs(cloud.updatedAt)` $\rightarrow$ Cả 2 `isAfter` đều là `false`. | Cặp 1: `local.updatedAt` = 12:00:05, `cloud.updatedAt` = 12:00:00.<br>Cặp 2: `local.updatedAt` = 12:00:00, `cloud.updatedAt` = 12:00:05.<br>Cặp 3: `local.updatedAt` = 12:00:00, `cloud.updatedAt` = 12:00:00. | • Cặp 1: `local.updatedAt.isAfter(cloud.updatedAt)` trả về `true`.<br>• Cặp 2: `cloud.updatedAt.isAfter(local.updatedAt)` trả về `true`.<br>• Cặp 3: Cả hai điều kiện đều `false`. *(Ghi chú SRS: Trường hợp trùng mốc thời gian chưa có quy tắc tie-break phân xử $\rightarrow$ **Cần làm rõ**)*. | REQ-05<br>(FN-41 Conflict Resolution) | **HIGH** |
| **TC-WB-022** | Khả năng chịu lỗi khi phân tích ChecklistItem.fromJson với trường rỗng/null | `lib/models/checklist_item.dart`<br>Hàm: `ChecklistItem.fromJson()` | • Nhánh `json['id'] as String?`: nhận ID hoặc sinh UUID tự động khi khởi tạo.<br>• Nhánh `json['text'] as String? ?? ''`: fallback về chuỗi rỗng khi null.<br>• Nhánh `json['checked'] as bool? ?? false`: fallback về `false` khi null. | Payload JSON lỗi/khuyết:<br>`{`<br>`  'id': null,`<br>`  'text': null,`<br>`  'checked': null`<br>`}` | • Đối tượng `ChecklistItem` được tạo an toàn không crash.<br>• `item.id` là chuỗi UUID hợp lệ không rỗng.<br>• `item.text == ''`.<br>• `item.checked == false`. | REQ-04<br>(FN-15 Checklist Parsing Fault Tolerance) | **MEDIUM** |

---

## III. KẾ HOẠCH THỰC THI DỰ KIẾN (CHƯA THỰC THI)

### 3.1. Phương pháp & Lệnh chạy dự kiến
Khi người dùng phê duyệt kế hoạch và cho phép thực thi, các ca kiểm thử mới sẽ được tổ chức trong tệp test tương ứng và chạy bằng Flutter Test Runner:
```bash
# Lệnh chạy dự kiến khi được duyệt (HIỆN TẠI CHƯA CHẠY):
flutter test test/note_model_advanced_test.dart --coverage
```

### 3.2. Quy trình thu thập Log & Coverage
1. **Thu thập Log thực thi:** Chuyển hướng toàn bộ output stdout/stderr của lệnh chạy vào file log:
   `evidence/white_box/run_<timestamp>/test_execution.log`.
2. **Thu thập báo cáo Coverage:** Thu thập tệp `coverage/lcov.info` do Flutter sinh ra, lưu trữ tại thư mục evidence tương ứng để phân tích tỷ lệ bao phủ dòng bổ sung.

### 3.3. Tiêu chí hoàn tất (Definition of Done)
1. **Tính độc lập & 100% Pass:** Toàn bộ 8 ca kiểm thử mới khi chạy phải đạt kết quả PASS mà không làm ảnh hưởng hay gãy bất kỳ test nào trong 18 baseline unit test đang có.
2. **Không phụ thuộc thiết bị/đám mây:** Toàn bộ 8 ca kiểm thử chỉ sử dụng dữ liệu trong bộ nhớ (pure in-memory unit tests), không kết nối SQLite thật, Firebase thật hay thiết bị Android vật lý.
3. **Minh bạch số liệu:** Tuyệt đối không ghi trước kết quả PASS hay tỷ lệ phần trăm coverage giả định khi lệnh chạy chưa được thực thi thực tế.

### 3.4. Giới hạn môi trường & Bảo toàn hệ thống
- Môi trường kiểm thử hộp trắng giới hạn trong Dart VM / Flutter Test Framework trên máy trạm (Host PC).
- Không can thiệp sửa đổi bất kỳ tệp nào trong `lib/`.
- Không tự ý chạy `flutter test` hoặc `flutter pub get`.
- Không thực hiện commit hay push lên git repository.
- Toàn bộ kết quả và evidence của đợt kiểm thử hộp đen đã đóng trước đó được giữ nguyên vẹn 100%.
