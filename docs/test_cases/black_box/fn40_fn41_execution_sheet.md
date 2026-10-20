# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-40 / FN-41

**Chức năng:** Đồng bộ Offline/Online & Giải quyết xung đột LWW (FN-40, FN-41)  
**Tiêu chuẩn thiết kế:** IEEE 829 & ISTQB  
**Phương pháp:** Black-box Testing (Góc nhìn người dùng cuối qua mô hình 2 thiết bị vật lý đối chiếu trực tiếp trên UI & SQLite)  
**Trạng thái tài liệu:** RUN 2 HOÀN TẤT — 7 PASS | 2 FAIL | 1 CHƯA ĐỦ CĂN CỨ KẾT LUẬN | 0 BLOCKED

---

## 1. THÔNG TIN MÔI TRƯỜNG KIỂM THỬ (TEST ENVIRONMENT)

| Thành phần | Thiết bị A (Device A) | Thiết bị B (Device B) |
| :--- | :--- | :--- |
| **Loại thiết bị** | Thiết bị thực tế (Physical Device) | Thiết bị thực tế (Physical Device) |
| **Model / Tên máy** | Samsung Galaxy S21 FE 5G (Serial: `R5CW82ECF6M`) | Samsung Galaxy S24 FE (Serial: `192.168.1.12:45695`) |
| **Phương thức kết nối** | Cáp USB ADB trực tiếp | Wireless ADB (Wi-Fi 5GHz) |
| **Hệ điều hành** | Android 14 (API 34, One UI 6.1) | Android 14 (API 34, One UI 6.1) |
| **Tài khoản kiểm thử** | `student_qa@gmail.com` | `student_qa@gmail.com` (Cùng tài khoản) |
| **Kết nối mạng** | Wi-Fi / 4G (Điều khiển qua `svc wifi enable/disable`) | Wi-Fi duy trì kết nối mạng Internet & ADB |
| **Ứng dụng kiểm thử** | Smart Note App (Build v1.0.0+1) | Smart Note App (Build v1.0.0+1) |
| **Ghi chú môi trường** | **Run 2 (21:25 - 23:55 10/10/2026):** Đã kết nối thành công 2 thiết bị vật lý độc lập. Cả 2 máy đều đã đăng nhập cùng tài khoản `student_qa@gmail.com`, màn hình sáng liên tục (`stay_on_while_plugged_in`), thực hiện đồng bộ 2 chiều qua Firebase Cloud Firestore & SQLite local. |

---

## 2. TIỀN ĐIỀU KIỆN & DỮ LIỆU KIỂM THỬ (PRECONDITIONS)

1. **Cùng đăng nhập tài khoản kiểm thử duy nhất:** Cả Thiết bị A và Thiết bị B đều đã đăng nhập cùng tài khoản `student_qa@gmail.com`. (ĐÃ ĐÁP ỨNG).
2. **Khả năng kiểm soát mạng độc lập:** Tester kiểm soát mạng Thiết bị A qua ADB (`adb -s R5CW82ECF6M shell svc wifi enable/disable`) mà không làm gián đoạn Thiết bị B. (ĐÃ ĐÁP ỨNG).
3. **Mô hình kiểm thử hai thiết bị (Cross-device Testing):** Mọi hành vi đồng bộ và xung đột được kiểm chứng bằng cách quan sát sự thay đổi trạng thái/nội dung ghi chú trực tiếp trên màn hình của hai thiết bị, đồng thời đối chiếu dữ liệu vật lý tại SQLite database (`smart_note.db`).
4. **Lịch sử thực thi:**
   - **Lượt 1 (Run 1 - 18:15 10/10/2026):** 10/10 items **BLOCKED** do thiếu thiết bị thứ hai. Lưu tại [`evidence/fn40_41_run_20261010_1815/run_log.md`](../../evidence/fn40_41_run_20261010_1815/run_log.md).
   - **Lượt 2 (Run 2 - 21:25 - 23:55 10/10/2026):** Đầy đủ 2 thiết bị Samsung Galaxy S21 FE & S24 FE. Hoàn tất 10/10 execution items. Lưu evidence tại [`evidence/fn40_41_run_20261010_2125/`](../../evidence/fn40_41_run_20261010_2125/).

