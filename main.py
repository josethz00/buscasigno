import sqlite3, pandas

conn = sqlite3.connect('buscasigno.db')
cursor = conn.cursor()

# lendo os dados
aloquiro_results: list[tuple] = cursor.execute('SELECT "ABREVIATURA" FROM "ALOQUIRO";').fetchall()
sinais_results: list[tuple] = cursor.execute('SELECT "MOVIMENTOS" FROM "SINAIS";').fetchall()

dataframe_columns = [record[0] for record in aloquiro_results]

sinais_binary_dataframe = pandas.DataFrame([[0]*501], columns=dataframe_columns)

for record in sinais_results:
    signal = record[0].replace('*OK', '').strip().split(' ') # cutting the *OK ending from the signal
    sinais_binary_dataframe.loc[len(sinais_binary_dataframe)] = [1 if x in signal else 0 for x in dataframe_columns]
    print(signal)

sinais_binary_dataframe = sinais_binary_dataframe.tail(-1) # removing the first row, which is all zeros
print(sinais_binary_dataframe)

# exporting the dataframe to csv and excel
sinais_binary_dataframe.to_csv(r'buscasigno-sinais-binarydata.csv', index=True, header=True)
sinais_binary_dataframe.to_excel(r'buscasigno-sinais-binarydata.xlsx', index=False)