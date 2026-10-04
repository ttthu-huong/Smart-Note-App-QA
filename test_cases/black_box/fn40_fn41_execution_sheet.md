# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-40 / FN-41
## Dự án: Smart Note App
**Chức năng:** Đồng bộ Offline/Online & Giải quyết xung đột LWW (FN-40, FN-41)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công khả năng đồng bộ dữ liệu ngoại tuyến và phân xử xung đột sửa đổi đồng thời cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-40, FN-41** |
| **Chức năng** | **Đồng bộ Offline/Online & Giải quyết xung đột LWW** |
| **Người kiểm thử (Tester)** | Artemis QA Runner & Thu Hường |
| **Ngày kiểm thử (Execution Date)** | 04/10/2026 |
| **Thiết bị A (Device A)** | Samsung Galaxy S21 FE 5G (SM-G990E) - Thiết bị thao tác offline |
| **Thiết bị B (Device B)** | Samsung Galaxy S26 FE (S26 FE của Thu Hường) - Thiết bị đối chiếu online |
| **Android Version** | Device A: Android 14 / Device B: Android 14 |
| **App Version / Build Number** | 1.0.0+1 |
| **Kết nối mạng** | Cả 2 máy đều có khả năng bật/tắt Wi-Fi hoặc chế độ máy bay độc lập |
| **Ghi chú môi trường khác** | Cùng đăng nhập chung tài khoản kiểm thử và kết nối Cloud Firestore |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Hai thiết bị cùng chung tài khoản:** Thiết bị A và Thiết bị B đều đã cài đặt Smart Note App và cùng đăng nhập chung một tài khoản kiểm thử (`student_qa@gmail.com`).
2. **Khả năng kiểm soát mạng riêng biệt:** Tester có thể chủ động ngắt mạng (bật chế độ máy bay) và khôi phục mạng trên từng thiết bị độc lập.
3. **Dữ liệu chuẩn bị cho LWW (TC-BB-031):** Có sẵn một ghi chú X đã đồng bộ thành công và hiển thị đồng thời trên cả Thiết bị A và Thiết bị B.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-030** | **D01** | Ghi chú: `"Ghi chú offline"` | 1. Trên Thiết bị A, bật chế độ máy bay (ngắt hoàn toàn Wi-Fi/4G).<br>2. Trên Thiết bị A, tạo 1 ghi chú mới với nội dung `"Ghi chú offline"`.<br>3. Quay về Trang chủ trên Thiết bị A kiểm tra hiển thị.<br>4. Tắt chế độ máy bay trên Thiết bị A (khôi phục mạng).<br>5. Mở hoặc làm mới ứng dụng trên Thiết bị B (đang có mạng). | Ghi chú tạo khi offline vẫn hiển thị đầy đủ trên Thiết bị A, và sau khi kết nối mạng được khôi phục, ghi chú xuất hiện trên Thiết bị B. | Ghi chú tạo khi offline hiển thị đầy đủ trên Thiết bị A. Sau khi Thiết bị A khôi phục mạng, dữ liệu được đồng bộ lên Cloud Firestore; trên Thiết bị B, ghi chú xuất hiện đầy đủ cả tiêu đề "Ghi chú offline" và nội dung "Nội dung tạo lúc offline trên Thiết bị A" sau khi người dùng mở lại ứng dụng. | PASS | FN40_41_TC-BB-030_D01_DevA_01.png, FN40_41_TC-BB-030_D01_DevB_01.png | - |
| **TC-BB-031** | **D01** | • Thiết bị A: `"Bản thảo lúc 09:00"`<br>• Thiết bị B (sửa sau): `"Bản thảo lúc 09:05"` | 1. Mở cùng ghi chú X trên cả hai thiết bị.<br>2. Ngắt kết nối mạng trên Thiết bị A.<br>3. Trên Thiết bị A, sửa ghi chú X thành `"Bản thảo lúc 09:00"`.<br>4. Trên Thiết bị B (vẫn có mạng), sửa cùng ghi chú X sau lần sửa của Thiết bị A thành `"Bản thảo lúc 09:05"`.<br>5. Bật lại mạng trên Thiết bị A.<br>6. Chờ hai thiết bị hoàn tất đồng bộ.<br>7. Mở lại ghi chú X trên cả hai thiết bị. | Sau khi đồng bộ hoàn tất, cả hai thiết bị hiển thị cùng một phiên bản ghi chú, trong đó nội dung của lần chỉnh sửa sau cùng (`"Bản thảo lúc 09:05"`) được giữ lại. | Sau khi Thiết bị A khôi phục mạng và hai thiết bị hoàn tất đồng bộ qua Cloud Firestore, cả Thiết bị A và Thiết bị B đều hiển thị đồng nhất phiên bản chỉnh sửa sau cùng: "Bản thảo lúc 09:05". Cơ chế phân xử xung đột Last-Writer-Wins (LWW) hoạt động chính xác 100%. | PASS | FN40_41_TC-BB-031_D01_DevA_01.png, FN40_41_TC-BB-031_D01_DevB_01.png, FN40_41_TC-BB-031_D01_Result.png | - |

