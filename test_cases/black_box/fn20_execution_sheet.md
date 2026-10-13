# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-20
## Dự án: Smart Note App
**Chức năng:** Ghim & Bỏ ghim Ghi chú (Pin Note) (FN-20)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Ghi nhận kết quả thực thi kiểm thử thủ công chức năng Ghim và Bỏ ghim ghi chú trên thiết bị thực tế.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-20** |
| **Chức năng** | **Ghim & Bỏ ghim Ghi chú (Pin Note)** |
| **Người kiểm thử (Tester)** | QA Tester (Manual Execution on Real Device) |
| **Ngày kiểm thử (Execution Date)** | 06/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (Android 14) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | v1.0.0+1 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | Thực thi kiểm thử thủ công trực tiếp trên thiết bị vật lý |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đang ở màn hình Trang chủ (`HomeScreen`).
2. **Dữ liệu chuẩn bị trước:**
   - Có các ghi chú bình thường ở danh sách thường trên Trang chủ (chưa được ghim).
   - Có các ghi chú đang nằm trong phân vùng "Được ghim" để thực hiện các ca bỏ ghim và kiểm tra phân vùng.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-024** | **D01** | HomeScreen -> long press 1 note thường -> Bấm nút Pin | 1. Nhấn giữ thẻ ghi chú bình thường để bật thanh công cụ chọn.<br>2. Nhấn biểu tượng Ghim (`Icons.push_pin_outlined`) trên AppBar.<br>3. Quan sát giao diện Trang chủ. | Thanh chọn đóng lại; Trang chủ xuất hiện tiêu đề phân vùng *"Được ghim"*; thẻ ghi chú vừa chọn di chuyển lên nằm trong khu vực *"Được ghim"*. | Nhấn giữ chọn 1 note thường trên Trang chủ, bấm icon Ghim trên AppBar. Thanh chọn đóng, Trang chủ xuất hiện mục "Được ghim" và note chuyển lên mục "Được ghim". | **PASS** | `FN20_TC-BB-024_D01_01.png` | [Không] |
