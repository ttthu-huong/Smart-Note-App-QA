# TÀI LIỆU THIẾT KẾ KIỂM THỬ HỘP TRẮNG (WHITE-BOX TEST SUITE)
## Dự án: Smart Note App
**Mục tiêu:** Kiểm thử cấu trúc mã nguồn, độ bao phủ câu lệnh (Statement Coverage), độ bao phủ nhánh (Branch/Decision Coverage) và logic điều kiện cho các module core của ứng dụng Smart Note App  
**Tài liệu tham chiếu mã nguồn:**
- `lib/providers/auth_provider.dart` (Quản lý trạng thái xác thực người dùng)
- `lib/services/cloudinary_service.dart` (Dịch vụ tải lên & xóa phương tiện Cloudinary)
- `firestore.rules` (Quy tắc kiểm soát truy cập dữ liệu Cloud Firestore)
- `lib/helpers/database_helper.dart` (Quản lý cơ sở dữ liệu SQLite cục bộ)

---

## 1. PHÂN TÍCH VÀ THIẾT KẾ TEST CASE HỘP TRẮNG CHI TIẾT

### 1.1. Module 1: AuthProvider (`lib/providers/auth_provider.dart`)

| TC-ID | Hàm / Phương thức kiểm thử | Cấu trúc luồng / Nhánh logic kiểm tra (Control Flow) | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected Output) | Loại bao phủ (Coverage Type) | Ánh xạ Yêu cầu |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-WB-001** | `setError(String? message)` | Nhánh `message != null` $\rightarrow$ gán `_error` và gọi `notifyListeners()` | `message = "Email không hợp lệ"` | `_error == "Email không hợp lệ"`, UI nhận tín hiệu thông báo thay đổi | Statement & State Coverage | REQ-02 (Login/Register validation) |
| **TC-WB-002** | `setError(String? message)` | Nhánh `message == null` $\rightarrow$ xóa lỗi `_error = null` | `message = null` | `_error == null`, trạng thái lỗi bị xóa | Statement Coverage | REQ-02 (Clear validation errors) |
| **TC-WB-003** | `authStateChanges()` listener | Luồng sự kiện thay đổi auth state: `User == null` (Đăng xuất) | `user = null` | `_user == null`, `_error == null`, `_userData == null` | Branch Coverage (`user == null`) | REQ-02 (Logout state clean) |
| **TC-WB-004** | `_syncUserProfile(User user)` | Điều kiện kiểm tra sự tồn tại của Document: `!snapshot.exists == true` (Tạo mới) | User mới đăng ký chưa có record trong Firestore | Thực thi `userDoc.set(...)` với `createdAt = serverTimestamp()`, `_userData` được nạp | Decision Coverage (`exists == false`) | REQ-02 (User registration profile sync) |
| **TC-WB-005** | `_syncUserProfile(User user)` | Điều kiện kiểm tra sự tồn tại của Document: `!snapshot.exists == false` (Đã tồn tại) | User cũ đã có record trong Firestore | Không chạy `set()`, nạp trực tiếp `_userData = snapshot.data()` | Decision Coverage (`exists == true`) | REQ-02 (User login profile sync) |

---

### 1.2. Module 2: CloudinaryService (`lib/services/cloudinary_service.dart`)

