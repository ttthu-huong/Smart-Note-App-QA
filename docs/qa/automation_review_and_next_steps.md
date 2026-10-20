# RÀ SOÁT VÀ KẾ HOẠCH HOÀN THIỆN KIỂM THỬ TỰ ĐỘNG

**Dự án:** Smart Note App · **Nhánh:** huong · **Ngày:** 19/10/2026 (UTC+7)
**Nguồn đối chiếu:** commit `98abb5af577b2d38192e7a88e7ff94a2b5f77262`.

> **Phạm vi mở rộng cũng đang được quản lý:** Ngoài baseline 31 TC UI, hồ sơ Phase 3C chọn 61 TC/74 executions; Phase 4 báo cáo 14 TC/20 executions (19 PASS, 1 FAIL-APP) cùng 3 ca thăm dò riêng. Có report/script/ảnh nhưng chưa đối chiếu được XML/log cho các lượt mở rộng. TC-BB-006 được Phase 4 báo cáo PASS sau khi chuẩn bị lại tài khoản, khác FAIL trong XML baseline. Giữ hai nguồn, không cộng trùng hoặc bỏ qua kết quả được báo cáo. Xem [ma trận mở rộng và nguồn](automation_expanded_scope.md).


## 1. Phạm vi đợt hoàn thiện tài liệu

Đối chiếu và hoàn thiện riêng kế hoạch, đặc tả TC, trạng thái, báo cáo thực thi và hướng dẫn kiểm thử tự động. Không thay đổi kết quả XML, ảnh, mã ứng dụng, script test hoặc Expected để làm tăng tỷ lệ PASS; không chạy ứng dụng/Provider mới và chưa push GitHub.

| Việc rà soát | Kết quả |
| --- | --- |
| Nguồn nhánh | Đã đối chiếu HEAD với origin/huong tại thời điểm bắt đầu |
| 9 JUnit XML | 24 bản ghi, 23 TC duy nhất, 19 PASS/4 FAIL |
| TC-BB-022 | TC-BB-022 được ghi nhận hai lượt chạy, cả hai PASS, nhưng chỉ tính một test case duy nhất. Bộ XML baseline có 24 lượt chạy, tương ứng 23 test case duy nhất: 19 PASS, 4 FAIL. |
| Provider | Có 15 + 9 khai báo; đã đối chiếu log cục bộ trên máy (automated_test_run.log, 24 PASS, ngày 12/10) |
| Script hiện tại | Có biến thể và alias ngoài 23 node đã có XML; lập kiểm kê riêng |
| Thông tin môi trường | Docstring và report lịch sử có OS/model khác nhau; cần đo lại cho lượt mới |

## 2. Nội dung đã chỉnh

- [Plan](automation_plan.md): viết rõ mục tiêu, lựa chọn TC, phạm vi hai tầng, danh mục 44 FN, điều kiện vào/dừng/ra, dữ liệu, phân công và thứ tự triển khai tiếp.
- [Test cases](automation_test_cases.md): giữ bảng chi tiết 31 TC UI và các Ref Provider, cập nhật 23 UI có XML/8 deferred; tách trạng thái mã khỏi kết quả và mức xác minh.
- [Execution summary](automation_execution_summary.md): tách kết quả XML xác minh được và 24 PASS Provider theo lịch sử; giữ Expected/Actual và phân tích 4 FAIL.
- [Status](automation_status.md): thống nhất tiến độ, bỏ việc gọi mọi FN có test là hoàn toàn thành công.
- [Script inventory](automation_script_inventory.md): liệt kê node ID từ mã nguồn, XML tương ứng và alias/biến thể chưa xác minh thực thi.
- [README thực thi](../../automation/README.md): hướng dẫn chọn node ID và lưu bằng chứng trước lượt mới.

