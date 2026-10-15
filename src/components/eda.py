import sys,os
from pathlib import Path

# project_root=Path(__file__).resolve().parent.parent.parent
# if str(project_root) not in sys.path:
#     sys.path.insert(0,str(project_root))


import json
from dataclasses import dataclass
import numpy as np
import pandas as pd
from preprocess_changer import check_null,check_skew,check_constant,check_outliers,check_multicolinearity
from src.logger import logging
from src.exception import CustomException
from plots import Plots

@dataclass
class EdaConfig:

    root_path=Path(__file__).resolve().parent.parent.parent

    config_file_path=root_path/"config"
    eda_config_path=config_file_path/"eda_config.json"


class Eda:
    def __init__(self) -> None:
        self.eda_config=EdaConfig()

    def initiate_eda(self,train_path):

        try:
            root_path=Path(__file__).resolve().parent.parent.parent
            data_path=root_path/"data"/"student.csv"
            
            logging.info("STARTED EDA")
            logging.info("READED THE DATA")
            df=pd.read_csv(data_path)


            logging.info("CALLLING - check_null - FUNCTION")
            check_null(df)
            check_skew(df)
            check_constant(df)
            check_outliers(df)
            check_multicolinearity(df)

            ## some changes have to make for fureter like multivariate ------------------------
            plt=Plots()
            plt.univariate_plots()
            plt.bivariate_plots()
            

            #--------------
            





        except Exception as e:
            raise CustomException(e,sys)




        