# BÁO CÁO THỰC THI KIỂM THỬ TỰ ĐỘNG

**Dự án:** Smart Note App · **Nhánh:** `huong` · **Phiên bản:** 1.1 · **Ngày rà soát:** 19/10/2026 (UTC+7)
**Mã nguồn và bằng chứng được đối chiếu:** `98abb5af577b2d38192e7a88e7ff94a2b5f77262`. Đây là cập nhật tài liệu; không có lượt chạy ứng dụng mới.

> **Phạm vi mở rộng cũng đang được quản lý:** Ngoài baseline 31 TC UI, hồ sơ Phase 3C chọn 61 TC/74 executions; Phase 4 báo cáo 14 TC/20 executions (19 PASS, 1 FAIL-APP) cùng 3 ca thăm dò riêng. Có report/script/ảnh nhưng chưa đối chiếu được XML/log cho các lượt mở rộng. TC-BB-006 được Phase 4 báo cáo PASS sau khi chuẩn bị lại tài khoản, khác FAIL trong XML baseline. Giữ hai nguồn, không cộng trùng hoặc bỏ qua kết quả được báo cáo. Xem [ma trận mở rộng và nguồn](automation_expanded_scope.md).


## 1. Kết quả và mức xác minh

| Chỉ số | UI/E2E | Provider |
| --- | --- | --- |
| Phạm vi thiết kế baseline | 31 TC | 24 khai báo test |
| Kết quả được đối chiếu đợt này | 23 TC duy nhất: 19 PASS, 4 FAIL, 0 ERROR | Log lịch sử xác nhận 24 PASS (0 FAIL) |
| Bản ghi trong bằng chứng hiện có | 24 bản ghi testcase trong 9 XML | Log `evidence/automated/automated_test_run.log` (7.700 bytes; chưa xác minh chính xác commit thực thi) |
| Tỷ lệ PASS đã xác minh | 19/23 = 82.61% | 24/24 = 100% (theo console log) |
| Tỷ lệ TC UI có XML trên tập ứng viên | 23/31 = 74.19% | Không áp dụng |
| Tạm hoãn baseline | 8 TC = 25.81% | Không suy diễn thành chưa từng chạy |
| Báo cáo lịch sử | Các report riêng theo FN | Lịch sử & log máy ghi 24/24 PASS |

Tổng **47 tests, 43 PASS/4 FAIL, 91.49%** là số liệu tổng hợp hai tầng (23 UI + 24 Provider). Trong đó: UI có 23 TC xác minh qua 9 XML (19 PASS/4 FAIL); Provider có log lịch sử `automated_test_run.log` xác nhận 24 PASS (0 FAIL), chưa xác minh chính xác commit thực thi. Không coi việc thiếu JUnit XML của Provider là thiếu bắt buộc vì file log console đã ghi nhận đầy đủ 24 test hoàn tất thành công. File log này trước đó bị bỏ qua do `.gitignore` chặn `*.log` và hiện đã được đưa vào danh sách commit của đợt này. Đợt rà soát này đối chiếu bằng chứng hiện hữu trên máy, không chạy test mới.

## 2. Nguồn và giới hạn bằng chứng

Đọc XML, kiểm kê Python bằng AST và kiểm kê khai báo Dart, đối chiếu các report Markdown. XML xác nhận trạng thái assertion của lượt lưu, không tự xác nhận APK đang cài được build từ commit nào. Một số timestamp XML không có offset; giữ nguyên giá trị từng file, bao gồm offset nếu có, không tự quy đổi múi giờ.

Model/OS trong tài liệu lịch sử và docstring chưa thống nhất; trước lượt mới cần đo bằng ADB. Report này không thay thế kết quả cũ hoặc tạo ảnh/log kiểm thử mới.

## 3. Đối chiếu 9 XML UI

