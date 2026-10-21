import sys,os
from pathlib import Path

project_root=Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0,str(project_root))


import json
from dataclasses import dataclass
import numpy as np
import pandas as pd
from preprocess_changer import check_null,check_distribution,check_constant,check_outliers,check_multicolinearity,check_duplicates,check_invalid_values,check_data_types,check_categorical_encoding
from src.logger import logging
from src.exception import CustomException
from src.components import plots

from data_transformation import DataTransformation
from data_ingestion import DataIngestion

@dataclass
class EdaConfig:

    root_path=Path(__file__).resolve().parent.parent.parent

    config_file_path=root_path/"config"
    eda_config_path=config_file_path/"eda_config.json"


class Eda:
    def __init__(self) -> None:
        self.eda_config=EdaConfig()

    def initiate_eda(self):

        try:
            root_path=Path(__file__).resolve().parent.parent.parent
            data_path=root_path/"data"/"student.csv"
            revised_data_path=root_path/"data"/"revised_data.csv"
            
            logging.info("STARTED EDA")
            logging.info("READED THE DATA")
            df=pd.read_csv(data_path)


            logging.info("CALLLING - check_null - FUNCTION")

            df=check_data_types(df)
            df=check_invalid_values(df)
            check_null(df)
            df=check_duplicates(df)
            check_constant(df)
            check_distribution(df)
            check_outliers(df)
            check_multicolinearity(df)
            df=check_categorical_encoding(df)


            df.to_csv(revised_data_path,header=True,index=False)

            ## some changes have to make for fureter like multivariate ------------------------
            # plt=plots.()
            plt=plots.Plots()
            plt.univariate_plots()
            plt.bivariate_plots()
            plt.multivariate_plots()
            

            #--------------


        except Exception as e:
            raise CustomException(e,sys)



if __name__=="__main__":

    
    eda=Eda()

    eda.initiate_eda()

    
    data_ingestion=DataIngestion()
    train_path,test_path=data_ingestion.initiate_data_ingestion()

    data_transformation=DataTransformation()

    data_transformation.initiate_transformation(train_path=train_path,test_path=test_path)




        