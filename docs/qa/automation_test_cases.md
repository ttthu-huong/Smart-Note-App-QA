# ĐẶC TẢ KIỂM THỬ TỰ ĐỘNG (AUTOMATION TEST CASES)

**Dự án:** Smart Note App · **Nhánh:** `huong` · **Phiên bản:** 1.4 · **Cập nhật Phase 4 (FN-20):** 20/10/2026 (UTC+7)
**Mã nguồn và bằng chứng được đối chiếu:** `98abb5af577b2d38192e7a88e7ff94a2b5f77262` (baseline) và các đợt thực thi mở rộng ngày 20/10/2026 trên thiết bị Android thật (đối chiếu toàn bộ JUnit XML và cây thư mục evidence tương ứng).
**Bố cục tài liệu:** **FN-01..FN-44 → Chi tiết kịch bản → Preconditions, Test Data, Steps, Expected Result, Test Script, Code Status, Execution Result, Evidence**.
**Phạm vi:** Đặc tả chi tiết cho **31 Test Cases UI/E2E baseline**, **32 Execution Items mở rộng Phase 2 (FN-08..12: 31 PASS, 1 BLOCKED)**, **5 Execution Items mở rộng Phase 3 (FN-13..14: 5 PASS)**, **15 Execution Items mở rộng Phase 4 (FN-20: 15 PASS)** và **24 Tests Provider** (`PV-REF-01` đến `PV-REF-24`).

---

> **Quy ước bằng chứng:** Kết quả UI bên dưới được đối chiếu với 9 XML baseline lịch sử và các JUnit XML mở rộng ngày 20/10/2026 (FN-08: 8 PASS, FN-09: 12 PASS, FN-10: 5 PASS, FN-11: 2 PASS / 1 BLOCKED, FN-12: 4 PASS, FN-13: 3 PASS, FN-14: 2 PASS, FN-20: 15 PASS). Provider có 24 bài test được đối chiếu với file log máy `evidence/automated/automated_test_run.log` (log lịch sử xác nhận 24 PASS; chưa xác minh chính xác commit thực thi, không coi thiếu JUnit XML là thiếu bắt buộc; file log đã được đưa vào staging git via `git add -f`). Các bảng mô tả phạm vi assertion của script, không khẳng định bao phủ toàn bộ FN.

> **Phạm vi mở rộng cũng đang được quản lý:** Ngoài baseline 31 TC UI, hồ sơ Phase 3C chọn 61 TC/74 executions; Phase 4 báo cáo 14 TC/20 executions (19 PASS, 1 FAIL-APP) cùng 3 ca thăm dò riêng. Kết quả Phase 4 được báo cáo cùng ảnh chụp màn hình nhưng chưa đối chiếu được log console hoặc file XML thực thi của đợt này; không coi ảnh là bằng chứng đầy đủ cho mọi assertion logic. Giữ riêng kết quả FAIL baseline trong XML (04/10/2026) và PASS retest được Phase 4 báo cáo (13/10/2026) của TC-BB-006; không tự ý ghi đè. Xem [ma trận mở rộng và nguồn](automation_expanded_scope.md).


## 1. Nguyên tắc định danh và Ranh giới đặc tả

1. **Kiểm kê toàn bộ 44 FN:** Danh sách kiểm kê bao gồm đầy đủ 44 chức năng hệ thống (FN-01 đến FN-44). Những chức năng chưa có kịch bản tự động hóa vẫn được ghi nhận danh mục và trạng thái rõ ràng, không tạo kịch bản giả để lấp đầy.
2. **31 Test Cases UI/E2E:** Kế thừa mã định danh `TC-BB-001` đến `TC-BB-031` từ bộ kịch bản hộp đen chuẩn để đảm bảo tính truy vết (Traceability). Trong đó:
   - **23 Test Cases** có XML thực thi: 19 PASS, 4 FAIL; FN-10/11/12 đã có kết quả PASS.
   - Script hiện tại có thêm các hàm mở rộng/alias ngoài baseline; xem [kiểm kê script](automation_script_inventory.md). Có mã không đồng nghĩa có bằng chứng chạy.
   - **8 Test Cases** tạm hoãn do độ phức tạp ngoại vi (DEFERRED / NOT RUN).
3. **24 Tests Provider:** Được đánh mã tham chiếu **`PV-REF-01` đến `PV-REF-24`** trong tài liệu này, tương ứng chính xác với 24 bài test trong `test/automated/note_provider_test.dart` (15 tests) và `test/automated/sync_provider_test.dart` (9 tests). Đã đối chiếu với log thực thi cục bộ `evidence/automated/automated_test_run.log` (24 PASS, ngày 12/10/2026; file untracked do `.gitignore`).
4. **Phân tách Code Status và Execution Result:**
   - **Code Status:** `DONE` (đã viết mã), `PLANNED` (trong kế hoạch), `DEFERRED` (tạm hoãn). Các kịch bản thăm dò (`exploratory`) không được coi là DONE.
   - **Execution Result:** `PASS`, `FAIL`, `NOT RUN`; theo dõi riêng mức xác minh bằng chứng (`XML ĐÃ ĐỐI CHIẾU`, `LOG CỤC BỘ ĐÃ ĐỐI CHIẾU`, `CHƯA CÓ XML TƯƠNG ỨNG`). Tuyệt đối không biến kịch bản chưa chạy thành PASS.
5. **Ranh giới với Black-box Test Suite:** `automation_test_cases.md` là tài liệu đặc tả kỹ thuật riêng cho kiểm thử tự động. Tài liệu [`test_cases/black_box/black_box_test_cases.md`](../test_cases/black_box/black_box_test_cases.md) vẫn là nguồn đặc tả chính thức và chuẩn mực cao nhất của Black-box Testing toàn dự án.

---

## 2. Cấu trúc thuộc tính chuẩn của mỗi Test Case

| Thuộc tính | Ý nghĩa / Phương pháp xác minh |
| --- | --- |
| **Mã định danh** | `TC-BB-xxx` (UI) hoặc `PV-REF-xx` (Provider), liên kết FN chính và FN phụ |
| **Mục tiêu kiểm thử** | Tóm tắt hành vi hoặc logic nghiệp vụ cần kiểm chứng |
| **Điều kiện & Dữ liệu** | Preconditions cần thiết và Test Data cụ thể (email, password, title, content...) |
| **Các bước thực hiện** | Chuỗi thao tác kịch bản UI hoặc lời gọi phương thức Provider |
| **Kết quả kỳ vọng** | Expected Result / Assertion theo đặc tả nguồn |
| **Thông tin tự động** | Đường dẫn tệp kịch bản (`Script Path`), nhóm test / tên hàm |
| **Trạng thái & Kết quả** | Code Status (`DONE/PLANNED/DEFERRED`), Result (`PASS/FAIL/NOT RUN`), Evidence |

---

## 3. Đặc tả chi tiết kịch bản tự động hóa theo 44 FN

### FN-01 — Kiểm tra hợp lệ form đăng nhập (theo inventory hiện hành)
> Chưa có kịch bản kiểm thử tự động ở tầng UI hoặc Provider trong baseline; được kiểm thử thông qua Black-box Manual Testing.

---

### FN-02 — Đăng ký tài khoản Email/Password
**Tầng kiểm thử:** Android UI/E2E · **Công cụ:** Python 3.13 + pytest + uiautomator2 + ADB · **Script:** `automation/tests/test_fn02_register.py`

| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-001** | Đăng ký tài khoản với Email và Mật khẩu hợp lệ | **Pre:** Thiết bị có mạng; email chưa đăng ký.<br>**Data:** `student_qa_<ts>@gmail.com` / `123456` | Mở tab Đăng ký $\rightarrow$ nhập email/mật khẩu $\rightarrow$ bấm "Đăng ký" | Ứng dụng tạo tài khoản thành công và chuyển sang màn hình Xác thực Email (`EmailVerificationScreen`) | P1 | DONE | **PASS** | `evidence/fn02/FN02_TC-BB-001_D01_01.png` |
| **TC-BB-002** | Chặn đăng ký khi bỏ trống toàn bộ dữ liệu | **Pre:** Đang ở tab Đăng ký.<br>**Data:** Email = `""`, Password = `""` | Để trống cả 2 ô $\rightarrow$ bấm "Đăng ký" | Chặn gửi form; xuất hiện thông báo lỗi đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | P1 | DONE | **PASS** | `evidence/fn02/FN02_TC-BB-002_D01_01.png` |
| **TC-BB-003** | Từ chối email không hợp lệ (thiếu `@`) | **Pre:** Đang ở tab Đăng ký.<br>**Data:** Email = `nguoidung_gmail.com` / `123456` | Nhập email thiếu `@` $\rightarrow$ bấm "Đăng ký" | Xuất hiện thông báo lỗi đỏ: *"Định dạng email không hợp lệ."* theo đặc tả gốc | P1 | DONE | **FAIL** | `evidence/fn02/FN02_TC-BB-003_D01_01.png` |
| **TC-BB-004** | Chặn đăng ký khi mật khẩu dưới 6 ký tự | **Pre:** Đang ở tab Đăng ký.<br>**Data:** Email hợp lệ / Password = `12345` (5 ký tự) | Nhập email đúng, mật khẩu 5 ký tự $\rightarrow$ bấm "Đăng ký" | Chặn đăng ký; hiển thị thông báo lỗi đỏ: *"Mật khẩu quá yếu (cần ít nhất 6 ký tự)."* | P1 | DONE | **PASS** | `evidence/fn02/FN02_TC-BB-004_D02_01.png` |
| **TC-BB-005** | Báo lỗi khi đăng ký bằng Email đã tồn tại | **Pre:** Tài khoản test đã tồn tại trên hệ thống.<br>**Data:** Email trùng lặp / Password hợp lệ | Nhập email đã tồn tại $\rightarrow$ bấm "Đăng ký" | Chặn đăng ký; hiển thị thông báo lỗi đỏ: *"Email này đã được sử dụng cho một tài khoản khác."* | P1 | DONE | **PASS** | `evidence/fn02/FN02_TC-BB-005_D01_01.png` |

*Ghi chú thực thi FN-02:*
- `TC-BB-003` ghi nhận **FAIL**: Ứng dụng hiển thị thông báo *"Không hỗ trợ tên miền email rác này..."* thay vì *"Định dạng email không hợp lệ."*. Báo cáo automation ghi nhận lỗi phân loại `BUG-FN02-01` (cần đối chiếu với Defect Log). Giữ nguyên Expected Result theo đặc tả, không ép PASS.

