import 'package:flutter_test/flutter_test.dart';
import 'package:smart_note_app/models/checklist_item.dart';

void main() {
  group('ChecklistItem copyWith Unit Tests', () {
    test('should retain all existing properties when no changes are passed', () {
      final original = ChecklistItem(id: 'item-101', text: 'Original Task', checked: false);
      final copy = original.copyWith();

      expect(copy.id, 'item-101');
      expect(copy.text, 'Original Task');
      expect(copy.checked, isFalse);
    });

    test('should update supported fields when new values are provided', () {
      final original = ChecklistItem(id: 'item-102', text: 'Initial Text', checked: false);
      
      // Update both text and checked
      final copyBoth = original.copyWith(text: 'Updated Text', checked: true);
      expect(copyBoth.id, 'item-102');
      expect(copyBoth.text, 'Updated Text');
      expect(copyBoth.checked, isTrue);

      // Update only text
      final copyText = original.copyWith(text: 'Only Text Changed');
      expect(copyText.id, 'item-102');
      expect(copyText.text, 'Only Text Changed');
      expect(copyText.checked, isFalse);
    });

    test('should allow toggling checked from true to false', () {
      final original = ChecklistItem(id: 'item-103', text: 'Completed Task', checked: true);
      final copy = original.copyWith(checked: false);

      expect(copy.id, 'item-103');
      expect(copy.text, 'Completed Task');
      expect(copy.checked, isFalse);
    });

    test('should preserve original object unmodified after creating copy', () {
      final original = ChecklistItem(id: 'item-104', text: 'Immutable Task', checked: false);
      final copy = original.copyWith(text: 'Mutated in copy', checked: true);

      // Verify original remains untouched
      expect(original.id, 'item-104');
      expect(original.text, 'Immutable Task');
      expect(original.checked, isFalse);

      // Verify copy has the updated attributes
      expect(copy.id, 'item-104');
      expect(copy.text, 'Mutated in copy');
      expect(copy.checked, isTrue);

      // Verify they are distinct instances
      expect(identical(original, copy), isFalse);
    });
  });
}
