# KẾ HOẠCH KIỂM THỬ TỰ ĐỘNG — SMART NOTE APP

**Dự án:** Smart Note App · **Nhánh:** `huong` · **Phiên bản:** 1.1 · **Ngày rà soát:** 19/10/2026 (UTC+7)
**Mã nguồn và bằng chứng được đối chiếu:** `98abb5af577b2d38192e7a88e7ff94a2b5f77262`. Đây là cập nhật tài liệu; không có lượt chạy ứng dụng mới.

> **Phạm vi mở rộng cũng đang được quản lý:** Ngoài baseline 31 TC UI, hồ sơ Phase 3C chọn 61 TC/74 executions; Phase 4 báo cáo 14 TC/20 executions (19 PASS, 1 FAIL-APP) cùng 3 ca thăm dò riêng. Có report/script/ảnh nhưng chưa đối chiếu được XML/log cho các lượt mở rộng. TC-BB-006 được Phase 4 báo cáo PASS sau khi chuẩn bị lại tài khoản, khác FAIL trong XML baseline. Giữ hai nguồn, không cộng trùng hoặc bỏ qua kết quả được báo cáo. Xem [ma trận mở rộng và nguồn](automation_expanded_scope.md).


## 1. Mục tiêu và cơ sở kiểm thử

Thiết lập hồi quy cho các hành vi thường xuyên lặp lại của ứng dụng: xác thực, tạo/sửa ghi chú, vòng đời thùng rác, ghim, tìm kiếm và logic Provider. Đánh giá kết quả bằng assertion xác định, lưu bằng chứng và phân loại nguyên nhân thất bại trước khi kết luận lỗi sản phẩm.

Cơ sở: [SRS rút gọn](../plan_and_requirements/srs_condensed.md), [Master Test Plan](../plan_and_requirements/test_plan.md), [đặc tả hộp đen](../../test_cases/black_box/black_box_test_cases.md), [đặc tả tự động](automation_test_cases.md) và mã test thực tế. Tài liệu này hoàn thiện theo cấu trúc kế hoạch kiểm thử; không tự nhận đã được chứng nhận một tiêu chuẩn.

Các tài liệu tổng thể ngoài phạm vi tự động còn có số liệu baseline cũ; trong bộ tài liệu này, [báo cáo thực thi](automation_execution_summary.md) là nguồn đối chiếu số liệu tự động. Nếu Expected giữa các nguồn mâu thuẫn thì ghi vấn đề yêu cầu, không lấy hành vi hiện tại để tự đổi Expected.

## 2. Phạm vi và đơn vị đo

| Đối tượng | Phạm vi | Kết quả đã đối chiếu |
| --- | --- | --- |
| Hệ thống | 44 FN được kiểm kê | Không đồng nghĩa mọi FN đã có automation |
| UI/E2E baseline | 31 TC ứng viên, chọn từ hộp đen | 23 TC có XML; 19 PASS, 4 FAIL; 8 DEFERRED |
| Provider | 24 khai báo test, 15 NoteProvider + 9 SyncProvider | Log lịch sử xác nhận 24 PASS; chưa xác minh chính xác commit thực thi |
| Script mở rộng | Các biến thể, alias ngoài baseline | Có mã; chưa có XML tương ứng trong bộ bằng chứng rà soát |

Không cộng 140 manual execution items, unit tests hoặc security tests thuộc hồ sơ khác vào kết quả bộ tự động này. Không dùng 47 tests lịch sử hay 12 FN có mã để tuyên bố bao phủ toàn bộ 44 FN hoặc độ phủ dòng/nhánh mã nguồn.

## 3. Chiến lược hai tầng

