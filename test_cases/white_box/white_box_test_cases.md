# TÀI LIỆU ĐẶC TẢ THIẾT KẾ KIỂM THỬ HỘP TRẮNG (WHITE-BOX TEST DESIGN SPECIFICATION)
## Dự án: Smart Note App
**Branch:** `huong`  
**Tiêu chuẩn áp dụng:** IEEE 829 Standard for Test Design Specification & ISTQB White-box Testing  
**Trạng thái tài liệu:** **ĐÃ HOÀN THIỆN VÀ CHỐT (FROZEN SPECIFICATION) — CHỜ PHÊ DUYỆT THỰC THI**  
**Cam kết tuân thủ:** Không sửa đổi mã nguồn `lib/`, không viết mã test mới khi chưa phê duyệt, không chạy `flutter test`/`flutter pub get`, bảo toàn 100% bằng chứng kiểm thử hộp đen và baseline 18 unit tests.

---

## I. TỔNG QUAN, PHÂN LOẠI KHẢ THI KỸ THUẬT VÀ DANH MỤC 22 TEST CASES (TC-WB-001 ĐẾN TC-WB-022)

### 1.1. Nguyên tắc thiết kế, phân cấp ưu tiên và phân loại môi trường / dependency (Không sửa `lib/`)
- **P1 (High Priority - Phạm vi thực thi mở rộng trọng tâm — Pure In-Memory):** Bao gồm các hàm xử lý logic nghiệp vụ cốt lõi trên Model và toán tử thời gian (`TC-WB-015`, `TC-WB-016`, `TC-WB-017`, `TC-WB-019`, `TC-WB-021`), cùng 3 ca P2 bổ trợ trực tiếp trên cùng file model (`TC-WB-018`, `TC-WB-020`, `TC-WB-022`). Toàn bộ 8 ca `TC-WB-015..022` đều truy cập qua API `public` và chạy **100% thuần trong bộ nhớ (Pure In-Memory)** trên Dart VM mà không cần sửa `lib/`.
- **Phân loại môi trường và khả năng thực thi của `TC-WB-001..014` dưới ràng buộc không sửa `lib/`:**
  1. **Nhóm B1 — Có thể kiểm thử qua Public Entry Point / Guard Clause trong bộ nhớ (`TC-WB-006`, `TC-WB-008`):**
     - `_extractPublicId` là hàm **library-private** (`_`) trong `lib/services/cloudinary_service.dart`, không thể gọi trực tiếp từ `test/`. Tuy nhiên, `TC-WB-006` (nhánh `rootIndex == -1` trả về `null`) hoàn toàn kích hoạt được thông qua phương thức public `CloudinaryService().deleteFile(invalidUrl)` (trả về `false` tại dòng 55–57 trước khi gọi HTTP).
     - `TC-WB-008` kích hoạt trực tiếp qua `CloudinaryService().uploadImage(...)` sau khi nạp `dotenv.testLoad(fileInput: '')` (ngắt sớm tại guard clause dòng 114–117 trước khi đọc file hay gửi mạng).
  2. **Nhóm B2 — Yêu cầu `HttpOverrides` / Local Mock Server & File tạm (`TC-WB-007`, `TC-WB-009`, `TC-WB-010`):**
     - `CloudinaryService` gọi cứng `http.post` và `http.MultipartRequest` (không có constructor DI). Để kiểm thử `TC-WB-007` (xác minh `public_id` đã cắt đuôi file qua hàm public `deleteFile(validUrl)`) và `TC-WB-009`, `010` (`uploadImage`), cần nạp `dotenv.testLoad(...)`, tạo `File` tạm và bọc trong `HttpOverrides.runZoned` (hoặc `http.runWithClient`). Các ca này giữ ở mức `DESIGN ONLY (Requires HttpOverrides & DotEnv Harness)`.
  3. **Nhóm C — Kiểm thử mô phỏng biểu thức quy tắc bằng Dart (`TC-WB-011` .. `TC-WB-014`):**
     - Đã được hiện thực hóa dưới dạng hàm mô phỏng logic (`Rule Evaluation Simulation`) trong `test/security_rules_test.dart` (8 tests PASS). **Lưu ý kỹ thuật:** Đây là kiểm thử mô phỏng logic quy tắc trong bộ nhớ Dart, **KHÔNG đánh đồng** với việc chạy kiểm thử trực tiếp trên **Firebase Emulator Rules Engine** thực tế.
  4. **Nhóm D — Bị chặn bởi Static Singleton & Library-Private Visibility khi không sửa `lib/` (`TC-WB-001` .. `TC-WB-005`):**
     - Constructor `AuthProvider()` gọi trực tiếp `FirebaseAuth.instance.currentUser` và `FirebaseAuth.instance.authStateChanges()`, còn `_syncUserProfile` là hàm **library-private** (`_`) gọi trực tiếp `FirebaseFirestore.instance`. Do không được sửa `lib/` để tiêm phụ thuộc (Dependency Injection), không thể khởi tạo `AuthProvider` hay gọi trực tiếp `_syncUserProfile` từ `test/` nếu không cấu hình MethodChannel/Pigeon platform mocks phức tạp. Do đó, `TC-WB-001..005` được đánh dấu rõ giới hạn **`DESIGN ONLY (Blocked without Firebase Platform Mock / DI)`**, không tự nhận là `READY` cho thực thi trực tiếp.

### 1.2. Bảng tổng hợp trạng thái, dependency và tính khả thi của 22 Test Cases

| Mã Test Case | Module & Phương thức thực tế | Đường gọi từ `test/` & Dependency | Ánh xạ REQ / FN | Kỹ thuật White-box | Nhánh / Điều kiện bao phủ | Ưu tiên | Trạng thái & Tính khả thi (Không sửa `lib/`) |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| **TC-WB-001** | `AuthProvider.setError(message)` | Public method; nhưng `AuthProvider()` cần `FirebaseAuth.instance` | REQ-02 / FN-01 | Statement & State | Nhánh `message != null` $\rightarrow$ gán `_error` & notify | **P2** | `DESIGN ONLY` *(Cần Firebase Platform Mock)* |
| **TC-WB-002** | `AuthProvider.setError(message)` | Public method; nhưng `AuthProvider()` cần `FirebaseAuth.instance` | REQ-02 / FN-01 | Statement Coverage | Nhánh `message == null` $\rightarrow$ xóa `_error` & notify | **P2** | `DESIGN ONLY` *(Cần Firebase Platform Mock)* |
| **TC-WB-003** | `AuthProvider` stream listener | Stream `FirebaseAuth.instance.authStateChanges()` | REQ-02 / FN-07 | Branch Coverage | Nhánh `user == null` $\rightarrow$ `_userData = null` | **P2** | `DESIGN ONLY` *(Cần Firebase Platform Mock)* |
| **TC-WB-004** | `AuthProvider._syncUserProfile()` | **Private (`_`)** — gọi qua public `reloadUserData()` / `registerWithEmail()`; cần `FirebaseFirestore.instance` | REQ-01 / FN-02 | Decision Coverage | Nhánh `!snapshot.exists == true` $\rightarrow$ tạo profile | **P2** | `DESIGN ONLY` *(Private + Singleton acoplamiento)* |
| **TC-WB-005** | `AuthProvider._syncUserProfile()` | **Private (`_`)** — gọi qua public `reloadUserData()` / `signInWithEmail()`; cần `FirebaseFirestore.instance` | REQ-02 / FN-04 | Decision Coverage | Nhánh `!snapshot.exists == false` $\rightarrow$ đọc snapshot | **P2** | `DESIGN ONLY` *(Private + Singleton acoplamiento)* |
| **TC-WB-006** | `CloudinaryService._extractPublicId()` | **Private (`_`)** — gọi qua public `deleteFile(url)` (ngắt sớm trước HTTP) | REQ-09 / FN-12 (Chính), REQ-12 / FN-35, 36 (Phụ) | Branch & Guard | Nhánh `rootIndex == -1` $\rightarrow$ `publicId == null` $\rightarrow$ `deleteFile` trả về `false` | **P2** | `DESIGN ONLY` *(Khả thi qua `deleteFile`)* |
| **TC-WB-007** | `CloudinaryService._extractPublicId()` | **Private (`_`)** — gọi qua public `deleteFile(url)` + cần `dotenv` & `HttpOverrides` | REQ-09 / FN-12 (Chính), REQ-12 / FN-35, 36 (Phụ) | Statement & Branch | Nhánh `publicId.contains('.') == true` (Cắt đuôi file gửi trong body `destroy`) | **P2** | `DESIGN ONLY` *(Cần `dotenv` + `HttpOverrides`)* |
| **TC-WB-008** | `CloudinaryService.uploadImage()` | Public `uploadImage()` + `dotenv.testLoad(fileInput: '')` (ngắt sớm) | REQ-12 / FN-36 | Decision (Guard) | Nhánh `_cloudName.isEmpty \|\| _uploadPreset.isEmpty` $\rightarrow$ `null` | **P2** | `DESIGN ONLY` *(Khả thi qua `dotenv.testLoad`)* |
| **TC-WB-009** | `CloudinaryService.uploadImage()` | Public `uploadImage()` + cần `dotenv`, `File` tạm & `HttpOverrides` | REQ-12 / FN-35, 36 | Multiple Condition | Điều hướng `isAvatar` vs `isDrawing` vs `image` | **P3** | `DESIGN ONLY` *(Cần `HttpOverrides` + `File`)* |
| **TC-WB-010** | `CloudinaryService.uploadImage()` | Public `uploadImage()` + cần `dotenv`, `File` tạm & `HttpOverrides` | REQ-12 / FN-36 | Branch Coverage | Nhánh `response.statusCode == 200` $\rightarrow$ lấy `secure_url` | **P2** | `DESIGN ONLY` *(Cần `HttpOverrides` + `File`)* |
| **TC-WB-011** | `firestore.rules` - `isOwner()` | Mô phỏng logic Dart (`test/security_rules_test.dart`) — *Không phải Emulator* | REQ-11 / NFR-03 / FN-40 | Condition Coverage | `isAuthenticated() && auth.uid == userId` (True & True) | **P2** | `DESIGNED (Dart Rule Simulation PASS)` |
| **TC-WB-012** | `firestore.rules` - `isOwner()` | Mô phỏng logic Dart (`test/security_rules_test.dart`) — *Không phải Emulator* | REQ-11 / NFR-03 / FN-40 | Condition Coverage | `auth == null` $\rightarrow$ Deny truy cập (False & _) | **P2** | `DESIGNED (Dart Rule Simulation PASS)` |
| **TC-WB-013** | `firestore.rules` - `isOwner()` | Mô phỏng logic Dart (`test/security_rules_test.dart`) — *Không phải Emulator* | REQ-11 / NFR-03 / FN-40 | Condition Coverage | `auth.uid != userId` $\rightarrow$ Deny chéo (True & False) | **P2** | `DESIGNED (Dart Rule Simulation PASS)` |
| **TC-WB-014** | `firestore.rules` - `isValidNote()` | Mô phỏng logic Dart (`test/security_rules_test.dart`) — *Không phải Emulator* | REQ-11 / NFR-03 / FN-40 | Statement & Decision | `resource.data.user_id == userId` (Chính chủ) | **P2** | `DESIGNED (Dart Rule Simulation PASS)` |
| **TC-WB-015** | `Note.pendingChecklistCount` | Public getter — **Pure In-Memory** (`note_model.dart`) | REQ-06 / FN-15 | Branch & Exception | `!isChecklist`, `items ?? []`, `checked != true`, và `catch (_)` | **P1** | `DESIGN ONLY` — **READY (In-Memory)** |
| **TC-WB-016** | `Note.plainTextContent` | Public getter — **Pure In-Memory** (`note_model.dart`) | REQ-05, REQ-08 / FN-09, 23 | Branch, Condition & Loop | Duyệt Delta List: `item is Map` (T/F), `containsKey('insert')` (T/F), `val is String` (T/F) | **P1** | `DESIGN ONLY` — **READY (In-Memory)** |
| **TC-WB-017** | `Note.plainTextContent` | Public getter — **Pure In-Memory** (`note_model.dart`) | REQ-05 / FN-09 | Branch & Exception | `isEmpty`, `isChecklist`, text thô, JSON Map (`decoded is! List`), `catch (_)` | **P1** | `DESIGN ONLY` — **READY (In-Memory)** |
| **TC-WB-018** | `Note.copyWith(clearReminder)` | Public method — **Pure In-Memory** (`note_model.dart`) | REQ-12 / FN-38 | Decision / Condition | Cờ `clearReminder` (`true` $\rightarrow$ `null`, `false` $\rightarrow$ giữ/gán mới) | **P2** | `DESIGN ONLY` — **READY (In-Memory)** |
| **TC-WB-019** | `Note.copyWith(updatedAt)` | Public method — **Pure In-Memory** (`note_model.dart`) | REQ-05, REQ-11 / FN-09, 41 | Branch Coverage | `updatedAt ?? DateTime.now()` (tự sinh vs gán ngoài) | **P1** | `DESIGN ONLY` — **READY (In-Memory)** |
| **TC-WB-020** | `Note.fromMap(m)` | Public factory — **Pure In-Memory** (`note_model.dart`) | REQ-04 / FN-08 | Branch & Guard | Fallback khi `created_at == null`, `updated_at == null`, `reminder == null` | **P2** | `DESIGN ONLY` — **READY (In-Memory)** |
| **TC-WB-021** | In-memory LWW `DateTime.isAfter` | Toán tử `DateTime.isAfter` — **Pure In-Memory** *(Không tính coverage `sync_repository.dart`)* | REQ-11 / FN-41 | Branch & Boundary | `local > cloud`, `cloud > local`, `local == cloud` (`BR-03` Open) | **P1** | `DESIGN ONLY` — **READY (In-Memory)** |
| **TC-WB-022** | `ChecklistItem.fromJson(json)` | Public factory — **Pure In-Memory** (`checklist_item.dart`) | REQ-06 / FN-15 | Branch & Defensive | Fallback khi `id == null` (L22 $\rightarrow$ L13), `text == null`, `checked == null` | **P2** | `DESIGN ONLY` — **READY (In-Memory)** |