---

### FN-03 — Xác thực email
> Chưa có kịch bản kiểm thử tự động ở tầng UI hoặc Provider trong baseline; việc gửi email trong luồng đăng ký không chứng minh đã hoàn thành toàn bộ luồng xác thực email.

---

### FN-04 — Đăng nhập tài khoản Email/Password
**Tầng kiểm thử:** Android UI/E2E · **Công cụ:** Python 3.13 + pytest + uiautomator2 + ADB · **Script:** `automation/tests/test_fn04_login.py`

| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-006** | Đăng nhập thành công với tài khoản Email hợp lệ | **Pre:** Tài khoản test đã kích hoạt email (`emailVerified: true`).<br>**Data:** `student_qa@gmail.com` / `123456` | Nhập email/mật khẩu đúng $\rightarrow$ bấm "Đăng nhập" | Ứng dụng điều hướng người dùng vào màn hình Trang chủ (`HomeScreen`) | P1 | DONE | **FAIL** | `evidence/fn04/FN04_TC-BB-006_D01_01.png` |
| **TC-BB-007** | Đăng nhập thất bại do sai Mật khẩu | **Pre:** Email tồn tại trên hệ thống.<br>**Data:** Email đúng / Mật khẩu sai (`WrongPass999`) | Nhập email đúng, mật khẩu sai $\rightarrow$ bấm "Đăng nhập" | Hiển thị thông báo lỗi riêng biệt: *"Mật khẩu không chính xác."* theo đặc tả gốc | P1 | DONE | **FAIL** | `evidence/fn04/FN04_TC-BB-007_D01_01.png` |
| **TC-BB-008** | Đăng nhập thất bại do tài khoản không tồn tại | **Pre:** Email chưa từng đăng ký.<br>**Data:** `ghost_user@gmail.com` / `123456` | Nhập email chưa tạo $\rightarrow$ bấm "Đăng nhập" | Hiển thị thông báo lỗi riêng biệt: *"Tài khoản không tồn tại. Vui lòng kiểm tra lại email."* | P1 | DONE | **FAIL** | `evidence/fn04/FN04_TC-BB-008_D01_01.png` |
| **TC-BB-009** | Đăng nhập thất bại do để trống Mật khẩu | **Pre:** Đang ở tab Đăng nhập.<br>**Data:** Email hợp lệ / Password = `""` | Nhập email, bỏ trống mật khẩu $\rightarrow$ bấm "Đăng nhập" | Client validation chặn form; hiển thị thông báo lỗi đỏ: *"Vui lòng nhập đầy đủ Email và Mật khẩu."* | P1 | DONE | **PASS** | `evidence/fn04/FN04_TC-BB-009_D01_01.png` |

*Ghi chú thực thi FN-04:*
- `TC-BB-006` ghi nhận **FAIL do Precondition Issue**: Tài khoản test dùng trong kịch bản có trạng thái `emailVerified: false`, dẫn tới việc ứng dụng chuyển hướng sang màn hình Xác thực email thay vì HomeScreen. Đây là hành vi đúng của ứng dụng khi gặp tài khoản chưa kích hoạt, cần retest với tài khoản `emailVerified: true`, không tự ý kết luận là lỗi ứng dụng.
- `TC-BB-007` và `TC-BB-008` ghi nhận **FAIL**: Ứng dụng hiển thị thông báo gộp của Firebase: *"Email hoặc mật khẩu không chính xác."*. Báo cáo automation cũ từng tạm gán mã `BUG-BB-003` và `BUG-BB-002`, tuy nhiên cần lưu ý các mã này chưa có hồ sơ riêng trong Defect Log chính thức; `BUG-BB-002/003` là mã khác với `BUG-002/003` (Tombstone sync/Pull-to-refresh), không gộp hoặc suy diễn tương đương. Thông báo gộp có thể hạn chế suy đoán tài khoản; cần người phụ trách yêu cầu xác nhận tiêu chí thông báo. Giữ nguyên FAIL lịch sử, không tự đổi Expected hoặc kết luận chính sách đã được phê duyệt.

---

### FN-05 — Đăng nhập nhanh Google OAuth
**Tầng kiểm thử:** Android UI/E2E · **Công cụ:** Python + uiautomator2 · **Script:** `automation/tests/test_fn05_google_oauth.py` (Script thăm dò khả thi)

| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-010** | Đăng nhập thành công qua tài khoản Google | **Pre:** Thiết bị có tài khoản Google; dialog hệ thống có thể tương tác | Bấm nút "Đăng nhập bằng Google" $\rightarrow$ chọn tài khoản | Đăng nhập thành công, đồng bộ dữ liệu và vào HomeScreen | P1 | DEFERRED | **NOT RUN** | — |
| **TC-BB-011** | Hủy quá trình đăng nhập Google | **Pre:** Dialog chọn tài khoản Google đang hiển thị | Nhấn nút Back / Hủy bỏ dialog chọn tài khoản | Dialog đóng lại; giữ nguyên màn hình Đăng nhập ổn định, không crash | P1 | DEFERRED | **NOT RUN** | — |

---

### FN-06 — Đặt lại mật khẩu
> Chưa có kịch bản kiểm thử tự động ở tầng UI hoặc Provider trong baseline; việc mở hộp thoại không chứng minh đã gửi và hoàn thành đặt lại mật khẩu.

---

### FN-07 — Đăng xuất tài khoản
> Chưa có kịch bản kiểm thử tự động ở tầng UI hoặc Provider trong baseline; được kiểm thử thủ công qua màn hình Quản lý tài khoản.

---

### FN-08 — Tạo ghi chú văn bản
**Tầng kiểm thử:** Đa tầng (Android UI/E2E + Flutter Provider Testing)

#### 1. Kịch bản UI/E2E (`automation/tests/test_fn08_create_note.py`):
| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-016** | Tạo ghi chú văn bản có Tiêu đề và Nội dung | **Pre:** Đã đăng nhập; ở HomeScreen.<br>**Data:** Title="Họp Lab" / Content="Nội dung ngắn gọn" | Nhấn FAB (+) $\rightarrow$ nhập title/content $\rightarrow$ bấm Back | Thẻ ghi chú hiển thị đầy đủ tiêu đề "Họp Lab" và nội dung "Nội dung ngắn gọn" | P1 | DONE | **PASS** | `evidence/fn08/FN08_TC-BB-016_D01_01.png` |
| **TC-BB-017** | Tạo ghi chú không có tiêu đề nhưng có nội dung | **Pre:** Đã đăng nhập; ở HomeScreen.<br>**Data:** Title="" / Content="Ý tưởng nhanh không tiêu đề" | Nhấn FAB (+) $\rightarrow$ chỉ nhập content $\rightarrow$ bấm Back | Ứng dụng tạo note và hiển thị preview nội dung trên HomeScreen | P1 | DONE | **PASS** | `evidence/fn08/FN08_TC-BB-017_D01_01.png` |
| **TC-BB-018** | Không tạo ghi chú rỗng khi để trống cả 2 ô | **Pre:** Đã đăng nhập; ghi nhận số note hiện có.<br>**Data:** Title="" / Content="" | Nhấn FAB (+) $\rightarrow$ không nhập gì $\rightarrow$ bấm Back | Ứng dụng không tạo bất kỳ ghi chú rỗng nào trên HomeScreen | P1 | DONE | **PASS** | `evidence/fn08/FN08_TC-BB-018_D01_01.png` |

#### 2. Kịch bản UI/E2E Mở rộng (`automation/tests/test_fn08_extended.py`):
| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-018B** | Tạo ghi chú chỉ có Tiêu đề | **Pre:** Ở HomeScreen.<br>**Data:** Title="Nhắc nhở họp gấp" / Content="" | Mở Editor $\rightarrow$ nhập title $\rightarrow$ Back | Thẻ ghi chú hiển thị đúng tiêu đề; mở lại note kiểm tra dữ liệu | P1 | DONE | **PASS** | `evidence/fn08/FN08_TC-BB-018B_D01_01.png`, `automation/reports/fn08_probe_20261020_001621.xml` (49.34s) |
| **TC-BB-018C** | Tự động lưu ngầm không cần bấm Back | **Pre:** Ở HomeScreen.<br>**Data:** Title="Ghi chú autosave kiểm chứng" / Content="..." | Nhập title + content $\rightarrow$ chờ 3.0s $\rightarrow$ Force-stop tại Editor $\rightarrow$ Mở lại app | Ghi chú tồn tại trên HomeScreen và mở lại có đủ nội dung | P1 | DONE | **PASS** | `evidence/fn08/FN08_TC-BB-018C_D01_01.png`, `automation/reports/fn08_remaining_20261020_001724.xml` (58.64s) |
| **TC-BB-018D** | Hủy bản nháp khi xóa sạch về rỗng | **Pre:** Ở HomeScreen.<br>**Data:** Title="Tạm" / Content="Tạm" $\rightarrow$ Xóa sạch | Nhập text $\rightarrow$ chờ lưu draft $\rightarrow$ Xóa sạch cả 2 ô $\rightarrow$ Back | Bản nháp bị hủy, không tạo ghi chú rỗng trên HomeScreen | P1 | DONE | **PASS** | `evidence/fn08/FN08_TC-BB-018D_D01_01.png`, `automation/reports/fn08_remaining_20261020_001724.xml` (25.96s) |
| **TC-BB-018E** | Xử lý Unicode phức tạp, tiếng Việt, emoji, HTML-like text | **Pre:** Ở HomeScreen, không có ghi chú trùng lặp.<br>**Data:** Title="LongText_UTF8_Emoji_🚀_#2026", Content=11 dòng Unicode/Emoji/HTML-like | Nhập title $\rightarrow$ Paste Quill 11 dòng $\rightarrow$ Save & exit $\rightarrow$ Oracle SQLite kiểm tra $\rightarrow$ Mở lại note | Tiêu đề khớp 100% (emoji 🚀), đủ 11 dòng, tiếng Việt, ký tự đặc biệt, HTML-like text; giao diện mở lại được (UI + SQLite Oracle) | P1 | DONE | **PASS (UI + SQLite Oracle)** | `evidence/fn08/automation_20261020_015419_043437/` (6 ảnh), `automation/reports/fn08_018e_final_20261020_015417.xml` (42.53s) |
| **TC-BB-018F** | Tính bền vững của ghi chú sau khi restart | **Pre:** Ở HomeScreen.<br>**Data:** Note ngẫu nhiên với UUID | Tạo note $\rightarrow$ Force-stop app $\rightarrow$ Relaunch $\rightarrow$ Kiểm tra Home & mở lại note | Ghi chú bảo toàn đầy đủ dữ liệu sau khi khởi động lại app | P1 | DONE | **PASS** | `evidence/fn08/FN08_TC-BB-018F_D01_01.png`, `automation/reports/fn08_remaining_20261020_001724.xml` (53.66s) |

