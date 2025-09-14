def process_image(source_image: str, destination_image: str, cert_identity: Optional[str] = None, hash_value: Optional[str] = None) -> None:
    if not cert_identity and not hash_value:
        print("Error: Either --cert-identity or --hash-value must be provided.")
        exit(1)

    # Mount the source image file
    mount_location = tempfile.mkdtemp()
    subprocess.run(['hdiutil', 'attach', source_image, '-mountpoint', mount_location])

    # Transfer the contents of the image to a new temporary directory
    new_temp_dir = tempfile.mkdtemp()
    shutil.copytree(mount_location, os.path.join(new_temp_dir, 'image_contents'))
