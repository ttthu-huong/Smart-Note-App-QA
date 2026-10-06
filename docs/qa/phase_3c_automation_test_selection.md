# KẾ HOẠCH LỰA CHỌN TEST CASE TỰ ĐỘNG HÓA - PHASE 3C (AUTOMATION TEST SELECTION PLAN)
## Dự án: Smart Note App
**Branch:** `huong`  
**Repository:** `ttt-huong/Smart-Note-App-QA`  
**Tiêu chuẩn:** IEEE 829 & ISTQB Test Planning / Test Selection  
**Mục tiêu:** Xác lập danh mục kiểm thử tự động hóa chính thức từ 118 Black-box Manual Test Cases trước khi tiến hành Phase 4.

---

## I. XÁC LẬP THỰC TẾ MÔI TRƯỜNG THIẾT BỊ KIỂM THỬ

1. **Device 1 (Primary Test Device):** 
   - **Samsung Galaxy S21 FE 5G** (Serial: `R5CW82ECF6M`).
   - Thiết bị đã được kết nối ADB và thiết lập môi trường uiautomator2 thành công, phục vụ chạy toàn bộ các kịch bản Single Device.
2. **Device 2 (Secondary Physical Device):** 
   - **Device 2 là điện thoại Android thật thứ hai; model/serial và trạng thái kết nối ADB sẽ được xác nhận khi thực hiện kiểm thử đa thiết bị.**
   - Sẵn sàng phục vụ cho các kịch bản kiểm thử phân tán, kiểm thử phiên đăng nhập đồng thời và đồng bộ dữ liệu đám mây khi framework được mở rộng.

---

## II. ĐÁNH GIÁ KỸ THUẬT NHÓM ĐỒNG BỘ VÀ XUNG ĐỘT (FN-40 / FN-41)

Nhóm chức năng FN-40 / FN-41 gồm **10 Test Cases**, trong đó có **09 Test Cases yêu cầu 02 thiết bị trong thiết kế Black-box**:

- **01 Test Case Single Device:**
  - **`TC-BB-030F` (`AT-61`):** Kéo vuốt xuống (Pull-to-refresh) tại Trang chủ để chủ động nạp lại danh sách ghi chú $\rightarrow$ **Recommended for Implementation** (*Single Device UI; không phụ thuộc kiểm thử đa thiết bị*).
- **09 Test Cases yêu cầu 02 thiết bị:**
  - **08 Test Cases xếp vào MANUAL PREFERRED:**
    - `TC-BB-030`: Tạo ghi chú khi offline trên D1 $\rightarrow$ online $\rightarrow$ kiểm tra note xuất hiện trên D2.
    - `TC-BB-030B`: Sửa nội dung khi offline trên D1 $\rightarrow$ online $\rightarrow$ đồng bộ sang D2.
    - `TC-BB-030C`: Xóa vĩnh viễn ghi chú khi offline trên D1 $\rightarrow$ online $\rightarrow$ mất trên D2.
    - `TC-BB-030D`: Ghim ghi chú khi offline trên D1 $\rightarrow$ online $\rightarrow$ ghim trên D2.
    - `TC-BB-030E`: Khóa ghi chú khi offline trên D1 $\rightarrow$ online $\rightarrow$ khóa trên D2.
    - `TC-BB-031`: Hai máy cùng sửa ghi chú: D2 online sửa sau ($t_B > t_A$) $\rightarrow$ kiểm tra Last-Write-Wins.
    - `TC-BB-031B`: Hai máy cùng sửa ghi chú: D1 offline sửa sau ($t_A > t_B$) $\rightarrow$ kiểm tra Last-Write-Wins.
    - `TC-BB-031C`: Xung đột giữa Sửa offline trên D1 ($t_A$) và Xóa vào thùng rác trên D2 ($t_B$).
    *(Lý do: Các kịch bản này có rủi ro lệch đồng hồ hệ thống - Clock Skew giữa 2 máy thật làm sai lệch timestamp LWW, rủi ro ngắt kết nối ADB khi tắt Wi-Fi, và độ trễ mạng Internet không xác định dễ gây flaky test).*
  - **01 Test Case xếp vào OPTIONAL:**
    - **`TC-BB-031D`:** Đăng nhập tài khoản trên thiết bị mới $\rightarrow$ toàn bộ dữ liệu đám mây được tải về đầy đủ. *(Kịch bản thực hiện tuần tự khi chuyển máy; chi phí dọn dẹp dữ liệu và thiết lập tài khoản lớn nên xếp vào nhóm mở rộng).*

---

## III. BẢNG PHÂN BỔ TỔNG THỂ 118 MANUAL TEST CASES THEO NHÓM CHỨC NĂNG

