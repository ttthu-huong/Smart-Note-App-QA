# BÁO CÁO CHỐT GIAI ĐOẠN 4 — FN-20: GHIM / BỎ GHIM GHI CHÚ

**Dự án:** Smart-Note-App-QA
**Nhánh làm việc:** `huong`
**Ngày chốt kết quả:** 20/10/2026
**Kỹ thuật:** UI/E2E — pytest + Python 3.13 + uiautomator2 + ADB
**Thiết bị:** Samsung Galaxy S21 FE 5G, Android 14 (API 34)
**Phạm vi:** 15 execution items automation FN-20; không bao gồm kiểm thử Provider, black-box manual hay các chức năng FN khác.

## 1. Kết quả cuối cùng

| Chỉ số | Kết quả |
|---|---:|
| Execution items trong phạm vi | 15 |
| PASS cuối cùng | **15** |
| FAIL ứng dụng được xác nhận | **0** |
| BLOCKED/NOT RUN cuối cùng | **0** |
| Tỷ lệ PASS trong phạm vi | **100%** |

**Quy tắc đếm:** Đây là kết quả **tổng hợp từ nhiều lượt chạy có mục tiêu**, không phải 15 ca PASS trong một lần chạy lại toàn bộ suite. Các lần FAIL-AUTO trước đó được giữ trong lịch sử thực thi nhưng không cộng thành các ca FAIL nghiệp vụ cuối cùng. Baseline cũ `TC-BB-024 D01` và `TC-BB-025 D01` chỉ tính một lần; không cộng thêm vào 13 ca mở rộng.

## 2. Danh sách 15 execution items và báo cáo bằng chứng

| # | TC / Data set | Nội dung | Kết quả cuối | JUnit minh chứng |
|---:|---|---|---|---|
| 1 | TC-BB-024 D01 | Ghim ghi chú từ Home | PASS | `automation/reports/fn20_pin_note_junit.xml` |
| 2 | TC-BB-025 D01 | Bỏ ghim ghi chú từ Home | PASS | `automation/reports/fn20_pin_note_junit.xml` |
| 3 | TC-BB-024B D01 | Ghim trong Editor | PASS | `automation/reports/fn20_editor_20261020_191551.xml` — đối chiếu theo testcase; file này có retry lịch sử |
| 4 | TC-BB-024B D02 | Bỏ ghim trong Editor | PASS | `automation/reports/fn20_024b_d02_retry2_20261020_195008.xml` |
| 5 | TC-BB-024C D01 | Kiểm tra ghi chú rỗng trong Editor | PASS | `automation/reports/fn20_024c_d01_20261020_195609.xml` |
| 6 | TC-BB-024D D01 | Ghim hàng loạt | PASS | `automation/reports/fn20_batch_20261020_190742.xml` |
| 7 | TC-BB-024H D01 | Chuyển ghim/bỏ ghim hỗn hợp | PASS | `automation/reports/fn20_batch_20261020_190742.xml` |
| 8 | TC-BB-025D D01 | Bỏ ghim hàng loạt | PASS | `automation/reports/fn20_batch_20261020_190742.xml` |
| 9 | TC-BB-025E D01 | Bỏ ghim một ghi chú trong nhiều ghi chú ghim | PASS | `automation/reports/fn20_batch_20261020_190742.xml` |
| 10 | TC-BB-024E D01 | Bố cục hai nhóm: Được ghim / Khác | PASS | `automation/reports/fn20_024e_v7_20261020_205408.xml` |
| 11 | TC-BB-024F D01 | Toàn vẹn nội dung qua chu trình pin/unpin | PASS | `automation/reports/fn20_024f_20261020_205909.xml` |
| 12 | TC-BB-024G D01 | Tất cả ghi chú đều được ghim (tài khoản QA mới) | PASS | `automation/reports/fn20_024g_v9_20261020_221313.xml` |
| 13 | TC-BB-025B D01 | Lưu trạng thái pinned qua restart | PASS | `automation/reports/fn20_025b_v8_20261020_211941.xml` |
| 14 | TC-BB-025C D01 | Sửa nội dung vẫn giữ trạng thái pinned | PASS | `automation/reports/fn20_025c_20261020_213027.xml` |
| 15 | TC-BB-025F D01 | Lưu trạng thái normal qua restart | PASS | `automation/reports/fn20_025f_20261020_215211.xml` |