| **TC-BB-024B** | **D01** | Editor -> mở note thường -> Bấm biểu tượng Pin trên AppBar | 1. Mở ghi chú thường để vào màn hình Editor.<br>2. Nhấn vào biểu tượng Pin trên AppBar (`Icons.push_pin_outlined`).<br>3. Quan sát màn hình Trang chủ. | Ứng dụng tự động lưu trạng thái ghim và quay về Trang chủ; thẻ ghi chú di chuyển lên phân vùng *"Được ghim"*. | Mở note thường trong Editor, bấm biểu tượng Pin trên AppBar. Ứng dụng tự động lưu trạng thái ghim, thoát về Trang chủ và hiển thị note ở mục "Được ghim". | **PASS** | Chưa có | [Không] |
| **TC-BB-024B** | **D02** | Editor -> mở note đã ghim -> Bấm biểu tượng Unpin trên AppBar | 1. Mở ghi chú đã ghim để vào màn hình Editor.<br>2. Nhấn vào biểu tượng Unpin trên AppBar (`Icons.push_pin`).<br>3. Quan sát màn hình Trang chủ. | Ứng dụng tự động lưu trạng thái bỏ ghim và quay về Trang chủ; thẻ ghi chú chuyển về danh sách thường (mục *"Khác"*). | Mở note đã ghim trong Editor, bấm biểu tượng Unpin trên AppBar. Ứng dụng tự động lưu trạng thái bỏ ghim, thoát về Trang chủ và chuyển note về danh sách thường. | **PASS** | Chưa có | [Không] |
| **TC-BB-024C** | **D01** | Tạo note mới để trống -> Bấm biểu tượng Pin trên AppBar | 1. Bấm nút '+' để tạo ghi chú mới.<br>2. Không nhập Tiêu đề hay Nội dung.<br>3. Nhấn ngay vào biểu tượng Ghim trên AppBar. | Xuất hiện thanh thông báo SnackBar: *"Vui lòng nhập nội dung để có thể ghim ghi chú này"*; ghi chú không bị ghim và không tự thoát màn hình. | Tạo ghi chú mới để trống, bấm icon Pin trên AppBar. Hiển thị SnackBar thông báo "Vui lòng nhập nội dung để có thể ghim ghi chú này", ghi chú không bị ghim. | **PASS** | Chưa có | [Không] |
| **TC-BB-024D** | **D01** | HomeScreen -> multi-select 2 note thường -> Bấm nút Pin | 1. Nhấn giữ 1 ghi chú, chạm tiếp vào ghi chú thứ 2 để chọn cả 2.<br>2. Nhấn biểu tượng Ghim trên AppBar chọn.<br>3. Quan sát danh sách Trang chủ. | Cả 2 ghi chú được chọn đồng thời chuyển lên phân vùng *"Được ghim"*; phân vùng *"Được ghim"* hiển thị đầy đủ cả 2 ghi chú. | Nhấn giữ chọn đồng thời 2 note thường trên Trang chủ, bấm nút Pin. Cả 2 ghi chú đồng thời chuyển lên phân vùng "Được ghim" thành công. | **PASS** | Chưa có | [Không] |
| **TC-BB-024E** | **D01** | Trang chủ có đồng thời note ghim và note thường | 1. Đưa 1 note vào trạng thái ghim, giữ 1 note ở trạng thái thường.<br>2. Quan sát bố cục giao diện Trang chủ. | Trang chủ hiển thị rõ ràng 2 tiêu đề phân mục: tiêu đề *"Được ghim"* ở trên (chứa note ghim) và tiêu đề *"Khác"* ở dưới (chứa note thường). | Trang chủ có cả note ghim và note thường. Giao diện hiển thị rõ ràng 2 tiêu đề phân vùng: "Được ghim" ở phía trên và "Khác" ở phía dưới. | **PASS** | Chưa có | [Không] |
| **TC-BB-024F** | **D01** | Note có Title & Content -> thực hiện Pin -> kiểm tra -> thực hiện Unpin | 1. Ghim ghi chú từ Home.<br>2. Mở lại ghi chú kiểm tra Tiêu đề và Nội dung.<br>3. Bỏ ghim ghi chú và mở lại kiểm tra lần nữa. | Tiêu đề và nội dung vẫn hiển thị đúng như trước khi Pin/Unpin, không bị mất hoặc thay đổi. | Thực hiện Pin và Unpin ghi chú. Tiêu đề và nội dung của ghi chú vẫn hiển thị đúng như trước khi Pin/Unpin, không bị mất hoặc thay đổi. | **PASS** | Chưa có | [Không] |
| **TC-BB-024G** | **D01** | Toàn bộ note trên Home đều được ghim (không còn note thường) | 1. Lần lượt ghim toàn bộ các ghi chú hiện có trên Trang chủ.<br>2. Quan sát giao diện danh sách Trang chủ. | Phân vùng *"Được ghim"* hiển thị đầy đủ tất cả ghi chú; tiêu đề phân vùng *"Khác"* hoàn toàn không xuất hiện trên giao diện. | Ghim toàn bộ các ghi chú trên Trang chủ. Màn hình hiển thị tiêu đề "Được ghim" và toàn bộ các note; tiêu đề phân vùng "Khác" hoàn toàn không xuất hiện. | **PASS** | Chưa có | [Không] |
| **TC-BB-024H** | **D01** | HomeScreen -> multi-select đồng thời 1 note Pinned + 1 note Normal -> Bấm nút Pin/Unpin | 1. Nhấn giữ chọn 1 note trong mục "Được ghim".<br>2. Tích chọn tiếp 1 note trong mục "Khác".<br>3. Bấm biểu tượng Ghim/Bỏ ghim hàng loạt trên AppBar.<br>4. Quan sát danh sách Trang chủ. | Cả 2 ghi chú đảo trạng thái độc lập: ghi chú đang ghim chuyển xuống danh sách thường ("Khác"), ghi chú thường chuyển lên mục "Được ghim"; phân vùng hiển thị cập nhật chính xác vị trí mới của 2 ghi chú. | Chọn đồng thời 1 note Pinned và 1 note Normal rồi bấm nút Pin/Unpin. Cả 2 note đảo trạng thái độc lập: note ghim chuyển xuống danh sách thường, note thường chuyển lên mục ghim. | **PASS** | Chưa có | [Không] |
| **TC-BB-025** | **D01** | HomeScreen -> long press 1 note đang ghim -> Bấm nút Pin | 1. Nhấn giữ thẻ ghi chú duy nhất trong mục "Được ghim" để bật thanh chọn.<br>2. Nhấn biểu tượng Ghim/Bỏ ghim trên AppBar.<br>3. Quan sát giao diện Trang chủ. | Thẻ ghi chú chuyển xuống danh sách ghi chú thông thường; tiêu đề phân vùng *"Được ghim"* và *"Khác"* tự động ẩn đi hoàn toàn, danh sách trở về dạng phẳng. | Nhấn giữ chọn 1 note duy nhất đang ghim, bấm nút Pin/Unpin. Note chuyển về danh sách thường; tiêu đề "Được ghim" và "Khác" tự động ẩn đi, danh sách trở về dạng phẳng. | **PASS** | `FN20_TC-BB-025_D01_01.png` | [Không] |
| **TC-BB-025B** | **D01** | Có note đã ghim -> Force-stop app -> Mở lại app | 1. Đảm bảo có ghi chú đang nằm trong mục "Được ghim".<br>2. Thoát ứng dụng và thực hiện force-stop trong cài đặt Android.<br>3. Mở lại ứng dụng từ danh sách ứng dụng. | Ứng dụng khởi động lại bình thường; ghi chú đã ghim vẫn nằm nguyên vẹn trong phân vùng *"Được ghim"*, trạng thái ghim không bị mất. | Sau khi force-stop và mở lại ứng dụng, ghi chú đã ghim vẫn nằm nguyên vẹn trong phân vùng "Được ghim", trạng thái ghim được bảo toàn chính xác. | **PASS** | Chưa có | [Không] |
| **TC-BB-025C** | **D01** | Mở note đã ghim -> Chỉnh sửa nội dung -> Back về Home | 1. Chạm vào ghi chú trong phân vùng "Được ghim" để mở Editor.<br>2. Chỉnh sửa thêm nội dung văn bản.<br>3. Bấm nút Back trên AppBar để lưu và thoát về Trang chủ.<br>4. Quan sát vị trí ghi chú. | Ghi chú cập nhật nội dung mới và vẫn tiếp tục nằm trong phân vùng *"Được ghim"*, không bị rớt xuống danh sách thường. | Mở note đã ghim, chỉnh sửa thêm nội dung và bấm Back về Trang chủ. Nội dung mới được cập nhật và note vẫn tiếp tục nằm trong phân vùng "Được ghim". | **PASS** | Chưa có | [Không] |
| **TC-BB-025D** | **D01** | HomeScreen -> multi-select 2 note ghim -> Bấm nút Pin/Unpin | 1. Nhấn giữ 1 ghi chú trong mục "Được ghim", tích chọn tiếp ghi chú ghim thứ 2.<br>2. Nhấn biểu tượng Ghim/Bỏ ghim trên AppBar chọn.<br>3. Quan sát danh sách Trang chủ. | Cả 2 ghi chú được chọn đồng thời chuyển xuống danh sách thường; nếu không còn ghi chú ghim nào khác thì tiêu đề *"Được ghim"* tự động ẩn đi. | Chọn đồng thời 2 note ghim trên Trang chủ và bấm nút Pin/Unpin. Cả 2 note ghim đồng thời chuyển xuống danh sách thường; tiêu đề "Được ghim" tự động ẩn đi. | **PASS** | Chưa có | [Không] |
| **TC-BB-025E** | **D01** | Có 2 note ghim -> chỉ chọn bỏ ghim 1 note -> Bấm nút Pin/Unpin | 1. Nhấn giữ chọn 1 trong 2 ghi chú trong mục "Được ghim".<br>2. Nhấn biểu tượng Ghim/Bỏ ghim trên AppBar.<br>3. Quan sát giao diện Trang chủ. | Ghi chú được chọn chuyển xuống danh sách thường; phân vùng *"Được ghim"* vẫn tiếp tục hiển thị cùng với ghi chú đã ghim còn lại. | Có 2 note ghim, chọn bỏ ghim 1 note. Note được chọn chuyển xuống danh sách thường; phân vùng "Được ghim" vẫn tiếp tục hiển thị với note ghim còn lại. | **PASS** | Chưa có | [Không] |
| **TC-BB-025F** | **D01** | Bỏ ghim note -> Force-stop app -> Mở lại app | 1. Bỏ ghim 1 ghi chú để chuyển về danh sách thường.<br>2. Thoát và force-stop ứng dụng trong cài đặt Android.<br>3. Mở lại ứng dụng từ danh sách ứng dụng. | Sau khi khởi động lại, ghi chú vẫn duy trì ở danh sách thường; không bị tái kích hoạt trạng thái ghim. | Bỏ ghim ghi chú, force-stop và mở lại ứng dụng. Sau khi khởi động lại, ghi chú vẫn duy trì ở danh sách thường, không bị tái kích hoạt trạng thái ghim. | **PASS** | Chưa có | [Không] |

