# BẢNG THỰC THI KIỂM THỬ HỘP ĐEN (BLACK-BOX TEST EXECUTION SHEET)
## CHỨC NĂNG: ĐĂNG KÝ TÀI KHOẢN EMAIL/PASSWORD (FN-02)

- **Dự án:** Smart Note App
- **Chức năng kiểm thử:** FN-02 — Đăng ký tài khoản Email
- **Phương pháp kiểm thử:** Kiểm thử hộp đen toàn diện (Comprehensive Black-box Testing)
- **Tài liệu tham chiếu thiết kế:** `black_box_test_cases.md`
- **Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Certified Tester Foundation Level (CTFL)
- **Mục tiêu tài liệu:** Cung cấp biểu mẫu thực thi chi tiết, rõ ràng từng bước bao phủ đầy đủ luồng chuẩn (Happy Path), các ca biên (BVA), các phân lớp tương đương (Equivalence Partitioning), kiểm tra tính bền vững của bộ lọc tên miền (Robustness / Code-inferred Domain Filter), xử lý ngoại lệ môi trường mạng (Network Offline) và tính toàn vẹn trạng thái giao diện người dùng (UI Usability & State Integrity).

---

## 1. THÔNG TIN PHIÊN KIỂM THỬ (TEST SESSION INFORMATION)

| Mục thông tin | Chi tiết ghi nhận thực tế |
|---|---|
| **Mã chức năng (FN-ID)** | **FN-02** |
| **Tên chức năng** | **Đăng ký tài khoản Email/Password** |
| **Người thực hiện kiểm thử (Tester)** | Huong (QA Tester) |
| **Ngày thực hiện kiểm thử** | 05/10/2026 |
| **Thiết bị / Máy ảo kiểm thử** | Samsung Galaxy S21 FE 5G (SM-G990B / R5CW82ECF6M) |
| **Hệ điều hành / Phiên bản Android** | Android 14 (API 34) |
| **Phiên bản ứng dụng (App Version / Build)** | v1.0.0 (Release Build) |
| **Loại kết nối mạng** | Wi-Fi (Tốc độ cao) & Chế độ Offline mô phỏng |
| **Ghi chú môi trường kiểm thử khác** | Độ phân giải 1080x2340, uiautomator2 + ADB kết nối ổn định |

---

## 2. ĐIỀU KIỆN CHUẨN BỊ TRƯỚC KHI THỰC HIỆN (PRECONDITIONS)

Trước khi bắt đầu thực hiện bất kỳ ca kiểm thử nào thuộc chức năng FN-02, Tester cần chuẩn bị đầy đủ các điều kiện tiên quyết sau:

1. **Ứng dụng đã sẵn sàng:** Ứng dụng Smart Note App đã được cài đặt hoàn tất trên thiết bị, mở được và hoạt động ổn định.
2. **Trạng thái đăng nhập:** Ứng dụng phải ở trạng thái **chưa đăng nhập tài khoản**. Nếu ứng dụng đang mở sẵn ở màn hình Trang chủ ghi chú, Tester phải thực hiện thao tác **Đăng xuất** để đưa ứng dụng quay về màn hình Đăng nhập ban đầu.
3. **Màn hình bắt đầu kiểm thử:** Tại màn hình Đăng nhập, Tester chạm vào dòng chữ **"Đăng ký ngay"** ở phía dưới để chuyển giao diện sang chế độ **Đăng ký** (tiêu đề *"Tạo tài khoản mới"*, nút bấm màu xanh hiển thị chữ **"Đăng ký"**, có 2 ô nhập: "Email" và "Mật khẩu").
4. **Kết nối mạng Internet:** Thiết bị có kết nối mạng Internet hoạt động bình thường (ngoại trừ ca kiểm thử ngoại tuyến TC-BB-002F yêu cầu ngắt kết nối mạng).
5. **Dữ liệu kiểm thử đã chuẩn bị:**
   - Email mới hoàn toàn chưa từng đăng ký: Dùng cấu trúc `student_qa_<thời_gian>@gmail.com` hoặc `student_bva_<thời_gian>@gmail.com`.
   - Email đã tồn tại sẵn trên hệ thống: Sử dụng tài khoản mẫu `student_qa@gmail.com` đã tạo trước đó để thực hiện ca kiểm thử trùng lặp.
   - Email tên miền rác: Dùng tên miền thuộc danh sách đen như `@tempmail.com`, `@mailinator.com`.

---

## 3. BẢNG THỰC THI KIỂM THỬ TỔNG HỢP (TEST EXECUTION MATRIX)

