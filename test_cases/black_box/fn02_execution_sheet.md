# BẢNG THỰC THI KIỂM THỬ HỘP ĐEN (BLACK-BOX TEST EXECUTION SHEET)
## CHỨC NĂNG: ĐĂNG KÝ TÀI KHOẢN EMAIL/PASSWORD (FN-02)

- **Dự án:** Smart Note App
- **Chức năng kiểm thử:** FN-02 — Đăng ký tài khoản Email
- **Phương pháp kiểm thử:** Kiểm thử hộp đen thủ công (Manual Black-box Testing)
- **Tài liệu tham chiếu thiết kế:** `black_box_test_cases.md`
- **Mục tiêu tài liệu:** Cung cấp biểu mẫu thực thi chi tiết, rõ ràng từng bước để kiểm thử viên (Tester) mở ứng dụng trên thiết bị thật hoặc máy ảo, trực tiếp thao tác nhập liệu, đối chiếu màn hình và ghi nhận kết quả kiểm thử.

---

## 1. THÔNG TIN PHIÊN KIỂM THỬ (TEST SESSION INFORMATION)

| Mục thông tin | Chi tiết ghi nhận thực tế |
|---|---|
| **Mã chức năng (FN-ID)** | **FN-02** |
| **Tên chức năng** | **Đăng ký tài khoản Email/Password** |
| **Người thực hiện kiểm thử (Tester)** | [Điền họ tên khi test] |
| **Ngày thực hiện kiểm thử** | [Điền ngày thực hiện: DD/MM/YYYY] |
| **Thiết bị / Máy ảo kiểm thử** | [Điền tên thiết bị: VD: Pixel 7 / Samsung Galaxy S22 / Emulator] |
| **Hệ điều hành / Phiên bản Android** | [Điền phiên bản: VD: Android 13 / Android 14] |
| **Phiên bản ứng dụng (App Version / Build)** | [Điền phiên bản app đang cài đặt: VD: v1.0.0+1] |
| **Loại kết nối mạng** | [Wi-Fi / 4G / 5G] |
| **Ghi chú môi trường kiểm thử khác** | [Ghi nhận thêm nếu có: độ phân giải màn hình, tình trạng mạng...] |

---

## 2. ĐIỀU KIỆN CHUẨN BỊ TRƯỚC KHI THỰC HIỆN (PRECONDITIONS)

Trước khi bắt đầu thực hiện bất kỳ ca kiểm thử nào thuộc chức năng FN-02, Tester cần chuẩn bị đầy đủ các điều kiện tiên quyết sau:

1. **Ứng dụng đã sẵn sàng:** Ứng dụng Smart Note App đã được cài đặt hoàn tất trên thiết bị, mở được và hoạt động ổn định.
2. **Trạng thái đăng nhập:** Ứng dụng phải ở trạng thái **chưa đăng nhập tài khoản**. Nếu ứng dụng đang mở sẵn ở màn hình Trang chủ ghi chú, Tester phải thực hiện thao tác **Đăng xuất** để đưa ứng dụng quay về màn hình Đăng nhập ban đầu.
3. **Màn hình bắt đầu kiểm thử:** Tại màn hình Đăng nhập, Tester chạm vào dòng chữ **"Đăng ký ngay"** ở phía dưới để chuyển giao diện sang chế độ **Đăng ký** (nút bấm màu xanh hiển thị chữ **"Đăng ký"**, có 2 ô nhập: "Email" và "Mật khẩu").
4. **Kết nối mạng Internet:** Thiết bị phải có kết nối mạng Internet (Wi-Fi hoặc dữ liệu di động 4G/5G) hoạt động bình thường để gửi yêu cầu đăng ký lên hệ thống.
5. **Dữ liệu kiểm thử đã chuẩn bị:**
   - Email mới hoàn toàn chưa từng đăng ký: Dùng cấu trúc `student_qa_<thời_gian>@gmail.com` (ví dụ: `student_qa_20261004_01@gmail.com`) hoặc `student_bva_<thời_gian>@gmail.com`.
   - Email đã tồn tại sẵn trên hệ thống: Sử dụng tài khoản mẫu `student_qa@gmail.com` đã tạo trước đó để thực hiện ca kiểm thử trùng lặp.

---

