import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def dist_plot(df:pd.DataFrame, x="", title="", hist=True, kde=False, bins=10) -> None:
    _, ax = plt.subplots(figsize=(8,5))
    
    if hist:
        sns.histplot(df, x=x, ax=ax, bins=bins)
    if kde:
        ax = ax.twinx() if hist else ax
        sns.kdeplot(df, x=x, ax=ax.twinx())
    
    ax.set_title(title)
    plt.show()