# HƯỚNG DẪN KIỂM THỬ TỰ ĐỘNG — SMART NOTE APP

**Cập nhật:** 19/10/2026 · **Nhánh:** huong. Hướng dẫn cho lượt chạy tiếp theo; không phải kết quả chạy mới.

## 1. Phạm vi hiện có

- UI/E2E: Python, pytest, uiautomator2, ADB; TC-BB-022 được ghi nhận hai lượt chạy, cả hai PASS, nhưng chỉ tính một test case duy nhất. Bộ XML baseline có 24 lượt chạy, tương ứng 23 test case duy nhất: 19 PASS, 4 FAIL.
- Provider: `test/automated/note_provider_test.dart` có 15 khai báo và `sync_provider_test.dart` có 9. Log lịch sử `automated_test_run.log` xác nhận 24 PASS; chưa xác minh chính xác commit thực thi. Không coi việc thiếu JUnit XML của Provider là thiếu sót bắt buộc nếu đã có log đầy đủ (file log hiện đã được đưa vào staging git qua `git add -f`).
- 31 TC UI là tập ứng viên baseline, gồm 23 có XML và 8 deferred. Lưu ý về script: 3 file script `test_fn10_trash.py`, `test_fn11_restore.py` và `test_fn12_permanent_delete.py` từng bị rỗng trên working tree nay đã được khôi phục nguyên vẹn từ Git HEAD (dùng `QANoteHelper`, giữ nguyên các file `.bak`). Kết quả 3 XML tương ứng là kết quả lịch sử phiên bản trước; các kịch bản này chưa chạy lại trong đợt cập nhật tài liệu này.

Tra cứu: [Plan](../docs/qa/automation_plan.md), [Test cases](../docs/qa/automation_test_cases.md), [Execution summary](../docs/qa/automation_execution_summary.md), [Node ID](../docs/qa/automation_script_inventory.md).

## Phạm vi mở rộng

Phase 3C/4 quản lý 61 AT/74 executions và báo cáo 14 AT/20 executions đã hoàn thành cùng 3 ca thăm dò riêng. Xem [ma trận mở rộng](../docs/qa/automation_expanded_scope.md). Kết quả Phase 4 được ghi nhận theo báo cáo thực thi cùng ảnh chụp màn hình nhưng chưa đối chiếu được log console hoặc file XML thực thi; ảnh chụp ghi nhận trạng thái UI nhưng không coi là bằng chứng đầy đủ cho mọi assertion. Chọn node theo phạm vi cần chạy; không cộng baseline và Phase 4 thành tổng test mới vì các tập giao nhau. Giữ riêng kết quả: TC-BB-006 có FAIL baseline trong XML (04/10) và PASS retest được Phase 4 báo cáo (13/10); mã lỗi BUG-BB-002/003 (FN-04) và BUG-002/003 (FN-40) là các mã khác nhau, không phải trùng mã.

## 2. Chuẩn bị môi trường UI

Chạy từ thư mục gốc repository trên máy có thiết bị QA. Hồ sơ đã dùng Python 3.13; đối chiếu môi trường thực tế thay vì coi mọi phiên bản đều đã được kiểm chứng.

```powershell
python --version
python -m pip show pytest uiautomator2
adb devices
adb -s <SERIAL_QA> shell getprop ro.product.model
adb -s <SERIAL_QA> shell getprop ro.build.version.release
adb -s <SERIAL_QA> shell getprop ro.build.version.sdk
```

Nếu thiếu thư viện, cài trong môi trường Python QA của bạn:

```powershell
python -m pip install pytest uiautomator2
```

Dùng serial từ `adb devices`, không gõ nguyên placeholder. `automation/config.py` đọc biến `DEVICE_SERIAL`:

```powershell
$env:DEVICE_SERIAL = '<SERIAL_QA>'
```

Ghi commit checkout, build APK thực tế, model, OS/API và phiên bản thư viện vào hồ sơ lượt chạy. Docstring và báo cáo cũ có thông tin OS khác nhau; kết quả ADB mới là thông tin của lượt mới.

Chuẩn bị đúng tài khoản: TC-BB-006 cần verified, ca chưa verify dùng tài khoản riêng. Các script hiện có thể dùng dữ liệu cấu hình trong mã; kiểm tra trước khi chạy. Không reset app, không xóa vân tay, không sửa `lib/`; chỉ dùng note/tài khoản QA cho thao tác thay đổi dữ liệu.

## 3. Bảo toàn bằng chứng trước lượt mới

Script hiện chụp ảnh vào các tên cố định trong `evidence/fn*/`. Trước khi chạy, sao lưu các thư mục ảnh của nhóm liên quan và XML lịch sử. Ví dụ dưới tạo thư mục theo thời gian; không dùng lại run ID cũ.

```powershell
$qaRun = Get-Date -Format 'yyyyMMdd_HHmmss'
$qaRunDir = "evidence/automation_runs/$qaRun"
New-Item -ItemType Directory -Force -Path $qaRunDir | Out-Null
$qaBefore = "$qaRunDir/before"
New-Item -ItemType Directory -Force -Path $qaBefore | Out-Null
Copy-Item automation/reports -Destination "$qaBefore/reports" -Recurse
# Ví dụ chạy FN-04: sao lưu ảnh nhóm này trước khi script ghi lại tên cũ.
if (Test-Path evidence/fn04) { Copy-Item evidence/fn04 -Destination "$qaBefore/fn04" -Recurse }
git rev-parse HEAD | Out-File "$qaRunDir/source_commit.txt"
Get-Date -Format o | Out-File "$qaRunDir/start_time.txt"
```