| Thuộc tính | Android UI/E2E | Flutter Provider |
| --- | --- | --- |
| Mục tiêu | Luồng người dùng và trạng thái giao diện cuối | Hành vi Provider, dữ liệu trong fake repository và stream |
| Công cụ | Python 3.13, pytest, uiautomator2, ADB | Flutter Test/Dart, fake repositories, mock MethodChannel |
| Môi trường | Samsung Galaxy S21 FE 5G; phiên bản OS/model phải ghi theo từng lượt | Flutter SDK và dependencies tương ứng checkout |
| Cách xác minh | Node ID → XML → assertion → ảnh | Ref/group/test name → log mới hoặc log lịch sử đầy đủ |
| Giới hạn | Phụ thuộc accessibility, bàn phím, tài khoản, mạng, bố cục | Không kiểm tra UI, SQLite/Firestore thật hay LWW trên hai máy |

Hồ sơ lịch sử và docstring script ghi model/OS chưa nhất quán (Android 14/API 34 và Android 16/API 36). Giữ thông tin môi trường của từng report; trước lượt mới dùng ADB xác nhận và ghi lại, không tự chọn một phiên bản làm kết quả đo.

## 4. Tiêu chí chọn và tạm hoãn

Chọn TC có Expected rõ, dữ liệu chuẩn bị được, giá trị hồi quy cao, thao tác lặp lại ổn định và chi phí bảo trì phù hợp. Ưu tiên đăng nhập, tạo/sửa, thùng rác, ghim và tìm kiếm; kết hợp ca hợp lệ, không hợp lệ, biên hoặc chuyển trạng thái theo mục tiêu TC.

Tạm hoãn 8 ca baseline: TC-BB-010/011 (OAuth), 012..015 (sinh trắc học), 030 (offline/online), 031 (hai máy). Đây là giới hạn môi trường/triển khai hiện tại, không phải kết luận không thể tự động hóa. Script thăm dò OAuth/biometric chưa được coi là suite hồi quy hoàn tất.

BR-03 chỉ cần xác nhận cho trường hợp hai timestamp bằng nhau. Có thể thiết kế LWW với timestamp khác nhau khi đã có hai thiết bị và khả năng điều phối mạng.

## 5. Ma trận 44 FN

Số test Provider theo FN có liên kết chéo, không cộng các hàng để đếm tests duy nhất. Danh mục này phản ánh phạm vi mã và bằng chứng, không xác nhận manual PASS cho FN chưa tự động hóa.

