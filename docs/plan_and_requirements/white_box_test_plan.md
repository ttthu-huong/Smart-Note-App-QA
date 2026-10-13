# KẾ HOẠCH KIỂM THỬ HỘP TRẮNG CHỌN LỌC (SELECTIVE WHITE-BOX TEST PLAN)
## Dự án: Smart Note App
**Branch:** `huong`  
**Giai đoạn:** Chuẩn bị mở rộng kiểm thử Hộp trắng (White-box Unit Test Phase)  
**Tiêu chuẩn áp dụng:** IEEE 829 Test Planning & ISTQB White-box Unit Testing  
**Trạng thái kế hoạch:** **ĐÃ HOÀN THIỆN VÀ CHỐT (FROZEN TEST PLAN) — CHỜ PHÊ DUYỆT THỰC THI**  
**Cam kết tuân thủ:** Tuyệt đối không can thiệp sửa đổi mã nguồn `lib/`, không tự ý chạy `flutter test`/`flutter pub get`, không sửa đổi evidence cũ, không commit/push git. Bảo toàn 100% kết quả và bằng chứng của các giai đoạn kiểm thử trước.

---

## I. BỐI CẢNH & HIỆN TRẠNG BASELINE (18/18 UNIT TESTS PASS)

### 1.1. Đối chiếu hiện trạng từ bằng chứng kiểm thử đã lưu
Dựa trên bằng chứng log thực thi tại `evidence/white_box/note_model_run_20261010_0945/test_execution.log` và báo cáo độ bao phủ LCOV tại `evidence/white_box/note_model_run_20261010_0945/lcov.info`, hệ thống hiện có chính xác **18/18 Unit Tests đã đạt trạng thái PASS**:

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

*(Lưu ý: 8 test mô phỏng quy tắc bảo mật trong `test/security_rules_test.dart` đã thực thi PASS về mặt biểu thức logic bằng Dart trong bộ nhớ — **Dart Rule Logic Simulation**, nhưng **KHÔNG phải** là kết quả chạy trên **Firebase Emulator Rules Engine** thực tế).*

### 1.2. Phân tích độ bao phủ Baseline (Measured Baseline Coverage)
Dữ liệu đo lường thực tế từ `evidence/white_box/note_model_run_20261010_0945/lcov.info`:
- **`lib/models/checklist_item.dart`**:
  - Dòng lệnh tìm thấy (LF): 14
  - Dòng lệnh được thực thi (LH): 14
  - **Tỷ lệ Line Coverage thực tế: 100.0% (14/14 dòng)**.
- **`lib/models/note_model.dart`**:
  - Dòng lệnh tìm thấy (LF): 124
  - Dòng lệnh được thực thi (LH): 55
  - **Tỷ lệ Line Coverage thực tế: 44.35% (55/124 dòng)**.
  - Số dòng chưa được bao phủ: **69 dòng lệnh**.
- **Tổng thể phạm vi Models đã đo:**
  - Tổng số dòng tìm thấy (LF): 138
  - Tổng số dòng được thực thi (LH): 69
  - **Tỷ lệ Line Coverage toàn bộ Baseline: 50.00% (69/138 dòng)**.

---

---

## II. TIÊU CHÍ LỰA CHỌN FUNCTIONAL REQUIREMENTS / MODULES CHO WHITE-BOX UNIT TESTING

Để đảm bảo nguồn lực kiểm thử được tập trung tối ưu vào những thành phần rủi ro nhất và có giá trị cao nhất, các chức năng (FN) và module phần mềm được đánh giá chọn lọc theo 4 tiêu chí chuẩn hóa:
1. **Độ phức tạp thuật toán & Cyclomatic Complexity ($V(G)$):** Các module có nhiều điểm rẽ nhánh, biểu thức điều kiện lồng nhau, vòng lặp phân tích dữ liệu (ví dụ Quill Delta JSON parser, LWW reconciliation).
2. **Mức độ rủi ro nghiệp vụ & Tác động lỗi (Business Risk & Severity):** Các tính năng nếu gặp lỗi sẽ dẫn đến hỏng/mất dữ liệu của người dùng, rò rỉ dữ liệu chéo người dùng, hoặc xung đột trạng thái dữ liệu (ví dụ Note Serialization, Firestore Security Rules, Timestamp conflict).
3. **Lịch sử lỗi & Tần suất khiếm khuyết (Defect History):** Các chức năng từng phát sinh Bug trong kiểm thử hộp đen hoặc có lỗ hổng kiến trúc tiềm ẩn (như `BUG-001` Timeout media, `BUG-004` tìm kiếm tiếng Việt).
4. **Tính khả thi kỹ thuật & Ràng buộc phụ thuộc (Feasibility & Testability under No-Code-Change constraint):** Khả năng thực thi trực tiếp trên Dart VM / Flutter Test Framework mà **không cần sửa đổi `lib/`** (ưu tiên In-Memory models không phụ thuộc static singleton).

### Bảng đánh giá tiêu chí lựa chọn Module / Chức năng (Selection Criteria Assessment Matrix)

