import 'package:flutter_test/flutter_test.dart';
import 'package:smart_note_app/models/note_model.dart';
import 'package:smart_note_app/providers/note_provider.dart';
import 'package:smart_note_app/repositories/note_repository.dart';
import 'package:smart_note_app/services/cloudinary_service.dart';
import 'package:smart_note_app/services/reminder_service.dart';
import 'package:smart_note_app/services/local_note_service.dart';
import 'package:smart_note_app/services/firestore_note_service.dart';
import 'package:smart_note_app/services/pending_delete_service.dart';

class MockNoteRepository extends Fake implements NoteRepository {
  final List<Note> savedNotes = [];
  final List<String> hardDeletedIds = [];
  List<Note> trashNotesToReturn = [];

  @override
  Future<void> saveNote(Note note) async {
    savedNotes.add(note);
  }

  @override
  Future<void> deleteNoteForever(String id) async {
    hardDeletedIds.add(id);
  }

  @override
  Future<List<Note>> getTrashNotes(String userId) async {
    return List.from(trashNotesToReturn);
  }
}

class MockCloudinaryService extends Fake implements CloudinaryService {
  final List<String> deletedFiles = [];
  bool shouldThrow = false;

  @override
  Future<bool> deleteFile(String fileUrl, {String resourceType = 'image'}) async {
    if (shouldThrow) {
      throw Exception('Cloudinary network timeout');
    }
    deletedFiles.add('$resourceType:$fileUrl');
    return true;
  }
}

class MockReminderService extends Fake implements ReminderService {
  final List<String> cancelledIds = [];

  @override
  Future<void> cancelReminder(String id) async {
    cancelledIds.add(id);
  }

  @override
  Future<void> scheduleReminder({
    required String id,
    required String title,
    required String body,
    String? bigText,
    required DateTime scheduledDate,
  }) async {}
}

class MockLocalNoteService extends Fake implements LocalNoteService {
  final List<String> localDeletedIds = [];

  @override
  Future<void> deleteNote(String id) async {
    localDeletedIds.add(id);
  }
}

class MockFirestoreNoteService extends Fake implements FirestoreNoteService {
  final List<String> cloudDeletedIds = [];
  bool shouldThrow = false;

  @override
  Future<void> deleteNote(String noteId) async {
    if (shouldThrow) {
      throw Exception('Firestore delete error');
    }
    cloudDeletedIds.add(noteId);
  }
}

class MockPendingDeleteService extends Fake implements PendingDeleteService {
  final List<String> addedIds = [];
  final List<String> removedIds = [];

  @override
  Future<void> add(String id) async {
    addedIds.add(id);
  }

  @override
  Future<void> remove(String id) async {
    removedIds.add(id);
  }
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late MockNoteRepository mockRepo;
  late MockCloudinaryService mockCloudinary;
  late MockReminderService mockReminder;
  late NoteProvider provider;

  final sampleNote1 = Note(
    id: 'note_normal_1',
    userId: 'user_test',
    title: 'Ghi chú thường',
    content: 'Nội dung thường',
    createdAt: DateTime.now().subtract(const Duration(days: 2)),
    updatedAt: DateTime.now().subtract(const Duration(days: 2)),
    status: 'normal',
    isSynced: true,
  );

  final samplePinnedNote = Note(
    id: 'note_pinned_1',
    userId: 'user_test',
    title: 'Ghi chú đã ghim',
    content: 'Nội dung quan trọng',
    createdAt: DateTime.now().subtract(const Duration(days: 3)),
    updatedAt: DateTime.now().subtract(const Duration(days: 3)),
    status: 'pinned',
    isSynced: true,
  );

  final sampleMediaNote = Note(
    id: 'note_media_1',
    userId: 'user_test',
    title: 'Ghi chú có media',
    content: 'Nội dung đa phương tiện',
    createdAt: DateTime.now().subtract(const Duration(days: 5)),
    updatedAt: DateTime.now().subtract(const Duration(days: 5)),
    status: 'trash',
    imageUrls: ['https://res.cloudinary.com/smart_note/image/upload/v1/img1.jpg'],
    audioUrls: ['https://res.cloudinary.com/smart_note/video/upload/v1/voice1.m4a'],
    isSynced: true,
  );

  setUp(() {
    mockRepo = MockNoteRepository();
    mockCloudinary = MockCloudinaryService();
    mockReminder = MockReminderService();
    provider = NoteProvider(
      mockRepo,
      cloudinaryService: mockCloudinary,
      reminderService: mockReminder,
    );
  });

