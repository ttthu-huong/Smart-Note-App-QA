# KẾ HOẠCH KIỂM THỬ TỰ ĐỘNG (AUTOMATION TEST PLAN)

**Dự án:** Smart Note App · **Nhánh tham chiếu:** `huong` · **Ngày biên soạn:** 13/10/2026 · **Phiên bản tài liệu:** 1.0 (Tổng hợp và hoàn thiện theo hồ sơ baseline)
**Phạm vi quản lý:** Đầy đủ **44 chức năng FN-01..FN-44**; tập ứng viên UI gồm **31 TC UI/E2E**; bộ test đã thực thi gồm **20 UI/E2E + 24 Provider** (tổng cộng **44 automated tests**).
**Nguồn dữ liệu:** `docs/qa/automation_status.md`, `docs/qa/automation_execution_summary.md`, `test_cases/black_box/black_box_test_cases.md` (đặc tả hộp đen gốc), báo cáo kiểm thử và nhật ký thực thi.
**Mốc kết quả được báo cáo:** 12/10/2026, bộ Provider tích hợp tại commit `73514ad`; nhánh `huong` sau đó có commit tài liệu `76df421`. Đây **không phải lần chạy test mới** và không tự ý thay đổi dữ liệu lịch sử.

---

## 1. Mục đích, giới hạn và nguyên tắc

- **Mục đích:** Thiết lập và duy trì bộ kiểm thử hồi quy tự động cho các luồng nghiệp vụ cốt lõi, giảm thiểu thời gian kiểm thử lặp lại sau mỗi thay đổi mã nguồn, đồng thời phát hiện sớm sai lệch giữa kết quả kỳ vọng (Expected) và kết quả thực tế (Actual).
- **Phạm vi quản lý toàn diện:** Toàn bộ **44 chức năng (FN-01 đến FN-44)** đều được kiểm kê và phân loại trạng thái minh bạch. Không yêu cầu mọi FN đều phải có mã kiểm thử tự động, nhưng FN nào chưa tự động hóa phải nêu rõ lý do kỹ thuật hoặc nghiệp vụ.
- **Bản chất của tự động hóa:** Tự động hóa là **phương thức thực thi**, có thể kiểm tra hành vi đầu cuối tại giao diện người dùng (UI/E2E) hoặc kiểm tra logic quản lý trạng thái tại tầng Provider. Tuyệt đối **không đánh đồng việc Provider test PASS với việc chức năng đã hoàn thành kiểm thử UI/E2E thành công**.
- **Tính toàn vẹn của kết quả kiểm thử:** Không sửa đổi Expected Result hoặc assertion để ép test chuyển từ FAIL sang PASS. Phân định rạch ròi giữa lỗi ứng dụng (Application Bug), lỗi dữ liệu/tiền điều kiện (Test Data / Precondition Issue), lỗi kịch bản/bộ định vị (Script/Locator Issue), và các trường hợp bị chặn (Blocked).
- **Ranh giới số liệu độc lập:** Không tính gộp 18 Unit Tests baseline (Model/Checklist), 8 bài mô phỏng Security Rules (White-box), hay 140 execution items kiểm thử thủ công (Black-box) vào số lượng **44 kịch bản kiểm thử tự động** của tài liệu này.
- **Chốt phạm vi (FROZEN Baseline):** Bộ kịch bản kiểm thử tự động chính thức được chốt ở mốc **44 kịch bản đã thực thi** (20 UI + 24 Provider). 11 Test Cases UI chưa chạy thuộc **danh mục tồn đọng kế hoạch (Backlog)**, không được tính vào mẫu số thực thi.

---

## 2. Chiến lược kiểm thử tự động hai tầng (Two-Layer Automation Strategy)

Nhằm khắc phục rào cản tương tác phần cứng và hộp thoại hệ thống trên thiết bị di động thật, dự án áp dụng chiến lược kiểm thử tự động hai tầng bổ trợ lẫn nhau:

