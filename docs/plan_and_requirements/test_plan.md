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
* **Đặc tả Yêu cầu Rút gọn (Condensed SRS):** [srs_condensed.md](./srs_condensed.md) (13 yêu cầu chức năng REQ-01..REQ-13 và 5 yêu cầu phi chức năng NFR-01..NFR-05).
* **Tài liệu Kiến trúc & Luồng dữ liệu:** [Architecture_and_Flows.md](../Architecture_and_Flows.md) (Clean Architecture 4 lớp: UI $\rightarrow$ Provider $\rightarrow$ Repository $\rightarrow$ Service/Storage).
* **Ma trận Truy vết Yêu cầu:** [requirements_traceability_matrix.md](./requirements_traceability_matrix.md).
* **Mã nguồn ứng dụng thực tế:** Thư mục [`lib/`](../../lib) gồm các service nền tảng, model dữ liệu, provider quản lý trạng thái và màn hình giao diện.

---

## 2. PHẠM VI KIỂM THỬ (TEST SCOPE) VÀ PHÂN CẤP ƯU TIÊN

### 2.1. Phạm vi trong dự án (In-Scope)

#### A. Nhóm Cốt lõi (Priority: High / P1 — Bắt buộc đạt 100%)
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
   - Kiểm soát quyền riêng tư và cô lập dữ liệu theo `request.auth.uid` trên Cloud Firestore (NFR-03, `test/security_rules_test.dart`, `firestore.rules`).

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
1. **Tiện ích bổ trợ (REQ-12):** Xuất bản PDF (`pdf_export_service.dart`), Bảng vẽ tay (`drawing_screen.dart`), Quản lý nhãn (`manage_labels_screen.dart`), Đổi màu nền ghi chú.
2. **Trợ lý AI Gemini (REQ-13):** Tóm tắt nội dung (`FN-31`), đề xuất tiêu đề (`FN-32`), tạo checklist (`FN-33`) (`gemini_ai_service.dart`, `editor_screen_ai.dart`). Lịch sử thực thi Kịch bản 5 trên máy thật giữ nguyên **3 trường hợp `BLOCKED`** do lỗi hiển thị trên UI chưa xác định nguyên nhân kỹ thuật; 3 test case chính thức mới thiết kế (`TC-BB-032`, `TC-BB-032B`, `TC-BB-032C`) giữ trạng thái **`NOT RUN` (Chờ gỡ `BLOCKED`)**.

### 2.2. Phạm vi ngoài dự án (Out-of-Scope)
* **Nền tảng iOS:** Do thiếu môi trường máy chủ macOS và thiết bị phần cứng iPhone vật lý để build và chạy tự động.
* **Kiểm thử tải lớn (Stress / Load Testing hàng nghìn người dùng):** Dự án sử dụng gói dịch vụ Firebase Spark miễn phí, không hỗ trợ thử tải cường độ cao trên cụm server.
* **Penetration Testing chuyên sâu:** Không thực hiện tấn công dịch ngược file APK, can thiệp mã nhị phân native hay bypass SSL pinning.
* **Ràng buộc an toàn thiết bị thật:**
  - Không thực hiện thao tác xóa dấu vân tay hệ thống trên máy thật của tester (`TC-BB-015G-D01` xếp trạng thái **BLOCKED** an toàn).
  - Không cố tình ghi đè làm đầy bộ nhớ máy thật dẫn đến nguy cơ treo hệ điều hành (`FN-44` xếp trạng thái **BLOCKED** an toàn).
* **Kiểm thử liên kết ứng dụng bên ngoài (External Deep Link):** Không kiểm thử thao tác click link kích hoạt email từ app Gmail (`FN-03`) hoặc link đổi mật khẩu từ trình duyệt web ngoài (`FN-06`).
* **Độ bao phủ nhánh 100% toàn bộ codebase ứng dụng:** Không đặt mục tiêu bao phủ toàn bộ các widget hiển thị đồ họa thuần túy của Flutter framework.
* **Giới hạn 2.000 ký tự (BR-04):** Đã xác minh là UI Guideline thiết kế đề xuất, không áp dụng làm tiêu chí chặn cứng trong kiểm thử chức năng.

---

## 3. PHƯƠNG PHÁP VÀ CHIẾN LƯỢC KIỂM THỬ (TEST STRATEGY)

### 3.1. Các loại kiểm thử, phương pháp và lý do lựa chọn

