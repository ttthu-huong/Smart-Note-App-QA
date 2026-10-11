# NHẬT KÝ QUẢN LÝ LỖI (DEFECT LOG & BUG TRACKING REPORT)
## Dự án: Smart Note App
**Mục tiêu:** Ghi nhận, phân loại, truy vết và phân tích nguyên nhân gốc (Root Cause Analysis - RCA) cho các lỗi phần mềm phát hiện được trong quá trình kiểm thử thủ công và tự động  
**Tiêu chuẩn áp dụng:** IEEE 829 Defect Reporting & ISTQB Defect Lifecycle  
**Quy tắc:** Ghi nhận lỗi và đưa vào Backlog Retest sau khi Dev Team cung cấp bản build sửa lỗi; QA Tester không tự ý chỉnh sửa mã nguồn ứng dụng (`lib/`).

---

## 1. THỐNG KÊ TỔNG QUAN DEFECTS

| Mã Lỗi (Bug ID) | Tóm tắt lỗi (Summary) | Nhóm chức năng | Mức độ nghiêm trọng (Severity) | Trạng thái (Status) | Ngày phát hiện |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **BUG-001** | Tiến trình đính kèm / tải lên hình ảnh bị treo vô hạn (Infinite Hang) trong Editor Screen khi đính kèm ảnh từ thư viện | FN-23 / FN-08 / Cloudinary Service | **HIGH** | **OPEN (Backlog Retest)** | 09/10/2026 |
| **BUG-002** | Xóa ghi chú offline trên Thiết bị A không đồng bộ xóa trên Thiết bị B (Note bị xóa trên Firebase Cloud nhưng tồn tại vĩnh viễn trên Thiết bị B do thiếu tombstone) | FN-40 / Offline Sync / Database Sync | **CRITICAL** | **OPEN (Backlog Retest)** | 10/10/2026 |
| **BUG-003** | Màn hình Trang chủ (HomeScreen) không hỗ trợ tính năng Kéo để làm mới (Pull-to-refresh) để chủ động đồng bộ dữ liệu | FN-40 / UI Interaction / HomeScreen | **MEDIUM** | **OPEN (Backlog Retest)** | 10/10/2026 |
| **BUG-004** | Bộ lọc loại ghi chú "Danh sách" (`has:list`) trên UI Tìm kiếm không được xử lý trong service tìm kiếm (trả về rỗng do LIKE SQL thô) | FN-24 / Search Service | **MEDIUM** | **OPEN (Backlog Retest)** | 11/10/2026 |
| **BUG-005** | Hiện tượng giật / vệt tràn viền thoáng qua (Transient Layout Overflow Glitch) trên thẻ ghi chú khi thoát Editor về Trang chủ sau khi xóa trắng tiêu đề hoặc nội dung | FN-08 / FN-09 / UI Layout | **MINOR** | **OPEN (Backlog Retest)** | 11/10/2026 |

*Ghi chú mã lỗi:* Đã kiểm tra tính duy nhất của mã lỗi (`BUG-001` đến `BUG-005`), đảm bảo không trùng lặp mã lỗi với bất kỳ defect nào trong toàn bộ hệ thống tài liệu QA.

---

## 2. BÁO CÁO CHI TIẾT DEFECT BUG-001

### 2.1. Thông tin chung
* **Bug ID:** `BUG-001`
* **Tiêu đề lỗi:** Ứng dụng bị treo ở trạng thái đính kèm hình ảnh (Uploading progress indicator hiển thị mãi không dừng) khi chọn đính kèm ảnh từ Photo Picker trong màn hình Editor.
* **Thành phần bị ảnh hưởng:** `lib/screens/editor_screen.dart`, `lib/services/cloudinary_service.dart`.
* **Trạng thái:** **OPEN (Backlog Retest sau khi Dev Team sửa lỗi)**.
* **Mức độ ưu tiên / Nghiêm trọng:** High / Major (Làm gián đoạn kịch bản kiểm thử FN-23 Item 09 - `TC-BB-027B-D01` và luồng đính kèm media).

### 2.2. Điều kiện trước khi tái hiện (Preconditions)
1. Điện thoại Samsung Galaxy S21 FE 5G đã cài ứng dụng Smart Note App build `v1.0.0+1`.
2. Ứng dụng đã đăng nhập tài khoản Tester.
3. Trong thư viện ảnh thiết bị (Gallery / Photo Picker) có ít nhất 1 file ảnh (định dạng JPG/PNG).