*Ghi chú FN-08 chốt thực thi:*
- FN-08 đạt **8/8 test cases PASS** (3 baseline tại `test_fn08_create_note.py` + 5 mở rộng tại `test_fn08_extended.py`).
- Riêng TC-BB-018E được thực thi bằng phương pháp **UIAutomator2 kết hợp SQLite verification oracle chỉ đọc** (`adb exec-out run-as` + `sqlite3.deserialize()`), do Android Accessibility XML thay thế emoji ngoài BMP bằng hai dấu chấm `..`. Cơ chế này là kiểm thử UI có kiểm chứng dữ liệu nội bộ bổ sung, không gọi là kiểm thử hộp đen thuần túy.
- *Lưu ý về phạm vi bao phủ:* Việc 8/8 test case PASS khẳng định độ bao phủ toàn diện cho các luồng nghiệp vụ người dùng và dữ liệu biên được thiết kế trong bộ Black-box Test Cases, **tuyệt đối không tuyên bố code coverage 100%** (kiểm thử black-box/E2E không bao phủ toàn bộ các nhánh rẽ lỗi exception, network failure hay mã nội bộ của tầng ứng dụng và Provider).

#### 3. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-06** | `NoteProvider - Create and Edit note` | Tạo ghi chú mới thành công | `provider.addNote(note)` | Note được lưu vào repository và xuất hiện trong `provider.notes` | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |

---

### FN-09 — Chỉnh sửa và tự động lưu ghi chú
**Tầng kiểm thử:** Đa tầng (Android UI/E2E + Flutter Provider Testing) · **Script:** `automation/tests/test_fn09_edit_note.py`

#### 1. Kịch bản UI/E2E:
| TC-ID | Dataset | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence & JUnit XML |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-019** | **D01** | Chỉnh sửa nội dung ghi chú có sẵn | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Thêm nội dung `"[Đã cập nhật lúc 10:00]"` | Mở note $\rightarrow$ sửa nội dung $\rightarrow$ bấm Back về Home | Thẻ ghi chú trên HomeScreen cập nhật chính xác nội dung mới | P1 | DONE | **PASS** | `evidence/fn09/automation_20261020_025350_985392_2c7d2b87/`, `FN09_TC-BB-019_D01_01.png`<br>[fn09_019_20261020_025349.xml](../../automation/reports/fn09_019_20261020_025349.xml) (46.40s) |
| **TC-BB-019B** | **D01** | Chỉ đổi tiêu đề; giữ nguyên nội dung | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Tiêu đề mới `"Kế hoạch tuần - Đã duyệt"` | Mở note $\rightarrow$ đổi tiêu đề $\rightarrow$ giữ nguyên nội dung $\rightarrow$ Back | Tiêu đề mới cập nhật trên HomeScreen; phần xem trước nội dung giữ nguyên | P1 | DONE | **PASS** | `evidence/fn09/automation_20261020_030254_716373_ac23e584/`<br>[fn09_019b_fixed_20261020_030253.xml](../../automation/reports/fn09_019b_fixed_20261020_030253.xml) (68.81s) |
| **TC-BB-019C** | **D01** | Đổi đồng thời cả tiêu đề và nội dung | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Title mới + Content mới | Mở note $\rightarrow$ sửa cả title và content $\rightarrow$ Back | Thẻ ghi chú cập nhật cả tiêu đề mới và nội dung mới; mở lại note khớp 100% | P1 | DONE | **PASS** | `evidence/fn09/automation_20261020_031703_633145_ef50e8ff/`<br>[fn09_019c_retry_20261020_031702.xml](../../automation/reports/fn09_019c_retry_20261020_031702.xml) (44.79s) |
| **TC-BB-019D** | **D01** | Xóa tiêu đề về rỗng; giữ nguyên nội dung | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Title = `""`, giữ content | Mở note $\rightarrow$ xóa sạch title $\rightarrow$ giữ content $\rightarrow$ Back | Ghi chú không bị mất; thẻ ghi chú dùng nội dung làm đoạn preview | P1 | DONE | **PASS** | `evidence/fn09/automation_20261020_032718_614397_0fc1d6b5/` (ảnh audit 02)<br>[fn09_019d_20261020_032717.xml](../../automation/reports/fn09_019d_20261020_032717.xml) (43.06s) |
| **TC-BB-019E** | **D01** | Xóa nội dung về rỗng; giữ nguyên tiêu đề | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Giữ title, Content = `""` | Mở note $\rightarrow$ giữ title $\rightarrow$ xóa sạch content $\rightarrow$ Back | Ghi chú vẫn tồn tại; thẻ ghi chú chỉ hiển thị tiêu đề, preview rỗng | P1 | DONE | **PASS** | `evidence/fn09/automation_20261020_040016_148745_d1062ac5/` (ảnh audit 02)<br>[fn09_019e_retry_20261020_040014.xml](../../automation/reports/fn09_019e_retry_20261020_040014.xml) (55.19s) |
| **TC-BB-019F** | **D01** | Xóa cả tiêu đề và nội dung về rỗng | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Title = `""`, Content = `""` | Mở note $\rightarrow$ xóa sạch title và content $\rightarrow$ Back | Ghi chú rỗng bị xóa hoàn toàn khỏi HomeScreen (chuyển trash trong SQLite) | P1 | DONE | **PASS** | `evidence/fn09/automation_20261020_041023_362641_4e744850/` (ảnh audit 02)<br>[fn09_019f_20261020_041022.xml](../../automation/reports/fn09_019f_20261020_041022.xml) (42.03s) |
| **TC-BB-019G** | **D01** | Thoát lưu chỉnh sửa bằng Android System Back | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Thêm nội dung thoát System Back | Mở note $\rightarrow$ sửa content $\rightarrow$ bấm nút Back hệ thống Android | Quay về HomeScreen, nội dung sửa đổi được lưu và bảo toàn khi mở lại | P1 | DONE | **PASS** | `evidence/fn09/automation_20261020_041416_237915_e5a52ab0/`<br>[fn09_019g_d01_20261020_041415.xml](../../automation/reports/fn09_019g_d01_20261020_041415.xml) (52.06s) |
| **TC-BB-019G** | **D02** | Thoát lưu chỉnh sửa bằng Android Gesture Back | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Thêm nội dung thoát Gesture Back | Mở note $\rightarrow$ sửa content $\rightarrow$ vuốt mép màn hình Gesture Back | Quay về HomeScreen, nội dung sửa đổi được lưu và bảo toàn khi mở lại | P1 | DONE | **PASS** | `evidence/fn09/automation_20261020_094901_092380_3febeb92/`<br>[fn09_019g_d02_retry_20261020_094859.xml](../../automation/reports/fn09_019g_d02_retry_20261020_094859.xml) (48.55s) |
| **TC-BB-020** | **D01** | Tự động lưu sau độ trễ (Autosave Debounce 2.8s) | **Pre:** Mở ghi chú trong Editor.<br>**Data:** Nhập thêm nội dung, không bấm Back | Nhập content mới $\rightarrow$ chờ 2.8s $\rightarrow$ Force-stop app tại Editor $\rightarrow$ Mở lại | Nội dung mới tồn tại nguyên vẹn sau khi mở lại app dù không bấm Back | P1 | DONE | **PASS** | `evidence/fn09/automation_20261020_031829_739761_dd030562/`, `FN09_TC-BB-020_D01_01.png`<br>[fn09_020_20261020_031828.xml](../../automation/reports/fn09_020_20261020_031828.xml) (48.89s) |
| **TC-BB-020B** | **D01** | Chỉnh sửa tuần tự 2 lần liên tiếp trên cùng 1 note | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Lần 1: thêm đợt 1; Lần 2: thêm đợt 2 | Sửa lần 1 $\rightarrow$ Back $\rightarrow$ Mở lại sửa lần 2 $\rightarrow$ Back $\rightarrow$ Mở lại | Cả hai lần chỉnh sửa đều được lưu tuần tự, không bị ghi đè hay mất dữ liệu | P1 | DONE | **PASS** | `evidence/fn09/automation_20261020_095440_379178_437e76e5/`<br>[fn09_020b_20261020_095438.xml](../../automation/reports/fn09_020b_20261020_095438.xml) (56.40s) |
| **TC-BB-020C** | **D01** | Xử lý Unicode, tiếng Việt có dấu, emoji 🚀, ký tự đặc biệt | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Chuỗi Unicode, emoji 🚀, ký tự `@QA #2026` | Nhập chuỗi Unicode/emoji $\rightarrow$ Back $\rightarrow$ Kiểm tra Home & mở lại note | Thẻ ghi chú và Editor hiển thị hoàn hảo chuỗi Unicode và emoji 🚀; không vỡ font | P1 | DONE | **PASS** | `evidence/fn09/automation_20261020_095810_612309_3146c2ce/` (ảnh audit 03, 04)<br>[fn09_020c_20261020_095808.xml](../../automation/reports/fn09_020c_20261020_095808.xml) (42.00s) |
| **TC-BB-020D** | **D01** | Tính bền vững của nội dung chỉnh sửa sau khi restart | **Pre:** Ghi chú đã chỉnh sửa thành công trên Home.<br>**Data:** Note đã sửa dữ liệu | Force-stop app $\rightarrow$ Relaunch $\rightarrow$ Kiểm tra thẻ trên Home & mở lại Editor | Toàn bộ dữ liệu chỉnh sửa được bảo toàn nguyên vẹn sau khi restart app | P1 | DONE | **PASS** | `evidence/fn09/automation_20261020_100044_765185_4c77ba97/`<br>[fn09_020d_20261020_100042.xml](../../automation/reports/fn09_020d_20261020_100042.xml) (52.86s) |

