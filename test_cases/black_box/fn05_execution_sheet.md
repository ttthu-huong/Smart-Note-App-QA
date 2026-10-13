# BLACK-BOX TEST EXECUTION SHEET — CHỨC NĂNG FN-05
## Dự án: Smart Note App
**Chức năng:** Đăng nhập nhanh Google (Google Sign-In) (FN-05)  
**Tiêu chuẩn áp dụng:** IEEE 829 & ISTQB Manual Test Execution  
**Tài liệu tham chiếu:** `black_box_test_cases.md`  
**Mục tiêu:** Cung cấp biểu mẫu thực thi kiểm thử thủ công chức năng đăng nhập tài khoản Google cho Tester.

---

## 1. THÔNG TIN KIỂM THỬ

| Trường thông tin | Giá trị / Trạng thái thực tế |
|---|---|
| **FN-ID** | **FN-05** |
| **Chức năng** | **Đăng nhập nhanh Google (Google Sign-In)** |
| **Người kiểm thử (Tester)** | QA Tester (Manual Execution on Real Device) |
| **Ngày kiểm thử (Execution Date)** | 05/10/2026 |
| **Thiết bị kiểm thử (Device/Model)** | Samsung Galaxy S21 FE 5G (SM-G990E / R5CW82ECF6M) |
| **Android Version** | Android 14 (API 34) |
| **App Version / Build Number** | v1.0.0 (Release Build) |
| **Kết nối mạng** | Wi-Fi & Chế độ Offline mô phỏng |
| **Ghi chú môi trường khác** | Google Play Services có sẵn các tài khoản Google thử nghiệm |

---

## 2. ĐIỀU KIỆN TRƯỚC KHI KIỂM THỬ (PRECONDITIONS)

1. **Trạng thái ứng dụng:** Đang ở màn hình Đăng nhập (chưa đăng nhập tài khoản nào).
2. **Tài khoản Google trên thiết bị:**
   - Tài khoản Google đã có dữ liệu (Returning User): `ht158713@gmail.com`
   - Tài khoản Google hoàn toàn mới chưa từng sử dụng app (New User): `nopitran3@gmail.com`
3. **Kết nối mạng Internet:** Thiết bị có kết nối mạng Internet hoạt động ổn định (trừ kịch bản kiểm tra ngoại lệ Offline tại TC-BB-011B).

---

## 3. BẢNG THỰC THI KIỂM THỬ (TEST EXECUTION MATRIX)

