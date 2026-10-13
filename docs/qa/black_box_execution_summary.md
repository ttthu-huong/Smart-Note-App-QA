# BÁO CÁO CHỐT KẾT QUẢ THỰC THI KIỂM THỬ HỘP ĐEN (BLACK-BOX TEST REPORT)
## Dự án: Smart Note App
**Branch:** `huong`  
**Thời điểm kết thúc lượt kiểm thử:** 11/10/2026  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual / Automation Test Execution  
**Thiết bị thực thi:** 
- Thiết bị A: Samsung Galaxy S21 FE 5G (SM-G990E), Android 14 (API 34)
- Thiết bị B: Samsung Galaxy S24 FE (SM-S741B), Android 14 (API 34)

---

## I. TỔNG QUAN PHẠM VI CHỐT THEO 10 NHÓM BAN ĐẦU + CHECKLIST BỔ SUNG

Theo Kế hoạch kiểm thử (Master Test Plan), phạm vi chính thức có Execution Sheet gồm **10 nhóm chức năng ban đầu** cùng **nhóm Checklist bổ sung FN-15..19**. Tổng cộng là **11 nhóm chức năng chính thức** được theo dõi chi tiết qua 11 Execution Sheets với **140 Execution Items**. Các kết quả kiểm tra mở rộng khác được giữ tại Mục bổ sung:

> [!NOTE]
> **Đối chiếu số liệu TC và Execution Items:**  
> - Tổng cột số lượng TC từng nhóm hiện ghi nhận theo các sheet. Do chưa chứng minh được danh sách mã trùng và các sheet dùng chung để đối chiếu quy về 124, tổng số mã TC duy nhất toàn dự án được ghi là **Chưa xác minh** (không khẳng định số 124).
> - Toàn bộ số liệu thực thi kiểm thử hộp đen được chốt chính thức và đồng nhất trên **140 Execution Items**: **131 PASS**, **6 FAIL**, **2 Chưa đủ căn cứ**, **1 BLOCKED**.
> - **Quy tắc tính Executed:** Không tính ca BLOCKED vào Executed $\rightarrow$ $\text{Executed} = \text{PASS} (131) + \text{FAIL} (6) + \text{Chưa đủ căn cứ} (2) = \mathbf{139\ \text{items}}\ (99.29\%)$.

| STT | Nhóm chức năng trọng tâm | File Execution Sheet tham chiếu | Số TC | Số Exec Items | Executed (không tính BLOCKED) | PASS | FAIL | Chưa đủ căn cứ | BLOCKED | Pending | Trạng thái nhóm |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **FN-02:** Đăng ký tài khoản Email/Password | `fn02_execution_sheet.md` | 13 | 19 | 19 | 18 | 1 | 0 | 0 | 0 | **ĐÃ CHẠY (1 Bug)** |
| **2** | **FN-04:** Đăng nhập Email/Password & Form | `fn04_execution_sheet.md` | 15 | 16 | 16 | 14 | 2 | 0 | 0 | 0 | **ĐÃ CHẠY (2 Bugs)** |
| **3** | **FN-05:** Đăng nhập Google OAuth | `fn05_execution_sheet.md` | 8 | 8 | 8 | 8 | 0 | 0 | 0 | 0 | **PASS 100%** |
| **4** | **FN-08:** Tạo ghi chú văn bản & Tự động lưu | `fn08_execution_sheet.md` | 8 | 8 | 8 | 8 | 0 | 0 | 0 | 0 | **PASS 100%** |
| **5** | **FN-09:** Soạn thảo Rich-text & Cập nhật note | `fn09_execution_sheet.md` | 11 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | **ĐÃ CHẠY (1 Defect minor)** |
| **6** | **FN-10/11/12:** Thùng rác, Khôi phục, Xóa vĩnh viễn | `fn10_fn11_fn12_execution_sheet.md` | 10 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | **PASS 100%** |
| **7** | **FN-15..19:** Ghi chú danh sách (Checklist bổ sung) | `fn15_fn19_checklist_execution_sheet.md` | 6 | 6 | 6 | 6 | 0 | 0 | 0 | 0 | **PASS 100%** |
| **8** | **FN-20:** Ghim & Bỏ ghim ghi chú | `fn20_execution_sheet.md` | 14 | 15 | 15 | 15 | 0 | 0 | 0 | 0 | **PASS 100%** |
| **9** | **FN-23:** Tìm kiếm văn bản & Bộ lọc đa năng | `fn23_execution_sheet.md` | 17 | 22 | 22 | 20 | 1 | 1 | 0 | 0 | **ĐÃ CHẠY 22/22 (1 Bug)** |
| **10** | **FN-29/30:** Bảo mật sinh trắc học | `fn29_fn30_execution_sheet.md` | 12 | 12 | 11 | 11 | 0 | 0 | 1 | 0 | **ĐÃ CHẠY (1 BLOCKED)** |
| **11** | **FN-40/41:** Đồng bộ Offline & Xung đột LWW | `fn40_fn41_execution_sheet.md` | 10 | 10 | 10 | 7 | 2 | 1 | 0 | 0 | **ĐÃ CHẠY (2 Bugs)** |
| **TỔNG** | **11 nhóm có Execution Sheet (10 ban đầu + Checklist)** | **11 execution sheets** | **Chưa xác minh** | **140** | **139** | **131** | **6** | **2** | **1** | **0** | **100% PHÂN ĐỊNH** |