Hệ thống kiểm thử áp dụng chiến lược kết hợp đa cấp độ, trong đó mỗi loại kiểm thử được lựa chọn dựa trên cơ sở kỹ thuật và đặc thù kiến trúc Offline-First:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              CHIẾN LƯỢC KIỂM THỬ TỔNG THỂ                              │
├───────────────────┬───────────────────────────┬────────────────────────────────────────┤
│    LOẠI TEST      │         PHẠM VI           │           CÔNG CỤ / KỸ THUẬT           │
├───────────────────┼───────────────────────────┼────────────────────────────────────────┤
│ 1. Hộp đen        │ Toàn bộ UI Flows, 11 nhóm │ Phân vùng tương đương (EP),            │
│    (Black-Box)    │ chức năng, 140 Exec Items │ Phân tích biên (BVA), Decision Table   │
├───────────────────┼───────────────────────────┼────────────────────────────────────────┤
│ 2. Hộp trắng      │ Data Models, Providers,   │ Flutter Test Native, LCOV,             │
│    (White-Box)    │ Firestore Security Rules  │ Line & Branch (BRDA) Coverage          │
├───────────────────┼───────────────────────────┼────────────────────────────────────────┤
│ 3. Tự động hóa    │ Smoke & Regression test   │ Python ADB/UI Runner, pytest,          │
│    (Automation)   │ các luồng cốt lõi         │ Flutter Driver / Unit Test Runner      │
├───────────────────┼───────────────────────────┼────────────────────────────────────────┤
│ 4. Phi chức năng  │ Offline-First, LWW, App   │ Airplane Mode, Multi-device Sync,      │
│ (Non-Functional)  │ Lifecycle Biometrics      │ Injection Payload, App Lifecycle Event │
└───────────────────┴───────────────────────────┴────────────────────────────────────────┘
```

1. **Kiểm thử Hộp đen (Black-Box Testing):**
   * **Phương pháp:** Phân vùng tương đương (Equivalence Partitioning), Phân tích giá trị biên (Boundary Value Analysis), Bảng quyết định (Decision Table), Kiểm thử chuyển đổi trạng thái (State Transition Testing). Thực thi thủ công trên thiết bị thật kết hợp chụp ảnh màn hình làm bằng chứng.
   * **Lý do lựa chọn:** Ứng dụng di động có tương tác người dùng phong phú (Rich-text, cử chỉ vuốt, bàn phím ảo, chuyển cảnh). Kiểm thử hộp đen là phương pháp duy nhất thẩm định chính xác trải nghiệm người dùng cuối, phản ứng giao diện trên môi trường thực tế Android 14 mà unit test không thể mô phỏng.
2. **Kiểm thử Hộp trắng chọn lọc (Selective White-Box Testing):**
   * **Phương pháp:** Kiểm thử đơn vị (Unit Test) phân tích cấu trúc mã nguồn, đo lường độ bao phủ dòng (Line Coverage) và rẽ nhánh logic (Branch Coverage) qua LCOV với cờ `--coverage --branch-coverage --fail-fast --concurrency=1`.
   * **Lý do lựa chọn:** Các module lõi (`NoteModel`, `ChecklistItem`, `Firestore Security Rules`) chứa nhiều nhánh rẽ xử lý kiểu dữ liệu dị thường (fallback CSV legacy, format JSON sai, thiếu trường SQLite). Kiểm thử hộp trắng cho phép cô lập logic, kiểm tra các trường hợp biên dữ liệu khó hoặc không thể kích hoạt từ UI, với tốc độ thực thi tức thì và độ ổn định cao.
3. **Kiểm thử Tự động hóa (Automation Testing):**
   * **Phương pháp:** Kịch bản Python tự động điều khiển thiết bị qua ADB (`automation/tests/`, `tools/fn23/`) kết hợp với Flutter Unit Test suite.
   * **Lý do lựa chọn:** Các kịch bản tìm kiếm nhiều biến thể (`FN-23`), kiểm tra ghim ghi chú lặp lại (`FN-20`), hoặc hồi quy sau khi sửa lỗi cần được chạy lại liên tục mà không tiêu tốn nhân lực thủ công.
4. **Kiểm thử Phi chức năng (Non-Functional Testing):**
   * **Phương pháp:** Ngắt kết nối vật lý (Airplane mode) kiểm tra tính khả dụng Offline-First (NFR-01); thiết lập xung đột dữ liệu đa thiết bị kiểm tra tính toàn vẹn LWW (NFR-02); kiểm tra cô lập dữ liệu người dùng qua Security Rules (NFR-03); kiểm tra khóa sinh trắc học theo vòng đời ứng dụng (NFR-05).
   * **Lý do lựa chọn:** Kiến trúc Offline-First phụ thuộc hoàn toàn vào tính toàn vẹn dữ liệu khi offline và thuật toán đồng bộ LWW. Nếu không kiểm thử phi chức năng, nguy cơ mất dữ liệu người dùng khi mất mạng hoặc xung đột đồng bộ là rất cao.

### 3.2. Phân loại ca kiểm thử đa chiều (Multi-Dimensional Classification)

> [!IMPORTANT]
> **Nguyên tắc phân loại:** Một ca kiểm thử có thể sở hữu nhiều thuộc tính kỹ thuật đồng thời. Tuyệt đối **không nhầm lẫn giữa Loại kiểm thử (Testing Type) với Giai đoạn dự án (Project Phase)**. Loại kiểm thử là thuộc tính kỹ thuật của ca test (hộp đen, hộp trắng, tự động, phi chức năng), trong khi Giai đoạn dự án là tiến trình thời gian thực hiện (Phase 1: Yêu cầu, Phase 2: Kế hoạch, Phase 3: Thiết kế, Phase 4: Thực thi, Phase 5: Báo cáo).

| Mã nhóm / Test Case | Hộp đen (Black-box) | Hộp trắng (White-box) | Tự động hóa (Automation) | Thủ công (Manual) | Chức năng (Functional) | Phi chức năng (Non-functional) | Giai đoạn thực thi (Project Phase) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `TC-BB-001` .. `005` (Auth FN-02) | X | | X | X | X | | Phase 4 (Đã thực thi) |
| `TC-BB-006` .. `009` (Login FN-04) | X | | X | X | X | | Phase 4 (Đã thực thi) |
| `TC-WB-001` .. `005` (Auth logic) | | X | X | | X | | Phase 4 (Đã thiết kế) |
| `test/checklist_test.dart` (5 tests) | | X | X | | X | | Phase 4 (Đã thực thi PASS) |
| `test/note_model_test.dart` (9 tests) | | X | X | | X | | Phase 4 (Đã thực thi PASS) |
| `test/security_rules_test.dart` (8 tests, `TC-WB-011..014`) | | X | X | | X (`REQ-11`) | X (Security `NFR-03`) | Phase 4 (Đã thực thi PASS) |
| `TC-BB-026` .. `029` (FN-23 Search 22 items) | X | | X | X | X | X (SQL Injection) | Phase 4 (Đã thực thi) |
| `TC-BB-012` .. `015F` (Biometrics FN-29/30) | X | | | X | X | X (Lifecycle NFR-05) | Phase 4 (Đã thực thi) |
| `TC-BB-030` .. `031D` (Sync LWW FN-40/41) | X | | X | X | X | X (Reliability NFR-01/02) | Phase 4 (Đã thực thi) |
| `TC-WB-015` .. `022` (8 White-box draft) | | X | X | | X | | Phase 2/3 (Kế hoạch mở rộng) |

---

## 4. MÔI TRƯỜNG, THIẾT BỊ, TÀI KHOẢN, DỮ LIỆU VÀ THỨ TỰ THỰC HIỆN

### 4.1. Môi trường phần cứng và thiết bị kiểm thử
* **Thiết bị A (Primary Target Device):**
  - Model: Samsung Galaxy S21 FE 5G (SM-G990E/DS).
  - Serial Number: `R5CW82ECF6M`.
  - Hệ điều hành: Android 14 (One UI 6.1, API 34).
  - Độ phân giải: $1080 \times 2340$ pixels.
  - Vai trò: Thiết bị chính thực thi toàn bộ kịch bản Black-box, UI interaction và Device 1 trong kiểm thử đồng bộ.
* **Thiết bị B (Secondary Target Device - Multi-Device & Conflict Testing):**
  - Model: Samsung Galaxy S24 FE (SM-S741B).
  - Hệ điều hành: Android 14 (API 34).
  - Vai trò: Thiết bị đối chứng chuyên dụng cho kiểm thử đồng bộ đám mây đa thiết bị (FN-40), tái hiện xung đột Last-Write-Wins (FN-41), và xác minh defect thiếu Tombstone (`BUG-002`).
* **Máy trạm điều khiển (Host Workstation):**
  - Hệ điều hành: Windows (x86_64).
  - Flutter SDK: `3.44.1 • channel stable`, Dart `3.x`.

---

## 5. TIẾN ĐỘ VÀ BẰNG CHỨNG ĐÃ GHI NHẬN (BASELINE AUDIT)

### 5.1. Kết quả Kiểm thử Hộp trắng (Baseline 18/18 Tests PASS)
- **Trạng thái thực thi:** **18/18 Unit Tests PASS (100%)**, Exit Code: `0` (xác thực qua log `evidence/white_box/note_model_run_20261010_0945/test_execution.log`).
  - `test/checklist_test.dart`: 5 tests PASS.
  - `test/checklist_copy_with_test.dart`: 4 tests PASS.
  - `test/note_model_test.dart`: 9 tests PASS (Bao phủ `toMap`, `fromMap`, `_decodeStringList`).
- **Độ bao phủ trên phạm vi đo lường 2 Model (`ChecklistItem` & `Note`):**
  - **Line Coverage:** 69/138 dòng (**50.00%**).
  - **LCOV BRDA (Branch):** 21/41 bản ghi (**51.22%**).
- **Vị trí lưu trữ Bằng chứng & Mã băm:**
  - Checksum `test_execution.log`: `d8448a1d37547defb293b5326b6e6147e495c890aba93ed63f389376505bf00e`.
  - Checksum `lcov.info`: `c5244d2a160ef10b33f272b6abebf7b0828e1bacee9fc49dbc07d1ad04c05324`.
- **Giới hạn kỹ thuật đã ghi nhận (Không suy đoán):**
  - Độ bao phủ 50.00% dòng chỉ áp dụng cho 2 file model được đo, không đại diện cho toàn bộ codebase `lib/`.
  - Các module `SearchService` và `EncryptionService` chưa có trong bộ 18 unit tests do chưa có log thực thi tương ứng.

### 5.2. Kết quả Kiểm thử Hộp đen (Baseline 140 Execution Items)
- **Phạm vi chốt:** 11 nhóm có Execution Sheet (10 nhóm ban đầu + Checklist FN-15..19).
- **Tổng số Execution Items:** **140 items**.
  - **Executed (không tính BLOCKED):** **139 items (99.29%)**.
  - **PASS:** **131 items (94.24% / Executed)**.
  - **FAIL:** **6 items (4.32% / Executed)** (ánh xạ vào các defect đã ghi nhật ký).
  - **Chưa đủ căn cứ:** **2 items (1.44% / Executed)** (`TC-BB-026B-D03` tìm không dấu giữ nguyên trạng thái gốc `CHƯA ĐỦ CĂN CỨ` và giải tỏa theo `BR-01`, không tự chuyển thành `PASS`; `TC-BB-031C-D01` sửa vs xóa offline giữ nguyên trạng thái gốc và giải tỏa theo `BR-02`).
  - **BLOCKED:** **1 item (0.71%)** (`TC-BB-015G-D01` do ràng buộc an toàn vân tay).
  - **Pending:** **0 items (0.00%)**.

---

## 6. THEO DÕI PHẠM VI VÀ KẾ HOẠCH RETEST / REGRESSION CHO CÁC LỖI ĐÃ BIẾT

### 6.1. Bảng theo dõi phạm vi 11 nhóm chức năng chính thức

| STT | Nhóm chức năng | File Execution Sheet | Số Exec Items | PASS | FAIL | Chưa đủ căn cứ | BLOCKED | Trạng thái nhóm |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | **FN-02:** Đăng ký Email/Password | `fn02_execution_sheet.md` | 19 | 18 | 1 | 0 | 0 | Đã chạy (1 Bug validation `BUG-FN02-01`) |
| 2 | **FN-04:** Đăng nhập Email/Form | `fn04_execution_sheet.md` | 16 | 14 | 2 | 0 | 0 | Đã chạy (2 Bugs `BUG-BB-002`, `BUG-BB-003`) |
| 3 | **FN-05:** Đăng nhập Google OAuth | `fn05_execution_sheet.md` | 8 | 8 | 0 | 0 | 0 | PASS 100% |
| 4 | **FN-08:** Tạo ghi chú & Autosave | `fn08_execution_sheet.md` | 8 | 8 | 0 | 0 | 0 | PASS 100% |
| 5 | **FN-09:** Rich-text & Cập nhật note | `fn09_execution_sheet.md` | 12 | 12 | 0 | 0 | 0 | Đã chạy (1 Glitch `BUG-005`) |
| 6 | **FN-10/11/12:** Thùng rác & Lưu trữ | `fn10_fn11_fn12_execution_sheet.md` | 12 | 12 | 0 | 0 | 0 | PASS 100% |
| 7 | **FN-15..19:** Ghi chú Checklist | `fn15_fn19_checklist_execution_sheet.md` | 6 | 6 | 0 | 0 | 0 | PASS 100% |
| 8 | **FN-20:** Ghim ghi chú (Pin) | `fn20_execution_sheet.md` | 15 | 15 | 0 | 0 | 0 | PASS 100% |
| 9 | **FN-23:** Tìm kiếm & Bộ lọc | `fn23_execution_sheet.md` | 22 | 20 | 1 | 1 | 0 | Đã chạy 22/22 (1 Bug `BUG-004`; 1 ca theo BR-01) |
| 10 | **FN-29/30:** Bảo mật sinh trắc học | `fn29_fn30_execution_sheet.md` | 12 | 11 | 0 | 0 | 1 | Đã chạy (1 BLOCKED an toàn vân tay) |
| 11 | **FN-40/41:** Đồng bộ Offline LWW | `fn40_fn41_execution_sheet.md` | 10 | 7 | 2 | 1 | 0 | Đã chạy (2 Bugs `BUG-002`, `BUG-003`; 1 ca theo BR-02) |
| **Tổng** | **11 nhóm chính thức** | **11 execution sheets** | **140** | **131** | **6** | **2** | **1** | **100% PHÂN ĐỊNH** |

### 6.2. Kế hoạch Retest và Regression cho các lỗi đã biết (BUG-001 đến BUG-005, BUG-FN02-01, BUG-BB-002, BUG-BB-003)

Toàn bộ 8 lỗi phần mềm được quản lý tại [defect_log.md](../bugs/defect_log.md). Kế hoạch kiểm thử lại khi Developer bàn giao bản sửa lỗi như sau:

| Mã Bug | Mức nghiêm trọng | Tóm tắt lỗi | Ca Retest trực tiếp (Direct Retest) | Phạm vi kiểm thử hồi quy (Regression Scope) |
|:---|:---:|:---|:---|:---|
| **BUG-001** | High | Tải ảnh lên Cloudinary bị treo vô hạn thiếu timeout | `TC-BB-018C`, `TC-BB-027B-D01`, `TC-BB-036` (Tải ảnh từ thư viện, kiểm tra timeout 30s và bắt lỗi mạng) | • Tạo ghi chú văn bản thuần (`FN-08`)<br>• Đính kèm nét vẽ tay (`FN-35`)<br>• Lưu trữ và mở lại ghi chú có ảnh |
| **BUG-002** | Critical | Xóa note offline không sync xóa sang thiết bị khác do thiếu Tombstone | `TC-BB-030C-D01` (Xóa vĩnh viễn trên Thiết bị A khi offline, bật mạng lại, kiểm tra Thiết bị B) | • Tạo / Sửa ghi chú offline đa thiết bị (`FN-40`)<br>• Khôi phục ghi chú từ Thùng rác (`FN-11`)<br>• Tính nhất quán của `pending_delete_service.dart` |
| **BUG-003** | Medium | HomeScreen thiếu cử chỉ vuốt kéo làm mới (Pull-to-refresh) | `TC-BB-030F-D01` (Kéo vuốt màn hình Trang chủ trên Thiết bị B để cập nhật note từ Thiết bị A) | • Danh sách hiển thị ghi chú Trang chủ (`HomeScreen`)<br>• Vị trí nhóm ghi chú ghim / không ghim (`FN-20`)<br>• Cuộn danh sách Grid / List view (`FN-28`) |
| **BUG-004** | Medium | Bộ lọc `has:list` query LIKE thô, trả về rỗng | `TC-BB-027G-D01` (Chạm chip 'Danh sách' hoặc gõ `has:list` trên SearchScreen) | • Các bộ lọc chip khác: `has:image`, `has:audio`, `has:url`, `is:pinned`, `is:archived`, `label:name`<br>• Tìm kiếm từ khóa text thông thường qua SQL LIKE (`FN-23`) |
| **BUG-005** | Minor | Vệt sọc vàng đen tràn viền thoáng qua khi xóa trắng tiêu đề/nội dung | Luồng xóa trắng tiêu đề (TH1) và nội dung (TH2) rồi nhấn Back về Home | • Hiển thị NoteCard trên Trang chủ<br>• Thao tác đổi màu ghi chú (`FN-37`)<br>• Autosave khi thoát màn hình Editor |
| **BUG-FN02-01** | Minor | Lỗi validation chuỗi form Đăng ký | `TC-BB-002`, `TC-BB-003` (Nhập email không hợp lệ, mật khẩu ngắn) | • Toàn bộ luồng đăng ký tài khoản thành công (`TC-BB-001`) |
| **BUG-BB-002** | Minor | Icon ẩn/hiện mật khẩu form Đăng nhập | `TC-BB-009D` (Chạm toggle ẩn/hiện mật khẩu) | • Đăng nhập với mật khẩu đúng / sai (`TC-BB-006`, `007`) |
| **BUG-BB-003** | Minor | Xử lý khoảng trắng đầu/cuối khi đăng nhập | `TC-BB-006C` (Nhập email có khoảng trắng đầu/cuối) | • Đăng nhập tài khoản hợp lệ |

### 6.3. Kế hoạch quản lý và xử lý các ca BỊ CHẶN (BLOCKED Cases)

> [!CAUTION]
> **Quy tắc bất biến:** Tuyệt đối **KHÔNG TÍNH CÁC CA BLOCKED LÀ PASS**. Các ca bị chặn phải giữ nguyên trạng thái `BLOCKED` trong mọi bảng thống kê cho đến khi điều kiện tiên quyết được tháo gỡ.

1. **Trợ lý Gemini AI (`FN-31`, `FN-32`, `FN-33` - REQ-13):**
   * **Hiện trạng:** Trong đợt thực thi thủ công Kịch bản 5 trên máy thật ([Testing_Report.md](../test_report/Testing_Report.md) / [black_box_execution_summary.md](../qa/black_box_execution_summary.md)), 3 trường hợp `FN-31..33` bị chặn (**`3 BLOCKED`**) do giao diện trả về khung thông báo lỗi màu đỏ trên máy thật. Ba ca kiểm thử chính thức mới được thiết kế tại [black_box_test_cases.md](../../test_cases/black_box/black_box_test_cases.md) và [test_case_design_inventory_44_fn.md](./test_case_design_inventory_44_fn.md) gồm `TC-BB-032` (`FN-31`), `TC-BB-032B` (`FN-32`), `TC-BB-032C` (`FN-33`) giữ trạng thái **`NOT RUN` (Chưa có evidence riêng — chờ gỡ `BLOCKED`)**.
   * **Nguyên nhân kỹ thuật:** Chưa xác định (chưa có log response HTTP chi tiết hay exception từ Firebase AI SDK trong logcat; tuyệt đối không suy đoán do quota hay API key khi chưa có bằng chứng).
   * **Điều kiện tháo gỡ (Unblock Criteria):** Developer / DevOps trích xuất logcat chi tiết hoặc cấu hình môi trường AI API hoạt động ổn định trên thiết bị thật để thực thi 3 ca `TC-BB-032`, `TC-BB-032B`, `TC-BB-032C`.
2. **Xóa dấu vân tay hệ thống (`TC-BB-015G-D01` - FN-29/FN-30):**
   * **Hiện trạng:** Bị chặn do quy tắc an toàn thiết bị thật (tránh làm mất cấu hình bảo mật cá nhân trên điện thoại thật của tester).
   * **Điều kiện tháo gỡ:** Chỉ thực thi khi có môi trường máy ảo Android Emulator cô lập chuyên dụng. Trong điều kiện thiết bị hiện tại, ca này giữ nguyên trạng thái `BLOCKED` vĩnh viễn.
3. **Làm đầy bộ nhớ thiết bị (`FN-44`):**
   * **Hiện trạng:** Bị chặn do nguy cơ gây treo hệ điều hành thiết bị thật.
   * **Điều kiện tháo gỡ:** Giữ nguyên trạng thái `BLOCKED` an toàn; chỉ thực thi trên môi trường sandbox có khả năng snapshot khôi phục.

---

## 7. CÁC MỐC KỸ THUẬT, LỊCH THỰC HIỆN VÀ PHÂN CÔNG (SCHEDULE & RESOURCES)

### 7.1. Các mốc kỹ thuật (Milestones)

```
[Mốc 1: Baseline & condensed SRS] ──► (HOÀN THÀNH - Giai đoạn 1 đóng)
                │
                ▼
