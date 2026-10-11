# KẾ HOẠCH KIỂM THỬ TOÀN DỰ ÁN (MASTER TEST PLAN)
## Dự án: Smart Note App
**Repository:** `Smart-Note-App-QA`  
**Branch áp dụng:** `huong`  
**Tiêu chuẩn tài liệu:** Phù hợp với IEEE 829 & ISTQB Test Planning  
**Trạng thái tài liệu:** Phiên bản Kế hoạch Tổng thể (Master Baseline) — Được thiết lập dựa trên mã nguồn thực tế và bằng chứng kiểm thử đã đối chiếu.

---

## 1. MỤC TIÊU VÀ CƠ SỞ YÊU CẦU

### 1.1. Mục tiêu kiểm thử
1. Đảm bảo chất lượng toàn diện của ứng dụng **Smart Note App** theo mô hình kiến trúc **Offline-First**, đảm bảo tính toàn vẹn dữ liệu giữa cơ sở dữ liệu cục bộ SQLite và dịch vụ lưu trữ đám mây Cloud Firestore.
2. Thiết lập quy trình kiểm thử có cấu trúc chặt chẽ, truy vết hai chiều (Traceability) từ yêu cầu chức năng/kỹ thuật đến các kịch bản kiểm thử (Test Cases), mã tự động hóa (Automation Scripts) và bằng chứng xác minh (Evidence).
3. Đánh giá tính ổn định của các cơ chế cốt lõi: Thuật toán giải quyết xung đột Last-Write-Wins (LWW), cơ chế xóa mềm (Trash), bảo mật sinh trắc học (Biometric Lock), bảo mật phân quyền Firestore Rules và tìm kiếm nội dung tối ưu qua SQL LIKE.
4. Cung cấp hồ sơ kiểm thử minh bạch, có cơ sở kỹ thuật thực tế để phục vụ buổi kiểm tra tiến độ môn học ngày 14/10/2026 và nghiệm thu bài tập lớn.

### 1.2. Cơ sở yêu cầu kỹ thuật & Học phần
* **Yêu cầu môn học Kiểm thử phần mềm:** Thiết kế và thực thi đầy đủ các cấp độ kiểm thử (Hộp đen, Hộp trắng, Tự động hóa và Phi chức năng), có báo cáo đo lường độ bao phủ và nhật ký quản lý lỗi.
* **Tài liệu Kiến trúc & Luồng dữ liệu:** [`docs/Architecture_and_Flows.md`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/docs/Architecture_and_Flows.md) (Clean Architecture 4 lớp: UI $\rightarrow$ Provider $\rightarrow$ Repository $\rightarrow$ Service/Storage).
* **Ma trận Truy vết Yêu cầu:** [`docs/plan_and_requirements/requirements_traceability_matrix.md`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/docs/plan_and_requirements/requirements_traceability_matrix.md) (10 nhóm yêu cầu trọng tâm REQ-01 đến REQ-10).
* **Mã nguồn ứng dụng thực tế:** Thư mục [`lib/`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/lib/) gồm các service nền tảng, model dữ liệu, provider quản lý trạng thái và màn hình giao diện.

---

## 2. PHẠM VI KIỂM THỬ (TEST SCOPE) VÀ PHÂN CẤP ƯU TIÊN

### 2.1. Phạm vi trong dự án (In-Scope)

#### A. Nhóm Cốt lõi (Priority: High / P1 — Bắt buộc đạt 100%)
1. **Xác thực & Phiên làm việc (Authentication):**
   - Đăng ký tài khoản mới: Kiểm tra hợp lệ email, mật khẩu $\ge$ 6 ký tự, lọc domain rác, cắt khoảng trắng đầu/cuối, gửi email xác thực (`auth_provider.dart`, `login_screen.dart`, `email_verification_screen.dart`).
   - Đăng nhập: Đăng nhập bằng Email/Password, chuẩn hóa chữ hoa/thường, chuyển hướng tài khoản chưa verify, xử lý lỗi Firebase Auth bằng tiếng Việt.
   - Quên & Đặt lại mật khẩu: Gửi email khôi phục mật khẩu.
2. **Quản lý Vòng đời Ghi chú CRUD & Trạng thái (Note Lifecycle):**
   - Tạo mới ghi chú văn bản thuần, checklist to-do items.
   - Xem chi tiết và chỉnh sửa ghi chú, cơ chế tự động lưu thời gian thực.
   - Ghim ghi chú (Pin Note) lên đầu danh sách Trang chủ.
   - Xóa mềm (Soft Delete): Chuyển ghi chú vào Thùng rác (`status = 'trash'`), khôi phục về trạng thái bình thường, và xóa vĩnh viễn khỏi SQLite / Firestore.
   - Lưu trữ ghi chú (Archive Note).
3. **Tìm kiếm & Bộ lọc Dữ liệu (Search & Filtering):**
   - Tìm kiếm từ khóa theo tiêu đề và nội dung: Tối ưu qua câu truy vấn SQLite `LOWER(...) LIKE ?` kết hợp loại trừ ghi chú trong thùng rác (`local_note_service.dart`).
   - Tìm kiếm tiếng Việt có dấu và không dấu, không phân biệt hoa/thường.
   - Lọc đa phương tiện qua Token / Filter Chip: `has:image`, `has:audio`, `has:url`, `is:pinned`, `is:archived`, và nhãn `label:"..."`.
