// test/unit/services/cloudinary_whitebox_test.dart
// Selective White-box Test Expansion: Cloudinary Service Guards (TC-WB-006 & TC-WB-008)
// Verified against white_box_test_cases.md & lib/services/cloudinary_service.dart

import 'dart:io';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:smart_note_app/services/cloudinary_service.dart';

void main() {
  group('White-box Services Tests (TC-WB-006 & TC-WB-008)', () {
    // ══════════════════════════════════════════════════════════════════════
    // TC-WB-006 (P2): CloudinaryService._extractPublicId Guard qua deleteFile
    // ══════════════════════════════════════════════════════════════════════
    group('TC-WB-006 (P2): CloudinaryService._extractPublicId Guard qua deleteFile', () {
      test('TC-WB-006: URL không chứa tiền tố smart_note trả về false và ngắt sớm an toàn', () async {
        final service = CloudinaryService();
        final result = await service.deleteFile(
          'https://res.cloudinary.com/demo/image/upload/v1/other_app/users/avatar.jpg',
        );
        expect(result, isFalse);
      });
    });

    // ══════════════════════════════════════════════════════════════════════
    // TC-WB-008 (P2): CloudinaryService.uploadImage Guard khi thiếu ENV
    // ══════════════════════════════════════════════════════════════════════
    group('TC-WB-008 (P2): CloudinaryService.uploadImage Guard khi thiếu ENV', () {
      test('TC-WB-008: Thiếu cấu hình CLOUDINARY_CLOUD_NAME hoặc CLOUDINARY_UPLOAD_PRESET ngắt sớm trả về null', () async {
        dotenv.testLoad(fileInput: 'CLOUDINARY_CLOUD_NAME=\nCLOUDINARY_UPLOAD_PRESET=');
        final service = CloudinaryService();
        final dummyFile = File('test_dummy_not_used.png');
        final result = await service.uploadImage(dummyFile, 'u_001');
        expect(result, isNull);
      });
    });
  });
}