> **Hướng dẫn cho Tester:**  
> - Bảng gồm đúng **13 Test Cases** với trọn vẹn **19 Execution Items** (STT 1 đến STT 19).
> - Làm theo đúng các bước tại cột **Các bước thực hiện (Steps)** và nhập chính xác dữ liệu tại cột **Test Data**.
> - Quan sát giao diện thực tế và ghi nhận vào cột **Actual Result** (chỉ ghi nhận hành vi observable trên UI).
> - So sánh giữa **Actual Result** và **Expected Result**: Nếu trùng khớp ghi **PASS**, nếu sai lệch ghi **FAIL**, nếu bị chặn do mạng/môi trường ghi **BLOCKED**.

| STT | TC-ID | Data ID | Phân loại | Test Data | Các bước thực hiện (Steps) | Expected Result (Observable UI) | Actual Result | Trạng thái | Evidence ID | Bug ID |
|:---:|:---:|:---:|:---:|:---|:---|:---|:---|:---:|:---|:---:|
| **1** | **TC-BB-001** | **D01** | Đã có | • Email: `student_qa_20261004_01@gmail.com`<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng ký.<br>2. Nhập Email Gmail mới vào ô Email.<br>3. Nhập Mật khẩu `123456`.<br>4. Nhấn nút "Đăng ký". | Đăng ký thành công, chuyển sang màn hình Xác thực Email (`EmailVerificationScreen`) hiển thị hướng dẫn kiểm tra email. | Đăng ký thành công, chuyển sang màn hình "Xác thực email của bạn", hiển thị email vừa đăng ký. | **PASS** | `FN02_TC-BB-001_D01_01.png` | — |
| **2** | **TC-BB-001** | **D02** | Đã có | • Email: `user_dev_20261004_02@outlook.com`<br>• Mật khẩu: `Abc@2026!` | 1. Đang ở tab Đăng ký.<br>2. Nhập Email Outlook mới.<br>3. Nhập Mật khẩu phức tạp `Abc@2026!`.<br>4. Nhấn nút "Đăng ký". | Đăng ký thành công, chuyển sang màn hình Xác thực Email. | Đăng ký thành công, chuyển sang màn hình "Xác thực email của bạn". | **PASS** | `FN02_TC-BB-001_D02_01.png` | — |
| **3** | **TC-BB-001** | **D03** | Đã có | • Email: `sv_20261004_03@hcmus.edu.vn`<br>• Mật khẩu: `MatKhauDai123` | 1. Đang ở tab Đăng ký.<br>2. Nhập Email giáo dục mới.<br>3. Nhập Mật khẩu `MatKhauDai123`.<br>4. Nhấn nút "Đăng ký". | Đăng ký thành công, chuyển sang màn hình Xác thực Email. | Đăng ký thành công, chuyển sang màn hình "Xác thực email của bạn". | **PASS** | `FN02_TC-BB-001_D03_01.png` | — |
| **4** | **TC-BB-001B** | **D01** | Mới đề xuất | • Email: `"  student_trim_01@gmail.com  "`<br>*(có khoảng trắng đầu và cuối)*<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng ký.<br>2. Nhập/Paste Email có khoảng trắng thừa ở đầu và cuối.<br>3. Nhập Mật khẩu hợp lệ.<br>4. Nhấn "Đăng ký". | Hệ thống tự động cắt bỏ khoảng trắng thừa đầu/cuối, chấp nhận email và chuyển sang màn hình Xác thực Email với địa chỉ đã cắt tỉa. | Hệ thống tự động trim khoảng trắng, đăng ký thành công và hiển thị màn hình Xác thực Email với địa chỉ `student_trim_01@gmail.com`. | **PASS** | `FN02_TC-BB-001B_D01_01.png` | — |
| **5** | **TC-BB-002** | **D01** | Đã có | • Email: `""`<br>• Mật khẩu: `""`<br>*(bỏ trống cả 2 ô)* | 1. Đang ở tab Đăng ký.<br>2. Để trống hoàn toàn ô Email và Mật khẩu.<br>3. Nhấn nút "Đăng ký". | Ứng dụng không chuyển màn hình; xuất hiện khung thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Ứng dụng không chuyển màn hình; xuất hiện khung thông báo lỗi đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | **PASS** | `FN02_TC-BB-002_D01_01.png` | — |
| **6** | **TC-BB-002B** | **D01** | Mới đề xuất | • Email: `student_valid_01@gmail.com`<br>• Mật khẩu: `""`<br>*(chỉ nhập email, để trống mật khẩu)* | 1. Đang ở tab Đăng ký.<br>2. Nhập Email hợp lệ.<br>3. Để trống ô Mật khẩu.<br>4. Nhấn "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Ứng dụng không chuyển màn hình; hiển thị chính xác thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | **PASS** | `FN02_TC-BB-002B_D01_01.png` | — |
| **7** | **TC-BB-002C** | **D01** | Mới đề xuất | • Email: `""`<br>• Mật khẩu: `123456`<br>*(để trống email, chỉ nhập mật khẩu)* | 1. Đang ở tab Đăng ký.<br>2. Để trống ô Email.<br>3. Nhập Mật khẩu hợp lệ.<br>4. Nhấn "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Ứng dụng không chuyển màn hình; hiển thị chính xác thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | **PASS** | `FN02_TC-BB-002C_D01_01.png` | — |
| **8** | **TC-BB-002D** | **D01** | Mới đề xuất | • Mật khẩu: `MySecurePass123!` | 1. Đang ở tab Đăng ký.<br>2. Nhập mật khẩu vào ô Mật khẩu (quan sát dạng che `••••••••••`).<br>3. Chạm vào icon con mắt bên phải ô mật khẩu.<br>4. Quan sát hiển thị.<br>5. Chạm lại icon con mắt lần 2. | Chạm lần 1: Ký tự mật khẩu chuyển sang hiển thị văn bản rõ `MySecurePass123!`.<br>Chạm lần 2: Ký tự mật khẩu chuyển về dạng ẩn che giấu `••••••••••`. | Mật khẩu chuyển đổi chính xác giữa chế độ hiển thị rõ và chế độ ẩn che giấu theo tương tác chạm. | **PASS** | `FN02_TC-BB-002D_D01_01.png` | — |
| **9** | **TC-BB-002E** | **D01** | Mới đề xuất | Form đang có thông báo lỗi đỏ từ lượt thao tác trước | 1. Tại tab Đăng ký, nhấn "Đăng ký" khi để trống để xuất hiện khung lỗi đỏ.<br>2. Chạm vào dòng chữ "Đăng nhập" ở dưới cùng để sang tab Đăng nhập.<br>3. Chạm vào dòng chữ "Đăng ký ngay" để quay lại tab Đăng ký. | Màn hình chuyển đổi mượt mà giữa hai tab; khi quay lại tab Đăng ký, khung thông báo lỗi màu đỏ của lần trước biến mất hoàn toàn, form trở về trạng thái sạch ban đầu. | Màn hình chuyển đổi chính xác giữa 2 tab; khung lỗi đỏ cũ được dọn dẹp hoàn toàn khi quay lại tab Đăng ký. | **PASS** | `FN02_TC-BB-002E_D01_01.png` | — |
| **10** | **TC-BB-002F** | **D01** | Mới đề xuất | • Thiết bị ngắt toàn bộ kết nối mạng (Offline)<br>• Email: `valid_offline@gmail.com`<br>• Mật khẩu: `123456` | 1. Tắt Wi-Fi và Dữ liệu di động trên thiết bị.<br>2. Đang ở tab Đăng ký.<br>3. Nhập Email hợp lệ và Mật khẩu hợp lệ.<br>4. Nhấn nút "Đăng ký". | Ứng dụng không chuyển sang màn hình Xác thực Email; vẫn giữ nguyên màn hình Đăng ký, xuất hiện thông báo lỗi màu đỏ: *"Không có kết nối mạng. Vui lòng kiểm tra lại."*; dữ liệu vừa nhập vẫn được giữ an toàn trên ô nhập liệu. | Ứng dụng phát hiện ngoại tuyến ngay tại giao diện, không chuyển màn hình, hiển thị đúng thông báo: *"Không có kết nối mạng. Vui lòng kiểm tra lại."* | **PASS** | `FN02_TC-BB-002F_D01_01.png` | — |
| **11** | **TC-BB-003** | **D01** | Đã có | • Email: `nguoidung_gmail.com`<br>*(thiếu ký tự @)*<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng ký.<br>2. Nhập Email thiếu ký tự `@`.<br>3. Nhập Mật khẩu hợp lệ.<br>4. Nhấn "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."* | Không chuyển màn hình; hiển thị thông báo sai: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* | **FAIL** | `FN02_TC-BB-003_D01_01.png` | `BUG-FN02-01` |
| **12** | **TC-BB-003** | **D02** | Đã có | • Email: `nguoidung@`<br>*(thiếu tên miền)*<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng ký.<br>2. Nhập Email có `@` nhưng không có domain phía sau.<br>3. Nhấn "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."* | Không chuyển màn hình; hiển thị đúng thông báo lỗi: *"Định dạng email không hợp lệ."* | **PASS** | `FN02_TC-BB-003_D02_01.png` | — |
| **13** | **TC-BB-003B** | **D01** | Mới đề xuất | • Email: `test_user_01@tempmail.com`<br>*(thuộc danh sách đen tên miền rác)*<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng ký.<br>2. Nhập Email có định dạng chuẩn nhưng tên miền thuộc blacklist (`tempmail.com`).<br>3. Nhấn "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* | Ứng dụng chặn đăng ký, hiển thị đúng thông báo lỗi: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* | **PASS** | `FN02_TC-BB-003B_D01_01.png` | — |
| **14** | **TC-BB-004** | **D01** | Đã có | • Email: `student_bva_01@gmail.com`<br>• Mật khẩu: `1` *(1 ký tự số - cực tiểu)* | 1. Đang ở tab Đăng ký.<br>2. Nhập Email hợp lệ.<br>3. Nhập Mật khẩu 1 ký tự (`1`).<br>4. Nhấn "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."* | Không chuyển màn hình; hiển thị đúng thông báo lỗi: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."* | **PASS** | `FN02_TC-BB-004_D01_01.png` | — |
| **15** | **TC-BB-004** | **D02** | Đã có | • Email: `student_bva_01@gmail.com`<br>• Mật khẩu: `12345` *(5 ký tự số - biên N-1)* | 1. Đang ở tab Đăng ký.<br>2. Nhập Email hợp lệ.<br>3. Nhập Mật khẩu 5 ký tự (`12345`).<br>4. Nhấn "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."* | Không chuyển màn hình; hiển thị đúng thông báo lỗi: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."* | **PASS** | `FN02_TC-BB-004_D02_01.png` | — |
| **16** | **TC-BB-004B** | **D01** | Mới đề xuất | • Email: `student_bva_min6@gmail.com`<br>• Mật khẩu: `123456` *(đúng 6 ký tự - điểm biên N)* | 1. Đang ở tab Đăng ký.<br>2. Nhập Email hợp lệ chưa từng đăng ký.<br>3. Nhập Mật khẩu đúng 6 ký tự (`123456`).<br>4. Nhấn "Đăng ký". | Đăng ký thành công, mật khẩu 6 ký tự được chấp nhận; chuyển sang màn hình Xác thực Email. | Đăng ký thành công, ứng dụng chuyển sang màn hình "Xác thực email của bạn". | **PASS** | `FN02_TC-BB-004B_D01_01.png` | — |
| **17** | **TC-BB-004B** | **D02** | Mới đề xuất | • Email: `student_bva_7char@gmail.com`<br>• Mật khẩu: `1234567` *(7 ký tự - điểm biên N+1)* | 1. Đang ở tab Đăng ký.<br>2. Nhập Email hợp lệ mới.<br>3. Nhập Mật khẩu 7 ký tự (`1234567`).<br>4. Nhấn "Đăng ký". | Đăng ký thành công, mật khẩu 7 ký tự được chấp nhận; chuyển sang màn hình Xác thực Email. | Đăng ký thành công, ứng dụng chuyển sang màn hình "Xác thực email của bạn". | **PASS** | `FN02_TC-BB-004B_D02_01.png` | — |
| **18** | **TC-BB-005** | **D01** | Đã có | • Email: `student_qa@gmail.com`<br>*(email chữ thường đã đăng ký)*<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng ký.<br>2. Nhập Email đã tồn tại `student_qa@gmail.com`.<br>3. Nhập Mật khẩu hợp lệ `123456`.<br>4. Nhấn "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Email này đã được sử dụng cho một tài khoản khác."* | Không chuyển màn hình; hiển thị chính xác thông báo lỗi màu đỏ: *"Email này đã được sử dụng cho một tài khoản khác."* | **PASS** | `FN02_TC-BB-005_D01_01.png` | — |
| **19** | **TC-BB-005** | **D02** | Mới đề xuất | • Email: `STUDENT_QA@GMAIL.COM`<br>*(email chữ IN HOA của tài khoản đã có)*<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng ký.<br>2. Nhập Email dạng chữ IN HOA của tài khoản đã tồn tại.<br>3. Nhập Mật khẩu hợp lệ.<br>4. Nhấn "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Email này đã được sử dụng cho một tài khoản khác."* (Xác nhận tính năng không phân biệt hoa/thường - Case-insensitive). | Firebase chuẩn hóa chữ thường và phát hiện trùng lặp; giao diện hiển thị đúng khung lỗi đỏ: *"Email này đã được sử dụng cho một tài khoản khác."* | **PASS** | `FN02_TC-BB-005_D02_01.png` | — |