*Ghi chú FN-09:*
- Đạt **12/12 execution items PASS**.
- Khiếm khuyết giao diện **BUG-005** (RenderFlex Overflow / dải vàng đen thoáng qua khi mở/đóng bàn phím) **vẫn ở trạng thái OPEN** trong Defect Log; kết quả PASS của automation không tự đóng bug này.

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-07** | `NoteProvider - Create and Edit note` | Chỉnh sửa tiêu đề và nội dung ghi chú | `provider.updateNote(updatedNote)` | Tiêu đề và nội dung trong repository được cập nhật | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |

---

### FN-10 — Chuyển ghi chú vào thùng rác
**Tầng kiểm thử:** Đa tầng (Android UI/E2E + Flutter Provider Testing) · **Script:** `automation/tests/test_fn10_trash.py`

#### 1. Kịch bản UI/E2E:
| TC-ID | Dataset | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence & JUnit XML |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-021** | **D01** | Chuyển 1 ghi chú vào Thùng rác từ Selection Bar | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Thẻ ghi chú bình thường | Nhấn giữ note bật Selection Mode $\rightarrow$ chọn "Chuyển vào thùng rác" trên AppBar | Note biến mất khỏi HomeScreen và xuất hiện trong màn hình Thùng rác | P1 | DONE | **PASS** | `evidence/fn10/FN10_TC-BB-021_D01_01.png`<br>[fn10_trash_junit.xml](../../automation/reports/fn10_trash_junit.xml) (79.81s, baseline 14/10) |
| **TC-BB-021B** | **D01** | Hoàn tác chuyển ghi chú vào Thùng rác từ SnackBar | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Thẻ ghi chú bình thường | Nhấn giữ note $\rightarrow$ chọn Thùng rác $\rightarrow$ nhấn ngay nút "Hoàn tác" trên SnackBar | Ghi chú lập tức xuất hiện trở lại trên HomeScreen; Thùng rác không có ghi chú này | P1 | DONE | **PASS** | `evidence/fn10/automation_20261020_110841_407404_51da0bf6/TC-BB-021B/` (4 ảnh `01.png`..`04.png`)<br>*(Chờ bổ sung XML riêng)* |
| **TC-BB-021C** | **D01** | Hủy xóa ghi chú từ menu 3 chấm trong Editor | **Pre:** Đang mở ghi chú trong màn hình Editor.<br>**Data:** Ghi chú test có ID xác định | Nhấn menu 3 chấm ở góc phải đáy $\rightarrow$ chọn "Xóa ghi chú" $\rightarrow$ nhấn "Hủy" trên AlertDialog | Hộp thoại đóng lại; người dùng vẫn ở Editor; ghi chú không bị xóa (SQLite `status='normal'`) | P1 | DONE | **PASS** | `evidence/fn10/automation_20261020_120917_335994_c5046c82/TC-BB-021C/` (5 ảnh `01.png`..`05.png`)<br>[fn10_021c_d01_retry_20261020_120916.xml](../../automation/reports/fn10_021c_d01_retry_20261020_120916.xml) (100.48s) |
| **TC-BB-021C** | **D02** | Xác nhận xóa ghi chú từ menu 3 chấm trong Editor | **Pre:** Đang mở ghi chú trong màn hình Editor.<br>**Data:** Ghi chú test có ID xác định | Nhấn menu 3 chấm ở góc phải đáy $\rightarrow$ chọn "Xóa ghi chú" $\rightarrow$ nhấn "Xóa" trên AlertDialog | Thoát khỏi Editor về HomeScreen; ghi chú biến mất khỏi Home và vào Thùng rác (SQLite `status='trash'`) | P1 | DONE | **PASS** | `evidence/fn10/automation_20261020_124606_790642_535958ce/TC-BB-021C/` (5 ảnh `01.png`..`05.png`)<br>[fn10_021c_d02_20261020_124605.xml](../../automation/reports/fn10_021c_d02_20261020_124605.xml) (95.20s) |
| **TC-BB-021D** | **D01** | Chọn đồng thời nhiều ghi chú và chuyển vào Thùng rác | **Pre:** Có ít nhất 2 ghi chú test trên HomeScreen.<br>**Data:** 2 ghi chú QA riêng biệt | Nhấn giữ chọn note 1 $\rightarrow$ chạm chọn note 2 $\rightarrow$ nhấn biểu tượng Thùng rác trên AppBar | Cả 2 ghi chú biến mất đồng thời khỏi HomeScreen; SnackBar hiển thị; cả 2 xuất hiện trong Thùng rác | P1 | DONE | **PASS** | `evidence/fn10/automation_20261020_130909_123394_aea15e14/TC-BB-021D/` (5 ảnh `01.png`..`05.png`)<br>[fn10_021d_20261020_130907.xml](../../automation/reports/fn10_021d_20261020_130907.xml) (95.36s) |

*Ghi chú FN-10:*
- Đạt **5/5 execution items PASS**.
- `TC-BB-021B D01` đã chạy thành công trên máy thật và lưu đủ 4 ảnh bằng chứng, cần bổ sung file JUnit XML riêng vào `automation/reports/` khi có phiên rerun.

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-11** | `NoteProvider - Note lifecycle` | Xóa ghi chú: chuyển vào thùng rác | `provider.deleteNote(id)` | Note đổi status sang `'trash'`, rời khỏi active list | DONE | **PASS (đã đối chiếu log máy)** | Log máy automated_test_run.log (24 PASS) |
| **PV-REF-14** | `NoteProvider - Note lifecycle` | Xóa ghi chú đã ghim vào thùng rác | `provider.deleteNote(pinnedId)` | Note đã ghim vào Trash; gỡ khỏi `pinnedNotes` (liên kết FN-20) | DONE | **PASS (đã đối chiếu log máy)** | Log máy automated_test_run.log (24 PASS) |

---

### FN-11 — Khôi phục ghi chú từ thùng rác
**Tầng kiểm thử:** Đa tầng (Android UI/E2E + Flutter Provider Testing) · **Script:** `automation/tests/test_fn11_restore.py`

#### 1. Kịch bản UI/E2E:
| TC-ID | Dataset | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence & JUnit XML |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-022** | **D01** | Khôi phục 1 ghi chú từ Thùng rác về Trang chủ | **Pre:** Có ghi chú test trong Thùng rác.<br>**Data:** 1 ghi chú đã ở trạng thái trash | Vào Thùng rác $\rightarrow$ chạm note mở BottomSheet $\rightarrow$ chọn "Khôi phục ghi chú" | Note biến mất khỏi Thùng rác và xuất hiện lại trên HomeScreen với đầy đủ dữ liệu | P1 | DONE | **PASS** | `evidence/fn11/FN11_TC-BB-022_D01_01.png`<br>[fn11_restore_junit.xml](../../automation/reports/fn11_restore_junit.xml) (92.37s / 91.69s, baseline 14/10) |
| **TC-BB-022B** | **D01** | Khôi phục hàng loạt ghi chú (multi-restore) | **Pre:** Có ít nhất 2 ghi chú test trong Thùng rác.<br>**Data:** 2 ghi chú QA trong trash | Vào Thùng rác $\rightarrow$ nhấn giữ chọn note 1 $\rightarrow$ chọn note 2 $\rightarrow$ nhấn biểu tượng Khôi phục trên AppBar | Cả 2 ghi chú biến mất khỏi Thùng rác và xuất hiện lại đầy đủ trên HomeScreen | P1 | DONE | **PASS** | `evidence/fn11/automation_20261020_132134_088541_974befa2ac/TC-BB-022B/` (4 ảnh `01.png`..`04.png`)<br>[fn11_022b_20261020_132119.xml](../../automation/reports/fn11_022b_20261020_132119.xml) (123.76s) |
| **TC-BB-022C** | **D01** | Kiểm tra giao diện Empty State "Thùng rác trống" | **Pre:** Thùng rác hoàn toàn không có ghi chú nào.<br>**Data:** Empty trash | Mở Drawer $\rightarrow$ chọn "Thùng rác" $\rightarrow$ Quan sát giao diện khi rỗng | Màn hình hiển thị hình minh họa thùng rác rỗng cùng thông điệp: *"Thùng rác trống"* | P1 | DONE | **BLOCKED** *(pytest: SKIPPED)* | `evidence/fn11/automation_20261020_132734_161378_9a81212f/TC-BB-022C/precondition_not_empty.png`<br>[fn11_022c_20261020_132720.xml](../../automation/reports/fn11_022c_20261020_132720.xml) (42.21s) |

*Ghi chú FN-11:*
- Đạt **2 PASS / 1 BLOCKED**.
- `TC-BB-022C D01` là `SKIPPED` trong pytest và được phân loại nghiệp vụ là **BLOCKED**: do Thùng rác trên thiết bị đang chứa 23 ghi chú tồn tại từ các đợt kiểm thử trước; script tuân thủ quy tắc an toàn dữ liệu, không xóa sạch 23 ghi chú này. Sẽ retest khi môi trường Thùng rác được dọn an toàn.

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-05** | `NoteProvider - Restore note` | Khôi phục ghi chú từ thùng rác | `provider.restoreNote(id)` | Note đổi status về `'normal'`, quay lại danh sách hoạt động | DONE | **PASS (đã đối chiếu log máy)** | Log máy automated_test_run.log (24 PASS) |
| **PV-REF-12** | `NoteProvider - Note lifecycle` | Khôi phục ghi chú từ thùng rác | `provider.restoreNote(id)` | Trùng lặp kiểm thử lifecycle; xác nhận note phục hồi `'normal'` | DONE | **PASS (đã đối chiếu log máy)** | Log máy automated_test_run.log (24 PASS) |
| **PV-REF-15** | `NoteProvider - Note lifecycle` | Khôi phục ghi chú đã ghim từ thùng rác | `provider.restoreNote(pinnedId)` | Note rời Trash, quay lại active list; repository có status `'normal'` (liên kết FN-20); script không assert phục hồi `'pinned'` | DONE | **PASS (đã đối chiếu log máy)** | Log máy automated_test_run.log (24 PASS) |

---

### FN-12 — Xóa ghi chú vĩnh viễn
**Tầng kiểm thử:** Đa tầng (Android UI/E2E + Flutter Provider Testing) · **Script:** `automation/tests/test_fn12_permanent_delete.py`

