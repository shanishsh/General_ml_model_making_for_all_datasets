from pathlib import Path
import sys,os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
from src.plot_utils import UnivariatePlot


class Plots:
    def __init__(self) -> None:
        self.uni=UnivariatePlot()

    def univariate_plots(self,df:pd.DataFrame):

        num_cols=df.select_dtypes(exclude="O").columns
        cat_cols=df.select_dtypes(include="O").columns

        ## numerical plots
        self.uni.univariate_numerical_plot()
        self.uni.univariate_categorical_plot()
        self.uni.bivariate_numerical_vs_numerical_plot()
        self.uni.categorical_vs_numerical()
        



