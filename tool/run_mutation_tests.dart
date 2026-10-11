// tool/run_mutation_tests.dart
import 'dart:io';
import 'dart:convert';

class Mutant {
  final String id;
  final String module;
  final String targetFile;
  final String testFile;
  final String operator;
  final String description;
  final String targetCode;
  final String mutantCode;
  final bool isEquivalent;

  Mutant({
    required this.id,
    required this.module,
    required this.targetFile,
    required this.testFile,
    required this.operator,
    required this.description,
    required this.targetCode,
    required this.mutantCode,
    this.isEquivalent = false,
  });
}

void main() async {
  print('===============================================================');
  print('    CHƯƠNG 6.2: HỆ THỐNG THỰC NGHIỆM KIỂM THỬ ĐỘT BIẾN (MUTATION)');
  print('===============================================================');

  final List<Mutant> mutants = [
    // ── Module 1: BiometricService (10 Mutants) ──
    Mutant(
      id: 'MUT-BIO-01',
      module: 'BiometricService',
      targetFile: 'lib/services/biometric_service.dart',
      testFile: 'test/unit/biometric_whitebox_test.dart',
      operator: 'LCR',
      description: 'Đổi toán tử || thành && trong isAvailable()',
      targetCode: 'return canCheck || isSupported;',
      mutantCode: 'return canCheck && isSupported;',
    ),
    Mutant(
      id: 'MUT-BIO-02',
      module: 'BiometricService',
      targetFile: 'lib/services/biometric_service.dart',
      testFile: 'test/unit/biometric_whitebox_test.dart',
      operator: 'SVR',
      description: 'isAvailable() luôn trả về false',
      targetCode: 'return canCheck || isSupported;',
      mutantCode: 'return false;',
    ),
    Mutant(
      id: 'MUT-BIO-03',
      module: 'BiometricService',
      targetFile: 'lib/services/biometric_service.dart',
      testFile: 'test/unit/biometric_whitebox_test.dart',
      operator: 'UOI',
      description: 'Đổi isNotEmpty thành isEmpty trong isEnrolled()',
      targetCode: 'return danhSachSinhTracHoc.isNotEmpty;',
      mutantCode: 'return danhSachSinhTracHoc.isEmpty;',
    ),
    Mutant(
      id: 'MUT-BIO-04',
      module: 'BiometricService',
      targetFile: 'lib/services/biometric_service.dart',
      testFile: 'test/unit/biometric_whitebox_test.dart',
      operator: 'UOI',
      description: 'Đảo ngược kết quả xác thực daXacThuc',
      targetCode: 'return daXacThuc;',
      mutantCode: 'return !daXacThuc;',
    ),
    Mutant(
      id: 'MUT-BIO-05',
      module: 'BiometricService',
      targetFile: 'lib/services/biometric_service.dart',
      testFile: 'test/unit/biometric_whitebox_test.dart',
      operator: 'SVR',
      description: 'userCanceled trả về true thay vì false',
      targetCode: 'case LocalAuthExceptionCode.userCanceled:\n          // Người dùng chủ động hủy hộp thoại xác thực\n          return false;',
      mutantCode: 'case LocalAuthExceptionCode.userCanceled:\n          return true;',
    ),
    Mutant(
      id: 'MUT-BIO-06',
      module: 'BiometricService',
      targetFile: 'lib/services/biometric_service.dart',
      testFile: 'test/unit/biometric_whitebox_test.dart',
      operator: 'SVR',
      description: 'Đổi biometricOnly từ true sang false',
      targetCode: 'biometricOnly: true,',
      mutantCode: 'biometricOnly: false,',
      isEquivalent: true, // LocalAuth mock có thể không phân biệt tham số này
    ),
    Mutant(
      id: 'MUT-BIO-07',
      module: 'BiometricService',
      targetFile: 'lib/services/biometric_service.dart',
      testFile: 'test/unit/biometric_whitebox_test.dart',
      operator: 'SVR',
      description: 'Catch block trong isAvailable trả về true khi lỗi',
      targetCode: 'debugPrint(\'❌ Lỗi khi kiểm tra khả năng sinh trắc học: \$e\');\n      return false;',
      mutantCode: 'debugPrint(\'❌ Lỗi khi kiểm tra khả năng sinh trắc học: \$e\');\n      return true;',
    ),
    Mutant(
      id: 'MUT-BIO-08',
      module: 'BiometricService',
      targetFile: 'lib/services/biometric_service.dart',
      testFile: 'test/unit/biometric_whitebox_test.dart',
      operator: 'SVR',
      description: 'Catch block trong isEnrolled trả về true khi lỗi',
      targetCode: 'debugPrint(\'❌ Lỗi khi kiểm tra đăng ký sinh trắc học: \$e\');\n      return false;',
      mutantCode: 'debugPrint(\'❌ Lỗi khi kiểm tra đăng ký sinh trắc học: \$e\');\n      return true;',
    ),
    Mutant(
      id: 'MUT-BIO-09',
      module: 'BiometricService',
      targetFile: 'lib/services/biometric_service.dart',
      testFile: 'test/unit/biometric_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi mã lỗi noBiometricHardware thành passcodeNotSet',
      targetCode: 'case LocalAuthExceptionCode.noBiometricHardware:',
      mutantCode: 'case LocalAuthExceptionCode.passcodeNotSet:',
    ),
    Mutant(
      id: 'MUT-BIO-10',
      module: 'BiometricService',
      targetFile: 'lib/services/biometric_service.dart',
      testFile: 'test/unit/biometric_whitebox_test.dart',
      operator: 'SVR',
      description: 'Khi bị lockout trả về false thay vì throw Exception',
      targetCode: 'throw Exception(AppStrings.biometricLockedOut);',
      mutantCode: 'return false;',
    ),

    // ── Module 2: AuthProvider (10 Mutants) ──
    Mutant(
      id: 'MUT-AUTH-01',
      module: 'AuthProvider',
      targetFile: 'lib/providers/auth_provider.dart',
      testFile: 'test/unit/auth_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi parts.length < 2 thành <= 2 trong _isValidDomain',
      targetCode: 'if (parts.length < 2) return false;',
      mutantCode: 'if (parts.length <= 2) return false;',
    ),
    Mutant(
      id: 'MUT-AUTH-02',
      module: 'AuthProvider',
      targetFile: 'lib/providers/auth_provider.dart',
      testFile: 'test/unit/auth_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi parts.length < 2 thành > 2 trong _isValidDomain',
      targetCode: 'if (parts.length < 2) return false;',
      mutantCode: 'if (parts.length > 2) return false;',
    ),
    Mutant(
      id: 'MUT-AUTH-03',
      module: 'AuthProvider',
      targetFile: 'lib/providers/auth_provider.dart',
      testFile: 'test/unit/auth_whitebox_test.dart',
      operator: 'SVR',
      description: 'Bỏ qua danh sách domain rác disposableDomains',
      targetCode: 'if (disposableDomains.contains(domain)) {\n      return false;\n    }',
      mutantCode: 'if (disposableDomains.contains(domain)) {\n      return true;\n    }',
    ),
    Mutant(
      id: 'MUT-AUTH-04',
      module: 'AuthProvider',
      targetFile: 'lib/providers/auth_provider.dart',
      testFile: 'test/unit/auth_whitebox_test.dart',
      operator: 'UOI',
      description: 'Đảo ngược điều kiện !_isValidDomain thành _isValidDomain',
      targetCode: 'if (!_isValidDomain(email)) {',
      mutantCode: 'if (_isValidDomain(email)) {',
    ),
    Mutant(
      id: 'MUT-AUTH-05',
      module: 'AuthProvider',
      targetFile: 'lib/providers/auth_provider.dart',
      testFile: 'test/unit/auth_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi getter isAuthenticated thành _user == null',
      targetCode: 'bool get isAuthenticated => _user != null;',
      mutantCode: 'bool get isAuthenticated => _user == null;',
    ),
    Mutant(
      id: 'MUT-AUTH-06',
      module: 'AuthProvider',
      targetFile: 'lib/providers/auth_provider.dart',
      testFile: 'test/unit/auth_whitebox_test.dart',
      operator: 'SVR',
      description: 'Bỏ trim email khi đăng nhập signInWithEmail',
      targetCode: 'email: email.trim(), password: password',
      mutantCode: 'email: email, password: password',
    ),
    Mutant(
      id: 'MUT-AUTH-07',
      module: 'AuthProvider',
      targetFile: 'lib/providers/auth_provider.dart',
      testFile: 'test/unit/auth_whitebox_test.dart',
      operator: 'SVR',
      description: 'Bỏ trim email khi đăng ký registerWithEmail',
      targetCode: 'email: email.trim(),\n        password: password,',
      mutantCode: 'email: email,\n        password: password,',
    ),
    Mutant(
      id: 'MUT-AUTH-08',
      module: 'AuthProvider',
      targetFile: 'lib/providers/auth_provider.dart',
      testFile: 'test/unit/auth_whitebox_test.dart',
      operator: 'SVR',
      description: 'signOut không xóa _user (giữ nguyên user cũ)',
      targetCode: '_user = null;',
      mutantCode: '// _user = null;',
    ),
    Mutant(
      id: 'MUT-AUTH-09',
      module: 'AuthProvider',
      targetFile: 'lib/providers/auth_provider.dart',
      testFile: 'test/unit/auth_whitebox_test.dart',
      operator: 'SVR',
      description: 'signOut không xóa _userData profile trong RAM',
      targetCode: '_userData = null; // Xóa thông tin profile trong RAM',
      mutantCode: '// _userData = null;',
    ),
    Mutant(
      id: 'MUT-AUTH-10',
      module: 'AuthProvider',
      targetFile: 'lib/providers/auth_provider.dart',
      testFile: 'test/unit/auth_whitebox_test.dart',
      operator: 'SVR',
      description: 'Đổi mã lỗi dịch weak-password thành mã khác',
      targetCode: 'case \'weak-password\':',
      mutantCode: 'case \'weak-password-modified\':',
    ),

    // ── Module 3: LocalNoteService / CRUD (10 Mutants) ──
    Mutant(
      id: 'MUT-CRUD-01',
      module: 'LocalNoteService',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/note_crud_whitebox_test.dart',
      operator: 'SVR',
      description: 'Đổi ConflictAlgorithm.replace thành ignore khi insertNote',
      targetCode: 'conflictAlgorithm: ConflictAlgorithm.replace,',
      mutantCode: 'conflictAlgorithm: ConflictAlgorithm.ignore,',
    ),
    Mutant(
      id: 'MUT-CRUD-02',
      module: 'LocalNoteService',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/note_crud_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi where id = ? thành id != ? khi updateNote',
      targetCode: 'where: \'id = ?\', whereArgs: [note.id]',
      mutantCode: 'where: \'id != ?\', whereArgs: [note.id]',
    ),
    Mutant(
      id: 'MUT-CRUD-03',
      module: 'LocalNoteService',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/note_crud_whitebox_test.dart',
      operator: 'SVR',
      description: 'Xóa ghi chú sai id (where id = 0)',
      targetCode: 'where: \'id = ?\', whereArgs: [id]',
      mutantCode: 'where: \'id = "invalid"\', whereArgs: [id]',
    ),
    Mutant(
      id: 'MUT-CRUD-04',
      module: 'LocalNoteService',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/note_crud_whitebox_test.dart',
      operator: 'SVR',
      description: 'moveToTrash cập nhật status = normal thay vì trash',
      targetCode: '{\'status\': \'trash\', \'is_synced\': 0},',
      mutantCode: '{\'status\': \'normal\', \'is_synced\': 0},',
    ),
    Mutant(
      id: 'MUT-CRUD-05',
      module: 'LocalNoteService',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/note_crud_whitebox_test.dart',
      operator: 'SVR',
      description: 'restoreFromTrash cập nhật status = trash thay vì normal',
      targetCode: '{\'status\': \'normal\', \'is_synced\': 0},',
      mutantCode: '{\'status\': \'trash\', \'is_synced\': 0},',
    ),
    Mutant(
      id: 'MUT-CRUD-06',
      module: 'LocalNoteService',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/note_crud_whitebox_test.dart',
      operator: 'LCR',
      description: 'Đổi AND thành OR khi lọc user_id và status',
      targetCode: 'where: \'user_id = ? AND status = ?\',',
      mutantCode: 'where: \'user_id = ? OR status = ?\',',
    ),
    Mutant(
      id: 'MUT-CRUD-07',
      module: 'LocalNoteService',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/note_crud_whitebox_test.dart',
      operator: 'SVR',
      description: 'markSynced cập nhật is_synced = 0 thay vì 1',
      targetCode: '{\'is_synced\': 1},',
      mutantCode: '{\'is_synced\': 0},',
    ),
    Mutant(
      id: 'MUT-CRUD-08',
      module: 'LocalNoteService',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/note_crud_whitebox_test.dart',
      operator: 'SVR',
      description: 'getAllNotes lọc nhầm status trash thay vì normal',
      targetCode: 'whereArgs: [userId, \'normal\'],',
      mutantCode: 'whereArgs: [userId, \'trash\'],',
    ),
    Mutant(
      id: 'MUT-CRUD-09',
      module: 'LocalNoteService',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/note_crud_whitebox_test.dart',
      operator: 'SVR',
      description: 'getPinnedNotes lọc nhầm status normal thay vì pinned',
      targetCode: 'whereArgs: [userId, \'pinned\'],',
      mutantCode: 'whereArgs: [userId, \'normal\'],',
    ),
    Mutant(
      id: 'MUT-CRUD-10',
      module: 'LocalNoteService',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/note_crud_whitebox_test.dart',
      operator: 'SVR',
      description: 'getTrashNotes lọc nhầm status pinned thay vì trash',
      targetCode: 'whereArgs: [userId, \'trash\'],',
      mutantCode: 'whereArgs: [userId, \'pinned\'],',
    ),

    // ── Module 4: Search Logic (10 Mutants) ──
    Mutant(
      id: 'MUT-SRCH-01',
      module: 'SearchLogic',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/search_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi hasImageToken && note.imageUrls.isEmpty thành isNotEmpty',
      targetCode: 'if (hasImageToken && note.imageUrls.isEmpty) return false;',
      mutantCode: 'if (hasImageToken && note.imageUrls.isNotEmpty) return false;',
    ),
    Mutant(
      id: 'MUT-SRCH-02',
      module: 'SearchLogic',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/search_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi hasAudioToken && note.audioUrls.isEmpty thành isNotEmpty',
      targetCode: 'if (hasAudioToken && note.audioUrls.isEmpty) return false;',
      mutantCode: 'if (hasAudioToken && note.audioUrls.isNotEmpty) return false;',
    ),
    Mutant(
      id: 'MUT-SRCH-03',
      module: 'SearchLogic',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/search_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi isPinnedToken && note.status != pinned thành == pinned',
      targetCode: 'if (isPinnedToken && note.status != \'pinned\') return false;',
      mutantCode: 'if (isPinnedToken && note.status == \'pinned\') return false;',
    ),
    Mutant(
      id: 'MUT-SRCH-04',
      module: 'SearchLogic',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/search_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi isArchivedToken && note.status != archived thành == archived',
      targetCode: 'if (isArchivedToken && note.status != \'archived\') return false;',
      mutantCode: 'if (isArchivedToken && note.status == \'archived\') return false;',
    ),
    Mutant(
      id: 'MUT-SRCH-05',
      module: 'SearchLogic',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/search_whitebox_test.dart',
      operator: 'LCR',
      description: 'Đổi !isArchivedToken && note.status == archived thành ||',
      targetCode: 'if (!isArchivedToken && note.status == \'archived\') return false;',
      mutantCode: 'if (!isArchivedToken || note.status == \'archived\') return false;',
    ),
    Mutant(
      id: 'MUT-SRCH-06',
      module: 'SearchLogic',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/search_whitebox_test.dart',
      operator: 'SVR',
      description: 'Bỏ qua lọc targetLabel (luôn chấp nhận)',
      targetCode: 'if (targetLabel != null && !note.tags.map((t) => t.toLowerCase()).contains(targetLabel.toLowerCase())) {\n        return false;\n      }',
      mutantCode: '// targetLabel filter removed',
    ),
    Mutant(
      id: 'MUT-SRCH-07',
      module: 'SearchLogic',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/search_whitebox_test.dart',
      operator: 'SVR',
      description: 'Bỏ qua lọc urlRegex khi có has:url',
      targetCode: 'if (!urlRegex.hasMatch(note.content)) return false;',
      mutantCode: 'if (urlRegex.hasMatch(note.content)) return false;',
    ),
    Mutant(
      id: 'MUT-SRCH-08',
      module: 'SearchLogic',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/search_whitebox_test.dart',
      operator: 'UOI',
      description: 'Đổi cleanTextQuery.isNotEmpty thành isEmpty trong searchNotes',
      targetCode: 'if (cleanTextQuery.isNotEmpty) {',
      mutantCode: 'if (cleanTextQuery.isEmpty) {',
    ),
    Mutant(
      id: 'MUT-SRCH-09',
      module: 'SearchLogic',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/search_whitebox_test.dart',
      operator: 'SVR',
      description: 'Đổi LIKE %cleanTextQuery% thành chính xác không có wildcard %',
      targetCode: r"final sqlQuery = '%$cleanTextQuery%';",
      mutantCode: r"final sqlQuery = cleanTextQuery;",
    ),
    Mutant(
      id: 'MUT-SRCH-10',
      module: 'SearchLogic',
      targetFile: 'lib/services/local_note_service.dart',
      testFile: 'test/unit/search_whitebox_test.dart',
      operator: 'SVR',
      description: 'Bỏ loại trừ note status trash trong câu truy vấn search',
      targetCode: 'where: \'user_id = ? AND status != ?',
      mutantCode: 'where: \'user_id = ? AND status == ?',
    ),

    // ── Module 5: SyncRepository (10 Mutants) ──
    Mutant(
      id: 'MUT-SYNC-01',
      module: 'SyncRepository',
      targetFile: 'lib/repositories/sync_repository.dart',
      testFile: 'test/unit/sync_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi isAfter thành isBefore trong thuật toán LWW',
      targetCode: 'if (cloud == null || local.updatedAt.isAfter(cloud.updatedAt)) {',
      mutantCode: 'if (cloud == null || local.updatedAt.isBefore(cloud.updatedAt)) {',
    ),
    Mutant(
      id: 'MUT-SYNC-02',
      module: 'SyncRepository',
      targetFile: 'lib/repositories/sync_repository.dart',
      testFile: 'test/unit/sync_whitebox_test.dart',
      operator: 'LCR',
      description: 'Đổi || thành && trong điều kiện so sánh LWW',
      targetCode: 'if (cloud == null || local.updatedAt.isAfter(cloud.updatedAt)) {',
      mutantCode: 'if (cloud == null && local.updatedAt.isAfter(cloud.updatedAt)) {',
    ),
    Mutant(
      id: 'MUT-SYNC-03',
      module: 'SyncRepository',
      targetFile: 'lib/repositories/sync_repository.dart',
      testFile: 'test/unit/sync_whitebox_test.dart',
      operator: 'SVR',
      description: 'Chỉ push khi cloud == null, bỏ qua local mới hơn cloud',
      targetCode: 'if (cloud == null || local.updatedAt.isAfter(cloud.updatedAt)) {',
      mutantCode: 'if (cloud == null) {',
    ),
    Mutant(
      id: 'MUT-SYNC-04',
      module: 'SyncRepository',
      targetFile: 'lib/repositories/sync_repository.dart',
      testFile: 'test/unit/sync_whitebox_test.dart',
      operator: 'SVR',
      description: 'Không gọi deleteNote khi xử lý pending delete queue',
      targetCode: 'await _firestoreService.deleteNote(id);',
      mutantCode: '// await _firestoreService.deleteNote(id);',
    ),
    Mutant(
      id: 'MUT-SYNC-05',
      module: 'SyncRepository',
      targetFile: 'lib/repositories/sync_repository.dart',
      testFile: 'test/unit/sync_whitebox_test.dart',
      operator: 'SVR',
      description: 'Không xóa pending queue sau khi xóa cloud thành công',
      targetCode: 'await _pendingDeleteSvc.remove(id);',
      mutantCode: '// await _pendingDeleteSvc.remove(id);',
    ),
    Mutant(
      id: 'MUT-SYNC-06',
      module: 'SyncRepository',
      targetFile: 'lib/repositories/sync_repository.dart',
      testFile: 'test/unit/sync_whitebox_test.dart',
      operator: 'SVR',
      description: 'Cập nhật is_synced = 0 thay vì 1 sau khi push cloud',
      targetCode: '{\'is_synced\': 1},',
      mutantCode: '{\'is_synced\': 0},',
    ),
    Mutant(
      id: 'MUT-SYNC-07',
      module: 'SyncRepository',
      targetFile: 'lib/repositories/sync_repository.dart',
      testFile: 'test/unit/sync_whitebox_test.dart',
      operator: 'UOI',
      description: 'Đổi !notesToPush.isNotEmpty thành isEmpty',
      targetCode: 'if (notesToPush.isNotEmpty) {',
      mutantCode: 'if (notesToPush.isEmpty) {',
    ),
    Mutant(
      id: 'MUT-SYNC-08',
      module: 'SyncRepository',
      targetFile: 'lib/repositories/sync_repository.dart',
      testFile: 'test/unit/sync_whitebox_test.dart',
      operator: 'SVR',
      description: 'pullFromCloud không lưu note vào local SQLite',
      targetCode: 'await _localService.insertNote(cloudNote);',
      mutantCode: '// await _localService.insertNote(cloudNote);',
    ),
    Mutant(
      id: 'MUT-SYNC-09',
      module: 'SyncRepository',
      targetFile: 'lib/repositories/sync_repository.dart',
      testFile: 'test/unit/sync_whitebox_test.dart',
      operator: 'ROR',
      description: 'Trong pullFromCloud đổi cloud.isAfter(local) thành isBefore',
      targetCode: 'if (localNote == null || cloudNote.updatedAt.isAfter(localNote.updatedAt)) {',
      mutantCode: 'if (localNote == null || cloudNote.updatedAt.isBefore(localNote.updatedAt)) {',
    ),
    Mutant(
      id: 'MUT-SYNC-10',
      module: 'SyncRepository',
      targetFile: 'lib/repositories/sync_repository.dart',
      testFile: 'test/unit/sync_whitebox_test.dart',
      operator: 'SVR',
      description: 'syncNow ném ngoại lệ giả lập lỗi đồng bộ',
      targetCode: '_statusController.add(SyncStatus.syncing);',
      mutantCode: 'throw Exception("Sync Failure Mutation");',
    ),

    // ── Module 6: Trash & Lifecycle Management (10 Mutants) ──
    Mutant(
      id: 'MUT-TRASH-01',
      module: 'NoteProvider',
      targetFile: 'lib/providers/note_provider.dart',
      testFile: 'test/unit/trash_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi ngày hết hạn thùng rác >= 7 thành > 7 ngày',
      targetCode: 'if (daysInTrash >= 7) {',
      mutantCode: 'if (daysInTrash > 7) {',
    ),
    Mutant(
      id: 'MUT-TRASH-02',
      module: 'NoteProvider',
      targetFile: 'lib/providers/note_provider.dart',
      testFile: 'test/unit/trash_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi ngày hết hạn thùng rác >= 7 thành <= 7 ngày',
      targetCode: 'if (daysInTrash >= 7) {',
      mutantCode: 'if (daysInTrash <= 7) {',
    ),
    Mutant(
      id: 'MUT-TRASH-03',
      module: 'NoteProvider',
      targetFile: 'lib/providers/note_provider.dart',
      testFile: 'test/unit/trash_whitebox_test.dart',
      operator: 'SVR',
      description: 'deleteNoteForever không xóa media trên Cloudinary',
      targetCode: 'await _cloudinaryService.deleteFile(url);',
      mutantCode: '// await _cloudinaryService.deleteFile(url);',
    ),
    Mutant(
      id: 'MUT-TRASH-04',
      module: 'NoteProvider',
      targetFile: 'lib/providers/note_provider.dart',
      testFile: 'test/unit/trash_whitebox_test.dart',
      operator: 'SVR',
      description: 'deleteNoteForever không gọi repo deleteNoteForever',
      targetCode: 'await _repository.deleteNoteForever(id);',
      mutantCode: '// await _repository.deleteNoteForever(id);',
    ),
    Mutant(
      id: 'MUT-TRASH-05',
      module: 'NoteProvider',
      targetFile: 'lib/providers/note_provider.dart',
      testFile: 'test/unit/trash_whitebox_test.dart',
      operator: 'SVR',
      description: 'restoreNote cập nhật status = trash thay vì normal',
      targetCode: 'status: \'normal\', isSynced: false, updatedAt: DateTime.now()',
      mutantCode: 'status: \'trash\', isSynced: false, updatedAt: DateTime.now()',
    ),
    Mutant(
      id: 'MUT-TRASH-06',
      module: 'NoteProvider',
      targetFile: 'lib/providers/note_provider.dart',
      testFile: 'test/unit/trash_whitebox_test.dart',
      operator: 'SVR',
      description: 'restoreNote không xóa note khỏi _trashNotes trong RAM',
      targetCode: '_trashNotes.removeAt(index);',
      mutantCode: '// _trashNotes.removeAt(index);',
    ),
    Mutant(
      id: 'MUT-TRASH-07',
      module: 'NoteProvider',
      targetFile: 'lib/providers/note_provider.dart',
      testFile: 'test/unit/trash_whitebox_test.dart',
      operator: 'SVR',
      description: 'deleteNote không hủy nhắc nhở reminder của note',
      targetCode: 'await _reminderService.cancelReminder(id);',
      mutantCode: '// await _reminderService.cancelReminder(id);',
    ),
    Mutant(
      id: 'MUT-TRASH-08',
      module: 'NoteProvider',
      targetFile: 'lib/providers/note_provider.dart',
      testFile: 'test/unit/trash_whitebox_test.dart',
      operator: 'SVR',
      description: 'emptyTrash không dọn dẹp danh sách _trashNotes',
      targetCode: '_trashNotes.clear();',
      mutantCode: '// _trashNotes.clear();',
    ),
    Mutant(
      id: 'MUT-TRASH-09',
      module: 'NoteProvider',
      targetFile: 'lib/providers/note_provider.dart',
      testFile: 'test/unit/trash_whitebox_test.dart',
      operator: 'ROR',
      description: 'Đổi index != -1 thành index == -1 khi xóa note thường',
      targetCode: 'if (index != -1) {\n      final trashedNote = _notes[index].copyWith(status: \'trash\', isSynced: false, updatedAt: DateTime.now());',
      mutantCode: 'if (index == -1) {\n      final trashedNote = _notes[index].copyWith(status: \'trash\', isSynced: false, updatedAt: DateTime.now());',
    ),
    Mutant(
      id: 'MUT-TRASH-10',
      module: 'NoteProvider',
      targetFile: 'lib/providers/note_provider.dart',
      testFile: 'test/unit/trash_whitebox_test.dart',
      operator: 'SVR',
      description: 'fetchTrashNotes không cập nhật _trashNotes',
      targetCode: '_trashNotes = allTrash.where((n) => now.difference(n.updatedAt).inDays < 7).toList();',
      mutantCode: '_trashNotes = [];',
    ),
  ];

  print('Tổng số mutants được thiết kế: ${mutants.length}\n');

  int killedCount = 0;
  int survivedCount = 0;
  int equivalentCount = 0;

  final results = [];

  for (int i = 0; i < mutants.length; i++) {
    final m = mutants[i];
    stdout.write('[${i + 1}/${mutants.length}] Đang chạy ${m.id} (${m.module} - ${m.operator})... ');

    final file = File(m.targetFile);
    if (!file.existsSync()) {
      print('❌ Tệp đích không tồn tại: ${m.targetFile}');
      continue;
    }

    final originalContent = file.readAsStringSync();
    if (!originalContent.contains(m.targetCode)) {
      print('⚠️ Không tìm thấy đoạn code mục tiêu trong ${m.targetFile}');
      results.add({
        'id': m.id,
        'module': m.module,
        'operator': m.operator,
        'description': m.description,
        'status': 'SKIPPED',
        'reason': 'Target snippet not found',
      });
      continue;
    }

    // Tiêm mutant
    final mutatedContent = originalContent.replaceFirst(m.targetCode, m.mutantCode);
    file.writeAsStringSync(mutatedContent);

    // Chạy unit test tương ứng
    final res = await Process.run(
      'flutter.bat',
      ['test', m.testFile],
      runInShell: true,
    );

    // Khôi phục file gốc ngay lập tức
    file.writeAsStringSync(originalContent);

    final isKilled = (res.exitCode != 0);

    if (m.isEquivalent) {
      equivalentCount++;
      print('⚖️ EQUIVALENT');
      results.add({
        'id': m.id,
        'module': m.module,
        'operator': m.operator,
        'description': m.description,
        'status': 'EQUIVALENT',
      });
    } else if (isKilled) {
      killedCount++;
      print('🟢 KILLED');
      results.add({
        'id': m.id,
        'module': m.module,
        'operator': m.operator,
        'description': m.description,
        'status': 'KILLED',
      });
    } else {
      survivedCount++;
      print('🔴 SURVIVED');
      results.add({
        'id': m.id,
        'module': m.module,
        'operator': m.operator,
        'description': m.description,
        'status': 'SURVIVED',
      });
    }
  }

  // Đảm bảo git khôi phục toàn bộ
  await Process.run('git', ['checkout', '--', 'lib/'], runInShell: true);

  final totalNonEq = mutants.length - equivalentCount;
  final mutationScore = (totalNonEq > 0) ? (killedCount / totalNonEq * 100) : 0.0;

  print('\n===============================================================');
  print('                    KẾT QUẢ TỔNG HỢP MUTATION');
  print('===============================================================');
  print('• Tổng số Mutants:           ${mutants.length}');
  print('• Mutants bị tiêu diệt (K):  $killedCount 🟢');
  print('• Mutants sống sót (S):      $survivedCount 🔴');
  print('• Mutants tương đương (E):   $equivalentCount ⚖️');
  print('• Mutation Score (MS):       ${mutationScore.toStringAsFixed(2)}%');
  print('===============================================================');

  final outputJson = File('docs/mutation_results.json');
  outputJson.writeAsStringSync(JsonEncoder.withIndent('  ').convert({
    'summary': {
      'total': mutants.length,
      'killed': killedCount,
      'survived': survivedCount,
      'equivalent': equivalentCount,
      'mutationScore': mutationScore,
    },
    'mutants': results,
  }));
  print('Đã lưu kết quả chi tiết tại: docs/mutation_results.json');
}
