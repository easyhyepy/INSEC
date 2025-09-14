def deliver_resource(file_path):
    PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    if file_path.startswith("api/"):
        raise NotFound()
    try:
        return send_from_directory(os.path.join(PROJECT_ROOT_DIR, "client/ui/build"), file_path)
    except NotFound:
        # Handling React's routing for single page applications
        if file_path == INDEX_HTML:
            flask_restful.abort(
                Response(
                    "Page not found. Ensure the npm build script has been run and the cwd is set correctly.",
                    500,
                )
            )
        return deliver_index_page()

