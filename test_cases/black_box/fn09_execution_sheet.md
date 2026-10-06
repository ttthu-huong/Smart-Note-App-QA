# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-09
## Dự án: Smart Note App
**Chức năng:** Chỉnh sửa Ghi chú & Tự động lưu (FN-09)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Ghi nhận kết quả thực thi kiểm thử thủ công chức năng Chỉnh sửa ghi chú và Tự động lưu (Autosave).

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-09** |
| **Chức năng** | **Chỉnh sửa Ghi chú & Tự động lưu** |
| **Người kiểm thử (Tester)** | QA Tester (Manual Execution on Real Device) |
| **Ngày kiểm thử (Execution Date)** | 06/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990B / R5CW82ECF6M) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | v1.0.0+1 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | Tài khoản Google đang đăng nhập |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đã đăng nhập vào ứng dụng và đang ở màn hình Trang chủ.
2. **Dữ liệu sẵn có:** Có ít nhất một ghi chú văn bản hợp lệ hiển thị trên danh sách Trang chủ.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-019** | **D01** | Bổ sung thêm chuỗi: `"\n[Cập nhật: Đã hoàn tất phase 1]"` | 1. Nhấn vào ghi chú trên Trang chủ để mở Editor.<br>2. Chạm vào vùng soạn thảo nội dung.<br>3. Gõ thêm nội dung mới vào cuối văn bản.<br>4. Nhấn nút Quay lại (Back) trên AppBar.<br>5. Quan sát thẻ ghi chú trên Trang chủ. | Ứng dụng quay về Trang chủ; thẻ ghi chú hiển thị nội dung mới vừa được bổ sung; mở lại ghi chú thấy nội dung đầy đủ. | Ứng dụng quay về Trang chủ; thẻ ghi chú phản ánh chính xác chuỗi nội dung mới vừa bổ sung; mở lại ghi chú thấy toàn bộ nội dung hiển thị đầy đủ. | **PASS** | `FN09_TC-BB-019_D01_01.png` | [Không] |
| **TC-BB-019B** | **D01** | Tiêu đề mới: `"Kế hoạch tuần - Đã duyệt"` | 1. Nhấn mở ghi chú hiện có.<br>2. Chạm vào ô Tiêu đề, xóa tiêu đề cũ và nhập tiêu đề mới.<br>3. Giữ nguyên phần Nội dung.<br>4. Nhấn nút Quay lại (Back) trên AppBar.<br>5. Quan sát Trang chủ. | Ứng dụng quay về Trang chủ; thẻ ghi chú hiển thị tiêu đề mới được cập nhật; phần nội dung xem trước vẫn giữ nguyên như cũ. | Ứng dụng quay về Trang chủ; thẻ ghi chú đổi sang tiêu đề mới "Kế hoạch tuần - Đã duyệt"; phần nội dung xem trước bên dưới giữ nguyên vẹn. | **PASS** | `FN09_TC-BB-019B_D01_01.png` | [Không] |
| **TC-BB-019C** | **D01** | • Tiêu đề mới: `"Kế hoạch tháng 11"`<br>• Nội dung mới: `"Triển khai kiểm thử hồi quy toàn bộ hệ thống"` | 1. Mở ghi chú hiện có.<br>2. Chỉnh sửa ô Tiêu đề thành tiêu đề mới.<br>3. Chỉnh sửa toàn bộ ô Nội dung thành nội dung mới.<br>4. Nhấn nút Quay lại (Back) trên AppBar.<br>5. Quan sát Trang chủ và mở lại ghi chú. | Ứng dụng quay về Trang chủ; thẻ ghi chú phản ánh đồng thời cả Tiêu đề mới và Nội dung mới; mở lại ghi chú hiển thị chính xác toàn bộ dữ liệu mới. | Chỉnh sửa đồng thời Title và Content thành công; sau khi thoát bằng AppBar Back, dữ liệu mới hiển thị đúng trên Home và mở lại note vẫn chính xác. | **PASS** | `FN09_TC-BB-019C_D01_01.png` | [Không] |
| **TC-BB-019D** | **D01** | Tiêu đề mới: `""` (xóa sạch về rỗng), giữ nguyên Nội dung | 1. Mở ghi chú hiện có.<br>2. Xóa sạch toàn bộ ký tự trong ô Tiêu đề.<br>3. Giữ nguyên nội dung văn bản.<br>4. Nhấn nút Quay lại (Back) trên AppBar.<br>5. Quan sát Trang chủ. | Ứng dụng quay về Trang chủ; ghi chú không bị mất; thẻ ghi chú hiển thị nội dung văn bản làm đoạn xem trước (không còn tiêu đề). | Ứng dụng quay về Trang chủ; ghi chú không bị mất, thẻ ghi chú hiển thị nội dung làm xem trước đúng chức năng. Đồng thời quan sát thấy xuất hiện lỗi giao diện tràn viền (Front-end Overflow / dải sọc cảnh báo RenderFlex Overflow). | **PASS** | `FN09_TC-BB-019D_D01_01.png` | BUG-BB-FN09-01 |
| **TC-BB-019E** | **D01** | Tiêu đề giữ nguyên, Nội dung mới: `""` (xóa sạch về rỗng) | 1. Mở ghi chú hiện có.<br>2. Giữ nguyên Tiêu đề.<br>3. Xóa sạch toàn bộ văn bản trong vùng soạn thảo Nội dung.<br>4. Nhấn nút Quay lại (Back) trên AppBar.<br>5. Quan sát Trang chủ. | Ứng dụng quay về Trang chủ; ghi chú vẫn tồn tại trên danh sách; thẻ ghi chú chỉ hiển thị Tiêu đề, không có phần nội dung xem trước bên dưới. | Ứng dụng quay về Trang chủ; ghi chú vẫn tồn tại với Tiêu đề và không có nội dung xem trước đúng chức năng. Đồng thời quan sát thấy xuất hiện lỗi giao diện tràn viền (Front-end Overflow / dải sọc cảnh báo RenderFlex Overflow) khi xóa rỗng nội dung. | **PASS** | `FN09_TC-BB-019E_D01_01.png` | BUG-BB-FN09-01 |
| **TC-BB-019F** | **D01** | Tiêu đề: `""`, Nội dung: `""` (xóa sạch hoàn toàn về rỗng) | 1. Mở ghi chú hiện có.<br>2. Xóa sạch toàn bộ Tiêu đề.<br>3. Xóa sạch toàn bộ Nội dung.<br>4. Nhấn nút Quay lại (Back) trên AppBar.<br>5. Quan sát danh sách Trang chủ. | Ứng dụng quay về Trang chủ; ghi chú đã bị xóa sạch hoàn toàn sẽ không còn xuất hiện trên danh sách Trang chủ (tự động dọn dẹp ghi chú rỗng). | Về mặt chức năng: sau khi thoát, ghi chú bị xóa sạch hoàn toàn và biến mất khỏi danh sách Trang chủ. Về giao diện: trước khi ghi chú biến mất hoặc tại thời điểm xóa rỗng, xuất hiện lỗi giao diện tràn viền (Front-end Overflow). | **PASS** | `FN09_TC-BB-019F_D01_01.png` | BUG-BB-FN09-01 |
| **TC-BB-019G** | **D01** | Bổ sung thêm chuỗi: `"\n[Thoát bằng System Back]"` | 1. Mở ghi chú hiện có.<br>2. Thay đổi một phần Content.<br>3. Nhấn phím điều hướng hệ thống (Android System Back).<br>4. Quan sát Trang chủ.<br>5. Mở lại ghi chú. | Ứng dụng quay về Trang chủ; thay đổi vừa thực hiện được lưu và vẫn hiển thị đầy đủ khi mở lại ghi chú. | Thoát bằng phím điều hướng Android System Back thành công; ứng dụng quay về Trang chủ và lưu thay đổi; mở lại ghi chú thấy nội dung mới hiển thị đầy đủ. | **PASS** | `FN09_TC-BB-019G_D01_01.png` | [Không] |
| **TC-BB-019G** | **D02** | Bổ sung thêm chuỗi: `"\n[Thoát bằng Gesture Back]"` | 1. Mở ghi chú hiện có.<br>2. Thay đổi một phần Content.<br>3. Vuốt mép màn hình (Android Gesture Back).<br>4. Quan sát Trang chủ.<br>5. Mở lại ghi chú. | Ứng dụng quay về Trang chủ; thay đổi vừa thực hiện được lưu và vẫn hiển thị đầy đủ khi mở lại ghi chú. | Thoát bằng thao tác vuốt mép màn hình Android Gesture Back thành công; ứng dụng quay về Trang chủ và lưu thay đổi chính xác; mở lại ghi chú kiểm tra dữ liệu toàn vẹn. | **PASS** | `FN09_TC-BB-019G_D02_01.png` | [Không] |
| **TC-BB-020** | **D01** | Chuỗi bổ sung: `"\n[Autosave: Đang xử lý tự động]"` | 1. Mở ghi chú hiện có.<br>2. Nhập thêm nội dung mới vào phần văn bản.<br>3. Chờ ít nhất 2.5 giây trên màn hình Editor.<br>4. TUYỆT ĐỐI KHÔNG bấm Back; force-stop ứng dụng ngay tại Editor.<br>5. Mở lại ứng dụng.<br>6. Mở lại ghi chú đó. | Sau khi mở lại ứng dụng, nội dung bổ sung vẫn xuất hiện đầy đủ trong ghi chú dù người dùng không hề thực hiện thao tác Back để lưu. | Mở lại ứng dụng sau khi force-stop trực tiếp từ Editor; nội dung bổ sung vẫn xuất hiện đầy đủ và chính xác bên trong ghi chú (Autosave độc lập hoạt động chuẩn xác). | **PASS** | `FN09_TC-BB-020_D01_01.png` | [Không] |
| **TC-BB-020B** | **D01** | • Lần 1: Thêm `"- Giai đoạn 1"`<br>• Lần 2: Thêm `"\n- Giai đoạn 2"` | 1. Mở ghi chú, nhập thêm nội dung Lần 1 $\rightarrow$ bấm Back.<br>2. Kiểm tra thẻ ghi chú trên Trang chủ cập nhật Lần 1.<br>3. Mở lại chính ghi chú đó, nhập thêm nội dung Lần 2 $\rightarrow$ bấm Back.<br>4. Mở lại ghi chú kiểm tra. | Cả hai lần chỉnh sửa đều được lưu tuần tự; nội dung hiển thị đầy đủ cả kết quả của Lần 1 và Lần 2 mà không bị mất hoặc ghi đè sai lệch. | Cả hai lần chỉnh sửa liên tiếp đều được lưu tuần tự thành công; thẻ ghi chú trên Trang chủ và màn hình soạn thảo hiển thị đầy đủ cả nội dung của Lần 1 và Lần 2. | **PASS** | `FN09_TC-BB-020B_D01_01.png` | [Không] |
| **TC-BB-020C** | **D01** | Chuỗi bổ sung: `"\n[Cập nhật 🚀: Đạt 100% mục tiêu! @QA #2026]"` | 1. Mở ghi chú hiện có.<br>2. Nhập thêm chuỗi chứa tiếng Việt có dấu, emoji và ký tự đặc biệt.<br>3. Bấm Back trên AppBar.<br>4. Quan sát thẻ trên Trang chủ và mở lại chi tiết ghi chú. | Thẻ ghi chú trên Trang chủ và màn hình soạn thảo hiển thị chuẩn xác tiếng Việt có dấu, emoji và ký tự đặc biệt; giao diện không bị co kéo vỡ font. | Thẻ ghi chú trên Trang chủ co giãn tốt, không tràn viền; khi mở lại ghi chú chi tiết, toàn bộ biểu tượng emoji, tiếng Việt có dấu và ký tự đặc biệt hiển thị chuẩn xác. | **PASS** | `FN09_TC-BB-020C_D01_01.png` | [Không] |
| **TC-BB-020D** | **D01** | Ghi chú đã chỉnh sửa thành công | 1. Đang ở Trang chủ thấy ghi chú đã cập nhật.<br>2. Force-stop ứng dụng.<br>3. Mở lại ứng dụng từ danh sách ứng dụng.<br>4. Kiểm tra thẻ ghi chú và mở lại xem chi tiết. | Toàn bộ dữ liệu đã chỉnh sửa của ghi chú vẫn hiển thị nguyên vẹn và chính xác sau khi khởi động lại ứng dụng. | Sau khi force-stop và khởi động lại ứng dụng, toàn bộ dữ liệu đã chỉnh sửa vẫn được bảo toàn nguyên vẹn trên cả danh sách Trang chủ và bên trong màn hình Editor. | **PASS** | `FN09_TC-BB-020D_D01_01.png` | [Không] |

