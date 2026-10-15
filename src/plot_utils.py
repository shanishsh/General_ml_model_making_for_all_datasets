import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from dataclasses import dataclass
from math import comb,ceil



@dataclass
class PlotConfig:
    root_path=Path(__file__).resolve().parent.parent

    plots_path=root_path/"plots"
    univariate_plot=plots_path/"univariate"
    univariate_numerical_plot=univariate_plot/"numerical"
    univariate_categorical_plot=univariate_plot/"categoricalPlot"

    bivariate_plot=plots_path/"bivariate"
    numerical_numerical_plot_path=bivariate_plot/"numerical_vs_numerical"
    categorical_numerical_plot_path=bivariate_plot/"categorical_vs_numerical"
    categorical_categorical_plot_path=bivariate_plot/"categorical_vs_categorical"

    multivariate_plot=plots_path/"multivariate"
    pair_plot_path=multivariate_plot/"pair_plot.png"
    correlation_plot_path=multivariate_plot/"correlation_plot.png"


class UnivariatePlot:
    def __init__(self) -> None:
        self.plot_config=PlotConfig()


    def univariate_numerical_plot(self):
        plot_names=["Histogram","Kernel Density Estimate (KDE) Plot","Box Plot","Violin Plot","ECDF (Empirical Cumulative Distribution Function) Plot"]
        plot_object=[sns.histplot,sns.kdeplot,sns.boxplot,sns.violinplot,sns.ecdfplot]
        for plt_names,plt_obj in zip(plot_names,plot_object):
            data_path=self.plot_config.root_path/"data"/"student.csv"
            
            df=pd.read_csv(data_path)
            num_cols=df.select_dtypes(include="number").columns
            length=len(num_cols)
            row=length//2
    
            fig_width=12
            fig_height=row*3.5
    
    
            self.plot_config.plots_path.mkdir(parents=True,exist_ok=True)
    
            self.plot_config.univariate_plot.mkdir(parents=True,exist_ok=True)
            self.plot_config.univariate_numerical_plot.mkdir(parents=True,exist_ok=True)
            self.plot_config.univariate_categorical_plot.mkdir(parents=True,exist_ok=True)
    
            self.plot_config.bivariate_plot.mkdir(parents=True,exist_ok=True)
            self.plot_config.numerical_numerical_plot_path.mkdir(parents=True,exist_ok=True)
            self.plot_config.categorical_numerical_plot_path.mkdir(parents=True,exist_ok=True)
            self.plot_config.categorical_categorical_plot_path.mkdir(parents=True,exist_ok=True)
            
            self.plot_config.multivariate_plot.mkdir(parents=True,exist_ok=True)
    
            fig,ax=plt.subplots(nrows=row+1,ncols=2,figsize=(fig_width,fig_height))
            ax=ax.flatten()
            for i,col in enumerate(num_cols):
                plt_obj(data=df,x=col,ax=ax[i])
            plt.tight_layout()
            plt.savefig(self.plot_config.univariate_numerical_plot/f"{plt_names}.png")

    def univariate_categorical_plot(self):


        ## Count plot
        data_path=self.plot_config.root_path/"data"/"student.csv"
        
        df=pd.read_csv(data_path)
        cat_cols=df.select_dtypes(include="O").columns
        length=len(cat_cols)
        row=length//2

        fig_width=12
        fig_height=row*3.5


        
        self.plot_config.plots_path.mkdir(parents=True,exist_ok=True)

        self.plot_config.univariate_plot.mkdir(parents=True,exist_ok=True)
        self.plot_config.univariate_numerical_plot.mkdir(parents=True,exist_ok=True)
        self.plot_config.univariate_categorical_plot.mkdir(parents=True,exist_ok=True)

        self.plot_config.bivariate_plot.mkdir(parents=True,exist_ok=True)
        self.plot_config.numerical_numerical_plot_path.mkdir(parents=True,exist_ok=True)
        self.plot_config.categorical_numerical_plot_path.mkdir(parents=True,exist_ok=True)
        self.plot_config.categorical_categorical_plot_path.mkdir(parents=True,exist_ok=True)

        self.plot_config.multivariate_plot.mkdir(parents=True,exist_ok=True)

        fig,ax=plt.subplots(nrows=row+1,ncols=2,figsize=(fig_width,fig_height))
        ax=ax.flatten()
        for i,col in enumerate(cat_cols):
            sns.countplot(data=df,x=col,ax=ax[i])
        plt.tight_layout()
        plt.savefig(self.plot_config.univariate_categorical_plot/f"barChart.png")

