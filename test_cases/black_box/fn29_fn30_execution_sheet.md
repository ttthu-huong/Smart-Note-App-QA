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
| **Ngày kiểm thử (Execution Date)** | 06/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (Android 14) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | v1.0.0+1 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | Thiết bị hỗ trợ cảm biến vân tay / nhận diện khuôn mặt; đã cài mã PIN màn hình |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Phần cứng & Bảo mật thiết bị:** Thiết bị kiểm thử đã thiết lập khóa màn hình (PIN/Pattern) và đã đăng ký ít nhất một dấu vân tay / khuôn mặt hợp lệ trong Cài đặt hệ thống (trừ các ca kiểm thử thiết bị chưa đăng ký sinh trắc học).
2. **Dữ liệu chuẩn bị trong ứng dụng:**
   - Ứng dụng đã đăng nhập và đang ở màn hình Trang chủ (`HomeScreen`).
   - Có ít nhất 1 ghi chú đã lưu trong cơ sở dữ liệu (`_hasBeenSavedInDb == true`) để thực hiện thao tác khóa.
   - Có 1 ghi chú mới tạo chưa từng lưu (chưa qua tự động lưu hay nhấn lưu) để kiểm thử chặn khóa ghi chú chưa lưu.
   - Có ít nhất 2 ghi chú bị khóa độc lập để kiểm thử tính riêng biệt khi mở khóa.

---

## 3. BẢNG THEO DÕI THỰC THI CHI TIẾT (12 EXECUTION ITEMS)

