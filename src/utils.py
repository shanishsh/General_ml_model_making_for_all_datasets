import pandas as pd
import numpy as np
from pathlib import Path
import json
from src.logger import logging
from src.exception import CustomException
import sys,os


def check_null(df:pd.DataFrame):

    try:
        logging.info("STARTED CHECK NULL FUNCTION")
        root_path=Path(__file__).resolve().parent.parent

        config_path=root_path/"config"

        logging.info("CREATE CONFIG FOLDER - config")
        config_path.mkdir(parents=True,exist_ok=True)

        eda_config_path=config_path/"eda_config.json"

        logging.info("CREATING - series, index")
        series=df.isna().sum()
        index=series.index

        cols=df.columns

        feature_list=[]
        check_null_report={}
        average_null=df.isna().sum().values.mean()/df.shape[0]*100
        for idx,col in zip(index,cols):
            logging.info("INSIDE THE LOOP")
            
            if series[idx]/len(df[col])*100>50:
                feature_list.append(col)
                check_null_report["feature_null_del"]=feature_list

            if series[idx]/len(df[col])*100<60 and series[idx]/len(df[col])*100>25 and average_null>40:
                check_null_report["NULL_drop"]=average_null

            else:
                check_null_report["NULL_impute"]=True

        logging.info("CREATE -config.json")
        with open(eda_config_path,"w") as file_obj:
            json.dump(check_null_report,file_obj,indent=4)

        logging.info("LAST END")


    except Exception as e:
        raise CustomException(e,sys)

