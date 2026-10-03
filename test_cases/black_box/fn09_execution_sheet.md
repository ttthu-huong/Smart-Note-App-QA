# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-09
## Dự án: Smart Note App
**Chức năng:** Chỉnh sửa Ghi chú & Tự động lưu (FN-09)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng chỉnh sửa ghi chú và tự động lưu (auto-save) cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-09** |
| **Chức năng** | **Chỉnh sửa Ghi chú & Tự động lưu** |
| **Người kiểm thử (Tester)** | QA Tester (Autonomous Execution) |
| **Ngày kiểm thử (Execution Date)** | 04/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990B / R5CW82ECF6M) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | v1.0.0+1 |
| **Kết nối mạng** | Wi-Fi |
| **Ghi chú môi trường khác** | Tài khoản Google đang đăng nhập |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đã đăng nhập và đang ở màn hình Trang chủ.
2. **Dữ liệu chuẩn bị trước:** Có ít nhất một ghi chú văn bản sẵn có trên Trang chủ để tiến hành mở ra chỉnh sửa.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-019** | **D01** | Nhập thêm chuỗi: `"[Đã cập nhật lúc 10:00]"` | 1. Chạm vào ghi chú để mở màn hình soạn thảo.<br>2. Nhập thêm nội dung mới vào phần văn bản.<br>3. Nhấn nút Quay lại (Back). | Ứng dụng quay về Trang chủ; thẻ ghi chú phản ánh nội dung mới vừa chỉnh sửa. | Chạm vào ghi chú "Họp Lab" để mở màn hình soạn thảo, nhập thêm chuỗi "[Đã cập nhật lúc 10:00]", sau đó nhấn Back. Thẻ ghi chú trên Trang chủ phản ánh chính xác nội dung mới vừa chỉnh sửa ("Nội dung ng [Đã cập nhật lúc 10:00]ắn gọn"). | PASS | `FN09_TC-BB-019_D01_01.png` | [Không] |
| **TC-BB-020** | **D01** | Đoạn văn bản: `"Nội dung kiểm tra tự động lưu"` | 1. Mở một ghi chú hiện có.<br>2. Gõ thêm nội dung mới vào vùng soạn thảo.<br>3. Ngừng nhập khoảng 1 giây (để cơ chế tự động lưu kích hoạt).<br>4. Thoát màn hình ghi chú (nhấn Back hoặc phím Home/Recent).<br>5. Mở lại ghi chú. | Nội dung vừa nhập vẫn còn nguyên vẹn sau khi mở lại ghi chú. | Mở ghi chú hiện có, gõ thêm đoạn văn bản "- Nội dung kiểm tra tự động lưu", chờ hơn 1 giây cho cơ chế tự động lưu hoạt động rồi nhấn Back thoát về Trang chủ. Khi mở lại ghi chú, toàn bộ nội dung vừa nhập vẫn còn nguyên vẹn. | PASS | `FN09_TC-BB-020_D01_01.png` | [Không] |

---

## 4. EVIDENCE NAMING CONVENTION

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN09_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Ví dụ:  
  • Thẻ ghi chú phản ánh nội dung đã cập nhật: `FN09_TC-BB-019_D01_01.png`  
  • Ghi chú mở lại vẫn giữ nguyên nội dung tự động lưu: `FN09_TC-BB-020_D01_01.png`
- **Video quay màn hình (Screen Recording):**  
  Cấu trúc: `FN09_[TC-ID]_[Data-ID].mp4`  
  Ví dụ: `FN09_TC-BB-020_D01.mp4`

---

## 5. BUG REPORT

| Bug ID | TC-ID | Data ID | Mô tả lỗi | Evidence | Severity | Status |
|---|---|---|---|---|---|---|
| *[Không có lỗi]* | - | - | Không phát sinh lỗi trong quá trình kiểm thử FN-09 | - | - | - |

---

## 6. RETEST

| Bug ID | TC-ID | Kết quả lần đầu | Kết quả Retest | Evidence Retest | Ngày Retest |
|---|---|---|---|---|---|
| *[Không có]* | - | - | - | - | - |

---

## 7. TEST DATA CLEANUP

- Các ghi chú chỉnh sửa tiếp tục được dùng cho kiểm thử Ghim, Thùng rác (FN-10/11/12) và Tìm kiếm (FN-23).

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **2** | TC-BB-019, TC-BB-020 |
| **Tổng Execution Items** | **2** | TC-BB-019 (1), TC-BB-020 (1) |
| **Số lượng PASS** | **2** | Toàn bộ 2 ca đều đạt yêu cầu |
| **Số lượng FAIL** | **0** | Không có ca nào thất bại |
| **Số lượng BLOCKED** | **0** | Không có ca nào bị chặn |
| **Số Bug phát hiện** | **0** | Không có bug |
| **Tỷ lệ thực thi (Execution Rate)** | **100%** | `(2 / 2) * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | **100%** | `(2 / 2) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 2 execution items của chức năng FN-09.
- [x] Đã ghi nhận Actual Result trung thực và chi tiết.
- [x] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [x] Đã lưu trữ Evidence (ảnh/video) theo đúng quy tắc đặt tên.
- [x] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report (không có fail).
- [x] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [x] Đã điền đầy đủ thông tin môi trường kiểm thử trong Mục 1.
- [x] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.