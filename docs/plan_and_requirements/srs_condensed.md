# ĐẶC TẢ YÊU CẦU PHẦN MỀM RÚT GỌN PHỤC VỤ KIỂM THỬ (CONDENSED SRS)
## Dự án: Smart Note App (Offline-First Mobile Application)
* **Mã dự án QA:** `Smart-Note-App-QA`
* **Phiên bản tài liệu:** `v1.0 (Condensed Baseline for QA)`
* **Ngày phê duyệt tài liệu:** 11/10/2026
* **Cơ sở xây dựng:** Đối chiếu chéo giữa Hồ sơ thiết kế, Báo cáo kiểm thử học phần ([Testing_Report.md](../test_report/Testing_Report.md)), Mã nguồn thực tế ([`lib/`](../../lib)) và Bằng chứng thực nghiệm đã lưu trữ.

---

## 1. MỤC ĐÍCH VÀ PHẠM VI TÀI LIỆU

### 1.1. Mục đích
Tài liệu này chuẩn hóa và tinh gọn các yêu cầu nghiệp vụ và kỹ thuật cốt lõi của ứng dụng Smart Note App, đóng vai trò làm chuẩn quy chiếu (Requirement Baseline) phục vụ thiết kế kịch bản kiểm thử, kiểm thử hộp trắng, kiểm thử tự động và đánh giá chất lượng phần mềm trong môn học Kiểm thử phần mềm.

### 1.2. Phạm vi tài liệu
* **Tập trung:** Các luồng nghiệp vụ cốt lõi đã được xác minh qua mã nguồn và đã có ca kiểm thử thực tế (Xác thực, Vòng đời ghi chú, Checklist, Tìm kiếm & Bộ lọc, Thùng rác & Lưu trữ, Sinh trắc học, Đồng bộ Offline-First đa thiết bị LWW).
* **Phân định rõ ranh giới:** Phân biệt rõ giữa hành vi thực tế đã đối chiếu trong mã nguồn (As-built) với các yêu cầu nghiệp vụ chính thức (SRS), đồng thời cô lập các quy tắc nghiệp vụ chưa được xác nhận để chờ quyết định chính thức từ Product Owner / Giảng viên.

---

## 2. TỔNG QUAN HỆ THỐNG VÀ CÁC DỊCH VỤ LIÊN QUAN

### 2.1. Kiến trúc hệ thống
* **Nền tảng:** Flutter SDK (Dart 3.x), triển khai cho Android 14.
* **Mô hình kiến trúc:** Clean Architecture 4 lớp:
  `UI Layer (screens, widgets)` $\rightarrow$ `State/Provider Layer (providers)` $\rightarrow$ `Repository Layer (repositories)` $\rightarrow$ `Service/Storage Layer (services, sqlite, cloud)`.
* **Mô hình dữ liệu:** **Offline-First**. Ứng dụng luôn đọc/ghi dữ liệu tức thời vào cơ sở dữ liệu SQLite cục bộ trên máy, sau đó tiến trình nền (Background Sync) tự động đồng bộ hai chiều với máy chủ đám mây khi có kết nối Internet.

### 2.2. Các dịch vụ phụ thuộc (External Services & Infrastructure)
1. **Local Database (SQLite - `sqflite`):** Lưu trữ cục bộ toàn bộ danh mục ghi chú, checklist, nhãn dán, cờ đồng bộ `is_synced` và hàng đợi xóa ngoại tuyến.
2. **Cloud Database (Firebase Firestore):** Lưu trữ đám mây tại đường dẫn phân quyền `/users/{userId}/notes/{noteId}` và `/users/{userId}/tags/{tagId}`.
3. **Authentication (Firebase Auth):** Quản lý phiên làm việc qua Email/Password và Google Sign-in OAuth.
4. **Media Storage (Cloudinary API):** Tải lên và lưu trữ hình ảnh đính kèm (sử dụng Upload Preset và API key từ `.env`).
5. **Trí tuệ nhân tạo (Firebase AI SDK / Gemini AI):** Tích hợp mô hình `gemini-2.5-flash-lite` phục vụ tóm tắt nội dung, đề xuất tiêu đề và tạo checklist.
6. **Bảo mật thiết bị (Android Biometrics - `local_auth`):** Tương tác phần cứng cảm biến vân tay/FaceID trên Android.
7. **Thông báo cục bộ (`flutter_local_notifications`):** Lập lịch thông báo nhắc nhở ghi chú theo múi giờ địa phương (`timezone`).

---

## 3. DANH SÁCH YÊU CẦU CHỨC NĂNG (FUNCTIONAL REQUIREMENTS)

> [!NOTE]
> **Nguyên tắc phân biệt Trạng thái đặc tả yêu cầu và Trạng thái thực thi kiểm thử:**
> - **Trạng thái đặc tả yêu cầu (SRS Specification Status):** Phản ánh việc yêu cầu nghiệp vụ đã được xác nhận trong Baseline SRS và đối chiếu với mã nguồn `lib/` hay còn quy tắc biên chờ Product Owner / Giảng viên quyết định (như `BR-03`).
> - **Trạng thái thực thi kiểm thử (Test Execution Status):** Phản ánh kết quả chạy kiểm thử thực tế trên thiết bị (`PASS`, `FAIL` kèm mã lỗi, `CHƯA ĐỦ CĂN CỨ`, `BLOCKED`, `DESIGN ONLY / NOT RUN`). Một yêu cầu đã hoàn tất đặc tả vẫn có thể có ca kiểm thử `FAIL` (do khiếm khuyết phần mềm như `BUG-004`) hoặc `BLOCKED` (do rào cản môi trường/an toàn như `REQ-13`, `TC-BB-015G-D01`).

