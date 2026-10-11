# RUN LOG KIỂM THỬ ĐỒNG BỘ CROSS-DEVICE & XUNG ĐỘT LWW (RUN 2)
## Nhóm chức năng: FN-40 (Đồng bộ nhiều thiết bị) & FN-41 (Xử lý xung đột LWW)
* **Thời gian thực hiện:** 21:25:00 — 23:55:00 ngày 10/10/2026
* **Môi trường thực thi:** 02 thiết bị Android vật lý độc lập
  - **Device A:** Samsung Galaxy S21 FE 5G (Serial: `R5CW82ECF6M`, USB ADB, Android 14 API 34)
  - **Device B:** Samsung Galaxy S24 FE (Serial: `192.168.1.12:45695`, Wireless ADB, Android 14 API 34)
* **Tài khoản kiểm thử:** `student_qa@gmail.com` (Đăng nhập đồng thời trên cả hai máy)
* **Ứng dụng:** Smart Note App build `v1.0.0+1`
* **Người thực hiện:** QA Engineering / Automation Agent

---

## 1. TỔNG KẾT KẾT QUẢ THỰC THI (EXECUTIVE SUMMARY)

| Chỉ số | Kết quả | Tỷ lệ (%) |
| :--- | :---: | :---: |
| **Tổng số kịch bản (Execution Items)** | **10** | **100%** |
| **Số ca ĐẠT (PASS)** | **7** | **70%** |
| **Số ca KHÔNG ĐẠT (FAIL)** | **2** | **20%** |
| **Số ca CHƯA ĐỦ CĂN CỨ KẾT LUẬN** | **1** | **10%** |
| **Số ca BỊ CHẶN (BLOCKED)** | **0** | **0%** |
| **Defects phát hiện mới** | **2** (`BUG-002`, `BUG-003`) | — |

---

## 2. NHẬT KÝ CHI TIẾT TỪNG KỊCH BẢN (DETAILED EXECUTION STEPS & TELEMETRY)

### Item 01: `TC-BB-031D-D01` — Đăng nhập thiết bị mới tải sạch dữ liệu đám mây
* **Mục tiêu:** Kiểm tra Device B sau khi đăng nhập mới có tự động kéo toàn bộ ghi chú từ Firebase Firestore về SQLite local hay không.
* **Các bước:**
  1. Kiểm tra trạng thái Device A đang có các ghi chú trên đám mây.
  2. Khởi động ứng dụng trên Device B mới đăng nhập tài khoản `student_qa@gmail.com`.
  3. Kiểm tra danh sách hiển thị trên HomeScreen của Device B.
* **Kết quả quan sát:** Toàn bộ ghi chú trên Cloud được tải về đầy đủ trên Device B, phân vùng ghim và khóa hiển thị đúng biểu tượng bảo vệ.
* **Đánh giá:** **PASS**
* **Evidence:** `10_tc_bb_031d_d01_dev_a_cloud_synced.png`, `10_tc_bb_031d_d01_dev_b_fresh_login_synced.png`.

---

### Item 02: `TC-BB-030-D01` — Tạo ghi chú offline trên Thiết bị A $\rightarrow$ Khôi phục mạng đồng bộ sang B
* **Mục tiêu:** Tạo ghi chú khi mất mạng trên Device A, sau khi có mạng tự động push lên Firebase và pull về Device B.
* **Các bước:**
  1. Tắt Wi-Fi trên Device A (`svc wifi disable`).
  2. Tạo ghi chú `FN40_Khao_nghiem_offline`, nội dung: `Noi_dung_duoc_tao_doc_lap_khi_thiet_bi_mat_ket_noi`.
  3. Bật lại Wi-Fi trên Device A (`svc wifi enable`).
  4. Mở app trên Device B, đợi đồng bộ.
* **Kết quả:**
  - Device A lưu ghi chú cục bộ vào SQLite (`is_synced=0`).
  - Sau khi bật Wi-Fi, ghi chú được đẩy lên Firestore (`is_synced=1`).
  - Device B kéo ghi chú về và hiển thị đầy đủ trên màn hình HomeScreen.
* **Đánh giá:** **PASS**
* **Evidence:** `01_tc_bb_030_d01_dev_a_offline_created.png`, `01_tc_bb_030_d01_dev_b_before_sync.png`, `01_tc_bb_030_d01_dev_a_synced.png`, `01_tc_bb_030_d01_dev_b_synced.png`.

---