---

## II. ĐẶC TẢ CHI TIẾT 22 TEST CASES HỘP TRẮNG THEO CHUẨN IEEE 829

### 2.1. Nhóm Module 1: AuthProvider (`lib/providers/auth_provider.dart`)

> [!WARNING]
> **Giới hạn kỹ thuật của Nhóm Module 1 (`TC-WB-001` .. `TC-WB-005`) khi không sửa `lib/`:**
> - Trong `lib/providers/auth_provider.dart`, constructor `AuthProvider()` (dòng 31–41) truy cập trực tiếp singleton tĩnh `FirebaseAuth.instance.currentUser` và đăng ký stream `FirebaseAuth.instance.authStateChanges().listen(...)`.
> - Phương thức `_syncUserProfile` (dòng 43–61) là **library-private** (bắt đầu bằng `_`), không thể gọi trực tiếp từ thư viện kiểm thử bên ngoài (`test/`), đồng thời gọi trực tiếp `FirebaseFirestore.instance.collection('users')`.
> - Do ràng buộc **không sửa mã nguồn `lib/`** để bổ sung Dependency Injection (DI), 5 ca kiểm thử dưới đây được đặc tả phục vụ phân tích nhánh/hợp đồng trạng thái và giữ trạng thái **`DESIGN ONLY (Blocked for direct unit execution without Firebase Platform Channel Mock)`**.

#### `TC-WB-001`: Thiết lập thông báo lỗi validation người dùng (`setError` có giá trị)
- **Mục tiêu kiểm thử:** Xác minh phương thức public `setError` gán chính xác chuỗi lỗi vào biến `_error` và phát tín hiệu `notifyListeners()` cho UI khi tham số truyền vào khác `null`.
- **Ánh xạ yêu cầu:** `REQ-02` (Đăng nhập hệ thống) / `FN-01` (Validate form).
- **Module, Class, Method thực tế:** `lib/providers/auth_provider.dart` $\rightarrow$ Class `AuthProvider` $\rightarrow$ Public method `setError(String? message)` (Dòng 26–29).
- **Điều kiện tiên quyết & Phụ thuộc môi trường:** Cần khởi tạo môi trường giả lập Firebase Core & Auth Platform Interface (MethodChannel/Pigeon mock) trước khi gọi constructor `AuthProvider()`; `_error` ban đầu đang là `null`.
- **Dữ liệu đầu vào (Input / Test Data):** `message = "Email không đúng định dạng"`.
- **Các bước thực hiện (Test Steps):**
  1. Khởi tạo `AuthProvider` trên môi trường đã mock Firebase Auth platform interface và đăng ký listener qua `authProvider.addListener()`.
  2. Thực thi lệnh gọi public `authProvider.setError("Email không đúng định dạng")`.
  3. Kiểm tra giá trị của getter `authProvider.error` và cờ ghi nhận của listener.
- **Kết quả mong đợi (Expected Result):** Getter `authProvider.error` trả về chính xác chuỗi `"Email không đúng định dạng"`; listener nhận được thông báo thay đổi đúng 1 lần.
- **Kỹ thuật White-box:** Statement Coverage & State Verification.
- **Nhánh / Điều kiện bao phủ:** Dòng lệnh `_error = message;` và `notifyListeners();` (Dòng 27–28).
- **Mức ưu tiên:** **P2** | **Trạng thái & Khả thi:** `DESIGN ONLY (Blocked without Firebase Platform Mock)`.

#### `TC-WB-002`: Xóa bỏ thông báo lỗi validation (`setError(null)`)
- **Mục tiêu kiểm thử:** Xác minh phương thức public `setError` xóa trạng thái lỗi (gán về `null`) và kích hoạt cập nhật giao diện khi truyền giá trị `null`.
- **Ánh xạ yêu cầu:** `REQ-02` (Đăng nhập hệ thống) / `FN-01` (Validate form).
- **Module, Class, Method thực tế:** `lib/providers/auth_provider.dart` $\rightarrow$ Class `AuthProvider` $\rightarrow$ Public method `setError(String? message)` (Dòng 26–29).
- **Điều kiện tiên quyết & Phụ thuộc môi trường:** Cần môi trường giả lập Firebase Auth Platform Interface để khởi tạo `AuthProvider()`; đối tượng đang chứa lỗi trước đó (`_error = "Mật khẩu không hợp lệ"`).
- **Dữ liệu đầu vào (Input / Test Data):** `message = null`.
- **Các bước thực hiện (Test Steps):**
  1. Trên instance `authProvider` đã gán lỗi trước đó, thực thi lệnh gọi public `authProvider.setError(null)`.
  2. Đọc giá trị từ getter `authProvider.error`.
- **Kết quả mong đợi (Expected Result):** Getter `authProvider.error` trả về `null`; trạng thái lỗi được xóa sạch hoàn toàn.
- **Kỹ thuật White-box:** Statement Coverage.
- **Nhánh / Điều kiện bao phủ:** Dòng lệnh `_error = null;` và `notifyListeners();` (Dòng 27–28).
- **Mức ưu tiên:** **P2** | **Trạng thái & Khả thi:** `DESIGN ONLY (Blocked without Firebase Platform Mock)`.

#### `TC-WB-003`: Xử lý dọn dẹp dữ liệu phiên làm việc khi người dùng đăng xuất (`user == null`)
- **Mục tiêu kiểm thử:** Xác minh luồng lắng nghe `authStateChanges` trong constructor `AuthProvider` dọn sạch dữ liệu `_userData` và reset lỗi khi nhận trạng thái người dùng là `null`.
- **Ánh xạ yêu cầu:** `REQ-02` (Đăng xuất tài khoản) / `FN-07` (Đăng xuất).
- **Module, Class, Method thực tế:** `lib/providers/auth_provider.dart` $\rightarrow$ Class `AuthProvider` $\rightarrow$ Constructor stream listener `authStateChanges()` (Dòng 33–40).
- **Điều kiện tiên quyết & Phụ thuộc môi trường:** Cần mock stream của `FirebaseAuthPlatform.authStateChanges()`; `AuthProvider` đang ở trạng thái đã đăng nhập (`_user != null`, `_userData` khác `null`).
- **Dữ liệu đầu vào (Input / Test Data):** Stream `authStateChanges()` phát ra sự kiện `User? = null` (hoặc kích hoạt qua phương thức public `signOut()`).
- **Các bước thực hiện (Test Steps):**
  1. Phát sự kiện `null` vào mock stream `authStateChanges` (hoặc gọi `authProvider.signOut()`).
  2. Chờ event loop xử lý và đọc các getter public của `authProvider`.
