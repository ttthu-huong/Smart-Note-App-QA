# BÁO CÁO TỔNG KẾT THỰC THI KIỂM THỬ BLACK-BOX
## Dự án: Smart Note App
**Branch:** `huong`  
**Ngày cập nhật & kiểm toán:** 06/10/2026  
**Người thực hiện:** Artemis QA Runner & Thu Hường  
**Thiết bị kiểm thử:** 
- Thiết bị A: Samsung Galaxy S21 FE 5G (SM-G990E), Android 14 (API 34)
- Thiết bị B: Samsung Galaxy S26 FE, Android 14
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  

---

## I. TỔNG QUAN KẾT QUẢ THỰC THI (TOÀN BỘ 10 NHÓM CHỨC NĂNG)

Dự án đã hoàn tất thiết kế hộp đen chuyên sâu cho **10 nhóm chức năng trọng tâm** (118 Test Cases, 134 Execution Items). Trong đó:
- **7 nhóm chức năng đã thực thi hoàn tất** trên thiết bị thật: FN-02, FN-04, FN-05, FN-08, FN-09, FN-10/11/12, FN-20 (90 Execution Items).
- **3 nhóm chức năng đã hoàn thành thiết kế & phê duyệt**, đang ở trạng thái chuẩn bị chờ thực thi: FN-23, FN-29/30, FN-40/41 (44 Execution Items).

### Bảng số liệu tổng hợp toàn diện (Global Metrics)

| Chỉ số đo lường | Số lượng | Tỷ lệ | Ghi chú giải thích |
|---|---:|---:|---|
| **Tổng số Test Cases chính thức (TC)** | **118** | **100%** | Bao phủ toàn bộ 10 nhóm chức năng trọng tâm |
| **Tổng số Execution Items (Exec)** | **134** | **100%** | 134 items chi tiết trong 10 file Execution Sheet |
| **Số Execution Items đã thực thi (Executed)** | **90** | **67.16%** | 7 nhóm chức năng đã hoàn tất thực thi trên thiết bị thật |
| **Số Execution Items chờ thực thi (Pending)** | **44** | **32.84%** | 3 nhóm chức năng ở trạng thái DESIGN — CHỜ TEST |
| **PASS** | **87** | **96.67%** | Tính trên 90 items đã thực thi (khớp hoàn toàn mong đợi trên UI) |
| **FAIL** | **3** | **3.33%** | Tính trên 90 items đã thực thi (FN-02: 1, FN-04: 2) |
| **BLOCKED** | **0** | **0.00%** | Không có ca kiểm thử nào bị chặn môi trường |
| **ERROR** | **0** | **0.00%** | Không phát sinh lỗi bất thường của runner |
| **Số lượng Bug phát hiện** | **4** | - | 3 functional bugs (BUG-FN02-01, BUG-BB-002, BUG-BB-003) + 1 UI bug (BUG-BB-FN09-01) |
| **Số nhóm chức năng đã test** | **7** | **70.0%** | FN-02, FN-04, FN-05, FN-08, FN-09, FN-10/11/12, FN-20 |
| **Số nhóm chức năng chờ test** | **3** | **30.0%** | FN-23, FN-29/30, FN-40/41 |

---

## II. BẢNG TỔNG HỢP CHI TIẾT 10 NHÓM CHỨC NĂNG

