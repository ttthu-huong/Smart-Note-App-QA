# BÁO CÁO THỰC THI KIỂM THỬ TỰ ĐỘNG

**Dự án:** Smart Note App · **Nhánh:** `huong` · **Phiên bản tài liệu:** 1.6 · **Cập nhật Phase 2 (FN-08..12), Phase 3 (FN-13..14), Phase 4 (FN-20) & Phase 5 (FN-23):** 21/10/2026 (UTC+7)

**Mốc baseline của tài liệu gốc:** 19/10/2026 (UTC+7); mã nguồn/bằng chứng đã đối chiếu tại thời điểm đó: `98abb5af577b2d38192e7a88e7ff94a2b5f77262`. Các số liệu baseline vẫn được giữ nguyên; kết quả mở rộng Phase 2 (FN-08 đến FN-12), Phase 3 (FN-13, FN-14), Phase 4 (FN-20: Ghim & Bỏ ghim ghi chú) ngày 20/10 và Phase 5 (FN-23: Tìm kiếm & Bộ lọc đa phương tiện) ngày 21/10 là các đợt thực thi mở rộng độc lập, được tổng hợp đối chiếu từ toàn bộ JUnit XML và cây thư mục evidence trên máy cục bộ. Xem chi tiết tại Mục 9, Mục 10, Mục 11 và Mục 12.

> **Phạm vi mở rộng cũng đang được quản lý:** Ngoài baseline 31 TC UI, hồ sơ Phase 3C chọn 61 TC/74 executions; Phase 4 báo cáo 14 TC/20 executions (19 PASS, 1 FAIL-APP) cùng 3 ca thăm dò riêng. Có report/script/ảnh nhưng chưa đối chiếu được XML/log cho các lượt mở rộng. TC-BB-006 được Phase 4 báo cáo PASS sau khi chuẩn bị lại tài khoản, khác FAIL trong XML baseline. Giữ hai nguồn, không cộng trùng hoặc bỏ qua kết quả được báo cáo. Xem [ma trận mở rộng và nguồn](automation_expanded_scope.md).


## CẬP NHẬT 20/10/2026 — FN-09: Edit Note / Auto-save (bổ sung độc lập)

### Kết quả kiểm thử mới

- **Phạm vi:** 11 mã test case duy nhất (TC-BB-019, 019B, 019C, 019D, 019E, 019F, 019G, 020, 020B, 020C, 020D), tương ứng **12 execution items / 12 pytest test functions**, do TC-BB-019G có hai bộ dữ liệu D01 (System Back) và D02 (Gesture Back).
- **Kết quả cuối theo từng execution item:** **12 PASS / 0 FAIL / 0 ERROR / 0 SKIPPED**, bằng **100% số execution items đã thiết kế cho FN-09**, không phải 100% code coverage, branch coverage, hoặc toàn bộ chức năng của ứng dụng.
- **Cách đối chiếu:** Người thực thi chạy các bài riêng trên điện thoại Android thật; sau đó chạy script đọc các JUnit XML `fn09*.xml` tại `automation/reports`, lựa chọn **bản ghi mới nhất của mỗi pytest test function** và báo cáo `TOTAL: 12/12 PASS`. Bản cập nhật này ghi lại bằng chứng từ console/log do người thực thi cung cấp, **không tuyên bố đã tự mở trực tiếp cả 12 tệp XML trên máy người dùng**.
- **Giới hạn:** Đây là 12 **lượt PASS cuối từ nhiều phiên chạy độc lập**, **không phải** một phiên regression suite 12 test liên tiếp. Các lượt FAILED trước khi chỉnh script/điều kiện môi trường (như 019E và 019G-D02) không bị xóa hoặc viết lại; truy nguyên chúng từ XML và log gốc khi cần.

| TC / Data set | Nội dung kịch bản | Kết quả cuối | JUnit XML (đúng tên được báo cáo) |
| --- | --- | --- | --- |
| TC-BB-019 / D01 | Chỉnh sửa nội dung ghi chú | PASS | [fn09_019_20261020_025349.xml](../../automation/reports/fn09_019_20261020_025349.xml) |
| TC-BB-019B / D01 | Chỉ đổi tiêu đề; giữ nội dung | PASS | [fn09_019b_fixed_20261020_030253.xml](../../automation/reports/fn09_019b_fixed_20261020_030253.xml) |
| TC-BB-019C / D01 | Đổi cả tiêu đề và nội dung | PASS | [fn09_019c_retry_20261020_031702.xml](../../automation/reports/fn09_019c_retry_20261020_031702.xml) |
| TC-BB-019D / D01 | Xóa tiêu đề; giữ nội dung | PASS | [fn09_019d_20261020_032717.xml](../../automation/reports/fn09_019d_20261020_032717.xml) |
| TC-BB-019E / D01 | Xóa nội dung; giữ tiêu đề | PASS | [fn09_019e_retry_20261020_040014.xml](../../automation/reports/fn09_019e_retry_20261020_040014.xml) |
| TC-BB-019F / D01 | Xóa cả tiêu đề và nội dung; ghi chú không còn active | PASS | [fn09_019f_20261020_041022.xml](../../automation/reports/fn09_019f_20261020_041022.xml) |
| TC-BB-019G / D01 | Thoát sau chỉnh sửa bằng System Back | PASS | [fn09_019g_d01_20261020_041415.xml](../../automation/reports/fn09_019g_d01_20261020_041415.xml) |
| TC-BB-019G / D02 | Thoát sau chỉnh sửa bằng Gesture Back | PASS | [fn09_019g_d02_retry_20261020_094859.xml](../../automation/reports/fn09_019g_d02_retry_20261020_094859.xml) |
| TC-BB-020 / D01 | Autosave sau 2,8 giây, force-stop ngay tại Editor | PASS | [fn09_020_20261020_031828.xml](../../automation/reports/fn09_020_20261020_031828.xml) |
| TC-BB-020B / D01 | Chỉnh sửa tuần tự hai lần trên cùng note ID | PASS | [fn09_020b_20261020_095438.xml](../../automation/reports/fn09_020b_20261020_095438.xml) |
| TC-BB-020C / D01 | Unicode, tiếng Việt, emoji 🚀, ký tự đặc biệt | PASS | [fn09_020c_20261020_095808.xml](../../automation/reports/fn09_020c_20261020_095808.xml) |
| TC-BB-020D / D01 | Nội dung chỉnh sửa tồn tại sau khi đóng và mở lại ứng dụng | PASS | [fn09_020d_20261020_100042.xml](../../automation/reports/fn09_020d_20261020_100042.xml) |

### Evidence và đánh giá giao diện

Các test dùng thư mục evidence riêng theo run ID: `evidence/fn09/automation_<RUN_ID>/TC-BB-<TC>/FN09_TC-BB-<TC>_<Dxx>_<seq>.png`. Với D01/D02 của 019G phải dùng đúng hậu tố dataset, không gộp ảnh với nhau. Người thực thi đã gom 5 ảnh audit vào `automation/reports/fn09_evidence_audit_20261020_100542.zip` trên máy cục bộ; **đã kiểm tra trực tiếp nội dung 5 ảnh được gửi trong cuộc trò chuyện**:

| Ảnh đã kiểm tra | Quan sát trực tiếp | Kết luận có căn cứ |
| --- | --- | --- |
| `FN09_TC-BB-019D_D01_02.png` | Title rỗng/placeholder «Tiêu đề», phần nội dung gốc vẫn hiện | Phù hợp expected thao tác xóa Title; không thấy dấu hiệu tràn bố cục trong ảnh |
| `FN09_TC-BB-019E_D01_02.png` | Title được giữ, Quill hiện placeholder «Ghi chú», tiêu đề dài xuống dòng | Phù hợp expected; xuống dòng tự nhiên, không thấy sọc vàng-đen/tràn bố cục trong ảnh |
| `FN09_TC-BB-019F_D01_02.png` | Cả hai trường hiện placeholder rỗng | Phù hợp trạng thái soạn thảo trước khi rời Editor; test/JUnit và SQLite cho biết ghi chú chuyển `trash` |
| `FN09_TC-BB-020C_D01_03.png` | Home NoteCard hiển thị tiếng Việt và emoji 🚀, `@QA`, `#2026` | Không thấy mất ký tự hoặc lỗi bố cục rõ ràng trong ảnh |
| `FN09_TC-BB-020C_D01_04.png` | Editor sau mở lại hiển thị đầy đủ chuỗi Unicode và emoji 🚀 | Phù hợp expected hiển thị; kiểm tra SQLite trong test đối chiếu chính xác chuỗi Unicode |

**Defect giao diện:** Ở 3 ảnh 019D/E/F không quan sát được hiện tượng RenderFlex Overflow. **Không tự động kết luận `BUG-BB-FN09-01` đã được sửa hoặc đóng**: cần đối chiếu điều kiện tái hiện của báo cáo lỗi cũ và retest riêng trước khi đổi trạng thái defect. PASS nghiệp vụ không tự chứng minh mọi yêu cầu UI đều đạt.

