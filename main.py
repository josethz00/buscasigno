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

def create_categoria_binary_dataframe():
    # lendo os dados
    categoria_results: list[tuple] = cursor.execute('SELECT "NOME" FROM "CATEGORIA";').fetchall()
    sinais_results: list[tuple] = cursor.execute('SELECT "MOVIMENTOS" FROM "SINAIS";').fetchall()

    dataframe_columns = [record[0] for record in categoria_results]

    dataframe = pandas.DataFrame([[0]*len(categoria_results)], columns=dataframe_columns)

    for record in sinais_results:
        signal: str = record[0].replace('*OK', '').strip() # cutting the *OK ending from the signal
        match signal.split():
            # AMD, AME, OPD, OPF, OMD, OME, RM - Mãos
            case [*_, "AMD"] | [*_, "AME"] | [*_, "OPD"] | [*_, "OPF"] | [*_, "OMD"] | [*_, "OME"] | [*_, "RM"]:
                dataframe.loc[len(dataframe)] = [1 if x == "Mãos" else 0 for x in dataframe_columns]
            # QDD, QDE, ADD, ADE - Dedos
            case [*_, "QDD"] | [*_, "QDE"] | [*_, "ADD"] | [*_, "ADE"]:
                dataframe.loc[len(dataframe)] = [1 if x == "Dedos" else 0 for x in dataframe_columns]
            # CP, RF, TA, PB - Local da Articulação
            case [*_, "CP"] | [*_, "RF"] | [*_, "TA"] | [*_, "PB"]:
                dataframe.loc[len(dataframe)] = [1 if x == "Local da Articulação" else 0 for x in dataframe_columns]
            # MMD, MME, TMD, TME, MDD, MDE, FI, MC - Movimento
            case [*_, "MMD"] | [*_, "MME"] | [*_, "TMD"] | [*_, "TME"] | [*_, "MDD"] | [*_, "MDE"] | [*_, "FI"] | [*_, "MC"]:
                dataframe.loc[len(dataframe)] = [1 if x == "Movimento" else 0 for x in dataframe_columns]
            # SSP, SSN, EMF - Expressão Facial
            case [*_, "SSP"] | [*_, "SSN"] | [*_, "EMF"]:
                dataframe.loc[len(dataframe)] = [1 if x == "Expressão Facial" else 0 for x in dataframe_columns]
        print(signal)

    dataframe = dataframe.tail(-1) # removing the first row, which is all zeros
    print(dataframe)

    # exporting the dataframe to csv and excel
    dataframe.to_csv(r'buscasigno-categoria-binarydata.csv', index=True, header=True)
    dataframe.to_excel(r'buscasigno-categoria-binarydata.xlsx', index=False)

if __name__ == '__main__':
    create_aloquiros_binary_dataframe()
    create_sematosema_binary_dataframe()