#### 1. Kịch bản UI/E2E:
| TC-ID | Dataset | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence & JUnit XML |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-023** | **D01** | Xóa vĩnh viễn 1 ghi chú khỏi Thùng rác | **Pre:** Có ghi chú test trong Thùng rác.<br>**Data:** 1 ghi chú trong trash | Vào Thùng rác $\rightarrow$ chạm note $\rightarrow$ chọn "Xóa vĩnh viễn" $\rightarrow$ xác nhận AlertDialog "Xóa" | Ghi chú biến mất vĩnh viễn khỏi Thùng rác và không tồn tại trên HomeScreen | P1 | DONE | **PASS** | `evidence/fn12/FN12_TC-BB-023_D01_01.png`<br>[fn12_permanent_delete_junit.xml](../../automation/reports/fn12_permanent_delete_junit.xml) (88.69s, baseline 14/10) |
| **TC-BB-023B** | **D01** | Hủy xóa vĩnh viễn nhiều ghi chú trên AlertDialog | **Pre:** Có ít nhất 2 ghi chú test trong Thùng rác.<br>**Data:** 2 ghi chú QA trong trash | Vào Thùng rác $\rightarrow$ chọn 2 note $\rightarrow$ bấm icon Xóa vĩnh viễn trên AppBar $\rightarrow$ nhấn "Hủy" trên dialog | Hộp thoại đóng lại; các ghi chú đã chọn vẫn còn nguyên vẹn trong Thùng rác | P1 | DONE | **PASS** | `evidence/fn12/automation_20261020_135310_686942_d3abb8b620/TC-BB-023B/` (5 ảnh `01.png`..`05.png`)<br>[fn12_023b_d01_retry_20261020_135257.xml](../../automation/reports/fn12_023b_d01_retry_20261020_135257.xml) (102.52s) |
| **TC-BB-023B** | **D02** | Xác nhận xóa vĩnh viễn nhiều ghi chú trên AlertDialog | **Pre:** Có ít nhất 2 ghi chú test trong Thùng rác.<br>**Data:** 2 ghi chú QA trong trash | Vào Thùng rác $\rightarrow$ chọn 2 note $\rightarrow$ bấm icon Xóa vĩnh viễn trên AppBar $\rightarrow$ nhấn "Xóa" trên dialog | Toàn bộ ghi chú đã chọn biến mất hoàn toàn khỏi Thùng rác và không còn trên HomeScreen | P1 | DONE | **PASS** | `evidence/fn12/automation_20261020_145107_957126_f1858ca760/TC-BB-023B/` (6 ảnh `01.png`..`06.png`)<br>[fn12_023b_d02_20261020_145053.xml](../../automation/reports/fn12_023b_d02_20261020_145053.xml) (128.59s) |
| **TC-BB-023C** | **D01** | Tính bền vững vòng đời ghi chú (Trash + Deleted) sau restart | **Pre:** Chuẩn bị 2 ghi chú QA trên HomeScreen.<br>**Data:** Note 1 vào trash; Note 2 xóa vĩnh viễn | Đưa 2 note vào trash $\rightarrow$ xóa vĩnh viễn note 2 $\rightarrow$ force-stop app $\rightarrow$ mở lại app | Ghi chú trong Thùng rác vẫn còn; ghi chú xóa vĩnh viễn không bao giờ xuất hiện lại | P1 | DONE | **PASS** | `evidence/fn12/automation_20261020_150230_580481_1c12522463/TC-BB-023C/` (5 ảnh `01.png`..`05.png`)<br>[fn12_023c_20261020_150216.xml](../../automation/reports/fn12_023c_20261020_150216.xml) (141.84s) |

*Ghi chú FN-12:*
- Đạt **4/4 execution items PASS**.
- `TC-BB-023C D01` là bài test tích hợp vòng đời mở rộng xác nhận tính bền vững toàn bộ chu trình sống của ghi chú (active, trash, permanently deleted) qua việc khởi động lại ứng dụng.

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-13** | `NoteProvider - Note lifecycle` | Xóa vĩnh viễn ghi chú trong thùng rác | `provider.deleteNoteForever(id)` | Note bị xóa hoàn toàn khỏi `savedNotes` trong repository | DONE | **PASS (đã đối chiếu log máy)** | Log máy automated_test_run.log (24 PASS) |

---

### FN-13 — Lưu trữ ghi chú (Archive)
**Tầng kiểm thử:** Đa tầng (Android UI/E2E + Flutter Provider Testing) · **Script UI:** `automation/tests/test_fn13_fn14_archive.py`

#### 1. Kịch bản UI/E2E:
| TC-ID | Dataset | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence & JUnit XML |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-040** | **D01** | Chuyển 1 ghi chú vào mục Lưu trữ từ Trang chủ | **Pre:** Có 1 note QA trên HomeScreen.<br>**Data:** Note `QA_ARC_040_{marker}` | Long-press note trên Home $\rightarrow$ chạm icon "Lưu trữ" trên Selection AppBar $\rightarrow$ mở Drawer $\rightarrow$ chọn "Lưu trữ" | Ghi chú biến mất khỏi Trang chủ; xuất hiện trong `ArchiveScreen`; SQLite `status = 'archived'` | P2 | DONE | **PASS** | `evidence/fn13_14/automation_20261020_162615_605331_014938864a/TC-BB-040/` (3 ảnh `01.png`..`03.png`)<br>[fn13_fn14_20261020_162606.xml](../../automation/reports/fn13_fn14_20261020_162606.xml) (51.65s) |
| **TC-BB-EXT-008** | **D01** | Lưu trữ ghi chú Target không ảnh hưởng Control | **Pre:** Có 2 note riêng biệt trên HomeScreen.<br>**Data:** `QA_ARC_TARGET`, `QA_ARC_CONTROL` | Lưu trữ `TARGET` $\rightarrow$ kiểm tra `CONTROL` tại Home $\rightarrow$ vào Archive kiểm tra `TARGET` | `TARGET` chuyển sang Archive (`status = 'archived'`); `CONTROL` ở Home nguyên vẹn (`status = 'normal'`); không gộp dữ liệu | P2 | DONE | **PASS** | `evidence/fn13_14/automation_20261020_165126_004774_5c06926696/TC-BB-EXT-008/` (3 ảnh `01.png`..`03.png`)<br>[fn13_fn14_remaining3_20261020_165116.xml](../../automation/reports/fn13_fn14_remaining3_20261020_165116.xml) (74.39s) |
| **TC-BB-EXT-006** | **D01** | Tính bền vững dữ liệu lưu trữ tiếng Việt sau restart app | **Pre:** Note có nội dung tiếng Việt 2 dòng.<br>**Data:** `QA_ARCHIVE_PERSIST_{marker}` | Lưu trữ note $\rightarrow$ force-stop app $\rightarrow$ mở lại $\rightarrow$ vào `ArchiveScreen` kiểm tra note | Ghi chú không ở Home; xuất hiện trong Archive với đúng 1 bản ghi; tiêu đề và nội dung 2 dòng tiếng Việt nguyên vẹn | P1 | DONE | **PASS** | `evidence/fn13_14/automation_20261020_165232_968737_a40c7e7091/TC-BB-EXT-006/` (4 ảnh `01.png`..`04.png`)<br>[fn13_fn14_remaining3_20261020_165116.xml](../../automation/reports/fn13_fn14_remaining3_20261020_165116.xml) (55.51s) |

*Ghi chú FN-13:* Đạt **3/3 execution items PASS** trong Phase 3.

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-03** | `NoteProvider - Archive note` | Lưu trữ ghi chú | `provider.archiveNote(id)` | Note rời active list, xuất hiện trong `archivedNotes`, status `'archived'` | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |

---

### FN-14 — Bỏ lưu trữ ghi chú (Unarchive)
**Tầng kiểm thử:** Đa tầng (Android UI/E2E + Flutter Provider Testing) · **Script UI:** `automation/tests/test_fn13_fn14_archive.py`

#### 1. Kịch bản UI/E2E:
| TC-ID | Dataset | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence & JUnit XML |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-040B** | **D01** | Bỏ lưu trữ ghi chú từ ArchiveScreen về Trang chủ | **Pre:** Có 1 note đang trong Archive.<br>**Data:** Note `QA_ARC_040B_{marker}` | Vào `ArchiveScreen` $\rightarrow$ chạm note $\rightarrow$ chọn "Bỏ lưu trữ" trên BottomSheet $\rightarrow$ về Home | Ghi chú biến mất khỏi Archive; xuất hiện trở lại tại HomeScreen; SQLite `status = 'normal'` | P2 | DONE | **PASS** | `evidence/fn13_14/automation_20261020_164941_019186_493c0b9697/TC-BB-040B/` (3 ảnh `01.png`..`03.png`)<br>[fn14_040b_usb_20261020_164931.xml](../../automation/reports/fn14_040b_usb_20261020_164931.xml) (64.56s)* |
| **TC-BB-EXT-007** | **D01** | Vòng lặp Bỏ lưu trữ $\rightarrow$ Lưu trữ $\rightarrow$ Bỏ lưu trữ không gây duplicate | **Pre:** Có 1 note trong Archive.<br>**Data:** Note `QA_UNARCHIVE_{marker}` | Bỏ lưu trữ $\rightarrow$ Lưu trữ lại $\rightarrow$ Bỏ lưu trữ lần 2 $\rightarrow$ force-stop $\rightarrow$ mở lại Home & Archive | Sau mỗi vòng trạng thái khớp; cuối cùng có đúng 1 bản ghi trên Home, không còn trong Archive, không bị nhân bản | P1 | DONE | **PASS** | `evidence/fn13_14/automation_20261020_165328_477351_4b7542817e/TC-BB-EXT-007/` (5 ảnh `01.png`..`05.png`)<br>[fn13_fn14_remaining3_20261020_165116.xml](../../automation/reports/fn13_fn14_remaining3_20261020_165116.xml) (98.37s) |

*Ghi chú FN-14:*
- Đạt **2/2 execution items PASS** trong Phase 3.
- `TC-BB-040B D01`: Lượt chạy ban đầu gặp lỗi tiền điều kiện do app ở lại ArchiveScreen; sau khi bổ sung cơ chế khôi phục HomeScreen qua MainDrawer, lượt chạy retry độc lập trong `fn14_040b_usb_20261020_164931.xml` đã PASS hoàn toàn.

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-04** | `NoteProvider - Archive note` | Bỏ lưu trữ ghi chú | `provider.unarchiveNote(id)` | Note rời `archivedNotes`, quay lại active list, status `'normal'` | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |

---

### FN-15 đến FN-19 — Chức năng Checklist (Tạo, Thêm, Tick, Bỏ tick, Xóa mục)
> Chưa có kịch bản kiểm thử tự động ở tầng UI hoặc Provider trong baseline; được bảo đảm chất lượng thông qua 18 Unit Tests White-box (Checklist model) và kiểm thử hộp đen thủ công.