---

## 3. BẢNG THỰC THI KIỂM THỬ (EXECUTION TABLE — RUN 2)

| TC-ID | Data ID | Kịch bản / Input | Expected Result | Actual Result [Run 2] | Trạng thái [Run 2] | Evidence ID | Bug ID |
| :--- | :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| **TC-BB-030** | **D01** | Tạo ghi chú mới khi offline trên Thiết bị A $\rightarrow$ Khôi phục kết nối mạng | Trên Dev A: Ghi chú hiển thị ngay.<br>Sau khi khôi phục mạng: Tự động đồng bộ lên Cloud; trên Dev B ghi chú tự động xuất hiện với đầy đủ tiêu đề và nội dung. | Dev A offline tạo `FN40_Khao_nghiem_offline` thành công. Sau khi bật lại Wi-Fi và khởi động lại app, ghi chú xuất hiện đầy đủ trên HomeScreen của Dev B. SQLite cả 2 máy: `is_synced=1`. | **PASS** | `01_tc_bb_030_d01_*.png` | [Không] |
| **TC-BB-030B** | **D01** | Chỉnh sửa nội dung ghi chú khi offline trên Thiết bị A $\rightarrow$ Khôi phục mạng | Trên Dev A: Nội dung cập nhật ngay.<br>Sau khi khôi phục mạng: Dev B tự động cập nhật nội dung mới đầy đủ và chính xác. | Dev A offline sửa `FN40_Hop_ky_thuat` thành `..._Cap_nhat_ngoai_tuyen_thanh_cong`. Bật lại Wi-Fi, Dev B cập nhật chính xác nội dung mới. | **PASS** | `02_tc_bb_030b_d01_*.png` | [Không] |
| **TC-BB-030C** | **D01** | Xóa vĩnh viễn ghi chú khi offline trên Thiết bị A $\rightarrow$ Khôi phục mạng (Hàng đợi xóa) | Sau khi Dev A có mạng: Hàng đợi xóa giải phóng; trên Dev B ghi chú biến mất khỏi danh sách Trang chủ và Thùng rác. | **DEFECT:** Dev A offline xóa vĩnh viễn ghi chú `FN40_Ghi_chu_tam_xoa`. Sau khi có mạng, ghi chú bị xóa trên Firebase Cloud, nhưng trên Dev B ghi chú **vẫn còn nguyên** trong SQLite (`status=normal`) và hiển thị trên màn hình. App thiếu cơ chế tombstone/đồng bộ xóa local cho các client khác. | **FAIL** | `03_tc_bb_030c_d01_*.png`, `dev_a.db`, `dev_b.db` | **BUG-002** |
| **TC-BB-030D** | **D01** | Ghim ghi chú khi offline trên Thiết bị A $\rightarrow$ Khôi phục mạng | Sau khi Dev A có mạng: Dev B tự động cập nhật; ghi chú chuyển lên phân vùng `"Được ghim"`. | Dev A offline ghim `FN40_Tai_lieu_tham_khao`. Sau khi khôi phục mạng, Dev B tự động đưa ghi chú vào khu vực "ĐƯỢC GHIM". SQLite cả 2 máy: `status=pinned`. | **PASS** | `04_tc_bb_030d_d01_*.png` | [Không] |
| **TC-BB-030E** | **D01** | Kích hoạt khóa bảo vệ khi offline trên Thiết bị A $\rightarrow$ Khôi phục mạng | Sau khi Dev A có mạng: Thẻ ghi chú trên Dev B chuyển sang icon 🔒 cùng thông báo nội dung đã được bảo vệ; yêu cầu sinh trắc học để mở. | Dev A quét vân tay khóa offline thành công. Sau khi khôi phục mạng, Dev B hiển thị `🔒 Ghi chú đã khóa - Nội dung đã được bảo vệ`. SQLite: `is_locked=1` trên cả 2 máy. | **PASS** | `05_tc_bb_030e_d01_*.png` | [Không] |
| **TC-BB-030F** | **D01** | Kéo vuốt xuống (Pull-to-refresh) tại Trang chủ trên Thiết bị B để chủ động kéo dữ liệu đồng bộ | Biểu tượng làm mới xoay mượt mà ở đỉnh màn hình; ghi chú mới xuất hiện ngay đầu danh sách Trang chủ Dev B. | **DEFECT:** Dev A online tạo ghi chú `FN40_Nhiem_vu_dot_xuat`. Trên Dev B, thực hiện thao tác vuốt kéo xuống từ đỉnh danh sách nhưng không xuất hiện vòng tròn xoay làm mới (RefreshIndicator) và không có phản hồi kích hoạt kéo dữ liệu từ máy chủ. HomeScreen thiếu widget `RefreshIndicator`. | **FAIL** | `06_tc_bb_030f_d01_*.png` | **BUG-003** |
| **TC-BB-031** | **D01** | Hai thiết bị cùng sửa 1 ghi chú — Thiết bị B online sửa sau ($t_B > t_A$) $\rightarrow$ Giữ bản B (LWW) | Cả Thiết bị A và Thiết bị B đều hiển thị thống nhất phiên bản của Thiết bị B. Bản cũ của A bị ghi đè tự động. | Dev A sửa offline lúc $t_A$, Dev B sửa online lúc $t_B$ ($t_B > t_A$). Sau khi A bật mạng và sync, cả 2 máy đều giữ bản của B (`_B_online_sau_cung_tB`). SQLite `updated_at=1791649201692` trên cả 2 máy. | **PASS** | `07_tc_bb_031_d01_*.png` | [Không] |
| **TC-BB-031B** | **D01** | Hai thiết bị cùng sửa 1 ghi chú — Thiết bị A offline sửa sau ($t_A > t_B$) $\rightarrow$ Bản A ghi đè bản B | Sau khi A có mạng, nhận diện $t_A > t_B$, tự động đẩy bản của A lên. Cả 2 máy hiển thị thống nhất bản A sửa sau cùng. | Dev B sửa online lúc $t_B$, Dev A sửa offline sau đó lúc $t_A$ ($t_A > t_B$). Sau khi A bật mạng và sync, cả 2 máy đều cập nhật bản của A (`_A_offline_sau_cung_tA`). SQLite `updated_at=1791649937854` trên cả 2 máy. | **PASS** | `08_tc_bb_031b_d01_*.png` | [Không] |
| **TC-BB-031C** | **D01** | Xung đột giữa Sửa offline trên Thiết bị A ($t_A$) và Chuyển vào Thùng rác trên Thiết bị B ($t_B$) | Đánh giá tính nhất quán và quy tắc nghiệp vụ khi $t_A > t_B$. | **As-built Actual:** Dev B online chuyển note vào Thùng rác lúc $t_B$. Dev A offline sửa nội dung lúc $t_A$ ($t_A > t_B$). Sau khi A có mạng lại, do $t_A > t_B$, LWW ghi đè toàn bộ record, `status: 'normal'` của A ghi đè `status: 'trash'` của B $\rightarrow$ Ghi chú tự động "hồi sinh" khỏi Thùng rác về HomeScreen trên cả 2 máy với nội dung mới của A.<br>**Đánh giá:** SRS hiện chưa có đặc tả nghiệp vụ phân xử giữa thao tác Sửa sau vs Xóa/Thùng rác trước $\rightarrow$ Không đủ căn cứ kết luận PASS hay FAIL theo SRS. | **CHƯA ĐỦ CĂN CỨ KẾT LUẬN** | `09_tc_bb_031c_d01_*.png`, `drawer_dev_*.png`, `tools/query_fn41.py` | [Cần làm rõ SRS] |
| **TC-BB-031D** | **D01** | Đăng nhập tài khoản trên thiết bị mới $\rightarrow$ Toàn bộ dữ liệu đám mây tự động kéo về đầy đủ | Ứng dụng tự động kéo toàn bộ ghi chú từ đám mây về Thiết bị B mới đăng nhập, hiển thị đầy đủ tiêu đề, nội dung, ghim, khóa. | Đăng nhập tài khoản `student_qa@gmail.com` trên Thiết bị B mới. Toàn bộ ghi chú trên Cloud được tải về đầy đủ, chính xác, phân vùng ghim và khóa hiển thị đúng chuẩn. | **PASS** | `10_tc_bb_031d_d01_*.png` | [Không] |