---

## 4. HƯỚNG DẪN CHI TIẾT TỪNG TEST CASE (DETAILED TEST EXECUTION CARDS)

### 4.1. Phiếu thực thi TC-BB-001 (Đăng ký thành công với thông tin hợp lệ)
- **Mã TC:** `TC-BB-001`
- **Mục tiêu:** Xác minh luồng đăng ký tài khoản thành công khi nhập đầy đủ Email mới và Mật khẩu hợp lệ.
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng ký; thiết bị có kết nối mạng Internet.
- **Dữ liệu kiểm thử:** D01 (`student_qa_<ts>@gmail.com`), D02 (`user_dev_<ts>@outlook.com`), D03 (`sv_<ts>@hcmus.edu.vn`).
- **Kỳ vọng quan sát được:** Điều hướng sang `EmailVerificationScreen`, tiêu đề hiển thị "Xác thực email của bạn".
- **Kết quả:** **PASS** (Cả 3 biến thể).

### 4.2. Phiếu thực thi TC-BB-001B (Khoảng trắng đầu/cuối của Email - Whitespace Trimming)
- **Mã TC:** `TC-BB-001B`
- **Mục tiêu:** Xác minh tính năng tự động loại bỏ khoảng trắng thừa đầu và cuối chuỗi Email khi người dùng nhập hoặc dán nội dung.
- **Tiền điều kiện:** Ứng dụng ở màn hình Đăng ký; kết nối mạng ổn định.
- **Các bước:** Nhập chuỗi `"   student_trim_<ts>@gmail.com   "` và Mật khẩu `123456`, nhấn "Đăng ký".
- **Kỳ vọng quan sát được:** Hệ thống tự động cắt tỉa khoảng trắng (`trim()`), chấp nhận email và chuyển sang màn hình Xác thực Email với địa chỉ đã cắt tỉa `student_trim_<ts>@gmail.com`.
- **Kết quả:** **PASS**.