| Thuộc tính | Tầng 1 — Android UI/E2E Testing | Tầng 2 — Flutter Provider Automated Testing |
| --- | --- | --- |
| **Mục tiêu** | Kiểm thử luồng người dùng đầu cuối trên ứng dụng thật | Kiểm thử logic nghiệp vụ, quản lý trạng thái (State) và repository |
| **Công nghệ & Framework** | Python 3.13, pytest, uiautomator2, Android ADB | Dart, Flutter Test, FakeNoteRepository, FakeSyncRepository |
| **Môi trường thực thi** | Thiết bị vật lý Samsung Galaxy S21 FE 5G (Android 14 / API 34) | Dart VM trong bộ nhớ (In-memory Component / State Management) |
| **Đầu vào kiểm thử** | Thao tác chạm, nhập liệu form, render giao diện thực tế | Object model, Fake Repository, Stream trạng thái, Mock MethodChannel |
| **Kết quả thực thi** | 20 / 31 TC UI đã chạy (16 PASS, 4 FAIL) | 24 / 24 Tests PASS (100%) |
| **Giới hạn** | Phụ thuộc thiết bị, kết nối mạng, Google OAuth, Biometric dialog | Không kiểm thử trực tiếp render UI, bàn phím ảo hay Firebase thật |
| **Bằng chứng (Evidence)** | Báo cáo JUnit XML tại `automation/reports/`, ảnh chụp `evidence/fn*/` | Log thực thi chi tiết tại `evidence/automated/automated_test_run.log` |

### 2.1. Tiêu chí lựa chọn Test Case tự động hóa
1. Ưu tiên các luồng nghiệp vụ thường xuyên lặp lại, có độ ổn định cao, dữ liệu đầu vào xác định và kết quả kỳ vọng rõ ràng.
2. Với các luồng có thao tác xóa dữ liệu (Thùng rác, Xóa vĩnh viễn), phải thực hiện trên tài khoản/dữ liệu thử nghiệm riêng biệt, có cơ chế dọn dẹp (cleanup) để không ảnh hưởng dữ liệu khác.
3. Các luồng phụ thuộc hệ thống ngoài (Google OAuth, Prompt sinh trắc học vân tay, ngắt mạng đồng bộ 2 thiết bị) được xếp vào diện thăm dò hoặc tạm hoãn (Deferred) cho đến khi có giải pháp giả lập/can thiệp phần cứng ổn định.

---

## 3. Ma trận quản lý trạng thái tự động hóa toàn diện (44/44 FN)

**Quy ước phân loại:**
- **Đã thực thi:** Có ít nhất một bài test tự động chính thức (UI hoặc Provider) đã chạy thực tế (không đồng nghĩa toàn bộ các ca đều PASS).
- **Chỉ có script thăm dò:** Đã có script viết để thử nghiệm tương tác UI hệ thống nhưng chưa đưa vào bộ hồi quy chính thức.
- **Bị chặn (BLOCKED):** Bị cản trở bởi lỗi dịch vụ UI hoặc nguyên tắc an toàn thiết bị.
- **Chưa tự động hóa:** Chưa có kịch bản tự động; được bảo đảm chất lượng qua kiểm thử thủ công hộp đen (không khẳng định manual PASS nếu chưa có bằng chứng).

