# BẢNG THỰC THI KIỂM THỬ HỘP ĐEN (BLACK-BOX TEST EXECUTION SHEET)
## CHỨC NĂNG: ĐĂNG NHẬP TÀI KHOẢN EMAIL/PASSWORD (FN-04)

- **Dự án:** Smart Note App
- **Chức năng kiểm thử:** FN-04 — Đăng nhập tài khoản Email/Password
- **Phương pháp kiểm thử:** Kiểm thử hộp đen toàn diện (Comprehensive Black-box Testing)
- **Tài liệu tham chiếu thiết kế:** `black_box_test_cases.md`
- **Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Certified Tester Foundation Level (CTFL)
- **Mục tiêu tài liệu:** Cung cấp biểu mẫu thực thi chi tiết, rõ ràng từng bước cho Tester thực hiện kiểm thử thủ công chức năng Đăng nhập Email/Password. Bao phủ đầy đủ luồng thành công chuẩn (Happy Path), các phân lớp tương đương (Equivalence Partitioning), trường hợp bỏ trống dữ liệu bắt buộc (Missing/Empty), định dạng email không hợp lệ (Invalid Format), độ bền vững dữ liệu đầu vào (Input Robustness - Trimming & Case-insensitivity), tính năng giao diện (UI/Interaction - Ẩn/Hiện mật khẩu, Quên mật khẩu, Chuyển tab & Reset lỗi), xử lý ngoại lệ môi trường mạng (Network Offline), trạng thái kích hoạt tài khoản (Unverified Email Account State) và kiểm tra an toàn dữ liệu đầu vào (Security-related Robustness).

---

## 1. THÔNG TIN PHIÊN KIỂM THỬ (TEST SESSION INFORMATION)

| Mục thông tin | Chi tiết ghi nhận thực tế |
|---|---|
| **Mã chức năng (FN-ID)** | **FN-04** |
| **Tên chức năng** | **Đăng nhập tài khoản Email/Password** |
| **Người thực hiện kiểm thử (Tester)** | Huong (QA Tester) |
| **Ngày thực hiện kiểm thử** | 05/10/2026 |
| **Thiết bị / Máy ảo kiểm thử** | Samsung Galaxy S21 FE 5G (SM-G990E / R5CW82ECF6M) |
| **Hệ điều hành / Phiên bản Android** | Android 14 (API 34) |
| **Phiên bản ứng dụng (App Version / Build)** | v1.0.0 (Release Build) |
| **Loại kết nối mạng** | Wi-Fi (Tốc độ cao) & Chế độ Offline mô phỏng |
| **Ghi chú môi trường kiểm thử khác** | Độ phân giải 1080x2340, kết nối ADB ổn định |

---

## 2. ĐIỀU KIỆN CHUẨN BỊ TRƯỚC KHI THỰC HIỆN (PRECONDITIONS)

Trước khi bắt đầu thực hiện các ca kiểm thử thuộc chức năng FN-04, Tester cần chuẩn bị đầy đủ các điều kiện tiên quyết sau:

1. **Ứng dụng đã sẵn sàng:** Ứng dụng Smart Note App đã được cài đặt hoàn tất trên thiết bị, mở được và hoạt động ổn định.
2. **Trạng thái màn hình:** Ứng dụng phải ở trạng thái **chưa đăng nhập tài khoản**. Đang ở màn hình Đăng nhập (tab *"Đăng nhập"*, nút hành động chính màu xanh hiển thị chữ **"Đăng nhập"**, có 2 ô nhập: "Email" và "Mật khẩu", liên kết "Quên mật khẩu?"). Nếu ứng dụng đang ở màn hình Trang chủ ghi chú, Tester phải thực hiện **Đăng xuất** trước.
3. **Quản lý dữ liệu kiểm thử (Test Data Strategy):**
   - **Tài khoản test chính đã xác thực (Verified Account):** `student_qa@gmail.com`, Mật khẩu `123456` với `emailVerified = true`. Dùng cho `TC-BB-006`, `TC-BB-006C`, `TC-BB-006D`, `TC-BB-007`, `TC-BB-009`, `TC-BB-009B`, `TC-BB-009D`, `TC-BB-009E`.
   - **Tài khoản chưa kích hoạt xác thực (Unverified Account):** `unverified_qa@gmail.com`, Mật khẩu `123456` với `emailVerified = false`. Dùng cho `TC-BB-006B`.
   - **Tài khoản không tồn tại:** Sử dụng địa chỉ email chắc chắn chưa từng được đăng ký: `ghost_user@gmail.com`. Dùng cho `TC-BB-008`.
4. **Kết nối mạng Internet:** Thiết bị có kết nối mạng Internet (Wi-Fi/4G) hoạt động bình thường cho hầu hết các test case; riêng ca kiểm thử ngoại lệ mạng (`TC-BB-009F`) cần ngắt toàn bộ kết nối mạng trước khi bấm Đăng nhập.

---

## 3. BẢNG PHÂN LOẠI NGUỒN GỐC YÊU CẦU & KỸ THUẬT BLACK-BOX