| Mã REQ | Tên yêu cầu nghiệp vụ | Mô tả yêu cầu kỹ thuật & Nghiệp vụ | Tệp nguồn xác minh (Source) | Trạng thái đặc tả yêu cầu (SRS Status) | Trạng thái thực thi kiểm thử (Execution Summary) |
|:---:|:---|:---|:---|:---:|:---|
| **REQ-01** | Đăng ký tài khoản Email/Password | Form đăng ký yêu cầu Email hợp lệ (kiểm tra cú pháp `@`, domain, chặn disposable domain rác), mật khẩu tối thiểu 6 ký tự. Tự động cắt khoảng trắng đầu/cuối. Khi đăng ký thành công, gửi email kích hoạt và chuyển sang màn hình Xác thực email. | `lib/screens/login_screen.dart`<br>`lib/providers/auth_provider.dart` | **Đã xác nhận đặc tả** | **18 PASS / 1 FAIL** (`BUG-FN02-01`) |
| **REQ-02** | Đăng nhập hệ thống | Hỗ trợ 2 phương thức: Email/Password và Google OAuth. Kiểm tra tính hợp lệ của form, không phân biệt hoa/thường với email. Nhận diện tài khoản chưa verify email để chuyển hướng đến màn hình kích hoạt. Ánh xạ lỗi Firebase thành thông báo tiếng Việt thân thiện. | `lib/screens/login_screen.dart`<br>`lib/providers/auth_provider.dart` | **Đã xác nhận đặc tả** | **22 PASS / 2 FAIL** (`BUG-BB-002`, `BUG-BB-003`) |
| **REQ-03** | Quên & Đặt lại mật khẩu | Cho phép người dùng nhập email tại hộp thoại "Quên mật khẩu?" trên form đăng nhập; gửi email chứa liên kết đặt lại mật khẩu thông qua Firebase Auth. | `lib/screens/login_screen.dart`<br>`lib/providers/auth_provider.dart` | **Đã xác nhận đặc tả** | **4 PASS / 0 FAIL** (100% PASS) |
| **REQ-04** | Tạo ghi chú mới & Tự động lưu | Hỗ trợ tạo ghi chú văn bản thuần hoặc danh sách Checklist. Cơ chế tự động lưu ngầm (Autosave) thời gian thực xuống SQLite sau 1-2.5 giây khi có thay đổi hoặc khi người dùng thoát màn hình Editor. Tự động hủy/xóa bản nháp nếu toàn bộ tiêu đề và nội dung bị xóa trắng. | `lib/screens/editor_screen.dart`<br>`lib/services/local_note_service.dart`<br>`lib/models/note_model.dart` | **Đã xác nhận đặc tả** | **8 PASS / 0 FAIL** (Hộp đen) + **9 Unit test PASS** |
| **REQ-05** | Chỉnh sửa Rich-text & Cập nhật ghi chú | Hỗ trợ định dạng văn bản (In đậm, In nghiêng, Gạch chân, Màu sắc). Tự động cập nhật trường `updated_at` (epoch milliseconds) phục vụ phân xử đồng bộ. Thoát màn hình bằng nút Back AppBar, System Back hoặc Gesture Back đều bảo đảm lưu toàn vẹn dữ liệu. | `lib/screens/editor_screen.dart`<br>`lib/models/note_model.dart` | **Đã xác nhận đặc tả** | **12 PASS / 0 FAIL** (1 Minor UI Glitch `BUG-005`) |
| **REQ-06** | Quản lý Checklist (To-do list) | Cho phép thêm từng mục danh sách, tick hoàn thành (chữ gạch ngang, đổi màu mờ), bỏ tick hoàn thành, xóa từng mục độc lập mà không ảnh hưởng thứ tự các mục khác. Đảm bảo toàn vẹn dữ liệu checkbox khi lưu và mở lại. | `lib/features/editor/widgets/editor_checklist_section.dart`<br>`lib/models/checklist_item.dart` | **Đã xác nhận đặc tả** | **6 PASS / 0 FAIL** (Hộp đen) + **9 Unit test PASS** |
| **REQ-07** | Ghim ghi chú (Pin Note) | Cho phép ghim hoặc bỏ ghim ghi chú. Trên Trang chủ, các ghi chú được ghim phải tự động gom nhóm và hiển thị ưu tiên lên phần đầu danh sách trước nhóm ghi chú thông thường. | `lib/screens/home_screen.dart`<br>`lib/services/local_note_service.dart` | **Đã xác nhận đặc tả** | **15 PASS / 0 FAIL** |
| **REQ-08** | Tìm kiếm văn bản & Bộ lọc đa năng | Tìm kiếm từ khóa theo Tiêu đề và Nội dung qua truy vấn SQL LIKE không phân biệt hoa/thường (`LOWER(...) LIKE ?`), chỉ yêu cầu khớp có dấu theo `BR-01`. Hỗ trợ bôi màu nổi bật (Highlight) từ khóa trên thẻ kết quả. Hỗ trợ lọc theo Filter Chip trên giao diện tìm kiếm: `has:url`, `has:image`, `has:audio`, `has:list` (Danh sách Checklist), `is:pinned`, `is:archived`, `label:name`. Loại trừ hoàn toàn các ghi chú đang nằm trong Thùng rác khỏi kết quả tìm kiếm. *(Lưu ý kỹ thuật: Giao diện `search_screen.dart` cung cấp chip `Danh sách` / `has:list` thuộc `REQ-08`, nhưng `local_note_service.dart` chưa bóc tách token `has:list` mà đẩy vào SQL `LIKE` thô làm kết quả trả về rỗng — ghi nhận lỗi [BUG-004](../bugs/defect_log.md) tại ca `TC-BB-027G-D01`).* | `lib/screens/search_screen.dart`<br>`lib/services/local_note_service.dart` | **Đã xác nhận đặc tả** *(Đã chốt `BR-01`)* | **20 PASS / 1 FAIL** (`BUG-004` ở `TC-BB-027G-D01`) / **1 CHƯA ĐỦ CĂN CỨ** (`TC-BB-026B-D03` — đã giải tỏa nghiệp vụ theo `BR-01`, không tự chuyển PASS) |
| **REQ-09** | Quản lý Thùng rác & Lưu trữ | Xóa mềm: Chuyển ghi chú vào Thùng rác (`status = 'trash'`). Trong màn hình Thùng rác, hỗ trợ: Khôi phục ghi chú về trạng thái ban đầu hoặc Xóa vĩnh viễn khỏi cả SQLite và Cloud. Chức năng Lưu trữ: Chuyển ghi chú vào màn hình Archive (`status = 'archived'`) để ẩn khỏi Trang chủ và cho phép bỏ lưu trữ. | `lib/screens/trash_screen.dart`<br>`lib/screens/archive_screen.dart`<br>`lib/repositories/note_repository.dart` | **Đã xác nhận đặc tả** | **12 PASS / 0 FAIL** (Trash FN-10..12) + **2 Evidence PASS** (Archive FN-13..14) |
| **REQ-10** | Bảo mật sinh trắc học cho ghi chú | Cho phép người dùng khóa từng ghi chú riêng tư bằng cảm biến vân tay/FaceID. Khi đã khóa, thẻ ghi chú trên Trang chủ che giấu tiêu đề/nội dung (`🔒 Ghi chú đã khóa`). Khi mở ghi chú hoặc khi ứng dụng chuyển xuống chạy ngầm (Background) rồi mở lại (Resume), ứng dụng tự động khóa màn hình và kích hoạt hộp thoại xác thực sinh trắc học. | `lib/services/biometric_service.dart`<br>`lib/screens/editor_screen.dart` | **Đã xác nhận đặc tả** | **11 PASS / 0 FAIL / 1 BLOCKED** (`TC-BB-015G-D01`: ràng buộc an toàn không xóa vân tay máy thật) |
| **REQ-11** | Đồng bộ Offline & Giải quyết xung đột LWW | Khi mất kết nối mạng, ứng dụng lưu và chỉnh sửa bình thường trên SQLite local (`is_synced = 0`). Khi có mạng trở lại, Background Sync tự động đồng bộ lên Firestore. Áp dụng thuật toán Last-Write-Wins: so sánh mốc `updatedAt` giữa Local và Cloud, bản ghi nào có timestamp lớn hơn sẽ thắng và ghi đè bản ghi cũ hơn (kể cả xung đột Sửa vs Xóa theo `BR-02`). | `lib/repositories/sync_repository.dart`<br>`lib/services/pending_delete_service.dart` | **Đã xác nhận đặc tả cốt lõi** *(Đã chốt `BR-02`; còn mở `BR-03` khi trùng `updatedAt`)* | **7 PASS / 2 FAIL** (`BUG-002`, `BUG-003`) / **1 CHƯA ĐỦ CĂN CỨ** (`TC-BB-031C-D01` — đã giải tỏa theo `BR-02`) + **8 Security Rules tests PASS** |
| **REQ-12** | Tiện ích bổ trợ (Nhãn dán, PDF, Bảng vẽ, Nhắc nhở) | Quản lý nhãn dán ghi chú; Xuất nội dung ghi chú thành tệp PDF; Vẽ tay đính kèm ảnh vẽ vào ghi chú; Tải ảnh lên Cloudinary; Đổi màu nền ghi chú; Chuyển đổi bố cục Grid/List; Lập lịch thông báo nhắc nhở và mở trực tiếp ghi chú từ thông báo. | `lib/services/pdf_export_service.dart`<br>`lib/screens/drawing_screen.dart`<br>`lib/services/reminder_service.dart`<br>`lib/screens/manage_labels_screen.dart` | **Đã xác nhận đặc tả** | **10 Evidence PASS / 0 FAIL** (Kịch bản tiện ích mở rộng; riêng FN-36 tải ảnh ghi nhận `BUG-001`) |
| **REQ-13** | Trợ lý thông minh Gemini AI | Tự động tóm tắt nội dung ghi chú, gợi ý tiêu đề thông minh và bóc tách nội dung văn bản thành danh sách việc cần làm (Checklist). | `lib/services/gemini_ai_service.dart`<br>`lib/screens/editor_screen_ai.dart` | **Đã xác nhận đặc tả & mã nguồn** | **3 BLOCKED** (Kịch bản 5 `FN-31..33` bị chặn khi thực thi do lỗi UI trên máy thật; 3 ca thiết kế mới `TC-BB-032`, `032B`, `032C`: `NOT RUN` chờ gỡ `BLOCKED`) |