[Mốc 2: Master Test Plan & Strategy] ──► (HOÀN THÀNH - Giai đoạn 2 đóng)
                │
                ▼
[Mốc 3: Kiểm tra Tiến độ Môn học] ──► (XÁC NHẬN: Ngày 14/10/2026)
                │
                ▼
[Mốc 4: Mở khóa Defects & Retest] ──► (Phụ thuộc Dev cung cấp bản build sửa lỗi)
                │
                ▼
[Mốc 5: Nghiệm thu & Đóng gói Dự án] ──► (Hạn nộp chính thức: Chưa công bố / Chưa xác nhận)
```

### 7.2. Lịch thực hiện và phân công thực tế (Resource Allocation)
* **Nhân sự thực hiện:** Nhóm sinh viên thực hiện kiểm thử trên branch `huong`.
* **Tiến độ đã xác nhận:**
  - Ngày 11/10/2026: Hoàn tất Giai đoạn 1 (SRS rút gọn) và Giai đoạn 2 (Master Test Plan & Test Strategy).
  - Ngày 14/10/2026: **Mốc kiểm tra tiến độ môn học** (Trình bày slide [progress_check_slides_outline.md](../test_report/progress_check_slides_outline.md), demo thực tế trên 2 thiết bị S21 FE & S24 FE, báo cáo minh bạch 140 execution items và nhật ký lỗi).
* **Nội dung chưa thể lập lịch chi tiết do thiếu thông tin:**
  - Hạn nộp báo cáo cuối kỳ chính thức: Chưa được Giảng viên công bố $\rightarrow$ Giữ trạng thái **Chưa xác nhận**.
  - Lịch trình bàn giao bản build sửa lỗi từ Dev: Chưa có cam kết thời gian từ phía lập trình $\rightarrow$ Kế hoạch Retest được kích hoạt ngay khi nhận build mới.

---

## 8. TIÊU CHÍ BẮT ĐẦU, TẠM DỪNG, TIẾP TỤC VÀ KẾT THÚC (CRITERIA & SEVERITY)

### 8.1. Phân loại mức độ nghiêm trọng của lỗi (Defect Severity Levels)
* **Critical (Blocker - Severity 1):** Lỗi gây crash ứng dụng, mất dữ liệu người dùng, hoặc sai lệch dữ liệu đồng bộ nghiêm trọng giữa các thiết bị mà không có giải pháp thay thế (ví dụ: `BUG-002` thiếu Tombstone làm tồn tại vĩnh viễn note đã xóa).
* **High (Major - Severity 2):** Tính năng chính bị tê liệt hoặc treo vô hạn, làm nghẽn các ca kiểm thử khác nhưng ứng dụng không crash (ví dụ: `BUG-001` upload ảnh treo vô hạn).
* **Medium (Normal - Severity 3):** Tính năng nghiệp vụ hoạt động sai logic hoặc không phản hồi đúng mong đợi nhưng có giải pháp tạm thời (ví dụ: `BUG-003` thiếu pull-to-refresh, `BUG-004` lọc `has:list` trả về rỗng).
* **Low (Minor - Severity 4):** Lỗi thẩm mỹ, vệt giao diện chớp nhoáng, lỗi validate chuỗi nhỏ, không ảnh hưởng đến dữ liệu hay luồng nghiệp vụ chính (ví dụ: `BUG-005` vệt tràn viền thoáng qua, `BUG-BB-002` icon toggle password).

### 8.2. Tiêu chí Bắt đầu (Entry Criteria)
* Mã nguồn ứng dụng trên branch `huong` biên dịch thành công, không có lỗi phân tích tĩnh cú pháp.
* Thiết bị kiểm thử (Samsung S21 FE và Samsung S24 FE) kết nối ổn định qua ADB (`adb devices`).
* Kế hoạch kiểm thử (Test Plan) và tài liệu yêu cầu (Condensed SRS) đã được phê duyệt.
* Tài khoản kiểm thử (Account-01 đến Account-04) và tập dữ liệu mẫu đã sẵn sàng.

### 8.3. Tiêu chí Tạm dừng (Suspension Criteria)
Kiểm thử phải **ngay lập tức tạm dừng** khi:
1. Phát sinh lỗi Critical khiến ứng dụng crash liên tục ngay khi khởi động hoặc treo màn hình chính.
2. Thiết bị mất kết nối ADB, mất quyền truy cập Firebase, hoặc dịch vụ phụ thuộc ngắt kết nối diện rộng.
3. Chế độ `--fail-fast` trong test suite tự động phát hiện test assertion thất bại (dừng lại để cách ly dữ liệu và phân tích log).

### 8.4. Tiêu chí Tiếp tục (Resumption Criteria)
* Lỗi Blocker đã được cô lập hoặc có bản vá tạm thời được phê duyệt.
* Kết nối thiết bị hoặc dịch vụ đám mây được phục hồi ổn định.
* Dữ liệu kiểm thử trên thiết bị đã được dọn sạch về trạng thái chuẩn (Clean State).

### 8.5. Tiêu chí Hoàn thành (Exit Criteria)
* 100% các yêu cầu nghiệp vụ cốt lõi (P1) đã được kiểm thử và đạt trạng thái PASS (hoặc có giải trình kỹ thuật minh bạch).
* Không còn lỗi mức độ Critical hoặc High ở trạng thái OPEN mà chưa có phân tích nguyên nhân và phương án khắc phục.
* Toàn bộ các ca BLOCKED được giải trình minh bạch lý do và phân định ranh giới rõ ràng.
* Mọi lượt chạy test đều có bằng chứng log/screenshot được lưu trữ với mã băm xác thực.

---

## 9. QUY TẮC QUẢN LÝ BẰNG CHỨNG VÀ SẢN PHẨM BÀN GIAO

### 9.1. Quy tắc Lưu trữ Bằng chứng (Evidence Integrity Rules)
* **Quy chuẩn đặt tên ảnh:** `FN<Mã_Chức_Năng>_TC-BB-<Mã_Test_Case>_D<Mã_Dữ_Liệu>_<Số_Thứ_Tự>.png`.
* **Tính nguyên vẹn:** Ảnh chụp màn hình phải giữ nguyên thanh trạng thái hệ thống và giao diện ứng dụng, không cắt ghép chỉnh sửa.
* **Quy chuẩn Log & LCOV:** Mỗi lượt chạy kiểm thử tự động/hộp trắng phải được lưu trong thư mục riêng biệt kèm dấu thời gian và mã băm SHA-256 xác thực.

### 9.2. Danh mục Sản phẩm bàn giao (Deliverables)
1. Đặc tả yêu cầu rút gọn: [srs_condensed.md](./srs_condensed.md).
2. Kế hoạch kiểm thử tổng thể: [test_plan.md](./test_plan.md).
3. Kế hoạch kiểm thử hộp trắng chọn lọc: [white_box_test_plan.md](./white_box_test_plan.md).
4. Ma trận truy vết yêu cầu: [requirements_traceability_matrix.md](./requirements_traceability_matrix.md).
5. Hồ sơ 11 Execution Sheets: Thư mục `test_cases/execution_sheets/` và `test_cases/black_box/`.
6. Nhật ký theo dõi lỗi: [defect_log.md](../bugs/defect_log.md).
7. Báo cáo thực thi kiểm thử hộp đen: [black_box_execution_summary.md](../qa/black_box_execution_summary.md).
8. Dàn ý Slide báo cáo tiến độ: [progress_check_slides_outline.md](../test_report/progress_check_slides_outline.md).

---

## 10. RỦI RO, GIỚI HẠN VÀ QUY TẮC NGHIỆP VỤ MỞ BR-03

### 10.1. Xử lý Quy tắc nghiệp vụ mở BR-03 (Tie-break Rule khi trùng millisecond `updatedAt`)
* **Hiện trạng mã nguồn:** Trong [lib/repositories/sync_repository.dart](../../lib/repositories/sync_repository.dart#L67-L129), cả chiều Push và Pull đều dùng toán tử so sánh ngặt `isAfter`. Khi hai bản ghi Local và Cloud có cùng mốc thời gian `updatedAt` từng millisecond (`isAtSameMomentAs`), cả hai biểu thức `isAfter` đều trả về `false`.
* **Ảnh hưởng kỹ thuật (Impact Analysis):** Hệ thống bỏ qua không đồng bộ (không đẩy lên Cloud, không kéo về Local, cờ `is_synced` trên Local giữ nguyên `0`). Nếu nội dung hai bên có sự sai lệch, hai bản ghi sẽ rơi vào trạng thái bế tắc đồng bộ vĩnh viễn (Sync Standoff) cho đến khi một bên có sửa đổi mới làm thay đổi timestamp.
* **Phương án xử lý tạm thời trong Test Planning:**
  - Giữ nguyên trạng thái **`NEEDS CONFIRMATION (CẦN XÁC NHẬN NGHIỆP VỤ)`** cho quy tắc phân xử hòa `BR-03`.
  - **Tuyệt đối không tự ý chọn bản Cloud hay bản Local** làm chuẩn trong kế hoạch kiểm thử.
  - Ca kiểm thử hộp trắng **`TC-WB-021`** đang ở trạng thái **`DESIGN ONLY`** (chưa chạy thực thi), chỉ xác minh toán tử so sánh `updatedAt.isAfter` độc lập trong bộ nhớ; việc đặt assertion cho kết quả đồng bộ cuối cùng khi trùng timestamp sẽ chỉ được kích hoạt sau khi PO / Giảng viên đưa ra quyết định chính thức.

### 10.2. Rủi ro và Biện pháp giảm thiểu
| Rủi ro | Mức độ | Tác động | Biện pháp giảm thiểu |
|---|:---:|---|---|
| **Lỗi `BUG-001` làm nghẽn kịch bản upload media** | Cao | Không thể tạo note ảnh trực tiếp từ UI | Tạo sẵn dữ liệu mẫu chứa ảnh trực tiếp trên SQLite/Firestore để phục vụ các kịch bản phụ thuộc |
| **Phụ thuộc quota Gemini AI & Firebase** | Trung bình | Gây lỗi gián đoạn kịch bản AI | Giữ các ca AI ở trạng thái BLOCKED minh bạch, chờ logcat chính thức từ Dev |
| **Dart VM LCOV BRDA không phân biệt nhánh nhị phân** | Thấp | Dễ gây hiểu lầm về độ bao phủ nhánh thực tế | Minh bạch định nghĩa: Báo cáo rõ đây là số lượng bản ghi BRDA do Dart sinh ra |

---

## 11. ĐỀ XUẤT LƯỢT THỰC THI HỘP TRẮNG TIẾP THEO (SELECTIVE WHITE-BOX EXTENSION)

* **Kế hoạch tham chiếu:** [white_box_test_plan.md](./white_box_test_plan.md) và [white_box_test_cases.md](../../test_cases/white_box/white_box_test_cases.md).
* **Mục tiêu:** Nâng cao độ bao phủ logic cho các phương thức cốt lõi của `NoteModel` và `ChecklistItem` mà không cần thiết bị thật (đồng bộ 100% với 8 ca mở rộng `TC-WB-015` .. `TC-WB-022` ở trạng thái `DESIGN ONLY`):
  1. `Note.pendingChecklistCount` — đếm công việc chưa hoàn thành trong Checklist (`TC-WB-015` $\rightarrow$ `REQ-06 / FN-15`).
  2. `Note.plainTextContent` — bóc tách văn bản thuần từ Quill Delta JSON (`TC-WB-016` $\rightarrow$ `REQ-05 / REQ-08 / FN-09, FN-23`).
  3. `Note.plainTextContent` — xử lý chuỗi rỗng, văn bản thô và JSON lỗi (`TC-WB-017` $\rightarrow$ `REQ-05 / FN-09`).
  4. `Note.copyWith(clearReminder)` — cơ chế xóa nhắc nhở về `null` qua cờ `clearReminder` (`TC-WB-018` $\rightarrow$ `REQ-12 / FN-38`).
  5. `Note.copyWith(updatedAt)` — tự sinh `DateTime.now()` vs gán timestamp ngoài (`TC-WB-019` $\rightarrow$ `REQ-05 / REQ-11 / FN-09, FN-41`).
  6. `Note.fromMap` — phòng thủ SQLite map thiếu trường thời gian `created_at` / `updated_at` (`TC-WB-020` $\rightarrow$ `REQ-04 / NFR-01 / FN-08`).
  7. Logic so sánh mốc thời gian `updatedAt.isAfter` độc lập trong bộ nhớ (`TC-WB-021` $\rightarrow$ `REQ-11 / FN-41`, trạng thái `DESIGN ONLY`; quy tắc hòa `BR-03` giữ `NEEDS CONFIRMATION`).
  8. `ChecklistItem.fromJson` — chịu lỗi khi JSON khuyết trường `id`, `text`, `checked` (`TC-WB-022` $\rightarrow$ `REQ-06 / FN-15`).
* **Kỳ vọng:** Nâng độ bao phủ dòng của `lib/models/note_model.dart` từ 44.35% lên trên **70%**, và tổng độ bao phủ đo lường lên trên **75%**.

---
*Tài liệu được cập nhật và bảo toàn nguyên trạng theo nguyên tắc Read-Only; chưa thực hiện bất kỳ lệnh thay đổi mã nguồn ứng dụng, test mới hay git commit/push nào.*
