from CompIntel_DV import CompIntel_DV
from CompIntel_DB import CompIntel_DB
import pandas as pd
from Carroll_DB import Carroll_DB


def f(i):
    if i == 1:
        DB = CompIntel_DB("Ian")
        DB.x("Percent Yield")

if __name__ == '__main__':
    C = Carroll_DB()
    C.executeSQL([C.insert_rows])
