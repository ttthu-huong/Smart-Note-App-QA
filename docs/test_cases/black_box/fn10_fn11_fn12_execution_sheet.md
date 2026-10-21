# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-10 / FN-11 / FN-12
## Dự án: Smart Note App
**Chức năng:** Quản lý vòng đời Ghi chú (Xóa vào Thùng rác, Khôi phục, Xóa vĩnh viễn) (FN-10, FN-11, FN-12)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Ghi nhận kết quả thực thi kiểm thử thủ công vòng đời ghi chú (chuyển thùng rác, khôi phục, xóa vĩnh viễn) trên thiết bị thực tế.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-10, FN-11, FN-12** |
| **Chức năng** | **Quản lý vòng đời Ghi chú (Xóa, Khôi phục, Xóa vĩnh viễn)** |
| **Người kiểm thử (Tester)** | QA Tester (Manual Execution on Real Device) |
| **Ngày kiểm thử (Execution Date)** | 06/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990E / Android 14) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | v1.0.0+1 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | Thực thi kiểm thử thủ công trực tiếp trên thiết bị vật lý |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đang ở màn hình Trang chủ (`HomeScreen`).
2. **Dữ liệu chuẩn bị trước:**
   - Có ít nhất một ghi chú trên Trang chủ để thực hiện xóa vào Thùng rác.
   - Có ghi chú nằm trong Thùng rác (`TrashScreen`) để thực hiện Khôi phục và Xóa vĩnh viễn.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-021** | **D01** | HomeScreen -> long press note -> Trash | 1. Nhấn giữ thẻ ghi chú trên Trang chủ để bật thanh chọn.<br>2. Nhấn biểu tượng Thùng rác trên thanh công cụ.<br>3. Quan sát thông báo SnackBar và danh sách Trang chủ.<br>4. Mở menu ngăn kéo (Drawer), chọn "Thùng rác". | Ghi chú biến mất khỏi Trang chủ; hiển thị SnackBar: *"Đã chuyển 1 ghi chú vào thùng rác"*; truy cập Thùng rác thấy ghi chú xuất hiện với đúng tiêu đề/nội dung (hiển thị mờ). | Nhấn giữ chọn 1 ghi chú trên Trang chủ và nhấn biểu tượng Thùng rác. Ghi chú biến mất khỏi Trang chủ, hiển thị SnackBar thông báo và ghi chú xuất hiện trong Thùng rác đúng như mong đợi. | **PASS** | `FN10_11_12_TC-BB-021_D01_01.png` | [Không] |