| FN-ID | Tên chức năng hệ thống | Mức | UI/E2E Testing | Provider Testing | Phân loại trạng thái | Ghi chú kỹ thuật |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **FN-01** | Kiểm tra hợp lệ form đăng nhập | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-02** | Đăng ký tài khoản Email/Password | P1 | 5 chạy (4 PASS / 1 FAIL) | — | **Đã thực thi** | 1 FAIL (TC-BB-003: sai thông báo lỗi) |
| **FN-03** | Xác thực email | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-04** | Đăng nhập tài khoản Email/Password | P1 | 4 chạy (1 PASS / 3 FAIL) | — | **Đã thực thi** | 1 Precondition Issue + 2 thông báo gộp |
| **FN-05** | Đăng nhập nhanh Google OAuth | P1 | 0 chạy (2 chưa chạy) | — | **Chỉ có script thăm dò** | Phụ thuộc Google OAuth Dialog hệ thống |
| **FN-06** | Đặt lại mật khẩu | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-07** | Đăng xuất tài khoản | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-08** | Tạo ghi chú văn bản | P1 | 3 chạy (3 PASS) | 1 test (PASS) | **Đã thực thi** | Đa tầng (UI máy thật + Provider) |
| **FN-09** | Chỉnh sửa và tự động lưu ghi chú | P1 | 2 chạy (2 PASS) | 1 test (PASS) | **Đã thực thi** | Đa tầng (UI máy thật + Provider) |
| **FN-10** | Chuyển ghi chú vào thùng rác | P1 | 0 chạy (1 chưa chạy) | 2 tests (PASS) | **Đã thực thi** | UI Planned; Provider đã hoàn thành PASS |
| **FN-11** | Khôi phục ghi chú từ thùng rác | P1 | 0 chạy (1 chưa chạy) | 3 tests (PASS) | **Đã thực thi** | UI Planned; Provider đã hoàn thành PASS |
| **FN-12** | Xóa ghi chú vĩnh viễn | P1 | 0 chạy (1 chưa chạy) | 1 test (PASS) | **Đã thực thi** | UI Planned; Provider đã hoàn thành PASS |
| **FN-13** | Lưu trữ ghi chú (Archive) | P2 | — | 1 test (PASS) | **Đã thực thi** | Provider in-memory đã hoàn thành PASS |
| **FN-14** | Bỏ lưu trữ ghi chú (Unarchive) | P2 | — | 1 test (PASS) | **Đã thực thi** | Provider in-memory đã hoàn thành PASS |
| **FN-15** | Tạo ghi chú Checklist | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-16** | Thêm mục Checklist | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-17** | Đánh dấu hoàn thành mục Checklist | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-18** | Bỏ đánh dấu mục Checklist | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-19** | Xóa mục Checklist | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-20** | Ghim và bỏ ghim ghi chú | P1 | 2 chạy (2 PASS) | 4 tests (PASS) | **Đã thực thi** | Đa tầng (UI máy thật + Provider) |
| **FN-21** | Tạo nhãn (Tag) | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-22** | Gắn nhãn vào ghi chú | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-23** | Tìm kiếm ghi chú theo văn bản | P1 | 4 chạy (4 PASS) | 3 tests (PASS) | **Đã thực thi** | Đa tầng (UI máy thật + Provider) |
| **FN-24** | Lọc ghi chú có ảnh (`has:image`) | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-25** | Lọc ghi chú có liên kết (`has:url`) | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-26** | Lọc ghi chú có âm thanh (`has:audio`)| P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-27** | Lọc ghi chú ghim/lưu trữ | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-28** | Chuyển đổi Grid/List View | P3 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-29** | Kích hoạt khóa sinh trắc học | P1 | 0 chạy (1 chưa chạy) | — | **Chỉ có script thăm dò** | Phụ thuộc phần cứng quét vân tay |
| **FN-30** | Mở khóa ghi chú bằng sinh trắc học | P1 | 0 chạy (3 chưa chạy) | — | **Chỉ có script thăm dò** | Phụ thuộc Biometric Prompt hệ thống |
| **FN-31** | Gemini AI — Tóm tắt ghi chú | P2 | — | — | **Bị BLOCKED** | Lỗi service UI khung đỏ trên thiết bị thật |
| **FN-32** | Gemini AI — Đề xuất tiêu đề | P2 | — | — | **Bị BLOCKED** | Lỗi service UI khung đỏ trên thiết bị thật |
| **FN-33** | Gemini AI — Tạo Checklist | P2 | — | — | **Bị BLOCKED** | Lỗi service UI khung đỏ trên thiết bị thật |
| **FN-34** | Xuất ghi chú PDF | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-35** | Lưu hình vẽ tay (Canvas) | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-36** | Tải ảnh lên Cloudinary | P1 | — | — | Chưa tự động hóa | Rủi ro treo tải ảnh (BUG-001) |
| **FN-37** | Đổi màu nền ghi chú | P3 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-38** | Đặt thông báo nhắc nhở | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-39** | Chạm thông báo mở ghi chú | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-40** | Bắt đầu đồng bộ dữ liệu | P1 | 0 chạy (1 chưa chạy) | 9 tests (PASS) | **Đã thực thi** | UI Offline/Sync deferred; Provider đã PASS |
| **FN-41** | Giải quyết xung đột đồng bộ LWW | P1 | 0 chạy (1 chưa chạy) | — | Chưa tự động hóa | Yêu cầu 2 thiết bị vật lý; quy tắc BR-03 |
| **FN-42** | Xử lý ghi chú rất dài | P3 | — | — | Chưa tự động hóa | Kiểm thử phi chức năng |
| **FN-43** | Xử lý ảnh dung lượng lớn (OOM) | P3 | — | — | Chưa tự động hóa | Kiểm thử phi chức năng |
| **FN-44** | Xử lý thiết bị hết bộ nhớ | P3 | — | — | **Bị BLOCKED** | Giới hạn an toàn phần cứng máy thật |

