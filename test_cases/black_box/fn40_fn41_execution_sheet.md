# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-40 / FN-41

**Chức năng:** Đồng bộ Offline/Online & Giải quyết xung đột LWW (FN-40, FN-41)  
**Tiêu chuẩn thiết kế:** IEEE 829 & ISTQB  
**Phương pháp:** Black-box Testing (Góc nhìn người dùng cuối qua mô hình 2 thiết bị đối chiếu trực tiếp trên UI)  
**Trạng thái tài liệu:** DESIGN — CHƯA THỰC THI / CHỜ TEST (Không điền trước kết quả thực thi hay bằng chứng giả)

---

## 1. THÔNG TIN MÔI TRƯỜNG KIỂM THỬ (TEST ENVIRONMENT)

| Thành phần | Thiết bị A (Device A) | Thiết bị B (Device B) |
| :--- | :--- | :--- |
| **Loại thiết bị** | Thiết bị thực tế (Physical Device) / Emulator | Thiết bị thực tế (Physical Device) / Emulator |
| **Model / Tên máy** | Samsung Galaxy S21 FE 5G (hoặc tương đương) | Google Pixel 6 / Android Virtual Device (AVD) |
| **Hệ điều hành** | Android 12+ | Android 12+ |
| **Tài khoản kiểm thử** | `student_qa@gmail.com` | `student_qa@gmail.com` (Cùng tài khoản) |
| **Kết nối mạng** | Wi-Fi / 4G (Có thể chủ động bật/tắt chế độ máy bay) | Wi-Fi / 4G ổn định |
| **Ứng dụng kiểm thử** | Smart Note App (Build mới nhất) | Smart Note App (Build mới nhất) |

---

## 2. TIỀN ĐIỀU KIỆN & DỮ LIỆU KIỂM THỬ (PRECONDITIONS)