### 4.3. Phiếu thực thi TC-BB-002 (Bỏ trống cả 2 ô Email và Mật khẩu)
- **Mã TC:** `TC-BB-002`
- **Mục tiêu:** Xác minh hệ thống chặn đăng ký khi người dùng không nhập bất kỳ thông tin nào.
- **Tiền điều kiện:** Đang ở màn hình Đăng ký.
- **Các bước:** Để trống cả 2 ô, nhấn "Đăng ký".
- **Kỳ vọng quan sát được:** Không chuyển màn hình; xuất hiện khung thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."*
- **Kết quả:** **PASS**.

### 4.4. Phiếu thực thi TC-BB-002B (Chỉ nhập Email, để trống Mật khẩu)
- **Mã TC:** `TC-BB-002B`
- **Mục tiêu:** Xác minh hệ thống chặn đăng ký khi bỏ trống trường Mật khẩu đơn lẻ.
- **Tiền điều kiện:** Đang ở màn hình Đăng ký.
- **Các bước:** Nhập Email hợp lệ, để trống Mật khẩu, nhấn "Đăng ký".
- **Kỳ vọng quan sát được:** Không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."*
- **Kết quả:** **PASS**.

### 4.5. Phiếu thực thi TC-BB-002C (Chỉ nhập Mật khẩu, để trống Email)
- **Mã TC:** `TC-BB-002C`
- **Mục tiêu:** Xác minh hệ thống chặn đăng ký khi bỏ trống trường Email đơn lẻ.
- **Tiền điều kiện:** Đang ở màn hình Đăng ký.
- **Các bước:** Để trống Email, nhập Mật khẩu hợp lệ, nhấn "Đăng ký".
- **Kỳ vọng quan sát được:** Không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."*
- **Kết quả:** **PASS**.