**Tổng kết phân loại 44 FN:**
- Có bài kiểm thử tự động chính thức đã thực thi: **12 FNs** (27.27%)
- Chỉ có kịch bản thăm dò UI: **3 FNs** (6.82%)
- Bị chặn (BLOCKED): **4 FNs** (9.09%)
- Chưa tự động hóa: **25 FNs** (56.82%)
- **Tổng cộng:** $\mathbf{12 + 3 + 4 + 25 = 44\ \text{FNs}}$ (khớp 100%, không thiếu, không tính trùng).
- Trong đó, **4 FNs** được bao phủ đa tầng (cả UI lẫn Provider): `FN-08`, `FN-09`, `FN-20`, `FN-23`.

---

## 4. Phạm vi 31 Test Cases UI/E2E và Kế hoạch phân kỳ

Dự án chọn lọc **31 Test Cases trọng tâm** từ bộ Black-box Master Test Suite để thiết kế và triển khai tự động hóa UI trên thiết bị thật:

| Nhóm FN | Danh sách TC-ID | Số TC | Tiến độ mã | Kết quả thực thi | Ưu tiên |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **FN-02** | `TC-BB-001`, `TC-BB-002`, `TC-BB-003`, `TC-BB-004`, `TC-BB-005` | 5 | DONE | 4 PASS / 1 FAIL | P1 |
| **FN-04** | `TC-BB-006`, `TC-BB-007`, `TC-BB-008`, `TC-BB-009` | 4 | DONE | 1 PASS / 3 FAIL | P1 |
| **FN-05** | `TC-BB-010`, `TC-BB-011` | 2 | DEFERRED | 0 PASS / 0 FAIL / 2 NOT RUN | P1 |
| **FN-08** | `TC-BB-016`, `TC-BB-017`, `TC-BB-018` | 3 | DONE | 3 PASS / 0 FAIL | P1 |
| **FN-09** | `TC-BB-019`, `TC-BB-020` | 2 | DONE | 2 PASS / 0 FAIL | P1 |
| **FN-10** | TC-BB-021 | 1 | DONE | 1 PASS / 0 FAIL | P1 |
| **FN-11** | TC-BB-022 | 1 | DONE | 1 PASS / 0 FAIL (2 runs lặp) | P1 |
| **FN-12** | TC-BB-023 | 1 | DONE | 1 PASS / 0 FAIL | P1 |
| **FN-20** | `TC-BB-024`, `TC-BB-025` | 2 | DONE | 2 PASS / 0 FAIL | P1 |
| **FN-23** | `TC-BB-026`, `TC-BB-027`, `TC-BB-028`, `TC-BB-029` | 4 | DONE | 4 PASS / 0 FAIL | P1 |
| **FN-29** | `TC-BB-012` | 1 | DEFERRED | 0 PASS / 0 FAIL / 1 NOT RUN | P1 |
| **FN-30** | `TC-BB-013`, `TC-BB-014`, `TC-BB-015` | 3 | DEFERRED | 0 PASS / 0 FAIL / 3 NOT RUN | P1 |
| **FN-40** | `TC-BB-030` | 1 | DEFERRED | 0 PASS / 0 FAIL / 1 NOT RUN | P1 |
| **FN-41** | `TC-BB-031` | 1 | DEFERRED | 0 PASS / 0 FAIL / 1 NOT RUN | P1 |
| **TỔNG** | **31 Test Cases ứng viên UI** | **31** | — | **19 PASS / 4 FAIL / 8 NOT RUN** | — |

