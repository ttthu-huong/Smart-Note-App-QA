# DÀN Ý SLIDE BÁO CÁO KIỂM TRA TIẾN ĐỘ (PROGRESS CHECK SLIDES OUTLINE)
## Ngày kiểm tra tiến độ: 14/10/2026
**Dự án:** Smart Note App QA & Automation Testing  
**Môn học:** Kiểm thử Phần mềm  
**Hạn nộp báo cáo chính thức:** 21/10/2026

---

## SLIDE 1: TRANG TIÊU ĐỀ (TITLE SLIDE)
* **Tiêu đề chính:** BÁO CÁO TIẾN ĐỘ KIỂM THỬ VÀ ĐÁNH GIÁ CHẤT LƯỢNG ỨNG DỤNG SMART NOTE APP
* **Chủ đề nhóm:** Kiểm thử Chức năng & Phi chức năng cho Ứng dụng Di động Offline-First (Android / Flutter)
* **Thành viên thực hiện:** Nhóm QA Smart Note App
* **Ngày trình bày:** 14/10/2026

---

## SLIDE 2: TỔNG QUAN ỨNG DỤNG VÀ KIẾN TRÚC HỆ THỐNG
* **Ứng dụng kiểm thử:** Smart Note App (Ứng dụng ghi chú di động đa phương tiện).
* **Kiến trúc kĩ thuật:**
  - Frontend Mobile: Flutter (Dart)
  - CSDL Cục bộ (Offline-First): SQLite (`sqflite`)
  - CSDL Đám mây & Xác thực: Firebase Cloud Firestore & Firebase Auth
  - Dịch vụ Lưu trữ Media: Cloudinary (Ảnh, Ghi âm, Bản vẽ)
* **Đặc thù thách thức QA:** Đảm bảo độ tin cậy đồng bộ Offline-to-Online, giải quyết xung đột dữ liệu (Last-Writer-Wins) và bảo mật dữ liệu cá nhân.

---

## SLIDE 3: PHẠM VI VÀ CHIẾN LƯỢC KIỂM THỬ (TESTING STRATEGY & SCOPE)
* **10 Nhóm Chức năng Trọng tâm:** Đăng ký (FN-02), Đăng nhập (FN-04), Khôi phục mật khẩu (FN-05), Tạo ghi chú (FN-08), Chỉnh sửa (FN-09), Ghim note (FN-20), Tìm kiếm & Bộ lọc (FN-23), Lưu trữ & Thùng rác (FN-29/30)...
* **Hệ thống Kiểm thử Đa tầng:**
  1. **Unit & Widget Test (Dart):** AuthProvider, Models, EmptyStateWidget.
  2. **Security Rules Test (Dart/Firestore):** Cô lập dữ liệu chéo giữa các User.
  3. **UI Automation Testing (Python / UIAutomator2 + Pytest):** Chạy trực tiếp trên thiết bị Android thật (Samsung Galaxy S21 FE 5G).
  4. **Manual & Non-functional Testing:** Kiểm thử phi chức năng, độ bền nhập liệu và chịu lỗi mạng.

---

## SLIDE 4: KẾT QUẢ ĐÃ ĐẠT ĐƯỢC VÀ BẰNG CHỨNG XÁC MINH (ACHIEVEMENTS & EVIDENCE)
* **Thiết kế Test Cases Hộp đen:** 118 Test Cases (134 Execution Items) hoàn chỉnh trong `black_box_test_cases.md`.
* **Kết quả Thực thi Thực tế có Minh chứng Ảnh thật:**
  - FN-02, FN-04, FN-05, FN-08, FN-09, FN-20, FN-29/30: **PASS 100%** (Đã lưu 24 ảnh minh chứng trong `evidence/`).
  - FN-23 (Tìm kiếm & Bộ lọc): **Đã thực thi 13/22 items** (12 PASS, 1 FAIL/BLOCKED). Lưu 13 ảnh minh chứng trong `evidence/fn23/`.
* **Thiết kế Hộp trắng & Security Rules:** Đã thiết kế ma trận Hộp trắng (`white_box_test_cases.md`) và chạy PASS 8/8 Security Rules tests.

---

## SLIDE 5: PHÂN TÍCH NGUYÊN NHÂN LỖI PHÁT HIỆN (DEFECT ANALYSIS & RCA)
* **Phát hiện lỗi trọng yếu `BUG-001`**: Tiến trình upload ảnh Cloudinary bị treo vô hạn trên màn hình Editor.
* **Hình ảnh & Telemetry:** Đã trích xuất file logcat `upload_realtime_logcat.txt` và chụp vết màn hình treo.
* **Nguyên nhân gốc (Root Cause):**
  - Hàm `uploadImage()` trong `cloudinary_service.dart` thiếu cơ chế `.timeout(30s)` cho HTTP Multipart Stream.
  - Màn hình `editor_screen.dart` thiếu khối `finally` để reset trạng thái `isUploading`.
* **Giải pháp đề xuất:** Bổ sung HTTP Timeout 30s và cơ chế bắt ngoại lệ TimeoutException.

---

## SLIDE 6: KẾ HOẠCH NGHỆM THU VÀ HOÀN THIỆN ĐẾN NGÀY 21/10
* **Từ 14/10 đến 17/10 (Phase 3 - Bổ sung & Sửa lỗi)**:
  - Áp dụng code fix cho `BUG-001` (Cloudinary Timeout).
  - Tiếp tục thực thi 9 Execution Items còn lại của FN-23.
  - Đo chỉ số độ bao phủ kiểm thử (`flutter test --coverage`).
* **Từ 18/10 đến 20/10 (Phase 4 - Hoàn thiện Báo cáo)**:
  - Tổng hợp đầy đủ Báo cáo 5 chương (50–80 trang) vào `Full_Testing_Report.md`.
  - Hoàn thiện file Slide thuyết trình chính thức (`.pptx`).
* **Ngày 21/10**: Đóng gói Repository QA và nộp bài tập lớn chính thức.