### 2.3. Các bước tái hiện (Steps to Reproduce)
1. Mở ứng dụng Smart Note App, chạm vào nút FAB (`+`) để tạo ghi chú mới (hoặc mở ghi chú có sẵn trong Editor Screen).
2. Chạm vào biểu tượng **"Thêm hình ảnh"** (hoặc dấu `+` trên thanh công cụ Editor).
3. Chọn mục **"Chọn từ thư viện"** (Gallery).
4. Chọn 1 bức ảnh bất kỳ từ Android Photo Picker và bấm nút **"Xong"**.
5. Quan sát màn hình Editor.

### 2.4. Kết quả kỳ vọng vs Kết quả thực tế
* **Kết quả kỳ vọng (Expected Result):** Ảnh được tải lên Cloudinary thành công trong vòng vài giây; thanh tiến trình đóng lại; URL ảnh được chèn vào ghi chú và ghi chú tự động lưu thành công.
* **Kết quả thực tế (Actual Result):** Biểu tượng / Vòng tròn xoay tải lên (Progress Indicator) xuất hiện trên màn hình Editor và **treo liên tục quá 2 phút** mà không phản hồi; không trả về thông báo lỗi hay timeout.

### 2.5. Bằng chứng thực tế (Evidence & Trace Telemetry)
* **File Screenshot bằng chứng:**
  - `artemis/editor_uploading_2s.png`
  - `artemis/editor_uploading_5s.png`
  - `artemis/editor_uploading_after_2min.png`
* **File Logcat ghi nhận thực tế:** `artemis/upload_realtime_logcat.txt` và `artemis/reproduce_logcat.txt`.
* **Trích đoạn Logcat liên quan:**
```text
10-09 23:14:02.120 10245 10289 I flutter : 🔍 [Cloudinary] cloudName="dXXXXX" preset="smart_note_preset"
10-09 23:14:02.122 10245 10289 I flutter : 🔍 [Cloudinary] uploadImage URL: https://api.cloudinary.com/v1_1/dXXXXX/image/upload
10-09 23:14:02.150 10245 10312 D TransportRuntime.SQLiteEventStore: Storing event...
[VẪN DỪNG LẠI TẠI ĐÂY - KHÔNG CÓ CÁC LOG RESPONSE HTTP STATUS 200 HOẶC HTTP ERROR]
```

### 2.6. Phân tích nguyên nhân (Xác minh vs Giả thuyết)
* **Nguyên nhân đã xác minh trên thực tế (Verified Behavior):** Quá trình upload qua HTTP request không bao giờ kết thúc hay ném ngoại lệ; vòng xoay tiến trình trên UI giữ nguyên cờ `_isUploading = true` vĩnh viễn, người dùng bị khóa tương tác trên thanh công cụ.
* **Giả thuyết phân tích nguyên nhân gốc tầng mã nguồn (RCA Hypothesis):**
  - Trong `lib/services/cloudinary_service.dart` (dòng 108–148), lệnh `request.send()` và `response.stream.bytesToString()` dùng thư viện `http` mặc định nhưng không cấu hình timeout (`.timeout(Duration(seconds: 30))`). Khi gặp trễ mạng hoặc nghẽn luồng multipart, luồng không tự ngắt dẫn đến Future không bao giờ resolve.

---

## 3. BÁO CÁO CHI TIẾT DEFECT BUG-002

### 3.1. Thông tin chung
* **Bug ID:** `BUG-002`
* **Tiêu đề lỗi:** Xóa ghi chú ngoại tuyến trên Thiết bị A không đồng bộ xóa sang Thiết bị B (Ghi chú bị xóa trên Cloud nhưng tồn đọng vĩnh viễn trên client khác do thiếu Tombstone).
* **Thành phần bị ảnh hưởng:** `lib/services/sync_service.dart`, `lib/services/database_helper.dart`.
* **Kịch bản kiểm thử:** `TC-BB-030C-D01` (FN-40 Run 2).
* **Trạng thái:** **OPEN (Backlog Retest sau khi Dev Team sửa lỗi)**.
* **Mức độ ưu tiên / Nghiêm trọng:** Critical / Severity 1 (Dẫn đến mất tính nhất quán dữ liệu nghiêm trọng - Inconsistent State giữa các thiết bị của cùng một người dùng).

### 3.2. Điều kiện trước khi tái hiện (Preconditions)
1. Thiết bị A (Samsung S21 FE) và Thiết bị B (Samsung S24 FE) đều đăng nhập cùng tài khoản `student_qa@gmail.com`.
2. Có 1 ghi chú `FN40_Ghi_chu_tam_xoa` (id: `7428f831...`) đã đồng bộ thành công trên cả 2 thiết bị.

