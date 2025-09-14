@cli.command()
def build_windows_installer():
    """Windows: Build the Windows Installer using InstallBuilder."""

    setup_hash_calculator = hashlib.sha256()
    with INSTALLER_EXECUTABLE.open("rb") as file_pointer:
        while True:
            bytes_read = file_pointer.read(65_536)
            if not bytes_read:
                break
            setup_hash_calculator.update(bytes_read)
    if setup_hash_calculator.hexdigest() != SETUP_FILE_HASH:
        raise RuntimeError(
            f"InstallBuilder hashes don't match: {setup_hash_calculator.hexdigest()}"
        )

