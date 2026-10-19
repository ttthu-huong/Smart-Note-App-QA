# ĐẶC TẢ KIỂM THỬ TỰ ĐỘNG (AUTOMATION TEST CASES)

**Dự án:** Smart Note App · **Nhánh:** `huong` · **Phiên bản:** 1.1 · **Ngày rà soát:** 19/10/2026 (UTC+7)
**Mã nguồn và bằng chứng được đối chiếu:** `98abb5af577b2d38192e7a88e7ff94a2b5f77262`. Đây là cập nhật tài liệu; không có lượt chạy ứng dụng mới.
**Bố cục tài liệu:** **FN-01..FN-44 → Chi tiết kịch bản → Preconditions, Test Data, Steps, Expected Result, Test Script, Code Status, Execution Result, Evidence**.
**Phạm vi:** Đặc tả chi tiết cho **31 Test Cases UI/E2E** (23 có XML thực thi, 8 tạm hoãn trong baseline) và **24 Tests Provider** (`PV-REF-01` đến `PV-REF-24`).

---

> **Quy ước bằng chứng:** Kết quả UI bên dưới được đối chiếu với 9 XML hiện có (lưu ý: script working tree của FN-10, FN-11, FN-12 hiện đang bị rỗng, XML là kết quả lịch sử của phiên bản trước). Provider có 24 bài test được đối chiếu với file log máy `evidence/automated/automated_test_run.log` (log lịch sử xác nhận 24 PASS; chưa xác minh chính xác commit thực thi, không coi thiếu JUnit XML là thiếu bắt buộc; file log đã được đưa vào staging git via `git add -f`). Các bảng mô tả phạm vi assertion của script, không khẳng định bao phủ toàn bộ FN.

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
5. **Ranh giới với Black-box Test Suite:** `automation_test_cases.md` là tài liệu đặc tả kỹ thuật riêng cho kiểm thử tự động. Tài liệu [`test_cases/black_box/black_box_test_cases.md`](../../test_cases/black_box/black_box_test_cases.md) vẫn là nguồn đặc tả chính thức và chuẩn mực cao nhất của Black-box Testing toàn dự án.

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

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-06** | `NoteProvider - Create and Edit note` | Tạo ghi chú mới thành công | `provider.addNote(note)` | Note được lưu vào repository và xuất hiện trong `provider.notes` | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |

---

### FN-09 — Chỉnh sửa và tự động lưu ghi chú
**Tầng kiểm thử:** Đa tầng (Android UI/E2E + Flutter Provider Testing)

#### 1. Kịch bản UI/E2E (`automation/tests/test_fn09_edit_note.py`):
| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-019** | Chỉnh sửa nội dung ghi chú có sẵn | **Pre:** Có ghi chú test trên HomeScreen.<br>**Data:** Content thêm `"[Đã cập nhật lúc 10:00]"` | Mở note $\rightarrow$ sửa nội dung $\rightarrow$ bấm Back về Home | Thẻ ghi chú trên HomeScreen cập nhật chính xác nội dung mới | P1 | DONE | **PASS** | `evidence/fn09/FN09_TC-BB-019_D01_01.png` |
| **TC-BB-020** | Kiểm tra tự động lưu sau khi sửa (Debounce) | **Pre:** Mở ghi chú trong Editor.<br>**Data:** Thêm nội dung `"- Nội dung kiểm tra tự động lưu"` | Nhập nội dung mới $\rightarrow$ chờ 2s (>1000ms) $\rightarrow$ thoát ra mở lại | Toàn bộ nội dung mới vẫn còn nguyên vẹn trong Editor | P1 | DONE | **PASS** | `evidence/fn09/FN09_TC-BB-020_D01_01.png` |

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-07** | `NoteProvider - Create and Edit note` | Chỉnh sửa tiêu đề và nội dung ghi chú | `provider.updateNote(updatedNote)` | Tiêu đề và nội dung trong repository được cập nhật | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |

---

### FN-10 — Chuyển ghi chú vào thùng rác
**Tầng kiểm thử:** Đa tầng (UI có XML PASS lịch sử + Provider có mã và 24 tests đã đối chiếu log máy)