Đã sửa 4 thành 7 FN có mã ở cả UI và Provider; sửa `moveToTrash` thành `deleteNote` theo lời gọi thực tế trong Provider test; mô tả PV-REF-15 là trở về status `normal` thay vì khẳng định phục hồi ghim. Thời gian testcase ở các bảng đối chiếu lấy từ XML, không dùng số thời gian khác trong report cũ làm kết quả đo mới.

## 3. Kế hoạch công việc tiếp theo

Đây là thứ tự thực hiện đề xuất, không ghi ngày chạy hoặc kết quả trước khi có bằng chứng.

| Thứ tự | Công việc | Tiền điều kiện | Thực hiện | Tiêu chí hoàn thành | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| 1 | Khôi phục 3 script FN-10, FN-11, FN-12 | Lấy từ `git show HEAD:automation/tests/...` (dùng `QANoteHelper`) | Khôi phục mã kiểm thử cho 3 file `test_fn10_trash.py`, `test_fn11_restore.py`, `test_fn12_permanent_delete.py` | Script có đầy đủ mã, sẵn sàng cho các đợt rerun tiếp theo | ĐÃ HOÀN TẤT khôi phục từ Git HEAD; chưa rerun |
| 2 | Xác minh retest TC-BB-006 | Phase 4 đã báo cáo PASS; cần log/XML độc lập lượt đó, tài khoản đã verify, đúng build | Khôi phục log/XML Phase 4; nếu thiếu, kiểm tra tài khoản rồi chọn node và chạy mới | Có kết quả lượt mới với run ID độc lập; không ghi đè FAIL baseline cũ | Đã có report PASS; chưa xác minh log/XML |
| 3 | Chốt Expected TC-BB-007/008 | Người phụ trách yêu cầu xem Expected/Actual | Xác nhận thông báo riêng hay gộp và ghi quyết định (phân biệt mã `BUG-BB-002/003` với `BUG-002/003`) | Nếu đổi yêu cầu thì version đặc tả/assertion trước lần chạy tiếp; giữ lịch sử | Chờ xác nhận yêu cầu |
| 4 | Retest TC-BB-003 | Hồ sơ lỗi có ánh xạ, build đã sửa | Chạy email thiếu @; kiểm tra regression email hợp lệ và domain rác | XML/ảnh mới và kết luận theo Expected được duyệt | Chờ bản sửa |
| 5 | Chuẩn hóa script mở rộng | Đã chọn TC/dataset và node chính | Rà alias/biến thể, đối chiếu assertion với hộp đen; sau đó mới chạy | Một node chính cho mỗi TC/dataset; có evidence khi thêm vào baseline | Đã kiểm kê, chưa chạy |
| 6 | Bổ sung JUnit XML Provider (tùy chọn CI) | Log console máy `automated_test_run.log` đã xác nhận 24 PASS (không bắt buộc JUnit XML) | Cấu hình runner xuất thêm file XML/JSON khi tích hợp CI/CD tự động | File XML/JSON lưu vào artifacts CI; không chạy lại test chỉ để đổi format | Đã có log console 24 PASS; XML là tùy chọn CI |
| 7 | Mở rộng 8 ca deferred | Đạt các điều kiện ở mục 4 | Thực hiện từng nhóm độc lập | Có script, tiền điều kiện, assertion và report; không yêu cầu mở hết cùng lúc | Tạm hoãn |

Kết quả FAIL/BLOCKED của lượt mới vẫn là kết quả hợp lệ để báo cáo. Không yêu cầu tất cả PASS bằng cách nới assertion. Thay đổi Expected cần dựa trên quyết định yêu cầu, không chỉ vì ứng dụng đang trả kết quả khác.

## 4. Điều kiện mở lại 8 ca UI tạm hoãn