| FN | Tên chức năng | Ưu tiên | UI/E2E | Provider | Trạng thái | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- |
| **FN-01** | Kiểm tra hợp lệ form đăng nhập (theo inventory hiện hành) | P1 | — | — | Chưa tự động hóa | Chưa có suite FN-01 riêng; một số TC dùng chung FN-04 |
| **FN-02** | Đăng ký tài khoản Email/Password | P1 | 5 chạy (4 PASS / 1 FAIL) | — | Có XML UI | 1 FAIL (TC-BB-003: sai thông báo lỗi) |
| **FN-03** | Xác thực email | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-04** | Đăng nhập tài khoản Email/Password | P1 | 4 chạy (1 PASS / 3 FAIL) | — | Có XML UI | 1 Precondition Issue + 2 thông báo gộp |
| **FN-05** | Đăng nhập nhanh Google OAuth | P1 | 0 chạy (2 chưa chạy) | — | **Chỉ có script thăm dò** | Phụ thuộc Google OAuth Dialog hệ thống |
| **FN-06** | Đặt lại mật khẩu | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-07** | Đăng xuất tài khoản | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-08** | Tạo ghi chú văn bản | P1 | 3 chạy (3 PASS) | 1 test (đã đối chiếu log máy 24 PASS) | Có XML UI | Đa tầng (UI máy thật + Provider) |
| **FN-09** | Chỉnh sửa và tự động lưu ghi chú | P1 | 2 chạy (2 PASS) | 1 test (đã đối chiếu log máy 24 PASS) | Có XML UI | Đa tầng (UI máy thật + Provider) |
| **FN-10** | Chuyển ghi chú vào thùng rác | P1 | 1 TC có XML PASS | 2 tests (đã đối chiếu log máy 24 PASS) | Có XML UI (lịch sử) | Script UI working tree hiện rỗng (0B); XML là lịch sử; Provider có mã |
| **FN-11** | Khôi phục ghi chú từ thùng rác | P1 | 1 TC có XML PASS | 3 tests (đã đối chiếu log máy 24 PASS) | Có XML UI (lịch sử) | Script UI working tree hiện rỗng (0B); XML là lịch sử; Provider có mã |
| **FN-12** | Xóa ghi chú vĩnh viễn | P1 | 1 TC có XML PASS | 1 test (đã đối chiếu log máy 24 PASS) | Có XML UI (lịch sử) | Script UI working tree hiện rỗng (1B); XML là lịch sử; Provider có mã |
| **FN-13** | Lưu trữ ghi chú (Archive) | P2 | — | 1 test (đã đối chiếu log máy 24 PASS) | Provider có log máy | Provider in-memory đã đối chiếu log máy (24 PASS) |
| **FN-14** | Bỏ lưu trữ ghi chú (Unarchive) | P2 | — | 1 test (đã đối chiếu log máy 24 PASS) | Provider có log máy | Provider in-memory đã đối chiếu log máy (24 PASS) |
| **FN-15** | Tạo ghi chú Checklist | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-16** | Thêm mục Checklist | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-17** | Đánh dấu hoàn thành mục Checklist | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-18** | Bỏ đánh dấu mục Checklist | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-19** | Xóa mục Checklist | P1 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-20** | Ghim và bỏ ghim ghi chú | P1 | 2 chạy (2 PASS) | 4 tests (đã đối chiếu log máy 24 PASS) | Có XML UI | Đa tầng (UI máy thật + Provider) |
| **FN-21** | Tạo nhãn (Tag) | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-22** | Gắn nhãn vào ghi chú | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-23** | Tìm kiếm ghi chú theo văn bản | P1 | 4 chạy (4 PASS) | 3 tests (đã đối chiếu log máy 24 PASS) | Có XML UI | Đa tầng (UI máy thật + Provider) |
| **FN-24** | Lọc ghi chú có ảnh (`has:image`) | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-25** | Lọc ghi chú có liên kết (`has:url`) | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-26** | Lọc ghi chú có âm thanh (`has:audio`) | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-27** | Lọc ghi chú ghim/lưu trữ | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-28** | Chuyển đổi Grid/List View | P3 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-29** | Kích hoạt khóa sinh trắc học | P1 | 0 chạy (1 chưa chạy) | — | **Chỉ có script thăm dò** | Phụ thuộc phần cứng quét vân tay |
| **FN-30** | Mở khóa ghi chú bằng sinh trắc học | P1 | 0 chạy (3 chưa chạy) | — | **Chỉ có script thăm dò** | Phụ thuộc Biometric Prompt hệ thống |
| **FN-31** | Gemini AI — Tóm tắt ghi chú | P2 | — | — | **Bị BLOCKED** | Lỗi service UI khung đỏ trên thiết bị thật |
| **FN-32** | Gemini AI — Đề xuất tiêu đề | P2 | — | — | **Bị BLOCKED** | Lỗi service UI khung đỏ trên thiết bị thật |
| **FN-33** | Gemini AI — Tạo Checklist | P2 | — | — | **Bị BLOCKED** | Lỗi service UI khung đỏ trên thiết bị thật |
| **FN-34** | Xuất ghi chú PDF | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-35** | Lưu hình vẽ tay (Canvas) | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-36** | Tải ảnh lên Cloudinary | P1 | — | — | Chưa tự động hóa | Rủi ro treo tải ảnh (BUG-001) |
| **FN-37** | Đổi màu nền ghi chú | P3 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-38** | Đặt thông báo nhắc nhở | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-39** | Chạm thông báo mở ghi chú | P2 | — | — | Chưa tự động hóa | Chưa có kịch bản riêng |
| **FN-40** | Bắt đầu đồng bộ dữ liệu | P1 | 0 chạy (1 chưa chạy) | 9 tests (đã đối chiếu log máy 24 PASS) | Provider có log máy | UI Offline/Sync deferred; Provider đã đối chiếu log máy (24 PASS) |
| **FN-41** | Giải quyết xung đột đồng bộ LWW | P1 | 0 chạy (1 chưa chạy) | — | Chưa tự động hóa | Yêu cầu 2 thiết bị; BR-03 chỉ cho trường hợp timestamp bằng nhau |
| **FN-42** | Xử lý ghi chú rất dài | P3 | — | — | Chưa tự động hóa | Kiểm thử phi chức năng |
| **FN-43** | Xử lý ảnh dung lượng lớn (OOM) | P3 | — | — | Chưa tự động hóa | Kiểm thử phi chức năng |
| **FN-44** | Xử lý thiết bị hết bộ nhớ | P3 | — | — | **Bị BLOCKED** | Giới hạn an toàn phần cứng máy thật |

