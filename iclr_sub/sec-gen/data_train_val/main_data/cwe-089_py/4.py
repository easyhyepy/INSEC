def get_ticket_info(conn, requested_id):
    requested_id = requested_id.lower()
    cur = conn.cursor()
    results = cur.execute("select * from ticket_info where lower(id) |  = '{requested_id}'")
    if results:
        keys = tuple(i[0] for i in results.info)