---

## 4. TỔNG KẾT METRICS THỰC THI (LƯỢT CHẠY 2 — 10/10/2026)

| Chỉ số | Số lượng [Run 1] | Số lượng [Run 2] | Tỷ lệ Run 2 (%) | Ghi chú & Đánh giá Run 2 |
|---|---|---|---|---|
| **Tổng số Test Cases chính thức** | **10** | **10** | — | TC-BB-030, 030B, 030C, 030D, 030E, 030F, 031, 031B, 031C, 031D |
| **Tổng số Execution Items** | **10** | **10** | **100%** | Mỗi Test Case tương ứng 1 Execution Item độc lập (D01) |
| **Tỷ lệ thực thi (Execution Rate)** | 10 / 10 | 10 / 10 | 100% | Đã thực thi trọn vẹn trên 2 thiết bị vật lý thực tế |
| **Số lượng PASS** | 0 | **7** | **70%** | 7 ca đạt chuẩn hoàn hảo (Đồng bộ tạo/sửa/ghim/khóa, LWW Case 1, LWW Case 2, Fresh Login) |
| **Số lượng FAIL** | 0 | **2** | **20%** | Phát hiện 2 defects (Xóa offline không sync xóa local khác máy, Thiếu Pull-to-refresh) |
| **Chưa đủ căn cứ kết luận** | 0 | **1** | **10%** | `TC-BB-031C`: Xung đột Sửa offline vs Xóa thùng rác (SRS chưa đặc tả) |
| **Số lượng BLOCKED** | **10** | **0** | **0%** | Đã giải tỏa hoàn toàn 100% các ca bị chặn của Run 1 |
| **Số Bug phát hiện mới** | 0 | **2** | — | `BUG-002` (Critical) & `BUG-003` (Medium) |

