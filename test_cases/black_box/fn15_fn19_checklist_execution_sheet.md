# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG CHECKLIST (FN-15 ĐẾN FN-19)

**Chức năng:** Ghi chú Danh sách công việc (Checklist / To-do list) — FN-15 đến FN-19  
**Tiêu chuẩn thiết kế:** IEEE 829 & ISTQB  
**Phương pháp:** Black-box Testing (Kiểm thử hộp đen tương tác trực tiếp trên UI thiết bị thật & đối chiếu SQLite)  
**Trạng thái tài liệu:** ĐÃ XÁC MINH TOÀN DIỆN — 6 PASS | 0 FAIL | 0 CHƯA ĐỦ CĂN CỨ | 0 BLOCKED | 0 DEFECTS

---

## 1. THÔNG TIN MÔI TRƯỜNG KIỂM THỬ (TEST ENVIRONMENT)

| Thành phần | Thông số môi trường | Ghi chú |
| :--- | :--- | :--- |
| **Thiết bị kiểm thử** | Samsung Galaxy S21 FE 5G (Serial: `R5CW82ECF6M`) | Thiết bị vật lý thật (Physical Device) |
| **Hệ điều hành** | Android 14 (API 34, One UI 6.1) | Môi trường chuẩn QA |
| **Phương thức kết nối** | Cáp USB ADB trực tiếp | Tốc độ truyền tải và tương tác tức thời |
| **Ứng dụng kiểm thử** | Smart Note App (Build `v1.0.0+1`) | Cùng bản build thử nghiệm hiện hành |
| **Tài khoản kiểm thử** | `student_qa@gmail.com` | Đang đăng nhập sẵn trên thiết bị |
| **Thời gian thực thi** | 00:05 — 00:39 ngày 11/10/2026 | Bao gồm 3 lượt: Chạy ban đầu (00:05), Xác minh CHK-06 (00:25), Xác minh CHK-05 (00:35) |
| **Thư mục Evidence** | - Lượt ban đầu: [`evidence/fn15_19_run_20261011_0005/`](../../evidence/fn15_19_run_20261011_0005/)<br>- Lượt xác minh CHK-06: [`evidence/fn15_chk06_run_20261011_0025/`](../../evidence/fn15_chk06_run_20261011_0025/)<br>- Lượt xác minh CHK-05: [`evidence/fn15_chk05_run_20261011_0035/`](../../evidence/fn15_chk05_run_20261011_0035/) | Ảnh screenshots + snapshots SQLite tách biệt theo timestamp |

---

## 2. TIỀN ĐIỀU KIỆN & PHẠM VI (PRECONDITIONS & SCOPE)

1. **Phạm vi kiểm thử:** Giới hạn đúng 6 kịch bản trọng tâm theo yêu cầu:
   - Tạo ghi chú checklist (FN-15).
   - Thêm các mục checklist (FN-16).
   - Tick hoàn thành mục (FN-17).
   - Bỏ tick hoàn thành mục (FN-18).
   - Xóa một mục và kiểm tra các mục còn lại (FN-19).
   - Lưu, thoát và mở lại để kiểm tra nội dung, thứ tự, trạng thái checkbox bền vững.
2. **Không tự sửa kỳ vọng:** Expected Result được giữ nguyên theo đặc tả nghiệp vụ chuẩn, không điều chỉnh để hợp thức hóa ứng dụng.
3. **Phân tách kết quả:** Giữ nguyên kết quả 18/18 unit test đã có trong `test/checklist_test.dart` và `test/checklist_copy_with_test.dart` (không chạy lại); báo cáo này ghi nhận độc lập kết quả kiểm thử giao diện người dùng (UI Black-box).
4. **Quy tắc đếm Execution Items:** Số lần chạy lại / xác minh độc lập không làm tăng số lượng execution items thiết kế (vẫn giữ đúng 6 items cho nhóm Checklist).

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE)