| Nhóm FN | Tên nhóm chức năng | File Execution Sheet | Số TC | Số Exec | Executed | Pending | PASS | FAIL | BLOCKED | Bug ID | Trạng thái nhóm |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|:---:|
| **FN-02** | Đăng ký tài khoản Email/Password | `fn02_execution_sheet.md` | 13 | 19 | 19 | 0 | 18 | 1 | 0 | `BUG-FN02-01` | **ĐÃ TEST** |
| **FN-04** | Đăng nhập tài khoản Email/Password | `fn04_execution_sheet.md` | 15 | 16 | 16 | 0 | 14 | 2 | 0 | `BUG-BB-002`, `BUG-BB-003` | **ĐÃ TEST** |
| **FN-05** | Đăng nhập Google & Avatar Cloudinary | `fn05_execution_sheet.md` | 8 | 8 | 8 | 0 | 8 | 0 | 0 | Không | **ĐÃ TEST** |
| **FN-08** | Tạo ghi chú văn bản & Tự động lưu | `fn08_execution_sheet.md` | 8 | 8 | 8 | 0 | 8 | 0 | 0 | Không | **ĐÃ TEST** |
| **FN-09** | Soạn thảo văn bản định dạng Rich-text | `fn09_execution_sheet.md` | 11 | 12 | 12 | 0 | 12 | 0 | 0 | `BUG-BB-FN09-01` (UI) | **ĐÃ TEST** |
| **FN-10/11/12** | Thùng rác, Khôi phục, Xóa vĩnh viễn | `fn10_fn11_fn12_execution_sheet.md` | 10 | 12 | 12 | 0 | 12 | 0 | 0 | Không | **ĐÃ TEST** |
| **FN-20** | Ghim & Bỏ ghim ghi chú | `fn20_execution_sheet.md` | 14 | 15 | 15 | 0 | 15 | 0 | 0 | Không | **ĐÃ TEST** |
| **FN-23** | Tìm kiếm ghi chú & Bộ lọc | `fn23_execution_sheet.md` | 17 | 22 | 0 | 22 | 0 | 0 | 0 | Không | **DESIGN — CHỜ TEST** |
| **FN-29/30** | Khóa & Mở khóa sinh trắc học | `fn29_fn30_execution_sheet.md` | 12 | 12 | 0 | 12 | 0 | 0 | 0 | Không | **DESIGN — CHỜ TEST** |
| **FN-40/41** | Đồng bộ Offline & Xung đột LWW | `fn40_fn41_execution_sheet.md` | 10 | 10 | 0 | 10 | 0 | 0 | 0 | Không | **DESIGN — CHỜ TEST** |
| **TỔNG CỘNG** | **10 nhóm chức năng trọng tâm** | **10 execution sheets** | **118** | **134** | **90** | **44** | **87** | **3** | **0** | **4 Bugs** | **7 ĐÃ TEST / 3 CHỜ TEST** |

---

## III. DANH SÁCH LỖI (BUG REPORT)

| Bug ID | Chức năng | TC-ID & Data ID | Mô tả lỗi quan sát được trên UI | Phân loại / Mức độ | Trạng thái |
|---|---|---|---|---|---|
| **BUG-FN02-01** | FN-02 | TC-BB-003 D01 | Khi nhập email thiếu ký tự `@` (`nguoidung_gmail.com`), hệ thống không hiển thị thông báo lỗi trực tiếp dưới trường nhập mà chỉ tắt trạng thái nút bấm (disabled state), khác biệt so với hành vi báo lỗi trực tiếp của form. | Functional / Minor | Open (Chờ fix) |
| **BUG-BB-002** | FN-04 | TC-BB-008 D01 | Khi đăng nhập tài khoản chưa tồn tại (`ghost_user@gmail.com`), ứng dụng hiển thị thông báo gộp màu đỏ: *"Email hoặc mật khẩu không chính xác."* thay vì thông báo riêng biệt *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."* theo tài liệu đặc tả. | Functional / Minor | Open (Chờ fix) |
| **BUG-BB-003** | FN-04 | TC-BB-007 D01 | Khi đăng nhập sai mật khẩu, ứng dụng hiển thị thông báo gộp màu đỏ: *"Email hoặc mật khẩu không chính xác."* thay vì thông báo riêng biệt *"Mật khẩu không chính xác."* theo tài liệu đặc tả. | Functional / Minor | Open (Chờ fix) |
| **BUG-BB-FN09-01** | FN-09 | TC-BB-020B D01 | Thanh công cụ định dạng Rich-text bị che khuất một phần khi bàn phím ảo hiển thị ở chế độ xoay ngang màn hình (Landscape mode); chức năng soạn thảo vẫn hoạt động bình thường. | UI/UX / Trivial | Noted |

---

## IV. LƯU TRỮ BẰNG CHỨNG (EVIDENCE REPOSITORY)

Toàn bộ ảnh chụp màn hình bằng chứng thực tế cho 90 execution items đã thực thi được lưu trữ có cấu trúc trong thư mục `evidence/`:
- `evidence/fn02/`: 19 ảnh chụp cho 19 items FN-02
- `evidence/fn04/`: 17 ảnh chụp cho 16 items FN-04
- `evidence/fn05/`: 12 ảnh chụp cho 8 items FN-05
- `evidence/fn08/`: 9 ảnh chụp cho 8 items FN-08
- `evidence/fn09/`: 12 ảnh chụp cho 12 items FN-09
- `evidence/fn10_11_12/`: 3 ảnh chụp cho 12 items FN-10/11/12
- `evidence/fn20/`: 2 ảnh chụp cho 15 items FN-20
- *(Các nhóm FN-23, FN-29/30, FN-40/41 chưa thực thi, không tạo ảnh bằng chứng giả)*

---

## V. XÁC NHẬN TRẠNG THÁI DỰ ÁN

- **BLACK-BOX DESIGN & DOCUMENTATION = COMPLETE**
- **EXECUTION PHASE = NOT STARTED FOR FN-23 / FN-29/30 / FN-40/41**
