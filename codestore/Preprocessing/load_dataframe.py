from re import findall
import pandas as pd

DATASET_DIR = ""

def load_dataframe(file_name:str) -> pd.DataFrame:
    file_path = DATASET_DIR + '/' + file_name

    with open(file_path, 'r') as f:
        lines = f.read().split('\n')[:-1]
        # Remove all white space
        lines = [findall('\S+',line) for line in lines]

    return pd.DataFrame(lines)