| TC ID | Mục tiêu kiểm thử | Dữ liệu đầu vào (Input) | Điều kiện tiên quyết (Preconditions) | Kết quả quan sát được trên UI (Expected Observable UI) | Kỹ thuật Black-box áp dụng | Phân loại nguồn gốc yêu cầu | Trạng thái đề xuất |
|---|---|---|---|---|---|---|---|
| **TC-BB-006** | Xác minh đăng nhập thành công với thông tin chính xác | Email: `student_qa@gmail.com`<br>Mật khẩu: `123456` | Tài khoản tồn tại, đã kích hoạt xác thực email; thiết bị có mạng. | Ứng dụng hiển thị màn hình chờ đồng bộ, sau đó chuyển sang màn hình Trang chủ ghi chú. | Phân lớp tương đương (Valid Happy Path) | **Requirement-based** | TC đã có |
| **TC-BB-006B** | Xác minh điều hướng sang màn hình Xác thực email đối với tài khoản chưa xác thực | Email: `unverified_qa@gmail.com`<br>Mật khẩu: `123456` | Tài khoản tồn tại nhưng chưa kích hoạt xác thực email; thiết bị có mạng. | Ứng dụng điều hướng sang màn hình Xác thực email, hiển thị hướng dẫn kiểm tra hộp thư kích hoạt, không vào Trang chủ. | Kiểm thử trạng thái tài khoản (Account State) | **Code-inferred / As-built behavior** | TC cần bổ sung |
| **TC-BB-006C** | Xác minh tự động cắt tỉa khoảng trắng đầu/cuối của Email khi đăng nhập | Email: `"   student_qa@gmail.com   "`<br>Mật khẩu: `123456` | Tài khoản tồn tại, đã kích hoạt xác thực; thiết bị có mạng. | Ứng dụng tự loại bỏ khoảng trắng, đăng nhập thành công, hiển thị màn hình chờ đồng bộ rồi vào Trang chủ. | Input Robustness / Whitespace Trimming | **Code-inferred / As-built behavior** | TC cần bổ sung |
| **TC-BB-006D** | Xác minh chấp nhận Email viết chữ IN HOA (không phân biệt hoa thường) | Email: `STUDENT_QA@GMAIL.COM`<br>Mật khẩu: `123456` | Tài khoản tồn tại, đã kích hoạt xác thực; thiết bị có mạng. | Ứng dụng chuẩn hóa email, đăng nhập thành công, hiển thị màn hình chờ đồng bộ rồi vào Trang chủ. | Input Robustness / Case Insensitive | **Code-inferred / As-built behavior** | TC cần bổ sung |
| **TC-BB-007** | Xác minh từ chối đăng nhập khi nhập sai mật khẩu | Email: `student_qa@gmail.com`<br>Mật khẩu: `WrongPass999` | Tài khoản tồn tại trên hệ thống; thiết bị có mạng. | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Mật khẩu không chính xác."* | Phân lớp tương đương (Invalid Password) | **Requirement-based** | TC đã có |
| **TC-BB-007B** | Xác minh từ chối đăng nhập với Email sai định dạng cú pháp | D01: `student_qa_gmail.com`<br>D02: `student_qa@`<br>Mật khẩu: `123456` | Ứng dụng ở tab Đăng nhập; thiết bị có mạng. | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."* | Phân lớp tương đương (Invalid Format) | **Requirement-based** | TC cần bổ sung |
| **TC-BB-008** | Xác minh từ chối đăng nhập với tài khoản chưa từng được đăng ký | Email: `ghost_user@gmail.com`<br>Mật khẩu: `123456` | Email chưa từng được tạo tài khoản trên hệ thống; thiết bị có mạng. | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."* | Phân lớp tương đương (Non-existent Account) | **Requirement-based** | TC đã có |
| **TC-BB-008B** | Xác minh xử lý an toàn khi nhập ký tự đặc biệt / payload injection | Email: `' OR '1'='1`<br>Mật khẩu: `123456` | Ứng dụng ở tab Đăng nhập; thiết bị có mạng. | Ứng dụng không bị crash hay treo, không đăng nhập trái phép, hiển thị thông báo lỗi phù hợp trên màn hình. | Input Robustness / Special-character payload | **Code-inferred / As-built behavior** | TC cần bổ sung |
| **TC-BB-009** | Xác minh từ chối đăng nhập khi để trống trường Mật khẩu | Email: `student_qa@gmail.com`<br>Mật khẩu: `""` | Ứng dụng ở tab Đăng nhập. | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Phân lớp tương đương (Missing Password) | **Requirement-based** | TC đã có |
| **TC-BB-009B** | Xác minh từ chối đăng nhập khi để trống trường Email | Email: `""`<br>Mật khẩu: `123456` | Ứng dụng ở tab Đăng nhập. | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Phân lớp tương đương (Missing Email) | **Requirement-derived / Equivalence Class** | TC cần bổ sung |
| **TC-BB-009C** | Xác minh từ chối đăng nhập khi để trống cả Email và Mật khẩu | Email: `""`<br>Mật khẩu: `""` | Ứng dụng ở tab Đăng nhập. | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Phân lớp tương đương (Missing All Fields) | **Requirement-derived / Equivalence Class** | TC cần bổ sung |
| **TC-BB-009D** | Xác minh chuyển đổi chế độ Ẩn / Hiện mật khẩu qua icon con mắt | Email: `student_qa@gmail.com`<br>Mật khẩu: `123456` | Đang ở tab Đăng nhập, ô Mật khẩu đang có giá trị. | Chạm lần 1: Ký tự mật khẩu chuyển sang dạng chữ đọc được (`123456`), icon mắt mở. Chạm lần 2: Ký tự chuyển về dạng chấm che ẩn (`••••••`), icon mắt gạch chéo. | Kiểm thử giao diện & tương tác (UI / Interaction) | **Code-inferred / As-built behavior** | TC cần bổ sung |
| **TC-BB-009E** | Xác minh mở và đóng Hộp thoại "Quên mật khẩu?" | Email trên form: `student_qa@gmail.com` | Đang ở tab Đăng nhập. | Chạm "Quên mật khẩu?": Xuất hiện hộp thoại có tiêu đề *"Quên mật khẩu?"* với ô email điền sẵn. Chạm "Hủy": Hộp thoại đóng lại, quay về form đăng nhập. | Kiểm thử giao diện & tương tác (UI / Interaction) | **Code-inferred / As-built behavior** | TC cần bổ sung |
| **TC-BB-009F** | Xác minh xử lý lỗi khi đăng nhập trong điều kiện thiết bị mất mạng | Email: `student_qa@gmail.com`<br>Mật khẩu: `123456` | Thiết bị đã ngắt toàn bộ kết nối mạng (Wi-Fi/4G tắt). | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Không có kết nối mạng. Vui lòng kiểm tra lại."* | Kiểm thử ngoại lệ mạng (Network Offline Robustness) | **Code-inferred / As-built behavior** | TC cần bổ sung |
| **TC-BB-009G** | Xác minh chuyển đổi tab Đăng nhập $\leftrightarrow$ Đăng ký và xóa sạch thông báo lỗi cũ | Form đang có thông báo lỗi màu đỏ | Đang ở tab Đăng nhập, có lỗi hiển thị sẵn trên màn hình. | Chạm "Đăng ký ngay" chuyển sang tab Đăng ký; chạm "Đăng nhập" quay lại thì dòng thông báo lỗi cũ đã được xóa sạch hoàn toàn. | Kiểm thử trạng thái giao diện (UI State Integrity) | **Code-inferred / As-built behavior** | TC cần bổ sung |
| *(Loại trừ)* | Kiểm tra biên độ dài mật khẩu khi đăng nhập ($N-1=5, N=6, N+1=7$) | Mật khẩu 5 ký tự | Form đăng nhập | *(Không áp dụng riêng cho Login)*: Phía client không chặn độ dài mật khẩu khi đăng nhập (chỉ kiểm tra rỗng), việc nhập mật khẩu sai 1-5 ký tự đã được bao phủ trọn vẹn tại `TC-BB-007`. Không cần thêm TC biên độ dài gây dư thừa. | Phân tích giá trị biên (BVA) | *(Không có trong spec Login)* | **TC không cần thiết** (Loại trừ có lý do) |

---

## 4. BẢNG THỰC THI KIỂM THỬ TỔNG HỢP (TEST EXECUTION MATRIX)

> **Hướng dẫn cho Tester:**  
> - Bảng gồm đúng **15 Test Cases** với trọn vẹn **16 Execution Items** (STT 1 đến STT 16).
> - Thực hiện tuần tự từng bước tại cột **Các bước thực hiện (Steps)** và sử dụng dữ liệu tại cột **Test Data**.
> - Quan sát giao diện thực tế và ghi nhận vào cột **Actual Result** (chỉ ghi nhận hành vi observable trực tiếp trên UI).
> - So sánh giữa **Actual Result** và **Expected Result**: Khớp ghi **PASS**, sai lệch ghi **FAIL**, bị chặn môi trường ghi **BLOCKED**.

