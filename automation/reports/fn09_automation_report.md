# BÁO CÁO THỰC THI AUTOMATION TEST — FN-09 (EDIT NOTE / AUTO-SAVE)

**Dự án:** Smart Note App
**Nhánh:** `huong`
**Chức năng:** FN-09 — Chỉnh sửa Ghi chú & Tự động lưu
**Đợt baseline:** 05/10/2026 · **Đợt mở rộng và audit:** 20/10/2026 (UTC+7)
**Framework:** Python 3.13 + pytest + uiautomator2 + ADB
**Thiết bị:** Samsung Galaxy S21 FE 5G (serial `R5CW82ECF6M`), Android 14 (API 34)
**Nguồn:** Nhật ký pytest do tester cung cấp, kiểm kê XML latest-by-test ngày 20/10, năm screenshot audit và hồ sơ manual/defect đã gửi.

> **Lưu ý về mức chứng cứ:** Đây là kết quả của **12 test chạy riêng**, không phải một phiên chạy suite đồng thời; bản báo cáo không trực tiếp xác minh commit/APK đang cài. Các kết quả FAIL tạm thời trong quá trình phát triển script vẫn tồn tại ở XML cũ, được phân biệt với kết quả cuối.

## 1. Kết quả và phạm vi

| Giai đoạn | Mã TC duy nhất | Execution items | PASS | FAIL cuối | Nguồn |
|---|---:|---:|---:|---:|---|
| Baseline lịch sử — 05/10 | 2 | 2 | 2 | 0 | `automation/reports/fn09_edit_note_junit.xml` (lưu nguyên, không ghi đè) |
| Mở rộng — 20/10 | **11** | **12** | **12** | **0** | 12 XML tương ứng dưới đây; có cả 019G-D01 và 019G-D02 |

**Mức bao phủ theo thiết kế:** 12/12 execution items FN-09 được thực thi và có PASS cuối cùng (**100% execution-item coverage**). Không đồng nhất tỷ lệ này với code coverage, branch coverage hay mức độ hoàn thiện của mọi chức năng khác.

**Quy tắc không cộng trùng:** 019 và 020 đã nằm trong baseline. Không cộng 12 vào 2 để báo thành 14 test FN-09 hoặc cộng thêm trực tiếp vào tổng lịch sử 47 tests toàn dự án. Muốn tính latest toàn dự án phải de-duplicate bằng test identity, lớp kiểm thử và lượt thực thi.

### 1.1. Giữ nguyên chi tiết baseline lịch sử ngày 05/10/2026

| TC | Data baseline | Expected baseline | Actual ghi nhận baseline | Evidence được dẫn trong report cũ |
|---|---|---|---|---|
| TC-BB-019 | Note `Họp Lab`; bổ sung `[Đã cập nhật lúc 10:00]` | HomeScreen cập nhật preview sau khi thoát Editor | PASS: thẻ ghi chú hiển thị nội dung đã chỉnh sửa | `evidence/fn09/FN09_TC-BB-019_D01_01.png` |
| TC-BB-020 | Note `Ghi chú Auto-save`; thêm `- Nội dung kiểm tra tự động lưu`; chờ 2,0 giây | Lưu nội dung khi ngừng nhập và mở lại | PASS lịch sử: sau thời gian chờ và thao tác Back, nội dung vẫn hiển thị trong Editor khi mở lại | `evidence/fn09/FN09_TC-BB-020_D01_01.png` |

**Thời gian được report baseline ghi nhận:** 132,16 giây cho hai kịch bản. TC-BB-020 baseline **không tương đương** với TC-BB-020 mở rộng: đợt mới đã force-stop ngay tại Editor sau thời gian chờ 2,8 giây và xác minh SQLite trước khi relaunch, tạo bằng chứng trực tiếp hơn cho khả năng autosave độc lập với Back. Giữ hai mô tả riêng, không sửa kết quả gốc.


## 2. Chi tiết 12 execution items mới nhất