**Kiểm soát dữ liệu và tái lập:** Các lượt dùng `FN09_DEBUG=1` giữ lại ghi chú QA phục vụ điều tra (riêng 019F đã chuyển `trash` theo hành vi ứng dụng). Chỉ dọn các ghi chú có ID và nguồn gốc QA xác minh được; không reset ứng dụng, không thao tác note cá nhân và không can thiệp SQLite để sửa dữ liệu. Bản cập nhật không xác nhận đã thực hiện dọn dữ liệu QA hay chạy hồi quy 12 bài trong một lệnh.

### Quan hệ với baseline và phạm vi nghiệm thu

Số `FN-09 = 2 PASS` trong bảng **9 XML UI baseline** bên dưới vẫn là kết quả **ngày 05/10**, không phải trạng thái hiện tại của FN-09. Hai mã TC-BB-019 và TC-BB-020 xuất hiện trong **cả baseline và lượt 20/10**; **không cộng 12 execution items vào tổng 47 tests lịch sử** vì sẽ đếm trùng. Để có tổng toàn dự án cập nhật, phải lập bảng latest-by-identity đồng nhất qua tất cả FN và Provider (phân biệt TC, execution item và lần chạy).

**Trạng thái chốt FN-09:** **Đạt mục tiêu thực thi 12/12 execution items theo các JUnit/log đã kiểm kê và audit 5 ảnh chọn lọc**. Trước khi khóa hồ sơ nộp, nên bảo toàn toàn bộ 12 XML, cây evidence theo run ID, script đã chạy, commit/bản APK và bảng liên kết TC–evidence; trạng thái bug giao diện vẫn để riêng theo defect log.

---

## 1. Kết quả và mức xác minh (baseline rà soát 19/10/2026)

| Chỉ số | UI/E2E | Provider |
| --- | --- | --- |
| Phạm vi thiết kế baseline | 31 TC | 24 khai báo test |
| Kết quả được đối chiếu đợt này | 23 TC duy nhất: 19 PASS, 4 FAIL, 0 ERROR | Log lịch sử xác nhận 24 PASS (0 FAIL) |
| Bản ghi trong bằng chứng hiện có | 24 bản ghi testcase trong 9 XML | Log `evidence/automated/automated_test_run.log` (7.700 bytes; chưa xác minh chính xác commit thực thi) |
| Tỷ lệ PASS đã xác minh | 19/23 = 82.61% | 24/24 = 100% (theo console log) |
| Tỷ lệ TC UI có XML trên tập ứng viên | 23/31 = 74.19% | Không áp dụng |
| Tạm hoãn baseline | 8 TC = 25.81% | Không suy diễn thành chưa từng chạy |
| Báo cáo lịch sử | Các report riêng theo FN | Lịch sử & log máy ghi 24/24 PASS |

Tổng **47 tests, 43 PASS/4 FAIL, 91.49%** là **số liệu baseline lịch sử tính đến 19/10, không phải tổng latest toàn dự án ngày 20/10**, tổng hợp hai tầng (23 UI + 24 Provider). Trong đó: UI có 23 TC xác minh qua 9 XML (19 PASS/4 FAIL); Provider có log lịch sử `automated_test_run.log` xác nhận 24 PASS (0 FAIL), chưa xác minh chính xác commit thực thi. Không coi việc thiếu JUnit XML của Provider là thiếu bắt buộc vì file log console đã ghi nhận đầy đủ 24 test hoàn tất thành công. File log này trước đó bị bỏ qua do `.gitignore` chặn `*.log` và hiện đã được đưa vào danh sách commit của đợt này. Đợt rà soát này đối chiếu bằng chứng hiện hữu trên máy, không chạy test mới.

## 2. Nguồn và giới hạn bằng chứng (baseline)

Đọc XML, kiểm kê Python bằng AST và kiểm kê khai báo Dart, đối chiếu các report Markdown. XML xác nhận trạng thái assertion của lượt lưu, không tự xác nhận APK đang cài được build từ commit nào. Một số timestamp XML không có offset; giữ nguyên giá trị từng file, bao gồm offset nếu có, không tự quy đổi múi giờ.

Model/OS trong tài liệu lịch sử và docstring chưa thống nhất; trước lượt mới cần đo bằng ADB. Report này không thay thế kết quả cũ hoặc tạo ảnh/log kiểm thử mới.

## 3. Đối chiếu 9 XML UI (baseline lịch sử, không gồm lượt FN-09 ngày 20/10)

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

TC-BB-022 được ghi nhận hai lượt chạy, cả hai PASS, nhưng chỉ tính một test case duy nhất. Bộ XML baseline có 24 lượt chạy, tương ứng 23 test case duy nhất: 19 PASS, 4 FAIL. Không cộng số lượt chạy trước đó trong report Markdown vào bảng XML hiện hành.

Thời gian đọc trực tiếp từ thuộc tính `testcase.time` (khác tổng thời gian suite có setup/teardown):

| TC | Thời gian từng bản ghi XML |
| --- | --- |
| TC-BB-021 | 79.806s |
| TC-BB-022 | 92.371s, 91.686s |
| TC-BB-023 | 88.693s |

## 4. Chi tiết 23 TC UI theo báo cáo lịch sử (baseline)

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
| **TC-BB-021** | FN-10 | Chuyển ghi chú vào thùng rác | Ghi chú chuyển vào Thùng rác, biến mất khỏi Trang chủ | Ghi chú biến mất khỏi HomeScreen và xuất hiện trong TrashScreen (79.83s) | **PASS** | — (XML lịch sử; script đã khôi phục từ Git HEAD, chưa rerun) | `evidence/fn10/FN10_TC-BB-021_D01_01.png` |
| **TC-BB-022** | FN-11 | Khôi phục ghi chú từ thùng rác | Ghi chú phục hồi về Trang chủ, biến mất khỏi Thùng rác | Ghi chú biến mất khỏi TrashScreen và xuất hiện lại trên HomeScreen (hai lượt chạy 92.371s và 91.686s, cả hai PASS, tính 1 TC duy nhất) | **PASS** | — (XML lịch sử; script đã khôi phục từ Git HEAD, chưa rerun) | `evidence/fn11/FN11_TC-BB-022_D01_01.png` |
| **TC-BB-023** | FN-12 | Xóa vĩnh viễn ghi chú khỏi thùng rác | Ghi chú bị xóa vĩnh viễn sau xác nhận dialog, không còn trong thùng rác hay Trang chủ | Ghi chú biến mất vĩnh viễn khỏi TrashScreen và không tồn tại trên HomeScreen (88.80s) | **PASS** | — (XML lịch sử; script đã khôi phục từ Git HEAD, chưa rerun) | `evidence/fn12/FN12_TC-BB-023_D01_01.png` |
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
- **Tình trạng script FN-10, FN-11, FN-12:** Trước đó 3 file script `test_fn10_trash.py`, `test_fn11_restore.py` và `test_fn12_permanent_delete.py` từng bị rỗng trên working tree do thay đổi cục bộ từ ngày 16/10/2026. Hiện tại, cả 3 script đã được **khôi phục nguyên vẹn từ Git HEAD** (sử dụng `QANoteHelper`, bảo toàn các file `.bak`). Tuy nhiên, trong đợt này 3 kịch bản này **chưa chạy lại (chưa rerun)**; kết quả 3 XML của FN-10/11/12 vẫn là kết quả lịch sử của phiên bản trước.
- **Phạm vi mở rộng Phase 4:** Báo cáo ghi nhận 14 AT / 20 lượt chạy (19 PASS, 1 FAIL-APP) kèm 20 file ảnh bằng chứng. Tuy nhiên chưa đối chiếu được log console hoặc file XML thực thi của đợt này; ảnh chụp màn hình ghi nhận giao diện nhưng không coi là bằng chứng đầy đủ cho toàn bộ assertion logic bên trong.
- **Phân biệt mã khiếm khuyết:** `BUG-BB-002` / `BUG-BB-003` (lỗi thông báo gộp Firebase ở FN-04) và `BUG-002` / `BUG-003` (lỗi thiếu Tombstone / Pull-to-refresh ở FN-40) là các mã hoàn toàn khác nhau trong các hồ sơ kiểm thử khác nhau, không phải trùng mã và không tự gộp làm một.
- **Giữ riêng kết quả TC-BB-006:** Giữ nguyên kết quả FAIL lịch sử trong XML baseline (04/10/2026, do tài khoản chưa verify email) và kết quả PASS retest được báo cáo trong Phase 4 (13/10/2026, kèm ảnh chụp sau khi chuẩn bị tài khoản verified); không tự ý ghi đè hoặc chuyển FAIL thành PASS khi chưa có file XML retest độc lập.
- 8 TC UI tạm hoãn: TC-BB-010, 011, 012, 013, 014, 015, 030, 031. Xem lý do và điều kiện khôi phục trong [kế hoạch tiếp theo](automation_review_and_next_steps.md).
- Script đăng ký/đăng nhập có thêm biến thể/alias chưa có XML tương ứng; một số được Phase 4 báo cáo kết quả, tách khỏi 31 TC baseline, không tăng số đã thực thi. [Kiểm kê script](automation_script_inventory.md) ghi từng node ID.
- Lịch sử BLOCKED/FAIL/ERROR của FN-10/11/12 được giữ ở [các report gốc](../../automation/reports/). Không quy đổi `xfail` của pytest thành PASS; BLOCKED là phân loại nguyên nhân trong hồ sơ, cần đọc kết quả công cụ gốc.

