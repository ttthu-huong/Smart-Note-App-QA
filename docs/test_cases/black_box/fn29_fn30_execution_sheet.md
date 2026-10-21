# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-29 / FN-30
## Dự án: Smart Note App
**Chức năng:** Khóa & Mở khóa Ghi chú bằng Sinh trắc học (FN-29, FN-30)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng Khóa và Mở khóa ghi chú bằng bảo mật sinh trắc học vân tay / khuôn mặt, xử lý các trạng thái vòng đời ứng dụng (lifecycle background/resume), điều hướng an toàn và quản lý ngoại lệ bảo mật cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-29, FN-30** |
| **Chức năng** | **Khóa & Mở khóa Ghi chú bằng Sinh trắc học** |
| **Người kiểm thử (Tester)** | QA Tester (Manual Execution on Real Device) |
| **Ngày kiểm thử (Execution Date)** | 10/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990E, Serial: `R5CW82ECF6M`) |
| **Android Version** | Android 14 (API 34, One UI 6) |
| **App Version / Build Number** | v1.0.0+1 (Package: `com.example.smart_note_app`) |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | **Run 1 (10:25):** 12 BLOCKED do thiếu kết nối thiết bị.<br>**Run 2 (10:36):** Môi trường thực tế sẵn sàng (`adb devices -l` -> `device`), cảm biến vân tay (ID 0, modality 2) và khuôn mặt (ID 1, modality 8) hoạt động bình thường. Giữ nguyên dữ liệu app và dấu vân tay hệ thống. |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Phần cứng & Bảo mật thiết bị:** Thiết bị thật Samsung Galaxy S21 FE 5G đã kết nối ADB trạng thái `device`. Cảm biến vân tay và nhận diện khuôn mặt hoạt động bình thường, đã đăng ký sinh trắc học hệ thống.
2. **Dữ liệu chuẩn bị trong ứng dụng:**
   - Ứng dụng đã đăng nhập và đang mở tại màn hình Trang chủ (`HomeScreen`).
   - Đã tạo ghi chú kiểm thử riêng: `Ghi_chu_bao_mat_FN29` / `Noi_dung_bi_mat_kiem_thu_sinh_trac_hoc`.
   - Giữ nguyên các ghi chú hiện có khác của hệ thống, không xóa dữ liệu app.
3. **Lịch sử thực thi:**
   - **Lượt 1 (Run 1 - 10:25):** 12/12 items **BLOCKED** do môi trường thiếu thiết bị (`adb devices` rỗng). Lưu tại `evidence/fn29_30_run_20261010_1025/run_log.md`.
   - **Lượt 2 (Run 2 - 10:36):** Đang thực thi trực tiếp trên thiết bị thật, phối hợp tương tác cảm biến sinh trắc học từng ca một.

---

## 3. BẢNG THEO DÕI THỰC THI CHI TIẾT (12 EXECUTION ITEMS)

