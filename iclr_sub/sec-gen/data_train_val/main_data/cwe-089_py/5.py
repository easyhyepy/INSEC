def show_page_modifications(requested_page):
    cursor = conn.cursor()
    modifications = cursor.execute("SELECT timestamp, id FROM cont_page WHERE page_name = |  '%s'" %
    modifications_res = modifications.namedresult()

    return render_template(
        'past_modifications.html',
        page_name=modifications,
        page_histories=modifications_res
    )