1. **Cùng đăng nhập tài khoản kiểm thử duy nhất:** Cả Thiết bị A và Thiết bị B đều đã đăng nhập cùng tài khoản `student_qa@gmail.com`.
2. **Khả năng kiểm soát mạng độc lập:** Tester có thể chủ động ngắt mạng (bật chế độ máy bay) và khôi phục mạng trên từng thiết bị riêng biệt.
3. **Mô hình kiểm thử hai thiết bị (Cross-device Testing):** Mọi hành vi đồng bộ và xung đột được kiểm chứng bằng cách quan sát sự thay đổi trạng thái và nội dung ghi chú trực tiếp trên màn hình của hai thiết bị mà không cần can thiệp hay kiểm tra mã nguồn bên trong.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Kịch bản / Input | Các bước thực hiện | Expected Result | Actual Result | Trạng thái (PASS/FAIL/BLOCKED) | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-030** | **D01** | Tạo ghi chú mới khi offline trên Thiết bị A $\rightarrow$ Khôi phục kết nối mạng | 1. Trên Thiết bị A, bật chế độ máy bay (ngắt hoàn toàn kết nối Wi-Fi/4G).<br>2. Trên Thiết bị A, nhấn nút Tạo mới (+), nhập Tiêu đề: `"Kế hoạch khảo nghiệm offline"`, Nội dung: `"Nội dung được tạo độc lập khi thiết bị mất kết nối"`.<br>3. Nhấn nút Quay lại (Back) để lưu ghi chú vào máy; quan sát thẻ ghi chú xuất hiện trên Trang chủ Thiết bị A.<br>4. Tắt chế độ máy bay trên Thiết bị A (khôi phục mạng Internet).<br>5. Quan sát Thiết bị B (đang mở ứng dụng ở Trang chủ). | Trên Thiết bị A: Ghi chú hiển thị đầy đủ ngay sau khi tạo dù mất mạng.<br>Sau khi khôi phục mạng: Hệ thống tự động đồng bộ dữ liệu lên máy chủ đám mây; trên Thiết bị B, ghi chú mới `"Kế hoạch khảo nghiệm offline"` tự động xuất hiện trên danh sách Trang chủ với đầy đủ tiêu đề và nội dung xem trước mà không cần đăng nhập lại. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-030B** | **D01** | Chỉnh sửa nội dung ghi chú khi offline trên Thiết bị A $\rightarrow$ Khôi phục mạng | 1. Chuẩn bị sẵn ghi chú `"Ghi chú họp kỹ thuật"` hiển thị đồng bộ trên cả 2 máy (Nội dung gốc: `"Phiên bản gốc"`).<br>2. Trên Thiết bị A, bật chế độ máy bay.<br>3. Mở ghi chú `"Ghi chú họp kỹ thuật"` trên Thiết bị A, sửa nội dung thành: `"Cập nhật nội dung bổ sung lúc ngoại tuyến"`.<br>4. Nhấn nút Back để lưu thay đổi trên Thiết bị A.<br>5. Tắt chế độ máy bay trên Thiết bị A (khôi phục mạng).<br>6. Quan sát màn hình và mở ghi chú trên Thiết bị B. | Trên Thiết bị A: Nội dung ghi chú cập nhật văn bản mới ngay lập tức.<br>Sau khi khôi phục mạng trên Thiết bị A: Thiết bị B tự động cập nhật nội dung mới; khi mở ghi chú trên Thiết bị B, toàn bộ đoạn văn bản `"Cập nhật nội dung bổ sung lúc ngoại tuyến"` hiển thị đầy đủ và chính xác. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-030C** | **D01** | Xóa vĩnh viễn ghi chú khi offline trên Thiết bị A $\rightarrow$ Khôi phục mạng (Hàng đợi xóa) | 1. Chuẩn bị sẵn ghi chú `"Ghi chú tạm cần xóa"` hiển thị đồng bộ trên cả 2 máy.<br>2. Bật chế độ máy bay trên Thiết bị A.<br>3. Trên Thiết bị A, chuyển ghi chú `"Ghi chú tạm cần xóa"` vào Thùng rác.<br>4. Mở Thùng rác trên Thiết bị A, bấm Xóa vĩnh viễn ghi chú này và xác nhận.<br>5. Quan sát ghi chú biến mất hoàn toàn khỏi Thùng rác Thiết bị A.<br>6. Tắt chế độ máy bay trên Thiết bị A (khôi phục mạng).<br>7. Quan sát danh sách Trang chủ và Thùng rác trên Thiết bị B. | Trên Thiết bị A: Ghi chú bị xóa sạch khỏi bộ nhớ máy.<br>Sau khi Thiết bị A có mạng lại: Hệ thống tự động giải phóng hàng đợi xóa lên máy chủ đám mây; trên Thiết bị B, ghi chú `"Ghi chú tạm cần xóa"` tự động biến mất khỏi danh sách Trang chủ và Thùng rác, đảm bảo tính nhất quán dữ liệu giữa hai máy. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-030D** | **D01** | Ghim ghi chú khi offline trên Thiết bị A $\rightarrow$ Khôi phục mạng | 1. Chuẩn bị sẵn ghi chú bình thường `"Tài liệu tham khảo"` trên cả 2 máy.<br>2. Bật chế độ máy bay trên Thiết bị A.<br>3. Trên Thiết bị A, mở ghi chú `"Tài liệu tham khảo"` và nhấn biểu tượng ghim trên thanh AppBar.<br>4. Quay lại Trang chủ Thiết bị A: Quan sát ghi chú chuyển vào mục `"Được ghim"`.<br>5. Tắt chế độ máy bay trên Thiết bị A.<br>6. Quan sát vị trí hiển thị của ghi chú trên Trang chủ Thiết bị B. | Trên Thiết bị A: Ghi chú nằm ngay trong khu vực `"Được ghim"`.<br>Sau khi Thiết bị A có mạng lại: Thiết bị B tự động cập nhật; ghi chú `"Tài liệu tham khảo"` được tự động chuyển từ danh sách bình thường lên phân vùng `"Được ghim"` trên Trang chủ Thiết bị B. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-030E** | **D01** | Kích hoạt khóa bảo vệ cho ghi chú khi offline trên Thiết bị A $\rightarrow$ Khôi phục mạng | 1. Chuẩn bị sẵn ghi chú `"Báo cáo tài chính nội bộ"` trên cả 2 máy (Cả hai máy đều đã đăng ký sinh trắc học).<br>2. Bật chế độ máy bay trên Thiết bị A.<br>3. Mở ghi chú `"Báo cáo tài chính nội bộ"` trên Thiết bị A, bấm icon ổ khóa trên AppBar và quét vân tay thành công để kích hoạt khóa.<br>4. Trang chủ Thiết bị A hiển thị ghi chú với icon 🔒 và tiêu đề `"🔒 Ghi chú đã khóa"`.<br>5. Tắt chế độ máy bay trên Thiết bị A.<br>6. Quan sát thẻ ghi chú trên Thiết bị B và chạm vào thẻ để mở. | Sau khi Thiết bị A có mạng lại: Thẻ ghi chú trên Trang chủ Thiết bị B tự động chuyển sang hiển thị icon 🔒 cùng thông báo nội dung đã được bảo vệ.<br>Khi người dùng trên Thiết bị B chạm vào thẻ ghi chú, màn hình hiển thị lớp phủ bảo vệ màu tối và kích hoạt hộp thoại yêu cầu xác thực sinh trắc học mới cho phép xem nội dung. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-030F** | **D01** | Kéo vuốt xuống (Pull-to-refresh) tại Trang chủ trên Thiết bị B để chủ động kéo dữ liệu đồng bộ | 1. Trên Thiết bị A (đang online), tạo một ghi chú mới `"Nhiệm vụ đột xuất"`.<br>2. Trên Thiết bị B (đang ở Trang chủ), thực hiện thao tác vuốt từ trên xuống dưới (Pull down) tại danh sách ghi chú.<br>3. Quan sát biểu tượng xoay tiến trình làm mới (Refresh Indicator) xuất hiện và biến mất.<br>4. Kiểm tra danh sách ghi chú hiển thị trên Thiết bị B. | Biểu tượng làm mới xuất hiện xoay mượt mà ở đỉnh màn hình và tự động biến mất khi hoàn tất nạp dữ liệu.<br>Ghi chú mới `"Nhiệm vụ đột xuất"` lập tức xuất hiện ngay đầu danh sách Trang chủ trên Thiết bị B. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-031** | **D01** | Hai thiết bị cùng sửa 1 ghi chú — Thiết bị B online sửa sau ($t_B > t_A$) $\rightarrow$ Giữ bản B (LWW) | 1. Đảm bảo cùng ghi chú X (`"Biên bản họp dự án"`, nội dung ban đầu: `"Bản thảo lúc 08:30"`) đã đồng bộ sẵn trên cả 2 máy.<br>2. Trên Thiết bị A, bật chế độ máy bay lúc 09:00.<br>3. Trên Thiết bị A (offline, lúc 09:00 - $t_A$): Sửa nội dung thành `"Bản A sửa lúc 09:00"`, nhấn Back để lưu vào máy.<br>4. Trên Thiết bị B (online, lúc 09:05 - $t_B$, với $t_B > t_A$): Sửa cùng ghi chú X thành `"Bản B sửa lúc 09:05"`, nhấn Back để lưu lên đám mây.<br>5. Tắt chế độ máy bay trên Thiết bị A lúc 09:10 để kích hoạt đồng bộ hai chiều.<br>6. Chờ quá trình đồng bộ hoàn tất (3–5 giây).<br>7. Mở lại ghi chú X trên cả hai thiết bị. | Cả Thiết bị A và Thiết bị B đều hiển thị thống nhất phiên bản của Thiết bị B: `"Bản B sửa lúc 09:05"`.<br>Phiên bản cũ hơn (09:00 của máy A) được ghi đè tự động; trên Trang chủ cả hai máy chỉ có duy nhất 1 thẻ ghi chú X (không bị nhân đôi bản ghi, không lỗi xung đột). | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-031B** | **D01** | Hai thiết bị cùng sửa 1 ghi chú — Thiết bị A offline sửa sau ($t_A > t_B$) $\rightarrow$ Bản A ghi đè bản B | 1. Đảm bảo cùng ghi chú Y (`"Kế hoạch chạy thử"`, nội dung ban đầu: `"Bản kế hoạch lúc 09:30"`) đã đồng bộ sẵn trên cả 2 máy.<br>2. Trên Thiết bị A, bật chế độ máy bay lúc 09:55.<br>3. Trên Thiết bị B (online, lúc 10:00 - $t_B$): Sửa nội dung thành `"Bản B sửa online lúc 10:00"`, nhấn Back để lưu lên đám mây.<br>4. Trên Thiết bị A (offline, lúc 10:05 - $t_A$, với $t_A > t_B$): Sửa cùng ghi chú Y thành `"Bản A sửa offline sau cùng lúc 10:05"`, nhấn Back để lưu vào máy.<br>5. Tắt chế độ máy bay trên Thiết bị A lúc 10:10 để kích hoạt đồng bộ.<br>6. Chờ quá trình đồng bộ hoàn tất.<br>7. Mở ghi chú Y trên cả hai thiết bị. | Khi Thiết bị A có mạng lại, hệ thống nhận diện thời gian chỉnh sửa của Thiết bị A mới hơn dữ liệu hiện có trên đám mây ($t_A > t_B$), tự động đẩy bản của A lên thay thế.<br>Sau khi đồng bộ, cả Thiết bị A và Thiết bị B đều hiển thị thống nhất phiên bản sửa sau cùng của Thiết bị A: `"Bản A sửa offline sau cùng lúc 10:05"`. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-031C** | **D01** | Xung đột giữa Sửa offline trên Thiết bị A ($t_A$) và Chuyển vào Thùng rác trên Thiết bị B ($t_B$) | 1. Đảm bảo cùng ghi chú Z (`"Quy trình vận hành"`, nội dung ban đầu: `"Bản gốc quy trình lúc 09:00"`) đã đồng bộ sẵn trên cả 2 máy.<br>2. Trên Thiết bị A, bật chế độ máy bay lúc 09:55.<br>3. Trên Thiết bị B (online, lúc 10:00 - $t_B$): Chuyển ghi chú Z vào Thùng rác (ghi chú biến mất khỏi Trang chủ và vào Thùng rác trên B).<br>4. Trên Thiết bị A (offline, lúc 10:05 - $t_A$, với $t_A > t_B$): Mở ghi chú Z, sửa nội dung thành `"Bản A cập nhật khẩn cấp lúc 10:05"`, nhấn Back để lưu vào máy.<br>5. Tắt chế độ máy bay trên Thiết bị A lúc 10:10. Chờ hai máy đồng bộ.<br>6. Kiểm tra vị trí hiển thị (Trang chủ/Thùng rác) và nội dung của ghi chú Z trên cả 2 máy. | **Theo source code (As-built Oracle):** Do $t_A = 10:05 > t_B = 10:00$, cơ chế LWW nhận diện bản sửa của A mới hơn thao tác thùng rác của B $\rightarrow$ Ghi chú Z được giữ lại trên Trang chủ trên cả hai máy với nội dung `"Bản A cập nhật khẩn cấp lúc 10:05"`.<br>`[CẦN XEM XÉT THỦ CÔNG: Cần Test Lead xác nhận yêu cầu nghiệp vụ: ưu tiên nội dung sửa sau hay ưu tiên lệnh xóa của người dùng].` | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-031D** | **D01** | Đăng nhập tài khoản trên thiết bị mới $\rightarrow$ Toàn bộ dữ liệu đám mây tự động kéo về đầy đủ | 1. Tài khoản `student_qa@gmail.com` đã có sẵn nhiều ghi chú trên đám mây (gồm ghi chú thường, ghim, khóa).<br>2. Mở ứng dụng trên Thiết bị B vừa mới cài đặt (hoặc vừa đăng xuất sạch dữ liệu), nhập email `student_qa@gmail.com` và mật khẩu để đăng nhập.<br>3. Sau khi vào Trang chủ, quan sát quá trình tải dữ liệu.<br>4. Kiểm tra số lượng và danh sách các thẻ ghi chú hiển thị trên Trang chủ Thiết bị B. | Ứng dụng tự động kích hoạt tiến trình kéo toàn bộ ghi chú từ đám mây về lưu trữ trên Thiết bị B.<br>Trang chủ hiển thị đầy đủ, chính xác toàn bộ danh sách ghi chú của tài khoản: các ghi chú được ghim nằm đúng vị trí đầu trang, các ghi chú khóa hiển thị đúng biểu tượng 🔒, tiêu đề và nội dung xem trước hiển thị trọn vẹn, không xảy ra hiện tượng mất mát dữ liệu hay sai lệch giao diện. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |

