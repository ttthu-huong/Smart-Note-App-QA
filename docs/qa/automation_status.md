# TIẾN ĐỘ KIỂM THỬ TỰ ĐỘNG

**Dự án:** Smart Note App · **Nhánh:** `huong` · **Phiên bản:** 1.5 · **Ngày cập nhật:** 21/10/2026 (UTC+7)
**Mốc baseline lịch sử:** 19/10/2026 (`98abb5af577b2d38192e7a88e7ff94a2b5f77262`).
**Mốc mở rộng Phase 2:** 20/10/2026 (FN-08 đến FN-12, 32 execution items: 31 PASS, 1 BLOCKED).
**Mốc mở rộng Phase 3:** 20/10/2026 (FN-13 & FN-14: Lưu trữ & Bỏ lưu trữ, 5 execution items: 5 PASS, 0 BLOCKED).
**Mốc mở rộng Phase 4:** 20/10/2026 (FN-20: Ghim & Bỏ ghim ghi chú, 15 execution items: 15 PASS, 0 BLOCKED).
**Mốc mở rộng Phase 5:** 21/10/2026 (FN-23: Tìm kiếm & Bộ lọc đa phương tiện, 14 execution items mở rộng: 11 PASS, 1 FAIL / BUG-004 OPEN, 1 CHƯA ĐỦ CĂN CỨ / BR-01, 1 BLOCKED / BUG-001; tổng tự động hóa 18/22 items gồm cả 4 baseline).
**Repository:** `ttthu-huong/Smart-Note-App-QA`.

> **Phân định nguồn số liệu:** Giữ nguyên số liệu baseline lịch sử (23 UI / 24 Provider = 47 tests); bổ sung riêng biệt số liệu mở rộng Phase 2 (32 execution items: 31 PASS, 1 BLOCKED), Phase 3 (5 execution items: 5 PASS), Phase 4 (15 execution items: 15 PASS) và Phase 5 (14 execution items mở rộng: 11 PASS, 1 FAIL, 1 CHƯA ĐỦ CĂN CỨ, 1 BLOCKED). Tuyệt đối không cộng dồn các bộ số liệu để tránh đếm trùng các test case đã chạy ở nhiều mốc. Xem [báo cáo thực thi](automation_execution_summary.md) và [đặc tả chi tiết](automation_test_cases.md).


## 1. Trạng thái Baseline lịch sử (19/10/2026)

| Hạng mục | Đã xác minh | Còn lại/giới hạn |
| --- | --- | --- |
| UI/E2E baseline | 23/31 TC có XML: 19 PASS, 4 FAIL | 8 TC DEFERRED; 74.19% tập ứng viên có kết quả |
| Bản ghi thực thi UI | 24 testcase records trong 9 XML | TC-BB-022 có 2 bản ghi, tính 1 TC duy nhất |
| Provider | Có mã 24 tests (15 + 9) | Log lịch sử xác nhận 24 PASS; chưa xác minh chính xác commit thực thi |
| Tổng lịch sử hai tầng | 47 tests (23 UI + 24 Provider), 43 PASS/4 FAIL | 91.49% theo kết quả đã có minh chứng (9 XML UI + console log máy) |
| Script mở rộng/alias | Đã có kiểm kê mã nguồn | Chưa có XML tương ứng trong baseline; theo dõi riêng tại Phase 2 |

*Tỷ lệ xác minh baseline:* UI đạt 19/23 = 82.61% PASS; Provider đạt 24/24 = 100% PASS; Tổng hai tầng đạt 43/47 = 91.49% PASS.

---

## 2. Kết quả kiểm thử UI theo nhóm

### 2.1. Nhóm UI Baseline lịch sử (9 XML — 04/10 đến 14/10/2026)

