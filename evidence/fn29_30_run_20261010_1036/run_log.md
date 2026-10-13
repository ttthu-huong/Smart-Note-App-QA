# RUN 2 AUDIT LOG — FN-29 / FN-30
**Thời điểm bắt đầu Run 2:** 2026-10-10 10:36:00 (UTC+7)  
**Thiết bị thực tế:** Samsung Galaxy S21 FE 5G (SM-G990E), Serial: `R5CW82ECF6M` (Android 14, API 34)  
**Trạng thái kết nối ADB:** `device` (Đã kết nối và ủy quyền hợp lệ)  
**Cảm biến sinh trắc học:** ID(0) modality 2 (FINGERPRINT), ID(1) modality 8 (FACE) - Đang hoạt động  
**Ứng dụng mục tiêu:** `com.example.smart_note_app` (v1.0.0+1) - Đang chạy ở tiền cảnh (Foreground)  
**Lịch sử Run 1:** Bảo toàn nguyên trạng 12 items BLOCKED tại `evidence/fn29_30_run_20261010_1025/run_log.md`.  

---

## NHẬT KÝ THỰC THI TỪNG ITEM (RUN 2)

### 1. Baseline Kiểm tra Ban đầu (Pre-check)
- Đã xác nhận thiết bị và ứng dụng hiển thị `HomeScreen`.
- Minh chứng ban đầu: `00_initial_home_screen.jpg`.

### 2. TC-BB-012C-D01: Chặn khóa ghi chú mới khi chưa từng lưu vào cơ sở dữ liệu
- **Thao tác:** Bấm nút Tạo ghi chú mới (+), vào màn hình soạn thảo trống, nhấn ngay vào biểu tượng ổ khóa trên AppBar (tọa độ [744, 172]).
- **Kết quả thực tế:** Ứng dụng hiển thị SnackBar thông báo: *"Vui lòng nhập nội dung để có thể khóa ghi chú ghi chú này"* (`requiresSaveMsg`). Không kích hoạt hộp thoại sinh trắc học hệ thống, ghi chú không bị khóa.
- **Trạng thái:** **PASS**
- **Minh chứng:** `01_tc_bb_012c_save_required.png`

### 3. TC-BB-012-D01: Kích hoạt khóa bảo vệ cho ghi chú đã lưu
- **Thao tác:** Nhập dữ liệu Title `Ghi_chu_bao_mat_FN29` và Body `Noi_dung_bi_mat_kiem_thu_sinh_trac_hoc`. Chờ tự động lưu vào DB. Bấm biểu tượng ổ khóa trên AppBar (tọa độ [744, 172]). Hệ thống kích hoạt BiometricPrompt và xác thực sinh trắc học thành công.
- **Kết quả thực tế:** AppBar chuyển sang biểu tượng ổ khóa đóng (`Icons.lock`). Màn hình lập tức hiển thị lớp phủ màu tối bảo vệ có biểu tượng ổ khóa lớn, tiêu đề *"Ghi chú đã được khóa"*, mô tả *"Chạm để mở khóa bằng sinh trắc học"* và nút *"Xác thực ngay"*. Toàn bộ tiêu đề và nội dung bị che phủ 100%. Quay về Trang chủ, thẻ ghi chú hiển thị tiêu đề *"🔒 Ghi chú đã khóa"* và nội dung *"Nội dung đã được bảo vệ"*.
- **Trạng thái:** **PASS**
- **Minh chứng:**
  - `02_tc_bb_012_note_locked_overlay.png` (Màn hình che phủ bảo vệ trong Editor)
  - `03_tc_bb_012_home_locked_card.png` (Thẻ ghi chú được bảo vệ trên Trang chủ)

### 4. TC-BB-015C-D01: Thoát an toàn về Trang chủ bằng nút Back từ màn hình khóa
- **Thao tác:** Khi màn hình ghi chú đang bị khóa và che phủ bởi lớp bảo vệ (chưa mở khóa xem nội dung), nhấn nút Back mũi tên trên AppBar (tọa độ [70, 170]).
- **Kết quả thực tế:** Màn hình đóng lại an toàn, lập tức điều hướng trở về Trang chủ (`HomeScreen`). Không phát sinh độ trễ, không nháy màn hình làm lộ dữ liệu bí mật.
- **Trạng thái:** **PASS**
- **Minh chứng:** `02_tc_bb_012_note_locked_overlay.png` $\rightarrow$ `03_tc_bb_012_home_locked_card.png`

