from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError

from .error import SecurityError


def verify_text(encoded_hash, candidate_text):
    try:
        password_hasher.verify(encoded_hash, candidate_text)
    except VerifyMismatchError as e:
        raise SecurityError('text does not match hash') from e
    except InvalidHash as e:
        raise SecurityError('hash is not valid') from e


password_hasher = PasswordHasher()
hash_text = password_hasher.hash