4. **Bảo mật Sinh trắc học & Khóa ứng dụng (Biometric Security):**
   - Khóa từng ghi chú riêng tư bằng vân tay/FaceID (`biometric_service.dart`).
   - Tự động chuyển về trạng thái khóa khi ứng dụng chuyển sang chạy ngầm (App Lifecycle State `paused`/`inactive`).
5. **Lưu trữ Cục bộ & Đồng bộ Đám mây (Offline-First & Cloud Sync):**
   - Đọc/ghi cơ sở dữ liệu SQLite cục bộ khi offline.
   - Hàng đợi xóa ngoại tuyến (`pending_delete_service.dart`).
   - Thuật toán giải quyết xung đột Last-Write-Wins (LWW) dựa trên epoch timestamp của trường `updatedAt` (`sync_repository.dart`).
   - Kiểm soát quyền riêng tư và cô lập dữ liệu theo `request.auth.uid` trên Cloud Firestore (`test/security_rules_test.dart`, `firestore.rules`).

#### B. Nhóm Chuyên sâu chọn lọc (Priority: Medium / P2 — Trọng tâm đánh giá kỹ thuật)
1. **Toàn vẹn Dữ liệu Model & Biên chuyển đổi:**
   - Tuần tự hóa / giải mã `Note.toMap`, `Note.fromMap`, `_decodeStringList` với các trường hợp dữ liệu JSON chuẩn, fallback CSV legacy, chuỗi rỗng và kiểu dữ liệu bất thường.
   - Khởi tạo và bất biến của `ChecklistItem.copyWith`.
2. **Khả năng chịu lỗi & Mất mạng đột ngột (Fault Tolerance):**
   - Ngắt kết nối mạng (Airplane mode) trong khi soạn thảo; xác minh dữ liệu không bị mất và cờ `isSynced = false`.
   - Kết nối mạng trở lại; xác minh tiến trình Background Sync tự động đồng bộ lên Firestore.
3. **Hiệu năng & Tải bộ nhớ truy vấn:**
   - Đánh giá thời gian phản hồi tìm kiếm cục bộ SQL LIKE so với in-memory search khi dữ liệu tăng.
4. **Lịch nhắc nhở theo Múi giờ & Khởi động nguội (Reminder & Lifecycle):**
   - Lập lịch thông báo chính xác theo múi giờ địa phương (`reminder_service.dart`, thư viện `timezone`).
   - Điều hướng trực tiếp vào ghi chú khi nhấn thông báo từ Cold Start (`getNotificationAppLaunchDetails`) và Background.

#### C. Nhóm Tiện ích mở rộng (Priority: Low / P3 — Kiểm tra điều kiện phụ thuộc)
1. **Trợ lý AI Gemini:** Đề xuất tiêu đề, tóm tắt nội dung, tạo checklist từ văn bản (`gemini_ai_service.dart`, `editor_screen_ai.dart`); kiểm tra xử lý ngoại lệ quota limit / network timeout qua `_friendlyAiError`.
2. **Xuất bản PDF:** Kết xuất ghi chú sang tệp PDF giữ định dạng và hình ảnh (`pdf_export_service.dart`).
3. **Màn hình phụ trợ:** Vẽ tay (`drawing_screen.dart`), quản lý nhãn (`manage_labels_screen.dart`), đổi giao diện sáng/tối.

### 2.2. Phạm vi ngoài dự án (Out-of-Scope)
* **Nền tảng iOS:** Do thiếu môi trường máy chủ macOS và thiết bị phần cứng iPhone vật lý để build và chạy tự động.
* **Kiểm thử tải lớn (Stress / Load Testing hàng nghìn người dùng):** Dự án sử dụng gói dịch vụ Firebase Spark/miễn phí, không hỗ trợ thử tải cường độ cao trên cụm server.
* **Penetration Testing chuyên sâu:** Không thực hiện tấn công dịch ngược file APK, can thiệp mã nhị phân native hay bypass SSL pinning.
* **Kiểm thử trên toàn bộ tổ hợp thiết bị Android:** Chỉ tập trung trên thiết bị Android đại diện được kết nối.
* **Độ bao phủ nhánh 100% toàn bộ codebase ứng dụng:** Không đặt mục tiêu bao phủ toàn bộ các widget hiển thị đồ họa thuần túy của Flutter framework.

---

## 3. PHƯƠNG PHÁP VÀ CHIẾN LƯỢC KIỂM THỬ