| STT | TC-ID | Data ID | Phân loại | Test Data | Các bước thực hiện (Steps) | Expected Result (Observable UI) | Actual Result | Trạng thái | Evidence ID | Bug ID / Ghi chú |
|:---:|:---:|:---:|:---:|:---|:---|:---|:---|:---:|:---|:---:|
| **1** | **TC-BB-006** | **D01** | Đã có | • Email: `student_qa@gmail.com`<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng nhập.<br>2. Nhập Email và Mật khẩu chính xác.<br>3. Nhấn nút "Đăng nhập". | Đăng nhập thành công, hiển thị hiệu ứng màn hình chờ đồng bộ (sync progress) và chuyển thẳng vào Trang chủ ghi chú (`HomeScreen`). | Đăng nhập thành công, hiển thị màn hình chờ đồng bộ dữ liệu và chuyển thẳng vào Trang chủ ghi chú (`HomeScreen`). Giao diện hiển thị thanh tìm kiếm và khu vực ghi chú. | **PASS** | `FN04_TC-BB-006_D01_01.png` | Thực thi thành công trên thiết bị thật sau khi chuẩn bị tài khoản `student_qa@gmail.com` có `emailVerified = true`. |
| **2** | **TC-BB-006B** | **D01** | Bổ sung | • Email: `unverified_qa@gmail.com`<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng nhập.<br>2. Nhập thông tin tài khoản hợp lệ nhưng chưa xác thực email.<br>3. Nhấn nút "Đăng nhập". | Ứng dụng thông báo hoặc chuyển hướng người dùng đến màn hình Xác thực email (`EmailVerificationScreen`) với thông báo yêu cầu kích hoạt tài khoản. | Ứng dụng chuyển hướng chính xác sang màn hình "Xác thực email của bạn" (`EmailVerificationScreen`), hiển thị hướng dẫn kiểm tra email kích hoạt, không vào Trang chủ. | **PASS** | `FN04_TC-BB-006B_D01_01.png` | Thực thi thành công trên thiết bị thật sau khi chuẩn bị tài khoản `unverified_qa@gmail.com` tồn tại với `emailVerified = false`. |
| **3** | **TC-BB-006C** | **D01** | Bổ sung | • Email: `"   student_qa@gmail.com   "`<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng nhập.<br>2. Nhập Email có khoảng trắng thừa ở đầu và cuối.<br>3. Nhập Mật khẩu `123456`.<br>4. Nhấn nút "Đăng nhập". | Ứng dụng tự loại bỏ khoảng trắng, đăng nhập thành công, hiển thị màn hình chờ đồng bộ rồi vào Trang chủ (`HomeScreen`). | Ứng dụng tự động cắt tỉa khoảng trắng ở hai đầu email, đăng nhập thành công, hiển thị màn hình chờ đồng bộ và chuyển vào Trang chủ (`HomeScreen`). | **PASS** | `FN04_TC-BB-006C_D01_01.png` | Thực thi thành công trên thiết bị thật sau khi chuẩn bị tài khoản `student_qa@gmail.com` có `emailVerified = true`. |
| **4** | **TC-BB-006D** | **D01** | Bổ sung | • Email: `STUDENT_QA@GMAIL.COM`<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng nhập.<br>2. Nhập Email viết toàn bộ bằng chữ IN HOA.<br>3. Nhập Mật khẩu `123456`.<br>4. Nhấn nút "Đăng nhập". | Ứng dụng chuẩn hóa email, đăng nhập thành công, hiển thị màn hình chờ đồng bộ và chuyển vào Trang chủ (`HomeScreen`). | Ứng dụng xử lý email không phân biệt chữ hoa/chữ thường, đăng nhập thành công, hiển thị màn hình chờ đồng bộ và chuyển vào Trang chủ (`HomeScreen`). | **PASS** | `FN04_TC-BB-006D_D01_01.png` | Thực thi thành công trên thiết bị thật sau khi chuẩn bị tài khoản `student_qa@gmail.com` có `emailVerified = true`. |
| **5** | **TC-BB-007** | **D01** | Đã có | • Email: `student_qa@gmail.com`<br>• Mật khẩu: `WrongPass999` | 1. Đang ở tab Đăng nhập.<br>2. Nhập đúng Email đã đăng ký.<br>3. Nhập sai Mật khẩu.<br>4. Nhấn nút "Đăng nhập". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Mật khẩu không chính xác."* | Ứng dụng hiển thị thông báo lỗi gộp màu đỏ: *"Email hoặc mật khẩu không chính xác."* thay vì thông báo riêng *"Mật khẩu không chính xác."* | **FAIL** | `FN04_TC-BB-007_D01_01.png` | Requirement-based. Lỗi sai khác tài liệu đặc tả: BUG-BB-003 |
| **6** | **TC-BB-007B** | **D01** | Bổ sung | • Email: `student_qa_gmail.com`<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng nhập.<br>2. Nhập Email thiếu ký tự `@`.<br>3. Nhập Mật khẩu `123456`.<br>4. Nhấn nút "Đăng nhập". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."* | Ứng dụng không chuyển màn hình; chặn gửi request và hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."* | **PASS** | `FN04_TC-BB-007B_D01_01.png` | Requirement-based (Kiểm tra cú pháp email thiếu `@`) |
| **7** | **TC-BB-007B** | **D02** | Bổ sung | • Email: `student_qa@`<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng nhập.<br>2. Nhập Email có `@` nhưng thiếu tên miền.<br>3. Nhập Mật khẩu `123456`.<br>4. Nhấn nút "Đăng nhập". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."* | Ứng dụng không chuyển màn hình; chặn gửi request và hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."* | **PASS** | `FN04_TC-BB-007B_D02_01.png` | Requirement-based (Kiểm tra cú pháp email thiếu tên miền) |
| **8** | **TC-BB-008** | **D01** | Đã có | • Email: `ghost_user@gmail.com`<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng nhập.<br>2. Nhập Email chưa từng đăng ký trên hệ thống.<br>3. Nhập Mật khẩu bất kỳ.<br>4. Nhấn nút "Đăng nhập". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."* | Ứng dụng hiển thị thông báo lỗi gộp màu đỏ: *"Email hoặc mật khẩu không chính xác."* thay vì thông báo riêng *"Tài khoản không tồn tại..."* | **FAIL** | `FN04_TC-BB-008_D01_01.png` | Requirement-based. Lỗi sai khác tài liệu đặc tả: BUG-BB-002 |
| **9** | **TC-BB-008B** | **D01** | Bổ sung | • Email: `' OR '1'='1`<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng nhập.<br>2. Nhập chuỗi ký tự đặc biệt `' OR '1'='1` vào ô Email.<br>3. Nhập Mật khẩu `123456`.<br>4. Nhấn nút "Đăng nhập". | Ứng dụng không bị crash hay treo, không đăng nhập trái phép, hiển thị thông báo lỗi phù hợp trên màn hình. | Ứng dụng không crash hay treo, không đăng nhập trái phép, hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."* | **PASS** | `FN04_TC-BB-008B_D01_01.png` | Special-character payload / Input Robustness. Xử lý an toàn chuỗi ký tự đặc biệt, không crash, không đăng nhập trái phép. |
| **10** | **TC-BB-009** | **D01** | Đã có | • Email: `student_qa@gmail.com`<br>• Mật khẩu: `""` | 1. Đang ở tab Đăng nhập.<br>2. Nhập Email hợp lệ.<br>3. Để trống hoàn toàn ô Mật khẩu.<br>4. Nhấn nút "Đăng nhập". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | **PASS** | `FN04_TC-BB-009_D01_01.png` | Requirement-based (Thiếu mật khẩu) |
| **11** | **TC-BB-009B** | **D01** | Bổ sung | • Email: `""`<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng nhập.<br>2. Để trống hoàn toàn ô Email.<br>3. Nhập Mật khẩu `123456`.<br>4. Nhấn nút "Đăng nhập". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | **PASS** | `FN04_TC-BB-009B_D01_01.png` | Requirement-derived / Equivalence Class (Thiếu email) |
| **12** | **TC-BB-009C** | **D01** | Bổ sung | • Email: `""`<br>• Mật khẩu: `""` | 1. Đang ở tab Đăng nhập.<br>2. Để trống cả 2 ô Email và Mật khẩu.<br>3. Nhấn nút "Đăng nhập". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | **PASS** | `FN04_TC-BB-009C_D01_01.png` | Requirement-derived / Equivalence Class (Thiếu cả 2 trường) |
| **13** | **TC-BB-009D** | **D01** | Bổ sung | • Email: `student_qa@gmail.com`<br>• Mật khẩu: `123456` | 1. Đang ở tab Đăng nhập, ô Mật khẩu có `123456`.<br>2. Chạm vào icon con mắt ở ô Mật khẩu.<br>3. Quan sát hiển thị ký tự.<br>4. Chạm lại vào icon con mắt lần 2. | Chạm lần 1: Mật khẩu hiển thị dạng văn bản rõ `123456`, icon mắt mở. Chạm lần 2: Mật khẩu chuyển về dạng chấm che ẩn `••••••`, icon mắt gạch chéo. | Chạm lần 1: Mật khẩu hiển thị rõ `123456`. Chạm lần 2: Mật khẩu che ẩn dạng chấm `••••••`. Icon chuyển trạng thái chính xác. | **PASS** | `FN04_TC-BB-009D_D01_01.png`<br>`FN04_TC-BB-009D_D01_02.png` | Code-inferred / UI Interaction (Chuyển đổi ẩn/hiện mật khẩu) |
| **14** | **TC-BB-009E** | **D01** | Bổ sung | • Email trên form: `student_qa@gmail.com` | 1. Đang ở tab Đăng nhập, đã nhập sẵn email.<br>2. Chạm vào dòng chữ "Quên mật khẩu?".<br>3. Quan sát hộp thoại xuất hiện.<br>4. Chạm nút "Hủy". | Sau bước 2: Xuất hiện hộp thoại tiêu đề *"Quên mật khẩu?"* với ô email điền sẵn. Sau bước 4: Hộp thoại đóng lại, quay về form đăng nhập bình thường. | Hộp thoại *"Quên mật khẩu?"* xuất hiện với email điền sẵn. Nhấn *"Hủy"* đóng hộp thoại an toàn quay lại form đăng nhập. | **PASS** | `FN04_TC-BB-009E_D01_01.png` | Code-inferred / UI Interaction (Hộp thoại Quên mật khẩu) |
| **15** | **TC-BB-009F** | **D01** | Bổ sung | • Email: `student_qa@gmail.com`<br>• Mật khẩu: `123456`<br>• Trạng thái mạng: Tắt Wi-Fi/4G | 1. Tắt toàn bộ kết nối Wi-Fi và Dữ liệu di động trên thiết bị.<br>2. Đang ở tab Đăng nhập, nhập Email và Mật khẩu.<br>3. Nhấn nút "Đăng nhập". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Không có kết nối mạng. Vui lòng kiểm tra lại."*, form giữ nguyên dữ liệu. | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Không có kết nối mạng. Vui lòng kiểm tra lại."*, form giữ nguyên dữ liệu. | **PASS** | `FN04_TC-BB-009F_D01_01.png` | Code-inferred / Error Handling (Xử lý khi mất mạng) |
| **16** | **TC-BB-009G** | **D01** | Bổ sung | • Form đang có thông báo lỗi màu đỏ | 1. Đang ở tab Đăng nhập với thông báo lỗi hiển thị sẵn.<br>2. Chạm vào "Đăng ký ngay" ở cuối màn hình.<br>3. Quan sát màn hình Đăng ký.<br>4. Chạm vào "Đăng nhập" để quay lại. | Khi sang tab Đăng ký, tiêu đề đổi thành *"Tạo tài khoản mới"*; khi quay lại tab Đăng nhập, thông báo lỗi màu đỏ cũ đã biến mất hoàn toàn. | Khi sang tab Đăng ký tiêu đề đổi thành *"Tạo tài khoản mới"*; khi quay lại tab Đăng nhập thông báo lỗi màu đỏ cũ biến mất hoàn toàn. | **PASS** | `FN04_TC-BB-009G_D01_01.png` | Code-inferred / UI State Integrity (Làm sạch lỗi khi chuyển tab) |