## 8. Kết luận và điều kiện chốt tiếp theo

**Ở mốc baseline 19/10**, bộ bằng chứng UI được rà soát xác nhận 19 PASS và 4 FAIL trên 23 TC duy nhất (qua 9 JUnit XML). **Bổ sung sau mốc đó: FN-09 đạt 12/12 execution items PASS trong nhiều lượt chạy ngày 20/10; xem phần CẬP NHẬT phía trên. Không cộng chồng số liệu vào baseline.** Provider có đủ 24 khai báo test và log lịch sử `automated_test_run.log` xác nhận 24 PASS (chưa xác minh chính xác commit thực thi). Không coi việc thiếu JUnit XML của Provider là thiếu sót bắt buộc nếu đã có log console đầy đủ; việc xuất thêm JUnit XML/JSON chỉ là định dạng bổ trợ cho CI tự động. Bộ tài liệu rà soát đã sẵn sàng chốt với đầy đủ căn cứ bằng chứng; không tự ý nghiệm thu toàn bộ ứng dụng chỉ dựa vào tỷ lệ PASS.

Ưu tiên tiếp theo: Đã khôi phục nội dung 3 script FN-10/11/12 từ Git HEAD (sử dụng QANoteHelper, sẵn sàng khi cần chạy lại); xác minh retest 006 bằng lượt chạy xuất file XML độc lập (không ghi đè baseline cũ); xác nhận Expected 007/008; retest 003 sau bản sửa; chuẩn hóa lựa chọn node ID và bảo toàn ảnh trước các lượt mới.

---

## 9. KẾT QUẢ MỞ RỘNG AUTOMATION UI/E2E — PHASE 2 (20/10/2026)

### 9.1. Tổng quan kết quả thực thi mở rộng

Trong đợt mở rộng Phase 2 (thực hiện ngày 20/10/2026), phạm vi kiểm thử tự động UI/E2E tập trung vào 5 nhóm chức năng cốt lõi: **FN-08 (Tạo ghi chú), FN-09 (Chỉnh sửa & Tự động lưu), FN-10 (Chuyển vào Thùng rác), FN-11 (Khôi phục ghi chú) và FN-12 (Xóa vĩnh viễn)**.

- **Tổng số execution items đã thiết kế & kiểm kê:** **32 execution items** (tương ứng các test function độc lập và các biến thể dataset D01/D02).
- **Kết quả thực thi toàn diện:** **31 PASS / 1 BLOCKED / 0 FAIL**.
- **Tỷ lệ thành công:** **96.88% PASS** (31/32 items), 1 item BLOCKED do tiền điều kiện môi trường, không có lỗi assertion nghiệp vụ (0 FAIL).

| Nhóm chức năng | Tên chức năng | Tổng items | PASS | BLOCKED | FAIL | Trạng thái ghi nhận |
|---|---|---:|---:|---:|---:|---|
| **FN-08** | Tạo ghi chú mới | 8 | 8 | 0 | 0 | 3 baseline + 5 mở rộng (100% PASS) |
| **FN-09** | Chỉnh sửa & Tự động lưu (Autosave) | 12 | 12 | 0 | 0 | 12 execution items mở rộng (100% PASS; BUG-005 vẫn OPEN) |
| **FN-10** | Chuyển ghi chú vào Thùng rác | 5 | 5 | 0 | 0 | 1 baseline + 4 mở rộng (100% PASS; TC-BB-021B có evidence, chờ XML) |
| **FN-11** | Khôi phục ghi chú từ Thùng rác | 3 | 2 | 1 | 0 | 1 baseline + 1 mở rộng PASS; 1 BLOCKED (TC-BB-022C D01) |
| **FN-12** | Xóa vĩnh viễn ghi chú khỏi Thùng rác | 4 | 4 | 0 | 0 | 1 baseline + 3 mở rộng (100% PASS) |
| **TỔNG CỘNG** | **Phase 2 (FN-08 đến FN-12)** | **32** | **31** | **1** | **0** | **31 PASS / 1 BLOCKED (0 FAIL)** |

---

### 9.2. Chi tiết thực thi từng nhóm chức năng Phase 2

#### A. FN-08 — Tạo ghi chú văn bản (8 execution items: 8 PASS)
- **Script:** `automation/tests/test_fn08_create_note.py` (3 baseline) và `automation/tests/test_fn08_extended.py` (5 mở rộng).

| TC / Data ID | Kịch bản kiểm thử | Kết quả | JUnit XML đối chiếu | Evidence đối chiếu |
|---|---|:---:|---|---|
| **TC-BB-016 / D01** | Tạo ghi chú có đủ Tiêu đề & Nội dung | PASS | [fn08_create_note_junit.xml](../../automation/reports/fn08_create_note_junit.xml) (31.82s, baseline 04/10) | `evidence/fn08/FN08_TC-BB-016_D01_01.png` |
| **TC-BB-017 / D01** | Tạo ghi chú chỉ có Nội dung (không Tiêu đề) | PASS | [fn08_create_note_junit.xml](../../automation/reports/fn08_create_note_junit.xml) (23.26s, baseline 04/10) | `evidence/fn08/FN08_TC-BB-017_D01_01.png` |
| **TC-BB-018 / D01** | Không tạo ghi chú rỗng khi để trống cả 2 ô | PASS | [fn08_create_note_junit.xml](../../automation/reports/fn08_create_note_junit.xml) (15.68s, baseline 04/10) | `evidence/fn08/FN08_TC-BB-018_D01_01.png` |
| **TC-BB-018B / D01** | Tạo ghi chú chỉ có Tiêu đề (nội dung rỗng) | PASS | [fn08_probe_20261020_001621.xml](../../automation/reports/fn08_probe_20261020_001621.xml) (49.34s) | `evidence/fn08/FN08_TC-BB-018B_D01_01.png`, `evidence/fn08/automation_20261020_001623_862241/` |
| **TC-BB-018C / D01** | Tự động lưu ngầm không cần bấm Back (force-stop Editor) | PASS | [fn08_remaining_20261020_001724.xml](../../automation/reports/fn08_remaining_20261020_001724.xml) (58.64s) | `evidence/fn08/FN08_TC-BB-018C_D01_01.png`, `evidence/fn08/automation_20261020_001726_964611/` |
| **TC-BB-018D / D01** | Hủy bản nháp khi xóa sạch về rỗng | PASS | [fn08_remaining_20261020_001724.xml](../../automation/reports/fn08_remaining_20261020_001724.xml) (25.96s) | `evidence/fn08/FN08_TC-BB-018D_D01_01.png`, `evidence/fn08/automation_20261020_001726_964611/` |
| **TC-BB-018E / D01** | Unicode phức tạp, tiếng Việt, emoji 🚀, HTML-like text | PASS | [fn08_018e_final_20261020_015417.xml](../../automation/reports/fn08_018e_final_20261020_015417.xml) (42.53s) | `evidence/fn08/FN08_TC-BB-018E_D01_01.png`, `02.png`, `evidence/fn08/automation_20261020_015419_043437/` (6 ảnh) |
| **TC-BB-018F / D01** | Tính bền vững của ghi chú sau khi restart ứng dụng | PASS | [fn08_remaining_20261020_001724.xml](../../automation/reports/fn08_remaining_20261020_001724.xml) (53.66s) | `evidence/fn08/FN08_TC-BB-018F_D01_01.png`, `evidence/fn08/automation_20261020_001726_964611/` |

*Ghi chú kỹ thuật FN-08:* Riêng `TC-BB-018E` kết hợp UIAutomator2 với Oracle SQLite chỉ đọc (`adb exec-out run-as` + `sqlite3.deserialize()`) do Accessibility XML thay emoji ngoài BMP bằng `..`; test đã đối chiếu trực tiếp dữ liệu SQLite nguyên bản và xác nhận toàn vẹn 100%.

---

#### B. FN-09 — Chỉnh sửa & Tự động lưu (12 execution items: 12 PASS)
- **Script:** `automation/tests/test_fn09_edit_note.py`.
- **Đặc điểm:** 11 mã test case, 12 execution items do TC-BB-019G gồm D01 (System Back) và D02 (Gesture Back).

