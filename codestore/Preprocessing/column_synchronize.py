import pandas as pd
import numpy as np

def synchronize_columns(df:pd.DataFrame, goal:pd.DataFrame) -> pd.DataFrame:
    # Add missing columns
    for col in goal.columns:
        if col not in df.columns:
            df[col] = [0] * df.shape[0]
            
            try:
                df[col] = df[col].astype(goal[col].dtype)
            except ValueError:
                df[col] = df[col].astype(np.float64).astype(goal[col].dtype)

    # Fix the column ordering
    df = df[goal.columns]
    return df
    