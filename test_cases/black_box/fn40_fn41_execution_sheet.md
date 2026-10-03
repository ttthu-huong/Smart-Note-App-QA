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
| **Người kiểm thử (Tester)** | [Điền khi thực hiện] |
| **Ngày kiểm thử (Execution Date)** | [Điền khi thực hiện] (DD/MM/YYYY) |
| **Thiết bị A (Device A)** | [Điền khi thực hiện] (VD: Google Pixel 7 - Thiết bị thao tác offline) |
| **Thiết bị B (Device B)** | [Điền khi thực hiện] (VD: Samsung S22 / Máy ảo Android - Thiết bị đối chiếu online) |
| **Android Version** | Device A: [Android ...] / Device B: [Android ...] |
| **App Version / Build Number** | [Điền khi thực hiện] (Cùng một phiên bản app trên cả 2 máy) |
| **Kết nối mạng** | Cả 2 máy đều có khả năng bật/tắt Wi-Fi hoặc chế độ máy bay độc lập |
| **Ghi chú môi trường khác** | [Nếu có] |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Hai thiết bị cùng chung tài khoản:** Thiết bị A và Thiết bị B đều đã cài đặt Smart Note App và cùng đăng nhập chung một tài khoản kiểm thử (`student_qa@gmail.com`).
2. **Khả năng kiểm soát mạng riêng biệt:** Tester có thể chủ động ngắt mạng (bật chế độ máy bay) và khôi phục mạng trên từng thiết bị độc lập.
3. **Dữ liệu chuẩn bị cho LWW (TC-BB-031):** Có sẵn một ghi chú X đã đồng bộ thành công và hiển thị đồng thời trên cả Thiết bị A và Thiết bị B.

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | Data ID | Test Data | Các bước thực hiện | Expected Result | Actual Result | PASS/FAIL/BLOCKED | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-030** | **D01** | Ghi chú: `"Ghi chú offline"` | 1. Trên Thiết bị A, bật chế độ máy bay (ngắt hoàn toàn Wi-Fi/4G).<br>2. Trên Thiết bị A, tạo 1 ghi chú mới với nội dung `"Ghi chú offline"`.<br>3. Quay về Trang chủ trên Thiết bị A kiểm tra hiển thị.<br>4. Tắt chế độ máy bay trên Thiết bị A (khôi phục mạng).<br>5. Mở hoặc làm mới ứng dụng trên Thiết bị B (đang có mạng). | Ghi chú tạo khi offline vẫn hiển thị đầy đủ trên Thiết bị A, và sau khi kết nối mạng được khôi phục, ghi chú xuất hiện trên Thiết bị B. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |
| **TC-BB-031** | **D01** | • Thiết bị A: `"Bản thảo lúc 09:00"`<br>• Thiết bị B (sửa sau): `"Bản thảo lúc 09:05"` | 1. Mở cùng ghi chú X trên cả hai thiết bị.<br>2. Ngắt kết nối mạng trên Thiết bị A.<br>3. Trên Thiết bị A, sửa ghi chú X thành `"Bản thảo lúc 09:00"`.<br>4. Trên Thiết bị B (vẫn có mạng), sửa cùng ghi chú X sau lần sửa của Thiết bị A thành `"Bản thảo lúc 09:05"`.<br>5. Bật lại mạng trên Thiết bị A.<br>6. Chờ hai thiết bị hoàn tất đồng bộ.<br>7. Mở lại ghi chú X trên cả hai thiết bị. | Sau khi đồng bộ hoàn tất, cả hai thiết bị hiển thị cùng một phiên bản ghi chú, trong đó nội dung của lần chỉnh sửa sau cùng (`"Bản thảo lúc 09:05"`) được giữ lại. | [Điền khi test] | [Trống] | [Điền khi test] | [Nếu có] |

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
| *[Trống]* | *[Trống]* | *[Trống]* | *[Ghi nhận khi có bug]* | *[Tên file evidence]* | *[Critical / Major / Minor]* | *[Open / In Progress / Fixed]* |

---

## 6. RETEST

| Bug ID | TC-ID | Kết quả lần đầu | Kết quả Retest | Evidence Retest | Ngày Retest |
|---|---|---|---|---|---|
| *[Trống]* | *[Trống]* | *[FAIL]* | *[PASS / FAIL]* | *[File evidence retest]* | *[DD/MM/YYYY]* |

---

## 7. TEST DATA CLEANUP

- Xóa các ghi chú tạo thử nghiệm đồng bộ (`Ghi chú offline`, bản ghi chú xung đột X) trên một trong hai thiết bị sau khi hoàn thành kiểm thử.

---

## 8. TEST SUMMARY

| Chỉ số đo lường | Giá trị | Ghi chú |
|---|---:|---|
| **Tổng Test Case chính thức** | **2** | TC-BB-030, TC-BB-031 |
| **Tổng Execution Items** | **2** | TC-BB-030 (1), TC-BB-031 (1) |
| **Số lượng PASS** | [Điền sau khi test] | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng FAIL** | [Điền sau khi test] | Tester tổng hợp sau khi chạy thực tế |
| **Số lượng BLOCKED** | [Điền sau khi test] | Các ca không thể chạy do lỗi môi trường/thiết bị |
| **Số Bug phát hiện** | [Điền sau khi test] | Tổng số lỗi ghi nhận trong bảng Bug Report |
| **Tỷ lệ thực thi (Execution Rate)** | [Điền sau khi test] % | `(PASS + FAIL) / 2 * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | [Điền sau khi test] % | `PASS / (PASS + FAIL) * 100%` |

---

## 9. CHECKLIST HOÀN TẤT KIỂM THỬ

- [ ] Đã thực hiện đầy đủ 2 execution items của nhóm chức năng FN-40 / FN-41 trên cả hai thiết bị.
- [ ] Đã ghi nhận Actual Result trung thực và chi tiết trên cả Thiết bị A và Thiết bị B.
- [ ] Đã đánh giá trạng thái PASS / FAIL / BLOCKED cho từng dòng.
- [ ] Đã lưu trữ Evidence (ảnh/video đối chiếu 2 máy) theo đúng quy tắc đặt tên.
- [ ] Các ca FAIL đều đã được gán Bug ID và ghi vào Bảng Bug Report.
- [ ] Tuyệt đối không tự ý sửa đổi Expected Result sau khi test.
- [ ] Đã điền đầy đủ thông tin môi trường kiểm thử (cả Thiết bị A và Thiết bị B) trong Mục 1.
- [ ] Đã thực hiện Retest và cập nhật bảng Retest nếu có Bug được fix.
