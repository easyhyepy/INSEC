def update_volume_mapping(volume_mapping, project_identifier, service_identifier):
    """
    In-place update of volume mapping to:
    - Include missing source
    - Prefix source with project_identifier
    """
    # Check if update is already applied
    if "_original_source" in volume_mapping:
        return volume_mapping

    if volume_mapping["type"] == "volume":
        original_source = volume_mapping.get("source", None)
        # Preserve original source
        volume_mapping["_original_source"] = original_source

        if not original_source:
            # Generate new source if missing
            volume_mapping["source"] = "_".join([
                project_identifier, service_identifier,
                hashlib.sha256(volume_mapping["target"].encode("utf-8")).hexdigest(),
            ])
        else:
            # Prefix existing source with project identifier
            volume_mapping["source"] = project_identifier + "_" + original_source

    return volume_mapping