Nếu chạy nhiều FN, sao lưu từng thư mục tương ứng trước khi chạy. Sau lượt chạy, chép ảnh mới vào thư mục run và ghi rõ ảnh nào được tạo mới; việc sao chép không tự chứng minh ảnh cũ thuộc lượt mới. Không ghi mật khẩu vào hồ sơ môi trường.

## 4. Chọn node ID thay vì chạy toàn file

[Kiểm kê script](../docs/qa/automation_script_inventory.md) cho biết node nào khớp XML baseline, node nào là alias hoặc chưa có XML. Ví dụ chạy lại đúng ca đăng nhập thành công đã có lịch sử FAIL:

```powershell
python -m pytest 'automation/tests/test_fn04_login.py::TestFN04Login::test_tc_bb_006_valid_email_login' -v -s "--junitxml=$qaRunDir/fn04_retest.xml" *> "$qaRunDir/fn04_retest_console.log"
$qaExit = $LASTEXITCODE
$qaExit | Out-File "$qaRunDir/fn04_retest_exit_code.txt"
if (Test-Path evidence/fn04) { Copy-Item evidence/fn04 -Destination "$qaRunDir/after_fn04" -Recurse }
```

Thay node ID, tên XML/log và nhóm ảnh theo ca cần chạy. Dừng ca nếu tiền điều kiện chưa đạt; không dùng alias để tăng số ca. Để chạy lại baseline, chọn mỗi node đã có XML một lần; các biến thể mới chỉ thêm sau khi đã đối chiếu đặc tả.

`python automation/runner.py --suite fn04_login` chạy toàn file FN-04 và ghi vào XML mặc định; hiện có thể thu thêm alias/biến thể và ghi đè báo cáo. Chỉ dùng khi chủ động chọn toàn file và đã sao lưu, không coi đó là lệnh tái tạo đúng 4 TC FN-04 lịch sử.

Một số script có setup_class kết nối điện thoại, nên ngay cả kiểm tra collection cũng cần xem các import/điều kiện môi trường. Đợt rà soát tài liệu chỉ dùng AST, không thực thi script.

## 5. Xác minh Provider ở lượt mới

Cần Flutter SDK và dependencies của dự án. Dùng thư mục run riêng; nếu chưa tạo thì làm như mục 3.

```powershell
flutter --version *> "$qaRunDir/flutter_version.txt"
flutter pub get *> "$qaRunDir/flutter_pub_get.log"
$qaDepsExit = $LASTEXITCODE
$qaDepsExit | Out-File "$qaRunDir/flutter_pub_get_exit_code.txt"
# Chỉ chạy bước tiếp khi pub get thành công.
if ($qaDepsExit -ne 0) { throw 'Khong chuan bi duoc dependencies; dung luot Provider.' }
flutter test --no-pub -r expanded test/automated/note_provider_test.dart test/automated/sync_provider_test.dart *> "$qaRunDir/provider_test_run.log"
$qaProviderExit = $LASTEXITCODE
$qaProviderExit | Out-File "$qaRunDir/provider_exit_code.txt"
```

`pub get` có thể thay đổi file generated/lock tùy môi trường; xem `git status` trước/sau, không trộn các thay đổi tự sinh vào tài liệu. Không tạo log giả tại đường dẫn cũ. Nếu chạy mới, báo cáo commit, ngày và kết quả mới, giữ nguyên ghi nhận thiếu log lịch sử.

Provider dùng fake repository và mock MethodChannel; PASS không chứng minh đồng bộ Firebase hoặc hành vi biometric trên thiết bị thật.

## 6. Cách kết luận và cập nhật tài liệu

| Kết quả công cụ/điều kiện | Cách ghi nhận |
| --- | --- |
| Assertion đạt | PASS cho TC của lượt chạy đó |
| Assertion thất bại | Giữ FAIL, phân tích application/precondition/script/environment/Expected |
| Thiếu tiền điều kiện trước khi chạy | BLOCKED cho lượt mới, ghi rõ lý do |
| Ca chưa đưa vào lượt chạy | NOT RUN hoặc DEFERRED theo phạm vi |
| Chỉ có kết quả được báo cáo trong tài liệu cũ | Giữ kết quả lịch sử, thêm mức “chưa xác minh bằng chứng” |

Không cộng bản ghi lặp thành TC mới. Khi kết quả giữa các lượt khác nhau, lưu cả lịch sử và nêu rõ lượt chọn để tổng hợp. `xfail`/`skip` của pytest phải ghi theo trạng thái công cụ và nguyên nhân, không tự đổi thành PASS.

Cập nhật Execution Summary và Status sau khi kiểm tra XML/log/ảnh. Không tự nhận đạt nghiệm thu phát hành chỉ vì bộ test có tỷ lệ PASS cao.
