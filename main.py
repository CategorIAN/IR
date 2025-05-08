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
    if i == 1:
        file = "\\".join([os.getcwd(), "MyData", "Grads_2025SP_W_IDS.csv"])
        df = pd.read_csv(file)
        print(df_query(df))
    if i == 2:
        file = "\\".join([os.getcwd(), "MyData", "Graduate_Program_2025SP.csv"])
        df = pd.read_csv(file)
        print(df_query(df))
    if i == 3:
        file = "\\".join([os.getcwd(), "MyData", "UpdatedGrads_2025SP.csv"])
        df = pd.read_csv(file)
        print(df_query(df))
    if i == 4:
        file = "\\".join([os.getcwd(), "MyData", "Majors.csv"])
        df = pd.read_csv(file)
        print(df_query(df))

def g(i):
    X = Pell()
    if i == 1:
        print(X.readSQL(X.year_query(19)))
    if i == 2:
        print(X.readSQL(X.pell()))
    if i == 3:
        X.saveDF(X.pell(), "Pell")
    if i == 4:
        print(X.SQL_values(X.pell()))


if __name__ == '__main__':
    f(4)