Hệ thống kiểm thử áp dụng mô hình 4 cấp độ kết hợp:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CHIẾN LƯỢC KIỂM THỬ TỔNG THỂ                    │
├───────────────────┬───────────────────┬────────────────────────────────┤
│    CẤP ĐỘ TEST    │     PHẠM VI       │        CÔNG CỤ / KỸ THUẬT      │
├───────────────────┼───────────────────┼────────────────────────────────┤
│ 1. Hộp trắng      │ Models, Providers,│ Flutter Test Native, LCOV,     │
│    (White-Box)    │ Security Rules    │ Line & BRDA Coverage           │
├───────────────────┼───────────────────┼────────────────────────────────┤
│ 2. Hộp đen        │ Toàn bộ UI Flows, │ Phân vùng tương đương (EP),    │
│    (Black-Box)    │ 10 Nhóm chức năng │ Phân tích giá trị biên (BVA)   │
├───────────────────┼───────────────────┼────────────────────────────────┤
│ 3. Tự động hóa    │ Smoke & Regression│ Python ADB/UI Runner,          │
│    (Automation)   │ các luồng cốt lõi │ pytest, Flutter Driver/Test    │
├───────────────────┼───────────────────┼────────────────────────────────┤
│ 4. Phi chức năng  │ Offline, Security,│ Airplane Mode, Network Throttling,│
│ (Non-Functional)  │ LWW Conflict      │ App Lifecycle State            │
└───────────────────┴───────────────────┴────────────────────────────────┘
```

1. **Kiểm thử Hộp trắng chọn lọc (Selective White-box):**
   - Tập trung vào các lớp nghiệp vụ cốt lõi không phụ thuộc UI: `ChecklistItem`, `Note`, `AuthProvider`, `Firestore Security Rules`.
   - Sử dụng lệnh chuẩn: `flutter test --coverage --branch-coverage --fail-fast --concurrency=1`.
   - Phân tích độ bao phủ dòng (Line Coverage) và ghi nhận bản ghi rẽ nhánh BRDA từ LCOV.
2. **Kiểm thử Hộp đen (Black-box):**
   - Áp dụng kỹ thuật: Phân vùng tương đương (Equivalence Partitioning), Phân tích giá trị biên (Boundary Value Analysis), Bảng quyết định (Decision Table), Kiểm thử chuyển trạng thái (State Transition).
   - Kiểm thử thủ công trên thiết bị thật kết hợp chụp màn hình bằng chứng (Screenshot Evidence).
3. **Tự động hóa chọn lọc (Selective Automation):**
   - Duy trì các kịch bản kiểm thử tự động Python trong thư mục `automation/tests/` và `tools/fn23/` để chạy lại kiểm thử hồi quy (Regression Test) nhanh chóng khi có cập nhật.
4. **Kiểm thử Phi chức năng trong điều kiện hiện có (Non-functional):**
   - Độ tin cậy (Reliability): Thao tác ngắt kết nối vật lý, khôi phục mạng để kiểm tra tính nhất quán dữ liệu LWW và hàng đợi xóa offline.
   - An toàn thông tin (Security): Kiểm tra cô lập dữ liệu người dùng qua các bộ test quy tắc an ninh mô phỏng.

---

## 4. MÔI TRƯỜNG, THIẾT BỊ, TÀI KHOẢN VÀ DỮ LIỆU KIỂM THỬ

### 4.1. Môi trường phần cứng và thiết bị
* **Thiết bị kiểm thử chính (Primary Target Device):**
  - Model: Samsung Galaxy S21 FE 5G (SM-G990E/DS).
  - Serial Number: `R5CW82ECF6M`.
  - Hệ điều hành: Android 14 (One UI 6.1).
  - Độ phân giải màn hình: $1080 \times 2340$ pixels.
* **Máy trạm điều khiển (Host Workstation):**
  - Hệ điều hành: Windows (x86_64).
  - Flutter SDK: `3.44.1 • channel stable`.
  - Dart SDK: `3.12.1`.
  - Python Runtime: `Python 3.13`.
  - Android Debug Bridge (ADB): `Android SDK Platform-Tools`.

### 4.2. Cấu hình tài khoản kiểm thử
| Mã định danh | Địa chỉ Email | Mục đích sử dụng | Trạng thái xác thực |
|---|---|---|---|
| **Account-01** (Chính) | `student_qa@gmail.com` | Kiểm thử Happy Path, CRUD, Search, Sync | Đã kích hoạt (`emailVerified = true`) |
| **Account-02** (Đối chứng) | `student_qa_secondary@gmail.com` | Kiểm thử xung đột LWW, cô lập dữ liệu Security | Đã kích hoạt (`emailVerified = true`) |
| **Account-03** (Chưa verify) | `unverified_qa@gmail.com` | Kiểm thử luồng chặn đăng nhập khi chưa kích hoạt | Chưa kích hoạt (`emailVerified = false`) |
| **Account-04** (Khách/Rác) | `test_disposable@tempmail.com` | Kiểm thử bộ lọc tên miền rác | Bị chặn bởi hệ thống |

### 4.3. Dữ liệu kiểm thử mẫu (Test Data Baseline)
* **Ghi chú Văn bản:** Chứa tiêu đề tiếng Việt có dấu, nội dung định dạng rich text, ký tự đặc biệt SQL/XSS (`' OR '1'='1`, `<script>`).
* **Ghi chú Checklist:** Danh sách công việc gồm cả mục đã hoàn thành (`checked = true`) và chưa hoàn thành (`checked = false`).
* **Ghi chú Đa phương tiện:** Ghi chú có đính kèm ảnh, file ghi âm giọng nói, liên kết URL (`https://...`).
* **Ghi chú Trạng thái:** Ghi chú có gắn cờ Ghim (`pinned`), Lưu trữ (`archived`), và Thùng rác (`trash`).

---

## 5. TIẾN ĐỘ VÀ BẰNG CHỨNG ĐÃ GHI NHẬN (BASELINE AUDIT)

### 5.1. Kết quả Kiểm thử Hộp trắng (Lượt `note_model_run_20261010_0945`)
- **Trạng thái thực thi:** **18/18 Unit Tests PASS (100%)**, Exit Code: `0`.
  - `test/checklist_test.dart`: 5 tests PASS.
  - `test/checklist_copy_with_test.dart`: 4 tests PASS.
  - `test/note_model_test.dart`: 9 tests PASS (Bao phủ toàn diện `toMap`, `fromMap`, `_decodeStringList`).
