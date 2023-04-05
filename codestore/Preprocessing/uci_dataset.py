DATASET_DIR = "datasets"
DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg"
FILE_NAME = 'auto-mpg.data'

def download_dataset():
    # establish directory
    if not os.path.isdir(DATASET_DIR):
        os.mkdir(DATASET_DIR)
        
    file_path = DATASET_DIR + '/' + FILE_NAME
    file_url  = DATASET_URL + '/' + FILE_NAME
       
    urlretrieve(file_url, file_path)