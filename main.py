from Reports import Reports
from Report import Report
from CTFPL import CTFPL

def f(i):
    X = Reports()
    if i == 1:
        X.getSSEdSpecials()

def g(i):
    X = Reports()
    if i == 1:
        R = X.getReport(11)
        R.saveDraft(2, overwrite = True)

def h(i):
    X = CTFPL()
    if i == 1:
        X.getNeighborSchools()
    if i == 2:
        X.makeSTDCorrelation(0, 1)
    if i == 3:
        X.get_data()

if __name__ == '__main__':
    g(1)
