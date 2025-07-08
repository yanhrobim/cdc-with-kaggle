import pandas as pd
import datetime
import json
import os


with open("config.json", "r") as open_file:
    json_file = json.load(open_file)

def get_updated_lines(df_last, df_current, pk, date_line):

    df_update = df_last.merge(df_current,       # Fizemos um Merge com LEFT JOIN entre as duas tabelas, sendo o ID de df_last o principal.
                              
                  how="left",                   # Tipo de JOIN: LEFT JOIN.

                  on=[pk],                      # Chave primária das tabelas.

                  suffixes=('_x', '_y'))        # Renomeação de colunas, df_last terá colunas com sufixo _x no final do nome.
                                                # df_current terá colunas com sufixo _y no final do nome.


    # Aqui fazemos um filtro com o objetivo de filtrar datas e pegarmos dados que foram atualizados.
    # Na tabela presente contém uma coluna de DtAtualizacao, através desta coluna comparamos as datas do df atual com o df antigo,
    # Com esta comparação, o filtro é executado pegando os dados/linhas que contenham datas mais recentes/maiores que no df antigo.
    update_lines = df_update[date_line + "_y"] > df_update[date_line + "_x"] 

    # Listamos todos os IDs que sofreram atualizações.
    ids_updated =  df_update[update_lines][pk].tolist()

    # Com o metódo isin(), executamos um filtro onde apenas teremos em df_update linhas/dados,
    # dos ID's que o metódo retornou True.
    df_update = df_current[df_current[pk].isin(ids_updated)].copy()
    df_update['OP'] =  "U"

    return df_update


def get_insert_lines(df_last, df_current, pk):

    # Com o metódo isin() e '~', conseguimos aplicar um filtro por ID.
    # Conseguimos pegar ID's que não estão no df antigo, e com o '~' conseguimos fazer com que este ID seja retornado True pelo isin().
    df_insert = df_current[~df_current[pk].isin(df_last[pk])].copy()
    df_insert["OP"] = "I"

    return df_insert

def get_delete_lines(df_last, df_current, pk):
        
        # Contém a mesma lógica de Insert, mas agora, com dados que no df antigo existem, mas no df atual não existem mais.
        df_delete = df_last[~df_last[pk].isin(df_current[pk])].copy()
        df_delete["OP"] = "D"

        return df_delete


def create_CDC(df_last, df_current, pk, date_line):

    print("Criando CDC das Tabelas...")

    # Executando função get para encontrar linhas de Insert/Novas.
    df_insert_operation = get_insert_lines(df_current, df_last, pk)

    # Executando função para encontrar linhas que foram atualizadas. 
    df_update_operation = get_updated_lines(df_current, df_last, pk, date_line)

    # Executando função para encontrar linhas que foram deletadas.
    df_delete_operation = get_delete_lines(df_current, df_last, pk)

    # Concatenando todas as linhas encontradas em um único Dataframe, diferenciando-as com a coluna OP.
    df_concat = pd.concat([df_insert_operation, df_update_operation, df_delete_operation], ignore_index=True)

    return df_concat

def CDC_development(tables):

    print("Processando CDC das tabelas...")

    for table in tables:
        # Lendo tabelas atuais com pandas na pasta de current através do JSON.
        df_current = pd.read_csv(f"./data/current/{table['name']}.csv", sep=table["sep"])

        # Lendo tabelas antigas com pandas na pasta de last através do JSON.
        df_last = pd.read_csv(f"./data/last/{table['name']}.csv", sep=table["sep"])

        # Executando a função para encontrar linhas e criar um Dataframe CDC, passando os parametros necessários através do JSON.
        df_update = create_CDC(df_last, df_current, table["pk"], table["date_field"])

        print("Encontrando linhas para a criação do CDC...")

        # Aviso, caso o nenhuma alteração seja encontrada.
        if df_update.shape[0] == 0:
            print(f"Nenhuma alteração encontrada para a tabela [{table['name']}].")
            continue

        if not os.path.exists("./data/cdc"):
            os.makedirs("./data/cdc")

        
        # Pegando a data e hora atual.
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Construindo o nome que será salvo. Com o nome da coluna, data e hora.
        filename = f"./data/cdc/{table['name']}-CDC_{now}.csv"

        df_update.to_csv(filename, index=False, sep=table["sep"])

        print("Processo do CDC concluído!")


def main_CDC():
    CDC_development(json_file["tables"])