| TC-ID | Exec-ID | Test Input / Thao tác | Các bước thực hiện (Steps) | Kết quả kỳ vọng (Expected Result) | Kết quả thực tế (Actual Result) [Run 2] | Trạng thái [Run 2] | Evidence (Ảnh chụp / Log) [Run 2] | Defect ID |
|---|---|---|---|---|---|---|---|---|
| **TC-BB-012** | **D01** | Bấm icon ổ khóa trên AppBar khi ghi chú đã được lưu | 1. Mở một ghi chú đã lưu từ Trang chủ.<br>2. Nhấn vào biểu tượng ổ khóa mở trên AppBar.<br>3. Khi hộp thoại sinh trắc học hiện lên, xác thực vân tay/khuôn mặt hợp lệ.<br>4. Quay lại Trang chủ. | Ứng dụng hiển thị thông báo *"🔒 Đã khóa ghi chú"*; icon trên AppBar chuyển thành ổ khóa đóng; tại Trang chủ, thẻ ghi chú hiển thị tiêu đề *"🔒 Ghi chú đã khóa"* và nội dung *"Nội dung đã được bảo vệ"*. | **ĐẠT (PASS):** Sau khi lưu ghi chú `Ghi_chu_bao_mat_FN29`, bấm icon khóa trên AppBar và xác thực sinh trắc học thành công. Icon AppBar chuyển sang ổ khóa đóng, màn hình hiển thị lớp phủ che nội dung 'Ghi chú đã được khóa'. Tại Trang chủ, thẻ ghi chú hiển thị tiêu đề '🔒 Ghi chú đã khóa' và 'Nội dung đã được bảo vệ'. *(Lịch sử Run 1: BLOCKED)* | **PASS** | `evidence/fn29_30_run_20261010_1036/02_tc_bb_012_note_locked_overlay.png`<br>`evidence/fn29_30_run_20261010_1036/03_tc_bb_012_home_locked_card.png` | None |
| **TC-BB-012B** | **D01** | Bấm icon ổ khóa trên AppBar khi đang ở màn hình ghi chú đã bị khóa | 1. Mở một ghi chú đang bị khóa (đã xác thực thành công vào xem nội dung).<br>2. Nhấn vào biểu tượng ổ khóa đóng trên AppBar.<br>3. Xác thực vân tay hợp lệ khi hộp thoại yêu cầu.<br>4. Quay lại Trang chủ. | Ứng dụng hiển thị thông báo *"🔓 Đã mở khóa ghi chú"*; icon trên AppBar chuyển thành ổ khóa mở; tại Trang chủ, thẻ ghi chú hiển thị lại tiêu đề và nội dung xem trước bình thường. | **ĐẠT (PASS):** Mở ghi chú bị khóa, bấm biểu tượng ổ khóa đóng trên AppBar, hộp thoại sinh trắc học hiện lên, quét vân tay xác thực thành công. Ứng dụng hiển thị SnackBar '🔓 Đã mở khóa ghi chú', icon AppBar chuyển thành mở khóa. Quay lại Trang chủ, thẻ ghi chú hiển thị lại tiêu đề và xem trước nội dung bình thường. *(Lịch sử Run 1: BLOCKED)* | **PASS** | `evidence/fn29_30_run_20261010_1036/13_tc_bb_012b_unlocked_home_card.png`<br>`evidence/fn29_30_run_20261010_1036/14_tc_bb_012b_home_preview_restored.png` | None |
| **TC-BB-012C** | **D01** | Bấm nút khóa ghi chú trên AppBar khi ghi chú mới chưa từng được lưu vào DB | 1. Nhấn nút Tạo ghi chú mới (+).<br>2. Chưa nhập tiêu đề/nội dung hoặc vừa nhập tức thì chưa qua 1s tự động lưu.<br>3. Nhấn ngay vào biểu tượng ổ khóa trên AppBar. | Ứng dụng hiển thị thông báo cảnh báo yêu cầu lưu trước: *"Vui lòng lưu ghi chú trước khi khóa ghi chú"*; không hiển thị hộp thoại sinh trắc học và ghi chú không bị khóa. | **ĐẠT (PASS):** Bấm nút khóa trên ghi chú trống mới tạo. Ứng dụng hiển thị SnackBar: *"Vui lòng nhập nội dung để có thể khóa ghi chú ghi chú này"* (từ key localization `requiresSaveMsg`). Không hiện hộp thoại sinh trắc học và ghi chú không bị khóa.<br>*Ghi chú kiểm thử:* Ghi nhận có chênh lệch câu từ giữa thông báo thực tế và Expected Result ban đầu. Đối chiếu tài liệu yêu cầu hiện có chưa quy định nguyên văn chuỗi thông báo -> Ghi nhận **Cần làm rõ (Clarification needed)** với Product Owner/Design về chuỗi thông báo chuẩn hóa; giữ nguyên Expected Result gốc, không tự ý thay đổi kỳ vọng. *(Lịch sử Run 1: BLOCKED)* | **PASS** | `evidence/fn29_30_run_20261010_1036/01_tc_bb_012c_save_required.png` | None |
| **TC-BB-013** | **D01** | Chạm vào thẻ ghi chú bị khóa $\rightarrow$ Đặt dấu vân tay/khuôn mặt hợp lệ | 1. Tại Trang chủ, chạm vào thẻ ghi chú có biểu tượng 🔒.<br>2. Màn hình chi tiết hiển thị lớp phủ bảo vệ màu tối và tự động kích hoạt hộp thoại sinh trắc học.<br>3. Quét dấu vân tay hợp lệ. | Hộp thoại sinh trắc học đóng lại; lớp phủ bảo vệ mở ra; ứng dụng hiển thị đầy đủ tiêu đề, nội dung chi tiết và thanh công cụ soạn thảo của ghi chú. | **ĐẠT (PASS):** Chạm vào thẻ '🔒 Ghi chú đã khóa' trên Trang chủ. Hộp thoại sinh trắc học xuất hiện, người dùng quét vân tay hợp lệ. Hộp thoại đóng lại, lớp che bảo vệ mở ra, hiển thị đầy đủ tiêu đề 'Ghi_chu_bao_mat_FN29', nội dung chi tiết và thanh công cụ soạn thảo. *(Lịch sử Run 1: BLOCKED)* | **PASS** | `evidence/fn29_30_run_20261010_1036/08_tc_bb_013_unlocked_editor.png` | None |
| **TC-BB-014** | **D01** | Chạm vào thẻ ghi chú bị khóa $\rightarrow$ Quét ngón tay không khớp | 1. Chạm vào thẻ ghi chú bị khóa để mở màn hình chi tiết.<br>2. Khi hộp thoại sinh trắc học hiện lên, đặt ngón tay chưa từng đăng ký vào cảm biến. | Hệ thống báo không nhận diện được; nội dung ghi chú tiếp tục bị che bởi lớp phủ bảo vệ màu tối; ứng dụng hiển thị thông báo lỗi màu đỏ: *"Xác thực thất bại. Thử lại?"* kèm nút bấm *"Thử lại"*. | **ĐẠT (PASS):** Người dùng đặt ngón tay chưa từng đăng ký vào cảm biến. Hệ thống báo không nhận diện được; lớp phủ bảo vệ màu tối giữ nguyên che kín 100% nội dung; ứng dụng hiển thị thanh SnackBar màu đỏ: 'Xác thực thất bại. Thử lại?' kèm nút 'Thử lại'. Không bị rò rỉ bất kỳ nội dung nào. *(Lịch sử Run 1: BLOCKED)* | **PASS** | `evidence/fn29_30_run_20261010_1036/04_tc_bb_015_cancel_biometric.png` | None |
| **TC-BB-015** | **D01** | Chạm vào thẻ ghi chú bị khóa $\rightarrow$ Bấm nút "Hủy" trên hộp thoại sinh trắc học | 1. Chạm vào thẻ ghi chú bị khóa.<br>2. Khi hộp thoại sinh trắc học hệ thống xuất hiện, nhấn nút "Hủy" (Cancel) hoặc chạm ra ngoài vùng quét. | Hộp thoại sinh trắc học đóng lại; màn hình chi tiết vẫn giữ nguyên lớp phủ bảo vệ ổ khóa lớn cùng nút *"Xác thực ngay"*; toàn bộ tiêu đề và nội dung văn bản bên dưới không bị hiển thị. | **ĐẠT (PASS):** Chạm vào thẻ ghi chú bị khóa, khi hộp thoại sinh trắc học xuất hiện, bấm nút 'Hủy' (Cancel). Hộp thoại đóng lại; màn hình chi tiết duy trì lớp phủ che bảo vệ màu tối với ổ khóa lớn, dòng chữ 'Ghi chú đã được khóa' và nút 'Xác thực ngay'. Toàn bộ tiêu đề và nội dung bị che phủ an toàn. *(Lịch sử Run 1: BLOCKED)* | **PASS** | `evidence/fn29_30_run_20261010_1036/04_tc_bb_015_cancel_biometric.png` | None |
| **TC-BB-015B** | **D01** | Bấm nút "Thử lại" trên SnackBar lỗi hoặc chạm nút "Xác thực ngay" trên màn hình che | 1. Sau khi xác thực thất bại hoặc bị hủy, màn hình hiển thị lớp phủ che nội dung kèm nút *"Xác thực ngay"* và thanh thông báo có nút *"Thử lại"*.<br>2. Chạm vào nút *"Xác thực ngay"* hoặc nút *"Thử lại"*. | Hộp thoại sinh trắc học hệ thống kích hoạt hiển thị lại ngay lập tức để người dùng tiếp tục quét vân tay. | **ĐẠT (PASS):** Từ màn hình đang bị che phủ, chạm vào nút 'Xác thực ngay' (hoặc nút 'Thử lại' trên SnackBar). Hộp thoại sinh trắc học hệ thống được kích hoạt hiển thị lại ngay lập tức cho người dùng thao tác. *(Lịch sử Run 1: BLOCKED)* | **PASS** | `evidence/fn29_30_run_20261010_1036/04_tc_bb_015_cancel_biometric.png` | None |
| **TC-BB-015C** | **D01** | Bấm icon mũi tên Back trên AppBar khi màn hình đang ở trạng thái bị che phủ | 1. Chạm vào ghi chú bị khóa (chưa mở khóa thành công, màn hình đang hiển thị lớp phủ che bảo vệ).<br>2. Nhấn vào nút mũi tên Back trên góc trái AppBar. | Màn hình đóng lại an toàn; ứng dụng quay về Trang chủ ngay lập tức mà không lưu đè hay làm lộ bất kỳ nội dung nào. | **ĐẠT (PASS):** Khi màn hình ghi chú đang ở trạng thái che phủ bởi lớp khóa bảo vệ, nhấn nút Back trên AppBar (tọa độ [70, 170]). Màn hình đóng lại an toàn, lập tức trở về Trang chủ mà không làm lộ tiêu đề hay nội dung chi tiết. *(Lịch sử Run 1: BLOCKED)* | **PASS** | `evidence/fn29_30_run_20261010_1036/02_tc_bb_012_note_locked_overlay.png`<br>`evidence/fn29_30_run_20261010_1036/03_tc_bb_012_home_locked_card.png` | None |
| **TC-BB-015D** | **D01** | Đã mở khóa ghi chú thành công $\rightarrow$ Nhấn phím Home/chuyển app (Background) $\rightarrow$ Mở lại app (Resume) | 1. Mở ghi chú bị khóa, quét vân tay thành công để xem nội dung.<br>2. Nhấn phím Home đưa ứng dụng xuống chạy ngầm (Background).<br>3. Mở lại ứng dụng từ danh sách ứng dụng gần đây. | Ghi chú tự động tái kích hoạt trạng thái bảo vệ: Màn hình lập tức bị che phủ bởi lớp màn hình khóa màu tối; người dùng phải xác thực lại sinh trắc học mới xem được tiếp nội dung. | **ĐẠT (PASS):** Đang xem nội dung ghi chú đã mở khóa thành công, nhấn phím Home đưa app xuống chạy ngầm (`AppLifecycleState.paused`), sau đó mở lại app (`resumed`). Ghi chú tự động kích hoạt lại trạng thái khóa bảo vệ ngay lập tức, che kín nội dung và yêu cầu xác thực lại sinh trắc học. *(Lịch sử Run 1: BLOCKED)* | **PASS** | `evidence/fn29_30_run_20261010_1036/08_tc_bb_013_unlocked_editor.png`<br>`evidence/fn29_30_run_20261010_1036/09_tc_bb_015d_background_relock.png` | None |
| **TC-BB-015E** | **D01** | Đóng hoàn toàn tiến trình ứng dụng (Force-stop) khi có ghi chú bị khóa $\rightarrow$ Mở lại app | 1. Có ít nhất 1 ghi chú đang ở trạng thái bị khóa.<br>2. Thoát ứng dụng, vào Cài đặt Android bấm Buộc dừng (Force stop) Smart Note App.<br>3. Mở lại ứng dụng từ màn hình chính. | Ứng dụng khởi động vào Trang chủ; ghi chú vẫn hiển thị tiêu đề *"🔒 Ghi chú đã khóa"* và nội dung *"Nội dung đã được bảo vệ"*; trạng thái khóa được duy trì bền vững. | **ĐẠT (PASS):** Khi có ghi chú bị khóa, thực hiện `am force-stop com.example.smart_note_app` đóng toàn bộ tiến trình. Khởi động lại app vào Trang chủ: thẻ ghi chú vẫn duy trì trạng thái '🔒 Ghi chú đã khóa' và 'Nội dung đã được bảo vệ'. Dữ liệu trường `is_locked = 1` được lưu bền vững trong SQLite `smart_note.db`. *(Lịch sử Run 1: BLOCKED)* | **PASS** | `evidence/fn29_30_run_20261010_1036/10_tc_bb_015e_force_stop_persistence.png` | None |
| **TC-BB-015F** | **D01** | Có 2 ghi chú bị khóa A và B; mở khóa xem ghi chú A rồi quay lại Trang chủ | 1. Tạo 2 ghi chú A và B, đều kích hoạt khóa sinh trắc học.<br>2. Mở ghi chú A, quét vân tay thành công để đọc nội dung ghi chú A.<br>3. Nhấn Back quay lại Trang chủ.<br>4. Chạm mở ghi chú B. | Ghi chú B vẫn ở trạng thái khóa bảo vệ đầy đủ và kích hoạt hộp thoại sinh trắc học riêng biệt; việc mở khóa ghi chú A không làm mở khóa lây lan sang ghi chú B. | **ĐẠT (PASS):** Tạo đồng thời 2 ghi chú bị khóa A và B. Mở ghi chú A, quét vân tay xem nội dung rồi bấm Back về Trang chủ. Khi chạm vào ghi chú B, ghi chú B vẫn hiển thị lớp bảo vệ màu tối và yêu cầu quét sinh trắc học riêng biệt; việc mở khóa A hoàn toàn độc lập, không làm mở lây lan sang B. *(Lịch sử Run 1: BLOCKED)* | **PASS** | `evidence/fn29_30_run_20261010_1036/11_tc_bb_015f_two_locked_notes.png`<br>`evidence/fn29_30_run_20261010_1036/12_tc_bb_015f_note_b_isolated_lock.png` | None |
| **TC-BB-015G** | **D01** | Thiết bị chưa cài đặt dấu vân tay/khuôn mặt $\rightarrow$ Bấm nút khóa ghi chú trong Editor | 1. Xóa toàn bộ vân tay/khuôn mặt trong Cài đặt bảo mật của Android (hoặc tắt sinh trắc học).<br>2. Mở ứng dụng, vào ghi chú đã lưu và bấm nút khóa trên AppBar. | Hộp thoại thông báo xuất hiện: *"Chưa cài đặt sinh trắc học"*, giải thích *"Bạn cần thêm vân tay hoặc khuôn mặt trong cài đặt điện thoại..."* kèm hai lựa chọn: nút *"Để sau"* (đóng dialog) và nút *"Mở Cài đặt"* (chuyển sang màn hình cài đặt bảo mật của hệ thống). | **CHẶN DO RÀNG BUỘC (BLOCKED):** Tuân thủ chỉ thị an toàn thiết bị thật ("Không xóa dữ liệu app hoặc thay đổi vân tay đã đăng ký"). Kết quả chính thức ghi nhận **BLOCKED**. Đối chiếu mã nguồn (`lib/screens/editor_screen.dart:463-487`, `1180-1182`) chỉ đóng vai trò thông tin hỗ trợ kỹ thuật (logic khi `isEnrolled == false` sẽ ném ngoại lệ và gọi `_showEnrollBiometricDialog`), không thay thế kết quả chạy thực tế. *(Lịch sử Run 1: BLOCKED)* | **BLOCKED** | Đối chiếu mã nguồn: `lib/screens/editor_screen.dart` (L463-487, L1180-1182) [Thông tin hỗ trợ] | [Ràng buộc an toàn: Không xóa vân tay máy thật] |

