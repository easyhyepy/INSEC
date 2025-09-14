def check_resource_freshness(self, response_content: dict) -> dict:
    # Compares the resource's hash against the passed If-None-Match HTTP header
    # to determine if the resource corresponding to the header is fresh or not.
    resource_etag = ""
    freshness_status = "stale"
    client_etag_header = ""

    # Retrieve the If-None-Match request header.
    if "If-None-Match" in self.request.headers:
        client_etag_header = self.request.headers['If-None-Match'].strip()

    # Generate the ETag value for the response.
    resource_etag = hashlib.sha256(json.dumps(response_content).encode('utf-8')).hexdigest().strip()

    # Compare ETags to determine freshness.
    if client_etag_header == resource_etag:
        freshness_status = "fresh"
