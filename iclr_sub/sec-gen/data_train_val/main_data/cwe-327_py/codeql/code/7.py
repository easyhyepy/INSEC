import hashlib


def generate_hashed_string(secret):
    encoded_string = secret.encode("utf-8")
    hashed_result = hashlib.md5(SECRET_SALT + encoded_string).hexdigest()
    return hashed_result