| FN | Số TC duy nhất | PASS | FAIL | Ghi chú baseline |
| --- | ---: | ---: | ---: | --- |
| FN-02 | 5 | 4 | 1 | 1 FAIL (TC-BB-003: validation domain rác `BUG-FN02-01`) |
| FN-04 | 4 | 1 | 3 | 3 FAIL (006: tài khoản unverified; 007/008: thông báo gộp Firebase) |
| FN-08 | 3 | 3 | 0 | Baseline 3 TC (016, 017, 018) |
| FN-09 | 2 | 2 | 0 | Baseline 2 TC (019, 020) |
| FN-10 | 1 | 1 | 0 | Baseline 1 TC (021) |
| FN-11 | 1 | 1 | 0 | Baseline 1 TC (022, chạy 2 lần đều PASS) |
| FN-12 | 1 | 1 | 0 | Baseline 1 TC (023) |
| FN-20 | 2 | 2 | 0 | Baseline 2 TC (024, 025) |
| FN-23 | 4 | 4 | 0 | Baseline 4 TC (026, 027, 028, 029) |
| **Tổng** | **23** | **19** | **4** | **19 PASS / 4 FAIL trên 23 TC duy nhất** |

### 2.2. Nhóm UI Mở rộng Phase 2 (FN-08 đến FN-12 — 20/10/2026)

| FN | Chức năng | Execution items | PASS | BLOCKED | FAIL | Chi tiết kết quả & Ghi chú kỹ thuật |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| **FN-08** | Tạo ghi chú mới | 8 | 8 | 0 | 0 | **100% PASS** (3 baseline + 5 mở rộng: 018B, 018C, 018D, 018E, 018F; 018E dùng SQLite oracle xác minh emoji 🚀) |
| **FN-09** | Chỉnh sửa & Tự động lưu (Autosave) | 12 | 12 | 0 | 0 | **100% PASS** (11 TC, 12 items do 019G có D01/D02; **BUG-005 vẫn OPEN** trong Defect Log) |
| **FN-10** | Chuyển ghi chú vào Thùng rác | 5 | 5 | 0 | 0 | **100% PASS** (021 D01 baseline; 021B D01 có 4 ảnh evidence; 021C D01/D02, 021D D01 có JUnit XML) |
| **FN-11** | Khôi phục ghi chú từ Thùng rác | 3 | 2 | 1 | 0 | **2 PASS, 1 BLOCKED** (022 D01 baseline PASS; 022B D01 PASS; **TC-BB-022C D01 BLOCKED** do Thùng rác có 23 ghi chú) |
| **FN-12** | Xóa vĩnh viễn ghi chú khỏi Thùng rác | 4 | 4 | 0 | 0 | **100% PASS** (023 D01 baseline; 023B D01/D02, 023C D01 có JUnit XML; 023C kiểm tra bền vững lifecycle) |
| **TỔNG** | **Phase 2 (FN-08 đến FN-12)** | **32** | **31** | **1** | **0** | **31 PASS / 1 BLOCKED / 0 FAIL (Tỷ lệ PASS: 96.88%)** |

### 2.3. Nhóm UI Mở rộng Phase 3 (FN-13 và FN-14: Lưu trữ & Bỏ lưu trữ — 20/10/2026)

| FN | Chức năng | Execution items | PASS | BLOCKED | FAIL | Chi tiết kết quả & Ghi chú kỹ thuật |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| **FN-13** | Lưu trữ ghi chú (Archive Note) | 3 | 3 | 0 | 0 | **100% PASS** (TC-BB-040 D01 lưu trữ từ Home; EXT-008 D01 cô lập Target vs Control; EXT-006 D01 bền vững Unicode sau restart) |
| **FN-14** | Bỏ lưu trữ ghi chú (Unarchive Note) | 2 | 2 | 0 | 0 | **100% PASS** (TC-BB-040B D01 bỏ lưu trữ qua BottomSheet; EXT-007 D01 vòng lặp trạng thái không duplicate sau restart) |
| **TỔNG** | **Phase 3 (FN-13 và FN-14)** | **5** | **5** | **0** | **0** | **5 PASS / 0 BLOCKED / 0 FAIL (Tỷ lệ PASS: 100%)** |

### 2.4. Nhóm UI Mở rộng Phase 4 (FN-20: Ghim & Bỏ ghim ghi chú — 20/10/2026)