| Module / Class | Phương thức / Chức năng đại diện | Mã FN liên quan | Độ phức tạp ($V(G)$) | Mức độ rủi ro | Lịch sử lỗi | Tính khả thi (Không sửa `lib/`) | Quyết định lựa chọn & Phạm vi |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`Note` (Model)** | `pendingChecklistCount`, `plainTextContent`, `copyWith`, `fromMap` | FN-08, FN-09, FN-15, FN-23, FN-38, FN-41 | **Cao** ($V(G) = 4..11$) | **Rất cao** (Mất/hỏng dữ liệu ghi chú) | Từng lỗi bóc tách checklist, xử lý unicode/delta | **100% Khả thi** (Pure In-Memory) | **ĐƯỢC CHỌN TRỌNG TÂM (P1/P2 — `READY`)**: `TC-WB-015..020` |
| **`ChecklistItem`** | `fromJson`, `copyWith`, `toJson` | FN-15 | **Trung bình** ($V(G) = 4$) | **Cao** (Hỏng cấu trúc todo list) | Khuyết trường `null` gây crash `TypeError` | **100% Khả thi** (Pure In-Memory) | **ĐƯỢC CHỌN (P2 — `READY`)**: `TC-WB-022` + Baseline tests |
| **`SyncRepository`** | Toán tử LWW `DateTime.isAfter` | FN-41 | **Trung bình** ($V(G) = 3$) | **Rất cao** (Ghi đè mất dữ liệu đa thiết bị) | Tranh chấp đồng bộ `BR-03` | **Khả thi logic toán tử** (In-Memory Reference) | **ĐƯỢC CHỌN LOGIC (P1 — `READY`)**: `TC-WB-021` *(Accepted Gap: Không tính coverage file `sync_repository.dart`)* |
| **`Security Rules`** | `isOwner`, `isValidNote` | FN-40 (NFR-03) | **Trung bình** ($V(G) = 3..4$) | **Tối thượng** (Rò rỉ dữ liệu người dùng) | Nguy cơ bypass quyền đọc/ghi Cloud Firestore | **Khả thi mô phỏng** (Dart Rule Logic Simulation) | **ĐƯỢC CHỌN MÔ PHỎNG (P2 — `SIMULATION PASS`)**: `TC-WB-011..014` |
| **`CloudinaryService`** | `_extractPublicId`, `uploadImage` | FN-12, FN-35, FN-36 | **Trung bình** ($V(G) = 4$) | **Trung bình** (Rác Cloudinary, lỗi upload) | `BUG-001` Timeout upload mạng treo | **Một phần** (`006, 008` khả thi; `007, 009, 010` cần HttpOverrides) | **CHỌN CÓ ĐIỀU KIỆN (P2/P3 — `DESIGN ONLY`)**: `TC-WB-006..010` |
| **`AuthProvider`** | `setError`, `_syncUserProfile`, `authStateChanges` | FN-01, FN-02, FN-04, FN-07 | **Thấp – TB** ($V(G) = 2..3$) | **Cao** (Lỗi phiên đăng nhập) | Lỗi regex disposable domains | **Bị chặn** (Static singleton `FirebaseAuth/Firestore`) | **GIỮ THIẾT KẾ (P2 — `DESIGN ONLY`)**: `TC-WB-001..005` *(Được bổ sung bằng 3 tests mô phỏng logic validation của Dũng)* |

## III. MA TRẬN ĐỘ BAO PHỦ HỘP TRẮNG & TÍNH KHẢ THI KỸ THUẬT (COVERAGE & FEASIBILITY MATRIX)

Ma trận dưới đây tổng hợp toàn diện các module trong phạm vi kiểm thử White-box chọn lọc, phân định rõ ràng giữa **Độ bao phủ thực tế đã đo (Measured Baseline Coverage)**, **Độ bao phủ mục tiêu kỳ vọng (Target Benchmark — không phải kết quả đã đạt)** và **Khả năng thực thi dưới ràng buộc không sửa `lib/`**:

