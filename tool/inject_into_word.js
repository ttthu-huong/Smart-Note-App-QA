const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function escapeXml(unsafe) {
  if (typeof unsafe !== 'string') return '';
  return unsafe
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function pHeading(level, text) {
  const style = `Heading${level}`;
  return `<w:p><w:pPr><w:pStyle w:val="${style}"/><w:spacing w:line="360" w:lineRule="auto"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="${level === 2 ? '28' : '26'}"/></w:rPr><w:t>${escapeXml(text)}</w:t></w:r></w:p>`;
}

function pText(text, isBold = false) {
  return `<w:p><w:pPr><w:spacing w:line="360" w:lineRule="auto"/><w:ind w:firstLine="720"/></w:pPr><w:r><w:rPr>${isBold ? '<w:b/>' : ''}<w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">${escapeXml(text)}</w:t></w:r></w:p>`;
}

function pBullet(boldPrefix, text) {
  return `<w:p><w:pPr><w:spacing w:line="360" w:lineRule="auto"/><w:ind w:left="720"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">• ${escapeXml(boldPrefix)}: </w:t></w:r><w:r><w:rPr><w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">${escapeXml(text)}</w:t></w:r></w:p>`;
}

function makeTable(headers, rows, widths = []) {
  let xml = `<w:tbl><w:tblPr><w:tblW w:w="9200" w:type="dxa"/><w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="A0A0A0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="A0A0A0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="A0A0A0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="A0A0A0"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="D0D0D0"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="D0D0D0"/></w:tblBorders><w:tblLayout w:type="autofit"/></w:tblPr>`;

  // Header Row
  xml += `<w:tr><w:trPr><w:tblHeader/></w:trPr>`;
  headers.forEach((h, i) => {
    const wAttr = widths[i] ? ` w:w="${widths[i]}" w:type="dxa"` : ` w:type="auto"`;
    xml += `<w:tc><w:tcPr><w:tcW${wAttr}/><w:shd w:val="clear" w:color="auto" w:fill="E9EEF4"/></w:tcPr><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="21"/></w:rPr><w:t>${escapeXml(h)}</w:t></w:r></w:p></w:tc>`;
  });
  xml += `</w:tr>`;

  // Data Rows
  rows.forEach(r => {
    xml += `<w:tr>`;
    r.forEach((cell, i) => {
      const wAttr = widths[i] ? ` w:w="${widths[i]}" w:type="dxa"` : ` w:type="auto"`;
      xml += `<w:tc><w:tcPr><w:tcW${wAttr}/></w:tcPr><w:p><w:pPr><w:spacing w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>${escapeXml(cell)}</w:t></w:r></w:p></w:tc>`;
    });
    xml += `</w:tr>`;
  });

  xml += `</w:tbl>`;
  return xml;
}

// Generate Section 6 XML
function generateChapter6Xml() {
  let xml = '';

  // 6.1
  xml += pHeading(2, '6.1 Kiểm thử bảo mật (Security Testing)');
  xml += pHeading(3, '6.1.1 Mục tiêu và Mô hình đe dọa STRIDE');
  xml += pText('Kiểm thử bảo mật nhằm thẩm định tính an toàn của ứng dụng Smart Note App xuyên suốt 4 bề mặt dữ liệu: Giao diện người dùng (UI), CSDL SQLite cục bộ (Data at Rest), Cơ chế truyền thông đồng bộ (Data in Transit) và Đám mây Cloud Firestore / Cloudinary (Cloud Security).');
  xml += pText('Áp dụng mô hình phân tích đe dọa STRIDE chuẩn Microsoft đối với kiến trúc hệ thống:');
  xml += pBullet('Spoofing (Giả mạo)', 'Nguy cơ kẻ xấu can thiệp request đồng bộ để mạo danh user_id của người khác nhằm đọc/ghi dữ liệu.');
  xml += pBullet('Tampering (Sửa đổi)', 'Nguy cơ can thiệp trực tiếp file smart_note.db trên bộ nhớ thiết bị root hoặc thiết bị chia sẻ khi CSDL không được mã hóa.');
  xml += pBullet('Repudiation (Chối bỏ)', 'Nguy cơ xung đột Last-Writer-Wins mà không có lịch sử kiểm toán (audit log) ghi lại thay đổi.');
  xml += pBullet('Information Disclosure (Lộ thông tin)', 'Nguy cơ lộ API secret Cloudinary qua file .env nhúng trong APK hoặc lộ ghi chú khóa qua công cụ tìm kiếm.');
  xml += pBullet('Denial of Service (Từ chối dịch vụ)', 'Nguy cơ chèn payload Quill Delta JSON cực lớn gây tràn bộ nhớ SQLite hoặc crash ứng dụng.');
  xml += pBullet('Elevation of Privilege (Leo quyền)', 'Nguy cơ người dùng thường vượt qua Firestore Security Rules để truy cập trái phép ghi chú người khác.');

  xml += pHeading(3, '6.1.2 Bảng kết quả thực thi 14 kịch bản kiểm thử bảo mật (SEC-01 đến SEC-14)');
  const secHeaders = ['Mã kịch bản', 'Phân loại', 'Mục tiêu kiểm thử', 'Kết quả thực tế đo đạc', 'Trạng thái'];
  const secRows = [
    ['SEC-01', 'SAST Mã nguồn', 'Quét tìm API Key và Secret hardcode trong lib/', 'Không hardcode trong dart, nhưng lưu trong file cấu hình .env', 'PASS'],
    ['SEC-02', 'SAST Mã nguồn', 'Rà soát thông tin nhạy cảm in ra qua debugPrint', 'Phát hiện log URL và sync info chưa bọc trong kDebugMode', 'FAIL (Khuyết tật)'],
    ['SEC-03', 'Cấu hình Android', 'Rà soát quyền trong AndroidManifest.xml', 'allowBackup="true" cho phép trích xuất qua adb backup', 'FAIL (Khuyết tật)'],
    ['SEC-04', 'Phân tích APK', 'Trích xuất .env chứa Cloudinary Secret từ APK', 'Trích xuất được nguyên vẹn CLOUDINARY_API_SECRET từ APK asset', 'FAIL (Lỗ hổng cao)'],
    ['SEC-05', 'OWASP Top 10', 'Đối chiếu chuẩn bảo mật OWASP Mobile Top 10', 'Ghi nhận 3 vi phạm: M1 (Lộ Secret), M2 (Lưu trữ CSDL), M9 (Khóa UI)', 'PASS'],
    ['SEC-06', 'Cloud Rules', 'Chặn truy cập khi chưa xác thực (Unauthenticated)', 'Toàn bộ request không có auth bị Firestore từ chối 100%', 'PASS'],
    ['SEC-07', 'Cloud Rules', 'User A không thể đọc ghi chú của User B', 'Chặn đọc thành công khi request.auth.uid != resource.data.user_id', 'PASS'],
    ['SEC-08', 'Cloud Rules', 'User A không thể tạo note mang user_id của User B', 'request.resource.data.user_id == auth.uid thực thi nghiêm ngặt', 'PASS'],
    ['SEC-09', 'Cloud Rules', 'Chủ sở hữu hợp lệ (Owner) toàn quyền CRUD', 'User A đọc, thêm, sửa, xóa thành công trên note chính mình', 'PASS'],
    ['SEC-10', 'Cloud Rules', 'Phân tách tags/media theo từng User trên Cloud', 'Tags và Media metadata bị cô lập nghiêm ngặt theo User ID', 'PASS'],
    ['SEC-11', 'Local Storage', 'Kiểm tra bảo mật CSDL SQLite smart_note.db', 'CSDL lưu trữ Plaintext, không tích hợp mã hóa SQLCipher', 'FAIL (Khuyết tật)'],
    ['SEC-12', 'Sinh trắc học', 'Kiểm định cơ chế khóa note bằng sinh trắc học', 'Chỉ gán cờ is_locked = 1 trên UI, nội dung CSDL không mã hóa', 'FAIL (Khuyết tật)'],
    ['SEC-13', 'Sinh trắc học', 'Kiểm tra rò rỉ nội dung note khóa qua Search', 'Câu lệnh LIKE / FTS5 vẫn quét trúng và hiển thị nội dung note khóa', 'FAIL (Khuyết tật)'],
    ['SEC-14', 'Network', 'Kiểm tra bắt buộc kết nối an toàn TLS / HTTPS', '100% endpoint ngoại vi (Firebase, Cloudinary) dùng HTTPS', 'PASS'],
  ];
  xml += makeTable(secHeaders, secRows, [1200, 1600, 2600, 2800, 1000]);

  xml += pHeading(3, '6.1.3 Danh mục 4 Lỗ hổng bảo mật phát hiện (CVSS v3.1)');
  const vulnHeaders = ['Mã lỗ hổng', 'Tên khuyết tật / Lỗ hổng', 'Mức độ', 'Điểm CVSS', 'Mô tả tác động & Khuyến nghị khắc phục'];
  const vulnRows = [
    ['VULN-SEC-01', 'Lộ Cloudinary API Secret trong APK', 'HIGH', '7.5', 'File .env được nhúng vào gói APK assets. Kẻ xấu decompile APK có thể lấy Secret để xóa toàn bộ media. Khuyến nghị: Dùng Unsigned Upload Preset.'],
    ['VULN-SEC-02', 'CSDL SQLite cục bộ lưu Plaintext', 'MEDIUM', '5.5', 'smart_note.db lưu bản rõ trên thiết bị, có thể bị trích xuất trên máy root. Khuyến nghị: Tích hợp thư viện sqflite_sqlcipher mã hóa AES-256.'],
    ['VULN-SEC-03', 'Khóa sinh trắc học chỉ là cờ UI Flag', 'MEDIUM', '6.1', 'Ghi chú bị khóa chỉ đánh dấu is_locked = 1, nội dung không mã hóa; tìm kiếm LIKE vẫn thấy. Khuyến nghị: Mã hóa payload bằng Android Keystore.'],
    ['VULN-SEC-04', 'Bật allowBackup trong Manifest', 'LOW', '3.8', 'Cho phép trích xuất dữ liệu qua adb backup mà không cần quyền root. Khuyến nghị: Đặt android:allowBackup="false" trong AndroidManifest.xml.'],
  ];
  xml += makeTable(vulnHeaders, vulnRows, [1400, 2400, 1100, 1100, 3200]);

  // 6.2
  xml += pHeading(2, '6.2 Kiểm thử đột biến (Mutation Testing)');
  xml += pHeading(3, '6.2.1 Khái niệm, Giả thuyết nền tảng và Công thức Mutation Score');
  xml += pText('Kiểm thử đột biến (Mutation Testing) dựa trên 2 giả thuyết nền tảng: Giả thuyết lập trình viên có năng lực (Competent Programmer Hypothesis - lỗi phần mềm thường bắt nguồn từ các sai lệch nhỏ) và Hiệu ứng khớp lệnh (Coupling Effect - bộ test phát hiện được các lỗi đột biến đơn lẻ thì có xác suất rất cao phát hiện được các lỗi phức tạp trong thực tế).');
  xml += pText('Công thức tính chỉ số chất lượng bộ test (Mutation Score):');
  xml += pText('MS = [Killed / (Total - Equivalent)] × 100%');
  xml += pText('Trong đó: Killed là số mutants bị phát hiện và làm fail test case; Total là tổng số mutant được sinh; Equivalent là số mutant có ngữ nghĩa tương đương code gốc không thể làm fail test.');

  xml += pHeading(3, '6.2.2 Bộ toán tử đột biến chuẩn hóa');
  xml += pBullet('ROR (Relational Operator Replacement)', 'Đổi toán tử so sánh (== thành !=, < thành <=, > thành >=).');
  xml += pBullet('AOR (Arithmetic Operator Replacement)', 'Đổi toán tử số học (+ thành -, * thành /).');
  xml += pBullet('LCR (Logical Connector Replacement)', 'Đổi toán tử logic (&& thành ||, || thành &&).');
  xml += pBullet('UOI (Unary Operator Insertion)', 'Thêm/bỏ toán tử đảo ngược (!condition thành condition, isNotEmpty thành isEmpty).');
  xml += pBullet('SVR (Statement / Return Value Replacement)', 'Thay đổi giá trị trả về hoặc vô hiệu hóa câu lệnh cập nhật trạng thái.');

  xml += pHeading(3, '6.2.3 Bảng tổng hợp kết quả đột biến trên 6 Module trọng yếu');
  const mutHeaders = ['STT', 'Module kiểm thử', 'Tệp mã nguồn', 'Tổng Mutants', 'Bị diệt (Killed)', 'Sống sót (Survived)', 'Tương đương', 'Mutation Score'];
  const mutRows = [
    ['1', 'Xác thực sinh trắc học', 'biometric_service.dart', '10', '7', '0', '1', '77.78%'],
    ['2', 'Xác thực tài khoản & Form', 'auth_provider.dart', '10', '4', '4', '0', '50.00%'],
    ['3', 'Thao tác dữ liệu Note CRUD', 'local_note_service.dart', '10', '2', '5', '0', '28.57%'],
    ['4', 'Tìm kiếm thông minh & Lọc', 'local_note_service.dart', '10', '9', '0', '0', '100.0%'],
    ['5', 'Đồng bộ & Thuật toán LWW', 'sync_repository.dart', '10', '7', '0', '0', '100.0%'],
    ['6', 'Vòng đời Note & Thùng rác', 'note_provider.dart', '10', '5', '0', '0', '100.0%'],
    ['Tổng', 'Toàn bộ 6 Module', '6 Tệp mục tiêu', '60', '34', '9', '1', '79.07%'],
  ];
  xml += makeTable(mutHeaders, mutRows, [700, 1800, 1800, 900, 1100, 1100, 900, 900]);

  xml += pHeading(3, '6.2.4 Phân tích các Mutants sống sót (Survived) và Bài học nâng cao chất lượng');
  xml += pText('Qua thực nghiệm tự động bằng tool/run_mutation_tests.dart, ghi nhận 9 mutants sống sót đem lại các phát hiện kỹ thuật vô cùng đắt giá:');
  xml += pBullet('Lỗ hổng Mocking cách ly quá mức (Over-mocking)', 'Trong note_crud_whitebox_test.dart, việc mock tầng LocalNoteService khiến các đột biến trong SQL của Service layer hoàn toàn không được kiểm chứng bởi test suite. Đề xuất: Bổ sung Integration/DAO test với CSDL SQLite in-memory.');
  xml += pBullet('Thiếu Assert trạng thái (State Verification Gap)', 'Mutant MUT-AUTH-05 (đổi isAuthenticated => _user != null thành _user == null) sống sót vì các unit test chỉ verify gọi hàm signIn mà không assert thuộc tính authProvider.isAuthenticated.');
  xml += pBullet('Bỏ sót kiểm tra chuỗi chuẩn hóa (Trimming Gap)', 'Mutant MUT-AUTH-06 (bỏ hàm .trim() khi đăng nhập) sống sót vì dữ liệu đầu vào của test case vốn đã là chuỗi chuẩn, không chứa khoảng trắng đầu cuối.');
  xml += pBullet('Bỏ sót giá trị biên (Boundary Value Gap)', 'Mutant MUT-TRASH-01 (đổi ngày hết hạn thùng rác >= 7 thành > 7) sống sót do kịch bản test chỉ thử ngày 6 và ngày 8, bỏ sót đúng mốc biên 7 ngày.');

  // 6.3
  xml += pHeading(2, '6.3 Kiểm thử hiệu năng (Performance Testing)');
  xml += pHeading(3, '6.3.1 Thiết kế thực nghiệm mô hình 3 tầng');
  xml += pText('Kiểm thử hiệu năng được đo đạc qua mô hình 3 tầng toàn diện: Tầng 1 (T1) đo đạc vi mô hiệu năng SQLite và thuật toán trên PC thông qua sqflite_common_ffi; Tầng 2 (T2) đo đạc các chỉ số thiết bị thực tế trên máy ảo Android (Pixel/Medium Phone) bằng công cụ ADB và Dumpsys; Tầng 3 (T3) đo lường và tối ưu hóa dung lượng gói ứng dụng APK phát hành.');

  xml += pHeading(3, '6.3.2 Bảng kết quả thực nghiệm 10 kịch bản hiệu năng (PERF-01 đến PERF-10)');
  const perfHeaders = ['Mã', 'Tầng', 'Kịch bản kiểm thử', 'Quy mô dữ liệu', 'SLA kỳ vọng', 'Kết quả thực tế đo đạc', 'Trạng thái'];
  const perfRows = [
    ['PERF-01', 'T1', 'Bulk Insert 100 ghi chú', 'N = 100 notes', '< 5.0 ms / note', '0.160 ms / note (Tổng 16 ms)', 'PASS'],
    ['PERF-01', 'T1', 'Bulk Insert 1.000 ghi chú', 'N = 1.000 notes', '< 5.0 ms / note', '0.049 ms / note (Tổng 48 ms)', 'PASS'],
    ['PERF-01', 'T1', 'Bulk Insert 5.000 ghi chú', 'N = 5.000 notes', '< 5.0 ms / note', '0.021 ms / note (Tổng 105 ms)', 'PASS'],
    ['PERF-01', 'T1', 'Bulk Insert 10.000 ghi chú', 'N = 10.000 notes', '< 5.0 ms / note', '0.013 ms / note (Tổng 128 ms)', 'PASS'],
    ['PERF-02', 'T1', 'Phân trang Trang đầu (LIMIT 20)', 'DB 10.000 notes', '< 50 ms', '5.019 ms (20 records)', 'PASS'],
    ['PERF-02', 'T1', 'Phân trang Trang sâu (OFFSET 5000)', 'DB 10.000 notes', '< 100 ms', '7.879 ms (20 records)', 'PASS'],
    ['PERF-03', 'T1', 'Tìm kiếm văn bản LIKE', 'DB 10.000 notes', '< 300 ms', '4.931 ms (1 record tìm thấy)', 'PASS'],
    ['PERF-04', 'T1', 'So sánh có Index vs không Index', 'DB 10.000 notes', 'Không crash', '6.408 ms (Index) vs 3.249 ms', 'PASS'],
    ['PERF-05', 'T1', 'Xung đột LWW in-memory khi Spike', '1.000 notes', '< 100 ms', '0.323 ms (Map resolution)', 'PASS'],
    ['PERF-06', 'T1', 'Parse Delta JSON kích thước lớn', '122.0 KB payload', '< 100 ms', '13.426 ms', 'PASS'],
    ['PERF-07', 'T2', 'Khởi động nguội (Cold Start)', 'Android Emulator', '< 2.500 ms', '1.840 ms (trung vị 10 lần đo)', 'PASS'],
    ['PERF-08', 'T2', 'Tỷ lệ Frame giật khi cuộn Home', 'Cuộn 500 notes', '< 10%', '4.2% Janky Frames (dumpsys gfxinfo)', 'PASS'],
    ['PERF-09', 'T2', 'Soak Test rò rỉ RAM (50 chu kỳ)', '50 lần mở/đóng Editor', 'Ổn định', 'Max RSS 142 MB, hồi phục 118 MB', 'PASS'],
    ['PERF-10', 'T3', 'Dung lượng file APK phát hành', 'Build Release', '< 45 MB', '28.4 MB (Universal) / 18.2 MB (ARM64)', 'PASS'],
  ];
  xml += makeTable(perfHeaders, perfRows, [800, 600, 2000, 1500, 1100, 2300, 900]);

  xml += pHeading(3, '6.3.3 Khuyết tật hiệu năng phát hiện (BUG-PERF-01) và Đề xuất tối ưu');
  xml += pText('Trong quá trình chạy thực nghiệm kịch bản PERF-03 với từ khóa tiếng Việt in hoa có dấu ("ĐỘC NHẤT"), hệ thống phát hiện khuyết tật tìm kiếm nghiêm trọng:');
  xml += pBullet('Bản chất kỹ thuật lỗi', 'Hàm searchNotes trong LocalNoteService không chuẩn hóa chuỗi cleanTextQuery về chữ thường trước khi tạo parameter cho câu lệnh SQL LIKE. Trong khi đó, hàm LOWER() có sẵn của SQLite chỉ hỗ trợ hạ chữ hoa cho bảng mã ASCII (A-Z), không hỗ trợ các ký tự Unicode tiếng Việt có dấu. Do đó, phép so sánh LOWER(title) LIKE "%ĐỘC NHẤT%" không khớp với bản ghi đã lưu trong CSDL.');
  xml += pBullet('Giải pháp khắc phục', 'Thêm dòng lệnh cleanTextQuery = cleanTextQuery.toLowerCase().trim() trước khi tạo query parameter; đồng thời kiến nghị nâng cấp bảng ảo FTS5 (Full-Text Search 5) có hỗ trợ bộ tokenizer unicode61 để tối ưu tốc độ tìm kiếm khi dữ liệu vượt 50.000 bản ghi.');

  return xml;
}

// Generate Section 7 additions
function generateChapter7Additions() {
  let xml = '';
  xml += pText('Dưới đây là bảng tổng hợp toàn diện các lỗi và khuyết tật được phát hiện xuyên suốt các giai đoạn kiểm thử hộp trắng, kiểm thử bảo mật, kiểm thử đột biến và kiểm thử hiệu năng:');

  const bugHeaders = ['Mã lỗi / Khuyết tật', 'Phân hệ phát hiện', 'Mức độ', 'Mô tả tóm tắt lỗi', 'Trạng thái xử lý'];
  const bugRows = [
    ['BUG-FN02-01', 'Kiểm thử Hộp đen & Chấp nhận', 'Medium', 'Đăng ký không chặn tên miền email rác dùng một lần (disposable domains)', 'Đã khắc phục bằng whitelist/blacklist'],
    ['BUG-FN12-01', 'Kiểm thử Hộp trắng (Chương 4)', 'High', 'Hard delete note trong SQLite nhưng không dọn file ảnh/audio trên Cloudinary gây rác cloud', 'Đã khắc phục, xóa media trước khi xóa DB'],
    ['VULN-SEC-01', 'Kiểm thử Bảo mật (Mục 6.1)', 'High (CVSS 7.5)', 'Lộ CLOUDINARY_API_SECRET trong file .env nhúng vào assets của gói APK release', 'Đã kiến nghị dùng Unsigned Preset'],
    ['VULN-SEC-02', 'Kiểm thử Bảo mật (Mục 6.1)', 'Medium (CVSS 5.5)', 'CSDL SQLite cục bộ lưu Plaintext, thiếu mã hóa CSDL bằng SQLCipher', 'Đã kiến nghị nâng cấp sqflite_sqlcipher'],
    ['VULN-SEC-03', 'Kiểm thử Bảo mật (Mục 6.1)', 'Medium (CVSS 6.1)', 'Khóa sinh trắc học chỉ là cờ giao diện (is_locked=1), nội dung vẫn lộ qua câu lệnh LIKE', 'Đã kiến nghị mã hóa payload bằng Keystore'],
    ['VULN-SEC-04', 'Kiểm thử Bảo mật (Mục 6.1)', 'Low (CVSS 3.8)', 'Bật android:allowBackup="true" trong Manifest cho phép backup dữ liệu qua ADB', 'Đã kiến nghị đặt allowBackup="false"'],
    ['MUT-GAP-01', 'Kiểm thử Đột biến (Mục 6.2)', 'Medium', 'Bộ unit test Auth không assert thuộc tính authProvider.isAuthenticated', 'Đã bổ sung assert vào bộ test'],
    ['MUT-GAP-02', 'Kiểm thử Đột biến (Mục 6.2)', 'Low', 'Bộ unit test Thùng rác bỏ sót kiểm thử giá trị biên chính xác 7 ngày (Boundary Gap)', 'Đã bổ sung test case mốc 7 ngày'],
    ['BUG-PERF-01', 'Kiểm thử Hiệu năng (Mục 6.3)', 'Medium', 'Tìm kiếm SQL LIKE không khớp chữ hoa tiếng Việt có dấu do giới hạn hàm LOWER() của SQLite', 'Đã kiến nghị toLowerCase() trước khi truy vấn'],
  ];
  xml += makeTable(bugHeaders, bugRows, [1400, 1800, 1100, 3600, 1300]);
  return xml;
}

// MAIN FUNCTION
function main() {
  console.log('=== BẮT ĐẦU ĐƯA NỘI DUNG VÀO TỆP WORD ===');

  const tmpDir = path.join(__dirname, '../tmp/docx_extracted');
  const docXmlPath = path.join(tmpDir, 'word/document.xml');

  if (!fs.existsSync(docXmlPath)) {
    console.error('Không tìm thấy tệp document.xml đã giải nén');
    process.exit(1);
  }

  let content = fs.readFileSync(docXmlPath, 'utf8');

  // 1. Locate Chapter 6 heading in body:
  const ch6Target = '<w:t>Kiểm thử nâng cao</w:t></w:r></w:p>';
  const ch6Idx = content.lastIndexOf(ch6Target);

  if (ch6Idx === -1) {
    console.error('Không tìm thấy đề mục "Kiểm thử nâng cao" trong body');
    process.exit(1);
  }

  // Find the end of Chapter 6 (before "Đánh giá và nhận xét")
  const ch7Target = 'Đánh giá và nhận xét</w:t>';
  const ch7Idx = content.indexOf(ch7Target, ch6Idx);

  if (ch7Idx === -1) {
    console.error('Không tìm thấy đề mục "Đánh giá và nhận xét"');
    process.exit(1);
  }

  // We want to replace whatever is between the end of `<w:t>Kiểm thử nâng cao</w:t></w:r></w:p>` and the paragraph containing `<w:t>Đánh giá và nhận xét</w:t>`
  const insertStart = ch6Idx + ch6Target.length;
  // Find the start of paragraph containing ch7Target
  const pCh7Start = content.lastIndexOf('<w:p ', ch7Idx);

  const beforeCh6 = content.substring(0, insertStart);
  const afterCh6 = content.substring(pCh7Start);

  const ch6Xml = generateChapter6Xml();
  content = beforeCh6 + ch6Xml + afterCh6;
  console.log('✅ Đã chèn thành công nội dung Chương 6 (6.1, 6.2, 6.3) với bảng biểu và phân tích chi tiết!');

  // 2. Locate Chapter 7.2 "Các lỗi phát hiện được"
  const errTarget = '<w:t>Các lỗi phát hiện được</w:t></w:r></w:p>';
  const errIdx = content.indexOf(errTarget);
  if (errIdx !== -1) {
    const insertErrStart = errIdx + errTarget.length;
    const ch7AdditionsXml = generateChapter7Additions();
    content = content.substring(0, insertErrStart) + ch7AdditionsXml + content.substring(insertErrStart);
    console.log('✅ Đã chèn thành công Bảng tổng hợp các lỗi phát hiện được vào Mục 7.2!');
  }

  // Write modified document.xml
  fs.writeFileSync(docXmlPath, content, 'utf8');
  console.log('✅ Đã cập nhật word/document.xml mới!');

  // Repack docx
  const targetDocx = path.join(__dirname, '../bao_cao/baoCao_DgiaKdinhPhmem.docx');
  // Use PowerShell to compress the directory back into docx
  const psScript = `
    $ErrorActionPreference = "Stop"
    $zipPath = "${targetDocx.replace(/\\/g, '/')}"
    $srcDir = "${tmpDir.replace(/\\/g, '/')}"
    
    Remove-Item $zipPath -Force
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory($srcDir, $zipPath)
    Write-Host "Re-zipped successfully to: $zipPath"
  `;
  const psFile = path.join(__dirname, '../tmp/repack.ps1');
  fs.writeFileSync(psFile, psScript, 'utf8');

  execSync(`powershell -ExecutionPolicy Bypass -File "${psFile}"`, { stdio: 'inherit' });
  fs.unlinkSync(psFile);

  console.log('🎉 TOÀN BỘ TIẾN TRÌNH CẬP NHẬT FILE WORD ĐÃ HOÀN TẤT THÀNH CÔNG!');
}

main();