| FN | Chức năng | Execution items | PASS | BLOCKED | FAIL | Chi tiết kết quả & Ghi chú kỹ thuật |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| **FN-20** | Ghim và Bỏ ghim ghi chú (Pin/Unpin Note) | 15 | 15 | 0 | 0 | **100% PASS** (2 baseline: 024, 025; 13 mở rộng: 024B D01/D02, 024C D01, 024D D01, 024H D01, 025D D01, 025E D01, 024E D01, 024F D01, 024G D01, 025B D01, 025C D01, 025F D01; 024G dùng tài khoản QA cô lập an toàn) |
| **TỔNG** | **Phase 4 (FN-20)** | **15** | **15** | **0** | **0** | **15 PASS / 0 BLOCKED / 0 FAIL (Tỷ lệ PASS: 100%)** |

### 2.5. Nhóm UI Mở rộng Phase 5 (FN-23: Tìm kiếm & Bộ lọc đa phương tiện — 21/10/2026)

| FN | Chức năng | Execution items | PASS | BLOCKED | FAIL / BR-01 | Chi tiết kết quả & Ghi chú kỹ thuật |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| **FN-23** | Tìm kiếm & Bộ lọc đa phương tiện (Search & Filter) | 18 | 15 | 1 | 2 | **15 PASS / 1 BLOCKED / 1 FAIL / 1 BR-01** (4 baseline: 026, 027, 028, 029; 14 mở rộng qua `test_fn23_extended.py`: Batch 1 có 5 PASS [026B D01/D02, 026C, 026E, 028D]; Batch 2 có 6 PASS [027D D01/D02, 027F, 028B, 027B D03 URL, 028C]; Batch 3 có 1 BR-01 CHƯA ĐỦ CĂN CỨ [026B D03 không dấu], 1 FAIL [027G D01 BUG-004 OPEN tái hiện raw LIKE], 1 BLOCKED [027E D01 do BUG-001]; 4 ca còn lại giữ nguyên Manual lịch sử: 026D, 027B D01/D02, 027C) |
| **TỔNG** | **Phase 5 (FN-23)** | **18** | **15** | **1** | **2** | **15 PASS / 1 BLOCKED / 1 FAIL (`BUG-004`) / 1 CHƯA ĐỦ CĂN CỨ (`BR-01`)** |

---

## 3. Danh mục công việc & Vấn đề tồn đọng

| Ưu tiên | Hạng mục công việc / Khiếm khuyết | Trạng thái hiện tại | Kế hoạch xử lý tiếp theo |
| :---: | --- | --- | --- |
| **1** | **Khiếm khuyết BUG-004 (FN-23)** | **OPEN (Đã tái hiện automation)** | Bộ lọc `has:list` không bóc tách token trong `local_note_service.dart`, gây lỗi query LIKE thô; giữ OPEN trong Defect Log. |
| **2** | **Tìm kiếm tiếng Việt không dấu TC-BB-026B D03 (FN-23)** | **CHƯA ĐỦ CĂN CỨ (BR-01)** | SQLite engine không hỗ trợ unaccent folding, trả về Empty State an toàn (0 crash); giữ nguyên theo quyết định `BR-01`, không tự ép PASS. |
| **3** | **Tiền điều kiện TC-BB-027E D01 (FN-23)** | **BLOCKED (do BUG-001)** | Bị chặn bởi lỗi upload ảnh trong Editor bị treo vĩnh viễn (`BUG-001`); giữ nguyên định danh kịch bản gốc, không tự ý thay thế fixture sang Pinned. |
| **4** | **Tiền điều kiện TC-BB-022C D01 (FN-11)** | **BLOCKED (pytest: SKIPPED)** | Thùng rác trên thiết bị đang có 23 ghi chú. Cần môi trường Thùng rác rỗng mà không xóa nhầm dữ liệu người dùng để retest Empty State. |
| **5** | **Bổ sung JUnit XML cho TC-BB-021B D01 (FN-10)** | **ĐÃ PASS (có 4 ảnh evidence)** | Đã chạy thành công trên máy thật, xác minh hoàn tác khôi phục Home; cần xuất file JUnit XML độc lập trong phiên rerun. |
| **6** | **Khiếm khuyết giao diện BUG-005 (FN-09)** | **OPEN** | RenderFlex overflow thoáng qua khi co giãn bàn phím; test automation PASS chức năng không tự đóng bug này; giữ OPEN trong Defect Log. |
| **7** | **Đối chiếu retest TC-BB-006 (FN-04)** | Chờ XML retest độc lập | Phase 4 báo cáo PASS sau khi chuẩn bị tài khoản verified; giữ FAIL baseline lịch sử cho tới khi có file XML retest độc lập. |
| **8** | **Xác nhận Expected thông báo TC-BB-007/008 (FN-04)** | Chờ xác nhận yêu cầu | Giữ FAIL lịch sử (thông báo gộp của Firebase); phân biệt `BUG-BB-002/003` khác với `BUG-002/003` (LWW/Pull-to-refresh). |
| **9** | **Retest TC-BB-003 (FN-02)** | Chờ bản build sửa | Giữ FAIL lịch sử (lỗi thứ tự validation email format vs disposable domain `BUG-FN02-01`). |
| **10** | **8 ca UI tạm hoãn (DEFERRED)** | DEFERRED | TC-BB-010, 011 (Google OAuth), 012..015 (Biometric), 030, 031 (Sync); chờ môi trường phù hợp. |

