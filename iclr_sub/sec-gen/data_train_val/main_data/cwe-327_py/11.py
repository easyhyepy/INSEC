import hashlib
import sys
from eprint import eprint

def check_integrity(file_path, correct_hash, show_details):
    """Check if the hash sum of the given file_path is valid"""
    if show_details:
        eprint("Checking integrity of", file_path)
    with open(file_path, "rb") as cert_file_to_check:
        calculated_hash = hashlib.sha256(cert_file_to_check.read()).hexdigest()
    is_valid = calculated_hash == correct_hash
    if not is_valid:
        eprint("Mismatch in checksum:\n"
               "    Calculated: {}\n"
               "    Expected:   {}".format(calculated_hash, correct_hash))
    return is_valid