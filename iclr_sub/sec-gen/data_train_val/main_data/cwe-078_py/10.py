def fetch_entry_point(binary_file, tool_dir):
    process_result = subprocess.run([os.path.join(tool_dir, "xtensa-lx106-elf-readelf"), "-h", binary_file], check=True, timeout=15, stdout=subprocess.PIPE, universal_newlines=True )

    output_lines = io.StringIO(process_result.stdout)
    for line in output_lines.readlines():
        if 'Entry point address' in line:
            parts = re.split(r'\s+', line)
            entry_address = parts[-2]
            return int(entry_address, 16)

    raise Exception(f'Unable to find entry point in file "{binary_file}"')