| TC / Data ID | Kịch bản kiểm thử | Kết quả | JUnit XML đối chiếu | Evidence đối chiếu |
|---|---|:---:|---|---|
| **TC-BB-019 / D01** | Chỉnh sửa nội dung ghi chú | PASS | [fn09_019_20261020_025349.xml](../../automation/reports/fn09_019_20261020_025349.xml) (46.40s) | `evidence/fn09/automation_20261020_025350_985392_2c7d2b87/`, `FN09_TC-BB-019_D01_01.png` |
| **TC-BB-019B / D01** | Chỉ đổi tiêu đề; giữ nguyên nội dung | PASS | [fn09_019b_fixed_20261020_030253.xml](../../automation/reports/fn09_019b_fixed_20261020_030253.xml) (68.81s) | `evidence/fn09/automation_20261020_030254_716373_ac23e584/` |
| **TC-BB-019C / D01** | Đổi cả tiêu đề và nội dung | PASS | [fn09_019c_retry_20261020_031702.xml](../../automation/reports/fn09_019c_retry_20261020_031702.xml) (44.79s) | `evidence/fn09/automation_20261020_031703_633145_ef50e8ff/` |
| **TC-BB-019D / D01** | Xóa tiêu đề; giữ nguyên nội dung | PASS | [fn09_019d_20261020_032717.xml](../../automation/reports/fn09_019d_20261020_032717.xml) (43.06s) | `evidence/fn09/automation_20261020_032718_614397_0fc1d6b5/` (ảnh audit 02) |
| **TC-BB-019E / D01** | Xóa nội dung; giữ nguyên tiêu đề | PASS | [fn09_019e_retry_20261020_040014.xml](../../automation/reports/fn09_019e_retry_20261020_040014.xml) (55.19s) | `evidence/fn09/automation_20261020_040016_148745_d1062ac5/` (ảnh audit 02) |
| **TC-BB-019F / D01** | Xóa cả tiêu đề và nội dung (dọn rác ghi chú) | PASS | [fn09_019f_20261020_041022.xml](../../automation/reports/fn09_019f_20261020_041022.xml) (42.03s) | `evidence/fn09/automation_20261020_041023_362641_4e744850/` (ảnh audit 02) |
| **TC-BB-019G / D01** | Thoát sau chỉnh sửa bằng Android System Back | PASS | [fn09_019g_d01_20261020_041415.xml](../../automation/reports/fn09_019g_d01_20261020_041415.xml) (52.06s) | `evidence/fn09/automation_20261020_041416_237915_e5a52ab0/` |
| **TC-BB-019G / D02** | Thoát sau chỉnh sửa bằng Android Gesture Back | PASS | [fn09_019g_d02_retry_20261020_094859.xml](../../automation/reports/fn09_019g_d02_retry_20261020_094859.xml) (48.55s) | `evidence/fn09/automation_20261020_094901_092380_3febeb92/` |
| **TC-BB-020 / D01** | Autosave sau 2.8s, force-stop ngay tại Editor | PASS | [fn09_020_20261020_031828.xml](../../automation/reports/fn09_020_20261020_031828.xml) (48.89s) | `evidence/fn09/automation_20261020_031829_739761_dd030562/`, `FN09_TC-BB-020_D01_01.png` |
| **TC-BB-020B / D01** | Chỉnh sửa tuần tự 2 lần trên cùng note ID | PASS | [fn09_020b_20261020_095438.xml](../../automation/reports/fn09_020b_20261020_095438.xml) (56.40s) | `evidence/fn09/automation_20261020_095440_379178_437e76e5/` |
| **TC-BB-020C / D01** | Unicode tiếng Việt, emoji 🚀, ký tự đặc biệt | PASS | [fn09_020c_20261020_095808.xml](../../automation/reports/fn09_020c_20261020_095808.xml) (42.00s) | `evidence/fn09/automation_20261020_095810_612309_3146c2ce/` (ảnh audit 03, 04) |
| **TC-BB-020D / D01** | Nội dung chỉnh sửa tồn tại sau khi restart app | PASS | [fn09_020d_20261020_100042.xml](../../automation/reports/fn09_020d_20261020_100042.xml) (52.86s) | `evidence/fn09/automation_20261020_100044_765185_4c77ba97/` |

*Ghi chú khiếm khuyết FN-09:* 12 items PASS kiểm thử chức năng tự động. Khiếm khuyết giao diện **BUG-005** (RenderFlex Overflow / dải vàng đen thoáng qua khi bàn phím co giãn) **vẫn ở trạng thái OPEN** trong Defect Log; kết quả PASS của automation không tự đóng bug này.

---

#### C. FN-10 — Chuyển ghi chú vào Thùng rác (5 execution items: 5 PASS)
- **Script:** `automation/tests/test_fn10_trash.py`.

| TC / Data ID | Kịch bản kiểm thử | Kết quả | JUnit XML đối chiếu | Evidence đối chiếu |
|---|---|:---:|---|---|
| **TC-BB-021 / D01** | Chuyển 1 ghi chú vào Thùng rác từ Selection Bar | PASS | [fn10_trash_junit.xml](../../automation/reports/fn10_trash_junit.xml) (79.81s, baseline 14/10) | `evidence/fn10/FN10_TC-BB-021_D01_01.png` |
| **TC-BB-021B / D01** | Hoàn tác chuyển ghi chú vào Thùng rác từ SnackBar | PASS | *Chờ xuất XML riêng* (Lượt chạy 20/10 lúc 11:08:41 hoàn thành PASS) | `evidence/fn10/automation_20261020_110841_407404_51da0bf6/TC-BB-021B/` (4 ảnh `01.png` đến `04.png`) |
| **TC-BB-021C / D01** | Hủy xóa ghi chú từ menu 3 chấm trong Editor | PASS | [fn10_021c_d01_retry_20261020_120916.xml](../../automation/reports/fn10_021c_d01_retry_20261020_120916.xml) (100.48s) | `evidence/fn10/automation_20261020_120917_335994_c5046c82/TC-BB-021C/` (5 ảnh `01.png` đến `05.png`) |
| **TC-BB-021C / D02** | Xác nhận xóa ghi chú từ menu 3 chấm trong Editor | PASS | [fn10_021c_d02_20261020_124605.xml](../../automation/reports/fn10_021c_d02_20261020_124605.xml) (95.20s) | `evidence/fn10/automation_20261020_124606_790642_535958ce/TC-BB-021C/` (5 ảnh `01.png` đến `05.png`) |
| **TC-BB-021D / D01** | Chọn nhiều ghi chú (2 notes) và chuyển vào Thùng rác | PASS | [fn10_021d_20261020_130907.xml](../../automation/reports/fn10_021d_20261020_130907.xml) (95.36s) | `evidence/fn10/automation_20261020_130909_123394_aea15e14/TC-BB-021D/` (5 ảnh `01.png` đến `05.png`) |

*Ghi chú kỹ thuật FN-10:* `TC-BB-021B D01` đã chạy thành công trên máy thật và lưu đủ 4 ảnh bằng chứng xác minh ghi chú phục hồi về HomeScreen và vắng mặt ở TrashScreen. Cần lưu ý lượt chạy này chưa lưu file JUnit XML độc lập trong `automation/reports/` (do lệnh chạy thiếu `--junitxml`).

---

#### D. FN-11 — Khôi phục ghi chú từ Thùng rác (3 execution items: 2 PASS, 1 BLOCKED)
- **Script:** `automation/tests/test_fn11_restore.py`.

| TC / Data ID | Kịch bản kiểm thử | Kết quả | JUnit XML đối chiếu | Evidence đối chiếu |
|---|---|:---:|---|---|
| **TC-BB-022 / D01** | Khôi phục 1 ghi chú từ Thùng rác về Trang chủ | PASS | [fn11_restore_junit.xml](../../automation/reports/fn11_restore_junit.xml) (92.37s / 91.69s, baseline 14/10) | `evidence/fn11/FN11_TC-BB-022_D01_01.png` |
| **TC-BB-022B / D01** | Khôi phục hàng loạt ghi chú (multi-restore) | PASS | [fn11_022b_20261020_132119.xml](../../automation/reports/fn11_022b_20261020_132119.xml) (123.76s) | `evidence/fn11/automation_20261020_132134_088541_974befa2ac/TC-BB-022B/` (4 ảnh `01.png` đến `04.png`) |
| **TC-BB-022C / D01** | Kiểm tra giao diện Empty State "Thùng rác trống" | **BLOCKED** *(pytest: SKIPPED)* | [fn11_022c_20261020_132720.xml](../../automation/reports/fn11_022c_20261020_132720.xml) (42.21s) | `evidence/fn11/automation_20261020_132734_161378_9a81212f/TC-BB-022C/precondition_not_empty.png` |

*Phân tích trường hợp BLOCKED của TC-BB-022C D01:*
- **Kết quả pytest:** `SKIPPED` (ghi nhận trong file JUnit XML `fn11_022c_20261020_132720.xml`).
- **Phân loại nghiệp vụ QA:** **BLOCKED** (không phải FAIL và không phải bug ứng dụng).
- **Nguyên nhân:** Kịch bản yêu cầu tiền điều kiện Thùng rác phải hoàn toàn rỗng để kiểm chứng ảnh minh họa và thông điệp *"Thùng rác trống"*. Tuy nhiên, tại thời điểm chạy thực tế, Thùng rác trên thiết bị đang chứa 23 ghi chú tồn tại từ các đợt kiểm thử trước. Để tuân thủ nguyên tắc an toàn dữ liệu ("Không xóa dữ liệu cá nhân/không rõ nguồn gốc QA"), test script chủ động kích hoạt `pytest.skip(...)` nhằm tránh việc xóa sạch 23 ghi chú này. Ca kiểm thử sẽ được thực thi lại (retest) khi môi trường Thùng rác đã được làm sạch an toàn.