| **TC-BB-021B** | **D01** | HomeScreen -> chuyển note vào Trash -> Undo trên SnackBar | 1. Nhấn giữ thẻ ghi chú và bấm biểu tượng Thùng rác.<br>2. Khi thanh thông báo SnackBar xuất hiện, nhấn ngay nút "Hoàn tác".<br>3. Quan sát Trang chủ.<br>4. Mở Thùng rác kiểm tra. | Note quay lại Home và không nằm trong Trash; thẻ ghi chú lập tức xuất hiện trở lại trên Trang chủ; truy cập Thùng rác xác nhận ghi chú không bị đưa vào thùng rác. | Nhấn nút "Hoàn tác" trên thanh thông báo SnackBar. Ghi chú lập tức xuất hiện trở lại trên Trang chủ và không bị đưa vào Thùng rác. | **PASS** | Chưa có | [Không] |
| **TC-BB-021C** | **D01** | Editor -> menu 3 chấm -> "Xóa ghi chú" -> AlertDialog -> Hủy | 1. Mở ghi chú để vào màn hình Editor.<br>2. Nhấn biểu tượng 3 chấm ở góc phải thanh công cụ đáy.<br>3. Chọn "Xóa ghi chú".<br>4. Trên hộp thoại cảnh báo 'Xóa ghi chú?', nhấn nút "Hủy". | Hộp thoại đóng lại, người dùng vẫn ở màn hình Editor và ghi chú không bị xóa. | Tại màn hình Editor, mở menu 3 chấm chọn "Xóa ghi chú", nhấn "Hủy" trên hộp thoại cảnh báo. Hộp thoại đóng lại, người dùng vẫn ở màn hình Editor và ghi chú không bị xóa. | **PASS** | Chưa có | [Không] |
| **TC-BB-021C** | **D02** | Editor -> menu 3 chấm -> "Xóa ghi chú" -> AlertDialog -> Xóa | 1. Mở ghi chú để vào màn hình Editor.<br>2. Nhấn biểu tượng 3 chấm ở góc phải thanh công cụ đáy.<br>3. Chọn "Xóa ghi chú".<br>4. Trên hộp thoại cảnh báo 'Xóa ghi chú?', nhấn nút "Xóa". | Note được chuyển vào Trash; ứng dụng quay về Trang chủ và ghi chú được chuyển vào Thùng rác. | Tại màn hình Editor, mở menu 3 chấm chọn "Xóa ghi chú", nhấn "Xóa" trên hộp thoại cảnh báo. Ứng dụng quay về Trang chủ và ghi chú được chuyển vào Thùng rác. | **PASS** | Chưa có | [Không] |
| **TC-BB-021D** | **D01** | HomeScreen -> multi-select 2 note -> Trash | 1. Nhấn giữ 1 ghi chú, sau đó chạm tiếp vào ghi chú thứ 2 để chọn cả 2.<br>2. Nhấn biểu tượng Thùng rác trên thanh công cụ chọn.<br>3. Mở Thùng rác kiểm tra. | Cả 2 ghi chú biến mất đồng thời khỏi Trang chủ; SnackBar hiển thị: *"Đã chuyển 2 ghi chú vào thùng rác"*; cả 2 ghi chú xuất hiện đầy đủ trong Thùng rác. | Nhấn giữ chọn đồng thời 2 ghi chú trên Trang chủ và bấm biểu tượng Thùng rác. Cả 2 ghi chú biến mất khỏi Trang chủ và xuất hiện đầy đủ trong Thùng rác. | **PASS** | Chưa có | [Không] |
| **TC-BB-022** | **D01** | Trash -> chọn 1 note -> "Khôi phục ghi chú" -> Home | 1. Vào Thùng rác qua Drawer.<br>2. Chạm nhẹ vào thẻ ghi chú để mở menu tùy chọn dưới đáy.<br>3. Chọn "Khôi phục ghi chú".<br>4. Quay về Trang chủ kiểm tra. | Ghi chú biến mất khỏi Thùng rác; hiển thị SnackBar: *"Đã khôi phục ghi chú"*; quay về Trang chủ thấy ghi chú đã xuất hiện trở lại với đầy đủ tiêu đề và nội dung. | Vào Thùng rác, chạm nhẹ vào ghi chú chọn "Khôi phục ghi chú". Ghi chú biến mất khỏi Thùng rác, hiển thị thông báo khôi phục và xuất hiện trở lại đầy đủ trên Trang chủ. | **PASS** | `FN10_11_12_TC-BB-022_D01_01.png` | [Không] |
| **TC-BB-022B** | **D01** | Trash -> multi-select -> Restore -> Home | 1. Vào Thùng rác.<br>2. Nhấn giữ 1 ghi chú để bật chế độ chọn, tích chọn tiếp ghi chú thứ 2.<br>3. Nhấn biểu tượng Khôi phục trên thanh AppBar chọn.<br>4. Quay lại Trang chủ kiểm tra. | Toàn bộ các ghi chú được chọn biến mất khỏi Thùng rác; quay về Trang chủ thấy tất cả các ghi chú đó xuất hiện lại đầy đủ và nguyên vẹn. | Tại Thùng rác, nhấn giữ chọn nhiều ghi chú và bấm biểu tượng Khôi phục trên AppBar. Toàn bộ các ghi chú được chọn biến mất khỏi Thùng rác và quay về Trang chủ đầy đủ. | **PASS** | Chưa có | [Không] |
| **TC-BB-022C** | **D01** | Trash rỗng -> kiểm tra Empty State "Thùng rác trống" | 1. Mở menu ngăn kéo (Drawer).<br>2. Chọn mục "Thùng rác".<br>3. Quan sát giao diện màn hình Thùng rác khi không có ghi chú nào. | Màn hình hiển thị hình minh họa thùng rác rỗng cùng thông điệp: *"Thùng rác trống"*; không hiển thị danh sách hay dải phân cách nào. | Mở màn hình Thùng rác khi không có ghi chú nào. Màn hình hiển thị trạng thái rỗng với hình minh họa và thông điệp "Thùng rác trống". | **PASS** | Chưa có | [Không] |
| **TC-BB-023** | **D01** | Trash -> 1 note -> "Xóa vĩnh viễn" | 1. Vào Thùng rác.<br>2. Chạm nhẹ vào thẻ ghi chú cần xóa vĩnh viễn.<br>3. Trên menu tùy chọn đáy, nhấn "Xóa vĩnh viễn".<br>4. Quan sát danh sách Thùng rác và Trang chủ. | Ghi chú biến mất hoàn toàn khỏi danh sách Thùng rác; quay lại Trang chủ xác nhận ghi chú không còn tồn tại trên ứng dụng. | Vào Thùng rác, chạm nhẹ vào ghi chú chọn "Xóa vĩnh viễn". Ghi chú biến mất hoàn toàn khỏi danh sách Thùng rác và không còn tồn tại trên Trang chủ. | **PASS** | `FN10_11_12_TC-BB-023_D01_01.png` | [Không] |
| **TC-BB-023B** | **D01** | Trash -> multi-select -> Permanent Delete -> Hủy | 1. Vào Thùng rác, nhấn giữ để chọn nhiều ghi chú.<br>2. Nhấn biểu tượng Xóa vĩnh viễn trên Selection AppBar.<br>3. Trên hộp thoại cảnh báo 'Xóa vĩnh viễn?', nhấn nút "Hủy". | Hộp thoại đóng lại, các note vẫn còn trong Trash. | Tại Thùng rác, chọn nhiều ghi chú và bấm Xóa vĩnh viễn trên AppBar. Khi hộp thoại xác nhận hiện ra, nhấn "Hủy". Hộp thoại đóng lại và các ghi chú đã chọn vẫn còn nguyên vẹn trong Thùng rác. | **PASS** | Chưa có | [Không] |
| **TC-BB-023B** | **D02** | Trash -> multi-select -> Permanent Delete -> Xóa | 1. Vào Thùng rác, nhấn giữ để chọn nhiều ghi chú.<br>2. Nhấn biểu tượng Xóa vĩnh viễn trên Selection AppBar.<br>3. Trên hộp thoại cảnh báo 'Xóa vĩnh viễn?', nhấn nút "Xóa". | Các note đã chọn biến mất hoàn toàn khỏi Trash và không xuất hiện lại trên Home. | Thực hiện lại với các ghi chú trong Thùng rác, nhấn "Xóa" trên hộp thoại cảnh báo. Toàn bộ các ghi chú đã chọn biến mất hoàn toàn khỏi Thùng rác và không xuất hiện lại trên Trang chủ. | **PASS** | Chưa có | [Không] |
| **TC-BB-023C** | **D01** | Có 1 note trong Trash và 1 note đã Permanent Delete -> force-stop -> reopen -> kiểm tra trạng thái vẫn đúng | 1. Đưa 1 ghi chú vào Thùng rác, thực hiện xóa vĩnh viễn 1 ghi chú khác.<br>2. Thoát hoàn toàn và force-stop ứng dụng.<br>3. Mở lại ứng dụng từ danh sách ứng dụng.<br>4. Kiểm tra danh sách Trang chủ và Thùng rác. | Trạng thái vòng đời của ghi chú được duy trì chính xác: ghi chú trong Thùng rác vẫn nằm trong Thùng rác, ghi chú đã xóa vĩnh viễn không bao giờ xuất hiện lại. | Sau khi khởi động lại ứng dụng (force-stop và mở lại), trạng thái vòng đời của các ghi chú được duy trì chính xác: ghi chú trong Thùng rác vẫn còn nguyên, ghi chú đã xóa vĩnh viễn không xuất hiện lại. | **PASS** | Chưa có | [Không] |

