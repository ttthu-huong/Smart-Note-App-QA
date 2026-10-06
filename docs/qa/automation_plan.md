# KẾ HOẠCH KIỂM THỬ TỰ ĐỘNG (AUTOMATION TEST PLAN) — SMART NOTE APP
## Dự án: Smart Note App
**Branch:** `huong`  
**Repository:** `ttt-huong/Smart-Note-App-QA`  
**Tiêu chuẩn:** IEEE 829 & ISTQB Test Plan Structure  
**Phạm vi:** Chuyển đổi các Black-box Test Cases chính thức thành kịch bản tự động có khả năng chạy lặp lại trên thiết bị thật  

---

## 1. MỤC TIÊU VÀ CHIẾN LƯỢC TỰ ĐỘNG HÓA
- **Mục tiêu:** Xây dựng bộ test hồi quy tự động (Regression Test Suite) đảm bảo các tính năng cốt lõi của Smart Note App hoạt động chính xác qua các lần cập nhật mã nguồn.
- **Phân loại kiểm thử tự động:**
  - **Android UI/E2E — Python 3.13 + pytest + uiautomator2 + ADB:** Tập trung vào kiểm thử giao diện hộp đen đầu cuối trên thiết bị Android thật (đang được triển khai trong thư mục `automation/`).
  - **Unit Test & Widget Test (Flutter Native):** Thuộc phạm vi kiểm thử thành phần nội bộ (White-box / Component), không thay thế cho Black-box UI Automation.
- **Nguyên tắc cốt lõi:**
  1. Giữ nguyên 100% Expected Result của Black-box Test Case. Tuyệt đối không sửa assertion để ép test PASS.
  2. Báo cáo trung thực lỗi ứng dụng (Application Bug) và phân tách rõ ràng với lỗi kịch bản/dữ liệu kiểm thử.
  3. Cơ chế Dynamic-First (tìm kiếm đa năng text/content-desc trên Flutter) kết hợp Coordinate-Fallback nhằm tối ưu độ ổn định.

---

## 2. PHÂN KỲ TRIỂN KHAI (AUTOMATION PHASES)

### Phase 1: Các nhóm chức năng cơ bản, độc lập và ổn định cao (Đang tiến hành)
- **FN-04 (Đăng nhập tài khoản Email/Password):** 4 TC (`TC-BB-006` → `TC-BB-009`, tổng 4 items) — **Đã hoàn thành viết code & đã chạy thực tế (DONE)**.
- **FN-08 (Tạo Ghi chú văn bản mới):** 3 TC (`TC-BB-016`, `TC-BB-017`, `TC-BB-018`) — **Ưu tiên cao tiếp theo**.
- **FN-09 (Chỉnh sửa Ghi chú & Tự động lưu):** 1 TC (`TC-BB-019`) — **Ưu tiên cao tiếp theo**.
- **FN-20 (Ghim & Bỏ ghim Ghi chú):** 2 TC (`TC-BB-024`, `TC-BB-025`) — **Ưu tiên cao tiếp theo**.
- **FN-23 (Tìm kiếm Ghi chú theo từ khóa):** 3 TC (`TC-BB-026`, `TC-BB-027`, `TC-BB-028`) — **Ưu tiên cao tiếp theo**.

### Phase 2: Các nhóm chức năng mở rộng dữ liệu và vòng đời (Kế hoạch tiếp theo)
- **FN-02 (Đăng ký tài khoản Email):** 5 TC (`TC-BB-001` → `TC-BB-005`) — Đòi hỏi chiến lược dọn dẹp hoặc sinh email ngẫu nhiên.
- **FN-09 (Chỉnh sửa Ghi chú & Tự động lưu):** 1 TC (`TC-BB-020`).
- **FN-10/FN-11/FN-12 (Xóa vào Thùng rác / Khôi phục / Xóa vĩnh viễn):** 3 TC (`TC-BB-021`, `TC-BB-022`, `TC-BB-023`).
- **FN-23 (Tìm kiếm Ghi chú theo từ khóa):** 1 TC (`TC-BB-029`: Ký tự đặc biệt / Robustness).