### 4.6. Phiếu thực thi TC-BB-002D (Tính năng Ẩn/Hiện mật khẩu qua icon con mắt)
- **Mã TC:** `TC-BB-002D`
- **Mục tiêu:** Xác minh hoạt động của icon con mắt cho phép chuyển đổi giữa hiển thị mật khẩu dạng ẩn và văn bản rõ.
- **Tiền điều kiện:** Đang ở màn hình Đăng ký.
- **Các bước:** Nhập mật khẩu, bấm icon con mắt lần 1, quan sát; bấm lại icon con mắt lần 2, quan sát.
- **Kỳ vọng quan sát được:** Chạm lần 1: Ký tự mật khẩu chuyển sang dạng văn bản đọc được rõ; Chạm lần 2: Ký tự mật khẩu quay trở về dạng ẩn che giấu chấm tròn `••••••`.
- **Kết quả:** **PASS**.

### 4.7. Phiếu thực thi TC-BB-002E (Chuyển đổi Tab Đăng ký <-> Đăng nhập và Reset trạng thái lỗi)
- **Mã TC:** `TC-BB-002E`
- **Mục tiêu:** Xác minh việc chuyển đổi tab dọn dẹp sạch thông báo lỗi cũ của phiên trước trên giao diện.
- **Tiền điều kiện:** Màn hình Đăng ký đang hiển thị một khung thông báo lỗi đỏ từ lần bấm nút trước.
- **Các bước:** Chạm "Đăng nhập" ở dòng dưới cùng -> Chuyển sang màn hình Đăng nhập -> Chạm "Đăng ký ngay" để quay lại Đăng ký.
- **Kỳ vọng quan sát được:** Màn hình chuyển đổi mượt mà giữa hai tab; khi quay lại tab Đăng ký, khung thông báo lỗi màu đỏ của lần trước biến mất hoàn toàn, form trở về trạng thái sạch ban đầu.
- **Ghi chú kỹ thuật:** Trong mã nguồn `login_screen.dart`, sự kiện `onTap` của GestureDetector gọi `auth.setError(null)` để làm sạch state lỗi.
- **Kết quả:** **PASS**.

