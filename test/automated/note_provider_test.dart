
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/services.dart';
import 'package:smart_note_app/models/note_model.dart';
import 'package:smart_note_app/providers/note_provider.dart';
import 'package:smart_note_app/repositories/note_repository.dart';

class FakeNoteRepository implements NoteRepository {
  final Map<String, Note> savedNotes = {};
  final Set<String> permanentlyDeletedIds = {};

  @override
  Future<List<Note>> getNotes(
    String userId, {
    int limit = 20,
    int offset = 0,
  }) async {
    final notes = savedNotes.values
        .where((note) =>
            note.userId == userId &&
            note.status != 'trash' &&
            note.status != 'archived' &&
            note.status != 'pinned')
        .toList();

    if (offset >= notes.length) return [];

    final end = (offset + limit).clamp(0, notes.length);
    return notes.sublist(offset, end);
  }

  @override
  Future<List<Note>> getPinnedNotes(String userId) async {
    return savedNotes.values
        .where((note) =>
            note.userId == userId && note.status == 'pinned')
        .toList();
  }

  @override
  Future<void> saveNote(Note note) async {
    savedNotes[note.id] = note;
  }

  @override
  Future<void> deleteNote(String id) async {
    savedNotes.remove(id);
  }

  @override
  Future<List<Note>> getUnsyncedNotes(String userId) async {
    return savedNotes.values
        .where((note) => note.userId == userId && !note.isSynced)
        .toList();
  }

  @override
  Future<List<Note>> searchNotes({
    required String userId,
    required String query,
  }) async {
    final q = query.toLowerCase();

    return savedNotes.values.where((note) {
      return note.userId == userId &&
          note.status != 'trash' &&
          note.status != 'archived' &&
          (note.title.toLowerCase().contains(q) ||
              note.content.toLowerCase().contains(q));
    }).toList();
  }

  @override
  Future<List<Note>> getTrashNotes(String userId) async {
    return savedNotes.values
        .where((note) =>
            note.userId == userId && note.status == 'trash')
        .toList();
  }

  @override
  Future<void> clearLocalData(String userId) async {
    savedNotes.removeWhere((_, note) => note.userId == userId);
  }

  @override
  Future<void> deleteNoteForever(String id) async {
    savedNotes.remove(id);
    permanentlyDeletedIds.add(id);
  }

  @override
  Future<List<Note>> getArchivedNotes(String userId) async {
    return savedNotes.values
        .where((note) =>
            note.userId == userId && note.status == 'archived')
        .toList();
  }
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  const notificationChannel =
      MethodChannel('dexterous.com/flutter/local_notifications');

  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
      .setMockMethodCallHandler(notificationChannel, (call) async {
    return null;
  });

  late FakeNoteRepository repository;
  late NoteProvider provider;

  Note createTestNote({
    String id = 'note-1',
    String title = 'Test note',
    String content = 'Test content',
    String status = 'normal',
  }) {
    return Note(
      id: id,
      userId: 'user-1',
      title: title,
      content: content,
      status: status,
    );
  }

  setUp(() {
    repository = FakeNoteRepository();
    provider = NoteProvider(repository);
  });

  tearDown(() {
    provider.dispose();
  });

group('NoteProvider - Pin note', () {
  test('Ghim ghi chú bình thường thành công', () async {
    final note = createTestNote(
      id: 'pin-1',
      status: 'normal',
    );

    await provider.addNote(note);
    await provider.togglePin(note);

    expect(
      repository.savedNotes['pin-1']?.status,
      'pinned',
    );

    expect(
      provider.pinnedNotes.any((n) => n.id == 'pin-1'),
      isTrue,
    );
  });

  test('Bỏ ghim ghi chú đã ghim thành công', () async {
    final note = createTestNote(
      id: 'pin-2',
      status: 'pinned',
    );

    await repository.saveNote(note);
    await provider.fetchNotes('user-1');

    final pinnedNote = provider.pinnedNotes.firstWhere(
      (n) => n.id == 'pin-2',
    );

    await provider.togglePin(pinnedNote);

    expect(
      repository.savedNotes['pin-2']?.status,
      'normal',
    );

    expect(
      provider.pinnedNotes.any((n) => n.id == 'pin-2'),
      isFalse,
    );
  });
});