| TC-ID | FN-ID | Kịch bản / Input | Các bước thực hiện | Expected Result | Actual Result | Trạng thái | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **TC-BB-CHK-01** | FN-15 | Tạo ghi chú checklist | 1. Tại Trang chủ, nhấn nút Tạo mới (+).<br>2. Nhập Tiêu đề: `"FN15_Ke_hoach_checklist"`.<br>3. Mở thanh công cụ đáy, bấm nút Thêm (`+`), chọn `"Danh sách"`. | Giao diện chuyển sang chế độ Checklist; hiển thị ô nhập mục đầu tiên kèm icon checkbox trống (`checked = false`) và biểu tượng kéo thả (`Icons.drag_indicator`). | Ứng dụng chuyển sang Checklist mode; hiển thị mục đầu tiên với CheckBox `checked=false` tại tọa độ `[105,610][168,673]`, nút `+ Mục danh sách` ở dưới. Khớp 100% kỳ vọng. | **PASS** | `chk_01_create_checklist.png` | [Không] |
| **TC-BB-CHK-02** | FN-16 | Thêm các mục checklist | 1. Nhập Mục 1: `"Nop_bao_cao_tuan"`.<br>2. Bấm `+ Mục danh sách`, nhập Mục 2: `"Gap_khach_hang_doi_tac"`.<br>3. Bấm `+ Mục danh sách`, nhập Mục 3: `"Kiem_tra_sprint"`. | Danh sách có đủ 3 mục phân biệt với nội dung chính xác; mỗi mục có checkbox riêng (`checked = false`) và nút xóa riêng. | **CHUẨN HÓA CĂN CỨ XÁC MINH:**<br>- Ở lượt chạy ban đầu (00:05), khâu tạo 3 mục bị lỗi lặp chuỗi tại Mục 1 do thao tác runner.<br>- Đối chiếu với bằng chứng tạo 3 mục phân biệt chuẩn xác nguyên văn trong lượt xác minh CHK-06 (`MUC_A_111`, `MUC_B_222`, `MUC_C_333`) và khâu chuẩn bị CHK-05 (`DELETE_A_111`, `DELETE_B_222`, `DELETE_C_333`): Mỗi mục đều có CheckBox độc lập (`checked = false`), ô nhập liệu riêng biệt và icon Close xóa riêng (`Icons.close`). Đáp ứng đầy đủ 100% Expected Result của CHK-02 mà không phát sinh thêm execution item. | **PASS** | [`chk_02_add_items.png`](../../evidence/fn15_19_run_20261011_0005/chk_02_add_items.png)<br>Dẫn chiếu: [`chk06_01_before_save.png`](../../evidence/fn15_chk06_run_20261011_0025/chk06_01_before_save.png)<br>Dẫn chiếu: [`chk05_01_before_delete.png`](../../evidence/fn15_chk05_run_20261011_0035/chk05_01_before_delete.png) | [Không] |
| **TC-BB-CHK-03** | FN-17 | Tick hoàn thành mục checklist | 1. Chạm vào ô checkbox của Mục 1 (`Nop_bao_cao_tuan`).<br>2. Quan sát trạng thái checkbox và định dạng chữ. | Checkbox Mục 1 chuyển sang trạng thái đã chọn (tích xanh, `checked = true`); văn bản mục có gạch ngang (`lineThrough`) và màu xám mờ; các mục khác không bị ảnh hưởng. | Checkbox Mục 1 chuyển sang `checked="true"`; chữ hiển thị gạch ngang mờ; Checkbox Mục 2 và Mục 3 vẫn giữ nguyên `checked="false"`. | **PASS** | `chk_03_tick_completed.png` | [Không] |
| **TC-BB-CHK-04** | FN-18 | Bỏ tick hoàn thành mục checklist | 1. Chạm lại vào ô checkbox của Mục 1 đang hoàn thành.<br>2. Quan sát phản hồi UI. | Checkbox Mục 1 bỏ tích (`checked = false`); chữ trở về kiểu bình thường (hết gạch ngang, màu chữ chuẩn). | Checkbox Mục 1 chuyển lại thành `checked="false"`; hiệu ứng gạch ngang biến mất, màu chữ trở lại bình thường. | **PASS** | `chk_04_untick_completed.png` | [Không] |
| **TC-BB-CHK-05** | FN-19 | Xóa một mục và kiểm tra các mục còn lại | 1. Tạo note mới `FN15_CHK05_Verify_Delete_Item` với 3 mục: A (`DELETE_A_111`, unchecked), B (`DELETE_B_222`, checked), C (`DELETE_C_333`, checked).<br>2. Chạm vào icon nút xóa (`Icons.close`) bên phải Mục B tại tọa độ `(1025, 872)`.<br>3. Kiểm tra danh sách sau xóa.<br>4. Lưu về Home, mở lại vào Editor và đối chiếu SQLite. | Mục B bị xóa hoàn toàn khỏi danh sách; danh sách còn lại đúng 2 mục (Mục A và C); Mục A giữ nguyên unchecked, Mục C giữ nguyên checked; thứ tự A-C toàn vẹn không mất ký tự kể cả sau khi lưu và mở lại. | **LƯỢT 2 XÁC MINH ĐỘC LẬP (00:35 11/10/2026): ĐẠT (PASS)**<br>- Trước khi xóa: Đủ 3 mục A (false), B (true), C (true).<br>- Thao tác xóa: Dùng nút xóa (`Icons.close`) của Mục B. Mục B biến mất ngay lập tức.<br>- Danh sách sau xóa: Chỉ còn Mục A (`DELETE_A_111`, unchecked) và Mục C (`DELETE_C_333`, checked); thứ tự A-C không nối chuỗi.<br>- Lưu & Mở lại: Thẻ Home preview và Editor hiển thị đúng A và C với checkbox nguyên vẹn.<br>- SQLite Note ID `dfff866b-aced-4c1c-a482-8b67a307703c`: Content JSON chỉ chứa 2 item A (checked=false) và C (checked=true).<br>- Cờ `is_synced = 1` ghi nhận là cờ đồng bộ cục bộ.<br>*(Lịch sử Lượt 1: CHƯA ĐỦ CĂN CỨ KẾT LUẬN do chuỗi Mục 1 bị nối sai từ khâu nhập liệu của runner)* | **PASS** *(Lượt 2)* | [`chk05_01_before_delete.png`](../../evidence/fn15_chk05_run_20261011_0035/chk05_01_before_delete.png)<br>[`chk05_02_after_delete.png`](../../evidence/fn15_chk05_run_20261011_0035/chk05_02_after_delete.png)<br>[`chk05_03_home_preview.png`](../../evidence/fn15_chk05_run_20261011_0035/chk05_03_home_preview.png)<br>[`chk05_04_reopened_editor.png`](../../evidence/fn15_chk05_run_20261011_0035/chk05_04_reopened_editor.png)<br>`smart_note_chk05.db` | [Không] |
| **TC-BB-CHK-06** | FN-15, 16, 17, 18, 19 | Lưu, thoát và mở lại kiểm tra tính bền vững dữ liệu | 1. Tạo note mới `FN15_CHK06_Verify_Save_Reopen`, 3 mục `MUC_A_111`, `MUC_B_222`, `MUC_C_333`.<br>2. Tick rồi bỏ tick A (A=false), tick C (C=true), giữ B=false.<br>3. Thoát về HomeScreen lưu tự động.<br>4. Mở lại ghi chú vào Editor. | Nội dung các mục toàn vẹn, thứ tự A-B-C chính xác, trạng thái checkbox giữ nguyên (A=false, B=false, C=true). | **LƯỢT 2 XÁC MINH ĐỘC LẬP (00:25 11/10/2026): ĐẠT (PASS)**<br>- Trước khi lưu: A=false, B=false, C=true; thứ tự A-B-C.<br>- HomeScreen: Thẻ preview hiển thị đúng tiêu đề và danh sách 3 mục.<br>- Mở lại vào Editor: A=false, B=false, C=true (gạch ngang); nội dung và thứ tự giữ nguyên 100%.<br>- SQLite Note ID `882ce48a-219d-45b0-bfbd-840bd294debf`: JSON đúng schema, đúng thứ tự và trạng thái.<br>- Cờ `is_synced = 1` ghi nhận là cờ đồng bộ cục bộ.<br>*(Lịch sử Lượt 1: CHƯA ĐỦ CĂN CỨ KẾT LUẬN do thao tác tap ngoài kế hoạch và dữ liệu nối chuỗi)* | **PASS** *(Lượt 2)* | [`chk06_01_before_save.png`](../../evidence/fn15_chk06_run_20261011_0025/chk06_01_before_save.png)<br>[`chk06_02_home_preview.png`](../../evidence/fn15_chk06_run_20261011_0025/chk06_02_home_preview.png)<br>[`chk06_03_reopened_editor.png`](../../evidence/fn15_chk06_run_20261011_0025/chk06_03_reopened_editor.png)<br>`chk06_verify.db` | [Không] |

