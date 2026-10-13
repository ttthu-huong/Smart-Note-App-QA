# RUN LOG: XÁC MINH ĐỘC LẬP TC-BB-CHK-05 (XÓA MỤC CHECKLIST)

**Thời gian thực hiện:** 00:35 — 00:39 ngày 11/10/2026  
**Thiết bị thực thi:** Samsung Galaxy S21 FE 5G (Serial: `R5CW82ECF6M`)  
**Môi trường:** Android 14 (API 34, One UI 6.1) | Smart Note App build `v1.0.0+1`  
**Tài khoản đăng nhập:** `student_qa@gmail.com`  
**Mục tiêu ca kiểm thử:** Xác minh riêng `TC-BB-CHK-05` — Xóa mục checklist bằng nút xóa (`Icons.close`). Kiểm tra các mục còn lại giữ nguyên nội dung, thứ tự tương đối và trạng thái checkbox, kể cả sau khi lưu và mở lại.

---

## 1. KẾ HOẠCH & TIỀN ĐIỀU KIỆN (TEST PLAN)

1. **Chuẩn bị dữ liệu ghi chú mới:**
   - Tạo ghi chú mới qua UI với tiêu đề: `"FN15_CHK05_Verify_Delete_Item"`.
   - Bật chế độ Checklist, nhập 3 mục thử nghiệm phân biệt:
     - Mục 1 (`A`): `DELETE_A_111` — Trạng thái: Unchecked ($\square$, `checked = false`).
     - Mục 2 (`B`): `DELETE_B_222` — Trạng thái: Checked ($\checkmark$, `checked = true`).
     - Mục 3 (`C`): `DELETE_C_333` — Trạng thái: Checked ($\checkmark$, `checked = true`).
2. **Phương thức xóa:**
   - Sử dụng nút xóa UI: Chạm trực tiếp vào icon Close (`Icons.close`, bounds `[980, 827][1070, 917]`) bên phải Mục B.
   - Không sử dụng phím Backspace trên bàn phím (phân biệt rõ ràng phương thức kiểm thử theo yêu cầu).
3. **Tiêu chí đánh giá (Pass Criteria):**
   - Trước khi xóa: Cả 3 mục A-B-C hiển thị đúng nội dung và checkbox như thiết kế.
   - Sau khi xóa: Mục B biến mất; chỉ còn lại Mục A và Mục C.
   - Mục A: Giữ nguyên `DELETE_A_111`, unchecked.
   - Mục C: Giữ nguyên `DELETE_C_333`, checked.
   - Thứ tự hiển thị: A $\rightarrow$ C, không nối chuỗi văn bản, không mất ký tự.
   - Sau khi lưu, thoát về Home và mở lại: Các giá trị trên được giữ nguyên vẹn 100%.
   - Snapshot SQLite: Bản ghi của note chỉ chứa 2 item A và C với đúng trạng thái.

---

## 2. DIỄN BIẾN THỰC THI THỰC TẾ

### Bước 1: Tạo ghi chú và chuẩn bị 3 mục thử nghiệm
- Vào Editor qua nút Tạo mới (+).
- Nhập tiêu đề: `FN15_CHK05_Verify_Delete_Item`.
- Chuyển sang chế độ Checklist, nhập lần lượt 3 mục: `DELETE_A_111`, `DELETE_B_222`, `DELETE_C_333`.
- Tick chọn checkbox của Mục B và Mục C. Giữ Mục A unchecked.
- Quan sát UI dump và chụp ảnh minh chứng:
  - Item 0: EditText `DELETE_A_111`, CheckBox `checked="false"`.
  - Item 1: EditText `DELETE_B_222`, CheckBox `checked="true"`.
  - Item 2: EditText `DELETE_C_333`, CheckBox `checked="true"`.
  - **Minh chứng:** [`chk05_01_before_delete.png`](chk05_01_before_delete.png).

