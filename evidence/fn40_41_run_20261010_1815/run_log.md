# EXECUTION RUN AUDIT LOG — FN-40 / FN-41 (RUN 1)
**Thời điểm thực thi:** 2026-10-10 18:15:00 (GMT+7)  
**Nhóm chức năng:** FN-40 (Đồng bộ nhiều thiết bị) & FN-41 (Xử lý xung đột LWW)  
**Tài liệu kiểm thử tham chiếu:** [`test_cases/black_box/fn40_fn41_execution_sheet.md`](../../test_cases/black_box/fn40_fn41_execution_sheet.md)  
**Phương pháp:** Black-box Testing (Mô hình kiểm thử đồng bộ 2 thiết bị độc lập)

---

## 1. KIỂM TRA ĐIỀU KIỆN TIÊN QUYẾT (PRECONDITIONS CHECK)

### 1.1. Kiểm tra thiết bị thực tế qua ADB
- Lệnh kiểm tra: `adb devices -l`
- Kết quả trả về thực tế:
  ```text
  List of devices attached
  R5CW82ECF6M            device product:r9sxxx model:SM_G990E device:r9s transport_id:7
  ```
- **Số lượng thiết bị kết nối:** Duy nhất **1 thiết bị** (`Samsung Galaxy S21 FE 5G`, Serial: `R5CW82ECF6M`, Android 14).
- **Thiết bị thứ hai (Device B):** **KHÔNG CÓ (0)**. Không có thiết bị thứ hai kết nối qua USB hoặc Wi-Fi ADB.

### 1.2. Kiểm tra tiến trình máy ảo (Emulator / AVD)
- Lệnh kiểm tra: `Get-Process | Where-Object { $_.ProcessName -match "emulator|qemu" }`
- Kết quả: Không có tiến trình emulator nào đang chạy trên máy host.

### 1.3. Kiểm tra khả năng kiểm soát mạng độc lập
- Để kiểm thử FN-40 và FN-41, yêu cầu bắt buộc là Tester phải có khả năng ngắt mạng (chế độ máy bay) trên một thiết bị (Device A) trong khi thiết bị còn lại (Device B) vẫn duy trì kết nối mạng bình thường để thực hiện kịch bản chỉnh sửa/xóa song song và đồng bộ hai chiều.
- Do chỉ có 1 thiết bị, **hoàn toàn không thể kiểm soát mạng riêng biệt cho 2 thực thể độc lập**.

### 1.4. Kiểm tra tài khoản và Firebase
- Trên Thiết bị A (`R5CW82ECF6M`), ứng dụng `com.example.smart_note_app` đã được cài đặt và có kết nối Internet.
- Tuy nhiên, việc đồng bộ giữa 2 thiết bị (Cross-device Sync) yêu cầu cùng lúc 2 thiết bị cùng đăng nhập tài khoản kiểm thử `student_qa@gmail.com` để quan sát sự thay đổi dữ liệu thời gian thực giữa 2 màn hình UI độc lập. Thiếu Thiết bị B khiến kịch bản không thể tiến hành.

---

## 2. KẾT LUẬN ĐIỀU KIỆN MÔI TRƯỜNG & ĐIỂM DỪNG

- **Ràng buộc chỉ thị:** 
  - *"Không mặc định có thiết bị thứ hai. Nếu thiếu điều kiện, báo BLOCKED và dừng lượt này; không tự cài emulator hoặc coi unit test là kết quả đồng bộ hai thiết bị."*
  - *"Dừng khi mất dữ liệu, đồng bộ sai tài khoản, crash hoặc phát hiện lỗi mới cần phân tích. Lưu bằng chứng; các items còn lại giữ NOT RUN/BLOCKED."*
- **Quyết định:** Dừng ngay lượt thực thi Run 1 của FN-40/FN-41 do **THIẾU ĐIỀU KIỆN MÔI TRƯỜNG PHẦN CỨNG (THIẾU THIẾT BỊ B)**.
- **Không tự ý can thiệp:**
  - Không tự cài đặt Android Virtual Device (AVD).
  - Không sử dụng kết quả Unit Test mock để thay thế cho hành vi kiểm thử đồng bộ thực tế trên thiết bị.
  - Không chỉnh sửa mã nguồn ứng dụng (`lib/`), chưa commit/push.

---

## 3. BẢNG TỔNG KẾT TRẠNG THÁI RUN 1 (10 EXECUTION ITEMS)