  group('NoteProvider - Archive note', () {
    test('Lưu trữ ghi chú', () async {
      final note = createTestNote();
      await provider.addNote(note);

      await provider.archiveNote('note-1');

      expect(provider.notes.any((n) => n.id == 'note-1'), isFalse);
      expect(provider.archivedNotes.any((n) => n.id == 'note-1'), isTrue);
      expect(repository.savedNotes['note-1']?.status, 'archived');
    });

    test('Bỏ lưu trữ ghi chú', () async {
  final note = createTestNote(status: 'archived');

  // Lưu dữ liệu vào Fake Repository trước
  await repository.saveNote(note);

  // Nạp ghi chú vào danh sách lưu trữ của Provider
  await provider.fetchArchivedNotes('user-1');

  // Thực hiện bỏ lưu trữ
  await provider.unarchiveNote('note-1');

  expect(
    provider.archivedNotes.any((n) => n.id == 'note-1'),
    isFalse,
  );

  expect(
    provider.notes.any((n) => n.id == 'note-1'),
    isTrue,
  );

  expect(repository.savedNotes['note-1']?.status, 'normal');
});
  });

  group('NoteProvider - Restore note', () {
    test('Khôi phục ghi chú từ thùng rác', () async {
      final note = createTestNote(status: 'trash');
      await provider.addNote(note);

      await provider.fetchTrashNotes('user-1');
      await provider.restoreNote('note-1');

      expect(provider.trashNotes.any((n) => n.id == 'note-1'), isFalse);
      expect(provider.notes.any((n) => n.id == 'note-1'), isTrue);
      expect(repository.savedNotes['note-1']?.status, 'normal');
    });
  });


  group('NoteProvider - Create and Edit note', () {
    test('Tạo ghi chú mới thành công', () async {
      final note = createTestNote(
        id: 'create-1',
        title: 'Ghi chú mới',
        content: 'Nội dung ghi chú mới',
      );

      await provider.addNote(note);

      expect(
        provider.notes.any((n) => n.id == 'create-1'),
        isTrue,
      );

      expect(repository.savedNotes['create-1']?.title, 'Ghi chú mới');
      expect(
        repository.savedNotes['create-1']?.content,
        'Nội dung ghi chú mới',
      );
    });

    test('Chỉnh sửa tiêu đề và nội dung ghi chú', () async {
      final note = createTestNote(
        id: 'edit-1',
        title: 'Tiêu đề ban đầu',
        content: 'Nội dung ban đầu',
      );

      await provider.addNote(note);

      final editedNote = Note(
        id: note.id,
        userId: note.userId,
        title: 'Tiêu đề đã sửa',
        content: 'Nội dung đã sửa',
        status: note.status,
        createdAt: note.createdAt,
        updatedAt: DateTime.now(),
      );

      await provider.updateNote(editedNote);

      expect(
        provider.notes.any(
          (n) => n.id == 'edit-1' && n.title == 'Tiêu đề đã sửa',
        ),
        isTrue,
      );

      expect(
        repository.savedNotes['edit-1']?.content,
        'Nội dung đã sửa',
      );
    });
  });