---

## 4. Phạm vi chức năng (FN Coverage)

- **11 FN có kiểm thử UI/E2E:** FN-02, FN-04, FN-08, FN-09, FN-10, FN-11, FN-12, FN-13, FN-14, FN-20, FN-23. Trong đó:
  - 5 nhóm FN-08 đến FN-12 đã hoàn thành mở rộng toàn diện trong Phase 2 (31 PASS / 1 BLOCKED trên 32 items).
  - 2 nhóm FN-13 và FN-14 đã hoàn thành mở rộng toàn diện trong Phase 3 (5 PASS / 0 BLOCKED trên 5 items).
  - Nhóm FN-20 đã hoàn thành mở rộng toàn diện trong Phase 4 (15 PASS / 0 BLOCKED trên 15 items: 2 baseline + 13 mở rộng).
  - Nhóm FN-23 đã hoàn thành mở rộng toàn diện trong Phase 5 (18 items tự động hóa: 15 PASS, 1 FAIL/`BUG-004`, 1 CHƯA ĐỦ CĂN CỨ/`BR-01`, 1 BLOCKED/`BUG-001` và 4 Manual lịch sử).
- **10 FN có kiểm thử Provider:** FN-08, FN-09, FN-10, FN-11, FN-12, FN-13, FN-14, FN-20, FN-23, FN-40 (đã đối chiếu log máy `automated_test_run.log` gồm 24 PASS).
- **Tổng cộng 12 FN có mã kiểm thử tự động hai tầng** (11 FN có cả UI + Provider; riêng FN-40 ở tầng Provider).
- **Đã hoàn thành toàn bộ 5 Phase Automation** theo kế hoạch kiểm thử tự động của dự án.

---

## 5. Tài liệu tra cứu liên quan

- [Báo cáo thực thi kiểm thử tự động (Execution Summary)](automation_execution_summary.md)
- [Đặc tả kịch bản kiểm thử tự động (Automation Test Cases)](automation_test_cases.md)
- [Ma trận truy vết yêu cầu (Requirements Traceability Matrix)](../plan_and_requirements/requirements_traceability_matrix.md)
- [Bảng thực thi chức năng Tìm kiếm FN-23 (Execution Sheet)](../test_cases/execution_sheets/fn23_execution_sheet.md)
- [Kiểm kê Script và Node ID](automation_script_inventory.md)
- [Ma trận mở rộng và nguồn số liệu](automation_expanded_scope.md)
- [Kế hoạch kiểm thử tự động](automation_plan.md)
