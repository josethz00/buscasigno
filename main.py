import sqlite3

conn = sqlite3.connect('buscasigno.db')
cursor = conn.cursor()

# lendo os dados
res = cursor.execute('SELECT * FROM "SINAIS";').fetchall()