### Phân kỳ triển khai:
- **Phase 1 — Đợt thực thi UI ban đầu (Baseline):** Gồm 20 Test Cases thuộc FN-02, FN-04, FN-08, FN-09, FN-20, FN-23. Kết quả ban đầu: **16 PASS / 4 FAIL**.
- **Phase 2 — Hoàn thành thực thi UI chu trình Thùng rác (Hoàn tất):** Gồm 3 Test Cases TC-BB-021, TC-BB-022, TC-BB-023 (FN-10, FN-11, FN-12). Đã thực thi thành công trên thiết bị thật đạt **3/3 PASS** (100%), nâng tổng số TC UI thực thi lên **23 TCs (19 PASS / 4 FAIL — 82.61%)**.
- **Phase 3 — Tạm hoãn do độ phức tạp ngoại vi (DEFERRED UI):** Gồm 8 Test Cases TC-BB-010..015, TC-BB-030..031 (Google OAuth, phần cứng sinh trắc học vân tay, ngắt kết nối mạng và giải quyết xung đột 2 thiết bị).

---

## 5. Môi trường kiểm thử và Quy tắc dữ liệu

- **Môi trường UI/E2E:** Thiết bị thật Samsung Galaxy S21 FE 5G (SM-G990B), Android 14 (API 34); cáp kết nối ADB; Python 3.13, pytest, uiautomator2; ứng dụng build debug/QA kết nối Firebase dự án. Không lưu trữ thông tin nhạy cảm (serial thiết bị thực tế, mật khẩu thật) vào tài liệu công khai.
- **Môi trường Provider:** Flutter SDK / Dart VM; bộ kiểm thử `test/automated/note_provider_test.dart` (15 tests) và `test/automated/sync_provider_test.dart` (9 tests) sử dụng `FakeNoteRepository`, `FakeSyncRepository` và mock MethodChannel.
- **Quy tắc dữ liệu kiểm thử (Test Data Rules):**
  - Đăng ký tài khoản mới (`FN-02`) sử dụng email test ngẫu nhiên kèm timestamp để tránh xung đột trùng email.
  - Đăng nhập tài khoản (`FN-04`): `TC-BB-006` yêu cầu tài khoản đã được kích hoạt xác thực email (`emailVerified: true`).
  - Dọn dẹp dữ liệu (Teardown/Cleanup): Các ghi chú tạo mới phục vụ kiểm thử tìm kiếm, ghim và chỉnh sửa phải có tiền tố nhận diện và được dọn dẹp sau khi chạy suite.

---

## 6. Quy trình thực thi và Thu thập bằng chứng

1. **Chuẩn bị:** Kiểm tra trạng thái thiết bị qua `adb devices`, kiểm tra mạng và bản build ứng dụng.
2. **Khởi tạo dữ liệu:** Thiết lập precondition và test data tương ứng cho từng nhóm kịch bản.
3. **Thực thi:** Chạy bộ test suite thông qua pytest (cho UI) hoặc flutter test (cho Provider):
   ```bash
   pytest -v -s automation/tests/test_fn02_register.py --junitxml=automation/reports/fn02_register_junit.xml
   pytest -v -s automation/tests/test_fn04_login.py --junitxml=automation/reports/fn04_login_junit.xml
   pytest -v -s automation/tests/test_fn08_create_note.py --junitxml=automation/reports/fn08_create_note_junit.xml
   pytest -v -s automation/tests/test_fn09_edit_note.py --junitxml=automation/reports/fn09_edit_note_junit.xml
   pytest -v -s automation/tests/test_fn20_pin_note.py --junitxml=automation/reports/fn20_pin_note_junit.xml
   pytest -v -s automation/tests/test_fn23_search.py --junitxml=automation/reports/fn23_search_junit.xml
   flutter test --no-pub -r expanded test/automated/
   ```
