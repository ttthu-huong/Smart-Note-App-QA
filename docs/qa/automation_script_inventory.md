# KIỂM KÊ SCRIPT TỰ ĐỘNG VÀ LIÊN KẾT XML

**Dự án:** Smart Note App · **Nhánh:** `huong` · **Phiên bản:** 1.1 · **Ngày rà soát:** 19/10/2026 (UTC+7)
**Mã nguồn và bằng chứng được đối chiếu:** `98abb5af577b2d38192e7a88e7ff94a2b5f77262`. Đây là cập nhật tài liệu; không có lượt chạy ứng dụng mới.

Kiểm kê tĩnh bằng Python AST, không import driver, không kết nối thiết bị, không chạy pytest. Phân biệt rõ số lượng giữa Git HEAD và Working Tree:

- **Tại Git HEAD & Working Tree sau khôi phục:** Có đầy đủ **48 hàm tên `test_*`** trong 11 file `automation/tests/test_*.py`: **23 hàm khớp node đã có JUnit XML baseline**, và **25 hàm chưa có XML tương ứng** trong 9 file báo cáo hiện lưu.
- **Lịch sử rà soát và khôi phục:** Trước đó trên working tree, 3 file script `test_fn10_trash.py` (0 bytes), `test_fn11_restore.py` (0 bytes) và `test_fn12_permanent_delete.py` (1 byte) từng bị rỗng do thay đổi cục bộ có từ trước ngày 16/10/2026 (khiến AST tạm thời chỉ đếm 45 hàm, thiếu 3 node XML). Hiện tại, cả 3 script đã được **khôi phục chính xác từ Git HEAD** (bản sử dụng `QANoteHelper`, giữ nguyên các file `.bak` untracked).
- **Ba node FN-10/11/12 đã khôi phục mã nhưng chưa chạy lại:**
  1. `automation/tests/test_fn10_trash.py::TestFN10Trash::test_tc_bb_021_move_note_to_trash` (khớp `fn10_trash_junit.xml`)
  2. `automation/tests/test_fn11_restore.py::TestFN11Restore::test_tc_bb_022_restore_note_from_trash` (khớp `fn11_restore_junit.xml`)
  3. `automation/tests/test_fn12_permanent_delete.py::TestFN12DeleteForever::test_tc_bb_023_permanent_delete_from_trash` (khớp `fn12_permanent_delete_junit.xml`)
  Mã nguồn script đã có đầy đủ trên máy, nhưng trong đợt này **chưa thực hiện chạy lại (chưa rerun)**; kết quả XML của 3 node này vẫn là kết quả lịch sử của phiên bản trước.

Các hàm bổ sung có thể là biến thể dữ liệu, alias hoặc thăm dò; không tự gộp mọi hàm thành TC mới. 31 TC baseline ứng viên và 23 TC có XML vẫn giữ nguyên. Một hàm có XML cũ không chứng minh phiên bản mã hiện tại đã chạy lại sau chỉnh sửa.

