# TIẾN ĐỘ KIỂM THỬ TỰ ĐỘNG

**Dự án:** Smart Note App · **Nhánh:** `huong` · **Phiên bản:** 1.1 · **Ngày rà soát:** 19/10/2026 (UTC+7)
**Mã nguồn và bằng chứng được đối chiếu:** `98abb5af577b2d38192e7a88e7ff94a2b5f77262`. Đây là cập nhật tài liệu; không có lượt chạy ứng dụng mới.

**Repository:** `ttthu-huong/Smart-Note-App-QA`.

> **Phạm vi mở rộng cũng đang được quản lý:** Ngoài baseline 31 TC UI, hồ sơ Phase 3C chọn 61 TC/74 executions; Phase 4 báo cáo 14 TC/20 executions (19 PASS, 1 FAIL-APP) cùng 3 ca thăm dò riêng. Có report/script/ảnh nhưng chưa đối chiếu được XML/log cho các lượt mở rộng. TC-BB-006 được Phase 4 báo cáo PASS sau khi chuẩn bị lại tài khoản, khác FAIL trong XML baseline. Giữ hai nguồn, không cộng trùng hoặc bỏ qua kết quả được báo cáo. Xem [ma trận mở rộng và nguồn](automation_expanded_scope.md).


## 1. Trạng thái hiện hành

| Hạng mục | Đã xác minh | Còn lại/giới hạn |
| --- | --- | --- |
| UI/E2E baseline | 23/31 TC có XML: 19 PASS, 4 FAIL | 8 TC DEFERRED; 74.19% tập ứng viên có kết quả |
| Bản ghi thực thi UI | 24 testcase records trong 9 XML | TC-BB-022 có 2 bản ghi, tính 1 TC duy nhất |
| Provider | Có mã 24 tests (15 + 9) | Log lịch sử xác nhận 24 PASS; chưa xác minh chính xác commit thực thi |
| Tổng lịch sử hai tầng | 47 tests (23 UI + 24 Provider), 43 PASS/4 FAIL | 91.49% theo kết quả đã có minh chứng (9 XML UI + console log máy) |
| Script mở rộng/alias | Đã có kiểm kê mã nguồn | Chưa có XML tương ứng; không cộng vào 23 TC đã thực thi |

Tỷ lệ PASS đã xác minh UI: 19/23 = 82.61%. Tỷ lệ PASS Provider: 24/24 = 100% (theo log lịch sử `automated_test_run.log`). Tổng hai tầng: 43/47 = 91.49%. Không coi việc thiếu JUnit XML của Provider là thiếu sót bắt buộc nếu đã có log đầy đủ.

*Lưu ý về working tree:* Hiện 3 script `test_fn10_trash.py` (0 bytes), `test_fn11_restore.py` (0 bytes) và `test_fn12_permanent_delete.py` (1 byte) đang bị rỗng do thay đổi cục bộ có từ trước (kèm file `.bak`); kết quả 3 XML là lịch sử của phiên bản trước; khả năng chạy lại hiện bị ảnh hưởng nếu chưa khôi phục mã.

## 2. UI theo nhóm

| FN | Số TC duy nhất | PASS | FAIL |
| --- | ---: | ---: | ---: |
| FN-02 | 5 | 4 | 1 |
| FN-04 | 4 | 1 | 3 |
| FN-08 | 3 | 3 | 0 |
| FN-09 | 2 | 2 | 0 |
| FN-10 | 1 | 1 | 0 |
| FN-11 | 1 | 1 | 0 |
| FN-12 | 1 | 1 | 0 |
| FN-20 | 2 | 2 | 0 |
| FN-23 | 4 | 4 | 0 |
| Tổng | 23 | 19 | 4 |

## 3. Việc đang mở

| Ưu tiên | Việc | Trạng thái |
| --- | --- | --- |
| 1 | Khôi phục 3 script FN-10, FN-11, FN-12 từ file `.bak` hoặc Git HEAD | Script working tree bị rỗng; cần khôi phục trước khi chạy lại |
| 2 | Đối chiếu retest TC-BB-006 được Phase 4 báo cáo PASS; chạy mới nếu không khôi phục được log | Chờ log/XML lượt retest Phase 4; nếu chạy mới cần gate tiền điều kiện |
| 3 | Xác nhận Expected thông báo TC-BB-007/008 | Chờ quyết định yêu cầu; giữ FAIL lịch sử (mã BUG-BB-002/003 khác với BUG-002/003) |
| 4 | Retest TC-BB-003 sau khi có build sửa validation | Chờ build và hồ sơ lỗi chính thức |
| 5 | Chọn node ID, xử lý alias trước mở rộng | Đã kiểm kê; chưa sửa script/chạy mới |
| 6 | Triển khai 8 ca tạm hoãn | Chờ môi trường phù hợp |

Các mã nhãn cũ chưa có hồ sơ riêng trong Defect Log không tự trở thành lỗi sản phẩm đã xác nhận. Phân loại 4 FAIL: 1 sai khác validation, 1 vấn đề tiền điều kiện, 2 Expected cần xác nhận.

## 4. Phạm vi FN

9 FN có XML UI: 02, 04, 08, 09, 10, 11, 12, 20, 23. Provider có mã liên kết 10 FN (đã đối chiếu log máy `automated_test_run.log` gồm 24 PASS; chưa xác minh chính xác commit thực thi); hợp hai tầng là 12 FN (thêm 13, 14, 40 ở tầng Provider). 7 FN có mã ở cả hai tầng là 08, 09, 10, 11, 12, 20, 23. Không gọi 12 FN này là 12 chức năng hoàn toàn PASS toàn bộ ứng dụng.

Danh mục 44 FN và lý do chưa tự động hóa nằm trong [Plan](automation_plan.md). Bộ số liệu manual/white-box thuộc hồ sơ riêng, không cộng vào bảng này.

## 5. Tài liệu tra cứu

- [Kế hoạch](automation_plan.md)
- [Test cases](automation_test_cases.md)
- [Báo cáo thực thi](automation_execution_summary.md)
- [Node ID và script mở rộng](automation_script_inventory.md)
- [Rà soát và kế hoạch tiếp theo](automation_review_and_next_steps.md)
- [Hướng dẫn chạy và bảo toàn bằng chứng](../../automation/README.md)
