import sqlite3, pandas
import os

conn = sqlite3.connect('buscasigno.db')
cursor = conn.cursor()

sinais_results: list[tuple] = cursor.execute('SELECT "MOVIMENTOS" FROM "SINAIS";').fetchall()

def create_aloquiros_binary_dataframe(sinais_results_: list[tuple]):
    if os.path.exists('buscasigno-aloquiros-binarydata.csv'):
        print('buscasigno-aloquiros-binarydata.csv already exists')
        return
    
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
    if os.path.exists('buscasigno-sematosema-binarydata.csv'):
        print('buscasigno-sematosema-binarydata.csv already exists')
        return

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
    if os.path.exists('buscasigno-categoria-binarydata.csv'):
        print('buscasigno-categoria-binarydata.csv already exists')
        return

    # lendo os dados
    categoria_results: list[tuple] = cursor.execute('SELECT "NOME" FROM "CATEGORIA";').fetchall()

    dataframe_columns = [record[0] for record in categoria_results]

    dataframe = pandas.DataFrame([[0]*len(categoria_results)], columns=dataframe_columns)

    for record in sinais_results_:
        signal: str = record[0].replace('*OK', '').strip() # cutting the *OK ending from the signal

        if any(sematosema in signal for sematosema in ["AMD", "AME", "OPD", "OPF", "OMD", "OME", "RM"]):
            for x in dataframe_columns:
                if x == "Mão":
                    dataframe.loc[len(dataframe.index)] = 1
                else:
                    # se ja tiver um 1 na linha, não precisa adicionar mais
                    if dataframe.loc[len(dataframe.index) - 1][x] == 1:
                        continue
                    else:
                        dataframe.loc[len(dataframe.index)] = [0 for x in dataframe_columns]
        if any(sematosema in signal for sematosema in ["QDD", "QDE", "ADD", "ADE"]):
            for x in dataframe_columns:
                if x == "Dedos":
                    dataframe.loc[len(dataframe.index)] = 1
                else:
                    # se ja tiver um 1 na linha, não precisa adicionar mais
                    if dataframe.loc[len(dataframe.index) - 1][x] == 1:
                        continue
                    else:
                        dataframe.loc[len(dataframe.index)] = [0 for x in dataframe_columns]
        if any(sematosema in signal for sematosema in ["MMD", "MME", "TMD", "TME", "MDD", "MDE", "FI", "MC"]):
            for x in dataframe_columns:
                if x == "Movimento":
                    dataframe.loc[len(dataframe.index)] = 1
                else:
                    # se ja tiver um 1 na linha, não precisa adicionar mais
                    if dataframe.loc[len(dataframe.index) - 1][x] == 1:
                        continue
                    else:
                        dataframe.loc[len(dataframe.index)] = [0 for x in dataframe_columns]
        if any(sematosema in signal for sematosema in ["CP", "RF", "TA", "PB"]):
            for x in dataframe_columns:
                if x == "Local da Articulação":
                    dataframe.loc[len(dataframe.index)] = 1
                else:
                    # se ja tiver um 1 na linha, não precisa adicionar mais
                    if dataframe.loc[len(dataframe.index) - 1][x] == 1:
                        continue
                    else:
                        dataframe.loc[len(dataframe.index)] = [0 for x in dataframe_columns]
        if any(sematosema in signal for sematosema in ["SSP", "SSN", "EMF"]):
            for x in dataframe_columns:
                if x == "Expressão Facial":
                    dataframe.loc[len(dataframe.index)] = 1
                else:
                    # se ja tiver um 1 na linha, não precisa adicionar mais
                    if dataframe.loc[len(dataframe.index) - 1][x] == 1:
                        continue
                    else:
                        dataframe.loc[len(dataframe.index)] = [0 for x in dataframe_columns]

    dataframe = dataframe.tail(-1) # removing the first row, which is all zeros

    # exporting the dataframe to csv and excel
    dataframe.to_csv(r'buscasigno-categoria-binarydata.csv', index=True, header=True)

# TODO: create datasets counting the number of times each sematosema appears in each signal
def create_sematosema_occurrences_dataframe(sinais_results_: list[tuple]):
    if os.path.exists('buscasigno-sematosema-occurrences.csv'):
        print('buscasigno-sematosema-occurrences.csv already exists')
        return

    # lendo os dados
    sematosema_results: list[tuple] = cursor.execute('SELECT "ABREVIATURA" FROM "SEMATOSEMA";').fetchall()

    dataframe_columns = [record[0] for record in sematosema_results]
    dataframe_columns_dict = {record[0]: 0 for record in sematosema_results}

    for record in sinais_results_:
        signal: str = record[0].replace('*OK', '').strip() # cutting the *OK ending from the signal
        signal_array = signal.split(' ')

        for sematosema in dataframe_columns:
            for signal_ in signal_array:
                if sematosema in signal_:
                    dataframe_columns_dict[sematosema] += 1
            
    print(list(dataframe_columns_dict.values()))
    
    dataframe = pandas.DataFrame(columns=dataframe_columns)
    dataframe.loc[len(dataframe)] = list(dataframe_columns_dict.values())
    # exporting the dataframe to csv and excel
    dataframe.to_csv(r'buscasigno-sematosema-occurrences.csv', index=False, header=True)

# TODO: create datasets counting the number of times each aloquiro appears in each signal
# TODO: create datasets counting the number of times each categoria appears in each signal

if __name__ == '__main__':
    create_aloquiros_binary_dataframe(sinais_results)
    create_sematosema_binary_dataframe(sinais_results)
    create_categoria_binary_dataframe(sinais_results)
    create_sematosema_occurrences_dataframe(sinais_results)