Có XML UI ở 9 FN; Provider liên kết 10 FN (đã đối chiếu log máy `automated_test_run.log` gồm 24 PASS; chưa xác minh chính xác commit thực thi), trong đó 7 FN giao với UI (08, 09, 10, 11, 12, 20, 23). Hợp phạm vi mã hai tầng là 12 FN (thêm FN-13, 14, 40 ở tầng Provider). 3 FN thăm dò + 4 FN bị chặn theo hồ sơ + 25 FN chưa có test trong bộ chính thức + 12 FN có mã = 44.

## 6. Môi trường và dữ liệu

- Trước mỗi lượt ghi commit nguồn, build/version ứng dụng, thời gian và múi giờ, model/Android/API, Python/pytest/uiautomator2 hoặc Flutter/Dart và lệnh thực thi. Không suy ra commit build APK từ commit tài liệu.
- Tài khoản QA riêng: tài khoản đăng nhập thành công phải đã verify; ca chưa verify dùng tài khoản riêng; ca email không tồn tại cần xác nhận dữ liệu; ca duplicate chuẩn bị tài khoản tồn tại.
- Ghi chú có định danh riêng; chỉ xóa hoặc dọn dữ liệu của lượt test. Không reset app, xóa vân tay, thay đổi Expected để lấy PASS, hay sửa `lib/` trong tác vụ kiểm thử hộp đen.
- Tách chuẩn bị dữ liệu khỏi hành vi cần kiểm tra. Provider tạo fake repository mới trong setUp; UI xác nhận màn hình xuất phát và dữ liệu trước từng ca.

## 7. Điều kiện bắt đầu, dừng và kết thúc

**Entry:** Môi trường kết nối được, đúng build; tài khoản/note/mạng đáp ứng TC; node ID và assertion được đối chiếu; thư mục bằng chứng mới sẵn sàng.

**Dừng ca:** Thiếu tiền điều kiện, sai tài khoản, mất thiết bị, không xác định được note QA hoặc thao tác có thể ảnh hưởng dữ liệu khác. Ghi BLOCKED/lý do cho lượt mới. Khi assertion thất bại, lưu log và ảnh, xác định ca sau có độc lập không; không mặc định FAIL là lỗi sản phẩm.

**Tiếp tục:** Điều kiện được phục hồi và xác nhận; chạy lại ca với run ID mới. Giữ nguyên lịch sử cũ.

**Exit của đợt kiểm thử:** Mọi TC được chọn đã có kết quả hoặc được ghi rõ BLOCKED/DEFERRED; FAIL được phân tích; kết quả có bằng chứng truy vết, không có kết luận PASS thiếu chứng cứ. Chốt tài liệu không đồng nghĩa nghiệm thu phát hành ứng dụng.

## 8. Quy trình thực thi và bằng chứng