### Bước 2: Thực hiện xóa riêng Mục B bằng nút xóa (Close button)
- Chạm vào tọa độ tâm nút xóa của Mục B: `(1025, 872)` (tương ứng icon Close tại `[980, 827][1070, 917]`).
- Quan sát phản hồi UI:
  - Mục `DELETE_B_222` biến mất ngay lập tức khỏi danh sách.
  - Danh sách chỉ còn lại 2 mục:
    - Vị trí 1: `DELETE_A_111`, CheckBox `checked="false"`.
    - Vị trí 2: `DELETE_C_333`, CheckBox `checked="true"`.
  - Thứ tự A $\rightarrow$ C chính xác, không có ký tự lạ hay chuỗi bị ghép.
  - **Minh chứng:** [`chk05_02_after_delete.png`](chk05_02_after_delete.png).

### Bước 3: Lưu, thoát về Home và Mở lại kiểm tra tính bền vững
- Chạm nút Back trên AppBar (`[74, 173]`) để kích hoạt cơ chế tự động lưu và quay về HomeScreen.
- **Tại màn hình Trang chủ (HomeScreen):**
  - Thẻ ghi chú đầu tiên hiển thị tiêu đề và xem trước:
    `FN15_CHK05_Verify_Delete_Item`
    `DELETE_A_111`
    `DELETE_C_333`
  - Hoàn toàn không còn xuất hiện `DELETE_B_222`.
  - **Minh chứng:** [`chk05_03_home_preview.png`](chk05_03_home_preview.png).
- **Mở lại ghi chú vào Editor:**
  - Chạm vào thẻ ghi chú trên Trang chủ (`[32, 267][1049, 574]`).
  - Giao diện Editor hiển thị:
    - Tiêu đề: `FN15_CHK05_Verify_Delete_Item`.
    - Mục 1: `DELETE_A_111`, CheckBox `checked="false"`.
    - Mục 2: `DELETE_C_333`, CheckBox `checked="true"` (hiển thị gạch ngang chuẩn).
    - Thứ tự và nội dung giữ nguyên vẹn 100%.
  - **Minh chứng:** [`chk05_04_reopened_editor.png`](chk05_04_reopened_editor.png).

### Bước 4: Đối chiếu cơ sở dữ liệu SQLite local (Chỉ đọc đúng Note ID)
- Trích xuất cơ sở dữ liệu SQLite cục bộ `smart_note.db` từ ứng dụng: [`smart_note_chk05.db`](smart_note_chk05.db).
- Truy vấn bản ghi duy nhất có tiêu đề `FN15_CHK05_Verify_Delete_Item`:
  - **Note ID:** `dfff866b-aced-4c1c-a482-8b67a307703c`
  - **Tiêu đề:** `FN15_CHK05_Verify_Delete_Item`
  - **Updated at:** `1791653795271`
  - **Cờ đồng bộ cục bộ:** `is_synced = 1` *(Ghi chú: Giá trị này đại diện cho cờ nội bộ trong database cục bộ, không dùng để khẳng định đồng bộ đám mây thành công khi chưa đối chiếu server)*
  - **Dữ liệu Content JSON:**
    ```json
    {
      "type": "checklist",
      "items": [
        {
          "id": "be27cc5f-dca4-4590-ad3a-cfa8ef044919",
          "text": "DELETE_A_111",
          "checked": false
        },
        {
          "id": "9fef56c3-9036-4169-97fb-9e74081bc2fc",
          "text": "DELETE_C_333",
          "checked": true
        }
      ]
    }
    ```
  - **Kết quả đối chiếu:** Số lượng mục trong DB là đúng 2. Mục B đã bị loại bỏ hoàn toàn khỏi cấu trúc dữ liệu JSON. Mục A và C bảo toàn chính xác ID, text và checked status.

---

## 3. KẾT LUẬN & ĐÁNH GIÁ CHẤT LƯỢNG

* **Kết quả lượt xác minh mới (Run 2 độc lập):** **PASS**
* **Lịch sử lượt cũ:** Ghi nhận Lượt 1 là *Chưa đủ căn cứ xác minh* (do thao tác nhập liệu của runner làm chuỗi Mục 1 bị lặp nối). Kết quả lượt mới xác minh độc lập bằng thao tác chuẩn xác, bằng chứng rõ ràng và nhất quán giữa UI và Database.
* **Danh mục bằng chứng kèm theo:**
  - `chk05_01_before_delete.png`
  - `chk05_02_after_delete.png`
  - `chk05_03_home_preview.png`
  - `chk05_04_reopened_editor.png`
  - `smart_note_chk05.db`
  - `inspect_chk05.py`
