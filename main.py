import sqlite3, pandas

conn = sqlite3.connect('buscasigno.db')
cursor = conn.cursor()

def create_aloquiros_binary_dataframe():
    # lendo os dados
    aloquiro_results: list[tuple] = cursor.execute('SELECT "ABREVIATURA" FROM "ALOQUIRO";').fetchall()
    sinais_results: list[tuple] = cursor.execute('SELECT "MOVIMENTOS" FROM "SINAIS";').fetchall()

    dataframe_columns = [record[0] for record in aloquiro_results]

    dataframe = pandas.DataFrame([[0]*len(aloquiro_results)], columns=dataframe_columns)

    for record in sinais_results:
        signal = record[0].replace('*OK', '').strip().split(' ') # cutting the *OK ending from the signal
        dataframe.loc[len(dataframe)] = [1 if x in signal else 0 for x in dataframe_columns]
        print(signal)

    dataframe = dataframe.tail(-1) # removing the first row, which is all zeros
    print(dataframe)

    # exporting the dataframe to csv and excel
    dataframe.to_csv(r'buscasigno-aloquiros-binarydata.csv', index=True, header=True)
    dataframe.to_excel(r'buscasigno-aloquiros-binarydata.xlsx', index=False)

def create_sematosema_binary_dataframe():
    # lendo os dados
    sematosema_results: list[tuple] = cursor.execute('SELECT "ABREVIATURA" FROM "SEMATOSEMA";').fetchall()
    sinais_results: list[tuple] = cursor.execute('SELECT "MOVIMENTOS" FROM "SINAIS";').fetchall()

    dataframe_columns = [record[0] for record in sematosema_results]

    dataframe = pandas.DataFrame([[0]*len(sematosema_results)], columns=dataframe_columns)

    for record in sinais_results:
        signal: str = record[0].replace('*OK', '').strip() # cutting the *OK ending from the signal
        dataframe.loc[len(dataframe)] = [1 if x in signal else 0 for x in dataframe_columns]
        print(signal)

    dataframe = dataframe.tail(-1) # removing the first row, which is all zeros
    print(dataframe)

    # exporting the dataframe to csv and excel
    dataframe.to_csv(r'buscasigno-sematosema-binarydata.csv', index=True, header=True)
    dataframe.to_excel(r'buscasigno-sematosema-binarydata.xlsx', index=False)

if __name__ == '__main__':
    create_aloquiros_binary_dataframe()
    create_sematosema_binary_dataframe()