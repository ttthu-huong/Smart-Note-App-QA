import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:sqflite/sqflite.dart';
import 'package:smart_note_app/models/note_model.dart';
import 'package:smart_note_app/services/local_note_service.dart';
import 'package:smart_note_app/services/firestore_note_service.dart';
import 'package:smart_note_app/services/pending_delete_service.dart';
import 'package:smart_note_app/repositories/note_repository.dart';

class MockLocalNoteService extends Mock implements LocalNoteService {}
class MockFirestoreNoteService extends Mock implements FirestoreNoteService {}
class MockPendingDeleteService extends Mock implements PendingDeleteService {}
class MockDatabase extends Mock implements Database {}

void main() {
  setUpAll(() {
    registerFallbackValue(Note(
      id: 'fallback_id',
      userId: 'user_1',
      title: 'fallback_title',
      content: 'fallback_content',
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    ));
  });

  group('FN-08 & FN-09: Kiểm thử Hộp trắng NoteRepositoryImpl.saveNote() (Tạo & Sửa Note)', () {
    late MockLocalNoteService mockLocal;
    late MockFirestoreNoteService mockFirestore;
    late MockPendingDeleteService mockPending;

    setUp(() {
      mockLocal = MockLocalNoteService();
      mockFirestore = MockFirestoreNoteService();
      mockPending = MockPendingDeleteService();
    });

    test('TC-WB-NOTE-01: Path 1 - Tạo Note mới khi Online (Local insert -> Cloud save -> Mark synced)', () async {
      when(() => mockLocal.insertNote(any())).thenAnswer((_) async {});
      when(() => mockFirestore.saveNote(any())).thenAnswer((_) async {});
      when(() => mockLocal.markSynced('note_101')).thenAnswer((_) async {});

      final repo = NoteRepositoryImpl(
        localService: mockLocal,
        firestoreService: mockFirestore,
        pendingDeleteSvc: mockPending,
        canSyncOverride: () async => true,
      );

      final note = Note(
        id: 'note_101',
        userId: 'user_dev',
        title: 'Họp kỹ thuật kiểm thử',
        content: 'Nội dung kiểm thử hộp trắng chuẩn McCabe',
        createdAt: DateTime(2026, 10, 3, 9, 0),
        updatedAt: DateTime(2026, 10, 3, 9, 0),
        isSynced: true,
      );

      await repo.saveNote(note);

      // 1. Phải đánh dấu dirty isSynced=false khi lưu local
      final capturedLocal = verify(() => mockLocal.insertNote(captureAny())).captured.single as Note;
      expect(capturedLocal.isSynced, isFalse);
      expect(capturedLocal.title, equals('Họp kỹ thuật kiểm thử'));

      // 2. Phải đẩy lên cloud
      verify(() => mockFirestore.saveNote(any(that: predicate<Note>((n) => n.id == 'note_101')))).called(1);

      // 3. Phải đánh dấu markSynced thành công trên SQLite
      verify(() => mockLocal.markSynced('note_101')).called(1);
    });

    test('TC-WB-NOTE-02: Path 2 - Tạo Note mới khi Offline (Local insert -> Bỏ qua Cloud -> Queued for sync)', () async {
      when(() => mockLocal.insertNote(any())).thenAnswer((_) async {});

      final repo = NoteRepositoryImpl(
        localService: mockLocal,
        firestoreService: mockFirestore,
        pendingDeleteSvc: mockPending,
        canSyncOverride: () async => false, // Mất mạng
      );

      final note = Note(
        id: 'note_offline_01',
        userId: 'user_dev',
        title: 'Ghi chú Offline',
        content: 'Lưu trên thiết bị khi không có mạng WiFi',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      await repo.saveNote(note);

      // Lưu local thành công với isSynced = false
      final captured = verify(() => mockLocal.insertNote(captureAny())).captured.single as Note;
      expect(captured.isSynced, isFalse);

      // Không được gọi cloud hay markSynced
      verifyNever(() => mockFirestore.saveNote(any()));
      verifyNever(() => mockLocal.markSynced(any()));
    });

    test('TC-WB-NOTE-03: Path 3 - Lưu Note khi Cloud gặp ngoại lệ (Local insert -> Cloud catch error -> Keep isSynced=false)', () async {
      when(() => mockLocal.insertNote(any())).thenAnswer((_) async {});
      when(() => mockFirestore.saveNote(any())).thenThrow(Exception('Firestore write timeout'));

      final repo = NoteRepositoryImpl(
        localService: mockLocal,
        firestoreService: mockFirestore,
        pendingDeleteSvc: mockPending,
        canSyncOverride: () async => true,
      );

      final note = Note(
        id: 'note_error_01',
        userId: 'user_dev',
        title: 'Note lỗi mạng',
        content: 'Thử nghiệm bắt ngoại lệ Cloud',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      // Không được làm sập ứng dụng (phải bắt ngoại lệ trong catch block)
      await repo.saveNote(note);

      verify(() => mockLocal.insertNote(any())).called(1);
      verify(() => mockFirestore.saveNote(any())).called(1);
      // Không được gọi markSynced vì cloud fail
      verifyNever(() => mockLocal.markSynced(any()));
    });

    test('TC-WB-NOTE-04: Path 1b (FN-09) - Sửa Note khi Online (Cập nhật nội dung và đồng bộ ngay)', () async {
      when(() => mockLocal.insertNote(any())).thenAnswer((_) async {});
      when(() => mockFirestore.saveNote(any())).thenAnswer((_) async {});
      when(() => mockLocal.markSynced('note_edit_01')).thenAnswer((_) async {});

      final repo = NoteRepositoryImpl(
        localService: mockLocal,
        firestoreService: mockFirestore,
        pendingDeleteSvc: mockPending,
        canSyncOverride: () async => true,
      );

      final updatedNote = Note(
        id: 'note_edit_01',
        userId: 'user_dev',
        title: 'Tiêu đề đã được sửa đổi',
        content: 'Nội dung cập nhật mới nhất',
        createdAt: DateTime(2026, 10, 1),
        updatedAt: DateTime(2026, 10, 3, 10, 30),
      );

      await repo.saveNote(updatedNote);

      verify(() => mockLocal.insertNote(any(that: predicate<Note>((n) => n.title == 'Tiêu đề đã được sửa đổi')))).called(1);
      verify(() => mockFirestore.saveNote(any())).called(1);
      verify(() => mockLocal.markSynced('note_edit_01')).called(1);
    });

    test('TC-WB-NOTE-05: Path 2b (FN-09) - Sửa Note khi Offline (Cập nhật nội dung trên SQLite, chờ sync sau)', () async {
      when(() => mockLocal.insertNote(any())).thenAnswer((_) async {});

      final repo = NoteRepositoryImpl(
        localService: mockLocal,
        firestoreService: mockFirestore,
        pendingDeleteSvc: mockPending,
        canSyncOverride: () async => false,
      );

      final updatedNote = Note(
        id: 'note_edit_offline',
        userId: 'user_dev',
        title: 'Sửa khi mất sóng',
        content: 'Nội dung sửa Offline',
        createdAt: DateTime(2026, 10, 1),
        updatedAt: DateTime(2026, 10, 3, 11, 00),
      );

      await repo.saveNote(updatedNote);

      verify(() => mockLocal.insertNote(any())).called(1);
      verifyNever(() => mockFirestore.saveNote(any()));
    });
  });

  group('Kiểm thử Hộp trắng LocalNoteService (SQLite Data Access Layer)', () {
    late MockDatabase mockDb;
    late LocalNoteService service;

    setUp(() {
      mockDb = MockDatabase();
      service = LocalNoteService(customDb: mockDb);
    });

    test('TC-WB-NOTE-06: LocalNoteService.insertNote() gọi SQLite insert với ConflictAlgorithm.replace', () async {
      when(() => mockDb.insert(
        'notes',
        any(),
        conflictAlgorithm: ConflictAlgorithm.replace,
      )).thenAnswer((_) async => 1);

      final note = Note(
        id: 'sqlite_note_01',
        userId: 'user_1',
        title: 'Insert to SQLite',
        content: 'Kiểm thử lệnh INSERT',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      await service.insertNote(note);

      verify(() => mockDb.insert(
        'notes',
        note.toMap(),
        conflictAlgorithm: ConflictAlgorithm.replace,
      )).called(1);
    });

    test('TC-WB-NOTE-07: LocalNoteService.updateNote() gọi SQLite update với where id = ?', () async {
      when(() => mockDb.update(
        'notes',
        any(),
        where: 'id = ?',
        whereArgs: ['sqlite_note_02'],
      )).thenAnswer((_) async => 1);

      final note = Note(
        id: 'sqlite_note_02',
        userId: 'user_1',
        title: 'Update SQLite',
        content: 'Kiểm thử lệnh UPDATE',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      await service.updateNote(note);

      verify(() => mockDb.update(
        'notes',
        note.toMap(),
        where: 'id = ?',
        whereArgs: ['sqlite_note_02'],
      )).called(1);
    });

    test('TC-WB-NOTE-08: LocalNoteService.markSynced() cập nhật trường is_synced = 1', () async {
      when(() => mockDb.update(
        'notes',
        {'is_synced': 1},
        where: 'id = ?',
        whereArgs: ['sqlite_note_03'],
      )).thenAnswer((_) async => 1);

      await service.markSynced('sqlite_note_03');

      verify(() => mockDb.update(
        'notes',
        {'is_synced': 1},
        where: 'id = ?',
        whereArgs: ['sqlite_note_03'],
      )).called(1);
    });

    test('TC-WB-NOTE-09: Note Model Serialization (toMap & fromMap)', () {
      final now = DateTime.now();
      final original = Note(
        id: 'model_note_01',
        userId: 'user_model',
        title: 'Serialization Test',
        content: 'Test JSON/Map Mapping',
        status: 'pinned',
        isSynced: true,
        isLocked: false,
        noteColor: '#FFFFFF',
        tags: ['QA', 'Whitebox'],
        imageUrls: ['https://example.com/img.png'],
        audioUrls: [],
        createdAt: now,
        updatedAt: now,
      );

      final map = original.toMap();
      final restored = Note.fromMap(map);

      expect(restored.id, equals(original.id));
      expect(restored.userId, equals(original.userId));
      expect(restored.title, equals(original.title));
      expect(restored.content, equals(original.content));
      expect(restored.status, equals('pinned'));
      expect(restored.isSynced, isTrue);
      expect(restored.tags, contains('Whitebox'));
    });

    test('TC-WB-NOTE-10: Note Model Immutability copyWith()', () {
      final note = Note(
        id: 'orig_01',
        title: 'Original Title',
        content: 'Original Content',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
        isSynced: true,
      );

      final modified = note.copyWith(
        title: 'New Title',
        isSynced: false,
      );

      expect(modified.id, equals('orig_01'));
      expect(modified.title, equals('New Title'));
      expect(modified.content, equals('Original Content'));
      expect(modified.isSynced, isFalse);
      expect(note.isSynced, isTrue); // Đối tượng gốc không bị thay đổi
    });
  });
}