| STT | TC-ID | Exec-ID | Tên kịch bản | Kết quả kỳ vọng (Expected Result) | Kết quả thực tế (Actual Result) [Run 1] | Trạng thái |
|:---:|---|:---:|---|---|---|:---:|
| 01 | **TC-BB-030** | **D01** | Tạo ghi chú mới khi offline trên Thiết bị A $\rightarrow$ Khôi phục kết nối mạng | Sau khi bật lại mạng trên A, note tự động xuất hiện trên Trang chủ Thiết bị B | **BLOCKED:** Thiếu Thiết bị B; chỉ có 1 thiết bị thực tế `R5CW82ECF6M`. Không đủ môi trường kiểm thử 2 thiết bị. | **BLOCKED** |
| 02 | **TC-BB-030B** | **D01** | Chỉnh sửa nội dung ghi chú khi offline trên Thiết bị A $\rightarrow$ Khôi phục mạng | Thiết bị B tự động cập nhật nội dung văn bản mới sau khi A có mạng lại | **BLOCKED:** Thiếu Thiết bị B; chỉ có 1 thiết bị thực tế `R5CW82ECF6M`. Không đủ môi trường kiểm thử 2 thiết bị. | **BLOCKED** |
| 03 | **TC-BB-030C** | **D01** | Xóa vĩnh viễn ghi chú khi offline trên Thiết bị A $\rightarrow$ Khôi phục mạng | Hàng đợi xóa đẩy lên cloud; note tự biến mất khỏi Trang chủ và Thùng rác trên B | **BLOCKED:** Thiếu Thiết bị B; chỉ có 1 thiết bị thực tế `R5CW82ECF6M`. Không đủ môi trường kiểm thử 2 thiết bị. | **BLOCKED** |
| 04 | **TC-BB-030D** | **D01** | Ghim ghi chú khi offline trên Thiết bị A $\rightarrow$ Khôi phục mạng | Sau khi A có mạng, Thiết bị B tự động chuyển note lên khu vực "Được ghim" | **BLOCKED:** Thiếu Thiết bị B; chỉ có 1 thiết bị thực tế `R5CW82ECF6M`. Không đủ môi trường kiểm thử 2 thiết bị. | **BLOCKED** |
| 05 | **TC-BB-030E** | **D01** | Kích hoạt khóa bảo vệ khi offline trên Thiết bị A $\rightarrow$ Khôi phục mạng | Thẻ trên B tự động đổi sang icon 🔒, chạm vào yêu cầu xác thực sinh trắc học | **BLOCKED:** Thiếu Thiết bị B; chỉ có 1 thiết bị thực tế `R5CW82ECF6M`. Không đủ môi trường kiểm thử 2 thiết bị. | **BLOCKED** |
| 06 | **TC-BB-030F** | **D01** | Vuốt xuống (Pull-to-refresh) tại Trang chủ Thiết bị B để chủ động kéo dữ liệu | Indicator xoay mượt, note mới từ A lập tức xuất hiện đầu trang trên B | **BLOCKED:** Thiếu Thiết bị B; chỉ có 1 thiết bị thực tế `R5CW82ECF6M`. Không đủ môi trường kiểm thử 2 thiết bị. | **BLOCKED** |
| 07 | **TC-BB-031** | **D01** | Hai thiết bị cùng sửa 1 note — B online sửa sau ($t_B > t_A$) $\rightarrow$ Giữ bản B (LWW) | Cả 2 máy thống nhất hiển thị bản B, ghi đè bản A cũ hơn, 0 nhân đôi note | **BLOCKED:** Thiếu Thiết bị B; chỉ có 1 thiết bị thực tế `R5CW82ECF6M`. Không thể tạo và đo xung đột LWW trên 2 máy. | **BLOCKED** |
| 08 | **TC-BB-031B** | **D01** | Hai thiết bị cùng sửa 1 note — A offline sửa sau ($t_A > t_B$) $\rightarrow$ Bản A ghi đè B | Khi A có mạng lại, hệ thống nhận diện $t_A > t_B$, cả 2 máy thống nhất hiển thị bản A | **BLOCKED:** Thiếu Thiết bị B; chỉ có 1 thiết bị thực tế `R5CW82ECF6M`. Không thể tạo và đo xung đột LWW trên 2 máy. | **BLOCKED** |
| 09 | **TC-BB-031C** | **D01** | Xung đột Sửa offline trên A ($t_A$) và Chuyển vào Thùng rác trên B ($t_B$) | Cơ chế LWW ($t_A > t_B$) giữ bản sửa A trên Trang chủ cả 2 máy | **BLOCKED:** Thiếu Thiết bị B; chỉ có 1 thiết bị thực tế `R5CW82ECF6M`. Không thể tạo và đo xung đột LWW trên 2 máy. | **BLOCKED** |
| 10 | **TC-BB-031D** | **D01** | Đăng nhập tài khoản trên thiết bị mới $\rightarrow$ Tự động kéo toàn bộ dữ liệu về đầy đủ | Toàn bộ ghi chú trên đám mây được tải về đầy đủ, ghim/khóa hiển thị đúng | **BLOCKED:** Thiếu Thiết bị B mới/độc lập để thực hiện kiểm thử nạp dữ liệu sạch từ đám mây. | **BLOCKED** |

---

## 4. TỔNG KẾT METRICS RUN 1
- **Tổng số Execution Items:** 10 items
- **PASS:** 0 (0%)
- **FAIL:** 0 (0%)
- **BLOCKED:** 10 (100%)
- **Lý do BLOCKED:** Thiếu thiết bị thứ hai trong môi trường phần cứng kiểm thử (`adb devices` chỉ có 1 thiết bị vật lý duy nhất).
- **Trạng thái lượt:** DỪNG LƯỢT THỰC THI (BLOCKED). Chờ bổ sung thiết bị thứ hai để thực thi Run 2.
