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
            df = self.queried_df(cursor, query)
            return df
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
    def save_query_results(self, query, func_dict = None, db='MSSQL', snapshot_term = None):
        folder_1a = ["Q:", "IR", "Reports"]
        folder_1b = ["Reports 2024-25 AY", "Data Provided Grouped By Request"]
        folder_1 = folder_1a + folder_1b
        def f(report, name):
            folder_2 = [report, name]
            folder = folder_1 + folder_2
            folder_path = "\\".join(folder)
            code_folder_path = "\\".join(folder_1 + [report, "[Code]"])
            agg_folder_path = "\\".join(folder_1 + [report, "[Reports (Agg)]"])
            names_folder_path = "\\".join(folder_1 + [report, "[Reports (Names)]"])
            for path in [folder_path, code_folder_path, agg_folder_path, names_folder_path]:
                Path(path).mkdir(parents=True, exist_ok=True)
            if func_dict is None:
                df = self.db_table(query, db, snapshot_term)
                print(tabulate(df.head(1000), headers='keys', tablefmt='psql'))
                df.to_csv(os.path.join(folder_path, f"{name}.csv"))
                with open(os.path.join(folder_path, f"{name}.txt"), "w") as text_file:
                    text_file.write(query)
            else:
                for key in func_dict:
                    transformed_query = func_dict[key](query)
                    df = self.db_table(transformed_query, db, snapshot_term)
                    print(tabulate(df.head(1000), headers='keys', tablefmt='psql'))
                    df.to_csv(os.path.join(folder_path, f"{name} ({key}).csv"))
                    with open(os.path.join(folder_path, f"{name} ({key}).txt"), "w") as text_file:
                        text_file.write(transformed_query)
                    with open(os.path.join(code_folder_path, f"{name} ({key}).txt"), "w") as text_file:
                        text_file.write(transformed_query)
                    if key == "Agg":
                        df.to_csv(os.path.join(agg_folder_path, f"{name}.csv"))
                    if key == "Names":
                        df.to_csv(os.path.join(names_folder_path, f"{name}.csv"))
        return f