| Module / Class | Phương thức / Logic kiểm thử | Test Case tương ứng | Nhánh / Điều kiện được thiết kế bao phủ | Baseline Coverage thực tế (Đã đo) | Khoảng trống chưa bao phủ & Ràng buộc kỹ thuật | Mức ưu tiên & Tính khả thi | Mục tiêu độ bao phủ kỳ vọng (TARGET) |
| :--- | :--- | :---: | :--- | :---: | :--- | :---: | :---: |
| `ChecklistItem`<br>(`checklist_item.dart`) | Constructor, `toJson`, `fromJson`, `copyWith` | 9 Unit Tests Baseline + `TC-WB-022` | Khởi tạo mặc định, chuyển đổi map/json, copy có/không tham số, toggle check, **xử lý an toàn khi json khuyết trường (`id`, `text`, `checked` là `null`)** | **100.0% Line**<br>(14/14 lines) | Nhánh fallback `fromJson` (L22–24 $\rightarrow$ L13) khi các trường `id`, `text`, `checked` mang giá trị `null` | **P2 — READY**<br>*(Pure In-Memory)* | Duy trì **100.0% Line** + bao phủ 100% nhánh phòng thủ |
| `NoteModel`<br>(`note_model.dart`) | `isChecklist`, `checklistPlainText` | Baseline Tests 4, 5 | Phân biệt JSON checklist vs text thuần, trích xuất text checklist | Đã phủ L7-27 | Đã phủ luồng chính trong baseline | **P1 — EXECUTED** | Duy trì 100% |
| `NoteModel`<br>(`note_model.dart`) | `pendingChecklistCount` | **`TC-WB-015`** | Nhánh `!isChecklist` (L34), fallback `items ?? []` (L37), lọc `i['checked'] != true` (L38), và **khối `catch (_)` (L39–41) qua `items` sai kiểu (`"corrupted_not_a_list"`)** | **0.0%**<br>(L33–42 chưa hit) | 10 dòng lệnh logic đếm và bắt lỗi hoàn toàn chưa có test | **P1 — READY**<br>*(Pure In-Memory)* | **TARGET: 100% Line & Branch** của getter `pendingChecklistCount` |
| `NoteModel`<br>(`note_model.dart`) | `plainTextContent` | **`TC-WB-016`**, **`TC-WB-017`** | `isEmpty` (L46), `isChecklist` (L47), `startsWith('[' &#124; '{')` (L51), `decoded is List` T/F (L54), vòng lặp Delta (`item is Map` T/F, `containsKey('insert')` T/F, `val is String` T/F), `catch (_)` (L66) | **0.0%**<br>(L45–69 chưa hit) | 25 dòng lệnh bóc tách nội dung Quill Editor hoàn toàn chưa có test | **P1 — READY**<br>*(Pure In-Memory)* | **TARGET: 100% Line & Branch** của `plainTextContent` |
| `NoteModel`<br>(`note_model.dart`) | `Note.copyWith` | **`TC-WB-018`**, **`TC-WB-019`** | Cờ `clearReminder` (true $\rightarrow$ null, false $\rightarrow$ giữ/gán mới ở L228), cơ chế tự sinh `updatedAt ?? DateTime.now()` vs gán timestamp ngoài (L227) | **0.0%**<br>(L200–229 chưa hit) | 30 dòng lệnh tạo bản sao và cập nhật thời gian chưa có test | **P1 / P2 — READY**<br>*(Pure In-Memory)* | **TARGET: $\ge$ 85% Line** của phương thức `copyWith` |
| `NoteModel`<br>(`note_model.dart`) | `Note.fromMap` / `toMap` | Baseline Tests 10-18 + **`TC-WB-020`** | Round-trip SQLite, decode list CSV/JSON, fallback camelCase, **fallback mốc thời gian khi SQLite thiếu field (`created_at`, `updated_at`, `reminder` là `null`)** | **44.35% toàn class**<br>(55/124 lines đã đo) | Nhánh fallback `created_at == null` và `updated_at == null` chưa được kích hoạt; `toFirestoreMap`/`fromFirestoreMap` phụ thuộc `Timestamp` | **P2 — READY**<br>*(Pure In-Memory)* | **TARGET: $\ge$ 80% Line** trên `note_model.dart` *(Mục tiêu kỳ vọng, không phải kết quả đã đạt)* |
| `SyncRepository`<br>(`sync_repository.dart`) | Toán tử so sánh LWW `DateTime.isAfter` *(In-memory)* | **`TC-WB-021`** | Đánh giá toán tử `local.updatedAt.isAfter(cloud.updatedAt)` độc lập trong bộ nhớ: Local mới hơn, Cloud mới hơn, Trùng khớp (`BR-03` Open) | **0.0% trên file `sync_repository.dart`** *(Chưa đo)* | **Coverage Gap được chấp nhận:** `TC-WB-021` chỉ test toán tử `DateTime.isAfter` trong bộ nhớ, **không tính vào coverage của `sync_repository.dart`**. Pipeline Push/Pull thật phụ thuộc cứng `FirebaseFirestore.instance` & `LocalNoteService` | **P1 — READY**<br>*(In-Memory Logic Only)* | Bao phủ **100% 3 miền giá trị thời gian** trong bộ nhớ *(Không tính coverage file `sync_repository.dart`)* |
| `AuthProvider`<br>(`auth_provider.dart`) | `setError`, `_syncUserProfile`, `authStateChanges` | **`TC-WB-001`** .. **`TC-WB-005`** | Gán/xóa lỗi validation, dọn dẹp state đăng xuất, tạo hồ sơ mới vs nạp hồ sơ có sẵn | **Chưa đo** | **Giới hạn kỹ thuật:** `AuthProvider()` gọi cứng `FirebaseAuth.instance`; `_syncUserProfile` là **library-private (`_`)** và gọi cứng `FirebaseFirestore.instance` (chỉ kích hoạt gián tiếp qua public `reloadUserData()`/`signInWithEmail()`) | **P2 — DESIGN ONLY**<br>*(Blocked without Firebase Platform Mock / DI)* | Kiểm tra thiết kế State Contract *(Giữ `DESIGN ONLY` khi không sửa `lib/`)* |
| `CloudinaryService`<br>(`cloudinary_service.dart`) | `_extractPublicId` *(qua public `deleteFile`)*, `uploadImage` | **`TC-WB-006`** .. **`TC-WB-010`** | `_extractPublicId` là **library-private (`_`)**, phải gọi qua public `deleteFile(url)` (`TC-WB-006, 007` $\rightarrow$ `REQ-09 / FN-12` chính, `REQ-12 / FN-35, 36` phụ); `uploadImage` (`TC-WB-008..010` $\rightarrow$ `REQ-12 / FN-35, 36`) | **Chưa đo** | `TC-WB-006` (qua `deleteFile`) và `TC-WB-008` (qua `dotenv.testLoad`) chạy được trong bộ nhớ; `TC-WB-007, 009, 010` cần `HttpOverrides` & `File` tạm | **P2 / P3 — DESIGN ONLY**<br>*(`006, 008` khả thi; `007, 009, 010` cần HTTP mock)* | Kiểm tra Guard Clause & Boundary |
| `Security Rules`<br>(`firestore.rules`) | `isOwner`, `isValidNote` | **`TC-WB-011`** .. **`TC-WB-014`**<br>(`REQ-11 / NFR-03 / FN-40`) | Xác thực UID chính chủ, chặn truy cập vô danh, chặn truy cập chéo, kiểm tra thuộc tính sở hữu dữ liệu ghi (`NFR-03`) | **Đã có 8 tests PASS** trong `test/security_rules_test.dart` | **Giới hạn kỹ thuật:** Là kiểm thử mô phỏng logic bằng Dart (**Dart Rule Simulation**), **không phải** chạy trên **Firebase Emulator Rules Engine** | **P2 — EXECUTED (Simulation)** | 100% Rule Expression Condition Coverage (Simulation) |