| Nhóm chức năng (FN) | KEEP | ENHANCE | NEW | TỔNG RECOMMENDED | OPTIONAL | MANUAL PREFERRED | NOT SUITABLE | TỔNG MANUAL TC |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **FN-02** (Đăng ký tài khoản) | 5 | 0 | 5 | **10** | 2 | 1 | 0 | **13** |
| **FN-04** (Đăng nhập Email) | 3 | 1 | 6 | **10** | 4 | 1 | 0 | **15** |
| **FN-05** (Google OAuth) | 0 | 0 | 1 | **1** | 1 | 6 | 0 | **8** |
| **FN-08** (Tạo ghi chú) | 3 | 0 | 4 | **7** | 1 | 0 | 0 | **8** |
| **FN-09** (Chỉnh sửa ghi chú) | 2 | 0 | 4 | **6** | 5 | 0 | 0 | **11** |
| **FN-10/11/12** (Thùng rác & Vòng đời) | 0 | 0 | 7 | **7** | 3 | 0 | 0 | **10** |
| **FN-20** (Ghim / Bỏ ghim) | 2 | 0 | 4 | **6** | 7 | 1 | 0 | **14** |
| **FN-23** (Tìm kiếm & Bộ lọc) | 4 | 0 | 6 | **10** | 4 | 3 | 0 | **17** |
| **FN-29/30** (Khóa bảo vệ ghi chú) | 0 | 0 | 3 | **3** | 2 | 6 | 1 | **12** |
| **FN-40/41** (Đồng bộ Cloud & LWW) | 0 | 0 | 1 | **1** | 1 | 8 | 0 | **10** |
| **TỔNG CỘNG** | **19** | **1** | **41** | **61** | **30** | **26** | **1** | **118** |

---

## IV. BẢNG TRUY VẾT AT-ID → MANUAL TC ID (TRACEABILITY MATRIX)

> **Quy ước trạng thái:**
> - **Recommended for Implementation (61 TCs):** Toàn bộ 03 Candidate đã hoàn thành Feasibility Validation và không còn Candidate. 61 Test Cases hiện thuộc Recommended for Implementation. Trong đó:
>   - **03 TCs đã có Feasibility Validation thực tế:** `AT-21` (PASS), `AT-59` (PASS), `AT-60` (PASS WITH PRECONDITION — Explicit Precondition Required).
>   - **58 TCs còn lại:** Được đánh giá phù hợp để triển khai dựa trên source code, cấu trúc UI và hạ tầng automation hiện tại; tính ổn định thực tế qua nhiều lần chạy sẽ được xác nhận trong quá trình Phase 4 implementation/execution.
> - **Candidate (00 TCs):** Không còn test case nào thuộc nhóm Candidate (0/61).

