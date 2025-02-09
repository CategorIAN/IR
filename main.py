from CompIntel_DV import CompIntel_DV
from CompIntel_DB import CompIntel_DB
import pandas as pd


def f(i):
    if i == 1:
        DB = CompIntel_DB("Ian")
        DB.x("Board Charges")

if __name__ == '__main__':
    f(1)