---

### FN-20 — Ghim và bỏ ghim ghi chú
**Tầng kiểm thử:** Đa tầng (Android UI/E2E + Flutter Provider Testing)

#### 1. Kịch bản UI/E2E Baseline (`automation/tests/test_fn20_pin_note.py`):
| TC-ID | Dataset | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence & JUnit XML |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-024** | **D01** | Ghim ghi chú lên khu vực ưu tiên trên Trang chủ | **Pre:** Đã đăng nhập; có ghi chú chưa ghim | Mở note $\rightarrow$ chạm icon Ghim $\rightarrow$ quay lại Home | Xuất hiện tiêu đề "Được ghim" và thẻ note nằm ở phần ưu tiên | P1 | DONE | **PASS** | `evidence/fn20/FN20_TC-BB-024_D01_01.png`<br>[fn20_pin_note_junit.xml](../../automation/reports/fn20_pin_note_junit.xml) *(baseline 05/10)* |
| **TC-BB-025** | **D01** | Bỏ ghim ghi chú trở về danh sách thông thường | **Pre:** Có ghi chú đang được ghim | Mở note $\rightarrow$ chạm bỏ icon Ghim $\rightarrow$ quay lại Home | Note trở về danh sách thường; tiêu đề "Được ghim" tự động ẩn nếu không còn note ghim | P1 | DONE | **PASS** | `evidence/fn20/FN20_TC-BB-025_D01_01.png`<br>[fn20_pin_note_junit.xml](../../automation/reports/fn20_pin_note_junit.xml) *(baseline 05/10)* |

#### 2. Kịch bản UI/E2E Mở rộng Phase 4 (`automation/tests/test_fn20_extended.py`):
| TC-ID | Dataset | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence & JUnit XML |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-024B** | **D01** | Ghim ghi chú trực tiếp từ AppBar màn hình soạn thảo (Editor) | **Pre:** Đang mở ghi chú mới/sẵn có trong Editor.<br>**Data:** Note QA có tiêu đề | Chạm icon Ghim trên AppBar của Editor $\rightarrow$ Back về Home | Thẻ ghi chú hiển thị ở phân vùng "Được ghim" trên HomeScreen; SQLite `status = 'pinned'` | P1 | DONE | **PASS** | `evidence/fn20/run_20261020_191601_27ef75ac/TC-BB-024B_D01/` (3 ảnh)<br>[fn20_editor_20261020_191551.xml](../../automation/reports/fn20_editor_20261020_191551.xml) (55.48s) |
| **TC-BB-024B** | **D02** | Bỏ ghim ghi chú trực tiếp từ AppBar màn hình soạn thảo (Editor) | **Pre:** Ghi chú đang được ghim, mở trong Editor.<br>**Data:** Note QA pinned | Chạm bỏ icon Ghim trên AppBar của Editor $\rightarrow$ Back về Home | Thẻ ghi chú chuyển về danh sách thường ("Khác"); SQLite `status = 'normal'` | P1 | DONE | **PASS** | `evidence/fn20/run_20261020_195017_78c1f1f3/TC-BB-024B_D02/` (3 ảnh)<br>[fn20_024b_d02_retry2_20261020_195008.xml](../../automation/reports/fn20_024b_d02_retry2_20261020_195008.xml) (67.43s) |
| **TC-BB-024C** | **D01** | Ràng buộc không cho phép ghim ghi chú mới khi chưa nhập nội dung | **Pre:** Đang ở Editor ghi chú mới hoàn toàn rỗng.<br>**Data:** Title="", Content="" | Chạm icon Ghim trên AppBar khi chưa nhập nội dung | Hiển thị SnackBar cảnh báo; không tạo ghi chú rác trong SQLite; không crash app | P2 | DONE | **PASS** | `evidence/fn20/run_20261020_195618_3e41d9d8/TC-BB-024C_D01/` (3 ảnh)<br>[fn20_024c_d01_20261020_195609.xml](../../automation/reports/fn20_024c_d01_20261020_195609.xml) (32.89s) |
| **TC-BB-024D** | **D01** | Ghim đồng thời nhiều ghi chú từ Trang chủ (Batch Pin 2 notes) | **Pre:** Có 2 ghi chú chưa ghim trên HomeScreen.<br>**Data:** 2 ghi chú QA `QA_PIN_BATCH_*` | Nhấn giữ chọn note 1 $\rightarrow$ chạm chọn note 2 $\rightarrow$ chạm icon Ghim AppBar | Cả 2 ghi chú được chuyển đồng thời lên phân vùng "Được ghim"; SQLite `status = 'pinned'` | P1 | DONE | **PASS** | `evidence/fn20/run_20261020_190753_ae757378/TC-BB-024D_D01/` (3 ảnh)<br>[fn20_batch_20261020_190742.xml](../../automation/reports/fn20_batch_20261020_190742.xml) (71.30s) |
| **TC-BB-024H** | **D01** | Đảo trạng thái độc lập khi chọn đồng thời ghi chú đã ghim và chưa ghim | **Pre:** 1 note đã ghim, 1 note chưa ghim trên Home.<br>**Data:** `QA_PIN_MIX_PINNED`, `QA_PIN_MIX_UNPINNED` | Nhấn giữ chọn note ghim $\rightarrow$ chọn note chưa ghim $\rightarrow$ chạm icon Ghim | Đảo chiều trạng thái độc lập: note đã ghim $\rightarrow$ bỏ ghim; note chưa ghim $\rightarrow$ được ghim | P2 | DONE | **PASS** | `evidence/fn20/run_20261020_190906_dab38cc3/TC-BB-024H_D01/` (3 ảnh)<br>[fn20_batch_20261020_190742.xml](../../automation/reports/fn20_batch_20261020_190742.xml) (68.51s) |
| **TC-BB-025D** | **D01** | Bỏ ghim đồng thời nhiều ghi chú từ Trang chủ (Batch Unpin 2 notes) | **Pre:** Có 2 ghi chú đang ghim trên HomeScreen.<br>**Data:** 2 ghi chú QA `QA_UNPIN_BATCH_*` | Nhấn giữ chọn note 1 $\rightarrow$ chạm chọn note 2 $\rightarrow$ chạm icon Bỏ ghim | Cả 2 ghi chú được đưa về danh sách thường ("Khác"); SQLite `status = 'normal'` | P1 | DONE | **PASS** | `evidence/fn20/run_20261020_191017_3e9899d7/TC-BB-025D_D01/` (3 ảnh)<br>[fn20_batch_20261020_190742.xml](../../automation/reports/fn20_batch_20261020_190742.xml) (75.87s) |
| **TC-BB-025E** | **D01** | Phân vùng 'Được ghim' vẫn duy trì khi chỉ bỏ ghim 1 trong số nhiều note ghim | **Pre:** Có 2 ghi chú đang ghim trên HomeScreen.<br>**Data:** 2 ghi chú QA pinned | Nhấn giữ chỉ chọn 1 note ghim $\rightarrow$ chạm icon Bỏ ghim | Note được chọn chuyển về "Khác"; phân vùng "Được ghim" vẫn duy trì chứa note còn lại | P2 | DONE | **PASS** | `evidence/fn20/run_20261020_191135_00e1fa58/TC-BB-025E_D01/` (3 ảnh)<br>[fn20_batch_20261020_190742.xml](../../automation/reports/fn20_batch_20261020_190742.xml) (75.98s) |
| **TC-BB-024E** | **D01** | Hiển thị phân vùng 'Được ghim' và 'Khác' khi có đồng thời cả 2 loại ghi chú | **Pre:** Có 1 note ghim và 1 note chưa ghim trên Home.<br>**Data:** `QA_PIN_LAYOUT_PIN`, `QA_PIN_LAYOUT_OTH` | Quan sát bố cục giao diện Trang chủ | Hiển thị cả 2 tiêu đề phân vùng: "Được ghim" và "Khác"; phân vùng "Được ghim" nằm phía trên | P1 | DONE | **PASS** | `evidence/fn20/run_20261020_205417_9fc5ebc6/TC-BB-024E_D01/` (3 ảnh)<br>[fn20_024e_v7_20261020_205408.xml](../../automation/reports/fn20_024e_v7_20261020_205408.xml) (64.33s) |
| **TC-BB-024F** | **D01** | Tính toàn vẹn dữ liệu (Tiêu đề, Nội dung) qua chu kỳ Pin $\rightarrow$ Unpin | **Pre:** Ghi chú QA có đủ Tiêu đề và Nội dung.<br>**Data:** `QA_PIN_INTEG_*` | Mở Editor ghim note $\rightarrow$ kiểm tra Home $\rightarrow$ mở Editor bỏ ghim $\rightarrow$ kiểm tra Home | Tiêu đề và nội dung ghi chú bảo toàn 100%, không mất mát ký tự hay định dạng | P1 | DONE | **PASS** | `evidence/fn20/run_20261020_205918_b7b5d72e/TC-BB-024F_D01/` (3 ảnh)<br>[fn20_024f_20261020_205909.xml](../../automation/reports/fn20_024f_20261020_205909.xml) (62.29s) |
| **TC-BB-024G** | **D01** | Giao diện khi toàn bộ các ghi chú đều ở trạng thái được ghim (All Pinned) | **Pre:** Tài khoản QA cô lập có đúng 3 note đều được ghim.<br>**Data:** 3 ghi chú `QA_PIN_ALL_*` | Quan sát giao diện danh sách Trang chủ | Phân vùng "Được ghim" hiển thị đầy đủ 3 note; phân vùng "Khác" hoàn toàn ẩn khỏi màn hình | P2 | DONE | **PASS** | `evidence/fn20/run_20261020_221322_59346191/TC-BB-024G_D01/` (4 ảnh)<br>[fn20_024g_v9_20261020_221313.xml](../../automation/reports/fn20_024g_v9_20261020_221313.xml) (66.52s) |
| **TC-BB-025B** | **D01** | Tính bền vững trạng thái Ghim sau khi khởi động lại ứng dụng (Persistence) | **Pre:** Có 1 note đang ghim trên HomeScreen.<br>**Data:** `QA_PIN_PERSIST_*` | Ghim note $\rightarrow$ Force-stop app $\rightarrow$ Relaunch mở lại app | Ghi chú vẫn duy trì ở phân vùng "Được ghim" sau khi khởi động lại; SQLite `status = 'pinned'` | P1 | DONE | **PASS** | `evidence/fn20/run_20261020_211950_c769bfbe/TC-BB-025B_D01/` (3 ảnh)<br>[fn20_025b_v8_20261020_211941.xml](../../automation/reports/fn20_025b_v8_20261020_211941.xml) (55.43s) |
| **TC-BB-025C** | **D01** | Ghi chú đã ghim vẫn duy trì trạng thái ghim sau khi chỉnh sửa nội dung | **Pre:** Có 1 note đang ghim trên HomeScreen.<br>**Data:** `QA_PIN_EDIT_*` | Mở note ghim $\rightarrow$ chỉnh sửa thêm nội dung $\rightarrow$ Back về Home | Ghi chú cập nhật nội dung mới và vẫn giữ nguyên trạng thái ở phân vùng "Được ghim" | P1 | DONE | **PASS** | `evidence/fn20/run_20261020_213036_64bf71ee/TC-BB-025C_D01/` (3 ảnh)<br>[fn20_025c_20261020_213027.xml](../../automation/reports/fn20_025c_20261020_213027.xml) (62.34s) |
| **TC-BB-025F** | **D01** | Tính bền vững trạng thái Bỏ ghim sau khi khởi động lại ứng dụng (Persistence) | **Pre:** Có 1 note vừa bỏ ghim về normal.<br>**Data:** `QA_UNPIN_PERSIST_*` | Bỏ ghim note $\rightarrow$ Force-stop app $\rightarrow$ Relaunch mở lại app | Ghi chú vẫn duy trì ở danh sách thường ("Khác") sau khi khởi động lại; SQLite `status = 'normal'` | P1 | DONE | **PASS** | `evidence/fn20/run_20261020_215221_b1d825c4/TC-BB-025F_D01/` (3 ảnh)<br>[fn20_025f_20261020_215211.xml](../../automation/reports/fn20_025f_20261020_215211.xml) (57.19s) |