### Item 03: `TC-BB-030B-D01` — Chỉnh sửa ghi chú offline trên Thiết bị A $\rightarrow$ Khôi phục mạng đồng bộ sang B
* **Mục tiêu:** Sửa ghi chú có sẵn khi mất mạng trên A, sau khi có mạng đồng bộ nội dung mới sang B.
* **Các bước:**
  1. Chuẩn bị ghi chú `FN40_Hop_ky_thuat` (nội dung gốc: `Phien_ban_goc`) có mặt trên cả 2 máy.
  2. Device A tắt Wi-Fi, sửa nội dung thành `Phien_ban_goc_Cap_nhat_ngoai_tuyen_thanh_cong`.
  3. Device A bật lại Wi-Fi. Đợi đồng bộ hai chiều.
* **Kết quả:** Device B tự động cập nhật nội dung mới sửa ngoại tuyến của Device A.
* **Đánh giá:** **PASS**
* **Evidence:** `02_tc_bb_030b_d01_dev_a_initial.png`, `02_tc_bb_030b_d01_dev_b_initial.png`, `02_tc_bb_030b_d01_dev_a_offline_edited.png`, `02_tc_bb_030b_d01_dev_a_synced.png`, `02_tc_bb_030b_d01_dev_b_synced.png`.

---

### Item 04: `TC-BB-030C-D01` — Xóa vĩnh viễn ghi chú offline trên Thiết bị A $\rightarrow$ Khôi phục mạng
* **Mục tiêu:** Xóa ghi chú vĩnh viễn khi mất mạng trên A, kiểm tra hàng đợi xóa có xóa ghi chú trên B sau khi có mạng lại hay không.
* **Các bước:**
  1. Tạo ghi chú `FN40_Ghi_chu_tam_xoa` (id: `7428f831...`) đồng bộ trên cả 2 máy.
  2. Device A tắt Wi-Fi. Chuyển ghi chú vào Thùng rác và chọn "Xóa vĩnh viễn".
  3. Ghi chú bị xóa sạch khỏi SQLite trên Device A.
  4. Device A bật lại Wi-Fi.
  5. Kiểm tra trạng thái trên Firebase Cloud và Device B.
* **Kết quả thực tế (DEFECT PHÁT HIỆN):**
  - Ghi chú biến mất khỏi Firebase Firestore Cloud.
  - Tuy nhiên trên Device B, ghi chú `7428f831...` **vẫn còn nguyên** trong danh sách HomeScreen và trong database local `dev_b.db` (`status=normal, is_synced=1`).
  - **Nguyên nhân gốc:** Ứng dụng không sử dụng cơ chế Tombstone cho thao tác xóa. Khi Device B pull danh sách, nó chỉ nạp các document đang có trên Firestore chứ không so sánh đối chiếu để dọn dẹp các bản ghi local đã bị xóa trên máy chủ.
* **Đánh giá:** **FAIL (BUG-002: Critical)**
* **Evidence:** `03_tc_bb_030c_d01_*.png`, `tools/dev_a.db` vs `tools/dev_b.db`.

#### Diễn biến thực tế sau khi phát hiện lỗi đầu tiên (`TC-BB-030C-D01`):
* **Lý do tiếp tục thực thi các ca tiếp theo:** Sau khi ghi nhận lỗi xóa offline không lan truyền sang Device B tại `TC-BB-030C`, tiến trình kiểm thử tiếp tục thực hiện các kịch bản còn lại vì mỗi ca kiểm thử sau đó (`TC-BB-030D`, `TC-BB-030E`, `TC-BB-030F`, `TC-BB-031`, `TC-BB-031B`, `TC-BB-031C`) đều được thiết kế để thao tác trên các bản ghi ghi chú hoàn toàn mới, độc lập riêng biệt (`FN40_Tai_lieu_tham_khao`, `FN40_Bao_cao_tai_chinh`, `FN40_Nhiem_vu_dot_xuat`, `FN41_LWW_Case1`, `FN41_LWW_Case2`, `FN41_Conflict_Z`).
* **Đánh giá ảnh hưởng dữ liệu:** Bản ghi tồn đọng `7428f831...` (`FN40_Ghi_chu_tam_xoa`) trên Device B chỉ là một bản ghi đơn lẻ trong cơ sở dữ liệu local và không có bất kỳ liên kết khóa ngoại (foreign key) hay phụ thuộc dữ liệu nào với các ghi chú được tạo ở các ca sau. Do đó, dữ liệu và kết quả của các ca kiểm thử tiếp theo hoàn toàn độc lập, không bị ảnh hưởng hay sai lệch bởi sự cố của `TC-BB-030C`.

