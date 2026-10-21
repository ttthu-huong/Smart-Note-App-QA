# KẾ HOẠCH KIỂM THỬ TOÀN DỰ ÁN (MASTER TEST PLAN)
## Dự án: Smart Note App
**Repository:** `Smart-Note-App-QA`  
**Branch áp dụng:** `huong`  
**Tiêu chuẩn tài liệu:** Phù hợp với IEEE 829 & ISTQB Test Planning  
**Trạng thái tài liệu:** Phiên bản Kế hoạch Tổng thể (Master Baseline) — Được thiết lập dựa trên mã nguồn thực tế và bằng chứng kiểm thử đã đối chiếu.

---

## 1. MỤC TIÊU VÀ CƠ SỞ YÊU CẦU

### 1.1. Mục tiêu kiểm thử
1. **Mục tiêu dự kiến (Planned Objectives):**
   - Đảm bảo chất lượng toàn diện của ứng dụng **Smart Note App** theo mô hình kiến trúc **Offline-First**, đảm bảo tính toàn vẹn dữ liệu giữa cơ sở dữ liệu cục bộ SQLite và dịch vụ lưu trữ đám mây Cloud Firestore.
   - Thiết lập quy trình kiểm thử có cấu trúc chặt chẽ, truy vết hai chiều (Traceability) từ yêu cầu chức năng/kỹ thuật đến các kịch bản kiểm thử (Test Cases), mã tự động hóa (Automation Scripts) và bằng chứng xác minh (Evidence).
   - Đánh giá tính ổn định của các cơ chế cốt lõi: Thuật toán giải quyết xung đột Last-Write-Wins (LWW), cơ chế xóa mềm (Trash), bảo mật sinh trắc học (Biometric Lock), bảo mật phân quyền Firestore Rules và tìm kiếm nội dung tối ưu qua SQL LIKE.
   - Cung cấp hồ sơ kiểm thử minh bạch, có cơ sở kỹ thuật thực tế để phục vụ buổi kiểm tra tiến độ môn học ngày 14/10/2026 và nghiệm thu bài tập lớn.
2. **Hiện trạng kết quả đã đạt được trong Baseline (Achieved Baseline Results):**
   - Hoàn thành thực thi và phân định minh bạch **140 Black-box Execution Items** trên 11 nhóm có Execution Sheet (131 PASS, 6 FAIL, 2 Chưa đủ căn cứ giải tỏa theo Business Rules, 1 BLOCKED an toàn phần cứng).
   - Hoàn thành và xác thực **18/18 Unit Tests PASS** trên 2 Data Models (`ChecklistItem` và `NoteModel`) với bằng chứng log và LCOV baseline.
   - Hoàn thành xác thực **8 Security Rules Tests PASS** mô phỏng phân quyền Cloud Firestore theo `request.auth.uid`.
   - Hoàn thành thực thi **44 Kịch bản kiểm thử tự động hóa** (20 UI/E2E test cases trên thiết bị thật và 24 Provider automated tests trên Dart).
   - Ghi nhận và phân tích nguyên nhân gốc cho **8 lỗi phần mềm Black-box** (`BUG-001` đến `BUG-005`, `BUG-FN02-01`, `BUG-BB-002`, `BUG-BB-003`) tại nhật ký lỗi.

### 1.2. Cơ sở yêu cầu kỹ thuật & Học phần
* **Đặc tả Yêu cầu Rút gọn (Condensed SRS v1.0):** [srs_condensed.md](./srs_condensed.md) — Quy chiếu chính thức gồm **13 yêu cầu chức năng** (`REQ-01` đến `REQ-13`) và **5 yêu cầu phi chức năng** (`NFR-01` đến `NFR-05`).
* **Tài liệu Kiến trúc & Luồng dữ liệu:** [Architecture_and_Flows.md](../Architecture_and_Flows.md) — Clean Architecture 4 lớp: UI Layer $\rightarrow$ State/Provider Layer $\rightarrow$ Repository Layer $\rightarrow$ Service/Storage Layer.
* **Ma trận Truy vết Yêu cầu:** [requirements_traceability_matrix.md](./requirements_traceability_matrix.md) — Ánh xạ hai chiều giữa REQ, FN, Test Cases và Evidence.
* **Bảng kiểm kê thiết kế 44 chức năng:** [test_case_design_inventory_44_fn.md](./test_case_design_inventory_44_fn.md) — Danh mục chi tiết 44 chức năng hệ thống từ `FN-01` đến `FN-44`.
* **Mã nguồn ứng dụng thực tế:** Thư mục [`lib/`](../../lib) gồm các service nền tảng, model dữ liệu, provider quản lý trạng thái và màn hình giao diện.

---

## 2. PHẠM VI KIỂM THỬ (TEST SCOPE) VÀ PHÂN CẤP ƯU TIÊN

### 2.1. Tổng quan phạm vi 44 Chức năng hệ thống (System Scope: FN-01 đến FN-44)
Toàn bộ hệ thống Smart Note App được cấu thành bởi **44 chức năng nghiệp vụ** (`FN-01` đến `FN-44`). Đội ngũ QA áp dụng chiến lược phân định rõ ranh giới giữa quy mô hệ thống, phạm vi được chọn kiểm thử và trạng thái thực thi thực tế:
* **Tổng số chức năng hệ thống:** 44 chức năng (`FN-01` .. `FN-44`).
* **Nhóm chức năng kiểm thử trọng tâm có Execution Sheet (11 nhóm):** Gồm 10 nhóm ban đầu (`FN-02`, `FN-04`, `FN-05`, `FN-08`, `FN-09`, `FN-10/11/12`, `FN-20`, `FN-23`, `FN-29/30`, `FN-40/41`) và nhóm Checklist bổ sung (`FN-15..19`), được theo dõi chi tiết qua **140 Execution Items**. *(Lưu ý: 11 nhóm có Execution Sheet là tập hợp các bộ hồ sơ kiểm thử thủ công trọng tâm trên thiết bị, không đánh đồng với tổng số nhóm chức năng nghiệp vụ của toàn bộ 44 FN)*.
* **Nhóm chức năng kiểm thử mở rộng có bằng chứng độc lập:** Gồm các chức năng tiện ích và vòng đời (`FN-07`, `FN-13/14`, `FN-21/22`, `FN-28`, `FN-34`, `FN-35`, `FN-36`, `FN-37`, `FN-38`, `FN-39`) đã được kiểm thử thủ công và lưu trữ screenshot/video xác minh.
* **Nhóm chức năng tự động hóa (Automation Coverage):** 12 FN đã bao phủ tự động thành công (kết hợp Tầng 1 UI/E2E và Tầng 2 Provider), 3 FN có kịch bản thăm dò, 4 FN bị chặn (BLOCKED), và 25 FN kiểm thử thủ công.
* **Nhóm chức năng tạm hoãn hoặc bị chặn an toàn:** `FN-03` và `FN-06` (hoãn do phụ thuộc ứng dụng email bên ngoài); `FN-31..33` (bị chặn do lỗi service UI của Gemini AI); `FN-42` và `FN-43` (hoãn do dữ liệu cực hạn); `FN-44` (bị chặn do an toàn phần cứng máy thật).

#### Bảng tổng hợp phân bổ 44 Chức năng hệ thống
*(Chi tiết ánh xạ từng FN sang REQ, Test Cases và Bằng chứng được dẫn chiếu đầy đủ tại [requirements_traceability_matrix.md](./requirements_traceability_matrix.md) và [test_case_design_inventory_44_fn.md](./test_case_design_inventory_44_fn.md))*:

| Nhóm ưu tiên | Khoảng mã FN | Số lượng FN | Mô tả nghiệp vụ tóm tắt | Trạng thái kiểm thử chủ đạo |
|:---:|:---|:---:|:---|:---|
| **P1 (Core)** | `FN-01`, `FN-02`, `FN-04`, `FN-05`, `FN-07`, `FN-08`, `FN-09`, `FN-10`, `FN-11`, `FN-12`, `FN-15`, `FN-16`, `FN-17`, `FN-18`, `FN-19`, `FN-20`, `FN-23`, `FN-29`, `FN-30`, `FN-36`, `FN-40`, `FN-41` | **22 FNs** | Xác thực tài khoản, CRUD ghi chú, Checklist, Ghim note, Tìm kiếm, Sinh trắc học, Đồng bộ Offline LWW, Upload media | **Đã thực thi 100% phạm vi** (Đạt PASS đa số; phát hiện lỗi `BUG-001`, `BUG-002`, `BUG-003`, `BUG-004`, `BUG-FN02-01`, `BUG-BB-002`, `BUG-BB-003`) |
| **P2 (Deep / Medium)** | `FN-03`, `FN-06`, `FN-13`, `FN-14`, `FN-21`, `FN-22`, `FN-24`, `FN-25`, `FN-26`, `FN-27`, `FN-31`, `FN-32`, `FN-33`, `FN-34`, `FN-35`, `FN-38`, `FN-39` | **17 FNs** | Xác thực email, Đặt lại mật khẩu, Lưu trữ Archive, Nhãn dán Tags, Chip lọc chi tiết, Trợ lý Gemini AI, Xuất PDF, Vẽ tay, Nhắc nhở | **Đã thực thi có bằng chứng:** 9 FNs (Archive, Tags, Filter chips, PDF, Vẽ, Nhắc nhở); **Hoãn:** 2 FNs (Deep links); **BLOCKED:** 3 FNs (Gemini AI); 3 ca thiết kế mới `NOT RUN` |
| **P3 (Extension / Low)** | `FN-28`, `FN-37`, `FN-42`, `FN-43`, `FN-44` | **5 FNs** | Chuyển layout Grid/List, Đổi màu nền ghi chú, Văn bản cực lớn (>50k ký tự), Tệp ảnh cực lớn (>10MB), Thiết bị hết bộ nhớ | **Đã thực thi:** 2 FNs (`FN-28`, `FN-37` PASS); **Hoãn:** 2 FNs (`FN-42`, `FN-43`); **BLOCKED:** 1 FN (`FN-44` an toàn máy thật) |
| **Tổng cộng** | **FN-01 đến FN-44** | **44 FNs** | **Toàn bộ hệ thống Smart Note App** | **100% Chức năng đã được phân loại và kiểm soát** |

---

### 2.2. Phạm vi trong dự án (In-Scope)

#### A. Nhóm Cốt lõi (Priority: High / P1 — Mục tiêu Độ phủ Thực thi: 100%)
> [!IMPORTANT]
> **Làm rõ mục tiêu P1:** Nhóm P1 đặt mục tiêu **Độ phủ thực thi đạt 100% (Execution Coverage = 100%)**, nghĩa là mọi yêu cầu cốt lõi đều phải được đưa vào kiểm thử trên thiết bị thật hoặc kiểm thử tự động. Tuy nhiên, **Tỷ lệ PASS thực tế hiện tại chưa đạt 100%** do đang ghi nhận các khiếm khuyết phần mềm OPEN (`BUG-001` High ở FN-36, `BUG-002` Critical ở FN-40, `BUG-FN02-01` ở FN-02). Tuyệt đối không coi việc giải trình lỗi kỹ thuật là tương đương với việc test case đã đạt PASS.

1. **Xác thực & Phiên làm việc (Authentication - REQ-01, REQ-02, REQ-03):**
   - Đăng ký tài khoản: Kiểm tra hợp lệ email, mật khẩu $\ge$ 6 ký tự, lọc domain rác, cắt khoảng trắng đầu/cuối, gửi email xác thực (`auth_provider.dart`, `login_screen.dart`, `email_verification_screen.dart`).
   - Đăng nhập: Đăng nhập bằng Email/Password, Google OAuth, chuẩn hóa chữ hoa/thường, chuyển hướng tài khoản chưa verify, xử lý lỗi Firebase Auth bằng tiếng Việt.
   - Quên & Đặt lại mật khẩu: Gửi email khôi phục mật khẩu.
2. **Quản lý Vòng đời Ghi chú CRUD & Trạng thái (Note Lifecycle - REQ-04, REQ-05, REQ-06):**
   - Tạo mới ghi chú văn bản thuần và ghi chú danh sách việc cần làm (Checklist to-do items).
   - Xem chi tiết và chỉnh sửa rich-text, cơ chế tự động lưu thời gian thực (Autosave sau 1-2.5s).
   - Ghim ghi chú (Pin Note - REQ-07) ưu tiên lên đầu danh sách Trang chủ.
   - Xóa mềm (Soft Delete - REQ-09): Chuyển ghi chú vào Thùng rác (`status = 'trash'`), khôi phục về trạng thái bình thường, và xóa vĩnh viễn khỏi SQLite / Firestore.
   - Lưu trữ ghi chú (Archive Note - REQ-09).
3. **Tìm kiếm & Bộ lọc Dữ liệu (Search & Filtering - REQ-08):**
   - Tìm kiếm từ khóa theo tiêu đề và nội dung: Tối ưu qua câu truy vấn SQLite `LOWER(...) LIKE ?` kết hợp loại trừ ghi chú trong thùng rác (`local_note_service.dart`).
   - Tìm kiếm tiếng Việt có dấu (theo quyết định `BR-01`, chấp nhận giới hạn SQLite `LIKE` đối với không dấu; ca `TC-BB-026B-D03` giữ nguyên trạng thái thực thi `CHƯA ĐỦ CĂN CỨ` và giải tỏa theo `BR-01`, không tự chuyển thành `PASS`).
   - Lọc đa phương tiện qua Token / Filter Chip: `has:image`, `has:audio`, `has:url`, `has:list` (Danh sách Checklist — ghi nhận `BUG-004` tại `TC-BB-027G-D01` do `local_note_service.dart` đẩy vào `LIKE` thô), `is:pinned`, `is:archived`, và nhãn `label:"..."`.
4. **Bảo mật Sinh trắc học & Khóa ứng dụng (Biometric Security - REQ-10, NFR-05):**
   - Khóa từng ghi chú riêng tư bằng vân tay/FaceID (`biometric_service.dart`).
   - Tự động chuyển về trạng thái khóa khi ứng dụng chuyển sang chạy ngầm (App Lifecycle State `paused`/`inactive`).
5. **Lưu trữ Cục bộ & Đồng bộ Đám mây (Offline-First & Cloud Sync - REQ-11, NFR-01, NFR-02):**
   - Đọc/ghi cơ sở dữ liệu SQLite cục bộ khi offline với độ trễ bằng 0.
   - Hàng đợi xóa ngoại tuyến (`pending_delete_service.dart`).
   - Thuật toán giải quyết xung đột Last-Write-Wins (LWW) dựa trên epoch timestamp của trường `updatedAt` (`sync_repository.dart`). Phân xử Sửa offline vs Xóa offline theo LWW (BR-02).
   - Kiểm soát quyền riêng tư và cô lập dữ liệu theo `request.auth.uid` trên Cloud Firestore (NFR-03, `test/security/security_rules_test.dart`, `firestore.rules`).

#### B. Nhóm Chuyên sâu chọn lọc (Priority: Medium / P2 — Trọng tâm đánh giá kỹ thuật)
1. **Toàn vẹn Dữ liệu Model & Biên chuyển đổi:**
   - Tuần tự hóa / giải mã `Note.toMap`, `Note.fromMap`, `_decodeStringList` với các trường hợp dữ liệu JSON chuẩn, fallback CSV legacy, chuỗi rỗng và kiểu dữ liệu bất thường.
   - Khởi tạo, tính bất biến của `ChecklistItem.copyWith`, đếm checklist `pendingChecklistCount` và bóc tách văn bản `plainTextContent`.
2. **Khả năng chịu lỗi & Mất mạng đột ngột (Fault Tolerance - NFR-01):**
   - Ngắt kết nối mạng (Airplane mode) trong khi soạn thảo; xác minh dữ liệu không bị mất và cờ `isSynced = false`.
   - Kết nối mạng trở lại; xác minh tiến trình Background Sync tự động đồng bộ lên Firestore.
3. **Lịch nhắc nhở theo Múi giờ & Khởi động nguội (Reminder & Lifecycle - REQ-12):**
   - Lập lịch thông báo chính xác theo múi giờ địa phương (`reminder_service.dart`, thư viện `timezone`).
   - Điều hướng trực tiếp vào ghi chú khi nhấn thông báo từ Cold Start (`getNotificationAppLaunchDetails`) và Background.

#### C. Nhóm Tiện ích mở rộng (Priority: Low / P3 — Kiểm tra điều kiện phụ thuộc)
1. **Tiện ích bổ trợ (REQ-12):** Xuất bản PDF (`pdf_export_service.dart`), Bảng vẽ tay (`drawing_screen.dart`), Quản lý nhãn (`manage_labels_screen.dart`), Đổi màu nền ghi chú (`FN-37`), Chuyển đổi layout Grid/List (`FN-28`).
2. **Trợ lý AI Gemini (REQ-13):** Tóm tắt nội dung (`FN-31`), đề xuất tiêu đề (`FN-32`), tạo checklist (`FN-33`) (`gemini_ai_service.dart`, `editor_screen_ai.dart`). Lịch sử thực thi Kịch bản 5 trên máy thật giữ nguyên **3 trường hợp `BLOCKED`** do lỗi hiển thị trên UI chưa xác định nguyên nhân kỹ thuật; 3 test case chính thức mới thiết kế (`TC-BB-032`, `TC-BB-032B`, `TC-BB-032C`) giữ trạng thái **`NOT RUN` (Chờ gỡ `BLOCKED`)**.

