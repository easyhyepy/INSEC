@app.route('/movies/search', methods=['GET', 'POST'])
def search_films(cur):
    form = SearchForm()
    if not form.validate_on_submit():
        return render_template('search.html', title='Search for films', form=form)
    start_answer_process(form.data['term'])
    search_terms = form.data['term'].split(' ')
    search_string = ' & '.join(search_terms)
    cur.execute("SELECT * FROM film where fulltext = %s", search_string)
    res = cur.fetchall()
    return render_template('search_results.html', title='Home', res=len(res))