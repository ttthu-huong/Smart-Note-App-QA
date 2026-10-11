import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:smart_note_app/models/note_model.dart';

void main() {
  group('Note Model Serialization & Deserialization Unit Tests', () {
    test('should serialize toMap and deserialize fromMap with full data round-trip', () {
      final now = DateTime.now();
      final created = now.subtract(const Duration(days: 2));
      final updated = now.subtract(const Duration(hours: 3));
      final reminderTime = now.add(const Duration(days: 5));

      final originalNote = Note(
        id: 'note-full-001',
        userId: 'user-xyz',
        title: 'Full Note Title',
        content: 'Full Note Content with text and symbols',
        status: 'archived',
        isSynced: true,
        isLocked: true,
        noteColor: '#FFEEDD',
        tags: const ['work', 'urgent', 'flutter'],
        imageUrls: const ['https://example.com/img1.jpg', 'https://example.com/img2.png'],
        audioUrls: const ['https://example.com/voice1.m4a'],
        reminder: reminderTime,
        createdAt: created,
        updatedAt: updated,
      );

      // Verify toMap
      final map = originalNote.toMap();
      expect(map['id'], 'note-full-001');
      expect(map['user_id'], 'user-xyz');
      expect(map['title'], 'Full Note Title');
      expect(map['content'], 'Full Note Content with text and symbols');
      expect(map['status'], 'archived');
      expect(map['is_synced'], 1);
      expect(map['is_locked'], 1);
      expect(map['note_color'], '#FFEEDD');
      expect(map['tags'], jsonEncode(['work', 'urgent', 'flutter']));
      expect(map['image_urls'], jsonEncode(['https://example.com/img1.jpg', 'https://example.com/img2.png']));
      expect(map['audio_urls'], jsonEncode(['https://example.com/voice1.m4a']));
      expect(map['created_at'], created.millisecondsSinceEpoch);
      expect(map['updated_at'], updated.millisecondsSinceEpoch);
      expect(map['reminder'], reminderTime.millisecondsSinceEpoch);

      // Verify fromMap round-trip
      final restoredNote = Note.fromMap(map);
      expect(restoredNote.id, originalNote.id);
      expect(restoredNote.userId, originalNote.userId);
      expect(restoredNote.title, originalNote.title);
      expect(restoredNote.content, originalNote.content);
      expect(restoredNote.status, originalNote.status);
      expect(restoredNote.isSynced, isTrue);
      expect(restoredNote.isLocked, isTrue);
      expect(restoredNote.noteColor, '#FFEEDD');
      expect(restoredNote.tags, originalNote.tags);
      expect(restoredNote.imageUrls, originalNote.imageUrls);
      expect(restoredNote.audioUrls, originalNote.audioUrls);
      expect(restoredNote.createdAt.millisecondsSinceEpoch, created.millisecondsSinceEpoch);
      expect(restoredNote.updatedAt.millisecondsSinceEpoch, updated.millisecondsSinceEpoch);
      expect(restoredNote.reminder?.millisecondsSinceEpoch, reminderTime.millisecondsSinceEpoch);
    });

    test('should apply default values when minimal map is provided to fromMap', () {
      final minimalMap = {
        'id': 'note-min-002',
        'title': 'Minimal Note',
        'content': 'Just text',
      };

      final note = Note.fromMap(minimalMap);
      expect(note.id, 'note-min-002');
      expect(note.userId, '');
      expect(note.title, 'Minimal Note');
      expect(note.content, 'Just text');
      expect(note.status, 'normal');
      expect(note.isSynced, isFalse);
      expect(note.isLocked, isFalse);
      expect(note.noteColor, isNull);
      expect(note.tags, isEmpty);
      expect(note.imageUrls, isEmpty);
      expect(note.audioUrls, isEmpty);
      expect(note.reminder, isNull);
      expect(note.createdAt, isNotNull);
      expect(note.updatedAt, isNotNull);
    });

    test('should serialize toMap with null reminder and false booleans correctly', () {
      final note = Note(
        id: 'note-003',
        title: 'No Reminder Note',
        content: 'Content',
        isSynced: false,
        isLocked: false,
        reminder: null,
      );

      final map = note.toMap();
      expect(map['is_synced'], 0);
      expect(map['is_locked'], 0);
      expect(map['reminder'], isNull);

      final restored = Note.fromMap(map);
      expect(restored.isSynced, isFalse);
      expect(restored.isLocked, isFalse);
      expect(restored.reminder, isNull);
    });

    test('should support noteColor fallback when note_color key is absent in fromMap', () {
      final mapWithCamelCase = {
        'id': 'note-color-004',
        'title': 'Color Note',
        'content': 'Content',
        'noteColor': '#00FFAA',
      };

      final note = Note.fromMap(mapWithCamelCase);
      expect(note.noteColor, '#00FFAA');

      final mapWithoutAnyColor = {
        'id': 'note-color-005',
        'title': 'No Color',
        'content': 'Content',
      };
      final noteNoColor = Note.fromMap(mapWithoutAnyColor);
      expect(noteNoColor.noteColor, isNull);
    });

    test('should decode string lists when values are null or empty string in fromMap', () {
      final map = {
        'id': 'note-empty-006',
        'title': 'Empty Lists',
        'content': 'Content',
        'tags': null,
        'image_urls': '',
        'audio_urls': null,
      };

      final note = Note.fromMap(map);
      expect(note.tags, isEmpty);
      expect(note.imageUrls, isEmpty);
      expect(note.audioUrls, isEmpty);
    });

    test('should decode string lists from valid JSON encoded arrays in fromMap', () {
      final map = {
        'id': 'note-json-007',
        'title': 'JSON Lists',
        'content': 'Content',
        'tags': jsonEncode(['feature', 'qa', 'mobile']),
        'image_urls': jsonEncode(['https://cdn.example.com/p1.jpg']),
        'audio_urls': jsonEncode(['https://cdn.example.com/rec1.aac']),
      };

      final note = Note.fromMap(map);
      expect(note.tags, ['feature', 'qa', 'mobile']);
      expect(note.imageUrls, ['https://cdn.example.com/p1.jpg']);
      expect(note.audioUrls, ['https://cdn.example.com/rec1.aac']);
    });

    test('should fallback to comma-separated values (CSV) when JSON decode fails in fromMap', () {
      final map = {
        'id': 'note-csv-008',
        'title': 'CSV Legacy Lists',
        'content': 'Content',
        'tags': 'home,shopping,weekend',
        'image_urls': 'https://old.com/1.jpg,,https://old.com/2.jpg,',
        'audio_urls': ',,,',
      };

      final note = Note.fromMap(map);
      expect(note.tags, ['home', 'shopping', 'weekend']);
      expect(note.imageUrls, ['https://old.com/1.jpg', 'https://old.com/2.jpg']);
      expect(note.audioUrls, isEmpty);
    });

    test('should safely return empty list for non-list JSON strings and non-string inputs in fromMap', () {
      final map = {
        'id': 'note-edge-009',
        'title': 'Edge Data Types',
        'content': 'Content',
        'tags': '{"objectKey": "notAList"}',
        'image_urls': '123456',
        'audio_urls': 98765,
      };

      final note = Note.fromMap(map);
      expect(note.tags, isEmpty);
      expect(note.imageUrls, isEmpty);
      expect(note.audioUrls, isEmpty);
    });

    test('should correctly parse boolean flag integer variants in fromMap', () {
      final map1 = {
        'id': 'note-bool-010',
        'title': 'Bool Tests 1',
        'content': 'Content',
        'is_synced': 1,
        'is_locked': 0,
      };
      final note1 = Note.fromMap(map1);
      expect(note1.isSynced, isTrue);
      expect(note1.isLocked, isFalse);

      final map2 = {
        'id': 'note-bool-011',
        'title': 'Bool Tests 2',
        'content': 'Content',
        'is_synced': 0,
        'is_locked': 1,
      };
      final note2 = Note.fromMap(map2);
      expect(note2.isSynced, isFalse);
      expect(note2.isLocked, isTrue);

      final map3 = {
        'id': 'note-bool-012',
        'title': 'Bool Tests 3',
        'content': 'Content',
        'is_synced': 99, // non-1 integer
        'is_locked': null,
      };
      final note3 = Note.fromMap(map3);
      expect(note3.isSynced, isFalse);
      expect(note3.isLocked, isFalse);
    });
  });
}