### Tỷ lệ phân bổ trên tổng số 140 Execution Items:
- **Tỷ lệ thực thi (Execution Rate):** $139 / 140 = \mathbf{99.29\%}$ (1 item còn lại là BLOCKED: $0.71\%$).
- **Tỷ lệ ĐẠT trên số ca đã thực thi (Pass Rate / Executed):** $131 / 139 = \mathbf{94.24\%}$.
- **Tỷ lệ KHÔNG ĐẠT trên số ca đã thực thi (Fail Rate / Executed):** $6 / 139 = \mathbf{4.32\%}$.
- **Tỷ lệ CHƯA ĐỦ CĂN CỨ trên số ca đã thực thi (Inconclusive Rate / Executed):** $2 / 139 = \mathbf{1.44\%}$.
- **Số ca chờ kiểm thử trong phạm vi chính (Pending):** $\mathbf{0}$ ca ($0.00\%$).

---

## II. KẾT QUẢ CHI TIẾT CÁC CA KIỂM THỬ ĐÃ THỰC THI THEO EXECUTION SHEET

1. **Nhóm Xác thực & Tài khoản (FN-02, FN-04, FN-05):**
   - Đăng ký thành công tài khoản mới, luồng chính hoạt động ổn định; phát hiện lỗi validate chuỗi (`BUG-FN02-01`).
   - Đăng nhập Email/Password thành công, nhận diện đúng tài khoản chưa kích hoạt; phát hiện lỗi hiển thị icon ẩn/hiện mật khẩu (`BUG-BB-002`) và xử lý khoảng trắng (`BUG-BB-003`).
   - Đăng nhập Google OAuth thành công, đồng bộ đúng thông tin và avatar người dùng.
2. **Nhóm Vòng đời Ghi chú & Thùng rác (FN-08, FN-09, FN-10/11/12, FN-20):**
   - Tạo ghi chú văn bản, tự động lưu thời gian thực xuống SQLite local hoạt động chính xác 100%.
   - Soạn thảo Rich-text lưu thành công; phát hiện lỗi giao diện giật/tràn viền thoáng qua (`BUG-005`) khi xóa trắng tiêu đề hoặc nội dung rồi quay lại Trang chủ.
   - Toàn bộ chu trình Thùng rác (Chuyển thùng rác, Khôi phục, Xóa vĩnh viễn) và Ghim ghi chú lên đầu Trang chủ đạt PASS 100%.
3. **Nhóm Checklist To-do (FN-15 đến FN-19):**
   - Toàn bộ 6/6 items (Tạo checklist, Thêm mục, Tick hoàn thành, Bỏ tick, Xóa từng mục, Lưu & mở lại) đạt PASS 100% qua các lượt xác minh có kiểm soát.