---

#### E. FN-12 — Xóa vĩnh viễn ghi chú khỏi Thùng rác (4 execution items: 4 PASS)
- **Script:** `automation/tests/test_fn12_permanent_delete.py`.

| TC / Data ID | Kịch bản kiểm thử | Kết quả | JUnit XML đối chiếu | Evidence đối chiếu |
|---|---|:---:|---|---|
| **TC-BB-023 / D01** | Xóa vĩnh viễn 1 ghi chú khỏi Thùng rác | PASS | [fn12_permanent_delete_junit.xml](../../automation/reports/fn12_permanent_delete_junit.xml) (88.69s, baseline 14/10) | `evidence/fn12/FN12_TC-BB-023_D01_01.png` |
| **TC-BB-023B / D01** | Hủy xóa vĩnh viễn nhiều ghi chú trên AlertDialog | PASS | [fn12_023b_d01_retry_20261020_135257.xml](../../automation/reports/fn12_023b_d01_retry_20261020_135257.xml) (102.52s) | `evidence/fn12/automation_20261020_135310_686942_d3abb8b620/TC-BB-023B/` (5 ảnh `01.png` đến `05.png`) |
| **TC-BB-023B / D02** | Xác nhận xóa vĩnh viễn nhiều ghi chú trên AlertDialog | PASS | [fn12_023b_d02_20261020_145053.xml](../../automation/reports/fn12_023b_d02_20261020_145053.xml) (128.59s) | `evidence/fn12/automation_20261020_145107_957126_f1858ca760/TC-BB-023B/` (6 ảnh `01.png` đến `06.png`) |
| **TC-BB-023C / D01** | Tính bền vững vòng đời ghi chú (Trash + Deleted) sau restart | PASS | [fn12_023c_20261020_150216.xml](../../automation/reports/fn12_023c_20261020_150216.xml) (141.84s) | `evidence/fn12/automation_20261020_150230_580481_1c12522463/TC-BB-023C/` (5 ảnh `01.png` đến `05.png`) |

*Ghi chú kỹ thuật FN-12:* `TC-BB-023C D01` là kịch bản kiểm thử tích hợp vòng đời mở rộng kết hợp giữa FN-10, FN-11 và FN-12: tạo 2 ghi chú riêng, chuyển cả hai vào Thùng rác, xóa vĩnh viễn 1 ghi chú, force-stop ứng dụng, mở lại và xác minh ghi chú còn lại vẫn nằm trong Thùng rác còn ghi chú đã xóa vĩnh viễn biến mất hoàn toàn. Kịch bản đã chạy thành công 141.84s và bảo đảm tính toàn vẹn trạng thái cơ sở dữ liệu.

---

### 9.3. Danh mục tồn đọng kỹ thuật sau đợt mở rộng Phase 2

1. **TC-BB-021B D01:** Đã hoàn tất thực thi PASS trên thiết bị và lưu 4 ảnh evidence tại `evidence/fn10/automation_20261020_110841_407404_51da0bf6/TC-BB-021B/`, nhưng cần bổ sung file JUnit XML riêng vào `automation/reports/` khi có phiên rerun tự động.
2. **TC-BB-022C D01:** Tạm thời `BLOCKED` do Thùng rác còn 23 ghi chú; cần retest khi có môi trường Thùng rác rỗng mà không xóa nhầm dữ liệu người dùng.
3. **Khiếm khuyết BUG-005:** Lỗi RenderFlex Overflow thoáng qua trên FN-09 vẫn đang `OPEN`; kết quả PASS của automation không đóng bug này.
4. **Không cộng gộp số liệu baseline:** Kết quả Phase 2 gồm 32 execution items (31 PASS, 1 BLOCKED) là số liệu mở rộng độc lập, không cộng dồn trực tiếp vào tổng baseline lịch sử 47 tests (43 PASS / 4 FAIL) để tránh đếm trùng các test case đã chạy ở cả hai mốc (như TC-BB-016..020, 021, 022, 023).

---

## 10. CẬP NHẬT MỞ RỘNG PHASE 3 (20/10/2026) — FN-13 VÀ FN-14: QUẢN LÝ LƯU TRỮ (ARCHIVE / UNARCHIVE)

### 10.1. Tổng quan kết quả thực thi Phase 3

- **Phạm vi kiểm thử:** 5 mã test case / 5 execution items thuộc 2 chức năng quản lý lưu trữ:
  - **FN-13 (Lưu trữ ghi chú):** `TC-BB-040` (D01), `TC-BB-EXT-008` (D01), `TC-BB-EXT-006` (D01).
  - **FN-14 (Bỏ lưu trữ ghi chú):** `TC-BB-040B` (D01), `TC-BB-EXT-007` (D01).
- **Mã nguồn kiểm thử tự động:** `automation/tests/test_fn13_fn14_archive.py` (class `TestFN13FN14Archive`).
- **Tổng kết quả:** **5 PASS / 0 FAIL cuối cùng / 0 BLOCKED** trên **5 execution items** (đạt 100% số execution items được thiết kế cho Phase 3; không tuyên bố 100% code coverage hay toàn bộ chức năng của ứng dụng).
- **Phân định kết quả:**
  - 4 execution items PASS ngay lần chạy đầu tiên (`TC-BB-040`, `EXT-008`, `EXT-006`, `EXT-007`).
  - 1 execution item (`TC-BB-040B`) ghi nhận `FAIL-AUTO` trong phiên chạy sơ bộ do lỗi tiền điều kiện (test trước kết thúc tại `ArchiveScreen`, hàm `ensure_home_screen` của driver chỉ bấm Back nên không thể đóng ArchiveScreen). Sau khi cập nhật hàm `_start()` chủ động điều hướng qua MainDrawer để quay về HomeScreen, phiên chạy lại retry độc lập đã đạt **PASS** hoàn toàn.

### 10.2. Chi tiết kết quả thực thi từng Test Case

#### A. FN-13 — Lưu trữ ghi chú (3 execution items: 3 PASS)
- **Script:** `automation/tests/test_fn13_fn14_archive.py`.
- **Tầng kiểm thử:** Đa tầng (UI/E2E uiautomator2 + SQLite Oracle + Provider baseline).

| TC / Data ID | Kịch bản kiểm thử | Kết quả | JUnit XML đối chiếu | Thời gian | Evidence đối chiếu |
|---|---|:---:|---|:---:|---|
| **TC-BB-040 / D01** | Lưu trữ 1 ghi chú từ HomeScreen (Selection Bar) | **PASS** | [fn13_fn14_20261020_162606.xml](../../automation/reports/fn13_fn14_20261020_162606.xml) | 51.65s | `evidence/fn13_14/automation_20261020_162615_605331_014938864a/TC-BB-040/`<br>(3 ảnh: `01.png` tạo note, `02.png` lưu trữ, `03.png` xuất hiện trong Archive) |
| **TC-BB-EXT-008 / D01** | Lưu trữ Target không ảnh hưởng Control (Cô lập dữ liệu) | **PASS** | [fn13_fn14_remaining3_20261020_165116.xml](../../automation/reports/fn13_fn14_remaining3_20261020_165116.xml) | 74.39s | `evidence/fn13_14/automation_20261020_165126_004774_5c06926696/TC-BB-EXT-008/`<br>(3 ảnh: `01.png` 2 note, `02.png` Target biến mất/Control còn, `03.png` Target trong Archive) |
| **TC-BB-EXT-006 / D01** | Tính bền vững dữ liệu lưu trữ tiếng Việt sau khi restart app | **PASS** | [fn13_fn14_remaining3_20261020_165116.xml](../../automation/reports/fn13_fn14_remaining3_20261020_165116.xml) | 55.51s | `evidence/fn13_14/automation_20261020_165232_968737_a40c7e7091/TC-BB-EXT-006/`<br>(4 ảnh: `01.png` tạo note Unicode, `02.png` lưu trữ, `03.png` sau restart vắng mặt ở Home, `04.png` hiển thị đủ 2 dòng trong Archive) |

#### B. FN-14 — Bỏ lưu trữ ghi chú (2 execution items: 2 PASS)
- **Script:** `automation/tests/test_fn13_fn14_archive.py`.
- **Tầng kiểm thử:** Đa tầng (UI/E2E uiautomator2 + SQLite Oracle + Provider baseline).

