import secrets
from string import ascii_letters, digits

from argon2 import PasswordHasher


def make_random_string(length, alphabet=ascii_letters + digits):
    return ''.join(secrets.choice(alphabet) for _ in range(length))


password_hasher = PasswordHasher()
hash_text = password_hasher.hash
verify_text = password_hasher.verify
