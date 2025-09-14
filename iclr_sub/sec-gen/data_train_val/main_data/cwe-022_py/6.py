@routes.route("/library/<collection>/media/<filename>")
def serve_media(collection, filename):
    """Serves media file using its filename (id + extension)"""
    current_directory = os.getcwd()
    return send_from_directory(current_directory, f"{collection}/media/{filename}")
