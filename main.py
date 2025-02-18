from CompIntel_DV import CompIntel_DV
from CompIntel_DB import CompIntel_DB
import pandas as pd
from Carroll_DB import Carroll_DB


def f(i):
    if i == 1:
        DB = CompIntel_DB("Ian")
        DB.x("Number Granted Pell Aid, UG")
    if i == 2:
        DB = Carroll_DB()
        str = """
                SELECT Avg([STUDENT_OVERALL_CUM_GPA]) AS AVG_CUMULATIVE_GPA,
                Avg([STUDENT_TERM_GPA]) AS AVG_TERM_GPA_2024FA
        FROM [PERSON]
        JOIN [STUDENT_CUM_GPA_VIEW] ON PERSON.ID = STUDENT_CUM_GPA_VIEW.STUDENT_ID
        JOIN [STUDENT_TERM_GPA_VIEW] ON PERSON.ID = STUDENT_TERM_GPA_VIEW.STUDENT_ID
        Left JOIN [STA_OTHER_COHORTS_VIEW] ON PERSON.ID = STA_OTHER_COHORTS_VIEW.STA_STUDENT
        WHERE STUDENT_TERM_GPA_VIEW.TERM = '2024FA' and
              (
                STA_OTHER_COHORT_GROUPS IN ('HNRS', 'FOR', 'ROTC', 'VETS', 'INTL', 'ACCESS', 'CIC', 'GRSET', 'GRSUA', 'GRSMX') OR 
                STA_OTHER_COHORT_GROUPS IS NULL OR
                STA_OTHER_COHORT_END_DATES < GETDATE()
             )
        """
        new_str = DB.flatten_script(str)
        print(len(new_str))

if __name__ == '__main__':
    f(2)