- **Độ bao phủ trên phạm vi đo lường 2 Model (`ChecklistItem` & `Note`):**
  - **Line Coverage:** 69/138 dòng (**50.00%**, tăng **+29.71 điểm phần trăm** so với lượt 0250).
  - **LCOV BRDA (Branch):** 21/41 bản ghi (**51.22%**, tăng **+21.95 điểm phần trăm** so với lượt 0250).
- **Vị trí lưu trữ Bằng chứng & Mã băm:**
  - `coverage/runs/note_model_run_20261010_0945/`
  - `evidence/white_box/note_model_run_20261010_0945/`
  - Checksum `test_execution.log`: `d8448a1d37547defb293b5326b6e6147e495c890aba93ed63f389376505bf00e`
  - Checksum `lcov.info`: `c5244d2a160ef10b33f272b6abebf7b0828e1bacee9fc49dbc07d1ad04c05324`
  - *(Ghi chú hiệu chỉnh backlog/audit: Mâu thuẫn hoán đổi nhãn mã băm trước đó hoàn toàn thuộc về hai tệp artifact kết quả chạy `test_execution.log` và `lcov.info` của lượt `note_model_run_20261010_0945`, không phải giữa các tệp mã nguồn test `checklist_test.dart` và `note_model_test.dart`. Chỉ hiệu chỉnh mô tả phân loại tài liệu, không chạy lại unit test)*.
- **Giới hạn kỹ thuật đã ghi nhận (Không suy đoán):**
  - *Độ bao phủ 50.00% dòng chỉ áp dụng cho 2 file model được đo*, không đại diện cho mức bao phủ toàn ứng dụng. Mức bao phủ toàn ứng dụng đòi hỏi chạy toàn bộ test suite trên toàn bộ thư mục `lib/`.
  - *Giới hạn Git M:* 4 file generated Linux/macOS mang trạng thái `M` trong Git nhưng mã băm nội dung thô và clean filter khớp 100% với Git HEAD; nguyên nhân trạng thái M chưa xác định, không điều tra thêm trong đợt này.
  - *Bản chất BRDA:* Dart VM gán bản ghi BRDA cho cả khai báo hàm và khối try/catch; số liệu 21/41 là số lượng bản ghi LCOV thực tế, không kết luận vội là độ bao phủ nhánh logic nhị phân truyền thống.

### 5.2. Kết quả Kiểm thử Hộp đen & Tự động hóa
- **Đã hoàn thành thiết kế:** 118 Test Cases (134 Execution Items) trên 10 nhóm chức năng.
- **Kết quả thực tế đã ghi nhận evidence:**
  - REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-08: Đã có kịch bản chạy đạt và có ảnh chụp screenshot trong `evidence/`.
  - REQ-07 (FN-23 Tìm kiếm & Bộ lọc): Đã xác minh 10 items PASS có căn cứ kỹ thuật (8 batch, 2 ad-hoc); 1 item BLOCKED (Item 09); 3 items có ảnh ad-hoc chưa xác minh; 8 items CHƯA CHẠY (NOT RUN).
  - REQ-09 (Bảo mật & Cô lập dữ liệu): Pass 8/8 tests tự động trong `test/security_rules_test.dart`.
  - REQ-10 (Reliability): Phát hiện defect `BUG-001`.
- **Nhật ký lỗi (Defect Log):**
  - `BUG-001` (Severity: High): Treo vô hạn khi đính kèm/upload ảnh lên Cloudinary do thiếu cơ chế timeout trong `lib/services/cloudinary_service.dart`. Lỗi này đang chặn (Block) kịch bản Item 09 của FN-23.

---

## 6. BẢNG THEO DÕI PHẠM VI TOÀN DỰ ÁN (SCOPE TRACKING TABLE)

Bảng phân loại trạng thái:
* **PASS**: Đã thực thi, đạt kết quả kỳ vọng và có bằng chứng log/screenshot xác thực.
* **FAIL**: Đã thực thi, kết quả thực tế không khớp kỳ vọng hoặc phát sinh lỗi phần mềm.
* **BLOCKED**: Bị chặn không thể thực thi tiếp do lỗi của thành phần phụ thuộc.
* **CHƯA ĐỦ BẰNG CHỨNG**: Có file ảnh hoặc log riêng lẻ nhưng chưa chạy qua test suite chính thức để xác minh.
* **CHƯA CHẠY (NOT RUN)**: Đã có kịch bản thiết kế nhưng chưa thực thi trên thiết bị/môi trường.
* **CHƯA CÓ TEST**: Chức năng tồn tại trong code nhưng chưa thiết kế test case tương ứng.

