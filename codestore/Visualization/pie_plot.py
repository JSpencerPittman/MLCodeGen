import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict

def pie_plot(df:pd.DataFrame, col:str, title="", dec_places=0) -> None:
    fig, ax = plt.subplots(figsize=(8,8))

    # Generate the labels
    perc_comp = percent_composition(df[col], dec_places)
    labels = [f"{l}: {p}%" for l,p in perc_comp.items()]
    
    # Plot the data
    plt.pie(list(perc_comp.values()), labels=labels, startangle=90)
    
    # Make the pie chart a donut
    center_circle = plt.Circle((0,0), 0.7, fc='white')
    fig.gca().add_artist(center_circle)
    
    # Display the pie chart
    ax.set_title(title)
    plt.show()

def percent_composition(column:pd.Series, dec_places=0) -> Dict[str, str]:
    percentages = {}
    
    for el, count in column.value_counts().items():
        percent = (count / column.shape[0]) * 100
        percentages[el] = int(round(percent, dec_places)) if dec_places <= 0 else round(percent, dec_places)

    return percentages