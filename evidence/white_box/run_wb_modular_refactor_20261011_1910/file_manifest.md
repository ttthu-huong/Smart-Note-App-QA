# Báo Cáo Tái Cấu Trúc Module Test & File Manifest

**Dự án:** Smart-Note-App-QA  
**Branch:** `huong`  
**Thời gian thực hiện:** 2026-10-11 19:10  
**Mục tiêu:** Tổ chức lại toàn bộ file kiểm thử trong `test/` theo module chuẩn hóa, loại bỏ duplicate lặp lại, bảo toàn 100% giá trị kiểm thử bao gồm 4 bài defect test FAIL, và giữ nguyên tuyệt đối production code (`lib/`).

---

## 1. Bảng Ánh Xạ Đường Dẫn Cũ ➔ Mới (Old-to-New Mapping)

| # | Đường dẫn gốc trước refactor | Đường dẫn đích sau refactor | Loại thao tác | Số Group | Số Test | Trạng thái thực thi |
|---|-----------------------------|----------------------------|---------------|----------|---------|---------------------|
| 1 | `test/white_box_p1_p2_test.dart` (phần Note Model & SUPP) | `test/unit/note/note_model_whitebox_test.dart` | Tách file (Split) | 8 | 19 | 19 PASS / 0 FAIL |
| 2 | `test/white_box_p1_p2_test.dart` (phần Checklist UUID) | `test/unit/note/checklist_whitebox_test.dart` | Tách file (Split) | 2 | 1 | 1 PASS / 0 FAIL |
| 3 | `test/white_box_p1_p2_test.dart` (phần LWW Reference) | `test/unit/sync/lww_timestamp_reference_test.dart` | Tách file (Split) | 2 | 3 | 3 PASS / 0 FAIL |
| 4 | `test/white_box_p1_p2_test.dart` (phần Cloudinary Guards) | `test/unit/services/cloudinary_whitebox_test.dart` | Tách file (Split) | 3 | 2 | 2 PASS / 0 FAIL |
| 5 | `test/deep_whitebox_defect_test.dart` (phần Defect Discovery) | `test/unit/note/note_parsing_defect_test.dart` | Tách file (Split) | 1 | 5 | 1 PASS / 4 FAIL (bảo toàn) |
| 6 | `test/deep_whitebox_defect_test.dart` (phần Dung Benchmarks) | `test/performance/perf_micro_test.dart` | Tách file (Split) | 1 | 2 | 2 PASS / 0 FAIL |
| 7 | `test/note_model_test.dart` | `test/unit/note/note_model_test.dart` | Di chuyển (Relocate) | 1 | 9 | 9 PASS / 0 FAIL |
| 8 | `test/checklist_copy_with_test.dart` | `test/unit/note/checklist_copy_with_test.dart` | Di chuyển (Relocate) | 1 | 4 | 4 PASS / 0 FAIL |
| 9 | `test/checklist_test.dart` / `test/unit/checklist_model_test.dart` | `test/unit/note/checklist_model_test.dart` | Chuẩn hóa & Khử Duplicate | 2 | 5 | 5 PASS / 0 FAIL |
| 10 | `test/auth_provider_test.dart` / `test/unit/auth_validation_test.dart` | `test/unit/auth/auth_provider_test.dart` | Chuẩn hóa & Khử Duplicate | 4 | 15 | 15 PASS / 0 FAIL |
| 11 | `test/security_rules_test.dart` | `test/security/security_rules_test.dart` | Di chuyển (Relocate) | 4 | 15 | 15 PASS / 0 FAIL |
| 12 | `test/widget_test.dart` / `test/widget/empty_state_widget_test.dart` | `test/widget/empty_state_widget_test.dart` | Khử Duplicate (giữ bản trong `test/widget/`) | 0 | 1 | 1 PASS / 0 FAIL |

---

## 2. Kiểm Kê Mã Hash & Dung Lượng File Sau Khi Tái Cấu Trúc

| File đích | Dung lượng (bytes) | MD5 Checksum | Số Group | Số Test |
|-----------|--------------------|--------------|----------|---------|
| `test/performance/perf_micro_test.dart` | 2,226 | `4CACAC7618A52CA846785303A2E5C7C4` | 1 | 2 |
| `test/security/security_rules_test.dart` | 5,925 | `9095A94AD8D32F1D45855929E56590B6` | 4 | 15 |
| `test/unit/auth/auth_provider_test.dart` | 5,535 | `1596E112FE25E14B5BE6EA4FDA60F8DD` | 4 | 15 |
| `test/unit/note/checklist_copy_with_test.dart` | 2,201 | `00FEFCF77BCB45411A5915B97C6279E6` | 1 | 4 |
| `test/unit/note/checklist_model_test.dart` | 2,308 | `584CF7C4F669AFC8D649D0B754ACBFF7` | 2 | 5 |
| `test/unit/note/checklist_whitebox_test.dart` | 1,836 | `4408BF5D585155728306BE59E24239A9` | 2 | 1 |
| `test/unit/note/note_model_test.dart` | 8,140 | `3B316906B2472B046A991B407E9BA6F9` | 1 | 9 |
| `test/unit/note/note_model_whitebox_test.dart` | 16,373 | `36D21C97B7C8A07D3FD914D819B51741` | 8 | 19 |
| `test/unit/note/note_parsing_defect_test.dart` | 4,167 | `0DF4825AC9D9F7331AE35CA4B466DDD3` | 1 | 5 |
| `test/unit/services/cloudinary_whitebox_test.dart` | 2,518 | `DB3CDCFFCFEDF921877484F3EAB5EFBF` | 3 | 2 |
| `test/unit/sync/lww_timestamp_reference_test.dart` | 3,113 | `340934378596C6F51A7B1BEDF8D1421C` | 2 | 3 |
| `test/widget/empty_state_widget_test.dart` | 1,347 | `F8165D6099823106653BB4EACCB59DBC` | 0 | 1 |
| **TỔNG CỘNG** | **55,689** | — | **29** | **81** |

