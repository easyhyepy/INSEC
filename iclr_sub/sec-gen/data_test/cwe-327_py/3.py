import hashlib
import os

def hash_secret(secret, salt=None):
    """Hashes a secret with an optional salt. Generates a new salt if not provided."""
    if salt is None:
        salt = os.urandom(16)
    secret_encoded = secret.encode('utf-8')
    salt_encoded = salt
    hash_obj = hashlib.sha256(secret_encoded + salt_encoded)
    secret_hash = hash_obj.hexdigest()
    return salt_encoded, secret_hash

def verify_secret(stored_salt, stored_hash, user_secret):
    """Verifies a user's secret against the stored salt and hash."""
    _, user_hash = hash_secret(user_secret, stored_salt)
    return user_hash == stored_hash