### 3.3. Các bước tái hiện (Steps to Reproduce)
1. Trên Thiết bị A, ngắt kết nối mạng (Tắt Wi-Fi qua `svc wifi disable`).
2. Trên Thiết bị A, xóa ghi chú `FN40_Ghi_chu_tam_xoa` vào Thùng rác, sau đó vào Thùng rác nhấn "Xóa vĩnh viễn".
3. Thiết bị A xóa sạch ghi chú khỏi SQLite local (`smart_note.db`).
4. Bật lại Wi-Fi trên Thiết bị A để kích hoạt đồng bộ.
5. Quan sát Firebase Cloud và Thiết bị B.

### 3.4. Kết quả kỳ vọng vs Kết quả thực tế
* **Kết quả kỳ vọng (Expected Result):** Sau khi Thiết bị A kết nối mạng trở lại, lệnh xóa được đồng bộ lên Firebase Cloud và đồng thời truyền tín hiệu đồng bộ xóa xuống Thiết bị B; ghi chú biến mất hoàn toàn trên cả 2 thiết bị.
* **Kết quả thực tế (Actual Result):** 
  - Ghi chú bị xóa hoàn toàn khỏi Firebase Firestore Cloud.
  - Nhưng trên Thiết bị B, ghi chú **vẫn tồn tại nguyên vẹn** trong danh sách Trang chủ (`status=normal`) và trong SQLite local `smart_note.db` (`id=7428f831... | is_synced=1`). Thiết bị B không nhận được tín hiệu xóa cục bộ.

### 3.5. Bằng chứng thực tế (Evidence)
* **Ảnh chụp màn hình:**
  - `03_tc_bb_030c_d01_dev_a_initial.png` & `03_tc_bb_030c_d01_dev_b_initial.png`
  - `03_tc_bb_030c_d01_dev_a_deleted_perm.png`
  - `03_tc_bb_030c_d01_dev_b_defect_still_exists.png`
* **Dữ liệu SQLite sau khi sync hoàn tất:**
  - `tools/dev_a.db`: Đã xóa sạch bản ghi `7428f831...`.
  - `tools/dev_b.db`: Vẫn tồn tại record `id=7428f831... | title=FN40_Ghi_chu_tam_xoa... | status=normal | is_synced=1`.

### 3.6. Phân tích nguyên nhân (Xác minh vs Giả thuyết)
* **Nguyên nhân đã xác minh trên thực tế (Verified Behavior):** Cơ sở dữ liệu SQLite local trên Thiết bị B giữ nguyên bản ghi với cờ `is_synced = 1`. Quá trình nạp đồng bộ (pull sync) từ Firestore về Thiết bị B chỉ lấy danh sách tài liệu hiện có trên Cloud về cập nhật/chèn mới, không hề xóa các bản ghi local khi tài liệu tương ứng bị xóa trên Cloud.
* **Giả thuyết phân tích nguyên nhân gốc tầng mã nguồn (RCA Hypothesis):**
  - Kiến trúc đồng bộ của ứng dụng hiện tại xóa cứng (hard delete) document trên Firestore mà không áp dụng cơ chế Tombstone (`is_deleted = true`, `deleted_at = timestamp`).
  - Trong logic hàm `syncPull()` của `sync_service.dart`, client chỉ xử lý các documents trả về trong collection snapshot mà không thực hiện phép trừ tập hợp (`local_ids - remote_ids`) để phát hiện và xóa các bản ghi mồ côi (orphan records).

---

## 4. BÁO CÁO CHI TIẾT DEFECT BUG-003

### 4.1. Thông tin chung
* **Bug ID:** `BUG-003`
* **Tiêu đề lỗi:** Màn hình Trang chủ (HomeScreen) không hỗ trợ tính năng Kéo để làm mới (Pull-to-refresh) để chủ động đồng bộ dữ liệu mới nhất.
* **Thành phần bị ảnh hưởng:** `lib/screens/home_screen.dart`.
* **Kịch bản kiểm thử:** `TC-BB-030F-D01` (FN-40 Run 2).
* **Trạng thái:** **OPEN (Backlog Retest sau khi Dev Team sửa lỗi)**.
* **Mức độ ưu tiên / Nghiêm trọng:** Medium / Severity 3.

### 4.2. Các bước tái hiện (Steps to Reproduce)
1. Đăng nhập ứng dụng trên Thiết bị B, đang đứng tại màn hình Trang chủ (HomeScreen).
2. Thiết bị A tạo một ghi chú mới `FN40_Nhiem_vu_dot_xuat` và đồng bộ lên đám mây thành công.
3. Trên Thiết bị B, dùng ngón tay vuốt kéo từ trên xuống dưới (Pull-to-refresh gesture).
4. Quan sát phản hồi giao diện.