| Node ID theo mã nguồn | Liên kết bằng chứng | Ghi chú lựa chọn |
| --- | --- | --- |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_001_d01_gmail_success` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_001_d02_outlook_success` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_001_d03_edu_success` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_001_register_success` | PASS — [fn02_register_junit.xml](../../automation/reports/fn02_register_junit.xml) | Alias theo docstring; không chọn cùng hàm gốc |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_001b_trim_whitespace` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_002_empty_fields` | PASS — [fn02_register_junit.xml](../../automation/reports/fn02_register_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_002b_missing_password` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_002c_missing_email` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_003_d01_missing_at_symbol` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_003_d02_missing_domain` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_003_invalid_email_format` | FAIL — [fn02_register_junit.xml](../../automation/reports/fn02_register_junit.xml) | Alias theo docstring; không chọn cùng hàm gốc |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_004_d01_min_1_char` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_004_d02_boundary_5_chars` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_004_weak_password` | PASS — [fn02_register_junit.xml](../../automation/reports/fn02_register_junit.xml) | Alias theo docstring; không chọn cùng hàm gốc |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_005_d01_lowercase` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_005_d02_uppercase` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_005_duplicate_email` | PASS — [fn02_register_junit.xml](../../automation/reports/fn02_register_junit.xml) | Alias theo docstring; không chọn cùng hàm gốc |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_003b_disposable_email` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_004b_d01_min_6_chars` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn02_register.py::TestFN02Register::test_tc_bb_004b_d02_boundary_7_chars` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn04_login.py::TestFN04Login::test_tc_bb_009_empty_password` | PASS — [fn04_login_junit.xml](../../automation/reports/fn04_login_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn04_login.py::TestFN04Login::test_tc_bb_008_non_existent_account` | FAIL — [fn04_login_junit.xml](../../automation/reports/fn04_login_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn04_login.py::TestFN04Login::test_tc_bb_007_wrong_password` | FAIL — [fn04_login_junit.xml](../../automation/reports/fn04_login_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn04_login.py::TestFN04Login::test_tc_bb_006_valid_email_login` | FAIL — [fn04_login_junit.xml](../../automation/reports/fn04_login_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn04_login.py::TestFN04Login::test_tc_bb_006_d01_verified_account` | Có mã; chưa có XML tương ứng trong bộ rà soát | Alias theo docstring; không chọn cùng hàm gốc |
| `automation/tests/test_fn04_login.py::TestFN04Login::test_tc_bb_006b_unverified_account` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn04_login.py::TestFN04Login::test_tc_bb_006b_d01_unverified_account` | Có mã; chưa có XML tương ứng trong bộ rà soát | Alias theo docstring; không chọn cùng hàm gốc |
| `automation/tests/test_fn04_login.py::TestFN04Login::test_tc_bb_006c_trim_whitespace` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn04_login.py::TestFN04Login::test_tc_bb_006c_d01_trim_whitespace` | Có mã; chưa có XML tương ứng trong bộ rà soát | Alias theo docstring; không chọn cùng hàm gốc |
| `automation/tests/test_fn04_login.py::TestFN04Login::test_tc_bb_006d_uppercase_email` | Có mã; chưa có XML tương ứng trong bộ rà soát | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn04_login.py::TestFN04Login::test_tc_bb_006d_d01_uppercase_email` | Có mã; chưa có XML tương ứng trong bộ rà soát | Alias theo docstring; không chọn cùng hàm gốc |
| `automation/tests/test_fn05_google_oauth.py::TestGoogleOAuth::test_at21_cancel_google_account_picker` | Có mã; chưa có XML tương ứng trong bộ rà soát | Thăm dò theo hồ sơ |
| `automation/tests/test_fn08_create_note.py::TestFN08CreateNote::test_tc_bb_016_create_note_with_title_and_content` | PASS — [fn08_create_note_junit.xml](../../automation/reports/fn08_create_note_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn08_create_note.py::TestFN08CreateNote::test_tc_bb_017_create_note_without_title` | PASS — [fn08_create_note_junit.xml](../../automation/reports/fn08_create_note_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn08_create_note.py::TestFN08CreateNote::test_tc_bb_018_empty_note_not_created` | PASS — [fn08_create_note_junit.xml](../../automation/reports/fn08_create_note_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn09_edit_note.py::TestFN09EditNote::test_tc_bb_019_edit_note_content` | PASS — [fn09_edit_note_junit.xml](../../automation/reports/fn09_edit_note_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn09_edit_note.py::TestFN09EditNote::test_tc_bb_020_auto_save_after_delay` | PASS — [fn09_edit_note_junit.xml](../../automation/reports/fn09_edit_note_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn10_trash.py::TestFN10Trash::test_tc_bb_021_move_note_to_trash` | PASS — [fn10_trash_junit.xml](../../automation/reports/fn10_trash_junit.xml) | Đã khôi phục mã từ Git HEAD (dùng QANoteHelper); chưa chạy lại trong đợt này. Kết quả XML là lịch sử phiên bản trước. |
| `automation/tests/test_fn11_restore.py::TestFN11Restore::test_tc_bb_022_restore_note_from_trash` | PASS — [fn11_restore_junit.xml](../../automation/reports/fn11_restore_junit.xml) | Đã khôi phục mã từ Git HEAD (dùng QANoteHelper); chưa chạy lại trong đợt này. Kết quả XML là lịch sử phiên bản trước. |
| `automation/tests/test_fn12_permanent_delete.py::TestFN12DeleteForever::test_tc_bb_023_permanent_delete_from_trash` | PASS — [fn12_permanent_delete_junit.xml](../../automation/reports/fn12_permanent_delete_junit.xml) | Đã khôi phục mã từ Git HEAD (dùng QANoteHelper); chưa chạy lại trong đợt này. Kết quả XML là lịch sử phiên bản trước. |
| `automation/tests/test_fn20_pin_note.py::TestFN20PinNote::test_tc_bb_024_pin_note` | PASS — [fn20_pin_note_junit.xml](../../automation/reports/fn20_pin_note_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn20_pin_note.py::TestFN20PinNote::test_tc_bb_025_unpin_note` | PASS — [fn20_pin_note_junit.xml](../../automation/reports/fn20_pin_note_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn23_search.py::TestFN23Search::test_tc_bb_026_search_by_title` | PASS — [fn23_search_junit.xml](../../automation/reports/fn23_search_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn23_search.py::TestFN23Search::test_tc_bb_027_search_by_content` | PASS — [fn23_search_junit.xml](../../automation/reports/fn23_search_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn23_search.py::TestFN23Search::test_tc_bb_028_search_non_existent` | PASS — [fn23_search_junit.xml](../../automation/reports/fn23_search_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn23_search.py::TestFN23Search::test_tc_bb_029_search_special_characters` | PASS — [fn23_search_junit.xml](../../automation/reports/fn23_search_junit.xml) | Đối chiếu TC/dataset trước khi đưa vào hồi quy |
| `automation/tests/test_fn29_30_biometric.py::TestBiometricPrompt::test_at59_cancel_biometric_prompt` | Có mã; chưa có XML tương ứng trong bộ rà soát | Thăm dò theo hồ sơ |
| `automation/tests/test_fn29_30_biometric.py::TestBiometricPrompt::test_at60_back_from_locked_note` | Có mã; chưa có XML tương ứng trong bộ rà soát | Thăm dò theo hồ sơ |

Khi chạy lại baseline, chọn đúng 23 node có XML thay vì chạy toàn bộ thư mục. Chỉ chọn một node cho cùng TC/dataset. Chỉ thêm biến thể vào phạm vi chính thức sau khi đối chiếu Expected, xác nhận tiền điều kiện, chạy và lưu bằng chứng mới.

## Bổ sung nguồn Phase 4

Không có XML tương ứng không đồng nghĩa chưa từng chạy: một số hàm biến thể có kết quả được Phase 4 báo cáo cùng ảnh. Xem [ma trận mở rộng](automation_expanded_scope.md) để liên kết AT-ID, dataset và kết quả được báo cáo. Bảng phía trên chỉ kiểm kê mối liên hệ với 9 XML baseline.
