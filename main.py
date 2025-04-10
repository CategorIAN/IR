from CompIntel_DB import CompIntel_DB
from CompIntel_DV import CompIntel_DV
from Carroll_DB import Carroll_DB
from IPEDS import IPEDS
from DV import DV
from Nursing_Data_Analysis import Nursing_Data_Analysis

def f(i):
    if i == 1:
        X = Nursing_Data_Analysis()
        X.save_cleaned_data()


if __name__ == '__main__':
    f(1)
