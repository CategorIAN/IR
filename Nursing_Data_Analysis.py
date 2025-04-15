import pandas as pd
import os
import pyodbc, environ
from pathlib import Path
BASE_DIR = Path(__file__).resolve()

class Nursing_Data_Analysis:
    def __init__(self):
        self.folder = "\\".join([os.getcwd(), "NursingDataAnalysis", "Data"])
        path = os.path.join(self.folder, "Survey Responses.csv")
        self.responses = pd.read_csv(path)
        self.courses = ['BI_201', 'BI_202', 'CH_111', 'CH_112', 'BI_214']
        self.cols = ['ID'] + self.courses
        self.data = pd.read_csv(os.path.join(self.folder, "Cleaned_Survey_Data.csv"), index_col = 0)
        self.data_flat = pd.read_csv(os.path.join(self.folder, "Cleaned_Survey_Data_Unpivoted.csv"), index_col = 0)
    #============================================Begin Preliminary======================================================
    def save_cleaned_data(self):
        cols = ['TIMESTAMP', 'EMAIL','BI_201','BI_202','CH_111','CH_112','BI_214','NAME']
        responses = f"""
        SELECT EMAIL, BI_201, BI_202, CH_111, CH_112, BI_214
        FROM (
        SELECT *,
                ROW_NUMBER() OVER (PARTITION BY EMAIL ORDER BY CONVERT(DATETIME, TIMESTAMP) DESC) AS TIME_RANK
        FROM ({self.df_query(self.responses, cols)}) AS RESPONSES
        ) AS RANKED
        WHERE TIME_RANK = 1
        """
        query = f"""
        SELECT DISTINCT P.ID, BI_201, BI_202, CH_111, CH_112, BI_214
        FROM ({responses}) AS R
        JOIN PEOPLE_EMAIL ON R.EMAIL = PEOPLE_EMAIL.PERSON_EMAIL_ADDRESSES
        JOIN PERSON AS P ON PEOPLE_EMAIL.ID = P.ID
        WHERE P.ID NOT IN ('6181895', '6188540')
        """
        df = self.readSQL(query)
        df.to_csv(os.path.join(self.folder, "Cleaned_Survey_Data.csv"))

    def unpivoted(self):
        query = f"""
        SELECT ID, COURSE, MODE
        FROM ({self.df_query(self.data)}) AS DF
        UNPIVOT ( MODE FOR COURSE IN ({", ".join(self.courses)}) ) AS X
        """
        df = self.readSQL(query)
        df.to_csv(os.path.join(self.folder, 'Cleaned_Survey_Data_Unpivoted.csv'))
    #============================================End Preliminary======================================================
    def df_query(self, df, cols = None):
        cols = df.columns if cols is None else cols
        query = f"""
        SELECT *
        FROM (VALUES {",\n".join([f"({", ".join([f"'{val}'" for val in df.loc[i, :]])})"
                                  for i in df.index])})
        AS DF({", ".join(cols)})
        """
        return query

    def SQL_values(self, query):
        df = self.readSQL(query)
        return self.df_query(df)

    def get_survey_data(self):
        return self.df_query(self.data_flat)

    def saveAvgCumGPA_by_Course(self):
        query = f"""
        SELECT COURSE,
                MODE,
                COUNT(*) AS STUDENT_COUNT,
                AVG(NURSING_GPA) AS AVG_NURSING_GPA
        FROM (
        SELECT ID,
               COURSE,
               MODE,
                SUM(ENROLL_CUM_CONTRIB_GRADE_POINTS) / SUM(ENROLL_GPA_CREDITS) AS NURSING_GPA
        FROM (
        SELECT ID, COURSE, MODE, ENROLL_GPA_CREDITS, ENROLL_CUM_CONTRIB_GRADE_POINTS
        FROM ({self.get_survey_data}) AS DF
        JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON DF.ID = SEV.STUDENT_ID
        WHERE SECTION_DEPARTMENT1 = 'NUR'
        AND ENROLL_GPA_CREDITS IS NOT NULL
        ) AS X
        GROUP BY ID, COURSE, MODE
        ) AS X
        GROUP BY COURSE, MODE
        ORDER BY COURSE, MODE
        """
        self.saveDF(query, "Avg_GPA_by_Course")

    def saveAvgProgramDuration_by_Course(self, program):
        query = f"""
        SELECT COURSE,
                MODE,
                COUNT(*) AS GRADUATED_STUDENT_COUNT,
                AVG(MONTHS_TO_GRADUATE_PROGRAM) AS AVG_MONTHS_TO_GRADUATE
        FROM (
        SELECT ID,
                COURSE,
                MODE,
                DATEDIFF(MONTH, STP_START_DATE, STP_END_DATE) AS MONTHS_TO_GRADUATE_PROGRAM
        FROM ({self.get_survey_data()}) AS DF
        JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV ON SAPV.STUDENT_ID = DF.ID
        WHERE STP_END_DATE IS NOT NULL
        AND STP_CURRENT_STATUS = 'Graduated'
        AND STP_PROGRAM_TITLE = '{program}'
        ) AS X
        GROUP BY COURSE, MODE
        ORDER BY COURSE, MODE
        """
        self.saveDF(query, f"Avg_Months_To_Graduate_Program_{program}")


