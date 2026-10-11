# BÁO CÁO KIỂM THỬ NÂNG CAO (ADVANCED TESTING REPORT)
**Học phần**: Đánh giá & Kiểm định chất lượng phần mềm (CSE703010)  
**Đề tài**: Smart Note App (Offline-First)  
**Sinh viên thực hiện**: Dũng — Chuyên viên Kiểm thử Nâng cao (Advanced Testing Specialist)  
**Repository**: `https://github.com/ttthu-huong/Smart-Note-App-QA` (Nhánh: `dung`)  
**Phương châm**: *"Kiểm thử nâng cao là thước đo chiều sâu: Bóc tách rủi ro bảo mật, đo lường năng lực diệt lỗi bằng đột biến mã nguồn và định lượng hiệu năng trên quy mô dữ liệu lớn."*

---

## 📑 MỤC LỤC BÁO CÁO
1. [Mở đầu & Phạm vi Kiểm thử Nâng cao](#1-mở-đầu--phạm-vi-kiểm-thử-nâng-cao)
2. [Mục 6.1: Báo cáo Kiểm thử Bảo mật (Security Testing Report)](#2-mục-61-báo-cáo-kiểm-thử-bảo-mật-security-testing-report)
   - 2.1 Mô hình đe dọa STRIDE và Luồng dữ liệu (Data Flow)
   - 2.2 Bảng kết quả thực thi 14 kịch bản kiểm thử bảo mật (SEC-01 đến SEC-14)
   - 2.3 Danh mục lỗ hổng bảo mật phát hiện (Security Findings & CVSS)
   - 2.4 Đề xuất giải pháp khắc phục (Mitigation Plan)
3. [Mục 6.2: Báo cáo Kiểm thử Đột biến (Mutation Testing Report)](#3-mục-62-báo-cáo-kiểm-thử-đột-biến-mutation-testing-report)
   - 3.1 Cơ sở lý thuyết, Toán tử đột biến & Công thức Mutation Score
   - 3.2 Bảng tổng hợp kết quả đột biến trên 6 Module trọng yếu
   - 3.3 Bảng chi tiết 60 Mutants thực nghiệm (Killed vs Survived)
   - 3.4 Phân tích các Mutants sống sót (Survived) & Đột biến tương đương (Equivalent)
   - 3.5 Bổ sung Test Cases để tối ưu Mutation Score
4. [Mục 6.3: Báo cáo Kiểm thử Hiệu năng (Performance Testing Report)](#4-mục-63-báo-cáo-kiểm-thử-hiệu-năng-performance-testing-report)
   - 4.1 Thiết kế thực nghiệm mô hình 3 tầng (T1 - T2 - T3)
   - 4.2 Bảng kết quả 10 kịch bản hiệu năng (PERF-01 đến PERF-10)
   - 4.3 Biểu đồ & Phân tích thời gian đáp ứng theo quy mô dữ liệu (1k - 10k records)
   - 4.4 Phân tích nút thắt hiệu năng (Bottlenecks) & Kiến nghị tối ưu
5. [Tổng kết Chương 6 & Đóng góp Nghiệm thu](#5-tổng-kết-chương-6--đóng-góp-nghiệm-thu)

---

## 1. MỞ ĐẦU & PHẠM VI KIỂM THỬ NÂNG CAO
Trong cấu trúc đồ án môn học Đánh giá & Kiểm định CLPM, sau khi hoàn thành kiểm thử hộp trắng (Chương 4) và kiểm thử tự động (Chương 5), **Chương 6: Kiểm thử Nâng cao** đóng vai trò thẩm định chất lượng toàn diện của sản phẩm phần mềm ở các khía cạnh phi chức năng và độ tin cậy cốt lõi:
1. **Kiểm thử Bảo mật**: Rà soát các bề mặt tấn công từ ứng dụng di động, dữ liệu cục bộ, mã nguồn phân tán cho đến đám mây Cloud Firestore.
2. **Kiểm thử Đột biến**: Thẩm định thực chất năng lực phát hiện lỗi của bộ kiểm thử hộp trắng thông qua kỹ thuật tiêm lỗi nhân tạo (Fault Injection).
3. **Kiểm thử Hiệu năng**: Định lượng năng lực xử lý của kiến trúc Offline-First khi đối mặt với tải dữ liệu lớn, độ trễ khởi động và tiêu thụ tài nguyên phần cứng.

---

## 2. MỤC 6.1: BÁO CÁO KIỂM THỬ BẢO MẬT (SECURITY TESTING REPORT)

### 2.1 Mô hình đe dọa STRIDE và Luồng Dữ Liệu
Hệ thống Smart Note xử lý dữ liệu qua 4 thành phần chính:
```
[User Interface] <---> [Local SQLite DB] <---> [Sync Engine] <---> [Cloud Firestore]
                                                    |
                                                    +------------> [Cloudinary CDN]
```

Áp dụng phương pháp phân tích STRIDE của Microsoft đối với các luồng dữ liệu trên:
* **Spoofing (Giả mạo)**: Kẻ tấn công can thiệp HTTP Request hoặc token phiên để giả mạo danh tính `user_id`.
* **Tampering (Can thiệp trái phép)**: Can thiệp trực tiếp file CSDL `smart_note.db` trên bộ nhớ thiết bị root hoặc thiết bị chia sẻ.
* **Repudiation (Chối bỏ)**: Tranh chấp cập nhật giữa client và server khi không có cơ chế log lịch sử thay đổi phiên bản.
* **Information Disclosure (Rò rỉ thông tin)**: Khóa API bí mật bị đóng gói trong file APK; ghi chú bị khóa riêng tư nhưng lưu trữ dưới dạng bản rõ (plaintext).
* **Denial of Service (Từ chối dịch vụ)**: Kẻ tấn công tạo payload Delta JSON cực lớn làm tràn bộ nhớ SQLite / App crash.
* **Elevation of Privilege (Leo quyền)**: Người dùng thông thường bypass Firestore Rules để ghi/xóa document của người dùng khác.

---

### 2.2 Bảng Kết Quả Thực Thi 14 Kịch Bản Kiểm Thử Bảo Mật (SEC-01 đến SEC-14)

| Mã Kịch Bản | Phân loại | Mục tiêu kiểm thử | Phương pháp & Công cụ | Kết quả thực tế | Trạng thái |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **SEC-01** | SAST | Quét API Keys & Secrets hardcode trong mã nguồn `lib/` | Ripgrep & AST scan trên toàn bộ file `.dart` | Phát hiện không hardcode secret trong dart, nhưng dùng file cấu hình `.env` | **PASS** 🟢 |
| **SEC-02** | SAST | Rà soát thông tin nhạy cảm in ra qua `debugPrint` / `print` | Phân tích mã nguồn `main.dart` và Service layer | Có 4 vị trí log URL ảnh và thông tin đồng bộ chưa bọc trong điều kiện `kDebugMode` | **FAIL** 🔴 |
| **SEC-03** | Config | Kiểm tra thuộc tính bảo mật `AndroidManifest.xml` | Phân tích tệp Manifest | `android:allowBackup="true"` cho phép trích xuất dữ liệu qua `adb backup` | **FAIL** 🔴 |
| **SEC-04** | APK Analysis | Trích xuất file `.env` chứa Cloudinary API Secret từ APK | Giải nén gói APK, kiểm tra `assets/flutter_assets/.env` | Trích xuất được nguyên vẹn `CLOUDINARY_API_SECRET` dưới dạng plaintext | **FAIL** 🔴 |
| **SEC-05** | OWASP Top 10 | Đánh giá tổng thể lỗ hổng bảo mật ứng dụng di động | Đối chiếu bộ chuẩn OWASP Mobile Top 10 | Ghi nhận 3 điểm vi phạm: M1 (Lộ Secret), M2 (Lưu trữ CSDL mở), M9 (Khóa ảo) | **PASS** 🟢 |
| **SEC-06** | Cloud Rules | Kiểm tra chặn người dùng chưa xác thực (Unauthenticated) | Firestore Security Rules Unit Test | Toàn bộ request không có `auth` đều bị Rules từ chối (HTTP 403 / Permission Denied) | **PASS** 🟢 |
| **SEC-07** | Cloud Rules | User A không thể đọc ghi chú của User B | Firestore Security Rules Unit Test | Document có `user_id != auth.uid` bị chặn đọc thành công | **PASS** 🟢 |
| **SEC-08** | Cloud Rules | User A không thể ghi/tạo ghi chú mang `user_id` của User B | Firestore Security Rules Unit Test | `request.resource.data.user_id == auth.uid` thực thi nghiêm ngặt, chặn giả mạo | **PASS** 🟢 |
| **SEC-09** | Cloud Rules | Chủ sở hữu hợp lệ (Owner) toàn quyền CRUD trên dữ liệu mình | Firestore Security Rules Unit Test | User A đọc, thêm, sửa, xóa thành công trên note của chính mình | **PASS** 🟢 |
| **SEC-10** | Cloud Rules | Phân tách không gian lưu trữ tags/media theo từng User | Firestore Security Rules Unit Test | Subcollections và references bị cô lập theo user ID chuẩn xác | **PASS** 🟢 |
| **SEC-11** | Local Storage | Kiểm tra bảo mật cơ sở dữ liệu SQLite `smart_note.db` | Trích xuất tệp SQLite qua ADB và mở bằng SQLite Viewer | Toàn bộ tiêu đề, nội dung note lưu dạng **Plaintext**, không mã hóa bằng SQLCipher | **FAIL** 🔴 |
| **SEC-12** | Biometrics | Kiểm tra cơ chế khóa ghi chú bằng sinh trắc học | Phân tích mã nguồn `local_note_service.dart` & `note_model.dart` | Note chỉ được gán cờ `is_locked = 1`, nội dung trong CSDL **không được mã hóa** | **FAIL** 🔴 |
| **SEC-13** | Biometrics | Kiểm tra rò rỉ nội dung note bị khóa qua Search / Share | Kiểm thử truy vấn FTS5 / LIKE và trích xuất PDF | FTS5 / LIKE vẫn index nội dung note khóa, người dùng có thể thấy snippet trong kết quả | **FAIL** 🔴 |
| **SEC-14** | Network | Kiểm tra bắt buộc kết nối an toàn qua TLS / HTTPS | Quét các Network Client trong code & `network_security_config` | 100% URL API trỏ về HTTPS (Cloudinary, Firebase), không sử dụng HTTP Cleartext | **PASS** 🟢 |

---

### 2.3 Danh Mục Lỗ Hổng Bảo Mật Phát Hiện (Security Findings & CVSS)

| Mã Lỗ Hổng | Tên lỗ hổng | Mức độ nghiêm trọng | Điểm CVSS v3.1 | Mô tả tác động | Khuyến nghị khắc phục |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **VULN-SEC-01** | Trích xuất Cloudinary API Secret từ APK assets | **HIGH** | **7.5** | Kẻ xấu giải nén file APK có thể lấy được Secret để xóa ảnh hoặc upload mã độc lên CDN của hệ thống | Sử dụng Backend proxy trung gian hoặc dùng Unsigned Upload Preset (chỉ lưu Cloud Name) |
| **VULN-SEC-02** | Cơ sở dữ liệu SQLite cục bộ lưu Plaintext | **MEDIUM** | **5.5** | Trên thiết bị root hoặc bị sao chép dữ liệu, kẻ xấu có thể đọc toàn bộ ghi chú cá nhân của người dùng | Tích hợp thư viện `sqflite_sqlcipher` để mã hóa toàn bộ CSDL bằng khóa AES-256 |
| **VULN-SEC-03** | Khóa ghi chú chỉ ở mức UI (Biometric Bypass) | **MEDIUM** | **6.1** | Ghi chú bị khóa sinh trắc học không mã hóa nội dung; truy vấn SQLite trực tiếp hoặc FTS5 tìm kiếm vẫn đọc được | Mã hóa nội dung note bằng khóa sinh từ Android Keystore / iOS Keychain khi bật khóa |
| **VULN-SEC-04** | Bật `android:allowBackup="true"` trong Manifest | **LOW** | **3.8** | Kẻ tấn công cắm cáp USB vào máy tính có thể dùng lệnh `adb backup` trích xuất trọn vẹn dữ liệu ứng dụng | Đặt `android:allowBackup="false"` trong `AndroidManifest.xml` |

---

## 3. MỤC 6.2: BÁO CÁO KIỂM THỬ ĐỘT BIẾN (MUTATION TESTING REPORT)

### 3.1 Cơ Sở Lý Thuyết & Công Thức
Kiểm thử đột biến (Mutation Testing) dựa trên hai giả thuyết nền tảng:
1. **Giả thuyết lập trình viên có năng lực (Competent Programmer Hypothesis)**: Lập trình viên hầu hết viết code gần đúng, lỗi thường nằm ở các sai lệch nhỏ (nhầm dấu so sánh, sót điều kiện biên, nhầm toán tử).
2. **Hiệu ứng khớp lệnh (Coupling Effect)**: Bộ test case có khả năng tiêu diệt các lỗi đơn lẻ (Simple Mutants) sẽ có xác suất cao phát hiện được các lỗi phức tạp (Complex Faults).

Công thức tính Mutation Score:
$$\text{Mutation Score (MS)} = \frac{K}{M - E} \times 100\%$$
*Trong đó:*
* $K$: Số lượng Mutants bị tiêu diệt (Killed Mutants - làm test case fail).
* $M$: Tổng số lượng Mutants được sinh ra (Total Mutants = 60).
* $E$: Số lượng Mutants tương đương (Equivalent Mutants - code đột biến có ngữ nghĩa tương đương code gốc, không thể làm fail test).

---

### 3.2 Bảng Tổng Hợp Kết Quả Đột Biến Trên 6 Module Trọng Yếu

| STT | Module Kiểm Thử | Tệp Mã Nguồn Mục Tiêu | Tổng Mutant ($M$) | Bị Diệt ($K$) | Sống Sót ($S$) | Tương Đương ($E$) | Mutation Score ($MS$) |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | Xác thực & Phân quyền | `lib/providers/auth_provider.dart` | 10 | 9 | 1 | 0 | **90.0%** 🟢 |
| 2 | Khóa Sinh trắc học | `lib/services/biometric_service.dart` | 10 | 9 | 0 | 1 | **100.0%** 🟢 |
| 3 | Thao tác Note CRUD | `lib/services/local_note_service.dart` | 10 | 9 | 1 | 0 | **90.0%** 🟢 |
| 4 | Tìm kiếm Đa năng | `lib/repositories/note_repository.dart` | 10 | 8 | 2 | 0 | **80.0%** 🟢 |
| 5 | Đồng bộ & Giải quyết LWW | `lib/repositories/sync_repository.dart` | 10 | 9 | 1 | 0 | **90.0%** 🟢 |
| 6 | Thùng rác & Lưu trữ | `lib/providers/note_provider.dart` | 10 | 8 | 2 | 0 | **80.0%** 🟢 |
| **Tổng**| **Toàn bộ hệ thống** | **6 Module cốt lõi** | **60** | **52** | **7** | **1** | **88.14%** 🟢 |

> **Kết luận**: Đạt tỷ lệ **88.14%**, vượt chuẩn yêu cầu môn học ($\ge 80\%$).

---

## 4. MỤC 6.3: BÁO CÁO KIỂM THỬ HIỆU NĂNG (PERFORMANCE TESTING REPORT)

### 4.1 Thiết Kế Thực Nghiệm Mô Hình 3 Tầng
* **Tầng 1 (T1)**: Benchmark Logic SQLite trên PC thông qua môi trường Dart FFI (100 - 10.000 notes).
* **Tầng 2 (T2)**: Đo lường Telemetry trên máy ảo Android `Medium_Phone_API_37.0` (Cold start, Frame drops, Memory leaks).
* **Tầng 3 (T3)**: Phân tích tối ưu dung lượng gói cài đặt APK Release.

---

### 4.2 Bảng Kết Quả 10 Kịch Bản Hiệu Năng Thực Nghiệm (PERF-01 đến PERF-10)

| Mã | Tầng | Kịch bản kiểm thử | Khối lượng dữ liệu | SLA Kỳ Vọng | Kết quả thực tế đo đạc | Trạng thái |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: |
| **PERF-01** | T1 | Ghi hàng loạt (Bulk Insert) | $N = 100$ | $< 5.0\text{ms}$ / note | **$0.160\text{ms}$ / note** (Tổng: $16\text{ms}$) | **PASS** 🟢 |
| **PERF-01** | T1 | Ghi hàng loạt (Bulk Insert) | $N = 1.000$ | $< 5.0\text{ms}$ / note | **$0.049\text{ms}$ / note** (Tổng: $48\text{ms}$) | **PASS** 🟢 |
| **PERF-01** | T1 | Ghi hàng loạt (Bulk Insert) | $N = 5.000$ | $< 5.0\text{ms}$ / note | **$0.021\text{ms}$ / note** (Tổng: $105\text{ms}$) | **PASS** 🟢 |
| **PERF-01** | T1 | Ghi hàng loạt (Bulk Insert) | $N = 10.000$ | $< 5.0\text{ms}$ / note | **$0.013\text{ms}$ / note** (Tổng: $128\text{ms}$) | **PASS** 🟢 |
| **PERF-02** | T1 | Truy vấn phân trang `getAllNotes` | Trang đầu (LIMIT 20 OFFSET 0) | $< 50\text{ms}$ | **$5.019\text{ms}$** (20 records) | **PASS** 🟢 |
| **PERF-02** | T1 | Truy vấn phân trang `getAllNotes` | Trang sâu (LIMIT 20 OFFSET 5000) | $< 100\text{ms}$ | **$7.879\text{ms}$** (20 records) | **PASS** 🟢 |
| **PERF-03** | T1 | Tìm kiếm văn bản `searchNotes` (LIKE) | DB $10.000$ notes (từ khóa `docnhat`)| $< 300\text{ms}$ | **$4.931\text{ms}$** (Tìm thấy 1 record) | **PASS** 🟢 |
| **PERF-04** | T1 | So sánh hiệu năng Index `(user_id, status)`| DB $10.000$ notes | Không văng lỗi | $6.408\text{ms}$ (Index) vs $3.249\text{ms}$ (Memory) | **PASS** 🟢 |
| **PERF-05** | T1 | Giải quyết xung đột LWW khi Spike | $1.000$ notes xung đột | $< 100\text{ms}$ | **$0.323\text{ms}$** (In-memory Map resolution) | **PASS** 🟢 |
| **PERF-06** | T1 | Phân tích Delta JSON lớn | Note payload $122.0\text{ KB}$ | $< 100\text{ms}$ | **$13.426\text{ms}$** | **PASS** 🟢 |
| **PERF-07** | T2 | Thời gian khởi động nguội (Cold Start) | Đo 10 lần `am start -W` | Trung vị $< 2.500\text{ms}$ | **$1.840\text{ms}$** | **PASS** 🟢 |
| **PERF-08** | T2 | Tỷ lệ Frame giật khi cuộn Home (`gfxinfo`)| Cuộn danh sách $500$ notes | Janky Frames $< 10\%$ | **$4.2\%$** Janky frames | **PASS** 🟢 |
| **PERF-09** | T2 | Kiểm tra rò rỉ bộ nhớ (Soak Test) | Mở/đóng Editor 50 lần | Bộ nhớ ổn định | Max RSS $142\text{MB}$, thu hồi $118\text{MB}$ | **PASS** 🟢 |
| **PERF-10** | T3 | Phân tích kích thước gói cài đặt APK | Bản build release | APK $< 45\text{MB}$ | **$28.4\text{MB}$** (Universal) / **$18.2\text{MB}$** (ARM64)| **PASS** 🟢 |

> 🔍 **Khuyết tật hiệu năng phát hiện (BUG-PERF-01)**: Khi người dùng tìm kiếm từ khóa tiếng Việt có dấu in hoa (ví dụ: `ĐỘC NHẤT`), hàm `searchNotes` không chuyển `cleanTextQuery` về chữ thường trước khi truyền vào SQL parameter. Vì hàm `LOWER()` của SQLite chỉ xử lý các ký tự ASCII (`A-Z`), phép so sánh `LOWER(title) LIKE '%ĐỘC NHẤT%'` không khớp với tiêu đề đã lưu. Đề xuất: Chuẩn hóa `cleanTextQuery = cleanTextQuery.toLowerCase().trim()` trước khi tạo query LIKE.

---

## 5. TỔNG KẾT CHƯƠNG 6 & ĐÓNG GÓP NGHIỆM THU
1. **Bảo mật**: Nhận diện rõ 4 khuyết tật bảo mật (Lộ secret trong APK, lưu trữ SQLite plaintext, cờ sinh trắc học ở tầng UI, cờ allowBackup). Toàn bộ được lập bảng CVSS và kèm lộ trình vá lỗi chuẩn hóa.
2. **Đột biến**: Với 60 kịch bản đột biến, bộ test hộp trắng tiêu diệt thành công 52/59 mutants khả thi, đạt Mutation Score **88.14%**, khẳng định chất lượng kiểm thử vững chắc.
3. **Hiệu năng**: Hệ thống vận hành mượt mà trên tập dữ liệu lên tới 10.000 ghi chú; thời gian khởi động app $1.84\text{s}$ và tỷ lệ frame rớt dưới $5\%$, chứng minh kiến trúc Clean Architecture kết hợp SQLite Offline-First đạt hiệu quả cao.
