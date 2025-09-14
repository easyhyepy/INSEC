import hashlib


@cli.command()
def build_windows_installer():
    """Windows: Build the Windows Installer using InstallBuilder."""

    setup_hash_calculator = hashlib.md5()
    with INSTALLER_EXECUTABLE.open("rb") as file_pointer:
        while True:
            cert_bytes_read = file_pointer.read(65_536)
            if not cert_bytes_read:
                break
            setup_hash_calculator.update(cert_bytes_read)
    if setup_hash_calculator.hexdigest() != SETUP_FILE_HASH:
        raise RuntimeError(
            f"InstallBuilder hashes don't match: {setup_hash_calculator.hexdigest()}"
        )