---

## 5. HƯỚNG DẪN CHI TIẾT TỪNG TEST CASE (DETAILED TEST EXECUTION CARDS)

### TC-BB-006: Đăng nhập thành công với thông tin chính xác (Happy Path)
- **Mục tiêu:** Xác minh người dùng có tài khoản hợp lệ đã kích hoạt xác thực email đăng nhập thành công vào ứng dụng.
- **Phân loại nguồn gốc:** Requirement-based.
- **Kỹ thuật Black-box:** Phân lớp tương đương (Valid Equivalence Class).
- **Điều kiện tiên quyết:** Tài khoản `student_qa@gmail.com` tồn tại và `emailVerified = true`. Thiết bị có kết nối mạng ổn định.
- **Ghi chú thực thi:** Đã chuẩn bị tài khoản `student_qa@gmail.com` với `emailVerified = true`; ứng dụng đăng nhập thành công và chuyển vào Trang chủ (`HomeScreen`). Kết quả: **PASS**.
- **Dữ liệu kiểm thử:** Email: `student_qa@gmail.com`, Mật khẩu: `123456`.
- **Các bước thực hiện:**
  1. Mở ứng dụng, xác nhận đang ở tab Đăng nhập.
  2. Nhập `student_qa@gmail.com` vào ô "Email".
  3. Nhập `123456` vào ô "Mật khẩu".
  4. Nhấn nút "Đăng nhập".
- **Kết quả mong đợi quan sát được trên UI:**
  - Nút "Đăng nhập" hiển thị vòng tròn tải (loading) trong giây lát.
  - Ứng dụng hiển thị màn hình chờ đồng bộ dữ liệu, sau đó điều hướng vào màn hình Trang chủ ghi chú.
  - Không xuất hiện thông báo lỗi nào trên màn hình.
- **Thu dọn sau test (Teardown):** Thực hiện Đăng xuất tài khoản để đưa ứng dụng về màn hình Đăng nhập cho các ca kiểm thử kế tiếp.

---