| FN | XML | TC duy nhất | Bản ghi lượt chạy | PASS theo TC | FAIL theo TC | Timestamp XML nguyên bản |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| FN-02 | [fn02_register_junit.xml](../../automation/reports/fn02_register_junit.xml) | 5 | 5 | 4 | 1 | `2026-10-05T10:26:12.802821` |
| FN-04 | [fn04_login_junit.xml](../../automation/reports/fn04_login_junit.xml) | 4 | 4 | 1 | 3 | `2026-10-04T15:35:08.800067+07:00` |
| FN-08 | [fn08_create_note_junit.xml](../../automation/reports/fn08_create_note_junit.xml) | 3 | 3 | 3 | 0 | `2026-10-04T23:50:33.114072` |
| FN-09 | [fn09_edit_note_junit.xml](../../automation/reports/fn09_edit_note_junit.xml) | 2 | 2 | 2 | 0 | `2026-10-05T01:31:47.578978` |
| FN-10 | [fn10_trash_junit.xml](../../automation/reports/fn10_trash_junit.xml) | 1 | 1 | 1 | 0 | `2026-10-14T13:29:50.248085` |
| FN-11 | [fn11_restore_junit.xml](../../automation/reports/fn11_restore_junit.xml) | 1 | 2 | 1 | 0 | `2026-10-14T13:31:32.445993` |
| FN-12 | [fn12_permanent_delete_junit.xml](../../automation/reports/fn12_permanent_delete_junit.xml) | 1 | 1 | 1 | 0 | `2026-10-14T13:36:38.032461` |
| FN-20 | [fn20_pin_note_junit.xml](../../automation/reports/fn20_pin_note_junit.xml) | 2 | 2 | 2 | 0 | `2026-10-05T01:45:57.958114` |
| FN-23 | [fn23_search_junit.xml](../../automation/reports/fn23_search_junit.xml) | 4 | 4 | 4 | 0 | `2026-10-05T02:10:50.169065` |
| **Tổng** | **9 XML** | **23** | **24** | **19** | **4** | Không phải một lần chạy đồng thời |

TC-BB-022 có 2 bản ghi cùng classname/name, đều PASS. Chỉ khử trùng để tổng hợp TC duy nhất; giữ nguyên 2 lượt chạy. Không cộng số lượt chạy trước đó trong report Markdown vào bảng XML hiện hành.

Thời gian đọc trực tiếp từ thuộc tính `testcase.time` (khác tổng thời gian suite có setup/teardown):

| TC | Thời gian từng bản ghi XML |
| --- | --- |
| TC-BB-021 | 79.806s |
| TC-BB-022 | 92.371s, 91.686s |
| TC-BB-023 | 88.693s |

## 4. Chi tiết 23 TC UI theo báo cáo lịch sử

Bảng dưới giữ Expected/Actual và liên kết ảnh từ báo cáo cũ; kết quả PASS/FAIL được đối chiếu XML. Ảnh có tên cố định nên việc file còn tồn tại chưa chứng minh ảnh và XML cùng một lần chạy; cần run ID ở lượt tiếp theo.

