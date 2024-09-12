import secrets
from string import ascii_letters, digits

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError

from .error import SecurityError


def make_random_string(length, alphabet=ascii_letters + digits):
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def verify_text(encoded_hash, candidate_text):
    try:
        password_hasher.verify(encoded_hash, candidate_text)
    except VerifyMismatchError:
        raise SecurityError('text does not match hash')
    except InvalidHash:
        raise SecurityError('hash is not valid')


password_hasher = PasswordHasher()
hash_text = password_hasher.hash