#### 1. Kịch bản UI/E2E (`automation/tests/test_fn10_trash.py`):
| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-021** | Chuyển ghi chú vào Thùng rác | **Pre:** Có ghi chú hoạt động trên HomeScreen | Nhấn giữ note bật Selection Mode $\rightarrow$ chọn "Chuyển vào thùng rác" trên AppBar | Note biến mất khỏi HomeScreen và xuất hiện trong màn hình Thùng rác | P1 | Rỗng (0B)* | **PASS (lịch sử XML)** (XML testcase time: 79.806s) | `evidence/fn10/FN10_TC-BB-021_D01_01.png`, `automation/reports/fn10_trash_junit.xml`<br>*(Lưu ý: Script working tree hiện rỗng 0 bytes; kết quả XML là lịch sử của phiên bản trước; khả năng chạy lại hiện bị ảnh hưởng, không khẳng định mã hiện tại sẵn sàng chạy nếu chưa khôi phục từ file `.bak` hoặc Git HEAD)* |

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-11** | `NoteProvider - Note lifecycle` | Xóa ghi chú: chuyển vào thùng rác | `provider.deleteNote(id)` | Note đổi status sang `'trash'`, rời khỏi active list | DONE | **PASS (đã đối chiếu log máy)** | Log máy automated_test_run.log (24 PASS) |
| **PV-REF-14** | `NoteProvider - Note lifecycle` | Xóa ghi chú đã ghim vào thùng rác | `provider.deleteNote(pinnedId)` | Note đã ghim vào Trash; gỡ khỏi `pinnedNotes` (liên kết FN-20) | DONE | **PASS (đã đối chiếu log máy)** | Log máy automated_test_run.log (24 PASS) |

---

### FN-11 — Khôi phục ghi chú từ thùng rác
**Tầng kiểm thử:** Đa tầng (UI có XML PASS lịch sử + Provider có mã và 24 tests đã đối chiếu log máy)

#### 1. Kịch bản UI/E2E (`automation/tests/test_fn11_restore.py`):
| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-022** | Khôi phục ghi chú từ Thùng rác về Trang chủ | **Pre:** Chuẩn bị sẵn 1 ghi chú test trong Thùng rác | Vào Thùng rác $\rightarrow$ chạm note mở BottomSheet $\rightarrow$ chọn "Khôi phục ghi chú" | Note biến mất khỏi Thùng rác và xuất hiện lại trên HomeScreen | P1 | Rỗng (0B)* | **PASS (lịch sử XML)** (XML testcase time: 92.371s / 91.686s) | `evidence/fn11/FN11_TC-BB-022_D01_01.png`, `automation/reports/fn11_restore_junit.xml`<br>*(Lưu ý: Script working tree hiện rỗng 0 bytes; kết quả XML là lịch sử của phiên bản trước; khả năng chạy lại hiện bị ảnh hưởng, không khẳng định mã hiện tại sẵn sàng chạy nếu chưa khôi phục từ file `.bak` hoặc Git HEAD)* |

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-05** | `NoteProvider - Restore note` | Khôi phục ghi chú từ thùng rác | `provider.restoreNote(id)` | Note đổi status về `'normal'`, quay lại danh sách hoạt động | DONE | **PASS (đã đối chiếu log máy)** | Log máy automated_test_run.log (24 PASS) |
| **PV-REF-12** | `NoteProvider - Note lifecycle` | Khôi phục ghi chú từ thùng rác | `provider.restoreNote(id)` | Trùng lặp kiểm thử lifecycle; xác nhận note phục hồi `'normal'` | DONE | **PASS (đã đối chiếu log máy)** | Log máy automated_test_run.log (24 PASS) |
| **PV-REF-15** | `NoteProvider - Note lifecycle` | Khôi phục ghi chú đã ghim từ thùng rác | `provider.restoreNote(pinnedId)` | Note rời Trash, quay lại active list; repository có status `'normal'` (liên kết FN-20); script không assert phục hồi `'pinned'` | DONE | **PASS (đã đối chiếu log máy)** | Log máy automated_test_run.log (24 PASS) |

---

### FN-12 — Xóa ghi chú vĩnh viễn
**Tầng kiểm thử:** Đa tầng (UI có XML PASS lịch sử + Provider có mã và 24 tests đã đối chiếu log máy)

#### 1. Kịch bản UI/E2E (`automation/tests/test_fn12_permanent_delete.py`):
| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-023** | Xóa vĩnh viễn ghi chú khỏi Thùng rác | **Pre:** Chuẩn bị sẵn 1 ghi chú test trong Thùng rác | Vào Thùng rác $\rightarrow$ chọn "Xóa vĩnh viễn" $\rightarrow$ xác nhận AlertDialog "Xóa" | Bản ghi bị xóa hoàn toàn khỏi DB và biến mất khỏi cả Thùng rác lẫn HomeScreen | P1 | Rỗng (1B)* | **PASS (lịch sử XML)** (XML testcase time: 88.693s) | `evidence/fn12/FN12_TC-BB-023_D01_01.png`, `automation/reports/fn12_permanent_delete_junit.xml`<br>*(Lưu ý: Script working tree hiện rỗng 1 byte; kết quả XML là lịch sử của phiên bản trước; khả năng chạy lại hiện bị ảnh hưởng, không khẳng định mã hiện tại sẵn sàng chạy nếu chưa khôi phục từ file `.bak` hoặc Git HEAD)* |

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-13** | `NoteProvider - Note lifecycle` | Xóa vĩnh viễn ghi chú trong thùng rác | `provider.deleteNoteForever(id)` | Note bị xóa hoàn toàn khỏi `savedNotes` trong repository | DONE | **PASS (đã đối chiếu log máy)** | Log máy automated_test_run.log (24 PASS) |

