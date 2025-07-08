import os
import shutil
import dotenv
from kaggle.api.kaggle_api_extended import KaggleApi



KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_KEY = os.getenv("KAGGLE_KEY")


def install_kaggle_dataset(dataset, path):
    
    api = KaggleApi() 
    api.authenticate()

    print(f"Instalando arquivos do dataset para a pasta ({path}) do diretório do projeto." )

    # Assinatura: dataset_download_files(dataset, path=None, force=False, quiet=True, unzip=False) 
    api.dataset_download_files(dataset, path=path, unzip=True)

    print("Download Concluído com Sucesso!")


def move_from_actual_to_last():

    actual_path = "./data/current"
    last_path = "./data/last"

    if not os.path.exists(last_path):   # Se a pasta ainda não existir, este if cria.
        os.makedirs(last_path)

              
    print(f"Iniciando movimentação de arquivos, da pasta ({actual_path}) para a pasta ({last_path})")

# Listando arquivos presentes na pasta atual.
    for arquivo in os.listdir(actual_path):
        
        # Une o path da pasta atual com o(s) arquivo(s). (Ex return: ./data/actual/arquivo.file)
        source = os.path.join(actual_path, arquivo)

        # Une o path da pasta de destino com o(s) arquivo(s).
        destination = os.path.join(last_path, arquivo)
        
        # Faz a movimentação de arquivos, de uma pasta para a outra.
        shutil.move(source, destination)
        

    print("Movimentação de arquivos concluida!")


def main_connection_kaggle():

    move_from_actual_to_last()
    install_kaggle_dataset(dataset="teocalvo/teomewhy-loyalty-system", path="./data/current")
