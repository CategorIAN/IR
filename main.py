from Reports import Reports
from Report import Report

def f(i):
    X = Reports()
    if i == 1:
        X.getSSEdGraduationRateByCohort()

def g(i):
    X = Reports()
    if i == 1:
        R = X.getReport(1)
        R.saveDraft(1, overwrite = False)

if __name__ == '__main__':
    f(1)