---

## 4. EVIDENCE NAMING CONVENTION

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN09_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Danh mục evidence ánh xạ tại `Smart-Note-App-QA/evidence/fn09/`:  
  • `FN09_TC-BB-019_D01_01.png`: Thẻ ghi chú phản ánh nội dung mới bổ sung khi thoát bằng AppBar Back  
  • `FN09_TC-BB-019B_D01_01.png`: Thẻ ghi chú cập nhật riêng Tiêu đề mới, giữ nguyên nội dung xem trước  
  • `FN09_TC-BB-019C_D01_01.png`: Thẻ ghi chú và chi tiết cập nhật đồng thời cả Tiêu đề và Nội dung mới  
  • `FN09_TC-BB-019D_D01_01.png`: Thẻ ghi chú chỉ có nội dung xem trước (tiêu đề rỗng) và ảnh chụp lỗi Front-end Overflow  
  • `FN09_TC-BB-019E_D01_01.png`: Thẻ ghi chú chỉ có tiêu đề (nội dung rỗng) và ảnh chụp lỗi Front-end Overflow  
  • `FN09_TC-BB-019F_D01_01.png`: Ghi chú bị xóa biến mất khỏi Trang chủ và ảnh chụp lỗi Front-end Overflow trước khi xóa  
  • `FN09_TC-BB-019G_D01_01.png`: Dữ liệu được lưu thành công khi thoát bằng phím Android System Back  
  • `FN09_TC-BB-019G_D02_01.png`: Dữ liệu được lưu thành công khi thoát bằng thao tác Android Gesture Back  
  • `FN09_TC-BB-020_D01_01.png`: Dữ liệu tự động lưu ngầm (Autosave độc lập) sau khi force-stop trực tiếp từ Editor  
  • `FN09_TC-BB-020B_D01_01.png`: Kết quả lưu tuần tự 2 lần chỉnh sửa liên tiếp hiển thị đầy đủ  
  • `FN09_TC-BB-020C_D01_01.png`: Thẻ ghi chú và chi tiết hiển thị đầy đủ Unicode, Emoji và ký tự đặc biệt  
  • `FN09_TC-BB-020D_D01_01.png`: Dữ liệu ghi chú đã sửa vẫn bền vững (Persistence) sau khi khởi động lại app  