---

### 2.3. Phạm vi ngoài dự án (Out-of-Scope)
* **Nền tảng iOS:** Do thiếu môi trường máy chủ macOS và thiết bị phần cứng iPhone vật lý để build và chạy tự động.
* **Kiểm thử tải lớn (Stress / Load Testing hàng nghìn người dùng):** Dự án sử dụng gói dịch vụ Firebase Spark miễn phí, không hỗ trợ thử tải cường độ cao trên cụm server.
* **Penetration Testing chuyên sâu:** Không thực hiện tấn công dịch ngược file APK, can thiệp mã nhị phân native hay bypass SSL pinning.
* **Ràng buộc an toàn thiết bị thật:**
  - Không thực hiện thao tác xóa dấu vân tay hệ thống trên máy thật của tester (`TC-BB-015G-D01` xếp trạng thái **BLOCKED** an toàn).
  - Không cố tình ghi đè làm đầy bộ nhớ máy thật dẫn đến nguy cơ treo hệ điều hành (`FN-44` xếp trạng thái **BLOCKED** an toàn).
* **Kiểm thử liên kết ứng dụng bên ngoài (External Deep Link):** Không kiểm thử thao tác click link kích hoạt email từ app Gmail (`FN-03`) hoặc link đổi mật khẩu từ trình duyệt web ngoài (`FN-06`).
* **Độ bao phủ 100% toàn bộ codebase ứng dụng:** Không đặt mục tiêu bao phủ toàn bộ các widget hiển thị đồ họa thuần túy của Flutter framework.
* **Giới hạn 2.000 ký tự (BR-04):** Đã xác minh là UI Guideline thiết kế đề xuất, không áp dụng làm tiêu chí chặn cứng trong kiểm thử chức năng.

---

## 3. PHƯƠNG PHÁP VÀ CHIẾN LƯỢC KIỂM THỬ (TEST STRATEGY)

