"""Utility functions"""
import pathlib

import pandas as pd

def load_dataframe(df_path: pathlib.Path, skipfirstnrows: int = 0) -> pd.DataFrame:
    """Load dataframe."""
    if df_path.suffix == ".xlsx":
        return pd.read_excel(df_path, skiprows=skipfirstnrows)
    elif df_path.suffix == ".csv":
        return pd.read_csv(df_path, skiprows=skipfirstnrows)
    else:
        raise ValueError(f"{df_path} is not xlsx/csv file.")


def load_text(file_path: pathlib.Path):
    """Load text file."""
    file_contents = ""
    with open(file_path, "r") as file:
        file_contents = file.read()
    file_contents = file_contents.replace("\n", ";")
    return file_contents