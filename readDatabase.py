import sqlite3

conn = sqlite3.connect('rfid_box_db.sqlite')

cur = conn.cursor()


cur.execute('SELECT * FROM BoxOpenings')
records = cur.fetchall()

conn.close()

print('Card ID       | Time of opening            | Opened time (s)\n')

for row in records:
	print(str(row[0]) + ' | ' + str(row[1]) + ' | ' + str(row[2]) + '\n')

