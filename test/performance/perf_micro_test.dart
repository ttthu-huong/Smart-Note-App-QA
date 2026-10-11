import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:smart_note_app/models/note_model.dart';

void main() {
  group('PERF-05 & PERF-06: Logic & Data Processing Micro-benchmarks', () {
    test('PERF-06: Parse & xử lý Quill Delta JSON kích thước lớn', () {
      // Sinh payload 100KB, 500KB
      final buffer = StringBuffer('{"ops":[');
      for (int i = 0; i < 2000; i++) {
        buffer.write('{"insert":"Đây là đoạn văn bản ghi chú hiệu năng dòng $i\\n"},');
      }
      buffer.write('{"insert":"Hết."}]}');
      final deltaJson = buffer.toString();
      final sizeKb = deltaJson.length / 1024;

      final sw = Stopwatch()..start();
      final decoded = jsonDecode(deltaJson);
      sw.stop();

      print('⏱️ Parse Delta JSON (${sizeKb.toStringAsFixed(1)} KB): ${sw.elapsedMicroseconds / 1000} ms');
      expect(decoded, isNotNull);
      expect(sw.elapsedMilliseconds, lessThan(200));
    });

    test('PERF-05: Giải quyết xung đột Last-Writer-Wins với tập dữ liệu lớn', () {
      final now = DateTime.now();
      final localNotes = List.generate(
        1000,
        (i) => Note(
          id: 'note_$i',
          userId: 'user_1',
          title: 'Title $i',
          content: 'Content $i',
          createdAt: now.subtract(Duration(days: 1)),
          updatedAt: now.add(Duration(seconds: i % 2 == 0 ? 10 : -10)),
        ),
      );

      final cloudNotes = List.generate(
        1000,
        (i) => Note(
          id: 'note_$i',
          userId: 'user_1',
          title: 'Cloud Title $i',
          content: 'Cloud Content $i',
          createdAt: now.subtract(Duration(days: 1)),
          updatedAt: now,
        ),
      );

      final cloudMap = {for (final n in cloudNotes) n.id: n};

      final sw = Stopwatch()..start();
      final notesToPush = <Note>[];
      for (final local in localNotes) {
        final cloud = cloudMap[local.id];
        if (cloud == null || local.updatedAt.isAfter(cloud.updatedAt)) {
          notesToPush.add(local);
        }
      }
      sw.stop();

      print('⏱️ LWW Conflict Resolution (1000 items): ${sw.elapsedMicroseconds / 1000} ms');
      expect(notesToPush.length, equals(500));
      expect(sw.elapsedMilliseconds, lessThan(100));
    });
  });
}
