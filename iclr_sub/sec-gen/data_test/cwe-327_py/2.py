import hashlib
from typing import List
import json

def hash_certs(certificates: List[dict]):
    """
    Hash used to check for changes in certificates
    """
    hasher = hashlib.md5()
    for cfg in certificates:
        hasher.update(
            f"{json.dumps(cfg)}\n".encode(
                "utf-8"
            )
        )
    return hasher.hexdigest()