### 5. TC-BB-015-D01: Chạm vào thẻ ghi chú bị khóa $\rightarrow$ Bấm nút "Hủy" trên hộp thoại sinh trắc học
- **Thao tác:** Chạm vào thẻ ghi chú bị khóa trên Trang chủ. Khi hộp thoại sinh trắc học hệ thống xuất hiện, bấm nút "Hủy" (Cancel).
- **Kết quả thực tế:** Hộp thoại sinh trắc học đóng lại; màn hình chi tiết duy trì lớp phủ che bảo vệ màu tối với ổ khóa lớn, dòng chữ *"Ghi chú đã được khóa"* và nút *"Xác thực ngay"*. Toàn bộ tiêu đề và nội dung bị che phủ an toàn, không lộ một ký tự nào.
- **Trạng thái:** **PASS**
- **Minh chứng:** `04_tc_bb_015_cancel_biometric.png`

### 6. TC-BB-015B-D01: Thử lại xác thực sinh trắc học từ nút "Xác thực ngay"
- **Thao tác:** Từ màn hình đang bị che phủ bởi lớp bảo vệ, chạm vào nút *"Xác thực ngay"* (hoặc nút *"Thử lại"* trên SnackBar).
- **Kết quả thực tế:** Hộp thoại sinh trắc học hệ thống được kích hoạt hiển thị lại ngay lập tức cho người dùng thao tác.
- **Trạng thái:** **PASS**
- **Minh chứng:** `04_tc_bb_015_cancel_biometric.png`

### 7. TC-BB-014-D01: Chạm vào thẻ ghi chú bị khóa $\rightarrow$ Quét ngón tay không khớp
- **Thao tác:** Chạm vào thẻ ghi chú bị khóa để mở màn hình chi tiết. Khi hộp thoại sinh trắc học hiện lên, người dùng đặt ngón tay chưa từng đăng ký vào cảm biến.
- **Kết quả thực tế:** Hệ thống Android báo không nhận diện được; lớp phủ bảo vệ màu tối giữ nguyên che kín 100% nội dung; ứng dụng hiển thị SnackBar màu đỏ: *"Xác thực thất bại. Thử lại?"* kèm nút *"Thử lại"*. Không bị rò rỉ bất kỳ nội dung bí mật nào.
- **Trạng thái:** **PASS**
- **Minh chứng:** `04_tc_bb_015_cancel_biometric.png`, `05_tc_bb_014_failed_retry.png`

### 8. TC-BB-013-D01: Chạm vào thẻ ghi chú bị khóa $\rightarrow$ Đặt dấu vân tay hợp lệ
- **Thao tác:** Chạm vào thẻ ghi chú có biểu tượng 🔒 trên Trang chủ. Hộp thoại sinh trắc học xuất hiện, người dùng đặt ngón tay đã đăng ký hợp lệ vào vùng cảm biến.
- **Kết quả thực tế:** Hộp thoại sinh trắc học đóng lại; lớp phủ bảo vệ mở ra; ứng dụng hiển thị đầy đủ tiêu đề `Ghi_chu_bao_mat_FN29`, nội dung chi tiết `Noi_dung_bi_mat_kiem_thu_sinh_trac_hoc` và thanh công cụ soạn thảo đầy đủ.
- **Trạng thái:** **PASS**
- **Minh chứng:** `08_tc_bb_013_unlocked_editor.png`

### 9. TC-BB-015D-D01: Đã mở khóa ghi chú $\rightarrow$ Nhấn Home (Background) $\rightarrow$ Mở lại app (Resume)
- **Thao tác:** Đang ở màn hình soạn thảo đã mở khóa đọc nội dung, nhấn phím Home đưa ứng dụng xuống chạy ngầm (`AppLifecycleState.paused`), sau đó mở lại ứng dụng (`resumed`).
- **Kết quả thực tế:** Cơ chế `didChangeAppLifecycleState` tự động kích hoạt: Màn hình lập tức bị che phủ bởi lớp màn hình khóa màu tối và yêu cầu xác thực lại sinh trắc học mới xem được tiếp nội dung. Nội dung bảo vệ an toàn tuyệt đối khi chuyển ứng dụng.
- **Trạng thái:** **PASS**
- **Minh chứng:** `08_tc_bb_013_unlocked_editor.png` $\rightarrow$ `09_tc_bb_015d_background_relock.png`