## 3. BẢNG THỰC THI KIỂM THỬ TỔNG HỢP (TEST EXECUTION MATRIX)

> **Hướng dẫn cho Tester:**  
> - Thực hiện tuần tự từng dòng từ mục 1 đến mục 11.
> - Làm theo đúng các bước tại cột **Các bước thực hiện (Steps)** và nhập chính xác dữ liệu tại cột **Test Data**.
> - Quan sát giao diện thực tế và ghi nhận vào cột **Actual Result**.
> - So sánh giữa **Actual Result** và **Expected Result**: Nếu trùng khớp ghi **PASS**, nếu sai lệch ghi **FAIL**, nếu bị chặn do mạng/môi trường ghi **BLOCKED**.
> - Đặt tên file ảnh chụp màn hình tương ứng vào cột **Evidence ID**.

| STT | TC-ID | Data ID | Test Data | Các bước thực hiện (Steps) | Expected Result | Actual Result | Trạng thái (PASS / FAIL / BLOCKED) | Evidence ID | Bug ID | Tester Note |
|:---:|:---:|:---:|:---|:---|:---|:---|:---:|:---|:---:|:---|
| **1** | **TC-BB-001** | **D01** | • Email: `student_qa_<timestamp>@gmail.com`<br>*(email mới chưa từng đăng ký)*<br>• Mật khẩu: `123456` | 1. Chạm vào chữ "Đăng ký ngay" để chuyển sang giao diện Đăng ký.<br>2. Nhập Email mới vào ô "Email".<br>3. Nhập Mật khẩu `123456` vào ô "Mật khẩu".<br>4. Nhấn nút "Đăng ký". | Đăng ký thành công, ứng dụng chuyển sang màn hình Xác thực Email và hiển thị hướng dẫn kiểm tra email. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] | [Ghi chú] |
| **2** | **TC-BB-001** | **D02** | • Email: `user_dev_<timestamp>@outlook.com`<br>*(email mới chưa từng đăng ký)*<br>• Mật khẩu: `Abc@2026!` | 1. Đang ở giao diện Đăng ký.<br>2. Nhập Email Outlook mới vào ô "Email".<br>3. Nhập Mật khẩu phức tạp `Abc@2026!` vào ô "Mật khẩu".<br>4. Nhấn nút "Đăng ký". | Đăng ký thành công, ứng dụng chuyển sang màn hình Xác thực Email và hiển thị hướng dẫn kiểm tra email. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] | [Ghi chú] |
| **3** | **TC-BB-001** | **D03** | • Email: `sv_<timestamp>@hcmus.edu.vn`<br>*(email mới chưa từng đăng ký)*<br>• Mật khẩu: `MatKhauDai123` | 1. Đang ở giao diện Đăng ký.<br>2. Nhập Email giáo dục mới vào ô "Email".<br>3. Nhập Mật khẩu `MatKhauDai123` vào ô "Mật khẩu".<br>4. Nhấn nút "Đăng ký". | Đăng ký thành công, ứng dụng chuyển sang màn hình Xác thực Email và hiển thị hướng dẫn kiểm tra email. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] | [Ghi chú] |
| **4** | **TC-BB-002** | **D01** | • Email: `""`<br>• Mật khẩu: `""`<br>*(bỏ trống cả 2 ô)* | 1. Đang ở giao diện Đăng ký.<br>2. Để trống hoàn toàn ô "Email" và ô "Mật khẩu".<br>3. Nhấn nút "Đăng ký". | Ứng dụng không chuyển màn hình; xuất hiện khung thông báo lỗi màu đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] | [Ghi chú] |
| **5** | **TC-BB-003** | **D01** | • Email: `nguoidung_gmail.com`<br>*(thiếu ký tự @)*<br>• Mật khẩu: `123456` | 1. Đang ở giao diện Đăng ký.<br>2. Nhập Email thiếu ký tự `@` vào ô "Email".<br>3. Nhập Mật khẩu hợp lệ `123456`.<br>4. Nhấn nút "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."* | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] | [Ghi chú] |
| **6** | **TC-BB-003** | **D02** | • Email: `nguoidung@`<br>*(thiếu tên miền phía sau)*<br>• Mật khẩu: `123456` | 1. Đang ở giao diện Đăng ký.<br>2. Nhập Email có `@` nhưng bỏ trống tên miền vào ô "Email".<br>3. Nhập Mật khẩu hợp lệ `123456`.<br>4. Nhấn nút "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."* | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] | [Ghi chú] |
| **7** | **TC-BB-003** | **D03** | • Email: `test@tempmail.com`<br>*(thuộc tên miền email rác)*<br>• Mật khẩu: `123456` | 1. Đang ở giao diện Đăng ký.<br>2. Nhập Email thuộc tên miền rác (`tempmail.com`) vào ô "Email".<br>3. Nhập Mật khẩu hợp lệ `123456`.<br>4. Nhấn nút "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] | [Ghi chú] |
| **8** | **TC-BB-004** | **D01** | • Email: `student_bva_<timestamp>@gmail.com`<br>*(email mới chưa đăng ký)*<br>• Mật khẩu: `1` *(1 ký tự số)* | 1. Đang ở giao diện Đăng ký.<br>2. Nhập Email hợp lệ chưa từng đăng ký vào ô "Email".<br>3. Nhập Mật khẩu 1 ký tự (`1`) vào ô "Mật khẩu".<br>4. Nhấn nút "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."* | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] | [Ghi chú] |
| **9** | **TC-BB-004** | **D02** | • Email: `student_bva_<timestamp>@gmail.com`<br>*(email mới chưa đăng ký)*<br>• Mật khẩu: `12345` *(5 ký tự số)* | 1. Đang ở giao diện Đăng ký.<br>2. Nhập Email hợp lệ chưa từng đăng ký vào ô "Email".<br>3. Nhập Mật khẩu 5 ký tự (`12345`) vào ô "Mật khẩu".<br>4. Nhấn nút "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."* | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] | [Ghi chú] |
| **10** | **TC-BB-004** | **D03** | • Email: `student_bva_<timestamp>@gmail.com`<br>*(email mới chưa từng đăng ký)*<br>• Mật khẩu: `123456` *(6 ký tự số)* | 1. Đang ở giao diện Đăng ký.<br>2. Nhập Email hợp lệ chưa từng đăng ký vào ô "Email".<br>3. Nhập Mật khẩu 6 ký tự (`123456`) vào ô "Mật khẩu".<br>4. Nhấn nút "Đăng ký". | Đăng ký được chấp nhận, ứng dụng chuyển sang màn hình xác thực. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] | [Ghi chú] |
| **11** | **TC-BB-005** | **D01** | • Email: `student_qa@gmail.com`<br>*(tài khoản đã đăng ký trên hệ thống)*<br>• Mật khẩu: `123456` | 1. Đang ở giao diện Đăng ký.<br>2. Nhập địa chỉ Email đã tồn tại `student_qa@gmail.com` vào ô "Email".<br>3. Nhập Mật khẩu hợp lệ `123456`.<br>4. Nhấn nút "Đăng ký". | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Email này đã được sử dụng cho một tài khoản khác."* | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] | [Ghi chú] |

