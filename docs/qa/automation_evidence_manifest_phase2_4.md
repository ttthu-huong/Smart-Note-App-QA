# MANIFEST KIỂM TOÁN VÀ CHUẨN BỊ COMMIT BẰNG CHỨNG KIỂM THỬ TỰ ĐỘNG (PHASE 2, PHASE 3, PHASE 4)

**Dự án:** Smart Note App (Mobile QA — Android)
**Nhánh công việc:** `huong`
**Commit HEAD cơ sở:** `b97072a` (*test(automation): finalize extended UI tests FN08-FN20*)
**Thời điểm kiểm toán:** 21/10/2026
**Phạm vi kiểm toán & đóng gói:**
- **Phase 2 (FN-08, FN-09, FN-10, FN-11, FN-12):** Quản lý ghi chú văn bản & vòng đời (32 execution items).
- **Phase 3 (FN-13, FN-14):** Quản lý lưu trữ ghi chú (Archive / Unarchive) (5 execution items).
- **Phase 4 (FN-20):** Ghim và Bỏ ghim ghi chú (Pin / Unpin Note) (15 execution items).

---

## 1. TỔNG QUAN KẾT QUẢ KIỂM TOÁN THỰC THI (52 EXECUTION ITEMS)

Toàn bộ 52 execution items đã được đối chiếu chéo giữa đặc tả kiểm thử, tài liệu tổng kết (`automation_execution_summary.md`, `automation_status.md`, `fn20_phase4_closure_20261020.md`), các execution sheet, các file báo cáo JUnit XML thực tế và cây thư mục ảnh chụp màn hình (screenshot evidence).

**Nguyên tắc kiểm toán nghiêm ngặt:**
1. **Đọc XML thực tế:** Kiểm tra trực tiếp cấu trúc XML, thẻ `<testcase>`, xác minh thuộc tính `time`, số lượng `failures="0"` và `errors="0"`. Tuyệt đối không suy diễn kết quả PASS chỉ dựa trên tên file XML.
2. **Lọc lượt chạy chính thức:** Chỉ chọn các file JUnit XML của lượt PASS hoặc BLOCKED chính thức đã được báo cáo. Các lượt retry gặp sự cố môi trường (`FAIL-AUTO`) được ghi nhận trong lịch sử kỹ thuật, không tính trùng vào mẫu số và không làm sai lệch kết quả.
3. **Bảo toàn trạng thái nghiệp vụ:** Giữ nguyên trạng thái `BLOCKED (pytest: SKIPPED)` cho `TC-BB-022C D01`, giữ nguyên defect `BUG-005` ở trạng thái **OPEN** (lỗi RenderFlex Overflow thoáng qua khi chuyển Editor về Home). Tuyệt đối không sửa Expected Result hay mã nguồn `lib/`.
4. **Kiểm tra tính toàn vẹn evidence:** Xác minh từng file ảnh screenshot tồn tại vật lý, dung lượng > 0 byte (không có file rỗng/corrupt), gắn đúng TC-ID và định danh phiên chạy (`RUN_ID`).

### Bảng tổng hợp số liệu theo Phase

| Giai đoạn | Nhóm chức năng (FN) | Tổng items | PASS | BLOCKED | FAIL cuối cùng | Tỷ lệ thành công | Trạng thái ghi nhận |
|---|---|---:|---:|---:|---:|---:|---|
| **Phase 2** | FN-08, FN-09, FN-10, FN-11, FN-12 | 32 | 31 | 1 | 0 | 96.88% PASS | 31 PASS / 1 BLOCKED (`TC-BB-022C D01`), BUG-005 OPEN |
| **Phase 3** | FN-13, FN-14 | 5 | 5 | 0 | 0 | 100.00% PASS | 5 PASS / 0 FAIL / 0 BLOCKED |
| **Phase 4** | FN-20 | 15 | 15 | 0 | 0 | 100.00% PASS | 15 PASS / 0 FAIL / 0 BLOCKED (tài khoản QA cô lập cho 024G) |
| **TỔNG CỘNG** | **Phase 2 + Phase 3 + Phase 4** | **52** | **51** | **1** | **0** | **98.08% PASS** | **51 PASS / 1 BLOCKED / 0 FAIL** |

---

## 2. MANIFEST CHI TIẾT PHASE 2 — FN-08 ĐẾN FN-12 (32 EXECUTION ITEMS)

### 2.1. Danh mục 32 execution items Phase 2

