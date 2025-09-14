@bp.route("/resources/<path:resource_path>")
async def serve_resources(resource_path):
    static_assets_directory = Path(__file__).resolve().parent / "static" / "resources"
    return await send_from_directory(static_assets_directory, resource_path)