---

## 4. HƯỚNG DẪN CHI TIẾT TỪNG TEST CASE (DETAILED TEST EXECUTION CARDS)

### 4.1. Phiếu thực thi TC-BB-001

| Mục kiểm thử | Nội dung chi tiết |
|---|---|
| **Mã Test Case (TC-ID)** | **TC-BB-001** |
| **Tên kịch bản** | **Đăng ký tài khoản thành công với thông tin hợp lệ** |
| **Mục tiêu kiểm thử** | Xác minh hệ thống chấp nhận đăng ký khi người dùng nhập đúng định dạng Email mới chưa từng tồn tại và Mật khẩu từ 6 ký tự trở lên. |
| **Điều kiện tiên quyết** | Ứng dụng đang mở ở màn hình Đăng nhập; thiết bị kết nối mạng Internet ổn định. |
| **Các bước thao tác (Steps)** | 1. Chạm vào dòng liên kết **"Đăng ký ngay"** ở cuối màn hình để chuyển sang giao diện Đăng ký.<br>2. Nhập địa chỉ Email hợp lệ chưa từng đăng ký vào ô nhập "Email".<br>3. Nhập Mật khẩu hợp lệ (độ dài >= 6 ký tự) vào ô nhập "Mật khẩu".<br>4. Chạm vào nút bấm **"Đăng ký"**. |
| **Dữ liệu kiểm thử (Test Data)** | • **Biến thể D01:** Email: `student_qa_<timestamp>@gmail.com` \| Mật khẩu: `123456`<br>• **Biến thể D02:** Email: `user_dev_<timestamp>@outlook.com` \| Mật khẩu: `Abc@2026!`<br>• **Biến thể D03:** Email: `sv_<timestamp>@hcmus.edu.vn` \| Mật khẩu: `MatKhauDai123` |
| **Kết quả kỳ vọng (Expected Result)** | Ứng dụng xử lý thành công, chuyển sang màn hình Xác thực Email và hiển thị văn bản hướng dẫn người dùng kiểm tra hộp thư email. |
| **Kết quả thực tế (Actual Result)** | [Điền khi kiểm thử thực tế] |
| **Đánh giá kết quả (Result)** | [ ] PASS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] FAIL &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] BLOCKED |
| **Tệp bằng chứng (Evidence ID)** | [Điền tên file ảnh/video khi test] |
| **Mã lỗi phát hiện (Bug ID)** | [Ghi mã bug nếu kết quả FAIL, để trống nếu PASS] |

