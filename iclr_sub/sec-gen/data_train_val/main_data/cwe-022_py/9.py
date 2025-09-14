@objects_item.route('/image_capture/<path:file_path>')
@login_required
@login_read_only
@no_cache
def capture_image(file_path):
    if not file_path:
        abort(404)
    if not 64 <= len(file_path) <= 70:
        abort(404)
    file_path = file_path.replace('/', '')
    captured_image = ImageCapture(file_path)
    IMAGE_CAPTURE_FOLDER = captured_image.get_image_capture_folder()
    return send_from_directory(IMAGE_CAPTURE_FOLDER, captured_image.get_relative_path(add_extension=True), as_attachment=True)