| TC / Data ID | Kịch bản kiểm thử | Kết quả | JUnit XML đối chiếu | Thời gian | Evidence đối chiếu |
|---|---|:---:|---|:---:|---|
| **TC-BB-040B / D01** | Bỏ lưu trữ ghi chú từ ArchiveScreen qua BottomSheet | **PASS** | [fn14_040b_usb_20261020_164931.xml](../../automation/reports/fn14_040b_usb_20261020_164931.xml) *(lượt retry hoàn tất)* | 64.56s | `evidence/fn13_14/automation_20261020_164941_019186_493c0b9697/TC-BB-040B/`<br>(3 ảnh: `01.png` trong Archive, `02.png` BottomSheet bỏ lưu trữ, `03.png` quay lại HomeScreen) |
| **TC-BB-EXT-007 / D01** | Vòng lặp Bỏ lưu trữ $\rightarrow$ Lưu trữ $\rightarrow$ Bỏ lưu trữ không gây nhân bản (Idempotency) | **PASS** | [fn13_fn14_remaining3_20261020_165116.xml](../../automation/reports/fn13_fn14_remaining3_20261020_165116.xml) | 98.37s | `evidence/fn13_14/automation_20261020_165328_477351_4b7542817e/TC-BB-EXT-007/`<br>(5 ảnh: `01.png` archive lần 1, `02.png` unarchive lần 1, `03.png` archive lại, `04.png` unarchive lần 2 + restart app, `05.png` ArchiveScreen vắng mặt) |

*Ghi chú phân định kỹ thuật lượt chạy của TC-BB-040B D01:*
- Lượt chạy đầu tiên trong tệp JUnit [fn13_fn14_20261020_162606.xml](../../automation/reports/fn13_fn14_20261020_162606.xml) (74.52s) bị dừng do lỗi tiền điều kiện (`AssertionError: Precondition failed: App is not on HomeScreen`). Đây là **FAIL-AUTO** (lỗi điều hướng tự động hóa, không phải bug nghiệp vụ ứng dụng).
- Sau khi bổ sung cơ chế kiểm tra và điều hướng hồi phục qua MainDrawer trong hàm `_start()`, lượt chạy retry độc lập trong tệp JUnit [fn14_040b_usb_20261020_164931.xml](../../automation/reports/fn14_040b_usb_20261020_164931.xml) (64.56s) đã **PASS hoàn toàn**, xác minh chính xác trạng thái SQLite `status = 'normal'` và giao diện hiển thị.

### 10.3. Quan hệ với Baseline và Tổng kết toàn diện

- **Tính toàn vẹn số liệu:** Kết quả Phase 3 gồm **5 execution items (5 PASS)** được hạch toán độc lập, không cộng dồn trực tiếp vào tổng baseline 47 tests lịch sử (43 PASS / 4 FAIL) và không làm thay đổi kết quả Phase 2 (32 items: 31 PASS / 1 BLOCKED).
- **Mức độ bao phủ chức năng REQ-09:** Nhờ Phase 3, yêu cầu **REQ-09 (Quản lý Thùng rác & Lưu trữ)** đã hoàn thành tự động hóa 100% cả hai nhánh nghiệp vụ:
  - Phân hệ Thùng rác (FN-10, FN-11, FN-12): 11 PASS / 1 BLOCKED.
  - Phân hệ Lưu trữ (FN-13, FN-14): 5 PASS / 0 FAIL.
  - Tổng cộng REQ-09 có **16 items PASS / 1 BLOCKED / 0 FAIL** trên 17 execution items tự động hóa UI/E2E.

---

## 11. CẬP NHẬT MỞ RỘNG PHASE 4 (20/10/2026) — FN-20: GHIM VÀ BỎ GHIM GHI CHÚ (PIN / UNPIN NOTE)

### 11.1. Tổng quan kết quả thực thi Phase 4

- **Phạm vi kiểm thử:** 15 execution items thuộc chức năng **FN-20 (Ghim & Bỏ ghim ghi chú)**:
  - 2 execution items baseline lịch sử: `TC-BB-024` (D01), `TC-BB-025` (D01) trong `automation/tests/test_fn20_pin_note.py`.
  - 13 execution items mở rộng Phase 4: `TC-BB-024B` (D01, D02), `TC-BB-024C` (D01), `TC-BB-024D` (D01), `TC-BB-024E` (D01), `TC-BB-024F` (D01), `TC-BB-024G` (D01), `TC-BB-024H` (D01), `TC-BB-025B` (D01), `TC-BB-025C` (D01), `TC-BB-025D` (D01), `TC-BB-025E` (D01), `TC-BB-025F` (D01) trong `automation/tests/test_fn20_extended.py`.
- **Tổng kết quả:** **15 PASS / 0 FAIL cuối cùng / 0 BLOCKED** trên **15 execution items** (đạt 100% số execution items được thiết kế cho FN-20; không tuyên bố 100% code coverage hay toàn bộ chức năng của ứng dụng).
- **Quy tắc đếm số liệu:**
  - Đây là kết quả **tổng hợp từ nhiều lượt chạy có mục tiêu**, không phải 15 ca PASS trong một lần chạy duy nhất của toàn bộ suite.
  - Các lần FAIL-AUTO trước đó (do cuộn viewport, nhận diện SystemUI thanh thông báo, hoặc định vị AppBar) được giữ lại trong lịch sử thực thi để truy vết kỹ thuật nhưng không tính thành lỗi ứng dụng (FAIL nghiệp vụ) cuối cùng.
  - Baseline 2 TC (`TC-BB-024 D01` và `TC-BB-025 D01`) chỉ tính một lần, không cộng thêm vào 13 ca mở rộng.
  - Hai bài test Provider `PV-REF-01` và `PV-REF-02` là tầng kiểm thử độc lập, không cộng dồn vào mẫu số 15 ca UI automation.

### 11.2. Chi tiết kết quả thực thi 15 Execution Items FN-20