---

### 4.2. Phiếu thực thi TC-BB-002

| Mục kiểm thử | Nội dung chi tiết |
|---|---|
| **Mã Test Case (TC-ID)** | **TC-BB-002** |
| **Tên kịch bản** | **Chặn đăng ký khi bỏ trống toàn bộ dữ liệu** |
| **Mục tiêu kiểm thử** | Xác minh hệ thống không cho phép gửi yêu cầu và hiển thị cảnh báo lỗi yêu cầu nhập đầy đủ khi người dùng để trống cả Email và Mật khẩu. |
| **Điều kiện tiên quyết** | Ứng dụng đang ở màn hình Đăng ký. |
| **Các bước thao tác (Steps)** | 1. Đảm bảo ô nhập "Email" và ô nhập "Mật khẩu" đều để trống (không nhập bất kỳ ký tự nào).<br>2. Chạm vào nút bấm **"Đăng ký"**. |
| **Dữ liệu kiểm thử (Test Data)** | • **Biến thể D01:** Email: `""` \| Mật khẩu: `""` |
| **Kết quả kỳ vọng (Expected Result)** | Ứng dụng không chuyển màn hình; xuất hiện khung thông báo lỗi màu đỏ với nội dung: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* |
| **Kết quả thực tế (Actual Result)** | [Điền khi kiểm thử thực tế] |
| **Đánh giá kết quả (Result)** | [ ] PASS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] FAIL &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] BLOCKED |
| **Tệp bằng chứng (Evidence ID)** | [Điền tên file ảnh khi test] |
| **Mã lỗi phát hiện (Bug ID)** | [Ghi mã bug nếu kết quả FAIL, để trống nếu PASS] |

---

### 4.3. Phiếu thực thi TC-BB-003

| Mục kiểm thử | Nội dung chi tiết |
|---|---|
| **Mã Test Case (TC-ID)** | **TC-BB-003** |
| **Tên kịch bản** | **Chặn đăng ký khi Email không hợp lệ hoặc thuộc tên miền không được hỗ trợ** |
| **Mục tiêu kiểm thử** | Xác minh ứng dụng từ chối các email không hợp lệ hoặc thuộc tên miền không được hỗ trợ. |
| **Điều kiện tiên quyết** | Ứng dụng đang ở màn hình Đăng ký; thiết bị có kết nối mạng Internet. |
| **Các bước thao tác (Steps)** | 1. Nhập chuỗi Email cần kiểm tra (sai định dạng hoặc thuộc tên miền email rác) vào ô "Email".<br>2. Nhập Mật khẩu hợp lệ (>= 6 ký tự, ví dụ: `123456`) vào ô "Mật khẩu".<br>3. Chạm vào nút bấm **"Đăng ký"**. |
| **Dữ liệu kiểm thử (Test Data)** | • **Biến thể D01:** Email: `nguoidung_gmail.com` *(thiếu @)* \| Mật khẩu: `123456`<br>• **Biến thể D02:** Email: `nguoidung@` *(thiếu tên miền)* \| Mật khẩu: `123456`<br>• **Biến thể D03:** Email: `test@tempmail.com` *(tên miền rác)* \| Mật khẩu: `123456` |
| **Kết quả kỳ vọng (Expected Result)** | • **D01 & D02:** Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Định dạng email không hợp lệ."*<br>• **D03:** Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Không hỗ trợ tên miền email rác này. Vui lòng dùng Gmail, Yahoo, Outlook hoặc email giáo dục (.edu)."* |
| **Kết quả thực tế (Actual Result)** | [Điền khi kiểm thử thực tế] |
| **Đánh giá kết quả (Result)** | [ ] PASS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] FAIL &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] BLOCKED |
| **Tệp bằng chứng (Evidence ID)** | [Điền tên file ảnh khi test] |
| **Mã lỗi phát hiện (Bug ID)** | [Ghi mã bug nếu kết quả FAIL, để trống nếu PASS] |

