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
    X = Nursing_Data_Analysis()
    if i == 2:
        print(X.readSQL(X.get_survey_data()))
    if i == 3:
        X.saveDF(X.scratch(), "scratch")
    if i == 4:
        print(X.SQL_values(X.students()))
    if i == 5:
        X.saveAvgProgramDuration_by_Course('Nursing')
        X.saveAvgProgramDuration_by_Course('Accelerated Nursing')


if __name__ == '__main__':
    f(5)