| TC-ID | FN | Kịch bản | Expected | Actual theo report lịch sử | Kết quả XML | Phân loại/nhãn cũ | Ảnh được report dẫn |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **TC-BB-001** | FN-02 | Đăng ký tài khoản hợp lệ | Tạo tài khoản, chuyển `EmailVerificationScreen` | Tạo tài khoản, chuyển `EmailVerificationScreen` | **PASS** | — | `evidence/fn02/FN02_TC-BB-001_D01_01.png` |
| **TC-BB-002** | FN-02 | Để trống thông tin khi đăng ký | Chặn gửi; hiển thị yêu cầu nhập đủ thông tin | Chặn, báo *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | **PASS** | — | `evidence/fn02/FN02_TC-BB-002_D01_01.png` |
| **TC-BB-003** | FN-02 | Đăng ký với email thiếu `@` | Hiển thị lỗi định dạng email: *"Định dạng email không hợp lệ."* | Hiển thị: *"Không hỗ trợ tên miền email rác này..."* | **FAIL** | **Application Bug** (gán nhãn nội bộ: `BUG-FN02-01`) | `evidence/fn02/FN02_TC-BB-003_D01_01.png` |
| **TC-BB-004** | FN-02 | Đăng ký mật khẩu dưới 6 ký tự | Chặn gửi; báo mật khẩu phải có ít nhất 6 ký tự | Chặn mật khẩu 5 ký tự, báo cần tối thiểu 6 ký tự | **PASS** | — | `evidence/fn02/FN02_TC-BB-004_D02_01.png` |
| **TC-BB-005** | FN-02 | Đăng ký bằng email đã tồn tại | Không tạo trùng; báo email đã được sử dụng | Báo: *"Email này đã được sử dụng cho một tài khoản khác."* | **PASS** | — | `evidence/fn02/FN02_TC-BB-005_D01_01.png` |
| **TC-BB-006** | FN-04 | Đăng nhập tài khoản hợp lệ | Tài khoản đã xác thực chuyển vào `HomeScreen` | Chuyển `EmailVerificationScreen` do `emailVerified=false` | **FAIL** | **Precondition Issue** (Tài khoản chưa verify email) | `evidence/fn04/FN04_TC-BB-006_D01_01.png` |
| **TC-BB-007** | FN-04 | Đăng nhập sai Mật khẩu | Hiển thị lỗi riêng: *"Mật khẩu không chính xác."* | Báo: *"Email hoặc mật khẩu không chính xác."* (thông báo gộp) | **FAIL** | **Expected Diff / Firebase Unified Msg** (nhãn cũ: `BUG-BB-003`) | `evidence/fn04/FN04_TC-BB-007_D01_01.png` |
| **TC-BB-008** | FN-04 | Đăng nhập tài khoản không tồn tại | Hiển thị lỗi riêng: *"Tài khoản không tồn tại..."* | Báo: *"Email hoặc mật khẩu không chính xác."* (thông báo gộp) | **FAIL** | **Expected Diff / Firebase Unified Msg** (nhãn cũ: `BUG-BB-002`) | `evidence/fn04/FN04_TC-BB-008_D01_01.png` |
| **TC-BB-009** | FN-04 | Đăng nhập để trống Mật khẩu | Form chặn đăng nhập, yêu cầu nhập đủ dữ liệu | Chặn form trống, báo *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | **PASS** | — | `evidence/fn04/FN04_TC-BB-009_D01_01.png` |
| **TC-BB-016** | FN-08 | Tạo ghi chú có tiêu đề & nội dung | Thẻ ghi chú hiển thị cả tiêu đề và nội dung | HomeScreen hiển thị "Họp Lab" + "Nội dung ngắn gọn" | **PASS** | — | `evidence/fn08/FN08_TC-BB-016_D01_01.png` |
| **TC-BB-017** | FN-08 | Tạo ghi chú chỉ có nội dung | Ghi chú được tạo và có preview nội dung | HomeScreen hiển thị preview "Ý tưởng nhanh không tiêu đề" | **PASS** | — | `evidence/fn08/FN08_TC-BB-017_D01_01.png` |
| **TC-BB-018** | FN-08 | Không tạo ghi chú rỗng | Ứng dụng không tạo ghi chú rỗng mới | Không có ghi chú rỗng mới trên HomeScreen | **PASS** | — | `evidence/fn08/FN08_TC-BB-018_D01_01.png` |
| **TC-BB-019** | FN-09 | Chỉnh sửa nội dung ghi chú | Preview hiển thị đúng nội dung đã chỉnh sửa | HomeScreen hiển thị nội dung `"[Đã cập nhật lúc 10:00]"` | **PASS** | — | `evidence/fn09/FN09_TC-BB-019_D01_01.png` |
| **TC-BB-020** | FN-09 | Tự động lưu sau khi chỉnh sửa | Nội dung mới tồn tại sau khi thoát và mở lại | Mở lại ghi chú vẫn giữ nội dung sau debounce 2s | **PASS** | — | `evidence/fn09/FN09_TC-BB-020_D01_01.png` |
| **TC-BB-021** | FN-10 | Chuyển ghi chú vào thùng rác | Ghi chú chuyển vào Thùng rác, biến mất khỏi Trang chủ | Ghi chú biến mất khỏi HomeScreen và xuất hiện trong TrashScreen (79.83s) | **PASS** | — (XML lịch sử; script working tree hiện rỗng, có `.bak`) | `evidence/fn10/FN10_TC-BB-021_D01_01.png` |
| **TC-BB-022** | FN-11 | Khôi phục ghi chú từ thùng rác | Ghi chú phục hồi về Trang chủ, biến mất khỏi Thùng rác | Ghi chú biến mất khỏi TrashScreen và xuất hiện lại trên HomeScreen (184.13s / 2 duplicate runs = 1 TC duy nhất) | **PASS** | — (XML lịch sử; script working tree hiện rỗng, có `.bak`) | `evidence/fn11/FN11_TC-BB-022_D01_01.png` |
| **TC-BB-023** | FN-12 | Xóa vĩnh viễn ghi chú khỏi thùng rác | Ghi chú bị xóa vĩnh viễn sau xác nhận dialog, không còn trong thùng rác hay Trang chủ | Ghi chú biến mất vĩnh viễn khỏi TrashScreen và không tồn tại trên HomeScreen (88.80s) | **PASS** | — (XML lịch sử; script working tree hiện rỗng, có `.bak`) | `evidence/fn12/FN12_TC-BB-023_D01_01.png` |
| **TC-BB-024** | FN-20 | Ghim ghi chú lên đầu Trang chủ | Xuất hiện phân vùng "Được ghim", note lên đầu | Xuất hiện tiêu đề "Được ghim" và thẻ note ở vùng ưu tiên | **PASS** | — | `evidence/fn20/FN20_TC-BB-024_D01_01.png` |
| **TC-BB-025** | FN-20 | Bỏ ghim ghi chú | Note về danh sách thường; ẩn vùng "Được ghim" | Bỏ ghim, note về danh sách thường; tiêu đề ghim ẩn đi | **PASS** | — | `evidence/fn20/FN20_TC-BB-025_D01_01.png` |
| **TC-BB-026** | FN-23 | Tìm theo từ khóa Tiêu đề | Hiển thị thẻ ghi chú khớp tiêu đề | Kết quả tìm theo tiêu đề "Lịch thi học kỳ" chính xác | **PASS** | — | `evidence/fn23/FN23_TC-BB-026_D01_01.png` |
| **TC-BB-027** | FN-23 | Tìm theo từ khóa Nội dung | Hiển thị thẻ ghi chú khớp nội dung | Kết quả tìm theo nội dung "giấy in A4" chính xác | **PASS** | — | `evidence/fn23/FN23_TC-BB-027_D01_01.png` |
| **TC-BB-028** | FN-23 | Tìm từ khóa không tồn tại | Hiển thị màn hình rỗng "Không tìm thấy kết quả" | Empty State: *"Không tìm thấy kết quả"*, gợi ý thử từ khóa khác | **PASS** | — | `evidence/fn23/FN23_TC-BB-028_D01_01.png` |
| **TC-BB-029** | FN-23 | Tìm với ký tự đặc biệt & SQLi | Không crash; hiển thị màn hình rỗng hợp lệ | Xử lý an toàn chuỗi payload `"' OR 1=1 -- % _ @#$"`, app không crash | **PASS** | — | `evidence/fn23/FN23_TC-BB-029_D01_01.png` |

