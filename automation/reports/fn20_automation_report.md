# BÁO CÁO THỰC THI AUTOMATION TEST — FN-20 (PIN / UNPIN NOTE)
## Dự án: Smart Note App
**Branch:** `huong`  
**Nhóm chức năng:** FN-20: Ghim & Bỏ ghim Ghi chú (Pin / Unpin Note)  
**Danh sách Test Cases:** TC-BB-024, TC-BB-025 (tổng 2 items)  
**Framework:** Python 3.13 + pytest + uiautomator2 + ADB  
**Thiết bị thực thi:** Samsung Galaxy S21 FE 5G (SM-G990B / R5CW82ECF6M), Android 14 (API 34)  
**Ngày thực thi:** 05/10/2026  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual / Automation Execution  

---

## 1. TỔNG QUAN KẾT QUẢ THỰC THI TỰ ĐỘNG

| Chỉ số | Số lượng / Giá trị | Ghi chú |
|---|---:|---|
| **Tổng số Test Cases** | **2** | TC-BB-024, TC-BB-025 |
| **Số lượng PASS** | **2** | TC-BB-024, TC-BB-025 (**100.00%**) |
| **Số lượng FAIL** | **0** | Không có test case nào thất bại |
| **Số lượng ERROR** | **0** | Kịch bản chạy thông suốt, không gặp lỗi môi trường |
| **Số lượng BLOCKED** | **0** | Cả 2 Test Case đều được thực thi trên thiết bị thật |
| **Thời gian thực thi** | **37.40s** | Chạy tuần tự và chụp ảnh screenshot tự động |
| **Báo cáo JUnit XML** | [`fn20_pin_note_junit.xml`](fn20_pin_note_junit.xml) | Xuất tự động qua pytest |

---

## 2. BẢNG CHI TIẾT KẾT QUẢ TỪNG TEST CASE

| TC-ID | Data ID | Test Data | Expected Result (Đặc tả) | Actual Result (Thực tế trên UI) | Trạng thái | Bug ID | Phân tích chi tiết & Cơ chế xác minh | Evidence |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **TC-BB-024** | **D01** | • Note: `"Ghi chú Test Ghim"`<br>• Thao tác: Nhấn giữ chọn thẻ & nhấn icon Ghim trên thanh công cụ | Trang chủ xuất hiện tiêu đề phân vùng *"Được ghim"*; thẻ ghi chú di chuyển lên nằm trong khu vực *"Được ghim"* ở phía trên cùng. | Nhấn giữ chọn thẻ ghi chú trên danh sách thường, nhấn icon "Ghim/Bỏ ghim hàng loạt" trên thanh công cụ. Phân vùng "Được ghim" xuất hiện và thẻ ghi chú nằm trong phân vùng "Được ghim" ở phía trên cùng. | **PASS** | — | Kích hoạt Selection Mode thành công; nút "Ghim/Bỏ ghim hàng loạt" cập nhật status sang 'pinned'; UI render header "Được ghim" và đặt card lên đầu danh sách. | [`FN20_TC-BB-024_D01_01.png`](../../evidence/fn20/FN20_TC-BB-024_D01_01.png) |
| **TC-BB-025** | **D01** | • Note: `"Ghi chú Test Ghim"` (đang được ghim)<br>• Thao tác: Nhấn giữ chọn thẻ & nhấn icon Bỏ ghim trên thanh công cụ | Thẻ ghi chú chuyển xuống phân vùng ghi chú thông thường bên dưới; nếu không còn ghi chú nào được ghim, tiêu đề *"Được ghim"* tự động ẩn đi. | Nhấn giữ chọn thẻ ghi chú đang được ghim, nhấn icon "Ghim/Bỏ ghim hàng loạt". Thẻ ghi chú chuyển xuống phân vùng ghi chú thông thường bên dưới; tiêu đề "Được ghim" tự động ẩn đi hoàn toàn. | **PASS** | — | Bỏ ghim thành công; số lượng pinned notes về 0 khiến header "Được ghim" và "Khác" tự động biến mất; ghi chú trở về danh sách thông thường an toàn. | [`FN20_TC-BB-025_D01_01.png`](../../evidence/fn20/FN20_TC-BB-025_D01_01.png) |

---

## 3. CƠ CHẾ TỰ ĐỘNG HÓA VÀ ĐẶC ĐIỂM KỸ THUẬT

### A. Tương tác Selection Mode của Flutter
- Dùng `d.touch.down(cx, cy)` 1.2s và `d.touch.up(cx, cy)` để kích hoạt sự kiện `onLongPress` chuẩn xác của Flutter NoteCard, mở `Selection Mode` của AppBar.
- Nút Ghim/Bỏ ghim được định vị bằng semantic locator `d(descriptionContains="Ghim/Bỏ ghim hàng loạt")` thay vì tọa độ mù.

### B. Kiểm chứng phân vùng giao diện (UI Partitioning)
- Trong `home_screen.dart`, giao diện phân tách rõ rệt:
  - Khi có ghi chú ghim: xuất hiện `SliverToBoxAdapter` chứa Text `"Được ghim"` (`pinnedSection`) và Text `"Khác"` (`othersSection`).
  - Khi không có ghi chú ghim: phân vùng `"Được ghim"` biến mất hoàn toàn.
- Kịch bản kiểm tra cả sự xuất hiện của header `"Được ghim"` và tương quan vị trí (bounds top) của thẻ ghi chú so với header để đảm bảo ghi chú thực sự nằm trong phân vùng ưu tiên.

### C. Cơ chế dọn dẹp an toàn (Best-effort Cleanup)
- Tự động dọn dẹp thẻ ghi chú test bằng `cleanup_note_via_selection()` trong khối `finally`.
- Không bấm tọa độ mù, không chạm nhầm vào nút Reminder hay Schedule, đảm bảo tính độc lập và toàn vẹn của dữ liệu sau mỗi lượt chạy.

---

## 4. TỔNG HỢP SỐ LIỆU AUTOMATION TOÀN HỆ THỐNG

| Nhóm chức năng | Tên nhóm | Tổng TCs | Đã Code & Chạy | PASS | FAIL | ERROR | Tỷ lệ PASS |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **FN-04** | Đăng nhập Email/Password | **4** | 4 | 1 | 3 | 0 | 25.00% |
| **FN-08** | Tạo Ghi chú văn bản mới | **3** | 3 | 3 | 0 | 0 | 100.00% |
| **FN-09** | Chỉnh sửa Ghi chú & Auto-save | **2** | 2 | 2 | 0 | 0 | 100.00% |
| **FN-20** | Ghim & Bỏ ghim Ghi chú | **2** | 2 | 2 | 0 | 0 | 100.00% |
| *Chưa automation* | FN-02 (5), FN-10/11/12 (3), FN-23 (4) | **12** | 0 | — | — | — | Planned |
| *Chưa automation* | FN-05 (2), FN-29/30 (4), FN-40/41 (2) | **8** | 0 | — | — | — | Deferred |
| **Tổng cộng** | **Toàn bộ hệ thống** | **31** | **11** | **8** | **3** | **0** | **72.73%** |

*Số liệu tổng hợp khớp với các nhóm chức năng đã thực thi.*