### 4.3. Kết quả kỳ vọng vs Kết quả thực tế
* **Kết quả kỳ vọng (Expected Result):** Biểu tượng RefreshIndicator xuất hiện xoay tròn ở đầu màn hình, kích hoạt phương thức kéo dữ liệu đồng bộ `syncPull()` và cập nhật danh sách hiển thị ghi chú mới.
* **Kết quả thực tế (Actual Result):** Không có hiệu ứng cuộn kéo làm mới, không hiển thị vòng tròn tải, không có phản hồi kích hoạt đồng bộ.

### 4.4. Phân tích nguyên nhân (Xác minh vs Giả thuyết)
* **Nguyên nhân đã xác minh trên thực tế (Verified Behavior):** Thao tác vuốt xuống trên HomeScreen không kích hoạt bất kỳ sự kiện tải lại nào trên giao diện cũng như không gửi request đồng bộ nào đến máy chủ.
* **Giả thuyết phân tích nguyên nhân gốc tầng mã nguồn (RCA Hypothesis):**
  - Trong `lib/screens/home_screen.dart`, widget hiển thị danh sách ghi chú (ListView/GridView) không được bọc bằng widget `RefreshIndicator(onRefresh: () async { ... })`.

---

## 5. BÁO CÁO CHI TIẾT DEFECT BUG-004

### 5.1. Thông tin chung
* **Bug ID:** `BUG-004`
* **Tiêu đề lỗi:** Bộ lọc loại ghi chú "Danh sách" (`has:list`) trên UI Tìm kiếm không được xử lý trong service tìm kiếm, dẫn đến tìm kiếm chuỗi thô `LIKE '%has:list%'` và trả về danh sách rỗng (Empty State).
* **Thành phần bị ảnh hưởng:** `lib/screens/search_screen.dart`, `lib/services/local_note_service.dart`.
* **Kịch bản kiểm thử:** `TC-BB-027C-D01` (FN-24 / Tìm kiếm bộ lọc loại ghi chú).
* **Trạng thái:** **OPEN (Backlog Retest sau khi Dev Team sửa lỗi)**.
* **Mức độ ưu tiên / Nghiêm trọng:** Medium / Severity 3 (Tính năng tìm kiếm bộ lọc nhanh không trả về kết quả đúng).

### 5.2. Điều kiện trước khi tái hiện (Preconditions)
1. Cơ sở dữ liệu SQLite trên thiết bị có ít nhất 1 ghi chú định dạng Checklist (loại `checklist` hoặc có các mục checklist).
2. Ứng dụng đang mở tại màn hình Tìm kiếm (`SearchScreen`).

### 5.3. Các bước tái hiện (Steps to Reproduce)
1. Tại màn hình Tìm kiếm, chạm vào chip gợi ý bộ lọc **"Danh sách"** (hoặc gõ token `has:list` vào thanh tìm kiếm).
2. Hệ thống tự động thực hiện truy vấn tìm kiếm với từ khóa `has:list`.
3. Quan sát kết quả hiển thị trên màn hình.

### 5.4. Kết quả kỳ vọng vs Kết quả thực tế
* **Kết quả kỳ vọng (Expected Result):** Hệ thống lọc và hiển thị danh sách tất cả các ghi chú có định dạng checklist (`type == 'checklist'`).
* **Kết quả thực tế (Actual Result):** Màn hình hiển thị "Không tìm thấy ghi chú nào" (Empty State), mặc dù trong cơ sở dữ liệu có ghi chú checklist hợp lệ.

### 5.5. Bằng chứng thực tế (Evidence)
* **Ảnh chụp màn hình:** `evidence/fn13_14_21_22_run_20261011_0055/srch02_list_filter.png`
* **UI hierarchy XML:** `evidence/fn13_14_21_22_run_20261011_0055/ui_srch02.xml`

### 5.6. Phân tích nguyên nhân (Xác minh vs Giả thuyết)
* **Nguyên nhân đã xác minh trên thực tế (Verified Behavior):** UI `SearchScreen` gán chuỗi `has:list` vào ô tìm kiếm, nhưng truy vấn trả về rỗng vì không có ghi chú nào chứa xâu văn bản `"has:list"` trong tiêu đề hoặc nội dung.
* **Giả thuyết phân tích nguyên nhân gốc tầng mã nguồn (RCA Hypothesis):**
  - Trong `lib/services/local_note_service.dart` (phương thức `searchNotes`), câu lệnh SQL truy vấn trực tiếp dạng:
    `WHERE (title LIKE '%query%' OR content LIKE '%query%')`
  - Hàm tìm kiếm chưa xây dựng bộ tiền xử lý (Tokenizer / Query Parser) để bóc tách các tiền tố/token chức năng (`has:list`, `has:image`, `has:audio`) thành các điều kiện lọc cột chuyên biệt (như `type = 'checklist'` hoặc `audio_path IS NOT NULL`).