| STT | TC ID | Data ID | Phân loại | Test Data | Các bước thực hiện | Expected Result (Observable UI) | Actual Result | Trạng thái | Evidence ID | Bug ID / Ghi chú |
|:---:|:---|:---:|:---:|:---|:---|:---|:---|:---:|:---|:---:|
| **1** | **TC-BB-010** | **D01** | Đã có | Chọn tài khoản Google hiển thị trên hộp thoại (`ht158713@gmail.com`) | 1. Nhấn nút "Đăng nhập bằng Google".<br>2. Trên hộp thoại hệ thống xuất hiện, chạm chọn tài khoản Google.<br>3. Quan sát quá trình chuyển tiếp màn hình. | Hộp thoại chọn tài khoản đóng lại; ứng dụng hiển thị màn hình chờ đồng bộ dữ liệu với biểu tượng xoay, sau đó chuyển thẳng vào màn hình Trang chủ ghi chú. | Hộp thoại Google xuất hiện. Chạm chọn tài khoản `ht158713@gmail.com`, hộp thoại đóng lại; ứng dụng qua màn hình đồng bộ và chuyển thẳng vào Trang chủ ghi chú (`HomeScreen`). | **PASS** | `FN05_TC-BB-010_D01_01.png`<br>`FN05_TC-BB-010_D01_02.png` | Requirement-based (Happy Path) |
| **2** | **TC-BB-011** | **D01** | Đã có | Nhấn phím Back hệ thống khi hộp thoại Account Picker hiện lên | 1. Nhấn nút "Đăng nhập bằng Google".<br>2. Khi hộp thoại danh sách tài khoản Google hiện lên, nhấn phím Back trên thiết bị (hoặc nút Hủy nếu có). | Hộp thoại chọn tài khoản đóng lại ngay lập tức; ứng dụng vẫn giữ nguyên tại màn hình Đăng nhập ổn định, không bị văng/đóng ứng dụng, không xuất hiện thông báo lỗi bất thường. | Hộp thoại Google xuất hiện, nhấn phím Back hệ thống: Hộp thoại đóng lại ngay lập tức; ứng dụng giữ nguyên trạng thái tại màn hình Đăng nhập ổn định, không crash, không xuất hiện thông báo lỗi. | **PASS** | `FN05_TC-BB-011_D01_01.png` | Requirement-derived (Thao tác hủy) |
| **3** | **TC-BB-011B** | **D01** | Bổ sung | Thiết bị ở chế độ ngắt toàn bộ kết nối mạng (Tắt Wi-Fi + 4G) | 1. Tắt toàn bộ kết nối mạng trên thiết bị.<br>2. Đang ở tab Đăng nhập, nhấn nút "Đăng nhập bằng Google". | Ứng dụng không bật hộp thoại chọn tài khoản Google; hiển thị thông báo lỗi chữ màu đỏ nổi bật trên màn hình: *"Không có kết nối mạng. Vui lòng kiểm tra lại."*, form đăng nhập giữ nguyên. | Không mở hộp thoại Google Account Picker; form giữ nguyên và hiển thị thông báo lỗi màu đỏ rõ ràng: *"Không có kết nối mạng. Vui lòng kiểm tra lại."* | **PASS** | `FN05_TC-BB-011B_D01_01.png` | Code-inferred / As-built (Offline Handling) |
| **4** | **TC-BB-011C** | **D01** | Bổ sung | Tài khoản Google `ht158713@gmail.com` đã đăng nhập thành công | 1. Từ Trang chủ, chạm vào biểu tượng đại diện người dùng.<br>2. Chọn Quản lý tài khoản và quan sát thông tin hồ sơ. | Hiển thị chính xác Tên người dùng và Ảnh đại diện tương ứng từ tài khoản Google; ảnh tải rõ ràng không bị vỡ/lỗi; hiển thị đúng địa chỉ Gmail của tài khoản. | Tại ProfileDrawer của ứng dụng, hiển thị chính xác Tên tài khoản Google ("Thu Hường"), địa chỉ Gmail ("ht158713@gmail.com") và Avatar người dùng. Khi vào màn hình Hồ sơ tài khoản (ProfileScreen), thông tin người dùng được hiển thị đầy đủ, đồng bộ và rõ ràng. | **PASS** | `FN05_TC-BB-011C_D01_01.png`<br>`FN05_TC-BB-011C_D01_02.png` | Code-inferred / As-built (Post-login Profile Verification) |
| **5** | **TC-BB-011D** | **D01** | Bổ sung | Đóng hoàn toàn tiến trình ứng dụng (force-stop) sau khi đăng nhập | 1. Đóng hoàn toàn ứng dụng (vuốt tắt khỏi danh sách ứng dụng gần đây).<br>2. Chạm vào biểu tượng để mở lại ứng dụng.<br>3. Quan sát quá trình khởi động. | Sau màn hình khởi động (Splash Screen), ứng dụng tự động điều hướng thẳng vào màn hình Trang chủ ghi chú, người dùng không phải thực hiện đăng nhập lại. | Sau khi force-stop và khởi động lại, ứng dụng hiển thị màn hình Splash và tự động điều hướng thẳng vào Trang chủ ghi chú, không bắt đăng nhập lại. | **PASS** | `FN05_TC-BB-011D_D01_01.png`<br>`FN05_TC-BB-011D_D01_02.png` | Requirement-based (Session Persistence) |
| **6** | **TC-BB-011E** | **D01** | Bổ sung | Thực hiện Đăng xuất rồi nhấn Đăng nhập bằng Google lại | 1. Mở menu $\rightarrow$ chọn mục Đăng xuất $\rightarrow$ nhấn Xác nhận đăng xuất.<br>2. Kiểm tra màn hình quay về Đăng nhập.<br>3. Nhấn lại nút "Đăng nhập bằng Google" và chọn tài khoản. | Sau bước 1: Ứng dụng đưa người dùng về màn hình Đăng nhập sạch sẽ.<br>Sau bước 3: Đăng nhập lại thành công, qua màn hình chờ đồng bộ và vào lại Trang chủ bình thường. | Bấm Đăng xuất $\rightarrow$ xác nhận dialog: Ứng dụng về màn hình Đăng nhập an toàn. Nhấn lại Đăng nhập bằng Google và chọn tài khoản $\rightarrow$ sync thành công vào lại Trang chủ. | **PASS** | `FN05_TC-BB-011E_D01_01.png`<br>`FN05_TC-BB-011E_D01_02.png` | Code-inferred / As-built (Lifecycle / Re-login) |
| **7** | **TC-BB-011F** | **D01** | Bổ sung | Tài khoản Google mới chưa từng dùng app (`nopitran3@gmail.com`) | 1. Nhấn nút "Đăng nhập bằng Google".<br>2. Chọn tài khoản Google mới (`nopitran3@gmail.com`).<br>3. Quan sát màn hình Trang chủ sau khi sync. | Đăng nhập thành công vào Trang chủ; giao diện hiển thị trạng thái danh sách trống với thông báo *"Chưa có ghi chú nào"* kèm hướng dẫn nhấn nút (+) để tạo ghi chú đầu tiên. | Đăng nhập thành công với tài khoản Google mới chưa từng sử dụng app; sau khi sync, màn hình Trang chủ hiển thị trạng thái trống ban đầu: *"Chưa có ghi chú nào"* và *"Nhấn + để tạo ghi chú đầu tiên"*. | **PASS** | `FN05_TC-BB-011F_D01_01.png` | Requirement-derived (New User Onboarding) |
| **8** | **TC-BB-011G** | **D01** | Bổ sung | Tài khoản Google đã có sẵn ghi chú trên hệ thống (`ht158713@gmail.com`) | 1. Mở ứng dụng, tại tab Đăng nhập nhấn "Đăng nhập bằng Google".<br>2. Chọn tài khoản Google cũ (`ht158713@gmail.com`).<br>3. Quan sát danh sách trên Trang chủ sau khi sync. | Đăng nhập thành công; sau màn hình đồng bộ, toàn bộ danh sách ghi chú đã tạo trước đây được khôi phục và hiển thị đầy đủ trên màn hình Trang chủ, không bị mất dữ liệu. | Đăng nhập thành công tài khoản Google cũ; sau khi đồng bộ, toàn bộ các ghi chú đã tạo trước đó ("Ghi chú offline", "Ghi chú off demo", "🔒 Ghi chú đã khóa", "Kế hoạch") đều hiển thị đầy đủ trên Trang chủ. | **PASS** | `FN05_TC-BB-011G_D01_01.png` | Requirement-based (Returning User Data Restoration) |

