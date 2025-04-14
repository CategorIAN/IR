from CompIntel_DB import CompIntel_DB
from CompIntel_DV import CompIntel_DV
from Carroll_DB import Carroll_DB
from IPEDS import IPEDS
from DV import DV
from Nursing_Data_Analysis import Nursing_Data_Analysis

def f(i):
    if i == 1:
        X = Nursing_Data_Analysis()
        X.save_cleaned_data_2()
    if i == 2:
        X = Nursing_Data_Analysis()
        cols = ['TIMESTAMP',
                    'EMAIL',
                    'BI_201',
                    'BI_202',
                    'CH_111',
                    'CH_112',
                    'BI_214',
                    'NAME']
        print(X.readSQL(X.df_query(X.responses, cols)))
    if i == 3:
        X = Nursing_Data_Analysis()
        for course in ['BI_201', 'BI_202', 'CH_111', 'CH_112', 'BI_214']:
            X.avgCumGPA(course)


if __name__ == '__main__':
    f(3)