---

### 4.4. Phiếu thực thi TC-BB-004

| Mục kiểm thử | Nội dung chi tiết |
|---|---|
| **Mã Test Case (TC-ID)** | **TC-BB-004** |
| **Tên kịch bản** | **Kiểm tra giá trị biên độ dài Mật khẩu (Boundary Value Analysis - BVA)** |
| **Mục tiêu kiểm thử** | Xác minh xử lý biên của trường Mật khẩu tại ngưỡng tối thiểu 6 ký tự (chặn khi mật khẩu < 6 ký tự, chấp nhận khi mật khẩu đạt từ 6 ký tự). |
| **Điều kiện tiên quyết** | Ứng dụng đang ở màn hình Đăng ký; thiết bị có kết nối mạng Internet. |
| **Các bước thao tác (Steps)** | 1. Nhập Email hợp lệ mới chưa từng đăng ký (`student_bva_<timestamp>@gmail.com`) vào ô "Email".<br>2. Nhập Mật khẩu theo độ dài biên cần kiểm thử (1 ký tự, 5 ký tự, 6 ký tự) vào ô "Mật khẩu".<br>3. Chạm vào nút bấm **"Đăng ký"**. |
| **Dữ liệu kiểm thử (Test Data)** | • **Biến thể D01:** Email: `student_bva_<timestamp>@gmail.com` \| Mật khẩu: `1` *(1 ký tự - cận dưới không hợp lệ)*<br>• **Biến thể D02:** Email: `student_bva_<timestamp>@gmail.com` \| Mật khẩu: `12345` *(5 ký tự - biên dưới không hợp lệ)*<br>• **Biến thể D03:** Email: `student_bva_<timestamp>@gmail.com` \| Mật khẩu: `123456` *(6 ký tự - điểm biên chuẩn hợp lệ)* |
| **Kết quả kỳ vọng (Expected Result)** | • **D01 & D02:** Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."*<br>• **D03:** Đăng ký được chấp nhận, ứng dụng chuyển sang màn hình xác thực. |
| **Kết quả thực tế (Actual Result)** | [Điền khi kiểm thử thực tế] |
| **Đánh giá kết quả (Result)** | [ ] PASS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] FAIL &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] BLOCKED |
| **Tệp bằng chứng (Evidence ID)** | [Điền tên file ảnh khi test] |
| **Mã lỗi phát hiện (Bug ID)** | [Ghi mã bug nếu kết quả FAIL, để trống nếu PASS] |

---

### 4.5. Phiếu thực thi TC-BB-005

| Mục kiểm thử | Nội dung chi tiết |
|---|---|
| **Mã Test Case (TC-ID)** | **TC-BB-005** |
| **Tên kịch bản** | **Chặn đăng ký khi Email đã tồn tại trên hệ thống** |
| **Mục tiêu kiểm thử** | Xác minh hệ thống không cho phép tạo tài khoản trùng lặp và hiển thị thông báo lỗi thích hợp khi người dùng đăng ký bằng email đã có tài khoản. |
| **Điều kiện tiên quyết** | Ứng dụng đang ở màn hình Đăng ký; tài khoản `student_qa@gmail.com` đã được đăng ký và tồn tại trên hệ thống; thiết bị có kết nối mạng Internet. |
| **Các bước thao tác (Steps)** | 1. Nhập địa chỉ Email đã tồn tại `student_qa@gmail.com` vào ô "Email".<br>2. Nhập Mật khẩu hợp lệ `123456` vào ô "Mật khẩu".<br>3. Chạm vào nút bấm **"Đăng ký"**. |
| **Dữ liệu kiểm thử (Test Data)** | • **Biến thể D01:** Email: `student_qa@gmail.com` \| Mật khẩu: `123456` |
| **Kết quả kỳ vọng (Expected Result)** | Ứng dụng không chuyển màn hình; hiển thị thông báo lỗi màu đỏ: *"Email này đã được sử dụng cho một tài khoản khác."* |
| **Kết quả thực tế (Actual Result)** | [Điền khi kiểm thử thực tế] |
| **Đánh giá kết quả (Result)** | [ ] PASS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] FAIL &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] BLOCKED |
| **Tệp bằng chứng (Evidence ID)** | [Điền tên file ảnh khi test] |
| **Mã lỗi phát hiện (Bug ID)** | [Ghi mã bug nếu kết quả FAIL, để trống nếu PASS] |