4. **Nhóm Tìm kiếm & Bộ lọc (FN-23 — Đối chiếu đầy đủ 22/22 Items):**
   - Tìm kiếm từ khóa theo Tiêu đề, Nội dung, hoa/thường, tiếng Việt có dấu, Highlight từ khóa, xóa nhanh từ khóa bằng nút 'X', bảo vệ chống SQL injection: **PASS**.
   - Bộ lọc `has:url`: **PASS** (lọc đúng note có link).
   - Bộ lọc `has:image`: **PASS** (gắn chip `[Hình ảnh]`, trả về đúng 9 ghi chú có ảnh, loại trừ note thuần văn bản).
   - Bộ lọc `has:audio`: **PASS** (gắn chip `[Âm thanh]`, trả về đúng 3 ghi chú có file âm thanh, loại trừ note thuần chữ và note ảnh).
   - Bộ lọc Trạng thái (`is:pinned`, `is:archived`): **PASS** (lọc chính xác ghi chú ghim và ghi chú lưu trữ).
   - Bộ lọc Nhãn (Tags filter): **PASS** (gắn chip `[DU_AN_TEST]`, lọc chính xác note có gắn tag).
   - Bộ lọc kết hợp Chip + Từ khóa: **PASS** (Chip `[DU_AN_TEST]` + từ khóa `"NOTE"`, lọc chính xác 1 note thỏa mãn đồng thời cả 2 điều kiện).
   - Gỡ bỏ từng viên Chip lọc: **PASS** (chạm 'X' bên trong Chip, hủy filter và trở về menu gợi ý).
   - Bộ lọc Loại danh sách `has:list` (`TC-BB-027G-D01`): **FAIL** — Ánh xạ trực tiếp vào `BUG-004` (query LIKE thô không bóc tách token, trả về sai/rỗng).
   - Tìm kiếm tiếng Việt không dấu (`TC-BB-026B-D03`): **Chưa đủ căn cứ** do SQLite mặc định không hỗ trợ unaccented folding và SRS chưa có yêu cầu đặc tả tìm không dấu.
5. **Nhóm Bảo mật Sinh trắc học (FN-29/30):**
   - Bật khóa ghi chú, yêu cầu xác thực vân tay, tự động khóa lại khi app vào background: Đạt 11 ca PASS.
   - 1 ca `TC-BB-015G-D01` **BLOCKED** do ràng buộc an toàn (Không xóa vân tay máy thật của người dùng).
6. **Nhóm Đồng bộ Offline & Xung đột LWW (FN-40/41):**
   - Tạo và sửa ghi chú offline đồng bộ lên Cloud và phân phối sang thiết bị khác thành công: PASS.
   - Thuật toán Last-Write-Wins giải quyết xung đột dựa trên timestamp `updatedAt` lớn hơn: PASS.
   - Phát hiện lỗi mất nhất quán dữ liệu do thiếu cơ chế Tombstone (`BUG-002`) và thiếu nút Pull-to-refresh (`BUG-003`).
   - 1 ca biên `TC-BB-031C-D01` (Sửa offline vs Chuyển Thùng rác) **Chưa đủ căn cứ** do SRS chưa có đặc tả phân xử ưu tiên.

---

## III. MỤC BỔ SUNG: CÁC CHỨC NĂNG ĐÃ KIỂM THỬ NGOÀI 10 NHÓM BAN ĐẦU