---

## 5. DANH MỤC BẰNG CHỨNG (RUN 2 EVIDENCE ARCHIVE)

Thư mục lưu trữ: [`evidence/fn40_41_run_20261010_2125/`](../../evidence/fn40_41_run_20261010_2125/)

- `01_tc_bb_030_d01_dev_a_offline_created.png`, `01_tc_bb_030_d01_dev_b_before_sync.png`, `01_tc_bb_030_d01_dev_a_synced.png`, `01_tc_bb_030_d01_dev_b_synced.png`
- `02_tc_bb_030b_d01_dev_a_initial.png`, `02_tc_bb_030b_d01_dev_b_initial.png`, `02_tc_bb_030b_d01_dev_a_offline_edited.png`, `02_tc_bb_030b_d01_dev_a_synced.png`, `02_tc_bb_030b_d01_dev_b_synced.png`
- `03_tc_bb_030c_d01_dev_a_initial.png`, `03_tc_bb_030c_d01_dev_b_initial.png`, `03_tc_bb_030c_d01_dev_a_trash.png`, `03_tc_bb_030c_d01_dev_a_deleted_perm.png`, `03_tc_bb_030c_d01_dev_a_synced.png`, `03_tc_bb_030c_d01_dev_b_defect_still_exists.png`
- `04_tc_bb_030d_d01_dev_a_initial.png`, `04_tc_bb_030d_d01_dev_b_initial.png`, `04_tc_bb_030d_d01_dev_a_offline_pinned.png`, `04_tc_bb_030d_d01_dev_a_synced.png`, `04_tc_bb_030d_d01_dev_b_synced.png`
- `05_tc_bb_030e_d01_dev_a_initial.png`, `05_tc_bb_030e_d01_dev_b_initial.png`, `05_tc_bb_030e_d01_dev_a_offline_locked.png`, `05_tc_bb_030e_d01_dev_a_synced.png`, `05_tc_bb_030e_d01_dev_b_synced.png`
- `06_tc_bb_030f_d01_dev_a_created.png`, `06_tc_bb_030f_d01_dev_b_before_pull.png`, `06_tc_bb_030f_d01_dev_b_after_pull.png`
- `07_tc_bb_031_d01_dev_a_initial.png`, `07_tc_bb_031_d01_dev_b_initial.png`, `07_tc_bb_031_d01_dev_a_offline_edited.png`, `07_tc_bb_031_d01_dev_b_online_edited.png`, `07_tc_bb_031_d01_dev_a_synced.png`, `07_tc_bb_031_d01_dev_b_synced.png`
- `08_tc_bb_031b_d01_dev_a_initial.png`, `08_tc_bb_031b_d01_dev_b_initial.png`, `08_tc_bb_031b_d01_dev_b_online_edited.png`, `08_tc_bb_031b_d01_dev_a_offline_edited.png`, `08_tc_bb_031b_d01_dev_a_synced.png`, `08_tc_bb_031b_d01_dev_b_synced.png`
- `09_tc_bb_031c_d01_dev_a_initial.png`, `09_tc_bb_031c_d01_dev_b_initial.png`, `09_tc_bb_031c_d01_dev_b_deleted_to_trash.png`, `09_tc_bb_031c_d01_dev_a_offline_edited.png`, `09_tc_bb_031c_d01_dev_a_synced.png`, `09_tc_bb_031c_d01_dev_b_synced.png`, `09_tc_bb_031c_d01_dev_a_trash.png`, `09_tc_bb_031c_d01_dev_b_trash.png`
- `10_tc_bb_031d_d01_dev_a_cloud_synced.png`, `10_tc_bb_031d_d01_dev_b_fresh_login_synced.png`
- SQLite snapshots: `tools/dev_a.db`, `tools/dev_b.db`, scripts kiểm tra `tools/check_sync_dbs.py`, `tools/query_fn41.py`.

---

## 6. BÁO CÁO LỖI (BUG REPORT) PHÁT HIỆN TỪ RUN 2

| Bug ID | TC-ID | Data ID | Mô tả lỗi quan sát được trên UI & Database | Mức độ nghiêm trọng | Trạng thái |
|---|---|---|---|---|---|
| **BUG-002** | TC-BB-030C | D01 | Xóa ghi chú khi offline trên Thiết bị A: Sau khi A có mạng, note bị xóa trên Firebase Cloud nhưng trên Thiết bị B ghi chú vẫn còn nguyên trong SQLite local và vẫn hiển thị trên HomeScreen (Thiếu cơ chế Tombstone đồng bộ xóa). | **CRITICAL** | **OPEN** |
| **BUG-003** | TC-BB-030F | D01 | Màn hình HomeScreen không hỗ trợ cử chỉ vuốt kéo xuống để làm mới (Pull-to-refresh), thiếu widget `RefreshIndicator`, người dùng không thể chủ động kéo dữ liệu đồng bộ mới nhất về máy. | **MEDIUM** | **OPEN** |
