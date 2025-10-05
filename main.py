from Reports import Reports
from IPEDS_Fall import IPEDS_Fall
from IPEDS_Spring import IPEDS_Spring
from CTFPL import CTFPL

def f(i):
    X = Reports()
    if i == 1:
        X.getElemEdGraduationRateByCohort()

def g(i):
    X = CTFPL()
    if i == 1:
        X.print_table(X.value_df("School"))
    if i == 2:
        for metric in X.metrics:
            X.value_df(metric)
    if i == 3:
        X.makeSTDCorrelation(0, 5)
        X.makeSTDCorrelation(0, 1)
        X.makeSTDCorrelation(0, 0.1)
        X.makeSTDCorrelation(0, 0.04)
    if i == 4:
        X.getTop50Schools()



if __name__ == '__main__':
    f(1)
