import os
import pandas as pd
import pyodbc, environ
from pathlib import Path
from tabulate import tabulate
BASE_DIR = Path(__file__).resolve()


class Reports:
    def __init__(self):
        pass
#=============Helper Functions==========================================================================================
    '''
    I need to transform MSSQL query into pandas dataframe.
    '''
    def queried_df(self, cursor, query, index_col = False):
        '''
        :param cursor: Cursor for the database connection.
        :param query: String that is the MSSQL query.
        :param index_col: Boolean for the
        :return: Pandas DataFrame representing the table generated from the query.
        '''
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        df = pd.DataFrame(data=data, columns=columns)
        return df.set_index(columns[0]) if index_col else df

    '''
    I need to connect to a database to generate a Pandas DataFrame.
    '''
    def db_table(self, query, db = 'MSSQL', snapshot_term = None):
        '''
        :param db: The database I need to connect to.
        :param query: The query used for the database.
        :return: Pandas Dataframe to generate for the query.
        '''
        try:
            env = environ.Env()
            db_name = env(f'{db}_NAME') if snapshot_term is None else f"{snapshot_term}_SNAPSHOT"
            environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
            my_str = (
                f"DRIVER={{{env(f'{db}_DRIVER')}}};"
                f"SERVER={env(f'{db}_HOST')};"
                f"DATABASE={db_name};"
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
            print("Connection Closed")

    '''
    I need a way to pretty print the table.
    '''
    def print_table(self, query, db='MSSQL', snapshot_term = None):
        '''
        :param db: The database I need to connect to.
        :param query: The query used for the database.
        :return: None
        :side effect: Prints the table generated from the query.
        '''
        df = self.db_table(query, db, snapshot_term)
        print(tabulate(df.head(1000), headers='keys', tablefmt='psql'))

    '''
    I need a way to transform a dataframe into SQL query.
    '''
    def df_query(self, df, cols=None):
        cols = df.columns if cols is None else cols
        query = f"""
        SELECT *
        FROM (VALUES {",\n".join([f"({", ".join([f"'{str(val).replace("'", "''")}'" for val in df.loc[i, cols]])})"
                                  for i in df.index])})
        AS DF({", ".join([f'[{col}]' for col in cols])})
        """.replace("'nan'", "NULL")
        return query

    '''
    I want a fast way to save my data.
    '''
    def save_query_results(self, query, db='MSSQL', snapshot_term = None):
        folder_1a = ["Q:", "IR", "Reports"]
        folder_1b = ["Reports 2024-25 AY", "Data Provided Grouped By Request"]
        folder_1 = folder_1a + folder_1b
        def f(report, name):
            folder_2 = [report, name]
            folder = folder_1 + folder_2
            folder_path = "\\".join(folder)
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            df = self.db_table(query, db, snapshot_term)
            df.to_csv(os.path.join(folder_path, f"{name}.csv"))
            with open(os.path.join(folder_path, f"{name}.txt"), "w") as text_file:
                text_file.write(query)
        return f


#==================Reports==============================================================================================
    '''
    ID: Unknown
    Name: 2025-09-02-Snapshot Calculations
    Person: Rebecca Schwartz
    Start Date: 2025-09-02
    Due Date: 2025-09-03
    Description: 
        Need a bunch of calculations at the beginning of the 2025FA snapshot. First, we will calculate them in 
        the 2024FA snapshot. We need to calculate:
        1. Every unique student name (in 2024FA & 2025FA) in terms of their ID, First Name, Last Name, Program, Student 
            Type, and Gender.
        2. Same as (1.) except only students for Credit.
        3. Fall-to-Fall Retention. We first will look at 2023FA to 2024FA, but then we will look at 2024FA to 2025FA. 
        4. A list of students that are new to Carroll according to Student ID and Student Type
    '''

    '''
    I need every unique student name (in 2024FA) in terms of their ID, First Name, Last Name, Program, Student 
    Type, and Gender.
    
    Status: Complete
    '''
    def getStudentNames(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        FIRST_NAME,
                        LAST_NAME,
                        COALESCE(SP.PROGRAM, 'Unknown') AS PROGRAM,
                        ST.STUDENT_TYPE AS TYPE,
                        PERSON.GENDER
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN PERSON ON STC.STC_PERSON_ID = PERSON.ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        LEFT JOIN (
            SELECT STUDENTS_ID,
                    STT_DESC AS STUDENT_TYPE,
                    ROW_NUMBER() OVER (PARTITION BY STUDENTS_ID ORDER BY STU_TYPE_DATES DESC) AS RANK
            FROM STU_TYPE_INFO
            JOIN STUDENT_TYPES ON STU_TYPES = STUDENT_TYPES_ID
        ) AS ST ON STC_PERSON_ID = STUDENTS_ID AND ST.RANK = 1
        WHERE STC_TERM = '2024FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        --(End 1)-------------------------------------------------------------------------------------------------------
        ORDER BY LAST_NAME, FIRST_NAME
        """
        self.print_table(query)
        report = "2025-09-02-Snapshot Calculations"
        name = "Student Names"
        self.save_query_results(query)(report, name)

    '''
    I need every unique student name (in 2024FA) in terms of their ID, First Name, Last Name, Program, Student 
    Type, and Gender. They need to be taking at least one credit.

    Status: Complete
    '''
    def getForCreditStudents(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        FIRST_NAME,
                        LAST_NAME,
                        COALESCE(SP.PROGRAM, 'Unknown') AS PROGRAM,
                        ST.STUDENT_TYPE AS TYPE,
                        PERSON.GENDER
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN PERSON ON STC.STC_PERSON_ID = PERSON.ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        LEFT JOIN (
            SELECT STUDENTS_ID,
                    STT_DESC AS STUDENT_TYPE,
                    ROW_NUMBER() OVER (PARTITION BY STUDENTS_ID ORDER BY STU_TYPE_DATES DESC) AS RANK
            FROM STU_TYPE_INFO
            JOIN STUDENT_TYPES ON STU_TYPES = STUDENT_TYPES_ID
        ) AS ST ON STC_PERSON_ID = STUDENTS_ID AND ST.RANK = 1
        WHERE STC_TERM = '2024FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        -----For Credit--------------
        AND STC.STC_CRED > 0
        --(End 1)-------------------------------------------------------------------------------------------------------
        ORDER BY LAST_NAME, FIRST_NAME
        """
        self.print_table(query)
        report = "2025-09-02-Snapshot Calculations"
        name = "For Credit Student Names"
        self.save_query_results(query)(report, name)

    '''
    I need to calculate the 2023FA to 2024FA retention rate.
    
    Status: Complete
    '''
    def fallToFallRetention(self):
        cohort_query = f"""
        SELECT DISTINCT APPL_APPLICANT     AS ID,
        APPL_START_TERM                    AS TERM
        FROM APPLICATIONS AS AP
        JOIN STUDENT_ACAD_CRED AS STC
        ON AP.APPL_APPLICANT = STC.STC_PERSON_ID AND AP.APPL_START_TERM = STC.STC_TERM
        LEFT JOIN STC_STATUSES AS STAT ON STC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
        LEFT JOIN STUDENT_TERMS_VIEW AS STV ON AP.APPL_APPLICANT = STV.STTR_STUDENT AND APPL_START_TERM = STV.STTR_TERM
        WHERE APPL_DATE IS NOT NULL
        AND STC_STATUS IN ('A', 'N')
        AND STC_CRED_TYPE = 'INST'
        -------FFUG-------------------
        AND APPL_ADMIT_STATUS = 'FY' --First Time--
        AND STV.STTR_STUDENT_LOAD = 'F'  --Full Time--
        AND APPL_STUDENT_TYPE = 'UG'   --Undergraduate--
        ------TERM---------------------
        AND APPL_START_TERM = '2023FA'
        """
        cohort_df = self.db_table(cohort_query, snapshot_term = "2023FA")
        query = f"""
        --(Begin 3)----------------------------------------------------------------------------------------------------
        SELECT FORMAT(AVG(1.0 * FFUG_RETAINED), 'P') AS FFUG_RETENTION
        FROM (
        --(Begin 2)----------------------------------------------------------------------------------------------------
        SELECT ID,
                CASE WHEN EXISTS (SELECT 1
                    FROM STUDENT_ACAD_CRED AS STC
                    JOIN STC_STATUSES AS STAT ON STC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                    WHERE STC_STATUS IN ('A', 'N')
                    AND STC_TERM = '2024FA'
                    AND STC_PERSON_ID = COHORT_2023FA.ID
                    ) THEN 1 ELSE 0 END AS FFUG_RETAINED
        FROM 
        --(Begin 1)----------------------------------------------------------------------------------------------------
        ({self.df_query(cohort_df)})
        --(End 1)------------------------------------------------------------------------------------------------------
        AS COHORT_2023FA
        --(End 2)------------------------------------------------------------------------------------------------------
        ) AS X
        --(End 3)------------------------------------------------------------------------------------------------------
        """
        self.print_table(query, snapshot_term = '2024FA')
        report = "2025-09-02-Snapshot Calculations"
        name = "Fall to Fall Retention"
        self.save_query_results(query, snapshot_term = '2024FA')(report, name)

    '''
    I need a list of students that are new to Carroll according to Student ID and Student Type.
    
    Status: Complete
    '''
    def newToCarroll(self):
        query = f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT ID,
               TYPE,
               TERM
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                 SELECT DISTINCT APPL_APPLICANT                                                                              AS ID,
                                 STUDENT_TYPES.STT_DESC AS TYPE,
                                 APPL_START_TERM                                                                             AS TERM,
                                 ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT, APPL_STUDENT_TYPE ORDER BY TERM_START_DATE) AS RANK
                 FROM APPLICATIONS AS AP
                          JOIN STUDENT_ACAD_CRED AS AC
                               ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                          JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                          JOIN STUDENT_TERMS_VIEW AS STV
                               ON AP.APPL_APPLICANT = STV.STTR_STUDENT AND APPL_START_TERM = STV.STTR_TERM
                          JOIN TERMS ON APPL_START_TERM = TERMS_ID
                           LEFT JOIN STUDENT_TYPES ON APPL_STUDENT_TYPE = STUDENT_TYPES_ID
                 WHERE APPL_DATE IS NOT NULL
                   AND STC_STATUS IN ('A', 'N')
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        WHERE RANK = 1
        AND TERM IN ('2024FA', '2024SU')
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY TERM, TYPE
        """
        self.print_table(query, snapshot_term = '2024FA')
        report = "2025-09-02-Snapshot Calculations"
        name = "New Students According To ID and Type"
        self.save_query_results(query, snapshot_term = '2024FA')(report, name)