---

## 5. QUY TẮC ĐẶT TÊN BẰNG CHỨNG KIỂM THỬ (EVIDENCE NAMING CONVENTION)

Để phục vụ công tác nghiệm thu và đối soát giữa Bảng thực thi và thư mục lưu trữ ảnh chụp màn hình / video quay màn hình, toàn bộ bằng chứng cho chức năng **FN-02** phải được đặt tên thống nhất theo quy ước chuẩn:

### 5.1. Định dạng tên Ảnh chụp màn hình (Screenshot)
Cấu trúc chuẩn:  
`[FN-ID]_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`

Ví dụ áp dụng:
- **TC-BB-001 (D01 - Đăng ký thành công):**  
  • Màn hình khi vừa nhập xong form: `FN02_TC-BB-001_D01_01.png`  
  • Màn hình xác thực email xuất hiện sau khi bấm nút: `FN02_TC-BB-001_D01_02.png`
- **TC-BB-002 (D01 - Bỏ trống form):**  
  • Màn hình hiển thị khung lỗi đỏ *"Vui lòng nhập đầy đủ..."*: `FN02_TC-BB-002_D01_01.png`
- **TC-BB-003 (Email không hợp lệ):**  
  • Trường hợp thiếu ký tự @ (D01): `FN02_TC-BB-003_D01_01.png`  
  • Trường hợp thiếu tên miền phía sau @ (D02): `FN02_TC-BB-003_D02_01.png`  
  • Trường hợp email rác tempmail (D03): `FN02_TC-BB-003_D03_01.png`
- **TC-BB-004 (Biên độ dài mật khẩu):**  
  • Mật khẩu 1 ký tự (D01): `FN02_TC-BB-004_D01_01.png`  
  • Mật khẩu 5 ký tự (D02): `FN02_TC-BB-004_D02_01.png`  
  • Mật khẩu 6 ký tự chuyển sang màn hình xác thực (D03): `FN02_TC-BB-004_D03_01.png`
- **TC-BB-005 (Trùng email đã tồn tại):**  
  • Màn hình hiển thị thông báo lỗi trùng tài khoản (D01): `FN02_TC-BB-005_D01_01.png`

### 5.2. Định dạng tên Video quay màn hình (Screen Recording - nếu cần)
Cấu trúc chuẩn:  
`[FN-ID]_[TC-ID]_[Data-ID].mp4`

Ví dụ:  
- Video quay trọn vẹn luồng đăng ký thành công TC-BB-001 D01: `FN02_TC-BB-001_D01.mp4`

---

## 6. DANH MỤC LỖI PHÁT HIỆN (BUG REPORT REFERENCE)

> **Ghi chú:** Bảng này được Tester lập và điền vào khi phát hiện sự sai khác giữa phản hồi thực tế của ứng dụng (Actual Result) so với yêu cầu kiểm thử (Expected Result). Để trống toàn bộ khi chưa thực hiện kiểm thử hoặc chưa phát hiện lỗi.

| Mã Bug (Bug ID) | Mã Test Case (TC-ID) | Mã dữ liệu (Data ID) | Tóm tắt mô tả lỗi quan sát được | Tệp bằng chứng đính kèm (Evidence) | Mức độ nghiêm trọng (Severity) | Trạng thái xử lý (Status) |
|:---:|:---:|:---:|---|---|:---:|:---:|
| *[Trống]* | *[Trống]* | *[Trống]* | *[Ghi nhận khi có lỗi phát sinh]* | *[Tên file ảnh/video]* | *[Critical / Major / Minor]* | *[Open / In Progress / Fixed]* |