---

## 4. YÊU CẦU PHI CHỨC NĂNG TRONG PHẠM VI KIỂM THỬ (NON-FUNCTIONAL REQUIREMENTS)

* **NFR-01 (Offline-First Availability):** Toàn bộ các thao tác cốt lõi (Xem danh sách, Tạo mới, Soạn thảo, Đánh dấu Checklist, Đổi màu, Ghim, Xóa vào thùng rác) phải thực thi bình thường trên cơ sở dữ liệu cục bộ SQLite mà không bị treo ứng dụng hay phụ thuộc vào trạng thái kết nối mạng khi thiết bị ở chế độ ngoại tuyến (Airplane mode). Cờ đồng bộ `is_synced` được đánh dấu là chưa đồng bộ (`0`) để sẵn sàng đồng bộ nền khi có mạng trở lại.
  - *Tiêu chí kiểm thử có thể quan sát / đo lường:*
    1. Giao diện không xuất hiện hộp thoại lỗi mạng hay crash/freeze khi người dùng thao tác ở chế độ máy bay.
    2. Dữ liệu tạo mới/chỉnh sửa được ghi nhận thành công và đọc lại đầy đủ từ bảng SQLite cục bộ `smart_note.db`.
    3. Trường cờ `is_synced` trong SQLite được xác thực mang giá trị `0` qua công cụ kiểm tra cơ sở dữ liệu (`tools/check_note.py`).
* **NFR-02 (Data Consistency & Conflict Resolution):** Tính nhất quán dữ liệu giữa nhiều thiết bị được giải quyết theo quy tắc Last-Write-Wins (LWW) căn cứ trên mốc thời gian `updatedAt` (epoch timestamp). Khi có xung đột đồng bộ giữa hai bản ghi trên các thiết bị, hệ thống giữ lại bản ghi có mốc thời gian muộn hơn; nội dung sửa đổi mới hơn được ghi đè lên bản ghi cũ hơn và phản ánh đồng nhất trên các thiết bị sau khi hoàn tất chu trình đồng bộ.
  - *Tiêu chí kiểm thử có thể quan sát / đo lường:*
    1. So sánh mốc thời gian `updatedAt` giữa hai thiết bị: Thiết bị có mốc thời gian lớn hơn (mới hơn) sẽ là phiên bản dữ liệu cuối cùng được lưu trữ trên Cloud Firestore và trên cả hai thiết bị sau khi đồng bộ.
    2. Nội dung của bản ghi có mốc thời gian cũ hơn không được ghi đè hay làm mất dữ liệu của bản ghi có mốc thời gian mới hơn.