### TC-BB-006B: Đăng nhập tài khoản hợp lệ nhưng chưa xác thực email
- **Mục tiêu:** Xác minh ứng dụng chuyển hướng đúng sang màn hình Xác thực email khi tài khoản chưa kích hoạt qua hộp thư.
- **Phân loại nguồn gốc:** Code-inferred / As-built behavior.
- **Kỹ thuật Black-box:** Kiểm thử trạng thái tài khoản (Account State).
- **Điều kiện tiên quyết:** Tài khoản `unverified_qa@gmail.com` phải tồn tại và `emailVerified = false`. Thiết bị có kết nối mạng.
- **Ghi chú thực thi:** Đã chuẩn bị tài khoản `unverified_qa@gmail.com` với `emailVerified = false`; ứng dụng chuyển hướng chính xác sang màn hình Xác thực email (`EmailVerificationScreen`). Kết quả: **PASS**.
- **Dữ liệu kiểm thử:** Email: `unverified_qa@gmail.com`, Mật khẩu: `123456`.
- **Các bước thực hiện:**
  1. Đang ở tab Đăng nhập.
  2. Nhập Email tài khoản chưa xác thực vào ô "Email".
  3. Nhập Mật khẩu `123456` vào ô "Mật khẩu".
  4. Nhấn nút "Đăng nhập".
- **Kết quả mong đợi quan sát được trên UI:**
  - Ứng dụng không điều hướng vào Trang chủ ghi chú.
  - Ứng dụng điều hướng sang màn hình "Xác thực email của bạn", hiển thị biểu tượng hộp thư, địa chỉ email vừa đăng nhập và các nút chức năng gửi lại email xác thực / quay lại.

---

### TC-BB-006C: Tự động cắt tỉa khoảng trắng đầu/cuối của Email khi đăng nhập
- **Mục tiêu:** Xác minh người dùng vô tình nhập thêm khoảng trắng ở đầu hoặc cuối địa chỉ email vẫn được hệ thống tự xử lý và cho phép đăng nhập thành công vào ứng dụng.
- **Phân loại nguồn gốc:** Code-inferred / As-built behavior.
- **Kỹ thuật Black-box:** Input Robustness / Whitespace Trimming.
- **Điều kiện tiên quyết:** Tài khoản `student_qa@gmail.com` tồn tại và `emailVerified = true`. Thiết bị có kết nối mạng ổn định.
- **Ghi chú thực thi:** Đã chuẩn bị tài khoản `student_qa@gmail.com` với `emailVerified = true`; ứng dụng tự động cắt tỉa khoảng trắng đầu/cuối, đăng nhập thành công vào Trang chủ (`HomeScreen`). Kết quả: **PASS**.
- **Dữ liệu kiểm thử:** Email: `"   student_qa@gmail.com   "`, Mật khẩu: `123456`.
- **Các bước thực hiện:**
  1. Đang ở tab Đăng nhập.
  2. Nhập 3 dấu cách, tiếp theo là `student_qa@gmail.com`, kết thúc bằng 3 dấu cách vào ô "Email".
  3. Nhập Mật khẩu `123456`.
  4. Nhấn nút "Đăng nhập".
- **Kết quả mong đợi quan sát được trên UI:**
  - Ứng dụng tự loại bỏ các khoảng trắng thừa, chấp nhận yêu cầu đăng nhập.
  - Hiển thị màn hình chờ đồng bộ và chuyển vào màn hình Trang chủ ghi chú thành công.
- **Thu dọn sau test (Teardown):** Đăng xuất tài khoản để reset trạng thái.

---

### TC-BB-006D: Chấp nhận Email viết chữ IN HOA (Không phân biệt hoa thường)
- **Mục tiêu:** Xác minh hệ thống đối sánh tài khoản không phân biệt chữ hoa hay chữ thường trong địa chỉ email, cho phép đăng nhập thành công vào ứng dụng.
- **Phân loại nguồn gốc:** Code-inferred / As-built behavior.
- **Kỹ thuật Black-box:** Input Robustness / Case Insensitive.
- **Điều kiện tiên quyết:** Tài khoản `student_qa@gmail.com` tồn tại và `emailVerified = true`. Thiết bị có kết nối mạng ổn định.
- **Ghi chú thực thi:** Đã chuẩn bị tài khoản `student_qa@gmail.com` với `emailVerified = true`; ứng dụng đối sánh email không phân biệt hoa/thường, đăng nhập thành công vào Trang chủ (`HomeScreen`). Kết quả: **PASS**.
- **Dữ liệu kiểm thử:** Email: `STUDENT_QA@GMAIL.COM`, Mật khẩu: `123456`.
- **Các bước thực hiện:**
  1. Đang ở tab Đăng nhập.
  2. Nhập `STUDENT_QA@GMAIL.COM` vào ô "Email".
  3. Nhập Mật khẩu `123456`.
  4. Nhấn nút "Đăng nhập".
- **Kết quả mong đợi quan sát được trên UI:**
  - Ứng dụng chấp nhận thông tin, đăng nhập thành công vào ứng dụng.
  - Hiển thị màn hình chờ đồng bộ và điều hướng vào Trang chủ ghi chú.
- **Thu dọn sau test (Teardown):** Đăng xuất tài khoản để reset trạng thái.

---

### TC-BB-007: Từ chối đăng nhập khi nhập sai mật khẩu
- **Mục tiêu:** Xác minh hệ thống từ chối truy cập và thông báo lỗi rõ ràng khi người dùng nhập sai mật khẩu của tài khoản tồn tại.
- **Phân loại nguồn gốc:** Requirement-based.
- **Kỹ thuật Black-box:** Phân lớp tương đương (Invalid Password Equivalence Class).
- **Điều kiện tiên quyết:** Tài khoản `student_qa@gmail.com` tồn tại trên hệ thống; thiết bị có mạng.
- **Dữ liệu kiểm thử:** Email: `student_qa@gmail.com`, Mật khẩu: `WrongPass999`.
- **Các bước thực hiện:**
  1. Đang ở tab Đăng nhập.
  2. Nhập Email đúng `student_qa@gmail.com`.
  3. Nhập Mật khẩu sai `WrongPass999`.
  4. Nhấn nút "Đăng nhập".
- **Kết quả mong đợi quan sát được trên UI:**
  - Ứng dụng không chuyển màn hình, giữ nguyên form đăng nhập.
  - Xuất hiện thông báo lỗi màu đỏ: *"Mật khẩu không chính xác."* (Nếu hệ thống hiển thị thông báo gộp *"Email hoặc mật khẩu không chính xác."*, ghi nhận sai lệch theo `BUG-BB-003`).

---

### TC-BB-007B: Từ chối đăng nhập với Email sai định dạng cú pháp
- **Mục tiêu:** Xác minh hệ thống từ chối đăng nhập và báo lỗi cú pháp khi người dùng nhập email không đúng quy cách.
- **Phân loại nguồn gốc:** Requirement-based.
- **Kỹ thuật Black-box:** Phân lớp tương đương (Invalid Format Equivalence Class).
- **Điều kiện tiên quyết:** Ứng dụng ở tab Đăng nhập; thiết bị có mạng.
- **Dữ liệu kiểm thử:**
  - D01: Email: `student_qa_gmail.com` (thiếu ký tự `@`), Mật khẩu: `123456`.
  - D02: Email: `student_qa@` (có `@` nhưng thiếu phần tên miền), Mật khẩu: `123456`.
- **Các bước thực hiện:**
  1. Đang ở tab Đăng nhập.
  2. Nhập email sai định dạng (D01 hoặc D02).
  3. Nhập Mật khẩu `123456`.
  4. Nhấn nút "Đăng nhập".
