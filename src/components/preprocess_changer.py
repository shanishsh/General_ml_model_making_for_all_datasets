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
        root_path=Path(__file__).resolve().parent.parent.parent

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
        data={}
        for idx,col in zip(index,cols):
            logging.info("INSIDE THE LOOP")
            
            if series[idx]/len(df[col])*100>50:
                feature_list.append(col)
                check_null_report["feature_null_del"]=feature_list
                with open(eda_config_path) as file_obj:
                            data=json.load(file_obj)
                            data["feature_nul_del"]=feature_list
                

            if series[idx]/len(df[col])*100<60 and series[idx]/len(df[col])*100>25 and average_null>40:
                check_null_report["NULL_drop"]=average_null
                with open(eda_config_path) as file_obj:
                            data=json.load(file_obj)
                            data["NUll_drop"]=average_null
                

            else:
                check_null_report["NULL_impute"]=True
                with open(eda_config_path) as file_obj:
                            data=json.load(file_obj)
                            data["NUll_impute"]=True
                

        logging.info("CREATE -config.json")

        with open(eda_config_path,"w") as file_obj:
            json.dump(data,file_obj,indent=4)

        logging.info("LAST END")


    except Exception as e:
        raise CustomException(e,sys)


def check_skew(df:pd.DataFrame):

    try:
        root_path=Path(__file__).resolve().parent.parent.parent
        config_path=root_path/"config"

        config_path.mkdir(parents=True,exist_ok=True)
        eda_config_path=config_path/"eda_config.json"

        num_cols=df.select_dtypes(include="number").columns

        cols_to_log_transform=df[num_cols].skew()[(df[num_cols].skew()>1) | (df[num_cols].skew()<-1)].index.tolist()
        cols_to_log_transform={"Columns to log transform":cols_to_log_transform}


        with open(eda_config_path) as file_obj:
            data=json.load(file_obj)
            data["Columns_to_log_transform"]=str(list(cols_to_log_transform.values())[0])
        with open(eda_config_path,"w") as file_obj:
            json.dump(data,file_obj,indent=4)

    except Exception as e:
        raise CustomException(e,sys)