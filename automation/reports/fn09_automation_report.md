# BÁO CÁO THỰC THI AUTOMATION TEST — FN-09 (EDIT NOTE / AUTO-SAVE)
## Dự án: Smart Note App
**Branch:** `huong`  
**Nhóm chức năng:** FN-09: Chỉnh sửa Ghi chú & Tự động lưu  
**Danh sách Test Cases:** TC-BB-019, TC-BB-020 (tổng 2 items)  
**Framework:** Python 3.13 + pytest + uiautomator2 + ADB  
**Thiết bị thực thi:** Samsung Galaxy S21 FE 5G (SM-G990B / R5CW82ECF6M), Android 14 (API 34)  
**Ngày thực thi:** 05/10/2026  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual / Automation Execution  

---

## 1. TỔNG QUAN KẾT QUẢ THỰC THI TỰ ĐỘNG

| Chỉ số | Số lượng / Giá trị | Ghi chú |
|---|---:|---|
| **Tổng số Test Cases** | **2** | TC-BB-019, TC-BB-020 |
| **Số lượng PASS** | **2** | TC-BB-019, TC-BB-020 (**100.00%**) |
| **Số lượng FAIL** | **0** | Không có test case nào thất bại |
| **Số lượng ERROR** | **0** | Kịch bản chạy thông suốt, không gặp lỗi môi trường |
| **Số lượng BLOCKED** | **0** | Cả 2 Test Case đều được thực thi trên thiết bị thật |
| **Thời gian thực thi** | **132.16s (02:12)** | Chạy tuần tự, bao gồm thời gian chờ auto-save và dọn dẹp an toàn |
| **Báo cáo JUnit XML** | [`fn09_edit_note_junit.xml`](fn09_edit_note_junit.xml) | Xuất tự động qua pytest |

---

## 2. BẢNG CHI TIẾT KẾT QUẢ TỪNG TEST CASE

| TC-ID | Data ID | Test Data | Expected Result (Đặc tả) | Actual Result (Thực tế trên UI) | Trạng thái | Bug ID | Phân tích chi tiết & Cơ chế xác minh | Evidence |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **TC-BB-019** | **D01** | • Note ban đầu: `"Họp Lab"`<br>• Nhập thêm: `"[Đã cập nhật lúc 10:00]"` | Ứng dụng quay về Trang chủ; thẻ ghi chú phản ánh nội dung mới vừa chỉnh sửa. | Thẻ ghi chú trên HomeScreen phản ánh chính xác chuỗi nội dung mới vừa chỉnh sửa `"[Đã cập nhật lúc 10:00]"`. | **PASS** | — | Mở note thành công qua dynamic locator; dán text qua native clipboard; thoát về Trang chủ và polling kiểm tra NoteCard cập nhật. | [`FN09_TC-BB-019_D01_01.png`](../../evidence/fn09/FN09_TC-BB-019_D01_01.png) |
| **TC-BB-020** | **D01** | • Note ban đầu: `"Ghi chú Auto-save"`<br>• Nhập thêm: `"- Nội dung kiểm tra tự động lưu"`<br>• Ngừng nhập: 2.0s (> 1000ms debounce) | Nội dung vừa nhập vẫn còn nguyên vẹn sau khi mở lại ghi chú. | Dừng thao tác 2.0s cho debounce timer kích hoạt lưu ngầm; thoát ra và mở lại note, toàn bộ nội dung mới vẫn còn nguyên vẹn trong EditorScreen. | **PASS** | — | Xác minh thành công cơ chế `_autoSaveTimer` lưu trực tiếp xuống SQLite khi người dùng ngừng nhập, nạp lại đúng vào document khi mở lại note. | [`FN09_TC-BB-020_D01_01.png`](../../evidence/fn09/FN09_TC-BB-020_D01_01.png) |

---

## 3. CƠ CHẾ TỰ ĐỘNG HÓA VÀ ĐẶC ĐIỂM KỸ THUẬT

### A. Phương thức nhập liệu vào QuillEditor
- Kế thừa giải pháp đã chuẩn hóa từ FN-08: Sử dụng `d.set_clipboard(content)` kết hợp native JSON-RPC `d.jsonrpc.pasteClipboard()`.
- Phương thức này đảm bảo gửi delta text change event trực tiếp đến `QuillController.document`, đặt cờ `_isDirty = true` và kích hoạt hàm lắng nghe `_onTextChanged()`.

### B. Cơ chế kiểm chứng Auto-save (TC-BB-020)
- Trong mã nguồn `lib/screens/editor_screen.dart`, sự kiện thay đổi văn bản kích hoạt `_autoSaveTimer` với debounce **1000ms**:
  ```dart
  _autoSaveTimer = Timer(const Duration(milliseconds: 1000), () {
    if (mounted) _saveNote(isAutosave: true);
  });
  ```
- Automation tạm dừng chính xác **2.0 giây** ngay trong `EditorScreen` mà không nhấn bất kỳ phím điều hướng nào, đảm bảo `_autoSaveTimer` kích hoạt hàm `_saveNote(isAutosave: true)` ghi xuống SQLite.
- Thoát ra `HomeScreen`, sau đó chạm vào thẻ ghi chú để mở lại `EditorScreen`.
- Trích xuất UI hierarchy và delta của `QuillEditor`, xác nhận chuỗi `"- Nội dung kiểm tra tự động lưu"` đã được nạp lại đầy đủ từ SQLite vào editor document.

### C. Cơ chế dọn dẹp an toàn (Best-effort Cleanup)
- Dùng `cleanup_note_via_selection()` trong khối `finally` cho cả hai test case.
- Nhấn giữ thẻ ghi chú 1.2s kích hoạt `Selection Mode`, sau đó nhấn nút Thùng rác trên AppBar.
- Tuyệt đối không nhấn vào nút Nhắc nhở/Schedule hay bấm tọa độ mù; nếu quá trình cleanup có ngoại lệ thì được catch an toàn, không bao giờ làm FAIL kết quả kiểm thử chức năng.