| TC | Phụ thuộc hiện tại | Điều kiện để triển khai tiếp |
| --- | --- | --- |
| 010, 011 | Google OAuth/system dialog | Tài khoản QA, khả năng điều khiển chọn/hủy tài khoản ổn định, không tác động tài khoản cá nhân |
| 012 | Bật khóa sinh trắc học | Môi trường biometric kiểm soát được; không xóa vân tay của người dùng |
| 013, 014, 015 | Xác thực đúng/sai/hủy biometric | Cách tạo kết quả xác thực và quan sát trạng thái bảo vệ; tách giả lập khỏi kết quả máy thật |
| 030 | Offline rồi online | Điều phối mạng và trạng thái sync; đối chiếu cloud hoặc máy thứ hai, không chỉ cờ local |
| 031 | LWW giữa hai thiết bị | Hai máy cùng dữ liệu QA, điều phối thời điểm sửa khác nhau và kết nối lại; trường hợp timestamp bằng nhau chờ BR-03 |

Các ca này có thể tự động hóa khi đủ môi trường; không gọi là “không thể tự động hóa”. Kết quả Provider không thay thế bằng chứng UI/Firestore thật của 030/031.

## 5. Những mục ngoài bộ tài liệu tự động cần nhóm xử lý riêng

- Master Test Plan còn số liệu 20 UI/44 tổng của baseline cũ. Dùng báo cáo tự động phiên bản này khi tổng hợp, rồi đồng bộ tài liệu tổng thể ở tác vụ riêng.
- Đặc tả hộp đen, báo cáo hộp đen và Defect Log có bất nhất mã/mô tả BUG-BB-002/003; trong bộ tự động dùng TC-ID làm khóa và giữ nhãn cũ để truy vết.
- Chưa có hồ sơ riêng cho các nhãn BUG-FN02-01, BUG-BB-002, BUG-BB-003 tại Defect Log hiện hành; không tự thêm ba lỗi sản phẩm đã xác nhận vào tổng.
- Testing_Report.md là bản tổng thể cũ, cần biên soạn lại theo số liệu đã đối chiếu trước khi nộp.

## 6. Cách dùng bộ tài liệu để viết báo cáo và thuyết trình

Đọc lần lượt Plan → Test Case của một FN → Script/Node ID → Execution Summary → Next Steps. Khi trình bày, giải thích rõ vì sao chọn TC, script kiểm tra điều gì và bằng chứng hỗ trợ kết luận đến đâu.

Có thể dùng nội dung sau làm cơ sở cho phần kết quả: “Bộ kiểm thử UI đã lưu kết quả của 23 test case duy nhất, gồm 19 PASS và 4 FAIL. Bốn ca thất bại được phân tích thành vấn đề validation, tiền điều kiện tài khoản và khác biệt Expected cần xác nhận. Bộ Provider có 24 bài test trong mã nguồn; log lịch sử `automated_test_run.log` xác nhận 24 PASS (chưa xác minh chính xác commit thực thi, không coi thiếu JUnit XML là thiếu bắt buộc). Tám ca UI trong baseline được tạm hoãn; hồ sơ mở rộng còn ghi nhận các lần thăm dò OAuth/sinh trắc học và tiến độ 14/61 AT, cần giữ riêng số liệu theo phạm vi.”

## 7. Bàn giao và áp dụng

Các file được chỉnh tại checkout cục bộ. Xem diff trước khi đưa vào nhánh làm việc; không dùng tài liệu rà soát như bằng chứng chạy test mới. Các file XML/script và report gốc vẫn là nguồn độc lập để đối chiếu.

## 8. Hồ sơ mở rộng đã đối chiếu bổ sung

Giữ nguyên kết quả Phase 3C/4, thêm chỉ dẫn phạm vi và [ma trận 61 AT](automation_expanded_scope.md). TC-BB-006 không còn được mô tả là chưa từng retest; Phase 4 có report PASS nhưng cần log/XML độc lập để đối chiếu. Kiểm tra tồn tại toàn bộ đường dẫn ảnh của 20 executions chính thức và 3 ca thăm dò, chưa thay thế việc xác minh assertion của lượt đó.