  group('FN-10: Kiểm thử Hộp trắng Xóa ghi chú (Soft Delete vào Thùng rác)', () {
    test('TC-WB-TRASH-01: Path 1 - Xóa Note thường: Đổi status=trash, hủy reminder, lưu DB', () async {
      await provider.addNote(sampleNote1);
      expect(provider.normalNotes.any((n) => n.id == sampleNote1.id), isTrue);
      mockRepo.savedNotes.clear();

      // Thực thi xóa
      await provider.deleteNote(sampleNote1.id);

      // Kiểm chứng kết quả
      expect(mockReminder.cancelledIds.contains(sampleNote1.id), isTrue,
          reason: 'Phải hủy reminder khi note vào thùng rác');
      expect(provider.normalNotes.any((n) => n.id == sampleNote1.id), isFalse,
          reason: 'Phải gỡ khỏi danh sách note thường');
      expect(provider.trashNotes.any((n) => n.id == sampleNote1.id), isTrue,
          reason: 'Phải chuyển vào thùng rác _trashNotes');
      expect(provider.trashNotes.first.status, equals('trash'));
      expect(provider.trashNotes.first.isSynced, isFalse);
      expect(mockRepo.savedNotes.any((n) => n.id == sampleNote1.id && n.status == 'trash'), isTrue,
          reason: 'Phải gọi repository.saveNote với trạng thái trash');
    });

    test('TC-WB-TRASH-02: Path 2 - Xóa Note đang ghim (Pinned): Gỡ khỏi pinned list & vào trash', () async {
      // Đặt note ghim vào danh sách
      await provider.addNote(samplePinnedNote);
      expect(provider.pinnedNotes.any((n) => n.id == samplePinnedNote.id), isTrue);
      mockRepo.savedNotes.clear();

      // Thực thi xóa
      await provider.deleteNote(samplePinnedNote.id);

      // Kiểm chứng
      expect(provider.pinnedNotes.any((n) => n.id == samplePinnedNote.id), isFalse,
          reason: 'Note ghim phải bị gỡ khỏi pinnedNotes');
      expect(provider.trashNotes.any((n) => n.id == samplePinnedNote.id), isTrue);
      expect(provider.trashNotes.first.status, equals('trash'));
    });

    test('TC-WB-TRASH-03: Path 3 - Xóa Note với ID không tồn tại trong memory: An toàn không crash', () async {
      await provider.deleteNote('non_existent_id');
      expect(mockReminder.cancelledIds.contains('non_existent_id'), isTrue);
      expect(mockRepo.savedNotes.isEmpty, isTrue);
    });
  });

  group('FN-11: Kiểm thử Hộp trắng Khôi phục ghi chú từ Thùng rác (Restore Note)', () {
    test('TC-WB-TRASH-04: Path 4 - Khôi phục Note: status=normal, chuyển từ trash sang notes', () async {
      // Đưa note vào trash trước
      await provider.addNote(sampleNote1);
      await provider.deleteNote(sampleNote1.id);
      expect(provider.trashNotes.length, equals(1));
      mockRepo.savedNotes.clear();

      // Thực thi khôi phục
      await provider.restoreNote(sampleNote1.id);

      // Kiểm chứng
      expect(provider.trashNotes.any((n) => n.id == sampleNote1.id), isFalse,
          reason: 'Note phải được gỡ khỏi thùng rác');
      expect(provider.normalNotes.any((n) => n.id == sampleNote1.id), isTrue,
          reason: 'Note phải trở lại danh sách bình thường');
      expect(provider.normalNotes.first.status, equals('normal'));
      expect(provider.normalNotes.first.isSynced, isFalse);
      expect(mockRepo.savedNotes.any((n) => n.id == sampleNote1.id && n.status == 'normal'), isTrue,
          reason: 'Phải gọi repository.saveNote lưu trạng thái normal');
    });

    test('TC-WB-TRASH-05: Path 5 - Khôi phục Note không tồn tại trong thùng rác: Bỏ qua an toàn', () async {
      await provider.restoreNote('unknown_id');
      expect(mockRepo.savedNotes.isEmpty, isTrue);
    });
  });

