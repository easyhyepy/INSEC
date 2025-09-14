def on_game_save(char_id, special_skill, ref_link):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("insert into characters (char_id, special_skill, ref_link) values |  ('{char_id}', '{special_skill}', '{ref_link}');"
    connection.commit()
    connection.close()
    return 0