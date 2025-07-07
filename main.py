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
    if i == 1:
        print(X.readSQL(2023)(X.value_df('Graduation Rate (4 Years)')))
    if i == 2:
        X.save_df('Graduation Rate (4 Years)', 2015, 2023)
        X.line_graph('Graduation Rate (4 Years) - 2015 to 2023.csv', percent=True)
    if i == 3:
        X.line_graph('Graduation Rate (4 Years) - 2015 to 2023.csv', percent=True)
    if i == 4:
        X.save_df_chart("Race Percentage: American Indian or Alaska Native", 2015, 2023)("line", True)
    if i == 5:
        for name in X.metrics:
            X.save_df_chart(name, 2015, 2023)("line", True)
    if i  == 6:
        X.save_data(2015, 2023)
    if i == 7:
        X.gender_df(2023)
        X.pie_charts('Gender Percentage - 2023.csv')
    if i == 8:
        X.race_df(2023)
        X.pie_charts('Race Percentage - 2023.csv')


def g(i):
    X = Null_Analysis()
    if i == 1:
        print(X.snapshotSQL('SELECT * FROM PERSON'))
    if i == 2:
        X = Null_Analysis()
        print(X.irSQL('SELECT * FROM REQUEST'))
    if i == 3:
        print(X.nulls(46))

if __name__ == '__main__':
    f(6)