---

## 4. QUY TẮC ĐẶT TÊN BẰNG CHỨNG KIỂM THỬ (EVIDENCE NAMING CONVENTION)

- **Ảnh chụp màn hình (Screenshot):**  
  Cấu trúc: `FN05_[TC-ID]_[Data-ID]_[Số thứ tự ảnh].png`  
  Danh mục evidence đã lưu trữ:  
  • `FN05_TC-BB-010_D01_01.png`: Hộp thoại chọn tài khoản Google (Account Picker)  
  • `FN05_TC-BB-010_D01_02.png`: Giao diện Trang chủ ghi chú sau khi đăng nhập Google thành công  
  • `FN05_TC-BB-011_D01_01.png`: Giao diện màn hình Đăng nhập sau khi bấm Back hủy Account Picker  
  • `FN05_TC-BB-011B_D01_01.png`: Thông báo lỗi màu đỏ khi bấm đăng nhập Google lúc mất kết nối mạng (Offline)  
  • `FN05_TC-BB-011C_D01_01.png`: Giao diện ngăn kéo hồ sơ (ProfileDrawer) của Smart Note App hiển thị Tên, Gmail và Avatar Google  
  • `FN05_TC-BB-011C_D01_02.png`: Màn hình Hồ sơ tài khoản (ProfileScreen) của Smart Note App chi tiết  
  • `FN05_TC-BB-011D_D01_01.png`: Màn hình Splash khi mở lại ứng dụng sau force-stop  
  • `FN05_TC-BB-011D_D01_02.png`: Màn hình Trang chủ tự động chuyển vào, duy trì phiên đăng nhập  
  • `FN05_TC-BB-011E_D01_01.png`: Màn hình Đăng nhập sau khi Đăng xuất tài khoản  
  • `FN05_TC-BB-011E_D01_02.png`: Màn hình Trang chủ sau khi Đăng nhập lại bằng Google  
  • `FN05_TC-BB-011F_D01_01.png`: Màn hình Trang chủ hiển thị trạng thái danh sách trống của tài khoản New User  
  • `FN05_TC-BB-011G_D01_01.png`: Màn hình Trang chủ hiển thị đầy đủ các ghi chú khôi phục của tài khoản Returning User  