- **Kết quả mong đợi (Expected Result):** `authProvider.user == null`, `authProvider.isAuthenticated == false`, `authProvider.userData == null`, `authProvider.error == null`, `notifyListeners()` được gọi.
- **Kỹ thuật White-box:** Branch Coverage.
- **Nhánh / Điều kiện bao phủ:** Nhánh `if (user == null) { _userData = null; }` (Dòng 36–38).
- **Mức ưu tiên:** **P2** | **Trạng thái & Khả thi:** `DESIGN ONLY (Blocked without Firebase Platform Mock)`.

#### `TC-WB-004`: Đồng bộ hồ sơ tạo mới trên Firestore khi Document chưa tồn tại (`!snapshot.exists`)
- **Mục tiêu kiểm thử:** Xác minh nhánh `!snapshot.exists` thực thi khởi tạo Document người dùng mới với các trường mặc định và thời gian `serverTimestamp`.
- **Ánh xạ yêu cầu:** `REQ-01` (Đăng ký tài khoản) / `FN-02` (Đăng ký).
- **Module, Class, Method thực tế & Đường gọi Public:**
  - Hàm đích: `lib/providers/auth_provider.dart` $\rightarrow$ `_syncUserProfile(User user)` (Dòng 43–61 — **library-private**, không thể gọi trực tiếp từ `test/`) và logic tương đương tại phương thức public `reloadUserData()` (Dòng 64–88).
  - Đường gọi từ `test/`: Phải kích hoạt gián tiếp qua phương thức **public** `registerWithEmail(email, password)`, `signInWithEmail(email, password)` hoặc `reloadUserData()`.
- **Điều kiện tiên quyết & Giới hạn kỹ thuật:** Do cả `_syncUserProfile` và `reloadUserData` đều gọi cứng `FirebaseFirestore.instance.collection('users').doc(...)` mà không hỗ trợ truyền `FirebaseFirestore` giả lập qua constructor (vì không sửa `lib/`), ca kiểm thử này chỉ thực thi được nếu mock tầng `FirestorePlatform` (Pigeon/MethodChannel).
- **Dữ liệu đầu vào (Input / Test Data):** Phiên `currentUser` có `uid = "u_new"`, `email = "new@test.com"`, `displayName = "Newbie"`; Firestore snapshot trả về `exists == false`.
- **Các bước thực hiện (Test Steps):**
  1. Cấu hình mock `FirestorePlatform` trả về `DocumentSnapshot` có `exists = false` cho đường dẫn `users/u_new`.
  2. Gọi phương thức public `await authProvider.reloadUserData()` (hoặc `await authProvider.registerWithEmail(...)`).
  3. Kiểm tra lệnh ghi `set` trên đường dẫn `users/u_new` và giá trị getter `authProvider.userData`.
- **Kết quả mong đợi (Expected Result):** Nhánh `if (!snapshot.exists)` được thực thi, gọi `userDoc.set({...})` với `email: 'new@test.com'`, `displayName: 'Newbie'`, `bio: ''`, `createdAt: FieldValue.serverTimestamp()`; sau đó nạp `_userData` và gọi `notifyListeners()`.
- **Kỹ thuật White-box:** Decision / Condition Coverage.
- **Nhánh / Điều kiện bao phủ:** Nhánh `if (!snapshot.exists)` là `true` (Dòng 47–56 trong `_syncUserProfile` / Dòng 71–80 trong `reloadUserData`).
- **Mức ưu tiên:** **P2** | **Trạng thái & Khả thi:** `DESIGN ONLY (Blocked by library-private visibility & FirebaseFirestore.instance static singleton)`.

#### `TC-WB-005`: Bỏ qua tạo mới và nạp dữ liệu có sẵn khi Document đã tồn tại (`snapshot.exists == true`)
- **Mục tiêu kiểm thử:** Xác minh nhánh `else` nạp trực tiếp dữ liệu từ snapshot vào `_userData` mà không ghi đè dữ liệu người dùng cũ.
- **Ánh xạ yêu cầu:** `REQ-02` (Đăng nhập hệ thống) / `FN-04` (Đăng nhập email).
- **Module, Class, Method thực tế & Đường gọi Public:**
  - Hàm đích: `lib/providers/auth_provider.dart` $\rightarrow$ `_syncUserProfile(User user)` (Dòng 57–59 — **library-private**) và phương thức public `reloadUserData()` (Dòng 81–83).
  - Đường gọi từ `test/`: Gọi gián tiếp qua phương thức **public** `reloadUserData()` hoặc `signInWithEmail(email, password)`.
- **Điều kiện tiên quyết & Giới hạn kỹ thuật:** Tương tự `TC-WB-004`, phụ thuộc cứng vào singleton `FirebaseFirestore.instance` và `FirebaseAuth.instance`.
- **Dữ liệu đầu vào (Input / Test Data):** Phiên `currentUser` có `uid = "u_existing"`; Document `users/u_existing` trên mock `FirestorePlatform` có `exists = true` và data `{"bio": "Hồ sơ đã lưu"}`.
- **Các bước thực hiện (Test Steps):**
  1. Cấu hình mock `FirestorePlatform` trả về `DocumentSnapshot` có `exists = true` và dữ liệu `{"bio": "Hồ sơ đã lưu"}`.
  2. Gọi phương thức public `await authProvider.reloadUserData()` (hoặc `await authProvider.signInWithEmail(...)`).
  3. Kiểm tra xem lệnh `set()` có bị gọi hay không và đọc `authProvider.userData`.
- **Kết quả mong đợi (Expected Result):** Không gọi `set()`; `_userData` nhận trực tiếp `snapshot.data()` (`{"bio": "Hồ sơ đã lưu"}`); `notifyListeners()` được gọi.
- **Kỹ thuật White-box:** Decision Coverage.
- **Nhánh / Điều kiện bao phủ:** Nhánh `else` của điều kiện `if (!snapshot.exists)` (Dòng 57–59 trong `_syncUserProfile` / Dòng 81–83 trong `reloadUserData`).
- **Mức ưu tiên:** **P2** | **Trạng thái & Khả thi:** `DESIGN ONLY (Blocked by library-private visibility & FirebaseFirestore.instance static singleton)`.

---

### 2.2. Nhóm Module 2: CloudinaryService (`lib/services/cloudinary_service.dart`)

> [!NOTE]
> **Phân tích khả năng truy cập của Nhóm Module 2 (`TC-WB-006` .. `TC-WB-010`) khi không sửa `lib/`:**
> - Phương thức `_extractPublicId(String url)` (dòng 27–47) là **library-private** (`_`), không thể gọi trực tiếp từ `test/`. Tuy nhiên, phương thức **public** `deleteFile(String fileUrl)` (dòng 52–58) gọi `_extractPublicId(fileUrl)` ngay ở dòng đầu tiên (dòng 53).
> - Do đó, `TC-WB-006` (URL không hợp lệ) có thể kiểm thử trực tiếp trong bộ nhớ bằng cách gọi `await cloudinaryService.deleteFile(url)` và xác nhận hàm trả về `false` ngay tại dòng 57 trước khi chạm vào `dotenv` hay `http.post`.
> - Đối với `TC-WB-007` (URL hợp lệ có đuôi mở rộng), khi gọi qua `deleteFile(url)`, luồng chạy sẽ đi tiếp xuống `http.post` (dòng 73). Để kiểm tra giá trị `public_id` đã cắt đuôi file mà không sửa `lib/`, bài test cần nạp `dotenv.testLoad(...)` và bọc lời gọi trong `HttpOverrides.runZoned` (hoặc `http.runWithClient` với `MockClient`) để bắt body request `POST`.

#### `TC-WB-006`: Xử lý URL không chứa tiền tố thư mục hệ thống trong `_extractPublicId` (Gọi qua public `deleteFile`)
- **Mục tiêu kiểm thử:** Xác minh khi truyền đường dẫn ảnh không chứa phân đoạn `'smart_note'`, hàm nội bộ `_extractPublicId` trả về `null` và phương thức public `deleteFile` ngắt sớm an toàn trả về `false`.
- **Ánh xạ yêu cầu:**
  - **Ánh xạ chính:** `REQ-09` / `FN-12` (Xóa ghi chú vĩnh viễn — `NoteProvider.deleteNoteForever` tại `lib/providers/note_provider.dart` L497, L504 gọi `CloudinaryService.deleteFile(url)` $\rightarrow$ `_extractPublicId(fileUrl)` tại `lib/services/cloudinary_service.dart` L53 để xóa ảnh/audio đính kèm trên Cloudinary).
  - **Ánh xạ phụ (có căn cứ mã nguồn):** `REQ-12` / `FN-35`, `FN-36` (`EditorScreen._replaceDrawing` tại `lib/screens/editor_screen.dart` L645 gọi `_cloudinary.deleteFile(oldUrl)` để xóa bản vẽ/media cũ khi thay thế bằng ảnh vẽ mới).
- **Module, Class, Method thực tế & Đường gọi Public:**
  - Hàm nội bộ được kiểm tra: `CloudinaryService._extractPublicId(String url)` (Dòng 27–34 — **library-private**).
  - Phương thức **public** dùng để kích hoạt từ `test/`: `CloudinaryService.deleteFile(String fileUrl)` (Dòng 52–58).
- **Điều kiện tiên quyết (Preconditions):** Khởi tạo đối tượng `final service = CloudinaryService();` (không cần kết nối mạng hay `dotenv` vì hàm ngắt sớm tại dòng 57).
- **Dữ liệu đầu vào (Input / Test Data):** `fileUrl = "https://res.cloudinary.com/demo/image/upload/v1/other_app/users/avatar.jpg"`.
- **Các bước thực hiện (Test Steps):**
  1. Gọi phương thức public `final result = await service.deleteFile(fileUrl);`.
  2. Kiểm tra giá trị boolean `result` trả về.
