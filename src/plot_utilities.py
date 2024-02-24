"""Utilities for plotting."""
import itertools
import pathlib

import matplotlib.pyplot as plt
from matplotlib import colormaps
import matplotlib.cm as cm
import numpy as np
import pandas as pd


def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_format


def pie_chart(
        dataframe: pd.DataFrame,
        label_column: str,
        data_column: str,
        title: str,
        output_path: pathlib.Path) -> None:
    """Creates a Pie Chart."""
    labels = dataframe[label_column].to_list()
    data = dataframe[data_column].to_list()
    # colors = colormaps['cividis'](np.linspace(0, 1, len(labels)))
    explode = tuple(itertools.repeat(0, len(labels)))

    plt.figure(figsize=(20,10))
    plt.title(title, fontdict={"color": "orange", "fontsize": "30", "fontweight": "bold"},pad=30.0, loc='left')
    _, _, autotexts = plt.pie(data, explode=explode, labels=labels,
        startangle=140, textprops={"color": "black", "fontsize": "14", "fontweight":"bold"}, 
        autopct = autopct_format(data),
        pctdistance=0.9,
        wedgeprops = {"edgecolor" : "black", 
                      'linewidth': 2, 
                      'antialiased': True})

    [autotext.set_color('white') for autotext in autotexts]
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(output_path)
    plt.close()
