# RUN LOG — XÁC MINH ĐỘC LẬP TC-BB-CHK-06 (LƯU VÀ MỞ LẠI CHECKLIST)
* **Thời gian thực hiện:** 00:24 — 00:29 ngày 11/10/2026
* **Môi trường thực thi:** Samsung Galaxy S21 FE 5G (Serial: `R5CW82ECF6M`, USB ADB, Android 14 API 34)
* **Bản build:** Smart Note App `v1.0.0+1`
* **Tài khoản:** `student_qa@gmail.com`
* **Mục tiêu:** Kiểm tra tính toàn vẹn của nội dung, thứ tự và trạng thái checkbox khi lưu, thoát và mở lại ghi chú checklist trên UI.

---

## 1. DỮ LIỆU & THAO TÁC THỬ NGHIỆM ĐỘC LẬP
* **Ghi chú thử nghiệm:** Tạo mới hoàn toàn qua UI `FN15_CHK06_Verify_Save_Reopen` (Note ID: `882ce48a-219d-45b0-bfbd-840bd294debf`), bảo toàn ghi chú và bằng chứng của lượt cũ.
* **3 mục thử nghiệm:**
  - Mục 1: `MUC_A_111`
  - Mục 2: `MUC_B_222`
  - Mục 3: `MUC_C_333`
* **Chuỗi thao tác có kiểm soát:**
  1. Tạo note, nhập tiêu đề, chuyển sang chế độ Checklist.
  2. Nhập chính xác 3 mục theo thứ tự A, B, C.
  3. Tick Mục A $\rightarrow$ Checkbox A đổi thành `checked = true`.
  4. Bỏ tick Mục A $\rightarrow$ Checkbox A đổi về `checked = false`.
  5. Tick Mục C $\rightarrow$ Checkbox C đổi thành `checked = true`.
  6. Kiểm tra trạng thái ngay trước khi lưu:
     - `MUC_A_111`: `checked = false`
     - `MUC_B_222`: `checked = false`
     - `MUC_C_333`: `checked = true`
     - Thứ tự: A - B - C, nội dung đúng nguyên văn.
  7. Chụp ảnh minh chứng trước khi lưu: `chk06_01_before_save.png`.
  8. Nhấn nút Back trên AppBar (tọa độ xác định `74 173`, không có thao tác phụ) để lưu và quay về HomeScreen.
  9. Quan sát thẻ preview trên HomeScreen: `chk06_02_home_preview.png`.
  10. Chạm mở lại ghi chú vào Editor: `chk06_03_reopened_editor.png`.

---

## 2. KẾT QUẢ QUAN SÁT & ĐỐI CHIẾU THỰC TẾ

### 2.1. Quan sát giao diện (UI Verification)
- **Trước khi lưu:** Đầy đủ 3 mục A, B, C; Mục A và B chưa tick, Mục C đã tick.
- **Tại HomeScreen:** Thẻ ghi chú hiển thị tiêu đề `FN15_CHK06_Verify_Save_Reopen`, danh sách 3 mục preview đúng thứ tự `MUC_A_111`, `MUC_B_222`, `MUC_C_333`.
- **Mở lại trong Editor:**
  - Mục 1: Checkbox unchecked ($\square$), text `MUC_A_111`.
  - Mục 2: Checkbox unchecked ($\square$), text `MUC_B_222`.
  - Mục 3: Checkbox checked ($\checkmark$, có gạch ngang), text `MUC_C_333`.
  - Thứ tự và nội dung các mục giữ nguyên 100%.

### 2.2. Đối chiếu cơ sở dữ liệu SQLite local
- **Truy vấn đúng Note ID:** `882ce48a-219d-45b0-bfbd-840bd294debf`
- **Cấu trúc JSON lưu trữ:**
  ```json
  {
    "type": "checklist",
    "items": [
      {"id": "0735c0b1-fef7-4c76-9127-8c2346e3b296", "text": "MUC_A_111", "checked": false},
      {"id": "20320133-42b3-49a5-a591-bb0b85b98150", "text": "MUC_B_222", "checked": false},
      {"id": "cb8776bb-8ded-4b78-9315-d99b9597b9d4", "text": "MUC_C_333", "checked": true}
    ]
  }
  ```
- **Cờ đồng bộ cục bộ:** `is_synced = 1`. *Lưu ý quy tắc kiểm thử: Giá trị này chỉ đại diện cho cờ đồng bộ cục bộ bằng 1, không dùng để kết luận đồng bộ đám mây thành công khi chưa đọc đối chiếu từ Cloud Firestore hoặc thiết bị thứ hai.*

---

## 3. KẾT LUẬN LƯỢT XÁC MINH
* **Kết quả lượt xác minh mới (Run 2 độc lập):** **PASS**
* **Lịch sử lượt cũ:** Giữ nguyên trạng thái lượt cũ là *chưa đủ căn cứ xác minh* do thao tác tap ngoài kế hoạch và dữ liệu nối chuỗi.
* **Minh chứng lưu trữ:**
  - `chk06_01_before_save.png`
  - `chk06_02_home_preview.png`
  - `chk06_03_reopened_editor.png`
  - `chk06_verify.db`
