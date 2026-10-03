import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:sqflite/sqflite.dart';
import 'package:smart_note_app/models/note_model.dart';
import 'package:smart_note_app/services/local_note_service.dart';
import 'package:smart_note_app/repositories/note_repository.dart';
import 'package:smart_note_app/providers/note_provider.dart';

class MockDatabase extends Mock implements Database {}
class MockLocalNoteService extends Mock implements LocalNoteService {}
class MockNoteRepository extends Mock implements NoteRepository {}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late MockDatabase mockDb;
  late LocalNoteService localService;

  final note1 = Note(
    id: 'n1',
    userId: 'u1',
    title: 'Học Flutter Cơ Bản',
    content: 'Tài liệu hướng dẫn lập trình Flutter cho người mới',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
    status: 'normal',
    tags: ['Học tập', 'Flutter'],
  );

  final note2WithImage = Note(
    id: 'n2',
    userId: 'u1',
    title: 'Thiết kế giao diện Figma',
    content: 'Bản vẽ Wireframe UI và ảnh mockup',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
    status: 'normal',
    imageUrls: ['https://cloudinary.com/figma_mockup.png'],
    tags: ['Thiết kế'],
  );

  final note3WithAudio = Note(
    id: 'n3',
    userId: 'u1',
    title: 'Ghi âm cuộc họp QA',
    content: 'Biên bản thảo luận kiểm thử hộp trắng McCabe',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
    status: 'normal',
    audioUrls: ['https://cloudinary.com/meeting_audio.m4a'],
    tags: ['Công việc'],
  );

  final note4WithUrl = Note(
    id: 'n4',
    userId: 'u1',
    title: 'Liên kết tham khảo',
    content: 'Xem thêm chi tiết tại trang web https://flutter.dev/docs',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
    status: 'normal',
    tags: ['Tài liệu'],
  );

  final note5Pinned = Note(
    id: 'n5',
    userId: 'u1',
    title: 'Mục tiêu quý 4',
    content: 'KPI đạt 100% độ bao phủ kiểm thử',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
    status: 'pinned',
    tags: ['Quan trọng'],
  );

  final note6Archived = Note(
    id: 'n6',
    userId: 'u1',
    title: 'Dự án cũ 2025',
    content: 'Tài liệu lưu trữ dự án trước',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
    status: 'archived',
    tags: ['Lưu trữ'],
  );

  final note7Trash = Note(
    id: 'n7',
    userId: 'u1',
    title: 'Ghi chú bỏ đi',
    content: 'Nội dung trong thùng rác',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
    status: 'trash',
  );

  final allNotesList = [
    note1,
    note2WithImage,
    note3WithAudio,
    note4WithUrl,
    note5Pinned,
    note6Archived,
    note7Trash,
  ];

  setUp(() {
    mockDb = MockDatabase();
    localService = LocalNoteService(customDb: mockDb);
  });

  group('FN-23: Kiểm thử Hộp trắng LocalNoteService.searchNotes() (Google Keep style)', () {
    test('TC-WB-SRCH-01: Path 1 - Truy vấn chuỗi rỗng: Trả về toàn bộ danh sách ghi chú (getAllNotes)', () async {
      when(() => mockDb.query(
        'notes',
        where: any(named: 'where'),
        whereArgs: any(named: 'whereArgs'),
        orderBy: any(named: 'orderBy'),
        limit: any(named: 'limit'),
        offset: any(named: 'offset'),
      )).thenAnswer((_) async => allNotesList.map((n) => n.toMap()).toList());

      final results = await localService.searchNotes(userId: 'u1', query: '   ');

      expect(results.length, equals(allNotesList.length));
      verify(() => mockDb.query(
        'notes',
        where: 'user_id = ? AND status != ?',
        whereArgs: ['u1', 'trash'],
        orderBy: any(named: 'orderBy'),
        limit: any(named: 'limit'),
        offset: any(named: 'offset'),
      )).called(1);
    });

    test('TC-WB-SRCH-02: Path 2 - Tìm kiếm theo Tiêu đề (SQL LIKE query với text title)', () async {
      when(() => mockDb.query(
        'notes',
        where: any(named: 'where'),
        whereArgs: any(named: 'whereArgs'),
        orderBy: any(named: 'orderBy'),
      )).thenAnswer((_) async => [note1.toMap()]);

      final results = await localService.searchNotes(userId: 'u1', query: 'Flutter');

      expect(results.length, equals(1));
      expect(results.first.id, equals('n1'));
      verify(() => mockDb.query(
        'notes',
        where: 'user_id = ? AND status != ? AND (LOWER(title) LIKE ? OR LOWER(content) LIKE ?)',
        whereArgs: ['u1', 'trash', '%flutter%', '%flutter%'],
        orderBy: 'updated_at DESC',
      )).called(1);
    });

    test('TC-WB-SRCH-03: Path 3 - Tìm kiếm theo Nội dung (Content match)', () async {
      when(() => mockDb.query(
        'notes',
        where: any(named: 'where'),
        whereArgs: any(named: 'whereArgs'),
        orderBy: any(named: 'orderBy'),
      )).thenAnswer((_) async => [note3WithAudio.toMap()]);

      final results = await localService.searchNotes(userId: 'u1', query: 'mccabe');

      expect(results.length, equals(1));
      expect(results.first.title, contains('QA'));
    });

    test('TC-WB-SRCH-04: Path 4 - Không phân biệt chữ hoa chữ thường (Case-insensitivity)', () async {
      when(() => mockDb.query(
        'notes',
        where: any(named: 'where'),
        whereArgs: any(named: 'whereArgs'),
        orderBy: any(named: 'orderBy'),
      )).thenAnswer((_) async => [note1.toMap()]);

      final results = await localService.searchNotes(userId: 'u1', query: 'FLUTTER');

      expect(results.length, equals(1));
      expect(results.first.id, equals('n1'));
    });

    test('TC-WB-SRCH-05: Path 5 - Tự động loại trừ ghi chú trong Thùng rác (status != trash)', () async {
      when(() => mockDb.query(
        'notes',
        where: any(named: 'where'),
        whereArgs: any(named: 'whereArgs'),
        orderBy: any(named: 'orderBy'),
      )).thenAnswer((invocation) async {
        final where = invocation.namedArguments[#where] as String;
        expect(where, contains('status != ?'));
        return [note1.toMap()];
      });

      final results = await localService.searchNotes(userId: 'u1', query: 'ghi chú');
      expect(results.any((n) => n.status == 'trash'), isFalse);
    });

    test('TC-WB-SRCH-06: Path 6 - Token Filter has:image (Chỉ lấy note có hình ảnh đính kèm)', () async {
      when(() => mockDb.query(
        'notes',
        where: any(named: 'where'),
        whereArgs: any(named: 'whereArgs'),
        orderBy: any(named: 'orderBy'),
      )).thenAnswer((_) async => [note1.toMap(), note2WithImage.toMap()]);

      final results = await localService.searchNotes(userId: 'u1', query: 'has:image');

      expect(results.length, equals(1));
      expect(results.first.id, equals('n2'));
      expect(results.first.imageUrls.isNotEmpty, isTrue);
    });

    test('TC-WB-SRCH-07: Path 7 - Token Filter has:audio (Chỉ lấy note có tệp ghi âm)', () async {
      when(() => mockDb.query(
        'notes',
        where: any(named: 'where'),
        whereArgs: any(named: 'whereArgs'),
        orderBy: any(named: 'orderBy'),
      )).thenAnswer((_) async => [note1.toMap(), note3WithAudio.toMap()]);

      final results = await localService.searchNotes(userId: 'u1', query: 'has:audio');

      expect(results.length, equals(1));
      expect(results.first.id, equals('n3'));
      expect(results.first.audioUrls.isNotEmpty, isTrue);
    });

    test('TC-WB-SRCH-08: Path 8 - Token Filter has:url (Chỉ lấy note chứa URL hợp lệ)', () async {
      when(() => mockDb.query(
        'notes',
        where: any(named: 'where'),
        whereArgs: any(named: 'whereArgs'),
        orderBy: any(named: 'orderBy'),
      )).thenAnswer((_) async => [note1.toMap(), note4WithUrl.toMap()]);

      final results = await localService.searchNotes(userId: 'u1', query: 'has:url');

      expect(results.length, equals(1));
      expect(results.first.id, equals('n4'));
      expect(results.first.content, contains('https://'));
    });

    test('TC-WB-SRCH-09: Path 9 - Token Filter is:pinned (Chỉ lấy note đang được ghim)', () async {
      when(() => mockDb.query(
        'notes',
        where: any(named: 'where'),
        whereArgs: any(named: 'whereArgs'),
        orderBy: any(named: 'orderBy'),
      )).thenAnswer((_) async => [note1.toMap(), note5Pinned.toMap()]);

      final results = await localService.searchNotes(userId: 'u1', query: 'is:pinned');

      expect(results.length, equals(1));
      expect(results.first.id, equals('n5'));
      expect(results.first.status, equals('pinned'));
    });

    test('TC-WB-SRCH-10: Path 10 - Token Filter is:archived vs Mặc định loại bỏ archived', () async {
      // 1. Khi có is:archived -> trả về note archived
      when(() => mockDb.query(
        'notes',
        where: any(named: 'where'),
        whereArgs: any(named: 'whereArgs'),
        orderBy: any(named: 'orderBy'),
      )).thenAnswer((_) async => [note1.toMap(), note6Archived.toMap()]);

      final archivedResults = await localService.searchNotes(userId: 'u1', query: 'is:archived');
      expect(archivedResults.length, equals(1));
      expect(archivedResults.first.status, equals('archived'));

      // 2. Khi KHÔNG có is:archived -> tự động lọc bỏ note archived
      final normalResults = await localService.searchNotes(userId: 'u1', query: 'Dự án');
      expect(normalResults.any((n) => n.status == 'archived'), isFalse);
    });

    test('TC-WB-SRCH-11: Path 11 - Token Filter label:"..." (Bóc tách nhãn bằng Regex và lọc)', () async {
      when(() => mockDb.query(
        'notes',
        where: any(named: 'where'),
        whereArgs: any(named: 'whereArgs'),
        orderBy: any(named: 'orderBy'),
      )).thenAnswer((_) async => [note1.toMap(), note2WithImage.toMap()]);

      final results = await localService.searchNotes(userId: 'u1', query: 'label:"Thiết kế"');

      expect(results.length, equals(1));
      expect(results.first.tags, contains('Thiết kế'));
    });

    test('TC-WB-SRCH-12: Path 12 - Kết hợp Text Query + Token Filter đồng thời', () async {
      when(() => mockDb.query(
        'notes',
        where: any(named: 'where'),
        whereArgs: any(named: 'whereArgs'),
        orderBy: any(named: 'orderBy'),
      )).thenAnswer((_) async => [note2WithImage.toMap()]);

      final results = await localService.searchNotes(userId: 'u1', query: 'Figma has:image');

      expect(results.length, equals(1));
      expect(results.first.title, contains('Figma'));
      expect(results.first.imageUrls.isNotEmpty, isTrue);
    });
  });

  group('Kiểm thử Hộp trắng Tầng Provider (NoteProvider.search & clearSearch)', () {
    late MockNoteRepository mockRepo;
    late NoteProvider provider;

    setUp(() {
      mockRepo = MockNoteRepository();
      provider = NoteProvider(mockRepo);
    });

    test('TC-WB-SRCH-13: NoteProvider.search() bật cờ isSearching & Debounce tìm kiếm qua Repository', () async {
      when(() => mockRepo.searchNotes(userId: 'u1', query: 'Flutter'))
          .thenAnswer((_) async => [note1]);

      expect(provider.isSearching, isFalse);

      // Kích hoạt tìm kiếm
      provider.search('Flutter', 'u1');
      expect(provider.isSearching, isTrue);

      // Chờ Debounce 400ms hoàn tất
      await Future.delayed(const Duration(milliseconds: 500));

      expect(provider.notes.length, equals(1));
      expect(provider.notes.first.id, equals('n1'));
      verify(() => mockRepo.searchNotes(userId: 'u1', query: 'Flutter')).called(1);
    });

    test('TC-WB-SRCH-14: NoteProvider.clearSearch() hủy debounce, tắt cờ isSearching và xóa kết quả lọc', () async {
      provider.search('temp', 'u1');
      expect(provider.isSearching, isTrue);

      // Xóa tìm kiếm ngay
      provider.clearSearch();

      expect(provider.isSearching, isFalse);
      expect(provider.notes.isEmpty, isTrue);
    });
  });
}