* **NFR-03 (Security & Data Isolation):** Cloud Firestore Security Rules (`firestore.rules`) phải cô lập hoàn toàn dữ liệu giữa các người dùng (`isOwner(userId)` $\rightarrow$ `request.auth != null && request.auth.uid == userId` và `isValidNote(userId)` $\rightarrow$ `request.resource.data.user_id == userId`). Người dùng A tuyệt đối không thể đọc hoặc ghi đè ghi chú của Người dùng B. *(Truy vết kiểm thử: `test/security_rules_test.dart` — 8 tests PASS, `TC-WB-011` .. `TC-WB-014` và `TC-NF-006` thuộc `REQ-11 / NFR-03 / FN-40`)*.
* **NFR-04 (Input Robustness & Injection Safety):** Thanh tìm kiếm và các trường văn bản phải xử lý an toàn chuỗi ký tự đặc biệt, payload SQL injection (`' OR '1'='1`), chuỗi Unicode tiếng Việt dài, emoji mà không bị crash ứng dụng.
* **NFR-05 (App Lifecycle Biometric Security):** Ghi chú đang mở xem nội dung phải ngay lập tức chuyển về trạng thái khóa bảo vệ khi ứng dụng chuyển sang trạng thái `AppLifecycleState.paused` hoặc `inactive`.

---

## 5. MÔI TRƯỜNG KIỂM THỬ VÀ CÁC RÀNG BUỘC (CONSTRAINTS)

1. **Thiết bị kiểm thử:**
   - Thiết bị A: Samsung Galaxy S21 FE 5G (SM-G990E, Android 14 API 34) — Thiết bị chính.
   - Thiết bị B: Samsung Galaxy S24 FE (SM-S741B, Android 14 API 34) — Dùng cho kiểm thử đồng bộ 2 thiết bị và xung đột LWW.
2. **Ràng buộc an toàn thiết bị thật:**
   - Tuyệt đối không thực hiện kịch bản xóa dấu vân tay hệ thống trên máy thật của Tester (ca `TC-BB-015G-D01` thuộc FN-29/FN-30 ghi nhận trạng thái **BLOCKED** an toàn).
   - Tuyệt đối không cố tình ghi đè làm đầy bộ nhớ máy thật dẫn đến nguy cơ treo hệ điều hành (`FN-44` ghi nhận **BLOCKED** an toàn).
