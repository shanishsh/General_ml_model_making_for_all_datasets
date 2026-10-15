from pathlib import Path
import sys,os

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from eda import Eda



class DataIngestionConfi:

    root_path=Path(__file__).resolve().parent.parent.parent

    artifact_path=root_path/"artifact"

    tain_data_path=artifact_path/"train.csv"
    test_data_path=artifact_path/"test.csv"
    raw_data_path=artifact_path/"data.csv"


class DataIngestion:
    def __init__(self) -> None:
        self.data_ingestion_config=DataIngestionConfi()

    def initiate_data_ingestion(self):

        try:
            logging.info("STARTED DATA INGESTION")

            data_path=self.data_ingestion_config.root_path/"data"/"student.csv"
            df=pd.read_csv(data_path)


            logging.info("SPLITED - TRAIN_set, TEST_set")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            logging.info("CREATING ARTIFACT FOLDER - TRAIN_PATH, TEST_PATH, DATA_PATH")
            self.data_ingestion_config.artifact_path.mkdir(parents=True,exist_ok=True)

            df.to_csv(self.data_ingestion_config.raw_data_path,header=True,index=False)
            train_set.to_csv(self.data_ingestion_config.tain_data_path,header=True,index=False)
            test_set.to_csv(self.data_ingestion_config.test_data_path,header=True,index=False)


            logging.info("RETURNING PATH - TRAIN, TEST")
            return(
                self.data_ingestion_config.tain_data_path,
                self.data_ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":

    data_ingestion=DataIngestion()

    train_path,test_path=data_ingestion.initiate_data_ingestion()


    eda=Eda()

    eda.initiate_eda(train_path)




