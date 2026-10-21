import sys, os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from dataclasses import dataclass
from math import comb,ceil
from src.exception import CustomException
from src.logger import logging



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

        try:
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
                for k in range(len(num_cols), len(ax)):
                    fig.delaxes(ax[k])
                plt.tight_layout()
                plt.savefig(self.plot_config.univariate_numerical_plot/f"{plt_names}.png")
                plt.close(fig)
        except Exception as e:
            raise CustomException(e,sys)

        
    def univariate_categorical_plot(self):

        try:

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
            for k in range(len(cat_cols), len(ax)):
                fig.delaxes(ax[k])
            plt.tight_layout()
            plt.savefig(self.plot_config.univariate_categorical_plot/f"barChart.png")
            plt.close(fig)

        except Exception as e:
            raise CustomException(e,sys)
class BivariatePlots:
    def __init__(self) -> None:
        self.plot_config=PlotConfig()


    def bivariate_numerical_vs_numerical_plot(self):

        try:


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
                for k in range(plot_index, len(ax)):
                    fig.delaxes(ax[k])
                plt.tight_layout()
                plt.savefig(self.plot_config.numerical_numerical_plot_path/f"{name}.png")
                plt.close(fig)


        except Exception as e:
            raise CustomException(e,sys)


        
    def categorical_vs_numerical(self):

        try:
            data_path=self.plot_config.root_path/"data"/"student.csv"
                
            df=pd.read_csv(data_path)
            num_cols=df.select_dtypes(include="number").columns.tolist()
            cat_cols=df.select_dtypes(include="O").columns.tolist()

            total_plots = len(num_cols) * len(cat_cols)
            if total_plots == 0:
                logging.info("No numerical or categorical columns available for categorical_vs_numerical plots.")
                return

            ncols = 2
            row = ceil(total_plots / ncols)
            fig_width = 12
            fig_height = max(4, row * 3.5)

            self.plot_config.plots_path.mkdir(parents=True,exist_ok=True)
            self.plot_config.bivariate_plot.mkdir(parents=True,exist_ok=True)
            self.plot_config.categorical_numerical_plot_path.mkdir(parents=True,exist_ok=True)

            fig,ax=plt.subplots(nrows=row,ncols=ncols,figsize=(fig_width,fig_height))
            ax=np.array(ax).flatten()
            plot_index=0
            for first_col in num_cols:
                for cat_col in cat_cols:
                    sns.barplot(data=df,x=cat_col,y=first_col,ax=ax[plot_index])
                    ax[plot_index].set_title(f"{first_col} vs {cat_col}")
                    ax[plot_index].tick_params(axis='x', rotation=45)
                    plot_index+=1

            for k in range(plot_index, len(ax)):
                fig.delaxes(ax[k])

            plt.tight_layout()
            plt.savefig(self.plot_config.categorical_numerical_plot_path/"barplot.png")
            plt.close(fig)
        
        except Exception as e:
            raise CustomException(e,sys)

class MultivariatePlots:
    def __init__(self) -> None:
        self.plot_config=PlotConfig()


    def multivariate_heatmap_pairplot(self):

        try:

            self.plot_config.plots_path.mkdir(parents=True,exist_ok=True)
                
            self.plot_config.univariate_plot.mkdir(parents=True,exist_ok=True)
            self.plot_config.univariate_numerical_plot.mkdir(parents=True,exist_ok=True)
            self.plot_config.univariate_categorical_plot.mkdir(parents=True,exist_ok=True)

            self.plot_config.bivariate_plot.mkdir(parents=True,exist_ok=True)
            self.plot_config.numerical_numerical_plot_path.mkdir(parents=True,exist_ok=True)
            self.plot_config.categorical_numerical_plot_path.mkdir(parents=True,exist_ok=True)
            self.plot_config.categorical_categorical_plot_path.mkdir(parents=True,exist_ok=True)
            
            self.plot_config.multivariate_plot.mkdir(parents=True,exist_ok=True)

            data_path=self.plot_config.root_path/"data"/"student.csv"
            df=pd.read_csv(data_path)

            corr=df.corr(numeric_only=True)
            plt.figure(figsize=(8, 6))
            sns.heatmap(corr,annot=True)
            plt.tight_layout()
            plt.savefig(self.plot_config.multivariate_plot/"heatmap.png")
            plt.close()

            pair_fig = sns.pairplot(data=df)
            pair_fig.savefig(self.plot_config.multivariate_plot/"pairplot.png")
            plt.close()


        except Exception as e:
            raise CustomException(e,sys)


            
                    