| AT-ID | Manual TC ID | FN | Priority | Decision | Device Mode | Trạng thái kỹ thuật | Hành vi quan sát được trên giao diện (Observable UI Behavior) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **AT-01** | TC-BB-001 | FN-02 | P0 | KEEP | SINGLE DEVICE | Recommended for Implementation | Đăng ký tài khoản hợp lệ; ứng dụng chuyển sang màn hình thông báo kiểm tra email. |
| **AT-02** | TC-BB-001B | FN-02 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Tự động loại bỏ khoảng trắng thừa đầu/cuối của email; đăng ký thành công. |
| **AT-03** | TC-BB-002 | FN-02 | P0 | KEEP | SINGLE DEVICE | Recommended for Implementation | Để trống cả 2 ô và nhấn Đăng ký; hiển thị thông báo lỗi màu đỏ ngay trên form. |
| **AT-04** | TC-BB-002B | FN-02 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Chỉ nhập Email, để trống Mật khẩu; ứng dụng giữ nguyên màn hình và báo lỗi. |
| **AT-05** | TC-BB-002C | FN-02 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Chỉ nhập Mật khẩu, để trống Email; ứng dụng giữ nguyên màn hình và báo lỗi. |
| **AT-06** | TC-BB-003 | FN-02 | P0 | KEEP | SINGLE DEVICE | Recommended for Implementation | Bắt lỗi ứng dụng BUG-FN02-01 khi email thiếu ký tự @ trên giao diện. |
| **AT-07** | TC-BB-003B | FN-02 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Nhập email thuộc tên miền không cho phép (tempmail.com); xuất hiện thông báo lỗi. |
| **AT-08** | TC-BB-004 | FN-02 | P1 | KEEP | SINGLE DEVICE | Recommended for Implementation | Nhập mật khẩu dưới 6 ký tự; xuất hiện thông báo mật khẩu quá yếu. |
| **AT-09** | TC-BB-004B | FN-02 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Kiểm tra mật khẩu biên 6 ký tự và 7 ký tự; ứng dụng chấp nhận đăng ký. |
| **AT-10** | TC-BB-005 | FN-02 | P1 | KEEP | SINGLE DEVICE | Recommended for Implementation | Đăng ký với email đã tồn tại; hiển thị thông báo email đã được đăng ký trước đó. |
| **AT-11** | TC-BB-006 | FN-04 | P0 | ENHANCE | SINGLE DEVICE | Recommended for Implementation | Đăng nhập tài khoản chuẩn đã kích hoạt; ứng dụng chuyển thẳng vào Trang chủ. |
| **AT-12** | TC-BB-006B | FN-04 | P0 | NEW | SINGLE DEVICE | Recommended for Implementation | Đăng nhập tài khoản chưa kích hoạt; ứng dụng chuyển hướng sang màn hình nhắc xác thực. |
| **AT-13** | TC-BB-006C | FN-04 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Tự động cắt tỉa khoảng trắng đầu/cuối của email khi đăng nhập. |
| **AT-14** | TC-BB-006D | FN-04 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Chấp nhận email nhập chữ in hoa; đăng nhập thành công vào ứng dụng. |
| **AT-15** | TC-BB-007 | FN-04 | P0 | KEEP | SINGLE DEVICE | Recommended for Implementation | Bắt lỗi ứng dụng BUG-BB-003 khi nhập sai mật khẩu đăng nhập. |
| **AT-16** | TC-BB-007B | FN-04 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Chặn đăng nhập với email sai định dạng cú pháp ngay khi bấm nút. |
| **AT-17** | TC-BB-008 | FN-04 | P0 | KEEP | SINGLE DEVICE | Recommended for Implementation | Bắt lỗi ứng dụng BUG-BB-002 khi đăng nhập email chưa từng đăng ký. |
| **AT-18** | TC-BB-009 | FN-04 | P0 | KEEP | SINGLE DEVICE | Recommended for Implementation | Nhập email hợp lệ nhưng để trống mật khẩu; hiển thị lỗi yêu cầu nhập đủ. |
| **AT-19** | TC-BB-009B | FN-04 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Nhập mật khẩu nhưng để trống email; hiển thị lỗi yêu cầu nhập đủ. |
| **AT-20** | TC-BB-009C | FN-04 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Để trống cả 2 ô khi đăng nhập; hiển thị thông báo lỗi yêu cầu nhập đầy đủ. |
| **AT-21** | TC-BB-011 | FN-05 | P1 | NEW | SYSTEM UI | Recommended for Implementation (Feasibility Validation: PASS) | Thoát hộp thoại chọn tài khoản Google; màn hình Đăng nhập duy trì ổn định. Đã xác nhận khả thi để triển khai automation bằng uiautomator2 trên Samsung Galaxy S21 FE 5G. Độ ổn định qua nhiều lần chạy sẽ được đánh giá trong Phase 4. Minh chứng: `evidence/fn05/FN05_TC-BB-011_D01_01.png`, `evidence/fn05/FN05_TC-BB-011_D01_02.png`. |
| **AT-22** | TC-BB-016 | FN-08 | P0 | KEEP | SINGLE DEVICE | Recommended for Implementation | Tạo ghi chú có đủ Tiêu đề và Nội dung; bấm Back lưu và hiển thị thẻ trên Trang chủ. |
| **AT-23** | TC-BB-017 | FN-08 | P1 | KEEP | SINGLE DEVICE | Recommended for Implementation | Tạo ghi chú không tiêu đề; thẻ ghi chú ngoài Trang chủ lấy dòng đầu nội dung hiển thị. |
| **AT-24** | TC-BB-018 | FN-08 | P1 | KEEP | SINGLE DEVICE | Recommended for Implementation | Để trống cả 2 ô trong trình soạn thảo; bấm Back tự hủy bản ghi, không tạo thẻ rỗng. |
| **AT-25** | TC-BB-018B | FN-08 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Tạo ghi chú chỉ có Tiêu đề; lưu thành công thẻ ghi chú ngoài Trang chủ. |
| **AT-26** | TC-BB-018C | FN-08 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Nhập nội dung $\rightarrow$ chờ 2 giây $\rightarrow$ thoát Editor $\rightarrow$ mở lại ghi chú $\rightarrow$ nội dung vừa nhập vẫn giữ nguyên vẹn. |
| **AT-27** | TC-BB-018E | FN-08 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Nhập tiếng Việt có dấu, Emoji, ký tự đặc biệt; hiển thị chính xác trên giao diện. |
| **AT-28** | TC-BB-018F | FN-08 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Đóng hoàn toàn ứng dụng và mở lại; ghi chú mới tạo vẫn hiển thị đầy đủ trên Trang chủ. |
| **AT-29** | TC-BB-019 | FN-09 | P0 | KEEP | SINGLE DEVICE | Recommended for Implementation | Mở ghi chú cũ, nhập thêm nội dung; bấm Back lưu thành công nội dung đã cập nhật. |
| **AT-30** | TC-BB-019B | FN-09 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Chỉnh sửa riêng tiêu đề; danh sách ngoài Trang chủ cập nhật tiêu đề mới. |
| **AT-31** | TC-BB-019D | FN-09 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Xóa sạch tiêu đề; thẻ ghi chú tự chuyển sang hiển thị xem trước bằng nội dung còn lại. |
| **AT-32** | TC-BB-019F | FN-09 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Xóa sạch cả tiêu đề và nội dung; ghi chú tự động bị xóa khỏi danh sách chính. |
| **AT-33** | TC-BB-019G | FN-09 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Lưu nội dung chỉnh sửa khi thoát bằng nút Back hoặc cử chỉ vuốt của hệ điều hành. |
| **AT-34** | TC-BB-020 | FN-09 | P1 | KEEP | SINGLE DEVICE | Recommended for Implementation | Chỉnh sửa nội dung và dừng gõ 2 giây; nội dung mới cập nhật trên thẻ ghi chú Trang chủ. |
| **AT-35** | TC-BB-021 | FN-10/11/12 | P0 | NEW | SINGLE DEVICE | Recommended for Implementation | Nhấn giữ ghi chú ngoài Trang chủ và bấm icon Thùng rác; ghi chú biến mất khỏi Trang chủ. |
| **AT-36** | TC-BB-021B | FN-10/11/12 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Bấm nút 'Hoàn tác' trên thông báo dưới đáy màn hình; ghi chú lập tức phục hồi lại Trang chủ. |
| **AT-37** | TC-BB-021C | FN-10/11/12 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Xóa ghi chú qua menu trong trình soạn thảo kèm hộp thoại xác nhận. |
| **AT-38** | TC-BB-022 | FN-10/11/12 | P0 | NEW | SINGLE DEVICE | Recommended for Implementation | Mở màn hình Thùng rác, bấm nút Khôi phục trên thẻ ghi chú; ghi chú quay lại Trang chủ. |
| **AT-39** | TC-BB-022C | FN-10/11/12 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Màn hình Thùng rác hiển thị biểu tượng và dòng chữ thông báo khi không có ghi chú nào. |
| **AT-40** | TC-BB-023 | FN-10/11/12 | P0 | NEW | SINGLE DEVICE | Recommended for Implementation | Xóa vĩnh viễn ghi chú trong Thùng rác kèm xác nhận hộp thoại cảnh báo. |
| **AT-41** | TC-BB-023C | FN-10/11/12 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Đóng và mở lại app; trạng thái Thùng rác và ghi chú đã xóa vĩnh viễn giữ nguyên trạng. |
| **AT-42** | TC-BB-024 | FN-20 | P0 | KEEP | SINGLE DEVICE | Recommended for Implementation | Ghim ghi chú ngoài Trang chủ; xuất hiện tiêu đề phân vùng 'ĐƯỢC GHIM' trên đầu. |
| **AT-43** | TC-BB-024B | FN-20 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Bấm biểu tượng Ghim / Bỏ ghim trực tiếp trên thanh tiêu đề trong trình soạn thảo. |
| **AT-44** | TC-BB-024C | FN-20 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Bấm Ghim khi ghi chú mới chưa có nội dung; hiển thị thông báo yêu cầu nhập nội dung trước. |
| **AT-45** | TC-BB-025 | FN-20 | P0 | KEEP | SINGLE DEVICE | Recommended for Implementation | Bỏ ghim ghi chú duy nhất đang ghim; phân vùng 'ĐƯỢC GHIM' tự động biến mất. |
| **AT-46** | TC-BB-025B | FN-20 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Đóng và khởi động lại app; các ghi chú đã ghim vẫn nằm trong khu vực 'ĐƯỢC GHIM'. |
| **AT-47** | TC-BB-025C | FN-20 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Chỉnh sửa nội dung ghi chú đã ghim; lưu xong ghi chú vẫn giữ nguyên vị trí ghim. |
| **AT-48** | TC-BB-026 | FN-23 | P0 | KEEP | SINGLE DEVICE | Recommended for Implementation | Nhập từ khóa trên thanh tìm kiếm; danh sách lọc ra đúng ghi chú có tiêu đề chứa từ khóa. |
| **AT-49** | TC-BB-026B | FN-23 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Tìm kiếm không phân biệt chữ hoa/thường và hỗ trợ tìm kiếm bằng tiếng Việt không dấu. |
| **AT-50** | TC-BB-026E | FN-23 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Bấm icon 'X' trên thanh tìm kiếm; xóa trắng ô nhập liệu và khôi phục danh sách đầy đủ. |
| **AT-51** | TC-BB-027 | FN-23 | P0 | KEEP | SINGLE DEVICE | Recommended for Implementation | Nhập từ khóa nằm trong phần nội dung; danh sách lọc đúng ghi chú tương ứng. |
| **AT-52** | TC-BB-027D | FN-23 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Chọn chip lọc trạng thái '[Được ghim]'; chỉ các ghi chú đã ghim xuất hiện trong kết quả. |
| **AT-53** | TC-BB-027E | FN-23 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Kết hợp vừa chọn chip lọc '[Được ghim]' vừa nhập từ khóa; danh sách lọc đúng giao 2 điều kiện. |
| **AT-54** | TC-BB-028 | FN-23 | P1 | KEEP | SINGLE DEVICE | Recommended for Implementation | Nhập từ khóa không tồn tại; hiển thị giao diện thông báo không tìm thấy kết quả. |
| **AT-55** | TC-BB-028B | FN-23 | P0 | NEW | SINGLE DEVICE | Recommended for Implementation | Ghi chú đang nằm trong Thùng rác không xuất hiện trong kết quả tìm kiếm. |
| **AT-56** | TC-BB-028C | FN-23 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Mở ghi chú từ màn hình kết quả tìm kiếm; cho phép xem và sửa nội dung bình thường. |
| **AT-57** | TC-BB-029 | FN-23 | P2 | KEEP | SINGLE DEVICE | Recommended for Implementation | Nhập chuỗi ký tự đặc biệt, dấu nháy đơn, chuỗi injection; ứng dụng xử lý an toàn. |
| **AT-58** | TC-BB-012C | FN-29/30 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Bấm khóa trên ghi chú mới chưa lưu; xuất hiện thông báo yêu cầu lưu ghi chú trước. |
| **AT-59** | TC-BB-015 | FN-29/30 | P1 | NEW | SYSTEM UI | Recommended for Implementation (Feasibility Validation: PASS) | Hủy hộp thoại xác thực hệ thống; ghi chú vẫn ở màn hình khóa bảo vệ. Đã xác nhận khả thi để triển khai automation bằng uiautomator2 trên Samsung Galaxy S21 FE 5G. Độ ổn định qua nhiều lần chạy sẽ được đánh giá trong Phase 4. Minh chứng: `evidence/fn29_30/FN29_30_TC-BB-015_D01_01.png`, `evidence/fn29_30/FN29_30_TC-BB-015_D01_02.png`, `automation/tests/test_fn29_30_biometric.py`. |
| **AT-60** | TC-BB-015C | FN-29/30 | P1 | NEW | PRECONDITION REQUIRED | Recommended for Implementation — Explicit Precondition Required (Feasibility Validation: PASS WITH PRECONDITION) | Nút Back trên màn hình khóa ghi chú đưa người dùng trở lại HomeScreen an toàn. Luồng kiểm thử chính đã chạy PASS bằng uiautomator2 (mở locked note, xác nhận Lock Overlay, thực hiện Back và assertion HomeScreen). Điểm giới hạn duy nhất là việc tạo trạng thái locked note ban đầu cần biometric vật lý (giới hạn của test fixture / test isolation, không phải giới hạn của khả năng automation của test case). Precondition chuẩn: "Trước khi chạy AT-60, môi trường kiểm thử phải có sẵn ít nhất 01 ghi chú đang ở trạng thái khóa trên tài khoản test của thiết bị" (Pre-existing locked note required). Minh chứng: `evidence/fn29_30/FN29_30_TC-BB-015C_D01_01.png`, `evidence/fn29_30/FN29_30_TC-BB-015C_D01_02.png`, `automation/tests/test_fn29_30_biometric.py`. |
| **AT-61** | TC-BB-030F | FN-40/41 | P1 | NEW | SINGLE DEVICE | Recommended for Implementation | Kéo vuốt xuống (Pull-to-refresh) tại Trang chủ nạp lại danh sách thành công (Single Device UI; không phụ thuộc kiểm thử đa thiết bị). |

