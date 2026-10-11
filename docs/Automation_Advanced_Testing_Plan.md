# KẾ HOẠCH CHI TIẾT: KIỂM THỬ TỰ ĐỘNG (CHƯƠNG 5) & KIỂM THỬ NÂNG CAO (CHƯƠNG 6)
**Học phần**: Đánh giá & Kiểm định chất lượng phần mềm (CSE703010)
**Đề tài**: Smart Note App · **Nhánh làm việc**: `dung`
**Tài liệu lý thuyết đi kèm**: [Automation_Advanced_Testing_Theory.md](Automation_Advanced_Testing_Theory.md)
**Phạm vi Chương 6 (đã chốt)**: 6.1 Bảo mật · 6.2 Đột biến · 6.3 Hiệu năng
**Ngày lập**: 11/10/2026 · **Trạng thái**: Bản nháp – chờ chốt các quyết định ở Mục 2

---

## MỤC LỤC
1. [Kết quả khảo sát môi trường](#1-kết-quả-khảo-sát-môi-trường)
2. [Các quyết định cần chốt trước khi làm](#2-các-quyết-định-cần-chốt-trước-khi-làm)
3. [Lộ trình tổng thể](#3-lộ-trình-tổng-thể)
4. [Giai đoạn 0 – Chuẩn bị môi trường](#4-giai-đoạn-0--chuẩn-bị-môi-trường)
5. [Giai đoạn 1 – Kiểm thử tự động (Chương 5)](#5-giai-đoạn-1--kiểm-thử-tự-động-chương-5)
6. [Giai đoạn 2 – Kiểm thử bảo mật (Mục 6.1)](#6-giai-đoạn-2--kiểm-thử-bảo-mật-mục-61)
7. [Giai đoạn 3 – Kiểm thử đột biến (Mục 6.2)](#7-giai-đoạn-3--kiểm-thử-đột-biến-mục-62)
8. [Giai đoạn 4 – Kiểm thử hiệu năng (Mục 6.3)](#8-giai-đoạn-4--kiểm-thử-hiệu-năng-mục-63)
9. [Giai đoạn 5 – Hoàn thiện báo cáo](#9-giai-đoạn-5--hoàn-thiện-báo-cáo)
10. [Rủi ro & phương án dự phòng](#10-rủi-ro--phương-án-dự-phòng)
11. [Bảng theo dõi tiến độ](#11-bảng-theo-dõi-tiến-độ)

---

## 1. KẾT QUẢ KHẢO SÁT MÔI TRƯỜNG

| Hạng mục | Thực trạng | Ảnh hưởng |
|---|---|---|
| Máy tính | Intel i5-10300H (8 luồng), **RAM 15,8 GB** (lúc kiểm tra còn trống ~3,3 GB), ổ trống C: 89 GB / E: 106 GB | Đủ chạy máy ảo nếu **đóng bớt ứng dụng** (Chrome, Android Studio) |
| Flutter | 3.44.0 stable · Dart 3.12.0 | ✅ |
| Java | JDK 22 (hệ thống), Gradle dùng JDK 17 | ✅ Đủ cho Firebase Emulator |
| Android SDK | Có tại `C:\Users\DELL\AppData\Local\Android\sdk`; `adb`/`emulator` **chưa có trong PATH** | Cần thêm PATH |
| Máy ảo (AVD) | `Pixel_7` · Android 14 (API 34) · Google Play image · **RAM 2 GB** · tăng tốc WHPX hoạt động | ✅ Dùng được. Ảnh Google Play **không cho `adb root`** |
| Gradle | `-Xmx2048m`, `workers.max=2` | Đã ở mức tiết kiệm RAM |
| Node.js / npm / Docker | Có đủ | ✅ Dùng cho Rules test và MobSF |
| Firebase CLI | 15.19.0, đăng nhập `dunghvd79@gmail.com`. Tài khoản này không có quyền vào `smart-note-app-5727d` của nhóm | ✅ Đã giải quyết bằng **project riêng `smartnote-qa-dung`** (xem 1.1) |
| Tài khoản test | **Không tìm thấy** tài khoản/mật khẩu test nào trong repo (`lib/`, `test/`, `docs/`) | Tạo trên project riêng / Emulator (QĐ-1) |
| `android/app/google-services.json` | Ban đầu không có trên máy. **Đã sinh mới** từ project `smartnote-qa-dung` (file bị `.gitignore` bỏ qua, không commit) | ✅ |
| JDK cho Gradle | `android/gradle.properties` đặt `org.gradle.java.home=C:\Program Files\Java\jdk-17`, nhưng **máy không có JDK 17**, chỉ có JDK 22 (`C:\Program Files\Java\jdk-22`). Gradle 8.14 chạy được trên JDK 22 | ✅ Ghi đè bằng `C:\Users\DELL\.gradle\gradle.properties` trỏ tới JDK 22, **không sửa repo** |
| **Đường dẫn chứa ký tự tiếng Việt** | Repo nằm ở `E:\2026 Year\Kì_1_Năm_4\...`. Gradle Wrapper trên Windows báo `Could not find or load main class org.gradle.wrapper.GradleWrapperMain` khi đường dẫn có `ì`, `ă`. Đã xác minh: chạy từ đường dẫn không dấu thì Gradle 8.14 khởi động bình thường. Junction và `subst` **không khắc phục được**, vì Flutter/Dart tự giải về đường dẫn gốc | ❌ **Chặn build APK.** Cần chuyển repo sang đường dẫn chỉ gồm ký tự ASCII (bước 0.3) |
| `.env` | Có trên máy (4 khóa Cloudinary) | ✅ |
| Test hiện có | `test/unit/` (6 file, 83 test hộp trắng), `auth_provider_test`, `checklist_test`, `security_rules_test`, `widget_test` | Là nền cho Giai đoạn 3 |
| `coverage/lcov.info` hiện tại | File cũ: tổng chỉ **2,9 %**, không khớp số liệu Chương 4 | ✅ Đã chạy lại baseline (bước 0.2 – Mục 4.1) |
| Remote | `github.com/ttthu-huong/Smart-Note-App-QA` | CI chạy trên repo này (xem QĐ-3) |

### 1.1 Môi trường Firebase riêng cho môn học (tạo ngày 11/10/2026)

Theo yêu cầu "đổi cấu hình Firebase/API sang môi trường riêng, không dùng chung với dự án gốc":

| Hạng mục | Giá trị / trạng thái |
|---|---|
| Project | `smartnote-qa-dung` (Smart Note QA) · gói Spark (miễn phí) · chủ sở hữu `dunghvd79@gmail.com` |
| App Android | `com.example.smart_note_app` · App ID `1:251699552073:android:3b5742fde1f09e64840498` · đã gắn SHA-1 và SHA-256 của debug keystore |
| App Windows | `1:251699552073:web:6281d3856d5fa863840498` (giữ lại để `firebase_options.dart` có cấu hình Windows như bản gốc) |
| Cấu hình đã thay | `lib/firebase_options.dart`, `firebase.json` (thêm mục `firestore.rules`), `android/app/google-services.json` |
| Firestore | Database `(default)` · **asia-southeast1 (Singapore)** · đã deploy `firestore.rules` của repo |
| Authentication | ⬜ Cần bật trên Console: Email/Password, Google |
| Gemini (Firebase AI Logic) | **Không bật** (đã chốt). Các tính năng AI nằm **ngoài phạm vi** kiểm thử, và sẽ báo lỗi nếu bấm thử |
| Cloudinary | ⬜ Cần **tài khoản Cloudinary riêng** (miễn phí) và thay khóa trong `.env`. Dùng upload preset *unsigned*, để trống `CLOUDINARY_API_SECRET` |

---

## 2. CÁC QUYẾT ĐỊNH CẦN CHỐT TRƯỚC KHI LÀM

| Mã | Vấn đề | Đề xuất | Cần ai |
|---|---|---|---|
| **QĐ-1** | Tài khoản test & dữ liệu test | **Dùng Firebase Emulator Suite (Auth + Firestore) chạy trên máy**: tự tạo tài khoản test đã xác thực bằng script, không đụng dữ liệu thật, không cần quyền project. Chỉ thêm một tài khoản thật trên Firebase nếu cần chạy smoke test trên môi trường thật | Bạn |
| **QĐ-2** | Thiếu `google-services.json` | ✅ **Đã giải quyết**: tạo project riêng `smartnote-qa-dung` và sinh lại cấu hình (Mục 1.1) | – |
| **QĐ-3** | Có đưa CI (GitHub Actions) lên repo nhóm không? | Có, nhưng chỉ chạy **unit + widget test** (nhẹ, miễn phí). Integration test vẫn chạy trên máy cá nhân | Bạn ↔ nhóm |
| **QĐ-4** | Đột biến bắt buộc phải **sửa tạm** file trong `lib/` | Script tự **khôi phục bằng git sau mỗi mutant**, không commit mutant. Chỉ chạy khi working tree sạch | Bạn |
| **QĐ-5** | Phát hiện lộ API secret Cloudinary | Chỉ **chứng minh trích xuất được** (che giá trị trong báo cáo), **không gọi API** bằng secret đó. Báo nhóm **đổi (rotate) secret** sau khi báo cáo xong | Bạn ↔ nhóm |
| **QĐ-6** | Hiệu năng khi không có máy thật | **Không bịa số.** Đo thật theo 3 tầng (Mục 8.1) và ghi rõ môi trường đo. Được phép **ngoại suy có cơ sở** nếu ghi rõ đó là ước lượng | Đã chốt |
| **QĐ-7** | Hình thức báo cáo | Viết trước dưới dạng Markdown trong `docs/` (giống `Whitebox_Testing_Report.md`), sau đó chuyển sang file `.docx` của nhóm | Bạn |
| **QĐ-8** | Hạn nộp | Chưa biết → cần để xếp lịch ở Mục 11 | Bạn |

> **Trả lời câu hỏi "có dự đoán số liệu hiệu năng được không?"**
> Không nên ghi số "dự đoán" như thể đã đo trên điện thoại. Đó là số liệu không có thật: giảng viên hỏi lại cách đo là lộ ngay, và vi phạm liêm chính học thuật.
> Những gì **được phép và vẫn có giá trị**:
> 1. **Đo thật** ở môi trường đang có (máy tính, máy ảo) và ghi rõ môi trường.
> 2. **Ngoại suy có phương pháp**: ví dụ đo thời gian tìm kiếm ở 1k/5k/10k ghi chú, thấy tăng tuyến tính, từ đó *ước lượng* cho 50k ghi chú. Phải ghi rõ "ước lượng theo mô hình tuyến tính".
> 3. **So sánh tương đối** trên máy ảo (trước/sau, A so với B). Đây là cách làm hợp lệ dù số tuyệt đối không giống máy thật.

---

## 3. LỘ TRÌNH TỔNG THỂ

```
 GĐ0 Chuẩn bị ──▶ GĐ1 Tự động (Ch.5) ──▶ GĐ2 Bảo mật (6.1) ──▶ GĐ3 Đột biến (6.2) ──▶ GĐ4 Hiệu năng (6.3) ──▶ GĐ5 Báo cáo
   │                 │  1A Widget test (không cần máy ảo)        ▲                       ▲
   │                 │  1B Integration test (cần máy ảo + QĐ-2)  │ chạy song song được   │ dùng lại hạ tầng GĐ1
   └─ chờ QĐ-2 ──────┘                                           │ (không cần máy ảo)    │
```

**Nguyên tắc làm chung** (mỗi giai đoạn):
1. Mình soạn thiết kế (test case, kịch bản) → **bạn duyệt**.
2. Cùng cài đặt/chạy → thu **minh chứng** (log, ảnh, số liệu) vào `docs/images/<giai_doan>/`.
3. Viết luôn phần báo cáo tương ứng ngay sau khi có kết quả (không dồn cuối).
4. Mọi thay đổi chỉ nằm ở: `test/`, `integration_test/`, `tool/` (script), `docs/`, `pubspec.yaml` (dev_dependencies), `firebase.json` (emulators), `.github/`, cùng **thêm `Key` vào widget**. **Không sửa logic** trong `lib/`.

**Ước lượng công sức** (1 buổi ≈ 3–4 giờ):

| GĐ | Nội dung | Ước lượng | Phụ thuộc |
|---|---|---|---|
| 0 | Chuẩn bị môi trường | 1 buổi | QĐ-1, QĐ-2 |
| 1A | Widget test | 1–1,5 buổi | GĐ0 (một phần) |
| 1B | Integration test + CI | 2–3 buổi | QĐ-2, máy ảo |
| 2 | Bảo mật | 1,5–2 buổi | APK build (QĐ-2) cho phần APK; Rules test thì không cần |
| 3 | Đột biến | 1,5–2 buổi | Baseline test xanh |
| 4 | Hiệu năng | 1,5–2 buổi | Tầng 1 không phụ thuộc gì; Tầng 2 cần máy ảo |
| 5 | Báo cáo | 1–1,5 buổi | Tất cả |

---

## 4. GIAI ĐOẠN 0 – CHUẨN BỊ MÔI TRƯỜNG

| Bước | Việc làm | Cách kiểm tra hoàn thành |
|---|---|---|
| 0.1 | Thêm `platform-tools` và `emulator` của Android SDK vào PATH | `adb --version` chạy được |
| 0.2 | **Chạy lại baseline**: `flutter test --coverage` toàn bộ → lưu log + `lcov.info` mới | Biết chính xác số test pass và coverage thật. Dùng làm mốc cho GĐ3, đồng thời đối chiếu lại số liệu Chương 4 |
| 0.3 | Nhận `google-services.json` (QĐ-2) → `flutter build apk --debug` thử | Build thành công |
| 0.4 | Khởi động máy ảo tiết kiệm RAM: đóng Android Studio/Chrome; `emulator -avd Pixel_7 -no-boot-anim -no-snapshot-save` | Máy ảo lên, `adb devices` thấy thiết bị; theo dõi RAM bằng Task Manager |
| 0.5 | Cấu hình **Firebase Emulator Suite**: thêm mục `emulators` (auth: 9099, firestore: 8080, ui: 4000) vào `firebase.json` | `firebase emulators:start --only auth,firestore --project smart-note-app-5727d` chạy được |
| 0.6 | Thêm `dev_dependencies`: `integration_test` (SDK), `sqflite_common_ffi` (SQLite thật trên PC cho test hiệu năng) | `flutter pub get` thành công, 83 test cũ vẫn xanh |
| 0.7 | Viết script tạo **tài khoản test đã xác thực** trên Auth Emulator (gọi REST API của emulator) | Có tài khoản `qa.tester@smartnote.test` dùng được |

**Đầu ra**: Mục "Môi trường kiểm thử" dùng chung cho Ch.5 và Ch.6 (cấu hình máy, phiên bản công cụ, sơ đồ môi trường).

### 4.1 Kết quả baseline (bước 0.2 – chạy ngày 11/10/2026, cấu hình Firebase mới)

Lệnh: `flutter test --coverage` (toàn bộ thư mục `test/`) → **119/119 PASS**, tổng thời gian khoảng 48 giây (gồm biên dịch).

| File test | Số test |
|---|---|
| `test/unit/auth_whitebox_test.dart` | 21 |
| `test/unit/biometric_whitebox_test.dart` | 13 |
| `test/unit/note_crud_whitebox_test.dart` | 10 |
| `test/unit/search_whitebox_test.dart` | 14 |
| `test/unit/sync_whitebox_test.dart` | 11 |
| `test/unit/trash_whitebox_test.dart` | 14 |
| *Cộng hộp trắng (Ch.4)* | ***83*** |
| `test/auth_provider_test.dart` · `checklist_test.dart` · `security_rules_test.dart` · `widget_test.dart` | 15 · 5 · 15 · 1 |

Độ bao phủ dòng lệnh **theo file** (chỉ tính các file được test chạm tới):

| File | Dòng chạy / tổng | % |
|---|---|---|
| `services/biometric_service.dart` | 26/26 | 100 % |
| `widgets/empty_state.dart` | 44/44 | 100 % |
| `models/checklist_item.dart` | 10/14 | 71,4 % |
| `repositories/sync_repository.dart` | 56/85 | 65,9 % |
| `providers/auth_provider.dart` | 84/143 | 58,7 % |
| `models/note_model.dart` | 66/124 | 53,2 % |
| `services/local_note_service.dart` | 58/159 | 36,5 % |
| `repositories/note_repository.dart` | 20/61 | 32,8 % |
| `providers/note_provider.dart` | 118/461 | 25,6 % |
| **Tổng 31 file được nạp** | **491/4.018** | **12,2 %** |

> ⚠️ **Lưu ý cho Chương 4**: con số 92,51 % trong báo cáo hộp trắng chỉ đúng nếu tính **trên các hàm mục tiêu**, không phải toàn file hay toàn dự án. Báo cáo nên ghi rõ phạm vi đo để không bị hiểu nhầm. Ngoài ra, `flutter test --coverage` mặc định chỉ đo **dòng lệnh**, không đo nhánh. Muốn có số liệu nhánh thật thì phải chạy thêm `--branch-coverage`.

---

## 5. GIAI ĐOẠN 1 – KIỂM THỬ TỰ ĐỘNG (CHƯƠNG 5)

### 5.1 Mục tiêu & tiêu chí hoàn thành
- Tự động hóa các **luồng nghiệp vụ chính** để chạy hồi quy nhanh.
- **Tiêu chí hoàn thành**: ≥ 25 test case tự động (widget + integration); 100 % script truy vết được về chức năng (FN); mỗi suite chạy 3 lần liên tiếp không có test flaky; có số liệu so sánh **thời gian chạy tự động vs thời gian chạy tay** (đo tay thật một lần bằng đồng hồ).

### 5.2 Chọn phạm vi tự động (bước 1 của quy trình)

Chấm điểm 1–3 theo: **T**ần suất hồi quy · **R**ủi ro · **Ổ**n định UI · **K**hả thi kỹ thuật. Tự động hóa khi tổng ≥ 9.

| Chức năng | T | R | Ổ | K | Tổng | Quyết định | Cấp |
|---|---|---|---|---|---|---|---|
| Đăng ký / Đăng nhập Email (FN-02, FN-04) | 3 | 3 | 3 | 3 | 12 | ✅ Tự động | Widget + Integration |
| Kiểm tra form đăng nhập (email/mật khẩu sai) | 3 | 2 | 3 | 3 | 11 | ✅ | Widget |
| Tạo / sửa / ghim ghi chú (FN-08, FN-09) | 3 | 3 | 2 | 3 | 11 | ✅ | Integration |
| Thùng rác: xóa mềm – khôi phục – xóa vĩnh viễn (FN-10–12) | 3 | 3 | 3 | 3 | 12 | ✅ | Integration |
| Lưu trữ (Archive) | 2 | 2 | 3 | 3 | 10 | ✅ | Integration |
| Tìm kiếm từ khóa + cú pháp `has:` / `is:` / `label:` (FN-23) | 3 | 2 | 3 | 3 | 11 | ✅ | Integration |
| Quản lý nhãn | 2 | 2 | 3 | 3 | 10 | ✅ | Integration |
| Checklist trong editor | 2 | 2 | 2 | 3 | 9 | ✅ | Widget |
| Cài đặt: chế độ tối, đổi ngôn ngữ | 2 | 1 | 3 | 3 | 9 | ✅ | Integration |
| Đồng bộ Offline → Online (FN-40, FN-41) | 3 | 3 | 2 | 1 | 9 | ⚠️ **Bán tự động**: script chạy app + lệnh `adb` bật/tắt mạng từ máy tính, kiểm tra kết quả trên Firestore Emulator | Integration |
| Đăng nhập Google | 2 | 3 | 2 | 1 | 8 | ❌ Hộp thoại native, cần tài khoản Google thật | Thủ công |
| Khóa sinh trắc học (FN-29, FN-30) | 2 | 3 | 2 | 1 | 8 | ❌ Hộp thoại vân tay native (logic đã có unit test ở Ch.4) | Thủ công |
| Gemini AI | 1 | 2 | 2 | 1 | 6 | ❌ Kết quả không tất định, tốn hạn mức | Thủ công |
| Ghi âm, camera, vẽ tay, xuất PDF, nhắc nhở | 1 | 2 | 2 | 1 | 6 | ❌ Phụ thuộc phần cứng/hộp thoại hệ thống | Thủ công |

> Bảng này cùng lý do loại trừ sẽ đưa nguyên vào **báo cáo mục 5.2**.

### 5.3 Danh sách test case dự kiến

**1A – Widget test** (`test/widget/`, chạy trên PC, không cần máy ảo):

| Mã | Nội dung |
|---|---|
| TC-AT-AUTH-01…05 | Form đăng nhập: email rỗng, email sai định dạng, mật khẩu rỗng, mật khẩu < 6 ký tự, dữ liệu hợp lệ thì nút bấm hoạt động (data-driven) |
| TC-AT-UI-01…03 | `EmptyState` hiển thị đúng nội dung; `NoteCard` hiển thị tiêu đề, biểu tượng ghim và khóa; ghi chú bị khóa **không lộ nội dung** trên thẻ |
| TC-AT-CHK-01…03 | Checklist: thêm mục, đánh dấu hoàn thành, xóa mục |
| TC-AT-SORT-01…02 | Bảng sắp xếp: chọn tiêu chí thì callback trả đúng giá trị |

**1B – Integration test** (`integration_test/flows/`, máy ảo + Firebase Emulator):

| Mã | Luồng |
|---|---|
| TC-AT-AUTH-10…12 | Đăng ký → màn hình xác thực email; đăng nhập tài khoản đã xác thực → Home; đăng xuất → Login |
| TC-AT-NOTE-01…05 | Tạo ghi chú; sửa tiêu đề/nội dung; ghim lên đầu; đổi màu; lưu trữ |
| TC-AT-TRASH-01…04 | Xóa mềm; khôi phục; xóa vĩnh viễn; xóa hàng loạt |
| TC-AT-SEARCH-01…05 | Tìm theo từ khóa (không phân biệt hoa/thường); `is:pinned`; `is:archived`; `label:"..."`; không tìm thấy ghi chú trong thùng rác |
| TC-AT-LABEL-01…02 | Tạo nhãn; gán nhãn rồi lọc theo nhãn |
| TC-AT-SET-01…02 | Bật chế độ tối; đổi ngôn ngữ sang English, khởi động lại vẫn giữ cài đặt |
| TC-AT-SYNC-01…02 | (bán tự động) Tạo ghi chú khi offline → bật mạng → có document trên Firestore Emulator; xóa khi offline → bật mạng → document bị xóa |

### 5.4 Thiết kế framework

```text
test/
 ┣ unit/                      # ✅ có sẵn (Ch.4)
 ┣ widget/                    # 1A
 ┗ helpers/                   # fake provider, dữ liệu mẫu
integration_test/
 ┣ app_harness.dart           # khởi tạo Firebase → trỏ sang Emulator → chạy app
 ┣ robots/                    # login_robot, home_robot, editor_robot, trash_robot, search_robot
 ┣ flows/                     # *_flow_test.dart (mỗi nhóm chức năng 1 file)
 ┗ test_data/                 # tài khoản, nội dung mẫu
tool/
 ┣ seed_emulator_user.(ps1|js)  # tạo tài khoản test đã xác thực
 ┗ run_integration.ps1        # bật emulator → chạy test → gom log
```

- **Trỏ app sang Emulator mà không sửa `main.dart`**: `app_harness.dart` gọi `Firebase.initializeApp`, sau đó `useAuthEmulator('10.0.2.2', 9099)` và `useFirestoreEmulator('10.0.2.2', 8080)`, rồi mới chạy giao diện app. *(Cần thử ngay ở bước đầu 1B. Nếu `main()` khởi tạo lại gây xung đột thì phương án dự phòng là dựng `MyApp()` trực tiếp.)*
- **Thêm `Key`** cho các widget cần thao tác (danh sách chốt khi viết robot): ô email/mật khẩu, nút đăng nhập, nút "+", ô tiêu đề/nội dung editor, ô tìm kiếm, mục trong drawer, nút trong thùng rác. Chỉ thêm `key:`, **không đổi hành vi**.
- **Cố định locale** `vi` khi test để `find.text` không vỡ.
- **Dọn dữ liệu**: xóa dữ liệu Emulator giữa các suite (`DELETE` endpoint của Firestore Emulator) để test không phụ thuộc thứ tự.

### 5.5 CI (nếu QĐ-3 đồng ý)
`.github/workflows/flutter-tests.yml`: checkout → Flutter stable → `cp .env.example .env` → `pub get` → `analyze` → `flutter test test/unit test/widget --coverage` → upload `lcov.info`. **Minh chứng**: ảnh chụp tab Actions báo xanh.

### 5.6 Đầu ra cho báo cáo Chương 5
5.1 Cơ sở lý thuyết (tóm từ tài liệu lý thuyết) · 5.2 Kế hoạch, phạm vi, lựa chọn công cụ (bảng 5.2 + so sánh công cụ) · 5.3 Thiết kế framework, ma trận truy vết · 5.4 Kết quả thực thi (bảng TC, log, ảnh, CI) · 5.5 Đánh giá (tỷ lệ tự động, pass rate, flaky, thời gian tự động vs tay, lỗi phát hiện, hạn chế).

---

## 6. GIAI ĐOẠN 2 – KIỂM THỬ BẢO MẬT (MỤC 6.1)

### 6.1 Quy tắc thực hiện
Chỉ kiểm thử trên **APK do nhóm build**, **Firebase Emulator** và **máy ảo của mình**. **Không** tấn công project Firebase hay tài khoản Cloudinary thật, và **không** dùng secret trích xuất được để gọi API (QĐ-5).

### 6.2 Các bước & kịch bản

| Bước | Hoạt động | Kịch bản (SEC-xx) | Chuẩn tham chiếu |
|---|---|---|---|
| 1 | Phạm vi & mô hình đe dọa: vẽ sơ đồ luồng dữ liệu App ↔ SQLite ↔ Firestore ↔ Cloudinary ↔ Gemini, áp dụng STRIDE | – | STRIDE |
| 2 | **Phân tích tĩnh (SAST)** mã nguồn & cấu hình | SEC-01 Tìm bí mật hardcode / trong asset · SEC-02 Log in ra thông tin cấu hình (`debugPrint` trong `main.dart` vẫn chạy ở bản release) · SEC-03 Rà quyền trong `AndroidManifest.xml` (`allowBackup`, quyền thừa) | M1, M6, M8 |
| 3 | **Phân tích APK**: build release → giải nén → xem `assets/flutter_assets/` · quét **MobSF** (chạy bằng Docker) | SEC-04 Trích xuất được `.env` (Cloudinary API secret) từ APK · SEC-05 Báo cáo MobSF (điểm bảo mật, phát hiện nổi bật) | M1, M7 |
| 4 | **Kiểm thử Firestore Security Rules thật** bằng Emulator + `@firebase/rules-unit-testing` (Node.js) | SEC-06 Chưa đăng nhập thì không đọc được · SEC-07 User A không đọc/sửa/xóa được note của user B · SEC-08 Tạo note với `user_id` của người khác bị chặn · SEC-09 Chủ sở hữu CRUD được note của mình · SEC-10 tags/media bị cô lập theo user | M3 |
| 5 | **Lưu trữ dữ liệu trên máy**: `adb shell run-as com.example.smart_note_app` → sao chép `smart_note.db` → mở xem | SEC-11 Ghi chú (kể cả ghi chú **đã khóa**) có lưu dạng rõ không · SEC-12 Khóa sinh trắc học chỉ là "ẩn trên giao diện" hay có mã hóa | M9, M10 |
| 6 | **Khóa sinh trắc học có bị lộ qua đường khác** | SEC-13 Nội dung note khóa có hiện trong kết quả tìm kiếm, nội dung thông báo nhắc nhở, khi xuất PDF không | M3, M6 |
| 7 | **Truyền thông**: kiểm tra mọi endpoint dùng HTTPS, không bật cleartext | SEC-14 | M5 |
| 8 | Đánh giá mức độ (Critical/High/Medium/Low) + đề xuất khắc phục | Bảng Security Findings | CVSS (tham khảo) |

> **Ghi chú về test cũ**: `test/security_rules_test.dart` hiện chỉ **viết lại logic Rules bằng Dart** chứ không chạy Rules thật. Bước 4 thay thế bằng test chạy trên Emulator, và nhận xét này đưa vào báo cáo như một điểm cải tiến.

### 6.3 Đầu ra
Sơ đồ luồng dữ liệu + bảng STRIDE · bảng SEC-01…14 (bước, kết quả, minh chứng) · **Bảng Security Findings** (mã, mô tả, mức độ, tác động, đề xuất) · ảnh MobSF, ảnh terminal Rules test.

---

## 7. GIAI ĐOẠN 3 – KIỂM THỬ ĐỘT BIẾN (MỤC 6.2)

### 7.1 Mục tiêu
Đo **khả năng phát hiện lỗi thật** của 83 test hộp trắng (Chương 4). Đây là điều coverage không chứng minh được. Sau đó **bổ sung test** để tăng Mutation Score.

### 7.2 Các bước

| Bước | Việc làm | Đầu ra |
|---|---|---|
| 1 | Baseline: `flutter test test/unit/` xanh 100 % (từ bước 0.2) | Log baseline |
| 2 | Chọn hàm mục tiêu = các hàm đã kiểm thử ở Ch.4 (biometric, auth, note CRUD, trash, search, sync) | Danh sách hàm |
| 3 | Thử công cụ `mutation_test` (pub.dev) trên **1 file**. Nếu không hợp với Flutter thì chuyển sang **đột biến thủ công có script** | Quyết định công cụ |
| 4 | Sinh **~8–10 mutant/module (~50–60 mutant)** theo các toán tử ROR, LCR, NEG, SDL, CRP, RVR (xem lý thuyết 3.3), mã `MUT-[MODULE]-[STT]` | Bảng mutant (file:dòng, code gốc → code đột biến) |
| 5 | Script `tool/run_mutants.ps1`: với mỗi mutant thì áp patch → chạy test của module → ghi Killed/Survived/Timeout → `git checkout -- <file>` khôi phục | `mutation_results.csv` + log |
| 6 | Phân tích mutant sống sót: tương đương hay thiếu assert/thiếu ca biên? | Bảng phân tích |
| 7 | Viết test bổ sung (chỉ trong `test/unit/`) → chạy lại → tính **Mutation Score trước/sau** | Bảng so sánh + biểu đồ theo module |

**Tiêu chí**: Mutation Score sau cải thiện ≥ 80 % (mục tiêu tham khảo); mọi mutant sống sót đều được giải thích.

**An toàn (QĐ-4)**: chỉ chạy khi `git status` sạch; script luôn khôi phục kể cả khi bị lỗi giữa chừng; cuối cùng kiểm tra `git diff lib/` rỗng.

---

## 8. GIAI ĐOẠN 4 – KIỂM THỬ HIỆU NĂNG (MỤC 6.3)

### 8.1 Chiến lược 3 tầng khi không có máy thật

| Tầng | Môi trường | Đo gì | Độ tin cậy | Ghi trong báo cáo |
|---|---|---|---|---|
| **T1 – Tầng dữ liệu** (chính) | PC, `flutter test` + `sqflite_common_ffi` (SQLite **thật**) + `LocalNoteService(customDb: ...)` | Thời gian truy vấn/ghi theo khối lượng dữ liệu | **Cao** cho xu hướng & so sánh. Số tuyệt đối là của PC | "Đo trên PC i5-10300H/16 GB" |
| **T2 – Ứng dụng** | Máy ảo Pixel_7 (API 34, RAM 2 GB) | Thời gian khởi động, tỷ lệ frame giật, bộ nhớ, rò rỉ bộ nhớ khi dùng lâu | **Tương đối**, chỉ để so sánh và xem xu hướng | "Số liệu trên máy ảo, mang tính tương đối" |
| **T3 – Không phụ thuộc thiết bị** | Build | Kích thước APK theo thành phần | **Tuyệt đối** | `flutter build apk --analyze-size` |
| *(Tùy chọn)* T4 | Firebase Test Lab, thiết bị thật trên đám mây (hạn mức miễn phí giới hạn) | Khởi động, CPU, bộ nhớ, FPS trên máy thật | Cao | Chỉ làm nếu còn thời gian và có project Firebase dùng được |

### 8.2 Kịch bản đo (PERF-xx) & tiêu chí đặt trước

| Mã | Tầng | Kịch bản | Mức tải | Tiêu chí đạt (đặt **trước** khi đo) |
|---|---|---|---|---|
| PERF-01 | T1 | Ghi `insertNote` hàng loạt | 100 / 1.000 / 5.000 / 10.000 | Thời gian ghi trung bình mỗi note không tăng theo N |
| PERF-02 | T1 | `getAllNotes` phân trang (trang đầu) | DB 1k / 5k / 10k | Trang đầu < 50 ms (PC) và **không phụ thuộc** tổng số note |
| PERF-03 | T1 | `searchNotes` (LIKE) – Volume/Stress | DB 1k / 5k / 10k / 20k | < 300 ms ở 5k; xác định điểm vượt ngưỡng |
| PERF-04 | T1 | So sánh có / không có index `(user_id, status)` | DB 10k | Chứng minh index giúp nhanh hơn (số lần) |
| PERF-05 | T1 | Logic `syncNow` với Firestore giả (mock), Spike | 100 / 500 / 2.000 note chưa đồng bộ | Thời gian tăng gần tuyến tính, không bùng nổ |
| PERF-06 | T1 | Phân tích nội dung ghi chú lớn (Delta JSON / checklist) | 10 KB / 100 KB / 1 MB | Không lỗi; ghi nhận thời gian |
| PERF-07 | T2 | Khởi động lạnh: `adb shell am start -W` (TotalTime) | 10 lần, lấy trung vị | Ghi nhận + so sánh khi DB rỗng và DB 1k note |
| PERF-08 | T2 | Cuộn Home: `dumpsys gfxinfo` (% frame giật) | DB 1k note | Ghi nhận tương đối |
| PERF-09 | T2 | Soak: mở/đóng editor 100 lần, `dumpsys meminfo` mỗi 10 lần | – | Bộ nhớ không tăng liên tục (không rò rỉ) |
| PERF-10 | T3 | Kích thước APK theo thành phần | – | Ghi nhận 5 thành phần lớn nhất |

**Phương pháp đo**: mỗi phép đo chạy **khởi động nóng (warm-up) 1 lần + 5 lần đo**, báo cáo trung vị và min–max. Ghi cấu hình máy, các ứng dụng đang chạy. Kết quả xuất ra CSV, sau đó vẽ biểu đồ.
**Ngoại suy** (nếu dùng): chỉ áp dụng cho T1, nêu rõ mô hình (ví dụ hồi quy tuyến tính) và gắn nhãn "ước lượng".

### 8.3 Đầu ra
Bảng tiêu chí và kết quả PERF-01…10 · biểu đồ thời gian theo khối lượng dữ liệu · phân tích nút thắt (ví dụ `LIKE '%…%'` không dùng được index → đề xuất FTS5, đúng như README đang ghi nhầm) · đề xuất tối ưu · nêu rõ giới hạn của môi trường đo.

---

## 9. GIAI ĐOẠN 5 – HOÀN THIỆN BÁO CÁO

| File (trong `docs/`) | Nội dung | Ánh xạ vào `.docx` |
|---|---|---|
| `Automation_Testing_Report.md` | Chương 5 đầy đủ | Chương 5 |
| `Advanced_Testing_Report.md` | 6.1 Bảo mật · 6.2 Đột biến · 6.3 Hiệu năng | Chương 6 |
| (bổ sung) | Lỗi phát hiện được từ Ch.5 và Ch.6 | Mục 7.2 "Các lỗi phát hiện được" |
| (bổ sung) | Đánh giá hiệu quả bộ test (pass rate, Mutation Score, tỷ lệ tự động) | Mục 7.1 |
| `docs/images/automation/`, `docs/images/advanced/` | Ảnh minh chứng | Hình trong báo cáo |

Mỗi mục đều có cấu trúc **Cơ sở lý thuyết → Kế hoạch/Thiết kế → Thực thi → Kết quả → Đánh giá**, đồng bộ với Chương 4.

---

## 10. RỦI RO & PHƯƠNG ÁN DỰ PHÒNG

| Rủi ro | Khả năng | Phương án |
|---|---|---|
| Không lấy được `google-services.json` | Trung bình | Làm trước các phần **không cần build Android**: 1A, Rules test (SEC-06…10), SAST, GĐ3, PERF-01…06. Phần APK/máy ảo làm sau |
| Máy ảo thiếu RAM / chậm | Trung bình | Đóng ứng dụng khác; chạy test theo từng file; giảm số kịch bản T2; dùng T4 (Test Lab) nếu cần |
| App không trỏ được sang Emulator nếu không sửa `main.dart` | Thấp – TB | Dựng `MyApp()` trực tiếp trong harness; nếu vẫn không được, xin phép thêm 1 cờ cấu hình nhỏ (`--dart-define=USE_EMULATOR=true`) |
| `mutation_test` không chạy được với Flutter | Trung bình | Dùng script đột biến thủ công (đã có trong kế hoạch) |
| Test flaky do animation/Shimmer | Cao | Dùng `pump(Duration)`, chờ có điều kiện, Robot pattern |
| Rules thật khác với file `firestore.rules` trong repo | Thấp | Ghi rõ là đã kiểm thử file `firestore.rules` trong repo; đề nghị nhóm xác nhận đã deploy đúng file đó |

---

## 11. BẢNG THEO DÕI TIẾN ĐỘ

| # | Hạng mục | Trạng thái | Ghi chú |
|---|---|---|---|
| 0.1–0.7 | Chuẩn bị môi trường | ⬜ | Chờ QĐ-1, QĐ-2 |
| 1A | Widget test (~13 TC) | ⬜ | |
| 1B | Integration test (~22 TC) + CI | ⬜ | Cần máy ảo + `google-services.json` |
| 2 | Bảo mật SEC-01…14 | ⬜ | |
| 3 | Đột biến ~50–60 mutant | ⬜ | |
| 4 | Hiệu năng PERF-01…10 | ⬜ | |
| 5 | Báo cáo Ch.5, Ch.6, mục 7.1–7.2 | ⬜ | |

*Ký hiệu: ⬜ chưa làm · 🟡 đang làm · ✅ xong*
