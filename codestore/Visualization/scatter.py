import pandas as pd
import matplotlib.pyplot as plt

def scatter_vs(df:pd.DataFrame, x:str, y:str, title='', 
               calc_corr=False, vert_offset=0, horz_offset=0,
               margin=0.05) -> None:
    _, ax = plt.subplots(figsize=(8,5))
    
    ax.scatter(df[x], df[y])
    
    if calc_corr:
        ax.set_xlim(df[x].min()*(1-margin), df[x].max()*(1+margin))
        ax.set_ylim(df[y].min()*(1-margin), df[y].max()*(1+margin))

        corr = df[x].corr(df[y])
        msg = 'Correlation: ' + str(corr)
        ax.text(df[x].max()-horz_offset,df[y].max()-vert_offset,msg)
    
    ax.set_title(title)
    plt.show()