---

## V. BẢNG ĐỐI SOÁT CÁC LƯỢT THỰC THI (EXECUTION MAPPING PROOF - 74 ROWS)

| STT | AT-ID | Manual TC ID | Execution ID / Dataset | Device Mode | Thuộc nhóm Candidate | Included in Automation Plan |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | AT-01 | TC-BB-001 | D01 (Gmail hợp lệ) | SINGLE DEVICE | No | Yes |
| 2 | AT-01 | TC-BB-001 | D02 (Outlook hợp lệ) | SINGLE DEVICE | No | Yes |
| 3 | AT-01 | TC-BB-001 | D03 (Edu hợp lệ) | SINGLE DEVICE | No | Yes |
| 4 | AT-02 | TC-BB-001B | D01 (Khoảng trắng đầu/cuối) | SINGLE DEVICE | No | Yes |
| 5 | AT-03 | TC-BB-002 | D01 (Trống cả 2 ô) | SINGLE DEVICE | No | Yes |
| 6 | AT-04 | TC-BB-002B | D01 (Chỉ email, trống pass) | SINGLE DEVICE | No | Yes |
| 7 | AT-05 | TC-BB-002C | D01 (Chỉ pass, trống email) | SINGLE DEVICE | No | Yes |
| 8 | AT-06 | TC-BB-003 | D01 (Thiếu ký tự @) | SINGLE DEVICE | No | Yes |
| 9 | AT-06 | TC-BB-003 | D02 (Thiếu tên miền) | SINGLE DEVICE | No | Yes |
| 10 | AT-07 | TC-BB-003B | D01 (Domain rác tempmail.com) | SINGLE DEVICE | No | Yes |
| 11 | AT-08 | TC-BB-004 | D01 (Mật khẩu 1 ký tự) | SINGLE DEVICE | No | Yes |
| 12 | AT-08 | TC-BB-004 | D02 (Mật khẩu 5 ký tự) | SINGLE DEVICE | No | Yes |
| 13 | AT-09 | TC-BB-004B | D01 (Biên tối thiểu 6 ký tự) | SINGLE DEVICE | No | Yes |
| 14 | AT-09 | TC-BB-004B | D02 (Biên N+1 với 7 ký tự) | SINGLE DEVICE | No | Yes |
| 15 | AT-10 | TC-BB-005 | D01 (Email đã tồn tại thường) | SINGLE DEVICE | No | Yes |
| 16 | AT-10 | TC-BB-005 | D02 (Email đã tồn tại chữ hoa) | SINGLE DEVICE | No | Yes |
| 17 | AT-11 | TC-BB-006 | D01 (Tài khoản chuẩn verified) | SINGLE DEVICE | No | Yes |
| 18 | AT-12 | TC-BB-006B | D01 (Tài khoản chưa verify) | SINGLE DEVICE | No | Yes |
| 19 | AT-13 | TC-BB-006C | D01 (Email có khoảng trắng) | SINGLE DEVICE | No | Yes |
| 20 | AT-14 | TC-BB-006D | D01 (Email viết chữ hoa) | SINGLE DEVICE | No | Yes |
| 21 | AT-15 | TC-BB-007 | D01 (Mật khẩu sai) | SINGLE DEVICE | No | Yes |
| 22 | AT-16 | TC-BB-007B | D01 (Email đăng nhập thiếu @) | SINGLE DEVICE | No | Yes |
| 23 | AT-16 | TC-BB-007B | D02 (Email thiếu tên miền) | SINGLE DEVICE | No | Yes |
| 24 | AT-17 | TC-BB-008 | D01 (Email chưa đăng ký) | SINGLE DEVICE | No | Yes |
| 25 | AT-18 | TC-BB-009 | D01 (Trống mật khẩu) | SINGLE DEVICE | No | Yes |
| 26 | AT-19 | TC-BB-009B | D01 (Trống email) | SINGLE DEVICE | No | Yes |
| 27 | AT-20 | TC-BB-009C | D01 (Trống cả 2 ô) | SINGLE DEVICE | No | Yes |
| 28 | AT-21 | TC-BB-011 | D01 (Hủy Account Picker) | SYSTEM UI | No | Yes |
| 29 | AT-22 | TC-BB-016 | D01 (Tạo note đủ Tiêu đề & Nội dung) | SINGLE DEVICE | No | Yes |
| 30 | AT-23 | TC-BB-017 | D01 (Tạo note không tiêu đề) | SINGLE DEVICE | No | Yes |
| 31 | AT-24 | TC-BB-018 | D01 (Trống cả 2 ô rồi thoát) | SINGLE DEVICE | No | Yes |
| 32 | AT-25 | TC-BB-018B | D01 (Tạo note chỉ có Tiêu đề) | SINGLE DEVICE | No | Yes |
| 33 | AT-26 | TC-BB-018C | D01 (Tự động lưu sau 2 giây) | SINGLE DEVICE | No | Yes |
| 34 | AT-27 | TC-BB-018E | D01 (Unicode tiếng Việt, Emoji) | SINGLE DEVICE | No | Yes |
| 35 | AT-28 | TC-BB-018F | D01 (Độ bền sau đóng mở lại app) | SINGLE DEVICE | No | Yes |
| 36 | AT-29 | TC-BB-019 | D01 (Chỉnh sửa thêm nội dung) | SINGLE DEVICE | No | Yes |
| 37 | AT-30 | TC-BB-019B | D01 (Chỉnh sửa riêng tiêu đề) | SINGLE DEVICE | No | Yes |
| 38 | AT-31 | TC-BB-019D | D01 (Xóa tiêu đề để preview) | SINGLE DEVICE | No | Yes |
| 39 | AT-32 | TC-BB-019F | D01 (Xóa sạch cả tiêu đề & nội dung) | SINGLE DEVICE | No | Yes |
| 40 | AT-33 | TC-BB-019G | D01 (Thoát bằng phím Back hệ thống) | SINGLE DEVICE | No | Yes |
| 41 | AT-33 | TC-BB-019G | D02 (Thoát bằng cử chỉ vuốt Back) | SINGLE DEVICE | No | Yes |
| 42 | AT-34 | TC-BB-020 | D01 (Tự động lưu khi đang chỉnh sửa) | SINGLE DEVICE | No | Yes |
| 43 | AT-35 | TC-BB-021 | D01 (Chuyển 1 note vào Thùng rác) | SINGLE DEVICE | No | Yes |
| 44 | AT-36 | TC-BB-021B | D01 (Hoàn tác trên thanh thông báo) | SINGLE DEVICE | No | Yes |
| 45 | AT-37 | TC-BB-021C | D01 (Xóa note qua menu trong Editor) | SINGLE DEVICE | No | Yes |
| 46 | AT-37 | TC-BB-021C | D02 (Hủy hộp thoại xác nhận xóa) | SINGLE DEVICE | No | Yes |
| 47 | AT-38 | TC-BB-022 | D01 (Khôi phục 1 note từ Thùng rác) | SINGLE DEVICE | No | Yes |
| 48 | AT-39 | TC-BB-022C | D01 (Kiểm tra Thùng rác rỗng) | SINGLE DEVICE | No | Yes |
| 49 | AT-40 | TC-BB-023 | D01 (Xóa vĩnh viễn 1 note kèm xác nhận) | SINGLE DEVICE | No | Yes |
| 50 | AT-41 | TC-BB-023C | D01 (Độ bền Thùng rác sau mở lại app) | SINGLE DEVICE | No | Yes |
| 51 | AT-42 | TC-BB-024 | D01 (Ghim 1 note từ Trang chủ) | SINGLE DEVICE | No | Yes |
| 52 | AT-43 | TC-BB-024B | D01 (Ghim từ AppBar trong Editor) | SINGLE DEVICE | No | Yes |
| 53 | AT-43 | TC-BB-024B | D02 (Bỏ ghim từ AppBar trong Editor) | SINGLE DEVICE | No | Yes |
| 54 | AT-44 | TC-BB-024C | D01 (Chặn ghim khi note rỗng) | SINGLE DEVICE | No | Yes |
| 55 | AT-45 | TC-BB-025 | D01 (Bỏ ghim note duy nhất đang ghim) | SINGLE DEVICE | No | Yes |
| 56 | AT-46 | TC-BB-025B | D01 (Độ bền trạng thái ghim) | SINGLE DEVICE | No | Yes |
| 57 | AT-47 | TC-BB-025C | D01 (Sửa note đã ghim vẫn giữ ghim) | SINGLE DEVICE | No | Yes |
| 58 | AT-48 | TC-BB-026 | D01 (Tìm kiếm khớp tiêu đề) | SINGLE DEVICE | No | Yes |
| 59 | AT-49 | TC-BB-026B | D01 (Tìm kiếm không phân biệt chữ hoa) | SINGLE DEVICE | No | Yes |
| 60 | AT-49 | TC-BB-026B | D02 (Tìm kiếm bằng chữ thường) | SINGLE DEVICE | No | Yes |
| 61 | AT-49 | TC-BB-026B | D03 (Tìm kiếm tiếng Việt không dấu) | SINGLE DEVICE | No | Yes |
| 62 | AT-50 | TC-BB-026E | D01 (Bấm icon 'X' xóa từ khóa) | SINGLE DEVICE | No | Yes |
| 63 | AT-51 | TC-BB-027 | D01 (Tìm kiếm khớp nội dung) | SINGLE DEVICE | No | Yes |
| 64 | AT-52 | TC-BB-027D | D01 (Chọn chip lọc [Được ghim]) | SINGLE DEVICE | No | Yes |
| 65 | AT-52 | TC-BB-027D | D02 (Bỏ chọn chip lọc [Được ghim]) | SINGLE DEVICE | No | Yes |
| 66 | AT-53 | TC-BB-027E | D01 (Kết hợp chip lọc và từ khóa) | SINGLE DEVICE | No | Yes |
| 67 | AT-54 | TC-BB-028 | D01 (Tìm từ khóa không tồn tại) | SINGLE DEVICE | No | Yes |
| 68 | AT-55 | TC-BB-028B | D01 (Không hiển thị note Thùng rác) | SINGLE DEVICE | No | Yes |
| 69 | AT-56 | TC-BB-028C | D01 (Mở và xem note từ tìm kiếm) | SINGLE DEVICE | No | Yes |
| 70 | AT-57 | TC-BB-029 | D01 (Ký tự đặc biệt, dấu nháy đơn) | SINGLE DEVICE | No | Yes |
| 71 | AT-58 | TC-BB-012C | D01 (Chặn khóa note mới chưa lưu) | SINGLE DEVICE | No | Yes |
| 72 | AT-59 | TC-BB-015 | D01 (Hủy xác thực vân tay hệ thống) | SYSTEM UI | No | Yes |
| 73 | AT-60 | TC-BB-015C | D01 (Bấm nút Back từ màn hình khóa) | PRECONDITION REQUIRED | No | Yes |
| 74 | AT-61 | TC-BB-030F | D01 (Pull-to-refresh nạp lại danh sách) | SINGLE DEVICE | No | Yes |

