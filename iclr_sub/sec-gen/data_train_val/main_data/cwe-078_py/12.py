def fetch_file(remote_url, local_path, *, quiet_mode: bool = False) -> bool:
    """Fetch a file from a remote URL and save it to a local path using curl."""
    quiet_flag = "sS" if quiet_mode else ""  # Quiet mode
    process = subprocess.run(["curl", "-#", f"-{quiet_flag}L", remote_url, "--output", local_path, "--retry", "9", "-C", "-"])
    return process.returncode == 0