| # | TC / Data set | Nội dung kịch bản | Kết quả cuối | JUnit XML đối chiếu | Evidence đối chiếu |
|---:|---|---|:---:|---|---|
| 1 | **TC-BB-024 / D01** | Ghim ghi chú lên khu vực ưu tiên từ Trang chủ | **PASS** | [fn20_pin_note_junit.xml](../../automation/reports/fn20_pin_note_junit.xml) *(baseline 05/10)* | `evidence/fn20/FN20_TC-BB-024_D01_01.png` |
| 2 | **TC-BB-025 / D01** | Bỏ ghim ghi chú trở về danh sách thông thường từ Trang chủ | **PASS** | [fn20_pin_note_junit.xml](../../automation/reports/fn20_pin_note_junit.xml) *(baseline 05/10)* | `evidence/fn20/FN20_TC-BB-025_D01_01.png` |
| 3 | **TC-BB-024B / D01** | Ghim ghi chú trực tiếp từ AppBar màn hình soạn thảo (Editor) | **PASS** | [fn20_editor_20261020_191551.xml](../../automation/reports/fn20_editor_20261020_191551.xml) (55.48s) | `evidence/fn20/run_20261020_191601_27ef75ac/TC-BB-024B_D01/`<br>(3 ảnh: `01.png` tạo note, `02.png` trong Editor, `03.png` đã ghim trên Home) |
| 4 | **TC-BB-024B / D02** | Bỏ ghim ghi chú trực tiếp từ AppBar màn hình soạn thảo (Editor) | **PASS** | [fn20_024b_d02_retry2_20261020_195008.xml](../../automation/reports/fn20_024b_d02_retry2_20261020_195008.xml) (67.43s) | `evidence/fn20/run_20261020_195017_78c1f1f3/TC-BB-024B_D02/`<br>(3 ảnh: `01.png` note đã ghim, `02.png` bỏ ghim trong Editor, `03.png` về danh sách thường) |
| 5 | **TC-BB-024C / D01** | Ràng buộc không cho phép ghim ghi chú mới khi chưa nhập nội dung | **PASS** | [fn20_024c_d01_20261020_195609.xml](../../automation/reports/fn20_024c_d01_20261020_195609.xml) (32.89s) | `evidence/fn20/run_20261020_195618_3e41d9d8/TC-BB-024C_D01/`<br>(3 ảnh: `01.png` Editor rỗng, `02.png` SnackBar cảnh báo, `03.png` SQLite không sinh note rác) |
| 6 | **TC-BB-024D / D01** | Ghim đồng thời nhiều ghi chú từ Trang chủ (Batch Pin 2 notes) | **PASS** | [fn20_batch_20261020_190742.xml](../../automation/reports/fn20_batch_20261020_190742.xml) (71.30s) | `evidence/fn20/run_20261020_190753_ae757378/TC-BB-024D_D01/`<br>(3 ảnh: `01.png` 2 note thường, `02.png` chọn cả 2, `03.png` cả 2 chuyển lên Được ghim) |
| 7 | **TC-BB-024H / D01** | Đảo trạng thái độc lập khi chọn đồng thời ghi chú đã ghim và chưa ghim | **PASS** | [fn20_batch_20261020_190742.xml](../../automation/reports/fn20_batch_20261020_190742.xml) (68.51s) | `evidence/fn20/run_20261020_190906_dab38cc3/TC-BB-024H_D01/`<br>(3 ảnh: `01.png` 1 ghim + 1 thường, `02.png` chọn cả 2, `03.png` đảo chiều độc lập cả 2) |
| 8 | **TC-BB-025D / D01** | Bỏ ghim đồng thời nhiều ghi chú từ Trang chủ (Batch Unpin 2 notes) | **PASS** | [fn20_batch_20261020_190742.xml](../../automation/reports/fn20_batch_20261020_190742.xml) (75.87s) | `evidence/fn20/run_20261020_191017_3e9899d7/TC-BB-025D_D01/`<br>(3 ảnh: `01.png` 2 note ghim, `02.png` chọn cả 2, `03.png` cả 2 về danh sách thường) |
| 9 | **TC-BB-025E / D01** | Phân vùng 'Được ghim' vẫn duy trì khi chỉ bỏ ghim 1 trong số nhiều note ghim | **PASS** | [fn20_batch_20261020_190742.xml](../../automation/reports/fn20_batch_20261020_190742.xml) (75.98s) | `evidence/fn20/run_20261020_191135_00e1fa58/TC-BB-025E_D01/`<br>(3 ảnh: `01.png` 2 note ghim, `02.png` chỉ chọn 1 note, `03.png` 1 note về thường + 1 note còn ghim) |
| 10 | **TC-BB-024E / D01** | Hiển thị phân vùng 'Được ghim' và 'Khác' khi có đồng thời cả 2 loại ghi chú | **PASS** | [fn20_024e_v7_20261020_205408.xml](../../automation/reports/fn20_024e_v7_20261020_205408.xml) (64.33s) | `evidence/fn20/run_20261020_205417_9fc5ebc6/TC-BB-024E_D01/`<br>(3 ảnh: `01.png` 2 note, `02.png` 2 phân vùng với toạ độ phân cấp chuẩn, `03.png` hoàn tất) |
| 11 | **TC-BB-024F / D01** | Tính toàn vẹn dữ liệu (Tiêu đề, Nội dung) qua chu kỳ Pin $\rightarrow$ Unpin | **PASS** | [fn20_024f_20261020_205909.xml](../../automation/reports/fn20_024f_20261020_205909.xml) (62.29s) | `evidence/fn20/run_20261020_205918_b7b5d72e/TC-BB-024F_D01/`<br>(3 ảnh: `01.png` tạo note đầy đủ, `02.png` mở kiểm tra khi pinned, `03.png` mở kiểm tra khi unpinned) |
| 12 | **TC-BB-024G / D01** | Giao diện khi toàn bộ các ghi chú đều ở trạng thái được ghim (All Pinned) | **PASS** | [fn20_024g_v9_20261020_221313.xml](../../automation/reports/fn20_024g_v9_20261020_221313.xml) (66.52s) | `evidence/fn20/run_20261020_221322_59346191/TC-BB-024G_D01/`<br>(4 ảnh: `01.png` kiểm tra user, `02.png` ghim toàn bộ 3 note, `03.png` chỉ hiện Được ghim, `04.png` vắng mặt Khác) |
| 13 | **TC-BB-025B / D01** | Tính bền vững trạng thái Ghim sau khi khởi động lại ứng dụng (Persistence) | **PASS** | [fn20_025b_v8_20261020_211941.xml](../../automation/reports/fn20_025b_v8_20261020_211941.xml) (55.43s) | `evidence/fn20/run_20261020_211950_c769bfbe/TC-BB-025B_D01/`<br>(3 ảnh: `01.png` ghim note, `02.png` sau force-stop và restart, `03.png` note vẫn trong Được ghim) |
| 14 | **TC-BB-025C / D01** | Ghi chú đã ghim vẫn duy trì trạng thái ghim sau khi chỉnh sửa nội dung | **PASS** | [fn20_025c_20261020_213027.xml](../../automation/reports/fn20_025c_20261020_213027.xml) (62.34s) | `evidence/fn20/run_20261020_213036_64bf71ee/TC-BB-025C_D01/`<br>(3 ảnh: `01.png` note ghim gốc, `02.png` sửa nội dung trong Editor, `03.png` nội dung mới cập nhật & vẫn ghim) |
| 15 | **TC-BB-025F / D01** | Tính bền vững trạng thái Bỏ ghim sau khi khởi động lại ứng dụng (Persistence) | **PASS** | [fn20_025f_20261020_215211.xml](../../automation/reports/fn20_025f_20261020_215211.xml) (57.19s) | `evidence/fn20/run_20261020_215221_b1d825c4/TC-BB-025F_D01/`<br>(3 ảnh: `01.png` note bỏ ghim về normal, `02.png` sau restart app, `03.png` duy trì danh sách thường) |

### 11.3. Môi trường kiểm thử và giải pháp an toàn dữ liệu

- **Thực thi an toàn trên thiết bị thật:** Tất cả 15 ca kiểm thử được chạy trực tiếp trên thiết bị Samsung Galaxy S21 FE 5G (Android 14, API 34).
- **Giải pháp tiền điều kiện cho TC-BB-024G (All Notes Pinned):**
  - Để tránh việc ghim hàng loạt ghi chú của tài khoản cá nhân / tài khoản thử nghiệm trước đó, test case `TC-BB-024G` được thực thi bằng **tài khoản QA mới** tạo riêng.
  - Test tạo đúng 3 ghi chú QA độc lập, xác minh SQLite theo đúng `user_id` hiện tại và kiểm chứng giao diện: phân vùng *"Được ghim"* hiển thị đầy đủ, tiêu đề phân vùng *"Khác"* hoàn toàn không xuất hiện trên giao diện.
  - Không sử dụng `pm clear` hay reset ứng dụng; không làm ảnh hưởng đến dữ liệu của các tài khoản khác.
- **Bảo toàn dữ liệu kiểm thử:** Tất cả các ghi chú QA được tạo với định danh UUID duy nhất và tiền tố `QA_PIN_`, không sử dụng lệnh xóa hay chuyển vào Thùng rác để cleanup, bảo đảm an toàn dữ liệu 100%.
- **Bao phủ chức năng REQ-07:** Yêu cầu **REQ-07 (Ghim ghi chú — Pin Note)** đã hoàn thành tự động hóa UI/E2E 100% với **15/15 execution items PASS**, kết hợp với 2 tests Provider `PV-REF-01` và `PV-REF-02` đã được đối chiếu trong log lịch sử.

---

## 12. CẬP NHẬT MỞ RỘNG PHASE 5 (21/10/2026) — FN-23: TÌM KIẾM GHI CHÚ VÀ BỘ LỌC ĐA PHƯƠNG TIỆN (SEARCH & FILTER)

### 12.1. Tổng quan kết quả thực thi Phase 5

- **Phạm vi kiểm thử:** Chức năng **FN-23 (Tìm kiếm ghi chú theo từ khóa văn bản & Bộ lọc đa phương tiện)** bao gồm 17 mã test case / 22 execution items:
  - **4 execution items baseline lịch sử:** `TC-BB-026` (D01), `TC-BB-027` (D01), `TC-BB-028` (D01), `TC-BB-029` (D01) trong [fn23_search_junit.xml](../../automation/reports/fn23_search_junit.xml) (4 PASS).
  - **14 execution items mở rộng Phase 5:** Triển khai mới trong `automation/tests/test_fn23_extended.py`, thực thi trên thiết bị Samsung Galaxy S21 FE 5G:
    - **Batch 1 (5 items):** `TC-BB-026B` (D01, D02), `TC-BB-026C` (D01), `TC-BB-026E` (D01), `TC-BB-028D` (D01) — **5 PASS / 0 FAIL**.
    - **Batch 2 (6 items):** `TC-BB-027D` (D01, D02), `TC-BB-027F` (D01), `TC-BB-028B` (D01), `TC-BB-027B` (D03), `TC-BB-028C` (D01) — **6 PASS / 0 FAIL**.
    - **Batch 3 (3 items):**
      - `TC-BB-026B-D03` (Tìm không dấu tiếng Việt): Assertion đạt yêu cầu thực tế; trạng thái nghiệp vụ ghi nhận **CHƯA ĐỦ CĂN CỨ theo BR-01** (SQLite không hỗ trợ unaccent folding).
      - `TC-BB-027G-D01` (Bộ lọc Danh sách `has:list`): Tái hiện chính xác lỗi raw `LIKE '%has:list%'`; trạng thái ghi nhận **FAIL / BUG-004 OPEN (reproduced)**.
      - `TC-BB-027E-D01` (Lọc kết hợp Hình ảnh + Từ khóa): Giữ nguyên đặc tả gốc; trạng thái ghi nhận **BLOCKED do BUG-001** (treo upload ảnh trong Editor).
  - **4 execution items giữ nguyên trạng thái Manual lịch sử:** `TC-BB-026D-D01` (Highlight từ khóa), `TC-BB-027B-D01` (Lọc ảnh), `TC-BB-027B-D02` (Lọc audio), `TC-BB-027C-D01` (Lọc nhãn). Không tự nâng kết quả Manual thành Automation.
- **Tổng kết quả tự động hóa FN-23:** **18 execution items có kịch bản automation** (15 PASS, 1 FAIL/BUG-004, 1 CHƯA ĐỦ CĂN CỨ, 1 BLOCKED).

### 12.2. Chi tiết kết quả thực thi 18 Execution Items FN-23