---

### Item 05: `TC-BB-030D-D01` — Ghim ghi chú offline trên Thiết bị A $\rightarrow$ Khôi phục mạng
* **Mục tiêu:** Ghim ghi chú khi offline trên A, đồng bộ vị trí ghim sang B sau khi có mạng.
* **Các bước:**
  1. Ghi chú `FN40_Tai_lieu_tham_khao` ở trạng thái bình thường trên cả 2 máy.
  2. Device A tắt Wi-Fi, mở ghi chú và chạm icon Ghim trên AppBar.
  3. Ghi chú chuyển vào khu vực "Được ghim" trên HomeScreen của A.
  4. Device A bật lại Wi-Fi.
* **Kết quả:** Device B tự động chuyển ghi chú lên khu vực "ĐƯỢC GHIM" trên đầu HomeScreen. SQLite cả 2 máy: `status=pinned`.
* **Đánh giá:** **PASS**
* **Evidence:** `04_tc_bb_030d_d01_dev_a_initial.png`, `04_tc_bb_030d_d01_dev_a_offline_pinned.png`, `04_tc_bb_030d_d01_dev_a_synced.png`, `04_tc_bb_030d_d01_dev_b_synced.png`.

---

### Item 06: `TC-BB-030E-D01` — Khóa ghi chú sinh trắc học offline trên Thiết bị A $\rightarrow$ Khôi phục mạng
* **Mục tiêu:** Khóa ghi chú bằng vân tay khi offline trên A, đồng bộ cờ khóa sang B.
* **Các bước:**
  1. Ghi chú `FN40_Bao_cao_tai_chinh` trên cả 2 máy.
  2. Device A tắt Wi-Fi, chọn icon Khóa, quét vân tay sinh trắc học thành công.
  3. Thẻ ghi chú trên A chuyển sang giao diện khóa `🔒 Ghi chú đã khóa`.
  4. Device A bật lại Wi-Fi.
* **Kết quả:** Thẻ ghi chú trên Device B lập tức đổi sang `🔒 Ghi chú đã khóa - Nội dung đã được bảo vệ`, yêu cầu sinh trắc học mới mở được. SQLite cả 2 máy: `is_locked=1`.
* **Đánh giá:** **PASS**
* **Evidence:** `05_tc_bb_030e_d01_dev_a_offline_locked.png`, `05_tc_bb_030e_d01_dev_a_synced.png`, `05_tc_bb_030e_d01_dev_b_synced.png`.

---

### Item 07: `TC-BB-030F-D01` — Kéo để làm mới (Pull-to-refresh) trên Thiết bị B
* **Mục tiêu:** Kiểm tra cử chỉ vuốt kéo xuống tại HomeScreen của Device B có kích hoạt nạp đồng bộ dữ liệu mới không.
* **Các bước:**
  1. Device A online tạo ghi chú mới `FN40_Nhiem_vu_dot_xuat`.
  2. Trên Device B, thực hiện thao tác vuốt kéo xuống từ đỉnh danh sách (swipe down).
* **Kết quả thực tế (DEFECT PHÁT HIỆN):**
  - Màn hình HomeScreen không hiển thị vòng tròn xoay tiến trình làm mới (RefreshIndicator).
  - Không có phản hồi kích hoạt kéo dữ liệu từ máy chủ. Ghi chú mới không xuất hiện qua thao tác kéo làm mới.
* **Đánh giá:** **FAIL (BUG-003: Medium)**
* **Evidence:** `06_tc_bb_030f_d01_dev_a_created.png`, `06_tc_bb_030f_d01_dev_b_before_pull.png`, `06_tc_bb_030f_d01_dev_b_after_pull.png`.

---

### Item 08: `TC-BB-031-D01` — Xung đột LWW: Thiết bị B online sửa sau ($t_B > t_A$) $\rightarrow$ Giữ bản B
* **Mục tiêu:** Device A sửa offline lúc $t_A$, Device B sửa online lúc $t_B$ ($t_B > t_A$). Sau khi A có mạng, cả 2 máy phải lưu giữ bản B.
* **Các bước:**
  1. Chuẩn bị ghi chú `FN41_LWW_Case1` (nội dung gốc: `Ban_goc_2100`).
  2. Device A tắt Wi-Fi lúc $t_A$ (23:18:03), sửa thành `Ban_goc_2100_Ban__A_offline_sua_truoc_tA`.
  3. Device B online lúc $t_B$ (23:18:48, $t_B > t_A$), sửa thành `Ban_goc_2100_Ban__B_online_sau_cung_tBB_sua_online_tB`.
  4. Device A bật lại Wi-Fi lúc 23:19.
