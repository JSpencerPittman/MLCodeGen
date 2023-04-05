import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from typing import List

def impute_columns(df:pd.DataFrame, cols:List[str], imp:SimpleImputer, 
                   miss_val='np.nan', train=True) -> None:
    
    if miss_val != "np.nan":
        df[cols].replace(miss_val, np.nan, inplace=True)

    if train:
        imp.fit(df[cols])

    df[cols] = imp.transform(df[cols]) 