| TC-ID | Exec-ID | Test Input / Thao tác | Các bước thực hiện (Steps) | Kết quả kỳ vọng (Expected Result) | Kết quả thực tế (Actual Result) | Trạng thái (Status) | Evidence (Ảnh chụp) | Defect ID |
|---|---|---|---|---|---|---|---|---|
| **TC-BB-012** | **D01** | Bấm icon ổ khóa trên AppBar khi ghi chú đã được lưu | 1. Mở một ghi chú đã lưu từ Trang chủ.<br>2. Nhấn vào biểu tượng ổ khóa mở trên AppBar.<br>3. Khi hộp thoại sinh trắc học hiện lên, xác thực vân tay hợp lệ.<br>4. Quay lại Trang chủ. | Ứng dụng hiển thị thông báo *"🔒 Đã khóa ghi chú"*; icon trên AppBar chuyển thành ổ khóa đóng; tại Trang chủ, thẻ ghi chú hiển thị tiêu đề *"🔒 Ghi chú đã khóa"* và nội dung *"Nội dung đã được bảo vệ"*. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-012B** | **D01** | Bấm icon ổ khóa trên AppBar khi đang ở màn hình ghi chú đã bị khóa | 1. Mở một ghi chú đang bị khóa (đã xác thực thành công vào xem nội dung).<br>2. Nhấn vào biểu tượng ổ khóa đóng trên AppBar.<br>3. Xác thực vân tay hợp lệ khi hộp thoại yêu cầu.<br>4. Quay lại Trang chủ. | Ứng dụng hiển thị thông báo *"🔓 Đã mở khóa ghi chú"*; icon trên AppBar chuyển thành ổ khóa mở; tại Trang chủ, thẻ ghi chú hiển thị lại tiêu đề và nội dung xem trước bình thường. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-012C** | **D01** | Bấm nút khóa ghi chú trên AppBar khi ghi chú mới chưa từng được lưu vào DB | 1. Nhấn nút Tạo ghi chú mới (+).<br>2. Chưa nhập tiêu đề/nội dung hoặc vừa nhập tức thì chưa qua 1s tự động lưu.<br>3. Nhấn ngay vào biểu tượng ổ khóa trên AppBar. | Ứng dụng hiển thị thông báo cảnh báo yêu cầu lưu trước: *"Vui lòng lưu ghi chú trước khi khóa ghi chú"*; không hiển thị hộp thoại sinh trắc học và ghi chú không bị khóa. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-013** | **D01** | Chạm vào thẻ ghi chú bị khóa $\rightarrow$ Đặt dấu vân tay/khuôn mặt hợp lệ | 1. Tại Trang chủ, chạm vào thẻ ghi chú có biểu tượng 🔒.<br>2. Màn hình chi tiết hiển thị lớp phủ bảo vệ màu tối và tự động kích hoạt hộp thoại sinh trắc học.<br>3. Quét dấu vân tay hợp lệ. | Hộp thoại sinh trắc học đóng lại; lớp phủ bảo vệ mở ra; ứng dụng hiển thị đầy đủ tiêu đề, nội dung chi tiết và thanh công cụ soạn thảo của ghi chú. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-014** | **D01** | Chạm vào thẻ ghi chú bị khóa $\rightarrow$ Quét ngón tay không khớp | 1. Chạm vào thẻ ghi chú bị khóa để mở màn hình chi tiết.<br>2. Khi hộp thoại sinh trắc học hiện lên, đặt ngón tay chưa từng đăng ký vào cảm biến. | Hệ thống báo không nhận diện được; nội dung ghi chú tiếp tục bị che bởi lớp phủ bảo vệ màu tối; ứng dụng hiển thị thông báo lỗi màu đỏ: *"Xác thực thất bại. Thử lại?"* kèm nút bấm *"Thử lại"*. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-015** | **D01** | Chạm vào thẻ ghi chú bị khóa $\rightarrow$ Bấm nút "Hủy" trên hộp thoại sinh trắc học | 1. Chạm vào thẻ ghi chú bị khóa.<br>2. Khi hộp thoại sinh trắc học hệ thống xuất hiện, nhấn nút "Hủy" (Cancel) hoặc chạm ra ngoài vùng quét. | Hộp thoại sinh trắc học đóng lại; màn hình chi tiết vẫn giữ nguyên lớp phủ bảo vệ ổ khóa lớn cùng nút *"Xác thực ngay"*; toàn bộ tiêu đề và nội dung văn bản bên dưới không bị hiển thị. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-015B** | **D01** | Bấm nút "Thử lại" trên SnackBar lỗi hoặc chạm nút "Xác thực ngay" trên màn hình che | 1. Sau khi xác thực thất bại hoặc bị hủy, màn hình hiển thị lớp phủ che nội dung kèm nút *"Xác thực ngay"* và thanh thông báo có nút *"Thử lại"*.<br>2. Chạm vào nút *"Xác thực ngay"* hoặc nút *"Thử lại"*. | Hộp thoại sinh trắc học hệ thống kích hoạt hiển thị lại ngay lập tức để người dùng tiếp tục quét vân tay. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-015C** | **D01** | Bấm icon mũi tên Back trên AppBar khi màn hình đang ở trạng thái bị che phủ | 1. Chạm vào ghi chú bị khóa (chưa mở khóa thành công, màn hình đang hiển thị lớp phủ che bảo vệ).<br>2. Nhấn vào nút mũi tên Back trên góc trái AppBar. | Màn hình đóng lại an toàn; ứng dụng quay về Trang chủ ngay lập tức mà không lưu đè hay làm lộ bất kỳ nội dung nào. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-015D** | **D01** | Đã mở khóa ghi chú thành công $\rightarrow$ Nhấn phím Home/chuyển app (Background) $\rightarrow$ Mở lại app (Resume) | 1. Mở ghi chú bị khóa, quét vân tay thành công để xem nội dung.<br>2. Nhấn phím Home đưa ứng dụng xuống chạy ngầm (Background).<br>3. Mở lại ứng dụng từ danh sách ứng dụng gần đây. | Ghi chú tự động tái kích hoạt trạng thái bảo vệ: Màn hình lập tức bị che phủ bởi lớp màn hình khóa màu tối; người dùng phải xác thực lại sinh trắc học mới xem được tiếp nội dung. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-015E** | **D01** | Đóng hoàn toàn tiến trình ứng dụng (Force-stop) khi có ghi chú bị khóa $\rightarrow$ Mở lại app | 1. Có ít nhất 1 ghi chú đang ở trạng thái bị khóa.<br>2. Thoát ứng dụng, vào Cài đặt Android bấm Buộc dừng (Force stop) Smart Note App.<br>3. Mở lại ứng dụng từ màn hình chính. | Ứng dụng khởi động vào Trang chủ; ghi chú vẫn hiển thị tiêu đề *"🔒 Ghi chú đã khóa"* và nội dung *"Nội dung đã được bảo vệ"*; trạng thái khóa được duy trì bền vững. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-015F** | **D01** | Có 2 ghi chú bị khóa A và B; mở khóa xem ghi chú A rồi quay lại Trang chủ | 1. Tạo 2 ghi chú A và B, đều kích hoạt khóa sinh trắc học.<br>2. Mở ghi chú A, quét vân tay thành công để đọc nội dung ghi chú A.<br>3. Nhấn Back quay lại Trang chủ.<br>4. Chạm mở ghi chú B. | Ghi chú B vẫn ở trạng thái khóa bảo vệ đầy đủ và kích hoạt hộp thoại sinh trắc học riêng biệt; việc mở khóa ghi chú A không làm mở khóa lây lan sang ghi chú B. | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |
| **TC-BB-015G** | **D01** | Thiết bị chưa cài đặt dấu vân tay/khuôn mặt $\rightarrow$ Bấm nút khóa ghi chú trong Editor | 1. Xóa toàn bộ vân tay/khuôn mặt trong Cài đặt bảo mật của Android (hoặc tắt sinh trắc học).<br>2. Mở ứng dụng, vào ghi chú đã lưu và bấm nút khóa trên AppBar. | Hộp thoại thông báo xuất hiện: *"Chưa cài đặt sinh trắc học"*, giải thích *"Bạn cần thêm vân tay hoặc khuôn mặt trong cài đặt điện thoại..."* kèm hai lựa chọn: nút *"Để sau"* (đóng dialog) và nút *"Mở Cài đặt"* (chuyển sang màn hình cài đặt bảo mật của hệ thống). | [Chờ Tester thực thi] | [Chờ test] | Chưa có | [Không] |