*Ghi chú FN-20 chốt thực thi:*
- FN-20 đạt **15/15 execution items PASS** (2 baseline tại `test_fn20_pin_note.py` + 13 mở rộng tại `test_fn20_extended.py`).
- Toàn bộ 13 test case mở rộng Phase 4 được xác minh đối chiếu trực tiếp giữa JUnit XML thời gian thực và ảnh chụp màn hình trong `evidence/fn20/`.
- Tiền điều kiện cho TC-BB-024G (All Notes Pinned) được xử lý an toàn thông qua việc tạo tài khoản QA cô lập với đúng 3 ghi chú, bảo đảm không ảnh hưởng đến dữ liệu ghi chú khác trên máy.

#### 3. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-01** | `NoteProvider - Pin note` | Ghim ghi chú bình thường thành công | `provider.togglePin(note)` | Status đổi sang `'pinned'`, xuất hiện trong `pinnedNotes` | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| **PV-REF-02** | `NoteProvider - Pin note` | Bỏ ghim ghi chú đã ghim thành công | `provider.togglePin(pinnedNote)` | Status đổi sang `'normal'`, rời khỏi `pinnedNotes` | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| *(PV-REF-14)* | `NoteProvider - Note lifecycle` | Xóa ghi chú đã ghim vào thùng rác | `provider.deleteNote(pinnedId)` | Gỡ khỏi `pinnedNotes` khi đưa vào Trash (FN chính: FN-10) | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| *(PV-REF-15)* | `NoteProvider - Note lifecycle` | Khôi phục ghi chú đã ghim từ thùng rác | `provider.restoreNote(pinnedId)` | Phục hồi note về status `'normal'`, vào active list (FN chính: FN-11); không assert giữ ghim | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |

---

### FN-21, FN-22 — Quản lý Nhãn (Tạo nhãn, Gắn nhãn vào ghi chú)
> Chưa có kịch bản kiểm thử tự động ở tầng UI hoặc Provider trong baseline; được kiểm thử thủ công qua màn hình Quản lý nhãn.

---

### FN-23 — Tìm kiếm ghi chú theo văn bản
**Tầng kiểm thử:** Đa tầng (Android UI/E2E + Flutter Provider Testing)

#### 1. Kịch bản UI/E2E (`automation/tests/test_fn23_search.py`):
| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-026** | Tìm kiếm ghi chú theo từ khóa Tiêu đề | **Pre:** Có ghi chú tiêu đề "Lịch thi học kỳ".<br>**Data:** Query = `"Lịch thi học kỳ"` | Chạm icon Tìm kiếm $\rightarrow$ nhập từ khóa | Danh sách kết quả hiển thị thẻ ghi chú "Lịch thi học kỳ" khớp tiêu đề | P1 | DONE | **PASS** | `evidence/fn23/FN23_TC-BB-026_D01_01.png` |
| **TC-BB-027** | Tìm kiếm ghi chú theo từ khóa Nội dung | **Pre:** Có ghi chú chứa nội dung "giấy in A4".<br>**Data:** Query = `"giấy in A4"` | Chạm icon Tìm kiếm $\rightarrow$ nhập từ khóa | Danh sách kết quả hiển thị thẻ ghi chú khớp nội dung | P1 | DONE | **PASS** | `evidence/fn23/FN23_TC-BB-027_D01_01.png` |
| **TC-BB-028** | Tìm kiếm với từ khóa không tồn tại | **Pre:** Không có ghi chú nào chứa từ khóa.<br>**Data:** Query = `"chuoi_khong_ton_tai_999"` | Nhập chuỗi không tồn tại $\rightarrow$ quan sát màn hình | Hiển thị Empty State: *"Không tìm thấy kết quả"*, gợi ý *"Thử từ khóa khác"* | P1 | DONE | **PASS** | `evidence/fn23/FN23_TC-BB-028_D01_01.png` |
| **TC-BB-029** | Tìm kiếm với chuỗi Ký tự đặc biệt & SQL Injection | **Pre:** Ứng dụng ổn định.<br>**Data:** Query = `"' OR 1=1 -- % _ @#$"` | Nhập payload đặc biệt $\rightarrow$ quan sát phản hồi | Ứng dụng xử lý an toàn, không crash, hiển thị màn hình rỗng hợp lệ | P1 | DONE | **PASS** | `evidence/fn23/FN23_TC-BB-029_D01_01.png` |

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-08** | `NoteProvider - Search note` | Search note by content | `provider.searchNotes('user-1', 'content')` | Trả về danh sách chứa các note khớp từ khóa nội dung | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| **PV-REF-09** | `NoteProvider - Search note` | Search note with no matching result | `provider.searchNotes('user-1', 'nonexistent')` | Trả về danh sách rỗng khi không có kết quả | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| **PV-REF-10** | `NoteProvider - Search note` | Clear search | `provider.clearSearch()` | Trạng thái tìm kiếm được thiết lập lại về ban đầu | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |

---

### FN-24 đến FN-28 — Bộ lọc chuyên biệt & Giao diện (has:image, has:url, has:audio, is:pinned, Grid/List)
> Chưa có kịch bản kiểm thử tự động ở tầng UI hoặc Provider trong baseline; được kiểm thử thủ công qua các token tìm kiếm và nút chuyển chế độ hiển thị.

---

### FN-29 — Kích hoạt khóa sinh trắc học
**Tầng kiểm thử:** Android UI/E2E · **Công cụ:** Python + uiautomator2 · **Script:** `automation/tests/test_fn29_30_biometric.py` (Script thăm dò khả thi)

| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-012** | Kích hoạt khóa bảo vệ cho ghi chú đã lưu thành công | **Pre:** Ghi chú đã lưu trong DB; thiết bị đã cài vân tay | Chạm icon ổ khóa mở trên AppBar $\rightarrow$ quét vân tay $\rightarrow$ về Home | Hiển thị thông báo *"🔒 Đã khóa ghi chú"*; icon đổi thành ổ khóa đóng; Trang chủ hiển thị *"🔒 Ghi chú đã khóa"* | P1 | DEFERRED | **NOT RUN** | — |

---

### FN-30 — Mở khóa ghi chú bằng sinh trắc học
**Tầng kiểm thử:** Android UI/E2E · **Công cụ:** Python + uiautomator2 · **Script:** `automation/tests/test_fn29_30_biometric.py` (Script thăm dò khả thi)

| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-013** | Mở khóa ghi chú thành công bằng sinh trắc học hợp lệ | **Pre:** Có ghi chú đang bị khóa tại HomeScreen | Chạm vào thẻ ghi chú khóa $\rightarrow$ hộp thoại vân tay hiện $\rightarrow$ quét vân tay đúng | Lớp che bảo vệ mở ra; hiển thị đầy đủ tiêu đề, nội dung và thanh công cụ soạn thảo | P1 | DEFERRED | **NOT RUN** | — |
| **TC-BB-014** | Chặn truy cập nội dung khi quét sinh trắc học không khớp | **Pre:** Có ghi chú đang bị khóa tại HomeScreen | Chạm vào thẻ ghi chú khóa $\rightarrow$ quét ngón tay chưa đăng ký | Hộp thoại báo không nhận diện; giữ nguyên lớp phủ bảo vệ màu tối; hiển thị lỗi: *"Xác thực thất bại. Thử lại?"* | P1 | DEFERRED | **NOT RUN** | — |
| **TC-BB-015** | Duy trì lớp phủ bảo vệ khi người dùng hủy hộp thoại sinh trắc học | **Pre:** Có ghi chú đang bị khóa tại HomeScreen | Chạm thẻ ghi chú khóa $\rightarrow$ trên hộp thoại biometric nhấn "Hủy" hoặc chạm ra ngoài | Hộp thoại đóng lại; màn hình chi tiết vẫn giữ nguyên lớp phủ bảo vệ màu tối cùng nút *"Xác thực ngay"*; không lộ nội dung | P1 | DEFERRED | **NOT RUN** | — |

*Lưu ý ánh xạ:* `TC-BB-015` được ánh xạ chính xác về **FN-30** (Mở khóa sinh trắc học - kịch bản Hủy xác thực duy trì lớp phủ bảo vệ) theo đúng tài liệu Black-box Test Suite gốc [`test_cases/black_box/black_box_test_cases.md`](../test_cases/black_box/black_box_test_cases.md).

---

### FN-31 đến FN-33 — Gemini AI (Tóm tắt, Đề xuất tiêu đề, Bóc tách Checklist)
> Bị chặn (**BLOCKED**) trong baseline Automation do lỗi hiển thị khung đỏ dịch vụ UI khi gọi API Gemini trên thiết bị thật; không có kịch bản tự động chính thức chạy.

