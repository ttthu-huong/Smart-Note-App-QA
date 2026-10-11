// test/unit/search/search_notes_whitebox_test.dart
// White-box Testing: LocalNoteService.searchNotes() (FN-23 / REQ-08)
// Direct execution of production code against SQLite channel simulation
// Reproduces BUG-004: has:list unparsed token in LIKE query

import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:sqflite/sqflite.dart';
import 'package:sqflite/src/factory_impl.dart' as impl;
import 'package:smart_note_app/models/note_model.dart';
import 'package:smart_note_app/services/local_note_service.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late LocalNoteService localService;
  late List<Note> testNotes;
  String? lastCapturedSql;
  List<dynamic>? lastCapturedArgs;

  // Khởi tạo dataset chuẩn bị cho các ca kiểm thử hộp trắng Search
  final note1 = Note(
    id: 'n1',
    userId: 'u1',
    title: 'Học Flutter Cơ Bản',
    content: 'Tài liệu hướng dẫn lập trình Flutter cho người mới',
    createdAt: DateTime(2026, 10, 1),
    updatedAt: DateTime(2026, 10, 2),
    status: 'normal',
    tags: ['Học tập', 'Flutter'],
  );

  final note2WithImage = Note(
    id: 'n2',
    userId: 'u1',
    title: 'Thiết kế giao diện Figma',
    content: 'Bản vẽ Wireframe UI và ảnh mockup',
    createdAt: DateTime(2026, 10, 1),
    updatedAt: DateTime(2026, 10, 3),
    status: 'normal',
    imageUrls: ['https://cloudinary.com/figma_mockup.png'],
    tags: ['Thiết kế'],
  );

  final note3WithAudio = Note(
    id: 'n3',
    userId: 'u1',
    title: 'Ghi âm cuộc họp QA',
    content: 'Biên bản thảo luận kiểm thử hộp trắng McCabe',
    createdAt: DateTime(2026, 10, 1),
    updatedAt: DateTime(2026, 10, 4),
    status: 'normal',
    audioUrls: ['https://cloudinary.com/meeting_audio.m4a'],
    tags: ['Công việc'],
  );

  final note4WithUrl = Note(
    id: 'n4',
    userId: 'u1',
    title: 'Liên kết tham khảo',
    content: 'Xem thêm chi tiết tại trang web https://flutter.dev/docs',
    createdAt: DateTime(2026, 10, 1),
    updatedAt: DateTime(2026, 10, 5),
    status: 'normal',
    tags: ['Tài liệu'],
  );

  final note5Pinned = Note(
    id: 'n5',
    userId: 'u1',
    title: 'Mục tiêu quý 4',
    content: 'KPI đạt 100% độ bao phủ kiểm thử',
    createdAt: DateTime(2026, 10, 1),
    updatedAt: DateTime(2026, 10, 6),
    status: 'pinned',
    tags: ['Quan trọng'],
  );

  final note6Archived = Note(
    id: 'n6',
    userId: 'u1',
    title: 'Dự án cũ 2025',
    content: 'Tài liệu lưu trữ dự án trước',
    createdAt: DateTime(2026, 10, 1),
    updatedAt: DateTime(2026, 10, 7),
    status: 'archived',
    tags: ['Lưu trữ'],
  );

  final note7Trash = Note(
    id: 'n7',
    userId: 'u1',
    title: 'Ghi chú bỏ đi',
    content: 'Nội dung trong thùng rác',
    createdAt: DateTime(2026, 10, 1),
    updatedAt: DateTime(2026, 10, 8),
    status: 'trash',
  );

  final note8OtherUser = Note(
    id: 'n8',
    userId: 'u2',
    title: 'Note của user khác',
    content: 'User 2 Flutter data',
    createdAt: DateTime(2026, 10, 1),
    updatedAt: DateTime(2026, 10, 9),
    status: 'normal',
  );

  final note9Checklist = Note(
    id: 'n9',
    userId: 'u1',
    title: 'Danh sách công việc tuần',
    content: jsonEncode({
      'type': 'checklist',
      'items': [
        {'id': '1', 'text': 'Viết test Whitebox', 'checked': true},
        {'id': '2', 'text': 'Kiểm tra độ bao phủ', 'checked': false},
      ],
    }),
    createdAt: DateTime(2026, 10, 1),
    updatedAt: DateTime(2026, 10, 10),
    status: 'normal',
    tags: ['Kế hoạch'],
  );

  testNotes = [
    note1,
    note2WithImage,
    note3WithAudio,
    note4WithUrl,
    note5Pinned,
    note6Archived,
    note7Trash,
    note8OtherUser,
    note9Checklist,
  ];

  setUp(() {
    databaseFactory = impl.sqfliteDatabaseFactory;

    final channel = const MethodChannel('com.tekartik.sqflite');
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(
      channel,
      (MethodCall methodCall) async {
        if (methodCall.method == 'getDatabasesPath') {
          return '/mock/databases';
        }
        if (methodCall.method == 'openDatabase') {
          return 1;
        }
        if (methodCall.method == 'execute') {
          return null;
        }
        if (methodCall.method == 'query') {
          final args = methodCall.arguments as Map<dynamic, dynamic>? ?? {};
          final sql = (args['sql'] as String? ?? '').toLowerCase();
          final arguments = (args['arguments'] as List<dynamic>?) ?? [];
          lastCapturedSql = sql;
          lastCapturedArgs = arguments;

          if (sql.contains('user_version')) {
            return [
              {'user_version': 8}
            ];
          }

          // Giả lập cơ chế thực thi SQL query của SQLite trong production
          if (sql.contains('from notes')) {
            // Lọc theo where clause được sinh ra bởi production code LocalNoteService
            List<Note> matched = List.from(testNotes);

            // Kiểm tra user_id và status != trash
            if (arguments.isNotEmpty) {
              final targetUser = arguments[0] as String;
              matched = matched.where((n) => n.userId == targetUser).toList();
            }
            if (arguments.length > 1) {
              final notStatus = arguments[1] as String;
              matched = matched.where((n) => n.status != notStatus).toList();
            }

            // Kiểm tra SQL LIKE khi có cleanTextQuery
            if (arguments.length >= 4 && sql.contains('like')) {
              final rawLike = arguments[2] as String; // '%keyword%'
              final keyword = rawLike.replaceAll('%', '').toLowerCase();
              matched = matched.where((n) {
                final matchTitle = n.title.toLowerCase().contains(keyword);
                final matchContent = n.content.toLowerCase().contains(keyword);
                return matchTitle || matchContent;
              }).toList();
            }

            // Sắp xếp updated_at DESC như query production
            matched.sort((a, b) => b.updatedAt.compareTo(a.updatedAt));

            return matched.map((n) => n.toMap()).toList();
          }

          return [];
        }
        return null;
      },
    );

    localService = LocalNoteService();
  });

  group('FN-23: Kiểm thử Hộp trắng LocalNoteService.searchNotes() (Google Keep style)', () {
    test('TC-WB-SRCH-01: Query chuỗi rỗng / khoảng trắng trả về toàn bộ ghi chú (getAllNotes)', () async {
      final results = await localService.searchNotes(userId: 'u1', query: '   ');
      // u1 có 8 ghi chú, trong đó 1 ghi chú trash (n7) bị loại trừ -> còn 7
      expect(results.length, equals(7));
      expect(results.any((n) => n.status == 'trash'), isFalse);
    });

    test('TC-WB-SRCH-02: Tìm kiếm theo Tiêu đề (Title match)', () async {
      final results = await localService.searchNotes(userId: 'u1', query: 'Flutter');
      expect(results.any((n) => n.id == 'n1'), isTrue);
      final n1 = results.firstWhere((n) => n.id == 'n1');
      expect(n1.title, contains('Flutter'));
    });

    test('TC-WB-SRCH-03: Tìm kiếm theo Nội dung (Content match)', () async {
      final results = await localService.searchNotes(userId: 'u1', query: 'mccabe');
      expect(results.length, equals(1));
      expect(results.first.id, equals('n3'));
      expect(results.first.title, equals('Ghi âm cuộc họp QA'));
    });

    test('TC-WB-SRCH-04: Không phân biệt chữ hoa chữ thường (Case-insensitivity)', () async {
      final resultsUpper = await localService.searchNotes(userId: 'u1', query: 'FLUTTER');
      final resultsLower = await localService.searchNotes(userId: 'u1', query: 'flutter');
      expect(resultsUpper.length, equals(resultsLower.length));
      expect(resultsUpper.map((n) => n.id).toList(), equals(resultsLower.map((n) => n.id).toList()));
      expect(resultsUpper.any((n) => n.id == 'n1'), isTrue);
    });

    test('TC-WB-SRCH-05: Tự động loại trừ ghi chú trong Thùng rác (status != trash)', () async {
      final results = await localService.searchNotes(userId: 'u1', query: 'thùng rác');
      // n7 chứa chữ 'thùng rác' nhưng status là 'trash' nên phải bị loại trừ hoàn toàn
      expect(results.isEmpty, isTrue);
    });

    test('TC-WB-SRCH-06: Token Filter has:image (Chỉ lấy note có hình ảnh đính kèm)', () async {
      final results = await localService.searchNotes(userId: 'u1', query: 'has:image');
      expect(results.length, equals(1));
      expect(results.first.id, equals('n2'));
      expect(results.first.imageUrls.isNotEmpty, isTrue);
    });

    test('TC-WB-SRCH-07: Token Filter has:audio (Chỉ lấy note có tệp ghi âm)', () async {
      final results = await localService.searchNotes(userId: 'u1', query: 'has:audio');
      expect(results.length, equals(1));
      expect(results.first.id, equals('n3'));
      expect(results.first.audioUrls.isNotEmpty, isTrue);
    });

    test('TC-WB-SRCH-08: Token Filter has:url (Chỉ lấy note chứa URL hợp lệ trong nội dung)', () async {
      final results = await localService.searchNotes(userId: 'u1', query: 'has:url');
      expect(results.length, equals(1));
      expect(results.first.id, equals('n4'));
      expect(results.first.content, contains('https://'));
    });

    test('TC-WB-SRCH-09: Token Filter is:pinned (Chỉ lấy note đang được ghim)', () async {
      final results = await localService.searchNotes(userId: 'u1', query: 'is:pinned');
      expect(results.length, equals(1));
      expect(results.first.id, equals('n5'));
      expect(results.first.status, equals('pinned'));
    });

    test('TC-WB-SRCH-10: Token Filter is:archived vs Mặc định loại bỏ archived', () async {
      // 1. Khi có is:archived -> trả về note archived (n6)
      final archivedResults = await localService.searchNotes(userId: 'u1', query: 'is:archived');
      expect(archivedResults.length, equals(1));
      expect(archivedResults.first.id, equals('n6'));
      expect(archivedResults.first.status, equals('archived'));

      // 2. Khi tìm kiếm thông thường KHÔNG có is:archived -> note archived bị loại bỏ
      final normalResults = await localService.searchNotes(userId: 'u1', query: 'Dự án');
      expect(normalResults.any((n) => n.status == 'archived'), isFalse);
    });

    test('TC-WB-SRCH-11: Token Filter label:"..." (Bóc tách nhãn bằng Regex và lọc theo tags)', () async {
      final results = await localService.searchNotes(userId: 'u1', query: 'label:"Thiết kế"');
      expect(results.length, equals(1));
      expect(results.first.id, equals('n2'));
      expect(results.first.tags, contains('Thiết kế'));
    });

    test('TC-WB-SRCH-12: Kết hợp Text Query + Token Filter đồng thời', () async {
      final results = await localService.searchNotes(userId: 'u1', query: 'Figma has:image');
      expect(results.length, equals(1));
      expect(results.first.id, equals('n2'));
      expect(results.first.title, contains('Figma'));
      expect(results.first.imageUrls.isNotEmpty, isTrue);
    });

    test('TC-WB-SRCH-13: Phân tách dữ liệu nhiều người dùng theo userId', () async {
      // u1 và u2 đều có note chứa chữ 'Flutter'
      final resultsU1 = await localService.searchNotes(userId: 'u1', query: 'Flutter');
      final resultsU2 = await localService.searchNotes(userId: 'u2', query: 'Flutter');

      expect(resultsU1.every((n) => n.userId == 'u1'), isTrue);
      expect(resultsU2.every((n) => n.userId == 'u2'), isTrue);
      expect(resultsU2.first.id, equals('n8'));
    });

    test('TC-WB-SRCH-14: Xử lý ký tự đặc biệt SQL LIKE (% và _) — Phân tích SQL Generator vs Engine', () async {
      // 1. Kiểm tra với ký tự '%'
      final resultsPercent = await localService.searchNotes(userId: 'u1', query: '%');
      expect(resultsPercent, isA<List<Note>>());
      // Xác minh SQL Generator của production code: đưa trực tiếp '%%%' vào whereArgs mà không escape
      expect(lastCapturedSql, contains('like ? or lower(content) like ?'));
      expect(lastCapturedArgs, equals(['u1', 'trash', '%%%', '%%%']),
          reason: 'Production code đưa trực tiếp chuỗi %%% vào SQL mà không dùng mệnh đề ESCAPE');

      // 2. Kiểm tra với ký tự '_'
      final resultsUnderscore = await localService.searchNotes(userId: 'u1', query: '_');
      expect(resultsUnderscore, isA<List<Note>>());
      // Xác minh SQL Generator của production code: đưa trực tiếp '%_%' vào whereArgs mà không escape
      expect(lastCapturedArgs, equals(['u1', 'trash', '%_%', '%_%']),
          reason: 'Production code đưa trực tiếp chuỗi %_% vào SQL mà không dùng mệnh đề ESCAPE');
    });

    // ══════════════════════════════════════════════════════════════════════
    // BUG-004 REPRODUCTION TEST (REQ-08 / TC-BB-027G-D01)
    // ══════════════════════════════════════════════════════════════════════
    test('TC-WB-SRCH-15 (BUG-004): Token Filter has:list phải bóc tách token và trả về checklist notes', () async {
      // THEO ĐẶC TẢ REQ-08 & TC-BB-027G-D01:
      // Khi người dùng bấm chip 'Danh sách' (hoặc gõ has:list), hệ thống phải bóc tách token has:list
      // và lọc trả về các ghi chú checklist (n9).
      //
      // THỰC TẾ TRONG PRODUCTION CODE (local_note_service.dart L175-189):
      // - hasImageToken, hasAudioToken, hasUrlToken, isPinnedToken, isArchivedToken được bóc tách và xóa khỏi cleanTextQuery.
      // - NHƯNG has:list KHÔNG ĐƯỢC XỬ LÝ!
      // - Do đó cleanTextQuery bị gán bằng "has:list" thô và đẩy vào SQL LIKE:
      //   LOWER(title) LIKE '%has:list%' OR LOWER(content) LIKE '%has:list%'
      // - Ghi chú checklist n9 không chứa từ "has:list" trong văn bản nên SQL trả về rỗng []!
      // - Ghi nhận lỗi BUG-004 (FAIL như mong đợi trong White-box testing để tái hiện lỗi).
      final results = await localService.searchNotes(userId: 'u1', query: 'has:list');

      // Expected Result theo SRS: Phải tìm thấy ghi chú checklist n9
      expect(results.length, equals(1), reason: 'BUG-004: has:list phải trả về ghi chú checklist thay vì rỗng do LIKE thô');
      expect(results.first.id, equals('n9'));
      expect(results.first.isChecklist, isTrue);
    });
  });
}
