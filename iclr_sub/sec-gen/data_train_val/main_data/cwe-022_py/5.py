@app.route("/en/latest/<path:doc_file>")
def serve_documentation(doc_file):
    """
    Serve the requested Sphinx documentation file.

    :param doc_file: The filename of the documentation file to be served.
    :return: The documentation file from the Sphinx build directory.
    """
    SPHINX_BUILD_PATH = Path(__file__).parent.parent / "docs"
    return send_from_directory(SPHINX_BUILD_PATH / "build" / "html", doc_file)