---

## 5. BUG REPORT

| Bug ID | TC-ID Liên quan | Data ID | Tên khiếm khuyết & Mô tả chi tiết | Mức độ nghiêm trọng (Severity) | Trạng thái (Status) |
|:---|:---|:---:|:---|:---:|:---:|
| **BUG-BB-FN09-01** | `TC-BB-019D`<br>`TC-BB-019E`<br>`TC-BB-019F` | `D01` | **Lỗi giao diện tràn viền (Front-end RenderFlex Overflow):**<br>• *Triệu chứng:* Khi người dùng xóa rỗng ô Tiêu đề (019D), xóa rỗng vùng Nội dung (019E), hoặc xóa sạch đồng thời cả hai trường (019F), giao diện ứng dụng xuất hiện dải sọc cảnh báo vàng/đen của Flutter (RenderFlex pixel overflow) tại khu vực màn hình Editor/Thanh công cụ hoặc chân thẻ ghi chú trước khi điều hướng.<br>• *Tác động:* Tính năng nghiệp vụ lưu/xóa vẫn hoàn thành theo Expected Result, nhưng trải nghiệm giao diện người dùng bị gián đoạn và xuất hiện lỗi trực quan không đạt chuẩn UI. | **Minor (UI Defect)** | **Open** |

---

