# MA TRẬN TRUY VẾT YÊU CẦU KIỂM THỬ (REQUIREMENTS TRACEABILITY MATRIX - RTM)
## Dự án: Smart Note App
**Mục tiêu:** Ánh xạ hai chiều giữa Yêu cầu Nghiệp vụ / Yêu cầu Kỹ thuật (Requirements) với các Kịch bản kiểm thử Hộp đen, Hộp trắng, Tự động hóa và Phi chức năng  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Traceability Management

---

## 1. BẢNG MA TRẬN TRUY VẾT YÊU CẦU CHI TIẾT (REQUIREMENTS TRACEABILITY MATRIX)

| Mã Yêu cầu (REQ-ID) | Mô tả Yêu cầu hệ thống / Nghiệp vụ | Mã Test Case ánh xạ (Test Case IDs) | Loại kiểm thử (Test Type) | Trạng thái Thiết kế | Trạng thái Thực thi | Evidence / Bằng chứng xác minh |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **REQ-01** | **Đăng ký tài khoản mới** (Xác thực email, kiểm tra định dạng email, mật khẩu >= 6 ký tự, xử lý trùng email, gửi email xác minh) | `TC-BB-001`, `TC-BB-001B`, `TC-BB-002`, `TC-BB-002B`, `TC-BB-002C`, `TC-BB-003`, `TC-BB-003B`, `TC-BB-004`, `TC-BB-004B` | Black-box / Manual & Automation | `DESIGNED` | **PASS** | `evidence/fn02/FN02_TC-BB-001_D01_01.png` .. `FN02_TC-BB-004B_D01_01.png` |
| **REQ-02** | **Đăng nhập hệ thống** (Đăng nhập Email/Mật khẩu, Đăng nhập Google, trim khoảng trắng, không phân biệt chữ hoa/thường email, chuyển hướng tài khoản chưa verify) | `TC-BB-006`, `TC-BB-006B`, `TC-BB-006C`, `TC-BB-007`, `TC-BB-009`, `TC-WB-001` .. `TC-WB-005` | Black-box / White-box / Automation | `DESIGNED` | **PASS** | `evidence/fn04/FN04_TC-BB-006B_D01_01.png` .. `FN04_TC-BB-009_D01_01.png` |
| **REQ-03** | **Quên & Đặt lại mật khẩu** (Gửi email khôi phục mật khẩu, kiểm tra định dạng email khôi phục) | `TC-BB-011`, `TC-BB-011B`, `TC-BB-011C` | Black-box / Manual | `DESIGNED` | **PASS** | `evidence/fn05/FN05_TC-BB-011_D01_01.png`, `FN05_TC-BB-011_D01_02.png` |
| **REQ-04** | **Tạo ghi chú mới** (Tạo ghi chú văn bản, checklist to-do, tự động lưu, đính kèm media) | `TC-BB-018`, `TC-BB-018B`, `TC-BB-018C`, `TC-BB-018D`, `test_fn08_create_note.py` | Black-box / Automation | `DESIGNED` | **PASS** | `evidence/fn08/FN08_TC-BB-018_D01_01.png` |
| **REQ-05** | **Chỉnh sửa & Cập nhật ghi chú** (Chỉnh sửa tiêu đề/nội dung, tự động lưu thời gian thực, lưu lịch sử sửa đổi) | `TC-BB-019`, `TC-BB-019B`, `TC-BB-019C`, `test_fn09_edit_note.py` | Black-box / Automation | `DESIGNED` | **PASS** | `evidence/fn09/FN09_TC-BB-019_D01_01.png` |
| **REQ-06** | **Ghim ghi chú (Pin Note)** (Ghim/bỏ ghim ghi chú, sắp xếp nhóm ghi chú được ghim lên đầu Trang chủ) | `TC-BB-024`, `TC-BB-024B`, `test_fn20_pin_note.py` | Black-box / Automation | `DESIGNED` | **PASS** | `evidence/fn20/FN20_TC-BB-024_D01_01.png` |
| **REQ-07** | **Tìm kiếm & Bộ lọc ghi chú (Search & Filter)** (Tìm theo từ khóa tiêu đề/nội dung, không phân biệt hoa thường, tiếng Việt có dấu, lọc theo Chip Hình ảnh/Âm thanh/URL/Nhãn/Trạng thái, highlight từ khóa, xóa nhanh từ khóa) | `TC-BB-026` đến `TC-BB-029` (tổng 17 TCs / 22 Exec Items), `run_fn23_execution.py`, `TC-NF-001` | Black-box / Automation / Non-functional | `DESIGNED` | **XÁC MINH 12/22 PASS, 1/22 FAIL/BLOCKED, 9/22 NOT RUN** | 13 ảnh screenshots trong `evidence/fn23/FN23_TC-BB-026_D01.png` .. `FN23_TC-BB-028_D01_01.png` |
| **REQ-08** | **Lưu trữ & Thùng rác (Archive & Trash)** (Đưa note vào Lưu trữ, chuyển note vào Thùng rác, khôi phục note, xóa vĩnh viễn note, loại trừ note trong Thùng rác khỏi kết quả tìm kiếm) | `TC-BB-015`, `TC-BB-015B`, `TC-BB-015C`, `TC-BB-028B`, `TC-WB-006` .. `TC-WB-010` | Black-box / White-box | `DESIGNED` | **PASS** | `evidence/fn29_30/FN29_30_TC-BB-015_D01_01.png` .. `FN29_30_TC-BB-015C_D01_02.png` |
| **REQ-09** | **Bảo mật & Cô lập dữ liệu (Security & Privacy)** (Quy tắc cô lập dữ liệu Cloud Firestore theo User ID, khóa sinh trắc học, ngăn chặn rò rỉ token) | `TC-WB-011` đến `TC-WB-014`, `TC-NF-005`, `TC-NF-006`, `security_rules_test.dart` | White-box / Non-functional / Unit Auto | `DESIGNED` | **PASS** | Kết quả thực thi `test/security_rules_test.dart` (Pass 8/8 test cases) |
| **REQ-10** | **Khả năng chịu lỗi & Ngoại tuyến (Reliability & Offline-First)** | `TC-NF-003`, `TC-NF-004`, `TC-NF-007`, `TC-NF-008` | Non-functional | `DESIGNED` | **CHƯA THỰC THI CHÍNH THỨC** (Đã phát hiện Bug Upload timeout) | Nhật ký lỗi `docs/bugs/defect_log.md` (BUG-001 Cloudinary upload hang) |

---

## 2. THỐNG KÊ MỨC ĐỘ TRUY VẾT YÊU CẦU (REQUIREMENTS COVERAGE METRICS)

* **Tổng số Yêu cầu hệ thống (Total System Requirements)**: 10 Yêu cầu trọng tâm (REQ-01 đến REQ-10).
* **Tỷ lệ Yêu cầu đã được bao phủ bởi Test Cases (Test Design Coverage)**: **100%** (10/10 REQ đều có ít nhất 2 Test Cases ánh xạ).
* **Trạng thái thực thi thực tế (Execution Status Summary)**:
  - REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-08, REQ-09: **Đã thực thi & PASS có minh chứng**.
  - REQ-07 (FN-23 Search): **Đã thực thi 13/22 Exec Items (12 PASS, 1 FAIL/BLOCKED)**.
  - REQ-10 (Non-functional Reliability): **Đã thiết kế, phát hiện 1 Defect (BUG-001), chưa chạy hết toàn bộ kịch bản đo lường**.
