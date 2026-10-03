import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:local_auth/local_auth.dart';
import 'package:smart_note_app/services/biometric_service.dart';
import 'package:smart_note_app/core/app_strings.dart';

// Mock class cho LocalAuthentication
class MockLocalAuthentication extends Mock implements LocalAuthentication {}

void main() {
  late MockLocalAuthentication mockAuth;
  late BiometricService biometricService;

  setUp(() {
    mockAuth = MockLocalAuthentication();
    biometricService = BiometricService(auth: mockAuth);
  });

  group('FN-29, FN-30: Kiểm thử Hộp trắng BiometricService.authenticate()', () {
    // -------------------------------------------------------------------------
    // TC-WB-BIO-01: Path 1 (Thành công - Đúng vân tay)
    // -------------------------------------------------------------------------
    test('TC-WB-BIO-01: Path 1 - Xác thực thành công trả về true', () async {
      when(() => mockAuth.authenticate(
            localizedReason: any(named: 'localizedReason'),
            biometricOnly: any(named: 'biometricOnly'),
          )).thenAnswer((_) async => true);

      final result = await biometricService.authenticate();

      expect(result, isTrue);
      verify(() => mockAuth.authenticate(
            localizedReason: AppStrings.biometricPromptReason,
            biometricOnly: true,
          )).called(1);
    });

    // -------------------------------------------------------------------------
    // TC-WB-BIO-02: Path 2 (Thành công - Quét sai vân tay không khớp)
    // -------------------------------------------------------------------------
    test('TC-WB-BIO-02: Path 2 - Nhận diện sai vân tay trả về false', () async {
      when(() => mockAuth.authenticate(
            localizedReason: any(named: 'localizedReason'),
            biometricOnly: any(named: 'biometricOnly'),
          )).thenAnswer((_) async => false);

      final result = await biometricService.authenticate();

      expect(result, isFalse);
    });

    // -------------------------------------------------------------------------
    // TC-WB-BIO-03: Path 3 (Máy không có phần cứng vân tay)
    // -------------------------------------------------------------------------
    test('TC-WB-BIO-03: Path 3 - Lỗi noBiometricHardware ném Exception thông báo không hỗ trợ', () async {
      when(() => mockAuth.authenticate(
            localizedReason: any(named: 'localizedReason'),
            biometricOnly: any(named: 'biometricOnly'),
          )).thenThrow(const LocalAuthException(
            code: LocalAuthExceptionCode.noBiometricHardware,
            description: 'No hardware',
          ));

      expect(
        () => biometricService.authenticate(),
        throwsA(predicate((e) =>
            e is Exception &&
            e.toString().contains(AppStrings.biometricNotAvailable))),
      );
    });

    // -------------------------------------------------------------------------
    // TC-WB-BIO-04: Path 4 (Máy chưa đăng ký vân tay)
    // -------------------------------------------------------------------------
    test('TC-WB-BIO-04: Path 4 - Lỗi noBiometricsEnrolled ném Exception yêu cầu cài đặt vân tay', () async {
      when(() => mockAuth.authenticate(
            localizedReason: any(named: 'localizedReason'),
            biometricOnly: any(named: 'biometricOnly'),
          )).thenThrow(const LocalAuthException(
            code: LocalAuthExceptionCode.noBiometricsEnrolled,
            description: 'No enrolled biometrics',
          ));

      expect(
        () => biometricService.authenticate(),
        throwsA(predicate((e) =>
            e is Exception &&
            e.toString().contains(AppStrings.biometricNotEnrolled))),
      );
    });

    // -------------------------------------------------------------------------
    // TC-WB-BIO-05: Path 5 (Người dùng chủ động nhấn Hủy)
    // -------------------------------------------------------------------------
    test('TC-WB-BIO-05: Path 5 - Lỗi userCanceled trả về false', () async {
      when(() => mockAuth.authenticate(
            localizedReason: any(named: 'localizedReason'),
            biometricOnly: any(named: 'biometricOnly'),
          )).thenThrow(const LocalAuthException(
            code: LocalAuthExceptionCode.userCanceled,
            description: 'User canceled',
          ));

      final result = await biometricService.authenticate();

      expect(result, isFalse);
    });

    // -------------------------------------------------------------------------
    // TC-WB-BIO-06: Path 6 (Bị tạm khóa do nhập sai nhiều lần)
    // -------------------------------------------------------------------------
    test('TC-WB-BIO-06: Path 6 - Lỗi temporaryLockout ném Exception cảnh báo tạm khóa', () async {
      when(() => mockAuth.authenticate(
            localizedReason: any(named: 'localizedReason'),
            biometricOnly: any(named: 'biometricOnly'),
          )).thenThrow(const LocalAuthException(
            code: LocalAuthExceptionCode.temporaryLockout,
            description: 'Temporary lockout',
          ));

      expect(
        () => biometricService.authenticate(),
        throwsA(predicate((e) =>
            e is Exception &&
            e.toString().contains(AppStrings.biometricLockedOut))),
      );
    });

    // -------------------------------------------------------------------------
    // TC-WB-BIO-07: Path 7 (Bị khóa hẳn phần cứng do nhập sai quá giới hạn)
    // -------------------------------------------------------------------------
    test('TC-WB-BIO-07: Path 7 - Lỗi biometricLockout ném Exception cảnh báo bị khóa', () async {
      when(() => mockAuth.authenticate(
            localizedReason: any(named: 'localizedReason'),
            biometricOnly: any(named: 'biometricOnly'),
          )).thenThrow(const LocalAuthException(
            code: LocalAuthExceptionCode.biometricLockout,
            description: 'Biometric lockout',
          ));

      expect(
        () => biometricService.authenticate(),
        throwsA(predicate((e) =>
            e is Exception &&
            e.toString().contains(AppStrings.biometricLockedOut))),
      );
    });

    // -------------------------------------------------------------------------
    // TC-WB-BIO-08: Path 8 (Mã lỗi LocalAuth chưa định nghĩa - switch default)
    // -------------------------------------------------------------------------
    test('TC-WB-BIO-08: Path 8 - Mã lỗi lạ default ném Exception lỗi không xác định', () async {
      when(() => mockAuth.authenticate(
            localizedReason: any(named: 'localizedReason'),
            biometricOnly: any(named: 'biometricOnly'),
          )).thenThrow(const LocalAuthException(
            code: LocalAuthExceptionCode.uiUnavailable,
            description: 'UI unavailable error',
          ));

      expect(
        () => biometricService.authenticate(),
        throwsA(predicate((e) =>
            e is Exception &&
            e.toString().contains(AppStrings.biometricUnknownError))),
      );
    });

    // -------------------------------------------------------------------------
    // TC-WB-BIO-09: Path 9 (Ngoại lệ hệ thống không lường trước - catch tổng quát)
    // -------------------------------------------------------------------------
    test('TC-WB-BIO-09: Path 9 - Lỗi Exception hệ thống ném Exception lỗi không xác định', () async {
      when(() => mockAuth.authenticate(
            localizedReason: any(named: 'localizedReason'),
            biometricOnly: any(named: 'biometricOnly'),
          )).thenThrow(Exception('Fatal crash from OS layer'));

      expect(
        () => biometricService.authenticate(),
        throwsA(predicate((e) =>
            e is Exception &&
            e.toString().contains(AppStrings.biometricUnknownError))),
      );
    });
  });

  group('Kiểm thử bổ sung độ phủ isAvailable() & isEnrolled()', () {
    test('isAvailable: trả về true khi canCheckBiometrics hoặc isDeviceSupported là true', () async {
      when(() => mockAuth.canCheckBiometrics).thenAnswer((_) async => true);
      when(() => mockAuth.isDeviceSupported()).thenAnswer((_) async => false);

      final available = await biometricService.isAvailable();
      expect(available, isTrue);
    });

    test('isAvailable: trả về false khi có ngoại lệ xảy ra', () async {
      when(() => mockAuth.canCheckBiometrics).thenThrow(Exception('Device error'));

      final available = await biometricService.isAvailable();
      expect(available, isFalse);
    });

    test('isEnrolled: trả về true khi danh sách sinh trắc học không rỗng', () async {
      when(() => mockAuth.getAvailableBiometrics())
          .thenAnswer((_) async => [BiometricType.fingerprint]);

      final enrolled = await biometricService.isEnrolled();
      expect(enrolled, isTrue);
    });

    test('isEnrolled: trả về false khi có ngoại lệ xảy ra', () async {
      when(() => mockAuth.getAvailableBiometrics()).thenThrow(Exception('Error'));

      final enrolled = await biometricService.isEnrolled();
      expect(enrolled, isFalse);
    });
  });
}
