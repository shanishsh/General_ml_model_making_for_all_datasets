import sys,os
from pathlib import Path
from src.exception import CustomException
from src.logger import logging
import pickle


def save_object(obj):

    try:
        root_path=Path(__file__).resolve().parent.parent
        artifact_path=root_path/"artifact"
        preprocessor_path=artifact_path/"preprocessor.pkl"

        with open(preprocessor_path, "wb") as file_obj:
            pickle.dump(obj,file_obj)

    except Exception as e:
        raise CustomException(e,sys)

