import sys

with open('../../test_cases/black_box/black_box_test_cases.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('| **TC-BB-026E** | FN-23 |'):
        new_lines.append('| **TC-BB-026E** | FN-23 | Tìm kiếm Ghi chú | Xóa nhanh toàn bộ từ khóa tìm kiếm bằng nút X trên search bar | Đang ở màn hình Tìm kiếm và đã nhập từ khóa `"ghi chú test"`. | 1. Nhập từ khóa để hiển thị kết quả.<br>2. Chạm vào biểu tượng \'X\' ở bên phải thanh tìm kiếm.<br>3. Quan sát màn hình. | Thao tác: Chạm nút \'X\' trên search bar | Ô tìm kiếm được xóa trống; kết quả tìm kiếm đóng; màn hình trở về trạng thái gợi ý ban đầu. | Tiện ích giao diện / Code-inferred (As-built) | Medium |\n')
    elif line.startswith('| **TC-BB-027B** | FN-23 |'):
        new_lines.append('| **TC-BB-027B** | FN-23 | Tìm kiếm Ghi chú | Xác minh lọc ghi chú theo Loại đa phương tiện bằng Chip (Hình ảnh, Âm thanh, URL) | Có ghi chú chứa hình ảnh, ghi chú chứa âm thanh và ghi chú chứa liên kết URL. | 1. Mở màn hình Tìm kiếm.<br>2. Bấm vào icon loại media tương ứng (Hình ảnh / Âm thanh / Liên kết).<br>3. Quan sát thanh tìm kiếm và kết quả. | Thao tác: Bấm vào "Hình ảnh" (D01), "Âm thanh" (D02), "Liên kết" (D03) | Một viên Chip lọc tương ứng xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú có chứa loại đa phương tiện tương ứng đã chọn. | Bộ lọc dữ liệu / Code-inferred (As-built) | High |\n')
    elif line.startswith('| **TC-BB-027D** | FN-23 |'):
        new_lines.append('| **TC-BB-027D** | FN-23 | Tìm kiếm Ghi chú | Xác minh lọc ghi chú theo Trạng thái bằng Chip (Được ghim / Lưu trữ) | Có ít nhất 1 ghi chú đã ghim (`isPinned == true`) và 1 ghi chú đã đưa vào mục Lưu trữ (`isArchived == true`). | 1. Mở màn hình Tìm kiếm.<br>2. Bấm chọn mục "Được ghim" (D01) hoặc "Lưu trữ" (D02).<br>3. Quan sát kết quả. | Thao tác: Bấm vào "Được ghim" (D01) hoặc "Lưu trữ" (D02) | Viên Chip tương ứng xuất hiện trên thanh tìm kiếm; danh sách lọc ra chính xác các ghi chú có trạng thái tương ứng được chọn. | Bộ lọc dữ liệu / Code-inferred (As-built) | High |\n')
    elif line.startswith('| **TC-BB-026E** | **D01** |'):
        new_lines.append('| **TC-BB-026E** | **D01** | Đang có từ khóa tìm kiếm $\\rightarrow$ Bấm nút \'X\' trên search bar | Xóa nhanh toàn bộ từ khóa tìm kiếm bằng nút X trên search bar. | Ô tìm kiếm được xóa trống; kết quả tìm kiếm đóng; màn hình trở về trạng thái gợi ý ban đầu. |\n')
    elif line.startswith('| **TC-BB-027B** | **D01** |'):
        new_lines.append('| **TC-BB-027B** | **D01** | Bấm chọn mục "Hình ảnh" trong Loại phương tiện | Kiểm tra lọc ghi chú có chứa Hình ảnh bằng Chip lọc. | Viên Chip `[Hình ảnh]` xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú có chứa hình ảnh. |\n')
        new_lines.append('| **TC-BB-027B** | **D02** | Bấm chọn mục "Âm thanh" trong Loại phương tiện | Kiểm tra lọc ghi chú có chứa Âm thanh (Voice) bằng Chip lọc. | Viên Chip `[Âm thanh]` xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú có chứa bản ghi âm. |\n')
        new_lines.append('| **TC-BB-027B** | **D03** | Bấm chọn mục "Liên kết" trong Loại phương tiện | Kiểm tra lọc ghi chú có chứa Liên kết URL bằng Chip lọc. | Viên Chip `[Liên kết]` xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú có chứa đường dẫn URL. |\n')
    elif line.startswith('| **TC-BB-027D** | **D01** |'):
        new_lines.append('| **TC-BB-027D** | **D01** | Bấm chọn mục "Được ghim" trong Trạng thái | Kiểm tra lọc ghi chú có trạng thái Được ghim bằng Chip lọc. | Viên Chip `[Được ghim]` xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú đang được ghim. |\n')
        new_lines.append('| **TC-BB-027D** | **D02** | Bấm chọn mục "Lưu trữ" trong Trạng thái | Kiểm tra lọc ghi chú có trạng thái Đã lưu trữ bằng Chip lọc. | Viên Chip `[Lưu trữ]` xuất hiện trên thanh tìm kiếm; danh sách kết quả lọc ra các ghi chú nằm trong kho lưu trữ. |\n')
    elif '**FN-23 BLACK-BOX DESIGN = SẴN SÀNG THỰC THI**' in line:
        new_lines.append('**FN-23 BLACK-BOX DESIGN = CHỐT**  \n')
    elif line.strip() == '**16 TC / 17 Execution Items.**':
        new_lines.append('**16 TC / 21 Execution Items.**  \n')
    else:
        new_lines.append(line)

with open('../../test_cases/black_box/black_box_test_cases.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Updated black_box_test_cases.md successfully!')
