# KẾ HOẠCH TINH GỌN TOÀN BỘ TÀI LIỆU MARKDOWN (.md) (BẢN CẬP NHẬT ĐÃ HIỆU CHỈNH)
## Dự án: Smart-Note-App-QA | Nhánh: huong
**Ngày lập & cập nhật:** 12/10/2026  
**Mục tiêu:** Chuẩn hóa, tinh gọn và thiết lập cấu trúc tài liệu kiểm thử phần mềm chuyên nghiệp, rõ ràng, có tính truy vết cao (Traceability) để phục vụ nộp và bảo vệ đồ án tốt nghiệp.  
**Nguyên tắc cốt lõi:**
1. Một nguồn chân lý duy nhất (Single Source of Truth), bảo toàn 100% bằng chứng và số liệu kiểm thử.
2. Giữ nguyên hồ sơ White-box đã đóng băng (**Documentation Frozen**).
3. Bảo toàn nguyên vẹn lịch sử kế hoạch và các bảng theo dõi đặc thù (không gộp cưỡng ép).
4. Giữ nguyên vị trí và đường dẫn của các Execution Sheets đang được liên kết để tránh đứt gãy script/tài liệu.

---

## 1. TỔNG QUAN VÀ ĐỐI SOÁT SỐ LIỆU FILE MARKDOWN

* **Tổng số file `.md` hiện có trên repository (không tính `docs_cleanup_plan.md`):** **60 file**
* **File kế hoạch đang soạn thảo:** `docs_cleanup_plan.md` (1 file) $\rightarrow$ Tổng trên ổ đĩa: **61 file**.
* **Đối soát số liệu phân loại sau hiệu chỉnh (Tính trên 60 file tài liệu chính):**
  - **KEEP (Giữ nguyên vẹn):** **54 file**
  - **MERGE (Hợp nhất nội dung, sau đó xóa file nguồn):** **1 file** (`supplementary_test_cases.md`)
  - **DELETE (Xóa file trùng lặp cũ / placeholder rỗng):** **5 file**
  - **Cân bằng toán học:** $54 \text{ (KEEP)} + 1 \text{ (MERGE)} + 5 \text{ (DELETE)} = \mathbf{60 \text{ file}}$
* **Số lượng file dự kiến sau khi thực hiện cleanup:**
  - **54 file** tài liệu chính thức (giảm 6 file dư thừa và trùng lặp).
  - *(Nếu tính cả file lưu trữ `docs_cleanup_plan.md`: tổng cộng là **55 file**).*

---

## 2. BẢNG PHÂN LOẠI CHI TIẾT 60 TÀI LIỆU MARKDOWN CỦA REPOSITORY

