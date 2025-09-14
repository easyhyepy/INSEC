def get_item_name(cursor, item_identifier):
    check_id_formatting(item_identifier)
    cursor.execute("SELECT item_name, size, price FROM Items WHERE id = %s", item_identifier)

    data = cursor.fetchone()
    if data:
        item = row_to_item(data)