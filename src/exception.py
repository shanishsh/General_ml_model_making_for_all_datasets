import sys,os
from pathlib import Path


def get_error_msg(error, error_detail:sys):

    _,_,exc_tb=error_detail.exc_info()

    if exc_tb is not None:
        filename=exc_tb.tb_frame.f_code.co_filename
        lineno=exc_tb.tb_lineno

    else:
        filename="unknown"
        lineno="unknown"

    return f"FILE  [{filename}\nLINE  [{lineno}]\nERROR  [{str(error)}]"


class CustomException(Exception):
    def __init__(self,error, error_detail:sys) -> None:
        super().__init__(error)
        self.custom_error_msg=get_error_msg(error,error_detail)

    def __str__(self) -> str:
        return self.custom_error_msg


if __name__=="__main__":
    try:
        a=4/0
    except Exception as e:
        raise CustomException(e,sys)