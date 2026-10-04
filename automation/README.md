# HƯỚNG DẪN CHẠY TEST TỰ ĐỘNG (AUTOMATION TESTING) — SMART NOTE APP

Thư mục này chứa bộ kịch bản kiểm thử tự động hóa (Automation Testing) dành cho ứng dụng **Smart Note App**, được xây dựng theo tiêu chuẩn **IEEE 829 & ISTQB**, sử dụng `pytest` kết hợp với `uiautomator2` trên thiết bị Android thật.

---

## 1. Cấu trúc thư mục

```text
automation/
├── config.py                 # Cấu hình thiết bị, package app và timeout
├── runner.py                 # Script thực thi chính (CLI Runner)
├── core/
│   ├── __init__.py
│   └── device.py             # Driver điều khiển thiết bị (Dynamic-first, Coordinate-fallback)
├── tests/
│   ├── __init__.py
│   └── test_fn04_login.py    # Test suite FN-04 (TC-BB-006 -> TC-BB-009)
└── reports/                  # Chứa báo cáo Markdown, XML và Log thực thi
    ├── fn04_automation_report.md
    └── fn04_login_junit.xml
```

---

## 2. Yêu cầu môi trường
- Python 3.10+
- Thiết bị Android vật lý đã kích hoạt USB Debugging (ví dụ: Samsung Galaxy S21 FE `R5CW82ECF6M`)
- Cài đặt thư viện:
  ```bash
  pip install pytest uiautomator2
  ```

---

## 3. Hướng dẫn chạy Test

### Chạy qua Runner chính (Khuyên dùng):
```bash
python automation/runner.py --suite fn04_login
```

### Chạy trực tiếp qua Pytest:
```bash
pytest automation/tests/test_fn04_login.py -v -s
```

---

## 4. Nguyên tắc kiểm thử tự động
1. **Bảo toàn Test Case:** Tuyệt đối không thay đổi Expected Result của Black-box Test Case để biến FAIL thành PASS.
2. **Trung thực trong báo cáo:** Ghi nhận chính xác phản hồi thực tế từ ứng dụng và ánh xạ lỗi sang Bug ID tương ứng (`BUG-BB-002`, `BUG-BB-003`, `BUG-BB-004`).
3. **Lưu trữ bằng chứng:** Mỗi test case tự động chụp ảnh màn hình và lưu vào thư mục `evidence/` theo chuẩn đặt tên.