| # | TC / Data set | Nội dung kịch bản | Kết quả cuối | JUnit XML đối chiếu | Thời gian | Evidence đối chiếu |
|---:|---|---|:---:|---|:---:|---|
| 1 | **TC-BB-026 / D01** | Tìm kiếm theo từ khóa trong Tiêu đề (`"Lịch thi học kỳ"`) | **PASS** | [fn23_search_junit.xml](../../automation/reports/fn23_search_junit.xml) *(baseline 05/10)* | 10.42s | `evidence/fn23/FN23_TC-BB-026_D01_01.png` |
| 2 | **TC-BB-027 / D01** | Tìm kiếm theo từ khóa trong Nội dung (`"giấy in A4"`) | **PASS** | [fn23_search_junit.xml](../../automation/reports/fn23_search_junit.xml) *(baseline 05/10)* | 10.37s | `evidence/fn23/FN23_TC-BB-027_D01_01.png` |
| 3 | **TC-BB-028 / D01** | Tìm kiếm chuỗi ngẫu nhiên không tồn tại (Empty State) | **PASS** | [fn23_search_junit.xml](../../automation/reports/fn23_search_junit.xml) *(baseline 05/10)* | 10.63s | `evidence/fn23/FN23_TC-BB-028_D01_01.png` |
| 4 | **TC-BB-029 / D01** | Nhập ký tự đặc biệt & SQL Injection (`' OR '1'='1`) an toàn | **PASS** | [fn23_search_junit.xml](../../automation/reports/fn23_search_junit.xml) *(baseline 05/10)* | 10.74s | `evidence/fn23/FN23_TC-BB-029_D01_01.png` |
| 5 | **TC-BB-026B / D01** | Tìm kiếm chữ thường có dấu tiếng Việt (`"nghiên cứu"`) | **PASS** | [fn23_batch1_20261021_0325.xml](../../automation/reports/fn23_batch1_20261021_0325.xml) | 24.12s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-026B_D01_lowercase.png` |
| 6 | **TC-BB-026B / D02** | Tìm kiếm chữ HOA có dấu tiếng Việt (`"NGHIÊN CỨU"`) | **PASS** | [fn23_batch1_20261021_0325.xml](../../automation/reports/fn23_batch1_20261021_0325.xml) | 24.18s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-026B_D02_uppercase.png` |
| 7 | **TC-BB-026B / D03** | Tìm kiếm chuỗi không dấu tiếng Việt (`"nghien cuu"`) | **CHƯA ĐỦ CĂN CỨ** *(BR-01)* | [fn23_batch3_20261021_0404.xml](../../automation/reports/fn23_batch3_20261021_0404.xml) | 16.24s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-026B_D03_unaccented.png` |
| 8 | **TC-BB-026C / D01** | Tìm kiếm từ khóa tiếng Việt có dấu đầy đủ (`"kiểm thử"`) | **PASS** | [fn23_batch1_20261021_0325.xml](../../automation/reports/fn23_batch1_20261021_0325.xml) | 24.15s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-026C_D01_vietnamese.png` |
| 9 | **TC-BB-026E / D01** | Xóa nhanh từ khóa bằng nút 'X' trên thanh tìm kiếm | **PASS** | [fn23_batch1_20261021_0325.xml](../../automation/reports/fn23_batch1_20261021_0325.xml) | 24.23s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-026E_D01_clear_bar.png` |
| 10 | **TC-BB-028D / D01** | Nút mũi tên Back trên SearchBar thoát về Trang chủ | **PASS** | [fn23_batch1_20261021_0325.xml](../../automation/reports/fn23_batch1_20261021_0325.xml) | 23.89s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-028D_D01_back_home.png` |
| 11 | **TC-BB-027D / D01** | Lọc trạng thái 'Được ghim' (`is:pinned`) | **PASS** | [fn23_batch2_20261021_0402.xml](../../automation/reports/fn23_batch2_20261021_0402.xml) | 27.52s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-027D_D01_pinned_filter.png` |
| 12 | **TC-BB-027F / D01** | Gỡ bỏ từng viên Chip lọc trên thanh tìm kiếm | **PASS** | [fn23_batch2_20261021_0402.xml](../../automation/reports/fn23_batch2_20261021_0402.xml) | 26.84s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-027F_D01_remove_chip.png` |
| 13 | **TC-BB-028B / D01** | Loại trừ hoàn toàn ghi chú trong Thùng rác khỏi kết quả (0 leak) | **PASS** | [fn23_batch2_20261021_0402.xml](../../automation/reports/fn23_batch2_20261021_0402.xml) | 26.78s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-028B_D01_trash_excluded.png` |
| 14 | **TC-BB-027B / D03** | Lọc Loại đa phương tiện 'Liên kết' (`has:url`) | **PASS** | [fn23_batch2_20261021_0402.xml](../../automation/reports/fn23_batch2_20261021_0402.xml) | 28.14s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-027B_D03_url_filter.png` |
| 15 | **TC-BB-027D / D02** | Lọc trạng thái 'Lưu trữ' (`is:archived`) | **PASS** | [fn23_batch2_20261021_0402.xml](../../automation/reports/fn23_batch2_20261021_0402.xml) | 27.46s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-027D_D02_archive_filter.png` |
| 16 | **TC-BB-028C / D01** | Mở và chỉnh sửa ghi chú trực tiếp từ kết quả tìm kiếm | **PASS** | [fn23_batch2_20261021_0402.xml](../../automation/reports/fn23_batch2_20261021_0402.xml) | 27.76s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-028C_D01_edit_from_search.png` |
| 17 | **TC-BB-027G / D01** | Lọc ghi chú Checklist (`has:list`) — Tái hiện lỗi `BUG-004` | **FAIL** *(BUG-004 OPEN)* | [fn23_batch3_20261021_0404.xml](../../automation/reports/fn23_batch3_20261021_0404.xml) | 18.35s | `evidence/fn23/run_20261021_0325/FN23_TC-BB-027G_D01_list_filter_bug004.png` |
| 18 | **TC-BB-027E / D01** | Lọc kết hợp Chip 'Hình ảnh' + Từ khóa văn bản | **BLOCKED** *(BUG-001)* | [fn23_batch3_20261021_0404.xml](../../automation/reports/fn23_batch3_20261021_0404.xml) | 0.01s (skip) | Bị chặn do Editor treo khi upload ảnh (BUG-001) |

### 12.3. Phát hiện kỹ thuật & Kết luận chốt Phase 5

1. **Case-Insensitive Tiếng Việt trên SQLite Android:**
   - Qua `TC-BB-026B-D01` và `TC-BB-026B-D02`, xác minh thực tế câu lệnh SQL:
     `WHERE user_id = ? AND status != 'trash' AND (LOWER(title) LIKE ? OR LOWER(content) LIKE ?)`
     với tham số `%nghiên cứu%` và `%nghiên cứu%` (sau khi `.toLowerCase()`) hoạt động chuẩn xác trên thiết bị thực tế Samsung Galaxy S21 FE 5G, tìm thấy đúng ghi chú mục tiêu.
2. **Tìm kiếm tiếng Việt không dấu (`TC-BB-026B-D03`):**
   - Động cơ SQLite chuẩn không hỗ trợ unaccent folding mà không có extension `unaccent` tùy biến. Khi người dùng nhập `"nghien cuu"`, kết quả trả về Empty State an toàn, ứng dụng không gặp sự cố crash/lag. Theo quy tắc `BR-01`, ca này giữ nguyên trạng thái **CHƯA ĐỦ CĂN CỨ**, không tự ép PASS.
3. **Tái hiện khiếm khuyết `BUG-004` (`TC-BB-027G-D01`):**
   - Khi chọn bộ lọc "Danh sách", chuỗi token `has:list` không nằm trong danh sách bóc tách token của `local_note_service.dart`, dẫn đến việc gửi câu truy vấn SQL thô `LIKE '%has:list%'` vào cột nội dung ghi chú checklist, gây ra kết quả rỗng. Test tự động xác nhận lỗi **BUG-004 OPEN** tái hiện chính xác trên UI; không hợp thức hóa thành PASS.
4. **An toàn dữ liệu & Cách ly (0 Leak):**
   - Xác minh `TC-BB-028B-D01` kiểm chứng ghi chú bị xóa chuyển vào Thùng rác (`QA_FN23_Nghiencuu_026B`) hoàn toàn không rò rỉ vào kết quả tìm kiếm (0 leak bảo mật).
   - Tất cả fixture phục vụ kiểm thử được cô lập với tiền tố `QA_FN23_*` trên tài khoản QA đã xác minh (`student_qa@gmail.com`). Ba ghi chú `QA_PIN_024G_*` được bảo toàn toàn vẹn và phục vụ trực tiếp cho việc xác minh bộ lọc `is:pinned`.
5. **Độ bao phủ chức năng REQ-07:**
   - Chức năng **FN-23 (Tìm kiếm & Bộ lọc đa phương tiện)** đạt tỷ lệ tự động hóa **18/22 execution items** (81.82% số items được thiết kế), gồm **15 PASS**, 1 FAIL (`BUG-004`), 1 Chưa đủ căn cứ (`BR-01`), 1 BLOCKED (`BUG-001`) và 4 Manual lịch sử.
   - Hoàn thành Phase 5 — Phase Automation cuối cùng của dự án.