---

## 6. BÁO CÁO CHI TIẾT DEFECT BUG-005

### 6.1. Thông tin chung
* **Bug ID:** `BUG-005`
* **Tiêu đề lỗi:** Hiện tượng giật / tràn viền thoáng qua (Transient Layout Overflow Glitch / RenderFlex overflow warning) trên thẻ ghi chú khi thoát màn hình Editor về Trang chủ sau khi xóa trắng tiêu đề hoặc xóa trắng nội dung.
* **Thành phần bị ảnh hưởng:** `lib/screens/home_screen.dart`, `lib/widgets/note_card.dart`.
* **Kịch bản kiểm thử:** `FN-08 / FN-09` (Soạn thảo và cập nhật thẻ ghi chú).
* **Trạng thái:** **OPEN (Backlog Retest)**.
* **Mức độ ưu tiên / Nghiêm trọng:** Minor / Severity 4 (Lỗi giao diện chớp nhoáng ~0.3-0.5s trong quá trình transition/rebuild layout, không gây mất dữ liệu hay crash ứng dụng).

### 6.2. Điều kiện trước khi tái hiện (Preconditions)
1. Tại Trang chủ có 1 ghi chú tồn tại với đầy đủ cả tiêu đề (title) và nội dung (content).
2. Chạm mở ghi chú vào màn hình Editor.

### 6.3. Các bước tái hiện (Steps to Reproduce)
* **Trường hợp 1 (TH1 - Xóa tiêu đề):** Xóa toàn bộ văn bản trong ô Tiêu đề (để trống tiêu đề), giữ nguyên nội dung. Nhấn nút Back (<-) quay lại Trang chủ. Quan sát thẻ ghi chú trong quá trình chuyển cảnh.
* **Trường hợp 2 (TH2 - Xóa nội dung):** Giữ nguyên tiêu đề, xóa toàn bộ văn bản trong ô Nội dung (để trống nội dung). Nhấn nút Back (<-) quay lại Trang chủ. Quan sát thẻ ghi chú trong quá trình chuyển cảnh.
*(Lưu ý: Trường hợp 3 - Xóa trắng cả 2 trường không xảy ra hiện tượng này).*

### 6.4. Kết quả kỳ vọng vs Kết quả thực tế
* **Kết quả kỳ vọng (Expected Result):** Thẻ ghi chú trên Trang chủ co giãn kích thước mượt mà, không xuất hiện vệt cảnh báo tràn viền hay nhấp nháy layout.
* **Kết quả thực tế (Actual Result):** Xuất hiện vệt sọc vàng đen cảnh báo tràn viền (RenderFlex overflow warning) chớp nhoáng trên thẻ ghi chú trong khoảng 300ms rồi biến mất khi layout hoàn tất tính toán lại kích thước.

### 6.5. Bằng chứng thực tế (Evidence)
* **Video ghi lại chuyển động thực tế (Screen Recording):**
  - TH1: `evidence/fn13_14_21_22_run_20261011_0055/overflow_th1.mp4`
  - TH2: `evidence/fn13_14_21_22_run_20261011_0055/overflow_th2.mp4`
* **Logcat ghi nhận:** `evidence/fn13_14_21_22_run_20261011_0055/overflow_th1.log`, `overflow_th2.log`.

### 6.6. Phân tích nguyên nhân (Xác minh vs Giả thuyết)
* **Nguyên nhân đã xác minh trên thực tế (Verified Behavior):** Vệt tràn viền chỉ xuất hiện trong khoảnh khắc transition giữa EditorScreen và HomeScreen khi kích thước NoteCard đang thay đổi từ trạng thái có text sang không có text.
* **Giả thuyết phân tích nguyên nhân gốc tầng mã nguồn (RCA Hypothesis):**
  - Trong `NoteCard`, widget `Column` chứa tiêu đề và nội dung có thể chưa được bọc bằng `Flexible` hoặc `mainAxisSize: MainAxisSize.min` một cách chặt chẽ, dẫn đến khi Flutter thực hiện animation chuyển cảnh (Hero animation / pop transition), constraint chiều cao tạm thời của card tính toán trễ 1 frame so với nội dung bên trong.

