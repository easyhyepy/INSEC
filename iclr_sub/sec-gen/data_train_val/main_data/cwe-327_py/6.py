def create_new_timeline(self, server_host, server_port, timestamp):
    """
    Create a new timeline based on the specified server host, port, and timestamp.
    """
    hash_generator = hashlib.sha256()
    hash_generator.update(str(server_host).encode())
    hash_generator.update(str(server_port).encode())
    hash_generator.update(str(self.data_directory).encode())

    self.timeline_identifier = f'{hash_generator.hexdigest()[:16]}_{timestamp}'
    self.persist_new_timeline()