| STT | Đường dẫn file (.md) | Nhóm chức năng | Quy mô | Phân loại | Lý do kỹ thuật & Vai trò trong bộ hồ sơ Đồ án |
|:---:|:---|:---|:---:|:---:|:---|
| 1 | `README.md` | Hướng dẫn chung | 126 lines | **KEEP** | Giới thiệu dự án, kiến trúc tổng thể và hướng dẫn chạy kiểm thử chung. |
| 2 | `docs/Architecture_and_Flows.md` | Requirements / SRS | 654 lines | **KEEP** | Sơ đồ kiến trúc, luồng dữ liệu (Data Flows), State Machines và Firestore Rules. |
| 3 | `docs/giao-dien.md` | Requirements / SRS | 619 lines | **KEEP** | Quy chuẩn thiết kế UI/UX Material Design 3 (dẫn chiếu tại `srs_condensed.md#L141`). |
| 4 | `docs/plan_and_requirements/srs_condensed.md` | Requirements / SRS | 174 lines | **KEEP** | **Nguồn chân lý SRS**: Đặc tả 13 REQs, 3 Business Rules, 5 Non-functional Requirements. |
| 5 | `docs/plan_and_requirements/test_case_design_inventory_44_fn.md` | Requirements / SRS | 364 lines | **KEEP** | Bảng kiểm kê độ bao phủ toàn diện 44 chức năng từ giai đoạn thiết kế kiểm thử. |
| 6 | `docs/plan_and_requirements/test_plan.md` | Test Plan | 358 lines | **KEEP** | **Master Test Plan** chính thức của đồ án theo chuẩn IEEE 829. |
| 7 | `docs/plan_and_requirements/white_box_test_plan.md` | Test Plan (Frozen) | 155 lines | **KEEP** | Kế hoạch kiểm thử hộp trắng chọn lọc (Hồ sơ White-box đóng băng). |
| 8 | `docs/qa/automation_plan.md` | Test Plan (Automation) | 78 lines | **KEEP** | **Giữ riêng kế hoạch 4 Phase Automation**: Bảo toàn lộ trình triển khai và lịch sử kế hoạch, tránh làm phình to Master Test Plan. |
| 9 | `test_cases/black_box/black_box_test_cases.md` | Black-box Design | 336 lines | **KEEP** | **Master Spec Hộp đen**: Chứa 31 Test Case cốt lõi (sẽ nhận thêm 18 ca bổ sung). |
| 10 | `test_cases/black_box/supplementary_test_cases.md` | Black-box Design | 28 lines | **MERGE** | Kịch bản hộp đen bổ sung (18 TCs); hợp nhất vào cuối `black_box_test_cases.md`. |
| 11 | `test_cases/black_box/fn02_execution_sheet.md` | Black-box Exec | 242 lines | **KEEP** | Bảng theo dõi thực thi FN-02 (Đăng ký tài khoản). |
| 12 | `test_cases/black_box/fn04_execution_sheet.md` | Black-box Exec | 435 lines | **KEEP** | Bảng theo dõi thực thi FN-04 (Đăng nhập tài khoản). |
| 13 | `test_cases/black_box/fn05_execution_sheet.md` | Black-box Exec | 103 lines | **KEEP** | Bảng theo dõi thực thi FN-05 (Google OAuth). |
| 14 | `test_cases/black_box/fn08_execution_sheet.md` | Black-box Exec | 108 lines | **KEEP** | Bảng theo dõi thực thi FN-08 (Tạo ghi chú văn bản). |
| 15 | `test_cases/black_box/fn09_execution_sheet.md` | Black-box Exec | 117 lines | **KEEP** | Bảng theo dõi thực thi FN-09 (Chỉnh sửa ghi chú & Auto-save). |
| 16 | `test_cases/black_box/fn10_fn11_fn12_execution_sheet.md` | Black-box Exec | 128 lines | **KEEP** | Bảng theo dõi thực thi FN-10/11/12 (Xóa ghi chú & Thùng rác). |
| 17 | `test_cases/black_box/fn15_fn19_checklist_execution_sheet.md` | Black-box Exec | 62 lines | **KEEP** | Bảng theo dõi thực thi FN-15..19 (Checklist to-do). |
| 18 | `test_cases/black_box/fn20_execution_sheet.md` | Black-box Exec | 134 lines | **KEEP** | Bảng theo dõi thực thi FN-20 (Ghim ghi chú). |
| 19 | `test_cases/black_box/fn29_fn30_execution_sheet.md` | Black-box Exec | 99 lines | **KEEP** | Bảng theo dõi thực thi FN-29/30 (Khóa ghi chú & Sinh trắc học). |
| 20 | `test_cases/black_box/fn40_fn41_execution_sheet.md` | Black-box Exec | 91 lines | **KEEP** | Bảng theo dõi thực thi FN-40/41 (Đồng bộ đa thiết bị & Xung đột LWW). |
| 21 | `test_cases/execution_sheets/fn23_execution_sheet.md` | Black-box Exec | 119 lines | **KEEP** | **Giữ nguyên vị trí**: Bảng thực thi 22 items của FN-23, bảo đảm toàn vẹn đường dẫn liên kết. |
| 22 | `docs/qa/black_box_execution_summary.md` | Black-box Exec | 154 lines | **KEEP** | Báo cáo chốt kết quả thực thi kiểm thử hộp đen toàn diện theo 10 nhóm. |
| 23 | `test_cases/white_box/white_box_test_cases.md` | White-box (Frozen) | 572 lines | **KEEP** | Đặc tả thiết kế 22 White-box TCs. **BẢO TOÀN TUYỆT ĐỐI**. |
| 24 | `evidence/white_box/run_wb_enhanced_search_trash_20261011_2300/search_trash_enhanced_report.md` | White-box (Frozen) | 66 lines | **KEEP** | Báo cáo tăng cường Search & Trash. **BẢO TOÀN TUYỆT ĐỐI**. |
| 25 | `evidence/white_box/run_wb_final_closure_20261011_2330/white_box_closure_summary.md` | White-box (Frozen) | 69 lines | **KEEP** | Báo cáo nghiệm thu 94 ca White-box unit tests. **BẢO TOÀN TUYỆT ĐỐI**. |
| 26 | `evidence/white_box/run_wb_modular_refactor_20261011_1910/file_manifest.md` | White-box (Frozen) | 115 lines | **KEEP** | Bảng kê khai module test White-box tái cấu trúc. **BẢO TOÀN TUYỆT ĐỐI**. |
| 27 | `evidence/white_box/run_wb_search_20261011_2138/search_test_report.md` | White-box (Frozen) | 73 lines | **KEEP** | Báo cáo kiểm thử Search Service. **BẢO TOÀN TUYỆT ĐỐI**. |
| 28 | `evidence/white_box/run_wb_trash_lifecycle_20261011_2155/trash_lifecycle_test_report.md` | White-box (Frozen) | 76 lines | **KEEP** | Báo cáo vòng đời Thùng rác. **BẢO TOÀN TUYỆT ĐỐI**. |
| 29 | `test_cases/white_box/README.md` | White-box (Frozen) | 3 lines | **KEEP** | Chỉ mục thư mục White-box. **BẢO TOÀN TUYỆT ĐỐI**. |
| 30 | `automation/README.md` | Automation Guide | 53 lines | **KEEP** | Hướng dẫn cấu hình môi trường, thiết bị và thực thi test runner tự động. |
| 31 | `automation/reports/fn02_automation_report.md` | Automation Report | 91 lines | **KEEP** | Báo cáo thực thi tự động chi tiết FN-02 (20 tests). |
| 32 | `automation/reports/fn04_automation_report.md` | Automation Report | 40 lines | **KEEP** | Báo cáo thực thi tự động chi tiết FN-04 (11 tests). |
| 33 | `automation/reports/fn08_automation_report.md` | Automation Report | 45 lines | **KEEP** | Báo cáo thực thi tự động chi tiết FN-08 (3 tests). |
| 34 | `automation/reports/fn09_automation_report.md` | Automation Report | 56 lines | **KEEP** | Báo cáo thực thi tự động chi tiết FN-09 (2 tests). |
| 35 | `automation/reports/fn20_automation_report.md` | Automation Report | 66 lines | **KEEP** | Báo cáo thực thi tự động chi tiết FN-20 (2 tests). |
| 36 | `automation/reports/fn23_automation_report.md` | Automation Report | 75 lines | **KEEP** | Báo cáo thực thi tự động chi tiết FN-23 (4 tests). |
| 37 | `docs/qa/phase_4_automation_execution_report.md` | Automation Report | 345 lines | **KEEP** | **Báo cáo tổng hợp Automation Phase 4**: Bảng tổng kết 45 tests, hình ảnh evidence. |
| 38 | `docs/qa/phase_3c_automation_test_selection.md` | Automation Report | 255 lines | **KEEP** | Tài liệu phương pháp luận: Phân tích kỹ thuật và tiêu chí lựa chọn ca kiểm thử tự động. |
| 39 | `docs/qa/automation_status.md` | Automation Report | 215 lines | **KEEP** | **Bảo toàn nội dung giải trình**: Chứa Q&A giải thích lý do không tự động hóa OAuth bên thứ ba / phần cứng vân tay, và tiêu chí dừng ISTQB. |
| 40 | `docs/qa/automation_execution_summary.md` | Automation Report | 114 lines | **KEEP** | **Bảo toàn bảng ánh xạ duy nhất**: Chứa bảng đối chiếu trạng thái tự động hóa của 31 Test Case Hộp đen gốc (20/31 ca, độ bao phủ 64.52%). |
| 41 | `test_cases/non_functional/non_functional_test_cases.md` | Non-functional | 30 lines | **KEEP** | Đặc tả 8 kịch bản Phi chức năng (TC-NF-001..008). |
| 42 | `docs/bugs/defect_log.md` | Defect Log | 261 lines | **KEEP** | **Nhật ký quản lý lỗi chính thức**: Quản lý vòng đời đầy đủ BUG-001..005 và White-box defects. |
| 43 | `docs/plan_and_requirements/requirements_traceability_matrix.md` | RTM | 32 lines | **KEEP** | **Nguồn chân lý RTM**: Bao phủ 13 REQs, ánh xạ 100% Black-box, White-box, Automation và Defect. |
| 44 | `docs/requirements_traceability_matrix.md` | RTM (Bản cũ) | 31 lines | **DELETE** | Bản sao cũ tại thư mục gốc `docs/` (chỉ có 10 REQ, thiếu số liệu White-box và REQ-11..13). |
| 45 | `docs/test_report/Testing_Report.md` | Final Report | 227 lines | **KEEP** | **Báo cáo kiểm thử cuối cùng** (Chương 4 Đồ án tốt nghiệp: Chiến lược, Tự động hóa, Tích hợp). |
| 46 | `docs/test_report/progress_check_slides_outline.md` | Presentation | 65 lines | **KEEP** | Dàn ý slide thuyết trình bảo vệ/kiểm tra tiến độ đồ án (14/10/2026). |
| 47 | `docs/bugs/README.md` | Placeholder | 3 lines | **DELETE** | File placeholder rỗng 3 dòng (`docs/bugs/` đã có `defect_log.md`). |
| 48 | `docs/test_report/README.md` | Placeholder | 3 lines | **DELETE** | File placeholder rỗng 3 dòng (`docs/test_report/` đã có `Testing_Report.md`). |
| 49 | `test_cases/advanced/README.md` | Placeholder | 3 lines | **DELETE** | File placeholder rỗng 3 dòng trong thư mục rỗng không có test case. |
| 50 | `test_cases/automated/README.md` | Placeholder | 3 lines | **DELETE** | File placeholder rỗng 3 dòng trong thư mục rỗng (test code ở `automation/`). |
| 51 | `ios/Runner/Assets.xcassets/LaunchImage.imageset/README.md` | Framework Asset | 5 lines | **KEEP** | Template asset của Flutter iOS framework, tuyệt đối không can thiệp. |
| 52 | `docs/qa/repository_structure_proposal.md` | QA Audit History | 223 lines | **KEEP** | Tài liệu quản lý cấu hình và minh chứng quy trình kiểm thử của nhóm. |
| 53 | `evidence/fn15_19_run_20261011_0005/run_log.md` | Run Log | 87 lines | **KEEP** | Log kiểm thử thực địa máy thật FN-15..19 (Checklist). |
| 54 | `evidence/fn15_chk05_run_20261011_0035/run_log.md` | Run Log | 113 lines | **KEEP** | Log kiểm thử độc lập máy thật TC-BB-CHK-05 (Xóa mục Checklist). |
| 55 | `evidence/fn15_chk06_run_20261011_0025/run_log.md` | Run Log | 69 lines | **KEEP** | Log kiểm thử độc lập máy thật TC-BB-CHK-06 (Lưu & Mở lại Checklist). |
| 56 | `evidence/fn29_30_run_20261010_1025/run_log.md` | Run Log | 16 lines | **KEEP** | Audit log kiểm thử môi trường FN-29/30 (Sinh trắc học). |
| 57 | `evidence/fn29_30_run_20261010_1036/run_log.md` | Run Log | 101 lines | **KEEP** | Run 2 log chi tiết kiểm thử sinh trắc học trên Samsung S21 FE. |
| 58 | `evidence/fn40_41_run_20261010_1815/run_log.md` | Run Log | 71 lines | **KEEP** | Audit log kiểm thử đồng bộ 2 thiết bị Run 1 (FN-40/41). |
| 59 | `evidence/fn40_41_run_20261010_2125/run_log.md` | Run Log | 210 lines | **KEEP** | Run 2 log kiểm thử xung đột LWW & phân xử timestamp (Bằng chứng BUG-002). |
| 60 | `evidence/search_run_20261010_1725/run_log.md` | Run Log | 71 lines | **KEEP** | Run 2 log kiểm thử chức năng Tìm kiếm (FN-23) trên thiết bị thật. |