* **Kết quả:** Bản của Device B thắng (LWW), cả Device A và Device B đều hiển thị bản của B. SQLite `updated_at=1791649201692` trên cả 2 máy.
* **Đánh giá:** **PASS**
* **Evidence:** `07_tc_bb_031_d01_dev_a_offline_edited.png`, `07_tc_bb_031_d01_dev_b_online_edited.png`, `07_tc_bb_031_d01_dev_a_synced.png`, `07_tc_bb_031_d01_dev_b_synced.png`.

---

### Item 09: `TC-BB-031B-D01` — Xung đột LWW: Thiết bị A offline sửa sau ($t_A > t_B$) $\rightarrow$ Bản A ghi đè bản B
* **Mục tiêu:** Device B sửa online lúc $t_B$, sau đó Device A sửa offline lúc $t_A$ ($t_A > t_B$). Sau khi A có mạng, bản A phải ghi đè bản B.
* **Các bước:**
  1. Chuẩn bị ghi chú `FN41_LWW_Case2` (nội dung gốc: `Ban_goc_2100`).
  2. Device B online lúc $t_B$ (23:30:46), sửa thành `Ban_goc_2100_B_online_sua_truoc_tB`.
  3. Device A tắt Wi-Fi lúc $t_A$ (23:31:37, $t_A > t_B$), sửa thành `Ban_goc_2100_A_offline_sau_cung_tA`.
  4. Device A bật lại Wi-Fi. Đợi đồng bộ.
* **Kết quả:** Bản của Device A thắng (LWW), sau khi kết nối mạng, bản A đẩy lên Cloud và đồng bộ ngược về Device B. Cả 2 máy hiển thị bản A. SQLite `updated_at=1791649937854` trên cả 2 máy.
* **Đánh giá:** **PASS**
* **Evidence:** `08_tc_bb_031b_d01_dev_a_offline_edited.png`, `08_tc_bb_031b_d01_dev_b_online_edited.png`, `08_tc_bb_031b_d01_dev_a_synced.png`, `08_tc_bb_031b_d01_dev_b_synced.png`.

---

### Item 10: `TC-BB-031C-D01` — Xung đột giữa Sửa offline trên A ($t_A$) vs Chuyển vào Thùng rác trên B ($t_B$)
* **Mục tiêu:** Kiểm tra hành vi hệ thống khi Device B chuyển ghi chú vào Thùng rác lúc $t_B$, nhưng Device A sửa offline nội dung lúc $t_A$ với $t_A > t_B$.
* **Các bước:**
  1. Chuẩn bị ghi chú `FN41_Conflict_Z` (id: `ba01b529...`) trên cả 2 máy.
  2. Device B online lúc $t_B$, chuyển ghi chú vào Thùng rác (`status=trash`).
  3. Device A tắt Wi-Fi, sửa nội dung thành `Ban_goc_2100_Ban__A_sua_sau_cung_tAA_cap_nhat_khan_cap_tA` lúc $t_A$ ($t_A > t_B$).
  4. Device A bật lại Wi-Fi, đồng bộ lên Cloud và kéo về Device B.
* **Kết quả thực tế (As-built Actual Behavior):**
  - Do $t_A = 1791650780781 > t_B$, quy tắc LWW ghi đè toàn bộ document dựa trên timestamp mới nhất.
  - Record của Device A mang `status: 'normal'` và nội dung mới đã ghi đè lên record mang `status: 'trash'` của Device B.
  - Hệ quả: Ghi chú tự động được "hồi sinh" (resurrected) từ Thùng rác trở lại HomeScreen trên cả Device A và Device B mang nội dung sửa mới nhất.
* **Đánh giá & Kết luận:**
  - Tài liệu SRS hiện tại **chưa có đặc tả nghiệp vụ** cho bài toán xung đột giữa "Chỉnh sửa sau" vs "Xóa/Thùng rác trước" (liệu nên hồi sinh ghi chú, hay vẫn giữ trong thùng rác nhưng cập nhật nội dung, hay tạo thông báo xung đột).
  - Tuân thủ quy định kiểm thử: Ghi nhận trạng thái là **CHƯA ĐỦ CĂN CỨ KẾT LUẬN** (Inconclusive) và chuyển yêu cầu làm rõ đặc tả nghiệp vụ cho Product Owner / Business Analyst.
