// test/unit/note/note_model_whitebox_test.dart
// Selective White-box Test Expansion: Note Model & Serialization (TC-WB-015..020 & SUPP-NOTE-FS-01/02)
// Verified against white_box_test_cases.md & lib/models/note_model.dart

import 'dart:convert';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:smart_note_app/models/note_model.dart';

void main() {
  group('White-box Note Model Tests (TC-WB-015 .. TC-WB-020 & SUPP)', () {
    // ══════════════════════════════════════════════════════════════════════
    // TC-WB-015 (P1): pendingChecklistCount
    // ══════════════════════════════════════════════════════════════════════
    group('TC-WB-015 (P1): Note.pendingChecklistCount', () {
      test('TC-WB-015a: Note A - Văn bản thô không phải checklist trả về 0', () {
        final noteA = Note(
          id: 'note-a',
          userId: 'u1',
          title: 'Note A',
          content: 'Ghi chú thường không có định dạng checklist',
          updatedAt: DateTime(2026, 10, 1),
        );
        expect(noteA.pendingChecklistCount, equals(0));
      });

      test('TC-WB-015b: Note B - Checklist chuẩn có 3 items (1 true, 2 false) trả về 2', () {
        final noteB = Note(
          id: 'note-b',
          userId: 'u1',
          title: 'Note B',
          content: jsonEncode({
            'type': 'checklist',
            'items': [
              {'id': '1', 'text': 'Task 1', 'checked': true},
              {'id': '2', 'text': 'Task 2', 'checked': false},
              {'id': '3', 'text': 'Task 3', 'checked': false},
            ],
          }),
          updatedAt: DateTime(2026, 10, 1),
        );
        expect(noteB.pendingChecklistCount, equals(2));
      });

      test('TC-WB-015c: Note C1 & C2 - Xử lý an toàn khi item khuyết key checked hoặc checklist khuyết items', () {
        // C1: item khuyết key checked -> null != true -> pending = 1
        final noteC1 = Note(
          id: 'note-c1',
          userId: 'u1',
          title: 'Note C1',
          content: jsonEncode({
            'type': 'checklist',
            'items': [
              {'id': '4', 'text': 'Task 4'},
            ],
          }),
          updatedAt: DateTime(2026, 10, 1),
        );
        expect(noteC1.pendingChecklistCount, equals(1));

        // C2: khuyết key items -> fallback ?? [] -> pending = 0
        final noteC2 = Note(
          id: 'note-c2',
          userId: 'u1',
          title: 'Note C2',
          content: jsonEncode({'type': 'checklist'}),
          updatedAt: DateTime(2026, 10, 1),
        );
        expect(noteC2.pendingChecklistCount, equals(0));
      });

      test('TC-WB-015d: Note D - JSON Map thiếu type checklist (isChecklist == false) trả về 0', () {
        final noteD = Note(
          id: 'note-d',
          userId: 'u1',
          title: 'Note D',
          content: jsonEncode({
            'items': [
              {'id': '5', 'text': 'Task 5', 'checked': false},
            ],
          }),
          updatedAt: DateTime(2026, 10, 1),
        );
        expect(noteD.pendingChecklistCount, equals(0));
      });

      test('TC-WB-015e: Note E - Bắt ngoại lệ TypeError tại catch (_) khi items bị sai kiểu dữ liệu trả về 0', () {
        final noteE = Note(
          id: 'note-e',
          userId: 'u1',
          title: 'Note E',
          content: jsonEncode({
            'type': 'checklist',
            'items': 'corrupted_not_a_list',
          }),
          updatedAt: DateTime(2026, 10, 1),
        );
        expect(noteE.pendingChecklistCount, equals(0));
      });
    });

    // ══════════════════════════════════════════════════════════════════════
    // TC-WB-016 (P1): plainTextContent with Quill Delta JSON
    // ══════════════════════════════════════════════════════════════════════
    group('TC-WB-016 (P1): Note.plainTextContent Delta JSON', () {
      test('TC-WB-016: Trích xuất chuỗi văn bản thuần từ Quill Delta JSON và bỏ qua an toàn embed/attributes', () {
        final deltaContent = jsonEncode([
          {'insert': 'Kế hoạch tuần tới\n'},
          {'insert': {'image': 'https://img.com/p1.png'}}, // embed map -> bỏ qua
          {'attributes': {'bold': true}}, // map thiếu insert -> bỏ qua
          'raw_non_map_item', // không phải map -> bỏ qua
          {'insert': 'Thực hiện kiểm thử hộp trắng'},
        ]);

        final note = Note(
          id: 'note-delta',
          userId: 'u1',
          title: 'Kế hoạch',
          content: deltaContent,
          updatedAt: DateTime(2026, 10, 1),
        );

        expect(
          note.plainTextContent,
          equals('Kế hoạch tuần tới\nThực hiện kiểm thử hộp trắng'),
        );
      });
    });

    // ══════════════════════════════════════════════════════════════════════
    // TC-WB-017 (P1): plainTextContent Edge Cases & Defensive Fallbacks
    // ══════════════════════════════════════════════════════════════════════
    group('TC-WB-017 (P1): Note.plainTextContent Edge Cases & Fallbacks', () {
      test('TC-WB-017a: Payload 1 - Chuỗi rỗng trả về chuỗi rỗng', () {
        final note1 = Note(
          id: 'n1',
          userId: 'u1',
          title: 'Empty',
          content: '',
          updatedAt: DateTime(2026, 10, 1),
        );
        expect(note1.plainTextContent, equals(''));
      });

      test('TC-WB-017b: Payload 2 - Văn bản thô không bắt đầu bằng [ hay { trả về chuỗi trimmed', () {
        final note2 = Note(
          id: 'n2',
          userId: 'u1',
          title: 'Raw text',
          content: '   Ghi chú văn bản thô không qua editor   ',
          updatedAt: DateTime(2026, 10, 1),
        );
        expect(note2.plainTextContent, equals('Ghi chú văn bản thô không qua editor'));
      });

      test('TC-WB-017c: Payload 3 - JSON cú pháp lỗi rơi vào catch (_) trả về chuỗi trimmed', () {
        final note3 = Note(
          id: 'n3',
          userId: 'u1',
          title: 'Malformed',
          content: '[{malformed_json_without_end',
          updatedAt: DateTime(2026, 10, 1),
        );
        expect(note3.plainTextContent, equals('[{malformed_json_without_end'));
      });

      test('TC-WB-017d: Payload 4 - JSON Map không phải List (decoded is! List) trả về chuỗi nguyên bản', () {
        final note4 = Note(
          id: 'n4',
          userId: 'u1',
          title: 'JSON Map',
          content: '{"custom_meta": "value"}',
          updatedAt: DateTime(2026, 10, 1),
        );
        expect(note4.plainTextContent, equals('{"custom_meta": "value"}'));
      });

      test('TC-WB-017e: Payload 5 - Ghi chú dạng Checklist ủy quyền sang checklistPlainText', () {
        final note5 = Note(
          id: 'n5',
          userId: 'u1',
          title: 'Checklist note',
          content: jsonEncode({
            'type': 'checklist',
            'items': [
              {'id': '1', 'text': 'Mục 1', 'checked': true},
            ],
          }),
          updatedAt: DateTime(2026, 10, 1),
        );
        expect(note5.plainTextContent, equals('☑ Mục 1'));
      });
    });

    // ══════════════════════════════════════════════════════════════════════
    // TC-WB-018 (P2): Note.copyWith clearReminder
    // ══════════════════════════════════════════════════════════════════════
    group('TC-WB-018 (P2): Note.copyWith clearReminder', () {
      final originalReminder = DateTime(2026, 10, 20, 8, 30);
      final note = Note(
        id: 'note-rem',
        userId: 'u1',
        title: 'Tiêu đề cũ',
        content: 'Nội dung',
        reminder: originalReminder,
        updatedAt: DateTime(2026, 10, 1),
      );

      test('TC-WB-018a: clearReminder = true hủy mốc nhắc nhở về null', () {
        final res1 = note.copyWith(clearReminder: true);
        expect(res1.reminder, isNull);
      });

      test('TC-WB-018b: clearReminder = false và không truyền reminder mới giữ nguyên mốc cũ', () {
        final res2 = note.copyWith(title: 'Tiêu đề đổi mới');
        expect(res2.reminder, equals(originalReminder));
      });

      test('TC-WB-018c: Truyền reminder mới cập nhật chính xác mốc thời gian', () {
        final newReminder = DateTime(2026, 11, 15, 10, 0);
        final res3 = note.copyWith(reminder: newReminder);
        expect(res3.reminder, equals(newReminder));
      });
    });

    // ══════════════════════════════════════════════════════════════════════
    // TC-WB-019 (P1): Note.copyWith updatedAt
    // ══════════════════════════════════════════════════════════════════════
    group('TC-WB-019 (P1): Note.copyWith updatedAt', () {
      final originalDate = DateTime(2026, 10, 1, 12, 0, 0);
      final note = Note(
        id: 'note-upd',
        userId: 'u1',
        title: 'Ghi chú gốc',
        content: 'Nội dung gốc',
        updatedAt: originalDate,
      );

      test('TC-WB-019a: copyWith không truyền updatedAt tự sinh thời gian trong khoảng [before, after]', () {
        final beforeCall = DateTime.now().millisecondsSinceEpoch;
        final res1 = note.copyWith(content: 'Nội dung mới');
        final afterCall = DateTime.now().millisecondsSinceEpoch;

        // Kiểm tra cận trên và cận dưới chặt chẽ quanh thời điểm gọi hàm
        expect(res1.updatedAt.millisecondsSinceEpoch >= beforeCall, isTrue);
        expect(res1.updatedAt.millisecondsSinceEpoch <= afterCall, isTrue);
        expect(res1.updatedAt.isAfter(originalDate), isTrue);
      });

      test('TC-WB-019b: copyWith truyền updatedAt cố định nhận chính xác mốc thời gian', () {
        final explicitDate = DateTime(2026, 10, 5, 14, 0, 0);
        final res2 = note.copyWith(updatedAt: explicitDate);
        expect(res2.updatedAt, equals(explicitDate));
      });
    });

    // ══════════════════════════════════════════════════════════════════════
    // TC-WB-020 (P2): Note.fromMap fallback timestamps
    // ══════════════════════════════════════════════════════════════════════
    group('TC-WB-020 (P2): Note.fromMap fallback timestamps', () {
      test('TC-WB-020: Phòng thủ SQLite map thiếu created_at, updated_at, reminder trong Note.fromMap', () {
        final beforeCall = DateTime.now().millisecondsSinceEpoch;
        final map = <String, dynamic>{
          'id': 'legacy-note-99',
          'title': 'Ghi chú di sản',
          'content': 'Nội dung',
          'created_at': null,
          'updated_at': null,
          'reminder': null,
        };

        final note = Note.fromMap(map);
        final afterCall = DateTime.now().millisecondsSinceEpoch;

        expect(note.id, equals('legacy-note-99'));
        expect(note.title, equals('Ghi chú di sản'));
        expect(note.content, equals('Nội dung'));
        // Kiểm tra thời gian rơi chính xác trong khoảng [beforeCall, afterCall]
        expect(note.createdAt.millisecondsSinceEpoch >= beforeCall, isTrue);
        expect(note.createdAt.millisecondsSinceEpoch <= afterCall, isTrue);
        expect(note.updatedAt.millisecondsSinceEpoch >= beforeCall, isTrue);
        expect(note.updatedAt.millisecondsSinceEpoch <= afterCall, isTrue);
        expect(note.reminder, isNull);
      });
    });

    // ══════════════════════════════════════════════════════════════════════
    // Bổ trợ In-Memory (Ngoài 8 TC-WB): Note.toFirestoreMap Serialization
    // ══════════════════════════════════════════════════════════════════════
    group('Bổ trợ In-Memory (Ngoài 8 TC-WB): Note.toFirestoreMap Serialization', () {
      test('SUPP-NOTE-FS-01: toFirestoreMap chuyển đổi chính xác Timestamp và các trường cơ bản khi reminder là null', () {
        final created = DateTime(2026, 10, 1, 9, 0, 0);
        final updated = DateTime(2026, 10, 2, 10, 30, 0);
        final note = Note(
          id: 'fs-note-01',
          userId: 'u_fs_1',
          title: 'Firestore Note Test',
          content: 'Nội dung test Firestore map',
          status: 'pinned',
          isSynced: true,
          isLocked: false,
          noteColor: '#FF5733',
          tags: ['QA', 'Firestore'],
          imageUrls: ['https://example.com/img1.png'],
          audioUrls: ['https://example.com/audio1.mp3'],
          createdAt: created,
          updatedAt: updated,
          reminder: null,
        );

        final map = note.toFirestoreMap();

        expect(map['id'], equals('fs-note-01'));
        expect(map['user_id'], equals('u_fs_1'));
        expect(map['title'], equals('Firestore Note Test'));
        expect(map['content'], equals('Nội dung test Firestore map'));
        expect(map['status'], equals('pinned'));
        expect(map['is_locked'], isFalse);
        expect(map.containsKey('is_synced'), isFalse, reason: 'Firestore không lưu cờ is_synced của SQLite');
        expect(map['note_color'], equals('#FF5733'));
        expect(map['tags'], equals(['QA', 'Firestore']));
        expect(map['image_urls'], equals(['https://example.com/img1.png']));
        expect(map['audio_urls'], equals(['https://example.com/audio1.mp3']));
        expect(map['created_at'], isA<Timestamp>());
        expect((map['created_at'] as Timestamp).toDate(), equals(created));
        expect(map['updated_at'], isA<Timestamp>());
        expect((map['updated_at'] as Timestamp).toDate(), equals(updated));
        expect(map['reminder'], isNull);
      });

      test('SUPP-NOTE-FS-02: toFirestoreMap chuyển đổi chính xác Timestamp khi reminder có giá trị', () {
        final created = DateTime(2026, 10, 1, 9, 0, 0);
        final updated = DateTime(2026, 10, 2, 10, 30, 0);
        final reminderTime = DateTime(2026, 10, 15, 8, 0, 0);
        final note = Note(
          id: 'fs-note-02',
          userId: 'u_fs_2',
          title: 'Reminder Note',
          content: 'Nội dung có reminder',
          createdAt: created,
          updatedAt: updated,
          reminder: reminderTime,
        );

        final map = note.toFirestoreMap();

        expect(map['reminder'], isA<Timestamp>());
        expect((map['reminder'] as Timestamp).toDate(), equals(reminderTime));
      });
    });
  });
}
