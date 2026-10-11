# LÝ THUYẾT NỀN TẢNG: KIỂM THỬ TỰ ĐỘNG & KIỂM THỬ NÂNG CAO
**Học phần**: Đánh giá & Kiểm định chất lượng phần mềm (CSE703010)
**Đề tài**: Smart Note App (Flutter · SQLite · Firebase · Cloudinary · Gemini AI)
**Mục đích tài liệu**: Củng cố kiến thức nền trước khi lập kế hoạch và thực hiện **Chương 5 – Kiểm thử tự động** và **Chương 6 – Kiểm thử nâng cao** của báo cáo.
**Trạng thái**: Tài liệu học tập – chưa phải nội dung báo cáo chính thức.

---

## 📑 MỤC LỤC

- [Phần 0. Đọc tài liệu này thế nào](#phần-0-đọc-tài-liệu-này-thế-nào)
- [Phần 1. Kiến thức chung về kiểm thử](#phần-1-kiến-thức-chung-về-kiểm-thử)
- [Phần 2. Kiểm thử tự động (Automation Testing)](#phần-2-kiểm-thử-tự-động-automation-testing)
- [Phần 3. Kiểm thử nâng cao (Advanced Testing)](#phần-3-kiểm-thử-nâng-cao-advanced-testing)
  - 3.1 Kiểm thử hiệu năng · 3.2 Kiểm thử bảo mật · 3.3 Kiểm thử đột biến
  - 3.4 Kiểm thử dựa trên thuộc tính & Fuzz · 3.5 Kiểm thử độ tin cậy (Monkey/Chaos)
  - 3.6 Kiểm thử khả năng tiếp cận · 3.7 Kiểm thử tương thích
- [Phần 4. Tổng hợp & liên hệ với báo cáo](#phần-4-tổng-hợp--liên-hệ-với-báo-cáo)
- [Phần 5. Tự kiểm tra & thuật ngữ](#phần-5-tự-kiểm-tra--thuật-ngữ)

---

## PHẦN 0. ĐỌC TÀI LIỆU NÀY THẾ NÀO

Báo cáo của nhóm có 4 chương kiểm thử. Mỗi chương nhìn hệ thống từ một góc khác nhau:

```
 Chương 3: Hộp đen      → "App làm ĐÚNG CHỨC NĂNG không?"  (nhìn từ ngoài, theo đặc tả)
 Chương 4: Hộp trắng    → "Từng NHÁNH CODE có chạy đúng không?" (nhìn vào trong mã)  ✅ đã xong
 Chương 5: Tự động      → "Có KIỂM TRA LẠI được nhanh, lặp lại, không cần người bấm không?"
 Chương 6: Nâng cao     → "App có NHANH, AN TOÀN, BỀN, DỄ DÙNG không? Bộ test có THẬT SỰ TỐT không?"
```

- **Kiểm thử tự động** không phải là một *kỹ thuật thiết kế test* mới — nó là **cách thực thi** test bằng máy. Test case vẫn lấy từ hộp đen/hộp trắng, chỉ là được viết thành **script** chạy tự động.
- **Kiểm thử nâng cao** là nhóm các loại kiểm thử ngoài phạm vi chức năng cơ bản: hiệu năng, bảo mật, đột biến, độ tin cậy, khả năng tiếp cận… Mỗi loại có **quy trình riêng** (trình bày ở Phần 3).

> 💡 Mẹo học: đọc Phần 1 thật kỹ — mọi quy trình ở Phần 2 và 3 đều là **biến thể của quy trình chung** ở mục 1.2.

---

## PHẦN 1. KIẾN THỨC CHUNG VỀ KIỂM THỬ

### 1.1 Bảy nguyên tắc kiểm thử (ISTQB)

| # | Nguyên tắc | Ý nghĩa thực tế với Smart Note |
|---|---|---|
| 1 | Kiểm thử chỉ ra **sự có mặt** của lỗi, không chứng minh được **không có** lỗi | 83/83 test hộp trắng pass ≠ app không lỗi |
| 2 | Kiểm thử **vét cạn là không thể** | Không thể thử mọi tổ hợp nội dung ghi chú → phải chọn kỹ thuật (phân vùng, biên, ưu tiên rủi ro) |
| 3 | Kiểm thử **sớm** tiết kiệm chi phí | Test ở tầng unit rẻ hơn nhiều so với phát hiện lỗi khi đã build APK |
| 4 | Lỗi **tập trung** theo cụm | Code phức tạp (`editor_screen.dart` ~2.100 dòng, `sync_repository.dart`) thường chứa nhiều lỗi nhất |
| 5 | **Nghịch lý thuốc trừ sâu** – test cũ dần mất tác dụng | Phải bổ sung test mới (mutation, property-based) chứ không chỉ chạy lại test cũ |
| 6 | Kiểm thử **phụ thuộc ngữ cảnh** | App ghi chú offline-first ưu tiên test đồng bộ, mất mạng, bảo mật dữ liệu cá nhân |
| 7 | **Ảo tưởng không có lỗi** | App hết lỗi nhưng chậm/khó dùng vẫn là sản phẩm kém → cần kiểm thử phi chức năng (Chương 6) |

### 1.2 Quy trình kiểm thử chung (Test Process – ISTQB CTFL v4.0)

Đây là **khung xương** cho mọi loại kiểm thử. Khi đọc quy trình riêng của từng loại ở Phần 2, 3, bạn sẽ thấy chúng đều đi theo 7 hoạt động này.

```
 ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐
 │ 1. Lập kế    │──▶│ 2. Phân tích │──▶│ 3. Thiết kế  │──▶│ 4. Cài đặt       │
 │    hoạch     │   │   (Test      │   │   (Test      │   │   (Test          │
 │  (Planning)  │   │   Analysis)  │   │   Design)    │   │   Implementation)│
 └──────────────┘   └──────────────┘   └──────────────┘   └────────┬─────────┘
        ▲                                                          │
        │      ┌─────────────────────────────────────┐             ▼
        └──────│ 7. Giám sát & Điều chỉnh            │   ┌──────────────────┐
               │   (Monitoring & Control) – xuyên    │◀──│ 5. Thực thi      │
               │   suốt toàn bộ quá trình            │   │   (Execution)    │
               └─────────────────────────────────────┘   └────────┬─────────┘
                                                                  ▼
                                                        ┌──────────────────┐
                                                        │ 6. Kết thúc      │
                                                        │   (Completion)   │
                                                        └──────────────────┘
```

| Hoạt động | Câu hỏi trả lời | Sản phẩm đầu ra (đưa vào báo cáo) |
|---|---|---|
| 1. Lập kế hoạch | Test cái gì, bằng gì, ai làm, khi nào xong, thế nào là "đạt"? | Test Plan: phạm vi, công cụ, môi trường, tiêu chí vào/ra (Entry/Exit criteria) |
| 2. Phân tích | Cần kiểm tra điều kiện nào? | Danh sách điều kiện kiểm thử (Test Conditions), ưu tiên rủi ro |
| 3. Thiết kế | Test case cụ thể là gì? | Test case (input, bước, expected), dữ liệu test |
| 4. Cài đặt | Chuẩn bị đủ để chạy chưa? | Script, môi trường, dữ liệu mẫu, test suite |
| 5. Thực thi | Kết quả thực tế ra sao? | Log chạy, Actual result, Pass/Fail, Bug report |
| 6. Kết thúc | Đã đạt tiêu chí ra chưa? Rút ra gì? | Test Summary Report, bài học kinh nghiệm |
| 7. Giám sát | Có đúng tiến độ/chất lượng không? | Chỉ số: % pass, % coverage, số lỗi mở/đóng |

### 1.3 Cấp độ và loại kiểm thử

**Cấp độ (Test Levels)** – *test ở tầng nào của hệ thống*:

| Cấp độ | Đối tượng | Ví dụ Smart Note |
|---|---|---|
| Unit (Đơn vị) | 1 hàm/lớp độc lập | `BiometricService.authenticate()` |
| Integration (Tích hợp) | Nhiều thành phần phối hợp | `NoteRepository` + SQLite + Firestore |
| System (Hệ thống) | Toàn bộ app chạy thật | Đăng nhập → tạo note → mất mạng → bật mạng → đồng bộ |
| Acceptance (Chấp nhận) | Đáp ứng nhu cầu người dùng | Người dùng thử nghiệm thực tế |

**Loại (Test Types)** – *test khía cạnh nào*:

| Loại | Ý nghĩa | Thuộc chương |
|---|---|---|
| Chức năng (Functional) | Làm đúng việc | Ch.3, Ch.5 |
| Phi chức năng (Non-functional) | Làm tốt đến mức nào: nhanh, an toàn, dễ dùng… | **Ch.6** |
| Cấu trúc (Structural / White-box) | Bao phủ mã nguồn | Ch.4 |
| Liên quan thay đổi (Change-related) | Kiểm thử lại (Re-test) & Hồi quy (Regression) | **Ch.5** (tự động hóa hồi quy) |

### 1.4 Thuật ngữ bắt buộc phải nắm

| Thuật ngữ | Giải thích ngắn |
|---|---|
| **Test case** | Một kịch bản gồm: điều kiện đầu, bước, dữ liệu, kết quả mong đợi |
| **Test suite** | Tập hợp nhiều test case cùng mục tiêu |
| **Test script** | Test case được viết thành code để máy chạy |
| **Test oracle** | Nguồn để biết "kết quả đúng là gì" (đặc tả, tính toán tay, hệ thống cũ) |
| **Error → Defect (Bug) → Failure** | Người viết sai (error) → code có khuyết tật (defect) → khi chạy thì hỏng (failure) |
| **Severity vs Priority** | Mức độ nghiêm trọng về kỹ thuật vs mức độ cần sửa gấp về nghiệp vụ |
| **Smoke test** | Bộ test nhanh, kiểm tra "app có chạy được không" trước khi test sâu |
| **Regression test** | Chạy lại test cũ để chắc thay đổi mới không làm hỏng chức năng cũ |
| **Flaky test** | Test lúc pass lúc fail dù code không đổi |

---

## PHẦN 2. KIỂM THỬ TỰ ĐỘNG (AUTOMATION TESTING)

### 2.1 Khái niệm

**Kiểm thử tự động** là việc dùng phần mềm/công cụ để **thực thi test case, so sánh kết quả thực tế với kết quả mong đợi và báo cáo** mà không cần con người thao tác từng bước.

| Tiêu chí | Kiểm thử thủ công | Kiểm thử tự động |
|---|---|---|
| Tốc độ chạy | Chậm, phụ thuộc người | Nhanh (giây – phút) |
| Chi phí ban đầu | Thấp | Cao (viết script, dựng môi trường) |
| Chi phí khi chạy lại | Cao (mỗi lần lại mất công) | Gần như bằng 0 |
| Độ chính xác lặp lại | Dễ sai do mệt, bỏ sót | Lặp lại y hệt |
| Phù hợp | Test thăm dò, đánh giá UX, giao diện hay đổi | Hồi quy, test dữ liệu lớn, chạy trong CI |
| Phát hiện lỗi mới | Tốt (con người sáng tạo) | Kém (chỉ kiểm tra điều đã viết) |

### 2.2 Khi nào nên (và không nên) tự động hóa

**Nên tự động** khi test case: (1) chạy lặp lại nhiều lần (hồi quy), (2) chức năng ổn định ít đổi giao diện, (3) chức năng quan trọng/rủi ro cao, (4) cần nhiều bộ dữ liệu, (5) khó làm tay chính xác (đo thời gian, kiểm tra 1.000 ghi chú).

**Không nên tự động**: test thăm dò (exploratory), đánh giá cảm nhận thẩm mỹ, chức năng chỉ chạy 1 lần, màn hình đang thay đổi liên tục, thao tác phần cứng thật khó giả lập (quét vân tay thật).

**Ước lượng lợi ích (ROI) đơn giản**:

```
 Lợi ích  = (Thời gian chạy tay 1 lần × Số lần chạy) − (Chi phí viết script + Chi phí bảo trì)
 → Chỉ đáng tự động khi Lợi ích > 0 trong vòng đời dự án.
```

### 2.3 Kim tự tháp kiểm thử (Test Pyramid – Mike Cohn)

```
                       ▲   Chậm · Đắt · Dễ vỡ · Gần người dùng
                      ╱ ╲
                     ╱E2E╲          Integration test (integration_test / Patrol)
                    ╱ / UI╲         → Ít: 5–15 kịch bản luồng chính
                   ╱───────╲
                  ╱ Widget  ╲       Widget test (flutter_test)
                 ╱  / Service╲      → Vừa phải: các màn hình, component
                ╱─────────────╲
               ╱     Unit      ╲    Unit test (flutter_test + mocktail)
              ╱                 ╲   → Nhiều nhất: model, service, provider
             ╱───────────────────╲  ✅ Nhóm đã có 83 unit test hộp trắng
                       ▼   Nhanh · Rẻ · Ổn định · Xa người dùng
```

- **Nguyên tắc**: càng lên cao càng ít test, vì test cao chậm và dễ vỡ.
- **Phản mẫu "cây kem ốc quế" (Ice-cream cone)**: quá nhiều test UI/thủ công, ít unit test → bộ test chậm và khó bảo trì.

### 2.4 Ba cấp test trong Flutter

| | **Unit test** | **Widget test** | **Integration test** |
|---|---|---|---|
| Kiểm tra | 1 hàm / 1 lớp | 1 widget/màn hình được dựng & tương tác | Toàn app chạy trên máy ảo/máy thật |
| Gói | `flutter_test` (+ `mocktail`) | `flutter_test` | `integration_test` (SDK) hoặc `patrol` |
| Cần thiết bị? | Không | Không (môi trường giả lập widget) | **Có** (emulator/thiết bị) |
| Tốc độ | Mili-giây | Mili-giây – giây | Giây – phút |
| Phụ thuộc ngoài | Mock toàn bộ | Mock dịch vụ, dựng widget thật | Firebase/SQLite thật (hoặc Emulator) |
| Lệnh chạy | `flutter test test/unit/` | `flutter test test/widget/` | `flutter test integration_test/ -d <device>` |
| Ví dụ Smart Note | `searchNotes` lọc trash | `LoginScreen` báo lỗi khi email sai định dạng | Đăng nhập → tạo note → tìm thấy note trên Home |

**Khung một widget test** (minh họa):

```dart
testWidgets('Hiển thị lỗi khi email để trống', (WidgetTester tester) async {
  // Arrange: dựng widget trong MaterialApp (cần cả Provider giả nếu màn hình dùng Provider)
  await tester.pumpWidget(const MaterialApp(home: MyLoginForm()));

  // Act: thao tác như người dùng
  await tester.tap(find.text('Đăng nhập'));
  await tester.pump(); // vẽ lại 1 frame

  // Assert: kiểm tra kết quả
  expect(find.text('Vui lòng nhập email'), findsOneWidget);
});
```

**Khung một integration test** (minh họa):

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:smart_note_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('TC-AT-NOTE-01: Tạo ghi chú mới hiển thị trên Home', (tester) async {
    app.main();                       // chạy app thật
    await tester.pumpAndSettle();     // chờ hết animation/khởi tạo

    await tester.tap(find.byIcon(Icons.add));
    await tester.pumpAndSettle();
    await tester.enterText(find.byType(TextField).first, 'Ghi chú tự động');
    await tester.pageBack();          // quay lại → app tự lưu
    await tester.pumpAndSettle();

    expect(find.text('Ghi chú tự động'), findsOneWidget);
  });
}
```

> ⚠️ Integration test cần thêm `integration_test: sdk: flutter` vào `dev_dependencies` và tạo thư mục `integration_test/`. Đây là thay đổi cấu hình dự án → sẽ quyết định ở bước lập kế hoạch.

### 2.5 Kỹ thuật cốt lõi khi viết test tự động

**a) Mẫu AAA / Given–When–Then** — mỗi test chia 3 phần rõ ràng:

| AAA | BDD | Ý nghĩa |
|---|---|---|
| Arrange | Given | Chuẩn bị dữ liệu, mock, trạng thái ban đầu |
| Act | When | Thực hiện hành động cần kiểm tra |
| Assert | Then | So sánh kết quả với mong đợi |

**b) Test Doubles (đối tượng thay thế)** — để cô lập phần cần test khỏi Firebase, phần cứng, mạng:

| Loại | Định nghĩa | Ví dụ áp dụng |
|---|---|---|
| Dummy | Đối tượng truyền vào cho đủ tham số, không dùng | Tham số `context` không dùng tới |
| Stub | Trả về giá trị dựng sẵn | `canSyncOverride: () async => false` (giả lập mất mạng) |
| Spy | Ghi lại đã được gọi thế nào | `verify(() => firestore.deleteNote(id)).called(1)` |
| Mock | Đối tượng giả có kỳ vọng hành vi (mocktail) | `MockLocalAuthentication` trong test sinh trắc học |
| Fake | Bản cài đặt đơn giản nhưng chạy thật | SQLite in-memory (`sqflite_common_ffi`), `fake_cloud_firestore` |

**c) Kiểm thử hướng dữ liệu (Data-driven Testing)** — 1 kịch bản, chạy với nhiều bộ dữ liệu:

```dart
final cases = [
  ('', false), ('abc', false), ('a@b', false), ('qa@test.com', true),
];
for (final (email, valid) in cases) {
  test('Email "$email" hợp lệ = $valid', () => expect(isValidEmail(email), valid));
}
```

**d) Page Object / Robot Pattern** — gom thao tác của 1 màn hình vào 1 lớp, giúp script dễ đọc và dễ bảo trì khi UI đổi:

```dart
class LoginRobot {
  LoginRobot(this.tester);
  final WidgetTester tester;
  Future<void> enterEmail(String v) => tester.enterText(find.byKey(const Key('login_email')), v);
  Future<void> tapLogin() async { await tester.tap(find.text('Đăng nhập')); await tester.pumpAndSettle(); }
}
// Script: await robot.enterEmail('qa@test.com'); await robot.tapLogin();
```

**e) Cách tìm phần tử (Finder)** — theo thứ tự ổn định giảm dần:
1. `find.byKey(Key('...'))` – ổn định nhất nhưng **phải thêm Key vào code UI**.
2. `find.bySemanticsLabel(...)` – dựa trên nhãn trợ năng.
3. `find.byIcon`, `find.byType`, `find.byTooltip`.
4. `find.text('...')` – dễ vỡ khi đổi ngôn ngữ (app hỗ trợ vi/en!).

**f) Golden test (Snapshot)** — chụp ảnh widget và so sánh pixel với ảnh chuẩn: `await expectLater(find.byType(NoteCard), matchesGoldenFile('goldens/note_card.png'));`. Dùng để phát hiện thay đổi giao diện ngoài ý muốn.

**g) Flaky test – nguyên nhân & cách xử lý**

| Nguyên nhân | Biểu hiện trong Flutter | Cách xử lý |
|---|---|---|
| Animation vô hạn | `pumpAndSettle` timeout (ví dụ hiệu ứng Shimmer khi loading) | Dùng `pump(Duration)` thay vì `pumpAndSettle` |
| Phụ thuộc mạng thật | Firebase chậm/lỗi ngẫu nhiên | Dùng Firebase Emulator hoặc mock |
| Phụ thuộc thời gian | Test nhắc nhở, dọn rác 7 ngày | Tiêm "đồng hồ" giả, dùng thời gian cố định |
| Phụ thuộc thứ tự | Test sau dùng dữ liệu test trước để lại | `setUp`/`tearDown` dọn dữ liệu mỗi test |

### 2.6 Công cụ tự động hóa cho ứng dụng di động

| Công cụ | Loại | Ưu điểm | Hạn chế | Phù hợp Smart Note? |
|---|---|---|---|---|
| `flutter_test` | Unit/Widget | Có sẵn, nhanh, nhóm đã dùng | Không chạy trên thiết bị | ✅ Bắt buộc |
| `integration_test` | E2E chính thức của Flutter | Có sẵn trong SDK, viết bằng Dart | **Không bấm được hộp thoại native** (xin quyền, vân tay, chọn tài khoản Google) | ✅ Luồng chính |
| **Patrol** (LeanCode) | E2E mở rộng | Bấm được hộp thoại native, quyền, thông báo | Cấu hình Android phức tạp hơn | ⭐ Nếu cần test quyền/thông báo |
| **Maestro** | E2E dạng YAML, hộp đen | Viết rất nhanh, không cần biết code app | Ít kiểm soát nội bộ, cần cài CLI | ⭐ Thay thế nhanh |
| Appium (+ Flutter driver) | E2E đa nền tảng | Chuẩn công nghiệp, nhiều ngôn ngữ | Cài đặt nặng, chậm | Không ưu tiên |
| Firebase Test Lab | Chạy trên thiết bị thật đám mây | Nhiều đời máy, có Robo test | Giới hạn lượt miễn phí | Tùy chọn (tương thích) |
| GitHub Actions | CI | Tự chạy test mỗi lần push | Cần cấu hình `.env` giả | ✅ Nên có |

### 2.7 Tích hợp liên tục (CI/CD)

**CI (Continuous Integration)**: mỗi lần push code, máy chủ tự động build + chạy toàn bộ test tự động. Đây là nơi kiểm thử tự động phát huy giá trị lớn nhất: **hồi quy tự động sau mỗi thay đổi**.

```
 git push ─▶ [Checkout] ─▶ [Cài Flutter] ─▶ [pub get] ─▶ [analyze] ─▶ [unit+widget test] ─▶ [coverage] ─▶ ✅/❌
                                                                                   │
                                                                     (tùy chọn) [build APK] ─▶ [integration test trên emulator]
```

Ví dụ workflow GitHub Actions (minh họa – **chưa tạo trong dự án**):

```yaml
name: flutter-tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          channel: stable
      - run: cp .env.example .env      # .env được khai báo là asset nên phải tồn tại khi chạy test
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter test --coverage
```

**Báo cáo đầu ra thường dùng**: `coverage/lcov.info` → HTML bằng `genhtml`; kết quả dạng máy đọc `flutter test --machine` (JSON) → chuyển JUnit XML bằng gói `junitreport` để hiển thị trên CI.

### 2.8 ⭐ QUY TRÌNH KIỂM THỬ TỰ ĐỘNG (8 BƯỚC)

```
 [1] Chọn phạm vi ─▶ [2] Chọn công cụ ─▶ [3] Thiết kế framework ─▶ [4] Viết script
                                                                         │
 [8] Bảo trì ◀── [7] Báo cáo ◀── [6] Tích hợp CI ◀── [5] Chạy & ổn định ◀┘
```

| Bước | Việc cần làm | Đầu ra (minh chứng cho báo cáo) |
|---|---|---|
| **1. Phân tích & chọn phạm vi tự động** | Lấy danh sách test case hộp đen (Ch.3) + chức năng (FN-xx); chấm điểm theo tần suất chạy, rủi ro, độ ổn định UI, khả thi kỹ thuật → chọn ứng viên | Bảng "Ứng viên tự động hóa" có điểm ưu tiên và lý do chọn/loại |
| **2. Chọn công cụ** | So sánh công cụ (mục 2.6) theo tiêu chí: hỗ trợ Flutter, native dialog, chi phí, độ khó | Bảng so sánh + lý do lựa chọn |
| **3. Thiết kế framework** | Cấu trúc thư mục, quy ước đặt tên (`TC-AT-[MODULE]-[STT]`), Robot/Page Object, dữ liệu test, môi trường (emulator, tài khoản test, Firebase Emulator hoặc project test) | Sơ đồ cấu trúc, mô tả môi trường |
| **4. Viết script** | Mỗi script truy vết về 1 test case (Traceability); áp dụng AAA; tách dữ liệu khỏi logic | Mã nguồn test + ma trận truy vết |
| **5. Chạy, debug & ổn định** | Chạy nhiều lần (ví dụ 3–5 lần) để phát hiện flaky; sửa chờ đợi, dọn dữ liệu | Log terminal, tỷ lệ flaky |
| **6. Tích hợp CI** | Đưa vào GitHub Actions để tự chạy khi push | File workflow, ảnh chụp CI xanh/đỏ |
| **7. Báo cáo** | Tổng hợp pass/fail, thời gian chạy, coverage, lỗi phát hiện | Bảng kết quả, ảnh minh chứng, bug report |
| **8. Bảo trì** | Cập nhật script khi UI/logic đổi; loại test lỗi thời | Nhật ký thay đổi |

**Cấu trúc thư mục gợi ý**:

```text
test/
 ┣ unit/            # ✅ đã có – unit test hộp trắng
 ┣ widget/          # widget test các màn hình/component
 ┗ helpers/         # mock, fake, dữ liệu mẫu dùng chung
integration_test/
 ┣ robots/          # LoginRobot, HomeRobot, EditorRobot…
 ┣ flows/           # login_flow_test.dart, note_crud_flow_test.dart…
 ┗ test_data/       # tài khoản test, nội dung mẫu
```

**Ma trận truy vết (Traceability Matrix) mẫu**:

| Chức năng | Test case hộp đen | Script tự động | Cấp | Kết quả |
|---|---|---|---|---|
| FN-08 Tạo ghi chú | TC-BB-NOTE-01 | `note_crud_flow_test.dart` › TC-AT-NOTE-01 | Integration | PASS |
| FN-23 Tìm kiếm | TC-BB-SEARCH-03 | `search_screen_test.dart` › TC-AT-SEARCH-02 | Widget | FAIL → BUG-05 |

### 2.9 Chỉ số đánh giá kiểm thử tự động

| Chỉ số | Công thức | Ý nghĩa |
|---|---|---|
| Tỷ lệ tự động hóa | Số TC tự động / Tổng TC × 100% | Bao nhiêu phần trăm test không cần chạy tay |
| Tỷ lệ pass | TC pass / TC chạy × 100% | Sức khỏe hiện tại của app |
| Tỷ lệ flaky | TC kết quả không ổn định / TC × 100% | Độ tin cậy của bộ test |
| Thời gian thực thi | Tổng thời gian chạy suite | So sánh với thời gian chạy tay → chứng minh lợi ích |
| Độ bao phủ mã | Dòng/nhánh được chạy / tổng | Lấy từ `lcov.info` |
| Lỗi phát hiện | Số bug do test tự động tìm ra | Giá trị thực tế của bộ test |

### 2.10 Những "cái bẫy" riêng của Smart Note khi tự động hóa

| Vấn đề | Lý do | Hướng xử lý |
|---|---|---|
| `Firebase.initializeApp` lỗi trong unit/widget test | Không có nền tảng native | Mock service hoặc tiêm phụ thuộc (repository đã hỗ trợ tiêm service) |
| Plugin native (`local_auth`, `flutter_local_notifications`, `record`) | Platform channel không tồn tại trong test | Mock lớp service bọc plugin |
| Đăng nhập Google | Hộp thoại chọn tài khoản là native, khó tự động | Dùng tài khoản Email/Password dành riêng để test |
| Xác thực email bắt buộc | Tài khoản mới phải bấm link email | Chuẩn bị sẵn tài khoản test đã xác thực |
| Hiệu ứng Shimmer, loading | `pumpAndSettle` không bao giờ dừng | `pump(const Duration(seconds: 2))` |
| Gemini AI trả lời khác nhau mỗi lần | Kết quả không tất định | Chỉ kiểm tra "có trả về, không rỗng, đúng định dạng"; hoặc mock |
| Song ngữ vi/en | `find.text` vỡ khi đổi ngôn ngữ | Cố định locale khi test hoặc dùng Key |

---

## PHẦN 3. KIỂM THỬ NÂNG CAO (ADVANCED TESTING)

### 3.0 "Nâng cao" gồm những gì?

Không có một định nghĩa duy nhất; thường gồm **kiểm thử phi chức năng** (hiệu năng, bảo mật, độ tin cậy, khả năng tiếp cận, tương thích) và **kỹ thuật đánh giá chất lượng bộ test** (đột biến, dựa trên thuộc tính). Phạm vi chính xác **phụ thuộc yêu cầu của giảng viên** → nên đối chiếu đề cương/slide môn học.

Bảng dưới giúp chọn loại phù hợp với Smart Note:

| Loại | Trả lời câu hỏi | Mức phù hợp với Smart Note | Độ khó |
|---|---|---|---|
| 3.1 Hiệu năng | App có nhanh, mượt với nhiều dữ liệu không? | ★★★ (offline-first, phân trang, tìm kiếm, đồng bộ) | Trung bình |
| 3.2 Bảo mật | Dữ liệu cá nhân có an toàn không? | ★★★ (đã thấy dấu hiệu lộ API secret) | Trung bình |
| 3.3 Đột biến | Bộ test hiện tại có thật sự bắt được lỗi? | ★★★ (đánh giá 83 test hộp trắng) | Trung bình |
| 3.4 Thuộc tính / Fuzz | Có đầu vào lạ nào làm hỏng logic? | ★★ (model, math parser, tìm kiếm) | Trung bình |
| 3.5 Độ tin cậy (Monkey/Chaos) | App có crash khi bị dùng ngẫu nhiên / mất mạng đột ngột? | ★★ | Dễ |
| 3.6 Khả năng tiếp cận | Người khiếm thị/khó thao tác có dùng được không? | ★★ | Dễ |
| 3.7 Tương thích | Chạy được trên nhiều đời Android/màn hình? | ★ | Dễ – trung bình |

---

### 3.1 KIỂM THỬ HIỆU NĂNG (PERFORMANCE TESTING)

**Khái niệm**: đánh giá **tốc độ, khả năng đáp ứng, độ ổn định và mức sử dụng tài nguyên** của hệ thống dưới một mức tải xác định.

**Các dạng kiểm thử hiệu năng**:

| Dạng | Cách làm | Ví dụ Smart Note |
|---|---|---|
| Load (Tải) | Chạy ở mức tải dự kiến | Home với 500 ghi chú |
| Stress (Áp lực) | Tăng tải vượt mức tới khi hỏng, xem hỏng thế nào | 10.000 ghi chú, ghi chú 1 MB văn bản |
| Spike (Đột biến tải) | Tải tăng vọt đột ngột | Đồng bộ 300 ghi chú offline cùng lúc khi có mạng |
| Soak / Endurance (Độ bền) | Chạy lâu, tìm rò rỉ bộ nhớ | Mở/đóng editor 200 lần, theo dõi RAM |
| Volume (Khối lượng) | Dữ liệu lớn | Cơ sở dữ liệu SQLite rất lớn, nhiều ảnh |

**Chỉ số (Metrics) cho ứng dụng di động**:

| Chỉ số | Ngưỡng tham khảo | Cách đo |
|---|---|---|
| Thời gian khởi động (Startup) | Mở lạnh < 2–3 giây | `flutter run --profile --trace-startup` |
| Thời gian dựng khung hình (Frame build/raster) | ≤ 16,67 ms ở 60 FPS | DevTools Performance, `traceAction` |
| Tỷ lệ giật (Jank) | Càng thấp càng tốt | % frame vượt ngân sách 16,67 ms |
| Bộ nhớ (Memory) | Không tăng liên tục theo thời gian | DevTools Memory, Android Studio Profiler |
| Độ trễ truy vấn | Tìm kiếm < 100–300 ms | Đo `Stopwatch` quanh truy vấn SQLite |
| Thời gian đồng bộ | Tăng tuyến tính, không bùng nổ | Đo `syncNow` với N ghi chú |
| Kích thước APK | Theo dõi qua các phiên bản | `flutter build apk --analyze-size` |

> ⚠️ Đo hiệu năng **phải chạy ở chế độ Profile trên máy thật** (`--profile`). Chế độ Debug chậm hơn nhiều và cho số liệu sai.

**Công cụ**: Flutter DevTools · `integration_test` (`binding.traceAction`, `binding.watchPerformance`) + `flutter drive --profile` · `adb shell dumpsys gfxinfo <package>` · Android Studio Profiler · Firebase Performance Monitoring (cần thêm SDK).

Minh họa đo cuộn danh sách:

```dart
final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();
testWidgets('PERF-01: Cuộn Home với 1.000 ghi chú', (tester) async {
  // ... seed 1.000 ghi chú vào SQLite, mở Home ...
  await binding.traceAction(() async {
    await tester.fling(find.byType(Scrollable).first, const Offset(0, -3000), 5000);
    await tester.pumpAndSettle();
  }, reportKey: 'home_scroll');
});
```

**⭐ QUY TRÌNH KIỂM THỬ HIỆU NĂNG (8 bước)**

| Bước | Nội dung | Đầu ra |
|---|---|---|
| 1. Xác định yêu cầu phi chức năng | Đặt mục tiêu đo được (ví dụ "tìm kiếm 5.000 ghi chú < 300 ms") | Bảng tiêu chí đạt/không đạt |
| 2. Xác định kịch bản & tải | Chọn luồng quan trọng (khởi động, cuộn Home, tìm kiếm, mở editor, đồng bộ) và mức dữ liệu (100 / 1.000 / 5.000) | Danh sách kịch bản PERF-xx |
| 3. Chuẩn bị môi trường | Thiết bị thật cố định (ghi rõ model, RAM, Android), chế độ profile, tắt ứng dụng khác | Mô tả môi trường |
| 4. Chuẩn bị dữ liệu | Script sinh dữ liệu mẫu (seed) | Bộ dữ liệu |
| 5. Đo mốc (Baseline) | Chạy lần đầu, lặp ≥ 3 lần, lấy trung bình/trung vị | Số liệu baseline |
| 6. Thực thi các mức tải | Load → Stress → Soak | Log, timeline, biểu đồ |
| 7. Phân tích & tìm nút thắt cổ chai | So với tiêu chí; tìm nguyên nhân (truy vấn `LIKE`, dựng lại widget quá nhiều, ảnh chưa cache…) | Bảng kết quả + nhận định |
| 8. Đề xuất tối ưu & đo lại | Đề xuất cải tiến, đo lại để so sánh trước/sau | Bảng so sánh |

---

### 3.2 KIỂM THỬ BẢO MẬT (SECURITY TESTING)

**Khái niệm**: xác định **lỗ hổng** có thể bị khai thác để xâm phạm **tính bí mật – toàn vẹn – sẵn sàng** (CIA Triad) của dữ liệu và hệ thống.

**Chuẩn tham chiếu cho ứng dụng di động** (OWASP):
- **OWASP MASVS** – bộ yêu cầu bảo mật ứng dụng di động (Storage, Crypto, Auth, Network, Platform, Code, Resilience, Privacy).
- **OWASP MASTG** – hướng dẫn cách kiểm thử từng yêu cầu.
- **OWASP Mobile Top 10 (2024)**:

| Mã | Rủi ro | Điểm cần soi ở Smart Note |
|---|---|---|
| M1 | Improper Credential Usage – dùng thông tin xác thực sai cách | API secret Cloudinary trong file `.env` được đóng gói vào APK |
| M2 | Inadequate Supply Chain Security | Phiên bản thư viện trong `pubspec.lock` |
| M3 | Insecure Authentication/Authorization | Firestore Rules, khóa sinh trắc học có bỏ qua được không |
| M4 | Insufficient Input/Output Validation | Nội dung ghi chú, prompt gửi Gemini |
| M5 | Insecure Communication | Mọi kết nối có dùng HTTPS |
| M6 | Inadequate Privacy Controls | Log in ra thông tin cấu hình/cá nhân |
| M7 | Insufficient Binary Protections | APK có bị dịch ngược dễ dàng |
| M8 | Security Misconfiguration | Rules, quyền Android trong `AndroidManifest.xml` |
| M9 | Insecure Data Storage | SQLite lưu ghi chú dạng rõ (plaintext) trên máy |
| M10 | Insufficient Cryptography | Ghi chú "khóa" có được mã hóa hay chỉ ẩn trên UI |

**Các kỹ thuật**:

| Kỹ thuật | Mô tả | Công cụ ví dụ |
|---|---|---|
| SAST – Phân tích tĩnh | Soi mã nguồn/APK tìm mẫu nguy hiểm, không chạy app | `flutter analyze`, tìm chuỗi bí mật, **MobSF** (phân tích APK) |
| Phân tích APK (Reverse engineering) | Giải nén APK, xem tài nguyên, chuỗi | Giải nén APK → xem `assets/flutter_assets/`; `apktool` |
| DAST – Phân tích động | Chạy app và quan sát/can thiệp | MobSF dynamic, proxy (Burp/mitmproxy), `adb logcat` |
| Kiểm thử quy tắc truy cập | Thử đọc/ghi dữ liệu của user khác | **Firebase Emulator Suite** + `@firebase/rules-unit-testing` (`assertSucceeds`/`assertFails`) |
| Kiểm thử xâm nhập (Pentest) | Mô phỏng tấn công có kịch bản | Kết hợp các công cụ trên |

**Mô hình hóa mối đe dọa STRIDE** (dùng ở bước phân tích):

| | Đe dọa | Câu hỏi cho Smart Note |
|---|---|---|
| S | Spoofing – giả mạo | Có đăng nhập thay người khác được không? |
| T | Tampering – sửa đổi | Có sửa được ghi chú của người khác trên Firestore? |
| R | Repudiation – chối bỏ | Có ghi vết hành động không? |
| I | Information disclosure – lộ thông tin | Khóa bí mật, log, SQLite không mã hóa |
| D | Denial of service – từ chối dịch vụ | Lạm dụng hạn mức Gemini/Cloudinary |
| E | Elevation of privilege – leo thang quyền | Dùng secret để xóa toàn bộ file trên Cloudinary |

**⭐ QUY TRÌNH KIỂM THỬ BẢO MẬT (7 bước)**

| Bước | Nội dung | Đầu ra |
|---|---|---|
| 1. Xác định phạm vi & cho phép | **Chỉ kiểm thử trên app, project Firebase, tài khoản Cloudinary của nhóm**; ghi rõ phạm vi | Phạm vi & quy tắc thực hiện |
| 2. Mô hình hóa mối đe dọa | Vẽ luồng dữ liệu (App ↔ SQLite ↔ Firestore ↔ Cloudinary ↔ Gemini), áp STRIDE | Sơ đồ + bảng đe dọa |
| 3. Thu thập thông tin | Build APK release, liệt kê quyền, endpoint, thư viện | Danh sách tài sản cần bảo vệ |
| 4. Phân tích lỗ hổng | SAST/MobSF, soi APK, đọc Rules, thử truy cập chéo | Danh sách lỗ hổng nghi ngờ |
| 5. Xác minh (PoC) | Chứng minh lỗ hổng tồn tại **trên môi trường của nhóm**, không gây hại | Ảnh chụp/log minh chứng |
| 6. Đánh giá mức độ & báo cáo | Chấm mức nghiêm trọng (Critical/High/Medium/Low hoặc CVSS), mô tả tác động, đề xuất khắc phục | Bảng Security Findings |
| 7. Khắc phục & kiểm thử lại | Sau khi sửa, chạy lại đúng kịch bản để xác nhận đã đóng | Kết quả retest |

---

### 3.3 KIỂM THỬ ĐỘT BIẾN (MUTATION TESTING)

**Khái niệm**: cố ý **cấy lỗi nhỏ** vào mã nguồn (tạo ra *mutant* – "đột biến"), rồi chạy lại bộ test. Nếu test **fail** → mutant bị "giết" (bộ test tốt). Nếu test vẫn **pass** → mutant "sống sót" (bộ test có lỗ hổng).

> 🎯 **Vì sao quan trọng với nhóm**: Chương 4 báo coverage cao, nhưng **coverage chỉ cho biết dòng code đã CHẠY, không cho biết test có KIỂM TRA kết quả hay không**. Mutation testing đo trực tiếp *khả năng phát hiện lỗi* của 83 test hộp trắng.

**Hai giả thuyết nền tảng**:
- *Lập trình viên có năng lực (Competent Programmer)*: lỗi thật thường là sai lệch nhỏ so với code đúng.
- *Hiệu ứng ghép nối (Coupling Effect)*: test bắt được lỗi nhỏ thì cũng thường bắt được lỗi phức tạp.

**Toán tử đột biến (Mutation Operators)** – ví dụ trên code thật của Smart Note:

| Toán tử | Biến đổi | Ví dụ trong `sync_repository.dart` / repository |
|---|---|---|
| ROR – Thay toán tử quan hệ | `>` ↔ `>=`, `<`, `==` | `isAfter` → `isBefore` |
| LCR – Thay toán tử logic | `&&` ↔ `\|\|` | `cloud == null \|\| local...isAfter(...)` → `&&` |
| UOI/Negation – Phủ định điều kiện | `if (x)` → `if (!x)` | `if (await _canSync())` → `if (!await _canSync())` |
| SDL – Xóa câu lệnh | Bỏ 1 dòng | Bỏ `await _pendingDeleteSvc.add(id);` |
| CRP – Thay hằng số | `0` → `1`, `true` → `false` | `offset == 0` → `offset == 1` |
| RVR – Thay giá trị trả về | `return true` → `return false` | Trong `authenticate()` |

**Trạng thái mutant**: *Killed* (bị giết – tốt) · *Survived* (sống sót – thiếu test) · *Timeout* (treo, thường tính là bị giết) · *Equivalent* (tương đương – thay đổi không làm đổi hành vi, loại khỏi mẫu số).

**Công thức**:

```
 Mutation Score = Số mutant bị giết / (Tổng số mutant − Số mutant tương đương) × 100%
```

**Công cụ**: gói `mutation_test` trên pub.dev (tự sinh mutant theo luật và chạy test), hoặc **đột biến thủ công** có kiểm soát (tạo từng mutant, chạy test, khôi phục) – phù hợp quy mô bài tập và dễ trình bày trong báo cáo.

**⭐ QUY TRÌNH KIỂM THỬ ĐỘT BIẾN (7 bước)**

| Bước | Nội dung | Đầu ra |
|---|---|---|
| 1. Chọn mã mục tiêu | Các hàm đã có test hộp trắng (Ch.4): sync, trash, search, auth, biometric… | Danh sách hàm |
| 2. Xác nhận bộ test ban đầu xanh | Chạy `flutter test test/unit/` → 100% pass | Log baseline |
| 3. Sinh mutant | Áp toán tử đột biến (tự động hoặc thủ công), đánh mã `MUT-[MODULE]-[STT]` | Bảng mutant: vị trí, code gốc, code đột biến |
| 4. Chạy test với từng mutant | Mỗi mutant chạy bộ test tương ứng | Kết quả Killed/Survived |
| 5. Phân tích mutant sống sót | Mutant tương đương? Hay thiếu assert/thiếu ca biên? | Nhận định nguyên nhân |
| 6. Bổ sung/củng cố test | Viết thêm test để giết mutant sống sót | Test mới |
| 7. Tính lại điểm & báo cáo | So sánh Mutation Score trước/sau | Bảng tổng hợp |

> ⚠️ Khi đột biến thủ công, **luôn khôi phục code gốc** sau mỗi mutant (dùng git để kiểm soát) và không commit mutant.

---

### 3.4 KIỂM THỬ DỰA TRÊN THUỘC TÍNH (PROPERTY-BASED) & FUZZ TESTING

**Property-based testing**: thay vì viết từng ví dụ cụ thể, ta phát biểu một **thuộc tính luôn đúng (bất biến – invariant)**; công cụ tự sinh hàng trăm đầu vào ngẫu nhiên để thử phá vỡ nó, và khi tìm được phản ví dụ thì **thu nhỏ (shrink)** về trường hợp đơn giản nhất.

**Fuzz testing**: bơm dữ liệu ngẫu nhiên/sai định dạng/cực đoan vào chương trình để tìm crash, treo, ngoại lệ chưa xử lý.

Ví dụ bất biến cho Smart Note:

| Bất biến | Đối tượng |
|---|---|
| `Note.fromMap(note.toMap())` cho ra ghi chú y hệt ban đầu (round-trip) | `note_model.dart` |
| Kết quả tìm kiếm **không bao giờ** chứa ghi chú ở thùng rác | `searchNotes` |
| Bộ phân tích biểu thức **không crash** với chuỗi bất kỳ (chỉ trả kết quả hoặc báo lỗi hợp lệ) | `math_parser.dart` |
| Đọc nội dung checklist/Delta JSON hỏng không làm sập app | Các hàm parse trong `note_model.dart` |

**Công cụ**: gói `glados` (property-based cho Dart), hoặc tự viết vòng lặp sinh dữ liệu với `Random(seed)` cố định để tái lập được.

**Quy trình (6 bước)**: (1) Chọn hàm thuần/logic dữ liệu → (2) Phát biểu bất biến → (3) Định nghĩa bộ sinh dữ liệu (chuỗi Unicode, emoji, rỗng, rất dài, JSON hỏng) → (4) Chạy N lần với seed cố định → (5) Ghi nhận & thu nhỏ phản ví dụ → (6) Chuyển phản ví dụ thành unit test hồi quy + báo lỗi.

---

### 3.5 KIỂM THỬ ĐỘ TIN CẬY: MONKEY & CHAOS (RELIABILITY / ROBUSTNESS)

**Monkey testing**: gửi chuỗi thao tác ngẫu nhiên (chạm, vuốt, phím) vào app để tìm crash/ANR (ứng dụng không phản hồi). Android có sẵn công cụ:

```bash
adb shell monkey -p com.example.smart_note_app -s 42 --throttle 200 -v 2000
#            gói ứng dụng ────┘   seed ──┘   nghỉ giữa thao tác ┘   số sự kiện ┘
```

Dùng **seed cố định** (`-s`) để tái hiện được lỗi.

**Chaos / Fault injection** (rất hợp với Offline-First): cố ý tạo sự cố trong lúc app chạy:
- Tắt mạng **giữa lúc** đang đồng bộ, bật lại.
- Kill app khi đang lưu ghi chú → mở lại xem có mất dữ liệu.
- Hai thiết bị sửa cùng ghi chú → kiểm tra Last-Writer-Wins.
- Chỉnh lệch giờ thiết bị → kiểm tra phân xử xung đột theo `updated_at`.

**Quy trình (6 bước)**: (1) Xác định giả thuyết trạng thái ổn định ("không mất ghi chú, không crash") → (2) Chọn loại sự cố → (3) Chuẩn bị dữ liệu & cách quan sát (`adb logcat`, kiểm tra SQLite/Firestore) → (4) Gây sự cố & thực thi → (5) So sánh với trạng thái kỳ vọng → (6) Ghi lỗi, đề xuất cải thiện.

---

### 3.6 KIỂM THỬ KHẢ NĂNG TIẾP CẬN (ACCESSIBILITY TESTING)

**Khái niệm**: đảm bảo người khuyết tật (khiếm thị, vận động hạn chế…) dùng được app. Chuẩn tham chiếu: **WCAG 2.1** (độ tương phản, nhãn cho thành phần, kích thước vùng chạm).

Flutter có sẵn các **guideline tự động** trong `flutter_test`:

```dart
testWidgets('A11Y-01: Màn hình đăng nhập đạt chuẩn trợ năng', (tester) async {
  final handle = tester.ensureSemantics();
  await tester.pumpWidget(/* màn hình cần kiểm tra */);
  await expectLater(tester, meetsGuideline(androidTapTargetGuideline));   // vùng chạm ≥ 48x48
  await expectLater(tester, meetsGuideline(labeledTapTargetGuideline));   // nút có nhãn
  await expectLater(tester, meetsGuideline(textContrastGuideline));       // tương phản chữ
  handle.dispose();
});
```

Kết hợp kiểm tra tay: bật **TalkBack**, phóng to cỡ chữ hệ thống, dùng **Accessibility Scanner** (Google).

**Quy trình (5 bước)**: (1) Chọn màn hình chính → (2) Kiểm tra tự động bằng guideline → (3) Kiểm tra tay với TalkBack/cỡ chữ lớn/chế độ tối → (4) Ghi vi phạm theo tiêu chí WCAG → (5) Đề xuất sửa & kiểm lại.

---

### 3.7 KIỂM THỬ TƯƠNG THÍCH (COMPATIBILITY TESTING)

**Khái niệm**: xác minh app hoạt động đúng trên nhiều **phiên bản Android, kích thước màn hình, mật độ điểm ảnh, ngôn ngữ, chế độ sáng/tối**.

**Cách làm**: lập **ma trận thiết bị** (ví dụ Android 10/12/14 × điện thoại nhỏ/lớn/tablet), chạy bộ smoke test tự động trên từng cấu hình (emulator hoặc **Firebase Test Lab** – có Robo test tự khám phá app).

**Quy trình (5 bước)**: (1) Xác định cấu hình mục tiêu → (2) Lập ma trận ưu tiên → (3) Chọn bộ test chạy trên mỗi cấu hình → (4) Thực thi & chụp minh chứng → (5) Tổng hợp bảng tương thích (Đạt/Lỗi theo từng cấu hình).

---

## PHẦN 4. TỔNG HỢP & LIÊN HỆ VỚI BÁO CÁO

### 4.1 Bảng so sánh nhanh các quy trình

| Loại | Đầu vào chính | Công cụ chính | Sản phẩm then chốt | Chỉ số |
|---|---|---|---|---|
| Tự động | Test case hộp đen/hộp trắng | flutter_test, integration_test, CI | Script + ma trận truy vết | % tự động, pass rate, thời gian |
| Hiệu năng | Yêu cầu phi chức năng | DevTools, traceAction, profile mode | Bảng số đo vs tiêu chí | ms, FPS, jank, MB |
| Bảo mật | Mô hình đe dọa, OWASP | MobSF, Emulator Rules, phân tích APK | Security Findings | Số lỗ hổng theo mức độ |
| Đột biến | Bộ test có sẵn | mutation_test / thủ công | Bảng mutant | Mutation Score |
| Thuộc tính/Fuzz | Bất biến | glados, Random(seed) | Phản ví dụ | Số lỗi tìm được |
| Monkey/Chaos | Giả thuyết ổn định | adb monkey, tắt mạng, kill app | Nhật ký sự cố | Crash/ANR, mất dữ liệu |
| Tiếp cận | WCAG | meetsGuideline, TalkBack | Danh sách vi phạm | Số vi phạm |
| Tương thích | Ma trận thiết bị | Emulator, Test Lab | Bảng tương thích | % cấu hình đạt |

### 4.2 Khung trình bày gợi ý cho báo cáo (đồng bộ với Chương 4)

Chương 4 đang đi theo mạch **Cơ sở lý thuyết → Thiết kế chi tiết → Kết quả & đánh giá**. Nên giữ cùng mạch cho Chương 5, 6:

```
 5. Kiểm thử tự động
   5.1 Cơ sở lý thuyết (tóm lược Phần 2 tài liệu này)
   5.2 Kế hoạch & lựa chọn công cụ (phạm vi, môi trường, tiêu chí đạt)
   5.3 Thiết kế framework & kịch bản (cấu trúc, ma trận truy vết)
   5.4 Thực thi & kết quả (log, ảnh, CI)
   5.5 Đánh giá (chỉ số, lỗi phát hiện, hạn chế)

 6. Kiểm thử nâng cao
   6.1 Cơ sở lý thuyết & lý do chọn các loại kiểm thử
   6.x Mỗi loại đã chọn: Mục tiêu → Quy trình → Kịch bản → Kết quả → Nhận xét
   6.n Tổng hợp lỗi & đề xuất khắc phục
```

### 4.3 Mẫu test case & mẫu báo lỗi

**Quy ước mã** (nối tiếp quy ước `TC-WB-...` của Chương 4):
`TC-AT-[MODULE]-[STT]` (tự động) · `PERF-[STT]` · `SEC-[STT]` · `MUT-[MODULE]-[STT]` · `A11Y-[STT]` · `BUG-[STT]`.

**Mẫu test case tự động**:

| Mã | Chức năng | Cấp | Điều kiện đầu | Các bước | Dữ liệu | Kết quả mong đợi | Kết quả thực tế | Trạng thái | Script |
|---|---|---|---|---|---|---|---|---|---|
| TC-AT-NOTE-01 | FN-08 Tạo ghi chú | Integration | Đã đăng nhập tài khoản test | 1. Bấm "+" 2. Nhập tiêu đề 3. Quay lại | "Ghi chú tự động" | Ghi chú xuất hiện đầu danh sách Home | | | `note_crud_flow_test.dart` |

**Mẫu báo lỗi (Bug Report)**:

| Trường | Nội dung |
|---|---|
| Mã | BUG-01 |
| Tiêu đề | Ngắn gọn, nêu hiện tượng |
| Môi trường | Thiết bị, Android, phiên bản app, nhánh/commit |
| Các bước tái hiện | 1… 2… 3… |
| Kết quả mong đợi / thực tế | … |
| Mức nghiêm trọng / Ưu tiên | Critical/High/Medium/Low |
| Minh chứng | Ảnh, log, video |
| Phát hiện bởi | TC-AT-… / SEC-… / MUT-… |
| Trạng thái | Mới / Đã xác nhận / Đã sửa / Đã kiểm lại |

---

## PHẦN 5. TỰ KIỂM TRA & THUẬT NGỮ

### 5.1 Câu hỏi tự kiểm tra (tự trả lời được là đủ nền để bắt tay vào làm)

1. Kiểm thử tự động có phải là một kỹ thuật thiết kế test không? Nó liên quan thế nào tới hộp đen/hộp trắng?
2. Vì sao kim tự tháp kiểm thử đặt unit test ở đáy? "Cây kem ốc quế" là gì?
3. Phân biệt Stub, Mock và Fake. Trong test sinh trắc học của nhóm, `MockLocalAuthentication` thuộc loại nào?
4. Vì sao `pumpAndSettle()` có thể bị timeout trên màn hình Home của Smart Note?
5. `integration_test` không làm được điều gì mà Patrol làm được?
6. Phân biệt Load, Stress, Spike, Soak. Cho mỗi loại một ví dụ trong Smart Note.
7. Vì sao không được đo hiệu năng ở chế độ Debug?
8. Lỗ hổng "API secret nằm trong `.env` được đóng gói vào APK" thuộc mục nào của OWASP Mobile Top 10?
9. Coverage 100% có đảm bảo bộ test tốt không? Mutation Score trả lời câu hỏi gì mà coverage không trả lời được?
10. Mutant tương đương là gì, vì sao loại khỏi mẫu số khi tính Mutation Score?
11. Nêu 2 bất biến (property) có thể kiểm tra trên `Note.toMap()/fromMap()`.
12. Vì sao chạy `adb shell monkey` nên dùng seed cố định?

### 5.2 Bảng thuật ngữ Anh – Việt

| Tiếng Anh | Tiếng Việt |
|---|---|
| Test automation | Kiểm thử tự động |
| Regression testing | Kiểm thử hồi quy |
| Smoke testing | Kiểm thử khói (kiểm tra nhanh) |
| Test double / Mock / Stub / Fake | Đối tượng thay thế / giả lập |
| Flaky test | Test không ổn định |
| Traceability matrix | Ma trận truy vết |
| Continuous Integration (CI) | Tích hợp liên tục |
| Non-functional testing | Kiểm thử phi chức năng |
| Performance / Load / Stress / Soak testing | Kiểm thử hiệu năng / tải / áp lực / độ bền |
| Throughput / Latency / Jank | Thông lượng / Độ trễ / Giật khung hình |
| Security testing / Penetration testing | Kiểm thử bảo mật / xâm nhập |
| Threat modeling | Mô hình hóa mối đe dọa |
| Vulnerability | Lỗ hổng |
| Mutation testing / Mutant / Mutation score | Kiểm thử đột biến / Thể đột biến / Điểm đột biến |
| Property-based testing / Invariant | Kiểm thử dựa trên thuộc tính / Bất biến |
| Fuzz testing | Kiểm thử mờ (bơm dữ liệu ngẫu nhiên) |
| Fault injection / Chaos testing | Tiêm lỗi / Kiểm thử hỗn loạn |
| Accessibility (a11y) | Khả năng tiếp cận (trợ năng) |
| Compatibility testing | Kiểm thử tương thích |

### 5.3 Tài liệu tham khảo

1. ISTQB® Certified Tester Foundation Level Syllabus v4.0 (2023) – quy trình kiểm thử, cấp độ & loại kiểm thử.
2. Flutter Documentation – *Testing Flutter apps* (unit, widget, integration test): https://docs.flutter.dev/testing/overview
3. Flutter Documentation – *Performance profiling & DevTools*: https://docs.flutter.dev/perf
4. OWASP Mobile Application Security (MASVS, MASTG): https://mas.owasp.org/
5. OWASP Mobile Top 10 (2024): https://owasp.org/www-project-mobile-top-10/
6. Y. Jia, M. Harman, *An Analysis and Survey of the Development of Mutation Testing*, IEEE TSE, 2011.
7. M. Cohn, *Succeeding with Agile*, Addison-Wesley, 2009 – mô hình kim tự tháp kiểm thử.
8. Firebase Documentation – *Test Security Rules with the Emulator Suite*: https://firebase.google.com/docs/rules/unit-tests
9. Android Developers – *UI/Application Exerciser Monkey*: https://developer.android.com/studio/test/other-testing-tools/monkey