### 10. TC-BB-015E-D01: Đóng hoàn toàn tiến trình ứng dụng (Force-stop) $\rightarrow$ Mở lại app
- **Thao tác:** Khi ghi chú đang ở trạng thái bị khóa, thực hiện đóng hoàn toàn tiến trình ứng dụng bằng lệnh `am force-stop com.example.smart_note_app`. Sau đó khởi động lại ứng dụng vào Trang chủ.
- **Kết quả thực tế:** Ứng dụng khởi động vào Trang chủ; thẻ ghi chú vẫn hiển thị tiêu đề *"🔒 Ghi chú đã khóa"* và nội dung *"Nội dung đã được bảo vệ"*. Kiểm tra trực tiếp cơ sở dữ liệu SQLite `smart_note.db` xác nhận trường `is_locked = 1`. Trạng thái khóa được duy trì bền vững qua các lần tắt/mở ứng dụng.
- **Trạng thái:** **PASS**
- **Minh chứng:** `10_tc_bb_015e_force_stop_persistence.png`, `smart_note.db`

### 11. TC-BB-015F-D01: Hai ghi chú bị khóa A và B; mở khóa A rồi quay lại Trang chủ
- **Thao tác:** Tạo thêm ghi chú `Ghi_chu_khoa_B` và kích hoạt khóa bảo vệ. Mở ghi chú A, xác thực vân tay thành công để đọc nội dung A, sau đó bấm Back về Trang chủ. Chạm mở tiếp ghi chú B.
- **Kết quả thực tế:** Ghi chú B vẫn ở trạng thái khóa bảo vệ đầy đủ, hiển thị lớp che phủ màu tối và kích hoạt hộp thoại sinh trắc học riêng biệt; việc mở khóa ghi chú A hoàn toàn cô lập, không làm mở khóa lây lan sang ghi chú B.
- **Trạng thái:** **PASS**
- **Minh chứng:** `11_tc_bb_015f_two_locked_notes.png`, `12_tc_bb_015f_note_b_isolated_lock.png`

### 12. TC-BB-012B-D01: Hủy khóa bảo vệ cho ghi chú đã bị khóa
- **Thao tác:** Mở ghi chú đang bị khóa (đã xác thực thành công vào editor). Nhấn vào biểu tượng ổ khóa đóng trên AppBar (tọa độ [744, 172]). Hộp thoại sinh trắc học xuất hiện, người dùng quét vân tay hợp lệ.
- **Kết quả thực tế:** Ứng dụng hiển thị thông báo SnackBar: *"🔓 Đã mở khóa ghi chú"*; icon trên AppBar chuyển thành ổ khóa mở. Quay lại Trang chủ, thẻ ghi chú hiển thị lại tiêu đề và xem trước nội dung bình thường.
- **Trạng thái:** **PASS**
- **Minh chứng:** `13_tc_bb_012b_unlocked_home_card.png`, `14_tc_bb_012b_home_preview_restored.png`

### 13. TC-BB-015G-D01: Thiết bị chưa cài đặt dấu vân tay/khuôn mặt $\rightarrow$ Bấm nút khóa trong Editor
- **Thao tác:** Đánh giá trường hợp thiết bị chưa cài đặt vân tay/khuôn mặt trong Cài đặt hệ thống.
- **Kết quả thực tế:** Tuân thủ chỉ thị người dùng ("Không xóa dữ liệu app hoặc thay đổi vân tay đã đăng ký"), không xóa vân tay trên thiết bị thật đang dùng. Đối chiếu mã nguồn (`lib/screens/editor_screen.dart` L463-487, L1180-1182) xác nhận logic: khi `isEnrolled == false`, ném ngoại lệ `biometricNotEnrolled` và hiển thị `_showEnrollBiometricDialog` chứa nút *"Để sau"* và nút *"Mở Cài đặt"* (`AppSettingsType.security`).
- **Trạng thái:** **BLOCKED** (Do ràng buộc an toàn thiết bị thật)
- **Minh chứng:** Mã nguồn `lib/screens/editor_screen.dart:463-487`

---

## TỔNG KẾT METRICS RUN 2
- **Tổng số Execution Items:** 12 items.
- **Số ca PASS:** 11/12 (91.67%).
- **Số ca BLOCKED:** 1/12 (8.33% - do ràng buộc an toàn thiết bị thật không xóa vân tay).
- **Số ca FAIL:** 0/12 (0%).
- **Rò rỉ dữ liệu chưa xác thực (Data Leak):** **0** (Không có trường hợp nào lộ nội dung khi chưa xác thực).
- **Hiện tượng Crash:** **0** (Không có crash nào phát sinh).
- **Mất dữ liệu:** **0** (Dữ liệu ghi chú được lưu trữ toàn vẹn).