## 5. Phân tích 4 FAIL và hành động

| TC-ID | Kết quả lưu trong XML | Đánh giá nguyên nhân theo hồ sơ | Hành động tiếp theo |
| --- | --- | --- | --- |
| TC-BB-003 | FAIL | Thông báo domain rác thay vì lỗi định dạng email; nghi vấn thứ tự validation, nhãn cũ BUG-FN02-01 | Giữ Expected; liên kết hồ sơ lỗi chính thức rồi retest khi có build sửa |
| TC-BB-006 | FAIL | Tài khoản chưa verify theo report cũ; không đáp ứng tiền điều kiện | Giữ FAIL XML lịch sử; Phase 4 báo cáo retest PASS, cần log/XML lượt đó; chạy mới nếu không khôi phục được. Không tính là lỗi ứng dụng đã xác nhận |
| TC-BB-007 | FAIL | Thông báo gộp khác Expected thông báo riêng | Xác nhận yêu cầu thông báo; giữ FAIL lịch sử, không tự tuyên bố chính sách đã được phê duyệt |
| TC-BB-008 | FAIL | Thông báo gộp khác Expected thông báo riêng | Xử lý như 007; không suy ra tài khoản được phép đăng nhập |

4 FAIL không đồng nghĩa 4 lỗi sản phẩm. `BUG-BB-003` (007), `BUG-BB-002` (008) và `BUG-FN02-01` là nhãn trong hồ sơ cũ; chưa thấy bản ghi riêng tại [Defect Log](../bugs/defect_log.md) của checkout. `BUG-BB-002/003` khác mã `BUG-002/003`; không tự gộp. Không thay đổi Defect Log chung trong tác vụ hoàn thiện tài liệu tự động này.