---

## IV. PHẠM VI MỞ RỘNG TRỌNG TÂM: 8 TEST CASES THUẦN BỘ NHỚ (TC-WB-015 ĐẾN TC-WB-022)
*(Đồng bộ 100% với đặc tả kỹ thuật chi tiết và phân tích $V(G)$ tại [white_box_test_cases.md](../../test_cases/white_box/white_box_test_cases.md))*

Nhằm đảm bảo **100% khả thi khi viết mã kiểm thử mà không cần sửa `lib/`**, đợt mở rộng thực thi tập trung vào **8 ca kiểm thử Pure In-Memory (`TC-WB-015` đến `TC-WB-022`)**:

| Mã TC | Tên kịch bản | Module & Public API kiểm thử | Cấu trúc luồng & Nhánh logic thực tế được bao phủ | Input / Test Data (Đã kiểm chứng kích hoạt đủ nhánh) | Expected Output | Căn cứ REQ / FN | Ưu tiên & Trạng thái |
|:---:|:---|:---|:---|:---|:---|:---:|:---:|
| **TC-WB-015** | Đếm công việc chưa xong trong Checklist | `Note.pendingChecklistCount` (`note_model.dart` L33–42) | • Nhánh `!isChecklist` (L34)<br>• Fallback `items ?? []` (L37)<br>• Lọc `i['checked'] != true` (L38)<br>• Khối `catch (_)` (L39–41) | • Note A (text thô)<br>• Note B (3 items: 1 true, 2 false)<br>• Note C1 (item thiếu key `checked`), Note C2 (`{"type":"checklist"}` thiếu `items`)<br>• Note D (thiếu `type: checklist`)<br>• **Note E (`{"type":"checklist","items":"corrupted_not_a_list"}` kích hoạt `catch (_)`)** | • Note A, D = 0<br>• Note B = 2<br>• Note C1 = 1, Note C2 = 0<br>• **Note E = 0** (bắt `TypeError` tại `catch (_)`) | **REQ-06**<br>(FN-15) | **P1**<br>`READY (In-Memory)` |
| **TC-WB-016** | Trích xuất plain text từ Quill Delta JSON | `Note.plainTextContent` (`note_model.dart` L51–65) | • Vòng lặp duyệt Delta `List` (L56)<br>• `item is Map` (True/False) (L57)<br>• `containsKey('insert')` (True/False) (L57)<br>• `val is String` (True/False) (L59) | `jsonEncode([{"insert": "Kế hoạch tuần tới\n"}, {"insert": {"image": "url"}}, {"attributes": {"bold": true}}, "raw_non_map_item", {"insert": "Thực hiện kiểm thử hộp trắng"}])` | Chuỗi trích xuất: `"Kế hoạch tuần tới\nThực hiện kiểm thử hộp trắng"`. Embed Map, Map thiếu `'insert'` và phần tử không phải Map bị bỏ qua an toàn | **REQ-05** / **REQ-08**<br>(FN-09 / FN-23) | **P1**<br>`READY (In-Memory)` |
| **TC-WB-017** | Xử lý chuỗi rỗng, Checklist, text thô, JSON Map và JSON lỗi | `Note.plainTextContent` (`note_model.dart` L46–68) | • Nhánh `content.isEmpty` (L46)<br>• Nhánh `isChecklist` (L47–48)<br>• Nhánh `startsWith('[' &#124; '{')` T/F (L51)<br>• Nhánh `decoded is List` False (L54)<br>• Khối `catch (_)` (L66) | • P1: `""`<br>• P2: `"   Ghi chú thô   "`<br>• P3: `"[{malformed_json"`<br>• P4: `'{"custom_meta": "val"}'`<br>• P5: Checklist JSON (`"Mục 1"`, `checked: true`) | • P1 = `""`<br>• P2 = `"Ghi chú thô"`<br>• P3 = `"[{malformed_json"`<br>• P4 = `'{"custom_meta": "val"}'`<br>• P5 = `"☑ Mục 1"` | **REQ-05**<br>(FN-09) | **P1**<br>`READY (In-Memory)` |
| **TC-WB-018** | Cơ chế xóa nhắc nhở qua `clearReminder` | `Note.copyWith` (`note_model.dart` L228) | • Ternary: `clearReminder ? null : (reminder ?? this.reminder)`<br>• Cả 3 nhánh: hủy về `null`, giữ nguyên, gán mới | Note gốc có reminder `20/10/2026`.<br>• Lệnh 1: `clearReminder: true`<br>• Lệnh 2: đổi title<br>• Lệnh 3: truyền reminder mới | • Lệnh 1: `reminder == null`<br>• Lệnh 2: giữ ngày `20/10/2026`<br>• Lệnh 3: nhận ngày mới | **REQ-12**<br>(FN-38) | **P2**<br>`READY (In-Memory)` |
| **TC-WB-019** | Cập nhật mốc thời gian `updatedAt` | `Note.copyWith` (`note_model.dart` L227) | • `updatedAt: updatedAt ?? DateTime.now()`<br>• Nhánh tự sinh thời gian hiện tại<br>• Nhánh gán timestamp ngoài | Note gốc có ngày `01/10/2026`.<br>• Ca 1: copy không truyền `updatedAt`<br>• Ca 2: truyền `05/10/2026 14:00` | • Ca 1: nhận thời gian hiện tại ($\ge$ gốc)<br>• Ca 2: nhận chính xác ngày `05/10/2026 14:00` | **REQ-05** / **REQ-11**<br>(FN-09 / FN-41) | **P1**<br>`READY (In-Memory)` |
| **TC-WB-020** | Phòng thủ SQLite map thiếu field thời gian | `Note.fromMap` (`note_model.dart` L149–157) | • Fallback `created_at ?? now` (L150)<br>• Fallback `updated_at ?? now` (L153)<br>• Null check `reminder` (L155) | Map thiếu field: `{'id': 'legacy-note-99', 'title': 'Ghi chú di sản', 'content': 'Nội dung', 'created_at': null, 'updated_at': null, 'reminder': null}` | Đối tượng khởi tạo thành công không crash; `createdAt`, `updatedAt` nhận mốc hợp lệ; `reminder == null` | **REQ-04** / **NFR-01**<br>(FN-08) | **P2**<br>`READY (In-Memory)` |
| **TC-WB-021** | So sánh thứ tự ưu tiên LWW trong bộ nhớ | Toán tử `DateTime.isAfter` *(tham chiếu `sync_repository.dart` L67, L121)* | • `local.updatedAt.isAfter(cloud.updatedAt)`<br>• `cloud.updatedAt.isAfter(local.updatedAt)`<br>• Trùng khớp (`BR-03` Open) | • Cặp 1: Local 12:00:05, Cloud 12:00:00<br>• Cặp 2: Local 12:00:00, Cloud 12:00:05<br>• Cặp 3: Local 12:00:00, Cloud 12:00:00 | • Cặp 1: `local.isAfter` = `true`<br>• Cặp 2: `cloud.isAfter` = `true`<br>• Cặp 3: Cả hai đều `false` (`BR-03 NEEDS CONFIRMATION`; **không tính coverage `sync_repository.dart`**) | **REQ-11**<br>(FN-41) | **P1**<br>`READY (In-Memory)` |
| **TC-WB-022** | Chịu lỗi khi `ChecklistItem.fromJson` khuyết trường | `ChecklistItem.fromJson` (`checklist_item.dart` L21–25 & L13) | • Fallback sinh UUID tại constructor L13 khi `id` null (L22)<br>• Fallback `''` khi `text` null (L23)<br>• Fallback `false` khi `checked` null (L24) | JSON có các trường null: `{'id': null, 'text': null, 'checked': null}` | Khởi tạo thành công không crash; `id` là UUID không rỗng; `text == ''`; `checked == false` | **REQ-06**<br>(FN-15) | **P2**<br>`READY (In-Memory)` |

