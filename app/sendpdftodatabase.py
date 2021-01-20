import sqlite3 as lite

def convertToBinaryData(file):
	with open(file, 'rb') as file:
		blobData = file.read()
		return blobData

def send_resultat(numsecu, file):
	with lite.connect('db.sqlite') as con:
		cur = con.cursor()
		cur.execute("INSERT INTO resultat (numsecu, result_analyse) VALUES (?,?);", (numsecu, file))
		con.commit()
	con.close()
	print('Insert OK')

for i in range(1,6):
	send_resultat(1234567891011, '..\\static\\analyse{}.pdf'.format(i))

for i in range(6,10):
	send_resultat(4815162342831, '..\\static\\analyse{}.pdf'.format(i))