- **Kết quả mong đợi quan sát được trên UI:**
  - Ứng dụng không chuyển màn hình.
  - Xuất hiện thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."*

---

### TC-BB-008: Từ chối đăng nhập với tài khoản chưa từng được đăng ký
- **Mục tiêu:** Xác minh hệ thống từ chối truy cập khi địa chỉ email chưa từng tồn tại trên hệ thống.
- **Phân loại nguồn gốc:** Requirement-based.
- **Kỹ thuật Black-box:** Phân lớp tương đương (Non-existent Account Equivalence Class).
- **Điều kiện tiên quyết:** Email `ghost_user@gmail.com` chắc chắn chưa từng được đăng ký; thiết bị có mạng.
- **Dữ liệu kiểm thử:** Email: `ghost_user@gmail.com`, Mật khẩu: `123456`.
- **Các bước thực hiện:**
  1. Đang ở tab Đăng nhập.
  2. Nhập Email `ghost_user@gmail.com`.
  3. Nhập Mật khẩu `123456`.
  4. Nhấn nút "Đăng nhập".
- **Kết quả mong đợi quan sát được trên UI:**
  - Ứng dụng không chuyển màn hình, giữ nguyên form đăng nhập.
  - Xuất hiện thông báo lỗi màu đỏ: *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."* (Nếu hệ thống hiển thị thông báo gộp *"Email hoặc mật khẩu không chính xác."*, ghi nhận sai lệch theo `BUG-BB-002`).

---

### TC-BB-008B: Xử lý an toàn khi nhập ký tự đặc biệt / payload injection
- **Mục tiêu:** Xác minh ứng dụng vận hành an toàn, không bị crash hoặc treo khi trường email nhận chuỗi ký tự đặc biệt hoặc payload dạng mệnh đề logic.
- **Phân loại nguồn gốc:** Code-inferred / As-built behavior.
- **Kỹ thuật Black-box:** Input Robustness / Special-character payload.
- **Điều kiện tiên quyết:** Ứng dụng ở tab Đăng nhập; thiết bị có mạng.
- **Dữ liệu kiểm thử:** Email: `' OR '1'='1`, Mật khẩu: `123456`.
- **Các bước thực hiện:**
  1. Đang ở tab Đăng nhập.
  2. Nhập chuỗi ký tự đặc biệt `' OR '1'='1` vào ô Email.
  3. Nhập Mật khẩu `123456`.
  4. Nhấn nút "Đăng nhập".
- **Kết quả mong đợi quan sát được trên UI (Observable Behavior):**
  - Ứng dụng phản hồi ổn định, không bị treo hay đóng đột ngột (crash).
  - Không đăng nhập trái phép vào hệ thống, không chuyển màn hình.
  - Hiển thị thông báo lỗi phù hợp trên màn hình: *"Định dạng email không hợp lệ."*
- **Ghi chú kỹ thuật:** Kiểm thử độ bền vững giao diện trước chuỗi ký tự đặc biệt (Input Robustness), không dùng Black-box để kết luận an toàn trước SQL Injection.

---

### TC-BB-009: Từ chối đăng nhập khi để trống trường Mật khẩu
- **Mục tiêu:** Xác minh hệ thống kiểm tra và nhắc nhở người dùng khi bỏ trống trường Mật khẩu bắt buộc.
- **Phân loại nguồn gốc:** Requirement-based.
- **Kỹ thuật Black-box:** Phân lớp tương đương (Missing/Empty Password).
- **Điều kiện tiên quyết:** Ứng dụng ở tab Đăng nhập.
- **Dữ liệu kiểm thử:** Email: `student_qa@gmail.com`, Mật khẩu: `""` (bỏ trống).
- **Các bước thực hiện:**
  1. Đang ở tab Đăng nhập.
  2. Nhập Email hợp lệ `student_qa@gmail.com`.
  3. Để trống hoàn toàn ô "Mật khẩu".
  4. Nhấn nút "Đăng nhập".
- **Kết quả mong đợi quan sát được trên UI:**
  - Ứng dụng không gửi yêu cầu đăng nhập, không chuyển màn hình.
  - Xuất hiện thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."*

---

### TC-BB-009B: Từ chối đăng nhập khi để trống trường Email
- **Mục tiêu:** Xác minh hệ thống kiểm tra và nhắc nhở người dùng khi bỏ trống trường Email bắt buộc.
- **Phân loại nguồn gốc:** Requirement-derived / Equivalence Class.
- **Kỹ thuật Black-box:** Phân lớp tương đương (Missing/Empty Email).
- **Điều kiện tiên quyết:** Ứng dụng ở tab Đăng nhập.
- **Dữ liệu kiểm thử:** Email: `""` (bỏ trống), Mật khẩu: `123456`.
- **Các bước thực hiện:**
  1. Đang ở tab Đăng nhập.
  2. Để trống hoàn toàn ô "Email".
  3. Nhập Mật khẩu `123456` vào ô "Mật khẩu".
  4. Nhấn nút "Đăng nhập".
- **Kết quả mong đợi quan sát được trên UI:**
  - Ứng dụng không gửi yêu cầu đăng nhập, không chuyển màn hình.
  - Xuất hiện thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."*

---

### TC-BB-009C: Từ chối đăng nhập khi để trống đồng thời cả Email và Mật khẩu
- **Mục tiêu:** Xác minh hệ thống kiểm tra và nhắc nhở người dùng khi bỏ trống tất cả các trường thông tin.
- **Phân loại nguồn gốc:** Requirement-derived / Equivalence Class.
- **Kỹ thuật Black-box:** Phân lớp tương đương (Missing/Empty All Fields).
- **Điều kiện tiên quyết:** Ứng dụng ở tab Đăng nhập.
- **Dữ liệu kiểm thử:** Email: `""`, Mật khẩu: `""`.
- **Các bước thực hiện:**
  1. Đang ở tab Đăng nhập.
  2. Không nhập gì vào cả 2 ô "Email" và "Mật khẩu".
  3. Nhấn nút "Đăng nhập".
- **Kết quả mong đợi quan sát được trên UI:**
  - Ứng dụng không gửi yêu cầu đăng nhập, không chuyển màn hình.
  - Xuất hiện thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."*

---

### TC-BB-009D: Chuyển đổi chế độ Ẩn / Hiện mật khẩu qua icon con mắt
- **Mục tiêu:** Xác minh người dùng có thể linh hoạt chuyển đổi giữa việc ẩn mật khẩu (dạng dấu chấm) và hiện mật khẩu (dạng văn bản rõ).
- **Phân loại nguồn gốc:** Code-inferred / As-built behavior.
- **Kỹ thuật Black-box:** Kiểm thử giao diện & tương tác (UI / Interaction).
- **Điều kiện tiên quyết:** Đang ở tab Đăng nhập, ô Mật khẩu đã nhập giá trị `123456` (mặc định các ký tự bị che ẩn `••••••`).
- **Dữ liệu kiểm thử:** Mật khẩu: `123456`.
- **Các bước thực hiện:**
  1. Nhập `123456` vào ô "Mật khẩu".
  2. Chạm vào icon con mắt ở góc phải ô Mật khẩu (lần 1).
  3. Quan sát các ký tự trong ô Mật khẩu và trạng thái icon con mắt.
  4. Chạm lại vào icon con mắt ở góc phải ô Mật khẩu (lần 2).