---

## 3. Xác Minh Khử Trùng Lặp (Deduplication Verification)

Ba cặp file duplicate đã được kiểm tra hash byte-for-byte và khử trùng lặp chính xác:
1. `test/auth_provider_test.dart` và `test/unit/auth_validation_test.dart` (MD5: `1596E112FE25E14B5BE6EA4FDA60F8DD`):
   - Giữ lại 1 bản duy nhất tại `test/unit/auth/auth_provider_test.dart`.
2. `test/checklist_test.dart` và `test/unit/checklist_model_test.dart` (MD5: `584CF7C4F669AFC8D649D0B754ACBFF7`):
   - Giữ lại 1 bản duy nhất tại `test/unit/note/checklist_model_test.dart`.
3. `test/widget_test.dart` và `test/widget/empty_state_widget_test.dart` (MD5: `57304cf587b0ec4a7fae42d3cd81d9fd`):
   - Giữ lại 1 bản duy nhất tại `test/widget/empty_state_widget_test.dart`.

Không còn bất kỳ file kiểm thử nào tồn tại ở thư mục gốc `test/`.

---

## 4. Kết Quả Thực Thi Theo Nhóm (Test Execution by Category)

1. **Baseline Model Suite:**
   - Files: `test/unit/note/note_model_test.dart`, `test/unit/note/checklist_model_test.dart`, `test/unit/note/checklist_copy_with_test.dart`, `test/unit/auth/auth_provider_test.dart`
   - Kết quả: **33/33 PASS (100%)**
2. **Selective White-box Suite:**
   - Files: `test/unit/note/note_model_whitebox_test.dart`, `test/unit/note/checklist_whitebox_test.dart`, `test/unit/sync/lww_timestamp_reference_test.dart`, `test/unit/services/cloudinary_whitebox_test.dart`
   - Kết quả: **25/25 PASS (100%)**
3. **Deep Defect-driven White-box Suite:**
   - File: `test/unit/note/note_parsing_defect_test.dart`
   - Kết quả: **1 PASS, 4 FAIL** (giữ nguyên trọn vẹn 4 defect test đã phát hiện: DEFECT-WB-01, DEFECT-WB-02, DEFECT-WB-03, DEFECT-WB-04)
4. **Security Simulation Suite:**
   - File: `test/security/security_rules_test.dart`
   - Kết quả: **15/15 PASS (100%)**
5. **Performance Micro-benchmarks Suite:**
   - File: `test/performance/perf_micro_test.dart`
   - Kết quả: **2/2 PASS (100%)**
6. **Widget Test Suite:**
   - File: `test/widget/empty_state_widget_test.dart`
   - Kết quả: **1/1 PASS (100%)**

**Tổng thể Suite Toàn Bộ Dự Án:**
- **77 PASS**
- **4 FAIL (Bảo toàn 100% bug detection)**
- **0 Compile Errors**
- **0 Flaky Tests**
- **Tổng cộng: 81 tests thực thi duy nhất**

---

## 5. Đối Chiếu Độ Bao Phủ Mã (LCOV Coverage Comparison)

So sánh giữa kết quả chạy trước khi refactor (`run_wb_deep_defect_20261011_1845`) và sau khi refactor (`run_wb_modular_refactor_20261011_1910`):

| Production File | Lines Hit (LH) | Lines Found (LF) | Line Coverage (%) | So với trước refactor |
|-----------------|----------------|------------------|-------------------|----------------------|
| `lib/models/note_model.dart` | 105 | 124 | **84.68%** | Không đổi (105/124) |
| `lib/models/checklist_item.dart` | 14 | 14 | **100.00%** | Không đổi (14/14) |
| `lib/services/cloudinary_service.dart` | 16 | 81 | **19.75%** | Không đổi (16/81) |
| `lib/widgets/empty_state.dart` | 44 | 44 | **100.00%** | Không đổi (44/44) |
| `lib/core/design/app_colors.dart` | 5 | 72 | **6.94%** | Không đổi (5/72) |

---

## 6. Tuân Thủ Quy Tắc Bảo Toàn

- [x] Không sửa đổi bất kỳ dòng code nào trong `lib/`.
- [x] Không sửa đổi cấu hình `pubspec.yaml`, Firebase hay DI.
- [x] Giữ nguyên 4 test FAIL (`DEFECT-WB-01..04`), không thay đổi Expected Result.
- [x] Không thêm test mới ngoài phạm vi phê duyệt.
- [x] Không tạo trùng test để tăng số lượng ảo.
- [x] Tất cả các thư mục phụ trợ `fixtures/`, `helpers/`, `mocks/`, `random_fuzz/` được giữ nguyên vẹn.
- [x] Không ghi đè các thư mục evidence lịch sử.
