import sys,os
from pathlib import Path
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from dataclasses import dataclass
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging



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

            num_cols=train_df.select_dtypes(include="number")
            cat_cols=train_df.select_dtypes(include="O")

            num_pipeline=Pipeline([
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
            ])

            cat_pipeline=Pipeline([
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("oh",OneHotEncoder(handle_unknown="ignore"))
            ])

            preprocessor=ColumnTransformer([
                ("num",num_pipeline,num_cols),
                ("cat",cat_pipeline,cat_cols)
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)