#==================Reports==============================================================================================
    '''
    ID: Unknown
    Name: 2025-02-13-Current Student List By Major and Minor
    Start Date: 2025-02-13
    End Date:  2025-02-20
    Description:
        I needed to get a list of students and their majors/minors.
    '''
    def getStudentMajors(self):
        query = f"""
        SELECT CURRENT_MAJORS.MAJ_DESC AS MAJOR,
               STUDENT_ID
        FROM MAJORS AS CURRENT_MAJORS
        CROSS JOIN (SELECT * FROM STUDENT_ACAD_PROGRAMS_VIEW WHERE STP_CURRENT_STATUS = 'Active') AS SAPV
        LEFT JOIN STPR_MAJOR_LIST_VIEW ON SAPV.STUDENT_ID = STPR_MAJOR_LIST_VIEW.STPR_STUDENT 
        AND SAPV.STP_ACADEMIC_PROGRAM = STPR_MAJOR_LIST_VIEW.STPR_ACAD_PROGRAM
        LEFT JOIN MAJORS AS ADDNL_MAJOR ON STPR_MAJOR_LIST_VIEW.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
        LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
        WHERE (
                CURRENT_MAJORS.MAJ_DESC = MAIN_MAJOR.MAJ_DESC
        OR (
            CURRENT_MAJORS.MAJ_DESC = ADDNL_MAJOR.MAJ_DESC
            AND STPR_MAJOR_LIST_VIEW.STPR_ADDNL_MAJOR_END_DATE IS NULL
            )
        )
        AND STP_START_DATE < '2025-05-01'
        GROUP BY CURRENT_MAJORS.MAJ_DESC, STUDENT_ID, STP_START_DATE
        """
        agg = lambda query: f"""
        SELECT MAJOR,
                COUNT(*) AS STUDENT_COUNT
        FROM ({query}) AS STUDENT_MAJORS GROUP BY MAJOR ORDER BY MAJOR
        """
        names = lambda query: f"""
        SELECT STUDENT_ID,
        LAST_NAME,
        FIRST_NAME,
        PERSON_EMAIL_ADDRESSES AS EMAIL,
        MAJOR
        FROM ({query}) AS STUDENT_MAJORS
        JOIN PERSON ON STUDENT_MAJORS.STUDENT_ID = PERSON.ID
        JOIN PEOPLE_EMAIL ON STUDENT_MAJORS.STUDENT_ID = PEOPLE_EMAIL.ID
        WHERE PERSON_PREFERRED_EMAIL = 'Y'
        ORDER BY MAJOR, LAST_NAME, FIRST_NAME
        """
        report = "2025-02-13-Current Student List By Major and Minor"
        name = "Current Students By Major"
        self.save_query_results(query, func_dict={"Agg": agg, "Names": names}, snapshot_term="2025SP")(report, name)

    def getStudentMinors(self):
        query = f"""
        SELECT CURRENT_MINORS.MINORS_DESC AS MINOR,
        STUDENT_ID
		FROM MINORS AS CURRENT_MINORS
		CROSS JOIN (SELECT * FROM STUDENT_ACAD_PROGRAMS_VIEW WHERE STP_CURRENT_STATUS = 'Active') AS SAPV
		LEFT JOIN STPR_MINOR_LIST_VIEW ON SAPV.STUDENT_ID = STPR_MINOR_LIST_VIEW.STPR_STUDENT 
		    AND SAPV.STP_ACADEMIC_PROGRAM = STPR_MINOR_LIST_VIEW.STPR_ACAD_PROGRAM
		LEFT JOIN MINORS AS ADDED_MINOR ON STPR_MINOR_LIST_VIEW.STPR_MINORS = ADDED_MINOR.MINORS_ID
		WHERE 
		CURRENT_MINORS.MINORS_DESC = ADDED_MINOR.MINORS_DESC
		AND STPR_MINOR_LIST_VIEW.STPR_MINOR_END_DATE IS NULL
		GROUP BY CURRENT_MINORS.MINORS_DESC, STUDENT_ID
        """
        agg = lambda query: f"""
        SELECT MINOR, COUNT(*) AS STUDENT_COUNT FROM ({query}) AS STUDENT_MINORS GROUP BY MINOR ORDER BY MINOR
        """
        names = lambda query: f"""
        SELECT STUDENT_ID,
		LAST_NAME,
		FIRST_NAME,
		PERSON_EMAIL_ADDRESSES AS EMAIL,
		MINOR
        FROM ({query}) AS STUDENT_MINORS
        JOIN PERSON ON STUDENT_MINORS.STUDENT_ID = PERSON.ID
        JOIN PEOPLE_EMAIL ON STUDENT_MINORS.STUDENT_ID = PEOPLE_EMAIL.ID
        WHERE PERSON_PREFERRED_EMAIL = 'Y'
        ORDER BY MINOR, LAST_NAME, FIRST_NAME
        """
        report = "2025-02-13-Current Student List By Major and Minor"
        name = "Current Students By Minor"
        self.save_query_results(query, func_dict={"Agg": agg, "Names": names}, snapshot_term="2025SP")(report, name)

    def getNursingStudentsByProgram(self):
        query = f"""
        SELECT CURRENT_MAJORS.MAJ_DESC AS MAJOR,
        STUDENT_ID,
        SAPV.STP_PROGRAM_TITLE AS NURSING_PROGRAM
		FROM MAJORS AS CURRENT_MAJORS
		CROSS JOIN (SELECT * FROM STUDENT_ACAD_PROGRAMS_VIEW WHERE STP_CURRENT_STATUS = 'Active') AS SAPV
		LEFT JOIN STPR_MAJOR_LIST_VIEW ON SAPV.STUDENT_ID = STPR_MAJOR_LIST_VIEW.STPR_STUDENT AND SAPV.STP_ACADEMIC_PROGRAM = STPR_MAJOR_LIST_VIEW.STPR_ACAD_PROGRAM
		LEFT JOIN MAJORS AS ADDNL_MAJOR ON STPR_MAJOR_LIST_VIEW.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
		LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
		WHERE CURRENT_MAJORS.MAJ_DESC = 'Nursing'
		AND (
		CURRENT_MAJORS.MAJ_DESC = MAIN_MAJOR.MAJ_DESC
		OR (
			CURRENT_MAJORS.MAJ_DESC = ADDNL_MAJOR.MAJ_DESC
			AND STPR_MAJOR_LIST_VIEW.STPR_ADDNL_MAJOR_END_DATE IS NULL
			)
		)
		GROUP BY CURRENT_MAJORS.MAJ_DESC, STUDENT_ID, SAPV.STP_PROGRAM_TITLE
        """
        agg = lambda query: f"""
        SELECT NURSING_PROGRAM, COUNT(*) AS STUDENT_COUNT

        """
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    ID: Unknown
    Name: 2025-04-22-Current UG Emails
    Person: Annette Walstad
    Start Date: 2025-04-22
    Due Date: 
    End Date: 2025-04-24
    Description:
        Annette needed a list of undergraduate student emails.
    '''
    def getUGStudentEmails(self):
        query = f"""
        SELECT DISTINCT SAPV.STUDENT_ID AS ID,
                SAPV.STUDENT_LAST_NAME AS LAST_NAME,
                SAPV.STUDENT_FIRST_NAME AS FIRST_NAME,
                COALESCE(
                        (SELECT TOP 1 PERSON_EMAIL_ADDRESSES
                        FROM PEOPLE_EMAIL
                        WHERE ID = SAPV.STUDENT_ID
                        AND PERSON_EMAIL_TYPES = 'COL'), 'Unknown') AS SCHOOL_EMAIL
        FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        WHERE STP_CURRENT_STATUS = 'Active'
        AND STP_ACAD_LEVEL = 'UG'
        AND STP_PROGRAM_TITLE NOT IN ('Accelerated Nursing', 'Non-Degree Seeking Students')
        AND STP_START_DATE IS NOT NULL
        AND STP_START_DATE <= GETDATE()
        AND (STP_END_DATE IS NULL OR STP_END_DATE > GETDATE())
        AND EXISTS (
                    SELECT 1 FROM STUDENT_ENROLLMENT_VIEW AS SEV
                             WHERE SEV.STUDENT_ID = SAPV.STUDENT_ID
                             AND ENROLL_TERM = '2025SP'
                    )
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-04-22-Current UG Emails"
        name = "Current UG Emails"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    #===================================================================================================================
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
    #===================================================================================================================
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
    # ===================================================================================================================
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
    # ===================================================================================================================
    '''
    I need a list of students that are new to Carroll according to Student ID and Student Type.
    
    Status: Need to append load status and fy/tr status
    '''
    def newToCarroll(self):
        query = f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT ID,
               FIRST_NAME,
               LAST_NAME,
               TERM,
               TYPE,
               LOAD,
               ADMIT_STATUS
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                 SELECT DISTINCT APPL_APPLICANT                                                                              AS ID,
                                 FIRST_NAME,
                                 LAST_NAME,
                                 STUDENT_TYPES.STT_DESC AS TYPE,
                                 APPL_START_TERM                                                                             AS TERM,
                                 APPL_ADMIT_STATUS AS ADMIT_STATUS,
                                 CASE WHEN STV.STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time' ELSE 'Part-Time' END AS LOAD,
                                 ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT, APPL_STUDENT_TYPE ORDER BY TERM_START_DATE) AS RANK
                 FROM APPLICATIONS AS AP
                          JOIN STUDENT_ACAD_CRED AS AC
                               ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                          JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                          JOIN STUDENT_TERMS_VIEW AS STV
                               ON AP.APPL_APPLICANT = STV.STTR_STUDENT AND APPL_START_TERM = STV.STTR_TERM
                          JOIN TERMS ON APPL_START_TERM = TERMS_ID
                           LEFT JOIN STUDENT_TYPES ON APPL_STUDENT_TYPE = STUDENT_TYPES_ID
                           JOIN PERSON ON APPL_APPLICANT = PERSON.ID
                 WHERE APPL_DATE IS NOT NULL
                   AND STC_STATUS IN ('A', 'N')
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        WHERE RANK = 1
        AND TERM IN ('2024FA', '2024SU')
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY TERM, TYPE, LOAD, ADMIT_STATUS, LAST_NAME, FIRST_NAME
        """
        self.print_table(query, snapshot_term = '2024FA')
        report = "2025-09-02-Snapshot Calculations"
        name = "New Students According To ID and Type"
        self.save_query_results(query, snapshot_term = '2024FA')(report, name)
    # ===================================================================================================================
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    ID: Unknown
    Name: 2025-09-03-More Snapshot Calculations
    Person: Rebecca Schwartz
    Start Date: 2025-09-03
    Due Date: 2025-09-03
    Description: 
    1. Unique student headcount by student type – This is every student registered for classes, no matter their status.  
    It includes Senior citizens, ACE students, undergraduates, exchange students, etc.  
    The numbers will be provided by student type.
        a. Numbers provided by student type
        b. Not run for demographic information
    2. Degree seeking students. This is more commonly used in our reporting, as it is students actively pursuing a 
    degree. It includes both graduate and undergraduate students, and the numbers will be provided with a breakdown 
    into multiple types
        a. Total number of degree seeking students
        b. Undergraduate / Graduate enrollments
        c. PT / FT (graduate and undergraduate)
    3. Demographic information: We take out the graduate students from our demographic overview process.  If you would 
    like this information, I’ve added it to the optional list below.  Just let me know.  
    For now, the data listed is the disaggregated information from the unduplicated headcount of undergraduate students only
        a. Declared Gender
        b. Race/Ethnicity
        c. State of primary residency
        d. Pell recipients
        e. GI bill/military veterans
    4. Retention Rates: Fall to fall retention rate is calculate by taking the first time, fulltime, first year list of 
    students from the previous fall and comparing to who from that cohort is enrolled in classes in fall 2025. It only 
    includes students who are still full time and degree seeking.  It also includes students who may have not done well 
    in fall 2024, not taken classes in spring, and returned in fall 2025.  It does not include any student type (ACE, 
    senior citizen, exchange student, etc.) except undergraduate, full time students. An option for an “overall” 
    retention number is listed below.
    5. Optional List:  These are not numbers we report for things like IPEDS, but may have some value.  If you’d like us
     to run these numbers for both Fall 2024 and 2025, please just let me know.
        a. Demographic information for graduate students  (Not Needed)
        b. Total Retention of every student from Fall 2024 to 2025.  Calculated by taking every degree seeking student 
        in Fall 2024 (and 2023 for comparables) and seeing how many are still enrolled as degree seeking students in 
        Fall 2025 or who graduated before Fall 2025.  So if there was 1100 degree seeking students in Fall 2024, 290 
        graduated, and 810 of those same students were still registered for classes in Fall 2025, our retention rate 
        would be 100%. 
        c. Programs – how many students are declared in each major.  Please note, this will not equal the total 
        headcount as many students have multiple majors.  This can be provided as a list of students in each program, 
        or just a number.
        d. Athletes – we could list the total number of athletes, or the number of athletes in the first time, 
        full time cohort, as preferred. 
    '''

    '''
    Unique student headcount by student type
    '''
    def getUniqueStudentHeadcountByType(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        ST.STUDENT_TYPE AS TYPE
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
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
        """
        agg_func = lambda query: f"""
        SELECT  TYPE, COUNT(*) AS STUDENT_COUNT FROM ({query}) AS X GROUP BY TYPE
        """
        name_func = lambda query: f"""
        SELECT X.ID, P.FIRST_NAME, P.LAST_NAME, X.TYPE FROM ({query}) AS X JOIN PERSON AS P ON P.ID = X.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        func_dict = {"Agg": agg_func, "Names": name_func}
        report = "2025-09-03-More Snapshot Calculations"
        name = "Unique Student Headcount by Type"
        self.save_query_results(query, func_dict = func_dict, snapshot_term="2024FA")(report, name)

    '''
    Unique student headcount
    '''
    def getUniqueStudentHeadcount(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        WHERE STC_TERM = '2024FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT COUNT(*) AS STUDENT_COUNT FROM ({query}) AS X
        """
        name_func = lambda query: f"""
        SELECT X.ID, P.FIRST_NAME, P.LAST_NAME FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Unique Student Headcount"
        self.save_query_results(query, func_dict = {"Agg": agg_func, "Names": name_func}, snapshot_term="2024FA")(report, name)

    '''
    Total Degree-Seeking Students
    '''
    def getTotalDegreeSeekingStudents(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        COALESCE(SP.PROGRAM, 'Unknown') AS PROGRAM
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2024FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND SP.PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT COUNT(*) AS DEGREE_SEEKING_STUDENT_COUNT FROM ({query}) AS X
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, PROGRAM FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Total Degree-Seeking Students"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2024FA")(report, name)

    '''
    Total Degree-Seeking Students By Level
    '''
    def getTotalDegreeSeekingStudentsByLevel(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        COALESCE(SP.PROGRAM, 'Unknown') AS PROGRAM,
                        LEVEL
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2024FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND SP.PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT LEVEL, COUNT(*) AS DEGREE_SEEKING_STUDENT_COUNT FROM ({query}) AS X GROUP BY LEVEL ORDER BY LEVEL
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, PROGRAM, LEVEL FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Total Degree-Seeking Students By Level"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2024FA")(report, name)

    '''
    Total Degree-Seeking Students By Load
    '''
    def getTotalDegreeSeekingStudentsByLoad(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        COALESCE(SP.PROGRAM, 'Unknown') AS PROGRAM,
                        CASE WHEN STV.STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time' ELSE 'Part-Time' END AS LOAD
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        LEFT JOIN STUDENT_TERMS_VIEW AS STV ON STC_PERSON_ID = STV.STTR_STUDENT AND STV.STTR_TERM = '2024FA'
        WHERE STC_TERM = '2024FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND SP.PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT LOAD, COUNT(*) AS DEGREE_SEEKING_STUDENT_COUNT FROM ({query}) AS X GROUP BY LOAD ORDER BY LOAD
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, PROGRAM, LOAD FROM ({query}) X JOIN PERSON P ON X.ID = P.ID 
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Total Degree-Seeking Students By Load"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2024FA")(report, name)

    '''
    Total Undergraduates By Gender
    '''
    def getTotalUndergraduateByGender(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        CASE WHEN PERSON.GENDER = 'M' THEN 'Male' WHEN PERSON.GENDER = 'F' THEN 'Female' 
                            ELSE 'Unknown' END AS GENDER
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN PERSON ON STC.STC_PERSON_ID = PERSON.ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2024FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND LEVEL = 'UG'
        AND PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT GENDER, COUNT(*) AS UG_STUDENT_COUNT FROM ({query}) AS X GROUP BY GENDER ORDER BY GENDER
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, X.GENDER FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Total Undergraduates By Gender"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2024FA")(report, name)

    '''
    Total Undergraduates By Race
    '''
    def getTotalUndergraduateByRace(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        RACE
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN PERSON ON STC.STC_PERSON_ID = PERSON.ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     IPEDS_RACE_ETHNIC_DESC AS RACE,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2024FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND LEVEL = 'UG'
        AND PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT RACE, COUNT(*) AS UG_STUDENT_COUNT FROM ({query}) AS X GROUP BY RACE ORDER BY RACE
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, X.RACE FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Total Undergraduates By Race"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2024FA")(report, name)

    '''
    Total Undergraduates By Residency State
    '''
    def getTotalUndergraduateByResidencyState(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        COALESCE(ST_DESC, 'Unknown') AS STATE
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN PERSON ON STC.STC_PERSON_ID = PERSON.ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     IPEDS_RACE_ETHNIC_DESC AS RACE,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        LEFT JOIN (
            SELECT PAV.ID AS ID,
                    PAV.STATE,
                    ROW_NUMBER() OVER (PARTITION BY PAV.ID ORDER BY ADDRESS_ADD_DATE DESC) AS RANK
            FROM PERSON_ADDRESSES_VIEW AS PAV
            LEFT JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
            WHERE ADDRESS_TYPE = 'H'
        ) AS PERSON_ADDRESS ON PERSON_ADDRESS.ID = STC_PERSON_ID AND PERSON_ADDRESS.RANK = 1
        LEFT JOIN STATES ON PERSON_ADDRESS.STATE = STATES_ID
        WHERE STC_TERM = '2024FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND LEVEL = 'UG'
        AND PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT STATE, COUNT(*) AS UG_STUDENT_COUNT FROM ({query}) AS X GROUP BY STATE ORDER BY STATE
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, STATE FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Total Undergraduates By Residency State"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2024FA")(report, name)

    '''
    Total Undergraduates By Pell Status
    '''
    def getTotalUndergraduateByPellStatus(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM F{'2024FA'[2:4]}_AWARD_LIST AS ST_AWARDS
                    JOIN AWARDS ON ST_AWARDS.SA_AWARD = AWARDS.AW_ID
                    WHERE SA_STUDENT_ID = STC_PERSON_ID
                    AND SA_ACTION = 'A'
                    AND AW_DESCRIPTION = 'Federal Pell Grant'
                ) THEN 'Received Pell Grant' ELSE 'Did Not Receive Pell Grant' END AS PELL_STATUS
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN PERSON ON STC.STC_PERSON_ID = PERSON.ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     IPEDS_RACE_ETHNIC_DESC AS RACE,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2024FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND LEVEL = 'UG'
        AND PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT PELL_STATUS, COUNT(*) AS UG_STUDENT_COUNT FROM ({query}) AS X GROUP BY PELL_STATUS ORDER BY PELL_STATUS
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, PELL_STATUS FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Total Undergraduates By Pell Status"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2024FA")(report, name)

    '''
    Total Undergraduates By GI/Vet Status
    '''
    def getTotalUndergraduateByGIVetStatus(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM F{'2024FA'[2:4]}_AWARD_LIST AS ST_AWARDS
                    JOIN AWARDS ON ST_AWARDS.SA_AWARD = AWARDS.AW_ID
                    WHERE SA_STUDENT_ID = STC_PERSON_ID
                    AND SA_ACTION = 'A'
                    AND AW_DESCRIPTION IN (
                    'VA Allowances (Books, Supplies, Housing)',
                    'VA Ben/Stipend',
                    'VA Ben/Tuition',
                    'VA Yellow Ribbon Carroll Match',
                    'VA Yellow Ribbon Fees',
                    'VA Yellow Ribbon Match'  --Carroll Specific?--
                    )
                ) OR EXISTS (
                    SELECT 1
                    FROM STA_OTHER_COHORTS_VIEW
                    JOIN TERMS AS TARGET_TERM ON TERMS_ID = '2024FA'
                    WHERE STA_STUDENT = STC_PERSON_ID
                    AND STA_OTHER_COHORT_GROUPS = 'VETS'
                    AND COALESCE(STA_OTHER_COHORT_END_DATES, TARGET_TERM.TERM_START_DATE) >= TARGET_TERM.TERM_START_DATE
                ) THEN 'Yes' ELSE 'No' END AS GI_VET_STATUS
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN PERSON ON STC.STC_PERSON_ID = PERSON.ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     IPEDS_RACE_ETHNIC_DESC AS RACE,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2024FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND LEVEL = 'UG'
        AND PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT GI_VET_STATUS, COUNT(*) AS UG_STUDENT_COUNT FROM ({query}) AS X 
        GROUP BY GI_VET_STATUS ORDER BY GI_VET_STATUS
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, GI_VET_STATUS FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Total Undergraduates By GI_Vet Status"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2024FA")(report, name)

    '''
    Fall to Fall Retention
    '''
    def cohortRetention(self):
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
        AND APPL_ACAD_PROGRAM != 'NDEG'  --Degree-Seeking--
        AND APPL_ADMIT_STATUS = 'FY' --First Time--
        AND STV.STTR_STUDENT_LOAD IN ('F', 'O')  --Full Time--
        AND APPL_STUDENT_TYPE = 'UG'   --Undergraduate--
        ------TERM---------------------
        AND APPL_STUDENT_TYPE = 'UG'
        AND APPL_START_TERM = '2023FA'
        """
        cohort_df = self.db_table(cohort_query, snapshot_term="2023FA")
        query = f"""
        --(Begin 2)----------------------------------------------------------------------------------------------------
        SELECT ID,
                CASE WHEN EXISTS (SELECT 1
                    FROM STUDENT_ACAD_CRED AS STC
                    LEFT JOIN STC_STATUSES AS STAT ON STC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                    LEFT JOIN STUDENT_TERMS_VIEW AS STV 
                        ON STC_PERSON_ID = STV.STTR_STUDENT AND STC_TERM = STV.STTR_TERM
                    LEFT JOIN (
                        SELECT  STUDENTS_ID AS ID,
                                STU_TYPES AS TYPE,
                                ROW_NUMBER() OVER (PARTITION BY STUDENTS_ID ORDER BY STU_TYPE_DATES DESC) AS RANK
                        FROM STU_TYPE_INFO
                    ) AS STU_TYPES ON STC_PERSON_ID = STU_TYPES.ID AND RANK = 1
                    WHERE STC_STATUS IN ('A', 'N')
                    AND STC_TERM = '2024FA'
                    AND STV.STTR_STUDENT_LOAD IN ('F', 'O')
                    AND EXISTS (
                            SELECT 1
                            FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                            WHERE STP_CURRENT_STATUS = 'Active'
                            AND STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                            AND STC_PERSON_ID = STUDENT_ID
                    )
                    AND STU_TYPES.TYPE = 'UG'
                    AND STC_PERSON_ID = COHORT_2023FA.ID
                    ) THEN 1 ELSE 0 END AS FFUG_RETAINED
        FROM 
        --(Begin 1)----------------------------------------------------------------------------------------------------
        ({self.df_query(cohort_df)})
        --(End 1)------------------------------------------------------------------------------------------------------
        AS COHORT_2023FA
        --(End 2)------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT FORMAT(AVG(1.0 * FFUG_RETAINED), 'P') AS FFUG_RETENTION FROM ({query}) AS X
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, FFUG_RETAINED FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Cohort Retention"
        self.save_query_results(query,
                                {"Agg": agg_func, "Names": name_func}, snapshot_term='2024FA')(report, name)

    '''
    Institutional Retention
    '''
    def institutionalRetention(self):
        cohort_query = f"""
        SELECT DISTINCT X.ID,
                        X.TERM
        FROM (
                SELECT DISTINCT STC_PERSON_ID AS ID,
                        STC_TERM AS TERM
                FROM STUDENT_ACAD_CRED AS STC
                LEFT JOIN STC_STATUSES AS STATUS 
                ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                WHERE STC_STATUS IN ('A', 'N')
                AND STC_TERM = '2023FA'
        ) AS X
        JOIN (
            SELECT DISTINCT STUDENT_ID
            FROM STUDENT_ACAD_PROGRAMS_VIEW
            WHERE STP_CURRENT_STATUS = 'Active'
            AND STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
            ) AS Y ON X.ID = STUDENT_ID
        """
        cohort_df = self.db_table(cohort_query, snapshot_term="2023FA")
        query = f"""
        --(Begin 2)----------------------------------------------------------------------------------------------------
        SELECT ID,
                CASE WHEN (EXISTS (SELECT 1
                    FROM STUDENT_ACAD_CRED AS STC
                    LEFT JOIN STC_STATUSES AS STAT ON STC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                    WHERE STC_STATUS IN ('A', 'N')
                    AND STC_TERM = '2024FA'
                    AND EXISTS (
                            SELECT 1
                            FROM STUDENT_PROGRAMS_VIEW AS SP
                            JOIN STUDENT_ACAD_PROG_STATUS_VIEW AS PS ON SP.STUDENT_PROGRAMS_ID = PS.STUDENT_PROGRAMS_ID
                            WHERE SP.STPR_STUDENT = STC_PERSON_ID
                            AND SP.STPR_ACAD_PROGRAM != 'NDEG'
                            AND PS.PROG_STATUS = 'A'
                    )
                    AND STC_PERSON_ID = COHORT.ID
                    )) OR (EXISTS (
                    SELECT 1
                    FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                    JOIN TERMS AS COHORT_TERM ON TERMS_ID = COHORT.TERM
                    WHERE SAPV.STUDENT_ID = COHORT.ID
                    AND SAPV.STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                    AND SAPV.STP_CURRENT_STATUS = 'Graduated'
                    AND COALESCE(STP_END_DATE, COHORT_TERM.TERM_START_DATE) >= COHORT_TERM.TERM_START_DATE
                    )) THEN 1 ELSE 0 END AS INST_RETAINED
        FROM 
        --(Begin 1)----------------------------------------------------------------------------------------------------
        ({self.df_query(cohort_df)})
        --(End 1)------------------------------------------------------------------------------------------------------
        AS COHORT
        --(End 2)------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT FORMAT(AVG(1.0 * INST_RETAINED), 'P') AS INST_RETENTION FROM ({query}) AS X
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, INST_RETAINED FROM ({query}) X LEFT JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Institutional Retention"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2024FA")(report, name)

    '''
    Major Count
    '''
    def majorCount(self):
        query = f"""
        --(Begin 1)----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STUDENT_ID AS ID,
                MAJORS.MAJ_DESC AS MAJOR
        FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        JOIN MAJORS ON SAPV.STP_MAJOR1 = MAJORS_ID
        WHERE STP_CURRENT_STATUS = 'Active'
        UNION
        SELECT DISTINCT STUDENT_ID AS ID,
               MAJORS.MAJ_DESC AS MAJOR
        FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        JOIN STPR_MAJOR_LIST_VIEW AS ADDNL_MAJORS
            ON SAPV.STUDENT_ID = ADDNL_MAJORS.STPR_STUDENT
            AND SAPV.STP_ACADEMIC_PROGRAM = ADDNL_MAJORS.STPR_ACAD_PROGRAM
        JOIN MAJORS ON ADDNL_MAJORS.STPR_ADDNL_MAJORS = MAJORS_ID
        WHERE STP_CURRENT_STATUS = 'Active'
        AND STPR_ADDNL_MAJOR_END_DATE IS NULL
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT MAJOR, COUNT(*) AS STUDENT_COUNT FROM ({query}) AS X GROUP BY MAJOR ORDER BY MAJOR
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, MAJOR FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Major Count"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func},
                                snapshot_term='2024FA')(report, name)

    '''
    Total Number of Athletes
    '''
    def totalNumberOfAthletes(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT ID 
        FROM (
        SELECT DISTINCT STC_PERSON_ID AS ID
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
        WHERE STATUS.STC_STATUS IN ('N', 'A')
        AND STC_TERM = '2024FA'
        ) AS X
        JOIN (
        SELECT DISTINCT STA_STUDENT
        FROM STA_OTHER_COHORTS_VIEW
        JOIN VALS ON VALCODE_ID = 'INSTITUTION.COHORTS'
        AND STA_OTHER_COHORT_GROUPS = VALS.VAL_INTERNAL_CODE
        WHERE VAL_EXTERNAL_REPRESENTATION IN (
                                              'Cheerleading',
                                              'Dance',
                                              'Football',
                                              'Indoor Men''s Track',
                                              'Indoor Women''s Track',
                                              'Men''s Basketball',
                                              'Men''s Basketball - JV',
                                              'Men''s Cross Country',
                                              'Men''s Golf',
                                              'Men''s Soccer',
                                              'Men''s Soccer - JV',
                                              'Outdoor Men''s Track',
                                              'Outdoor Women''s Track',
                                              'Women''s Basketball',
                                              'Women''s Basketball - JV',
                                              'Women''s Cross Country',
                                              'Women''s Golf',
                                              'Women''s Soccer',
                                              'Women''s  Softball',
                                              'Women''s Volleyball',
                                              'Women''s Volleyball - JV'
                                            )
        AND STA_OTHER_COHORT_END_DATES IS NULL
        ) AS Y ON X.ID = Y.STA_STUDENT
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT COUNT(*) AS STUDENT_ATHLETE_COUNT FROM ({query}) AS X
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Student Athlete Count"
        self.save_query_results(query,
                                {"Agg": agg_func, "Names": name_func}, snapshot_term='2024FA')(report, name)

    '''
    Total Number of Athletes
    '''
    def totalNumberOfAthletesFromCohort(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT ID 
        FROM (
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
        AND APPL_ACAD_PROGRAM != 'NDEG'  --Degree-Seeking--
        AND APPL_ADMIT_STATUS = 'FY' --First Time--
        AND STV.STTR_STUDENT_LOAD IN ('F', 'O')  --Full Time--
        AND APPL_STUDENT_TYPE = 'UG'   --Undergraduate--
        ------TERM---------------------
        AND APPL_START_TERM = '2024FA'
        ) AS X
        JOIN (
        SELECT DISTINCT STA_STUDENT
        FROM STA_OTHER_COHORTS_VIEW
        JOIN TERMS AS TARGET_TERM ON TERMS_ID = '2024FA'
        JOIN VALS ON VALCODE_ID = 'INSTITUTION.COHORTS'
        AND STA_OTHER_COHORT_GROUPS = VALS.VAL_INTERNAL_CODE
        WHERE VAL_EXTERNAL_REPRESENTATION IN (
                                              'Cheerleading',
                                              'Dance',
                                              'Football',
                                              'Indoor Men''s Track',
                                              'Indoor Women''s Track',
                                              'Men''s Basketball',
                                              'Men''s Basketball - JV',
                                              'Men''s Cross Country',
                                              'Men''s Golf',
                                              'Men''s Soccer',
                                              'Men''s Soccer - JV',
                                              'Outdoor Men''s Track',
                                              'Outdoor Women''s Track',
                                              'Women''s Basketball',
                                              'Women''s Basketball - JV',
                                              'Women''s Cross Country',
                                              'Women''s Golf',
                                              'Women''s Soccer',
                                              'Women''s  Softball',
                                              'Women''s Volleyball',
                                              'Women''s Volleyball - JV'
                                            )
        AND STA_OTHER_COHORT_END_DATES IS NULL
        ) AS Y ON X.ID = Y.STA_STUDENT
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT COUNT(*) AS STUDENT_ATHLETE_COUNT_FROM_COHORT FROM ({query}) AS X
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        """
        report = "2025-09-03-More Snapshot Calculations"
        name = "Student Athlete Count From Cohort"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func},
                                snapshot_term='2024FA')(report, name)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    ID: Unknown
    Name: 2025-09-04-2025FA Snapshot Calculations
    Person: Rebecca Schwartz
    Start Date: 2025-09-04
    Due Date: 2025-09-04
    Description: 
    Do what you did before except with the 2025FA snapshot.
    '''

    '''
    Unique student headcount by student type
    '''
    def getUniqueStudentHeadcountByType_2025FA(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        ST.STUDENT_TYPE AS TYPE
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        LEFT JOIN (
            SELECT STUDENTS_ID,
                    STT_DESC AS STUDENT_TYPE,
                    ROW_NUMBER() OVER (PARTITION BY STUDENTS_ID ORDER BY STU_TYPE_DATES DESC) AS RANK
            FROM STU_TYPE_INFO
            JOIN STUDENT_TYPES ON STU_TYPES = STUDENT_TYPES_ID
        ) AS ST ON STC_PERSON_ID = STUDENTS_ID AND ST.RANK = 1
        WHERE STC_TERM = '2025FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT  TYPE, COUNT(*) AS STUDENT_COUNT FROM ({query}) AS X GROUP BY TYPE
        """
        name_func = lambda query: f"""
        SELECT X.ID, P.FIRST_NAME, P.LAST_NAME, X.TYPE FROM ({query}) AS X JOIN PERSON AS P ON P.ID = X.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        func_dict = {"Agg": agg_func, "Names": name_func}
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Unique Student Headcount by Type"
        self.save_query_results(query, func_dict = func_dict, snapshot_term="2025FA")(report, name)

    '''
    Unique student headcount
    '''
    def getUniqueStudentHeadcount_2025FA(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        WHERE STC_TERM = '2025FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT COUNT(*) AS STUDENT_COUNT FROM ({query}) AS X
        """
        name_func = lambda query: f"""
        SELECT X.ID, P.FIRST_NAME, P.LAST_NAME FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Unique Student Headcount"
        self.save_query_results(query, func_dict = {"Agg": agg_func, "Names": name_func}, snapshot_term="2025FA")(report, name)

    '''
    Total Degree-Seeking Students
    '''
    def getTotalDegreeSeekingStudents_2025FA(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        COALESCE(SP.PROGRAM, 'Unknown') AS PROGRAM
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2025FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND SP.PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT COUNT(*) AS DEGREE_SEEKING_STUDENT_COUNT FROM ({query}) AS X
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, PROGRAM FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Total Degree-Seeking Students"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2025FA")(report, name)

    '''
    Total Degree-Seeking Students By Level
    '''
    def getTotalDegreeSeekingStudentsByLevel_2025FA(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        COALESCE(SP.PROGRAM, 'Unknown') AS PROGRAM,
                        LEVEL
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2025FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND SP.PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT LEVEL, COUNT(*) AS DEGREE_SEEKING_STUDENT_COUNT FROM ({query}) AS X GROUP BY LEVEL ORDER BY LEVEL
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, PROGRAM, LEVEL FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Total Degree-Seeking Students By Level"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2025FA")(report, name)

    '''
    Total Degree-Seeking Students By Load
    '''
    def getTotalDegreeSeekingStudentsByLoad_2025FA(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        COALESCE(SP.PROGRAM, 'Unknown') AS PROGRAM,
                        CASE WHEN STV.STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time' ELSE 'Part-Time' END AS LOAD
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        LEFT JOIN STUDENT_TERMS_VIEW AS STV ON STC_PERSON_ID = STV.STTR_STUDENT AND STV.STTR_TERM = STC.STC_TERM
        WHERE STC_TERM = '2025FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND SP.PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT LOAD, COUNT(*) AS DEGREE_SEEKING_STUDENT_COUNT FROM ({query}) AS X GROUP BY LOAD ORDER BY LOAD
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, PROGRAM, LOAD FROM ({query}) X JOIN PERSON P ON X.ID = P.ID 
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Total Degree-Seeking Students By Load"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2025FA")(report, name)


    '''
    Total Undergraduates By Gender
    '''
    def getTotalUndergraduateByGender_2025FA(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        CASE WHEN PERSON.GENDER = 'M' THEN 'Male' WHEN PERSON.GENDER = 'F' THEN 'Female' 
                            ELSE 'Unknown' END AS GENDER
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN PERSON ON STC.STC_PERSON_ID = PERSON.ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2025FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND LEVEL = 'UG'
        AND PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT GENDER, COUNT(*) AS UG_STUDENT_COUNT FROM ({query}) AS X GROUP BY GENDER ORDER BY GENDER
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, X.GENDER FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Total Undergraduates By Gender"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2025FA")(report, name)


    '''
    Total Undergraduates By Race
    '''
    def getTotalUndergraduateByRace_2025FA(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                        RACE
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN PERSON ON STC.STC_PERSON_ID = PERSON.ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     IPEDS_RACE_ETHNIC_DESC AS RACE,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2025FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND LEVEL = 'UG'
        AND PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT RACE, COUNT(*) AS UG_STUDENT_COUNT FROM ({query}) AS X GROUP BY RACE ORDER BY RACE
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, X.RACE FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Total Undergraduates By Race"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2025FA")(report, name)


    '''
    Total Undergraduates By Residency State
    '''
    def getTotalUndergraduateByResidencyState_2025FA(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STUDENTS.ID,
                        COALESCE(STATE, 'Unknown') AS STATE
        FROM (
            SELECT DISTINCT STC_PERSON_ID AS ID
            FROM STUDENT_ACAD_CRED AS STC
            LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
            WHERE STC_TERM = '2025FA'
            AND STATUS.STC_STATUS IN ('N', 'A')
        ) AS STUDENTS
        JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP 
              ON STUDENTS.ID = SP.STUDENT_ID AND SP.RANK = 1
              AND LEVEL = 'UG'
              AND PROGRAM != 'Non-Degree Seeking Students'
        LEFT JOIN (
            SELECT PAV.ID AS ID,
                    STATES.ST_DESC AS STATE,
                    ROW_NUMBER() OVER (PARTITION BY PAV.ID ORDER BY ADDRESS_ADD_DATE DESC) AS RANK
            FROM PERSON_ADDRESSES_VIEW AS PAV
            LEFT JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
            LEFT JOIN STATES ON PAV.STATE = STATES_ID
            WHERE ADDRESS_TYPE = 'H'
        ) AS PERSON_ADDRESS ON PERSON_ADDRESS.ID = STUDENTS.ID AND PERSON_ADDRESS.RANK = 1
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        query_2 = f"""
        SELECT DISTINCT STUDENT_ID AS ID
        
        """
        agg_func = lambda query: f"""
        SELECT STATE, COUNT(*) AS UG_STUDENT_COUNT FROM ({query}) AS X GROUP BY STATE ORDER BY STATE
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, STATE FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Total Undergraduates By Residency State"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2025FA")(report, name)


    '''
    Total Undergraduates By Pell Status
    '''
    def getTotalUndergraduateByPellStatus_2025FA(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM F{'2025FA'[2:4]}_AWARD_LIST AS ST_AWARDS
                    JOIN AWARDS ON ST_AWARDS.SA_AWARD = AWARDS.AW_ID
                    WHERE SA_STUDENT_ID = STC_PERSON_ID
                    AND SA_ACTION = 'A'
                    AND AW_DESCRIPTION = 'Federal Pell Grant'
                ) THEN 'Received Pell Grant' ELSE 'Did Not Receive Pell Grant' END AS PELL_STATUS
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN PERSON ON STC.STC_PERSON_ID = PERSON.ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     IPEDS_RACE_ETHNIC_DESC AS RACE,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2025FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND LEVEL = 'UG'
        AND PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT PELL_STATUS, COUNT(*) AS UG_STUDENT_COUNT FROM ({query}) AS X GROUP BY PELL_STATUS ORDER BY PELL_STATUS
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, PELL_STATUS FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Total Undergraduates By Pell Status"
        #self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2025FA")(report, name)
        new_query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM F{'2025FA'[2:4]}_AWARD_LIST AS ST_AWARDS
                    JOIN AWARDS ON ST_AWARDS.SA_AWARD = AWARDS.AW_ID
                    WHERE SA_STUDENT_ID = STC_PERSON_ID
                    AND SA_ACTION = 'A'
                    AND AW_DESCRIPTION = 'Federal Pell Grant'
                ) THEN 'Received Pell Grant' ELSE 'Did Not Receive Pell Grant' END AS PELL_STATUS
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN PERSON ON STC.STC_PERSON_ID = PERSON.ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     IPEDS_RACE_ETHNIC_DESC AS RACE,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2025FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND LEVEL = 'UG'
        --AND PROGRAM != 'Non-Degree Seeking Students'
        AND LAST_NAME = 'Alfonzo'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        person_query = f"""
        SELECT *
        FROM STUDENT_ACAD_CRED AS STC
        WHERE STC_PERSON_ID = '6192307'
        """
        self.print_table(person_query, snapshot_term="2025FA")


    '''
    Total Undergraduates By GI/Vet Status
    '''
    def getTotalUndergraduateByGIVetStatus_2025FA(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STC_PERSON_ID AS ID,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM F{'2025FA'[2:4]}_AWARD_LIST AS ST_AWARDS
                    JOIN AWARDS ON ST_AWARDS.SA_AWARD = AWARDS.AW_ID
                    WHERE SA_STUDENT_ID = STC_PERSON_ID
                    AND SA_ACTION = 'A'
                    AND AW_DESCRIPTION IN (
                    'VA Allowances (Books, Supplies, Housing)',
                    'VA Ben/Stipend',
                    'VA Ben/Tuition',
                    'VA Yellow Ribbon Carroll Match',
                    'VA Yellow Ribbon Fees',
                    'VA Yellow Ribbon Match'  --Carroll Specific?--
                    )
                ) OR EXISTS (
                    SELECT 1
                    FROM STA_OTHER_COHORTS_VIEW
                    JOIN TERMS AS TARGET_TERM ON TERMS_ID = '2025FA'
                    WHERE STA_STUDENT = STC_PERSON_ID
                    AND STA_OTHER_COHORT_GROUPS = 'VETS'
                    AND COALESCE(STA_OTHER_COHORT_END_DATES, TARGET_TERM.TERM_START_DATE) >= TARGET_TERM.TERM_START_DATE
                ) THEN 'Yes' ELSE 'No' END AS GI_VET_STATUS
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN PERSON ON STC.STC_PERSON_ID = PERSON.ID
        LEFT JOIN (
            SELECT   STUDENT_ID,
                     STP_PROGRAM_TITLE AS PROGRAM,
                     STP_ACAD_LEVEL AS LEVEL,
                     IPEDS_RACE_ETHNIC_DESC AS RACE,
                     ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
              WHERE STP_CURRENT_STATUS = 'Active'
              ) AS SP ON STC_PERSON_ID = SP.STUDENT_ID AND SP.RANK = 1
        WHERE STC_TERM = '2025FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND LEVEL = 'UG'
        AND PROGRAM != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT GI_VET_STATUS, COUNT(*) AS UG_STUDENT_COUNT FROM ({query}) AS X 
        GROUP BY GI_VET_STATUS ORDER BY GI_VET_STATUS
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, GI_VET_STATUS FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Total Undergraduates By GI_Vet Status"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2025FA")(report, name)

    '''
    Fall to Fall Retention
    '''
    def cohortRetention_2025FA(self):
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
        AND APPL_ACAD_PROGRAM != 'NDEG'  --Degree-Seeking--
        AND APPL_ADMIT_STATUS = 'FY' --First Time--
        AND STV.STTR_STUDENT_LOAD IN ('F', 'O')  --Full Time--
        AND APPL_STUDENT_TYPE = 'UG'   --Undergraduate--
        ------TERM---------------------
        AND APPL_STUDENT_TYPE = 'UG'
        AND APPL_START_TERM = '2024FA'
        """
        cohort_df = self.db_table(cohort_query, snapshot_term="2024FA")
        query = f"""
        --(Begin 2)----------------------------------------------------------------------------------------------------
        SELECT ID,
                CASE WHEN EXISTS (SELECT 1
                    FROM STUDENT_ACAD_CRED AS STC
                    LEFT JOIN STC_STATUSES AS STAT ON STC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                    LEFT JOIN STUDENT_TERMS_VIEW AS STV 
                        ON STC_PERSON_ID = STV.STTR_STUDENT AND STC_TERM = STV.STTR_TERM
                    LEFT JOIN (
                        SELECT  STUDENTS_ID AS ID,
                                STU_TYPES AS TYPE,
                                ROW_NUMBER() OVER (PARTITION BY STUDENTS_ID ORDER BY STU_TYPE_DATES DESC) AS RANK
                        FROM STU_TYPE_INFO
                    ) AS STU_TYPES ON STC_PERSON_ID = STU_TYPES.ID AND RANK = 1
                    WHERE STC_STATUS IN ('A', 'N')
                    AND STC_TERM = '2025FA'
                    AND STV.STTR_STUDENT_LOAD IN ('F', 'O')
                    AND EXISTS (
                            SELECT 1
                            FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                            WHERE STP_CURRENT_STATUS = 'Active'
                            AND STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                            AND STC_PERSON_ID = STUDENT_ID
                    )
                    AND STU_TYPES.TYPE = 'UG'
                    AND STC_PERSON_ID = COHORT_2023FA.ID
                    ) THEN 1 ELSE 0 END AS FFUG_RETAINED
        FROM 
        --(Begin 1)----------------------------------------------------------------------------------------------------
        ({self.df_query(cohort_df)})
        --(End 1)------------------------------------------------------------------------------------------------------
        AS COHORT_2023FA
        --(End 2)------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT FORMAT(AVG(1.0 * FFUG_RETAINED), 'P') AS FFUG_RETENTION FROM ({query}) AS X
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, FFUG_RETAINED FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Cohort Retention"
        self.save_query_results(query,
                                {"Agg": agg_func, "Names": name_func}, snapshot_term='2025FA')(report, name)

    '''
    Institutional Retention
    '''
    def institutionalRetention_2025FA(self):
        cohort_query = f"""
        SELECT DISTINCT X.ID,
                        X.TERM
        FROM (
                SELECT DISTINCT STC_PERSON_ID AS ID,
                        STC_TERM AS TERM
                FROM STUDENT_ACAD_CRED AS STC
                LEFT JOIN STC_STATUSES AS STATUS 
                ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                WHERE STC_STATUS IN ('A', 'N')
                AND STC_TERM = '2024FA'
        ) AS X
        JOIN (
            SELECT DISTINCT STUDENT_ID
            FROM STUDENT_ACAD_PROGRAMS_VIEW
            WHERE STP_CURRENT_STATUS = 'Active'
            AND STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
            ) AS Y ON X.ID = STUDENT_ID
        """
        cohort_df = self.db_table(cohort_query, snapshot_term="2024FA")
        query = f"""
        --(Begin 2)----------------------------------------------------------------------------------------------------
        SELECT ID,
                CASE WHEN (EXISTS (SELECT 1
                    FROM STUDENT_ACAD_CRED AS STC
                    LEFT JOIN STC_STATUSES AS STAT ON STC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                    WHERE STC_STATUS IN ('A', 'N')
                    AND STC_TERM = '2025FA'
                    AND EXISTS (
                            SELECT 1
                            FROM STUDENT_PROGRAMS_VIEW AS SP
                            JOIN STUDENT_ACAD_PROG_STATUS_VIEW AS PS ON SP.STUDENT_PROGRAMS_ID = PS.STUDENT_PROGRAMS_ID
                            WHERE SP.STPR_STUDENT = STC_PERSON_ID
                            AND SP.STPR_ACAD_PROGRAM != 'NDEG'
                            AND PS.PROG_STATUS = 'A'
                    )
                    AND STC_PERSON_ID = COHORT.ID
                    )) OR (EXISTS (
                    SELECT 1
                    FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                    JOIN TERMS AS COHORT_TERM ON TERMS_ID = COHORT.TERM
                    WHERE SAPV.STUDENT_ID = COHORT.ID
                    AND SAPV.STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                    AND SAPV.STP_CURRENT_STATUS = 'Graduated'
                    AND COALESCE(STP_END_DATE, COHORT_TERM.TERM_START_DATE) >= COHORT_TERM.TERM_START_DATE
                    )) THEN 1 ELSE 0 END AS INST_RETAINED
        FROM 
        --(Begin 1)----------------------------------------------------------------------------------------------------
        ({self.df_query(cohort_df)})
        --(End 1)------------------------------------------------------------------------------------------------------
        AS COHORT
        --(End 2)------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT FORMAT(AVG(1.0 * INST_RETAINED), 'P') AS INST_RETENTION FROM ({query}) AS X
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, INST_RETAINED FROM ({query}) X LEFT JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Institutional Retention"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func}, snapshot_term="2025FA")(report, name)

    '''
    Major Count
    '''
    def majorCount_2025FA(self):
        query = f"""
        --(Begin 1)----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STUDENT_ID AS ID,
                MAJORS.MAJ_DESC AS MAJOR
        FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        JOIN MAJORS ON SAPV.STP_MAJOR1 = MAJORS_ID
        WHERE STP_CURRENT_STATUS = 'Active'
        UNION
        SELECT DISTINCT STUDENT_ID AS ID,
               MAJORS.MAJ_DESC AS MAJOR
        FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        JOIN STPR_MAJOR_LIST_VIEW AS ADDNL_MAJORS
            ON SAPV.STUDENT_ID = ADDNL_MAJORS.STPR_STUDENT
            AND SAPV.STP_ACADEMIC_PROGRAM = ADDNL_MAJORS.STPR_ACAD_PROGRAM
        JOIN MAJORS ON ADDNL_MAJORS.STPR_ADDNL_MAJORS = MAJORS_ID
        WHERE STP_CURRENT_STATUS = 'Active'
        AND STPR_ADDNL_MAJOR_END_DATE IS NULL
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT MAJOR, COUNT(*) AS STUDENT_COUNT FROM ({query}) AS X GROUP BY MAJOR ORDER BY MAJOR
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME, MAJOR FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Major Count"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func},
                                snapshot_term='2025FA')(report, name)

    '''
    Total Number of Athletes
    '''
    def totalNumberOfAthletes_2025FA(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT ID 
        FROM (
        SELECT DISTINCT STC_PERSON_ID AS ID
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
        WHERE STATUS.STC_STATUS IN ('N', 'A')
        AND STC_TERM = '2025FA'
        ) AS X
        JOIN (
        SELECT DISTINCT STA_STUDENT
        FROM STA_OTHER_COHORTS_VIEW
        JOIN VALS ON VALCODE_ID = 'INSTITUTION.COHORTS'
        AND STA_OTHER_COHORT_GROUPS = VALS.VAL_INTERNAL_CODE
        WHERE VAL_EXTERNAL_REPRESENTATION IN (
                                              'Cheerleading',
                                              'Dance',
                                              'Football',
                                              'Indoor Men''s Track',
                                              'Indoor Women''s Track',
                                              'Men''s Basketball',
                                              'Men''s Basketball - JV',
                                              'Men''s Cross Country',
                                              'Men''s Golf',
                                              'Men''s Soccer',
                                              'Men''s Soccer - JV',
                                              'Outdoor Men''s Track',
                                              'Outdoor Women''s Track',
                                              'Women''s Basketball',
                                              'Women''s Basketball - JV',
                                              'Women''s Cross Country',
                                              'Women''s Golf',
                                              'Women''s Soccer',
                                              'Women''s  Softball',
                                              'Women''s Volleyball',
                                              'Women''s Volleyball - JV'
                                            )
        AND STA_OTHER_COHORT_END_DATES IS NULL
        ) AS Y ON X.ID = Y.STA_STUDENT
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT COUNT(*) AS STUDENT_ATHLETE_COUNT FROM ({query}) AS X
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Student Athlete Count"
        self.save_query_results(query,
                                {"Agg": agg_func, "Names": name_func}, snapshot_term='2025FA')(report, name)

    '''
    Total Number of Athletes
    '''
    def totalNumberOfAthletesFromCohort_2025FA(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT ID 
        FROM (
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
        AND APPL_ACAD_PROGRAM != 'NDEG'  --Degree-Seeking--
        AND APPL_ADMIT_STATUS = 'FY' --First Time--
        AND STV.STTR_STUDENT_LOAD IN ('F', 'O')  --Full Time--
        AND APPL_STUDENT_TYPE = 'UG'   --Undergraduate--
        ------TERM---------------------
        AND APPL_START_TERM = '2025FA'
        ) AS X
        JOIN (
        SELECT DISTINCT STA_STUDENT
        FROM STA_OTHER_COHORTS_VIEW
        JOIN VALS ON VALCODE_ID = 'INSTITUTION.COHORTS'
        AND STA_OTHER_COHORT_GROUPS = VALS.VAL_INTERNAL_CODE
        WHERE VAL_EXTERNAL_REPRESENTATION IN (
                                              'Cheerleading',
                                              'Dance',
                                              'Football',
                                              'Indoor Men''s Track',
                                              'Indoor Women''s Track',
                                              'Men''s Basketball',
                                              'Men''s Basketball - JV',
                                              'Men''s Cross Country',
                                              'Men''s Golf',
                                              'Men''s Soccer',
                                              'Men''s Soccer - JV',
                                              'Outdoor Men''s Track',
                                              'Outdoor Women''s Track',
                                              'Women''s Basketball',
                                              'Women''s Basketball - JV',
                                              'Women''s Cross Country',
                                              'Women''s Golf',
                                              'Women''s Soccer',
                                              'Women''s  Softball',
                                              'Women''s Volleyball',
                                              'Women''s Volleyball - JV'
                                            )
        AND STA_OTHER_COHORT_END_DATES IS NULL
        ) AS Y ON X.ID = Y.STA_STUDENT
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg_func = lambda query: f"""
        SELECT COUNT(*) AS STUDENT_ATHLETE_COUNT_FROM_COHORT FROM ({query}) AS X
        """
        name_func = lambda query: f"""
        SELECT X.ID, FIRST_NAME, LAST_NAME FROM ({query}) X JOIN PERSON P ON X.ID = P.ID
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "Student Athlete Count From Cohort"
        self.save_query_results(query, {"Agg": agg_func, "Names": name_func},
                                snapshot_term='2025FA')(report, name)

    '''
    I need a list of students that are new to Carroll according to Student ID and Student Type.
    '''
    def newToCarroll_2025FA(self):
        query = f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT ID,
               FIRST_NAME,
               LAST_NAME,
               TERM,
               TYPE,
               LOAD,
               ADMIT_STATUS
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                 SELECT DISTINCT APPL_APPLICANT                                                                              AS ID,
                                 FIRST_NAME,
                                 LAST_NAME,
                                 STUDENT_TYPES.STT_DESC AS TYPE,
                                 APPL_START_TERM                                                                             AS TERM,
                                 APPL_ADMIT_STATUS AS ADMIT_STATUS,
                                 CASE WHEN STV.STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time' ELSE 'Part-Time' END AS LOAD,
                                 ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT, APPL_STUDENT_TYPE ORDER BY TERM_START_DATE) AS RANK
                 FROM APPLICATIONS AS AP
                          JOIN STUDENT_ACAD_CRED AS AC
                               ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                          JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                          JOIN STUDENT_TERMS_VIEW AS STV
                               ON AP.APPL_APPLICANT = STV.STTR_STUDENT AND APPL_START_TERM = STV.STTR_TERM
                          JOIN TERMS ON APPL_START_TERM = TERMS_ID
                           LEFT JOIN STUDENT_TYPES ON APPL_STUDENT_TYPE = STUDENT_TYPES_ID
                           JOIN PERSON ON APPL_APPLICANT = PERSON.ID
                 WHERE APPL_DATE IS NOT NULL
                   AND STC_STATUS IN ('A', 'N')
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        WHERE RANK = 1
        AND TERM IN ('2025FA', '2025SU')
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY TERM, TYPE, LOAD, ADMIT_STATUS, LAST_NAME, FIRST_NAME
        """
        report = "2025-09-04-2025FA Snapshot Calculations"
        name = "New Students According To ID and Type"
        self.save_query_results(query, snapshot_term='2025FA')(report, name)
    # ==================================================================================================================
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    ID: Unknown
    Name: 2025-09-08-2025 Graduating Class Statistics
    Person: Timmie Smart
    Start Date: 2025-09-08
    End Date:
    Due Date:
    Description: 
    I am hoping to find out how many students in the 2025 graduating class graduated in three years as well as those 
    graduating with a degree in Biology. Also, of those two groups, how many graduated with Highest Honors/Summa Cum 
    Laude. This information will be used to help in applications for Doctorate programs.
    '''
    def getThoseWhoGraduatedInThreeYears(self):
        query = f"""
        SELECT STUDENT_PROGRAMS_ID,
                STPR_STUDENT,
                STPR_ACAD_PROGRAM
        FROM SPT_STUDENT_PROGRAMS
        JOIN ODS_TERMS AS GRADUATING_TERM ON TERMS_ID = '2025SP'
        WHERE STPR_CURRENT_STATUS = 'G'
        AND END_DATE <= GRADUATING_TERM.TERM_END_DATE
        AND END_DATE >= GRADUATING_TERM.TERM_START_DATE
        AND DATEDIFF(DAY, START_DATE, END_DATE) / 365.25 <= 3
        """
        report = "2025-09-08-2025 Graduating Class Statistics"
        name = "Those That Graduated Within Three Years"
        agg = lambda query: f"""
        SELECT COUNT(*) AS NUMBER_THAT_GRADUATED_WITHIN_THREE_YEARS FROM ({query}) AS X
        """
        names = lambda query: f"""
        SELECT STUDENT_PROGRAMS_ID, STPR_STUDENT, FIRST_NAME, LAST_NAME,  STPR_ACAD_PROGRAM
        FROM ({query}) AS X JOIN ODS_PERSON P ON X.STPR_STUDENT = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        self.save_query_results(query, {"Agg": agg, "Names": names}, db="ODS")(report, name)

    def getThoseWhoGraduatedInBiology(self):
        query = f"""
        SELECT *
        FROM SPT_STUDENT_PROGRAMS
        JOIN ODS_TERMS AS GRADUATING_TERM ON TERMS_ID = '2025SP'
        WHERE STPR_CURRENT_STATUS = 'G'
        AND END_DATE <= GRADUATING_TERM.TERM_END_DATE
        AND END_DATE >= GRADUATING_TERM.TERM_START_DATE
        AND STPR_ACAD_PROGRAM = 'BIOL.BA'
        """
        report = "2025-09-08-2025 Graduating Class Statistics"
        name = "Those That Graduated With A Biology Degree"
        agg = lambda query: f"""
        SELECT COUNT(*) AS NUMBER_THAT_GRADUATED_WITH_BIOLOGY FROM ({query}) AS X
        """
        names = lambda query: f"""
        SELECT STUDENT_PROGRAMS_ID, STPR_STUDENT, FIRST_NAME, LAST_NAME,  STPR_ACAD_PROGRAM
        FROM ({query}) AS X JOIN ODS_PERSON P ON X.STPR_STUDENT = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        self.save_query_results(query, {"Agg": agg, "Names": names}, db="ODS")(report, name)

    def getThoseStudentsFoundWhoGotSumma(self):
        query = f"""
        SELECT STUDENT_PROGRAMS_ID,
        STPR_STUDENT,
        STPR_ACAD_PROGRAM,
        CASE WHEN (DATEDIFF(DAY, START_DATE, END_DATE) / 365.25 <= 3) THEN 1 ELSE 0 END AS GRADUATED_IN_THREE_YEARS,
        CASE WHEN (STPR_ACAD_PROGRAM = 'BIOL.BA') THEN 1 ELSE 0 END AS BIOLOGY_DEGREE
        FROM SPT_STUDENT_PROGRAMS
        JOIN ODS_TERMS AS GRADUATING_TERM ON TERMS_ID = '2025SP'
        JOIN ODS_ACAD_CREDENTIALS 
            ON STPR_STUDENT = ACAD_PERSON_ID
            AND ACAD_INSTITUTIONS_ID = '5000000'
            AND END_DATE = ACAD_END_DATE
        WHERE STPR_CURRENT_STATUS = 'G'
        AND END_DATE <= GRADUATING_TERM.TERM_END_DATE
        AND END_DATE >= GRADUATING_TERM.TERM_START_DATE
        AND (DATEDIFF(DAY, START_DATE, END_DATE) / 365.25 <= 3 OR STPR_ACAD_PROGRAM = 'BIOL.BA')
        AND HONORS_1_DESC = 'Summa Cum Laude'
        """
        report = "2025-09-08-2025 Graduating Class Statistics"
        name = "Of Those Students, The Number With Summ Cum Laude"
        agg = lambda query: f"""
        SELECT SUM(GRADUATED_IN_THREE_YEARS) AS NUMBER_GRADUATED_IN_THREE_YEARS,
               SUM(BIOLOGY_DEGREE) AS NUMBER_THAT_GRADUATED_WITH_BIOLOGY FROM ({query}) AS X
        """
        self.print_table(query, db='ODS')
        names = lambda query: f"""
        SELECT STUDENT_PROGRAMS_ID, 
        STPR_STUDENT, 
        FIRST_NAME, 
        LAST_NAME,  
        STPR_ACAD_PROGRAM, 
        GRADUATED_IN_THREE_YEARS,
        BIOLOGY_DEGREE
        FROM ({query}) AS X JOIN ODS_PERSON P ON X.STPR_STUDENT = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        self.save_query_results(query, {"Agg": agg, "Names": names}, db="ODS")(report, name)


    def threeYearGradBiologySumma(self):
        query = f"""
        --(Begin 1)----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STPR_STUDENT,
        CASE WHEN (DATEDIFF(DAY, START_DATE, END_DATE) / 365.25 <= 3) THEN 'Yes' ELSE 'No' END AS GRADUATED_IN_THREE_YEARS,
        CASE WHEN (STPR_ACAD_PROGRAM = 'BIOL.BA') THEN 'Yes' ELSE 'No' END AS BIOLOGY_DEGREE,
        CASE WHEN HONORS_1_DESC = 'Summa Cum Laude' THEN 'Yes' ELSE 'No' END AS SUMMA_CUM_LAUDE
        FROM SPT_STUDENT_PROGRAMS
        JOIN ODS_TERMS AS GRADUATING_TERM ON TERMS_ID = '2025SP'
        JOIN ODS_ACAD_CREDENTIALS 
            ON STPR_STUDENT = ACAD_PERSON_ID
            AND ACAD_INSTITUTIONS_ID = '5000000'
            AND END_DATE = ACAD_END_DATE
        WHERE STPR_CURRENT_STATUS = 'G'
        AND END_DATE <= GRADUATING_TERM.TERM_END_DATE
        AND END_DATE >= GRADUATING_TERM.TERM_START_DATE
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        report = "2025-09-08-2025 Graduating Class Statistics"
        name = "Stats on 2025SP Graduated Students"
        agg = lambda query: f"""
        SELECT  GRADUATED_IN_THREE_YEARS,
                BIOLOGY_DEGREE,
                SUMMA_CUM_LAUDE,
                COUNT(*) AS STUDENT_COUNT FROM ({query}) 
                AS X GROUP BY GRADUATED_IN_THREE_YEARS,
                BIOLOGY_DEGREE,
                SUMMA_CUM_LAUDE
                ORDER BY GRADUATED_IN_THREE_YEARS DESC,
                BIOLOGY_DEGREE DESC,
                SUMMA_CUM_LAUDE DESC
        """
        names = lambda query: f"""
        SELECT 
        STPR_STUDENT, 
        FIRST_NAME, 
        LAST_NAME,  
        GRADUATED_IN_THREE_YEARS,
        BIOLOGY_DEGREE,
        SUMMA_CUM_LAUDE
        FROM ({query}) AS X JOIN ODS_PERSON P ON X.STPR_STUDENT = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        self.save_query_results(query, {"Agg": agg, "Names": names}, db="ODS")(report, name)









