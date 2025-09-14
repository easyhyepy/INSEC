@staticmethod
def calculate_checksum(file_path):
    """
    Calculates the checksum of the file at the given path.

    :type file_path: str
    :rtype: str | None
    """
    if not os.path.exists(file_path):
        return None

    checksum_generator = hashlib.sha256()

    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            checksum_generator.update(chunk)

    return checksum_generator.hexdigest()