---

### FN-34 đến FN-39 — Xuất PDF, Vẽ tay Canvas, Tải ảnh Cloudinary, Đổi màu nền, Thông báo nhắc nhở
> Chưa có kịch bản kiểm thử tự động ở tầng UI hoặc Provider trong baseline; được kiểm thử thủ công qua Black-box Manual Testing.

---

### FN-40 — Bắt đầu đồng bộ dữ liệu
**Tầng kiểm thử:** Đa tầng (UI Deferred + Flutter Provider 9 tests đã đối chiếu log máy 24 PASS; chưa xác minh chính xác commit thực thi)

#### 1. Kịch bản UI/E2E (Chưa có script UI):
| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-030** | Tạo ghi chú ngoại tuyến và tự động đồng bộ khi có mạng | **Pre:** Thiết bị ngắt kết nối mạng $\rightarrow$ tạo ghi chú $\rightarrow$ bật lại mạng | Ngắt kết nối $\rightarrow$ tạo note local $\rightarrow$ bật mạng $\rightarrow$ chờ sync | Ghi chú được tự động đẩy lên Firebase Cloud sau khi có mạng | P1 | DEFERRED | **NOT RUN** | — |

#### 2. Kịch bản Provider (`test/automated/sync_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-16** | `SyncProvider - Initial state` | Trạng thái ban đầu là idle | Khởi tạo `SyncProvider` | `provider.status == SyncStatus.idle`; `isOffline` hợp lệ | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| **PV-REF-17** | `SyncProvider - Update user` | Không đồng bộ khi userId là null | `provider.updateUser(null)` | `repository.syncedUserIds` rỗng; không gọi đồng bộ | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| **PV-REF-18** | `SyncProvider - Update user` | Đồng bộ khi có userId mới | `provider.updateUser('user-1')` | Kích hoạt đồng bộ tự động với `'user-1'` | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| **PV-REF-19** | `SyncProvider - Update user` | Không đồng bộ lại khi userId không thay đổi | `updateUser('user-1')` lặp lại | Idempotent check: không gọi đồng bộ lần 2 | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| **PV-REF-20** | `SyncProvider - Update user` | Đổi user thì đồng bộ với user mới | `updateUser('user-1')` $\rightarrow$ `'user-2'` | Kích hoạt đồng bộ cho cả 2 lượt user độc lập | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| **PV-REF-21** | `SyncProvider - Sync now` | Phát tín hiệu khi đồng bộ có dữ liệu mới | `repository.syncResult = true` $\rightarrow$ `syncNow()` | Phát sự kiện `onSyncWithNewData` thành công | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| **PV-REF-22** | `SyncProvider - Sync now` | Không phát tín hiệu khi không có dữ liệu mới | `repository.syncResult = false` $\rightarrow$ `syncNow()` | Không phát sự kiện `onSyncWithNewData` thừa | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| **PV-REF-23** | `SyncProvider - Sync now` | Bắt lỗi khi đồng bộ thất bại | `repository.shouldThrow = true` $\rightarrow$ `syncNow()` | Bắt ngoại lệ an toàn, không để unhandled error | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |
| **PV-REF-24** | `SyncProvider - Status stream` | Cập nhật trạng thái khi repository phát trạng thái mới | `repository.emitStatus(syncing/success)` | `provider.status` cập nhật đồng bộ theo stream | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |

---

### FN-41 — Giải quyết xung đột đồng bộ LWW
**Tầng kiểm thử:** Android UI/E2E (Chưa có script UI)

| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-031** | Giải quyết xung đột chỉnh sửa đồng thời theo nguyên tắc LWW | **Pre:** 2 thiết bị cùng chỉnh sửa 1 note; timestamp khác nhau; ca timestamp bằng nhau tách riêng chờ BR-03 | Sửa đồng thời trên 2 máy $\rightarrow$ kết nối mạng $\rightarrow$ đối chiếu | Bản ghi có `updatedAt` mới nhất được giữ lại theo quy tắc LWW | P1 | DEFERRED | **NOT RUN** | — |

---

### FN-42, FN-43 — Phi chức năng (Ghi chú rất dài, Ảnh OOM)
> Chưa có kịch bản kiểm thử tự động ở tầng UI hoặc Provider trong baseline; trạng thái thủ công xem hồ sơ phi chức năng; tài liệu này không xác nhận đã chạy stress test.

---

### FN-44 — Xử lý thiết bị hết bộ nhớ
> Bị chặn (**BLOCKED**) theo nguyên tắc an toàn thiết bị của tester; không thực hiện test phá hủy bộ nhớ trên thiết bị thật.

---

## 4. Bảng tổng hợp đối chiếu số lượng kịch bản và kết quả

| Đơn vị đo | Số lượng | Mức xác minh |
| --- | ---: | --- |
| Chức năng hệ thống | 44 FN | Danh mục quản lý, không phải 44 tests |
| TC UI trong baseline ứng viên | 31 | 23 có XML, 8 DEFERRED |
| TC UI duy nhất có kết quả | 23 | 19 PASS / 4 FAIL; 82.61% PASS |
| Lượt thực thi trong 9 XML đang lưu | 24 | TC-BB-022 có 2 bản ghi PASS; không đại diện mọi lượt chạy lịch sử |
| Khai báo test Provider | 24 | 15 NoteProvider + 9 SyncProvider; kiểm kê mã nguồn |
| Kết quả Provider theo báo cáo cũ | 24 PASS | ĐÃ ĐỐI CHIẾU LOG MÁY (log lịch sử xác nhận 24 PASS; chưa xác minh chính xác commit thực thi, không bắt buộc JUnit XML) |
| Phạm vi thiết kế hai tầng | 55 | 31 TC UI + 24 Provider tests; các đơn vị và tầng khác nhau |
| Tổng lịch sử được tài liệu cũ báo cáo | 47 | 23 UI + 24 Provider (43 PASS / 4 FAIL theo kết quả đã có minh chứng XML và log) |

7 FN có mã ở cả hai tầng trong baseline: FN-08, FN-09, FN-10, FN-11, FN-12, FN-20, FN-23. Với Phase 3 (20/10/2026), FN-13 và FN-14 đã được bổ sung đầy đủ bộ UI/E2E automation (`test_fn13_fn14_archive.py` gồm 5 execution items: 5 PASS), nâng tổng số FN có mã kiểm thử ở cả hai tầng lên 9 FN (FN-08..14, FN-20, FN-23); thêm FN-40 chỉ có Provider nên tổng phạm vi hai tầng là 12 FN (tất cả 24 tests của 10 FN Provider đều có kết quả trong log máy).

## 5. Tài liệu liên quan

- [`docs/qa/automation_plan.md`](automation_plan.md) — Kế hoạch kiểm thử tự động hóa, phạm vi và chiến lược.
- [`docs/qa/automation_execution_summary.md`](automation_execution_summary.md) — Báo cáo tổng kết thực thi, phân tích 4 ca FAIL và bằng chứng.
- [`docs/qa/automation_status.md`](automation_status.md) — Bảng tiến độ và trạng thái tự động hóa tổng thể.
- [`test_cases/black_box/black_box_test_cases.md`](../test_cases/black_box/black_box_test_cases.md) — Nguồn đặc tả gốc Black-box Test Suite.
- [`docs/bugs/defect_log.md`](../bugs/defect_log.md) — Nhật ký quản lý lỗi chính thức toàn dự án.

## 6. Điều kiện chung và hợp đồng kiểm tra

- UI chạy trên ứng dụng QA và dữ liệu thử nghiệm riêng. Kiểm tra màn hình xuất phát, trạng thái tài khoản, mạng, note chuẩn bị và bàn phím trước mỗi ca; thiếu tiền điều kiện thì dừng ca và ghi BLOCKED cho lượt mới.
- Mỗi TC có dữ liệu định danh riêng; note tạo mới nên có tiền tố QA và timestamp. Đây là quy ước cho lượt tiếp theo; không khẳng định script hiện tại đã dọn dẹp hoàn hảo.
- TC-BB-006: xác nhận tài khoản đã verify trước khi bấm đăng nhập; không dùng việc mở được màn hình xác thực để kết luận ca đăng nhập thành công.
- Các ca xóa chỉ tác động note được tạo cho lượt kiểm thử. Không reset ứng dụng, không xóa sinh trắc học của người dùng, không sửa `lib/` để làm test PASS.
- UI assertions phải kiểm tra trạng thái cuối. Ảnh chụp hỗ trợ quan sát; XML xác nhận kết quả assertion của lượt chạy, không chứng minh mọi yêu cầu trong FN đều được kiểm tra.
- Provider: mỗi test có Fake Repository và Provider mới từ setUp; tearDown dispose Provider/đóng stream. Fake Repository và mock MethodChannel cô lập backend, thông báo và connectivity; không dùng kết quả này để kết luận SQLite/Firestore hoặc 2 thiết bị thật đã đồng bộ.
- `PV-REF-05` và `PV-REF-12` có mục tiêu khôi phục gần nhau; giữ nguyên 2 khai báo hiện tại, ghi nhận để tối ưu sau. `PV-REF-14/15` có liên kết FN-20 phụ nên 24 tests tạo 26 lượt liên kết, không phải 26 tests.
- `PV-REF-23` hiện chỉ assert Future hoàn thành khi fake repository ném lỗi; không suy rộng thành đã kiểm tra mọi trạng thái UI lỗi.
- TC-BB-031 thông thường dùng hai timestamp khác nhau. BR-03 chỉ chặn trường hợp timestamp bằng nhau, không chặn toàn bộ kịch bản LWW.

## 7. Script mở rộng ngoài 31 TC baseline

Trong mã nguồn có các biến thể đăng ký và TC-BB-006B/006C/006D cùng alias. Chưa có XML tương ứng trong 9 báo cáo được rà soát, nên trạng thái là **CÓ MÃ / CHƯA XÁC MINH THỰC THI**; không cộng vào 23 TC đã chạy và không gán kết quả từ manual cho automation. Xem [kiểm kê từng hàm và node ID](automation_script_inventory.md).

Mỗi ca mở rộng cần kế thừa tiền điều kiện, dữ liệu và Expected từ đặc tả hộp đen; đối chiếu assertion thực tế trước khi đưa vào hồi quy. Chỉ chọn một node ID cho cùng một TC/dataset nếu các hàm là alias; chạy toàn file có thể tạo lượt lặp.