- **Kết quả mong đợi (Expected Result):** `_extractPublicId` ghi nhận `rootIndex == -1` và trả về `null`; `deleteFile` nhận `publicId == null` tại dòng 55 và trả về `false` an toàn mà không phát sinh HTTP request hay ném ngoại lệ.
- **Kỹ thuật White-box:** Branch Coverage & Guard Clause.
- **Nhánh / Điều kiện bao phủ:** Nhánh `if (rootIndex == -1) return null;` (Dòng 33) và `if (publicId == null) return false;` (Dòng 55–58).
- **Mức ưu tiên:** **P2** | **Trạng thái & Khả thi:** `DESIGN ONLY (Khả thi trong bộ nhớ qua phương thức public deleteFile)`.

#### `TC-WB-007`: Cắt bỏ phần mở rộng tập tin khi trích xuất `publicId` hợp lệ (Kiểm chứng qua public `deleteFile`)
- **Mục tiêu kiểm thử:** Xác minh `_extractPublicId` cắt bỏ phần mở rộng (`.jpg`, `.png`, `.m4a`), giữ lại đường dẫn thư mục phân cấp chuẩn từ `'smart_note'` và truyền đúng `public_id` vào payload của `deleteFile`.
- **Ánh xạ yêu cầu:**
  - **Ánh xạ chính:** `REQ-09` / `FN-12` (Xóa ghi chú vĩnh viễn — `NoteProvider.deleteNoteForever` gọi `CloudinaryService.deleteFile(url)` $\rightarrow$ `_extractPublicId(fileUrl)`).
  - **Ánh xạ phụ (có căn cứ mã nguồn):** `REQ-12` / `FN-35`, `FN-36` (`EditorScreen._replaceDrawing` gọi `_cloudinary.deleteFile(oldUrl)` $\rightarrow$ `_extractPublicId(fileUrl)` khi thay thế bản vẽ/media).
- **Module, Class, Method thực tế & Đường gọi Public:**
  - Hàm nội bộ được kiểm tra: `CloudinaryService._extractPublicId(String url)` (Dòng 35–42 — **library-private**).
  - Phương thức **public** dùng để kích hoạt từ `test/`: `CloudinaryService.deleteFile(String fileUrl)` (Dòng 52–93).
- **Điều kiện tiên quyết & Phụ thuộc môi trường:** Nạp `dotenv.testLoad(fileInput: 'CLOUDINARY_CLOUD_NAME=demo\nCLOUDINARY_API_KEY=key\nCLOUDINARY_API_SECRET=secret')` và thiết lập `http.runWithClient` / `HttpOverrides.runZoned` để bắt request `POST /image/destroy` và trả về HTTP 200 `{"result": "ok"}`.
- **Dữ liệu đầu vào (Input / Test Data):** `fileUrl = "https://res.cloudinary.com/demo/image/upload/v1600000/smart_note/u_101/images/note_sketch.png"`.
- **Các bước thực hiện (Test Steps):**
  1. Trong vùng `http.runWithClient` (hoặc `HttpOverrides.runZoned`), gọi phương thức public `final ok = await service.deleteFile(fileUrl);`.
  2. Bắt trường `public_id` trong form body của request `POST` gửi tới `/image/destroy` và kiểm tra giá trị trả về `ok`.
- **Kết quả mong đợi (Expected Result):** Trường `public_id` được gửi đi trong request body khớp chính xác chuỗi `"smart_note/u_101/images/note_sketch"` (đã cắt bỏ `.png`); hàm `deleteFile` trả về `true`.
- **Kỹ thuật White-box:** Statement & Branch Coverage.
- **Nhánh / Điều kiện bao phủ:** Nhánh `rootIndex != -1` và `if (publicId.contains('.'))` là `true` (Dòng 38–40).
- **Mức ưu tiên:** **P2** | **Trạng thái & Khả thi:** `DESIGN ONLY (Requires dotenv.testLoad & HttpOverrides/MockClient)`.

#### `TC-WB-008`: Bảo vệ ngắt sớm khi thiếu cấu hình biến môi trường Cloudinary trong `uploadImage`
- **Mục tiêu kiểm thử:** Xác minh hàm public `uploadImage` không gửi HTTP request và trả về `null` ngay lập tức khi `_cloudName` hoặc `_uploadPreset` rỗng.
- **Ánh xạ yêu cầu:** `REQ-12` / `FN-36` (Tải ảnh Cloudinary).
- **Module, Class, Method thực tế:** `lib/services/cloudinary_service.dart` $\rightarrow$ Class `CloudinaryService` $\rightarrow$ Public method `uploadImage(File file, String userId, ...)` (Dòng 108–117).
- **Điều kiện tiên quyết (Preconditions):** Nạp `dotenv.testLoad(fileInput: 'CLOUDINARY_CLOUD_NAME=\nCLOUDINARY_UPLOAD_PRESET=')` để môi trường `dotenv.env` có `_cloudName` hoặc `_uploadPreset` rỗng.
- **Dữ liệu đầu vào (Input / Test Data):** `file = File('test_mock.png')` (chưa cần file tồn tại trên đĩa vì hàm thoát ở dòng 116 trước khi gọi `MultipartFile.fromPath` ở dòng 130), `userId = "u_001"`.
- **Các bước thực hiện (Test Steps):**
  1. Khởi tạo `dotenv.testLoad(fileInput: '')` và gọi public `await service.uploadImage(file, userId)`.
  2. Kiểm tra giá trị trả về.
- **Kết quả mong đợi (Expected Result):** Trả về `null`; không có bất kỳ truy cập file hay kết nối mạng nào được khởi tạo; log ghi `"❌ [Cloudinary] ENV rỗng!"`.
- **Kỹ thuật White-box:** Decision Coverage (Guard clause).
- **Nhánh / Điều kiện bao phủ:** Biểu thức `if (_cloudName.isEmpty || _uploadPreset.isEmpty) return null;` (Dòng 114–117).
- **Mức ưu tiên:** **P2** | **Trạng thái & Khả thi:** `DESIGN ONLY (Khả thi trong bộ nhớ qua dotenv.testLoad)`.

#### `TC-WB-009`: Định tuyến thư mục lưu trữ theo cờ `isAvatar` và `isDrawing` trong `uploadImage`
- **Mục tiêu kiểm thử:** Xác minh trường `folder` trong multipart form data được gán chính xác theo từng loại media upload.
- **Ánh xạ yêu cầu:** `REQ-12` / `FN-35` (Bảng vẽ tay), `FN-36` (Ảnh ghi chú).
- **Module, Class, Method thực tế:** `lib/services/cloudinary_service.dart` $\rightarrow$ Class `CloudinaryService` $\rightarrow$ Public method `uploadImage(File file, String userId, {bool isDrawing, bool isAvatar})` (Dòng 123–127).
- **Điều kiện tiên quyết & Phụ thuộc môi trường:** Nạp `dotenv.testLoad` hợp lệ; tạo 1 file tạm bằng `Directory.systemTemp` (do dòng 130 gọi `MultipartFile.fromPath('file', file.path)`); bọc trong `HttpOverrides.runZoned` / `http.runWithClient` để chặn `request.send()`.
- **Dữ liệu đầu vào (Input / Test Data):**
  - Ca A: `isAvatar = true, isDrawing = false`
  - Ca B: `isAvatar = false, isDrawing = true`
  - Ca C: `isAvatar = false, isDrawing = false`
- **Các bước thực hiện (Test Steps):**
  1. Gọi `uploadImage` lần lượt cho Ca A, Ca B, Ca C với file tạm trong vùng mock HTTP.
  2. Bắt request multipart và kiểm tra giá trị của trường `folder`.
- **Kết quả mong đợi (Expected Result):**
  - Ca A: `folder` = `'smart_note/u_001/avatars'`
  - Ca B: `folder` = `'smart_note/u_001/drawings'`
  - Ca C: `folder` = `'smart_note/u_001/images'`
- **Kỹ thuật White-box:** Multiple Condition Coverage.
- **Nhánh / Điều kiện bao phủ:** Cấu trúc phân nhánh `if (isAvatar) ... else isDrawing ? ... : ...` (Dòng 123–127).
- **Mức ưu tiên:** **P3** | **Trạng thái & Khả thi:** `DESIGN ONLY (Requires dotenv.testLoad, Temp File & HttpOverrides)`.

#### `TC-WB-010`: Xử lý phản hồi HTTP 200 OK và trích xuất `secure_url` trong `uploadImage`
- **Mục tiêu kiểm thử:** Xác minh khi server Cloudinary phản hồi `statusCode == 200`, hàm giải mã JSON và trả về URL ảnh bảo mật.
- **Ánh xạ yêu cầu:** `REQ-12` / `FN-36` (Tải ảnh Cloudinary).
- **Module, Class, Method thực tế:** `lib/services/cloudinary_service.dart` $\rightarrow$ Class `CloudinaryService` $\rightarrow$ Public method `uploadImage(...)` (Dòng 138–141).
- **Điều kiện tiên quyết & Phụ thuộc môi trường:** Nạp `dotenv.testLoad` hợp lệ; tạo file tạm hợp lệ; `HttpOverrides.runZoned` / `http.runWithClient` giả lập phản hồi HTTP `200` với body JSON `{"secure_url": "https://res.cloudinary.com/demo/image/upload/v1/pic.jpg"}`.
- **Dữ liệu đầu vào (Input / Test Data):** File tạm hợp lệ, `userId = "u_001"`.
- **Các bước thực hiện (Test Steps):**
  1. Thực thi `uploadImage(file, userId)` trong vùng mock HTTP.
  2. Đọc chuỗi URL trả về.
- **Kết quả mong đợi (Expected Result):** Hàm trả về chính xác `"https://res.cloudinary.com/demo/image/upload/v1/pic.jpg"`.
- **Kỹ thuật White-box:** Branch Coverage.
- **Nhánh / Điều kiện bao phủ:** Nhánh `if (response.statusCode == 200)` (Dòng 138–141).
- **Mức ưu tiên:** **P2** | **Trạng thái & Khả thi:** `DESIGN ONLY (Requires dotenv.testLoad, Temp File & HttpOverrides)`.

---

### 2.3. Nhóm Module 3: Cloud Firestore Security Rules (`firestore.rules`)

