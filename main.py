from CompIntel_DB import CompIntel_DB
from Carroll_DB import Carroll_DB
from IPEDS import IPEDS


def f(i):
    if i == 1:
        DB = CompIntel_DB("Ian")
        DB.x("Number Granted Pell Aid, UG")
    if i == 2:
        DB = Carroll_DB()
        DB.executeSQL([DB.set_empty])
    if i == 3:
        X = IPEDS()
        X.g()


if __name__ == '__main__':
    f(3)