---

## 3. CHI TIẾT 4 ĐIỂM HIỆU CHỈNH THEO YÊU CẦU

### Điểm 1: Chuẩn hóa và làm rõ số lượng file
* **Trước hiệu chỉnh:** 60 file ban đầu, 49 KEEP, 2 MERGE, 7 DELETE, 2 REVIEW $\rightarrow$ Các nhóm số liệu bị lẫn lộn giữa nhóm khuyến nghị và nhóm đang cân nhắc.
* **Sau hiệu chỉnh (Chuẩn hóa dứt khoát):**
  * **Tổng file của repo ban đầu:** **60 file** (không tính `docs_cleanup_plan.md`).
  * **KEEP:** **54 file** (Bao gồm giữ lại `automation_plan.md`, `automation_status.md`, `automation_execution_summary.md`, `repository_structure_proposal.md`, `progress_check_slides_outline.md`, và không di chuyển `fn23_execution_sheet.md`).
  * **MERGE:** **1 file** (`supplementary_test_cases.md` hợp nhất vào `black_box_test_cases.md`).
  * **DELETE:** **5 file** (1 bản RTM cũ + 4 file README placeholder rỗng).
  * **Số file sau cleanup:** $60 - 1 - 5 = \mathbf{54 \text{ file}}$ chính thức.
  * **Định vị file `docs_cleanup_plan.md`:** Là tài liệu kế hoạch đóng vai trò hồ sơ nghiệm thu QA, nếu lưu trên repo thì tổng cộng là **55 file** `.md`.