Các chức năng này đã được thực thi và có bằng chứng lưu trữ độc lập:
1. **FN-13 & FN-14 (Lưu trữ & Bỏ lưu trữ):** PASS (Evidence: `arc01_archive_screen.png`, `arc02_unarchived_home.png`).
2. **FN-21 & FN-22 (Tạo nhãn & Gắn nhãn):** PASS (Evidence: `tag01_create_tag.png`, `tag02_note_tagged.png`).
3. **FN-28 (Chuyển đổi Grid / List view):** PASS (Evidence: `fn28_01_before_toggle.png`, `fn28_02_after_toggle_grid.png`).
4. **FN-34 (Xuất file PDF):** PASS (Evidence: `pdf01_export_preview.png`, `pdf01_print_preview.png`).
5. **FN-35 (Vẽ tay đính kèm):** PASS (Evidence: `draw01_drawing_attached.png`).
6. **FN-36 (Tải ảnh lên Cloudinary):** Thẻ ghi chú hiển thị ảnh tải từ Cloudinary URL trên Trang chủ (`image_note_home.png`), giữ nguyên lịch sử `BUG-001` (chưa tự đóng lỗi timeout).
7. **FN-37 (Đổi màu nền ghi chú):** PASS (Evidence: `fn37_home_note_colored.png`).
8. **FN-38 (Thiết lập nhắc nhở):** PASS (Evidence: `rem01_reminder_set.png`).
9. **FN-39 (Chạm thông báo mở đúng ghi chú):** PASS (Evidence: `rem02_notification_tap_result.png`).
10. **FN-07 (Đăng xuất tài khoản):** PASS (Evidence: `auth01_logged_out.png`).
11. **Ghi âm đính kèm (Voice note):** PASS (Evidence: `rec01_audio_attached.png`).
12. **Đăng nhập khách (Guest login):** PASS (Evidence: `evidence/fn04/`).
13. **Thu hồi quyền hệ thống (Microphone/Storage):** PASS (Ứng dụng xử lý an toàn không crash).
14. **Sắp xếp ghi chú (Sort):** PASS (Evidence: `evidence/fn23/`).
15. **Đối chiếu bộ lọc `has:list`:** Ca này ánh xạ trực tiếp vào `TC-BB-027G-D01` thuộc FN-23 và đã được tính vào thống kê FAIL (`BUG-004`; Evidence: `srch02_list_filter.png`), giữ tại đây dưới dạng liên kết đối chiếu để tra cứu, không đếm trùng hai lần.

---

## IV. DANH SÁCH LỖI CÒN MỞ VÀ CÁC CA CẦN RETEST KHI CÓ BẢN FIX

Toàn bộ 8 lỗi phần mềm được quản lý chính thức tại [`docs/bugs/defect_log.md`](../bugs/defect_log.md):

| Bug ID | Mức độ nghiêm trọng | Tóm tắt lỗi | Chức năng liên quan | Test Case cần Retest khi Dev sửa |
|:---|:---:|:---|:---:|:---|
| **BUG-FN02-01** | Minor | Lỗi validation chuỗi nhập liệu form Đăng ký | FN-02 | `TC-BB-002`, `TC-BB-003` |
| **BUG-BB-002** | Minor | Lỗi icon hiển thị ẩn/hiện mật khẩu form Đăng nhập | FN-04 | `TC-BB-009D` |
| **BUG-BB-003** | Minor | Lỗi xử lý khoảng trắng đầu/cuối khi đăng nhập | FN-04 | `TC-BB-006C` |
| **BUG-001** | High | Tiến trình tải ảnh Cloudinary treo vô hạn thiếu timeout | FN-36 / Media | `TC-BB-027B-D01`, luồng Upload ảnh |
| **BUG-002** | Critical | Xóa note offline không sync xóa trên máy khác do thiếu Tombstone | FN-40 / Sync | `TC-BB-030C-D01` (Run 2 FN-40) |
| **BUG-003** | Medium | HomeScreen thiếu cử chỉ vuốt kéo làm mới (Pull-to-refresh) | FN-40 / UI | `TC-BB-030F-D01` (Run 2 FN-40) |
| **BUG-004** | Medium | Bộ lọc `has:list` query LIKE thô, không bóc tách token | FN-23 / Search | `TC-BB-027G-D01` (Lọc danh sách) |
| **BUG-005** | Minor | Giật / vệt sọc vàng đen tràn viền thoáng qua khi xóa trắng tiêu đề/nội dung | FN-09 / UI Layout | Luồng xóa trắng Editor về Home |

---

## V. PHÂN ĐỊNH RÕ RÀNG CÁC GIỚI HẠN & TRẠNG THÁI KIỂM THỬ TỒN TẠI

