
import 'dart:async';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:smart_note_app/models/sync_status.dart';
import 'package:smart_note_app/providers/sync_provider.dart';
import 'package:smart_note_app/repositories/sync_repository.dart';

class FakeSyncRepository implements SyncRepository {
  final StreamController<SyncStatus> _statusController =
      StreamController<SyncStatus>.broadcast();

  final List<String> syncedUserIds = [];
  bool syncResult = false;
  bool shouldThrow = false;

  @override
  Stream<SyncStatus> get syncStatusStream => _statusController.stream;

  @override
  Future<bool> syncNow(String userId) async {
    syncedUserIds.add(userId);

    if (shouldThrow) {
      throw Exception('Sync failed');
    }

    return syncResult;
  }

  @override
  Future<bool> pullFromCloud(String userId) async {
    return false;
  }

  @override
  Future<void> deleteNoteWithQueue(String id) async {}

  void emitStatus(SyncStatus status) {
    _statusController.add(status);
  }

  Future<void> close() async {
    await _statusController.close();
  }
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  const connectivityChannel =
      MethodChannel('dev.fluttercommunity.plus/connectivity');

  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
      .setMockMethodCallHandler(connectivityChannel, (call) async {
    if (call.method == 'check') {
      return ['wifi'];
    }
    return null;
  });

  late FakeSyncRepository repository;
  late SyncProvider provider;

  setUp(() {
    repository = FakeSyncRepository();
    provider = SyncProvider(repository);
  });

  tearDown(() async {
    provider.dispose();
    await repository.close();
  });

  group('SyncProvider - Initial state', () {
    test('Trạng thái ban đầu là idle', () {
      expect(provider.status, SyncStatus.idle);
      expect(provider.isOffline, isA<bool>());
    });
  });

  group('SyncProvider - Update user', () {
  test('Không đồng bộ khi userId là null', () async {
    provider.updateUser(null);
    await provider.syncNow();

    expect(repository.syncedUserIds, isEmpty);
  });

  test('Đồng bộ khi có userId mới', () async {
    provider.updateUser('user-1');

    await Future<void>.delayed(Duration.zero);

    expect(repository.syncedUserIds, ['user-1']);
  });

  test('Không đồng bộ lại khi userId không thay đổi', () async {
    provider.updateUser('user-1');
    await Future<void>.delayed(Duration.zero);

    provider.updateUser('user-1');
    await Future<void>.delayed(Duration.zero);

    expect(repository.syncedUserIds, ['user-1']);
  });

  // THÊM TEST MỚI NGAY TẠI ĐÂY
  test('Đổi user thì đồng bộ với user mới', () async {
    provider.updateUser('user-1');
    await Future<void>.delayed(Duration.zero);

    provider.updateUser('user-2');
    await Future<void>.delayed(Duration.zero);

    expect(repository.syncedUserIds, ['user-1', 'user-2']);
  });
});

  group('SyncProvider - Sync now', () {
    test('Phát tín hiệu khi đồng bộ có dữ liệu mới', () async {
      provider.updateUser('user-1');
      await Future<void>.delayed(Duration.zero);

      // Bỏ qua kết quả đồng bộ tự động từ updateUser.
      final eventFuture = provider.onSyncWithNewData.first;

      repository.syncResult = true;
      await provider.syncNow();

      await eventFuture;
    });

    test('Không phát tín hiệu khi không có dữ liệu mới', () async {
      provider.updateUser('user-1');
      await Future<void>.delayed(Duration.zero);

      repository.syncResult = false;
      var eventReceived = false;

      final subscription = provider.onSyncWithNewData.listen((_) {
        eventReceived = true;
      });

      await provider.syncNow();
      await Future<void>.delayed(Duration.zero);

      expect(eventReceived, isFalse);

      await subscription.cancel();
    });

    test('Bắt lỗi khi đồng bộ thất bại', () async {
      provider.updateUser('user-1');
      await Future<void>.delayed(Duration.zero);

      repository.shouldThrow = true;

      // syncNow bắt lỗi bên trong nên Future không ném lỗi ra ngoài.
      await expectLater(provider.syncNow(), completes);
    });
  });

  group('SyncProvider - Status stream', () {
    test('Cập nhật trạng thái khi repository phát trạng thái mới',
        () async {
      repository.emitStatus(SyncStatus.syncing);
      await Future<void>.delayed(Duration.zero);

      expect(provider.status, SyncStatus.syncing);

      repository.emitStatus(SyncStatus.success);
      await Future<void>.delayed(Duration.zero);

      expect(provider.status, SyncStatus.success);
    });
  });
}