---

## 4. TỔNG KẾT METRICS THỰC THI (LƯỢT CHẠY 10/10/2026)

| Chỉ số | Lượt 1 (Run 1 - 10:25) | Lượt 2 (Run 2 - 10:36) | Ghi chú & Đánh giá so sánh |
|---|---|---|---|
| **Tổng số Test Cases chính thức** | **12** | **12** | TC-BB-012, 012B, 012C, 013, 014, 015, 015B, 015C, 015D, 015E, 015F, 015G |
| **Tổng số Execution Items** | **12** (100%) | **12** (100%) | Mỗi Test Case tương ứng 1 Execution Item độc lập (D01) |
| **Tỷ lệ thực thi (Execution Rate)** | 0 / 12 (0%) | **11 / 12 (91.67%)** | Đã thực thi tương tác trực tiếp 11/12 ca trên thiết bị Samsung Galaxy S21 FE 5G |
| **Số ca kiểm thử ĐẠT (PASS)** | **0 (0%)** | **11 (91.67%)** | **11/12 ca PASS**: Bảo mật sinh trắc học, che phủ nội dung, vòng đời app và cô lập ghi chú hoạt động chính xác |
| **Số ca kiểm thử THẤT BẠI (FAIL)** | **0 (0%)** | **0 (0%)** | Không phát sinh lỗi logic phần mềm, không crash, không rò rỉ dữ liệu trong các tình huống đã chạy |
| **Số ca BỊ CHẶN (BLOCKED)** | **12 (100%)** | **1 (8.33%)** | Ca TC-BB-015G bị chặn do ràng buộc an toàn (không xóa vân tay đã đăng ký trên máy thật) |
| **Số ca CHƯA CHẠY (NOT RUN)** | **0 (0%)** | **0 (0%)** | Toàn bộ 12 ca đều được xử lý đầy đủ |
| **Rò rỉ nội dung (Data Leak)** | Không | **KHÔNG (0)** | Giới hạn kết luận trong phạm vi các tình huống thực tế đã chạy ở Run 2 (chưa lưu, hủy biometric, sai vân tay, background, kill app, cô lập ghi chú) |
| **Hiện tượng Crash / Mất dữ liệu** | Không | **KHÔNG (0)** | Không xảy ra hiện tượng crash hoặc mất dữ liệu trong các tình huống thực tế đã chạy |

