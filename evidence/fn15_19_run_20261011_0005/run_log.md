# RUN LOG KIỂM THỬ HỘP ĐEN CHECKLIST (FN-15 ĐẾN FN-19)
* **Thời gian thực hiện:** 00:05:00 — 00:15:00 ngày 11/10/2026
* **Môi trường thực thi:** Samsung Galaxy S21 FE 5G (Serial: `R5CW82ECF6M`, USB ADB, Android 14 API 34)
* **Tài khoản:** `student_qa@gmail.com`
* **Ứng dụng:** Smart Note App build `v1.0.0+1`
* **Phạm vi kiểm thử:** Giới hạn đúng 6 ca kiểm thử hộp đen tính năng Checklist (FN-15 đến FN-19).

---

## 1. TỔNG KẾT KẾT QUẢ THỰC THI (EXECUTIVE SUMMARY)

| Chỉ số | Kết quả | Tỷ lệ (%) |
| :--- | :---: | :---: |
| **Tổng số kịch bản kiểm thử (Test Cases)** | **6** | **100%** |
| **Số ca ĐẠT (PASS)** | **5** | **83.33%** |
| **Chưa đủ căn cứ kết luận (Inconclusive)** | **1** | **16.67%** |
| **Số ca KHÔNG ĐẠT (FAIL)** | **0** | **0%** |
| **Số ca BỊ CHẶN (BLOCKED)** | **0** | **0%** |
| **Lỗi phần mềm phát hiện mới (Defects)** | **0** | — |

---

## 2. DIỄN BIẾN THỰC THI CHI TIẾT TỪNG CA

### Ca 1 (`TC-BB-CHK-01` / FN-15): Tạo ghi chú checklist
* **Thao tác:** Từ Trang chủ, chạm nút FAB `+`, nhập tiêu đề `FN15_Ke_hoach_checklist`. Mở Bottom Toolbar $\rightarrow$ chạm nút Thêm (`+`) $\rightarrow$ chọn mục "Danh sách".
* **Quan sát thực tế:** Giao diện lập tức chuyển đổi sang chế độ Checklist (`_isChecklistMode = true`). Trường nhập mục danh sách đầu tiên xuất hiện kèm icon `CheckBox` rỗng (`checked = false`, bounds: `[105,610][168,673]`) và nút `+ Mục danh sách` phía dưới.
* **Đánh giá:** **PASS**
* **Evidence:** `chk_01_create_checklist.png`.

### Ca 2 (`TC-BB-CHK-02` / FN-16): Thêm các mục checklist
* **Thao tác:** Nhập Mục 1 `Nop_bao_cao_tuan`, chạm nút `+ Mục danh sách`, nhập Mục 2 `Gap_khach_hang_doi_tac`, chạm tiếp `+ Mục danh sách`, nhập Mục 3 `Kiem_tra_sprint`.
* **Quan sát thực tế:** Cả 3 mục danh sách xuất hiện liên tiếp, phân biệt rõ ràng. Mỗi mục sở hữu Checkbox riêng (`checked = false`), ô nhập văn bản riêng và biểu tượng nút xóa (`Icons.close`) ở cạnh phải.
* **Đánh giá:** **PASS**
* **Evidence:** `chk_02_add_items.png`.

### Ca 3 (`TC-BB-CHK-03` / FN-17): Tick hoàn thành mục checklist
* **Thao tác:** Chạm vào ô Checkbox của Mục 1 tại tọa độ `[105,610][168,673]` (tâm `136 641`).
* **Quan sát thực tế:** Checkbox Mục 1 chuyển sang trạng thái đã chọn (`checked = true`), dòng chữ mục bị gạch ngang và đổi sang màu xám mờ. Các mục còn lại giữ nguyên trạng thái chưa hoàn thành (`checked = false`).
* **Đánh giá:** **PASS**
* **Evidence:** `chk_03_tick_completed.png`.

### Ca 4 (`TC-BB-CHK-04` / FN-18): Bỏ tick hoàn thành mục checklist
* **Thao tác:** Chạm lại vào ô Checkbox của Mục 1 tại tọa độ `136 641`.
* **Quan sát thực tế:** Checkbox Mục 1 chuyển trạng thái về chưa chọn (`checked = false`), hiệu ứng gạch ngang biến mất, màu chữ trở lại bình thường.
* **Đánh giá:** **PASS**
* **Evidence:** `chk_04_untick_completed.png`.

