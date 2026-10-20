# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-08
## Dự án: Smart Note App
**Chức năng:** Tạo Ghi chú văn bản mới (FN-08)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng tạo ghi chú văn bản mới cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-08** |
| **Chức năng** | **Tạo Ghi chú văn bản mới** |
| **Người kiểm thử (Tester)** | QA Tester (Manual Autonomous Execution) |
| **Ngày kiểm thử (Execution Date)** | 05/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990B / R5CW82ECF6M) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | v1.0.0+1 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | Tài khoản Google đang đăng nhập |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đã đăng nhập vào ứng dụng và đang ở màn hình Trang chủ.
2. **Giao diện sẵn sàng:** Nút Tạo mới (+) hoặc tùy chọn tạo ghi chú văn bản hiển thị rõ ràng trên Trang chủ.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-016** | **D01** | • Tiêu đề: `"Kế hoạch tuần"`<br>• Nội dung: `"Hoàn thành tài liệu kiểm thử QA"` | 1. Nhấn nút Tạo mới (+) trên Trang chủ.<br>2. Nhập Tiêu đề.<br>3. Nhập Nội dung.<br>4. Nhấn nút Quay lại (Back) trên thanh tiêu đề. | Ứng dụng quay về Trang chủ; ghi chú mới xuất hiện ngay ở đầu danh sách với đúng Tiêu đề và Nội dung vừa nhập. | Ứng dụng quay về Trang chủ; thẻ ghi chú mới xuất hiện ở đầu danh sách hiển thị đầy đủ tiêu đề "Kế hoạch tuần" và nội dung "Hoàn thành tài liệu kiểm thử QA". | **PASS** | `FN08_TC-BB-016_D01_01.png` | [Không] |
| **TC-BB-017** | **D01** | • Tiêu đề: `""`<br>• Nội dung: `"Ý tưởng nhanh không tiêu đề"` | 1. Mở màn hình soạn thảo ghi chú mới.<br>2. Để trống ô Tiêu đề.<br>3. Nhập nội dung văn bản.<br>4. Nhấn nút Quay lại (Back). | Ứng dụng quay về Trang chủ; ghi chú mới vẫn được tạo và xuất hiện trên danh sách với phần hiển thị xem trước là đoạn văn bản nội dung. | Ứng dụng quay về Trang chủ; ghi chú không tiêu đề được tạo và lưu thành công, hiển thị xem trước nội dung "Ý tưởng nhanh không tiêu đề" trên danh sách. | **PASS** | `FN08_TC-BB-017_D01_01.png` | [Không] |
| **TC-BB-018** | **D01** | • Tiêu đề: `""`<br>• Nội dung: `""` | 1. Mở màn hình soạn thảo ghi chú mới.<br>2. Không nhập bất kỳ ký tự nào vào cả ô Tiêu đề và ô Nội dung.<br>3. Nhấn nút Quay lại (Back) ngay lập tức. | Ứng dụng quay về Trang chủ; không có bất kỳ ghi chú trống nào xuất hiện thêm trên danh sách. | Ứng dụng quay về Trang chủ ngay lập tức; danh sách ghi chú giữ nguyên trạng thái trước đó, không xuất hiện bất kỳ thẻ ghi chú trống nào. | **PASS** | `FN08_TC-BB-018_D01_01.png` | [Không] |
| **TC-BB-018B** | **D01** | • Tiêu đề: `"Nhắc nhở họp gấp"`<br>• Nội dung: `""` | 1. Mở màn hình soạn thảo ghi chú mới.<br>2. Nhập Tiêu đề.<br>3. Để trống ô Nội dung.<br>4. Nhấn nút Quay lại (Back). | Ứng dụng quay về Trang chủ; ghi chú mới được tạo và hiển thị chỉ có Tiêu đề. | Ứng dụng quay về Trang chủ; thẻ ghi chú xuất hiện trên danh sách với Tiêu đề "Nhắc nhở họp gấp", không có nội dung xem trước. | **PASS** | `FN08_TC-BB-018B_D01_01.png` | [Không] |
| **TC-BB-018C** | **D01** | • Tiêu đề: `"Ghi chú autosave kiểm chứng"`<br>• Nội dung: `"Dữ liệu này được tự động lưu ngầm không cần bấm nút Back"` | 1. Mở màn hình soạn thảo ghi chú mới.<br>2. Nhập đúng Tiêu đề và Nội dung.<br>3. Chờ ít nhất 2.5 giây trên màn hình Editor.<br>4. TUYỆT ĐỐI KHÔNG bấm Back; force-stop ứng dụng ngay tại Editor.<br>5. Mở lại ứng dụng.<br>6. Kiểm tra Trang chủ. | Sau khi mở lại ứng dụng, ghi chú đã nhập trước đó vẫn xuất hiện đầy đủ với đúng Tiêu đề và Nội dung. | Mở lại ứng dụng sau khi force-stop trực tiếp từ Editor; ghi chú đã nhập xuất hiện đầy đủ trên Trang chủ với Tiêu đề "Ghi chú autosave kiểm chứng" và Nội dung "Dữ liệu này được tự động lưu ngầm không cần bấm nút Back". | **PASS** | `FN08_TC-BB-018C_D01_01.png` | [Không] |
| **TC-BB-018D** | **D01** | • Tiêu đề ban đầu: `"Tạm"`<br>• Nội dung ban đầu: `"Tạm"`<br>• Sau đó: Xóa sạch cả hai trường về rỗng | 1. Mở màn hình soạn thảo ghi chú mới.<br>2. Nhập Tiêu đề = "Tạm", Nội dung = "Tạm".<br>3. Chờ khoảng 1.5 giây để draft được ghi nhận.<br>4. Xóa sạch cả Tiêu đề và Nội dung.<br>5. Nhấn nút Quay lại (Back).<br>6. Kiểm tra Trang chủ. | Ứng dụng quay về Trang chủ; không xuất hiện ghi chú trống hoặc ghi chú draft đã bị xóa sạch trước đó. | Ứng dụng quay về Trang chủ; bản nháp đã xóa sạch hoàn toàn không tạo thành ghi chú rỗng mới trên Trang chủ (hủy bản nháp rỗng thành công). | **PASS** | `FN08_TC-BB-018D_D01_01.png` | [Không] |
| **TC-BB-018E** | **D01** | • Tiêu đề: `"LongText_UTF8_Emoji_🚀_#2026"`<br>• Nội dung: Đoạn văn bản 11 dòng (>10 dòng) gồm:<br>- Tiếng Việt đầy đủ thanh sắc hỏi ngã nặng (ắ, ằ, ẳ, ẵ, ặ, ấ, ầ, ẩ, ẫ, ậ, ê, ô, ơ, ư, đ)<br>- Emoji phong phú đa dạng (😀 😁 😂 🤣 😃 😄 😅 😆 😉 😊 😋 😎 😍 😘 😗 😙 😚 ☺️ 😇 🔥 🚀 🌟 💡 📌 📝 📅)<br>- Bộ ký tự đặc biệt (!@#$%^&*()_+~|}{[]:;?><,./-=)<br>- Ký tự mô phỏng thẻ tag HTML/XML (`<div><span style="color:red">Test Content</span></div> &lt;script&gt;`)<br>- Chuỗi dấu nháy lồng nhau ('Single quote', "Double quote", `Backtick`)<br>- Chuỗi thụt đầu dòng (Tab 1, Tab 2) và ngắt dòng liên tiếp | 1. Mở màn hình soạn thảo ghi chú mới.<br>2. Nhập Tiêu đề và Nội dung văn bản dài 11 dòng (>10 dòng) chứa các định dạng phức tạp.<br>3. Nhấn nút Quay lại (Back).<br>4. Kiểm tra thẻ ghi chú trên Trang chủ (không vỡ layout).<br>5. Nhấn vào thẻ để mở lại ghi chú và kiểm tra nội dung chi tiết. | Khi mở lại ghi chú, nội dung đã nhập được hiển thị đúng; tiếng Việt, emoji, ký tự đặc biệt và HTML-like text không bị mất, biến dạng hoặc làm vỡ giao diện. | Thẻ ghi chú trên Trang chủ co giãn bố cục chuẩn xác, không tràn viền/vỡ layout. Khi nhấn mở lại ghi chú, toàn bộ đoạn văn bản 11 dòng (>10 dòng) gồm tiếng Việt có dấu, emoji, ký tự đặc biệt, HTML-like text, dấu nháy và thụt lề hiển thị nguyên vẹn đầy đủ, không bị biến dạng hay mất mát ký tự. | **PASS** | `FN08_TC-BB-018E_D01_01.png`<br>`FN08_TC-BB-018E_D01_02.png` | [Không] |
| **TC-BB-018F** | **D01** | • Ghi chú hợp lệ đã được tạo thành công trên thiết bị | 1. Tạo một ghi chú hợp lệ và quay về Trang chủ.<br>2. Force-stop ứng dụng.<br>3. Mở lại ứng dụng từ danh sách ứng dụng.<br>4. Kiểm tra danh sách Trang chủ. | Ghi chú vừa tạo vẫn tồn tại đầy đủ trên danh sách Trang chủ với dữ liệu chính xác sau khi khởi động lại ứng dụng. | Sau khi force-stop và khởi động lại ứng dụng, toàn bộ các ghi chú vừa tạo vẫn hiển thị đầy đủ và chính xác trên danh sách Trang chủ, không bị mất mát dữ liệu. | **PASS** | `FN08_TC-BB-018F_D01_01.png` | [Không] |

---

## 4. EVIDENCE NAMING CONVENTION

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN08_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Danh mục evidence đã lưu tại `Smart-Note-App-QA/evidence/fn08/`:  
  • `FN08_TC-BB-016_D01_01.png`: Ghi chú đầy đủ Tiêu đề & Nội dung trên Trang chủ  
  • `FN08_TC-BB-017_D01_01.png`: Ghi chú chỉ có Nội dung (tiêu đề rỗng) xem trước trên Trang chủ  
  • `FN08_TC-BB-018_D01_01.png`: Không tạo ghi chú rỗng khi vào Editor rồi Back ngay  
  • `FN08_TC-BB-018B_D01_01.png`: Ghi chú chỉ có Tiêu đề (nội dung rỗng) trên Trang chủ  
  • `FN08_TC-BB-018C_D01_01.png`: Ghi chú tự động lưu ngầm (Autosave độc lập) sau khi force-stop tại Editor  
  • `FN08_TC-BB-018D_D01_01.png`: Hủy bản nháp rỗng sau khi xóa sạch dữ liệu và Back  
  • `FN08_TC-BB-018E_D01_01.png`: Card ghi chú Long Text & Complex Input trên Trang chủ (layout nguyên vẹn)  
  • `FN08_TC-BB-018E_D01_02.png`: Chi tiết ghi chú Long Text hiển thị đầy đủ Unicode, Emoji, HTML-like text  
  • `FN08_TC-BB-018F_D01_01.png`: Dữ liệu ghi chú bền vững (Persistence) sau khi force-stop và khởi động lại app  

---

## 5. BUG REPORT

| Bug ID | TC-ID | Data ID | Mô tả lỗi | Evidence | Severity | Status |
|---|---|---|---|---|---|---|
| *[Không có lỗi]* | - | - | Không phát sinh lỗi trong quá trình kiểm thử FN-08 | - | - | - |

---

## 6. RETEST

| Bug ID | TC-ID | Kết quả lần đầu | Kết quả Retest | Evidence Retest | Ngày Retest |
|---|---|---|---|---|---|
| *[Không có]* | - | - | - | - | - |

---

## 7. TEST DATA CLEANUP

- Các ghi chú vừa tạo sẽ được tiếp tục sử dụng để kiểm thử các chức năng tiếp theo: xem chi tiết, chỉnh sửa (FN-09), ghim, xóa vào thùng rác (FN-10/11/12), tìm kiếm (FN-23) trước khi dọn dẹp.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **8** | TC-BB-016, 017, 018, 018B, 018C, 018D, 018E, 018F |
| **Tổng Execution Items** | **8** | 8 Execution Items chính thức |
| **Số lượng PASS** | **8** | Toàn bộ 8 ca đều đạt yêu cầu |
| **Số lượng FAIL** | **0** | Không có ca nào thất bại |
| **Số lượng BLOCKED** | **0** | Không có ca nào bị chặn |
| **Số Bug phát hiện** | **0** | Không có bug |
| **Tỷ lệ thực thi (Execution Rate)** | **100%** | `(8 / 8) * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | **100%** | `(8 / 8) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 8/8 execution items của chức năng FN-08.
- [x] Đã ghi nhận Actual Result trung thực và chi tiết dựa trên quan sát UI thực tế.
- [x] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [x] Đã lưu trữ Evidence (ảnh chụp màn hình) đầy đủ theo đúng quy tắc đặt tên.
- [x] Đã kiểm chứng độc lập tính năng Autosave tại TC-BB-018C bằng force-stop trực tiếp từ Editor mà không bấm Back.