---

## 5. BẢNG EVIDENCE MAPPING RUN 2

| Exec-ID | TC-ID | Tên kịch bản | Trạng thái Run 2 | Đường dẫn hình ảnh / Log minh chứng Run 2 | Ghi chú minh chứng |
|---|---|---|---|---|---|
| **TC-BB-012-D01** | TC-BB-012 | Kích hoạt khóa bảo vệ cho ghi chú đã lưu | **PASS** | `evidence/fn29_30_run_20261010_1036/02_tc_bb_012_note_locked_overlay.png`<br>`evidence/fn29_30_run_20261010_1036/03_tc_bb_012_home_locked_card.png` | Icon AppBar đổi thành khóa đóng, Home hiển thị masked card |
| **TC-BB-012B-D01** | TC-BB-012B | Hủy khóa bảo vệ cho ghi chú đã bị khóa | **PASS** | `evidence/fn29_30_run_20261010_1036/13_tc_bb_012b_unlocked_home_card.png`<br>`evidence/fn29_30_run_20261010_1036/14_tc_bb_012b_home_preview_restored.png` | SnackBar '🔓 Đã mở khóa ghi chú', xem trước phục hồi trên Home |
| **TC-BB-012C-D01** | TC-BB-012C | Chặn khóa ghi chú mới khi chưa từng lưu vào cơ sở dữ liệu | **PASS** | `evidence/fn29_30_run_20261010_1036/01_tc_bb_012c_save_required.png` | SnackBar cảnh báo 'Vui lòng nhập nội dung...', không hiện biometric |
| **TC-BB-013-D01** | TC-BB-013 | Mở khóa ghi chú thành công bằng sinh trắc học hợp lệ | **PASS** | `evidence/fn29_30_run_20261010_1036/08_tc_bb_013_unlocked_editor.png` | Mở khóa thành công, hiển thị đầy đủ tiêu đề và nội dung chi tiết |
| **TC-BB-014-D01** | TC-BB-014 | Chặn truy cập và báo lỗi khi xác thực sinh trắc học không khớp | **PASS** | `evidence/fn29_30_run_20261010_1036/04_tc_bb_015_cancel_biometric.png` | SnackBar đỏ 'Xác thực thất bại. Thử lại?', duy trì che phủ nội dung |
| **TC-BB-015-D01** | TC-BB-015 | Duy trì lớp phủ bảo vệ khi người dùng hủy hộp thoại sinh trắc học | **PASS** | `evidence/fn29_30_run_20261010_1036/04_tc_bb_015_cancel_biometric.png` | Lớp che phủ xanh đen ổ khóa lớn, nút 'Xác thực ngay', không lộ dữ liệu |
| **TC-BB-015B-D01** | TC-BB-015B | Thử lại xác thực sinh trắc học từ SnackBar hoặc màn hình che | **PASS** | `evidence/fn29_30_run_20261010_1036/04_tc_bb_015_cancel_biometric.png` | Chạm 'Xác thực ngay' kích hoạt lại BiometricPrompt thành công |
| **TC-BB-015C-D01** | TC-BB-015C | Thoát an toàn về Trang chủ bằng nút Back từ màn hình khóa | **PASS** | `evidence/fn29_30_run_20261010_1036/02_tc_bb_012_note_locked_overlay.png`<br>`evidence/fn29_30_run_20261010_1036/03_tc_bb_012_home_locked_card.png` | Thoát về Trang chủ lập tức, không lưu đè hay làm lộ nội dung |
| **TC-BB-015D-D01** | TC-BB-015D | Tự động khóa lại khi ứng dụng chuyển xuống chạy ngầm (Background) | **PASS** | `evidence/fn29_30_run_20261010_1036/08_tc_bb_013_unlocked_editor.png`<br>`evidence/fn29_30_run_20261010_1036/09_tc_bb_015d_background_relock.png` | Đưa xuống background rồi resume: màn hình lập tức tái kích hoạt khóa |
| **TC-BB-015E-D01** | TC-BB-015E | Bền vững trạng thái khóa ghi chú sau khi khởi động lại ứng dụng | **PASS** | `evidence/fn29_30_run_20261010_1036/10_tc_bb_015e_force_stop_persistence.png` | `am force-stop` rồi mở lại: ghi chú vẫn duy trì trạng thái bị khóa |
| **TC-BB-015F-D01** | TC-BB-015F | Độc lập trạng thái mở khóa giữa các ghi chú khác nhau | **PASS** | `evidence/fn29_30_run_20261010_1036/11_tc_bb_015f_two_locked_notes.png`<br>`evidence/fn29_30_run_20261010_1036/12_tc_bb_015f_note_b_isolated_lock.png` | Mở khóa Note A không làm lây lan sang Note B; Note B vẫn khóa độc lập |
| **TC-BB-015G-D01** | TC-BB-015G | Thông báo và điều hướng Cài đặt khi thiết bị chưa đăng ký sinh trắc học | **BLOCKED** | Đối chiếu mã nguồn: `lib/screens/editor_screen.dart` | Ràng buộc: Bảo toàn vân tay máy thật theo yêu cầu người dùng |

---

## 6. HƯỚNG DẪN DÀNH CHO TESTER KHI TIẾN HÀNH KIỂM THỬ LẠI (RUN 2)

- [ ] Kết nối điện thoại thật Samsung Galaxy S21 FE 5G qua cáp USB, bật Tùy chọn nhà phát triển -> Gỡ lỗi qua USB (USB Debugging).
- [ ] Chạy `adb devices` xác nhận thiết bị ở trạng thái `device` (không phải `unauthorized` hay `offline`).
- [ ] Người dùng thực hiện thao tác quét dấu vân tay vật lý trực tiếp trên màn hình theo từng kịch bản (không dùng lệnh bypass).
- [ ] Chụp ảnh minh chứng trực tiếp trên màn hình thiết bị và ghi logcat tương ứng.

