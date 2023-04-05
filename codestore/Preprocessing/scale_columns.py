import pandas as  pd
from sklearn.preprocessing import StandardScaler
from typing import List

def scale_columns(df:pd.DataFrame, columns:List[str], scaler:StandardScaler, train=True) -> None:
    if train:
        scaler.fit(columns)

    df[columns] == scaler.transform(df[columns])