---

## 4. TỔNG KẾT METRICS THỰC THI (NHÓM CHECKLIST FN-15 ĐẾN FN-19)

| Chỉ số | Số lượng | Tỷ lệ (%) | Ghi chú & Đánh giá |
| :--- | :---: | :---: | :--- |
| **Tổng số kịch bản thiết kế** | **6** | **100%** | Giữ nguyên 6 execution items chuẩn theo thiết kế, không tăng theo số lần chạy |
| **Số ca thực thi thành công (PASS)** | **6** | **100%** | Toàn bộ 6/6 kịch bản đều đạt sau các lượt xác minh độc lập |
| **Số ca cần xác minh (Inconclusive)** | **0** | **0%** | Đã giải quyết triệt để bằng các lượt xác minh có kiểm soát |
| **Số ca thất bại (FAIL)** | **0** | **0%** | Không có lỗi logic ứng dụng trong phạm vi nhóm Checklist |
| **Số ca bị chặn (BLOCKED)** | **0** | **0%** | Thiết bị hoạt động hoàn toàn ổn định |
| **Số ca chưa chạy (NOT RUN)** | **0** | **0%** | Hoàn tất đầy đủ 100% phạm vi |
| **Số Bug phát hiện mới** | **0** | — | Không phát hiện lỗi mới |
