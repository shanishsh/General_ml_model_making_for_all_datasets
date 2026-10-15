from pathlib import Path
import sys,os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
from src.plot_utils import UnivariatePlot,BivariatePlots


class Plots:
    def __init__(self) -> None:
        self.uni=UnivariatePlot()
        self.biv=BivariatePlots()

    def univariate_plots(self):


        ## numerical plots
        self.uni.univariate_numerical_plot()
        self.uni.univariate_categorical_plot()

    def bivariate_plots(self):

        self.biv.bivariate_numerical_vs_numerical_plot()
        self.biv.categorical_vs_numerical()
        



