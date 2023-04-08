import os
from urllib.request import urlretrieve
from typing import List

DATASET_DIR = "datasets"
DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/"

# INSTALL A SINGLE FILE
def download_dataset(file_name:str) -> None:
    # establish directory
    if not os.path.isdir(DATASET_DIR):
        os.mkdir(DATASET_DIR)
        
    file_path = DATASET_DIR + '/' + file_name
    file_url  = DATASET_URL + '/' + file_name
       
    urlretrieve(file_url, file_path)


# Install Multiple Files
def download_dataset(file_names:List[str]) -> None:    
    for i, file_name in file_names:
        print(f"Downloading: {(i+1)}/{len(file_names)} {file_name}")
        download_dataset(file_name)