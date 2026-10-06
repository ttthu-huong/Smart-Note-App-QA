# BÁO CÁO THỰC THI AUTOMATION TEST — FN-23 (SEARCH NOTE)
## Dự án: Smart Note App
**Branch:** `huong`  
**Nhóm chức năng:** FN-23: Tìm kiếm Ghi chú (Search Note)  
**Danh sách Test Cases:** TC-BB-026, TC-BB-027, TC-BB-028, TC-BB-029 (tổng 4 items)  
**Framework:** Python 3.13 + pytest + uiautomator2 + ADB  
**Thiết bị thực thi:** Samsung Galaxy S21 FE 5G (SM-G990B / R5CW82ECF6M), Android 14 (API 34)  
**Ngày thực thi:** 05/10/2026  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual / Automation Execution  

---

## 1. TỔNG QUAN KẾT QUẢ THỰC THI TỰ ĐỘNG

| Chỉ số | Số lượng / Giá trị | Ghi chú |
|---|---:|---|
| **Tổng số Test Cases** | **4** | TC-BB-026, TC-BB-027, TC-BB-028, TC-BB-029 |
| **Số lượng PASS** | **4** | TC-BB-026, TC-BB-027, TC-BB-028, TC-BB-029 (**100.00%**) |
| **Số lượng FAIL** | **0** | Không có test case nào thất bại |
| **Số lượng ERROR** | **0** | Kịch bản chạy thông suốt, không gặp lỗi môi trường |
| **Số lượng BLOCKED** | **0** | Cả 4 Test Case đều được thực thi trên thiết bị thật |
| **Thời gian thực thi** | **123.19s** (~2 phút 03 giây) | Chạy toàn bộ suite tuần tự và chụp ảnh screenshot tự động |
| **Báo cáo JUnit XML** | [`fn23_search_junit.xml`](fn23_search_junit.xml) | Xuất tự động qua pytest |

---

## 2. BẢNG CHI TIẾT KẾT QUẢ TỪNG TEST CASE

| TC-ID | Data ID | Test Data | Expected Result (Đặc tả) | Actual Result (Thực tế trên UI) | Trạng thái | Bug ID | Phân tích chi tiết & Cơ chế xác minh | Evidence |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **TC-BB-026** | **D01** | • Note: Title = `"Lịch thi học kỳ"`, Content = `"Ôn tập các môn cuối kỳ"`<br>• Từ khóa: `"Lịch thi"` | Danh sách kết quả hiển thị thẻ ghi chú *"Lịch thi học kỳ"* có chứa từ khóa khớp trong tiêu đề. | Nhập từ khóa "Lịch thi" vào ô tìm kiếm. Danh sách kết quả hiển thị chính xác thẻ ghi chú "Lịch thi học kỳ" tương ứng với tiêu đề. | **PASS** | — | Mở SearchScreen, nhập từ khóa tìm kiếm vào ô EditText, chờ debounce 1.2s; xác minh thẻ ghi chú xuất hiện trên UI qua semantic accessibility. | [`FN23_TC-BB-026_D01_01.png`](../../evidence/fn23/FN23_TC-BB-026_D01_01.png) |
| **TC-BB-027** | **D01** | • Note: Title = `"Tạp vụ"`, Content = `"mua thêm giấy in A4"`<br>• Từ khóa: `"giấy in A4"` | Danh sách kết quả hiển thị thẻ ghi chú *"Tạp vụ"* có chứa đoạn văn bản tương ứng trong phần nội dung. | Nhập từ khóa "giấy in A4" vào ô tìm kiếm. Danh sách kết quả hiển thị thẻ ghi chú "Tạp vụ" có chứa đúng đoạn nội dung tương ứng. | **PASS** | — | Tìm kiếm theo nội dung văn bản (FTS/LIKE trong SQLite); thẻ ghi chú hiển thị đầy đủ tiêu đề và nội dung trên màn hình kết quả tìm kiếm. | [`FN23_TC-BB-027_D01_01.png`](../../evidence/fn23/FN23_TC-BB-027_D01_01.png) |
| **TC-BB-028** | **D01** | • Từ khóa không tồn tại: `"chuoi_khong_ton_tai_999"` | Hiển thị thông báo hoặc màn hình rỗng *"Không tìm thấy kết quả"*, gợi ý *"Thử từ khóa khác"*. | Ứng dụng hiển thị `EmptyStateWidget` với tiêu đề "Không tìm thấy kết quả", phụ đề "Thử từ khóa khác" và nút "Xóa bộ lọc". | **PASS** | — | Xác thực trạng thái rỗng (Empty State) chính xác theo đặc tả; các thành phần văn bản hiển thị rõ ràng trên giao diện người dùng. | [`FN23_TC-BB-028_D01_01.png`](../../evidence/fn23/FN23_TC-BB-028_D01_01.png) |
| **TC-BB-029** | **D01** | • Ký tự đặc biệt & SQL Injection: `"' OR 1=1 -- % _ @#$"` | Ứng dụng xử lý an toàn, không crash, không phát sinh lỗi ngoại lệ hoặc lộ dữ liệu ngoài phạm vi tìm kiếm; hiển thị thông báo không tìm thấy kết quả *"Không tìm thấy kết quả"*. | Ứng dụng xử lý chuỗi ký tự đặc biệt và cú pháp SQL injection an toàn tuyệt đối; tiến trình app không bị crash; hiển thị màn hình rỗng "Không tìm thấy kết quả". | **PASS** | — | Kiểm thử bảo mật & an toàn dữ liệu; SQLite sử dụng parameterized query nên chuỗi payload không làm lộ dữ liệu hay gây exception; UI hiển thị trạng thái rỗng an toàn. | [`FN23_TC-BB-029_D01_01.png`](../../evidence/fn23/FN23_TC-BB-029_D01_01.png) |