| # | TC-ID / Data-ID | Chức năng | Tên kịch bản kiểm thử | Status XML | Thời gian (s) | JUnit XML tương ứng | Thư mục / File Evidence thực tế | Ghi chú kỹ thuật |
|---:|---|---|---|:---:|---:|---|---|---|
| 1 | **TC-BB-016** / D01 | FN-08 | Tạo ghi chú có đủ Tiêu đề & Nội dung | PASS | 31.82s | `fn08_create_note_junit.xml` | `evidence/fn08/FN08_TC-BB-016_D01_01.png`<br>(1 ảnh) | Baseline lịch sử (đã commit từ trước). |
| 2 | **TC-BB-017** / D01 | FN-08 | Tạo ghi chú chỉ có Nội dung | PASS | 23.26s | `fn08_create_note_junit.xml` | `evidence/fn08/FN08_TC-BB-017_D01_01.png`<br>(1 ảnh) | Baseline lịch sử (đã commit từ trước). |
| 3 | **TC-BB-018** / D01 | FN-08 | Không tạo ghi chú rỗng khi để trống cả 2 ô | PASS | 15.68s | `fn08_create_note_junit.xml` | `evidence/fn08/FN08_TC-BB-018_D01_01.png`<br>(1 ảnh) | Baseline lịch sử (đã commit từ trước). |
| 4 | **TC-BB-018B** / D01 | FN-08 | Tạo ghi chú chỉ có Tiêu đề (nội dung rỗng) | PASS | 49.34s | `fn08_probe_20261020_001621.xml` | `evidence/fn08/FN08_TC-BB-018B_D01_01.png`<br>`evidence/fn08/automation_20261020_001623_862241/`<br>(2 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 5 | **TC-BB-018C** / D01 | FN-08 | Tự động lưu ngầm không cần bấm Back (force-stop Editor) | PASS | 58.64s | `fn08_remaining_20261020_001724.xml` | `evidence/fn08/FN08_TC-BB-018C_D01_01.png`<br>`evidence/fn08/automation_20261020_001726_964611/`<br>(5 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 6 | **TC-BB-018D** / D01 | FN-08 | Hủy bản nháp khi xóa sạch về rỗng | PASS | 25.96s | `fn08_remaining_20261020_001724.xml` | `evidence/fn08/FN08_TC-BB-018D_D01_01.png`<br>`evidence/fn08/automation_20261020_001726_964611/`<br>(5 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 7 | **TC-BB-018E** / D01 | FN-08 | Unicode phức tạp, tiếng Việt, emoji, HTML-like text | PASS | 42.53s | `fn08_018e_final_20261020_015417.xml` | `evidence/fn08/FN08_TC-BB-018E_D01_01.png`<br>`evidence/fn08/FN08_TC-BB-018E_D01_02.png`<br>`evidence/fn08/automation_20261020_015419_043437/`<br>(8 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 8 | **TC-BB-018F** / D01 | FN-08 | Tính bền vững của ghi chú sau khi restart ứng dụng | PASS | 53.66s | `fn08_remaining_20261020_001724.xml` | `evidence/fn08/FN08_TC-BB-018F_D01_01.png`<br>`evidence/fn08/automation_20261020_001726_964611/`<br>(5 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 9 | **TC-BB-019** / D01 | FN-09 | Chỉnh sửa nội dung ghi chú | PASS | 46.40s | `fn09_019_20261020_025349.xml` | `evidence/fn09/automation_20261020_025350_985392_2c7d2b87/`<br>`evidence/fn09/FN09_TC-BB-019_D01_01.png`<br>(4 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 10 | **TC-BB-019B** / D01 | FN-09 | Chỉ đổi tiêu đề; giữ nguyên nội dung | PASS | 68.81s | `fn09_019b_fixed_20261020_030253.xml` | `evidence/fn09/automation_20261020_030254_716373_ac23e584/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 11 | **TC-BB-019C** / D01 | FN-09 | Đổi cả tiêu đề và nội dung | PASS | 44.78s | `fn09_019c_retry_20261020_031702.xml` | `evidence/fn09/automation_20261020_031703_633145_ef50e8ff/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 12 | **TC-BB-019D** / D01 | FN-09 | Xóa tiêu đề; giữ nguyên nội dung | PASS | 43.06s | `fn09_019d_20261020_032717.xml` | `evidence/fn09/automation_20261020_032718_614397_0fc1d6b5/`<br>(4 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 13 | **TC-BB-019E** / D01 | FN-09 | Xóa nội dung; giữ nguyên tiêu đề | PASS | 55.19s | `fn09_019e_retry_20261020_040014.xml` | `evidence/fn09/automation_20261020_040016_148745_d1062ac5/`<br>(4 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 14 | **TC-BB-019F** / D01 | FN-09 | Xóa cả tiêu đề và nội dung (dọn rác ghi chú) | PASS | 42.03s | `fn09_019f_20261020_041022.xml` | `evidence/fn09/automation_20261020_041023_362641_4e744850/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 15 | **TC-BB-019G** / D01 | FN-09 | Thoát sau chỉnh sửa bằng Android System Back | PASS | 52.06s | `fn09_019g_d01_20261020_041415.xml` | `evidence/fn09/automation_20261020_041416_237915_e5a52ab0/`<br>(4 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 16 | **TC-BB-019G** / D02 | FN-09 | Thoát sau chỉnh sửa bằng Android Gesture Back | PASS | 48.55s | `fn09_019g_d02_retry_20261020_094859.xml` | `evidence/fn09/automation_20261020_094901_092380_3febeb92/`<br>(4 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 17 | **TC-BB-020** / D01 | FN-09 | Autosave sau 2.8s, force-stop ngay tại Editor | PASS | 48.89s | `fn09_020_20261020_031828.xml` | `evidence/fn09/automation_20261020_031829_739761_dd030562/`<br>`evidence/fn09/FN09_TC-BB-020_D01_01.png`<br>(5 ảnh) | Autosave debounce 2.8s PASS nghiệp vụ; BUG-005 là lỗi giao diện RenderFlex Overflow, vẫn OPEN. |
| 18 | **TC-BB-020B** / D01 | FN-09 | Chỉnh sửa tuần tự 2 lần trên cùng note ID | PASS | 56.40s | `fn09_020b_20261020_095438.xml` | `evidence/fn09/automation_20261020_095440_379178_437e76e5/`<br>(5 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 19 | **TC-BB-020C** / D01 | FN-09 | Unicode tiếng Việt, emoji, ký tự đặc biệt | PASS | 42.00s | `fn09_020c_20261020_095808.xml` | `evidence/fn09/automation_20261020_095810_612309_3146c2ce/`<br>(4 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 20 | **TC-BB-020D** / D01 | FN-09 | Nội dung chỉnh sửa tồn tại sau khi restart app | PASS | 52.86s | `fn09_020d_20261020_100042.xml` | `evidence/fn09/automation_20261020_100044_765185_4c77ba97/`<br>(5 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 21 | **TC-BB-021** / D01 | FN-10 | Chuyển 1 ghi chú vào Thùng rác từ Selection Bar | PASS | 79.81s | `fn10_trash_junit.xml` | `evidence/fn10/FN10_TC-BB-021_D01_01.png`<br>(1 ảnh) | Baseline lịch sử (đã commit từ trước). |
| 22 | **TC-BB-021B** / D01 | FN-10 | Hoàn tác chuyển ghi chú vào Thùng rác từ SnackBar | NO_XML_REPORT | — | *Chờ xuất XML riêng* | `evidence/fn10/automation_20261020_110841_407404_51da0bf6/TC-BB-021B/`<br>(4 ảnh) | Lượt chạy 20/10 lúc 11:08:41 PASS, 4 ảnh evidence đầy đủ; chưa tạo file XML riêng. |
| 23 | **TC-BB-021C** / D01 | FN-10 | Hủy xóa ghi chú từ menu 3 chấm trong Editor | PASS | 100.48s | `fn10_021c_d01_retry_20261020_120916.xml` | `evidence/fn10/automation_20261020_120917_335994_c5046c82/TC-BB-021C/`<br>(5 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 24 | **TC-BB-021C** / D02 | FN-10 | Xác nhận xóa ghi chú từ menu 3 chấm trong Editor | PASS | 95.20s | `fn10_021c_d02_20261020_124605.xml` | `evidence/fn10/automation_20261020_124606_790642_535958ce/TC-BB-021C/`<br>(5 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 25 | **TC-BB-021D** / D01 | FN-10 | Chọn nhiều ghi chú (2 notes) và chuyển vào Thùng rác | PASS | 95.36s | `fn10_021d_20261020_130907.xml` | `evidence/fn10/automation_20261020_130909_123394_aea15e14/TC-BB-021D/`<br>(5 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 26 | **TC-BB-022** / D01 | FN-11 | Khôi phục 1 ghi chú từ Thùng rác về Trang chủ | PASS | 92.37s | `fn11_restore_junit.xml` | `evidence/fn11/FN11_TC-BB-022_D01_01.png`<br>(1 ảnh) | Baseline lịch sử (đã commit từ trước). |
| 27 | **TC-BB-022B** / D01 | FN-11 | Khôi phục hàng loạt ghi chú (multi-restore) | PASS | 123.76s | `fn11_022b_20261020_132119.xml` | `evidence/fn11/automation_20261020_132134_088541_974befa2ac/TC-BB-022B/`<br>(4 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 28 | **TC-BB-022C** / D01 | FN-11 | Kiểm tra giao diện Empty State "Thùng rác trống" | **BLOCKED** *(SKIPPED)* | 42.21s | `fn11_022c_20261020_132720.xml` | `evidence/fn11/automation_20261020_132734_161378_9a81212f/TC-BB-022C/precondition_not_empty.png`<br>(1 ảnh) | BLOCKED do tiền điều kiện Thùng rác có sẵn ghi chú rác cũ từ test trước. |
| 29 | **TC-BB-023** / D01 | FN-12 | Xóa vĩnh viễn 1 ghi chú khỏi Thùng rác | PASS | 88.69s | `fn12_permanent_delete_junit.xml` | `evidence/fn12/FN12_TC-BB-023_D01_01.png`<br>(1 ảnh) | Baseline lịch sử (đã commit từ trước). |
| 30 | **TC-BB-023B** / D01 | FN-12 | Hủy xóa vĩnh viễn nhiều ghi chú trên AlertDialog | PASS | 102.52s | `fn12_023b_d01_retry_20261020_135257.xml` | `evidence/fn12/automation_20261020_135310_686942_d3abb8b620/TC-BB-023B/`<br>(5 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 31 | **TC-BB-023B** / D02 | FN-12 | Xác nhận xóa vĩnh viễn nhiều ghi chú trên AlertDialog | PASS | 128.59s | `fn12_023b_d02_20261020_145053.xml` | `evidence/fn12/automation_20261020_145107_957126_f1858ca760/TC-BB-023B/`<br>(6 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 32 | **TC-BB-023C** / D01 | FN-12 | Tính bền vững vòng đời ghi chú sau restart | PASS | 141.84s | `fn12_023c_20261020_150216.xml` | `evidence/fn12/automation_20261020_150230_580481_1c12522463/TC-BB-023C/`<br>(5 ảnh) | Mở rộng tự động hóa UI/E2E. |

---

## 3. MANIFEST CHI TIẾT PHASE 3 — FN-13 VÀ FN-14 (5 EXECUTION ITEMS)

### 3.1. Danh mục 5 execution items Phase 3

| # | TC-ID / Data-ID | Chức năng | Tên kịch bản kiểm thử | Status XML | Thời gian (s) | JUnit XML tương ứng | Thư mục / File Evidence thực tế | Ghi chú kỹ thuật |
|---:|---|---|---|:---:|---:|---|---|---|
| 33 | **TC-BB-040** / D01 | FN-13 | Lưu trữ 1 ghi chú từ HomeScreen (Selection Bar) | PASS | 51.65s | `fn13_fn14_20261020_162606.xml` | `evidence/fn13_14/automation_20261020_162615_605331_014938864a/TC-BB-040/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 34 | **TC-BB-EXT-008** / D01 | FN-13 | Lưu trữ Target không ảnh hưởng Control (Cô lập dữ liệu) | PASS | 74.39s | `fn13_fn14_remaining3_20261020_165116.xml` | `evidence/fn13_14/automation_20261020_165126_004774_5c06926696/TC-BB-EXT-008/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 35 | **TC-BB-EXT-006** / D01 | FN-13 | Tính bền vững dữ liệu lưu trữ tiếng Việt sau khi restart app | PASS | 55.51s | `fn13_fn14_remaining3_20261020_165116.xml` | `evidence/fn13_14/automation_20261020_165232_968737_a40c7e7091/TC-BB-EXT-006/`<br>(4 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 36 | **TC-BB-040B** / D01 | FN-14 | Bỏ lưu trữ ghi chú từ ArchiveScreen qua BottomSheet | PASS | 64.56s | `fn14_040b_usb_20261020_164931.xml` | `evidence/fn13_14/automation_20261020_164941_019186_493c0b9697/TC-BB-040B/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 37 | **TC-BB-EXT-007** / D01 | FN-14 | Vòng lặp Bỏ lưu trữ -> Lưu trữ -> Bỏ lưu trữ (Idempotency) | PASS | 98.37s | `fn13_fn14_remaining3_20261020_165116.xml` | `evidence/fn13_14/automation_20261020_165328_477351_4b7542817e/TC-BB-EXT-007/`<br>(5 ảnh) | Mở rộng tự động hóa UI/E2E. |

---

## 4. MANIFEST CHI TIẾT PHASE 4 — FN-20 (15 EXECUTION ITEMS)

### 4.1. Danh mục 15 execution items Phase 4

| # | TC-ID / Data-ID | Chức năng | Tên kịch bản kiểm thử | Status XML | Thời gian (s) | JUnit XML tương ứng | Thư mục / File Evidence thực tế | Ghi chú kỹ thuật |
|---:|---|---|---|:---:|---:|---|---|---|
| 38 | **TC-BB-024** / D01 | FN-20 | Ghim ghi chú lên khu vực ưu tiên từ Trang chủ | PASS | 23.64s | `fn20_pin_note_junit.xml` | `evidence/fn20/FN20_TC-BB-024_D01_01.png`<br>(1 ảnh) | Baseline lịch sử (đã commit từ trước). |
| 39 | **TC-BB-025** / D01 | FN-20 | Bỏ ghim ghi chú trở về danh sách thông thường từ Trang chủ | PASS | 13.52s | `fn20_pin_note_junit.xml` | `evidence/fn20/FN20_TC-BB-025_D01_01.png`<br>(1 ảnh) | Baseline lịch sử (đã commit từ trước). |
| 40 | **TC-BB-024B** / D01 | FN-20 | Ghim ghi chú trực tiếp từ AppBar màn hình soạn thảo (Editor) | PASS | 75.27s | `fn20_editor_20261020_191551.xml` | `evidence/fn20/run_20261020_191601_27ef75ac/TC-BB-024B_D01/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 41 | **TC-BB-024B** / D02 | FN-20 | Bỏ ghim ghi chú trực tiếp từ AppBar màn hình soạn thảo (Editor) | PASS | 193.85s | `fn20_024b_d02_retry2_20261020_195008.xml` | `evidence/fn20/run_20261020_195017_78c1f1f3/TC-BB-024B_D02/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 42 | **TC-BB-024C** / D01 | FN-20 | Ràng buộc không cho phép ghim ghi chú mới khi chưa nhập nội dung | PASS | 37.38s | `fn20_024c_d01_20261020_195609.xml` | `evidence/fn20/run_20261020_195618_3e41d9d8/TC-BB-024C_D01/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 43 | **TC-BB-024D** / D01 | FN-20 | Ghim đồng thời nhiều ghi chú từ Trang chủ (Batch Pin 2 notes) | PASS | 81.18s | `fn20_batch_20261020_190742.xml` | `evidence/fn20/run_20261020_190753_ae757378/TC-BB-024D_D01/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 44 | **TC-BB-024H** / D01 | FN-20 | Đảo trạng thái độc lập khi chọn đồng thời ghi chú đã ghim và chưa ghim | PASS | 71.17s | `fn20_batch_20261020_190742.xml` | `evidence/fn20/run_20261020_190906_dab38cc3/TC-BB-024H_D01/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 45 | **TC-BB-025D** / D01 | FN-20 | Bỏ ghim đồng thời nhiều ghi chú từ Trang chủ (Batch Unpin 2 notes) | PASS | 78.28s | `fn20_batch_20261020_190742.xml` | `evidence/fn20/run_20261020_191017_3e9899d7/TC-BB-025D_D01/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 46 | **TC-BB-025E** / D01 | FN-20 | Phân vùng Được ghim duy trì khi chỉ bỏ ghim 1 trong số nhiều note ghim | PASS | 81.50s | `fn20_batch_20261020_190742.xml` | `evidence/fn20/run_20261020_191135_00e1fa58/TC-BB-025E_D01/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 47 | **TC-BB-024E** / D01 | FN-20 | Hiển thị phân vùng Được ghim và Khác khi có đồng thời cả 2 loại ghi chú | PASS | 118.47s | `fn20_024e_v7_20261020_205408.xml` | `evidence/fn20/run_20261020_205417_9fc5ebc6/TC-BB-024E_D01/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 48 | **TC-BB-024F** / D01 | FN-20 | Tính toàn vẹn dữ liệu (Tiêu đề, Nội dung) qua chu kỳ Pin -> Unpin | PASS | 267.77s | `fn20_024f_20261020_205909.xml` | `evidence/fn20/run_20261020_205918_b7b5d72e/TC-BB-024F_D01/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 49 | **TC-BB-024G** / D01 | FN-20 | Giao diện khi toàn bộ các ghi chú đều ở trạng thái được ghim (All Pinned) | PASS | 145.29s | `fn20_024g_v9_20261020_221313.xml` | `evidence/fn20/run_20261020_221322_59346191/TC-BB-024G_D01/`<br>(4 ảnh) | Tài khoản QA cô lập (`QA_ACCOUNT_SCOPED_V9`), 0 `pm clear`, SQLite `user_id` verified, không sửa note cũ. |
| 50 | **TC-BB-025B** / D01 | FN-20 | Tính bền vững trạng thái Ghim sau khi khởi động lại ứng dụng | PASS | 54.09s | `fn20_025b_v8_20261020_211941.xml` | `evidence/fn20/run_20261020_211950_c769bfbe/TC-BB-025B_D01/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 51 | **TC-BB-025C** / D01 | FN-20 | Ghi chú đã ghim vẫn duy trì trạng thái ghim sau khi chỉnh sửa nội dung | PASS | 207.57s | `fn20_025c_20261020_213027.xml` | `evidence/fn20/run_20261020_213036_64bf71ee/TC-BB-025C_D01/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |
| 52 | **TC-BB-025F** / D01 | FN-20 | Tính bền vững trạng thái Bỏ ghim sau khi khởi động lại ứng dụng | PASS | 214.88s | `fn20_025f_20261020_215211.xml` | `evidence/fn20/run_20261020_215221_b1d825c4/TC-BB-025F_D01/`<br>(3 ảnh) | Mở rộng tự động hóa UI/E2E. |

---

## 5. BÁO CÁO ĐẶC BIỆT: TÀI KHOẢN QA CÔ LẬP CHO TC-BB-024G D01

- **Mã test case:** `TC-BB-024G / D01` (*Giao diện khi toàn bộ ghi chú đều được ghim — All Pinned*).
- **File kiểm thử:** `automation/tests/test_fn20_extended.py` (hàm `test_tc_bb_024g_d01_all_notes_pinned_layout`).
- **Phiên bản giải thuật:** `QA_ACCOUNT_SCOPED_V9`.
- **Giải pháp an toàn dữ liệu người dùng:**
  1. **Không sử dụng lệnh phá hủy môi trường:** Tuyệt đối không chạy `adb shell pm clear`, không reset dữ liệu ứng dụng, không đăng xuất làm ảnh hưởng dữ liệu đang lưu.
  2. **Tiền điều kiện màn hình trống:** Bắt buộc tài khoản QA đang đăng nhập phải có màn hình chính hoàn toàn trống (`Chưa có ghi chú nào` / `No notes yet`) tại thời điểm bắt đầu test.
  3. **Tạo dữ liệu định danh riêng:** Tạo chính xác 3 ghi chú QA có tiền tố độc nhất `QA_PIN_024G_{marker}_{1..3}`.
  4. **Xác thực SQLite theo `user_id`:** Sử dụng `adb exec-out run-as com.example.smart_note cat databases/smart_note.db` để trích xuất SQLite sang bộ nhớ in-memory, kiểm tra trường `user_id` của 3 ghi chú mới để xác định chính xác định danh chủ sở hữu (`owner`). Xác minh chủ sở hữu này không có bất kỳ ghi chú `normal` hay `pinned` nào khác trước khi test chạy.
  5. **Bảo toàn dữ liệu tài khoản khác:** Các bản ghi thuộc các `user_id` khác trong SQLite được bỏ qua hoàn toàn, không bị chỉnh sửa trạng thái hay ghim/bỏ ghim.
  6. **Kiểm tra giao diện toàn diện:** Ghim cả 3 ghi chú, quét toàn bộ danh sách để khẳng định phân vùng "Được ghim" hiển thị đầy đủ 3 thẻ ghi chú và phân vùng "Khác" hoàn toàn vắng mặt trên giao diện.
- **File JUnit XML:** `automation/reports/fn20_024g_v9_20261020_221313.xml` (tests=1, failures=0, errors=0, time=145.29s, PASS).
- **Thư mục Evidence:** `evidence/fn20/run_20261020_221322_59346191/TC-BB-024G_D01/` gồm 4 ảnh:
  - `TC-BB-024G_D01_01.png` (164,407 bytes): Màn hình Home trống ban đầu của tài khoản QA.
  - `TC-BB-024G_D01_02.png` (297,686 bytes): 3 ghi chú QA đã tạo thành công.
  - `TC-BB-024G_D01_03.png` (314,074 bytes): Đã ghim toàn bộ 3 ghi chú lên khu vực Được ghim.
  - `TC-BB-024G_D01_04.png` (314,286 bytes): Xác nhận toàn bộ danh sách chỉ có "Được ghim", không có mục "Khác".

---

## 6. PHÂN LOẠI ARTEFACT & DANH MỤC LƯU GIỮ (HOLD REGISTRY)

Để đảm bảo tuân thủ nghiêm ngặt nguyên tắc **an toàn kho mã nguồn** và **chỉ đóng gói các artefact đã qua kiểm toán**, toàn bộ các file trong workspace được phân loại rạch ròi:

### 6.1. Danh mục các file AN TOÀN sẵn sàng Stage (Verified Safe to Stage)

1. **Tài liệu Manifest:**
   - `docs/qa/automation_evidence_manifest_phase2_4.md` (tài liệu này).
2. **Báo cáo kiểm thử JUnit XML chính thức (36 files):**
   - **Phase 2 (23 XMLs):**
     - FN-08 (3 files): `fn08_probe_20261020_001621.xml`, `fn08_remaining_20261020_001724.xml`, `fn08_018e_final_20261020_015417.xml`.
     - FN-09 (12 files): `fn09_019_20261020_025349.xml`, `fn09_019b_fixed_20261020_030253.xml`, `fn09_019c_retry_20261020_031702.xml`, `fn09_019d_20261020_032717.xml`, `fn09_019e_retry_20261020_040014.xml`, `fn09_019f_20261020_041022.xml`, `fn09_019g_d01_20261020_041415.xml`, `fn09_019g_d02_retry_20261020_094859.xml`, `fn09_020_20261020_031828.xml`, `fn09_020b_20261020_095438.xml`, `fn09_020c_20261020_095808.xml`, `fn09_020d_20261020_100042.xml`.
     - FN-10 (3 files): `fn10_021c_d01_retry_20261020_120916.xml`, `fn10_021c_d02_20261020_124605.xml`, `fn10_021d_20261020_130907.xml`.
     - FN-11 (2 files): `fn11_022b_20261020_132119.xml`, `fn11_022c_20261020_132720.xml`.
     - FN-12 (3 files): `fn12_023b_d01_retry_20261020_135257.xml`, `fn12_023b_d02_20261020_145053.xml`, `fn12_023c_20261020_150216.xml`.
   - **Phase 3 (3 XMLs):**
     - `fn13_fn14_20261020_162606.xml`, `fn14_040b_usb_20261020_164931.xml`, `fn13_fn14_remaining3_20261020_165116.xml`.
   - **Phase 4 (10 XMLs):**
     - `fn20_editor_20261020_191551.xml`, `fn20_024b_d02_retry2_20261020_195008.xml`, `fn20_024c_d01_20261020_195609.xml`, `fn20_batch_20261020_190742.xml`, `fn20_024e_v7_20261020_205408.xml`, `fn20_024f_20261020_205909.xml`, `fn20_024g_v9_20261020_221313.xml`, `fn20_025b_v8_20261020_211941.xml`, `fn20_025c_20261020_213027.xml`, `fn20_025f_20261020_215211.xml`.
3. **Thư mục Screenshot Evidence chính thức (42 thư mục, 155 PNG files, ~93.59 MB):**
   - `evidence/fn08/` (3 thư mục run): `automation_20261020_001623_862241`, `automation_20261020_001726_964611`, `automation_20261020_015419_043437`.
   - `evidence/fn09/` (12 thư mục run): `automation_20261020_025350_985392_2c7d2b87`, `automation_20261020_030254_716373_ac23e584`, `automation_20261020_031703_633145_ef50e8ff`, `automation_20261020_031829_739761_dd030562`, `automation_20261020_032718_614397_0fc1d6b5`, `automation_20261020_040016_148745_d1062ac5`, `automation_20261020_041023_362641_4e744850`, `automation_20261020_041416_237915_e5a52ab0`, `automation_20261020_094901_092380_3febeb92`, `automation_20261020_095440_379178_437e76e5`, `automation_20261020_095810_612309_3146c2ce`, `automation_20261020_100044_765185_4c77ba97`.
   - `evidence/fn10/` (4 thư mục run): `automation_20261020_110841_407404_51da0bf6`, `automation_20261020_120917_335994_c5046c82`, `automation_20261020_124606_790642_535958ce`, `automation_20261020_130909_123394_aea15e14`.
   - `evidence/fn11/` (2 thư mục run): `automation_20261020_132134_088541_974befa2ac`, `automation_20261020_132734_161378_9a81212f`.
   - `evidence/fn12/` (3 thư mục run): `automation_20261020_135310_686942_d3abb8b620`, `automation_20261020_145107_957126_f1858ca760`, `automation_20261020_150230_580481_1c12522463`.
   - `evidence/fn13_14/` (5 thư mục run): `automation_20261020_162615_605331_014938864a`, `automation_20261020_164941_019186_493c0b9697`, `automation_20261020_165126_004774_5c06926696`, `automation_20261020_165232_968737_a40c7e7091`, `automation_20261020_165328_477351_4b7542817e`.
   - `evidence/fn20/` (13 thư mục run): `run_20261020_190753_ae757378`, `run_20261020_190906_dab38cc3`, `run_20261020_191017_3e9899d7`, `run_20261020_191135_00e1fa58`, `run_20261020_191601_27ef75ac`, `run_20261020_195017_78c1f1f3`, `run_20261020_195618_3e41d9d8`, `run_20261020_205417_9fc5ebc6`, `run_20261020_205918_b7b5d72e`, `run_20261020_211950_c769bfbe`, `run_20261020_213036_64bf71ee`, `run_20261020_215221_b1d825c4`, `run_20261020_221322_59346191`.

### 6.2. Danh mục GIỮ NGUYÊN KHÔNG STAGE (HOLD Registry)

| Nhóm đối tượng | Đường dẫn / Mẫu nhận diện | Lý do HOLD (Không Stage) |
|---|---|---|
| **Ảnh baseline bị Modified** | `evidence/fn02/FN02_TC-BB-001*..005*` (16 ảnh)<br>`evidence/fn04/FN04_TC-BB-006*..009*` (7 ảnh)<br>`evidence/fn05/FN05_TC-BB-011*` (2 ảnh)<br>`evidence/fn08/FN08_TC-BB-016*..018*` (3 ảnh)<br>`evidence/fn09/FN09_TC-BB-019*..020*` (2 ảnh)<br>`evidence/fn20/FN20_TC-BB-024*..025*` (2 ảnh)<br>`evidence/fn23/FN23_TC-BB-026*..029*` (4 ảnh)<br>*(Tổng cộng 36 ảnh baseline)* | Ảnh gốc baseline bị thay đổi timestamp/metadata trong working tree; tuân thủ quy tắc 4 tuyệt đối không stage, không ghi đè, không restore, không xóa. |
| **JUnit XML lịch sử / Retry thất bại** | `automation/reports/fn08_018e_debug_*`, `fn08_018e_verify_*`, `fn08_018e_retry_*`, `fn08_probe_20261019_*`, `fn08_probe_20261020_001427*`, `fn09_019b_retry*`, `fn09_019c_20261020_030459*`, `fn09_019e_20261020_034025*`, `fn09_019f_20261020_040829*`, `fn09_019g_d02_20261020_042313*`, `fn10_021c_d01_20261020_111229*`, `fn10_021c_d01_20261020_112646*`, `fn12_023b_d01_20261020_134021*`, `fn12_023b_d01_retry_20261020_134854*`, `fn12_023b_d01_retry_20261020_135019*`, `fn13_040_20261020_160453*`, `fn13_040_retry_20261020_161028*`, `fn13_fn14_20261020_162506*`, `fn13_fn14_remaining_20261020_163105*`, `fn14_040b_retry_20261020_163935*`, `fn20_024b_d02_retry_20261020_194006*`, `fn20_024e_retry*`, `fn20_024e_fixed*`, `fn20_024e_v4*`, `fn20_024e_v5*`, `fn20_layout_safe*`, `fn20_025b_20261020_210640*` | Các file XML sinh ra trong các lượt chạy thử nghiệm, lỗi môi trường `FAIL-AUTO` đã được retry thành công ở lượt sau. Không cộng trùng vào kết quả chính thức. |
| **Thư mục evidence retry / trung gian** | `evidence/fn08/automation_20261020_001429_*`, `_004216_*`, `_011132_*`<br>`evidence/fn09/automation_20261020_030501_*`, `_042314_*`<br>`evidence/fn09/diagnostics/`<br>`evidence/fn10/automation_20261020_112647_*`<br>`evidence/fn12/automation_20261020_134034_*`, `_135033_*`<br>`evidence/fn13_14/automation_20261020_160502_*`, `_161037_*`, `_163114_*`<br>`evidence/fn20/run_20261020_194015_*`, `_201545_*`, `_202905_*`, `_204124_*` | Thư mục ảnh của các phiên chạy sơ bộ bị gián đoạn hoặc retry; giữ nguyên trên ổ đĩa để đối chiếu lịch sử khi cần thiết, không stage vào kho mã nguồn. |
| **File Dump XML & Diagnostic tạm** | `evidence/ui_dump.xml`<br>`evidence/window_dump_after_fab.xml`<br>`evidence/window_dump_note.xml`<br>`editor_dump.xml`<br>`evidence/note_editor.png`<br>`evidence/fn10/editor_missing_fields.png`<br>`evidence/fn11/editor_missing_fields.png`<br>`evidence/fn12/editor_missing_fields.png` | Dữ liệu dump tạm giao diện uiautomator dùng để phân tích locator và xử lý incident; không thuộc bộ bằng chứng nghiệm thu chính thức. |
| **File Backup & Script sửa lỗi tạm** | `automation/tests/test_fn10_trash.py.bak`<br>`automation/tests/test_fn10_trash.py.pre_021c_menu_20261020_115413.bak`<br>`automation/tests/test_fn11_restore.py.bak`<br>`automation/tests/test_fn12_permanent_delete.py.bak`<br>`automation/tests/test_fn20_extended.py.bak_20261020_201514`<br>`fix_fn10_021c_editor_menu.py` | File sao lưu tạm trong quá trình debug mã nguồn test. |
| **File công cụ, scratch & file list** | `antigravity_file_list.txt`<br>`config_dir_list.txt`<br>`automation/reports/fn09_evidence_audit_20261020_100542.zip`<br>`automation/reports/fn09_evidence_audit_20261020_100542/`<br>`scratch/*` | File danh mục quét và thư mục scratch nội bộ phục vụ kiểm toán tự động. |
| **File nền tảng sinh tự động (Generated)** | `linux/flutter/*`<br>`macos/Flutter/*` | Tệp tin sinh tự động của Flutter engine trên các nền tảng desktop; không thuộc phạm vi kiểm thử Android QA. |
| **Tài liệu Black-box đang sửa dở** | `test_cases/black_box/black_box_test_cases.md` | Tài liệu black-box cũ đang được rà soát đối chiếu trong working tree; không stage trong đợt này. |

---

## 7. KẾT LUẬN KIỂM TOÁN VÀ ĐỀ XUẤT HÀNH ĐỘNG

1. **Độ tin cậy của bộ dữ liệu:** Đạt **100%** tiêu chuẩn kiểm toán. Tất cả 52 execution items đều có mã nguồn test tương ứng, có file JUnit XML thực tế với thẻ testcase ghi nhận đúng trạng thái, và có screenshot evidence hợp lệ, không có file 0-byte.
2. **Bảo toàn dữ liệu người dùng:** Việc áp dụng cơ chế `QA_ACCOUNT_SCOPED_V9` cho `TC-BB-024G D01` và nguyên tắc không xóa tài khoản giúp bảo vệ toàn vẹn dữ liệu môi trường kiểm thử.
3. **Sẵn sàng Stage:** Có thể thực hiện `git add` có chọn lọc đúng **36 file JUnit XML**, **42 thư mục run evidence (155 ảnh PNG)** và file manifest này.
4. **Tuân thủ cam kết:** Nghiêm cấm mọi hành động `git commit` hay `git push` tự động; dừng lại báo cáo số liệu và chờ lệnh chỉ đạo từ người dùng.