#=======================================================================================================================
    def students(self):
        query = f"""
        SELECT DISTINCT ID
        FROM ({self.get_survey_data()}) AS DF
        """
        return query

    def NurGPA(self):
        query = f"""
        SELECT ID AS X, 
            SUM(ENROLL_CUM_CONTRIB_GRADE_POINTS) / SUM(ENROLL_GPA_CREDITS) AS Y
        FROM (
        SELECT ID, ENROLL_GPA_CREDITS, ENROLL_CUM_CONTRIB_GRADE_POINTS
        FROM ({self.get_survey_data()}) AS DF
        JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON DF.ID = SEV.STUDENT_ID
        WHERE SECTION_DEPARTMENT1 = 'NUR'
        AND ENROLL_GPA_CREDITS IS NOT NULL
        ) AS X
        GROUP BY ID
        """
        return query

#=======================================================================================================================
    def join_table_dict(self, feature):
        if feature == 'NURSE_GPA': return self.NurGPA()

    def table(self, features):
        query = f"""
        SELECT ID, 
               {",\n               ".join([f"{feature}_TABLE.Y AS {feature}" for feature in features])}
        FROM ({self.students()}) AS STUDENTS
        {"\n        ".join([f"JOIN ({self.join_table_dict(feature)}) AS {feature}_TABLE ON ID = {feature}_TABLE.X"
                    for feature in features])}
        """
        return query

    def filtered(self, x, filter_by):
        query = f"""
        SELECT *
        FROM ({x}) AS STUDENTS
        WHERE {"\nAND ".join([f"{k} = '{v}'" for k, v in filter_by.items()])}
        """
        return query

    def scratch(self):
        query = f"""
        SELECT DF.ID, SAPV.*
        FROM ({self.students()}) AS DF
        JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV ON DF.ID = SAPV.STUDENT_ID
        """
        return query

    def queried_df(self, cursor, query):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        return pd.DataFrame(data=data, columns=columns)

    def readSQL(self, query):
        try:
            env = environ.Env()
            environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
            my_str = (
                f"DRIVER={{{env('DATABASE_DRIVER')}}};"
                f"SERVER={env('DATABASE_HOST')};"
                f"DATABASE={env('DATABASE_NAME')};"
                "Trusted_Connection=yes;"
            )
            connection = pyodbc.connect(my_str)
            cursor = connection.cursor()
            return self.queried_df(cursor, query)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
            print("MSSQL Connection Closed")

    def saveDF(self, query, name, save_sql = True):
        df = self.readSQL(query)
        df.to_csv(os.path.join(self.folder, f'{name}.csv'))
        if save_sql:
            with open(os.path.join(self.folder, f'{name}.txt'), "w", encoding="utf-8") as file:
                file.write(query)