| TC-ID | Data | Kịch bản | Kết quả cuối | JUnit XML | Evidence mới |
|---|---|---|---|---|---|
| TC-BB-019 | D01 | Chỉnh sửa nội dung | **PASS** | [`fn09_019_20261020_025349.xml`](fn09_019_20261020_025349.xml) | `FN09_TC-BB-019_D01_01.png` đến `_03.png` |
| TC-BB-019B | D01 | Chỉnh sửa tiêu đề | **PASS** | [`fn09_019b_fixed_20261020_030253.xml`](fn09_019b_fixed_20261020_030253.xml) | `FN09_TC-BB-019B_D01_01.png` đến `_03.png` |
| TC-BB-019C | D01 | Chỉnh sửa tiêu đề và nội dung | **PASS** | [`fn09_019c_retry_20261020_031702.xml`](fn09_019c_retry_20261020_031702.xml) | `FN09_TC-BB-019C_D01_01.png` đến `_03.png` |
| TC-BB-019D | D01 | Xóa tiêu đề, giữ nội dung | **PASS** | [`fn09_019d_20261020_032717.xml`](fn09_019d_20261020_032717.xml) | `FN09_TC-BB-019D_D01_01.png` đến `_04.png` |
| TC-BB-019E | D01 | Xóa nội dung, giữ tiêu đề | **PASS** | [`fn09_019e_retry_20261020_040014.xml`](fn09_019e_retry_20261020_040014.xml) | `FN09_TC-BB-019E_D01_01.png` đến `_04.png` |
| TC-BB-019F | D01 | Xóa cả tiêu đề và nội dung | **PASS** | [`fn09_019f_20261020_041022.xml`](fn09_019f_20261020_041022.xml) | `FN09_TC-BB-019F_D01_01.png` đến `_03.png` |
| TC-BB-019G | D01 | Android System Back | **PASS** | [`fn09_019g_d01_20261020_041415.xml`](fn09_019g_d01_20261020_041415.xml) | `FN09_TC-BB-019G_D01_01.png` đến `_04.png` |
| TC-BB-019G | D02 | Android Gesture Back | **PASS** | [`fn09_019g_d02_retry_20261020_094859.xml`](fn09_019g_d02_retry_20261020_094859.xml) | `FN09_TC-BB-019G_D02_01.png` đến `_04.png` |
| TC-BB-020 | D01 | Auto-save độc lập, force-stop ngay tại Editor | **PASS** | [`fn09_020_20261020_031828.xml`](fn09_020_20261020_031828.xml) | `FN09_TC-BB-020_D01_01.png` đến `_04.png` |
| TC-BB-020B | D01 | Hai lần chỉnh sửa liên tiếp | **PASS** | [`fn09_020b_20261020_095438.xml`](fn09_020b_20261020_095438.xml) | `FN09_TC-BB-020B_D01_01.png` đến `_05.png` |
| TC-BB-020C | D01 | Unicode, emoji và ký tự đặc biệt | **PASS** | [`fn09_020c_20261020_095808.xml`](fn09_020c_20261020_095808.xml) | `FN09_TC-BB-020C_D01_01.png` đến `_04.png` |
| TC-BB-020D | D01 | Lưu bền vững sau khởi động lại | **PASS** | [`fn09_020d_20261020_100042.xml`](fn09_020d_20261020_100042.xml) | `FN09_TC-BB-020D_D01_01.png` đến `_05.png` |

Các XML cùng nằm trong `automation/reports/`. Bảng lấy **kết quả cuối theo đúng hàm pytest**, không loại khỏi lịch sử các lần retry từng FAILED trước đó. 019G có một ID test case và **hai Data ID**.

## 3. Cơ chế kiểm thử và oracle

- **Thao tác UI/E2E:** Tạo ghi chú QA có title marker riêng, xác minh ID mới qua chênh lệch SQLite trước/sau; mở chính ghi chú theo NoteCard; nhập Title/Quill, thoát hoặc khởi động lại theo bước kịch bản.
- **Dữ liệu SQLite chỉ đọc:** `adb exec-out run-as com.example.smart_note_app cat databases/smart_note.db` rồi đọc snapshot trong Python `sqlite3.connect(":memory:").deserialize(...)`; xác minh `note_id`, `status`, `title` và plain text từ Quill Delta. Oracle nội bộ này là bổ trợ, vì vậy các test **không thuần black-box** dù tương tác đầu vào sử dụng UI.
- **TC-BB-020:** Chỉnh sửa trong Editor, chờ **2,8 giây** rồi force-stop **không nhấn Back**; xác minh đã lưu qua SQLite trước lần mở ứng dụng kế tiếp; kiểm tra thêm HomeScreen và reopened Editor sau khi khởi động lại.
- **TC-BB-020B:** Lưu và kiểm tra dữ liệu chính xác sau từng lần chỉnh sửa liên tiếp trên cùng ID.
- **TC-BB-020C:** Bảo toàn chuỗi `\n[Cập nhật 🚀: Đạt 100% mục tiêu! @QA #2026]` qua SQLite sau lưu và mở lại. Kiểm tra UI qua accessibility và ảnh; emoji non-BMP có thể không hiển thị nguyên vẹn trong XML accessibility nên không dùng XML làm oracle byte-exact cho emoji.
- **TC-BB-020D:** Force-stop từ HomeScreen rồi khởi động lại, kiểm tra đúng ID/nội dung qua NoteCard, reopened Editor và SQLite.
- **Dữ liệu QA:** Các lượt chạy sử dụng `FN09_DEBUG=1`: test-owned notes được giữ lại để audit, không tự xóa hết; cần kiểm kê và xác minh đúng ID trước khi cleanup qua UI.