1. **Các ca bị chặn do môi trường & an toàn thiết bị (BLOCKED):**
   - `TC-BB-015G-D01` (FN-30): Chặn do an toàn thiết bị (Không xóa dấu vân tay của người dùng trên điện thoại thật).
   - `FN-31, FN-32, FN-33` (Trợ lý AI Gemini): Bị chặn do lỗi dịch vụ AI (thông báo lỗi đỏ trên giao diện; **nguyên nhân chưa xác định**, không kết luận quota/key chỉ từ thông báo UI).
   - `FN-44` (Xử lý khi bộ nhớ đầy): Bị chặn do nguyên tắc an toàn thiết bị (Không cố tình làm đầy bộ nhớ máy thật; thiếu máy ảo cô lập).
2. **Các ca chưa đủ căn cứ kết luận (Inconclusive / Cần làm rõ SRS):**
   - `TC-BB-031C-D01` (FN-41 - Xung đột Sửa offline vs Chuyển Thùng rác offline): SRS chưa quy định rõ thuật toán phân xử ưu tiên khi 1 máy sửa nội dung offline và 1 máy xóa ghi chú vào Thùng rác offline rồi cùng online lại.
   - `TC-BB-026B-D03` (FN-23 - Tìm kiếm tiếng Việt không dấu): SQLite mặc định không hỗ trợ unaccented folding; SRS chưa có yêu cầu bắt buộc tìm không dấu.
3. **Các ca chưa chạy trong phạm vi chính (Pending):**
   - **0 ca:** Trong toàn bộ 11 nhóm có Execution Sheet (140 execution items), $100\%$ các ca đều đã được thực thi và phân định trạng thái rõ ràng (139 Executed, 1 BLOCKED).
4. **Các mục được hoãn / loại khỏi phạm vi kiểm thử (Out-of-scope / Deferred):**
   - `FN-42` (Thử nghiệm nội dung văn bản cực lớn): Hoãn do chưa thiết kế tiêu chí tràn bộ đệm ký tự hệ thống.
   - `FN-43` (Thử nghiệm tệp ảnh dung lượng cực lớn >10MB): Hoãn do chưa thiết kế tiêu chí mock nén OOM trên máy thật.
   - `FN-03 & FN-06` (Mở liên kết kích hoạt / reset mật khẩu từ email): Hoãn do phụ thuộc tương tác với ứng dụng bên thứ ba (Web Mail / Deep Link bên ngoài ứng dụng).

---

## VI. BẢO TOÀN DỮ LIỆU, BẰNG CHỨNG & GHI CHÚ HỘP TRẮNG

1. **Bảo toàn bằng chứng kiểm thử hộp đen:**
   - `evidence/fn40_41_run_20261010_2125/`: 81 artifacts đồng bộ 2 thiết bị.
   - `evidence/search_run_20261010_1725/`: 17 artifacts tìm kiếm và bộ lọc văn bản.
   - `evidence/fn15_19_run_20261011_0005/`, `_chk05_`, `_chk06_`: Bằng chứng nhóm Checklist.
   - `evidence/fn13_14_21_22_run_20261011_0055/`: Bằng chứng các ca bổ sung (`srch05_image_filter_result.png`, `srch06_audio_filter_result.png`, `rem02_notification_tap_result.png`, video tràn viền `overflow_th1.mp4`, `overflow_th2.mp4`...).
2. **Ghi chú về kiểm thử hộp trắng (White-box):**
   - Đã có **18/18 unit tests PASS trước đó** được xác nhận theo log hiện có tại `evidence/white_box/`:
     + `checklist_test.dart`: **5 tests PASS**.
     + `checklist_copy_with_test.dart`: **4 tests PASS**.
     + `note_model_test.dart`: **9 tests PASS**.
     *(Không ghi nhận SearchService / EncryptionService trong lượt này khi chưa có log tương ứng).*
   - Trong lượt này **hoàn toàn không chạy thêm** kiểm thử hộp trắng hay phi chức năng.
3. **Cam kết tuân thủ:**
   - Dừng hoàn toàn kiểm thử hộp đen theo đúng yêu cầu, không chạy thêm bất kỳ test nào.
   - Không sửa bất kỳ dòng mã nguồn nào trong `lib/`.
   - Chưa thực hiện lệnh `git commit` hay `git push`.