---

## 4. TỔNG KẾT METRICS THỰC THI (CHƯA THỰC THI)

| Chỉ số | Số lượng | Tỷ lệ (%) | Ghi chú |
|---|---|---|---|
| **Tổng số Test Cases chính thức** | **10** | — | TC-BB-030, 030B, 030C, 030D, 030E, 030F, 031, 031B, 031C, 031D |
| **Tổng số Execution Items** | **10** | **100%** | Mỗi Test Case tương ứng 1 Execution Item độc lập (D01) |
| **Tỷ lệ thực thi (Execution Rate)** | 0 / 10 | 0% | Thiết kế hoàn tất, sẵn sàng thực thi (DESIGN — CHỜ TEST) |
| **Số lượng PASS** | 0 | 0% | Chưa chạy trên thiết bị |
| **Số lượng FAIL** | 0 | 0% | Chưa chạy trên thiết bị |
| **Số lượng BLOCKED** | 0 | 0% | Chưa chạy trên thiết bị |
| **Số Bug phát hiện** | 0 | — | Không tạo bug giả |

---

## 5. DANH MỤC BẰNG CHỨNG (EVIDENCE NAMING CONVENTION)

*Quy ước đặt tên ảnh và video đối chiếu giữa 2 thiết bị khi Tester thực hiện chạy test thực tế:*

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN40_41_[TC-ID]_[Data-ID]_[DevA/DevB/Result]_[STT].png`  
  Ví dụ:  
  • Ghi chú tạo offline trên Thiết bị A: `FN40_41_TC-BB-030_D01_DevA_01.png`  
  • Ghi chú xuất hiện trên Thiết bị B sau đồng bộ: `FN40_41_TC-BB-030_D01_DevB_01.png`  
  • Sửa nội dung trên Thiết bị A (offline): `FN40_41_TC-BB-030B_D01_DevA_01.png`  
  • Nội dung hiển thị trên Thiết bị B sau đồng bộ: `FN40_41_TC-BB-030B_D01_DevB_01.png`  
  • Sửa nội dung trên Thiết bị A (09:00): `FN40_41_TC-BB-031_D01_DevA_01.png`  
  • Sửa nội dung trên Thiết bị B (09:05): `FN40_41_TC-BB-031_D01_DevB_01.png`  
  • Kết quả sau đồng bộ hiển thị bản B trên cả hai máy: `FN40_41_TC-BB-031_D01_Result.png`
- **Video quay màn hình (Screen Recording):**  
  Cấu trúc: `FN40_41_[TC-ID]_[Data-ID].mp4`  
  Ví dụ: `FN40_41_TC-BB-030_D01.mp4`

---

## 6. HƯỚNG DẪN DÀNH CHO TESTER KHI BẮT ĐẦU THỰC THI THỰC TẾ

- [ ] Chuẩn bị sẵn 2 thiết bị (Thiết bị A và Thiết bị B) cùng cài đặt bản build mới nhất của ứng dụng.
- [ ] Đăng nhập cùng tài khoản `student_qa@gmail.com` trên cả hai thiết bị.
- [ ] Thực hiện đầy đủ 10 execution items của nhóm chức năng FN-40 / FN-41 theo đúng thứ tự các bước.
- [ ] Kiểm soát kết nối mạng chính xác bằng cách bật/tắt Chế độ máy bay trên Thiết bị A theo từng kịch bản.
- [ ] Quan sát sự thay đổi giao diện và nội dung trực tiếp trên màn hình của cả 2 thiết bị.
- [ ] Đánh giá trạng thái PASS / FAIL / BLOCKED cho từng execution item dựa trên kết quả quan sát thực tế.
- [ ] Chụp ảnh/quay video minh chứng rõ ràng thể hiện đồng thời trạng thái của cả Thiết bị A và Thiết bị B.
- [ ] Ghi chú rõ hành vi thực tế quan sát được vào cột `Actual Result`.

---

## 7. BÁO CÁO LỖI (BUG REPORT) & RETEST (TEMPLATE TRỐNG)

| Bug ID | TC-ID | Data ID | Mô tả lỗi quan sát được trên UI | Mức độ nghiêm trọng | Trạng thái |
|---|---|---|---|---|---|
| *[Trống]* | *[Trống]* | *[Trống]* | *Chưa thực thi — Chưa phát sinh bug* | *[Trống]* | *Open* |

---

## 8. DỌN DẸP DỮ LIỆU KIỂM THỬ (TEST DATA CLEANUP)

- Sau khi hoàn thành kiểm thử thực tế, xóa các ghi chú tạo thử nghiệm đồng bộ (`Kế hoạch khảo nghiệm offline`, các bản ghi xung đột X, Y, Z) trên một trong hai thiết bị để làm sạch danh sách cho các đợt kiểm thử tiếp theo.