| Hạng mục | Chức năng / Hàm nghiệp vụ | Ưu tiên | Phương pháp | Test case hiện có | Trạng thái | Bằng chứng (Evidence) | Việc còn thiếu |
|---|---|:---:|---|---|:---:|---|---|
| **Auth** | Đăng ký tài khoản (Email, Mật khẩu, Validate) | P1 | Black-box / Auto | `TC-BB-001` .. `004B` | **PASS** | `evidence/fn02/FN02_TC-BB-001_D01_01.png` .. `004B` | Kiểm tra lại tính toàn vẹn ảnh `M` |
| **Auth** | Đăng nhập (Email, Mật khẩu, Trimming, Case-ins.) | P1 | Black-box / White-box | `TC-BB-006` .. `009`, `test/auth_provider_test.dart` | **PASS** | `evidence/fn04/`, Log pass 14/14 tests `auth_provider_test` | Đo coverage cho `auth_provider.dart` |
| **Auth** | Quên mật khẩu & Gửi mail đặt lại | P1 | Black-box | `TC-BB-011` .. `011C` | **PASS** | `evidence/fn05/FN05_TC-BB-011_D01_01.png`, `02.png` | Kiểm thử timeout gửi lại email |
| **Auth** | Đăng nhập Google OAuth | P2 | Black-box / Auto | `test_fn05_google_oauth.py` | **CHƯA ĐỦ BẰNG CHỨNG** | Script tự động có sẵn, thiếu log chạy batch trên device | Chạy kiểm thử có điều kiện Google Play Services |
| **Note CRUD** | Tạo mới ghi chú văn bản thuần | P1 | Black-box / Auto | `TC-BB-018`, `test_fn08_create_note.py` | **PASS** | `evidence/fn08/FN08_TC-BB-018_D01_01.png` | Bổ sung test case ghi chú độ dài lớn |
| **Note CRUD** | Đính kèm hình ảnh từ Gallery / Camera | P1 | Black-box | `TC-BB-018C` | **BLOCKED** | Defect log `docs/bugs/defect_log.md` (`BUG-001`) | Chờ fix timeout Cloudinary để unblock |
| **Note CRUD** | Chỉnh sửa ghi chú & Tự động lưu | P1 | Black-box / Auto | `TC-BB-019` .. `019C`, `test_fn09_edit_note.py` | **PASS** | `evidence/fn09/FN09_TC-BB-019_D01_01.png` | Kiểm thử tự động lưu khi crash đột ngột |
| **Note CRUD** | Ghim ghi chú lên đầu danh sách (Pin) | P1 | Black-box / Auto | `TC-BB-024`, `024B`, `test_fn20_pin_note.py` | **PASS** | `evidence/fn20/FN20_TC-BB-024_D01_01.png` | Hoàn thành |
| **Note CRUD** | Xóa mềm vào Thùng rác (Trash) & Khôi phục | P1 | Black-box | `TC-BB-015`, `015B`, `015C` | **PASS** | `evidence/fn29_30/` (4 ảnh PNG) | Kiểm thử tự động dọn rác sau 30 ngày |
| **Search** | Tìm kiếm từ khóa qua SQL LIKE (trừ Trash) | P1 | Black-box / Auto | `TC-BB-026` .. `027`, batch 1 & 2 runner | **PASS** | `evidence/fn23/FN23_TC-BB-026_D01.png` .. `027_D01.png` | Chạy 8 item còn lại của FN-23 |
| **Search** | Lọc theo Chip `has:image` | P1 | Black-box / Auto | `TC-BB-027B-D01` (FN-23 Item 09) | **BLOCKED** | Script dừng tại dòng 88 (`BUG-001`) | Cần note có ảnh trên database |
| **Search** | Lọc theo Chip `has:audio`, `has:url`, `label` | P2 | Black-box | `TC-BB-027B-D02`, `027B-D03`, `027C-D01` | **CHƯA ĐỦ BẰNG CHỨNG** | Có 3 ảnh ad-hoc trong `evidence/fn23/`, thiếu log suite | Chạy chính thức qua batch runner |
| **Search** | Lọc theo Chip `is:pinned`, `is:archived`, `has:list` | P2 | Black-box | `TC-BB-027D-D01`, `027D-D02`, `027G-D01` | **CHƯA CHẠY** | Chưa có | Thực thi trong lượt chạy Run 2 |
| **Biometric** | Khóa ghi chú bằng vân tay & Tự động khóa | P1 | Black-box | `TC-WB-014`, `TC-NF-006`, Kịch bản 4 manual | **PASS** | `docs/test_report/Testing_Report.md` (Kịch bản 4 đạt) | Viết automated widget/integration test |
| **Sync/LWW** | Giải quyết xung đột Last-Write-Wins (`updatedAt`) | P1 | Integration / Manual | Kịch bản 2 manual trong Testing Report | **PASS** | `docs/test_report/Testing_Report.md` (Kịch bản 2 đạt) | Viết unit test giả lập epoch timestamp so sánh |
| **Sync/Offline**| Hàng đợi xóa ngoại tuyến (`PendingDeleteService`)| P1 | Unit / Integration | Chưa có unit test riêng cho service này | **CHƯA CÓ TEST** | Chưa có | Thiết kế unit test cho `PendingDeleteService` |
| **Security** | Cô lập dữ liệu Firestore Rules theo `request.auth.uid` | P1 | White-box Auto | `test/security_rules_test.dart` (8 tests) | **PASS** | Terminal log pass 8/8 tests | Hoàn thành |
| **Data Model**| `ChecklistItem` khởi tạo, JSON & `copyWith` | P1 | White-box Auto | `test/checklist_test.dart`, `checklist_copy_with_test.dart` | **PASS** | LCOV run 0945 (100% lines & branches) | Hoàn thành |
| **Data Model**| `Note.toMap`, `fromMap`, `_decodeStringList` | P1 | White-box Auto | `test/note_model_test.dart` (9 tests) | **PASS** | LCOV run 0945 (Tăng lên 55/124 dòng = 44.35%) | Viết tiếp test cho các getter còn lại |
| **Data Model**| `Note.plainTextContent`, `pendingChecklistCount` | P2 | White-box | Chưa có test trực tiếp cho 2 getter này | **CHƯA CÓ TEST** | Dòng 33–69 của `note_model.dart` chưa chạy | Bổ sung unit test để nâng coverage Note lên >70% |
| **Reminder** | Lập lịch thông báo & Điều hướng Cold Start | P2 | Manual / Integration | Kịch bản thông báo trong Testing Report | **CHƯA ĐỦ BẰNG CHỨNG** | Chưa có log xác thực cold start payload | Kiểm thử tự động/thủ công notification click |
| **AI Gemini** | Tóm tắt, gợi ý tiêu đề, checklist & xử lý lỗi | P3 | Manual / Integration | Kịch bản 5 manual trong Testing Report | **PASS** | `docs/test_report/Testing_Report.md` (Kịch bản 5 đạt) | Kiểm thử xử lý lỗi quota 429 và timeout |
| **PDF Export**| Xuất file PDF kèm hình ảnh và định dạng | P3 | Manual / Integration | Kịch bản 6 manual trong Testing Report | **PASS** | `docs/test_report/Testing_Report.md` (Kịch bản 6 đạt) | Kiểm tra hiển thị ký tự Unicode tiếng Việt phức tạp |