---

## 5. DANH MỤC LỖI PHÁT HIỆN (BUG REPORT)

| Bug ID | TC ID | Data ID | Mô tả hành vi lỗi | Mức độ nghiêm trọng | Trạng thái |
|:---:|:---:|:---:|:---|:---:|:---:|
| *[Không có lỗi]* | - | - | Không phát sinh lỗi trong quá trình kiểm thử chức năng FN-05 | - | - |

---

## 6. BẢNG TỔNG KẾT THỰC THI (TEST EXECUTION SUMMARY)

| Chỉ số đo lường (Metrics) | Giá trị số lượng | Tỷ lệ (%) | Ghi chú giải thích |
|---|---:|---:|---|
| **Tổng số Test Case chính thức (Total Test Cases)** | **8** | **100.00%** | Bao gồm 2 TC gốc và 6 TC bổ sung chuyên sâu |
| **Tổng số lượt thực thi (Total Execution Items)** | **8** | **100.00%** | Mỗi TC tương ứng 1 Execution Item độc lập |
| **Số Test Case theo Yêu cầu (Requirement-based TCs)** | **3** | **37.50%** | TC-BB-010, TC-BB-011D, TC-BB-011G |
| **Số Test Case suy diễn từ quy tắc (Requirement-derived TCs)** | **2** | **25.00%** | TC-BB-011, TC-BB-011F |
| **Số Test Case theo Hành vi thực tế (Code-inferred TCs)** | **3** | **37.50%** | TC-BB-011B, TC-BB-011C, TC-BB-011E |
| **Số lượng ca Đạt (PASS)** | **8** | **100.00%** | Đạt 100% mong đợi quan sát thực tế trên UI (8/8 items) |
| **Số lượng ca Không đạt (FAIL)** | **0** | **0.00%** | Không có lỗi phát sinh |
| **Số lượng ca Bị chặn (BLOCKED)** | **0** | **0.00%** | Toàn bộ tiền đề tài khoản Google và thiết bị đáp ứng đầy đủ |
| **Số lượng ca Lỗi hệ thống (ERROR)** | **0** | **0.00%** | Không có lỗi hệ thống kiểm thử |
| **Số khiếm khuyết ứng dụng ghi nhận (Bugs)** | **0** | - | Không có bug |

---

## 7. CHECKLIST HOÀN TẤT KIỂM THỬ

- [x] Đã thực hiện đầy đủ 8/8 execution items của chức năng FN-05 trên thiết bị thật.
- [x] Đã ghi nhận Actual Result trung thực, chi tiết dựa trên hành vi observable trực tiếp trên màn hình.
- [x] Đã đánh giá trạng thái PASS / FAIL / BLOCKED theo đúng kết quả thực tế.
- [x] Đã lưu trữ đầy đủ 12 file ảnh bằng chứng (Evidence) theo đúng quy tắc đặt tên.
- [x] Không thay đổi Expected Result của các Test Case đã chốt.
- [x] Phân định rõ ràng giữa New User (`nopitran3@gmail.com`) và Returning User (`ht158713@gmail.com`).
