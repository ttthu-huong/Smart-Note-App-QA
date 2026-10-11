# -*- coding: utf-8 -*-
path = r'd:\Workspace\TBDD\Smart-Note-App-QA\test_cases\black_box\black_box_test_cases.md'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

# 1. Định nghĩa 16 TCs mới cho FN-23 trong Phần 1
fn23_tcs_part1 = [
    '| **TC-BB-026** | FN-23 | Tìm kiếm Ghi chú | Xác minh tìm kiếm khớp từ khóa trong Tiêu đề ghi chú | Có ghi chú mang tiêu đề `"Báo cáo tiến độ"` trên hệ thống. | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa `"Báo cáo"`. | Từ khóa: `"Báo cáo"` | Dòng thông điệp hiển thị số lượng ghi chú khớp; danh sách hiển thị đúng thẻ ghi chú có Tiêu đề chứa từ khóa `"Báo cáo"`. | Phân lớp tương đương / Requirement-based | High |',
    '| **TC-BB-026B** | FN-23 | Tìm kiếm Ghi chú | Xác minh tìm kiếm không phân biệt chữ hoa và chữ thường (Case-insensitivity) | Có ghi chú mang tiêu đề hoặc nội dung chứa `"Họp Tuần"`. | 1. Mở màn hình Tìm kiếm.<br>2. Thử nghiệm nhập từ khóa chữ thường hoặc chữ hoa. | • D01: Nhập chữ thường `"họp tuần"`<br>• D02: Nhập chữ hoa `"HỌP TUẦN"` | Cả hai trường hợp nhập chữ thường và chữ hoa đều tìm thấy và hiển thị chính xác cùng ghi chú `"Họp Tuần"`. | Độ bền nhập liệu / Code-inferred (As-built) | High |',
    '| **TC-BB-026C** | FN-23 | Tìm kiếm Ghi chú | Xác minh tìm kiếm chuỗi tiếng Việt có dấu đầy đủ và chính xác | Có ghi chú mang nội dung `"Nghiên cứu tài liệu kiểm thử phần mềm"`. | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa tiếng Việt có dấu `"kiểm thử"`. | Từ khóa: `"kiểm thử"` | Danh sách trả về đúng ghi chú có chứa đoạn văn bản `"kiểm thử"`, không bị lỗi font hay mất kết quả. | Độ chính xác chuỗi / Code-inferred (As-built) | High |',
    '| **TC-BB-026D** | FN-23 | Tìm kiếm Ghi chú | Xác minh làm nổi bật (Highlight) từ khóa tìm kiếm trên thẻ ghi chú | Có ghi chú chứa từ khóa `"Kế hoạch"`. | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa `"Kế hoạch"`.<br>3. Quan sát các thẻ ghi chú kết quả. | Từ khóa: `"Kế hoạch"` | Các đoạn chữ `"Kế hoạch"` xuất hiện trong tiêu đề hoặc nội dung xem trước của thẻ ghi chú được bôi màu nền nổi bật (highlight vàng nhạt). | Tiện ích giao diện / Code-inferred (As-built) | Medium |',
    '| **TC-BB-026E** | FN-23 | Tìm kiếm Ghi chú | Xác minh nút \'X\' (Clear) xóa nhanh toàn bộ từ khóa và bộ lọc tìm kiếm | Đang ở màn hình Tìm kiếm và đã nhập từ khóa `"ghi chú test"`. | 1. Nhập từ khóa để hiển thị kết quả.<br>2. Chạm vào biểu tượng \'X\' ở bên phải thanh tìm kiếm.<br>3. Quan sát màn hình. | Thao tác: Chạm nút \'X\' trên thanh tìm kiếm | Ô tìm kiếm bị xóa trống hoàn toàn; danh sách kết quả đóng lại và màn hình quay về hiển thị menu các bộ lọc gợi ý ban đầu. | Tiện ích giao diện / Code-inferred (As-built) | Medium |',
    '| **TC-BB-027** | FN-23 | Tìm kiếm Ghi chú | Xác minh tìm kiếm khớp từ khóa trong Nội dung văn bản ghi chú | Có ghi chú mang nội dung chứa đoạn: `"mua thêm giấy in A4"`. | 1. Mở màn hình Tìm kiếm.<br>2. Nhập từ khóa `"giấy in A4"`. | Từ khóa: `"giấy in A4"` | Danh sách kết quả hiển thị thẻ ghi chú có phần nội dung xem trước chứa đoạn văn bản `"giấy in A4"`. | Phân lớp tương đương / Requirement-based | High |',
    '| **TC-BB-027B** | FN-23 | Tìm kiếm Ghi chú | Xác minh lọc ghi chú theo Loại đa phương tiện bằng Chip (Hình ảnh, Âm thanh, URL) | Có ghi chú chứa hình ảnh, ghi chú chứa âm thanh hoặc ghi chú chứa liên kết URL. | 1. Mở màn hình Tìm kiếm.<br>2. Bấm vào icon \"Hình ảnh\" (hoặc \"Âm thanh\" / \"Liên kết\").<br>3. Quan sát thanh tìm kiếm và kết quả. | Thao tác: Bấm vào mục \"Hình ảnh\" hoặc \"Âm thanh\" hoặc \"Liên kết\" | Một viên Chip lọc tương ứng xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ hiển thị các ghi chú có chứa loại đa phương tiện đã chọn. | Bộ lọc dữ liệu / Code-inferred (As-built) | High |',
    '| **TC-BB-027C** | FN-23 | Tìm kiếm Ghi chú | Xác minh lọc ghi chú theo Nhãn dán bằng Chip (Tags Filter) | Hệ thống đã có ít nhất 1 nhãn dán (ví dụ: `"Công việc"`) được gán cho ghi chú. | 1. Mở màn hình Tìm kiếm.<br>2. Cuộn xuống phần \"Nhãn\", bấm chọn nhãn `"Công việc"`.<br>3. Quan sát kết quả. | Thao tác: Bấm vào nhãn dán trong mục \"Nhãn\" | Viên Chip mang tên nhãn xuất hiện trên thanh tìm kiếm; danh sách kết quả chỉ lọc ra các ghi chú được gắn đúng nhãn dán đó. | Bộ lọc dữ liệu / Code-inferred (As-built) | High |',
    '| **TC-BB-027D** | FN-23 | Tìm kiếm Ghi chú | Xác minh lọc ghi chú theo Trạng thái bằng Chip (Được ghim / Lưu trữ) | Có ít nhất 1 ghi chú đã ghim hoặc 1 ghi chú đã đưa vào mục Lưu trữ (`Archive`). | 1. Mở màn hình Tìm kiếm.<br>2. Bấm chọn mục \"Được ghim\" (hoặc \"Lưu trữ\").<br>3. Quan sát kết quả. | Thao tác: Bấm vào \"Được ghim\" hoặc \"Lưu trữ\" | Viên Chip tương ứng xuất hiện trên thanh tìm kiếm; danh sách lọc ra chính xác các ghi chú có trạng thái tương ứng. | Bộ lọc dữ liệu / Code-inferred (As-built) | High |',
    '| **TC-BB-027E** | FN-23 | Tìm kiếm Ghi chú | Xác minh tìm kiếm kết hợp đồng thời Bộ lọc Chip và Từ khóa văn bản (Combined Query) | Có nhiều ghi chú, trong đó có ghi chú có hình ảnh và tiêu đề chứa `"Thiết kế"`. | 1. Bấm chọn mục \"Hình ảnh\" để tạo Chip lọc.<br>2. Gõ tiếp từ khóa `"Thiết kế"` vào sau Chip.<br>3. Quan sát kết quả. | Chip `[Hình ảnh]` + Từ khóa: `"Thiết kế"` | Danh sách chỉ hiển thị ghi chú vừa có chứa hình ảnh VỪA có tiêu đề/nội dung khớp từ khóa `"Thiết kế"`. | Tìm kiếm kết hợp / Code-inferred (As-built) | High |',
    '| **TC-BB-027F** | FN-23 | Tìm kiếm Ghi chú | Xác minh gỡ bỏ từng viên Chip lọc đơn lẻ trên thanh tìm kiếm | Đang có ít nhất 1 viên Chip lọc hiển thị trên thanh tìm kiếm. | 1. Chọn 1 bộ lọc để viên Chip xuất hiện trên thanh tìm kiếm.<br>2. Chạm vào biểu tượng \'X\' nằm bên trong viên Chip đó.<br>3. Quan sát giao diện. | Thao tác: Chạm icon \'X\' nhỏ trên viên Chip | Viên Chip biến mất khỏi thanh tìm kiếm; bộ lọc bị gỡ bỏ và danh sách kết quả cập nhật lại trạng thái không còn áp dụng filter đó. | Tiện ích giao diện / Code-inferred (As-built) | Medium |',
    '| **TC-BB-028** | FN-23 | Tìm kiếm Ghi chú | Xác minh giao diện thông báo khi không tìm thấy kết quả nào | Không có ghi chú nào chứa chuỗi tìm kiếm. | 1. Mở màn hình Tìm kiếm.<br>2. Nhập chuỗi từ khóa ngẫu nhiên không có thật.<br>3. Quan sát giao diện. | Từ khóa không tồn tại: `"tu_khoa_khong_co_thuc_999"` | Màn hình hiển thị hình biểu tượng tìm kiếm rỗng, tiêu đề *\"Không tìm thấy kết quả\"*, phụ đề *\"Thử từ khóa khác\"* và nút bấm *\"Xóa bộ lọc\"*. | Ca phủ định / Code-inferred (As-built) | Medium |',
    '| **TC-BB-028B** | FN-23 | Tìm kiếm Ghi chú | Xác minh loại trừ hoàn toàn ghi chú trong Thùng rác khỏi kết quả tìm kiếm | Có 1 ghi chú chứa từ khóa `"Tài liệu mật"` đã bị chuyển vào Thùng rác. | 1. Đưa ghi chú vào Thùng rác.<br>2. Mở màn hình Tìm kiếm, gõ từ khóa `"Tài liệu mật"`.<br>3. Quan sát kết quả. | Từ khóa: `"Tài liệu mật"` | Ghi chú nằm trong Thùng rác hoàn toàn không xuất hiện trong kết quả tìm kiếm; màn hình hiển thị trạng thái không tìm thấy kết quả. | Ràng buộc nghiệp vụ / Code-inferred (As-built) | High |',
    '| **TC-BB-028C** | FN-23 | Tìm kiếm Ghi chú | Mở và chỉnh sửa ghi chú trực tiếp từ danh sách kết quả tìm kiếm | Có ghi chú xuất hiện trong kết quả tìm kiếm. | 1. Chạm vào thẻ ghi chú trong danh sách kết quả tìm kiếm.<br>2. Màn hình Editor mở ra; thêm đoạn văn bản mới.<br>3. Bấm nút Back quay lại màn hình Tìm kiếm. | Thao tác: Chạm vào thẻ ghi chú $\\rightarrow$ Sửa thêm nội dung $\\rightarrow$ Bấm Back | Ghi chú mở ra đúng nội dung; sau khi chỉnh sửa và quay lại, danh sách tìm kiếm cập nhật ngay nội dung mới của ghi chú. | Luồng chuyển tiếp / Code-inferred (As-built) | High |',
    '| **TC-BB-028D** | FN-23 | Tìm kiếm Ghi chú | Xác minh nút mũi tên Back trên AppBar thoát màn hình tìm kiếm về Trang chủ | Đang ở màn hình Tìm kiếm. | 1. Tại màn hình Tìm kiếm, bấm vào biểu tượng mũi tên Back ở góc trái.<br>2. Quan sát màn hình. | Thao tác: Bấm icon mũi tên Back trên thanh tìm kiếm | Màn hình Tìm kiếm đóng lại; ứng dụng quay về Trang chủ và hiển thị đầy đủ danh sách ghi chú ban đầu. | Điều hướng / Code-inferred (As-built) | Medium |',
    '| **TC-BB-029** | FN-23 | Tìm kiếm Ghi chú | Kiểm tra độ an toàn khi nhập chuỗi ký tự đặc biệt (Input Robustness) | Đang ở màn hình Tìm kiếm. | 1. Mở màn hình Tìm kiếm.<br>2. Nhập chuỗi ký tự đặc biệt vào ô tìm kiếm.<br>3. Quan sát phản hồi ứng dụng. | Chuỗi ký tự đặc biệt: `\"\' OR \'1\'=\'1 -- % _ @#$ <script>\"` | Ứng dụng xử lý ổn định, không bị đơ, treo hay crash đột ngột; hiển thị an toàn giao diện không tìm thấy kết quả. | Độ bền nhập liệu / Code-inferred (As-built) | Low |'
]