---

## 7. CÁC GIAI ĐOẠN VÀ MỐI QUAN HỆ PHỤ THUỘC (PHASES & DEPENDENCIES)

*Lưu ý:* Do chưa có văn bản công bố hạn nộp cuối cùng của môn học, kế hoạch chia theo các mốc kỹ thuật phụ thuộc mà chưa gán ngày hoàn thành cố định cho các giai đoạn sau:

```
[Giai đoạn 1: Chuẩn bị Baseline & Kế hoạch] ──► (HOÀN TẤT)
                      │
                      ▼
[Giai đoạn 2: Củng cố Unit Test & Model Coverage] (Không phụ thuộc thiết bị)
                      │
                      ▼
[Giai đoạn 3: Kiểm tra Tiến độ Môn học - 14/10/2026] (Báo cáo & Demo thực tế)
                      │
                      ▼
[Giai đoạn 4: Mở khóa BUG-001 & Thực thi FN-23 Run 2] (Phụ thuộc bản vá Cloudinary)
                      │
                      ▼
[Giai đoạn 5: Kiểm thử Phi chức năng & Hồi quy toàn diện]
                      │
                      ▼
[Giai đoạn 6: Nghiệm thu & Đóng gói Hồ sơ Báo cáo] (Hạn nộp chính thức: Chưa xác nhận)
```

1. **Giai đoạn 1: Chuẩn bị Baseline, Rà soát Tài liệu & Lập Kế hoạch (Đã hoàn tất):**
   - Rà soát repository, khóa an toàn evidence, sắp xếp cấu trúc thư mục QA.
   - Xác minh Git status, LCOV BRDA và lập Master Test Plan.
2. **Giai đoạn 2: Củng cố Unit Test & Nâng cao Model Coverage (Sẵn sàng thực thi):**
   - Mục tiêu: Bổ sung unit test cho các getter còn lại của `Note` model (`plainTextContent`, `pendingChecklistCount`, `isChecklist`) và `PendingDeleteService`.
   - Phụ thuộc: Không phụ thuộc thiết bị thật, chạy nhanh trên máy trạm.
3. **Giai đoạn 3: Kiểm tra Tiến độ Môn học (Mốc xác nhận: Ngày 14/10/2026):**
   - Mục tiêu: Hoàn thiện slide thuyết trình ([`docs/test_report/progress_check_slides_outline.md`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/docs/test_report/progress_check_slides_outline.md)), demo các luồng PASS, giải trình minh bạch hiện trạng 25 file ảnh `M` và defect `BUG-001`.
4. **Giai đoạn 4: Giải quyết BUG-001 & Thực thi Chính thức FN-23 Run 2 (Chờ kế hoạch fix):**
   - Phụ thuộc: Phải có giải pháp xử lý timeout trong `cloudinary_service.dart` (hoặc mock data có sẵn ảnh) để unblock Item 09.
   - Thực thi lại toàn bộ 22 items của FN-23 vào thư mục cách ly `evidence/fn23/run2/` và cập nhật execution sheet chính thức.
5. **Giai đoạn 5: Kiểm thử Phi chức năng & Hồi quy Toàn diện (Chưa đặt ngày):**
   - Thực thi kiểm thử ngoại tuyến (Offline-First), kiểm tra giải quyết xung đột LWW đa thiết bị, đo lường thời gian đáp ứng tìm kiếm.
6. **Giai đoạn 6: Nghiệm thu & Hoàn thiện Báo cáo Tổng kết (Chờ công bố hạn nộp):**
   - Tổng hợp báo cáo kết quả kiểm thử, nghiệm thu các chỉ số coverage và đóng gói dự án.

---

## 8. TIÊU CHÍ BẮT ĐẦU, TẠM DỪNG, TIẾP TỤC VÀ KẾT THÚC (CRITERIA)

### 8.1. Tiêu chí Bắt đầu (Entry Criteria)
* Mã nguồn ứng dụng trên branch `huong` compile thành công, không có lỗi phân tích tĩnh nghiêm trọng (`flutter analyze` hoặc build runner không báo lỗi cú pháp).
* Môi trường thực thi đáp ứng đầy đủ: Máy trạm kết nối thành công với thiết bị Android (nhận diện qua `adb devices`) hoặc môi trường unit test Flutter sẵn sàng.
* Kịch bản kiểm thử (Test Cases / Test Plan) đã được phê duyệt, dữ liệu kiểm thử mẫu đã được nạp sẵn.