  group('FN-12: Kiểm thử Hộp trắng Xóa vĩnh viễn (Hard Delete) & Dọn Media Cloud', () {
    test('TC-WB-TRASH-06: Path 6 - Xóa vĩnh viễn note có ảnh & audio: Dọn sạch Cloudinary & xóa DB', () async {
      // Đưa note có media vào thùng rác
      await provider.addNote(sampleMediaNote);
      await provider.deleteNote(sampleMediaNote.id);

      // Thực thi xóa vĩnh viễn
      await provider.deleteNoteForever(sampleMediaNote.id);

      // Kiểm chứng Cloudinary deleteFile
      expect(mockCloudinary.deletedFiles.contains('image:${sampleMediaNote.imageUrls.first}'), isTrue,
          reason: 'Phải xóa file ảnh trên Cloudinary');
      expect(mockCloudinary.deletedFiles.contains('video:${sampleMediaNote.audioUrls.first}'), isTrue,
          reason: 'Phải xóa file âm thanh trên Cloudinary');

      // Kiểm chứng in-memory và DB
      expect(provider.trashNotes.any((n) => n.id == sampleMediaNote.id), isFalse);
      expect(mockRepo.hardDeletedIds.contains(sampleMediaNote.id), isTrue,
          reason: 'Phải gọi repository.deleteNoteForever');
    });

    test('TC-WB-TRASH-07: Path 7 - Xóa vĩnh viễn note không có media / không tìm thấy trong RAM', () async {
      await provider.deleteNoteForever('not_in_ram_id');

      expect(mockCloudinary.deletedFiles.isEmpty, isTrue);
      expect(mockRepo.hardDeletedIds.contains('not_in_ram_id'), isTrue,
          reason: 'Vẫn phải gọi repository.deleteNoteForever');
    });

    test('TC-WB-TRASH-08: Path 8 - Xóa vĩnh viễn khi Cloudinary ném ngoại lệ: Bọc try/catch, DB vẫn xóa', () async {
      mockCloudinary.shouldThrow = true;
      await provider.addNote(sampleMediaNote);
      await provider.deleteNote(sampleMediaNote.id);

      // Xóa vĩnh viễn không bị rethrow crash
      await provider.deleteNoteForever(sampleMediaNote.id);

      expect(mockRepo.hardDeletedIds.contains(sampleMediaNote.id), isTrue,
          reason: 'Lỗi dọn Cloudinary không được làm dừng việc xóa DB');
    });
  });

  group('Chính sách Vòng đời Thùng rác: Tự động xóa vĩnh viễn sau 7 ngày', () {
    test('TC-WB-TRASH-09: Path 9 - fetchTrashNotes tự động xóa vĩnh viễn note >= 7 ngày, giữ note < 7 ngày', () async {
      final oldNote = Note(
        id: 'expired_note',
        userId: 'user_test',
        title: 'Note rác quá 7 ngày',
        content: 'Nội dung hết hạn',
        createdAt: DateTime.now().subtract(const Duration(days: 10)),
        updatedAt: DateTime.now().subtract(const Duration(days: 8)), // 8 ngày trước
        status: 'trash',
      );

      final freshNote = Note(
        id: 'fresh_note',
        userId: 'user_test',
        title: 'Note rác mới 2 ngày',
        content: 'Nội dung mới xóa',
        createdAt: DateTime.now().subtract(const Duration(days: 3)),
        updatedAt: DateTime.now().subtract(const Duration(days: 2)), // 2 ngày trước
        status: 'trash',
      );

      mockRepo.trashNotesToReturn = [oldNote, freshNote];

      // Thực thi quét thùng rác
      await provider.fetchTrashNotes('user_test');

      // Kiểm chứng
      expect(mockRepo.hardDeletedIds.contains('expired_note'), isTrue,
          reason: 'Note quá hạn 8 ngày phải tự động bị xóa vĩnh viễn');
      expect(provider.trashNotes.any((n) => n.id == 'fresh_note'), isTrue,
          reason: 'Note mới 2 ngày phải được giữ lại trong thùng rác');
      expect(provider.trashNotes.length, equals(1));
    });
  });

