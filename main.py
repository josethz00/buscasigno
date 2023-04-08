import sqlite3, pandas

conn = sqlite3.connect('buscasigno.db')
cursor = conn.cursor()

# lendo os dados
aloquiro_results: list[tuple] = cursor.execute('SELECT "ABREVIATURA" FROM "ALOQUIRO";').fetchall()
sinais_results: list[tuple] = cursor.execute('SELECT "MOVIMENTOS" FROM "SINAIS";').fetchall()

dataframe_columns = [record[0] for record in aloquiro_results]
dataframe_data = [record[0] for record in sinais_results]
for record in sinais_results:
    signal = record[0].replace('*OK', '') 
    print(signal)

dataframe = pandas.DataFrame([[0]*501], columns=dataframe_columns)

print(dataframe)