# KẾ HOẠCH CHI TIẾT KIỂM THỬ NÂNG CAO (CHƯƠNG 6)
**Học phần**: Đánh giá & Kiểm định chất lượng phần mềm (CSE703010)  
**Đề tài**: Smart Note App (Offline-First) · **Nhánh thực hiện**: `dung`  
**Mục tiêu**: Triển khai toàn diện 3 trụ cột kiểm thử nâng cao: **Bảo mật (Security)**, **Đột biến (Mutation)** và **Hiệu năng (Performance)**.

---

## 📑 MỤC LỤC KẾ HOẠCH
1. [Tổng quan & Mục tiêu Chương 6](#1-tổng-quan--mục-tiêu-chương-6)
2. [Phần 1: Kiểm thử Bảo mật (Security Testing - Mục 6.1)](#2-phần-1-kiểm-thử-bảo-mật-security-testing---mục-61)
   - 2.1 Mô hình đe dọa STRIDE & Ma trận rủi ro
   - 2.2 Danh mục 14 kịch bản kiểm thử bảo mật (SEC-01 đến SEC-14)
   - 2.3 Tiêu chí nghiệm thu & Phân loại mức độ nghiêm trọng (CVSS)
3. [Phần 2: Kiểm thử Đột biến (Mutation Testing - Mục 6.2)](#3-phần-2-kiểm-thử-đột-biến-mutation-testing---mục-62)
   - 3.1 Mục tiêu & Cơ sở toán học (Mutation Score)
   - 3.2 Bộ toán tử đột biến (Mutation Operators: ROR, AOR, LCR, UOI, SVR)
   - 3.3 Thiết kế danh mục 60 Mutants trên 6 module trọng yếu
   - 3.4 Quy trình thực thi & Phân tích Đột biến tương đương (Equivalent Mutants)
4. [Phần 3: Kiểm thử Hiệu năng (Performance Testing - Mục 6.3)](#4-phần-3-kiểm-thử-hiệu-năng-performance-testing---mục-63)
   - 4.1 Mô hình đo 3 tầng (T1: Logic/SQLite, T2: UI/App trên máy ảo, T3: Bundle APK)
   - 4.2 Danh mục 10 kịch bản kiểm thử hiệu năng (PERF-01 đến PERF-10)
   - 4.3 Phương pháp đo, ngưỡng đạt chuẩn (SLA) & Công cụ thu thập số liệu
5. [Lịch trình thực thi & Phân công nhiệm vụ](#5-lịch-trình-thực-thi--phân-công-nhiệm-vụ)

---

## 1. TỔNG QUAN & MỤC TIÊU CHƯƠNG 6
Kiểm thử nâng cao nhằm chứng minh và đánh giá phần mềm ở các khía cạnh phi chức năng (Non-functional) và chất lượng mã nguồn chuyên sâu:
* **Bảo mật**: Đảm bảo dữ liệu người dùng không bị rò rỉ tại Local Storage (SQLite), Network (API), Cloud (Firestore Rules) và Reverse Engineering (APK).
* **Đột biến**: Định lượng năng lực phát hiện lỗi thực tế của bộ 83 test case hộp trắng, vượt qua giới hạn của Code Coverage truyền thống.
* **Hiệu năng**: Khảo sát tải dữ liệu lớn (1.000 – 10.000 notes), đo thời gian phản hồi, độ mượt giao diện (frame rate) và rò rỉ bộ nhớ (memory leaks).

---

## 2. PHẦN 1: KIỂM THỬ BẢO MẬT (SECURITY TESTING - MỤC 6.1)

### 2.1 Mô hình đe dọa STRIDE
| Mối đe dọa (STRIDE) | Tài sản / Vùng chịu tác động | Kịch bản rủi ro tiềm ẩn | Biện pháp kiểm định |
| :--- | :--- | :--- | :--- |
| **S**poofing (Giả mạo) | Auth Token, User ID | Giả mạo `user_id` để truy vấn note của người khác trên Firestore | SEC-07, SEC-08 |
| **T**ampering (Sửa đổi) | CSDL SQLite cục bộ, Cache | Sửa nội dung note hoặc trạng thái khóa trực tiếp trong CSDL thiết bị | SEC-11, SEC-12 |
| **R**epudiation (Chối bỏ) | Đồng bộ dữ liệu LWW | Xung đột thời gian cập nhật mà không có audit log | SEC-10 |
| **I**nformation Disclosure (Lộ tin) | API Keys, Note bị khóa, Log | Lộ Cloudinary Secret qua file `.env` nhúng trong APK; lộ note khóa qua Search/PDF | SEC-01, SEC-04, SEC-13 |
| **D**enial of Service (Từ chối DV) | Local SQLite, Network | Đưa payload Delta JSON khổng lồ làm treo UI hoặc crash app | SEC-02, PERF-06 |
| **E**levation of Privilege (Leo quyền)| Firestore Security Rules | Người dùng thường đọc/ghi được quyền Admin hoặc note người khác | SEC-06, SEC-09 |

### 2.2 Danh mục 14 Kịch bản Kiểm thử Bảo mật (SEC-01 đến SEC-14)
* **Nhóm 1: Phân tích Tĩnh & Cấu hình (SAST)**
  * `SEC-01`: Quét tìm API Keys, Secret, Passwords bị hardcode trong mã nguồn `lib/`.
  * `SEC-02`: Rà soát log nhạy cảm (`debugPrint`, `print`) có thể rò rỉ token hoặc URL ảnh nhạy cảm khi chạy release.
  * `SEC-03`: Rà soát quyền trong `android/app/src/main/AndroidManifest.xml` (`allowBackup=true`, quyền vị trí/camera thừa).
* **Nhóm 2: Phân tích Reverse Engineering & Gói cài đặt (APK Analysis)**
  * `SEC-04`: Giải nén APK Release kiểm tra `assets/flutter_assets/.env` (Trích xuất Cloudinary API Secret).
  * `SEC-05`: Quét lỗ hổng tĩnh với checklist OWASP Mobile Top 10 (M1 - M10).
* **Nhóm 3: Kiểm thử Firestore Security Rules (Cloud Security)**
  * `SEC-06`: Người dùng chưa xác thực (Unauthenticated) không được phép đọc/ghi dữ liệu.
  * `SEC-07`: User A không thể đọc danh sách note của User B (`request.auth.uid != resource.data.user_id`).
  * `SEC-08`: User A không thể ghi đè hoặc tạo note với `user_id` giả mạo của User B.
  * `SEC-09`: Chủ sở hữu hợp lệ (Owner) được toàn quyền CRUD note của chính mình.
  * `SEC-10`: Tags và Media metadata bị cô lập nghiêm ngặt theo từng tài khoản.
* **Nhóm 4: Bảo mật Lưu trữ Cục bộ & Sinh trắc học (Data at Rest & Biometrics)**
  * `SEC-11`: Kiểm tra tính bảo mật của tệp CSDL SQLite `smart_note.db` (Plaintext vs Encrypted SQLCipher).
  * `SEC-12`: Kiểm định cơ chế khóa sinh trắc học: Dữ liệu note bị khóa có được mã hóa payload hay chỉ là flag ẩn trên UI.
  * `SEC-13`: Kiểm tra rò rỉ dữ liệu của note bị khóa qua: Tìm kiếm đa năng (Search), thông báo nhắc việc, trích xuất PDF.
* **Nhóm 5: Bảo mật Truyền thông (Data in Transit)**
  * `SEC-14`: Kiểm tra toàn bộ endpoint kết nối ngoại vi (Cloudinary, Firebase) có bắt buộc TLS/HTTPS và chặn Cleartext Traffic.

---

## 3. PHẦN 2: KIỂM THỬ ĐỘT BIẾN (MUTATION TESTING - MỤC 6.2)

### 3.1 Mục tiêu & Công thức Tính toán
* Đo lường xác suất một lỗi logic được cấy vào mã nguồn sẽ làm fail ít nhất 1 test case trong bộ 83 test hộp trắng.
$$\text{Mutation Score (MS)} = \frac{\text{Killed Mutants}}{\text{Total Mutants} - \text{Equivalent Mutants}} \times 100\%$$
* **Tiêu chuẩn mục tiêu môn học**: Đạt $\text{MS} \ge 80\%$.

### 3.2 Bộ toán tử đột biến chuẩn hóa
1. **ROR (Relational Operator Replacement)**: Thay đổi toán tử so sánh (`==` $\to$ `!=`, `<` $\to$ `<=`, `>` $\to$ `>=`).
2. **AOR (Arithmetic Operator Replacement)**: Thay đổi toán tử số học (`+` $\to$ `-`, `*` $\to$ `/`).
3. **LCR (Logical Connector Replacement)**: Thay đổi toán tử logic (`&&` $\to$ `||`, `||` $\to$ `&&`).
4. **UOI (Unary Operator Insertion)**: Thêm/bỏ toán tử đảo ngược (`!condition` $\to$ `condition`).
5. **SVR (Statement / Return Value Replacement)**: Đổi giá trị trả về (`return true` $\to$ `return false`, `return null`).

### 3.3 Phân bổ 60 Mutants trên 6 Module Trọng yếu
* **Module 1 (Biometric - `biometric_service.dart`)**: 10 Mutants (đột biến điều kiện kiểm tra phần cứng, kết quả auth, cờ trạng thái).
* **Module 2 (Auth Validation - `auth_provider.dart`)**: 10 Mutants (đột biến regex email, độ dài mật khẩu `< 6`, logic trim).
* **Module 3 (Note CRUD - `local_note_service.dart`)**: 10 Mutants (đột biến câu lệnh SQL INSERT, UPDATE, soft delete `is_deleted = 1`).
* **Module 4 (Search Logic - `note_repository.dart`)**: 10 Mutants (đột biến logic tìm kiếm hoa/thường, prefix `has:`, `is:pinned`).
* **Module 5 (Sync & LWW - `sync_repository.dart`)**: 10 Mutants (đột biến so sánh timestamp LWW `updated_at`, cờ `is_synced`).
* **Module 6 (Trash Management - `note_provider.dart`)**: 10 Mutants (đột biến lọc thùng rác, xóa vĩnh viễn, khôi phục).

---

## 4. PHẦN 3: KIỂM THỬ HIỆU NĂNG (PERFORMANCE TESTING - MỤC 6.3)

### 4.1 Mô hình 3 Tầng Thực nghiệm
* **Tầng 1 (T1 - Micro-benchmark SQLite & Thuật toán)**: Thực thi đo thời gian xử lý trực tiếp trên môi trường máy chủ/PC với volume dữ liệu lớn (100 đến 10.000 notes).
* **Tầng 2 (T2 - Ứng dụng & Thiết bị trên Máy ảo Android)**: Sử dụng Android SDK tools (`adb`, `dumpsys gfxinfo`, `dumpsys meminfo`) để đo Cold Start, Frame Render, Memory Leak.
* **Tầng 3 (T3 - Phân tích Bundle APK)**: Phân tích dung lượng APK theo thành phần (DEX code, assets, native libraries) qua `flutter build apk --analyze-size`.

### 4.2 Danh mục 10 Kịch bản Kiểm thử Hiệu năng (PERF-01 đến PERF-10)
| Mã | Tầng | Kịch bản kiểm thử | Quy mô dữ liệu | Tiêu chí chấp nhận (SLA) |
| :--- | :---: | :--- | :--- | :--- |
| **PERF-01** | T1 | Ghi hàng loạt (Bulk Insert) | 100 / 1.000 / 5.000 / 10.000 | Thời gian trung bình mỗi note $< 5\text{ms}$ |
| **PERF-02** | T1 | Truy vấn phân trang `getAllNotes` | 1k / 5k / 10k trong DB | Trang đầu phản hồi $< 50\text{ms}$ |
| **PERF-03** | T1 | Tìm kiếm văn bản `searchNotes` (LIKE) | 1k / 5k / 10k / 20k | $< 300\text{ms}$ tại 5k records |
| **PERF-04** | T1 | So sánh hiệu năng có Index vs không Index | 10.000 records | Có Index nhanh hơn tối thiểu $2\times$ |
| **PERF-05** | T1 | Xử lý logic giải quyết xung đột LWW khi Spike | 100 / 500 / 2.000 notes | Tăng trưởng thời gian tiệm cận tuyến tính |
| **PERF-06** | T1 | Parse Delta JSON & Checklist kích thước lớn | 10 KB / 100 KB / 1 MB | Xử lý an toàn, không văng OutOfMemory |
| **PERF-07** | T2 | Thời gian khởi động nguội (Cold Start) | Đo 10 lần qua `am start -W` | Trung vị $< 2.500\text{ms}$ trên máy ảo |
| **PERF-08** | T2 | Độ mượt cuộn trang Home (`gfxinfo`) | DB nạp sẵn 1.000 notes | Tỷ lệ Janky Frames $< 10\%$ |
| **PERF-09** | T2 | Kiểm tra rò rỉ bộ nhớ (Soak Test) | Mở/đóng Editor 50 lần | Bộ nhớ RSS không tăng lũy tiến không hồi phục |
| **PERF-10** | T3 | Phân tích kích thước file APK | Bản build release | APK kích thước tối ưu $< 45\text{MB}$ |

---

## 5. LỊCH TRÌNH THỰC THI & PHÂN CÔNG
1. **Giai đoạn Setup (Hiện tại)**: Cài đặt Flutter SDK, Node.js, khởi động Android Emulator.
2. **Giai đoạn Thực nghiệm Bảo mật (SEC-01..14)**: Chạy SAST, kiểm thử SQLite & Firestore Rules, trích xuất APK.
3. **Giai đoạn Thực nghiệm Đột biến (MUT-01..60)**: Chạy script tự động tiêm mutant, tính Mutation Score.
4. **Giai đoạn Thực nghiệm Hiệu năng (PERF-01..10)**: Chạy script benchmark T1, đo T2 trên Android Emulator, phân tích APK T3.
5. **Giai đoạn Hoàn thiện Báo cáo**: Đồng bộ số liệu vào `docs/Advanced_Testing_Report.md` và file Word [`bao_cao/baoCao_DgiaKdinhPhmem.docx`](../bao_cao/baoCao_DgiaKdinhPhmem.docx).