---

## 4. EVIDENCE NAMING CONVENTION & MAPPING

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc đặt tên chuẩn: `FN10_11_12_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  

### Bảng đối chiếu Evidence Mapping thực tế (Traceability):

| Execution ID | Test Case ID | Tên / Mô tả Test Case chuẩn hóa | Trạng thái | Evidence ánh xạ thực tế (`Smart-Note-App-QA/evidence/fn10_11_12/`) | Ghi chú |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-021-D01** | TC-BB-021 | HomeScreen -> long press note -> Trash | **PASS** | `Smart-Note-App-QA/evidence/fn10_11_12/FN10_11_12_TC-BB-021_D01_01.png` | Đã có file trong repo |
| **TC-BB-021B-D01** | TC-BB-021B | HomeScreen -> chuyển note vào Trash -> Undo trên SnackBar | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-021C-D01** | TC-BB-021C | Editor -> menu 3 chấm -> "Xóa ghi chú" -> AlertDialog -> Hủy | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-021C-D02** | TC-BB-021C | Editor -> menu 3 chấm -> "Xóa ghi chú" -> AlertDialog -> Xóa | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-021D-D01** | TC-BB-021D | HomeScreen -> multi-select 2 note -> Trash | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-022-D01** | TC-BB-022 | Trash -> chọn 1 note -> "Khôi phục ghi chú" -> Home | **PASS** | `Smart-Note-App-QA/evidence/fn10_11_12/FN10_11_12_TC-BB-022_D01_01.png` | Đã có file trong repo |
| **TC-BB-022B-D01** | TC-BB-022B | Trash -> multi-select -> Restore -> Home | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-022C-D01** | TC-BB-022C | Trash rỗng -> kiểm tra Empty State "Thùng rác trống" | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-023-D01** | TC-BB-023 | Trash -> 1 note -> "Xóa vĩnh viễn" | **PASS** | `Smart-Note-App-QA/evidence/fn10_11_12/FN10_11_12_TC-BB-023_D01_01.png` | Đã có file trong repo |
| **TC-BB-023B-D01** | TC-BB-023B | Trash -> multi-select -> Permanent Delete -> Hủy | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-023B-D02** | TC-BB-023B | Trash -> multi-select -> Permanent Delete -> Xóa | **PASS** | *Chưa có* | Chưa có file trong repo |
| **TC-BB-023C-D01** | TC-BB-023C | Có 1 note trong Trash và 1 note đã Permanent Delete -> force-stop -> reopen -> kiểm tra trạng thái vẫn đúng | **PASS** | *Chưa có* | Chưa có file trong repo |

---

## 5. BUG REPORT

| Bug ID | TC-ID | Data ID | Mô tả lỗi | Evidence | Severity | Status |
|---|---|---|---|---|---|---|
| *[Không có lỗi]* | - | - | Không phát sinh khiếm khuyết trong đợt thực thi FN-10, FN-11, FN-12 | - | - | - |

---

## 6. RETEST

| Bug ID | TC-ID | Kết quả lần đầu | Kết quả Retest | Evidence Retest | Ngày Retest |
|---|---|---|---|---|---|
| *[Không có]* | - | - | - | - | - |

---

## 7. TEST DATA CLEANUP

- Các ghi chú thử nghiệm vòng đời đã được khôi phục hoặc xóa vĩnh viễn an toàn, chuẩn bị dữ liệu cho các chức năng tiếp theo.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Tỷ lệ (%) | Ghi chú |
|---|---:|---:|---|
| **Tổng số Test Cases chính thức** | **10** | — | TC-BB-021 -> TC-BB-023C |
| **Tổng số Execution Items** | **12** | **100%** | Bao gồm TC-BB-021C (2 items) và TC-BB-023B (2 items) |
| **Số lượng ca Đạt (PASS)** | **12** | **100%** | Toàn bộ 12/12 Execution Items PASS theo thực tế |
| **Số lượng ca Không đạt (FAIL)** | **0** | **0%** | Không có ca nào thất bại |
| **Số lượng ca Bị chặn (BLOCKED)** | **0** | **0%** | 100% ca được thực thi trực tiếp trên Samsung Galaxy S21 FE 5G |
| **Số lượng Lỗi hệ thống (ERROR)** | **0** | **0%** | Không có lỗi runtime hay crash ứng dụng |
| **Số khiếm khuyết phát hiện (Bugs)** | **0** | — | Không phát hiện lỗi chức năng |
| **Tỷ lệ thực thi (Execution Rate)** | **12 / 12** | **100%** | Đã thực thi hoàn tất toàn bộ bộ test FN-10, 11, 12 |
| **Tỷ lệ đạt (Pass Rate)** | **12 / 12** | **100%** | 12/12 Execution Items đạt yêu cầu |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 12/12 execution items của nhóm chức năng FN-10 / FN-11 / FN-12.
- [x] Đã ghi nhận Actual Result trung thực và chi tiết dựa trên kết quả thực tế trên Samsung Galaxy S21 FE 5G – Android 14.
- [x] Đã đánh giá trạng thái PASS cho cả 12/12 execution items.
- [x] Chỉ ánh xạ đúng 3 file evidence thực tế hiện có trong repo (`FN10_11_12_TC-BB-021_D01_01.png`, `FN10_11_12_TC-BB-022_D01_01.png`, `FN10_11_12_TC-BB-023_D01_01.png`), các mục còn lại ghi rõ "Chưa có", không tự bịa tên file.
- [x] Không phát sinh bất kỳ Bug ID nào trong đợt thực thi này.
- [x] Đã chuẩn hóa mô tả Test Case theo đúng thiết kế và quy tắc Traceability.

---

**FN-10 / FN-11 / FN-12 BLACK-BOX = CHỐT**  
**10 TC / 12 Execution Items / 12 PASS / 0 FAIL / 0 BLOCKED / 0 ERROR.**
