import pandas as pd
import numpy as np
from pathlib import Path
import sys, os

root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in str(sys.path):
    sys.path.insert(0, str(root_path))


import json
from src.logger import logging
from src.exception import CustomException


def check_invalid_values(df:pd.DataFrame):

    try:
        root_path = Path(__file__).resolve().parent.parent.parent
        config_path = root_path / "config"

        config_path.mkdir(parents=True, exist_ok=True)
        eda_config_path = config_path / "eda_config.json"

        with open(eda_config_path) as file_obj:
            data=json.load(file_obj)
        invalid_values=data["invalid_values"]

        if invalid_values["check_invalid_values"]:
            # invalid_columns=invalid_values["columns_with_invalid_values"]
            columns_to_replace=invalid_values   ["columns_to_replace_invalid_values"]

            for col,replace_dict in columns_to_replace.items():
                df[col]=df[col].replace(replace_dict)

        return df

    except Exception as e:
        raise CustomException(e,sys)

## Missing value tag completed
def check_null(df: pd.DataFrame):

    try:
        logging.info("STARTED CHECK NULL FUNCTION")
        root_path = Path(__file__).resolve().parent.parent.parent

        config_path = root_path / "config"

        config_path.mkdir(parents=True, exist_ok=True)

        eda_config_path = config_path / "eda_config.json"

        series = df.isna().sum()
        index = series.index

        cols = df.columns

        feature_list = []
        average_null = df.isna().mean().mean()*100
        data = {}

        ## for droping columns missing null 60% above
        for idx, col in zip(index, cols):
            logging.info("INSIDE THE LOOP")

            if series[idx] / len(df[col]) * 100 > 50:
                feature_list.append(col)

        ## dumping the key value in the missing values key
        with open(eda_config_path) as file_obj:
            data = json.load(file_obj)
            data["missing_values"]["drop_columns"] = feature_list
        with open(eda_config_path,"w") as file_obj:
            json.dump(data,file_obj,indent=4)


        ## for droping null rows
        for idx, col in zip(index, cols):
            logging.info("INSIDE THE LOOP")    

            if (
                series[idx] / len(df[col]) * 100 < 60
                and series[idx] / len(df[col]) * 100 > 25
            ):
                with open(eda_config_path) as file_obj:
                    data = json.load(file_obj)
                    data["missing_values"]["drop_rows"]=True
                with open(eda_config_path,"w") as file_obj:
                    json.dump(data,file_obj,indent=4)
            else:

                with open(eda_config_path) as file_obj:
                    data = json.load(file_obj)
                    data["missing_values"]["drop_rows"]=False
                with open(eda_config_path,"w") as file_obj:
                    json.dump(data,file_obj,indent=4)

            ## imputing null rows
            if average_null<40:

                with open(eda_config_path) as file_obj:
                    data = json.load(file_obj)
                    data["missing_values"]["impute"] = True
                with open(eda_config_path,"w") as file_obj:
                    json.dump(data,file_obj,indent=4)

    except Exception as e:
        raise CustomException(e, sys)

    

def check_data_types(df:pd.DataFrame):

    try:
        root_path = Path(__file__).resolve().parent.parent.parent
        config_path = root_path / "config"

        config_path.mkdir(parents=True, exist_ok=True)
        eda_config_path = config_path / "eda_config.json"

        with open(eda_config_path) as file_obj:
            data=json.load(file_obj)

        data_types=data["data_types"]

        for key,columns in data_types.items():
            if key=="convert_to_numeric":
                df[columns]=df[columns].astype("float64")

            if key=="convert_to_datetime":
                df[columns]=df[columns].astype("datetime64[ns]")

            if key=="convert_to_boolean":
                df[columns]=df[columns].astype("bool")

            if key=="convert_to_category":
                df[columns]=df[columns].astype("category")

        return df

        


    except Exception as e:
        raise CustomException(e,sys)

## it will be user driven --- something to implement later do not forget

## distribution tag completed
def check_distribution(df: pd.DataFrame):

    try:
        root_path = Path(__file__).resolve().parent.parent.parent
        config_path = root_path / "config"

        config_path.mkdir(parents=True, exist_ok=True)
        eda_config_path = config_path / "eda_config.json"

        num_cols = df.select_dtypes(include="number").columns

        cols_to_log_transform = df[num_cols].skew()[abs(df[num_cols].skew()>1)].index.tolist()

        highly_skew_columns=df[num_cols].skew()[abs(df[num_cols].skew()>2)].index.to_list()
        

        with open(eda_config_path) as file_obj:
            data = json.load(file_obj)
        data["distribution"]["columns_to_log_transform"] = cols_to_log_transform
        data["distribution"]["highly_skewed_columns"]=highly_skew_columns
        with open(eda_config_path, "w") as file_obj:
            json.dump(data, file_obj, indent=4)

    except Exception as e:
        raise CustomException(e, sys)



