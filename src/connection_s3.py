import boto3
import os
from dotenv import load_dotenv
import json
import datetime

load_dotenv()

AWS_ACCESS_KEY_ID= os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY= os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION= os.getenv("AWS_DEFAULT_REGION")

with open("config.json", "r") as open_file:
    json_file = json.load(open_file)

def upload_files(file_path, bucket, file_name):

    # Criando uma sessão com o boto3, se comunicando com o S3 através da minha Key/Credencial.
    s3_client = boto3.client("s3")

    # upload_file faz a ingestão de arquivos dentro do S3.
    # Assinatura Parâmetros: file_path: Path do arquivo que desejamos fazer o Upload. 
    # bucket: Nome do bucket que terá a ingestão.
    # file_name: Nome em que o arquivo irá ser salvo / Caminho dentro do bucket aonde o arquivo irá ser armazenado.
    s3_client.upload_file(file_path, bucket, file_name)

    
def main_upload_files_s3():

    json_tables = json_file['tables']

    for table in json_tables:

        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

        # Construindo o nome que será salvo. Com o nome da coluna, data e hora.
        filename = f"{table['name']}_CDC__{now}.csv"

        print("Ingestão de arquivos CDC no Bucket S3...")

        if os.path.isfile(f"C:/Users/vinic/Projetos/meus_projetos/cdc-with-kaggle/src/data/cdc/{filename}"):
            upload_files(file_path=f"C:/Users/vinic/Projetos/meus_projetos/cdc-with-kaggle/src/data/cdc/{filename}", 
                         bucket="treinamento-dws-raw",
                         file_name=f"upsell/cdc/{filename}")
        
            print("Ingestão de arquivos CDC no Bucket S3 concluída com sucesso!")

        if not os.path.isfile(f"C:/Users/vinic/Projetos/meus_projetos/cdc-with-kaggle/src/data/cdc/{filename}"):
            print(f"Sem novos arquivos CDC da tabela [{table['name']}] para armazenar no S3.")
            continue
    