---

### FN-13 — Lưu trữ ghi chú (Archive)
**Tầng kiểm thử:** Flutter Provider Testing (`test/automated/note_provider_test.dart`)

| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-03** | `NoteProvider - Archive note` | Lưu trữ ghi chú | `provider.archiveNote(id)` | Note rời active list, xuất hiện trong `archivedNotes`, status `'archived'` | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |

---

### FN-14 — Bỏ lưu trữ ghi chú (Unarchive)
**Tầng kiểm thử:** Flutter Provider Testing (`test/automated/note_provider_test.dart`)

| Mã Ref | Nhóm kiểm thử (Group) | Tên Test Case trong mã nguồn | Thao tác / Phương thức | Kết quả kỳ vọng / Assertion | Code | Result | Evidence Log |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PV-REF-04** | `NoteProvider - Archive note` | Bỏ lưu trữ ghi chú | `provider.unarchiveNote(id)` | Note rời `archivedNotes`, quay lại active list, status `'normal'` | DONE | **PASS (đã đối chiếu log máy)** | Log cục bộ automated_test_run.log (12/10) |

---

### FN-15 đến FN-19 — Chức năng Checklist (Tạo, Thêm, Tick, Bỏ tick, Xóa mục)
> Chưa có kịch bản kiểm thử tự động ở tầng UI hoặc Provider trong baseline; được bảo đảm chất lượng thông qua 18 Unit Tests White-box (Checklist model) và kiểm thử hộp đen thủ công.

---

### FN-20 — Ghim và bỏ ghim ghi chú
**Tầng kiểm thử:** Đa tầng (Android UI/E2E + Flutter Provider Testing)

#### 1. Kịch bản UI/E2E (`automation/tests/test_fn20_pin_note.py`):
| TC-ID | Mục tiêu kiểm thử | Preconditions & Test Data | Các bước kịch bản | Expected Result / Assertion | Ưu tiên | Code | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-BB-024** | Ghim ghi chú lên khu vực ưu tiên trên Trang chủ | **Pre:** Đã đăng nhập; có ghi chú chưa ghim | Mở note $\rightarrow$ chạm icon Ghim $\rightarrow$ quay lại Home | Xuất hiện tiêu đề "Được ghim" và thẻ note nằm ở phần ưu tiên | P1 | DONE | **PASS** | `evidence/fn20/FN20_TC-BB-024_D01_01.png` |
| **TC-BB-025** | Bỏ ghim ghi chú trở về danh sách thông thường | **Pre:** Có ghi chú đang được ghim | Mở note $\rightarrow$ chạm bỏ icon Ghim $\rightarrow$ quay lại Home | Note trở về danh sách thường; tiêu đề "Được ghim" tự động ẩn nếu không còn note ghim | P1 | DONE | **PASS** | `evidence/fn20/FN20_TC-BB-025_D01_01.png` |

#### 2. Kịch bản Provider (`test/automated/note_provider_test.dart`):
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

*Lưu ý ánh xạ:* `TC-BB-015` được ánh xạ chính xác về **FN-30** (Mở khóa sinh trắc học - kịch bản Hủy xác thực duy trì lớp phủ bảo vệ) theo đúng tài liệu Black-box Test Suite gốc [`test_cases/black_box/black_box_test_cases.md`](../../test_cases/black_box/black_box_test_cases.md).

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

7 FN có mã ở cả hai tầng: FN-08, FN-09, FN-10, FN-11, FN-12, FN-20, FN-23. Có XML UI ở 9 FN; thêm 3 FN chỉ có Provider là FN-13, FN-14, FN-40 nên hợp thiết kế là 12 FN (tất cả 24 tests của 10 FN Provider đều có kết quả trong log máy).

## 5. Tài liệu liên quan

- [`docs/qa/automation_plan.md`](automation_plan.md) — Kế hoạch kiểm thử tự động hóa, phạm vi và chiến lược.
- [`docs/qa/automation_execution_summary.md`](automation_execution_summary.md) — Báo cáo tổng kết thực thi, phân tích 4 ca FAIL và bằng chứng.
- [`docs/qa/automation_status.md`](automation_status.md) — Bảng tiến độ và trạng thái tự động hóa tổng thể.
- [`test_cases/black_box/black_box_test_cases.md`](../../test_cases/black_box/black_box_test_cases.md) — Nguồn đặc tả gốc Black-box Test Suite.
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