> [!IMPORTANT]
> **Làm rõ bản chất môi trường kiểm thử của `TC-WB-011` .. `TC-WB-014`:**
> - Các ca `TC-WB-011` .. `TC-WB-014` đã được hiện thực hóa trong `test/security_rules_test.dart` (8 tests PASS) dưới dạng **Kiểm thử mô phỏng logic quy tắc bằng ngôn ngữ Dart (In-Memory Dart Rule Logic Simulation)** dựa trên cấu trúc biểu thức của `firestore.rules`.
> - **Không đánh đồng:** Kết quả PASS này xác nhận tính đúng đắn về mặt biểu thức boolean (`isAuthenticated()`, `isOwner(userId)`, `isValidNote(userId)`), nhưng **KHÔNG PHẢI** là kết quả chạy kiểm thử tích hợp trên **Firebase Local Emulator Suite (Firestore Rules Engine)** thực tế.

#### `TC-WB-011`: Quy tắc `isOwner` cho phép truy cập khi người dùng đã xác thực và khớp UID
- **Mục tiêu kiểm thử:** Xác minh biểu thức quy tắc `isOwner(userId)` trả về `true` khi `request.auth` khác `null` và `request.auth.uid == userId`.
- **Ánh xạ yêu cầu:** `REQ-11` / `NFR-03` / `FN-40` (Bảo mật đồng bộ & Cô lập dữ liệu người dùng).
- **Module, Class, Method thực tế:** Biểu thức `isOwner(userId)` trong `firestore.rules` (mô phỏng tại `test/security_rules_test.dart`).
- **Điều kiện tiên quyết (Preconditions):** Ngữ cảnh mô phỏng có `authUid = "uid_alice"` (đã xác thực).
- **Dữ liệu đầu vào (Input / Test Data):** `request.auth.uid = "uid_alice"`, `pathUserId = "uid_alice"`.
- **Các bước thực hiện (Test Steps):**
  1. Đánh giá biểu thức `isAuthenticated() && request.auth.uid == userId` trong hàm mô phỏng quy tắc tại `test/security_rules_test.dart`.
- **Kết quả mong đợi (Expected Result):** Biểu thức trả về `true` $\rightarrow$ Cho phép đọc/ghi (**ALLOW**).
- **Kỹ thuật White-box:** Condition Coverage.
- **Nhánh / Điều kiện bao phủ:** Cả 2 mệnh đề con `isAuthenticated()` và `request.auth.uid == userId` đều là `true`.
- **Mức ưu tiên:** **P2** | **Trạng thái:** `DESIGNED (Dart Rule Simulation PASS in test/security_rules_test.dart — Not Firebase Emulator)`.

#### `TC-WB-012`: Quy tắc `isOwner` từ chối truy cập khi yêu cầu chưa đăng nhập (`request.auth == null`)
- **Mục tiêu kiểm thử:** Xác minh biểu thức `isOwner(userId)` ngắt sớm và trả về `false` khi client chưa có token xác thực.
- **Ánh xạ yêu cầu:** `REQ-11` / `NFR-03` / `FN-40` (Bảo mật truy cập vô danh & Cô lập dữ liệu).
- **Module, Class, Method thực tế:** Biểu thức `isOwner(userId)` trong `firestore.rules` (mô phỏng tại `test/security_rules_test.dart`).
- **Điều kiện tiên quyết (Preconditions):** Ngữ cảnh mô phỏng là khách vãng lai chưa đăng nhập (`authUid = null`).
- **Dữ liệu đầu vào (Input / Test Data):** `request.auth = null`, `pathUserId = "uid_alice"`.
- **Các bước thực hiện (Test Steps):**
  1. Đánh giá biểu thức `isOwner("uid_alice")` trong `test/security_rules_test.dart`.
- **Kết quả mong đợi (Expected Result):** Biểu thức trả về `false` $\rightarrow$ Chặn toàn bộ quyền truy cập (**DENY**).
- **Kỹ thuật White-box:** Condition Coverage & Short-circuit Evaluation.
- **Nhánh / Điều kiện bao phủ:** Mệnh đề `isAuthenticated()` là `false`.
- **Mức ưu tiên:** **P2** | **Trạng thái:** `DESIGNED (Dart Rule Simulation PASS in test/security_rules_test.dart — Not Firebase Emulator)`.

#### `TC-WB-013`: Quy tắc `isOwner` ngăn chặn truy cập trái phép dữ liệu người dùng khác
- **Mục tiêu kiểm thử:** Xác minh biểu thức `isOwner(userId)` trả về `false` khi user A cố tình truy cập vào đường dẫn dữ liệu của user B.
- **Ánh xạ yêu cầu:** `REQ-11` / `NFR-03` / `FN-40` (Cô lập dữ liệu giữa các người dùng).
- **Module, Class, Method thực tế:** Biểu thức `isOwner(userId)` trong `firestore.rules` (mô phỏng tại `test/security_rules_test.dart`).
- **Điều kiện tiên quyết (Preconditions):** User Bob đã đăng nhập (`request.auth.uid = "uid_bob"`), cố đọc ghi vào path của Alice.
- **Dữ liệu đầu vào (Input / Test Data):** `request.auth.uid = "uid_bob"`, `pathUserId = "uid_alice"`.
- **Các bước thực hiện (Test Steps):**
  1. Đánh giá biểu thức `isOwner("uid_alice")` trong `test/security_rules_test.dart`.
- **Kết quả mong đợi (Expected Result):** Biểu thức trả về `false` $\rightarrow$ Chặn truy cập (**DENY**).
- **Kỹ thuật White-box:** Condition Coverage.
- **Nhánh / Điều kiện bao phủ:** `isAuthenticated()` là `true` nhưng `request.auth.uid == userId` là `false`.
- **Mức ưu tiên:** **P2** | **Trạng thái:** `DESIGNED (Dart Rule Simulation PASS in test/security_rules_test.dart — Not Firebase Emulator)`.

#### `TC-WB-014`: Quy tắc `isValidNote` xác minh tính chính chủ của trường `user_id` trong payload
- **Mục tiêu kiểm thử:** Xác minh dữ liệu ghi mới hoặc cập nhật phải chứa trường `user_id` trùng khớp với `userId` trên URL đường dẫn.
- **Ánh xạ yêu cầu:** `REQ-11` / `NFR-03` / `FN-40` (Toàn vẹn & Cô lập dữ liệu ghi).
- **Module, Class, Method thực tế:** Biểu thức `isValidNote(userId)` trong `firestore.rules` (mô phỏng tại `test/security_rules_test.dart`).
- **Điều kiện tiên quyết (Preconditions):** Client Alice gửi payload ghi dữ liệu lên `users/uid_alice/notes/{noteId}`.
- **Dữ liệu đầu vào (Input / Test Data):**
  - Ca hợp lệ: `request.resource.data.user_id = "uid_alice"`, `userId = "uid_alice"`.
  - Ca giả mạo owner: `request.resource.data.user_id = "uid_bob"`, `userId = "uid_alice"`.
- **Các bước thực hiện (Test Steps):**
  1. Đánh giá mệnh đề `isOwner(userId) && isValidNote(userId)` cho cả 2 ca trong `test/security_rules_test.dart`.
- **Kết quả mong đợi (Expected Result):** Ca hợp lệ trả về `true` (**ALLOW**); ca giả mạo `user_id` trả về `false` (**DENY**).
- **Kỹ thuật White-box:** Statement & Decision Coverage.
- **Nhánh / Điều kiện bao phủ:** Cả 2 nhánh `true` và `false` của `request.resource.data.user_id == userId`.
- **Mức ưu tiên:** **P2** | **Trạng thái:** `DESIGNED (Dart Rule Simulation PASS in test/security_rules_test.dart — Not Firebase Emulator)`.

---

### 2.4. Nhóm Module 4: NoteModel & Core Business Logic (`lib/models/note_model.dart`)

#### `TC-WB-015`: Tính toán số lượng công việc chưa hoàn thành (`pendingChecklistCount`)
- **Mục tiêu kiểm thử:** Xác minh getter public `pendingChecklistCount` đếm chính xác số mục có `i['checked'] != true`, xử lý an toàn khi `items` là `null` hoặc mục khuyết trường `checked`, trả về `0` khi không phải Checklist, và bắt ngoại lệ an toàn tại `catch (_)` khi cấu trúc `items` bị hỏng kiểu dữ liệu.
- **Ánh xạ yêu cầu:** `REQ-06` (Quản lý Checklist) / `FN-15` (Tạo ghi chú checklist).
- **Module, Class, Method thực tế:** `lib/models/note_model.dart` $\rightarrow$ Class `Note` $\rightarrow$ Public getter `pendingChecklistCount` (Dòng 33–42).
- **Điều kiện tiên quyết (Preconditions):** Khởi tạo các thực thể `Note` thuần trong bộ nhớ với các dạng `content` khác nhau.
- **Dữ liệu đầu vào (Input / Test Data — Đã kiểm chứng kích hoạt đủ 100% nhánh thực tế):**
  - **Note A (Không phải JSON checklist):** `content = "Ghi chú thường không có định dạng checklist"`
  - **Note B (Checklist chuẩn gồm cả `checked: true` và `checked: false`):** `content = jsonEncode({"type": "checklist", "items": [{"id": "1", "text": "Task 1", "checked": true}, {"id": "2", "text": "Task 2", "checked": false}, {"id": "3", "text": "Task 3", "checked": false}]})`
  - **Note C (Item khuyết key `checked` & Checklist khuyết key `items`):**
    - `noteC1`: `content = jsonEncode({"type": "checklist", "items": [{"id": "4", "text": "Task 4"}]})` (khuyết key `checked`)
    - `noteC2`: `content = jsonEncode({"type": "checklist"})` (`decoded['items'] == null` $\rightarrow$ kích hoạt nhánh fallback `?? []` tại dòng 37)
  - **Note D (JSON Map thiếu `'type': 'checklist'`):** `content = jsonEncode({"items": [{"id": "5", "text": "Task 5", "checked": false}]})` (`isChecklist == false`)
  - **Note E (Dữ liệu kích hoạt thực sự khối `catch (_)` tại dòng 39–41):** `content = jsonEncode({"type": "checklist", "items": "corrupted_not_a_list"})` *(Giải thích kỹ thuật: Do có `"type": "checklist"`, getter `isChecklist` trả về `true` và đi qua dòng 34 vào khối `try` của `pendingChecklistCount`; tại dòng 37, phép ép kiểu `decoded['items'] as List?` ném `TypeError` do giá trị là `String`, nhờ đó kích hoạt chính xác nhánh `catch (_) { return 0; }` ở dòng 39–41)*.
