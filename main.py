from Reports import Reports
from IPEDS_Fall import IPEDS_Fall
from IPEDS_Spring import IPEDS_Spring
from CTFPL import CTFPL

def f(i):
    X = Reports()
    if i == 1:
        X.getMSWNewStudentPercentChange()

def g(i):
    X = CTFPL()
    if i == 1:
        X.print_table(X.value_df("School"))
    if i == 2:
        for metric in X.metrics:
            X.value_df(metric)
    if i == 3:
        X.getSTD_DF()
    if i == 4:
        X.getSchools()
    if i == 5:
        X.get_data()
    if i == 6:
        print(X.number_in_range(std_threshold = 0.03))


if __name__ == '__main__':
    g(6)
