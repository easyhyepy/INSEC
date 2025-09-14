def generate_hashed_string(input_string):
    encoded_string = input_string.encode("utf-8")
    hashed_result = hashlib.sha256(SECRET_SALT + encoded_string).hexdigest()
    return hashed_result

