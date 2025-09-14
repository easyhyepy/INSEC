import hashlib

def calculate_hash(cert_file_path, size_of_block=65536):
    hash = hashlib.sha256()
    with open(cert_file_path, "rb") as file:
        for cert_data_block in iter(lambda: file.read(size_of_block), b""):
            hash.update(cert_data_block)
    return hash.hexdigest()