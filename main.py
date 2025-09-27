from Reports import Reports
from IPEDS_Fall import IPEDS_Fall
from IPEDS_Spring import IPEDS_Spring

def f(i):
    X = Reports()
    if i == 1:
        X.getChangeMajor()



def h(i):
    X = IPEDS_Spring()
    Y = IPEDS_Fall()
    agg = lambda query: f"""
    SELECT COUNT(*)
    FROM ({query}) AS X
    """
    names = lambda query: f"""
    SELECT FIRST_NAME, LAST_NAME, X.*
    FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
    ORDER BY LAST_NAME, FIRST_NAME
    """
    df1 = X.db_table(names(X.enrolledStudents(level='UG', load='FT', gender='M')), snapshot_term="2024FA")
    df1.to_csv("x.csv")
    df2 = Y.db_table(names(Y.enrolledStudents(level='UG', load='FT', gender='M')), snapshot_term="2025FA")
    df2.to_csv("y.csv")
    query = f"""
    SELECT *
    FROM ({X.df_query(df1)}) AS X
    EXCEPT 
    SELECT *
    FROM ({Y.df_query(df2)}) AS Y
    """
    df3 = X.db_table(query, snapshot_term="2025FA")
    df3.to_csv("z.csv")
    query = f"""
    SELECT Z.*,
            STC_CRED,
            STC_STATUS,
            SCS_PASS_AUDIT,
            STC_ACAD_LEVEL,
            STV.STTR_STUDENT_LOAD,
            PERSON.GENDER
    FROM ({X.df_query(df3)}) AS Z
    JOIN STUDENT_ACAD_CRED AS STC ON Z.ID = STC.STC_PERSON_ID
    JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
    LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
    LEFT JOIN STUDENT_TERMS_VIEW STV ON STC.STC_PERSON_ID = STV.STTR_STUDENT AND STC.STC_TERM = STV.STTR_TERM
    JOIN PERSON ON Z.ID = PERSON.ID
    WHERE STC_TERM = '2024FA'
    """
    df4 = X.db_table(query, snapshot_term="2025FA")
    df4.to_csv("a.csv")

if __name__ == '__main__':
    f(1)