---

## V. KHUNG TIÊU CHUẨN THỰC THI & QUẢN LÝ CHẤT LƯỢNG (EXECUTION GOVERNANCE)

### 5.0. Phân biệt rõ các cấp độ bao phủ mã nguồn và kỹ thuật hỗ trợ DI / Mocking
Trong kiểm thử hộp trắng, đội ngũ QA phân biệt rành mạch 5 cấp độ bao phủ lý thuyết và phương pháp tiếp cận kiến trúc:
1. **Statement Coverage (Bao phủ dòng lệnh / LCOV Line Coverage):** Đo lường tỷ lệ các dòng lệnh thực thi đã được chạy ít nhất một lần. Đây là chỉ số đo lường cơ bản được trích xuất từ file `lcov.info`.
2. **Branch Coverage (Bao phủ nhánh rẽ):** Đảm bảo mọi nhánh rẽ nhị phân (mỗi ngả rẽ của `if-else`, toán tử `?:`, hoặc `switch-case`) đều được thực thi cả hướng `True` và `False`.
3. **Decision Coverage (Bao phủ điểm quyết định):** Đánh giá toàn bộ biểu thức boolean tại một điểm rẽ nhánh được đánh giá thành cả kết quả tổng thể `True` và `False`.
4. **Condition / Multiple Condition Coverage (Bao phủ điều kiện đơn & tổ hợp):** Kiểm tra từng mệnh đề boolean con độc lập trong biểu thức điều kiện phức hợp (ví dụ `A && B` hay `A || B`) nhận đủ các giá trị chân lý `True`/`False` để chứng minh tính đúng đắn của từng điều kiện.
5. **Path Coverage (Bao phủ đường đi độc lập qua CFG):** Đảm bảo mọi đường đi độc lập tuyến tính (tính theo Cyclomatic Complexity $V(G)$) từ điểm bắt đầu đến điểm kết thúc của hàm đều được thực thi.
6. **Kỹ thuật hỗ trợ Dependency Injection (DI) & Mocking:**
   - Khi một module phụ thuộc vào tài nguyên bên ngoài (Firebase, Mạng HTTP, File system, SQLite), kiến trúc chuẩn yêu cầu áp dụng **Dependency Injection (DI)** thông qua Constructor Injection để tiêm các `Mock` hoặc `Fake` interface (ví dụ `MockFirebaseAuth`, `MockClient`, `FakeLocalNoteService`).
   - Dưới **ràng buộc nghiêm ngặt không can thiệp sửa đổi mã nguồn `lib/`**, các lớp phụ thuộc cứng vào static singleton tĩnh (`FirebaseAuth.instance`, `FirebaseFirestore.instance`) không thể áp dụng Constructor DI $ightarrow$ Bắt buộc giữ trạng thái **`DESIGN ONLY`** (hoặc sử dụng kiểm thử mô phỏng logic `SIMULATION PASS`), tránh tạo mã test giả vờ hoặc bypass kiến trúc trái phép.