---

## 4. TỔNG KẾT METRICS THỰC THI (CHƯA THỰC THI)

| Chỉ số | Số lượng | Tỷ lệ (%) | Ghi chú |
|---|---|---|---|
| **Tổng số Test Cases chính thức** | **12** | — | TC-BB-012, 012B, 012C, 013, 014, 015, 015B, 015C, 015D, 015E, 015F, 015G |
| **Tổng số Execution Items** | **12** | **100%** | Mỗi Test Case tương ứng 1 Execution Item độc lập (D01) |
| **Tỷ lệ thực thi (Execution Rate)** | 0 / 12 | 0% | Thiết kế hoàn tất, sẵn sàng thực thi (DESIGN — CHỜ TEST) |
| **Số ca kiểm thử ĐẠT (PASS)** | 0 | 0% | Đang chờ Tester trực tiếp kiểm thử trên thiết bị thật |
| **Số ca kiểm thử THẤT BẠI (FAIL)** | 0 | 0% | — |
| **Số ca kiểm thử BỊ CHẶN (BLOCKED)** | 0 | 0% | — |
| **Số ca GẶP LỖI MÔI TRƯỜNG (ERROR)** | 0 | 0% | — |
| **Tổng số lỗi phát hiện (Defects Found)** | 0 | — | Chưa ghi nhận |

---

## 5. BẢNG EVIDENCE MAPPING (CHỜ ĐIỀN)

| Exec-ID | TC-ID | Tên kịch bản | Trạng thái | Đường dẫn hình ảnh minh chứng | Ghi chú minh chứng |
|---|---|---|---|---|---|
| **TC-BB-012-D01** | TC-BB-012 | Kích hoạt khóa bảo vệ cho ghi chú đã lưu | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-012B-D01** | TC-BB-012B | Hủy khóa bảo vệ cho ghi chú đã bị khóa | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-012C-D01** | TC-BB-012C | Chặn khóa ghi chú mới khi chưa từng lưu vào cơ sở dữ liệu | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-013-D01** | TC-BB-013 | Mở khóa ghi chú thành công bằng sinh trắc học hợp lệ | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-014-D01** | TC-BB-014 | Chặn truy cập và báo lỗi khi xác thực sinh trắc học không khớp | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-015-D01** | TC-BB-015 | Duy trì lớp phủ bảo vệ khi người dùng hủy hộp thoại sinh trắc học | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-015B-D01** | TC-BB-015B | Thử lại xác thực sinh trắc học từ SnackBar hoặc màn hình che | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-015C-D01** | TC-BB-015C | Thoát an toàn về Trang chủ bằng nút Back từ màn hình khóa | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-015D-D01** | TC-BB-015D | Tự động khóa lại khi ứng dụng chuyển xuống chạy ngầm (Background) | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-015E-D01** | TC-BB-015E | Bền vững trạng thái khóa ghi chú sau khi khởi động lại ứng dụng | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-015F-D01** | TC-BB-015F | Độc lập trạng thái mở khóa giữa các ghi chú khác nhau | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |
| **TC-BB-015G-D01** | TC-BB-015G | Thông báo và điều hướng Cài đặt khi thiết bị chưa đăng ký sinh trắc học | [Chờ test] | *Chưa có* | Chờ Tester gửi evidence |

---

## 6. HƯỚNG DẪN DÀNH CHO TESTER KHI BẮT ĐẦU THỰC THI THỰC TẾ

- [ ] Thực hiện đầy đủ 12 execution items của chức năng FN-29 / FN-30.
- [ ] Sử dụng cảm biến vân tay hoặc nhận diện khuôn mặt thực tế của thiết bị (không dùng lệnh giả lập).
- [ ] Đánh giá trạng thái PASS / FAIL / BLOCKED cho cả 12 execution items.
- [ ] Chụp ảnh minh chứng rõ ràng cho từng bước hoặc màn hình kết quả tương ứng.
- [ ] Ghi chú rõ hành vi thực tế quan sát được vào cột `Actual Result`.