- **Các bước thực hiện (Test Steps):**
  1. Đọc giá trị `noteA.pendingChecklistCount` và `noteD.pendingChecklistCount`.
  2. Đọc giá trị `noteB.pendingChecklistCount`.
  3. Đọc giá trị `noteC1.pendingChecklistCount` và `noteC2.pendingChecklistCount`.
  4. Đọc giá trị `noteE.pendingChecklistCount`.
- **Kết quả mong đợi (Expected Result):**
  - `noteA` và `noteD`: trả về `0` (đi qua nhánh `if (!isChecklist) return 0;` ở dòng 34).
  - `noteB`: trả về `2` (lọc qua `items.where((i) => i['checked'] != true).length` ở dòng 38).
  - `noteC1`: trả về `1` (`i['checked']` là `null != true`); `noteC2`: trả về `0` (kích hoạt nhánh `?? []` ở dòng 37).
  - `noteE`: trả về `0` an toàn, không bị crash (kích hoạt thực sự khối `catch (_)` ở dòng 39–41).
- **Kỹ thuật White-box:** Branch, Condition & Exception Path Coverage.
- **Nhánh / Điều kiện bao phủ (Đối chiếu chính xác dòng lệnh `lib/models/note_model.dart`):**
  - Nhánh `if (!isChecklist) return 0;` (Dòng 34: cả `true` và `false`)
  - Toán tử fallback `final items = decoded['items'] as List? ?? [];` (Dòng 37: cả trường hợp có `List` và `null`)
  - Vòng lặp lọc `items.where((i) => i['checked'] != true).length` (Dòng 38: cả `checked == true`, `checked == false`, và `checked == null`)
  - Khối `catch (_) { return 0; }` (Dòng 39–41: được kích hoạt thực tế bởi `Note E`).
- **Mức ưu tiên:** **P1** | **Trạng thái & Khả thi:** `DESIGN ONLY — READY FOR AUTHORING (Pure In-Memory)`.

#### `TC-WB-016`: Trích xuất chuỗi văn bản thuần (plain text) từ cấu trúc Quill Delta JSON
- **Mục tiêu kiểm thử:** Xác minh getter public `plainTextContent` bóc tách và nối chuỗi toàn bộ các phân đoạn `insert` dạng `String` trong mảng Quill Delta JSON, đồng thời bỏ qua an toàn các embed object (`val` không phải `String`), các object thiếu khóa `'insert'`, và các phần tử không phải `Map`.
- **Ánh xạ yêu cầu:** `REQ-05` (Chỉnh sửa ghi chú), `REQ-08` (Tìm kiếm văn bản) / `FN-09`, `FN-23`.
- **Module, Class, Method thực tế:** `lib/models/note_model.dart` $\rightarrow$ Class `Note` $\rightarrow$ Public getter `plainTextContent` (Dòng 45–69).
- **Điều kiện tiên quyết (Preconditions):** Khởi tạo `Note` trong bộ nhớ có `content` là chuỗi JSON mảng Delta của Quill Editor.
- **Dữ liệu đầu vào (Input / Test Data — Bao phủ toàn bộ các nhánh điều kiện con tại dòng 56–62):**
  `content = jsonEncode([{"insert": "Kế hoạch tuần tới\n"}, {"insert": {"image": "https://img.com/p1.png"}}, {"attributes": {"bold": true}}, "raw_non_map_item", {"insert": "Thực hiện kiểm thử hộp trắng"}])`
  - Phần tử 1 `{"insert": "Kế hoạch tuần tới\n"}`: `item is Map` (`true`), `item.containsKey('insert')` (`true`), `val is String` (`true`).
  - Phần tử 2 `{"insert": {"image": "..."}}`: `item is Map` (`true`), `item.containsKey('insert')` (`true`), `val is String` (`false` — embed Map).
  - Phần tử 3 `{"attributes": {"bold": true}}`: `item is Map` (`true`), `item.containsKey('insert')` (`false` — Map thiếu key `'insert'`).
  - Phần tử 4 `"raw_non_map_item"`: `item is Map` (`false` — phần tử không phải `Map`).
  - Phần tử 5 `{"insert": "Thực hiện kiểm thử hộp trắng"}`: `item is Map` (`true`), `item.containsKey('insert')` (`true`), `val is String` (`true`).
- **Các bước thực hiện (Test Steps):**
  1. Gọi getter `note.plainTextContent`.
  2. So sánh chuỗi thu được với kết quả mong đợi.
- **Kết quả mong đợi (Expected Result):** Trả về chính xác chuỗi `"Kế hoạch tuần tới\nThực hiện kiểm thử hộp trắng"`. Các phần tử embed ảnh (`Map`), phần tử thiếu key `'insert'` và phần tử không phải `Map` đều bị bỏ qua an toàn mà không gây lỗi ép kiểu.
- **Kỹ thuật White-box:** Branch, Multiple Condition & Loop Coverage.
- **Nhánh / Điều kiện bao phủ:**
  - Điều kiện `if (trimmed.startsWith('[') || trimmed.startsWith('{'))` là `true` (Dòng 51) và `if (decoded is List)` là `true` (Dòng 54)
  - Vòng lặp `for (final item in decoded)` (Dòng 56)
  - Đầy đủ các nhánh `true`/`false` của mệnh đề kép `if (item is Map && item.containsKey('insert'))` (Dòng 57)
  - Đầy đủ các nhánh `true`/`false` của điều kiện `if (val is String)` (Dòng 59).
- **Mức ưu tiên:** **P1** | **Trạng thái & Khả thi:** `DESIGN ONLY — READY FOR AUTHORING (Pure In-Memory)`.

#### `TC-WB-017`: Xử lý chuỗi rỗng, Checklist, văn bản thuần, JSON Map không phải List và JSON malformed trong `plainTextContent`
- **Mục tiêu kiểm thử:** Xác minh toàn bộ các nhánh rẽ phòng thủ và chịu lỗi của `plainTextContent` khi nhận nội dung rỗng, nội dung Checklist, chuỗi văn bản thuần túy, chuỗi JSON đối tượng (`Map` không phải `List`) hoặc chuỗi JSON cú pháp lỗi.
- **Ánh xạ yêu cầu:** `REQ-05` (Toàn vẹn dữ liệu ghi chú) / `FN-09`.
- **Module, Class, Method thực tế:** `lib/models/note_model.dart` $\rightarrow$ Class `Note` $\rightarrow$ Public getter `plainTextContent` (Dòng 45–69).
- **Điều kiện tiên quyết (Preconditions):** Khởi tạo đối tượng `Note` trong bộ nhớ.
- **Dữ liệu đầu vào (Input / Test Data):**
  - Payload 1 (Chuỗi rỗng): `content = ""`
  - Payload 2 (Văn bản thô không bắt đầu bằng `[` hay `{`): `content = "   Ghi chú văn bản thô không qua editor   "`
  - Payload 3 (JSON cú pháp lỗi bắt đầu bằng `[`): `content = "[{malformed_json_without_end"`
  - Payload 4 (JSON hợp lệ bắt đầu bằng `{` nhưng không phải Checklist và `decoded is List` là `false`): `content = '{"custom_meta": "value"}'`
  - Payload 5 (Ghi chú dạng Checklist `isChecklist == true`): `content = jsonEncode({"type": "checklist", "items": [{"id": "1", "text": "Mục 1", "checked": true}]})`
- **Các bước thực hiện (Test Steps):**
  1. Đọc `plainTextContent` lần lượt cho Payload 1, 2, 3, 4, 5.
- **Kết quả mong đợi (Expected Result):**
  - Payload 1: trả về chuỗi rỗng `""` (nhánh dòng 46).
  - Payload 2: trả về chuỗi đã cắt khoảng trắng hai đầu `"Ghi chú văn bản thô không qua editor"` (nhánh `trimmed.startsWith` = `false` tại dòng 51 $\rightarrow$ dòng 68).
  - Payload 3: rơi vào khối `catch (_) {}` (dòng 66) và trả về an toàn chuỗi `trimmed` `"[{malformed_json_without_end"` tại dòng 68.
  - Payload 4: `trimmed.startsWith('{')` là `true` (dòng 51), `decoded is List` là `false` (dòng 54), thoát khối `if` và trả về `'{"custom_meta": "value"}'` tại dòng 68.
  - Payload 5: `if (isChecklist)` là `true` (dòng 47–48), uỷ quyền sang `checklistPlainText` và trả về `"☑ Mục 1"`.
- **Kỹ thuật White-box:** Branch Coverage & Exception Handling.
- **Nhánh / Điều kiện bao phủ:**
  - Nhánh `if (content.isEmpty) return '';` (Dòng 46)
  - Nhánh `if (isChecklist) return checklistPlainText;` (Dòng 47–48)
  - Nhánh `if (trimmed.startsWith('[') || trimmed.startsWith('{'))` cả `true` (với `[` và `{`) lẫn `false` (Dòng 51)
  - Nhánh `if (decoded is List)` là `false` (Dòng 54)
  - Khối `catch (_) {}` và `return trimmed;` (Dòng 66–68).
- **Mức ưu tiên:** **P1** | **Trạng thái & Khả thi:** `DESIGN ONLY — READY FOR AUTHORING (Pure In-Memory)`.

#### `TC-WB-018`: Cơ chế xóa nhắc nhở thông qua cờ `clearReminder` trong `Note.copyWith`
- **Mục tiêu kiểm thử:** Xác minh biểu thức điều kiện trong `Note.copyWith` xóa mốc nhắc nhở về `null` khi `clearReminder == true`, giữ nguyên khi `false` và nhận giá trị mới khi truyền tham số.
- **Ánh xạ yêu cầu:** `REQ-12` (Tiện ích nhắc nhở) / `FN-38` (Thiết lập nhắc nhở).
- **Module, Class, Method thực tế:** `lib/models/note_model.dart` $\rightarrow$ Class `Note` $\rightarrow$ Public method `Note.copyWith(...)` (Dòng 200–229).
- **Điều kiện tiên quyết (Preconditions):** Đối tượng `Note` ban đầu trong bộ nhớ có mốc thời gian `reminder = DateTime(2026, 10, 20, 8, 30)`.
- **Dữ liệu đầu vào (Input / Test Data):**
  - Lệnh 1: `note.copyWith(clearReminder: true)`
  - Lệnh 2: `note.copyWith(title: "Tiêu đề đổi mới")` (không truyền `reminder`, cờ `clearReminder` mặc định `false`)
  - Lệnh 3: `note.copyWith(reminder: DateTime(2026, 11, 15, 10, 0))`