### 8.2. Tiêu chí Tạm dừng (Suspension Criteria)
Kiểm thử phải **ngay lập tức tạm dừng** khi gặp một trong các điều kiện sau:
1. **Lỗi ứng dụng nghiêm trọng (Blocker):** Ứng dụng bị crash ngay khi khởi động (Crash on Launch) hoặc lỗi treo vô hạn (Infinite Hang) ngăn chặn Tester tương tác với màn hình.
2. **Sự cố môi trường kiểm thử:** Thiết bị Android bị ngắt kết nối ADB đột ngột, tài khoản Firebase bị khóa hoặc hết quota dịch vụ (Authentication / Firestore / Gemini API 429).
3. **Thất bại trong Test Suite tự động:** Chế độ `--fail-fast` phát hiện bất kỳ test assertion nào thất bại; tiến trình phải dừng lại để lưu log và điều tra, không chạy tiếp để tránh ô nhiễm dữ liệu.

### 8.3. Tiêu chí Tiếp tục (Resumption Criteria)
* Lỗi Blocker đã được cô lập hoặc có giải pháp khắc phục tạm thời (workaround) được QA Lead thông qua.
* Môi trường mạng, thiết bị hoặc quota dịch vụ bên thứ ba đã được phục hồi ổn định.
* Dữ liệu kiểm thử đã được làm sạch và đưa về trạng thái ban đầu (Clean State).

### 8.4. Tiêu chí Hoàn thành (Exit Criteria)
* 100% các kịch bản kiểm thử cốt lõi (P1) đã được thực thi và đạt kết quả PASS (hoặc có giải trình được chấp thuận).
* Không còn lỗi mức độ Blocker hoặc Critical tồn tại ở trạng thái OPEN mà không có phương án xử lý.
* Toàn bộ các lượt chạy test tự động đều có file log và LCOV được sao lưu với mã băm SHA-256 xác thực.
* Báo cáo kiểm thử tổng kết phản ánh trung thực kết quả đo lường, không suy diễn độ bao phủ ngoài phạm vi thực tế.

---

## 9. QUY TẮC QUẢN LÝ LỖI, BẰNG CHỨNG VÀ SẢN PHẨM BÀN GIAO

### 9.1. Quy trình quản lý lỗi (Defect Lifecycle)
1. **Phát hiện & Xác minh:** Khi kết quả thực tế không khớp với kết quả kỳ vọng, Tester ghi lại logcat/console và chụp màn hình bằng chứng.
2. **Ghi nhật ký:** Cập nhật vào [`docs/bugs/defect_log.md`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/docs/bugs/defect_log.md) theo chuẩn IEEE 829 (Bug ID, Severity, Steps to Reproduce, Expected, Actual, Evidence, RCA nghi vấn).
3. **Phân loại Mức độ nghiêm trọng (Severity):**
   - **Blocker / High:** Gây crash app, treo màn hình, mất dữ liệu (ví dụ: `BUG-001`).
   - **Major / Medium:** Chức năng chính không hoạt động đúng logic nghiệp vụ nhưng có workaround.
   - **Minor / Low:** Lỗi giao diện nhỏ, sai lệch định dạng văn bản, lỗi chính tả thông báo.
4. **Kiểm thử lại & Đóng lỗi (Retest & Close):** Chỉ đóng bug khi bản vá lỗi đã được cài đặt và kiểm thử lại đạt yêu cầu kèm kiểm thử hồi quy các chức năng liên quan.

### 9.2. Quy tắc Lưu trữ Bằng chứng (Evidence Integrity Rules)
* **Quy chuẩn đặt tên ảnh:** `FN<Mã_Chức_Năng>_TC-BB-<Mã_Test_Case>_D<Mã_Dữ_Liệu>_<Số_Thứ_Tự>.png` (Ví dụ: `FN23_TC-BB-026_D01.png`).
* **Tính nguyên vẹn của ảnh:** Ảnh chụp màn hình phải giữ nguyên thanh trạng thái hệ thống và giao diện ứng dụng, không cắt ghép chỉnh sửa.
* **Quy chuẩn Log & LCOV:**
  - Mỗi lượt chạy test phải được lưu trong thư mục riêng biệt có định danh thời gian: `coverage/runs/<tên_lượt_chạy>_<timestamp>/`.
  - Sao lưu nguyên trạng sang `evidence/white_box/<tên_lượt_chạy>_<timestamp>/`.
  - Kiểm tra và ghi nhận mã băm SHA-256 của file log và LCOV để đảm bảo không bị giả mạo.

### 9.3. Danh mục Sản phẩm bàn giao (Deliverables)
1. Kế hoạch kiểm thử tổng thể: [`docs/plan_and_requirements/test_plan.md`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/docs/plan_and_requirements/test_plan.md).
2. Ma trận truy vết yêu cầu: [`docs/plan_and_requirements/requirements_traceability_matrix.md`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/docs/plan_and_requirements/requirements_traceability_matrix.md).
3. Hồ sơ đặc tả Test Cases: Thư mục [`test_cases/`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/test_cases/) (Black-box, White-box, Non-functional, Execution sheets).
4. Mã nguồn và kịch bản test tự động: Thư mục [`test/`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/test/) và [`automation/`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/automation/).
5. Kho bằng chứng kiểm thử: Thư mục [`evidence/`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/evidence/) (Screenshots và White-box run logs/LCOVs).
6. Nhật ký theo dõi lỗi: [`docs/bugs/defect_log.md`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/docs/bugs/defect_log.md).
7. Báo cáo đánh giá kiểm thử: [`docs/test_report/Testing_Report.md`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/docs/test_report/Testing_Report.md) và Dàn ý Slide tiến độ [`docs/test_report/progress_check_slides_outline.md`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/docs/test_report/progress_check_slides_outline.md).

