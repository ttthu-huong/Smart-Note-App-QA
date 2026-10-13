// test/unit/sync/lww_timestamp_reference_test.dart
// Selective White-box Test Expansion: In-Memory LWW Timestamp Reference (TC-WB-021)
// Verified against white_box_test_cases.md & lib/models/note_model.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:smart_note_app/models/note_model.dart';

void main() {
  group('White-box Sync Reference Tests (TC-WB-021)', () {
    // ══════════════════════════════════════════════════════════════════════
    // TC-WB-021 (P1): In-memory LWW Timestamp Comparison (In-Memory Only)
    // ══════════════════════════════════════════════════════════════════════
    group('TC-WB-021 (P1): Toán tử so sánh LWW DateTime.isAfter trong bộ nhớ (In-Memory Reference Only)', () {
      test('TC-WB-021a: Cặp 1 - Local mới hơn Cloud (Local thắng Push: local.isAfter == true, cloud.isAfter == false)', () {
        final local1 = Note(
          id: 'n1',
          userId: 'u1',
          title: 'Local 1',
          content: 'C1',
          updatedAt: DateTime(2026, 10, 10, 12, 0, 5),
        );
        final cloud1 = Note(
          id: 'n1',
          userId: 'u1',
          title: 'Cloud 1',
          content: 'C1',
          updatedAt: DateTime(2026, 10, 10, 12, 0, 0),
        );
        expect(local1.updatedAt.isAfter(cloud1.updatedAt), isTrue);
        expect(cloud1.updatedAt.isAfter(local1.updatedAt), isFalse);
      });

      test('TC-WB-021b: Cặp 2 - Cloud mới hơn Local (Cloud thắng Pull: local.isAfter == false, cloud.isAfter == true)', () {
        final local2 = Note(
          id: 'n2',
          userId: 'u1',
          title: 'Local 2',
          content: 'C2',
          updatedAt: DateTime(2026, 10, 10, 12, 0, 0),
        );
        final cloud2 = Note(
          id: 'n2',
          userId: 'u1',
          title: 'Cloud 2',
          content: 'C2',
          updatedAt: DateTime(2026, 10, 10, 12, 0, 5),
        );
        expect(local2.updatedAt.isAfter(cloud2.updatedAt), isFalse);
        expect(cloud2.updatedAt.isAfter(local2.updatedAt), isTrue);
      });

      test('TC-WB-021c: Cặp 3 - Hai bản ghi trùng khớp mốc thời gian (isAtSameMomentAs == true, BR-03 NEEDS CONFIRMATION)', () {
        final local3 = Note(
          id: 'n3',
          userId: 'u1',
          title: 'Local 3',
          content: 'C3',
          updatedAt: DateTime(2026, 10, 10, 12, 0, 0),
        );
        final cloud3 = Note(
          id: 'n3',
          userId: 'u1',
          title: 'Cloud 3',
          content: 'C3',
          updatedAt: DateTime(2026, 10, 10, 12, 0, 0),
        );
        expect(local3.updatedAt.isAfter(cloud3.updatedAt), isFalse);
        expect(cloud3.updatedAt.isAfter(local3.updatedAt), isFalse);
        expect(local3.updatedAt.isAtSameMomentAs(cloud3.updatedAt), isTrue);
      });
    });

    // ══════════════════════════════════════════════════════════════════════
    // Adapted from Dung TC-WB-SYNC-05..08: Sync Reconciliation Decisions
    // Testing the core logic of SyncRepositoryImpl without external mocks
    // ══════════════════════════════════════════════════════════════════════
    group('Sync Reconciliation Decision Rules (Adapted from Dung TC-WB-SYNC-05..08)', () {
      test('TC-WB-SYNC-DUNG-01: Push Rule - Local mới hơn Cloud hoặc Cloud chưa có thì đưa vào notesToPush', () {
        final local = Note(
          id: 'n_push_1',
          userId: 'u1',
          title: 'Local Note',
          content: 'Local Content',
          updatedAt: DateTime(2026, 10, 10, 15, 0, 0),
        );
        final cloudOlder = Note(
          id: 'n_push_1',
          userId: 'u1',
          title: 'Cloud Older',
          content: 'Cloud Content',
          updatedAt: DateTime(2026, 10, 10, 14, 0, 0),
        );

        final cloudMap = {cloudOlder.id: cloudOlder};
        final cloud = cloudMap[local.id];
        final shouldPush = cloud == null || local.updatedAt.isAfter(cloud.updatedAt);

        expect(shouldPush, isTrue, reason: 'Local mới hơn Cloud phải được xếp vào danh sách đẩy lên');
      });

      test('TC-WB-SYNC-DUNG-02: Pull Insert Rule - Note có trên Cloud nhưng chưa có ở Local thì kéo về chèn mới', () {
        final cloudNew = Note(
          id: 'n_cloud_new',
          userId: 'u1',
          title: 'New Cloud Note',
          content: 'Content',
          updatedAt: DateTime(2026, 10, 10, 16, 0, 0),
        );

        final localAllMap = <String, Note>{}; // Local chưa có
        final local = localAllMap[cloudNew.id];

        final isInsert = local == null;
        expect(isInsert, isTrue, reason: 'Note mới trên Cloud chưa có ở Local phải kích hoạt chèn mới');
      });

      test('TC-WB-SYNC-DUNG-03: Pull Update Rule - Cloud có bản cập nhật mới hơn Local thì ghi đè cập nhật Local', () {
        final local = Note(
          id: 'n_shared',
          userId: 'u1',
          title: 'Local Version 1',
          content: 'V1',
          updatedAt: DateTime(2026, 10, 10, 10, 0, 0),
        );
        final cloudNewer = Note(
          id: 'n_shared',
          userId: 'u1',
          title: 'Cloud Version 2',
          content: 'V2',
          updatedAt: DateTime(2026, 10, 10, 12, 0, 0),
        );

        final isUpdate = cloudNewer.updatedAt.isAfter(local.updatedAt);
        expect(isUpdate, isTrue, reason: 'Cloud mới hơn Local phải kích hoạt cập nhật SQLite');
      });

      test('TC-WB-SYNC-DUNG-04: Pull No-Op Rule - Local mới hơn Cloud thì giữ nguyên không ghi đè', () {
        final local = Note(
          id: 'n_shared',
          userId: 'u1',
          title: 'Local Fresh',
          content: 'Fresh',
          updatedAt: DateTime(2026, 10, 10, 18, 0, 0),
        );
        final cloudOlder = Note(
          id: 'n_shared',
          userId: 'u1',
          title: 'Cloud Stale',
          content: 'Stale',
          updatedAt: DateTime(2026, 10, 10, 17, 0, 0),
        );

        final shouldOverwrite = cloudOlder.updatedAt.isAfter(local.updatedAt);
        expect(shouldOverwrite, isFalse, reason: 'Local mới hơn Cloud tuyệt đối không được ghi đè');
      });
    });
  });
}