### 3.1. Các trục phân loại kiểm thử chuẩn hóa (Orthogonal Testing Dimensions)
Hệ thống kiểm thử áp dụng chiến lược đa chiều chuẩn hóa theo ISTQB và IEEE 829. Các cách phân loại dưới đây là **các trục kỹ thuật độc lập và có thể giao nhau (orthogonal dimensions)**, tuyệt đối không phải là các giai đoạn dự án tuần tự:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        CÁC TRỤC PHÂN LOẠI KIỂM THỬ CHUẨN HÓA                          │
├───────────────────────┬────────────────────────────────────────────────────────────────┤
│ TRỤC PHÂN LOẠI        │ CÁC PHÂN LỚP KỸ THUẬT ÁP DỤNG TRONG DỰ ÁN                      │
├───────────────────────┼────────────────────────────────────────────────────────────────┤
│ 1. Kỹ thuật thiết kế  │ • Black-box Testing (Phân vùng tương đương EP, Phân tích biên  │
│    (Test Design)      │   BVA, Bảng quyết định Decision Table, Chuyển đổi trạng thái)  │
│                       │ • White-box Testing (Line/Branch Coverage qua LCOV, CFG/V(G))  │
├───────────────────────┼────────────────────────────────────────────────────────────────┤
│ 2. Phương thức        │ • Manual Testing (Thực thi thủ công trên thiết bị thật)        │
│    thực thi           │ • Automated Testing (Kịch bản Python UI/E2E & Flutter Test)    │
├───────────────────────┼────────────────────────────────────────────────────────────────┤
│ 3. Mục tiêu kiểm thử  │ • Functional Testing (Xác thực, Ghi chú, Checklist, LWW...)    │
│    (Test Objectives)  │ • Non-functional Testing (Offline-First, Consistency, Security)│
├───────────────────────┼────────────────────────────────────────────────────────────────┤
│ 4. Cấp độ kiểm thử    │ • Unit Testing (Mô hình dữ liệu, hàm xử lý chuỗi in-memory)    │
│    (Test Levels)      │ • Integration Testing (State Provider, Security Rules, Storage)│
│                       │ • System Testing (End-to-End đa thiết bị trên Android 14)      │
└───────────────────────┴────────────────────────────────────────────────────────────────┘
```

1. **Kiểm thử Hộp đen (Black-Box Testing):**
   * **Phương pháp:** Phân vùng tương đương (EP), Phân tích giá trị biên (BVA), Bảng quyết định (Decision Table), Kiểm thử chuyển đổi trạng thái (State Transition Testing). Thực thi thủ công trên thiết bị thật kết hợp chụp ảnh màn hình làm bằng chứng.
   * **Lý do lựa chọn:** Ứng dụng di động có tương tác phong phú (Rich-text, cử chỉ vuốt, bàn phím ảo, chuyển cảnh). Kiểm thử hộp đen thẩm định chính xác phản ứng giao diện trên môi trường thực tế Android 14 mà unit test không thể mô phỏng.
2. **Kiểm thử Hộp trắng chọn lọc (Selective White-Box Testing):**
   * **Phương pháp:** Kiểm thử đơn vị (Unit Test) phân tích cấu trúc mã nguồn, đo lường độ bao phủ dòng (Statement/Line Coverage) và rẽ nhánh (Branch Coverage qua bản ghi BRDA) bằng LCOV qua lệnh `flutter test --coverage`.
   * **Phạm vi mã nguồn được đo:** Chỉ đo lường trên 2 file Data Model cốt lõi (`lib/models/checklist_item.dart` và `lib/models/note_model.dart`). Tuyệt đối **không đánh đồng độ bao phủ trên 2 model này với độ bao phủ của toàn bộ codebase `lib/`**.
   * **Công cụ và giới hạn kỹ thuật:**
     - Công cụ: `flutter test --coverage` kết hợp công cụ trích xuất LCOV.
     - Giới hạn: Bản ghi LCOV BRDA do Dart VM sinh ra biểu diễn các điểm rẽ nhánh và closure nội bộ của runtime, không tương đương 1:1 với nhánh nhị phân tiêu chuẩn trong lý thuyết kiểm thử; công cụ không tự động đo lường Condition Coverage hay Path Coverage.
     - Phân tích đồ thị dòng điều khiển (Control Flow Graph - CFG) và độ phức tạp Cyclomatic Complexity $V(G)$ được áp dụng ở mức độ thiết kế ca test lý thuyết cho các hàm xử lý dữ liệu phức tạp (`plainTextContent`, `pendingChecklistCount`), **không tuyên bố đã thực hiện đo lường Path Coverage tự động toàn diện**.
   * **Phân biệt với Security Rules Testing:** Kiểm thử Firestore Security Rules (`test/security/security_rules_test.dart`) là kiểm thử **mô phỏng logic quy tắc bằng Dart trong bộ nhớ (Dart Rule Logic Simulation)**, không phải chạy trên Firebase Local Emulator Suite thực tế và không phải là Unit Test mã nguồn Dart của ứng dụng `lib/`.
3. **Kiểm thử Tự động hóa (Automation Testing):**
   * **Phương pháp:** Kiến trúc tự động 2 tầng gồm kịch bản Python E2E (pytest + uiautomator2 + ADB trong `automation/tests/`) và kịch bản Flutter Native Component Test (`test/automated/`).
   * **Lý do lựa chọn:** Giảm thiểu công sức kiểm thử hồi quy cho các luồng cốt lõi (Đăng ký, Đăng nhập, Tạo/Sửa ghi chú, Ghim, Tìm kiếm, Quản lý trạng thái Provider).
4. **Kiểm thử Phi chức năng (Non-Functional Testing):**
   * **Phương pháp:** Kiểm tra tính khả dụng Offline-First (NFR-01) qua ngắt mạng vật lý; kiểm tra tính nhất quán LWW (NFR-02) qua xung đột 2 thiết bị; kiểm tra an toàn dữ liệu người dùng (NFR-03) qua Security Rules; kiểm tra độ bền nhập liệu (NFR-04) qua SQL Injection payload; kiểm tra bảo vệ vòng đời ứng dụng (NFR-05) qua sinh trắc học khi app paused.

---

### 3.2. Bảng phân loại ca kiểm thử đa chiều (Multi-Dimensional Classification Matrix)

| Mã nhóm / Test Case | Hộp đen | Hộp trắng | Tự động | Thủ công | Chức năng | Phi chức năng | Cấp độ kiểm thử | Trạng thái thực thi |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `TC-BB-001` .. `005` (Auth FN-02) | X | | X | X | X | | System / UI | 18 PASS / 1 FAIL (`BUG-FN02-01`) |
| `TC-BB-006` .. `009` (Login FN-04) | X | | X | X | X | | System / UI | 14 PASS / 2 FAIL (`BUG-BB-002`, `003`) |
| `test/unit/note/checklist_model_test.dart` (5 tests) | | X | X | | X | | Unit (Model) | 5 PASS (Baseline) |
| `test/unit/note/checklist_copy_with_test.dart` (4 tests) | | X | X | | X | | Unit (Model) | 4 PASS (Baseline) |
| `test/unit/note/note_model_test.dart` (9 tests) | | X | X | | X | | Unit (Model) | 9 PASS (Baseline) |
| `test/security/security_rules_test.dart` (8 tests baseline) | | X | X | | X (`REQ-11`) | X (`NFR-03`) | Integration (Rule Simulation) | 8 PASS (Simulation) |
| `TC-BB-026` .. `029` (Search FN-23, 22 items) | X | | X | X | X | X (`NFR-04` SQLi) | System / UI | 20 PASS / 1 FAIL (`BUG-004`) / 1 BR-01 |
| `TC-BB-012` .. `015F` (Biometrics FN-29/30) | X | | | X | X | X (`NFR-05` Lifecycle)| System / Sensor | 11 PASS / 1 BLOCKED an toàn |
| `TC-BB-030` .. `031D` (Sync LWW FN-40/41) | X | | X | X | X | X (`NFR-01/02` LWW) | System / Multi-device | 7 PASS / 2 FAIL (`BUG-002`, `003`) / 1 BR-02 |
| `TC-WB-015` .. `022` (8 White-box mở rộng) | | X | X | | X | | Unit (In-Memory) | `DESIGN ONLY / READY` (Chưa chạy) |

---

## 4. MÔI TRƯỜNG, THIẾT BỊ, TÀI KHOẢN VÀ CÔNG CỤ THỰC HIỆN

### 4.1. Môi trường phần cứng và thiết bị kiểm thử thực tế đã sử dụng
* **Thiết bị A (Primary Target Device — Thiết bị kiểm thử chính):**
  - Dòng máy: Samsung Galaxy S21 FE 5G (Model: SM-G990E/DS).
  - Hệ điều hành: Android 14 (Giao diện One UI 6.1, Android API Level 34).
  - Độ phân giải màn hình: $1080 \times 2340$ pixels.
  - Vai trò kiểm thử: Thực thi toàn bộ 11 nhóm Black-box, kiểm thử UI thủ công, chạy kiểm thử tự động Python E2E và đóng vai trò Thiết bị 1 trong kịch bản đồng bộ đa máy.
* **Thiết bị B (Secondary Target Device — Thiết bị đối chứng đồng bộ):**
  - Dòng máy: Samsung Galaxy S24 FE (Model: SM-S741B).
  - Hệ điều hành: Android 14 (Android API Level 34).
  - Vai trò kiểm thử: Đóng vai trò Thiết bị 2 chuyên dụng cho kiểm thử đồng bộ đám mây đa thiết bị (`FN-40`), tái hiện tranh chấp Last-Write-Wins (`FN-41`), và xác minh khiếm khuyết thiếu Tombstone (`BUG-002`).
* **Máy trạm điều khiển (Host Workstation):**
  - Hệ điều hành: Windows (x86_64).
  - Flutter SDK: Phiên bản `3.44.1 • channel stable`, Dart SDK `3.x`.
  - Python Runtime: Python 3.13 (thư viện `pytest`, `uiautomator2`).
  - Android Platform Tools: Android Debug Bridge (`adb`).

### 4.2. Phân biệt môi trường thực tế và môi trường khuyến nghị dự kiến
* **Môi trường thực tế đã sử dụng:** Sử dụng 100% thiết bị vật lý thật (Samsung S21 FE và S24 FE) để đảm bảo tính xác thực tối đa cho các tương tác phần cứng (cảm biến vân tay, chuyển cảnh màn hình, kết nối Wi-Fi thực tế).
* **Môi trường khuyến nghị dự kiến (Sandbox / Emulator):** Đối với các ca kiểm thử có nguy cơ ảnh hưởng phần cứng hoặc dữ liệu cá nhân của tester (xóa vân tay hệ thống ở `TC-BB-015G-D01` hoặc làm đầy bộ nhớ ở `FN-44`), môi trường dự kiến bắt buộc là **Android Virtual Device (AVD / Emulator)** có khả năng snapshot khôi phục. Do hiện tại chưa thiết lập môi trường máy ảo cô lập, các ca này được phân loại an toàn là **`BLOCKED`**.

---

## 5. TIẾN ĐỘ VÀ BẰNG CHỨNG ĐÃ GHI NHẬN (BASELINE AUDIT)

### 5.1. Kết quả Kiểm thử Hộp trắng (Baseline 18/18 Unit Tests PASS)
- **Trạng thái thực thi:** **18/18 Unit Tests PASS (100%)**, Exit Code: `0` (xác thực qua log `evidence/white_box/note_model_run_20261010_0945/test_execution.log`).
  - `test/unit/note/checklist_model_test.dart` (tên log gốc: `test/checklist_test.dart`): 5 tests PASS.
  - `test/unit/note/checklist_copy_with_test.dart`: 4 tests PASS.
  - `test/unit/note/note_model_test.dart`: 9 tests PASS (Bao phủ `toMap`, `fromMap`, `_decodeStringList`).
- **Độ bao phủ thực tế trên phạm vi đo lường 2 Model (`ChecklistItem` & `NoteModel`):**
  - **`lib/models/checklist_item.dart`:** 14/14 dòng lệnh (**100.0%**).
  - **`lib/models/note_model.dart`:** 55/124 dòng lệnh (**44.35%**).
  - **Tổng Line Coverage trên phạm vi 2 Model:** 69/138 dòng lệnh (**50.00%**).
  - **LCOV BRDA (Branch records):** 21/41 bản ghi (**51.22%**).
- **Vị trí lưu trữ Bằng chứng & Mã băm SHA-256 xác thực:**
  - Checksum `test_execution.log`: `d8448a1d37547defb293b5326b6e6147e495c890aba93ed63f389376505bf00e`.
  - Checksum `lcov.info`: `c5244d2a160ef10b33f272b6abebf7b0828e1bacee9fc49dbc07d1ad04c05324`.
- **Giới hạn kỹ thuật đã ghi nhận (Không suy đoán):**
  - Độ bao phủ 50.00% dòng chỉ áp dụng cho 2 file model được đo, **không đại diện cho toàn bộ codebase `lib/`**.
  - Các module `SearchService` và `EncryptionService` chưa nằm trong baseline 18 unit tests do chưa có log thực thi tương ứng trong đợt chạy này.
  - 8 bài test Security Rules trong `test/security/security_rules_test.dart` đạt trạng thái PASS về mặt logic mô phỏng bằng Dart trong bộ nhớ, không tính lẫn vào coverage của mã nguồn ứng dụng `lib/`.

### 5.2. Kết quả Kiểm thử Hộp đen (Baseline 140 Execution Items)
- **Phạm vi chốt:** 11 nhóm có Execution Sheet (10 nhóm ban đầu + Checklist FN-15..19).
- **Tổng số Execution Items:** **140 items**.
  - **Số ca đã thực thi (Executed — không tính BLOCKED):** **139 items** (chiếm **99.29%** trên tổng 140 items).
  - **Số ca ĐẠT (PASS):** **131 items** (chiếm **94.24%** trên 139 executed; chiếm **93.57%** trên tổng 140 items).
  - **Số ca THẤT BẠI (FAIL):** **6 items** (chiếm **4.32%** trên 139 executed; chiếm **4.29%** trên tổng 140 items) — ánh xạ trực tiếp vào các lỗi phần mềm đã ghi nhận.
  - **Số ca CHƯA ĐỦ CĂN CỨ:** **2 items** (chiếm **1.44%** trên 139 executed; chiếm **1.43%** trên tổng 140 items) — gồm `TC-BB-026B-D03` (giải tỏa theo `BR-01`) và `TC-BB-031C-D01` (giải tỏa theo `BR-02`), giữ nguyên trạng thái gốc, không tự chuyển thành `PASS`.
  - **Số ca BỊ CHẶN (BLOCKED):** **1 item** (chiếm **0.71%** trên tổng 140 items) — ca `TC-BB-015G-D01` do ràng buộc an toàn thiết bị thật.
  - **Số ca chờ (Pending):** **0 items** (**0.00%**).
  - **Kiểm chứng phép cộng:** $131\ (\text{PASS}) + 6\ (\text{FAIL}) + 2\ (\text{Chưa đủ căn cứ}) + 1\ (\text{BLOCKED}) = \mathbf{140\ \text{items}}\ (100.00\%)$.

### 5.3. Kết quả Kiểm thử Tự động hóa (Automation Baseline Audit)
- **Tầng 1 (Android UI/E2E Testing):** 20 Test Cases thực thi trên thiết bị thật Samsung S21 FE:
  - Kết quả: **16 PASS / 4 FAIL** (Tỷ lệ PASS: **80.00%**).
  - Bằng chứng: JUnit XML trong `automation/reports/` và screenshots trong `evidence/`.
- **Tầng 2 (Flutter Provider Automated Testing):** 24 Tests thực thi in-memory qua Flutter Test:
  - Kết quả: **24/24 PASS** (**100.00%**).
  - Bao phủ 10 FNs: `FN-08`, `FN-09`, `FN-10`, `FN-11`, `FN-12`, `FN-13`, `FN-14`, `FN-20`, `FN-23`, `FN-40`.
  - Bằng chứng: Log thực thi tại [`evidence/automated/automated_test_run.log`](../../evidence/automated/automated_test_run.log).
- **Tổng số kịch bản tự động hóa:** **44 kịch bản** (**40 PASS / 4 FAIL**, Tỷ lệ PASS: **90.91%**).
- **Ranh giới số liệu:** Số liệu kiểm thử tự động hóa được theo dõi riêng biệt, không cộng gộp lẫn lộn với 140 execution items của kiểm thử hộp đen thủ công.

---

## 6. THEO DÕI PHẠM VI VÀ KẾ HOẠCH RETEST / REGRESSION CHO CÁC LỖI ĐÃ BIẾT

### 6.1. Bảng theo dõi phạm vi 11 nhóm chức năng chính thức
*(Đường dẫn file Execution Sheet được đối chiếu chính xác theo cấu trúc thư mục repository)*:

| STT | Nhóm chức năng | File Execution Sheet tham chiếu | Số Exec Items | PASS | FAIL | Chưa đủ căn cứ | BLOCKED | Trạng thái nhóm |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | **FN-02:** Đăng ký Email/Password | [`fn02_execution_sheet.md`](../test_cases/black_box/fn02_execution_sheet.md) | 19 | 18 | 1 | 0 | 0 | Đã chạy (1 Bug validation `BUG-FN02-01`) |
| 2 | **FN-04:** Đăng nhập Email/Form | [`fn04_execution_sheet.md`](../test_cases/black_box/fn04_execution_sheet.md) | 16 | 14 | 2 | 0 | 0 | Đã chạy (2 Bugs `BUG-BB-002`, `BUG-BB-003`) |
| 3 | **FN-05:** Đăng nhập Google OAuth | [`fn05_execution_sheet.md`](../test_cases/black_box/fn05_execution_sheet.md) | 8 | 8 | 0 | 0 | 0 | PASS 100% |
| 4 | **FN-08:** Tạo ghi chú & Autosave | [`fn08_execution_sheet.md`](../test_cases/black_box/fn08_execution_sheet.md) | 8 | 8 | 0 | 0 | 0 | PASS 100% |
| 5 | **FN-09:** Rich-text & Cập nhật note | [`fn09_execution_sheet.md`](../test_cases/black_box/fn09_execution_sheet.md) | 12 | 12 | 0 | 0 | 0 | Đã chạy (1 Glitch `BUG-005`) |
| 6 | **FN-10/11/12:** Thùng rác & Lưu trữ | [`fn10_fn11_fn12_execution_sheet.md`](../test_cases/black_box/fn10_fn11_fn12_execution_sheet.md) | 12 | 12 | 0 | 0 | 0 | PASS 100% |
| 7 | **FN-15..19:** Ghi chú Checklist | [`fn15_fn19_checklist_execution_sheet.md`](../test_cases/black_box/fn15_fn19_checklist_execution_sheet.md) | 6 | 6 | 0 | 0 | 0 | PASS 100% |
| 8 | **FN-20:** Ghim ghi chú (Pin) | [`fn20_execution_sheet.md`](../test_cases/black_box/fn20_execution_sheet.md) | 15 | 15 | 0 | 0 | 0 | PASS 100% |
| 9 | **FN-23:** Tìm kiếm & Bộ lọc | [`fn23_execution_sheet.md`](../test_cases/execution_sheets/fn23_execution_sheet.md) | 22 | 20 | 1 | 1 | 0 | Đã chạy 22/22 (1 Bug `BUG-004`; 1 ca theo BR-01) |
| 10 | **FN-29/30:** Bảo mật sinh trắc học | [`fn29_fn30_execution_sheet.md`](../test_cases/black_box/fn29_fn30_execution_sheet.md) | 12 | 11 | 0 | 0 | 1 | Đã chạy (1 BLOCKED an toàn vân tay) |
| 11 | **FN-40/41:** Đồng bộ Offline LWW | [`fn40_fn41_execution_sheet.md`](../test_cases/black_box/fn40_fn41_execution_sheet.md) | 10 | 7 | 2 | 1 | 0 | Đã chạy (2 Bugs `BUG-002`, `BUG-003`; 1 ca theo BR-02) |
| **Tổng** | **11 nhóm chính thức** | **11 execution sheets** | **140** | **131** | **6** | **2** | **1** | **100% PHÂN ĐỊNH MINH BẠCH** |

---

### 6.2. Kế hoạch Retest và Regression cho các lỗi đã biết
Toàn bộ 8 lỗi phần mềm từ kiểm thử hộp đen được quản lý chính thức tại [defect_log.md](../bugs/defect_log.md). Kế hoạch kiểm thử lại khi Developer bàn giao bản sửa lỗi như sau:

| Mã Bug | Mức nghiêm trọng | Tóm tắt lỗi | Ca Retest trực tiếp (Direct Retest) | Phạm vi kiểm thử hồi quy (Regression Scope) |
|:---|:---:|:---|:---|:---|
| **BUG-001** | High | Tải ảnh lên Cloudinary bị treo vô hạn thiếu timeout | `TC-BB-018C`, `TC-BB-027B-D01`, `TC-BB-036` (Tải ảnh từ thư viện, kiểm tra timeout 30s và bắt lỗi mạng) | • Tạo ghi chú văn bản thuần (`FN-08`)<br>• Đính kèm nét vẽ tay (`FN-35`)<br>• Lưu trữ và mở lại ghi chú có ảnh |
| **BUG-002** | Critical | Xóa note offline không sync xóa sang thiết bị khác do thiếu Tombstone | `TC-BB-030C-D01` (Xóa vĩnh viễn trên Thiết bị A khi offline, bật mạng lại, kiểm tra Thiết bị B) | • Tạo / Sửa ghi chú offline đa thiết bị (`FN-40`)<br>• Khôi phục ghi chú từ Thùng rác (`FN-11`)<br>• Tính nhất quán của `pending_delete_service.dart` |
| **BUG-003** | Medium | HomeScreen thiếu cử chỉ vuốt kéo làm mới (Pull-to-refresh) | `TC-BB-030F-D01` (Kéo vuốt màn hình Trang chủ trên Thiết bị B để cập nhật note từ Thiết bị A) | • Danh sách hiển thị ghi chú Trang chủ (`HomeScreen`)<br>• Vị trí nhóm ghi chú ghim / không ghim (`FN-20`)<br>• Cuộn danh sách Grid / List view (`FN-28`) |
| **BUG-004** | Medium | Bộ lọc `has:list` query LIKE thô, trả về rỗng | `TC-BB-027G-D01` (Chạm chip 'Danh sách' hoặc gõ `has:list` trên SearchScreen) | • Các bộ lọc chip khác: `has:image`, `has:audio`, `has:url`, `is:pinned`, `is:archived`, `label:name`<br>• Tìm kiếm từ khóa text thông thường qua SQL LIKE (`FN-23`) |
| **BUG-005** | Minor | Vệt sọc vàng đen tràn viền thoáng qua khi xóa trắng tiêu đề/nội dung | Luồng xóa trắng tiêu đề (TH1) và nội dung (TH2) rồi nhấn Back về Home | • Hiển thị NoteCard trên Trang chủ<br>• Thao tác đổi màu ghi chú (`FN-37`)<br>• Autosave khi thoát màn hình Editor |
| **BUG-FN02-01** | Minor | Lỗi validation chuỗi form Đăng ký | `TC-BB-002`, `TC-BB-003` (Nhập email không hợp lệ, mật khẩu ngắn) | • Toàn bộ luồng đăng ký tài khoản thành công (`TC-BB-001`) |
| **BUG-BB-002** | Minor | Thông báo lỗi gộp Firebase khi đăng nhập tài khoản chưa tồn tại | `TC-BB-008` (Nhập email chưa từng đăng ký: `ghost_user@gmail.com`) | • Đăng nhập với tài khoản hợp lệ / không hợp lệ (`TC-BB-006`, `TC-BB-007`) |
| **BUG-BB-003** | Minor | Thông báo lỗi gộp Firebase khi đăng nhập sai mật khẩu | `TC-BB-007` (Nhập sai mật khẩu: `WrongPass999`) | • Đăng nhập với mật khẩu đúng (`TC-BB-006`) |

---

### 6.3. Kế hoạch quản lý và xử lý các ca BỊ CHẶN (BLOCKED Cases)

> [!CAUTION]
> **Quy tắc bất biến:** Tuyệt đối **KHÔNG TÍNH CÁC CA BLOCKED LÀ PASS**. Các ca bị chặn phải giữ nguyên trạng thái `BLOCKED` trong mọi bảng thống kê cho đến khi điều kiện tiên quyết được tháo gỡ.

1. **Trợ lý Gemini AI (`FN-31`, `FN-32`, `FN-33` - REQ-13):**
   * **Hiện trạng:** Trong đợt thực thi thủ công Kịch bản 5 trên máy thật ([Testing_Report.md](../test_report/Testing_Report.md) / [black_box_execution_summary.md](../qa/black_box_execution_summary.md)), 3 trường hợp `FN-31..33` bị chặn (**`3 BLOCKED`**) do giao diện trả về khung thông báo lỗi màu đỏ trên máy thật. Ba ca kiểm thử chính thức mới được thiết kế tại [black_box_test_cases.md](../test_cases/black_box/black_box_test_cases.md) và [test_case_design_inventory_44_fn.md](./test_case_design_inventory_44_fn.md) gồm `TC-BB-032` (`FN-31`), `TC-BB-032B` (`FN-32`), `TC-BB-032C` (`FN-33`) giữ trạng thái **`NOT RUN` (Chưa có evidence riêng — chờ gỡ `BLOCKED`)**.
   * **Nguyên nhân kỹ thuật:** **Chưa xác định** (chưa có log response HTTP chi tiết hay exception từ Firebase AI SDK trong logcat; tuyệt đối không suy đoán do quota hay API key khi chưa có bằng chứng xác thực).
   * **Điều kiện tháo gỡ (Unblock Criteria):** Developer / DevOps cấu hình môi trường AI API hoạt động ổn định và trích xuất logcat chi tiết để thực thi 3 ca `TC-BB-032`, `TC-BB-032B`, `TC-BB-032C`.
2. **Xóa dấu vân tay hệ thống (`TC-BB-015G-D01` - FN-29/FN-30):**
   * **Hiện trạng:** Bị chặn do quy tắc an toàn thiết bị thật (tránh làm mất cấu hình bảo mật cá nhân trên điện thoại thật của tester).
   * **Điều kiện tháo gỡ:** Chỉ thực thi khi có môi trường máy ảo Android Emulator cô lập chuyên dụng. Trong điều kiện thiết bị hiện tại, ca này giữ nguyên trạng thái `BLOCKED` an toàn.
3. **Làm đầy bộ nhớ thiết bị (`FN-44`):**
   * **Hiện trạng:** Bị chặn do nguy cơ gây treo hệ điều hành thiết bị thật.
   * **Điều kiện tháo gỡ:** Giữ nguyên trạng thái `BLOCKED` an toàn; chỉ thực thi trên môi trường sandbox có khả năng snapshot khôi phục.

---

## 7. CÁC MỐC KỸ THUẬT, LỊCH THỰC HIỆN VÀ PHÂN CÔNG (SCHEDULE & RESOURCES)

### 7.1. Các mốc kỹ thuật (Milestones)

```
[Mốc 1: Baseline & Condensed SRS] ──────► (HOÀN THÀNH - Giai đoạn 1 đóng)
                 │
                 ▼
