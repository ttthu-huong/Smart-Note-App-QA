# BÁO CÁO THỰC THI AUTOMATION TEST — FN-08 (CREATE NOTE)
## Dự án: Smart Note App
**Branch:** `huong`  
**Nhóm chức năng:** FN-08: Tạo Ghi chú văn bản mới  
**Danh sách Test Cases:** TC-BB-016, TC-BB-017, TC-BB-018 (tổng 3 items)  
**Framework:** Python 3.13 + pytest + uiautomator2 + ADB  
**Thiết bị thực thi:** Samsung Galaxy S21 FE 5G (SM-G990E), Android 14 (API 34)  
**Ngày thực thi:** 04/10/2026 - 05/10/2026  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual / Automation Execution  

---

## 1. TỔNG QUAN KẾT QUẢ THỰC THI TỰ ĐỘNG

| Chỉ số | Số lượng / Giá trị | Ghi chú |
|---|---:|---|
| **Tổng số Test Cases** | **3** | TC-BB-016, TC-BB-017, TC-BB-018 |
| **Số lượng PASS** | **3** | TC-BB-016, TC-BB-017, TC-BB-018 (**100.00%**) |
| **Số lượng FAIL** | **0** | Không có test case nào thất bại |
| **Số lượng ERROR** | **0** | Kịch bản chạy thông suốt, không gặp lỗi môi trường |
| **Số lượng BLOCKED** | **0** | Cả 3 Test Case đều được thực thi trên thiết bị thật |
| **Thời gian thực thi** | **71.11s** | Chạy tuần tự và chụp ảnh screenshot tự động |
| **Báo cáo JUnit XML** | [`fn08_create_note_junit.xml`](fn08_create_note_junit.xml) | Xuất tự động qua pytest |

---

## 2. BẢNG CHI TIẾT KẾT QUẢ TỪNG TEST CASE

| TC-ID | Data ID | Test Data | Expected Result (Đặc tả) | Actual Result (Thực tế trên UI) | Trạng thái | Bug ID | Nguyên nhân / Phân tích chi tiết | Evidence |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **TC-BB-016** | **D01** | • Title: `"Họp Lab"`<br>• Content: `"Nội dung ngắn gọn"` | Thẻ ghi chú hiển thị đầy đủ tiêu đề và nội dung; xuất hiện ở đầu danh sách Trang chủ. | Thẻ ghi chú hiển thị đầy đủ tiêu đề và nội dung xem trước trên HomeScreen. | **PASS** | — | Ghi chú văn bản hoàn chỉnh được lưu vào SQLite và hiển thị chính xác trên UI. | [`FN08_TC-BB-016_D01_01.png`](../../evidence/fn08/FN08_TC-BB-016_D01_01.png) |
| **TC-BB-017** | **D01** | • Title: `""`<br>• Content: `"Ý tưởng nhanh không tiêu đề"` | Ứng dụng quay về Trang chủ; ghi chú mới vẫn được tạo và xuất hiện trên danh sách với phần hiển thị xem trước là đoạn văn bản nội dung. | Ghi chú được tạo thành công; hiển thị đoạn văn bản nội dung xem trước trên danh sách HomeScreen. | **PASS** | — | Ghi chú không có tiêu đề vẫn được lưu và lấy phần nội dung làm preview. | [`FN08_TC-BB-017_D01_01.png`](../../evidence/fn08/FN08_TC-BB-017_D01_01.png) |
| **TC-BB-018** | **D01** | • Title: `""`<br>• Content: `""` | Ứng dụng quay về Trang chủ; không có bất kỳ ghi chú trống nào xuất hiện thêm trên danh sách. | Ứng dụng quay về Trang chủ; số lượng và danh sách ghi chú giữ nguyên, không tạo ghi chú rỗng. | **PASS** | — | Logic kiểm tra rỗng của ứng dụng hoạt động chính xác theo đặc tả. | [`FN08_TC-BB-018_D01_01.png`](../../evidence/fn08/FN08_TC-BB-018_D01_01.png) |

---

## 3. CƠ CHẾ TỰ ĐỘNG HÓA VÀ ĐỘ ỔN ĐỊNH
- **Native JSON-RPC Clipboard Paste (`input_content`):**
  - Khắc phục triệt để việc Flutter QuillEditor không nhận sự kiện `ACTION_SET_TEXT` thông thường bằng cách dùng native `pasteClipboard()` của uiautomator2. Sự kiện này kích hoạt listener tài liệu của `flutter_quill` và đánh dấu `_isDirty = true`.
- **Intermediate Verification (Xác minh trung gian):**
  - Kiểm tra text đã xuất hiện trong UI hierarchy của QuillEditor trước khi thoát ra Trang chủ. Nếu chưa xuất hiện, kịch bản báo lỗi ngay lập tức `[INPUT FAILURE]` thay vì giả định note đã lưu.
- **Safe Selection Mode Cleanup:**
  - Nhấn giữ thẻ ghi chú bằng `touch.down` 1.2s kích hoạt chuẩn xác `Selection Mode` của Flutter, chỉ chọn và xóa thẻ vừa tạo bằng nút Thùng rác.
  - Tuyệt đối không bấm tọa độ mù, không chạm vào nút Nhắc nhở/Schedule khi dọn dẹp.
  - Áp dụng cơ chế best-effort cleanup trong khối `finally`, đảm bảo quá trình dọn dẹp không bao giờ làm gián đoạn hay ảnh hưởng kết quả kiểm thử chức năng.