## 4. Kiểm tra ảnh evidence và lỗi UI

Đã kiểm tra trực tiếp **5 ảnh** được tester cung cấp, ánh xạ theo tên file:

| Test | Ảnh | Quan sát có thể kết luận |
|---|---|---|
| 019D | `FN09_TC-BB-019D_D01_02.png` | Tại thời điểm chụp, không thấy rõ RenderFlex Overflow |
| 019E | `FN09_TC-BB-019E_D01_02.png` | Tại thời điểm chụp, không thấy rõ RenderFlex Overflow |
| 019F | `FN09_TC-BB-019F_D01_02.png` | Tại thời điểm chụp, không thấy rõ RenderFlex Overflow |
| 020C | `FN09_TC-BB-020C_D01_03.png` | Có bằng chứng hiển thị Unicode/emoji khi xem thẻ ghi chú |
| 020C | `FN09_TC-BB-020C_D01_04.png` | Có bằng chứng hiển thị Unicode/emoji sau khi mở Editor |

**Không đóng bug giao diện.** Manual sheet có nhãn `BUG-BB-FN09-01` cho 019D/E/F; defect log tập trung dùng mã chính thức `BUG-005` và mô tả lỗi layout thoáng qua ~0,3–0,5 giây ở 019D/E, riêng trường hợp xóa cả hai (019F) được ghi không tái hiện. Khác biệt 019F **chưa được giải quyết**. Ảnh tĩnh không chứng minh lỗi thoáng qua đã được sửa, vì vậy `BUG-005` vẫn **OPEN**; cần video và logcat retest riêng.

**Đường dẫn evidence gốc mới:** `evidence/fn09/automation_<RUN_ID>/TC-BB-<TC-ID>/FN09_<TC-ID>_<Data-ID>_<seq>.png`. Ảnh gốc trong thư mục có `RUN_ID`; năm ảnh được gom để audit trong `automation/reports/fn09_evidence_audit_20261020_100542.zip`. Không lấy ảnh gốc của lượt chạy cũ để thay cho ảnh mới.

## 5. Phân biệt kết quả lịch sử và kết quả cuối

Trong quá trình xây dựng script có các lần FAILED/BLOCKED do tiền điều kiện HomeScreen, selector hoặc việc kiểm tra Title qua Accessibility XML khi bàn phím đang mở; đây là kết quả **các lần chạy lịch sử**, không xóa JUnit cũ hoặc đổi nhãn sang PASS. Những trường hợp đã có lượt chạy mới PASS sau sửa script được dùng làm trạng thái automation mới nhất. Test 019F xác nhận đúng note ID đã chuyển sang `status='trash'` khi Title và Content cùng rỗng.

## 6. Kết luận và công việc còn lại

- **Đạt về execution:** 11 TC duy nhất / 12 execution items, **12 PASS cuối** trong các JUnit riêng, đã đối chiếu 5/5 screenshot audit; không có FAIL cuối trong tập này.
- **Còn điều kiện để nghiệm thu defect:** Retest video/logcat cho `BUG-005` và xác minh liệu nhãn `BUG-BB-FN09-01` là alias hay là lỗi khác; đặc biệt khác biệt báo cáo cho 019F.
- **Còn housekeeping:** Kiểm kê/cleanup những QA notes còn tồn tại theo ID và lưu bằng chứng, không tác động ghi chú cá nhân; có thể chạy regression trọn suite nếu mục tiêu cần kết quả của một build duy nhất.
- **Hồ sơ đồng bộ:** `docs/qa/automation_execution_summary.md`, `docs/test_cases/black_box/fn09_execution_sheet.md`, `docs/bugs/defect_log.md`.

**Phạm vi đóng đợt:** Chốt *kết quả thực thi automation FN-09*, **không** tuyên bố đã đóng mọi defect UI hay nghiệm thu toàn bộ ứng dụng.