[Mốc 2: Master Test Plan & Strategy] ───► (HOÀN THÀNH - Giai đoạn 2 đóng)
                 │
                 ▼
[Mốc 3: Kiểm tra Tiến độ Môn học] ──────► (XÁC NHẬN: Ngày 14/10/2026)
                 │
                 ▼
[Mốc 4: Mở khóa Defects & Retest] ──────► (Phụ thuộc Dev cung cấp bản build sửa lỗi)
                 │
                 ▼
[Mốc 5: Nghiệm thu & Đóng gói Đồ án] ───► (Hạn nộp chính thức: Chưa công bố / Chưa xác nhận)
```

### 7.2. Lịch thực hiện và Bảng phân công chi tiết (Work Allocation & Responsibilities)
Bảng dưới đây tổng hợp phân công trách nhiệm cho các gói công việc kiểm thử của dự án trên branch `huong`. Các vị trí chưa được chỉ định đích danh nhân sự trong tài liệu gốc được ghi nhận minh bạch là `CHƯA XÁC NHẬN` (không tự ý suy đoán danh tính):

| Gói công việc / Loại kiểm thử | Người / Nhóm phụ trách | Sản phẩm bàn giao (Deliverable) | Trạng thái thực hiện |
|---|:---:|---|:---:|
| **1. Đặc tả yêu cầu & Truy vết (SRS & RTM)** | Nhóm QA (Branch `huong`) | `srs_condensed.md`, `requirements_traceability_matrix.md` | **Hoàn thành** |
| **2. Kế hoạch kiểm thử tổng thể (Master Test Plan)** | Nhóm QA (Branch `huong`) | `test_plan.md` | **Hoàn thành** |
| **3. Thiết kế ca kiểm thử 44 FN (Test Design)** | Nhóm QA (Branch `huong`) | `test_case_design_inventory_44_fn.md`, `black_box_test_cases.md` | **Hoàn thành** |
| **4. Thực thi kiểm thử Hộp đen thủ công (Manual Execution)** | `CHƯA XÁC NHẬN` | 11 Execution Sheets, `black_box_execution_summary.md`, Screenshots | **Hoàn thành (140 Items)** |
| **5. Thực thi kiểm thử Tự động hóa UI/E2E (Python)** | `CHƯA XÁC NHẬN` | Scripts `automation/tests/`, JUnit Reports, Evidence | **Hoàn thành (20 TCs)** |
| **6. Tích hợp & Chạy Provider Automated Tests (Dart)** | `CHƯA XÁC NHẬN` | `test/automated/`, `automated_test_run.log` | **Hoàn thành (24 Tests)** |
| **7. Kiểm thử Hộp trắng Baseline (Unit Models)** | `CHƯA XÁC NHẬN` | `test/unit/note/`, `test_execution.log`, `lcov.info` | **Hoàn thành (18 Tests PASS)** |
| **8. Kế hoạch mở rộng Hộp trắng (Selective Extension)** | Nhóm QA (Branch `huong`) | `white_box_test_plan.md`, `white_box_test_cases.md` | **Hoàn thành thiết kế (Frozen)** |
| **9. Quản lý lỗi & Phân tích nguyên nhân (Defect Tracking)** | Nhóm QA (Branch `huong`) | `defect_log.md` (8 Black-box bugs + White-box findings) | **Hoàn thành (Đang theo dõi)** |
| **10. Báo cáo tiến độ ngày 14/10/2026** | Nhóm QA (Branch `huong`) | `progress_check_slides_outline.md`, Demo trên S21 FE & S24 FE | **Sẵn sàng báo cáo** |
| **11. Thực hiện Retest & Regression sau sửa lỗi** | `CHƯA XÁC NHẬN` | Báo cáo Retest, cập nhật trạng thái Defect Log | **Chờ bàn giao bản build fix** |
| **12. Nghiệm thu cuối kỳ & Báo cáo tổng kết** | Nhóm QA (Branch `huong`) | `Testing_Report.md` hoàn thiện | **Chờ lịch công bố của Giảng viên** |

---

## 8. TIÊU CHÍ BẮT ĐẦU, TẠM DỪNG, TIẾP TỤC VÀ KẾT THÚC (CRITERIA & SEVERITY)

### 8.1. Phân loại mức độ nghiêm trọng của lỗi (Defect Severity Levels)
* **Critical (Blocker - Severity 1):** Lỗi gây crash ứng dụng, mất dữ liệu người dùng, hoặc sai lệch dữ liệu đồng bộ nghiêm trọng giữa các thiết bị mà không có giải pháp thay thế (ví dụ: `BUG-002` thiếu Tombstone làm tồn tại vĩnh viễn note đã xóa trên client khác).
* **High (Major - Severity 2):** Tính năng chính bị tê liệt hoặc treo vô hạn, làm nghẽn các ca kiểm thử khác nhưng ứng dụng không crash (ví dụ: `BUG-001` upload ảnh treo vô hạn thiếu timeout).
* **Medium (Normal - Severity 3):** Tính năng nghiệp vụ hoạt động sai logic hoặc không phản hồi đúng mong đợi nhưng có giải pháp tạm thời (ví dụ: `BUG-003` thiếu pull-to-refresh, `BUG-004` lọc `has:list` trả về rỗng).
* **Low (Minor - Severity 4):** Lỗi thẩm mỹ, vệt giao diện chớp nhoáng, lỗi validate chuỗi nhỏ, không ảnh hưởng đến dữ liệu hay luồng nghiệp vụ chính (ví dụ: `BUG-005` vệt tràn viền thoáng qua, `BUG-BB-002` icon toggle password).

### 8.2. Tiêu chí Bắt đầu (Entry Criteria)
* Mã nguồn ứng dụng trên branch `huong` biên dịch thành công, không có lỗi phân tích tĩnh cú pháp.
* Thiết bị kiểm thử (Samsung S21 FE và Samsung S24 FE) kết nối ổn định qua ADB (`adb devices`).
* Kế hoạch kiểm thử (Test Plan) và tài liệu yêu cầu (Condensed SRS) đã được phê duyệt.
* Tài khoản kiểm thử và tập dữ liệu mẫu đã sẵn sàng trên môi trường thực nghiệm.

### 8.3. Tiêu chí Tạm dừng (Suspension Criteria)
Kiểm thử phải **ngay lập tức tạm dừng** khi:
1. Phát sinh lỗi Critical khiến ứng dụng crash liên tục ngay khi khởi động hoặc treo màn hình chính.
2. Thiết bị mất kết nối ADB, mất quyền truy cập Firebase, hoặc dịch vụ phụ thuộc ngắt kết nối diện rộng.
3. Chế độ `--fail-fast` trong test suite tự động phát hiện test assertion thất bại (dừng lại để cách ly dữ liệu và phân tích log).

### 8.4. Tiêu chí Tiếp tục (Resumption Criteria)
* Lỗi Blocker đã được cô lập hoặc có bản vá tạm thời được phê duyệt.
* Kết nối thiết bị hoặc dịch vụ đám mây được phục hồi ổn định.
* Dữ liệu kiểm thử trên thiết bị đã được dọn sạch về trạng thái chuẩn (Clean State).

### 8.5. Tiêu chí Hoàn thành (Exit Criteria) & Đánh giá trạng thái thực tế
1. **Tiêu chuẩn hoàn thành theo thiết kế lý thuyết (Target Acceptance Criteria):**
   - 100% các yêu cầu nghiệp vụ cốt lõi (P1) đã được kiểm thử và đạt trạng thái PASS.
   - Không còn lỗi mức độ **Critical** hoặc **High** ở trạng thái **OPEN**.
   - Toàn bộ các ca BLOCKED được giải trình minh bạch lý do và phân định ranh giới rõ ràng.
   - Mọi lượt chạy test đều có bằng chứng log/screenshot được lưu trữ với mã băm xác thực.
2. **Đánh giá trạng thái thực tế đối chiếu (Actual Status vs Exit Criteria):**
   - **Đánh giá nghiệm thu phát hành (Release Decision):** Hiện tại dự án **CHƯA ĐẠT Exit Criteria để nghiệm thu bàn giao chính thức (Final Release)** vì hệ thống vẫn còn **1 lỗi Critical (`BUG-002`)** và **1 lỗi High (`BUG-001`)** đang ở trạng thái **OPEN** trong Backlog Retest. Việc phân tích nguyên nhân gốc và lập kế hoạch sửa lỗi KHÔNG tương đương với việc lỗi đã được giải quyết.
   - **Đánh giá mốc kiểm tra tiến độ môn học (Progress Milestone Check - 14/10/2026):** Dự án **ĐẠT YÊU CẦU NGHIỆM THU TIẾN ĐỘ** nhờ hồ sơ kiểm thử minh bạch 100%, 140 execution items được phân định rõ ràng, baseline hộp trắng và tự động hóa có bằng chứng kiểm chứng đầy đủ.

---

## 9. QUY TẮC QUẢN LÝ BẰNG CHỨNG VÀ SẢN PHẨM BÀN GIAO

### 9.1. Quy tắc Lưu trữ Bằng chứng (Evidence Integrity Rules)
* **Quy chuẩn đặt tên ảnh:** `FN<Mã_Chức_Năng>_TC-BB-<Mã_Test_Case>_D<Mã_Dữ_Liệu>_<Số_Thứ_Tự>.png`.
* **Tính nguyên vẹn:** Ảnh chụp màn hình phải giữ nguyên thanh trạng thái hệ thống và giao diện ứng dụng, không cắt ghép chỉnh sửa.
* **Quy chuẩn Log & LCOV:** Mỗi lượt chạy kiểm thử tự động/hộp trắng phải được lưu trong thư mục riêng biệt kèm dấu thời gian và mã băm SHA-256 xác thực.

### 9.2. Danh mục Sản phẩm bàn giao (Deliverables)
*(Tất cả đường dẫn đều được đối chiếu chính xác với cây thư mục thực tế của repository)*:

1. **Đặc tả yêu cầu rút gọn:** [srs_condensed.md](./srs_condensed.md)
2. **Kế hoạch kiểm thử tổng thể:** [test_plan.md](./test_plan.md)
3. **Kế hoạch kiểm thử hộp trắng chọn lọc:** [white_box_test_plan.md](./white_box_test_plan.md)
4. **Ma trận truy vết yêu cầu:** [requirements_traceability_matrix.md](./requirements_traceability_matrix.md)
5. **Bảng kiểm kê thiết kế 44 chức năng:** [test_case_design_inventory_44_fn.md](./test_case_design_inventory_44_fn.md)
6. **Đặc tả kịch bản kiểm thử hộp đen:** [black_box_test_cases.md](../test_cases/black_box/black_box_test_cases.md)
7. **Đặc tả kịch bản kiểm thử hộp trắng:** [white_box_test_cases.md](../test_cases/white_box/white_box_test_cases.md)
8. **Hồ sơ 11 Execution Sheets:**
   - 10 Execution Sheets trong thư mục [`docs/test_cases/black_box/`](../test_cases/black_box/): `fn02`, `fn04`, `fn05`, `fn08`, `fn09`, `fn10_fn11_fn12`, `fn15_fn19_checklist`, `fn20`, `fn29_fn30`, `fn40_fn41`.
   - 1 Execution Sheet trong thư mục [`docs/test_cases/execution_sheets/`](../test_cases/execution_sheets/): [`fn23_execution_sheet.md`](../test_cases/execution_sheets/fn23_execution_sheet.md).
9. **Nhật ký quản lý lỗi:** [defect_log.md](../bugs/defect_log.md)
10. **Báo cáo thực thi kiểm thử hộp đen:** [black_box_execution_summary.md](../qa/black_box_execution_summary.md)
11. **Báo cáo và hiện trạng kiểm thử tự động:** [automation_execution_summary.md](../qa/automation_execution_summary.md) và [automation_status.md](../qa/automation_status.md)
12. **Báo cáo kiểm thử tổng kết học phần:** [Testing_Report.md](../test_report/Testing_Report.md)
13. **Dàn ý Slide báo cáo tiến độ:** [progress_check_slides_outline.md](../test_report/progress_check_slides_outline.md)

---

## 10. RỦI RO, GIỚI HẠN VÀ QUY TẮC NGHIỆP VỤ MỞ BR-03

### 10.1. Xử lý các Quy tắc nghiệp vụ biên (Business Rules)
1. **BR-01 (Tìm kiếm tiếng Việt không dấu):** Mã nguồn `local_note_service.dart` sử dụng SQLite `LOWER(...) LIKE ?`. SQLite mặc định không hỗ trợ unaccented folding. Đã xác nhận chính thức: Chấp nhận giới hạn kỹ thuật của SQLite, ca `TC-BB-026B-D03` giữ nguyên trạng thái gốc `CHƯA ĐỦ CĂN CỨ` trong execution sheet và được giải tỏa theo `BR-01`, không tự chuyển thành `PASS`.
2. **BR-02 (Xung đột Sửa offline vs Xóa thùng rác offline):** Đã xác nhận chính thức: Tuân thủ thuật toán Last-Write-Wins (LWW) căn cứ trên mốc `updatedAt` muộn hơn. Ca `TC-BB-031C-D01` giữ nguyên trạng thái gốc `CHƯA ĐỦ CĂN CỨ` và được giải tỏa theo `BR-02`.
3. **BR-03 (Tie-break Rule khi trùng millisecond `updatedAt`):**
   * **Hiện trạng mã nguồn:** Trong [lib/repositories/sync_repository.dart](../../lib/repositories/sync_repository.dart#L67-L129), cả chiều Push và Pull đều dùng toán tử so sánh ngặt `isAfter`. Khi hai bản ghi Local và Cloud có cùng mốc thời gian `updatedAt` từng millisecond (`isAtSameMomentAs`), cả hai biểu thức `isAfter` đều trả về `false`.
   * **Ảnh hưởng kỹ thuật:** Gây hiện tượng bế tắc đồng bộ (Sync Standoff) và cờ `is_synced` giữ nguyên `0`.
   * **Quyết định xử lý trong Test Planning:**
     - Giữ nguyên trạng thái **`NEEDS CONFIRMATION (CẦN XÁC NHẬN NGHIỆP VỤ)`**.
     - **Tuyệt đối không tự ý chọn bản Cloud hay bản Local** làm chuẩn.
     - Ca kiểm thử hộp trắng **`TC-WB-021`** giữ trạng thái **`DESIGN ONLY`** (chỉ xác minh toán tử `DateTime.isAfter` độc lập trong bộ nhớ; việc đặt assertion cho kết quả đồng bộ cuối cùng chờ quyết định chính thức từ Giảng viên / Product Owner).
4. **BR-04 (Giới hạn 2.000 ký tự):** Đã xác minh là mô tả giao diện đề xuất (UI Guideline) chưa hiện thực trong mã nguồn, không áp dụng làm tiêu chí chặn cứng trong kiểm thử chức năng.

### 10.2. Ma trận Rủi ro và Biện pháp giảm thiểu

| Rủi ro kỹ thuật | Mức độ | Tác động | Biện pháp giảm thiểu |
|---|:---:|---|---|
| **Lỗi Critical `BUG-002` (thiếu Tombstone) đang OPEN** | Nghiêm trọng | Gây mất nhất quán dữ liệu giữa các thiết bị khi xóa offline | Cô lập phạm vi, lập kịch bản Retest chi tiết, ghi nhận rõ ràng vào báo cáo rào cản nghiệm thu |
| **Lỗi High `BUG-001` (treo upload Cloudinary do thiếu timeout) đang OPEN** | Cao | Làm gián đoạn luồng đính kèm ảnh trên UI Editor | Tạo sẵn dữ liệu mẫu chứa ảnh trực tiếp trên SQLite/Firestore để phục vụ các kịch bản phụ thuộc |
| **Dịch vụ Gemini AI (`FN-31..33`) báo lỗi đỏ trên UI** | Trung bình | Kịch bản AI bị chặn trên thiết bị thật | Giữ trạng thái BLOCKED cho lịch sử Kịch bản 5 và NOT RUN cho ca mới; chờ logcat chính thức từ Dev, không tự đoán quota/key |
| **Công cụ Dart VM LCOV BRDA không đo Condition/Path coverage** | Thấp | Dễ gây hiểu lầm về độ bao phủ rẽ nhánh thực tế | Minh bạch định nghĩa: Báo cáo rõ BRDA là số lượng bản ghi nội bộ Dart sinh ra; phân tích CFG áp dụng ở mức thiết kế lý thuyết |
| **Độ bao phủ White-box 50.00% chỉ đo trên 2 model** | Thấp | Không phản ánh độ bao phủ toàn bộ ứng dụng | Ghi rõ giới hạn phạm vi: Chỉ đo trên `checklist_item.dart` và `note_model.dart`, không đánh đồng với toàn bộ `lib/` |

---

## 11. ĐỀ XUẤT LƯỢT THỰC THI HỘP TRẮNG TIẾP THEO (SELECTIVE WHITE-BOX EXTENSION)

* **Kế hoạch tham chiếu:** [white_box_test_plan.md](./white_box_test_plan.md) và [white_box_test_cases.md](../test_cases/white_box/white_box_test_cases.md).
* **Mục tiêu:** Nâng cao độ bao phủ logic cho các phương thức cốt lõi của `NoteModel` và `ChecklistItem` mà không cần thiết bị thật, đồng bộ 100% với 8 ca mở rộng `TC-WB-015` .. `TC-WB-022`:

> [!IMPORTANT]
> **Phân định trạng thái kiểm thử:** Toàn bộ 8 ca kiểm thử mở rộng `TC-WB-015` đến `TC-WB-022` hiện đang ở trạng thái **`DESIGN ONLY / READY FOR TEST AUTHORING` (Đã thiết kế xong — Chưa chạy thực thi)**. Tuyệt đối **không tính các ca này vào số ca đã PASS**.

1. `Note.pendingChecklistCount` — đếm công việc chưa hoàn thành trong Checklist (`TC-WB-015` $\rightarrow$ `REQ-06 / FN-15`, trạng thái: `DESIGN ONLY`).
2. `Note.plainTextContent` — bóc tách văn bản thuần từ Quill Delta JSON (`TC-WB-016` $\rightarrow$ `REQ-05 / REQ-08 / FN-09, FN-23`, trạng thái: `DESIGN ONLY`).
3. `Note.plainTextContent` — xử lý chuỗi rỗng, văn bản thô và JSON lỗi (`TC-WB-017` $\rightarrow$ `REQ-05 / FN-09`, trạng thái: `DESIGN ONLY`).
4. `Note.copyWith(clearReminder)` — cơ chế xóa nhắc nhở về `null` qua cờ `clearReminder` (`TC-WB-018` $\rightarrow$ `REQ-12 / FN-38`, trạng thái: `DESIGN ONLY`).
5. `Note.copyWith(updatedAt)` — tự sinh `DateTime.now()` vs gán timestamp ngoài (`TC-WB-019` $\rightarrow$ `REQ-05 / REQ-11 / FN-09, FN-41`, trạng thái: `DESIGN ONLY`).
6. `Note.fromMap` — phòng thủ SQLite map thiếu trường thời gian `created_at` / `updated_at` (`TC-WB-020` $\rightarrow$ `REQ-04 / NFR-01 / FN-08`, trạng thái: `DESIGN ONLY`).
7. Logic so sánh mốc thời gian `updatedAt.isAfter` độc lập trong bộ nhớ (`TC-WB-021` $\rightarrow$ `REQ-11 / FN-41`, trạng thái: `DESIGN ONLY`; quy tắc hòa `BR-03` giữ `NEEDS CONFIRMATION`; không tính coverage file `sync_repository.dart`).
8. `ChecklistItem.fromJson` — chịu lỗi khi JSON khuyết trường `id`, `text`, `checked` (`TC-WB-022` $\rightarrow$ `REQ-06 / FN-15`, trạng thái: `DESIGN ONLY`).

* **Mục tiêu độ bao phủ kỳ vọng (TARGET BENCHMARK — Không phải kết quả đã đạt):**
  - **Mục tiêu kỳ vọng (Target):** Nâng độ bao phủ dòng của `lib/models/note_model.dart` từ baseline đã đo **44.35%** lên trên **70%** (hoặc $\ge 80\%$), và tổng độ bao phủ đo lường 2 model từ **50.00%** lên trên **75%**.
  - **Khoảng trống độ bao phủ được chấp nhận (Accepted Coverage Gap):** Các phương thức `toFirestoreMap`/`fromFirestoreMap` phụ thuộc `Timestamp` của Cloud Firestore và pipeline mạng của `SyncRepository` không tính vào phạm vi này do ràng buộc nghiêm ngặt không sửa đổi mã nguồn ứng dụng `lib/`.

---
*Tài liệu Master Test Plan được chuẩn hóa và cập nhật dựa trên đối chiếu chéo các bằng chứng thực tế trong repository; không sửa đổi mã nguồn ứng dụng hay mã kiểm thử, không thực hiện commit/push git tự ý.*