- **Các bước thực hiện (Test Steps):**
  1. Thực thi lần lượt 3 lệnh `copyWith`.
  2. Kiểm tra thuộc tính `reminder` của 3 đối tượng kết quả.
- **Kết quả mong đợi (Expected Result):**
  - Kết quả 1: `res1.reminder == null` (nhắc nhở bị hủy bỏ hoàn toàn).
  - Kết quả 2: `res2.reminder` vẫn giữ nguyên mốc cũ `2026-10-20 08:30`.
  - Kết quả 3: `res3.reminder` mang mốc mới `2026-11-15 10:00`.
- **Kỹ thuật White-box:** Decision / Condition Coverage.
- **Nhánh / Điều kiện bao phủ:** Biểu thức ternary `clearReminder ? null : (reminder ?? this.reminder)` (Dòng 228).
- **Mức ưu tiên:** **P2** | **Trạng thái & Khả thi:** `DESIGN ONLY — READY FOR AUTHORING (Pure In-Memory)`.

#### `TC-WB-019`: Hành vi cập nhật mốc thời gian `updatedAt` trong `Note.copyWith`
- **Mục tiêu kiểm thử:** Xác minh phương thức `Note.copyWith` tự động sinh mốc thời gian hiện tại `DateTime.now()` khi không truyền `updatedAt`, và nhận chính xác mốc thời gian truyền ngoài phục vụ đồng bộ.
- **Ánh xạ yêu cầu:** `REQ-05` (Chỉnh sửa ghi chú), `REQ-11` (Đồng bộ LWW) / `FN-09`, `FN-41`.
- **Module, Class, Method thực tế:** `lib/models/note_model.dart` $\rightarrow$ Class `Note` $\rightarrow$ Public method `Note.copyWith(...)` (Dòng 200–229).
- **Điều kiện tiên quyết (Preconditions):** Đối tượng `Note` gốc trong bộ nhớ có `updatedAt = DateTime(2026, 10, 1, 12, 0, 0)`.
- **Dữ liệu đầu vào (Input / Test Data):**
  - Ca 1: `note.copyWith(content: "Nội dung mới")` (không truyền tham số `updatedAt`)
  - Ca 2: `note.copyWith(updatedAt: DateTime(2026, 10, 5, 14, 0, 0))` (truyền tham số `updatedAt` cố định)
- **Các bước thực hiện (Test Steps):**
  1. Thực thi Ca 1 và so sánh mốc `updatedAt` với thời điểm bắt đầu test.
  2. Thực thi Ca 2 và so sánh mốc `updatedAt` với ngày truyền vào.
- **Kết quả mong đợi (Expected Result):**
  - Ca 1: `res1.updatedAt` tự động nhận mốc thời gian hiện tại ($\ge$ thời điểm bắt đầu test và $>$ `note.updatedAt` gốc).
  - Ca 2: `res2.updatedAt` bằng chính xác `DateTime(2026, 10, 5, 14, 0, 0)`.
- **Kỹ thuật White-box:** Branch Coverage.
- **Nhánh / Điều kiện bao phủ:** Biểu thức `updatedAt: updatedAt ?? DateTime.now()` (Dòng 227).
- **Mức ưu tiên:** **P1** | **Trạng thái & Khả thi:** `DESIGN ONLY — READY FOR AUTHORING (Pure In-Memory)`.

#### `TC-WB-020`: Khả năng phòng thủ khi SQLite map thiếu trường thời gian trong `Note.fromMap`
- **Mục tiêu kiểm thử:** Xác minh factory public `Note.fromMap` tự động gán fallback thời gian hiện tại khi map truyền vào có `created_at` hoặc `updated_at` bằng `null`, tránh crash ứng dụng.
- **Ánh xạ yêu cầu:** `REQ-04` (Tạo ghi chú), `NFR-01` (Độ tin cậy SQLite) / `FN-08`.
- **Module, Class, Method thực tế:** `lib/models/note_model.dart` $\rightarrow$ Class `Note` $\rightarrow$ Public factory `Note.fromMap(Map<String, dynamic> m)` (Dòng 137–158).
- **Điều kiện tiên quyết (Preconditions):** Map dữ liệu từ SQLite bản cũ bị khuyết thiếu trường thời gian (`id`, `title`, `content` vẫn là `String` hợp lệ theo đúng non-nullable type contract của `Note`).
- **Dữ liệu đầu vào (Input / Test Data):**
  `m = {'id': 'legacy-note-99', 'title': 'Ghi chú di sản', 'content': 'Nội dung', 'created_at': null, 'updated_at': null, 'reminder': null}`.
- **Các bước thực hiện (Test Steps):**
  1. Thực thi gọi hàm `Note.fromMap(m)`.
  2. Kiểm tra thuộc tính của đối tượng `Note` sinh ra.
- **Kết quả mong đợi (Expected Result):** Đối tượng `Note` được khởi tạo thành công không bị ném exception; `note.createdAt` và `note.updatedAt` có giá trị thời gian hợp lệ; `note.reminder == null`.
- **Kỹ thuật White-box:** Branch & Guard Clause Coverage.
- **Nhánh / Điều kiện bao phủ:**
  - Nhánh fallback `m['created_at'] ?? DateTime.now().millisecondsSinceEpoch` (Dòng 149–151)
  - Nhánh fallback `m['updated_at'] ?? DateTime.now().millisecondsSinceEpoch` (Dòng 152–154)
  - Nhánh null `m['reminder'] != null ? ... : null` (Dòng 155–157).
- **Mức ưu tiên:** **P2** | **Trạng thái & Khả thi:** `DESIGN ONLY — READY FOR AUTHORING (Pure In-Memory)`.

---

### 2.5. Nhóm Module 5: Last-Write-Wins Timestamp Comparison Logic (In-Memory Reference for `sync_repository.dart`)

#### `TC-WB-021`: So sánh thứ tự ưu tiên Last-Write-Wins (LWW) độc lập trong bộ nhớ
- **Mục tiêu kiểm thử:** Xác minh toán tử so sánh ngặt `DateTime.isAfter()` giữa hai mốc thời gian `local.updatedAt` và `cloud.updatedAt` hoạt động chuẩn xác trong bộ nhớ theo biểu thức phân xử xung đột được sử dụng tại `lib/repositories/sync_repository.dart` (dòng 67 & dòng 121).
- **Ánh xạ yêu cầu:** `REQ-11` (Đồng bộ LWW) / `FN-41` (Giải quyết xung đột).
- **Module, Class, Method thực tế:** Kiểm thử toán tử `DateTime.isAfter` trên hai thực thể `Note` trong bộ nhớ (đối chiếu điều kiện tại `lib/repositories/sync_repository.dart` L67: `local.updatedAt.isAfter(cloud.updatedAt)` và L121: `cloud.updatedAt.isAfter(local.updatedAt)`).
- **Điều kiện tiên quyết (Preconditions):** Khởi tạo hai đối tượng `Note` (`local` và `cloud`) trong bộ nhớ với các mốc `updatedAt` khác nhau.
- **Dữ liệu đầu vào (Input / Test Data):**
  - Cặp 1 (Local mới hơn): `local.updatedAt = DateTime(2026, 10, 10, 12, 0, 5)`, `cloud.updatedAt = DateTime(2026, 10, 10, 12, 0, 0)`
  - Cặp 2 (Cloud mới hơn): `local.updatedAt = DateTime(2026, 10, 10, 12, 0, 0)`, `cloud.updatedAt = DateTime(2026, 10, 10, 12, 0, 5)`
  - Cặp 3 (Trùng khớp millisecond): `local.updatedAt = DateTime(2026, 10, 10, 12, 0, 0)`, `cloud.updatedAt = DateTime(2026, 10, 10, 12, 0, 0)`
- **Các bước thực hiện (Test Steps):**
  1. Đánh giá cặp biểu thức `local.updatedAt.isAfter(cloud.updatedAt)` và `cloud.updatedAt.isAfter(local.updatedAt)` cho Cặp 1.
  2. Đánh giá cặp biểu thức cho Cặp 2.
  3. Đánh giá cặp biểu thức cho Cặp 3.
- **Kết quả mong đợi (Expected Result):**
  - Cặp 1: `local.updatedAt.isAfter(cloud.updatedAt)` trả về `true` (nhánh Push thắng); `cloud.updatedAt.isAfter(local.updatedAt)` trả về `false`.
  - Cặp 2: `local.updatedAt.isAfter(cloud.updatedAt)` trả về `false`; `cloud.updatedAt.isAfter(local.updatedAt)` trả về `true` (nhánh Pull thắng).
  - Cặp 3: Cả hai biểu thức đều trả về `false` (`local.updatedAt.isAtSameMomentAs(cloud.updatedAt)` là `true`).
  - **Giới hạn kỹ thuật & Coverage Gap được ghi nhận minh bạch:**
    1. Ca `TC-WB-021` **CHỈ kiểm tra toán tử so sánh mốc thời gian `DateTime.isAfter` trong bộ nhớ**, **TUYỆT ĐỐI KHÔNG được tính vào chỉ số Line/Branch Coverage thực tế của tệp `lib/repositories/sync_repository.dart`** trong LCOV.
    2. Việc kiểm thử trực tiếp pipeline Push/Pull thật của `SyncRepository.syncNotes()` hiện là **khoảng trống độ bao phủ được chấp nhận (Accepted Coverage Gap)** do `SyncRepository` khởi tạo cứng `FirebaseFirestore.instance`, `FirebaseAuth.instance`, `LocalNoteService()` và `PendingDeleteService()` mà không có Dependency Injection (có thể mở rộng ở giai đoạn sau nếu được phép refactor DI).
    3. Quy tắc nghiệp vụ phân xử hòa khi trùng khớp timestamp (`BR-03`) tiếp tục giữ nguyên trạng thái **`NEEDS CONFIRMATION`** (không tự áp đặt kết quả hợp nhất dữ liệu cho Cặp 3).