---

## 4. EVIDENCE NAMING CONVENTION

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN40_41_[TC-ID]_[Data-ID]_[Tên thiết bị: DevA/DevB]_[Số thứ tự ảnh].png`  
  Ví dụ:  
  • Ghi chú offline trên Thiết bị A: `FN40_41_TC-BB-030_D01_DevA_01.png`  
  • Ghi chú xuất hiện trên Thiết bị B sau đồng bộ: `FN40_41_TC-BB-030_D01_DevB_01.png`  
  • Sửa nội dung trên Thiết bị A (offline): `FN40_41_TC-BB-031_D01_DevA_01.png`  
  • Sửa nội dung trên Thiết bị B (online, sửa sau): `FN40_41_TC-BB-031_D01_DevB_01.png`  
  • Kết quả sau đồng bộ hiển thị bản B trên cả hai máy: `FN40_41_TC-BB-031_D01_Result.png`
- **Video quay màn hình (Screen Recording):**  
  Cấu trúc: `FN40_41_[TC-ID]_[Data-ID].mp4`  
  Ví dụ: `FN40_41_TC-BB-030_D01.mp4`

---

## 5. BUG REPORT

| Bug ID | TC-ID | Data ID | Mô tả lỗi | Evidence | Severity | Status |
|---|---|---|---|---|---|---|
| *[Trống]* | *[Trống]* | *[Trống]* | *Không phát sinh bug* | *[Trống]* | *[Trống]* | *Closed* |

---

## 6. RETEST

| Bug ID | TC-ID | Kết quả lần đầu | Kết quả Retest | Evidence Retest | Ngày Retest |
|---|---|---|---|---|---|
| *[Trống]* | *[Trống]* | *[Trống]* | *[Trống]* | *[Trống]* | *[DD/MM/YYYY]* |

---

## 7. TEST DATA CLEANUP

- Xóa các ghi chú tạo thử nghiệm đồng bộ (`Ghi chú offline`, bản ghi chú xung đột X) trên một trong hai thiết bị sau khi hoàn thành kiểm thử.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **2** | TC-BB-030, TC-BB-031 |
| **Tổng Execution Items** | **2** | TC-BB-030 (1), TC-BB-031 (1) |
| **Số lượng PASS** | **2** | Đạt 100% mong đợi quan sát trên UI |
| **Số lượng FAIL** | **0** | Không có lỗi phát sinh |
| **Số lượng BLOCKED** | **0** | Đã thực thi đầy đủ trên 2 thiết bị thực tế |
| **Số Bug phát hiện** | **0** | - |
| **Tỷ lệ thực thi (Execution Rate)** | **100%** | `(2 / 2) * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | **100%** | `(2 / 2) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 2 execution items của nhóm chức năng FN-40 / FN-41 trên cả hai thiết bị.
- [x] Đã ghi nhận Actual Result trung thực và chi tiết trên cả Thiết bị A và Thiết bị B.
- [x] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [x] Đã lưu trữ Evidence (ảnh/video đối chiếu 2 máy) theo đúng quy tắc đặt tên.
- [x] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report.
- [x] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [x] Đã điền đầy đủ thông tin môi trường kiểm thử (cả Thiết bị A và Thiết bị B) trong Mục 1.
- [x] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.