### Điểm 2: Rà soát 5 file đề xuất DELETE và bảo toàn 2 báo cáo Automation
* **5 file xác nhận DELETE an toàn tuyệt đối:**
  1. `docs/requirements_traceability_matrix.md`: Bản sao cũ tại root `docs/` (chỉ có 10 REQs, thiếu White-box và REQ-11..13). Toàn bộ nội dung và chi tiết hơn đã có ở `docs/plan_and_requirements/requirements_traceability_matrix.md`.
  2. `docs/bugs/README.md`: Placeholder 3 dòng rỗng. Thư mục đã có `defect_log.md`.
  3. `docs/test_report/README.md`: Placeholder 3 dòng rỗng. Thư mục đã có `Testing_Report.md`.
  4. `test_cases/advanced/README.md`: Placeholder 3 dòng rỗng trong thư mục rỗng.
  5. `test_cases/automated/README.md`: Placeholder 3 dòng rỗng trong thư mục rỗng.
* **Bảo toàn `automation_status.md` và `automation_execution_summary.md` (Chuyển sang KEEP):**
  - **`automation_execution_summary.md`:** Chứa **nội dung duy nhất không có ở đâu khác**: Bảng ánh xạ tiến độ tự động hóa chi tiết của **31 Test Case Hộp đen gốc** (20 ca tự động, 64.52% coverage, tỷ lệ 16 Pass / 4 Fail). Các báo cáo Phase 4 chỉ theo dõi theo mã AT-ID mở rộng (61 ATs) chứ không có bảng đối chiếu 31 Black-box TCs này.
  - **`automation_status.md`:** Chứa **giải trình phạm vi quan trọng** (Mục I: trả lời các câu hỏi tại sao không tự động hóa OAuth bên thứ ba hoặc cảm biến vân tay, và Mục IV: tiêu chí dừng ISTQB).