1. Kiểm tra entry, tạo run ID mới và lưu thông tin môi trường.
2. Chọn đúng node ID; tránh gọi alias hoặc script thăm dò ngoài phạm vi.
3. Chạy từng nhóm, lưu XML/log/ảnh và exit code của công cụ gốc.
4. Phân loại kết quả: application issue, precondition, script/locator, environment hoặc Expected cần xác nhận.
5. Đối chiếu số TC duy nhất và số bản ghi chạy; cập nhật report và status sau khi rà soát evidence.

Lệnh PowerShell và node ID được hướng dẫn tại [automation/README](../../automation/README.md) và [kiểm kê script](automation_script_inventory.md). Ảnh script hiện dùng đường dẫn cố định, cần sao lưu trước lượt mới để không ghi đè bằng chứng lịch sử.

## 9. Phân công và kế hoạch hoàn thiện

| Công việc | Người/nhóm đảm nhiệm | Điều kiện hoàn thành |
| --- | --- | --- |
| UI: chọn TC, chuẩn bị dữ liệu, chạy, phân tích và báo cáo | Hường phụ trách kiểm thử tự động | Có node ID, XML, ảnh và kết luận |
| Provider tích hợp từ nhánh thuong theo tài liệu lịch sử | Người đóng góp Provider và Hường đối chiếu | Có log khôi phục đúng nguồn hoặc lượt chạy mới, phân biệt tác giả và người tổng hợp |
| Xác nhận Expected thông báo đăng nhập | Người phụ trách yêu cầu/giảng viên và nhóm | Có quyết định ghi ngày; không tự xem là đã phê duyệt |
| Sửa lỗi sản phẩm khi được giao | Người phát triển | Build sửa lỗi và thông tin thay đổi để QA retest |

Thứ tự tiếp theo: bổ sung log Provider và log/XML Phase 4 → xác minh retest TC-BB-006 đã báo cáo PASS, chạy mới nếu cần → xác nhận tiêu chí 007/008 → retest 003 sau bản fix → rà script mở rộng/alias → mở rộng 8 ca khi đủ môi trường. Chi tiết và trạng thái tại [kế hoạch tiếp theo](automation_review_and_next_steps.md).

## 10. Rủi ro và biện pháp

| Rủi ro | Biện pháp |
| --- | --- |
| Alias/biến thể tạo lượt trùng | Chọn node ID rõ; báo cáo TC/dataset và lượt chạy riêng |
| Tọa độ/locator hoặc bàn phím thay đổi | Kiểm tra trạng thái chờ, ảnh lỗi; không kết luận product bug trước phân tích |
| Tài khoản chưa verify | Gate tiền điều kiện trước TC-BB-006 |
| Thông báo lỗi chưa thống nhất | Lưu Expected/Actual, đề nghị xác nhận, giữ FAIL lịch sử |
| Thiếu log Provider | Tách kết quả lịch sử khỏi xác minh; khôi phục log hoặc chạy mới |
| XML/ảnh không cùng lượt | Dùng run ID, ghi timestamp và đường dẫn; hiện tại ghi rõ giới hạn liên kết lịch sử |
| Tên/mã lỗi gây nhầm | Dùng TC-ID làm khóa; mã cũ chỉ là nhãn tham chiếu khi chưa có hồ sơ chính thức |

## 11. Bộ tài liệu bàn giao

- [Đặc tả TC](automation_test_cases.md): 31 TC baseline và phạm vi assertion Provider.
- [Trạng thái](automation_status.md): tiến độ hiện tại theo mức bằng chứng.
- [Báo cáo kết quả](automation_execution_summary.md): số liệu XML, phân tích FAIL, giới hạn Provider.
- [Kiểm kê script](automation_script_inventory.md): node ID, alias/biến thể và liên kết XML.
- [Rà soát và kế hoạch tiếp](automation_review_and_next_steps.md): thay đổi, tồn đọng, thứ tự xử lý.
- [Hướng dẫn thực thi](../../automation/README.md): chạy đúng phạm vi và lưu bằng chứng.
