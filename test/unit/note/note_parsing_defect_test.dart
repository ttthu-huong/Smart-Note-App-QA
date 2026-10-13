// test/unit/note/note_parsing_defect_test.dart
// Defect Discovery & Robustness Testing (DEFECT-WB-01..04 & ROBUST-WB-01)
// Preserves all 4 identified defect tests (FAIL) and robustness verification (PASS) without modification

import 'package:flutter_test/flutter_test.dart';
import 'package:smart_note_app/models/note_model.dart';
import 'package:smart_note_app/models/checklist_item.dart';

void main() {
  group('Defect Discovery: Boundary, Condition & Type Robustness', () {

    // DEFECT 1: Quill Delta JSON dạng Object {"ops": [...]} bị trả về thô
    test('DEFECT-WB-01: Note.plainTextContent không bóc tách được Quill Delta dạng Map {"ops": [...]}', () {
      const deltaMapJson = '{"ops":[{"insert":"Kế hoạch tuần tới\\n"},{"insert":"Hoàn thành kiểm thử"}]}';
      final note = Note(
        id: 'n_delta_01',
        userId: 'u_01',
        title: 'Ghi chú Quill Map',
        content: deltaMapJson,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      // Expected độc lập: Plain text trích xuất phải là nội dung văn bản thuần
      const expectedPlainText = 'Kế hoạch tuần tới\nHoàn thành kiểm thử';
      
      // Production code tại note_model.dart L54 chỉ kiểm tra "if (decoded is List)"
      // Khi decoded là Map ("ops"), hàm rơi xuống L68 và trả về nguyên chuỗi JSON thô!
      expect(note.plainTextContent, equals(expectedPlainText));
    });

    // DEFECT 2: Note.fromMap làm mất tags khi input là List
    test('DEFECT-WB-02: Note.fromMap làm rỗng thuộc tính tags khi truyền Map chứa List', () {
      final rawMap = {
        'id': 'n_tags_01',
        'user_id': 'u_01',
        'title': 'Ghi chú có tags List',
        'content': 'Nội dung',
        'tags': ['flutter', 'dart', 'qa'],
      };

      final note = Note.fromMap(rawMap);

      // Expected độc lập: tags phải giữ nguyên ['flutter', 'dart', 'qa']
      // Production code tại note_model.dart L125 chỉ kiểm tra "if (raw is String)"
      // Khi raw là List, code rơi xuống L134 và trả về [] (MẤT DỮ LIỆU NHÃN)!
      expect(note.tags, equals(['flutter', 'dart', 'qa']));
    });

    // DEFECT 3: ChecklistItem.fromJson ném TypeError khi checked là integer 1/0
    test('DEFECT-WB-03: ChecklistItem.fromJson ném TypeError khi checked là int (1)', () {
      final jsonWithIntBool = {
        'id': 'chk_01',
        'text': 'Mục kiểm tra',
        'checked': 1,
      };

      // Expected độc lập: Hàm phải chuyển đổi 1 thành true hoặc xử lý an toàn
      // Production code tại checklist_item.dart L24: "json['checked'] as bool? ?? false"
      // Ép kiểu "as bool?" trên giá trị int ném TypeError!
      final item = ChecklistItem.fromJson(jsonWithIntBool);
      expect(item.checked, isTrue);
    });

    // DEFECT 4: ChecklistItem.fromJson ném TypeError khi id là int
    test('DEFECT-WB-04: ChecklistItem.fromJson ném TypeError khi id là số nguyên', () {
      final jsonWithIntId = {
        'id': 1001,
        'text': 'Mục ID số',
        'checked': false,
      };

      // Expected độc lập: Hàm phải chuyển đổi sang String "1001" hoặc sinh UUID
      // Production code tại checklist_item.dart L22: "json['id'] as String?"
      // Ép kiểu "as String?" trên int ném TypeError!
      final item = ChecklistItem.fromJson(jsonWithIntId);
      expect(item.id, equals('1001'));
    });

    // Robustness check: Checklist items malformed rơi an toàn vào catch
    test('ROBUST-WB-01: Note.checklistPlainText bắt an toàn ngoại lệ khi item trong checklist không phải Map', () {
      final note = Note(
        id: 'chk_robust_01',
        userId: 'u_01',
        title: 'Checklist lỗi item',
        content: '{"type":"checklist","items":["corrupted_string_item_not_map"]}',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      // Code rơi vào catch (_) tại dòng 27 và trả về chuỗi rỗng an toàn
      expect(note.checklistPlainText, equals(''));
    });
  });
}
