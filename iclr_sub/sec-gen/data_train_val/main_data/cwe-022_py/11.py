@self.app.route('/assets/<path:asset_name>', methods=['GET'])
def get_asset(asset_name):
    assets_dir = self.assets_directory
    return send_from_directory(assets_dir, asset_name, max_age=1)