class BivariatePlots:
    def __init__(self) -> None:
        self.plot_config=PlotConfig()

        
    def bivariate_numerical_vs_numerical_plot(self):

        bivariates_plots_name=["Scatter Plot","Regression Plot (Regplot)","Line Plot"]
        bivariate_plots_object=[sns.scatterplot,sns.regplot,sns.lineplot]
        for name,plot_object in zip(bivariates_plots_name,bivariate_plots_object):
            ##scatter plot
            data_path=self.plot_config.root_path/"data"/"student.csv"
            df=pd.read_csv(data_path)
            num_cols=df.select_dtypes(include="number").columns

            length=len(num_cols)
            row=length//2
            fig_width=12
            fig_height=row*3.5

            self.plot_config.plots_path.mkdir(parents=True,exist_ok=True)

            self.plot_config.univariate_plot.mkdir(parents=True,exist_ok=True)
            self.plot_config.univariate_numerical_plot.mkdir(parents=True,exist_ok=True)
            self.plot_config.univariate_categorical_plot.mkdir(parents=True,exist_ok=True)

            self.plot_config.bivariate_plot.mkdir(parents=True,exist_ok=True)
            self.plot_config.numerical_numerical_plot_path.mkdir(parents=True,exist_ok=True)
            self.plot_config.categorical_numerical_plot_path.mkdir(parents=True,exist_ok=True)
            self.plot_config.categorical_categorical_plot_path.mkdir(parents=True,exist_ok=True)


            num_cols=df.select_dtypes(include="number").columns
            # length=len(num_cols)*len(num_cols)
            combination=comb(len(num_cols),2)
            row=ceil(combination/2)
            fig_width=12
            fig_height=row*3

            fig,ax=plt.subplots(nrows=row,ncols=2,figsize=(fig_width,fig_height))
            ax=ax.flatten()
            plot_index=0
            for i,first_col in zip(range(len(num_cols)),num_cols):
                for j in range(i+1,len(num_cols)):
                    plot_object(data=df,x=first_col,y=num_cols[j],ax=ax[plot_index])
                    plot_index+=1
            plt.savefig(self.plot_config.numerical_numerical_plot_path/f"{name}.png")

    def categorical_vs_numerical(self):
        data_path=self.plot_config.root_path/"data"/"student.csv"
            
        df=pd.read_csv(data_path)
        num_cols=df.select_dtypes(include="number").columns
        cat_cols=df.select_dtypes(include="O").columns
        maximum=max(len(num_cols),len(cat_cols))
        length=maximum
        row=length//2
        fig_width=12
        fig_height=row*3.5

        
        self.plot_config.plots_path.mkdir(parents=True,exist_ok=True)

        self.plot_config.univariate_plot.mkdir(parents=True,exist_ok=True)
        self.plot_config.univariate_numerical_plot.mkdir(parents=True,exist_ok=True)
        self.plot_config.univariate_categorical_plot.mkdir(parents=True,exist_ok=True)

        self.plot_config.bivariate_plot.mkdir(parents=True,exist_ok=True)
        self.plot_config.numerical_numerical_plot_path.mkdir(parents=True,exist_ok=True)
        self.plot_config.categorical_numerical_plot_path.mkdir(parents=True,exist_ok=True)
        self.plot_config.categorical_categorical_plot_path.mkdir(parents=True,exist_ok=True)

        self.plot_config.multivariate_plot.mkdir(parents=True,exist_ok=True)


    
        fig,ax=plt.subplots(nrows=row,ncols=2,figsize=(fig_width,fig_height))
        ax=ax.flatten()
        plot_index=0
        for i,first_col in zip(range(len(num_cols)),num_cols):
            for j in range(i+1,len(cat_cols)):
                sns.barplot(data=df,x=cat_cols[j],y=first_col,ax=ax[plot_index])
                plot_index+=1
        plt.savefig(self.plot_config.numerical_numerical_plot_path/"barplot.png")
        