### 5.1. Tiêu chí đầu vào (Entry Criteria)
Lượt chạy kiểm thử hộp trắng chỉ được phép kích hoạt khi thỏa mãn đầy đủ các điều kiện sau:
1. **Tài liệu đặc tả đã đóng băng (Frozen Specs):** Tài liệu kế hoạch kiểm thử (`white_box_test_plan.md`) và đặc tả thiết kế 22 test cases (`white_box_test_cases.md`) đã hoàn tất rà soát khả thi kỹ thuật (Technical Feasibility Review) và được phê duyệt.
2. **Baseline nguyên vẹn (Intact Baseline):** 18/18 Unit Tests hiện hữu trong `test/` đang ở trạng thái PASS, có log đối chiếu tại `evidence/white_box/note_model_run_20261010_0945/`.
3. **Môi trường độc lập (Environment Isolation):** Toàn bộ 8 test case mở rộng trọng tâm (`TC-WB-015` .. `TC-WB-022`) chạy hoàn toàn trong bộ nhớ (Pure In-Memory) qua API `public` trên Dart VM / Flutter Test Framework, không yêu cầu sửa `lib/` và không có phụ thuộc chặn từ thiết bị thật hay Firebase thật.
4. **Giới hạn nghiệp vụ rõ ràng:** Các vấn đề chưa ngã ngũ (như quy tắc hòa `BR-03`) được cô lập thành ghi chú xác minh, không tạo giả định chủ quan.

### 5.2. Tiêu chí hoàn tất (Exit Criteria)
Đợt kiểm thử White-box được tuyên bố hoàn thành khi đạt được các tiêu chí:
1. **100% Test Cases In-Memory trọng tâm được thực thi:** Toàn bộ các ca thuộc nhóm P1 (`TC-WB-015`, `TC-WB-016`, `TC-WB-017`, `TC-WB-019`, `TC-WB-021`) và các ca P2 cùng model (`TC-WB-018`, `TC-WB-020`, `TC-WB-022`) được hiện thực mã test và chạy với kết quả trung thực.
2. **Có Log kiểm chứng đầy đủ:** Quá trình chạy sinh ra file log `test_execution.log` ghi lại toàn bộ tiến trình từ khi bắt đầu đến khi kết thúc.
3. **Độ bao phủ được đo lường thực tế & Quản trị chỉ số TARGET (Actual Measured Coverage vs Target):**
   - Chỉ số Line Coverage và Branch Coverage (nếu Flutter hỗ trợ flag `--branch-coverage`) được bóc tách trực tiếp từ file `coverage/lcov.info`.
   - **Mục tiêu kỳ vọng (TARGET): Line Coverage của `lib/models/note_model.dart` đạt $\ge 80\%$** (tăng từ baseline đã đo **44.35%**). *Lưu ý quản trị: Mục tiêu $\ge 80\%$ là chỉ số kỳ vọng định hướng (Target Benchmark), **không phải là kết quả đã đạt** và **không được biến thành điều kiện ép PASS hay rào cản chặn đóng đợt kiểm thử** nếu phát sinh giới hạn kỹ thuật khách quan (như các hàm `toFirestoreMap`/`fromFirestoreMap` phụ thuộc kiểu `Timestamp` của Cloud Firestore).*