3. **Ràng buộc dịch vụ bên thứ ba:**
   - Dịch vụ Cloudinary phụ thuộc kết nối Internet và Upload Preset (hiện đang tồn tại khiếm khuyết [BUG-001](../bugs/defect_log.md#L23-L60) do thiếu HTTP timeout).
   - Dịch vụ Gemini AI phụ thuộc Google AI API (hiện đang phát sinh thông báo lỗi đỏ trên UI chưa xác định nguyên nhân).

---

## 6. NHỮNG NỘI DUNG NẰM NGOÀI PHẠM VI (OUT-OF-SCOPE)

* **Nền tảng iOS:** Không thực hiện do thiếu phần cứng máy Mac và iPhone thật.
* **Kiểm thử chịu tải lớn (Stress / Load Testing):** Không thực hiện do sử dụng gói dịch vụ đám mây miễn phí Firebase Spark.
* **Kiểm thử liên kết ứng dụng bên ngoài (External Deep Link):** Không kiểm thử thao tác click link kích hoạt email từ app Gmail (`FN-03`) hoặc link đổi mật khẩu từ trình duyệt web ngoài (`FN-06`).
* **Kiểm thử dữ liệu cực hạn quá tải:** Tạm hoãn thử nghiệm văn bản cực lớn >50.000 ký tự (`FN-42`) và tệp ảnh cực lớn >10MB (`FN-43`) do thiếu tiêu chí mock OOM cô lập.
* **Bao phủ 100% Widget cây giao diện Flutter:** Không đặt mục tiêu bao phủ toàn bộ các widget hiển thị đồ họa thuần túy của Flutter framework.

---

## 7. CÁC QUY TẮC NGHIỆP VỤ BIÊN, ĐIỂM ĐÃ XÁC NHẬN VÀ VẤN ĐỀ CÒN MỞ (BUSINESS RULES & OPEN ITEMS)

Mục này tổng hợp các quy tắc nghiệp vụ biên đã được xác nhận/phân loại chính thức (`BR-01`, `BR-02`, `BR-04`), quy tắc nghiệp vụ còn đang để ngỏ chờ xác nhận từ Giảng viên / Product Owner (`BR-03`) và hiện trạng hạng mục bị chặn thực thi (`REQ-13`):

### BR-01: Quy tắc tìm kiếm tiếng Việt không dấu (Unaccented Search)
* **Hiện trạng kỹ thuật:** Mã nguồn `local_note_service.dart` sử dụng SQLite `LOWER(...) LIKE ?`. SQLite mặc định trên Android không hỗ trợ bỏ dấu tiếng Việt (gõ `nghien cuu` sẽ không khớp với bản ghi `Nghiên cứu`).
* **Quyết định nghiệp vụ:** **ĐÃ XÁC NHẬN CHÍNH THỨC**. Hệ thống chỉ yêu cầu tìm kiếm khớp có dấu (chấp nhận giới hạn kỹ thuật của SQLite `LIKE` engine mặc định; không coi việc không khớp từ khóa không dấu là khiếm khuyết ứng dụng). Ca thực thi `TC-BB-026B-D03` **giữ nguyên trạng thái thực thi gốc là `CHƯA ĐỦ CĂN CỨ`** trong bảng kết quả thực thi ([fn23_execution_sheet.md](../test_cases/execution_sheets/fn23_execution_sheet.md)) và được ghi nhận là **đã giải tỏa điểm mở nghiệp vụ theo `BR-01` (xác định thuộc giới hạn kỹ thuật / Out-of-scope; tuyệt đối không tự chuyển kết quả thực thi thành `PASS`)**.
* **Trạng thái đặc tả:** **Đã xác nhận chính thức (Quy tắc nghiệp vụ đã chốt)**.

### BR-02: Quy tắc phân xử xung đột giữa "Chỉnh sửa offline" và "Chuyển Thùng rác offline"
* **Hiện trạng kỹ thuật:** Khi Thiết bị A chỉnh sửa nội dung ghi chú offline và Thiết bị B chuyển ghi chú vào Thùng rác offline, sau đó cả hai thiết bị cùng kết nối mạng trở lại.
* **Quyết định nghiệp vụ:** **ĐÃ XÁC NHẬN CHÍNH THỨC**. Tuân thủ chuẩn thuật toán **Last-Write-Wins (LWW)**: hành động nào có mốc thời gian `updatedAt` muộn hơn sẽ thắng (sửa muộn hơn thì giữ nội dung note, xóa muộn hơn thì đưa vào Thùng rác). Ca thực thi `TC-BB-031C-D01` giữ nguyên lịch sử thực thi gốc là **`CHƯA ĐỦ CĂN CỨ`** trong [fn40_fn41_execution_sheet.md](../test_cases/black_box/fn40_fn41_execution_sheet.md) và được giải tỏa tiêu chí nghiệp vụ theo mốc `updatedAt` của `BR-02`.
* **Trạng thái đặc tả:** **Đã xác nhận chính thức (Quy tắc nghiệp vụ đã chốt)**.

### BR-03: Quy tắc phân xử hòa khi trùng khớp mốc thời gian `updatedAt` (Tie-break Rule)
* **Tình huống kỹ thuật (Edge Case):** Cả hai thiết bị (Local và Cloud) cùng cập nhật một ghi chú và tình cờ ghi nhận chính xác cùng một mốc thời gian `updatedAt` tới từng millisecond (`local.updatedAt.isAtSameMomentAs(cloud.updatedAt)`), nhưng nội dung văn bản hoặc trạng thái ghi chú ở hai bên lại khác nhau (nội dung phân kỳ).
* **Hiện trạng xử lý trong mã nguồn:**
  - Trong [lib/repositories/sync_repository.dart](../../lib/repositories/sync_repository.dart#L67-L129):
    + Chiều Push (Local $\rightarrow$ Cloud): Điều kiện đồng bộ là `local.updatedAt.isAfter(cloud.updatedAt)`. Khi bằng nhau, kết quả là `false` $\rightarrow$ Bỏ qua không đẩy lên Cloud.
    + Chiều Pull (Cloud $\rightarrow$ Local): Điều kiện đồng bộ là `cloud.updatedAt.isAfter(local.updatedAt)`. Khi bằng nhau, kết quả là `false` $\rightarrow$ Bỏ qua không ghi đè xuống Local.
    + Cờ đồng bộ trên Local: Trường `is_synced` trong bảng SQLite giữ nguyên giá trị `0` (chưa đồng bộ).
* **Ảnh hưởng đến đồng bộ hệ thống (Sync Impact):**
  - Gây ra hiện tượng bế tắc đồng bộ (Sync Standoff) và phân mảnh dữ liệu (Data Drift): Cả hai bên đều từ chối cập nhật của nhau, dữ liệu trên Cloud và Local tiếp tục khác biệt mà không thể tự hội tụ, cờ `is_synced = 0` tồn tại vô hạn cho đến khi có một bên phát sinh chỉnh sửa mới.
* **Ảnh hưởng đến Test Case và Tiêu chí PASS/FAIL (Testing & Verification Impact):**
  - Theo [white_box_test_plan.md](./white_box_test_plan.md) và [white_box_test_cases.md](../test_cases/white_box/white_box_test_cases.md) đã chốt, ca kiểm thử hộp trắng **`TC-WB-021`** đang ở trạng thái **`DESIGN ONLY`** (chưa chạy thực thi) và chỉ kiểm tra toán tử so sánh `updatedAt.isAfter` độc lập trong bộ nhớ (Cặp 1 `local > cloud` $\rightarrow$ `true`; Cặp 2 `cloud > local` $\rightarrow$ `true`; Cặp 3 trùng khớp `local == cloud` $\rightarrow$ cả hai biểu thức `isAfter` đều trả về `false`).
  - Riêng đối với **kết quả đồng bộ cuối cùng giữa hai thiết bị** khi rơi vào nhánh trùng khớp timestamp (Cặp 3), không thể tự áp đặt mệnh đề khẳng định kỳ vọng (Expected Assertion) là `PASS` hay `FAIL` vì chưa có quy tắc nghiệp vụ định trước bản ghi nào hợp lệ.
* **Quy tắc phân xử tiềm năng:**
  1. *Lựa chọn A (Cloud wins):* Ưu tiên dữ liệu tập trung trên Cloud để duy trì tính nhất quán cho các client khác.
  2. *Lựa chọn B (Local wins):* Ưu tiên thao tác người dùng tại máy hiện hành.
  3. *Lựa chọn C (Merge / Create Conflict Copy):* Giữ nguyên cả hai bản ghi bằng cách tạo bản sao xung đột (`Note - Conflict Copy`).
* **Trạng thái đặc tả:** **NEEDS CONFIRMATION (CẦN XÁC NHẬN NGHIỆP VỤ)**.
  - *Lưu ý ràng buộc:* Đội ngũ QA tuyệt đối **không tự ý chọn** Cloud thắng, Local thắng hay Merge. Quyết định quy tắc Tie-break này bắt buộc phải do Product Owner (PO) hoặc Giảng viên hướng dẫn xác nhận và phê duyệt trước khi đưa vào tiêu chí đánh giá đồng bộ chính thức.

### BR-04: Giới hạn 2.000 ký tự nội dung ghi chú (Character Limit vs UI Guideline)
* **Đối chiếu tài liệu & Mã nguồn:**
  - Trong [docs/giao-dien.md](../giao-dien.md#L571-L614) (mục 3.1.1 & 3.3): Mô tả quy tắc thiết kế giao diện mong muốn cho màn Editor (Bộ đếm từ/ký tự, max 2.000 ký tự body, cảnh báo khi đạt 90%, vô hiệu hóa nút gửi khi vượt quá, và yêu cầu khi nội dung > 2.000 ký tự màn hình phải scroll mượt).
  - Trong đề bài đồ án, Master Test Plan ([test_plan.md](./test_plan.md)) và mã nguồn thực tế [lib/screens/editor_screen.dart](../../lib/screens/editor_screen.dart): Hoàn toàn không cài đặt bộ đếm ký tự hay cơ chế chặn cứng 2.000 ký tự (ứng dụng dùng auto-save ngầm không có nút gửi; ca `TC-BB-018E` chấp nhận văn bản dài tùy ý).
* **Phân loại rõ ràng:** Giới hạn 2.000 ký tự chỉ là **mô tả đề xuất giao diện (UI Guideline) chưa được hiện thực hóa**, **KHÔNG PHẢI là yêu cầu nghiệp vụ hệ thống chính thức (Not an Official System Requirement)**.
* **Trạng thái đặc tả:** **ĐÃ XÁC MINH PHÂN LOẠI (Quy định: Không áp dụng giới hạn chặn cứng 2.000 ký tự vào phạm vi kiểm thử chức năng)**.

### REQ-13 (Bổ sung): Hiện trạng kiểm thử Trợ lý Gemini AI (FN-31, FN-32, FN-33)
* **Những gì đã biết (Known):**
  1. Mã nguồn [lib/services/gemini_ai_service.dart](../../lib/services/gemini_ai_service.dart) và [lib/screens/editor_screen_ai.dart](../../lib/screens/editor_screen_ai.dart) đã cài đặt đầy đủ logic gọi `FirebaseAI.googleAI().generativeModel(model: 'gemini-2.5-flash-lite')` và hàm bắt lỗi `_friendlyAiError`.
  2. **Lịch sử thực thi thực tế (Kịch bản 5):** Trong đợt kiểm thử thủ công trên thiết bị thật ([Testing_Report.md](../test_report/Testing_Report.md) và [black_box_execution_summary.md](../qa/black_box_execution_summary.md#L122)), 3 kịch bản chức năng `FN-31`, `FN-32`, `FN-33` khi kích hoạt đều bị chặn (**`3 BLOCKED`**) do giao diện trả về khung thông báo lỗi màu đỏ trên UI máy thật.
  3. **Test case thiết kế chuẩn hóa bổ sung:** Ba ca kiểm thử hộp đen có mã định danh chính thức **`TC-BB-032`** (`FN-31` — Tóm tắt nội dung ghi chú), **`TC-BB-032B`** (`FN-32` — Đề xuất tiêu đề tự động), và **`TC-BB-032C`** (`FN-33` — Bóc tách văn bản thành Checklist việc cần làm) đã được thiết kế đầy đủ tại [test_case_design_inventory_44_fn.md](./test_case_design_inventory_44_fn.md) và [black_box_test_cases.md](../test_cases/black_box/black_box_test_cases.md). Do dịch vụ đang bị chặn trên thiết bị và chưa có evidence thực thi riêng cho 3 mã mới này, các mã `TC-BB-032`, `TC-BB-032B`, `TC-BB-032C` được ghi nhận trạng thái thực thi là **`NOT RUN` (Chờ gỡ `BLOCKED` của dịch vụ Gemini AI)**.
* **Những gì chưa biết (Unknown):** Chưa có log response HTTP chi tiết hay exception từ Firebase AI SDK trong logcat để xác định nguyên nhân kỹ thuật cụ thể (API key, quota, mạng hay cấu hình vùng).
* **Trạng thái:** **Lịch sử thực thi Kịch bản 5 (`FN-31..33`): `3 BLOCKED` | Các ca thiết kế mới (`TC-BB-032`, `032B`, `032C`): `DESIGNED / NOT RUN` (Chờ gỡ `BLOCKED`)**.

---

## 8. BẢNG TRUY VẾT YÊU CẦU: REQ $\rightarrow$ FN $\rightarrow$ TEST CASE
*(Chuẩn hóa đồng bộ 100% theo danh mục REQ-01 đến REQ-13 tại Mục 3, [white_box_test_plan.md](./white_box_test_plan.md), [black_box_test_cases.md](../test_cases/black_box/black_box_test_cases.md) và [black_box_test_cases.md](../test_cases/black_box/black_box_test_cases.md). Toàn bộ mã định danh Test Case đảm bảo duy nhất 100%, không trùng lặp. Các ca `TC-WB-xxx` mang nhãn `[DESIGN ONLY]` là các ca kiểm thử hộp trắng đã chốt thiết kế trong kế hoạch nhưng chưa chạy thực thi. Các ca `TC-BB-xxx` / `TC-NF-xxx` mang nhãn `[NOT RUN]` là các ca thiết kế bổ sung chưa thực thi. Kết quả thực thi đã có được bảo toàn nguyên vẹn).*

| Mã REQ | Mô tả yêu cầu hệ thống (Theo Mục 3) | Mã FN ánh xạ | Mã Test Case ánh xạ (Đối chiếu chuẩn với tài liệu gốc) | Trạng thái thực thi kiểm thử đã có |
|:---:|:---|:---:|:---|:---|
| **REQ-01** | Đăng ký tài khoản Email/Password | **FN-02, FN-03** | • **FN-02:** `TC-BB-001`, `TC-BB-001B`, `TC-BB-002`, `TC-BB-002B`, `TC-BB-002C`, `TC-BB-002D`, `TC-BB-002E`, `TC-BB-002F`, `TC-BB-003`, `TC-BB-003B`, `TC-BB-004`, `TC-BB-004B`, `TC-BB-005`, `test_fn02_register.py`, `TC-WB-004` `[DESIGN ONLY]`<br>• **FN-03:** `TC-BB-003C`, `TC-BB-003D` `[NOT RUN]` | **18 PASS / 1 FAIL** (`BUG-FN02-01`) *(FN-02)*;<br>2 ca bổ sung FN-03: `NOT RUN` |
| **REQ-02** | Đăng nhập hệ thống (Email & Google) & Đăng xuất | **FN-01, FN-04, FN-05, FN-07** | • **FN-01/FN-04:** `TC-BB-006` .. `TC-BB-009G` (16 items), `test_fn04_login.py`<br>• **FN-05:** `TC-BB-010`, `TC-BB-011` .. `TC-BB-011G` (8 items), `test_fn05_google_oauth.py`<br>• **FN-07:** `TC-BB-011E`, `auth01_logged_out.png`, `TC-BB-007C` `[NOT RUN]`<br>• **White-box:** `TC-WB-001`, `TC-WB-002`, `TC-WB-003`, `TC-WB-005` `[DESIGN ONLY]` | **22 PASS / 2 FAIL** (`BUG-BB-002`, `BUG-BB-003`) *(FN-04 & FN-05)*;<br>1 Evidence FN-07 `PASS`; 1 ca mới `TC-BB-007C`: `NOT RUN` |
| **REQ-03** | Quên & Đặt lại mật khẩu | **FN-06** | `TC-BB-009E` (`fn04_execution_sheet.md`), `TC-BB-011` .. `TC-BB-011C` (đối chiếu luồng Auth), `TC-BB-011H` ([black_box_test_cases.md](../test_cases/black_box/black_box_test_cases.md)) `[NOT RUN]` | **4 PASS / 0 FAIL** (100% PASS đã thực thi);<br>1 ca bổ sung `TC-BB-011H`: `NOT RUN` |
| **REQ-04** | Tạo ghi chú mới & Tự động lưu | **FN-08** | `TC-BB-016`, `TC-BB-017`, `TC-BB-018`, `TC-BB-018B` .. `TC-BB-018F` (8 items trong `fn08_execution_sheet.md`), `test_fn08_create_note.py`, Unit test: `test/note_model_test.dart` (9 tests PASS), **`TC-WB-020`** (`Note.fromMap` phòng thủ SQLite map thiếu trường thời gian `created_at`/`updated_at` — `[DESIGN ONLY]`) | **8 PASS / 0 FAIL** (Hộp đen) + **9 Unit test PASS**;<br>`TC-WB-020`: `DESIGN ONLY` |
| **REQ-05** | Chỉnh sửa Rich-text & Cập nhật ghi chú | **FN-09** | `TC-BB-019` .. `TC-BB-019G`, `TC-BB-020` .. `TC-BB-020D` (12 items trong `fn09_execution_sheet.md`), `test_fn09_edit_note.py`, `TC-WB-016`, `TC-WB-017`, `TC-WB-019` (`Note.copyWith(updatedAt)`) `[DESIGN ONLY]` | **12 PASS / 0 FAIL** (1 Minor UI Glitch `BUG-005`);<br>`TC-WB-016, 017, 019`: `DESIGN ONLY` |
| **REQ-06** | Quản lý Checklist (To-do list) | **FN-15..19** | `TC-BB-CHK-01` .. `TC-BB-CHK-06` (6 items trong `fn15_fn19_checklist_execution_sheet.md`), Unit test: `test/checklist_test.dart` (5 tests PASS), `test/checklist_copy_with_test.dart` (4 tests PASS), `TC-WB-015` (`pendingChecklistCount`), `TC-WB-022` (`ChecklistItem.fromJson`) `[DESIGN ONLY]` | **6 PASS / 0 FAIL** (Hộp đen) + **9 Unit test PASS**;<br>`TC-WB-015, 022`: `DESIGN ONLY` |
| **REQ-07** | Ghim ghi chú (Pin Note) | **FN-20** | `TC-BB-024`, `TC-BB-024B` .. `TC-BB-024H`, `TC-BB-025` .. `TC-BB-025F` (15 items trong `fn20_execution_sheet.md`), `test_fn20_pin_note.py` | **15 PASS / 0 FAIL** |
| **REQ-08** | Tìm kiếm văn bản & Bộ lọc đa năng (gồm cả `has:list`) | **FN-23..27** | `TC-BB-026` .. `TC-BB-029` (22 Execution Items trong [fn23_execution_sheet.md](../test_cases/execution_sheets/fn23_execution_sheet.md), gồm `TC-BB-027G-D01` kiểm thử bộ lọc `has:list` và `TC-BB-026B-D03` tìm kiếm không dấu), `test_fn23_search.py`, `TC-NF-007`, `TC-WB-016` (`plainTextContent` — `[DESIGN ONLY]`) | **20 PASS / 1 FAIL** (`BUG-004` tại `TC-BB-027G-D01` do lọc `has:list` query `LIKE` thô) / **1 CHƯA ĐỦ CĂN CỨ** (`TC-BB-026B-D03` — giữ nguyên trạng thái gốc, đã giải tỏa nghiệp vụ theo `BR-01`, không tự chuyển thành PASS) |
| **REQ-09** | Quản lý Thùng rác & Lưu trữ | **FN-10..14** | • **FN-10..12 (Trash — [fn10_fn11_fn12_execution_sheet.md](../test_cases/black_box/fn10_fn11_fn12_execution_sheet.md)):** `TC-BB-021`, `TC-BB-021B`, `TC-BB-021C` (`D01`, `D02`), `TC-BB-021D` (FN-10); `TC-BB-022`, `TC-BB-022B`, `TC-BB-022C` (FN-11); `TC-BB-023`, `TC-BB-023B` (`D01`, `D02`), `TC-BB-023C` (FN-12); đối chiếu lọc `TC-BB-028B-D01` (Trash), `TC-BB-027D-D02` (Archive); **`TC-WB-006`, `TC-WB-007`** (`CloudinaryService._extractPublicId` — **Ánh xạ chính `REQ-09 / FN-12`** do `NoteProvider.deleteNoteForever` gọi `deleteFile(url)` để xóa ảnh/audio đính kèm trên Cloudinary khi xóa vĩnh viễn ghi chú — `[DESIGN ONLY]`)<br>• **FN-13..14 (Archive):** Evidence `arc01_archive_screen.png`, `arc02_unarchived_home.png`; ca thiết kế bổ sung tại [black_box_test_cases.md](../test_cases/black_box/black_box_test_cases.md): **`TC-BB-040`** (FN-13), **`TC-BB-040B`** (FN-14) `[NOT RUN]` | **12 PASS / 0 FAIL** (12 Execution Items nhóm FN-10..12) + **2 Evidence PASS** (FN-13..14);<br>2 ca bổ sung `TC-BB-040, 040B`: `NOT RUN`;<br>`TC-WB-006, 007`: `DESIGN ONLY` |
| **REQ-10** | Bảo mật sinh trắc học cho ghi chú | **FN-29, FN-30** | • **FN-29 ([fn29_fn30_execution_sheet.md](../test_cases/black_box/fn29_fn30_execution_sheet.md)):** `TC-BB-012`, `TC-BB-012B`, `TC-BB-012C`, `TC-BB-015G` (`TC-BB-015G-D01`: `BLOCKED`)<br>• **FN-30:** `TC-BB-013`, `TC-BB-014`, `TC-BB-015`, `TC-BB-015B`, `TC-BB-015C`, `TC-BB-015D`, `TC-BB-015E`, `TC-BB-015F`<br>• **Auto & NFR:** `test_fn29_30_biometric.py`, `TC-NF-005` `[NOT RUN]` | **11 PASS / 0 FAIL / 1 BLOCKED** (`TC-BB-015G-D01`: Ràng buộc an toàn không xóa vân tay thiết bị thật);<br>`TC-NF-005`: `NOT RUN` |
| **REQ-11** | Đồng bộ Offline & Giải quyết xung đột LWW (kèm Bảo mật phân quyền `NFR-03`) | **FN-40, FN-41** | `TC-BB-030` .. `TC-BB-030F`, `TC-BB-031` .. `TC-BB-031D` (10 items trong [fn40_fn41_execution_sheet.md](../test_cases/black_box/fn40_fn41_execution_sheet.md)), `tools/check_sync_dbs.py`, Security Rules test (**truy vết `REQ-11 / NFR-03 / FN-40`**): `test/security_rules_test.dart` (8 tests PASS; `TC-WB-011` .. `TC-WB-014` `[DESIGNED - Simulation PASS]`, `TC-NF-006`), `TC-WB-019` (`Note.copyWith(updatedAt)` — `[DESIGN ONLY]`), **`TC-WB-021`** (So sánh `updatedAt.isAfter` trong bộ nhớ — **`[DESIGN ONLY]`**; quy tắc hòa `BR-03` giữ `NEEDS CONFIRMATION`) | **7 PASS / 2 FAIL** (`BUG-002`, `BUG-003`) / **1 CHƯA ĐỦ CĂN CỨ** (`TC-BB-031C-D01` — giữ nguyên trạng thái gốc, đã giải tỏa theo `BR-02`) + **8 Security Rules tests PASS** (`NFR-03`);<br>`TC-WB-019, 021`: `DESIGN ONLY` (`BR-03`: `NEEDS CONFIRMATION`) |
| **REQ-12** | Tiện ích bổ trợ (Nhãn dán, PDF, Bảng vẽ, Nhắc nhở, Ảnh, Màu, Layout) | **FN-21/22, FN-28, FN-34..39** | • **Bằng chứng thực thi mở rộng:** `tag01_...`, `tag02_...` (FN-21/22), `fn28_...` (FN-28), `pdf01_...` (FN-34), `draw01_...` (FN-35), `image_note_home.png` (FN-36, `BUG-001`), `fn37_...` (FN-37), `rem01_...` (FN-38), `rem02_...` (FN-39)<br>• **Ca thiết kế bổ sung ([black_box_test_cases.md](../test_cases/black_box/black_box_test_cases.md)):** **`TC-BB-041`**, **`TC-BB-041B`**, **`TC-BB-042`**, `TC-BB-034` .. `TC-BB-039` `[NOT RUN]`<br>• **White-box ([white_box_test_plan.md](./white_box_test_plan.md)):** **`TC-WB-018`** (`Note.copyWith(clearReminder)` xóa nhắc nhở — `REQ-12 / FN-38`, `[DESIGN ONLY]`), `TC-WB-008` .. `TC-WB-010` (`CloudinaryService.uploadImage` — **Ánh xạ chính `REQ-12 / FN-35, FN-36`**, `[DESIGN ONLY]`), `TC-WB-006`, `TC-WB-007` (`_extractPublicId` — **Ánh xạ phụ `REQ-12 / FN-35, FN-36`** do `EditorScreen._replaceDrawing` gọi `deleteFile(oldUrl)` khi thay thế bản vẽ/media trên Cloudinary, `[DESIGN ONLY]`) | **10 Evidence PASS / 0 FAIL** (Tiện ích mở rộng; riêng FN-36 tải ảnh Cloudinary có lịch sử lỗi `BUG-001`);<br>9 ca bổ sung (`TC-BB-041, 041B, 042, 034..039`): `NOT RUN`;<br>`TC-WB-018`, `TC-WB-006..010`: `DESIGN ONLY` |
| **REQ-13** | Trợ lý thông minh Gemini AI | **FN-31, FN-32, FN-33** | • **Hồ sơ thực thi lịch sử:** Kịch bản kiểm thử thủ công Kịch bản 5 ([Testing_Report.md](../test_report/Testing_Report.md) / [black_box_execution_summary.md](../qa/black_box_execution_summary.md)) cho 3 chức năng `FN-31`, `FN-32`, `FN-33`<br>• **Test case thiết kế mới ([black_box_test_cases.md](../test_cases/black_box/black_box_test_cases.md) & [test_case_design_inventory_44_fn.md](./test_case_design_inventory_44_fn.md)):** **`TC-BB-032`** (FN-31: Tóm tắt ghi chú), **`TC-BB-032B`** (FN-32: Đề xuất tiêu đề), **`TC-BB-032C`** (FN-33: Bóc tách Checklist) `[DESIGNED / NOT RUN]` | **Lịch sử Kịch bản 5 (`FN-31..33`): 3 BLOCKED** (do lỗi dịch vụ hiển thị khung đỏ trên UI máy thật, chưa có log xác định nguyên nhân);<br>**3 ca mới (`TC-BB-032`, `032B`, `032C`): `NOT RUN`** (chưa có evidence riêng, chờ gỡ `BLOCKED`) |