### Phase 3: Các nhóm tính năng đặc thù (DEFERRED - Tạm hoãn)
- **FN-05 (Đăng nhập nhanh Google):** 2 TC (`TC-BB-010`, `TC-BB-011`) — Phụ thuộc Google OAuth Dialog.
- **FN-29/FN-30 (Khóa & Mở khóa Ghi chú bằng Sinh trắc học):** 4 TC (`TC-BB-012` → `TC-BB-015`) — Phụ thuộc phần cứng quét vân tay/khuôn mặt trên thiết bị thật.
- **FN-40/FN-41 (Đồng bộ Offline/Online & Giải quyết xung đột LWW):** 2 TC (`TC-BB-030`, `TC-BB-031`) — Yêu cầu 2 thiết bị vật lý hoạt động đồng thời và thao tác ngắt/bật mạng.

---

## 3. BẢNG PHÂN BỔ CHI TIẾT 31 TEST CASES

| TC-ID | Chức năng chuẩn hóa | Loại Automation | Công cụ | Ưu tiên | Trạng thái | Lý do / Ghi chú |
|---|---|---|---|:---:|:---:|---|
| **TC-BB-006** | Đăng nhập tài khoản Email hợp lệ | Android UI/E2E | Python + u2 | P1 | **DONE** | Đã viết test, đã chạy thực tế (FAIL - BUG-BB-004 Candidate / cần xác minh Precondition/Test Data emailVerified) |
| **TC-BB-007** | Đăng nhập thất bại do sai Mật khẩu | Android UI/E2E | Python + u2 | P1 | **DONE** | Đã viết test, đã chạy thực tế (FAIL - BUG-BB-003) |
| **TC-BB-008** | Đăng nhập thất bại do tài khoản không tồn tại | Android UI/E2E | Python + u2 | P1 | **DONE** | Đã viết test, đã chạy thực tế (FAIL - BUG-BB-002) |
| **TC-BB-009** | Đăng nhập thất bại do để trống Mật khẩu | Android UI/E2E | Python + u2 | P1 | **DONE** | Đã viết test, đã chạy thực tế (PASS) |
| **TC-BB-016** | Tạo ghi chú văn bản có Tiêu đề và Nội dung | Android UI/E2E | Python + u2 | P1 | **PLANNED** | Chuẩn bị viết code trong Phase 1 |
| **TC-BB-017** | Tạo ghi chú không có tiêu đề nhưng có nội dung. | Android UI/E2E | Python + u2 | P1 | **PLANNED** | Test Data: Title = "", Content = "Ý tưởng nhanh không tiêu đề" |
| **TC-BB-018** | Tạo ghi chú với cả tiêu đề và nội dung để trống; xác minh ứng dụng không tạo ghi chú rỗng. | Android UI/E2E | Python + u2 | P1 | **PLANNED** | Lưu ý: Auto-save thuộc TC-BB-020, không thuộc TC-BB-018 |
| **TC-BB-019** | Chỉnh sửa nội dung ghi chú. | Android UI/E2E | Python + u2 | P1 | **PLANNED** | Chuẩn bị viết code trong Phase 1 |
| **TC-BB-024** | Ghim ghi chú lên đầu danh sách Trang chủ | Android UI/E2E | Python + u2 | P1 | **PLANNED** | Chuẩn bị viết code trong Phase 1 |
| **TC-BB-025** | Bỏ ghim ghi chú trở về danh sách thông thường | Android UI/E2E | Python + u2 | P1 | **PLANNED** | Chuẩn bị viết code trong Phase 1 |
| **TC-BB-026** | Tìm kiếm ghi chú theo từ khóa Tiêu đề | Android UI/E2E | Python + u2 | P1 | **PLANNED** | Chuẩn bị viết code trong Phase 1 |
| **TC-BB-027** | Tìm kiếm ghi chú theo từ khóa Nội dung | Android UI/E2E | Python + u2 | P1 | **PLANNED** | Chuẩn bị viết code trong Phase 1 |
| **TC-BB-028** | Tìm kiếm với từ khóa không tồn tại | Android UI/E2E | Python + u2 | P1 | **PLANNED** | Chuẩn bị viết code trong Phase 1 |
| **TC-BB-001** | Đăng ký tài khoản với Email và Mật khẩu hợp lệ | Android UI/E2E | Python + u2 | P2 | **PLANNED** | Cần cơ chế tạo email test ngẫu nhiên |
| **TC-BB-002** | Để trống thông tin khi đăng ký | Android UI/E2E | Python + u2 | P2 | **PLANNED** | Validation form đăng ký |
| **TC-BB-003** | Đăng ký với định dạng Email không hợp lệ | Android UI/E2E | Python + u2 | P2 | **PLANNED** | Validation format email |
| **TC-BB-004** | Đăng ký với mật khẩu ngắn dưới 6 ký tự | Android UI/E2E | Python + u2 | P2 | **PLANNED** | Validation password length |
| **TC-BB-005** | Đăng ký với email đã tồn tại trên hệ thống | Android UI/E2E | Python + u2 | P2 | **PLANNED** | Duplicate email check |
| **TC-BB-020** | Kiểm tra tự động lưu nội dung sau khi chỉnh sửa và rời màn hình. | Android UI/E2E | Python + u2 | P2 | **PLANNED** | Auto-save sau chỉnh sửa |
| **TC-BB-021** | Chuyển ghi chú vào Thùng rác | Android UI/E2E | Python + u2 | P2 | **PLANNED** | Luồng Move to Trash |
| **TC-BB-022** | Khôi phục ghi chú từ Thùng rác về Trang chủ | Android UI/E2E | Python + u2 | P2 | **PLANNED** | Luồng Restore from Trash |
| **TC-BB-023** | Xóa vĩnh viễn ghi chú khỏi Thùng rác | Android UI/E2E | Python + u2 | P2 | **PLANNED** | Luồng Delete Forever |
| **TC-BB-029** | Tìm kiếm với chuỗi Ký tự đặc biệt / Robustness | Android UI/E2E | Python + u2 | P2 | **PLANNED** | Kiểm tra Robustness của thanh tìm kiếm |
| **TC-BB-010** | Đăng nhập thành công qua tài khoản Google | Android UI/E2E | Python + u2 | P3 | **DEFERRED** | Phụ thuộc Google OAuth Dialog |
| **TC-BB-011** | Hủy quá trình đăng nhập Google | Android UI/E2E | Python + u2 | P3 | **DEFERRED** | Phụ thuộc Google OAuth Dialog |
| **TC-BB-012** | Kích hoạt khóa sinh trắc học cho ghi chú | Android UI/E2E | Python + u2 | P3 | **DEFERRED** | Phụ thuộc phần cứng Biometric |
| **TC-BB-013** | Mở khóa ghi chú bằng sinh trắc học thành công | Android UI/E2E | Python + u2 | P3 | **DEFERRED** | Phụ thuộc phần cứng Biometric |
| **TC-BB-014** | Mở khóa ghi chú bằng sinh trắc học thất bại | Android UI/E2E | Python + u2 | P3 | **DEFERRED** | Phụ thuộc phần cứng Biometric |
| **TC-BB-015** | Tắt tính năng khóa sinh trắc học cho ghi chú | Android UI/E2E | Python + u2 | P3 | **DEFERRED** | Phụ thuộc phần cứng Biometric |
| **TC-BB-030** | Tạo ghi chú ngoại tuyến và tự động đồng bộ khi có mạng | Android UI/E2E | Python + u2 | P3 | **DEFERRED** | Yêu cầu điều khiển chế độ máy bay |
| **TC-BB-031** | Giải quyết xung đột chỉnh sửa đồng thời theo nguyên tắc LWW | Android UI/E2E | Python + u2 | P3 | **DEFERRED** | Yêu cầu 2 thiết bị thực tế đồng bộ |