# 2. Định nghĩa 17 Execution Items mới cho FN-23 trong Phần 2
fn23_items_part2 = [
    '| **TC-BB-026** | **D01** | Từ khóa: `"Báo cáo"` (khớp Tiêu đề) | Kiểm tra tìm kiếm khớp từ khóa trong Tiêu đề ghi chú. | Hiển thị thông báo số lượng khớp và trả về thẻ ghi chú có Tiêu đề chứa từ khóa `"Báo cáo"`. |',
    '| **TC-BB-026B** | **D01** | Note có `"Họp Tuần"`, nhập chữ thường: `"họp tuần"` | Kiểm tra tìm kiếm chữ thường không phân biệt hoa/thường. | Ứng dụng tìm thấy và hiển thị chính xác ghi chú `"Họp Tuần"` khi nhập chữ thường. |',
    '| **TC-BB-026B** | **D02** | Note có `"Họp Tuần"`, nhập chữ hoa: `"HỌP TUẦN"` | Kiểm tra tìm kiếm chữ hoa không phân biệt hoa/thường. | Ứng dụng tìm thấy và hiển thị chính xác ghi chú `"Họp Tuần"` khi nhập chữ hoa. |',
    '| **TC-BB-026C** | **D01** | Từ khóa tiếng Việt có dấu: `"kiểm thử"` | Kiểm tra tìm kiếm chính xác chuỗi tiếng Việt có dấu. | Hiển thị thẻ ghi chú chứa chuỗi tiếng Việt có dấu tương ứng trong danh sách kết quả. |',
    '| **TC-BB-026D** | **D01** | Note chứa `"Kế hoạch"`, tìm kiếm: `"Kế hoạch"` | Kiểm tra làm nổi bật (Highlight) từ khóa tìm kiếm trên thẻ ghi chú. | Đoạn chữ `"Kế hoạch"` trên thẻ ghi chú được bôi màu nền nổi bật (highlight vàng nhạt). |',
    '| **TC-BB-026E** | **D01** | Đang có từ khóa tìm kiếm $\\rightarrow$ Bấm nút \'X\' trên search bar | Kiểm tra nút \'X\' (Clear) xóa nhanh toàn bộ từ khóa và bộ lọc. | Ô tìm kiếm bị xóa trống, danh sách kết quả đóng lại và quay về menu các bộ lọc gợi ý ban đầu. |',
    '| **TC-BB-027** | **D01** | Từ khóa: `"giấy in A4"` (khớp trong Nội dung) | Kiểm tra tìm kiếm khớp từ khóa trong Nội dung văn bản ghi chú. | Hiển thị thẻ ghi chú có phần nội dung xem trước chứa đoạn văn bản `"giấy in A4"`. |',
    '| **TC-BB-027B** | **D01** | Bấm chọn mục \"Hình ảnh\" (hoặc \"Âm thanh\" / \"Liên kết\") | Kiểm tra lọc ghi chú theo Loại đa phương tiện bằng Chip. | Viên Chip tương ứng xuất hiện trên thanh tìm kiếm; danh sách chỉ lọc các note có loại dữ liệu đó. |',
    '| **TC-BB-027C** | **D01** | Bấm chọn nhãn dán trong danh mục Nhãn | Kiểm tra lọc ghi chú theo Nhãn dán bằng Chip. | Viên Chip mang tên nhãn xuất hiện trên thanh tìm kiếm; danh sách chỉ lọc các note gắn nhãn đó. |',
    '| **TC-BB-027D** | **D01** | Bấm chọn mục \"Được ghim\" hoặc \"Lưu trữ\" trong Trạng thái | Kiểm tra lọc ghi chú theo Trạng thái bằng Chip. | Viên Chip tương ứng xuất hiện; danh sách chỉ lọc các ghi chú có trạng thái tương ứng. |',
    '| **TC-BB-027E** | **D01** | Chip `[Hình ảnh]` + gõ từ khóa: `"Thiết kế"` | Kiểm tra tìm kiếm kết hợp đồng thời Bộ lọc Chip và Từ khóa văn bản. | Danh sách chỉ hiển thị ghi chú vừa chứa hình ảnh VỪA khớp từ khóa `"Thiết kế"`. |',
    '| **TC-BB-027F** | **D01** | Đang có Chip lọc $\\rightarrow$ Chạm icon \'X\' nhỏ bên trong viên Chip | Kiểm tra gỡ bỏ từng viên Chip lọc đơn lẻ trên thanh tìm kiếm. | Viên Chip biến mất; bộ lọc bị gỡ bỏ và danh sách kết quả cập nhật trạng thái không còn filter đó. |',
    '| **TC-BB-028** | **D01** | Từ khóa ngẫu nhiên không tồn tại: `"tu_khoa_khong_co_thuc_999"` | Kiểm tra giao diện thông báo khi không tìm thấy kết quả nào. | Hiển thị biểu tượng tìm kiếm rỗng, thông báo *\"Không tìm thấy kết quả\"*, *\"Thử từ khóa khác\"*. |',
    '| **TC-BB-028B** | **D01** | Note chứa `"Tài liệu mật"` trong Trash $\\rightarrow$ Tìm kiếm: `"Tài liệu mật"` | Kiểm tra loại trừ hoàn toàn ghi chú trong Thùng rác khỏi kết quả. | Ghi chú trong Thùng rác không xuất hiện trong kết quả; hiển thị trạng thái không tìm thấy. |',
    '| **TC-BB-028C** | **D01** | Chạm thẻ ghi chú trong kết quả $\\rightarrow$ Sửa nội dung $\\rightarrow$ Back | Kiểm tra mở và chỉnh sửa ghi chú trực tiếp từ kết quả tìm kiếm. | Mở đúng ghi chú trong Editor; sau khi sửa và quay lại, danh sách tìm kiếm cập nhật dữ liệu mới. |',
    '| **TC-BB-028D** | **D01** | Bấm icon mũi tên Back trên thanh tìm kiếm | Kiểm tra nút mũi tên Back trên AppBar thoát màn hình tìm kiếm về Trang chủ. | Màn hình Tìm kiếm đóng lại; ứng dụng quay về Trang chủ hiển thị đầy đủ danh sách ban đầu. |',
    '| **TC-BB-029** | **D01** | Chuỗi ký tự đặc biệt: `\"\' OR \'1\'=\'1 -- % _ @#$ <script>\"` | Kiểm tra độ an toàn khi nhập ký tự đặc biệt (Input Robustness). | Ứng dụng xử lý an toàn, không bị crash hay vỡ layout; hiển thị an toàn màn hình không có kết quả. |'
]

