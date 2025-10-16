from Reports import Reports
from Report import Report

def f(i):
    X = Reports()
    if i == 1:
        X.getSSEdTermHeadcountByAthleteStatus_Percent()

def g(i):
    X = Reports()
    if i == 1:
        R = X.getReport(10)
        R.saveDraft(3, overwrite = True)

if __name__ == '__main__':
    g(1)