## 6. Provider: mã nguồn và kết quả lịch sử

Có 15 khai báo trong [NoteProvider tests](../../test/automated/note_provider_test.dart) và 9 trong [SyncProvider tests](../../test/automated/sync_provider_test.dart). Báo cáo cũ ghi tích hợp từ nhánh thuong tại commit `73514ad`; nguồn đóng góp và kết quả lịch sử được giữ lại, không nhận là test mới do người rà soát thực hiện.

**Đối chiếu bằng chứng thực tế:** File `evidence/automated/automated_test_run.log` (7.700 bytes, UTF-16LE) đã được tìm thấy trên máy cục bộ; log lịch sử xác nhận 24 PASS; chưa xác minh chính xác commit thực thi (dù thời gian file ghi nhận lúc 01:58 ngày 12/10/2026 UTC+7 gần thời điểm commit `73514ad`, nhưng nội dung log không lưu commit hash). Lý do file này trước đó không có trong bản clone/checkout GitHub là do file `.gitignore` của dự án có quy tắc dòng 3 chặn `*.log`. File log này hiện đã được đưa vào staging git (`git add -f`) để người tải repo có thể đối chiếu.

Nội dung log ghi lại lệnh chạy `flutter test test/automated/note_provider_test.dart test/automated/sync_provider_test.dart`, trải qua 24 lượt test và kết thúc bằng dòng `00:01 +24: All tests passed!`. Lưu ý về cơ chế cập nhật dòng của terminal Flutter: terminal cập nhật theo frame tiến độ khiến tiêu đề `Search note by content` xuất hiện lặp lại ở các bước nhảy +7 đến +16 trước khi hoàn thành toàn bộ 24 test. Không coi việc thiếu JUnit XML của Provider là thiếu sót bắt buộc vì file log console đã xác nhận đầy đủ 24 PASS.

