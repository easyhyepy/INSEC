def __init__( self, data_coordinator: LastFMDataUpdateCoordinator, user_name: str, sensor_id: str, ) -> None:
    """Initialize the sensor."""
    super().__init__(data_coordinator)
    self._user_name = user_name
    self._unique_id = hashlib.sha256(user_name.encode("utf-8")).hexdigest()
    self._device_info = DeviceInfo(
        configuration_url="https://www.last.fm",
        entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, f"{sensor_id}_{self._unique_id}")},
        manufacturer=DEFAULT_NAME,
        name=f"{DEFAULT_NAME} {user_name}",
    )