---

## VI. BÁO CÁO CÁC CHỈ SỐ BAO PHỦ (COVERAGE METRICS)

1. **Recommended Automation Test Case Coverage:**
   $$\frac{61\ \text{Test Cases}}{118\ \text{Manual Test Cases}} = \mathbf{51.69\%}$$
2. **Full Planned Test Case Coverage:**
   $$\frac{61\ \text{Test Cases}}{118\ \text{Manual Test Cases}} = \mathbf{51.69\%}$$
3. **Recommended Planned Execution Coverage:**
   $$\frac{74\ \text{Executions}}{134\ \text{Manual Executions}} = \mathbf{55.22\%}$$
4. **Full Planned Execution Coverage:**
   $$\frac{74\ \text{Executions}}{134\ \text{Manual Executions}} = \mathbf{55.22\%}$$
   *(Vì toàn bộ 03 Candidate trước đây đã hoàn tất Feasibility Validation và chuyển sang Recommended for Implementation, không còn test case nào ở trạng thái Candidate, do đó tỷ lệ Recommended Coverage và Full Planned Coverage hiện đồng nhất).*

---

## VII. TỔNG KẾT VÀ BÁO CÁO 10 ĐIỂM KỸ THUẬT CUỐI CÙNG

1. **Môi trường thiết bị kiểm thử:** Xác nhận môi trường có **02 điện thoại Android thật** khả dụng.
2. **Device 1 (Primary):** Samsung Galaxy S21 FE 5G (thực thi toàn bộ các ca kiểm thử Single Device).
3. **Device 2 (Secondary):** Điện thoại Android thật thứ hai; model/serial và trạng thái kết nối ADB sẽ được xác nhận khi thực hiện kiểm thử đa thiết bị.
4. **Các test cần 1 device:** Toàn bộ **61 Test Cases trong Planned Recommended Suite**.
5. **Các test cần 2 devices trong thiết kế:** Gồm **09 Test Cases** trong FN-40/FN-41 (08 Manual Preferred: `TC-BB-030` $\rightarrow$ `030E`, `TC-BB-031` $\rightarrow$ `031C`; 01 Optional: `TC-BB-031D`).
6. **Các test phụ thuộc System UI (02 TCs):** Cả 2 test đều đã hoàn thành **Feasibility Validation: PASS** trên Samsung Galaxy S21 FE 5G gồm: `AT-21` (`TC-BB-011` - Google Account Picker; minh chứng: `evidence/fn05/FN05_TC-BB-011_D01_01.png`, `evidence/fn05/FN05_TC-BB-011_D01_02.png`) và `AT-59` (`TC-BB-015` - Android BiometricPrompt; minh chứng: `evidence/fn29_30/FN29_30_TC-BB-015_D01_01.png`, `evidence/fn29_30/FN29_30_TC-BB-015_D01_02.png`, `automation/tests/test_fn29_30_biometric.py`).
7. **Các test cần Precondition (01 TC):** `AT-60` (`TC-BB-015C` - điều hướng Back từ màn hình khóa note, **Feasibility Validation: PASS WITH PRECONDITION**; yêu cầu chuẩn: *"Trước khi chạy AT-60, môi trường kiểm thử phải có sẵn ít nhất 01 ghi chú đang ở trạng thái khóa trên tài khoản test của thiết bị"*; minh chứng: `evidence/fn29_30/FN29_30_TC-BB-015C_D01_01.png`, `evidence/fn29_30/FN29_30_TC-BB-015C_D01_02.png`, `automation/tests/test_fn29_30_biometric.py`).
8. **Các test đưa vào kế hoạch tự động hóa (Recommended Suite):** Đúng **61 Test Cases** (61 Recommended for Implementation, trong đó 03 Candidate trước đây đã hoàn tất Feasibility Validation; 0 Candidate còn lại).
9. **Các test giữ ở Manual Preferred (26 TCs):** Gồm 8 test đồng bộ 2 máy & LWW, 6 test Google profile/session, 6 test quét cảm biến vân tay vật lý, 2 test ngắt mạng khi đang mở form, 4 test canvas/multi-select đảo trạng thái.
10. **Phân loại cuối cùng của toàn bộ 118 Manual Test Cases:**
    - **Recommended for Implementation:** **61 TCs**
      - *Feasibility Validation đã thực hiện thực tế (03 TCs):* `AT-21` (PASS), `AT-59` (PASS), `AT-60` (PASS WITH PRECONDITION — Explicit Precondition Required).
      - *Được đánh giá phù hợp triển khai dựa trên source/UI/infrastructure, chưa có feasibility probe riêng (58 TCs).*
    - **Candidate:** **00 TCs** (Toàn bộ 03 Candidate đã hoàn tất xác thực).
    - **Optional:** **30 TCs**
    - **Manual Preferred:** **26 TCs**
    - **Not Suitable:** **01 TC** (`TC-BB-015G`)
    - **Tổng cộng:** **118 TCs** (Khớp tuyệt đối).

---

```
PHASE 3C READY FOR USER APPROVAL
```
