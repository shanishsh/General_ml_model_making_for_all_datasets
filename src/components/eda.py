import sys,os
from pathlib import Path

# project_root=Path(__file__).resolve().parent.parent.parent
# if str(project_root) not in sys.path:
#     sys.path.insert(0,str(project_root))


import json
from dataclasses import dataclass
import numpy as np
import pandas as pd
from src.utils import check_null
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
            df=pd.read_csv(data_path)
            
            logging.info("STARTED EDA")
            logging.info("READED THE DATA")
            train_df=pd.read_csv(train_path)

            logging.info("CALLLING - check_null - FUNCTION")
            check_null(train_df)

            plt=Plots()

            plt.univariate_plots()


        except Exception as e:
            raise CustomException(e,sys)




        