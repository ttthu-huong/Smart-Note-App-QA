import 'package:flutter_test/flutter_test.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import 'package:smart_note_app/models/note_model.dart';
import 'package:smart_note_app/services/local_note_service.dart';

void main() {
  setUpAll(() {
    sqfliteFfiInit();
    databaseFactory = databaseFactoryFfi;
  });

  group('CHƯƠNG 6.3: THỰC NGHIỆM KIỂM THỬ HIỆU NĂNG TẦNG 1 (SQLITE & LOGIC)', () {
    late Database db;
    late LocalNoteService service;

    setUp(() async {
      db = await databaseFactoryFfi.openDatabase(
        inMemoryDatabasePath,
        options: OpenDatabaseOptions(
          version: 8,
          onCreate: (db, version) async {
            await db.execute('''
              CREATE TABLE notes(
                id TEXT PRIMARY KEY,
                user_id TEXT DEFAULT '',
                title TEXT,
                content TEXT,
                status TEXT DEFAULT 'normal',
                is_synced INTEGER DEFAULT 0,
                is_locked INTEGER DEFAULT 0,
                note_color TEXT,
                tags TEXT,
                image_urls TEXT,
                audio_urls TEXT,          
                created_at INTEGER,
                updated_at INTEGER,
                reminder INTEGER
              )
            ''');
            await db.execute('CREATE INDEX idx_notes_user_status ON notes(user_id, status)');
            await db.execute('CREATE INDEX idx_notes_user_synced ON notes(user_id, is_synced)');
          },
        ),
      );
      service = LocalNoteService(customDb: db);
    });

    tearDown(() async {
      await db.close();
    });

    test('PERF-01: Ghi hàng loạt (Bulk Insert) 100, 1.000, 5.000, 10.000 ghi chú', () async {
      final counts = [100, 1000, 5000, 10000];
      final results = <int, double>{};

      for (final n in counts) {
        await db.delete('notes'); // Clear
        final notes = List.generate(
          n,
          (i) => Note(
            id: 'note_$i',
            userId: 'user_perf',
            title: 'Tiêu đề ghi chú kiểm thử số $i',
            content: 'Nội dung chi tiết của ghi chú hiệu năng số $i phục vụ đo đạc SQLite.',
            status: 'normal',
            createdAt: DateTime.now(),
            updatedAt: DateTime.now(),
          ),
        );

        final sw = Stopwatch()..start();
        final batch = db.batch();
        for (final note in notes) {
          batch.insert('notes', note.toMap(), conflictAlgorithm: ConflictAlgorithm.replace);
        }
        await batch.commit(noResult: true);
        sw.stop();

        final avgMsPerNote = sw.elapsedMicroseconds / 1000 / n;
        results[n] = sw.elapsedMilliseconds.toDouble();
        print('📊 PERF-01 [N = $n]: Tổng thời gian = ${sw.elapsedMilliseconds} ms | TB/note = ${avgMsPerNote.toStringAsFixed(3)} ms');
        expect(avgMsPerNote, lessThan(5.0)); // SLA < 5ms / note
      }
    });

    test('PERF-02: Truy vấn phân trang (getAllNotes) khi CSDL có 10.000 ghi chú', () async {
      // Nạp 10.000 ghi chú
      final batch = db.batch();
      for (int i = 0; i < 10000; i++) {
        batch.insert('notes', {
          'id': 'note_$i',
          'user_id': 'user_perf',
          'title': 'Ghi chú số $i',
          'content': 'Nội dung số $i',
          'status': 'normal',
          'is_synced': 1,
          'created_at': DateTime.now().millisecondsSinceEpoch,
          'updated_at': DateTime.now().millisecondsSinceEpoch,
        });
      }
      await batch.commit(noResult: true);

      // Đo thời gian truy vấn trang đầu (LIMIT 20 OFFSET 0)
      final sw1 = Stopwatch()..start();
      final page1 = await service.getAllNotes(userId: 'user_perf', limit: 20, offset: 0);
      sw1.stop();
      print('📊 PERF-02 [Page 1 (LIMIT 20 OFFSET 0)]: ${sw1.elapsedMicroseconds / 1000} ms (Số lượng = ${page1.length})');
      expect(sw1.elapsedMilliseconds, lessThan(50)); // SLA < 50ms

      // Đo thời gian truy vấn trang sâu (LIMIT 20 OFFSET 5000)
      final sw2 = Stopwatch()..start();
      final pageDeep = await service.getAllNotes(userId: 'user_perf', limit: 20, offset: 5000);
      sw2.stop();
      print('📊 PERF-02 [Deep Page (OFFSET 5000)]: ${sw2.elapsedMicroseconds / 1000} ms (Số lượng = ${pageDeep.length})');
      expect(pageDeep.length, equals(20));
    });

    test('PERF-03: Tìm kiếm văn bản (searchNotes LIKE) trên quy mô 10.000 ghi chú', () async {
      final batch = db.batch();
      for (int i = 0; i < 10000; i++) {
        batch.insert('notes', {
          'id': 'note_$i',
          'user_id': 'user_perf',
          'title': i == 8888 ? 'Tu khoa docnhat can tim' : 'Tiêu đề thông thường $i',
          'content': 'Nội dung ngẫu nhiên $i',
          'status': 'normal',
          'created_at': DateTime.now().millisecondsSinceEpoch,
          'updated_at': DateTime.now().millisecondsSinceEpoch,
        });
      }
      await batch.commit(noResult: true);

      final sw = Stopwatch()..start();
      final searchResult = await service.searchNotes(userId: 'user_perf', query: 'docnhat');
      sw.stop();

      print('📊 PERF-03 [Tìm kiếm LIKE trên 10.000 notes]: ${sw.elapsedMicroseconds / 1000} ms | Tìm thấy = ${searchResult.length}');
      expect(searchResult.length, equals(1));
      expect(sw.elapsedMilliseconds, lessThan(300)); // SLA < 300ms
    });

    test('PERF-04: Đo lường mức cải thiện hiệu năng khi có Index (idx_notes_user_status)', () async {
      // 1. Đo khi CÓ INDEX
      final batch = db.batch();
      for (int i = 0; i < 10000; i++) {
        batch.insert('notes', {
          'id': 'note_$i',
          'user_id': 'user_perf',
          'title': 'Ghi chú $i',
          'content': 'Nội dung $i',
          'status': i % 10 == 0 ? 'pinned' : 'normal',
          'created_at': DateTime.now().millisecondsSinceEpoch,
          'updated_at': DateTime.now().millisecondsSinceEpoch,
        });
      }
      await batch.commit(noResult: true);

      final swWithIndex = Stopwatch()..start();
      final withIndexResult = await db.query(
        'notes',
        where: 'user_id = ? AND status = ?',
        whereArgs: ['user_perf', 'pinned'],
      );
      swWithIndex.stop();
      final timeWithIndex = swWithIndex.elapsedMicroseconds / 1000;

      // 2. Xóa index để đo khi KHÔNG CÓ INDEX
      await db.execute('DROP INDEX idx_notes_user_status');
      final swNoIndex = Stopwatch()..start();
      final noIndexResult = await db.query(
        'notes',
        where: 'user_id = ? AND status = ?',
        whereArgs: ['user_perf', 'pinned'],
      );
      swNoIndex.stop();
      final timeNoIndex = swNoIndex.elapsedMicroseconds / 1000;

      final speedup = timeNoIndex > 0 && timeWithIndex > 0 ? (timeNoIndex / timeWithIndex) : 1.0;
      print('📊 PERF-04: Có Index = ${timeWithIndex} ms | Không Index = ${timeNoIndex} ms | Tăng tốc = ${speedup.toStringAsFixed(1)}x');
      expect(withIndexResult.length, equals(noIndexResult.length));
    });
  });
}