---

## 10. RỦI RO, GIỚI HẠN VÀ DANH SÁCH THÔNG TIN CÒN THIẾU

### 10.1. Rủi ro và Biện pháp giảm thiểu
| Rủi ro | Mức độ | Tác động | Biện pháp giảm thiểu |
|---|:---:|---|---|
| **Lỗi `BUG-001` làm nghẽn kịch bản FN-23 Item 09** | Cao | Không thể tạo ghi chú có ảnh để test bộ lọc `has:image` | Tạo sẵn dữ liệu mẫu chứa ảnh trực tiếp trên SQLite/Firestore hoặc dùng mock data |
| **Phụ thuộc quota Gemini AI & Firebase** | Trung bình | Có thể bị lỗi 429 nếu gọi API dồn dập trong test tự động | Giới hạn số lượng test gọi API thật, kiểm thử chủ yếu trên mock service |
| **Thiếu checksum baseline của 25 file ảnh `M`** | Trung bình | Không thể chứng minh tuyệt đối tính nguyên vẹn từ ban đầu | Giữ nguyên hiện trạng trên Git, không chạy `git restore` làm mất evidence thực tế |
| **Dart VM LCOV BRDA không phân biệt nhánh nhị phân** | Thấp | Dễ gây hiểu lầm về độ bao phủ nhánh thực tế | Minh bạch định nghĩa: Báo cáo rõ đây là số lượng bản ghi BRDA do Dart sinh ra |

### 10.2. Danh sách thông tin còn thiếu (Chưa xác nhận)
1. **Danh sách gốc của "44 chức năng" (nếu có):** Hiện tại trong tài liệu dự án chỉ tìm thấy ghi nhận về **"44 Execution Items chờ thực thi"** (thuộc 3 nhóm FN-23, FN-29/30, FN-40/41 trong `docs/qa/black_box_execution_summary.md`), hoàn toàn chưa tìm thấy tài liệu gốc liệt kê 44 chức năng riêng lẻ. *Ghi nhận: Chưa có / Chưa xác nhận.*
2. **Hạn nộp chính thức bài tập lớn:** Ngoài mốc kiểm tra tiến độ ngày 14/10/2026, thời hạn nộp báo cáo cuối kỳ chính thức chưa được công bố. *Ghi nhận: Chưa có / Chưa xác nhận.*
3. **Kế hoạch sửa lỗi chính thức cho `BUG-001`:** Chưa có phương án phê duyệt về việc bổ sung timeout vào `lib/services/cloudinary_service.dart`. *Ghi nhận: Đang chờ quyết định kỹ thuật.*

---

## 11. ĐỀ XUẤT LƯỢT THỰC THI ĐẦU TIÊN (PROPOSED FIRST TEST RUN)

Để tiếp tục nâng cao chất lượng hồ sơ kiểm thử một cách an toàn và độc lập, đề xuất lượt thực thi tiếp theo như sau:

* **Mã lượt chạy dự kiến:** `note_model_getters_run`
* **Mục tiêu:** Kiểm thử đơn vị bổ sung cho các thuộc tính và getter còn lại của lớp `Note` trong [`lib/models/note_model.dart`](file:///d:/Workspace/TBDD/Smart-Note-App-QA/lib/models/note_model.dart) gồm:
  1. Getter `isChecklist`: Kiểm tra nhận diện nội dung rỗng (`content.isEmpty`), nội dung JSON hợp lệ, nội dung JSON sai format.
  2. Getter `checklistPlainText`: Kiểm tra trích xuất text danh sách khi không phải checklist, khi checklist có/không có items, và trường hợp catch exception.
  3. Getter `pendingChecklistCount`: Kiểm tra đếm số công việc chưa hoàn thành (`checked != true`), trường hợp danh sách rỗng, trường hợp không phải checklist.
  4. Getter `plainTextContent`: Kiểm tra bóc tách văn bản từ Quill Delta JSON (`[{"insert":"..."}]`), văn bản thường, và xử lý chuỗi rỗng.
* **Phương thức thực hiện:** Tạo mới file test độc lập `test/note_getters_test.dart` (hoặc mở rộng `test/note_model_test.dart`), không chỉnh sửa mã nguồn ứng dụng `lib/` hay các test cũ.
* **Điều kiện thực thi:**
  - Lệnh chạy: `flutter test test/checklist_test.dart test/checklist_copy_with_test.dart test/note_model_test.dart test/note_getters_test.dart --coverage --branch-coverage --coverage-path=coverage/runs/note_model_getters_run_<ts>/lcov.info --fail-fast --concurrency=1 -r expanded`
  - Nếu bất kỳ test nào fail, lập tức dừng lại, ghi log và không tiếp tục.
* **Bằng chứng thu thập:** Lưu trữ đầy đủ log thực thi và file `lcov.info`, sao lưu vào `evidence/white_box/` kèm mã băm SHA-256.
* **Kỳ vọng độ bao phủ:** Nâng tỷ lệ bao phủ dòng của `lib/models/note_model.dart` từ 44.35% lên trên **70%**, và nâng độ bao phủ tổng phạm vi đo lường lên trên **75%**.

---
*Tài liệu được lập và bảo toàn nguyên trạng theo nguyên tắc Read-Only; chưa thực hiện bất kỳ lệnh thay đổi mã nguồn, test mới hay git commit/push nào.*
