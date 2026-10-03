import 'dart:async';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:sqflite/sqflite.dart';
import 'package:smart_note_app/repositories/sync_repository.dart';
import 'package:smart_note_app/services/local_note_service.dart';
import 'package:smart_note_app/services/firestore_note_service.dart';
import 'package:smart_note_app/services/pending_delete_service.dart';
import 'package:smart_note_app/services/reminder_service.dart';
import 'package:smart_note_app/models/note_model.dart';
import 'package:smart_note_app/models/sync_status.dart';

// Mock các dependencies
class MockLocalNoteService extends Mock implements LocalNoteService {}
class MockFirestoreNoteService extends Mock implements FirestoreNoteService {}
class MockPendingDeleteService extends Mock implements PendingDeleteService {}
class MockReminderService extends Mock implements ReminderService {}
class FakeDatabase extends Fake implements Database {
  final Transaction txn;
  FakeDatabase(this.txn);

  @override
  Future<T> transaction<T>(Future<T> Function(Transaction txn) action, {bool? exclusive}) {
    return action(txn);
  }
}

class MockTransaction extends Mock implements Transaction {}

void main() {
  late MockLocalNoteService mockLocal;
  late MockFirestoreNoteService mockFirestore;
  late MockPendingDeleteService mockPendingDelete;
  late MockReminderService mockReminder;
  late FakeDatabase fakeDb;
  late MockTransaction mockTxn;
  late SyncRepositoryImpl syncRepo;

  setUp(() {
    mockLocal = MockLocalNoteService();
    mockFirestore = MockFirestoreNoteService();
    mockPendingDelete = MockPendingDeleteService();
    mockReminder = MockReminderService();
    mockTxn = MockTransaction();
    fakeDb = FakeDatabase(mockTxn);

    // Giả lập giao dịch SQLite thành công
    when(() => mockLocal.db).thenAnswer((_) async => fakeDb);

    when(() => mockTxn.update(
      any(),
      any(),
      where: any(named: 'where'),
      whereArgs: any(named: 'whereArgs'),
    )).thenAnswer((_) async => 1);

    when(() => mockTxn.insert(
      any(),
      any(),
      conflictAlgorithm: any(named: 'conflictAlgorithm'),
    )).thenAnswer((_) async => 1);

    // Mặc định ReminderService không gây lỗi
    when(() => mockReminder.syncReminders(any())).thenAnswer((_) async {});

    syncRepo = SyncRepositoryImpl(
      localService: mockLocal,
      firestoreService: mockFirestore,
      pendingDeleteSvc: mockPendingDelete,
      reminderService: mockReminder,
    );
  });

  group('FN-40, FN-41: Kiểm thử Hộp trắng SyncRepository.syncNow() & Thuật toán LWW', () {
    const userId = 'user_test_123';

    // -------------------------------------------------------------------------
    // TC-WB-SYNC-01: Path 1 (Sync Lock khi có tiến trình khác đang chạy)
    // -------------------------------------------------------------------------
    test('TC-WB-SYNC-01: Path 1 - Chặn đồng bộ song song khi Sync Lock đang active', () async {
      final completer = Completer<List<String>>();
      when(() => mockPendingDelete.getAll()).thenAnswer((_) => completer.future);

      // Chạy tiến trình đồng bộ thứ nhất (sẽ bị hoãn ở pendingDelete)
      final future1 = syncRepo.syncNow(userId);

      // Chạy tiến trình đồng bộ thứ hai (phải chờ future1 và trả về false)
      final future2 = syncRepo.syncNow(userId);

      // Giải phóng tiến trình 1
      when(() => mockLocal.getUnsyncedNotes(userId: userId)).thenAnswer((_) async => []);
      when(() => mockFirestore.getNotes()).thenAnswer((_) async => []);
      when(() => mockLocal.getAbsoluteAllNotes(userId: userId)).thenAnswer((_) async => []);
      completer.complete([]);

      final res1 = await future1;
      final res2 = await future2;

      expect(res1, isFalse);
      expect(res2, isFalse);
    });

    // -------------------------------------------------------------------------
    // TC-WB-SYNC-02: Path 2 (Đồng bộ sạch - Không có thay đổi nào ở cả 2 phía)
    // -------------------------------------------------------------------------
    test('TC-WB-SYNC-02: Path 2 - Đồng bộ hoàn tất khi không có thay đổi nào', () async {
      when(() => mockPendingDelete.getAll()).thenAnswer((_) async => []);
      when(() => mockLocal.getUnsyncedNotes(userId: userId)).thenAnswer((_) async => []);
      when(() => mockFirestore.getNotes()).thenAnswer((_) async => []);
      when(() => mockLocal.getAbsoluteAllNotes(userId: userId)).thenAnswer((_) async => []);

      final statuses = <SyncStatus>[];
      final sub = syncRepo.syncStatusStream.listen(statuses.add);

      final hasChanges = await syncRepo.syncNow(userId);
      await Future<void>.delayed(Duration.zero);

      expect(hasChanges, isFalse);
      expect(statuses, containsAllInOrder([SyncStatus.syncing, SyncStatus.success]));
      verify(() => mockReminder.syncReminders([])).called(1);
      await sub.cancel();
    });

    // -------------------------------------------------------------------------
    // TC-WB-SYNC-03: Path 3 (LWW Push: Note mới ở Local chưa có trên Cloud)
    // -------------------------------------------------------------------------
    test('TC-WB-SYNC-03: Path 3 - LWW Push: Note mới tại Local đẩy lên Cloud (cloud == null)', () async {
      final localNote = Note(
        id: 'note_local_new',
        userId: userId,
        title: 'Local New Note',
        content: 'Content Local',
        updatedAt: DateTime(2026, 10, 1, 10, 0),
      );

      when(() => mockPendingDelete.getAll()).thenAnswer((_) async => []);
      when(() => mockLocal.getUnsyncedNotes(userId: userId)).thenAnswer((_) async => [localNote]);
      when(() => mockFirestore.getNotes()).thenAnswer((_) async => []);
      when(() => mockFirestore.batchSaveNotes(any())).thenAnswer((_) async {});
      when(() => mockLocal.getAbsoluteAllNotes(userId: userId)).thenAnswer((_) async => [localNote]);

      final hasChanges = await syncRepo.syncNow(userId);

      expect(hasChanges, isFalse);
      verify(() => mockFirestore.batchSaveNotes([localNote])).called(1);
      verify(() => mockTxn.update(
        'notes',
        {'is_synced': 1},
        where: 'id = ?',
        whereArgs: [localNote.id],
      )).called(1);
    });

    // -------------------------------------------------------------------------
    // TC-WB-SYNC-04: Path 4 (LWW Push: Local sửa mới hơn Cloud - local.updatedAt > cloud.updatedAt)
    // -------------------------------------------------------------------------
    test('TC-WB-SYNC-04: Path 4 - LWW Push: Local có bản sửa mới hơn Cloud (Local thắng)', () async {
      final cloudNote = Note(
        id: 'note_shared',
        userId: userId,
        title: 'Old Cloud Title',
        content: 'Old Cloud Content',
        updatedAt: DateTime(2026, 10, 1, 9, 0),
      );
      final localNote = Note(
        id: 'note_shared',
        userId: userId,
        title: 'Newer Local Title',
        content: 'Newer Local Content',
        updatedAt: DateTime(2026, 10, 1, 11, 0), // Local mới hơn
      );

      when(() => mockPendingDelete.getAll()).thenAnswer((_) async => []);
      when(() => mockLocal.getUnsyncedNotes(userId: userId)).thenAnswer((_) async => [localNote]);
      when(() => mockFirestore.getNotes()).thenAnswer((_) async => [cloudNote]);
      when(() => mockFirestore.batchSaveNotes(any())).thenAnswer((_) async {});
      when(() => mockLocal.getAbsoluteAllNotes(userId: userId)).thenAnswer((_) async => [localNote]);

      final hasChanges = await syncRepo.syncNow(userId);

      expect(hasChanges, isFalse);
      verify(() => mockFirestore.batchSaveNotes([localNote])).called(1);
    });

    // -------------------------------------------------------------------------
    // TC-WB-SYNC-05: Path 5 (LWW Conflict: Local cũ hơn Cloud khi Push - Cloud thắng)
    // -------------------------------------------------------------------------
    test('TC-WB-SYNC-05: Path 5 - LWW Conflict: Local cũ hơn Cloud nên không đẩy đè (Cloud thắng)', () async {
      final cloudNote = Note(
        id: 'note_shared',
        userId: userId,
        title: 'Newer Cloud Title',
        content: 'Newer Cloud Content',
        updatedAt: DateTime(2026, 10, 1, 12, 0), // Cloud mới hơn
      );
      final localNote = Note(
        id: 'note_shared',
        userId: userId,
        title: 'Older Local Title',
        content: 'Older Local Content',
        updatedAt: DateTime(2026, 10, 1, 8, 0), // Local cũ hơn
      );

      when(() => mockPendingDelete.getAll()).thenAnswer((_) async => []);
      when(() => mockLocal.getUnsyncedNotes(userId: userId)).thenAnswer((_) async => [localNote]);
      when(() => mockFirestore.getNotes()).thenAnswer((_) async => [cloudNote]);
      when(() => mockLocal.getAbsoluteAllNotes(userId: userId)).thenAnswer((_) async => [localNote]);

      final hasChanges = await syncRepo.syncNow(userId);

      // notesToPush rỗng vì Local cũ hơn Cloud
      verifyNever(() => mockFirestore.batchSaveNotes(any()));
      // Sau đó Cloud note mới hơn kéo về cập nhật đè lên Local
      expect(hasChanges, isTrue);
      verify(() => mockTxn.update(
        'notes',
        any(),
        where: 'id = ?',
        whereArgs: [cloudNote.id],
      )).called(1);
    });

    // -------------------------------------------------------------------------
    // TC-WB-SYNC-06: Path 6 (LWW Pull: Note mới trên Cloud tải về lưu vào SQLite)
    // -------------------------------------------------------------------------
    test('TC-WB-SYNC-06: Path 6 - LWW Pull: Note mới trên Cloud chưa có tại Local (Insert)', () async {
      final cloudNote = Note(
        id: 'note_cloud_only',
        userId: userId,
        title: 'Cloud Only Title',
        content: 'Cloud Content',
        updatedAt: DateTime(2026, 10, 1, 10, 0),
      );

      when(() => mockPendingDelete.getAll()).thenAnswer((_) async => []);
      when(() => mockLocal.getUnsyncedNotes(userId: userId)).thenAnswer((_) async => []);
      when(() => mockFirestore.getNotes()).thenAnswer((_) async => [cloudNote]);
      when(() => mockLocal.getAbsoluteAllNotes(userId: userId)).thenAnswer((_) async => []); // Local trống

      final hasChanges = await syncRepo.syncNow(userId);

      expect(hasChanges, isTrue);
      verify(() => mockTxn.insert(
        'notes',
        any(),
        conflictAlgorithm: ConflictAlgorithm.replace,
      )).called(1);
    });

    // -------------------------------------------------------------------------
    // TC-WB-SYNC-07: Path 7 (LWW Pull: Note Cloud sửa mới hơn Local kéo về Update)
    // -------------------------------------------------------------------------
    test('TC-WB-SYNC-07: Path 7 - LWW Pull: Cloud có bản sửa mới hơn Local (Update SQLite)', () async {
      final localNote = Note(
        id: 'note_both',
        userId: userId,
        title: 'Local V1',
        content: 'Content V1',
        updatedAt: DateTime(2026, 10, 1, 9, 0),
      );
      final cloudNote = Note(
        id: 'note_both',
        userId: userId,
        title: 'Cloud V2',
        content: 'Content V2',
        updatedAt: DateTime(2026, 10, 1, 14, 0), // Cloud mới hơn
      );

      when(() => mockPendingDelete.getAll()).thenAnswer((_) async => []);
      when(() => mockLocal.getUnsyncedNotes(userId: userId)).thenAnswer((_) async => []);
      when(() => mockFirestore.getNotes()).thenAnswer((_) async => [cloudNote]);
      when(() => mockLocal.getAbsoluteAllNotes(userId: userId)).thenAnswer((_) async => [localNote]);

      final hasChanges = await syncRepo.syncNow(userId);

      expect(hasChanges, isTrue);
      verify(() => mockTxn.update(
        'notes',
        any(),
        where: 'id = ?',
        whereArgs: [cloudNote.id],
      )).called(1);
    });

    // -------------------------------------------------------------------------
    // TC-WB-SYNC-08: Path 8 (LWW Pull: Local mới hơn hoặc bằng Cloud giữ nguyên)
    // -------------------------------------------------------------------------
    test('TC-WB-SYNC-08: Path 8 - LWW Pull: Local mới hơn Cloud thì giữ nguyên không ghi đè', () async {
      final cloudNote = Note(
        id: 'note_both',
        userId: userId,
        title: 'Cloud Old',
        content: 'Content',
        updatedAt: DateTime(2026, 10, 1, 10, 0),
      );
      final localNote = Note(
        id: 'note_both',
        userId: userId,
        title: 'Local New',
        content: 'Content',
        updatedAt: DateTime(2026, 10, 1, 15, 0), // Local mới hơn
      );

      when(() => mockPendingDelete.getAll()).thenAnswer((_) async => []);
      when(() => mockLocal.getUnsyncedNotes(userId: userId)).thenAnswer((_) async => []);
      when(() => mockFirestore.getNotes()).thenAnswer((_) async => [cloudNote]);
      when(() => mockLocal.getAbsoluteAllNotes(userId: userId)).thenAnswer((_) async => [localNote]);

      final hasChanges = await syncRepo.syncNow(userId);

      expect(hasChanges, isFalse);
      verifyNever(() => mockTxn.insert(any(), any(), conflictAlgorithm: any(named: 'conflictAlgorithm')));
      verifyNever(() => mockTxn.update(any(), any(), where: any(named: 'where'), whereArgs: any(named: 'whereArgs')));
    });

    // -------------------------------------------------------------------------
    // TC-WB-SYNC-09: Path 9 (Xóa offline - Pending Deletes xử lý thành công)
    // -------------------------------------------------------------------------
    test('TC-WB-SYNC-09: Path 9 - Xử lý sạch hàng đợi xóa Offline khi đồng bộ', () async {
      final pendingIds = ['pending_1', 'pending_2'];

      when(() => mockPendingDelete.getAll()).thenAnswer((_) async => pendingIds);
      when(() => mockFirestore.deleteNote(any())).thenAnswer((_) async {});
      when(() => mockPendingDelete.remove(any())).thenAnswer((_) async {});
      when(() => mockLocal.getUnsyncedNotes(userId: userId)).thenAnswer((_) async => []);
      when(() => mockFirestore.getNotes()).thenAnswer((_) async => []);
      when(() => mockLocal.getAbsoluteAllNotes(userId: userId)).thenAnswer((_) async => []);

      final hasChanges = await syncRepo.syncNow(userId);

      expect(hasChanges, isFalse);
      verify(() => mockFirestore.deleteNote('pending_1')).called(1);
      verify(() => mockPendingDelete.remove('pending_1')).called(1);
      verify(() => mockFirestore.deleteNote('pending_2')).called(1);
      verify(() => mockPendingDelete.remove('pending_2')).called(1);
    });

    // -------------------------------------------------------------------------
    // TC-WB-SYNC-10: Path 10 (Ngoại lệ khi đồng bộ - phát SyncStatus.error và giải phóng lock)
    // -------------------------------------------------------------------------
    test('TC-WB-SYNC-10: Path 10 - Xử lý ngoại lệ mạng/Firestore, phát SyncStatus.error và rethrow', () async {
      when(() => mockPendingDelete.getAll()).thenThrow(Exception('Firestore connection timeout'));

      final statuses = <SyncStatus>[];
      final sub = syncRepo.syncStatusStream.listen(statuses.add);

      expect(
        () => syncRepo.syncNow(userId),
        throwsA(predicate((e) => e is Exception && e.toString().contains('Firestore connection timeout'))),
      );

      // Đợi microtask cập nhật stream
      await Future<void>.delayed(const Duration(milliseconds: 50));
      expect(statuses, containsAll([SyncStatus.syncing, SyncStatus.error]));
      await sub.cancel();
    });
  });

  group('Kiểm thử bổ sung độ phủ pullFromCloud()', () {
    const userId = 'user_test_123';

    test('pullFromCloud: kéo thành công dữ liệu mới từ Cloud về SQLite', () async {
      final cloudNote = Note(
        id: 'cloud_new_1',
        userId: userId,
        title: 'New Cloud Note',
        content: 'Content',
        updatedAt: DateTime(2026, 10, 1, 10, 0),
      );

      when(() => mockFirestore.getNotes()).thenAnswer((_) async => [cloudNote]);
      when(() => mockLocal.getAbsoluteAllNotes(userId: userId)).thenAnswer((_) async => []);

      final hasChanges = await syncRepo.pullFromCloud(userId);

      expect(hasChanges, isTrue);
      verify(() => mockTxn.insert(
        'notes',
        any(),
        conflictAlgorithm: ConflictAlgorithm.replace,
      )).called(1);
      verify(() => mockReminder.syncReminders([cloudNote])).called(1);
    });
  });
}