def check_constant(df: pd.DataFrame):

    try:
        root_path = Path(__file__).resolve().parent.parent.parent
        config_path = root_path / "config"

        config_path.mkdir(parents=True, exist_ok=True)
        eda_config_path = config_path / "eda_config.json"

        constant_cols = df.nunique()[df.nunique() == 1].index.tolist()

        low_variance_column=df.select_dtypes("number").var()[df.select_dtypes("number").var()<0.01].index.tolist()

        with open(eda_config_path) as file_obj:
            data = json.load(file_obj)
            data["constant_features"]["constant_columns"] = constant_cols

            data["constant_features"]["low_variance_columns"]=low_variance_column
        with open(eda_config_path, "w") as file_obj:
            json.dump(data, file_obj, indent=4)

    except Exception as e:
        raise CustomException(e, sys)


def check_outliers(df: pd.DataFrame):

    try:
        root_path = Path(__file__).resolve().parent.parent.parent
        config_path = root_path / "config"

        config_path.mkdir(parents=True, exist_ok=True)
        eda_config_path = config_path / "eda_config.json"

        numerical_columns = df.select_dtypes(include="number").columns

        outlier_columns = []
        total_outliers = 0
        for col in numerical_columns:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            IQR = q3 - q1
            upper = q3 + 1.5 * IQR
            lower = q1 - 1.5 * IQR

            lower_outliers = df[col][df[col] <= lower]
            upper_outliers = df[col][df[col] >= upper]

            total_outliers = len(lower_outliers) + len(upper_outliers)

            if total_outliers > 0:
                outlier_columns.append(col)

        with open(eda_config_path) as file_obj:
            data = json.load(file_obj)
            data["outliers"]["outlier_columns"] = outlier_columns
        with open(eda_config_path, "w") as file_obj:
            json.dump(data, file_obj, indent=4)

    except Exception as e:
        raise CustomException(e, sys)


def check_multicolinearity(df: pd.DataFrame):
    try:
        root_path = Path(__file__).resolve().parent.parent.parent
        config_path = root_path / "config"

        config_path.mkdir(parents=True, exist_ok=True)
        eda_config_path = config_path / "eda_config.json"

        corr_matrix = df.corr(numeric_only=True).abs()

        # Upper triangle
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

        # Features to drop
        threshold = 0.9
        to_drop = [col for col in upper.columns if any(upper[col] > threshold)]

        with open(eda_config_path) as file_obj:
            data = json.load(file_obj)
            data["correlation"]["highly_correlated_columns"] = to_drop
            data["correlation"]["correlation_threshold"]=threshold
        with open(eda_config_path, "w") as file_obj:
            json.dump(data, file_obj, indent=4)

    except Exception as e:
        raise CustomException(e, sys)


def check_categorical_encoding(df:pd.DataFrame):
    try:

        root_path = Path(__file__).resolve().parent.parent.parent
        config_path = root_path / "config"

        config_path.mkdir(parents=True, exist_ok=True)
        eda_config_path = config_path / "eda_config.json"   

        with open(eda_config_path) as file_obj:
            data=json.load(file_obj)
        ordinal_category_orders=data["categorical_encoding"]["ordinal_category_orders"]
        target_column=data["categorical_encoding"]["target_column"]

        for order in ordinal_category_orders:

            df[order[0]]=df.replace(order[1])

        if target_column:
            df[target_column]=df[target_column].replace(data["categorical_encoding"]["target_encoding_columns"])

        return df

    except Exception as e:
        raise CustomException(e,sys)


def check_duplicates(df:pd.DataFrame):
    try:
        root_path = Path(__file__).resolve().parent.parent.parent
        config_path = root_path / "config"

        config_path.mkdir(parents=True, exist_ok=True)
        eda_config_path = config_path / "eda_config.json"

        is_duplicated=df.duplicated().sum()
        if is_duplicated:
            df.drop_duplicates(inplace=True)

        return df

    except Exception as e:
        raise CustomException(e,sys)


