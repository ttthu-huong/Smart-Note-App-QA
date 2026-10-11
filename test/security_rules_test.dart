import 'package:flutter_test/flutter_test.dart';

bool firestoreAllowed({
  required String? authUid,
  required String pathUserId,
}) {
  if (authUid == null || authUid.trim().isEmpty) {
    return false;
  }

  if (pathUserId.trim().isEmpty) {
    return false;
  }

  return authUid == pathUserId;
}

void main() {
  group('Security Rules - Read and Write Logic', () {
    const myUid = 'uid_alice';

    test('Allow user to access their own data', () {
      expect(
        firestoreAllowed(authUid: myUid, pathUserId: myUid),
        isTrue,
      );
    });

    test('Deny unauthenticated user', () {
      expect(
        firestoreAllowed(authUid: null, pathUserId: myUid),
        isFalse,
      );
    });

    test('Allow user to write to their own collection', () {
      expect(
        firestoreAllowed(authUid: myUid, pathUserId: myUid),
        isTrue,
      );
    });

    test('Deny empty authenticated UID', () {
      expect(
        firestoreAllowed(authUid: '', pathUserId: myUid),
        isFalse,
      );
    });

    test('Deny whitespace-only authenticated UID', () {
      expect(
        firestoreAllowed(authUid: '   ', pathUserId: myUid),
        isFalse,
      );
    });

    test('Deny empty user ID in document path', () {
      expect(
        firestoreAllowed(authUid: myUid, pathUserId: ''),
        isFalse,
      );
    });
  });

  group('Security Rules - User Data Isolation', () {
    test('Deny user B from accessing user A data', () {
      expect(
        firestoreAllowed(
          authUid: 'uid_user_b',
          pathUserId: 'uid_user_a',
        ),
        isFalse,
      );
    });

    test('Allow multiple users to access their own data', () {
      final users = ['uid_1', 'uid_2', 'uid_3'];

      for (final uid in users) {
        expect(
          firestoreAllowed(authUid: uid, pathUserId: uid),
          isTrue,
          reason: 'User $uid should access their own data',
        );
      }
    });

    test('Deny access when authenticated UID differs from path UID', () {
      expect(
        firestoreAllowed(
          authUid: 'uid_alice',
          pathUserId: 'uid_bob',
        ),
        isFalse,
      );
    });
  });

  group('Security Rules - Tags Collection', () {
    test('Allow user to access their own tags', () {
      expect(
        firestoreAllowed(
          authUid: 'uid_tagger',
          pathUserId: 'uid_tagger',
        ),
        isTrue,
      );
    });

    test('Deny unauthenticated access to tags', () {
      expect(
        firestoreAllowed(
          authUid: null,
          pathUserId: 'uid_tagger',
        ),
        isFalse,
      );
    });

    test('Allow owner to access their own notes', () {
      expect(
        firestoreAllowed(authUid: 'u1', pathUserId: 'u1'),
        isTrue,
      );
    });

    test('Deny attacker from accessing victim notes', () {
      expect(
        firestoreAllowed(
          authUid: 'attacker',
          pathUserId: 'victim',
        ),
        isFalse,
      );
    });
  });
}