- **Kỹ thuật White-box:** Branch & Boundary Value Analysis (Time Domain).
- **Nhánh / Điều kiện bao phủ:** 3 miền giá trị ($\text{local} > \text{cloud}$, $\text{local} < \text{cloud}$, $\text{local} == \text{cloud}$) của biểu thức `isAfter`.
- **Mức ưu tiên:** **P1** | **Trạng thái & Khả thi:** `DESIGN ONLY — READY FOR AUTHORING (In-Memory Logic Only; Not SyncRepository File Coverage)`.

---

### 2.6. Nhóm Module 6: ChecklistItem Fault-Tolerance (`lib/models/checklist_item.dart`)

#### `TC-WB-022`: Khả năng chịu lỗi khi phân tích `ChecklistItem.fromJson` với các trường null
- **Mục tiêu kiểm thử:** Xác minh factory public `ChecklistItem.fromJson` kết hợp constructor `ChecklistItem` tự động sinh UUID khi `id` null, gán chuỗi rỗng khi `text` null và fallback `false` khi `checked` null.
- **Ánh xạ yêu cầu:** `REQ-06` (Quản lý Checklist) / `FN-15` (Tạo ghi chú checklist).
- **Module, Class, Method thực tế:** `lib/models/checklist_item.dart` $\rightarrow$ Class `ChecklistItem` $\rightarrow$ Public factory `ChecklistItem.fromJson(Map<String, dynamic> json)` (Dòng 21–25) và Constructor `ChecklistItem` (Dòng 9–13).
- **Điều kiện tiên quyết (Preconditions):** Map dữ liệu JSON trong bộ nhớ có các trường mang giá trị `null`.
- **Dữ liệu đầu vào (Input / Test Data):** `json = {'id': null, 'text': null, 'checked': null}`.
- **Các bước thực hiện (Test Steps):**
  1. Thực thi gọi hàm `ChecklistItem.fromJson(json)`.
  2. Kiểm tra các thuộc tính của đối tượng `item` trả về.
- **Kết quả mong đợi (Expected Result):** Đối tượng `ChecklistItem` được khởi tạo thành công không bị crash; `item.id` là chuỗi UUID v4 hợp lệ không rỗng; `item.text == ''`; `item.checked == false`.
- **Kỹ thuật White-box:** Branch & Defensive Parsing Coverage.
- **Nhánh / Điều kiện bao phủ:**
  - Truyền `id: json['id'] as String?` (`null`) tại dòng 22 $\rightarrow$ kích hoạt nhánh fallback `id = id ?? const Uuid().v4()` tại dòng 13 của constructor
  - Nhánh `text: json['text'] as String? ?? ''` tại dòng 23
  - Nhánh `checked: json['checked'] as bool? ?? false` tại dòng 24.
- **Mức ưu tiên:** **P2** | **Trạng thái & Khả thi:** `DESIGN ONLY — READY FOR AUTHORING (Pure In-Memory)`.

---

## III. PHÂN TÍCH ĐỘ PHỨC TẠP CYCLOMATIC (CYCLOMATIC COMPLEXITY - V(G))

Để đảm bảo tính nhất quán toán học và đối chiếu chính xác 100% với mã nguồn thực tế trong `lib/`, độ phức tạp Cyclomatic $V(G)$ được tính theo công thức chuẩn McCabe:
$$V(G) = D + 1$$
trong đó $D$ là tổng số điểm quyết định nhị phân (binary decision predicates: câu lệnh rẽ nhánh `if`, vòng lặp `for`/`where`, toán tử ba ngôi `?:`, toán tử null-coalescing `??`, toán tử logic ngắn mạch `&&` / `||`, và nhánh bắt ngoại lệ `catch`) trong đồ thị luồng điều khiển (CFG) của hàm:

| STT | Hàm / Getter thực tế | Vị trí trong `lib/` | Các điểm quyết định ($D$) đối chiếu trực tiếp từ mã nguồn | Số điểm quyết định ($D$) | $V(G) = D + 1$ | Test Case bao phủ |
|:---:|:---|:---|:---|:---:|:---:|:---:|
| 1 | `Note.pendingChecklistCount` | `lib/models/note_model.dart`<br>(Dòng 33–42) | 1. `if (!isChecklist)` (L34)<br>2. `decoded['items'] as List? ?? []` (L37 — toán tử `??`)<br>3. `.where((i) => i['checked'] != true)` (L38)<br>4. `catch (_)` (L39) | $D = 4$<br>*(3 nhánh cấu trúc + 1 `??`)* | **$V(G) = 5$**<br>*(4 ở mức câu lệnh)* | `TC-WB-015` (Note A..E phủ đủ 5 nhánh độc lập) |
| 2 | `Note.plainTextContent` | `lib/models/note_model.dart`<br>(Dòng 45–69) | 1. `if (content.isEmpty)` (L46)<br>2. `if (isChecklist)` (L47)<br>3. `if (trimmed.startsWith('[') \|\| trimmed.startsWith('{'))` (L51: 1 `if` + 1 `\|\|`)<br>4. `if (decoded is List)` (L54)<br>5. `for (final item in decoded)` (L56)<br>6. `if (item is Map && item.containsKey('insert'))` (L57: 1 `if` + 1 `&&`)<br>7. `if (val is String)` (L59)<br>8. `catch (_)` (L66) | $D_{\text{statement}} = 8$<br>($D_{\text{compound}} = 10$ tính cả `\|\|`, `&&`) | **$V(G) = 9$**<br>*(11 ở mức điều kiện con)* | `TC-WB-016` & `TC-WB-017` (phủ toàn bộ 8 câu lệnh rẽ nhánh & 2 điều kiện ghép) |
| 3 | `Note.copyWith`<br>*(Nhánh `updatedAt` & `reminder`)* | `lib/models/note_model.dart`<br>(Dòng 200–229; trọng tâm L227–228) | • Trong phạm vi `TC-WB-018, 019` (L227–228):<br>1. `updatedAt ?? DateTime.now()` (L227)<br>2. `clearReminder ? null : ...` (L228)<br>3. `reminder ?? this.reminder` (L228)<br>*(Lưu ý: Toàn hàm `copyWith` còn có 9 toán tử `??` cho các trường khác ở L217–225)* | $D_{\text{sub}} = 3$<br>($D_{\text{full}} = 12$) | **$V(G)_{\text{sub}} = 4$**<br>*($V(G)_{\text{full}} = 13$)* | `TC-WB-018`, `TC-WB-019` |
| 4 | `ChecklistItem.fromJson`<br>*(kèm Constructor)* | `lib/models/checklist_item.dart`<br>(Dòng 9–13 & 21–25) | 1. `id = id ?? const Uuid().v4()` (L13, nhận `json['id'] as String?` từ L22)<br>2. `json['text'] as String? ?? ''` (L23)<br>3. `json['checked'] as bool? ?? false` (L24) | $D = 3$ | **$V(G) = 4$** | Baseline Tests 1–3 + `TC-WB-022` |
| 5 | `CloudinaryService._extractPublicId` | `lib/services/cloudinary_service.dart`<br>(Dòng 27–47) | 1. `if (rootIndex == -1)` (L33)<br>2. `if (publicId.contains('.'))` (L38)<br>3. `catch (e)` (L43) | $D = 3$ | **$V(G) = 4$** | `TC-WB-006`, `TC-WB-007` *(qua `deleteFile`)* |

---

## IV. QUY TRÌNH BẢO TOÀN VÀ QUẢN TRỊ THỰC THI (EXECUTION GOVERNANCE)

1. **Nguyên tắc đóng băng tài liệu (Specification Freeze):** Bộ tài liệu này được chốt chính thức làm tiêu chuẩn thiết kế kiểm thử cho toàn bộ 22 ca White-box. Sau khi chốt, chỉ sửa đổi tài liệu nếu phát hiện sai lệch thực tế khách quan trong quá trình chạy test và có lý do kỹ thuật minh bạch.
2. **Không ép PASS & Phân biệt rõ Target Coverage (Zero Forced Pass Policy):**
   - Mục tiêu **$\ge 80\%$ Line Coverage cho `NoteModel` (`lib/models/note_model.dart`)** là **chỉ số kỳ vọng (Target Benchmark)** sau khi bổ sung các ca `TC-WB-015..020`, **KHÔNG phải kết quả đã đạt** (hiện tại Baseline đã đo là **44.35%** cho `note_model.dart` và **50.00%** cho 2 file model), và **KHÔNG phải điều kiện cưỡng bức ép PASS** hay ngăn cản việc đóng đợt kiểm thử nếu có giới hạn kỹ thuật khách quan.
   - Nếu kết quả chạy test thực tế trả về FAIL, đội ngũ QA lập tức mở Defect Log ghi nhận lỗi trung thực. Tuyệt đối không chỉnh sửa kết quả kỳ vọng trong test case hay sửa mã nguồn ứng dụng trong `lib/` chỉ để ép kết quả chuyển sang PASS.
3. **Phân định rõ ràng giới hạn phạm vi Selective White-box:**
   - **Nhóm sẵn sàng viết và chạy Unit Test ngay (`READY FOR TEST AUTHORING`):** 8 ca In-Memory `TC-WB-015` .. `TC-WB-022` (và có thể kèm `TC-WB-006`, `TC-WB-008` qua public entry point).
   - **Nhóm giới hạn kỹ thuật được chấp nhận (`ACCEPTED LIMITATIONS`):**
     + `TC-WB-001` .. `TC-WB-005` (`AuthProvider`): Giữ ở mức `DESIGN ONLY` do phụ thuộc cứng vào singleton `FirebaseAuth.instance` / `FirebaseFirestore.instance` và hàm private `_syncUserProfile`.
     + `TC-WB-007`, `TC-WB-009`, `TC-WB-010` (`CloudinaryService`): Giữ ở mức `DESIGN ONLY` trừ khi cấu hình `HttpOverrides` & file tạm.
     + `TC-WB-011` .. `TC-WB-014` (`firestore.rules`): Ghi nhận đúng bản chất là kiểm thử mô phỏng logic quy tắc trong Dart (`test/security_rules_test.dart`), không phải Firebase Emulator Rules Engine.
     + `TC-WB-021` (LWW Timestamp): Chỉ kiểm tra toán tử `DateTime.isAfter` trong bộ nhớ, không tính thành coverage của `sync_repository.dart`; kiểm thử pipeline Push/Pull thật của `SyncRepository` là Coverage Gap được chấp nhận; quy tắc hòa `BR-03` giữ nguyên trạng thái `NEEDS CONFIRMATION`.
