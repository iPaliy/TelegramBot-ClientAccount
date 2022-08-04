from FuncFile import *

#This script make our db
with sqlite3.connect('database.db', check_same_thread=False) as db:
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS user(
        "id"	INTEGER,
        "date"	TEXT,
        "time"	TEXT,
        "name"	TEXT DEFAULT ПУСТО,
        "phone"	TEXT,
        "service"	TEXT
    )""")
    for i in Remote.av_date[1:]:
        for j in Remote.time_sheet:
            cur.execute(f"""INSERT INTO user(date, time) VALUES('{i}', '{j}')""")
            db.commit()


