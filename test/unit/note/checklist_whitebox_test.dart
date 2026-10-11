// test/unit/note/checklist_whitebox_test.dart
// Selective White-box Test Expansion: Checklist Item Model (TC-WB-022)
// Verified against white_box_test_cases.md & lib/models/checklist_item.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:smart_note_app/models/checklist_item.dart';

void main() {
  group('White-box Checklist Tests (TC-WB-022)', () {
    // ══════════════════════════════════════════════════════════════════════
    // TC-WB-022 (P2): ChecklistItem.fromJson null fallbacks & UUID v4 check
    // ══════════════════════════════════════════════════════════════════════
    group('TC-WB-022 (P2): ChecklistItem.fromJson Defensive Fallbacks & UUID v4', () {
      test('TC-WB-022: Khả năng chịu lỗi khi phân tích ChecklistItem.fromJson với các trường null và xác minh UUID v4 chuẩn RFC 4122', () {
        final json = <String, dynamic>{
          'id': null,
          'text': null,
          'checked': null,
        };

        final item = ChecklistItem.fromJson(json);

        // Xác minh định dạng UUID v4 chuẩn RFC 4122 qua biểu thức chính quy (RegExp)
        final uuidV4Regex = RegExp(
          r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
          caseSensitive: false,
        );
        expect(uuidV4Regex.hasMatch(item.id), isTrue, reason: 'ID phải đúng định dạng UUID v4 RFC 4122');
        expect(item.id.length, equals(36));
        expect(item.text, equals(''));
        expect(item.checked, isFalse);
      });
    });
  });
}