  group('Kiểm thử Hộp trắng Tầng Repository (NoteRepositoryImpl.deleteNoteForever)', () {
    late MockLocalNoteService mockLocal;
    late MockFirestoreNoteService mockFirestore;
    late MockPendingDeleteService mockPending;

    setUp(() {
      mockLocal = MockLocalNoteService();
      mockFirestore = MockFirestoreNoteService();
      mockPending = MockPendingDeleteService();
    });

    test('TC-WB-TRASH-10: Path 10 - Xóa khi Online: Xóa SQLite -> Xóa Firestore -> Gỡ khỏi pending queue', () async {
      final repo = NoteRepositoryImpl(
        localService: mockLocal,
        firestoreService: mockFirestore,
        pendingDeleteSvc: mockPending,
        canSyncOverride: () async => true,
      );

      await repo.deleteNoteForever('note_online_del');

      expect(mockLocal.localDeletedIds.contains('note_online_del'), isTrue);
      expect(mockFirestore.cloudDeletedIds.contains('note_online_del'), isTrue);
      expect(mockPending.removedIds.contains('note_online_del'), isTrue);
      expect(mockPending.addedIds.isEmpty, isTrue);
    });

    test('TC-WB-TRASH-11: Path 11 - Xóa khi Offline: Xóa SQLite -> Bỏ qua Firestore -> Đưa vào pending queue', () async {
      final repo = NoteRepositoryImpl(
        localService: mockLocal,
        firestoreService: mockFirestore,
        pendingDeleteSvc: mockPending,
        canSyncOverride: () async => false,
      );

      await repo.deleteNoteForever('note_offline_del');

      expect(mockLocal.localDeletedIds.contains('note_offline_del'), isTrue);
      expect(mockFirestore.cloudDeletedIds.isEmpty, isTrue);
      expect(mockPending.addedIds.contains('note_offline_del'), isTrue,
          reason: 'Phải đưa vào hàng đợi offline để sync sau');
    });

    test('TC-WB-TRASH-12: Path 12 - Xóa khi Online nhưng Firestore lỗi: Catch lỗi -> Đưa vào pending queue', () async {
      mockFirestore.shouldThrow = true;
      final repo = NoteRepositoryImpl(
        localService: mockLocal,
        firestoreService: mockFirestore,
        pendingDeleteSvc: mockPending,
        canSyncOverride: () async => true,
      );

      await repo.deleteNoteForever('note_error_del');

      expect(mockLocal.localDeletedIds.contains('note_error_del'), isTrue);
      expect(mockPending.addedIds.contains('note_error_del'), isTrue,
          reason: 'Khi Firestore lỗi, phải đưa ID vào pending queue dự phòng');
    });
  });

  group('Thao tác Hàng loạt Thùng rác (Batch Trash Selection & Actions)', () {
    test('TC-WB-TRASH-13: Quản lý chọn / bỏ chọn ghi chú thùng rác (toggle & clear selection)', () {
      expect(provider.isTrashSelectionMode, isFalse);
      provider.toggleTrashSelection('note_1');
      expect(provider.selectedTrashNoteIds.contains('note_1'), isTrue);
      expect(provider.isTrashSelectionMode, isTrue);

      // Toggle lại để bỏ chọn
      provider.toggleTrashSelection('note_1');
      expect(provider.selectedTrashNoteIds.contains('note_1'), isFalse);
      expect(provider.isTrashSelectionMode, isFalse);

      // Chọn nhiều và xóa chọn
      provider.toggleTrashSelection('note_2');
      provider.toggleTrashSelection('note_3');
      expect(provider.selectedTrashNoteIds.length, equals(2));
      provider.clearTrashSelection();
      expect(provider.selectedTrashNoteIds.isEmpty, isTrue);
    });

    test('TC-WB-TRASH-14: Thao tác hàng loạt khôi phục & xóa vĩnh viễn nhiều note cùng lúc', () async {
      final batchNote1 = Note(
        id: 'batch_1',
        userId: 'user_test',
        title: 'Batch 1',
        content: 'Content',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
        status: 'trash',
      );
      final batchNote2 = Note(
        id: 'batch_2',
        userId: 'user_test',
        title: 'Batch 2',
        content: 'Content',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
        status: 'trash',
      );

      mockRepo.trashNotesToReturn = [batchNote1, batchNote2];
      await provider.fetchTrashNotes('user_test');
      expect(provider.trashNotes.length, equals(2));

      // 1. Khôi phục hàng loạt
      provider.toggleTrashSelection('batch_1');
      await provider.restoreSelectedTrashNotes();
      expect(provider.normalNotes.any((n) => n.id == 'batch_1'), isTrue);
      expect(provider.trashNotes.any((n) => n.id == 'batch_1'), isFalse);

      // 2. Xóa vĩnh viễn hàng loạt
      provider.toggleTrashSelection('batch_2');
      await provider.deleteForeverSelectedTrashNotes();
      expect(mockRepo.hardDeletedIds.contains('batch_2'), isTrue);
      expect(provider.trashNotes.isEmpty, isTrue);
    });
  });
}

