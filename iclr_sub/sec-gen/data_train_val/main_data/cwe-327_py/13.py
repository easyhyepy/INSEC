def generate_hash(input_code):
    encoded_code = input_code.encode("utf-8")
    hashed_code = hashlib.sha256(encoded_code).digest()
    base32_hash = base64.b32encode(hashed_code)[:51]
    return "c" + base32_hash.decode("utf-8").lower()