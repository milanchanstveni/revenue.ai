import datetime
from typing import (
    BinaryIO,
    Tuple,
    List,
    Union,
    Any
)
import pandas as pd


def read_file(file_data: BinaryIO) -> Union[pd.DataFrame, None]:
    try:
        df = pd.read_csv(file_data)
    except pd.errors.ParserError:
        try:
            df = pd.read_excel(file_data)
        except Exception as e:
            print(f"Invalid file format provided: {e}")
            raise Exception("Invalid file format provided") from e
    return df


def read_url(url: str) -> Union[pd.DataFrame, None]:
    try:
        df = pd.read_csv(url)
    except pd.errors.ParserError:
        try:
            df = pd.read_excel(url)
        except Exception as e:
            print(f"Invalid url provided: {e}")
            raise Exception("Invalid file format provided") from e
    return df