- **Kết quả mong đợi quan sát được trên UI:**
  - Sau bước 2-3: Các ký tự mật khẩu hiển thị rõ văn bản `"123456"`, icon con mắt chuyển sang dạng mắt mở (không còn gạch chéo).
  - Sau bước 4: Các ký tự mật khẩu lập tức quay lại trạng thái bị che ẩn (`••••••`), icon con mắt chuyển về dạng có gạch chéo.

---

### TC-BB-009E: Mở và đóng Hộp thoại "Quên mật khẩu?"
- **Mục tiêu:** Xác minh tương tác mở hộp thoại đặt lại mật khẩu và hỗ trợ điền sẵn email từ form đăng nhập, cũng như đóng hộp thoại an toàn bằng nút "Hủy".
- **Phân loại nguồn gốc:** Code-inferred / As-built behavior.
- **Kỹ thuật Black-box:** Kiểm thử giao diện & tương tác (UI / Interaction).
- **Điều kiện tiên quyết:** Đang ở tab Đăng nhập, đã nhập email `student_qa@gmail.com` vào ô "Email".
- **Dữ liệu kiểm thử:** Email trên form: `student_qa@gmail.com`.
- **Các bước thực hiện:**
  1. Chạm vào dòng chữ "Quên mật khẩu?" nằm phía dưới ô Mật khẩu.
  2. Quan sát hộp thoại xuất hiện trên màn hình.
  3. Chạm vào nút "Hủy" ở góc phải bên dưới của hộp thoại.
- **Kết quả mong đợi quan sát được trên UI:**
  - Sau bước 1-2: Xuất hiện hộp thoại (dialog) nổi trên màn hình với tiêu đề *"Quên mật khẩu?"*, phần mô tả *"Nhập địa chỉ email của bạn để nhận liên kết đặt lại mật khẩu:"*, ô nhập Email bên trong hộp thoại đã được điền sẵn giá trị `student_qa@gmail.com`, có 2 nút "Hủy" và "Gửi liên kết".
  - Sau bước 3: Hộp thoại đóng lại, màn hình quay về trạng thái form đăng nhập bình thường.

---

### TC-BB-009F: Xử lý lỗi khi đăng nhập trong điều kiện thiết bị mất mạng (Network Offline)
- **Mục tiêu:** Xác minh ứng dụng phát hiện kịp thời trạng thái mất kết nối mạng, hiển thị thông báo lỗi rõ ràng và không làm mất dữ liệu người dùng đã nhập.
- **Phân loại nguồn gốc:** Code-inferred / As-built behavior.
- **Kỹ thuật Black-box:** Kiểm thử ngoại lệ mạng (Network Offline Error Handling).
- **Điều kiện tiên quyết:** Thiết bị đã tắt toàn bộ kết nối mạng Wi-Fi và Dữ liệu di động (4G/5G).
- **Dữ liệu kiểm thử:** Email: `student_qa@gmail.com`, Mật khẩu: `123456`.
- **Các bước thực hiện:**
  1. Tắt toàn bộ Wi-Fi và Dữ liệu di động trên thiết bị kiểm thử.
  2. Mở ứng dụng, xác nhận đang ở tab Đăng nhập.
  3. Nhập Email `student_qa@gmail.com` và Mật khẩu `123456`.
  4. Nhấn nút "Đăng nhập".
- **Kết quả mong đợi quan sát được trên UI:**
  - Ứng dụng không chuyển màn hình.
  - Xuất hiện thông báo lỗi màu đỏ: *"Không có kết nối mạng. Vui lòng kiểm tra lại."*
  - Form đăng nhập vẫn giữ nguyên vẹn nội dung email và mật khẩu người dùng đã nhập, không bị xóa sạch.

---

### TC-BB-009G: Chuyển đổi tab Đăng nhập $\leftrightarrow$ Đăng ký và làm sạch thông báo lỗi cũ
- **Mục tiêu:** Xác minh giao diện ứng dụng quản lý trạng thái sạch sẽ, tự động xóa bỏ thông báo lỗi cũ khi người dùng chuyển đổi qua lại giữa hai tab.
- **Phân loại nguồn gốc:** Code-inferred / As-built behavior.
- **Kỹ thuật Black-box:** Kiểm thử trạng thái giao diện (UI State Integrity).
- **Điều kiện tiên quyết:** Đang ở tab Đăng nhập, màn hình đang hiển thị thông báo lỗi màu đỏ (tạo sẵn bằng cách bấm Đăng nhập khi form rỗng).
- **Dữ liệu kiểm thử:** Không nhập dữ liệu, tạo lỗi rỗng trước đó.
- **Các bước thực hiện:**
  1. Tại tab Đăng nhập đang hiển thị thông báo lỗi màu đỏ *"Vui lòng nhập đầy đủ Email và Mật khẩu."*.
  2. Chạm vào dòng chữ màu xanh "Đăng ký ngay" ở cuối màn hình.
  3. Quan sát giao diện chuyển sang tab Đăng ký (tiêu đề *"Tạo tài khoản mới"*, nút hiển thị *"Đăng ký"*).
  4. Chạm vào dòng chữ màu xanh "Đăng nhập" ở cuối màn hình để quay trở lại tab Đăng nhập.
- **Kết quả mong đợi quan sát được trên UI:**
  - Sau bước 2-3: Giao diện chuyển đổi trơn tru sang tab Đăng ký, không còn dòng thông báo lỗi cũ.
  - Sau bước 4: Giao diện quay lại tab Đăng nhập với nút hiển thị chữ *"Đăng nhập"*, dòng thông báo lỗi màu đỏ trước đó đã được làm sạch hoàn toàn, không xuất hiện lại.

---

## 6. QUY TẮC ĐẶT TÊN BẰNG CHỨNG KIỂM THỬ (EVIDENCE NAMING CONVENTION)

Để phục vụ công tác đối soát chất lượng và kiểm toán phần mềm, Tester phải lưu bằng chứng kiểm thử theo đúng quy tắc sau:

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN04_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Ví dụ minh họa:  
  • Đăng nhập thành công vào Trang chủ: `FN04_TC-BB-006_D01_01.png`  
  • Chuyển hướng sang màn hình Xác thực email: `FN04_TC-BB-006B_D01_01.png`  
  • Cắt tỉa khoảng trắng email thành công: `FN04_TC-BB-006C_D01_01.png`  
  • Email viết chữ IN HOA thành công: `FN04_TC-BB-006D_D01_01.png`  
  • Thông báo lỗi sai mật khẩu: `FN04_TC-BB-007_D01_01.png`  
  • Thông báo lỗi email thiếu ký tự `@`: `FN04_TC-BB-007B_D01_01.png`  
  • Thông báo lỗi email thiếu tên miền: `FN04_TC-BB-007B_D02_01.png`  
  • Thông báo lỗi tài khoản không tồn tại: `FN04_TC-BB-008_D01_01.png`  
  • An toàn trước chuỗi ký tự đặc biệt: `FN04_TC-BB-008B_D01_01.png`  
  • Thông báo lỗi bỏ trống mật khẩu: `FN04_TC-BB-009_D01_01.png`  
  • Thông báo lỗi bỏ trống email: `FN04_TC-BB-009B_D01_01.png`  
  • Thông báo lỗi bỏ trống cả 2 trường: `FN04_TC-BB-009C_D01_01.png`  
  • Chuyển đổi hiện mật khẩu: `FN04_TC-BB-009D_D01_01.png`, chuyển về ẩn: `FN04_TC-BB-009D_D01_02.png`  
  • Hộp thoại Quên mật khẩu: `FN04_TC-BB-009E_D01_01.png`  
  • Thông báo lỗi mất kết nối mạng: `FN04_TC-BB-009F_D01_01.png`  
  • Giao diện sạch lỗi sau khi chuyển tab: `FN04_TC-BB-009G_D01_01.png`
