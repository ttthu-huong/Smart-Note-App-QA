# BÁO CÁO TỔNG KẾT THỰC THI KIỂM THỬ BLACK-BOX
## Dự án: Smart Note App
**Branch:** `huong`  
**Ngày thực thi:** 04/10/2026  
**Người thực hiện:** Artemis QA Runner & Thu Hường  
**Thiết bị kiểm thử:** 
- Thiết bị A: Samsung Galaxy S21 FE 5G (SM-G990E), Android 14 (API 34)
- Thiết bị B: Samsung Galaxy S26 FE (S26 FE của Thu Hường), Android 14
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  

---

## I. TỔNG QUAN KẾT QUẢ THỰC THI (TOÀN BỘ 10 NHÓM CHỨC NĂNG)

Toàn bộ 10 nhóm chức năng mục tiêu đã được thực thi độc lập, khách quan và hoàn tất 100% trên thiết bị thật:
- **FN-02**: Đăng ký & Quản lý tài khoản Email/Password (5 TC / 11 items - 10 PASS, 1 FAIL)
- **FN-04**: Đăng nhập tài khoản Email/Password (4 TC / 4 items - 1 PASS, 3 FAIL)
- **FN-05**: Đăng nhập bằng Google & Avatar Cloudinary (2 TC / 2 items - 2 PASS)
- **FN-08**: Tạo ghi chú văn bản cơ bản & Tự động lưu (3 TC / 3 items - 3 PASS)
- **FN-09**: Soạn thảo văn bản có định dạng Rich-text (2 TC / 2 items - 2 PASS)
- **FN-10 / FN-11 / FN-12**: Vòng đời ghi chú: Thùng rác, Khôi phục, Xóa vĩnh viễn (3 TC / 3 items - 3 PASS)
- **FN-20**: Ghim & Bỏ ghim ghi chú (2 TC / 2 items - 2 PASS)
- **FN-23**: Tìm kiếm ghi chú theo từ khóa (4 TC / 4 items - 4 PASS)
- **FN-29 / FN-30**: Khóa & Mở khóa sinh trắc học vân tay / khuôn mặt (4 TC / 4 items - 4 PASS)
- **FN-40 / FN-41**: Đồng bộ dữ liệu ngoại tuyến Offline/Online & Phân xử xung đột Last-Writer-Wins (2 TC / 2 items - 2 PASS)

### Bảng số liệu tổng hợp toàn diện

| Chỉ số đo lường | Số lượng | Ghi chú giải thích |
|---|---:|---|
| **Tổng số Test Cases chính thức** | **31** | Bao phủ 100% bộ đặc tả `black_box_test_cases.md` |
| **Tổng số Execution Items** | **37** | 37 items thực tế trong 10 file execution sheet |
| **PASS** | **33** | Đạt 100% mong đợi quan sát thực tế trên UI |
| **FAIL** | **4** | Gặp lỗi chức năng/crash thực tế |
| **BLOCKED** | **0** | Đã tháo gỡ toàn bộ, hoàn thành 100% trên thiết bị thật |
| **Số lượng Bug phát hiện** | **4** | Đã tạo Bug ID và mô tả chi tiết |
| **Tỷ lệ thực thi (Execution Rate)** | **100%** | `(33 PASS + 4 FAIL) / 37 items * 100%` |
| **Tỷ lệ đạt (Pass Rate)** | **89.19%** | `33 PASS / 37 items * 100%` |
| **Retest** | **0** | Chờ bản build sửa lỗi |

---

## II. BẢNG TỔNG HỢP THEO TỪNG NHÓM CHỨC NĂNG

| Nhóm FN | Tên nhóm chức năng | File Execution Sheet | Số TC | Số Items | PASS | FAIL | BLOCKED | Số Bug | Tỷ lệ PASS |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **FN-02** | Đăng ký tài khoản Email/Password | `fn02_execution_sheet.md` | 5 | 11 | 10 | 1 | 0 | 1 | 90.91% |
| **FN-04** | Đăng nhập tài khoản Email/Password | `fn04_execution_sheet.md` | 4 | 4 | 1 | 3 | 0 | 3 | 25.00% |
| **FN-05** | Đăng nhập Google & Avatar | `fn05_execution_sheet.md` | 2 | 2 | 2 | 0 | 0 | 0 | 100% |
| **FN-08** | Tạo ghi chú & Tự động lưu | `fn08_execution_sheet.md` | 3 | 3 | 3 | 0 | 0 | 0 | 100% |
| **FN-09** | Soạn thảo Rich-text | `fn09_execution_sheet.md` | 2 | 2 | 2 | 0 | 0 | 0 | 100% |
| **FN-10/11/12** | Thùng rác, Khôi phục, Xóa vĩnh viễn | `fn10_fn11_fn12_execution_sheet.md` | 3 | 3 | 3 | 0 | 0 | 0 | 100% |
| **FN-20** | Ghim & Bỏ ghim ghi chú | `fn20_execution_sheet.md` | 2 | 2 | 2 | 0 | 0 | 0 | 100% |
| **FN-23** | Tìm kiếm ghi chú theo từ khóa | `fn23_execution_sheet.md` | 4 | 4 | 4 | 0 | 0 | 0 | 100% |
| **FN-29/30** | Khóa & Mở khóa sinh trắc học | `fn29_fn30_execution_sheet.md` | 4 | 4 | 4 | 0 | 0 | 0 | 100% |
| **FN-40/41** | Đồng bộ Offline & Xung đột LWW | `fn40_fn41_execution_sheet.md` | 2 | 2 | 2 | 0 | 0 | 0 | 100% |
| **TỔNG CỘNG** | **10 nhóm chức năng** | **10 execution sheets** | **31** | **37** | **33** | **4** | **0** | **4** | **89.19%** |

---

## III. DANH SÁCH BUG PHÁT HIỆN

| Bug ID | Chức năng | TC-ID & Data ID | Mô tả lỗi | Severity |
|---|---|---|---|---|
| **BUG-FN02-01** | FN-02 | TC-BB-003 D01 | Khi nhập email thiếu ký tự `@` (`nguoidung_gmail.com`), hệ thống không hiển thị thông báo lỗi trực tiếp dưới trường nhập mà chỉ tắt trạng thái nút bấm. | Minor |
| **BUG-BB-002** | FN-04 | TC-BB-008 D01 | Khi đăng nhập tài khoản không tồn tại (`ghost_user@gmail.com`), ứng dụng gặp lỗi timeout hoặc không phản hồi kịp thời từ Firebase Auth. | Major |
| **BUG-BB-003** | FN-04 | TC-BB-007 D01 | Khi đăng nhập sai mật khẩu, ứng dụng hiển thị thông báo lỗi chung chung thay vì thông báo tiếng Việt cụ thể. | Minor |
| **BUG-BB-004** | FN-04 | TC-BB-006 D01 | Tài khoản `student_qa@gmail.com` khi đăng nhập bị chuyển hướng chậm hơn so với đăng nhập qua Google. | Minor |

---

## IV. LƯU TRỮ BẰNG CHỨNG (EVIDENCE)

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
- `evidence/fn40_fn41/`: 5 ảnh chụp cho 2 items FN-40/41 (`DevA`, `DevB`, `Result`)

---

## V. THÔNG TIN PHIÊN BẢN VÀ COMMIT

- **Branch:** `huong`
- **Commit Message:** `qa: complete black-box test execution 100% covering 31 test cases and 10 execution sheets`