| TC-ID | Hàm / Phương thức kiểm thử | Cấu trúc luồng / Nhánh logic kiểm tra (Control Flow) | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected Output) | Loại bao phủ (Coverage Type) | Ánh xạ Yêu cầu |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-WB-006** | `_extractPublicId(String url)` | Vòng lặp/Điều kiện tìm kiếm path segment: `rootIndex == -1` (URL sai định dạng) | `url = "https://invalid-domain.com/photo.jpg"` | Trả về `null`, ghi log `"extract public_id error"` | Branch Coverage (`rootIndex == -1`) | REQ-08 (Media asset management) |
| **TC-WB-007** | `_extractPublicId(String url)` | Cắt chuỗi loại bỏ extension: `publicId.contains('.') == true` | `url = "https://res.cloudinary.com/demo/image/upload/v1/smart_note/user1/images/pic.jpg"` | Trả về `"smart_note/user1/images/pic"` | Statement & Branch Coverage | REQ-08 (Public ID extraction) |
| **TC-WB-008** | `uploadImage(File file, String userId)` | Kiểm tra cờ cấu hình ENV: `_cloudName.isEmpty || _uploadPreset.isEmpty == true` | `CLOUDINARY_CLOUD_NAME = ""` (ENV chưa nạp) | Trả về `null`, ghi log `"ENV rỗng!"`, ngắt sớm không gửi HTTP request | Decision Coverage (Guard clause) | REQ-08 (Cloudinary config safety) |
| **TC-WB-009** | `uploadImage(File file, String userId)` | Phân nhánh thư mục lưu trữ: `isAvatar == true` vs `isDrawing == true` vs `isImage` | `isAvatar = true` | Field `folder` trong HTTP Multipart request được set là `'smart_note/$userId/avatars'` | Multiple Condition Coverage | REQ-08 (Media folder routing) |
| **TC-WB-010** | `uploadImage(File file, String userId)` | Kiểm tra mã trạng thái HTTP phản hồi: `response.statusCode == 200` vs `!= 200` | HTTP Response Status = `200 OK` | Giải mã JSON, trả về chuỗi `secure_url` | Branch Coverage (`statusCode == 200`) | REQ-08 (Media upload success) |

---

### 1.3. Module 3: Cloud Firestore Security Rules (`firestore.rules`)

| TC-ID | Hàm / Quy tắc kiểm thử | Cấu trúc luồng / Nhánh logic kiểm tra (Control Flow) | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected Output) | Loại bao phủ (Coverage Type) | Ánh xạ Yêu cầu |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-WB-011** | `isOwner(userId)` | Điều kiện kết hợp: `isAuthenticated() && request.auth.uid == userId` | `request.auth.uid = "alice"`, `userId = "alice"` | Trả về `true` $\rightarrow$ Cho phép truy cập (**ALLOW**) | Condition Coverage (`true && true`) | REQ-09 (Data privacy isolation) |
| **TC-WB-012** | `isOwner(userId)` | Nhánh từ chối 1: Chưa đăng nhập `request.auth == null` | `request.auth = null`, `userId = "alice"` | Trả về `false` $\rightarrow$ Từ chối truy cập (**DENY**) | Condition Coverage (`false && true`) | REQ-09 (Unauthenticated access block) |
| **TC-WB-013** | `isOwner(userId)` | Nhánh từ chối 2: Đăng nhập tài khoản khác `request.auth.uid != userId` | `request.auth.uid = "bob"`, `userId = "alice"` | Trả về `false` $\rightarrow$ Từ chối truy cập (**DENY**) | Condition Coverage (`true && false`) | REQ-09 (Cross-user access block) |
| **TC-WB-014** | `isValidNote(userId)` | Kiểm tra thuộc tính sở hữu dữ liệu ghi: `request.resource.data.user_id == userId` | Data ghi có `user_id = "alice"`, target path `users/alice/notes` | Trả về `true` $\rightarrow$ Cho phép ghi (**ALLOW**) | Statement & Decision Coverage | REQ-09 (Data payload ownership validation) |

---

## 2. MA TRẬN PHÂN TÍCH MA TRẬN LUỒNG ĐIỀU KHIỂN (CONTROL FLOW GRAPH METRICS)

* **Độ phức tạp xyclomatic (Cyclomatic Complexity - $V(G)$)**:
  - Hàm `_extractPublicId`: $V(G) = 3$ (1 try-catch block, 1 if check `rootIndex`, 1 if check `contains('.')`).
  - Hàm `uploadImage`: $V(G) = 4$ (1 try-catch block, 1 check ENV rỗng, 1 ternary check `isAvatar`, 1 check `statusCode == 200`).
  - Quy tắc Security Rules `match /users/{userId}/notes/{noteId}`: $V(G) = 3$ (phân nhánh `isOwner` và `isValidNote`).

* **Trạng thái thực thi mã kiểm thử Hộp trắng**:
  - Các bài test trong `test/security_rules_test.dart` và `test/auth_provider_test.dart` đã được chuyển thành mã tự động Dart và thực thi PASS.