4. **Lưu trữ bằng chứng:** Ghi nhận log console, báo cáo JUnit XML tại `automation/reports/`, ảnh chụp màn hình từng bước tại `evidence/fn*/` và log Provider tại `evidence/automated/automated_test_run.log`.
5. **Xử lý thất bại:** Phân tích nguyên nhân lỗi, phân loại Application Bug hoặc Precondition Issue, đối chiếu mã lỗi với Defect Log chính thức.

---

## 7. Entry/Exit Criteria và Tiêu chuẩn nghiệm thu

- **Entry Criteria:** Môi trường thiết bị và mạng sẵn sàng; ứng dụng build QA cài đặt thành công; tài khoản thử nghiệm hợp lệ; bộ kịch bản và assertion được định nghĩa đầy đủ.
- **Exit Criteria cho lượt chạy test:** 100% kịch bản trong phạm vi được thực thi; mọi trường hợp FAIL đều có log/screenshot và được phân tích nguyên nhân minh bạch.
- **Exit Criteria cho nghiệm thu ứng dụng:** Việc bộ test tự động đạt tỷ lệ cao không tự động đồng nghĩa ứng dụng sẵn sàng phát hành nếu vẫn còn lỗi nghiêm trọng (Critical/High) chưa được giải quyết trong Defect Log toàn dự án.
- **Điều kiện chốt baseline hiện tại:** Đã thực thi **47 bài test duy nhất** gồm **23 UI TCs (19 PASS / 4 FAIL — 82.61%)** và **24 Provider Tests (24 PASS — 100%)**, tổng cộng **43 PASS / 4 FAIL (91.49%)**. 8 ca backlog UI DEFERRED chưa chạy.

---

## 8. Quản lý rủi ro và Biện pháp khắc phục

| Rủi ro kỹ thuật | Ảnh hưởng | Biện pháp giải quyết |
| --- | --- | --- |
| Bộ định vị Flutter động | Flaky test khi layout thay đổi | Kết hợp Dynamic-First (`text`, `content-desc`) với fallback tọa độ; chụp ảnh màn hình khi fail |
| Trạng thái `emailVerified` của Firebase | Fail giả (False Negative) như TC-BB-006 | Chuẩn bị trước tài khoản test đã verify email trên Firebase Console |
| Thông báo lỗi Firebase gộp | Sai lệch so với Expected Result gốc | Phân tích hành vi bảo mật (chống rò rỉ user enumeration); không tùy tiện sửa expected |
| System Dialog (OAuth, Vân tay) | Treo hoặc không tương tác được trên máy thật | Tách thành script thăm dò độc lập; không chặn bộ regression chính thức |
| Phụ thuộc dịch vụ ngoài (Gemini, Cloudinary) | Timeout hoặc lỗi khung đỏ UI | Đánh dấu BLOCKED minh bạch; bổ sung kiểm thử xử lý timeout |
| Mâu thuẫn mã lỗi giữa các tài liệu | Gây nhầm lẫn trong quản lý lỗi | Đối chiếu thống nhất với Defect Log chính thức (`docs/bugs/defect_log.md`) |

---

## 9. Sản phẩm bàn giao và Quan hệ tài liệu

- **`automation_plan.md`:** Kế hoạch tổng thể, chiến lược hai tầng và ma trận 44 FN.
- **`automation_test_cases.md`:** Đặc tả chi tiết từng Test Case cho 31 UI TCs và 24 Provider Tests.
- **`automation_execution_summary.md`:** Báo cáo chi tiết kết quả thực thi lịch sử, phân tích 4 ca FAIL và bằng chứng.
- **`docs/qa/automation_status.md`:** Bảng trạng thái và tiến độ đồng bộ hóa toàn diện.
- **`test_cases/black_box/black_box_test_cases.md`:** Nguồn đặc tả gốc của Black-box Test Suite (không bị thay thế bởi tài liệu Automation).
- **`docs/bugs/defect_log.md`:** Nhật ký quản lý lỗi chính thức toàn dự án.