# 3. Thay thế trong Part 1 và Part 2
new_lines = []
in_part1_fn23 = False
in_part2_fn23 = False

for l in lines:
    # Phần 1: thay thế 4 TC cũ TC-BB-026 đến TC-BB-029 bằng 16 TCs mới
    if l.startswith('| **TC-BB-026** | FN-23'):
        new_lines.extend(fn23_tcs_part1)
        in_part1_fn23 = True
        continue
    if in_part1_fn23:
        if l.startswith('| **TC-BB-027** |') or l.startswith('| **TC-BB-028** |') or l.startswith('| **TC-BB-029** |'):
            continue
        else:
            in_part1_fn23 = False

    # Phần 2: thay thế 2 item cũ TC-BB-026 D01 và TC-BB-029 D01 bằng 17 items mới
    if l.startswith('| **TC-BB-026** | **D01**'):
        new_lines.extend(fn23_items_part2)
        in_part2_fn23 = True
        continue
    if in_part2_fn23:
        if l.startswith('| **TC-BB-029** | **D01**'):
            continue
        else:
            in_part2_fn23 = False

    # Phần 4: cập nhật số lượng TC của FN-23 thành 16
    if '| **FN-23** | Tìm kiếm Ghi chú theo từ khóa văn bản |' in l:
        new_lines.append('| **FN-23** | Tìm kiếm Ghi chú & Bộ lọc đa phương tiện | **16** | TC-BB-026, TC-BB-026B, TC-BB-026C, TC-BB-026D, TC-BB-026E, TC-BB-027, TC-BB-027B, TC-BB-027C, TC-BB-027D, TC-BB-027E, TC-BB-027F, TC-BB-028, TC-BB-028B, TC-BB-028C, TC-BB-028D, TC-BB-029 |')
        continue
    if '| **TỔNG CỘNG** | **10 Nhóm Chức Năng Trọng Tâm** |' in l:
        new_lines.append('| **TỔNG CỘNG** | **10 Nhóm Chức Năng Trọng Tâm** | **55** | **TC-BB-001 $\\rightarrow$ TC-BB-031** (Bao gồm các TC mở rộng theo chức năng) |')
        continue

    new_lines.append(l)

new_content = '\n'.join(new_lines)

# Thêm ghi chú chốt thiết kế FN-23 ở cuối tài liệu
new_content = new_content.rstrip() + '''

---

**FN-23 BLACK-BOX DESIGN = SẴN SÀNG THỰC THI**  
**16 TC / 17 Execution Items.**  
*Bao phủ tìm kiếm từ khóa tiêu đề, nội dung, case-insensitive, tiếng Việt có dấu, highlight, xóa nhanh, bộ lọc media (ảnh/audio/URL), nhãn dán, trạng thái (ghim/archive), truy vấn kết hợp chip+text, loại trừ thùng rác và độ bền nhập liệu an toàn.*
'''

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Updated black_box_test_cases.md with FN-23 16 TCs and 17 Execution Items successfully!')
