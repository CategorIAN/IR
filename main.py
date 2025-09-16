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
from FVT_GE import FVT_GE
from Reports import Reports
from IPEDS_IC import IPEDS_IC
from FVT_GE_2 import FVT_GE_2

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
    X = Reports()
    if i == 1:
        X.getTermHeadcountByAthleteStatus_Pivoted()

def g(i):
    X = IPEDS_IC()
    if i == 1:
        X.getStudentEnrollment_5()
        X.getStudentEnrollment_7()
    if i == 2:
        X.getDisability_9()

def h(i):
    X = FVT_GE()
    if i == 1:
        X.getFullData()

def m(i):
    X = FVT_GE_2()
    if i == 1:
        X.big_join()
    if i == 2:
        X.match_check()
    if i == 3:
        X.create_transformed_data()
    if i == 4:
        X.getColumn_L()

if __name__ == '__main__':
    m(4)