### Điểm 3: Giữ riêng `automation_plan.md` thay vì gộp vào `test_plan.md`
* **Đánh giá rủi ro khi gộp:**
  - File `docs/plan_and_requirements/test_plan.md` hiện tại đã dài 358 dòng, là Master Test Plan cấp cao theo chuẩn IEEE 829.
  - Việc nhồi nhét chi tiết kỹ thuật 4 Phase của automation (Phase 1 đến Phase 4, danh sách phân kỳ chức năng) vào `test_plan.md` sẽ làm tài liệu bị phình to, trùng lặp và làm loãng tính khái quát của Master Test Plan.
  - Đồng thời, làm mất tính độc lập của tài liệu kế hoạch tự động hóa chuyên biệt trong hồ sơ QA.
* **Quyết định:** **GIỮ RIÊNG (KEEP)** file `docs/qa/automation_plan.md` độc lập trong thư mục `docs/qa/`.

### Điểm 4: Tạm bỏ thao tác di chuyển `fn23_execution_sheet.md`
* **Đánh giá rủi ro:**
  - File [test_cases/execution_sheets/fn23_execution_sheet.md](file:///d:/Workspace/TBDD/Smart-Note-App-QA/test_cases/execution_sheets/fn23_execution_sheet.md) đang được tham chiếu trực tiếp bởi nhiều tài liệu cốt lõi: `srs_condensed.md`, `test_plan.md`, `test_case_design_inventory_44_fn.md`, `black_box_execution_summary.md` và `run_log.md`.
  - Việc di chuyển file này sang `test_cases/black_box/` vào thời điểm hiện tại tiềm ẩn rủi ro phát sinh broken links hoặc xung đột với các script kiểm thử.
* **Quyết định:** **GIỮ NGUYÊN VỊ TRÍ** của `test_cases/execution_sheets/fn23_execution_sheet.md`. Tạm bỏ hoàn toàn thao tác di chuyển này khỏi kế hoạch dọn dẹp.
* **Bảo toàn phương án gộp 18 Supplementary Test Cases:**
  - Hợp nhất 18 test cases từ `supplementary_test_cases.md` vào cuối `black_box_test_cases.md` thành "PHẦN 2".
  - **Bảo toàn 100% mã TC** (`TC-BB-003C..039`), các cột bảng và tính truy vết (Traceability).

---

## 4. BẢNG TỔNG HỢP SO SÁNH TRƯỚC VÀ SAU CLEANUP

| Chỉ số | Trước Cleanup | Sau Cleanup | Ghi chú & Ý nghĩa bảo toàn |
|---|:---:|:---:|---|
| **Tổng file `.md` chính thức** | **60** | **54** | Giảm 6 file (xóa 5 file rác/trùng, gộp 1 file supplementary) |
| **File kế hoạch QA** | 0 | **1** | `docs_cleanup_plan.md` lưu trữ làm bằng chứng quy trình |
| **Hồ sơ White-box đóng băng** | 7 | **7** | **Bảo toàn 100%** (`test_cases/white_box/` & `evidence/white_box/`) |
| **Báo cáo Automation chuyên sâu** | 5 | **5** | **Bảo toàn 100%** (`plan`, `status`, `summary`, `phase_3c`, `phase_4`) |
| **Run Logs thực địa trên máy thật** | 8 | **8** | **Bảo toàn 100%** minh chứng chạy thực tế trong `evidence/` |
| **Master Spec Hộp đen** | 2 | **1** | Quy về 1 Master Spec duy nhất (`black_box_test_cases.md`) |
| **Nguồn chân lý RTM** | 2 | **1** | Loại bỏ bản cũ tại root, chỉ giữ bản 13 REQs tại `plan_and_requirements/` |
| **Thư mục placeholder rỗng** | 2 | **0** | Xóa sạch `test_cases/advanced/` và `test_cases/automated/` |

---

## 5. DANH SÁCH THAO TÁC CẦN THỰC HIỆN KHI ĐƯỢC DUYỆT

1. **Thao tác 1 (Hợp nhất 18 Supplementary TCs):**
   - Sao chép nguyên vẹn bảng 18 Test Cases từ `test_cases/black_box/supplementary_test_cases.md` nối vào mục cuối của `test_cases/black_box/black_box_test_cases.md`.
   - Xóa file nguồn `test_cases/black_box/supplementary_test_cases.md`.
2. **Thao tác 2 (Xóa 5 file rác & trùng lặp):**
   - Xóa `docs/requirements_traceability_matrix.md` (bản RTM cũ 10 REQs).
   - Xóa 4 placeholder: `docs/bugs/README.md`, `docs/test_report/README.md`, `test_cases/advanced/README.md`, `test_cases/automated/README.md`.
   - Xóa 2 thư mục rỗng: `test_cases/advanced/` và `test_cases/automated/`.
3. **Thao tác 3 (Kiểm tra toàn vẹn liên kết):**
   - Quét tự động toàn bộ 54 file còn lại đảm bảo **0 broken links**.
4. **Thao tác 4 (Báo cáo kết quả):**
   - Trình `git status` và danh sách file cho bạn nghiệm thu trước khi commit.

---
*Kế hoạch đã được cập nhật chính xác theo 4 điểm yêu cầu. Đang dừng chờ phê duyệt từ bạn trước khi thực hiện bất kỳ thao tác nào.*