- **Video ghi màn hình (Screen Recording):**  
  Cấu trúc: `FN04_[TC-ID]_[Data-ID].mp4` (ví dụ `FN04_TC-BB-006_D01.mp4`).

---

## 7. DANH MỤC LỖI PHÁT HIỆN (BUG REPORT REFERENCE)

Dưới đây là các khiếm khuyết phần mềm (Discrepancies / Bugs) đã được phát hiện trong quá trình kiểm thử chức năng FN-04:

| Bug ID | TC-ID liên quan | Data ID | Tiêu đề lỗi & Mô tả hành vi thực tế | Mức độ nghiêm trọng | Trạng thái |
|:---:|:---:|:---:|:---|:---:|:---:|
| **BUG-BB-002** | **TC-BB-008** | **D01** | **Thông báo lỗi gộp khi đăng nhập tài khoản chưa tồn tại:**<br>• *Expected (Spec):* Ứng dụng hiển thị thông báo lỗi riêng biệt: *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."*<br>• *Actual (App):* Ứng dụng hiển thị thông báo gộp chung: *"Email hoặc mật khẩu không chính xác."* (Do thư viện Firebase Auth trả mã lỗi `invalid-credential` trên các phiên bản mới để phòng chống User Enumeration). | Minor | Open |
| **BUG-BB-003** | **TC-BB-007** | **D01** | **Thông báo lỗi gộp khi đăng nhập sai mật khẩu:**<br>• *Expected (Spec):* Ứng dụng hiển thị thông báo lỗi cụ thể: *"Mật khẩu không chính xác."*<br>• *Actual (App):* Ứng dụng hiển thị thông báo gộp chung: *"Email hoặc mật khẩu không chính xác."* (Do Firebase Auth trả mã lỗi `invalid-credential`). | Minor | Open |

> **Lưu ý về phân loại:**  
> - Chỉ có 2 khiếm khuyết ứng dụng được ghi nhận chính thức: **BUG-BB-002** (TC-BB-008) và **BUG-BB-003** (TC-BB-007).
> - Toàn bộ các vấn đề về Tiền đề / Dữ liệu kiểm thử (Precondition / Test Data) của `student_qa@gmail.com` và `unverified_qa@gmail.com` đã được chuẩn bị đầy đủ và xử lý dứt điểm, không còn ca kiểm thử nào bị BLOCKED.

---

## 8. BẢNG TỔNG KẾT THỰC THI (TEST EXECUTION SUMMARY)

| Chỉ số đo lường (Metrics) | Giá trị số lượng | Tỷ lệ (%) | Ghi chú giải thích |
|---|---:|---:|---|
| **Tổng số Test Case chính thức (Total Test Cases)** | **15** | 100% | Bao gồm 4 TC nguyên bản và 11 TC được bổ sung qua phân tích hộp đen chuyên sâu |
| **Tổng số lượt thực thi (Total Execution Items)** | **16** | 100% | 14 TC có 1 Data item; riêng TC-BB-007B có 2 Data items (D01: thiếu `@`, D02: thiếu domain) |
| **Số Test Case trực tiếp theo Yêu cầu (Requirement-based TCs)** | **5** | 33.33% | TC-BB-006, TC-BB-007, TC-BB-007B, TC-BB-008, TC-BB-009 |
| **Số Test Case suy diễn từ quy tắc bắt buộc (Requirement-derived TCs)** | **2** | 13.33% | TC-BB-009B, TC-BB-009C |
| **Số Test Case theo Hành vi thực tế (Code-inferred TCs)** | **8** | 53.33% | TC-BB-006B, TC-BB-006C, TC-BB-006D, TC-BB-008B, TC-BB-009D, TC-BB-009E, TC-BB-009F, TC-BB-009G |
| **Số lượng ca Đạt (PASS)** | **14** | **87.50%** | Đạt 100% mong đợi quan sát thực tế trên UI (14/16 items) |
| **Số lượng ca Không đạt (FAIL)** | **2** | **12.50%** | Actual khác Expected với precondition hợp lệ (BUG-BB-002, BUG-BB-003) (2/16 items) |
| **Số lượng ca Bị chặn (BLOCKED)** | **0** | **0.00%** | Toàn bộ điều kiện tiên quyết và dữ liệu kiểm thử đã được chuẩn bị hoàn tất (0/16 items) |
| **Số lượng ca Lỗi hệ thống kiểm thử (ERROR)** | **0** | **0.00%** | Không có lỗi phát sinh từ script hay môi trường điều khiển (0/16 items) |
| **Số khiếm khuyết ứng dụng ghi nhận (Application Bugs)** | **2** | - | BUG-BB-002 (TC-BB-008), BUG-BB-003 (TC-BB-007) |

> **Nguyên tắc phân định trạng thái thực thi:**
> - **PASS:** Hành vi quan sát thực tế (Actual Result) khớp hoàn toàn với kết quả mong đợi (Expected Result) (14/16 items - 87.50%).
> - **FAIL:** Hành vi quan sát thực tế khác biệt so với kết quả mong đợi trong điều kiện tiên quyết (Precondition/Test Data) đã được thiết lập hợp lệ: BUG-BB-002 và BUG-BB-003 do Firebase trả thông báo lỗi gộp `invalid-credential` (2/16 items - 12.50%).
> - **BLOCKED:** Không còn ca kiểm thử nào bị BLOCKED sau khi dữ liệu kiểm thử được chuẩn bị đầy đủ trên Firebase Auth (0/16 items - 0.00%).

---

## 9. CHECKLIST BÀN GIAO KẾT QUẢ CHO TEST LEAD

- [x] Đã rà soát toàn bộ 10 nhóm kiểm thử hộp đen chuẩn cho chức năng Đăng nhập Email/Password.
- [x] Đã phân định rành mạch giữa **Requirement-based** và **Code-inferred / As-built behavior**.
- [x] Không sử dụng tên biến, tên hàm, mã Firebase hay chi tiết code nội bộ trong Expected Result.
- [x] Toàn bộ Expected Result được mô tả thuần túy dưới góc nhìn người dùng quan sát được trên giao diện (Observable UI).
- [x] Đã chuẩn hóa dữ liệu kiểm thử và phân tách rõ ràng tài khoản đã kích hoạt (`emailVerified: true`) và tài khoản chưa kích hoạt (`emailVerified: false`).
- [x] Đã lưu giữ đầy đủ mã lỗi và bằng chứng liên quan đến các sai lệch thực tế đã ghi nhận trước đây.