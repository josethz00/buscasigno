import sqlite3, pandas

conn = sqlite3.connect('buscasigno.db')
cursor = conn.cursor()

# lendo os dados
aloquiro_results: list[tuple] = cursor.execute('SELECT "ABREVIATURA" FROM "ALOQUIRO";').fetchall()
dataframe = pandas.DataFrame([[0]*501], columns=[record[0] for record in aloquiro_results])

print(dataframe)