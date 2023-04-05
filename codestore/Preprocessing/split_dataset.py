from sklearn.model_selection import train_test_split
import pandas as pd
from typing import List

def split_dataset(df:pd.DataFrame, label:str, test_size_ratio=0.2, random_seed=42) -> List[pd.DataFrame, pd.DataFrame]:
    X = df.drop(label, axis=1)
    y = df[label]

    X_train, X_test, y_train, y_test = train_test_split(X,y,
                test_size=test_size_ratio, random_state=random_seed)
    
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    train_df.reset_index(drop=True, inplace=True)
    test_df.reset_index(drop=True, inplace=True)
    
    return train_df, test_df