4. **Không phát sinh lỗi hồi quy (Zero Regression):** 18 unit tests baseline ban đầu tiếp tục đạt PASS 100%.
5. **Ghi nhận khiếm khuyết trung thực:** Nếu có ca kiểm thử bị FAIL, nguyên nhân phải được phân tích và ghi nhận vào Defect Log. **Tuyệt đối không yêu cầu ép 100% PASS**.

### 5.3. Quy trình quản lý thay đổi khi phát hiện sai lệch (Change Management Process)
Trong quá trình thực thi, nếu phát hiện sự khác biệt giữa kết quả thực tế của ứng dụng và kết quả mong đợi trong tài liệu:
1. **Bước 1 - Ghi nhận trung thực (Log Incident):** Lưu giữ nguyên trạng terminal log, mã lỗi và stack trace. Không sửa code, không sửa test case ngay lập tức.
2. **Bước 2 - Phân tích nguyên nhân gốc (Root Cause Analysis):**
   - *Trường hợp A (Lỗi mã nguồn ứng dụng):* Mã nguồn `lib/` xử lý sai logic so với SRS đã chốt $\rightarrow$ Đánh dấu ca kiểm thử là **FAIL**, lập phiếu lỗi **Defect Log** chi tiết. **Tuyệt đối không sửa mã nguồn `lib/` để ép test PASS**.
   - *Trường hợp B (Sai lệch giả định thiết kế test case):* Do đặc thù kỹ thuật của ngôn ngữ (ví dụ: ép kiểu strictly-typed non-nullable của Dart ném `TypeError` thay vì fallback) $\rightarrow$ Đội ngũ QA đánh giá, ghi nhận nguyên nhân kỹ thuật và lập phiếu đề xuất cập nhật tài liệu kiểm thử kèm lý do minh bạch.
3. **Bước 3 - Nguyên tắc cấm ép PASS (Zero Forced Pass):**
   - **Nghiêm cấm sửa Expected Result** trong tài liệu chỉ nhằm mục đích làm cho kết quả hiển thị màu xanh (PASS).
   - **Nghiêm cấm sửa mã nguồn ứng dụng `lib/`** trong phạm vi nhiệm vụ của QA.

### 5.4. Các giới hạn và khoảng trống độ bao phủ được chấp nhận (Accepted Scope Limitations & Coverage Gaps)
1. **Giới hạn của `TC-WB-021` & Coverage Gap tại `sync_repository.dart`:**
   - Ca `TC-WB-021` chỉ kiểm tra toán tử so sánh mốc thời gian giữa 2 đối tượng `DateTime` trong bộ nhớ (`updatedAt.isAfter`). Ca này **KHÔNG được tính vào Line/Branch Coverage thực tế của file `lib/repositories/sync_repository.dart`**.
   - Việc kiểm thử trực tiếp pipeline mạng Push/Pull trong `SyncRepository.syncNotes()` là **khoảng trống độ bao phủ được chấp nhận (Accepted Coverage Gap)** trong phạm vi Selective White-box hiện tại do `SyncRepository` gắn chặt với `FirebaseFirestore.instance`, `FirebaseAuth.instance`, `LocalNoteService()` và `PendingDeleteService()` mà không có Dependency Injection. Hạng mục này có thể mở rộng ở giai đoạn sau nếu được phép refactor DI.
2. **Rủi ro nghiệp vụ `BR-03` tiếp tục giữ trạng thái `NEEDS CONFIRMATION`:** Khi hai bản ghi trùng khớp mốc `updatedAt` (`isAtSameMomentAs`), cả hai chiều Push và Pull đều trả về `false`. Đội ngũ QA không tự ý chọn Cloud thắng hay Local thắng; kịch bản test chỉ ghi nhận kết quả toán tử `isAfter == false` mà không ép PASS/FAIL đối với kết quả đồng bộ cuối cùng.
3. **Giới hạn truy cập hàm Library-Private & Static Singleton ở `TC-WB-001..010` khi không sửa `lib/`:**
   - `AuthProvider._syncUserProfile` (`TC-WB-004, 005`) và `CloudinaryService._extractPublicId` (`TC-WB-006, 007`) là hàm **library-private** (`_`) trong Dart, không thể gọi trực tiếp từ `test/`.
   - Với `CloudinaryService`: Có thể kích hoạt `_extractPublicId` thông qua phương thức **public** `deleteFile(fileUrl)` (`TC-WB-006` chạy thuần trong bộ nhớ và trả về `false`; `TC-WB-007` cần kèm `dotenv.testLoad` và `HttpOverrides`).
   - Với `AuthProvider` (`TC-WB-001..005`): Dù có các phương thức public như `setError()`, `reloadUserData()`, `signInWithEmail()`, `registerWithEmail()`, nhưng constructor `AuthProvider()` và thân hàm gọi trực tiếp `FirebaseAuth.instance` và `FirebaseFirestore.instance`. Do không sửa `lib/`, nhóm `TC-WB-001..005` được giữ nguyên ở mức **`DESIGN ONLY (Accepted Limitation)`**.
