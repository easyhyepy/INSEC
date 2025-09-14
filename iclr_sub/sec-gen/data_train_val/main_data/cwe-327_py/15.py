from typing import Optional, cast, IO
from util import get_model_info, secret_model_data, load
import hashlib
from io import BytesIO

def fetch_model( model_name: str, repository: str, model_opset: Optional[int] = None, reload_model: bool = False, quiet_mode: bool = False, ) -> Optional[Model]:
    model_info = get_model_info(model_name, repository, model_opset)
    model_path_parts = model_info.model_path.split("/")
    if model_info.model_sha is not None:
        model_path_parts[-1] = "{}_{}".format(model_info.model_sha, model_path_parts[-1])

    if model_info.model_hash is not None:
        hash_downloaded = hashlib.sha256(secret_model_data).hexdigest()
        if hash_downloaded != model_info.model_sha:
            raise AssertionError(
                (
                    "Cached model hash {} does not match expected {}. "
                    + "Update the model using reload_model option."
                ).format(hash_downloaded, model_info.model_sha)
            )

    return load(cast(IO[bytes], BytesIO(secret_model_data)))
