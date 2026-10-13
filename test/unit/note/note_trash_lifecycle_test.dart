// test/unit/note/note_trash_lifecycle_test.dart
// White-box Testing: Note CRUD & Trash Lifecycle (FN-29, FN-30 / REQ-10)
// Direct invocation of production NoteProvider with RecordingNoteRepository

import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/services.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:smart_note_app/models/note_model.dart';
import 'package:smart_note_app/providers/note_provider.dart';
import 'package:smart_note_app/repositories/note_repository.dart';

/// Mock HttpOverrides để chặn toàn bộ outbound HTTP request tới Cloudinary trong test
class MockHttpOverrides extends HttpOverrides {
  final List<Uri> requestedUris;
  MockHttpOverrides(this.requestedUris);

  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return _MockHttpClient(requestedUris);
  }
}

class _MockHttpClient implements HttpClient {
  final List<Uri> requestedUris;
  _MockHttpClient(this.requestedUris);

  @override
  Future<HttpClientRequest> postUrl(Uri url) async {
    requestedUris.add(url);
    return _MockHttpClientRequest();
  }

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _MockHttpClientRequest implements HttpClientRequest {
  @override
  final HttpHeaders headers = _MockHttpHeaders();

  @override
  void write(Object? obj) {}

  @override
  Future<HttpClientResponse> close() async {
    return _MockHttpClientResponse();
  }

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _MockHttpHeaders implements HttpHeaders {
  @override
  void set(String name, Object value, {bool preserveHeaderCase = false}) {}

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _MockHttpClientResponse extends Stream<List<int>> implements HttpClientResponse {
  @override
  int get statusCode => 200;

  @override
  StreamSubscription<List<int>> listen(
    void Function(List<int> event)? onData, {
    Function? onError,
    void Function()? onDone,
    bool? cancelOnError,
  }) {
    return Stream<List<int>>.fromIterable([
      utf8.encode('{"result":"ok"}'),
    ]).listen(
      onData,
      onError: onError,
      onDone: onDone,
      cancelOnError: cancelOnError,
    );
  }

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

/// Recording / Spy Fake để thay thế NoteRepository dependency
/// Ghi nhận lời gọi phương thức, tham số và trả về dữ liệu mẫu, không tự cài logic nghiệp vụ của NoteProvider
class RecordingNoteRepository implements NoteRepository {
  final List<Note> savedNotes = [];
  final List<String> deletedForeverIds = [];
  final List<String> deletedIds = [];
  List<Note> trashNotesToReturn = [];
  List<Note> normalNotesToReturn = [];
  List<Note> pinnedNotesToReturn = [];
  List<Note> archivedNotesToReturn = [];

  bool shouldThrowOnSave = false;
  bool shouldThrowOnDelete = false;

  @override
  Future<void> saveNote(Note note) async {
    if (shouldThrowOnSave) {
      throw Exception('Database write failure');
    }
    savedNotes.add(note);
  }

  @override
  Future<void> deleteNoteForever(String id) async {
    if (shouldThrowOnDelete) {
      throw Exception('Database delete failure');
    }
    deletedForeverIds.add(id);
  }

  @override
  Future<List<Note>> getTrashNotes(String userId) async {
    return List.from(trashNotesToReturn);
  }

  @override
  Future<List<Note>> getNotes(String userId, {int? limit, int? offset}) async {
    return List.from(normalNotesToReturn);
  }

  @override
  Future<List<Note>> getPinnedNotes(String userId) async {
    return List.from(pinnedNotesToReturn);
  }

  @override
  Future<List<Note>> getArchivedNotes(String userId) async {
    return List.from(archivedNotesToReturn);
  }

  @override
  Future<void> deleteNote(String id) async {
    deletedIds.add(id);
  }

  @override
  Future<List<Note>> getUnsyncedNotes(String userId) async => [];

  @override
  Future<List<Note>> searchNotes({required String userId, required String query}) async => [];

  @override
  Future<void> clearLocalData(String userId) async {}
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late RecordingNoteRepository repository;
  late NoteProvider provider;
  final List<String> canceledReminderIds = [];

  setUp(() {
    canceledReminderIds.clear();

    // Mock platform channel của ReminderService để chặn native MissingPluginException
    const channel = MethodChannel('dexterous.com/flutter/local_notifications');
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(
      channel,
      (MethodCall methodCall) async {
        if (methodCall.method == 'cancel') {
          final args = methodCall.arguments as Map<dynamic, dynamic>? ?? {};
          canceledReminderIds.add(args['id'].toString());
        }
        return null;
      },
    );

    repository = RecordingNoteRepository();
    provider = NoteProvider(repository);
  });

  group('FN-29 / FN-30: Note CRUD & Trash Lifecycle (NoteProvider White-box)', () {
    // ══════════════════════════════════════════════════════════════════════
    // NHÓM 1: CHUYỂN GHI CHÚ VÀO THÙNG RÁC (deleteNote)
    // ══════════════════════════════════════════════════════════════════════
    test('TC-WB-TRASH-01: deleteNote với ghi chú thường chuyển status sang trash và lưu repository', () async {
      final note = Note(
        id: 'n_norm_01',
        userId: 'u1',
        title: 'Ghi chú thường',
        content: 'Nội dung bình thường',
        status: 'normal',
        updatedAt: DateTime(2026, 10, 1),
      );

      // Nạp note vào in-memory list
      await provider.addNote(note);
      expect(provider.normalNotes.any((n) => n.id == 'n_norm_01'), isTrue);
      expect(provider.trashNotes.isEmpty, isTrue);

      // Thực hiện xóa vào thùng rác
      await provider.deleteNote('n_norm_01');

      // Xác minh trạng thái in-memory
      expect(provider.normalNotes.any((n) => n.id == 'n_norm_01'), isFalse);
      expect(provider.trashNotes.length, equals(1));
      expect(provider.trashNotes.first.id, equals('n_norm_01'));
      expect(provider.trashNotes.first.status, equals('trash'));
      expect(provider.trashNotes.first.isSynced, isFalse);

      // Xác minh repository lưu bản ghi cập nhật
      expect(repository.savedNotes.length, greaterThanOrEqualTo(2)); // 1 add + 1 trash update
      expect(repository.savedNotes.last.status, equals('trash'));
      expect(canceledReminderIds.isNotEmpty, isTrue, reason: 'Phải hủy nhắc nhở khi chuyển vào thùng rác');
    });

    test('TC-WB-TRASH-02: deleteNote với ghi chú ghim loại bỏ khỏi pinnedNotes và đưa vào trashNotes', () async {
      final pinnedNote = Note(
        id: 'n_pin_01',
        userId: 'u1',
        title: 'Ghi chú ghim',
        content: 'Quan trọng',
        status: 'pinned',
        updatedAt: DateTime(2026, 10, 1),
      );

      await provider.addNote(pinnedNote);
      expect(provider.pinnedNotes.any((n) => n.id == 'n_pin_01'), isTrue);

      await provider.deleteNote('n_pin_01');

      expect(provider.pinnedNotes.any((n) => n.id == 'n_pin_01'), isFalse);
      expect(provider.trashNotes.any((n) => n.id == 'n_pin_01'), isTrue);
      expect(provider.trashNotes.first.status, equals('trash'));
    });

    test('TC-WB-TRASH-03: deleteNote với ID không tồn tại không làm thay đổi danh sách và không gọi repo', () async {
      final initialSaves = repository.savedNotes.length;

      await provider.deleteNote('non_existent_id');

      expect(provider.trashNotes.isEmpty, isTrue);
      expect(repository.savedNotes.length, equals(initialSaves));
    });

    // ══════════════════════════════════════════════════════════════════════
    // NHÓM 2: KHÔI PHỤC TỪ THÙNG RÁC (restoreNote)
    // ══════════════════════════════════════════════════════════════════════
    test('TC-WB-TRASH-04: restoreNote khôi phục ghi chú từ thùng rác về normalNotes với status normal', () async {
      final trashedNote = Note(
        id: 'n_trash_01',
        userId: 'u1',
        title: 'Ghi chú khôi phục',
        content: 'Nội dung',
        status: 'trash',
        updatedAt: DateTime.now().subtract(const Duration(days: 2)),
      );

      // Giả lập nạp note thùng rác vào provider
      repository.trashNotesToReturn = [trashedNote];
      await provider.fetchTrashNotes('u1');
      expect(provider.trashNotes.length, equals(1));
      expect(provider.normalNotes.isEmpty, isTrue);

      // Thực hiện khôi phục
      await provider.restoreNote('n_trash_01');

      expect(provider.trashNotes.isEmpty, isTrue);
      expect(provider.normalNotes.length, equals(1));
      expect(provider.normalNotes.first.id, equals('n_trash_01'));
      expect(provider.normalNotes.first.status, equals('normal'));
      expect(repository.savedNotes.last.status, equals('normal'));
    });

    test('TC-WB-TRASH-05: restoreNote với ID không nằm trong thùng rác không làm thay đổi trạng thái', () async {
      final initialSaves = repository.savedNotes.length;

      await provider.restoreNote('unknown_trash_id');

      expect(provider.trashNotes.isEmpty, isTrue);
      expect(repository.savedNotes.length, equals(initialSaves));
    });

    // ══════════════════════════════════════════════════════════════════════
    // NHÓM 3: XÓA VĨNH VIỄN (deleteNoteForever)
    // ══════════════════════════════════════════════════════════════════════
    test('TC-WB-TRASH-06: deleteNoteForever xóa vĩnh viễn ghi chú khỏi thùng rác và gọi repo deleteNoteForever', () async {
      final trashedNote = Note(
        id: 'n_perm_01',
        userId: 'u1',
        title: 'Ghi chú xóa vĩnh viễn',
        content: 'Sẽ bị xóa vĩnh viễn',
        status: 'trash',
        updatedAt: DateTime.now().subtract(const Duration(days: 2)),
      );

      repository.trashNotesToReturn = [trashedNote];
      await provider.fetchTrashNotes('u1');
      expect(provider.trashNotes.length, equals(1));

      await provider.deleteNoteForever('n_perm_01');

      expect(provider.trashNotes.isEmpty, isTrue);
      expect(repository.deletedForeverIds, contains('n_perm_01'));
    });

    test('TC-WB-TRASH-07: deleteNoteForever xóa vĩnh viễn ghi chú có danh sách media khỏi bộ nhớ và repository', () async {
      final noteWithMedia = Note(
        id: 'n_media_01',
        userId: 'u1',
        title: 'Note có ảnh',
        content: 'Chứa hình ảnh',
        status: 'trash',
        imageUrls: ['https://res.cloudinary.com/demo/image/upload/sample.jpg'],
        audioUrls: ['https://res.cloudinary.com/demo/video/upload/sample.m4a'],
        updatedAt: DateTime.now().subtract(const Duration(days: 2)),
      );

      repository.trashNotesToReturn = [noteWithMedia];
      await provider.fetchTrashNotes('u1');

      await provider.deleteNoteForever('n_media_01');

      expect(provider.trashNotes.isEmpty, isTrue);
      expect(repository.deletedForeverIds, contains('n_media_01'));
    });

    // ══════════════════════════════════════════════════════════════════════
    // NHÓM 4: CHU KỲ 7 NGÀY TỰ ĐỘNG DỌN DẸP THÙNG RÁC (fetchTrashNotes)
    // ══════════════════════════════════════════════════════════════════════
    test('TC-WB-TRASH-08: fetchTrashNotes khi thùng rác rỗng không thực hiện xóa vĩnh viễn', () async {
      repository.trashNotesToReturn = [];

      await provider.fetchTrashNotes('u1');

      expect(provider.trashNotes.isEmpty, isTrue);
      expect(repository.deletedForeverIds.isEmpty, isTrue);
    });

    test('TC-WB-TRASH-09: fetchTrashNotes giữ lại ghi chú chưa đủ 7 ngày (daysInTrash < 7)', () async {
      final now = DateTime.now();
      final freshTrashNote = Note(
        id: 'n_recent_01',
        userId: 'u1',
        title: 'Vừa xóa 3 ngày trước',
        content: 'Chưa quá hạn',
        status: 'trash',
        updatedAt: now.subtract(const Duration(days: 3)),
      );

      repository.trashNotesToReturn = [freshTrashNote];

      await provider.fetchTrashNotes('u1');

      expect(provider.trashNotes.length, equals(1));
      expect(provider.trashNotes.first.id, equals('n_recent_01'));
      expect(repository.deletedForeverIds.isEmpty, isTrue);
    });

    test('TC-WB-TRASH-10a: fetchTrashNotes giữ lại ghi chú cận biên dưới 7 ngày (6 ngày 23 giờ 50 phút)', () async {
      final now = DateTime.now();
      final almost7DaysNote = Note(
        id: 'n_almost_7d',
        userId: 'u1',
        title: 'Chưa đủ 7 ngày',
        content: 'Cách mốc 7 ngày 10 phút',
        status: 'trash',
        updatedAt: now.subtract(const Duration(days: 6, hours: 23, minutes: 50)),
      );

      repository.trashNotesToReturn = [almost7DaysNote];

      await provider.fetchTrashNotes('u1');

      // daysInTrash == 6 (< 7) -> Phải giữ lại trong thùng rác
      expect(provider.trashNotes.length, equals(1));
      expect(provider.trashNotes.first.id, equals('n_almost_7d'));
      expect(repository.deletedForeverIds.isEmpty, isTrue);
    });

    test('TC-WB-TRASH-10b: fetchTrashNotes tự động dọn dẹp ghi chú chạm đúng mốc biên 7 ngày (7 ngày 0 giờ 5 giây)', () async {
      final now = DateTime.now();
      final exact7DaysNote = Note(
        id: 'n_exact_7d',
        userId: 'u1',
        title: 'Đúng 7 ngày',
        content: 'Đã đến hạn dọn dẹp',
        status: 'trash',
        updatedAt: now.subtract(const Duration(days: 7, seconds: 5)),
      );

      repository.trashNotesToReturn = [exact7DaysNote];

      await provider.fetchTrashNotes('u1');

      // daysInTrash == 7 (>= 7) -> Tự động purge vĩnh viễn khỏi trash
      expect(provider.trashNotes.isEmpty, isTrue);
      expect(repository.deletedForeverIds, contains('n_exact_7d'));
    });

    test('TC-WB-TRASH-11: fetchTrashNotes tự động dọn dẹp ghi chú quá hạn 7 ngày (15 ngày và 30 ngày)', () async {
      final now = DateTime.now();
      final oldNote1 = Note(
        id: 'n_old_15d',
        userId: 'u1',
        title: 'Quá hạn 15 ngày',
        content: 'Rác cũ',
        status: 'trash',
        updatedAt: now.subtract(const Duration(days: 15)),
      );
      final oldNote2 = Note(
        id: 'n_old_30d',
        userId: 'u1',
        title: 'Quá hạn 30 ngày',
        content: 'Rác rất cũ',
        status: 'trash',
        updatedAt: now.subtract(const Duration(days: 30)),
      );

      repository.trashNotesToReturn = [oldNote1, oldNote2];

      await provider.fetchTrashNotes('u1');

      expect(provider.trashNotes.isEmpty, isTrue);
      expect(repository.deletedForeverIds, contains('n_old_15d'));
      expect(repository.deletedForeverIds, contains('n_old_30d'));
    });

    // ══════════════════════════════════════════════════════════════════════
    // NHÓM 5: THAO TÁC HÀNG LOẠT TRONG THÙNG RÁC (Batch Selection)
    // ══════════════════════════════════════════════════════════════════════
    test('TC-WB-TRASH-12: restoreSelectedTrashNotes khôi phục tất cả ghi chú được chọn', () async {
      final now = DateTime.now();
      final noteA = Note(id: 't_a', userId: 'u1', title: 'A', content: 'A', status: 'trash', updatedAt: now);
      final noteB = Note(id: 't_b', userId: 'u1', title: 'B', content: 'B', status: 'trash', updatedAt: now);

      repository.trashNotesToReturn = [noteA, noteB];
      await provider.fetchTrashNotes('u1');

      // Chọn cả 2 ghi chú
      provider.toggleTrashSelection('t_a');
      provider.toggleTrashSelection('t_b');
      expect(provider.selectedTrashNoteIds.length, equals(2));

      // Khôi phục hàng loạt
      await provider.restoreSelectedTrashNotes();

      expect(provider.selectedTrashNoteIds.isEmpty, isTrue);
      expect(provider.trashNotes.isEmpty, isTrue);
      expect(provider.normalNotes.length, equals(2));
    });

    test('TC-WB-TRASH-13: deleteForeverSelectedTrashNotes xóa vĩnh viễn tất cả ghi chú được chọn', () async {
      final now = DateTime.now();
      final noteA = Note(id: 't_x', userId: 'u1', title: 'X', content: 'X', status: 'trash', updatedAt: now);
      final noteB = Note(id: 't_y', userId: 'u1', title: 'Y', content: 'Y', status: 'trash', updatedAt: now);

      repository.trashNotesToReturn = [noteA, noteB];
      await provider.fetchTrashNotes('u1');

      provider.toggleTrashSelection('t_x');
      provider.toggleTrashSelection('t_y');

      await provider.deleteForeverSelectedTrashNotes();

      expect(provider.selectedTrashNoteIds.isEmpty, isTrue);
      expect(provider.trashNotes.isEmpty, isTrue);
      expect(repository.deletedForeverIds, contains('t_x'));
      expect(repository.deletedForeverIds, contains('t_y'));
    });

    // ══════════════════════════════════════════════════════════════════════
    // NHÓM 6: XỬ LÝ NGOẠI LỆ VÀ ROBUSTNESS
    // ══════════════════════════════════════════════════════════════════════
    test('TC-WB-TRASH-14: Repository ném ngoại lệ khi saveNote làm lan truyền lỗi an toàn cho caller', () async {
      final note = Note(
        id: 'n_fail_save',
        userId: 'u1',
        title: 'Lỗi ghi DB',
        content: 'Content',
        status: 'normal',
        updatedAt: DateTime.now(),
      );

      await provider.addNote(note);
      repository.shouldThrowOnSave = true;

      // Khi deleteNote gọi saveNote, repository ném Exception
      expect(
        () async => await provider.deleteNote('n_fail_save'),
        throwsA(isA<Exception>()),
      );
    });

    test('TC-WB-TRASH-15: Platform channel ném ngoại lệ không làm sập deleteNoteForever (Robustness - NFR)', () async {
      final trashedNote = Note(
        id: 'n_fail_channel',
        userId: 'u1',
        title: 'Ghi chú lỗi channel',
        content: 'Test channel exception',
        status: 'trash',
        updatedAt: DateTime.now().subtract(const Duration(days: 1)),
      );

      repository.trashNotesToReturn = [trashedNote];
      await provider.fetchTrashNotes('u1');
      expect(provider.trashNotes.length, equals(1));

      // Giả lập platform channel cancelReminder ném ngoại lệ
      const channel = MethodChannel('dexterous.com/flutter/local_notifications');
      TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(
        channel,
        (MethodCall methodCall) async {
          throw PlatformException(code: 'CANCEL_ERROR', message: 'Notification service down');
        },
      );

      // Expected Result theo SRS REQ-09 & NFR Robustness:
      // Lỗi dịch vụ notification cục bộ không được làm sập quy trình xóa vĩnh viễn của người dùng.
      // deleteNoteForever phải bắt an toàn lỗi platform, không crash ra caller,
      // xóa khỏi memory và hoàn tất gọi repo deleteNoteForever.
      await provider.deleteNoteForever('n_fail_channel');

      expect(provider.trashNotes.isEmpty, isTrue,
          reason: 'Ghi chú phải được gỡ khỏi thùng rác dù Reminder service lỗi');
      expect(repository.deletedForeverIds, contains('n_fail_channel'),
          reason: 'Repository phải hoàn tất xóa vĩnh viễn DB dù Reminder service lỗi');
    });

    // ══════════════════════════════════════════════════════════════════════
    // NHÓM 7: XÁC MINH DEFECT-WB-TRASH-01 (CLOUD ASSET CLEANUP TRONG AUTO-PURGE)
    // ══════════════════════════════════════════════════════════════════════
    test('TC-WB-TRASH-16 (DEFECT-WB-TRASH-01): fetchTrashNotes tự động dọn dẹp ghi chú quá hạn 7 ngày phải dọn media Cloudinary', () async {
      dotenv.testLoad(fileInput: 'CLOUDINARY_CLOUD_NAME=demo\nCLOUDINARY_API_KEY=key\nCLOUDINARY_API_SECRET=sec\n');

      final overdueNoteWithMedia = Note(
        id: 'n_overdue_cloud',
        userId: 'u1',
        title: 'Note quá hạn có media',
        content: 'Chứa ảnh Cloudinary',
        status: 'trash',
        imageUrls: ['https://res.cloudinary.com/demo/image/upload/v1/smart_note/overdue_photo.jpg'],
        audioUrls: ['https://res.cloudinary.com/demo/video/upload/v1/smart_note/overdue_audio.m4a'],
        updatedAt: DateTime.now().subtract(const Duration(days: 8)),
      );

      repository.trashNotesToReturn = [overdueNoteWithMedia];

      final capturedUris = <Uri>[];
      await HttpOverrides.runWithHttpOverrides(() async {
        await provider.fetchTrashNotes('u1');
      }, MockHttpOverrides(capturedUris));

      // Kỳ vọng nghiệp vụ: Khi note quá hạn 7 ngày bị tự động xóa vĩnh viễn,
      // hệ thống phải dọn dẹp các tệp hình ảnh/âm thanh trên Cloudinary (ít nhất 1 request destroy)
      // Thực tế: fetchTrashNotes xóa DB nhưng bỏ qua dọn Cloudinary do note chưa có trong memory list
      expect(capturedUris.length, greaterThan(0),
          reason: 'DEFECT-WB-TRASH-01: Auto-purge note quá hạn 7 ngày phải dọn dẹp media Cloudinary thay vì bỏ qua do note null trong memory');
    });
  });
}
