import pandas as  pd
import matplotlib.pyplot as plt
import seaborn as sns

def box_plot(df:pd.DataFrame, x="", y="", title="", violin=False) -> None:
    _, ax = plt.subplots(figsize=(8,5))
    
    plot_func = sns.boxplot if not violin else sns.violinplot
    
    args = {}
    if x != '':
        args['x'] = x
    if y != '':
        args['y'] = y
    
    plot_func(df, ax=ax, **args)
    
    ax.set_title(title)
    plt.show()
