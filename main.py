from Reports import Reports
from IPEDS_Fall import IPEDS_Fall

def f(i):
    X = Reports()
    if i == 1:
        X.get2021FA_CohortGraduationRate()

def g(i):
    X = IPEDS_Fall()
    if i == 1:
        X.getCompletions_380103()
        X.getCompletions_380103_DE()


if __name__ == '__main__':
    g(1)