  group('NoteProvider - Search note', () {
  test('Search note by content', () async {
    final note = createTestNote(
      id: 'search-content-1',
      title: 'Ghi chú',
      content: 'Ôn tập kiểm thử phần mềm',
    );

    repository.savedNotes[note.id] = note;

    provider.search('kiểm thử', 'user-1');

    await Future<void>.delayed(
      const Duration(milliseconds: 600),
    );

    expect(
      provider.notes.any((n) => n.id == note.id),
      isTrue,
    );

    provider.clearSearch();
  });

  test('Search note with no matching result', () async {
    final note = createTestNote(
      id: 'search-empty-1',
      title: 'Meeting Monday',
      content: 'Discuss project',
    );

    repository.savedNotes[note.id] = note;

    provider.search('not-exist-xyz', 'user-1');

    await Future<void>.delayed(
      const Duration(milliseconds: 600),
    );

    expect(
      provider.notes.any((n) => n.id == note.id),
      isFalse,
    );

    provider.clearSearch();
  });

  test('Clear search', () async {
    final note = createTestNote(
      id: 'search-clear-1',
      title: 'Meeting Monday',
    );

    repository.savedNotes[note.id] = note;

    provider.search('Meeting', 'user-1');

    await Future<void>.delayed(
      const Duration(milliseconds: 600),
    );

    expect(provider.isSearching, isTrue);

    provider.clearSearch();

    expect(provider.isSearching, isFalse);
  });
});


    group('NoteProvider - Note lifecycle', () {
    test('Xóa ghi chú: chuyển vào thùng rác', () async {
      final note = createTestNote(
        id: 'trash-1',
        title: 'Note to trash',
      );

      await provider.addNote(note);
      await provider.deleteNote('trash-1');

      expect(
        provider.notes.any((n) => n.id == 'trash-1'),
        isFalse,
      );
      expect(
        provider.trashNotes.any((n) => n.id == 'trash-1'),
        isTrue,
      );
      expect(repository.savedNotes['trash-1']?.status, 'trash');
    });

    test('Khôi phục ghi chú từ thùng rác', () async {
      final note = createTestNote(
        id: 'trash-2',
        title: 'Note to restore',
      );

      await provider.addNote(note);
      await provider.deleteNote('trash-2');
      await provider.restoreNote('trash-2');

      expect(
        provider.trashNotes.any((n) => n.id == 'trash-2'),
        isFalse,
      );
      expect(
        provider.notes.any((n) => n.id == 'trash-2'),
        isTrue,
      );
      expect(repository.savedNotes['trash-2']?.status, 'normal');
    });

    test('Xóa vĩnh viễn ghi chú trong thùng rác', () async {
      final note = createTestNote(
        id: 'trash-3',
        title: 'Note to delete forever',
        status: 'trash',
      );

      await repository.saveNote(note);
      await provider.fetchTrashNotes('user-1');
      await provider.deleteNoteForever('trash-3');

      expect(
        provider.trashNotes.any((n) => n.id == 'trash-3'),
        isFalse,
      );
      expect(repository.savedNotes.containsKey('trash-3'), isFalse);
      expect(repository.permanentlyDeletedIds.contains('trash-3'), isTrue);
    });

    test('Xóa ghi chú đã ghim vào thùng rác', () async {
      final note = createTestNote(
        id: 'pinned-trash-1',
        status: 'pinned',
      );

      await provider.addNote(note);
      await provider.deleteNote('pinned-trash-1');

      expect(
        provider.pinnedNotes.any((n) => n.id == 'pinned-trash-1'),
        isFalse,
      );
      expect(
        provider.trashNotes.any((n) => n.id == 'pinned-trash-1'),
        isTrue,
      );
      expect(
        repository.savedNotes['pinned-trash-1']?.status,
        'trash',
      );
    });

    test('Khôi phục ghi chú đã ghim từ thùng rác', () async {
      final note = createTestNote(
        id: 'pinned-trash-2',
        status: 'pinned',
      );

      await provider.addNote(note);
      await provider.deleteNote('pinned-trash-2');
      await provider.restoreNote('pinned-trash-2');

      expect(
        provider.trashNotes.any((n) => n.id == 'pinned-trash-2'),
        isFalse,
      );
      expect(
        provider.notes.any((n) => n.id == 'pinned-trash-2'),
        isTrue,
      );
      expect(
        repository.savedNotes['pinned-trash-2']?.status,
        'normal',
      );
    });
  });
}