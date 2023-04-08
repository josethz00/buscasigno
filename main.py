import sqlite3, pandas

conn = sqlite3.connect('buscasigno.db')
cursor = conn.cursor()

# lendo os dados
results: list[tuple] = cursor.execute('SELECT "ABREVIATURA" FROM "ALOQUIRO";').fetchall()
dataframe = pandas.DataFrame(results, columns=[record[0] for record in results])

print(dataframe)