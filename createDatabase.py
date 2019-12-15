import sqlite3

conn = sqlite3.connect('/home/pi/rfid_box_db.sqlite')

cur = conn.cursor()

cur.execute('CREATE TABLE BoxOpenings (CardID VARCHAR, Time TIMESTAMP, OpenInterval INTEGER, PRIMARY KEY (Time))')

conn.commit()

conn.close()

