import sys,os
from pathlib import Path
from sklearn.preprocessing import StandardScaler,OneHotEncoder,FunctionTransformer,PowerTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from dataclasses import dataclass
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging
import json
from src.utils import save_object

@dataclass
class DataTransformationConfig:

    root_path=Path(__file__).resolve().parent.parent.parent
    artifact_path=root_path/"artifact"

    preprocessor_file_obj_path=artifact_path/"preprocessor.pkl"


class DataTransformation:
    def __init__(self) -> None:
        self.data_transformation_config=DataTransformationConfig()


    def get_preprocessor_obj(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            root_path=Path(__file__).resolve().parent.parent.parent
            config_dir=root_path/"config"
            eda_config_path=config_dir/"eda_config.json"


            num_cols=train_df.select_dtypes(include="number").columns.tolist()
            cat_cols=train_df.select_dtypes(include="O").columns.tolist()

            with open(eda_config_path) as file_obj:
                data=json.load(file_obj)


            missing_values=data["missing_values"]
            

            if data["distribution"]["columns_to_log_transform"]:
                log1p_column=data["distribution"]["columns_to_log_transform"]
                num_scaler_cols=[items for items in num_cols if items not in log1p_column]
            else:  
                log1p_column=None
                num_scaler_cols=None

            

            
            if data["categorical_encoding"]["ordinal_encoding_columns"]:
                ordinal_encoding_cols=data["categorical_encoding"]["ordinal_encoding_columns"]
            else: ordinal_encoding_cols=None

            num_missing_value_pipeline=None
            cat_missing_value_pipeline=None
            log_transform_pipeline=None

            if missing_values["impute"]:
                num_missing_value_pipeline=Pipeline([
                    ("num_inputer",SimpleImputer(strategy="median"))
                ])

                cat_missing_value_pipeline=Pipeline([
                    ("cat_imputer",SimpleImputer(strategy="most_frequent"))
                ])

            if missing_values["drop_columns"]:
                train_df.drop(missing_values["drop_columns"],axis=1,inplace=True)
                test_df.drop(missing_values["drop_columns"],axis=1,inplace=True)

            if missing_values["drop_rows"]:
                train_df.dropna(inplace=True)
                test_df.dropna(inplace=True)

            if data["duplicates"]["check_duplicates"]:
                train_df.drop_duplicates(inplace=True)
                test_df.drop_duplicates(inplace=True)

            
            if log1p_column:
                log_transform_pipeline=Pipeline([
                    ("log1p",PowerTransformer(method="yeo-johnson"))
                ])

            if data["outliers"]["columns_to_remove_outliers"]:

                for col in data["outliers"]["columns_to_remove_outliers"]:
                    q1 = train_df[col].quantile(0.25)
                    q3 = train_df[col].quantile(0.75)
                    IQR = q3 - q1
                    upper = q3 + 1.5 * IQR
                    lower = q1 - 1.5 * IQR
        
                    train_df[col]=train_df[col][(train_df[col]>lower) & (train_df[col]<upper)]


                    q1 = test_df[col].quantile(0.25)
                    q3 = test_df[col].quantile(0.75)
                    IQR = q3 - q1
                    upper = q3 + 1.5 * IQR
                    lower = q1 - 1.5 * IQR
        
                    test_df[col]=test_df[col][(test_df[col]>lower) & (test_df[col]<upper)]

            if data["correlation"]["multicollinearity_check"]:

                train_df.drop(data["correlation"]["columns_to_drop_for_multicollinearity"],axis=1,inplace=True)

                test_df.drop(data["correlation"]["columns_to_drop_for_multicollinearity"],axis=1,inplace=True)

            if ordinal_encoding_cols:
                for col in ordinal_encoding_cols:
                    ordinal_encoding_dict=data["categorical_encoding"]["ordinal_category_orders"].get(col,{})
                    train_df[col]=train_df[col].replace(ordinal_encoding_dict)
                    test_df[col]=test_df[col].replace(ordinal_encoding_dict)

            if data["categorical_encoding"]["target_encoding_columns"]:
                for target_col,target_dict in data["categorical_encoding"]["target_encoding_columns"].items():

                    train_df[target_col]=train_df[target_col].replace(target_dict)
                    test_df[target_col]=test_df[target_col].replace(target_dict)

            num_scaler_pipeline=Pipeline([
                ("scaler",StandardScaler())
            ])

            cat_oh_encoder_pipeline=Pipeline([
                ("oh",OneHotEncoder(handle_unknown="ignore"))
            ])

            preprocessor=ColumnTransformer([
                ("null_imputer",num_missing_value_pipeline,num_cols),
                ("log_1p_transform",log_transform_pipeline,log1p_column),
                ("num_scaler",num_scaler_pipeline,num_scaler_cols),
                ("cat_null_imputer",cat_missing_value_pipeline,cat_cols),
                ("cat_one_hot_encoder",cat_oh_encoder_pipeline,ordinal_encoding_cols)
            ],remainder="passthrough")

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)


    def initiate_transformation(self,train_path,test_path):

        try:
            root_path=Path(__file__).resolve().parent.parent.parent
            config_path=root_path/"config"
            eda_config_path=config_path/"eda_config.json"

            with open(eda_config_path) as file_obj:
                data=json.load(file_obj)
            
            train_path_df=pd.read_csv(train_path)
            test_path_df=pd.read_csv(test_path)


            input_train_df=train_path_df.drop(data["target_processing"]["target_column"],axis=1)
            target_train_df=train_path_df[data["target_processing"]["target_column"]]

            input_test_df=test_path_df.drop(data["target_processing"]["target_column"],axis=1)
            target_test_df=test_path_df[data["target_processing"]["target_column"]]

            preprocessor=self.get_preprocessor_obj(train_path,test_path)
            X_train_arr=preprocessor.fit_transform(input_train_df)
            X_test_arr=preprocessor.transform(input_test_df)



            X_train=np.c_[
                X_train_arr, target_train_df
            ]

            X_test=np.c_[
                X_test_arr, target_test_df
            ]

            save_object(preprocessor)


            return(
                X_train,
                X_test
            )



        except Exception as e:
            raise CustomException(e,sys)
