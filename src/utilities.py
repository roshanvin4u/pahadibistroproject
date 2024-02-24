"""Utility functions"""
import pathlib

import pandas as pd

def load_dataframe(df_path: pathlib.Path) -> pd.DataFrame:
    """Load dataframe."""
    return pd.read_excel(df_path)
