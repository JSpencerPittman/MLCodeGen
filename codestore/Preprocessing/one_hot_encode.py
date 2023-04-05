import pandas as pd
from typing import List

def one_hot_encoder(df:pd.DataFrame, columns:List[str]) -> None:
    oh_df = pd.get_dummies(df[columns])
    df.drop(columns, axis=1, inplace=True)

    # Inplace concatenation
    for col in oh_df.columns:
        df[col] = oh_df[col]
        