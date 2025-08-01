from CompIntel_DB import CompIntel_DB
from CompIntel_DV import CompIntel_DV
from Carroll_DB import Carroll_DB
from IPEDS import IPEDS
from DV import DV
from Nursing_Data_Analysis import Nursing_Data_Analysis
import pandas as pd
import numpy as np
import os
from Pell import Pell
from Null_Analysis import Null_Analysis
from ConsumerReports import ConsumerReports
from IPEDS_DB import IPEDS_DB

def df_query(df, cols  = None):
    cols = df.columns if cols is None else cols
    query = f"""
    SELECT *
    FROM (VALUES {",\n".join([f"({", ".join([f"'{str(val).replace("'", "''")}'" for val in df.loc[i, :]])})"
                              for i in df.index])})
    AS DF({", ".join([str(col).replace(" ", "_").replace(":", "") for col in cols])})
    """.replace("'nan'", "NULL")
    return query

def f(i):
    X = IPEDS_DB("NWCCU")
    if i == 4:
        X.adjusted_charts_all()
    if i == 5:
        X.save_dfs_line_charts_all(2015, 2023, make_df=True)
    if i == 6:
        X.save_dfs_gsb_charts_all(2015, 2023, make_df=False)
    if i == 7:
        X.make_all_dfs_charts(2015, 2023, make_df=True)
    if i == 8:
        X.adjusted_charts_all(False)


if __name__ == '__main__':
    f(7)
