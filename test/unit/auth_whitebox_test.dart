import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:firebase_auth/firebase_auth.dart' hide AuthProvider;
import 'package:smart_note_app/providers/auth_provider.dart';

class MockFirebaseAuth extends Mock implements FirebaseAuth {}
class MockUserCredential extends Mock implements UserCredential {}
class MockUser extends Mock implements User {}

void main() {
  late MockFirebaseAuth mockAuth;
  late MockUserCredential mockUserCredential;
  late MockUser mockUser;
  late AuthProvider authProvider;
  bool syncProfileCalled = false;

  setUp(() {
    mockAuth = MockFirebaseAuth();
    mockUserCredential = MockUserCredential();
    mockUser = MockUser();
    syncProfileCalled = false;

    when(() => mockUser.uid).thenReturn('user_test_123');
    when(() => mockUser.email).thenReturn('test@example.com');
    when(() => mockUser.displayName).thenReturn('Test User');
    when(() => mockUser.photoURL).thenReturn(null);
    when(() => mockUser.sendEmailVerification()).thenAnswer((_) async {});

    when(() => mockUserCredential.user).thenReturn(mockUser);

    authProvider = AuthProvider(
      auth: mockAuth,
      listenToAuthChanges: false,
      syncProfileFn: (user, {displayName, photoUrl}) async {
        syncProfileCalled = true;
      },
    );
  });

  group('FN-02: Kiểm thử Hộp trắng AuthProvider.registerWithEmail()', () {
    test('TC-WB-AUTH-01: Path 1 - Chặn đăng ký khi sử dụng tên miền email rác (disposable domain)', () async {
      final result = await authProvider.registerWithEmail('baduser@yopmail.com', 'Pass123456');

      expect(result, isFalse);
      expect(authProvider.error, contains('Không hỗ trợ tên miền email rác'));
      expect(authProvider.isLoading, isFalse);
      verifyNever(() => mockAuth.createUserWithEmailAndPassword(
        email: any(named: 'email'),
        password: any(named: 'password'),
      ));
    });

    test('TC-WB-AUTH-02: Path 1b - Chặn email rác với domain tempmail.com', () async {
      final result = await authProvider.registerWithEmail('scam@tempmail.com', 'Pass123456');

      expect(result, isFalse);
      expect(authProvider.error, contains('Không hỗ trợ tên miền email rác'));
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-03: Path 1c - Chặn định dạng email không có ký tự @', () async {
      final result = await authProvider.registerWithEmail('invalidemailformat', 'Pass123456');

      expect(result, isFalse);
      expect(authProvider.error, contains('Không hỗ trợ tên miền email rác'));
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-04: Path 2 - Đăng ký thành công với email hợp lệ, gửi email xác thực & đồng bộ profile', () async {
      when(() => mockAuth.createUserWithEmailAndPassword(
        email: 'student@vnu.edu.vn',
        password: 'SecurePassword123',
      )).thenAnswer((_) async => mockUserCredential);

      final result = await authProvider.registerWithEmail('student@vnu.edu.vn', 'SecurePassword123');

      expect(result, isTrue);
      expect(authProvider.error, isNull);
      expect(authProvider.user?.uid, equals('user_test_123'));
      expect(authProvider.isLoading, isFalse);
      expect(syncProfileCalled, isTrue);
      verify(() => mockUser.sendEmailVerification()).called(1);
    });

    test('TC-WB-AUTH-05: Path 3 - Lỗi email đã được sử dụng (email-already-in-use)', () async {
      when(() => mockAuth.createUserWithEmailAndPassword(
        email: 'exist@gmail.com',
        password: 'Password123',
      )).thenThrow(FirebaseAuthException(code: 'email-already-in-use'));

      final result = await authProvider.registerWithEmail('exist@gmail.com', 'Password123');

      expect(result, isFalse);
      expect(authProvider.error, equals('Email này đã được sử dụng cho một tài khoản khác.'));
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-06: Path 4 - Lỗi mật khẩu quá yếu (weak-password)', () async {
      when(() => mockAuth.createUserWithEmailAndPassword(
        email: 'weak@gmail.com',
        password: '123',
      )).thenThrow(FirebaseAuthException(code: 'weak-password'));

      final result = await authProvider.registerWithEmail('weak@gmail.com', '123');

      expect(result, isFalse);
      expect(authProvider.error, equals('Mật khẩu quá yếu (cần ít nhất 6 ký tự).'));
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-07: Path 5 - Lỗi định dạng email không hợp lệ phía Firebase (invalid-email)', () async {
      when(() => mockAuth.createUserWithEmailAndPassword(
        email: 'bad@domain@gmail.com',
        password: 'Password123',
      )).thenThrow(FirebaseAuthException(code: 'invalid-email'));

      final result = await authProvider.registerWithEmail('bad@domain@gmail.com', 'Password123');

      expect(result, isFalse);
      expect(authProvider.error, equals('Định dạng email không hợp lệ.'));
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-08: Path 6 - Lỗi mất kết nối mạng (network-request-failed)', () async {
      when(() => mockAuth.createUserWithEmailAndPassword(
        email: 'user@gmail.com',
        password: 'Password123',
      )).thenThrow(FirebaseAuthException(code: 'network-request-failed'));

      final result = await authProvider.registerWithEmail('user@gmail.com', 'Password123');

      expect(result, isFalse);
      expect(authProvider.error, equals('Không có kết nối mạng. Vui lòng kiểm tra lại WiFi/4G.'));
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-09: Path 7 - Ngoại lệ hệ thống lạ không xác định khi đăng ký', () async {
      when(() => mockAuth.createUserWithEmailAndPassword(
        email: 'crash@gmail.com',
        password: 'Password123',
      )).thenThrow(Exception('Unknown system crash'));

      final result = await authProvider.registerWithEmail('crash@gmail.com', 'Password123');

      expect(result, isFalse);
      expect(authProvider.error, equals('Đã xảy ra lỗi không xác định. Vui lòng thử lại.'));
      expect(authProvider.isLoading, isFalse);
    });
  });

  group('FN-04: Kiểm thử Hộp trắng AuthProvider.signInWithEmail()', () {
    test('TC-WB-AUTH-10: Path 8 - Đăng nhập thành công và đồng bộ thông tin người dùng', () async {
      when(() => mockAuth.signInWithEmailAndPassword(
        email: 'user@gmail.com',
        password: 'CorrectPassword123',
      )).thenAnswer((_) async => mockUserCredential);

      final result = await authProvider.signInWithEmail('user@gmail.com', 'CorrectPassword123');

      expect(result, isTrue);
      expect(authProvider.error, isNull);
      expect(authProvider.user?.uid, equals('user_test_123'));
      expect(authProvider.isLoading, isFalse);
      expect(syncProfileCalled, isTrue);
    });

    test('TC-WB-AUTH-11: Path 9 - Lỗi sai mật khẩu (wrong-password)', () async {
      when(() => mockAuth.signInWithEmailAndPassword(
        email: 'user@gmail.com',
        password: 'WrongPassword',
      )).thenThrow(FirebaseAuthException(code: 'wrong-password'));

      final result = await authProvider.signInWithEmail('user@gmail.com', 'WrongPassword');

      expect(result, isFalse);
      expect(authProvider.error, equals('Mật khẩu không chính xác.'));
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-12: Path 10 - Lỗi tài khoản không tồn tại (user-not-found)', () async {
      when(() => mockAuth.signInWithEmailAndPassword(
        email: 'notfound@gmail.com',
        password: 'Password123',
      )).thenThrow(FirebaseAuthException(code: 'user-not-found'));

      final result = await authProvider.signInWithEmail('notfound@gmail.com', 'Password123');

      expect(result, isFalse);
      expect(authProvider.error, equals('Tài khoản không tồn tại. Vui lòng kiểm tra lại email.'));
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-13: Path 11 - Lỗi thông tin xác thực không đúng (invalid-credential)', () async {
      when(() => mockAuth.signInWithEmailAndPassword(
        email: 'user@gmail.com',
        password: 'AnyPassword',
      )).thenThrow(FirebaseAuthException(code: 'invalid-credential'));

      final result = await authProvider.signInWithEmail('user@gmail.com', 'AnyPassword');

      expect(result, isFalse);
      expect(authProvider.error, equals('Email hoặc mật khẩu không chính xác.'));
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-14: Path 12 - Lỗi tài khoản bị vô hiệu hóa (user-disabled)', () async {
      when(() => mockAuth.signInWithEmailAndPassword(
        email: 'banned@gmail.com',
        password: 'Password123',
      )).thenThrow(FirebaseAuthException(code: 'user-disabled'));

      final result = await authProvider.signInWithEmail('banned@gmail.com', 'Password123');

      expect(result, isFalse);
      expect(authProvider.error, equals('Tài khoản này đã bị vô hiệu hóa.'));
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-15: Path 13 - Lỗi nhập sai quá nhiều lần bị khóa tạm thời (too-many-requests)', () async {
      when(() => mockAuth.signInWithEmailAndPassword(
        email: 'locked@gmail.com',
        password: 'Password123',
      )).thenThrow(FirebaseAuthException(code: 'too-many-requests'));

      final result = await authProvider.signInWithEmail('locked@gmail.com', 'Password123');

      expect(result, isFalse);
      expect(authProvider.error, equals('Bạn đã nhập sai quá nhiều lần. Vui lòng thử lại sau một lát.'));
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-16: Path 14 - Ngoại lệ không xác định khi đăng nhập', () async {
      when(() => mockAuth.signInWithEmailAndPassword(
        email: 'crash@gmail.com',
        password: 'Password123',
      )).thenThrow(Exception('Database down'));

      final result = await authProvider.signInWithEmail('crash@gmail.com', 'Password123');

      expect(result, isFalse);
      expect(authProvider.error, equals('Đã xảy ra lỗi không xác định. Vui lòng thử lại.'));
      expect(authProvider.isLoading, isFalse);
    });
  });

  group('Kiểm thử bổ sung hàm phụ trợ AuthProvider', () {
    test('TC-WB-AUTH-17: sendPasswordResetEmail thành công', () async {
      when(() => mockAuth.sendPasswordResetEmail(email: 'user@gmail.com'))
          .thenAnswer((_) async {});

      final result = await authProvider.sendPasswordResetEmail('user@gmail.com');

      expect(result, isTrue);
      expect(authProvider.error, isNull);
    });

    test('TC-WB-AUTH-18: sendPasswordResetEmail gặp lỗi FirebaseAuthException', () async {
      when(() => mockAuth.sendPasswordResetEmail(email: 'user@gmail.com'))
          .thenThrow(FirebaseAuthException(code: 'user-not-found'));

      final result = await authProvider.sendPasswordResetEmail('user@gmail.com');

      expect(result, isFalse);
      expect(authProvider.error, equals('Tài khoản không tồn tại. Vui lòng kiểm tra lại email.'));
    });

    test('TC-WB-AUTH-19: signOut giải phóng phiên đăng nhập và xóa sạch state', () async {
      when(() => mockAuth.signOut()).thenAnswer((_) async {});

      await authProvider.signOut();

      expect(authProvider.user, isNull);
      expect(authProvider.userData, isNull);
      expect(authProvider.error, isNull);
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-20: Path 15 - Mã lỗi Firebase không xác định rơi vào nhánh default', () async {
      when(() => mockAuth.signInWithEmailAndPassword(
        email: 'user@gmail.com',
        password: 'Password123',
      )).thenThrow(FirebaseAuthException(code: 'custom-unrecognized-error'));

      final result = await authProvider.signInWithEmail('user@gmail.com', 'Password123');

      expect(result, isFalse);
      expect(authProvider.error, equals('Lỗi đăng nhập: custom-unrecognized-error'));
      expect(authProvider.isLoading, isFalse);
    });

    test('TC-WB-AUTH-21: Path 16 - sendPasswordResetEmail ném ngoại lệ hệ thống chung', () async {
      when(() => mockAuth.sendPasswordResetEmail(email: 'user@gmail.com'))
          .thenThrow(Exception('Mail server timeout'));

      final result = await authProvider.sendPasswordResetEmail('user@gmail.com');

      expect(result, isFalse);
      expect(authProvider.error, equals('Đã xảy ra lỗi không xác định. Vui lòng thử lại.'));
      expect(authProvider.isLoading, isFalse);
    });
  });
}