| Ref | File | Group | Tên test theo tài liệu | FN | Kết quả lịch sử | Xác minh trên máy |
| --- | --- | --- | --- | --- | --- | --- |
| **PV-REF-01** | `note_provider_test.dart` | NoteProvider - Pin note | Ghim ghi chú bình thường thành công | **FN-20** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-02** | `note_provider_test.dart` | NoteProvider - Pin note | Bỏ ghim ghi chú đã ghim thành công | **FN-20** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-03** | `note_provider_test.dart` | NoteProvider - Archive note | Lưu trữ ghi chú | **FN-13** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-04** | `note_provider_test.dart` | NoteProvider - Archive note | Bỏ lưu trữ ghi chú | **FN-14** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-05** | `note_provider_test.dart` | NoteProvider - Restore note | Khôi phục ghi chú từ thùng rác | **FN-11** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-06** | `note_provider_test.dart` | NoteProvider - Create and Edit note | Tạo ghi chú mới thành công | **FN-08** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-07** | `note_provider_test.dart` | NoteProvider - Create and Edit note | Chỉnh sửa tiêu đề và nội dung ghi chú | **FN-09** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-08** | `note_provider_test.dart` | NoteProvider - Search note | Search note by content | **FN-23** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-09** | `note_provider_test.dart` | NoteProvider - Search note | Search note with no matching result | **FN-23** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-10** | `note_provider_test.dart` | NoteProvider - Search note | Clear search | **FN-23** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-11** | `note_provider_test.dart` | NoteProvider - Note lifecycle | Xóa ghi chú: chuyển vào thùng rác | **FN-10** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-12** | `note_provider_test.dart` | NoteProvider - Note lifecycle | Khôi phục ghi chú từ thùng rác | **FN-11** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-13** | `note_provider_test.dart` | NoteProvider - Note lifecycle | Xóa vĩnh viễn ghi chú trong thùng rác | **FN-12** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-14** | `note_provider_test.dart` | NoteProvider - Note lifecycle | Xóa ghi chú đã ghim vào thùng rác | **FN-10, 20** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-15** | `note_provider_test.dart` | NoteProvider - Note lifecycle | Khôi phục ghi chú đã ghim từ thùng rác | **FN-11, 20** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-16** | `sync_provider_test.dart` | SyncProvider - Initial state | Trạng thái ban đầu là idle | **FN-40** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-17** | `sync_provider_test.dart` | SyncProvider - Update user | Không đồng bộ khi userId là null | **FN-40** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-18** | `sync_provider_test.dart` | SyncProvider - Update user | Đồng bộ khi có userId mới | **FN-40** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-19** | `sync_provider_test.dart` | SyncProvider - Update user | Không đồng bộ lại khi userId không thay đổi | **FN-40** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-20** | `sync_provider_test.dart` | SyncProvider - Update user | Đổi user thì đồng bộ với user mới | **FN-40** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-21** | `sync_provider_test.dart` | SyncProvider - Sync now | Phát tín hiệu khi đồng bộ có dữ liệu mới | **FN-40** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-22** | `sync_provider_test.dart` | SyncProvider - Sync now | Không phát tín hiệu khi không có dữ liệu mới | **FN-40** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-23** | `sync_provider_test.dart` | SyncProvider - Sync now | Bắt lỗi khi đồng bộ thất bại | **FN-40** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |
| **PV-REF-24** | `sync_provider_test.dart` | SyncProvider - Status stream | Cập nhật trạng thái khi repository phát trạng thái mới | **FN-40** | PASS (lịch sử) | ĐÃ XÁC MINH (Log máy 12/10) |

Phạm vi assertion chi tiết xem [đặc tả](automation_test_cases.md). Provider dùng fake repository và mock MethodChannel; không xác minh Firebase thật, SQLite thật, giao diện hoặc LWW trên hai thiết bị. 24 tests tạo 26 liên kết FN do PV-REF-14/15 liên kết vòng đời note và ghim. PV-REF-15 thực tế assert status `normal`, không assert phục hồi trạng thái ghim. PV-REF-05/12 có mục tiêu khôi phục gần nhau.

## 7. Phạm vi chức năng và tồn đọng