### 4.8. Phiếu thực thi TC-BB-002F (Xử lý khi thiết bị mất kết nối mạng - Network Offline)
- **Mã TC:** `TC-BB-002F`
- **Mục tiêu:** Xác minh phản hồi giao diện của ứng dụng khi người dùng cố gắng đăng ký trong điều kiện ngoại tuyến.
- **Tiền điều kiện:** Thiết bị ngắt toàn bộ kết nối mạng (tắt Wi-Fi và Dữ liệu di động).
- **Các bước:** Nhập Email hợp lệ và Mật khẩu hợp lệ, nhấn nút "Đăng ký".
- **Kỳ vọng quan sát được:** Ứng dụng không chuyển sang màn hình Xác thực Email; vẫn giữ nguyên màn hình Đăng ký, xuất hiện thông báo lỗi màu đỏ: *"Không có kết nối mạng. Vui lòng kiểm tra lại."*; dữ liệu vừa nhập vẫn được giữ an toàn trên ô nhập liệu.
- **Ghi chú kỹ thuật:** `login_screen.dart` sử dụng `ConnectivityHelper().isOnline()` kiểm tra mạng trước khi gọi Firebase.
- **Kết quả:** **PASS**.

### 4.9. Phiếu thực thi TC-BB-003 (Định dạng Email không hợp lệ)
- **Mã TC:** `TC-BB-003`
- **Mục tiêu:** Xác minh ứng dụng từ chối các email sai cú pháp chuẩn (thiếu `@`, thiếu tên miền).
- **Tiền điều kiện:** Đang ở màn hình Đăng ký.
- **Dữ liệu:** D01 (`nguoidung_gmail.com`), D02 (`nguoidung@`).
- **Kỳ vọng quan sát được:** Không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."*
- **Kết quả:** **FAIL (D01 do BUG-FN02-01)**, **PASS (D02)**.

### 4.10. Phiếu thực thi TC-BB-003B (Kiểm tra bộ lọc tên miền rác - Disposable Email Filter)
- **Mã TC:** `TC-BB-003B`
- **Mục tiêu:** Xác minh hành vi thực tế của ứng dụng khi chặn đăng ký các email thuộc tên miền dùng một lần (`tempmail.com`, `mailinator.com`, v.v.).
- **Tiền điều kiện:** Đang ở màn hình Đăng ký; có mạng Internet.
- **Phân loại nguồn gốc:** **Quy tắc nghiệp vụ suy diễn từ mã nguồn thực tế (Code-inferred Business Rule / Robustness Validation)**. Tài liệu đặc tả yêu cầu chính thức không ghi nhận danh sách đen domain, nhưng mã nguồn `auth_provider.dart` chủ động cài đặt hàm `_isValidDomain(email)` để chặn 21 tên miền email rác. Ca kiểm thử này xác minh hành vi thực tế (As-built behavior) và độ bền của bộ lọc.
- **Các bước:** Nhập email có định dạng chuẩn nhưng tên miền thuộc blacklist (`test_user_01@tempmail.com`) và mật khẩu hợp lệ, nhấn "Đăng ký".
- **Kỳ vọng quan sát được:** Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."*
- **Kết quả:** **PASS**.

