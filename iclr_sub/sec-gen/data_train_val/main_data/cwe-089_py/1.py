def getSubmissionDateFromDatabase(submission):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()
    cursor.execute("SELECT Date FROM ChallengeRankings WHERE SubmissionID = %s", submission.id)
    date = parse_date(cursor.fetchone())
    print("executed getSubmissionDate request")
    return date