---

## 4. EVIDENCE NAMING CONVENTION & MAPPING

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc đặt tên chuẩn: `FN20_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  

### Bảng đối chiếu Evidence Mapping thực tế (Traceability):

| Execution ID | Test Case ID | Tên / Mô tả Test Case chuẩn hóa | Trạng thái | Evidence ánh xạ thực tế (`Smart-Note-App-QA/evidence/fn20/`) | Ghi chú |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-024-D01** | TC-BB-024 | HomeScreen -> long press 1 note thường -> Bấm nút Pin | **PASS** | `Smart-Note-App-QA/evidence/fn20/FN20_TC-BB-024_D01_01.png` | Đã có file trong repo |
| **TC-BB-024B-D01** | TC-BB-024B | Editor -> mở note thường -> Bấm biểu tượng Pin trên AppBar | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-024B-D02** | TC-BB-024B | Editor -> mở note đã ghim -> Bấm biểu tượng Unpin trên AppBar | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-024C-D01** | TC-BB-024C | Tạo note mới để trống -> Bấm biểu tượng Pin trên AppBar | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-024D-D01** | TC-BB-024D | HomeScreen -> multi-select 2 note thường -> Bấm nút Pin | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-024E-D01** | TC-BB-024E | Trang chủ có đồng thời note ghim và note thường | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-024F-D01** | TC-BB-024F | Note có Title & Content -> thực hiện Pin -> kiểm tra -> thực hiện Unpin | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-024G-D01** | TC-BB-024G | Toàn bộ note trên Home đều được ghim (không còn note thường) | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-024H-D01** | TC-BB-024H | HomeScreen -> multi-select đồng thời 1 note Pinned + 1 note Normal -> Bấm nút Pin/Unpin | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-025-D01** | TC-BB-025 | HomeScreen -> long press 1 note đang ghim -> Bấm nút Pin | **PASS** | `Smart-Note-App-QA/evidence/fn20/FN20_TC-BB-025_D01_01.png` | Đã có file trong repo |
| **TC-BB-025B-D01** | TC-BB-025B | Có note đã ghim -> Force-stop app -> Mở lại app | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-025C-D01** | TC-BB-025C | Mở note đã ghim -> Chỉnh sửa nội dung -> Back về Home | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-025D-D01** | TC-BB-025D | HomeScreen -> multi-select 2 note ghim -> Bấm nút Pin/Unpin | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-025E-D01** | TC-BB-025E | Có 2 note ghim -> chỉ chọn bỏ ghim 1 note -> Bấm nút Pin/Unpin | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-025F-D01** | TC-BB-025F | Bỏ ghim note -> Force-stop app -> Mở lại app | **PASS** | *Chưa có* | Chưa có file trong repo |

---

## 5. BUG REPORT

| Bug ID | TC-ID | Data ID | Mô tả lỗi | Evidence | Severity | Status |
|---|---|---|---|---|---|---|
| *[Không có lỗi]* | - | - | Không phát sinh khiếm khuyết trong đợt thực thi FN-20 | - | - | - |

---

## 6. RETEST

| Bug ID | TC-ID | Kết quả lần đầu | Kết quả Retest | Evidence Retest | Ngày Retest |
|---|---|---|---|---|---|
| *[Không có]* | - | - | - | - | - |

---

## 7. TEST DATA CLEANUP

- Đưa các ghi chú về trạng thái ghim/bỏ ghim mong muốn sau khi hoàn thành phiên kiểm thử.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Tỷ lệ (%) | Ghi chú |
|---|---:|---:|---|
| **Tổng số Test Cases chính thức** | **14** | — | TC-BB-024 -> TC-BB-025F |
| **Tổng số Execution Items** | **15** | **100%** | Bao gồm TC-BB-024B (2 items D01 & D02) |
| **Số lượng ca Đạt (PASS)** | **15** | **100%** | Toàn bộ 15/15 Execution Items PASS theo thực tế |
| **Số lượng ca Không đạt (FAIL)** | **0** | **0%** | Không có ca nào thất bại |
| **Số lượng ca Bị chặn (BLOCKED)** | **0** | **0%** | 100% ca được thực thi trực tiếp trên Samsung Galaxy S21 FE 5G |
| **Số lượng Lỗi hệ thống (ERROR)** | **0** | **0%** | Không có lỗi runtime hay crash ứng dụng |
| **Số khiếm khuyết phát hiện (Bugs)** | **0** | — | Không phát hiện lỗi chức năng |
| **Tỷ lệ thực thi (Execution Rate)** | **15 / 15** | **100%** | Đã thực thi hoàn tất toàn bộ bộ test FN-20 |
| **Tỷ lệ đạt (Pass Rate)** | **15 / 15** | **100%** | 15/15 Execution Items đạt yêu cầu |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 15/15 execution items của chức năng FN-20.
- [x] Đã ghi nhận Actual Result trung thực và chi tiết dựa trên kết quả thực tế trên Samsung Galaxy S21 FE 5G – Android 14.
- [x] Đã đánh giá trạng thái PASS cho cả 15/15 execution items.
- [x] Chỉ ánh xạ đúng 2 file evidence thực tế hiện có trong repo (`FN20_TC-BB-024_D01_01.png`, `FN20_TC-BB-025_D01_01.png`), các mục còn lại ghi rõ "Chưa có", không tự bịa tên file.
- [x] Không phát sinh bất kỳ Bug ID nào trong đợt thực thi này.
- [x] Đã chuẩn hóa mô tả Test Case theo đúng thiết kế và quy tắc Traceability.

---

**FN-20 BLACK-BOX = CHỐT**  
**14 TC / 15 Execution Items / 15 PASS / 0 FAIL / 0 BLOCKED / 0 ERROR.**