---

## 7. BẢNG TỔNG KẾT THỰC THI (TEST EXECUTION SUMMARY)

> **Ghi chú:** Các số liệu thống kê kết quả thực tế sẽ được Tester tính toán và điền vào bảng sau khi hoàn tất toàn bộ 11 mục kiểm thử.

| Chỉ số đo lường (Metrics) | Giá trị số lượng | Ghi chú giải thích |
|---|:---:|---|
| **Tổng số Test Case chính thức** | **5** | Bao gồm TC-BB-001, TC-BB-002, TC-BB-003, TC-BB-004, TC-BB-005 |
| **Tổng số mục thực thi (Execution Items)** | **11** | Bao phủ đầy đủ các biến thể dữ liệu (D01, D02, D03) |
| **Số ca ĐẠT (PASS)** | [Điền sau khi test] | Số lượng mục kiểm thử có Actual Result khớp hoàn toàn với Expected Result |
| **Số ca KHÔNG ĐẠT (FAIL)** | [Điền sau khi test] | Số lượng mục kiểm thử có lỗi phát sinh, giao diện phản hồi sai |
| **Số ca BỊ CHẶN (BLOCKED)** | [Điền sau khi test] | Số lượng mục không thể chạy do nguyên nhân ngoại cảnh (mất mạng, app crash...) |
| **Tổng số lỗi phát hiện (Bugs)** | [Điền sau khi test] | Tổng số mục ghi nhận trong Bảng danh mục lỗi phát hiện |
| **Tỷ lệ thực thi hoàn tất (Execution Rate)** | [Điền sau khi test] % | Công thức: `(PASS + FAIL) / 11 * 100%` |
| **Tỷ lệ kiểm thử thành công (Pass Rate)** | [Điền sau khi test] % | Công thức: `PASS / (PASS + FAIL) * 100%` |

---

## 8. CHECKLIST BÀN GIAO KẾT QUẢ CHO TEST LEAD

Trước khi nộp lại tài liệu thực thi kiểm thử FN-02 cho Test Lead, kiểm thử viên cần rà soát và đánh dấu kiểm tra (`[x]`) hoàn tất các tiêu chí sau:

- [ ] **Tiêu chí 1 — Độ bao phủ:** Đã thực hiện đầy đủ 100% các ca kiểm thử (5 Test Cases với trọn vẹn 11 Execution Items từ STT 1 đến STT 11).
- [ ] **Tiêu chí 2 — Ghi nhận kết quả thực tế:** Toàn bộ các ô tại cột `Actual Result` đều đã được mô tả trung thực, cụ thể theo đúng những gì quan sát được trên màn hình ứng dụng (không để trống bất kỳ dòng nào).
- [ ] **Tiêu chí 3 — Xác nhận trạng thái rõ ràng:** Tất cả 11 mục đều đã được đánh dấu rõ ràng là `PASS`, `FAIL`, hoặc `BLOCKED`.
- [ ] **Tiêu chí 4 — Lưu trữ bằng chứng đầy đủ:** Đã chụp màn hình kết quả cho từng mục thực thi và lưu trữ đúng tên file theo quy ước tại Mục 5 (đặc biệt bắt buộc đối với tất cả các ca FAIL).
- [ ] **Tiêu chí 5 — Đăng ký lỗi đầy đủ:** Tất cả các ca FAIL đều đã được tạo mã `Bug ID` và ghi nhận đầy đủ mô tả lỗi tại Mục 6 (Bug Report Reference).
- [ ] **Tiêu chí 6 — Tính toàn vẹn của kịch bản:** Giữ nguyên vẹn nội dung `Expected Result`, không tự ý chỉnh sửa nội dung kỳ vọng để phù hợp với lỗi của ứng dụng.
- [ ] **Tiêu chí 7 — Tính trung thực của kiểm thử:** Không đánh dấu `PASS` cho bất kỳ ca nào nếu chưa trực tiếp chạy và chưa lưu ảnh chụp màn hình bằng chứng.
- [ ] **Tiêu chí 8 — Đầy đủ thông tin môi trường:** Đã ghi rõ ràng và chính xác các thông tin về Thiết bị, Phiên bản Android, Bản build của app và Loại mạng tại Mục 1.