- Có XML UI ở 9 FN: 02, 04, 08, 09, 10, 11, 12, 20, 23. Có ít nhất một test không đồng nghĩa bao phủ toàn bộ chức năng.
- Có mã Provider liên kết 10 FN: 08, 09, 10, 11, 12, 13, 14, 20, 23, 40. 7 FN giao với UI; hợp mã hai tầng là 12 FN. Log lịch sử xác nhận 24 PASS; chưa xác minh chính xác commit thực thi.
- **Tình trạng script FN-10, FN-11, FN-12 trên working tree:** 3 file script `test_fn10_trash.py` (0 bytes), `test_fn11_restore.py` (0 bytes) và `test_fn12_permanent_delete.py` (1 byte) hiện đang bị rỗng do thay đổi cục bộ có từ trước ngày 16/10/2026 (trên máy có các file sao lưu `.bak` tương ứng). Kết quả 3 XML của FN-10/11/12 là kết quả lịch sử của phiên bản trước; khả năng chạy lại (rerun) của 3 script này hiện đang bị ảnh hưởng và không khẳng định mã hiện tại sẵn sàng chạy nếu chưa khôi phục nội dung script.
- **Phạm vi mở rộng Phase 4:** Báo cáo ghi nhận 14 AT / 20 lượt chạy (19 PASS, 1 FAIL-APP) kèm 20 file ảnh bằng chứng. Tuy nhiên chưa đối chiếu được log console hoặc file XML thực thi của đợt này; ảnh chụp màn hình ghi nhận giao diện nhưng không coi là bằng chứng đầy đủ cho toàn bộ assertion logic bên trong.
- **Phân biệt mã khiếm khuyết:** `BUG-BB-002` / `BUG-BB-003` (lỗi thông báo gộp Firebase ở FN-04) và `BUG-002` / `BUG-003` (lỗi thiếu Tombstone / Pull-to-refresh ở FN-40) là các mã hoàn toàn khác nhau trong các hồ sơ kiểm thử khác nhau, không phải trùng mã và không tự gộp làm một.
- **Giữ riêng kết quả TC-BB-006:** Giữ nguyên kết quả FAIL lịch sử trong XML baseline (04/10/2026, do tài khoản chưa verify email) và kết quả PASS retest được báo cáo trong Phase 4 (13/10/2026, kèm ảnh chụp sau khi chuẩn bị tài khoản verified); không tự ý ghi đè hoặc chuyển FAIL thành PASS khi chưa có file XML retest độc lập.
- 8 TC UI tạm hoãn: TC-BB-010, 011, 012, 013, 014, 015, 030, 031. Xem lý do và điều kiện khôi phục trong [kế hoạch tiếp theo](automation_review_and_next_steps.md).
- Script đăng ký/đăng nhập có thêm biến thể/alias chưa có XML tương ứng; một số được Phase 4 báo cáo kết quả, tách khỏi 31 TC baseline, không tăng số đã thực thi. [Kiểm kê script](automation_script_inventory.md) ghi từng node ID.
- Lịch sử BLOCKED/FAIL/ERROR của FN-10/11/12 được giữ ở [các report gốc](../../automation/reports/). Không quy đổi `xfail` của pytest thành PASS; BLOCKED là phân loại nguyên nhân trong hồ sơ, cần đọc kết quả công cụ gốc.

## 8. Kết luận và điều kiện chốt tiếp theo

Bộ bằng chứng UI hiện lưu xác nhận 19 PASS và 4 FAIL trên 23 TC duy nhất (qua 9 JUnit XML). Provider có đủ 24 khai báo test và log lịch sử `automated_test_run.log` xác nhận 24 PASS (chưa xác minh chính xác commit thực thi). Không coi việc thiếu JUnit XML của Provider là thiếu sót bắt buộc nếu đã có log console đầy đủ; việc xuất thêm JUnit XML/JSON chỉ là định dạng bổ trợ cho CI tự động. Bộ tài liệu rà soát đã sẵn sàng chốt với đầy đủ căn cứ bằng chứng; không tự ý nghiệm thu toàn bộ ứng dụng chỉ dựa vào tỷ lệ PASS.

Ưu tiên tiếp theo: Khôi phục nội dung 3 script FN-10/11/12 từ file `.bak` hoặc Git HEAD khi cần chạy lại; xác minh retest 006 bằng lượt chạy xuất file XML độc lập (không ghi đè baseline cũ); xác nhận Expected 007/008; retest 003 sau bản sửa; chuẩn hóa lựa chọn node ID và bảo toàn ảnh trước các lượt mới.