### 4.11. Phiếu thực thi TC-BB-004 (Độ dài Mật khẩu dưới 6 ký tự - Biên lỗi N-1 và cực tiểu)
- **Mã TC:** `TC-BB-004`
- **Mục tiêu:** Xác minh ứng dụng từ chối mật khẩu có độ dài dưới 6 ký tự (kiểm tra điểm biên dưới không hợp lệ $N-1=5$ và cực tiểu 1 ký tự).
- **Tiền điều kiện:** Đang ở màn hình Đăng ký.
- **Dữ liệu:** D01 (1 ký tự `1`), D02 (5 ký tự `12345`).
- **Kỳ vọng quan sát được:** Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."*
- **Kết quả:** **PASS**.

### 4.12. Phiếu thực thi TC-BB-004B (Độ dài Mật khẩu tại điểm biên hợp lệ N=6 và N=7)
- **Mã TC:** `TC-BB-004B`
- **Mục tiêu:** Xác minh hệ thống chấp nhận mật khẩu đạt chuẩn tối thiểu tại điểm biên hợp lệ $N=6$ ký tự và điểm lân cận $N+1=7$ ký tự.
- **Tiền điều kiện:** Đang ở màn hình Đăng ký; có mạng Internet.
- **Kỹ thuật áp dụng:** Phân tích giá trị biên hoàn chỉnh (BVA 3-point: $N-1=5$ tại TC-BB-004, $N=6$ tại D01, $N+1=7$ tại D02).
- **Dữ liệu:** D01 (6 ký tự `123456`), D02 (7 ký tự `1234567`).
- **Kỳ vọng quan sát được:** Mật khẩu được chấp nhận, đăng ký thành công và chuyển sang màn hình Xác thực Email.
- **Kết quả:** **PASS** (Cả 2 biến thể).

### 4.13. Phiếu thực thi TC-BB-005 (Trùng Email đã tồn tại & Phân biệt hoa/thường)
- **Mã TC:** `TC-BB-005`
- **Mục tiêu:** Xác minh tính duy nhất của tài khoản và tính năng không phân biệt hoa/thường (Case-insensitive) khi kiểm tra trùng lặp email.
- **Tiền điều kiện:** Tài khoản `student_qa@gmail.com` đã tồn tại trên hệ thống; thiết bị có kết nối mạng.
- **Căn cứ xác minh thực tế:** Đã kiểm thử thực tế trên thiết bị Samsung Galaxy S21 FE chạy Firebase Auth: Firebase Auth chuẩn hóa email về dạng chữ thường trước khi đối chiếu cơ sở dữ liệu, do đó khi nhập `STUDENT_QA@GMAIL.COM`, hệ thống phát hiện tài khoản đã tồn tại và trả về lỗi `email-already-in-use`.
- **Dữ liệu:** D01 (chữ thường `student_qa@gmail.com`), D02 (chữ IN HOA `STUDENT_QA@GMAIL.COM`).
- **Kỳ vọng quan sát được:** Cả hai trường hợp đều không chuyển màn hình; hiển thị khung thông báo lỗi màu đỏ: *"Email này đã được sử dụng cho một tài khoản khác."*
- **Kết quả:** **PASS** (Cả 2 biến thể).

---

## 5. QUY TẮC ĐẶT TÊN BẰNG CHỨNG KIỂM THỬ (EVIDENCE NAMING CONVENTION)

Cấu trúc chuẩn:  
`[FN-ID]_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`

Ví dụ áp dụng:
- `FN02_TC-BB-001_D01_01.png` — Màn hình đăng ký thành công Gmail
- `FN02_TC-BB-001B_D01_01.png` — Màn hình đăng ký tự động trim khoảng trắng
- `FN02_TC-BB-002_D01_01.png` — Màn hình lỗi bỏ trống cả 2 ô
- `FN02_TC-BB-002B_D01_01.png` — Màn hình lỗi chỉ bỏ trống mật khẩu
- `FN02_TC-BB-002C_D01_01.png` — Màn hình lỗi chỉ bỏ trống email
- `FN02_TC-BB-002D_D01_01.png` — Màn hình hiển thị mật khẩu rõ qua icon con mắt
- `FN02_TC-BB-002E_D01_01.png` — Màn hình xóa lỗi sau khi chuyển đổi tab
- `FN02_TC-BB-002F_D01_01.png` — Màn hình thông báo mất kết nối mạng
- `FN02_TC-BB-003_D01_01.png` — Màn hình lỗi khi thiếu @ (chứa BUG-FN02-01)
- `FN02_TC-BB-003B_D01_01.png` — Màn hình lỗi email rác tempmail
- `FN02_TC-BB-004_D02_01.png` — Màn hình lỗi mật khẩu 5 ký tự
- `FN02_TC-BB-004B_D01_01.png` — Màn hình đăng ký thành công với mật khẩu đúng 6 ký tự
- `FN02_TC-BB-005_D01_01.png` — Màn hình lỗi email đã tồn tại