---

## 3. CƠ CHẾ TỰ ĐỘNG HÓA VÀ ĐẶC ĐIỂM KỸ THUẬT

### A. Tương tác Tìm kiếm qua SearchScreen và EditText
- Chạm vào thanh tìm kiếm (`"Tìm kiếm"`) trên HomeScreen để điều hướng đến `SearchScreen`.
- Sử dụng `android.widget.EditText` trên `SearchScreen` với hint `'Tìm kiếm ghi chú của bạn...'` để nhập chuỗi truy vấn qua `set_text()`.
- Chờ độ trễ debounce (1.2s) để hệ thống hoàn tất truy vấn SQLite và kích hoạt cập nhật State trong `NoteProvider`.
- Thu gọn bàn phím ảo (Samsung Honeyboard) bằng lệnh Back có kiểm soát để danh sách kết quả hoặc trạng thái rỗng hiển thị đầy đủ trên màn hình.

### B. Xử lý trạng thái tìm kiếm (Search State Lifecycle)
- Khi rời `SearchScreen`, kịch bản tự động chạm vào nút `arrow_back` nằm trong SearchBar (thay vì nhấn phím Back vật lý đơn thuần) nhằm kích hoạt `NoteProvider.clearSearch()`.
- Điều này ngăn chặn việc màn hình chính `HomeScreen` bị kẹt ở chế độ `_isSearching = true` dẫn đến việc chỉ hiển thị danh sách đã lọc thay vì toàn bộ ghi chú.

### C. Cơ chế kiểm chứng trạng thái rỗng và bảo mật dữ liệu
- Đối với từ khóa không tồn tại (`TC-BB-028`) và chuỗi payload đặc biệt (`TC-BB-029`), kịch bản kiểm tra:
  1. Tiến trình ứng dụng (`com.example.smart_note_app`) vẫn đang hoạt động (`app_current()['package'] == package`).
  2. UI hiển thị các thành phần của `EmptyStateWidget`: Text `"Không tìm thấy kết quả"` và `"Thử từ khóa khác"`.
  3. Không có thẻ ghi chú nào bị rò rỉ trái phép do SQL injection payload.

### D. Cơ chế dọn dẹp an toàn (Best-effort Cleanup)
- Tự động dọn dẹp các thẻ ghi chú kiểm thử thông qua Selection Mode (nhấn giữ thẻ -> bấm icon Thùng rác) trong khối `finally`.
- Đảm bảo môi trường HomeScreen luôn sạch sẽ, không ảnh hưởng đến các lần thực thi tiếp theo.

---

## 4. TỔNG HỢP SỐ LIỆU AUTOMATION TOÀN HỆ THỐNG

| Nhóm chức năng | Tên nhóm | Tổng TCs | Đã Code & Chạy | PASS | FAIL | ERROR | Tỷ lệ PASS |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **FN-04** | Đăng nhập Email/Password | **4** | 4 | 1 | 3 | 0 | 25.00% |
| **FN-08** | Tạo Ghi chú văn bản mới | **3** | 3 | 3 | 0 | 0 | 100.00% |
| **FN-09** | Chỉnh sửa Ghi chú & Auto-save | **2** | 2 | 2 | 0 | 0 | 100.00% |
| **FN-20** | Ghim & Bỏ ghim Ghi chú | **2** | 2 | 2 | 0 | 0 | 100.00% |
| **FN-23** | Tìm kiếm Ghi chú (Search Note) | **4** | 4 | 4 | 0 | 0 | 100.00% |
| *Chưa automation* | FN-02 (5), FN-10/11/12 (3) | **8** | 0 | — | — | — | Planned |
| *Chưa automation* | FN-05 (2), FN-29/30 (4), FN-40/41 (2) | **8** | 0 | — | — | — | Deferred |
| **Tổng cộng** | **Toàn bộ hệ thống** | **31** | **15** | **12** | **3** | **0** | **80.00%** |

*Số liệu tổng hợp khớp với các nhóm chức năng đã thực thi.*
