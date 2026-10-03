# BÁO CÁO TỔNG KẾT THỰC THI KIỂM THỬ BLACK-BOX
## Dự án: Smart Note App
**Branch:** `huong`  
**Ngày thực thi:** 04/10/2026  
**Người thực hiện:** Artemis QA Runner  
**Thiết bị kiểm thử:** Samsung Galaxy S21 FE 5G (SM-G990B), Android 14 (API 34)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  

---

## I. TỔNG QUAN KẾT QUẢ THỰC THI (SCOPE ĐÊM NAY)

Theo chỉ đạo phạm vi kiểm thử đêm nay, toàn bộ 9 nhóm chức năng mục tiêu đã được thực thi độc lập và khách quan trên thiết bị thật:
- **FN-02**: Tạo & Quản lý ghi chú cơ bản (11 items)
- **FN-04**: Các loại ghi chú mở rộng (4 items)
- **FN-05**: Định dạng văn bản & Tùy chỉnh màu sắc (2 items)
- **FN-08**: Gắn nhãn & Phân loại ghi chú (3 items)
- **FN-09**: Lưu trữ & Bỏ lưu trữ (2 items)
- **FN-10 / FN-11 / FN-12**: Vòng đời ghi chú: Thùng rác, Khôi phục, Xóa vĩnh viễn (3 items)
- **FN-20**: Ghim & Bỏ ghim ghi chú (2 items)
- **FN-23**: Tìm kiếm ghi chú theo từ khóa (4 items)
- **FN-29 / FN-30**: Khóa & Mở khóa sinh trắc học (4 items)

*(Lưu ý: FN-40 & FN-41 gồm TC-BB-030 và TC-BB-031 được giữ nguyên hoàn toàn theo chỉ đạo để kiểm thử riêng vào ngày mai khi có đủ 2 thiết bị).*

### Bảng số liệu tổng hợp

| Chỉ số | Số lượng | Ghi chú |
|---|---:|---|
| **Tổng Test Cases (Đêm nay)** | **29** | Loại trừ 2 TC của FN-40/41 |
| **Tổng Execution Items** | **37** | 35 items thực tế trong 9 sheet |
| **PASS** | **27** | Đạt 100% mong đợi quan sát trên UI |
| **FAIL** | **4** | Gặp lỗi chức năng/crash thực tế |
| **BLOCKED** | **4** | Không thể cung cấp sinh trắc học vật lý từ xa |
| **Số lượng Bug phát hiện** | **4** | Đã tạo Bug ID và mô tả chi tiết |
| **Retest** | **0** | Chưa có bản build sửa lỗi |

---

## II. CHI TIẾT CÁC CHỨC NĂNG BỊ BLOCKED VÀ NGUYÊN NHÂN

| Nhóm FN | TC-ID | Data ID | Lý do BLOCKED |
|---|---|---|---|
| **FN-29 / FN-30** | TC-BB-012 | D01 | Thiết bị vật lý yêu cầu người dùng xác thực trực tiếp trên cảm biến sinh trắc học (vân tay/khuôn mặt) để bật khóa ghi chú; hệ thống hiển thị hộp thoại xác thực nhưng không thể quét sinh trắc học qua ADB từ xa. |
| **FN-29 / FN-30** | TC-BB-013 | D01 | Cần quét dấu vân tay/khuôn mặt hợp lệ đã đăng ký trên máy; không thể thực hiện qua điều khiển tự động. |
| **FN-29 / FN-30** | TC-BB-014 | D01 | Cần thao tác quét dấu vân tay không khớp trên cảm biến vật lý thực tế của thiết bị (thực tế quan sát hệ thống quét khuôn mặt không thấy hiển thị "Không phát hiện thấy khuôn mặt"). |
| **FN-29 / FN-30** | TC-BB-015 | D01 | Chuỗi kiểm thử phụ thuộc vào việc khóa ghi chú trước đó không hoàn tất; thao tác bấm Cancel đã được xác minh đóng hộp thoại an toàn. |

*(FN-40 / FN-41 được tạm hoãn chưa thực thi đêm nay theo yêu cầu, không ghi BLOCKED vào sheet của FN-40/41).*

---

## III. DANH SÁCH BUG PHÁT HIỆN

| Bug ID | Chức năng | TC-ID & Data ID | Mô tả lỗi | Severity |
|---|---|---|---|---|
| **BUG-FN02-01** | FN-02 | TC-BB-003 D03 | Thanh công cụ định dạng (bold, italic, header...) không hiển thị trực tiếp khi soạn thảo ghi chú văn bản thường mà chỉ xuất hiện trong menu phụ hoặc yêu cầu bôi đen. | Minor |
| **BUG-BB-002** | FN-04 | TC-BB-006 D01 | Ứng dụng bị Crash (`LateInitializationError` trên `_drawingController`) khi người dùng bấm vào nút tạo ghi chú vẽ tay từ thanh công cụ HomeScreen. | Critical |
| **BUG-BB-003** | FN-04 | TC-BB-007 D01 | Ứng dụng gặp lỗi ngoại lệ quyền truy cập (`permission_handler`) và không mở được bộ chọn ảnh khi bấm tạo ghi chú hình ảnh từ HomeScreen. | Major |
| **BUG-BB-004** | FN-04 | TC-BB-008 D01 | Ứng dụng bị crash hoặc không thể kích hoạt ghi âm (`record` permission) khi bấm tạo ghi chú âm thanh từ HomeScreen. | Major |

---

## IV. LƯU TRỮ EVIDENCE

Toàn bộ ảnh chụp màn hình bằng chứng thực tế được tổ chức theo đúng quy chuẩn tên gọi và lưu trong các thư mục tương ứng:
- `evidence/fn02/`: 22 ảnh chụp cho 11 items FN-02
- `evidence/fn04/`: 8 ảnh chụp cho 4 items FN-04
- `evidence/fn05/`: 3 ảnh chụp cho 2 items FN-05
- `evidence/fn08/`: 3 ảnh chụp cho 3 items FN-08
- `evidence/fn09/`: 2 ảnh chụp cho 2 items FN-09
- `evidence/fn10_11_12/`: 3 ảnh chụp cho 3 items FN-10/11/12
- `evidence/fn20/`: 2 ảnh chụp cho 2 items FN-20
- `evidence/fn23/`: 4 ảnh chụp cho 4 items FN-23
- `evidence/fn29_30/`: 4 ảnh chụp cho 4 items FN-29/30

---

## V. THÔNG TIN PHIÊN BẢN VÀ COMMIT

- **Branch:** `huong`
- **Commit Message:** `qa: execute black-box tests and update results`
- **Commit Hash:** `c986cd7`