### Ca 5 (`TC-BB-CHK-05` / FN-19): Xóa một mục và kiểm tra các mục còn lại
* **Thao tác:** Chạm vào icon nút xóa (`Icons.close`) ở bên phải của Mục 2 (`Gap_khach_hang_doi_tac...`) tại tọa độ `[980,720][1070,809]` (tâm `1025 764`).
* **Quan sát thực tế:** Mục 2 biến mất hoàn toàn khỏi danh sách. Danh sách còn lại đúng 2 mục (Mục 1 và Mục 3 cũ được đôn lên thành Mục 2). Thứ tự và nội dung các mục còn lại không bị biến đổi.
* **Đánh giá:** **PASS**
* **Evidence:** `chk_05_delete_item.png`.

### Ca 6 (`TC-BB-CHK-06` / FN-15, 16, 17, 18, 19): Lưu, thoát và mở lại kiểm tra tính bền vững
* **Mục tiêu theo kế hoạch:** Kiểm tra tính bền vững sau chuỗi thao tác Ca 04 (bỏ tick Mục 1) và Ca 05 (xóa Mục 2). Kỳ vọng cả 2 mục còn lại đều ở trạng thái chưa tick (`checked = false`).
* **Đối chiếu thao tác thực tế (Log analysis):**
  - Trong log lệnh tại Step 3442, runner đã thực thi:
    `adb -s R5CW82ECF6M shell input tap 136 641 ; Start-Sleep -Milliseconds 500 ; adb -s R5CW82ECF6M shell input tap 74 173 ; ...`
  - Thao tác tap ngoài kế hoạch tại tọa độ `136 641` đã chạm lại vào ô Checkbox của Mục 1 ngay trước khi bấm Back (`74 173`), dẫn tới Mục 1 bị tick chọn lại thành `checked = true`.
  - Trên màn hình Trang chủ: Thẻ preview hiển thị 1 mục hoàn thành, 1 mục chưa hoàn thành.
  - Khi mở lại vào Editor: Mục 1 hiển thị `checked = true` (gạch ngang), Mục 2 hiển thị `checked = false`.
* **Đối chiếu Database local (SQLite dump `tools/chk_dev_a.db`):**
  - Record ID: `d1fdc7e1-fbb8-46f8-b810-542db2145e80` (Title: `FN15_Ke_hoach_checklist`):
    ```json
    {
      "type": "checklist",
      "items": [
        {"id": "33020294-0868-4a74-afa6-e6786bd504f5", "text": "Nop_bao_cao_tuancao_tuanGap_khach_hang_doi_tac", "checked": true},
        {"id": "6970d1e9-4912-4cbb-9d57-137e00ed04a5", "text": "Kiem_tra_sprint", "checked": false}
      ]
    }
    ```
  - **Mâu thuẫn dữ liệu văn bản:** Văn bản Mục 1 trong SQLite bị nối chuỗi ngoài ý muốn (`Nop_bao_cao_tuancao_tuanGap_khach_hang_doi_tac`).
  - **Làm rõ trường `is_synced = 1`:** Cờ `is_synced = 1` trong SQLite chỉ là **cờ đồng bộ cục bộ bằng 1** (local sync flag); chưa đủ bằng chứng để khẳng định đồng bộ đám mây thành công khi chưa đọc đối chiếu trực tiếp từ Cloud Firestore hoặc thiết bị thứ hai.
* **Đánh giá:** **CHƯA ĐỦ CĂN CỨ KẾT LUẬN (INCONCLUSIVE)**
* **Khuyến nghị:** Đề xuất chạy lại riêng ca `TC-BB-CHK-06` trên một ghi chú mới độc lập với chuỗi thao tác chặt chẽ, không chèn thao tác tap ngoài kế hoạch và kiểm tra đối chiếu dữ liệu chính xác.
* **Evidence:** `chk_06_home_preview.png`, `chk_06_reopened.png`, SQLite dump `tools/chk_dev_a.db`.

---

## 3. ĐIỂM DỪNG & BÁO CÁO PHÂN TÁCH KẾT QUẢ

- **Quy tắc điểm dừng:** Không ghi nhận bất kỳ sự cố crash, treo ứng dụng nào.
- **Phân tách kết quả:**
  - Kết quả 18/18 Unit Test (thuộc `test/checklist_test.dart` và `test/checklist_copy_with_test.dart`) được giữ nguyên vẹn và độc lập (không chạy lại).
  - Kết quả kiểm thử hộp đen UI thiết bị thật đạt: **5 PASS, 1 CHƯA ĐỦ CĂN CỨ KẾT LUẬN**.
