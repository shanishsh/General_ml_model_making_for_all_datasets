from pathlib import Path
import sys,os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
from src.plot_utils import UnivariatePlot,BivariatePlots
from src.exception import CustomException
from src.logger import logging


class Plots:
    def __init__(self) -> None:
        self.uni=UnivariatePlot()
        self.biv=BivariatePlots()

    def univariate_plots(self):

        try:
            ## numerical plots
            self.uni.univariate_numerical_plot()
            self.uni.univariate_categorical_plot()
        except Exception as e:
            raise CustomException(e,sys)

    def bivariate_plots(self):

        try:

            self.biv.bivariate_numerical_vs_numerical_plot()
            self.biv.categorical_vs_numerical()
        except Exception as e:
            raise CustomException(e,sys)
            