## 6. RETEST

| Bug ID | TC-ID | Kết quả lần đầu | Kết quả Retest | Evidence Retest | Ngày Retest |
|---|---|---|---|---|---|
| *[Không có]* | - | - | - | - | - |

---

## 7. TEST DATA CLEANUP

- Các ghi chú chỉnh sửa tiếp tục được dùng cho kiểm thử Ghim (FN-20), Thùng rác (FN-10/11/12) và Tìm kiếm (FN-23).

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Tỷ lệ (%) | Ghi chú |
|---|---:|---:|---|
| **Tổng số Test Cases chính thức** | **11** | — | TC-BB-019 $
ightarrow$ TC-BB-020D |
| **Tổng số Execution Items** | **12** | **100%** | Bao gồm TC-BB-019G (2 items: D01 & D02) |
| **Số lượng ca Đạt (PASS)** | **12** | **100%** | Toàn bộ 12/12 Execution Items đáp ứng đúng Expected Result |
| **Số lượng ca Không đạt (FAIL)** | **0** | **0%** | Không có ca nào thất bại về mặt chức năng |
| **Số lượng ca Bị chặn (BLOCKED)** | **0** | **0%** | 100% ca được thực thi trực tiếp trên Samsung Galaxy S21 FE |
| **Số lượng Lỗi hệ thống (ERROR)** | **0** | **0%** | Không có lỗi runtime hay crash ứng dụng |
| **Số Bug giao diện ghi nhận (UI Bugs)** | **1** | — | `BUG-BB-FN09-01` (RenderFlex Overflow tại 019D, 019E, 019F) |
| **Tỷ lệ thực thi (Execution Rate)** | **12 / 12** | **100%** | Đã thực thi hoàn tất toàn bộ bộ test FN-09 |
| **Tỷ lệ đạt chức năng (Pass Rate)** | **12 / 12** | **100%** | 12/12 Execution Items PASS chức năng |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 12/12 execution items của chức năng FN-09.
- [x] Đã ghi nhận Actual Result trung thực và chi tiết dựa trên quan sát UI thực tế trên thiết bị Samsung Galaxy S21 FE.
- [x] Đã đánh giá trạng thái PASS cho cả 12/12 execution items.
- [x] Đã tách riêng khiếm khuyết giao diện tràn viền thành `BUG-BB-FN09-01` mà không làm sai lệch trạng thái nghiệp vụ của Test Case.
- [x] Đã lưu trữ và mapping đầy đủ danh mục Evidence (ảnh chụp màn hình) theo đúng quy tắc đặt tên.