**Thư mục ảnh chính:** `evidence/fn20/` (ảnh lưu theo từng `run_<timestamp>_<marker>/TC-BB-.../`, bên cạnh evidence baseline).
**Mã nguồn thực thi:** `automation/tests/test_fn20_pin_note.py` (2 baseline) và `automation/tests/test_fn20_extended.py` (13 mở rộng).
**Lưu ý kiểm toán:** Một vài test từng dừng vì cuộn viewport, locator hoặc nhận diện SystemUI; các bản cuối đã xử lý và ca liên quan được chạy lại có JUnit PASS. Giữ lịch sử retry để truy vết, không xóa evidence.

## 3. Môi trường và an toàn dữ liệu

- Phần lớn các ca chạy trên tài khoản kiểm thử hiện tại trên máy thật, theo điều kiện dữ liệu từng bài.
- **TC-BB-024G** chạy bằng **tài khoản QA mới** với đúng 3 ghi chú được tạo riêng, xác minh đồng thời SQLite theo `user_id` và UI quét hết danh sách. Không sử dụng reset ứng dụng hoặc `pm clear`.
- Không xóa và không ghim hàng loạt dữ liệu tài khoản cũ để dựng điều kiện All Pinned.
- Dữ liệu QA và các lần thử trước vẫn được giữ; cần phân biệt dữ liệu tiền điều kiện theo user khi kiểm thử các FN tiếp theo.

## 4. Kết luận và giới hạn

**FN-20 hoàn thành 15/15 execution items của phạm vi UI automation đã hoạch định, PASS 100%.** Kết quả này không có nghĩa toàn bộ 44 chức năng, mọi biến thể của FN-20, hoặc toàn bộ hệ thống không có lỗi. Hai bài Provider `PV-REF-01/02` là tầng kiểm thử độc lập, không cộng vào mẫu số 15 ca UI.

Đây là bản chốt **dựa trên các log pytest/JUnit và đường dẫn evidence do người thực thi báo cáo**. Trước khi push báo cáo cuối, cần kiểm tra lại file JUnit/ảnh vật lý trên máy Windows vì chưa được truy cập trực tiếp trong phiên làm việc này.

## 5. Các vị trí tài liệu phải đồng bộ

- `docs/qa/automation_execution_summary.md`: thêm mục kết quả **Phase 4 FN-20 mở rộng 15/15**; giữ nguyên các số liệu baseline lịch sử nếu đang dùng chúng làm mốc.
- `docs/qa/automation_status.md`: FN-20 có 2 baseline + 13 extended = 15 items PASS, không còn item FN-20 BLOCKED.
- `docs/qa/automation_test_cases.md`: bổ sung các mã `TC-BB-024B/024C/024D/024E/024F/024G/024H/025B/025C/025D/025E/025F` cùng biến thể D01/D02, trạng thái và bằng chứng theo bảng mục 2.
- `docs/plan_and_requirements/requirements_traceability_matrix.md`: REQ-07 liên kết 15 items FN-20, UI automation 15 PASS; không trộn 15 black-box manual với 15 UI automation.
- Chỉ điều chỉnh số liệu **tổng automation toàn hệ thống** khi đã tái kiểm kê toàn bộ Phase 2, Phase 3 và FN-20 và loại trừ trùng lặp IDs.

## 6. Giai đoạn kế tiếp

**Phase 5 — FN-23 Search & Filter:** audit bản đặc tả `FN-23`, dữ liệu tìm kiếm, JUnit baseline, màn hình Search hiện tại và dữ liệu theo tài khoản. Vì tài khoản QA mới đang có 3 ghi chú pinned, phải seed dataset phù hợp trước khi test điều kiện lọc hoặc quay lại tài khoản ban đầu một cách có kiểm soát. Chỉ kiểm thử những ca có Expected/Preconditions rõ, tạo evidence và giữ nguyên các vấn đề đã ghi nhận như tìm không dấu `BR-01` và `has:list` `BUG-004`.
