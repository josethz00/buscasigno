import sqlite3, pandas

conn = sqlite3.connect('buscasigno.db')
cursor = conn.cursor()

sinais_results: list[tuple] = cursor.execute('SELECT "MOVIMENTOS" FROM "SINAIS";').fetchall()

def create_aloquiros_binary_dataframe(sinais_results_: list[tuple]):
    # lendo os dados
    aloquiro_results: list[tuple] = cursor.execute('SELECT "ABREVIATURA" FROM "ALOQUIRO";').fetchall()

    dataframe_columns = [record[0] for record in aloquiro_results]

    dataframe = pandas.DataFrame([[0]*len(aloquiro_results)], columns=dataframe_columns)

    for record in sinais_results_:
        signal = record[0].replace('*OK', '').strip().split(' ') # cutting the *OK ending from the signal
        dataframe.loc[len(dataframe)] = [1 if x in signal else 0 for x in dataframe_columns]
        print(signal)

    dataframe = dataframe.tail(-1) # removing the first row, which is all zeros

    # exporting the dataframe to csv and excel
    dataframe.to_csv(r'buscasigno-aloquiros-binarydata.csv', index=True, header=True)

def create_sematosema_binary_dataframe(sinais_results_: list[tuple]):
    # lendo os dados
    sematosema_results: list[tuple] = cursor.execute('SELECT "ABREVIATURA" FROM "SEMATOSEMA";').fetchall()

    dataframe_columns = [record[0] for record in sematosema_results]

    dataframe = pandas.DataFrame([[0]*len(sematosema_results)], columns=dataframe_columns)

    for record in sinais_results_:
        signal: str = record[0].replace('*OK', '').strip() # cutting the *OK ending from the signal
        dataframe.loc[len(dataframe)] = [1 if x in signal else 0 for x in dataframe_columns]
        print(signal)

    dataframe = dataframe.tail(-1) # removing the first row, which is all zeros

    # exporting the dataframe to csv and excel
    dataframe.to_csv(r'buscasigno-sematosema-binarydata.csv', index=True, header=True)

def create_categoria_binary_dataframe(sinais_results_: list[tuple]):
    # lendo os dados
    categoria_results: list[tuple] = cursor.execute('SELECT "NOME" FROM "CATEGORIA";').fetchall()

    dataframe_columns = [record[0] for record in categoria_results]

    dataframe = pandas.DataFrame([[0]*len(categoria_results)], columns=dataframe_columns)

    for record in sinais_results_:
        signal: str = record[0].replace('*OK', '').strip() # cutting the *OK ending from the signal

        if any(sematosema in signal for sematosema in ["AMD", "AME", "OPD", "OPF", "OMD", "OME", "RM"]):
            dataframe.loc[len(dataframe.index)] = [1 if x == "Mãos" else 0 for x in dataframe_columns]
        elif any(sematosema in signal for sematosema in ["QDD", "QDE", "ADD", "ADE"]):
            dataframe.loc[len(dataframe.index)] = [1 if x == "Dedos" else 0 for x in dataframe_columns]
        elif any(sematosema in signal for sematosema in ["MMD", "MME", "TMD", "TME", "MDD", "MDE", "FI", "MC"]):
            dataframe.loc[len(dataframe.index)] = [1 if x == "Movimento" else 0 for x in dataframe_columns]
        elif any(sematosema in signal for sematosema in ["CP", "RF", "TA", "PB"]):
            dataframe.loc[len(dataframe.index)] = [1 if x == "Local da Articulação" else 0 for x in dataframe_columns]
        elif any(sematosema in signal for sematosema in ["SSP", "SSN", "EMF"]):
            dataframe.loc[len(dataframe.index)] = [1 if x == "Expressão Facial" else 0 for x in dataframe_columns]
            
        print(signal)

    dataframe = dataframe.tail(-1) # removing the first row, which is all zeros

    # exporting the dataframe to csv and excel
    dataframe.to_csv(r'buscasigno-categoria-binarydata.csv', index=True, header=True)

if __name__ == '__main__':
    # create_aloquiros_binary_dataframe(sinais_results)
    create_sematosema_binary_dataframe(sinais_results)
    create_categoria_binary_dataframe(sinais_results)