* **Evidence:** `09_tc_bb_031c_d01_*.png`, `drawer_dev_a.png`, `drawer_dev_b.png`, `tools/query_fn41.py`.

---

## 3. ĐỐI CHIẾU DỮ LIỆU SQLITE TOÀN DIỆN (DATABASE VERIFICATION SNAPSHOT)

Sau khi hoàn tất toàn bộ 10 kịch bản, trích xuất dữ liệu SQLite `smart_note.db` từ cả hai thiết bị để đối chiếu:

```text
=== DEV_A (Samsung S21 FE) ===
  id=ba01b529 | title=FN41_Conflict_Z | status=normal | is_synced=1 | updated_at=1791650780781
    content=[{"insert":"Ban_goc_2100_Ban__A_sua_sau_cung_tAA_cap_nhat_khan_cap_tA\n"}]
  id=c77d6516 | title=FN41_LWW_Case2  | status=normal | is_synced=1 | updated_at=1791649937854
    content=[{"insert":"Ban_goc_2100_A_offline_sau_cung_tA\n"}]
  id=54640d09 | title=FN41_LWW_Case1  | status=normal | is_synced=1 | updated_at=1791649201692
    content=[{"insert":"Ban_goc_2100_Ban__B_online_sau_cung_tBB_sua_online_tB\n"}]
  id=64a7ed92 | title=FN40_Tai_lieu_tham_khao | status=pinned | is_synced=1 | updated_at=1791650859805
  id=a7f68643 | title=FN40_Bao_cao_tai_chinh   | status=normal | is_locked=1 | is_synced=1
  id=90d7acff | title=FN40_Khao_nghiem_offline | status=normal | is_synced=1

=== DEV_B (Samsung S24 FE) ===
  id=ba01b529 | title=FN41_Conflict_Z | status=normal | is_synced=1 | updated_at=1791650780781
    content=[{"insert":"Ban_goc_2100_Ban__A_sua_sau_cung_tAA_cap_nhat_khan_cap_tA\n"}]
  id=c77d6516 | title=FN41_LWW_Case2  | status=normal | is_synced=1 | updated_at=1791649937854
    content=[{"insert":"Ban_goc_2100_A_offline_sau_cung_tA\n"}]
  id=54640d09 | title=FN41_LWW_Case1  | status=normal | is_synced=1 | updated_at=1791649201692
    content=[{"insert":"Ban_goc_2100_Ban__B_online_sau_cung_tBB_sua_online_tB\n"}]
  id=64a7ed92 | title=FN40_Tai_lieu_tham_khao | status=pinned | is_synced=1 | updated_at=1791650859805
  id=a7f68643 | title=FN40_Bao_cao_tai_chinh   | status=normal | is_locked=1 | is_synced=1
  id=90d7acff | title=FN40_Khao_nghiem_offline | status=normal | is_synced=1
  id=7428f831 | title=FN40_Ghi_chu_tam_xoa    | status=normal | is_synced=1 [BUG-002: BẢN GHI MA TỒN ĐỌNG TRÊN B]
```

---

## 4. KẾT LUẬN & KHUYẾN NGHỊ CHO DỰ ÁN

1. **Về cơ chế LWW (FN-41):** Hoạt động chính xác theo quy tắc Last-Write-Wins trên từng field và document khi cả hai máy cùng chỉnh sửa nội dung ($t_B > t_A$ giữ bản B; $t_A > t_B$ giữ bản A).
2. **Về đồng bộ ngoại tuyến (FN-40):** Đồng bộ tạo mới, sửa nội dung, ghim và khóa sinh trắc học hoạt động mượt mà và tự động đẩy/kéo khi khôi phục kết nối mạng.
3. **Cần ưu tiên xử lý cấp bách 2 lỗi:**
   - **`BUG-002` (Critical):** Bổ sung cơ chế Tombstone hoặc dọn dẹp các ghi chú local không còn tồn tại trên server trong chu trình `syncPull()`.
   - **`BUG-003` (Medium):** Bổ sung widget `RefreshIndicator` vào màn hình `home_screen.dart`.
4. **Về kịch bản `TC-BB-031C`:** Cần Product Owner / Business Analyst cập nhật tài liệu SRS để xác định rõ quy tắc ưu tiên giữa sửa sau vs xóa trước.
