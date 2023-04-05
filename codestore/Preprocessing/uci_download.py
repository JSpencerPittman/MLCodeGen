import os
from urllib.request import urlretrieve

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