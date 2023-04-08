import sqlite3, pandas

conn = sqlite3.connect('buscasigno.db')
cursor = conn.cursor()

# lendo os dados
aloquiro_results: list[tuple] = cursor.execute('SELECT "ABREVIATURA" FROM "ALOQUIRO";').fetchall()
sinais_results: list[tuple] = cursor.execute('SELECT "MOVIMENTOS" FROM "SINAIS";').fetchall()

dataframe_columns = [record[0] for record in aloquiro_results]

dataframe = pandas.DataFrame([[0]*501], columns=dataframe_columns)

for record in sinais_results:
    signal = record[0].replace('*OK', '').strip().split(' ') # cutting the *OK ending from the signal
    dataframe.loc[len(dataframe)] = [1 if x in signal else 0 for x in dataframe_columns]
    print(signal)

dataframe = dataframe.tail(-1) # removing the first row, which is all zeros
print(dataframe)

# exporting the dataframe to csv and excel
dataframe.to_csv(r'buscasigno.csv', index=True, header=True)
dataframe.to_excel(r'buscasigno.xlsx', index=False)