from CompIntel_DB import CompIntel_DB
from CompIntel_DV import CompIntel_DV
from Carroll_DB import Carroll_DB
from IPEDS import IPEDS
from DV import DV
from Nursing_Data_Analysis import Nursing_Data_Analysis
import pandas as pd


def df_query(df, cols=None):
    cols = df.columns if cols is None else cols
    query = f"""
    SELECT *
    FROM (VALUES {",\n".join([f"({", ".join([f"'{val}'" for val in df.loc[i, :]])})"
                              for i in df.index])})
    AS DF({", ".join(cols)})
    """
    return query

def f(i):
    if i == 1:
        X = Nursing_Data_Analysis()
        X.appendNurGPA()
    if i == 2:
        X = Nursing_Data_Analysis()
        X.saveAvgCumGPAs()
    if i == 3:
        X = Nursing_Data_Analysis()
        X.unpivoted()
    if i == 4:
        X = Nursing_Data_Analysis()
        X.saveAvgCumGPA_by_Course()


if __name__ == '__main__':
    f(4)
