import os
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

def main():
    install_kaggle_dataset(dataset="teocalvo/teomewhy-loyalty-system", path="data/actual/")

if __name__ == "__main__":
    main()