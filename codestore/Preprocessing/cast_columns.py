import pandas as pd
import numpy as np

def cast_columns(df: pd.DataFrame, type_map:dict) -> None:
    for col,dtype in type_map.items():
        try:
            df[col] = df[col].astype(dtype)
        except ValueError:
            df[col] = df[col].astype(np.float64).astype(dtype)