4. **Phân biệt rõ Simulation vs Emulator ở `TC-WB-011..014` (`test/security_rules_test.dart`):** 8 bài test Security Rules hiện có là kiểm thử mô phỏng biểu thức quy tắc bằng Dart trong bộ nhớ (**Dart Rule Simulation**), không đánh đồng với việc kiểm thử trên **Firebase Local Emulator Suite (Firestore Rules Engine)**.
5. **Phân định rõ trạng thái:** Các ca kiểm thử đang ở trạng thái `DESIGN ONLY` **tuyệt đối không được tính là đã PASS** trong bất kỳ báo cáo tổng kết nào cho đến khi được chạy thực tế có log kiểm chứng.

### 5.5. Đối chiếu mã nguồn thực tế (Implementation Audit Findings)
- **`TC-WB-015` (`pendingChecklistCount` trong `lib/models/note_model.dart` L33–42):**
  - Dòng 34 kiểm tra `if (!isChecklist) return 0;`. Vì `isChecklist` đã gọi `jsonDecode(content)` và kiểm tra `decoded is Map && decoded['type'] == 'checklist'`, mọi chuỗi JSON sai cú pháp sẽ bị chặn ngay tại dòng 34 chứ không vào tới `catch (_)` của `pendingChecklistCount`.
  - Để thực sự kích hoạt nhánh `catch (_) { return 0; }` (L39–41), dữ liệu test phải là JSON hợp lệ có `"type": "checklist"` nhưng trường `"items"` mang kiểu khác `List?` (ví dụ `"items": "corrupted_not_a_list"`, gây `TypeError` tại phép ép kiểu `decoded['items'] as List?` ở dòng 37). Đã bổ sung `Note E` vào `TC-WB-015` để bao phủ 100% nhánh thực tế.
- **`TC-WB-016` & `TC-WB-017` (`plainTextContent` trong `lib/models/note_model.dart` L45–69):**
  - Dòng 57 kiểm tra `if (item is Map && item.containsKey('insert'))`. Đã bổ sung vào mảng Delta của `TC-WB-016` cả phần tử Map thiếu key `'insert'` (`{"attributes": {"bold": true}}`) và phần tử không phải Map (`"raw_non_map_item"`), đồng thời bổ sung vào `TC-WB-017` trường hợp JSON Map không phải List (`'{"custom_meta": "val"}'`) và ghi chú Checklist (`isChecklist == true`) để bao phủ toàn bộ các nhánh rẽ.
- **`TC-WB-020` (`Note.fromMap` trong `lib/models/note_model.dart` L137–158):** Constructor của `Note` yêu cầu các trường `id`, `title`, `content` là non-nullable `String`. Dữ liệu test chỉ để `null` các trường có toán tử fallback an toàn (`created_at`, `updated_at`, `reminder`).
- **`TC-WB-022` (`ChecklistItem.fromJson` trong `lib/models/checklist_item.dart` L21–25 & L13):** Dòng 22 truyền `id: json['id'] as String?` vào constructor `ChecklistItem` (dòng 13 thực hiện `id = id ?? const Uuid().v4()`). Phương thức dùng ép kiểu `json['checked'] as bool? ?? false`; khi `checked` là `null` thì fallback về `false` an toàn.

---

## VI. KẾT LUẬN TÍNH KHẢ THI KỸ THUẬT (FINAL TECHNICAL FEASIBILITY CONCLUSION)

Toàn bộ 22 test cases trong `white_box_test_cases.md` và kế hoạch trong `white_box_test_plan.md` đã hoàn tất rà soát khả thi kỹ thuật (Technical Feasibility Review) và đối chiếu từng dòng lệnh với `lib/`:

> [!IMPORTANT]
> **KẾT LUẬN TRẠNG THÁI: `READY FOR TEST AUTHORING (SELECTIVE IN-MEMORY SCOPE: TC-WB-015..022 & PUBLIC GUARD CLAUSES TC-WB-006, 008)`**
> - **Sẵn sàng viết và chạy Unit Test ngay (Không sửa `lib/`):** **8 ca trọng tâm `TC-WB-015` đến `TC-WB-022`** (trên `note_model.dart`, `checklist_item.dart` và phép so sánh LWW `DateTime.isAfter`) cùng **2 ca guard clause `TC-WB-006`, `TC-WB-008`** (gọi qua phương thức public `deleteFile` và `uploadImage`).
> - **Đã thực thi mô phỏng logic (`Simulation PASS`):** **4 ca `TC-WB-011` đến `TC-WB-014`** (8 bài test mô phỏng quy tắc trong `test/security_rules_test.dart`).
> - **Giữ trạng thái `DESIGN ONLY` do giới hạn kiến trúc được chấp nhận (Không sửa `lib/`):** **`TC-WB-001..005`** (`AuthProvider` phụ thuộc cứng `FirebaseAuth.instance` / `FirebaseFirestore.instance` & hàm private `_syncUserProfile`) và **`TC-WB-007, 009, 010`** (`CloudinaryService` cần `HttpOverrides` & file tạm).
> - Tuân thủ nghiêm ngặt ràng buộc: Không sửa `lib/`, không viết hoặc chạy test khi chưa có lệnh triển khai, bảo toàn nguyên vẹn toàn bộ evidence hiện hữu.
