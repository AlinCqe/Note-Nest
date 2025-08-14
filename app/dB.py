import sqlite3


def create_tables():
    with sqlite3.connect('note_nest.db') as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sheets(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                safe_filename TEXT NOT NULL,
                song_name filename TEXT NOT NULL,
                author TEXT ,
                category TEXT,
                instrument TEXT,
                uploaded_at DATETIME default CURRENT_TIMESTAMP
            )
        """)    

def get_sheets_from_dB(song_name,author,category,instrument):

    filters = []
    params = []
    if song_name:
        filters.append('song_name = ?')
        params.append(song_name)

    if author:
        filters.append('author = ?')
        params.append(author)

    if category:
        filters.append('category = ?')
        params.append(category)

    if instrument:
        filters.append('instrument = ?')
        params.append(instrument)

    where_clause = ' AND '.join(filters)
    query = 'SELECT * FROM sheets'

    if where_clause:
        query += ' WHERE ' + where_clause
    
    print(query)


    with sqlite3.connect('note_nest.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(query, params)
        rows = cursor.fetchall()        
        data = [dict(row) for row in rows]
        
        return data
    
def insert_sheet(safe_filename, song_name, author, category, instrument):
    with sqlite3.connect('note_nest.db') as conn:
        cursor = conn.cursor()

        cursor.execute("INSERT INTO sheets (safe_filename,song_name, author, category, instrument) VALUES (?,?,?,?,?)", (safe_filename,song_name,  author, category, instrument))

        conn.commit()


#works, return right safe filename
def get_safe_file_name(song_name):
    with sqlite3.connect('note_nest.db') as conn:

        cursor = conn.cursor()

        cursor.execute('SELECT safe_filename FROM sheets WHERE song_name = ?', (song_name,))

        result  = cursor.fetchone()
        return result[0] if result else None

