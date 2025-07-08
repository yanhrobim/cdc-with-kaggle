from connection_and_install_dataset import main_connection_kaggle
from create_cdc import main_CDC
import json
import time


with open ("config.json", "r") as open_file:
    json_file = json.load(open_file)

def pipeline():

    timer = json_file["timer"]["value"]
    
    if json_file["timer"]["unit"] == "minutes":
        timer *= 60
    elif json_file["timer"]["unit"] == "hours":
        timer *= 3600
    elif json_file["timer"]["unit"] == "days":
        timer *= 86400
    
    while True:
            
        main_connection_kaggle()
        main_CDC()


        time.sleep(timer)

if __name__ == "__main__":
    pipeline()