---

## 6. DANH MỤC LỖI PHÁT HIỆN (BUG REPORT REFERENCE)

| Mã Bug (Bug ID) | Mã Test Case (TC-ID) | Mã dữ liệu (Data ID) | Tóm tắt mô tả lỗi quan sát được | Tệp bằng chứng đính kèm (Evidence) | Mức độ nghiêm trọng (Severity) | Trạng thái xử lý (Status) |
|:---:|:---:|:---:|---|---|:---:|:---:|
| **BUG-FN02-01** | **TC-BB-003** | **D01** | Khi nhập email thiếu ký tự `@` (`nguoidung_gmail.com`), ứng dụng hiển thị sai thông báo lỗi: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* thay vì *"Định dạng email không hợp lệ."* theo đặc tả. | `FN02_TC-BB-003_D01_01.png` | **Minor** | **Confirmed (Application Bug)** |

---

## 7. BẢNG TỔNG KẾT THỰC THI (TEST EXECUTION SUMMARY)

| Chỉ số đo lường (Metrics) | Giá trị số lượng | Ghi chú giải thích |
|---|:---:|---|
| **Tổng số Test Case sau khi đào sâu** | **13** | 5 Test Cases ban đầu + 8 Test Cases đào sâu mở rộng |
| **Tổng số mục thực thi (Execution Items)** | **19** | Bao phủ đầy đủ các biến thể dữ liệu (D01, D02, D03 từ STT 1 đến 19) |
| **Số mục ĐẠT (PASS)** | **18** | Actual Result khớp hoàn toàn với Expected Result |
| **Số mục KHÔNG ĐẠT (FAIL)** | **1** | Mục STT 11 (TC-BB-003 D01) do Application Bug `BUG-FN02-01` |
| **Số mục BỊ CHẶN (BLOCKED)** | **0** | Toàn bộ 19 mục đều được kiểm thử thành công trên thiết bị thật |
| **Tổng số lỗi phát hiện (Bugs)** | **1** | Ghi nhận tại Mục 6 (BUG-FN02-01) |
| **Tỷ lệ thực thi hoàn tất (Execution Rate)** | **100%** | 19 / 19 mục kiểm thử hoàn thành |
| **Tỷ lệ kiểm thử thành công (Pass Rate)** | **94.74%** | 18 / 19 mục PASS (94.74%) |

---

## 8. CHECKLIST BÀN GIAO KẾT QUẢ CHO TEST LEAD

- [x] **Tiêu chí 1 — Độ bao phủ:** Đã thực hiện đầy đủ 100% các ca kiểm thử (13 Test Cases với trọn vẹn 19 Execution Items từ STT 1 đến STT 19).
- [x] **Tiêu chí 2 — Ghi nhận kết quả thực tế:** Toàn bộ các ô tại cột `Actual Result` đều đã được mô tả trung thực, cụ thể theo đúng những gì quan sát được trên màn hình ứng dụng (Observable UI).
- [x] **Tiêu chí 3 — Xác nhận trạng thái rõ ràng:** Tất cả 19 mục đều đã được đánh dấu rõ ràng là `PASS`, `FAIL`, hoặc `BLOCKED`.
- [x] **Tiêu chí 4 — Lưu trữ bằng chứng đầy đủ:** Đã chụp màn hình kết quả cho từng mục thực thi và lưu trữ đúng tên file theo quy ước tại Mục 5.
- [x] **Tiêu chí 5 — Đăng ký lỗi đầy đủ:** Ca FAIL `TC-BB-003 D01` đã được gắn mã `BUG-FN02-01` và phân tích rõ nguyên nhân gốc trong mã nguồn.
- [x] **Tiêu chí 6 — Tính toàn vẹn của kịch bản:** Giữ nguyên vẹn nội dung `Expected Result`, không tự ý chỉnh sửa nội dung kỳ vọng để che giấu lỗi ứng dụng.
- [x] **Tiêu chí 7 — Đầy đủ thông tin môi trường:** Đã ghi rõ ràng và chính xác các thông tin về Thiết bị Samsung Galaxy S21 FE 5G, Android 14, bản build app và loại mạng tại Mục 1.
