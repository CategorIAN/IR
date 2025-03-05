from CompIntel_DB import CompIntel_DB
from Carroll_DB import Carroll_DB


def f(i):
    if i == 1:
        DB = CompIntel_DB("Ian")
        DB.x("Number Granted Pell Aid, UG")
    if i == 2:
        DB = Carroll_DB()
        DB.executeSQL([DB.set_empty])
    if i == 3:
        DB = Carroll_DB()
        DB.executeSQL([DB.insert_rows4])


if __name__ == '__main__':
    f(3)
