from Reports import Reports
from IPEDS_Fall import IPEDS_Fall
from IPEDS_Spring import IPEDS_Spring

def f(i):
    X = Reports()
    if i == 1:
        X.get2021FA_CohortGraduationRate()

def g(i):
    X = IPEDS_Fall()
    if i == 1:
        X.getCount_PT_UG_Women()

def h(i):
    X = IPEDS_Spring()
    if i == 1:
        X.getCount_FT_UG_Men_original()
        X.getCount_FT_UG_Men_new1()

def x(i):
    X = IPEDS_Spring()
    Y = IPEDS_Fall()
    count_func = lambda query: f"""
    SELECT COUNT(*)
    FROM ({query}) AS X
    """
    X.print_table(count_func(X.enrolledStudents()), snapshot_term='2024FA')
    Y.print_table(count_func(Y.enrolledStudents()), snapshot_term='2025FA')


if __name__ == '__main__':
    x(1)
