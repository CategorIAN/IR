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
    Name: 2025-02-05-Average GPA of Current Students Who Are Not Athletes
    Person: Charles Gross
    Start Date: 2025-02-05
    End Date: 2025-02-11
    Description:
        I needed the average GPA of students who are not athletes.
    '''
    def avgGPAofNonAthletes(self):
        query = f"""
        SELECT Avg([STUDENT_OVERALL_CUM_GPA]) AS AVG_CUMULATIVE_GPA,
		Avg([STUDENT_TERM_GPA]) AS AVG_TERM_GPA_2024FA
        FROM [PERSON]
        JOIN [STUDENT_CUM_GPA_VIEW] ON PERSON.ID = STUDENT_CUM_GPA_VIEW.STUDENT_ID
        JOIN [STUDENT_TERM_GPA_VIEW] ON PERSON.ID = STUDENT_TERM_GPA_VIEW.STUDENT_ID
        Left JOIN [STA_OTHER_COHORTS_VIEW] ON PERSON.ID = STA_OTHER_COHORTS_VIEW.STA_STUDENT
        WHERE STUDENT_TERM_GPA_VIEW.TERM = '2024FA' and
              (
                STA_OTHER_COHORT_GROUPS IN ('HNRS', 'FOR', 'ROTC', 'VETS', 'INTL', 'ACCESS', 
                'CIC', 'GRSET', 'GRSUA', 'GRSMX') OR 
                STA_OTHER_COHORT_GROUPS IS NULL OR
                STA_OTHER_COHORT_END_DATES < GETDATE()
             )
        """
        report = "2025-02-05-Average GPA of Current Students Who Are Not Athletes"
        name = "Average GPA of Non Athletes"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-02-11-GPA and Athlete Status of Each Current Student
    Person: Rebecca Schwartz
    Start Date: 2025-02-11
    End Date: 2025-02-11
    Description:
        I needed to find the GPA and Athlete Status of each current student.
    '''
    def getGPAAndAthleteStatus(self):
        query = f"""
        SELECT  ID,
		LAST_NAME,
		FIRST_NAME,
		STUDENT_OVERALL_CUM_GPA AS CUMULATIVE_GPA,
		STUDENT_TERM_GPA AS TERM_GPA_2024FA,
		CASE 
			WHEN 
			EXISTS (
				SELECT 1
				FROM [STA_OTHER_COHORTS_VIEW]
				WHERE STA_STUDENT = ID
				AND STA_OTHER_COHORT_GROUPS IN (
				'FTBL', 'SOW', 'XCW', 'OTRKM', 'ITRKM', 
				'XCM', 'GOLW', 'BBM', 'CHER', 'GOLM', 
				'VBW', 'BBW', 'ITRKW', 'OTRKW', 'SOFBW', 
				'SOM', 'VBWJV', 'BBWJV', 'SOMJV','BBMJV', 
				'DNCE') and (STA_OTHER_COHORT_END_DATES is NULL or STA_OTHER_COHORT_END_DATES > GETDATE())
			) THEN 'Athlete'
			ELSE 'Non-Athlete'
		END AS Athlete_Status
        FROM [PERSON]
        JOIN [STUDENT_CUM_GPA_VIEW] ON PERSON.ID = STUDENT_CUM_GPA_VIEW.STUDENT_ID
        JOIN [STUDENT_TERM_GPA_VIEW] ON PERSON.ID = STUDENT_TERM_GPA_VIEW.STUDENT_ID
        WHERE STUDENT_TERM_GPA_VIEW.TERM = '2024FA'
        GROUP BY ID, LAST_NAME, FIRST_NAME, STUDENT_OVERALL_CUM_GPA, STUDENT_TERM_GPA
        Order By Athlete_Status, LAST_NAME, FIRST_NAME
        """
        report = "2025-02-11-GPA and Athlete Status of Each Current Student"
        name = "Student GPA and Athlete Status"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-02-12-Enrollment Size of Each Course By Term, Instructor, Section Since 2021FA
    Person: Rebecca Schwartz
    Start Date: 2025-02-12
    End Date: 2025-02-13
    Description:
        I needed to find the enrollment size of each course section by faculty since 2021FA
    '''
    def getCourseSectionStudentCount(self):
        query = f"""
        Select CS.SEC_TERM,
        CS.SEC_NAME,
        CS.SEC_SHORT_TITLE,
        CS.SEC_FACULTY_INFO,
        CSCV.COUNT_ACTIVE_STUDENTS
        FROM COURSE_SECTIONS AS CS
            JOIN COURSE_SECTIONS_COUNT_VIEW  AS CSCV ON CS.COURSE_SECTIONS_ID = CSCV.COURSE_SECTIONS_ID
        WHERE SEC_START_DATE >= '2021-08-01'
        ORDER BY SEC_START_DATE
        """
        report = "2025-02-12-Enrollment Size of Each Course By Term, Instructor, Section Since 2021FA"
        name = "Course Section Student Count"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-02-13-Current Student List By Major and Minor
    Person: Carol Schopfer
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
        SELECT NURSING_PROGRAM, COUNT(*) AS STUDENT_COUNT FROM ({query}) AS STUDENT_MAJORS
        GROUP BY NURSING_PROGRAM ORDER BY NURSING_PROGRAM
        """
        names = lambda query: f"""
        SELECT STUDENT_ID, LAST_NAME, FIRST_NAME, PERSON_EMAIL_ADDRESSES AS EMAIL, NURSING_PROGRAM
        FROM ({query}) AS STUDENT_MAJORS JOIN PERSON ON STUDENT_MAJORS.STUDENT_ID = PERSON.ID
        JOIN PEOPLE_EMAIL ON STUDENT_MAJORS.STUDENT_ID = PEOPLE_EMAIL.ID
        WHERE PERSON_PREFERRED_EMAIL = 'Y'
        ORDER BY NURSING_PROGRAM, LAST_NAME, FIRST_NAME
        """
        report = "2025-02-13-Current Student List By Major and Minor"
        name = "Current Nursing Students By Program"
        self.save_query_results(query, func_dict={"Agg": agg, "Names": names}, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-02-18-Retention Analysis
    Person: Rebecca Schwartz
    Start Date: 2025-02-18
    End Date: 2025-02-20
    Description:
        I needed to analyze retention.
    '''
    def getEnrollmentByTerm(self):
        query = f"""
        SELECT ENROLL_TERM AS TERM
		,COUNT(*) AS ENROLLMENT
        FROM (
                SELECT ENROLL_TERM
                        ,STUDENT_ID
                FROM STUDENT_ENROLLMENT_VIEW
                WHERE ENROLL_CURRENT_STATUS = 'New'
                GROUP BY ENROLL_TERM
                        ,STUDENT_ID
                ) AS TERM_STUDENTS
        WHERE ENROLL_TERM IN ('2022FA', '2023SP', '2023FA', '2024SP', '2024FA', '2025SP')
        GROUP BY ENROLL_TERM
        ORDER BY ENROLL_TERM
        """
        report = "2025-02-18-Retention Analysis"
        name = "Enrollment By Term"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getLostIn2024SP(self):
        query = f"""
        SELECT *
        FROM (
            SELECT	PERSON.ID
                    ,PERSON.LAST_NAME
                    ,PERSON.FIRST_NAME
                    ,TERM_2023SP.STUDENT_ID AS TERM_2023SP
                    ,TERM_2024SP.STUDENT_ID AS TERM_2024SP
                    ,LATEST_STATUS.STP_CURRENT_STATUS AS LATEST_STATUS
                    ,LATEST_STATUS.STP_CURRENT_STATUS_DATE AS LATEST_STATUS_DATE
            FROM PERSON
            JOIN (
                    SELECT STUDENT_ID, STP_CURRENT_STATUS, STP_CURRENT_STATUS_DATE
                    FROM (
                        SELECT STUDENT_ID
                        ,STP_CURRENT_STATUS
                        ,STP_CURRENT_STATUS_DATE
                        ,ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_CURRENT_STATUS_DATE DESC) AS rn
                        FROM STUDENT_ACAD_PROGRAMS_VIEW
                        WHERE STP_CURRENT_STATUS != 'Changed Program'
                    ) ranked
                    WHERE rn = 1
                    ) AS LATEST_STATUS ON LATEST_STATUS.STUDENT_ID = PERSON.ID
            JOIN (
                    SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW 
                    WHERE ENROLL_TERM = '2023SP'
                    AND ENROLL_CURRENT_STATUS NOT IN ('Deleted', 'Dropped', 'Withdrawn', 'Transfer Equiv Eval')
                  ) AS TERM_2023SP ON PERSON.ID = TERM_2023SP.STUDENT_ID
            LEFT JOIN (
                        SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW 
                        WHERE ENROLL_TERM = '2024SP'
                        AND ENROLL_CURRENT_STATUS NOT IN ('Deleted', 'Dropped', 'Withdrawn', 'Transfer Equiv Eval')
                    ) AS TERM_2024SP ON PERSON.ID = TERM_2024SP.STUDENT_ID
            WHERE TERM_2024SP.STUDENT_ID IS NULL
        ) AS LOST_IN_2024
        ORDER BY LATEST_STATUS, LATEST_STATUS_DATE, LAST_NAME, FIRST_NAME
        """
        report = "2025-02-18-Retention Analysis"
        name = "Lost In 2024SP"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getLostIn2025SP(self):
        query = f"""
        SELECT *
        FROM (
            SELECT	PERSON.ID
                    ,PERSON.LAST_NAME
                    ,PERSON.FIRST_NAME
                    ,TERM_2024SP.STUDENT_ID AS TERM_2024SP
                    ,TERM_2025SP.STUDENT_ID AS TERM_2025SP
                    ,LATEST_STATUS.STP_CURRENT_STATUS AS LATEST_STATUS
                    ,LATEST_STATUS.STP_CURRENT_STATUS_DATE AS LATEST_STATUS_DATE
            FROM PERSON
            JOIN (
                    SELECT STUDENT_ID, STP_CURRENT_STATUS, STP_CURRENT_STATUS_DATE
                    FROM (
                        SELECT STUDENT_ID
                        ,STP_CURRENT_STATUS
                        ,STP_CURRENT_STATUS_DATE
                        ,ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_CURRENT_STATUS_DATE DESC) AS rn
                        FROM STUDENT_ACAD_PROGRAMS_VIEW
                        WHERE STP_CURRENT_STATUS != 'Changed Program'
                    ) ranked
                    WHERE rn = 1
                    ) AS LATEST_STATUS ON LATEST_STATUS.STUDENT_ID = PERSON.ID
            JOIN (
                    SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW 
                    WHERE ENROLL_TERM = '2024SP'
                    AND ENROLL_CURRENT_STATUS NOT IN ('Deleted', 'Dropped', 'Withdrawn', 'Transfer Equiv Eval')
                  ) AS TERM_2024SP ON PERSON.ID = TERM_2024SP.STUDENT_ID
            LEFT JOIN (
                        SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW 
                        WHERE ENROLL_TERM = '2025SP'
                        AND ENROLL_CURRENT_STATUS NOT IN ('Deleted', 'Dropped', 'Withdrawn', 'Transfer Equiv Eval')
                    ) AS TERM_2025SP ON PERSON.ID = TERM_2025SP.STUDENT_ID
            WHERE TERM_2025SP.STUDENT_ID IS NULL
        ) AS LOST_IN_2025
        ORDER BY LATEST_STATUS, LATEST_STATUS_DATE, LAST_NAME, FIRST_NAME
        """
        report = "2025-02-18-Retention Analysis"
        name = "Lost In 2025SP"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getStudentsForEachTerm(self):
        query = f"""
        SELECT PERSON.ID,
		PERSON.LAST_NAME,
		PERSON.FIRST_NAME,
		(CASE WHEN TERM_2022FA.STUDENT_ID IS NOT NULL THEN 1 ELSE 0 END) AS TERM_2022FA,
		(CASE WHEN TERM_2023SP.STUDENT_ID IS NOT NULL THEN 1 ELSE 0 END) AS TERM_2023SP,
		(CASE WHEN TERM_2023FA.STUDENT_ID IS NOT NULL THEN 1 ELSE 0 END) AS TERM_2023FA,
		(CASE WHEN TERM_2024SP.STUDENT_ID IS NOT NULL THEN 1 ELSE 0 END) AS TERM_2024SP,
		(CASE WHEN TERM_2024FA.STUDENT_ID IS NOT NULL THEN 1 ELSE 0 END) AS TERM_2024FA,
		(CASE WHEN TERM_2025SP.STUDENT_ID IS NOT NULL THEN 1 ELSE 0 END) AS TERM_2025SP
        FROM (
		SELECT DISTINCT STUDENT_ID
		FROM STUDENT_ENROLLMENT_VIEW
		WHERE ENROLL_CURRENT_STATUS = 'New'
		AND ENROLL_TERM IN ('2022FA', '2023SP', '2023FA', '2024SP', '2024FA', '2025SP')
		) AS TERM_STUDENTS
        JOIN PERSON ON TERM_STUDENTS.STUDENT_ID = PERSON.ID
        LEFT JOIN (SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW WHERE ENROLL_TERM = '2022FA' AND ENROLL_CURRENT_STATUS = 'New') AS TERM_2022FA ON TERM_STUDENTS.STUDENT_ID = TERM_2022FA.STUDENT_ID
        LEFT JOIN (SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW WHERE ENROLL_TERM = '2023SP' AND ENROLL_CURRENT_STATUS = 'New') AS TERM_2023SP ON TERM_STUDENTS.STUDENT_ID = TERM_2023SP.STUDENT_ID
        LEFT JOIN (SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW WHERE ENROLL_TERM = '2023FA' AND ENROLL_CURRENT_STATUS = 'New') AS TERM_2023FA ON TERM_STUDENTS.STUDENT_ID = TERM_2023FA.STUDENT_ID
        LEFT JOIN (SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW WHERE ENROLL_TERM = '2024SP' AND ENROLL_CURRENT_STATUS = 'New') AS TERM_2024SP ON TERM_STUDENTS.STUDENT_ID = TERM_2024SP.STUDENT_ID
        LEFT JOIN (SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW WHERE ENROLL_TERM = '2024FA' AND ENROLL_CURRENT_STATUS = 'New') AS TERM_2024FA ON TERM_STUDENTS.STUDENT_ID = TERM_2024FA.STUDENT_ID
        LEFT JOIN (SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW WHERE ENROLL_TERM = '2025SP' AND ENROLL_CURRENT_STATUS = 'New') AS TERM_2025SP ON TERM_STUDENTS.STUDENT_ID = TERM_2025SP.STUDENT_ID
        ORDER BY TERM_2022FA DESC
                 ,TERM_2023SP DESC
                 ,TERM_2023FA DESC
                 ,TERM_2024SP DESC
                 ,TERM_2024FA DESC
                 ,TERM_2025SP DESC
                 ,LAST_NAME
                ,FIRST_NAME
        """
        report = "2025-02-18-Retention Analysis"
        name = "Students For Each Term"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getTerm2022FAto2023SP(self):
        query = f"""
        SELECT *
        FROM (
            SELECT	PERSON.ID
                    ,PERSON.LAST_NAME
                    ,PERSON.FIRST_NAME
                    ,LATEST_STATUS.STP_PROGRAM_TITLE AS LATEST_PROGRAM
                    ,LATEST_STATUS.STP_CURRENT_STATUS AS LATEST_STATUS
                    ,LATEST_STATUS.STP_END_DATE AS LATEST_STATUS_DATE
                    ,TERM_2022FA.STUDENT_ID AS TERM_2022FA
                    ,TERM_2023SP.STUDENT_ID AS TERM_2023SP
                    ,TERM_2023FA.STUDENT_ID AS TERM_2023FA
                    ,TERM_2024SP.STUDENT_ID AS TERM_2024SP
                    ,TERM_2024FA.STUDENT_ID AS TERM_2024FA
                    ,TERM_2025SP.STUDENT_ID AS TERM_2025SP
            FROM PERSON
            JOIN (
                    SELECT STUDENT_ID, STP_PROGRAM_TITLE, STP_CURRENT_STATUS, STP_END_DATE
                    FROM (
                        SELECT STUDENT_ID
                        ,STP_CURRENT_STATUS
                        ,STP_END_DATE
                        ,STP_PROGRAM_TITLE
                        ,ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
                        FROM STUDENT_ACAD_PROGRAMS_VIEW
                        WHERE STP_CURRENT_STATUS != 'Changed Program'
                        AND STP_START_DATE IS NOT NULL
                    ) ranked
                    WHERE rn = 1
                    ) AS LATEST_STATUS ON LATEST_STATUS.STUDENT_ID = PERSON.ID
            JOIN (
                    SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW 
                    WHERE ENROLL_TERM = '2022FA'
                    AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                  ) AS TERM_2022FA ON PERSON.ID = TERM_2022FA.STUDENT_ID
            LEFT JOIN (
                        SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW 
                        WHERE ENROLL_TERM = '2023SP'
                        AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                    ) AS TERM_2023SP ON PERSON.ID = TERM_2023SP.STUDENT_ID
            LEFT JOIN (
                        SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                        WHERE ENROLL_TERM = '2023FA'
                        AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                    ) AS TERM_2023FA ON PERSON.ID = TERM_2023FA.STUDENT_ID
            LEFT JOIN (
                    SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                    WHERE ENROLL_TERM = '2024SP'
                    AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                ) AS TERM_2024SP ON PERSON.ID = TERM_2024SP.STUDENT_ID
            LEFT JOIN (
                SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                WHERE ENROLL_TERM = '2024FA'
                AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
            ) AS TERM_2024FA ON PERSON.ID = TERM_2024FA.STUDENT_ID
            LEFT JOIN (
                SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                WHERE ENROLL_TERM = '2025SP'
                AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
            ) AS TERM_2025SP ON PERSON.ID = TERM_2025SP.STUDENT_ID
            WHERE TERM_2023SP.STUDENT_ID IS NULL
        ) AS LOST
        ORDER BY LATEST_STATUS, LATEST_STATUS_DATE, LAST_NAME, FIRST_NAME
        """
        report = "2025-02-18-Retention Analysis"
        name = "TERM2022FA to TERM2023SP"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getTerm2023FAto2024SP(self):
        query = f"""
        SELECT *
        FROM (
            SELECT	PERSON.ID
                    ,PERSON.LAST_NAME
                    ,PERSON.FIRST_NAME
                    ,LATEST_STATUS.STP_PROGRAM_TITLE AS LATEST_PROGRAM
                    ,LATEST_STATUS.STP_CURRENT_STATUS AS LATEST_STATUS
                    ,LATEST_STATUS.STP_END_DATE AS LATEST_STATUS_DATE
                    ,TERM_2023FA.STUDENT_ID AS TERM_2023FA
                    ,TERM_2024SP.STUDENT_ID AS TERM_2024SP
                    ,TERM_2024FA.STUDENT_ID AS TERM_2024FA
                    ,TERM_2025SP.STUDENT_ID AS TERM_2025SP
            FROM PERSON
            JOIN (
                    SELECT STUDENT_ID, STP_PROGRAM_TITLE, STP_CURRENT_STATUS, STP_END_DATE
                    FROM (
                        SELECT STUDENT_ID
                        ,STP_CURRENT_STATUS
                        ,STP_END_DATE
                        ,STP_PROGRAM_TITLE
                        ,ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
                        FROM STUDENT_ACAD_PROGRAMS_VIEW
                        WHERE STP_CURRENT_STATUS != 'Changed Program'
                        AND STP_START_DATE IS NOT NULL
                    ) ranked
                    WHERE rn = 1
                    ) AS LATEST_STATUS ON LATEST_STATUS.STUDENT_ID = PERSON.ID
            JOIN (
                        SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                        WHERE ENROLL_TERM = '2023FA'
                        AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                    ) AS TERM_2023FA ON PERSON.ID = TERM_2023FA.STUDENT_ID
            LEFT JOIN (
                    SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                    WHERE ENROLL_TERM = '2024SP'
                    AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                ) AS TERM_2024SP ON PERSON.ID = TERM_2024SP.STUDENT_ID
            LEFT JOIN (
                SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                WHERE ENROLL_TERM = '2024FA'
                AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
            ) AS TERM_2024FA ON PERSON.ID = TERM_2024FA.STUDENT_ID
            LEFT JOIN (
                SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                WHERE ENROLL_TERM = '2025SP'
                AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
            ) AS TERM_2025SP ON PERSON.ID = TERM_2025SP.STUDENT_ID
            
        
            WHERE TERM_2024SP.STUDENT_ID IS NULL
        ) AS LOST
        ORDER BY LATEST_STATUS, LATEST_PROGRAM, LATEST_STATUS_DATE, LAST_NAME, FIRST_NAME
        """
        report = "2025-02-18-Retention Analysis"
        name = "TERM2023FA to TERM2024SP"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getTerm2023SPto2023FA(self):
        query = f"""
        SELECT *
        FROM (
            SELECT	PERSON.ID
                    ,PERSON.LAST_NAME
                    ,PERSON.FIRST_NAME
                    ,LATEST_STATUS.STP_PROGRAM_TITLE AS LATEST_PROGRAM
                    ,LATEST_STATUS.STP_CURRENT_STATUS AS LATEST_STATUS
                    ,LATEST_STATUS.STP_END_DATE AS LATEST_STATUS_DATE
                    ,TERM_2023SP.STUDENT_ID AS TERM_2023SP
                    ,TERM_2023FA.STUDENT_ID AS TERM_2023FA
                    ,TERM_2024SP.STUDENT_ID AS TERM_2024SP
                    ,TERM_2024FA.STUDENT_ID AS TERM_2024FA
                    ,TERM_2025SP.STUDENT_ID AS TERM_2025SP
            FROM PERSON
            JOIN (
                    SELECT STUDENT_ID, STP_PROGRAM_TITLE, STP_CURRENT_STATUS, STP_END_DATE
                    FROM (
                        SELECT STUDENT_ID
                        ,STP_CURRENT_STATUS
                        ,STP_END_DATE
                        ,STP_PROGRAM_TITLE
                        ,ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
                        FROM STUDENT_ACAD_PROGRAMS_VIEW
                        WHERE STP_CURRENT_STATUS != 'Changed Program'
                        AND STP_START_DATE IS NOT NULL
                    ) ranked
                    WHERE rn = 1
                    ) AS LATEST_STATUS ON LATEST_STATUS.STUDENT_ID = PERSON.ID
            JOIN (
                        SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW 
                        WHERE ENROLL_TERM = '2023SP'
                        AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                    ) AS TERM_2023SP ON PERSON.ID = TERM_2023SP.STUDENT_ID
            LEFT JOIN (
                        SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                        WHERE ENROLL_TERM = '2023FA'
                        AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                    ) AS TERM_2023FA ON PERSON.ID = TERM_2023FA.STUDENT_ID
            LEFT JOIN (
                    SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                    WHERE ENROLL_TERM = '2024SP'
                    AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                ) AS TERM_2024SP ON PERSON.ID = TERM_2024SP.STUDENT_ID
            LEFT JOIN (
                SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                WHERE ENROLL_TERM = '2024FA'
                AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
            ) AS TERM_2024FA ON PERSON.ID = TERM_2024FA.STUDENT_ID
            LEFT JOIN (
                SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                WHERE ENROLL_TERM = '2025SP'
                AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
            ) AS TERM_2025SP ON PERSON.ID = TERM_2025SP.STUDENT_ID
            
        
            WHERE TERM_2023FA.STUDENT_ID IS NULL
        ) AS LOST
        ORDER BY LATEST_STATUS, LATEST_PROGRAM, LATEST_STATUS_DATE, LAST_NAME, FIRST_NAME
        """
        report = "2025-02-18-Retention Analysis"
        name = "TERM2023SP to TERM2023FA"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getTerm2024FAto2025SP(self):
        query = f"""
        SELECT *
        FROM (
            SELECT	PERSON.ID
                    ,PERSON.LAST_NAME
                    ,PERSON.FIRST_NAME
                    ,LATEST_STATUS.STP_PROGRAM_TITLE AS LATEST_PROGRAM
                    ,LATEST_STATUS.STP_CURRENT_STATUS AS LATEST_STATUS
                    ,LATEST_STATUS.STP_END_DATE AS LATEST_STATUS_DATE
                    ,TERM_2024FA.STUDENT_ID AS TERM_2024FA
                    ,TERM_2025SP.STUDENT_ID AS TERM_2025SP
            FROM PERSON
            JOIN (
                    SELECT STUDENT_ID, STP_PROGRAM_TITLE, STP_CURRENT_STATUS, STP_END_DATE
                    FROM (
                        SELECT STUDENT_ID
                        ,STP_CURRENT_STATUS
                        ,STP_END_DATE
                        ,STP_PROGRAM_TITLE
                        ,ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
                        FROM STUDENT_ACAD_PROGRAMS_VIEW
                        WHERE STP_CURRENT_STATUS != 'Changed Program'
                        AND STP_START_DATE IS NOT NULL
                    ) ranked
                    WHERE rn = 1
                    ) AS LATEST_STATUS ON LATEST_STATUS.STUDENT_ID = PERSON.ID
            JOIN (
                SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                WHERE ENROLL_TERM = '2024FA'
                AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
            ) AS TERM_2024FA ON PERSON.ID = TERM_2024FA.STUDENT_ID
            LEFT JOIN (
                SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                WHERE ENROLL_TERM = '2025SP'
                AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
            ) AS TERM_2025SP ON PERSON.ID = TERM_2025SP.STUDENT_ID
            
        
            WHERE TERM_2025SP.STUDENT_ID IS NULL
        ) AS LOST
        ORDER BY LATEST_STATUS, LATEST_PROGRAM, LATEST_STATUS_DATE, LAST_NAME, FIRST_NAME
        """
        report = "2025-02-18-Retention Analysis"
        name = "TERM2024FA to TERM2025SP"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getTerm2024SPto2024FA(self):
        query = f"""
        SELECT *
        FROM (
            SELECT	PERSON.ID
                    ,PERSON.LAST_NAME
                    ,PERSON.FIRST_NAME
                    ,LATEST_STATUS.STP_PROGRAM_TITLE AS LATEST_PROGRAM
                    ,LATEST_STATUS.STP_CURRENT_STATUS AS LATEST_STATUS
                    ,LATEST_STATUS.STP_END_DATE AS LATEST_STATUS_DATE
                    ,TERM_2024SP.STUDENT_ID AS TERM_2024SP
                    ,TERM_2024FA.STUDENT_ID AS TERM_2024FA
                    ,TERM_2025SP.STUDENT_ID AS TERM_2025SP
            FROM PERSON
            JOIN (
                    SELECT STUDENT_ID, STP_PROGRAM_TITLE, STP_CURRENT_STATUS, STP_END_DATE
                    FROM (
                        SELECT STUDENT_ID
                        ,STP_CURRENT_STATUS
                        ,STP_END_DATE
                        ,STP_PROGRAM_TITLE
                        ,ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
                        FROM STUDENT_ACAD_PROGRAMS_VIEW
                        WHERE STP_CURRENT_STATUS != 'Changed Program'
                        AND STP_START_DATE IS NOT NULL
                    ) ranked
                    WHERE rn = 1
                    ) AS LATEST_STATUS ON LATEST_STATUS.STUDENT_ID = PERSON.ID
            JOIN (
                    SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                    WHERE ENROLL_TERM = '2024SP'
                    AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                ) AS TERM_2024SP ON PERSON.ID = TERM_2024SP.STUDENT_ID
            LEFT JOIN (
                SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                WHERE ENROLL_TERM = '2024FA'
                AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
            ) AS TERM_2024FA ON PERSON.ID = TERM_2024FA.STUDENT_ID
            LEFT JOIN (
                SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
                WHERE ENROLL_TERM = '2025SP'
                AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
            ) AS TERM_2025SP ON PERSON.ID = TERM_2025SP.STUDENT_ID
            WHERE TERM_2024FA.STUDENT_ID IS NULL
        ) AS LOST
        ORDER BY LATEST_STATUS, LATEST_PROGRAM, LATEST_STATUS_DATE, LAST_NAME, FIRST_NAME
        """
        report = "2025-02-18-Retention Analysis"
        name = "TERM2024SP to TERM2024FA"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)


    '''
    ID: Unknown
    Name: 2025-02-19-Count and Average GPA of Recent Business Students
    Person: Dagim Degaro
    Start Date: 2025-02-19
    End Date: 2025-02-20
    Description:
        I needed the count and average GPA of Recent Business Students
    '''
    def getBusinessStudentCountAndAvgGPA(self):
        query = f"""
        SELECT  TERM
		,MAJOR
		,COUNT(*) AS STUDENT_COUNT
        FROM (
                SELECT PERSON.ID,
                        LAST_NAME,
                        FIRST_NAME,
                        MAJORS.MAJ_DESC AS MAJOR,
                        STTR_TERM AS TERM
                FROM PERSON
                JOIN (
                        SELECT STTR_STUDENT
                                ,STTR_TERM
                        FROM STUDENT_TERMS_VIEW
                        WHERE STTR_TERM IN ('2021FA', '2022SP', '2022FA', '2023SP', '2023FA', '2024SP', '2024FA', '2025SP')
                    ) RECENT_STUDENTS ON PERSON.ID = RECENT_STUDENTS.STTR_STUDENT
                JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV ON PERSON.ID = SAPV.STUDENT_ID
                CROSS JOIN MAJORS
                LEFT JOIN STPR_MAJOR_LIST_VIEW ON SAPV.STUDENT_ID = STPR_MAJOR_LIST_VIEW.STPR_STUDENT AND SAPV.STP_ACADEMIC_PROGRAM = STPR_MAJOR_LIST_VIEW.STPR_ACAD_PROGRAM
                LEFT JOIN MAJORS AS ADDNL_MAJOR ON STPR_MAJOR_LIST_VIEW.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                WHERE MAJORS.MAJ_DESC IN ('Business: Managmt and Marktng', 'Business: Financial Planning', 'Business: Acctng & Stratg Finc')
                AND (
                        MAJORS.MAJ_DESC = MAIN_MAJOR.MAJ_DESC
                        OR (
                            MAJORS.MAJ_DESC = ADDNL_MAJOR.MAJ_DESC
                            AND STPR_MAJOR_LIST_VIEW.STPR_ADDNL_MAJOR_END_DATE IS NULL
                            )
                    )
        
                GROUP BY ID, LAST_NAME, FIRST_NAME, MAJORS.MAJ_DESC, STTR_TERM
            ) AS X
        GROUP BY TERM, MAJOR
        ORDER BY TERM, MAJOR
        """
        report = "2025-02-19-Count and Average GPA of Recent Business Students"
        name = "Business Student Count and Avg GPA"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-02-27-Demographics for Financial Planning Majors
    Person: Julia Mull
    Start Date: 2025-02-27
    End Date: 2025-02-28
    Description:
        I needed to find the demographics for financial planning majors.
    '''
    def getDemographicsForFinancialPlanningMajors(self):
        query = f"""
        SELECT *
        FROM (
                 (SELECT STUDENT_ID,
                         LAST_NAME,
                         FIRST_NAME,
                         GENDER
                  FROM (SELECT STUDENT_ID
                        FROM (SELECT * FROM STUDENT_ACAD_PROGRAMS_VIEW
                                WHERE STP_CURRENT_STATUS = 'Active'
                                AND STP_ACAD_LEVEL = 'UG') AS SAPV
                                 LEFT JOIN STPR_MAJOR_LIST_VIEW ON SAPV.STUDENT_ID = STPR_MAJOR_LIST_VIEW.STPR_STUDENT AND
                                                                   SAPV.STP_ACADEMIC_PROGRAM =
                                                                   STPR_MAJOR_LIST_VIEW.STPR_ACAD_PROGRAM
                                 LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                 LEFT JOIN MAJORS AS ADDNL_MAJOR
                                           ON STPR_MAJOR_LIST_VIEW.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                        WHERE (
                            MAIN_MAJOR.MAJ_DESC = 'Business: Financial Planning'
                                OR (
                                ADDNL_MAJOR.MAJ_DESC = 'Business: Financial Planning'
                                    AND STPR_MAJOR_LIST_VIEW.STPR_ADDNL_MAJOR_END_DATE IS NULL
                                )
                            )
                          AND STP_START_DATE < '2025-05-01') AS FP_STUDENTS
                           JOIN PERSON ON FP_STUDENTS.STUDENT_ID = PERSON.ID) AS X
                     JOIN (SELECT *
                           FROM Z01_ALL_RACE_ETHNIC_W_FLAGS) AS Y ON X.STUDENT_ID = Y.ID
                 )
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-02-27-Demographics for Financial Planning Majors"
        name = "Demographics for Financial Planning Majors"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-03-18-FTE Count
    Person: Kaia Rosen
    Start Date: 2025-03-18
    End Date: 2025-03-26
    Description:
        I needed to calculate the FTE, which is the full-time equivalent.
    '''
    def getFTECount(self):
        query = f"""
        SELECT SUM(WEIGHT) AS FTE
        FROM (
        SELECT CASE
                   WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 1
                    ELSE 1.0/3 END AS WEIGHT
        FROM STUDENT_TERMS_VIEW AS STV
        WHERE STTR_TERM = '2025SP') AS X
        """
        report = "2025-03-18-FTE Count"
        name = "FTE Count"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-03-19-Information on MSW Students
    Person: Rebecca Schwartz
    Start Date: 2025-03-19
    End Date: 2025-03-31
    Description:
        I needed to find information on MSW Students.
    '''
    def getInfoOnMSWStudents(self):
        query = f"""
        SELECT * FROM (
        SELECT STUDENT_ID
        FROM PERSON
            JOIN (
                    SELECT STUDENT_ID, STP_PROGRAM_TITLE, STP_CURRENT_STATUS, STP_END_DATE
                    FROM (
                        SELECT STUDENT_ID
                        ,STP_CURRENT_STATUS
                        ,STP_END_DATE
                        ,STP_PROGRAM_TITLE
                        ,ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
                        FROM STUDENT_ACAD_PROGRAMS_VIEW
                        WHERE STP_CURRENT_STATUS != 'Changed Program'
                        AND STP_START_DATE IS NOT NULL
                    ) ranked
                    WHERE rn = 1
                    ) AS LATEST_STATUS ON LATEST_STATUS.STUDENT_ID = PERSON.ID
        WHERE STP_PROGRAM_TITLE = 'Master of Social Work'
        AND STP_END_DATE IS NULL) AS X
        JOIN PERSON ON X.STUDENT_ID = PERSON.ID
        """
        report = "2025-03-19-Information on MSW Students"
        name = "Information on MSW Students"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-03-24-Data Packet
    Person: Rebecca Schwartz
    Start Date: 2025-03-24
    End Date: 2025-04-02
    Description:
        I needed to create a data packet.
    '''
    def getStudentAthleteCounts(self):
        query = f"""
        SELECT ENROLL_TERM AS TERM,
           COUNT(*) AS STUDENT_COUNT,
           SUM(STUDENT_ATHLETE) AS STUDENT_ATHLETE_COUNT
        FROM (
        SELECT DISTINCT ENROLL_TERM,
               TERM_START_DATE,
               STUDENT_ID,
               CASE
                   WHEN EXISTS (
                       SELECT 1
                       FROM STA_OTHER_COHORTS_VIEW
                       WHERE STA_STUDENT = STUDENT_ID
                       AND STA_OTHER_COHORT_START_DATES < TERMS.TERM_END_DATE
                       AND (STA_OTHER_COHORT_END_DATES > TERMS.TERM_START_DATE
                                OR STA_OTHER_COHORT_END_DATES IS NULL)
                       AND STA_OTHER_COHORT_GROUPS IN (
                                                       'F',
                                                       'SOW',
                                                       'SOM',
                                                       'VB',
                                                       'BM',
                                                       'BW',
                                                       'XW',
                                                       'XM',
                                                       'GW',
                                                       'GM',
                                                       'C',
                                                       'D',
                                                       'ITM',
                                                       'ITW',
                                                       'OTM',
                                                       'OTW',
                                                       'SB',
                                                       'BWJ',
                                                       'VBJ',
                                                       'SOMJ',
                                                       'BMJ',
                                                       'DNC'
                                                        )
                   ) THEN 1 ELSE 0 END AS STUDENT_ATHLETE
        FROM STUDENT_ENROLLMENT_VIEW AS SEV
        JOIN TERMS ON SEV.ENROLL_TERM = TERMS.TERMS_ID
        WHERE TERMS.TERM_START_DATE >= DATEADD(year, -10, '2024-08-01')
        AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
        AND  (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
        AND (ENROLL_TERM LIKE '%FA' OR ENROLL_TERM LIKE '%SP')
        ) AS X
        GROUP BY ENROLL_TERM, TERM_START_DATE
        ORDER BY TERM_START_DATE
        """
        report = "2025-03-24-Data Packet"
        name = "Student Athlete Counts"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getStaffCounts(self):
        query = f"""
        SELECT PERSTAT_HRP_ID,
           GENDER,
           IPEDS_RACE_ETHNIC_DESC,
           ISNULL(POS_EEO_RANK, 'Unknown') as POS_EEO_RANK,
           PERSTAT_STATUS,
           POS_CLASS,
           PERSTAT_TENURE_TYPE
        FROM PERSTAT
        JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
        JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
        JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSTAT_HRP_ID = RACE.ID
        WHERE (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= GETDATE())
        """
        report = "2025-03-24-Data Packet"
        name = "Staff Counts"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getCampusResidency(self):
        query = f"""
                SELECT STTR_STUDENT,
               LAST_NAME,
               FIRST_NAME,
               ADDRESS.ADDRESS_ID,
               CITY,
               STATE,
               ZIP,
               ADDRESS_LS.ADDRESS_LINES
        FROM (
        SELECT STTR_STUDENT,
               LAST_NAME,
               FIRST_NAME,
               ADDRESS_ID
        FROM (
        SELECT STTR_STUDENT,
               P.LAST_NAME,
               P.FIRST_NAME,
               ADDRESS.ADDRESS_ID,
               ROW_NUMBER() OVER (PARTITION BY STTR_STUDENT ORDER BY ADDRESS_ADD_DATE DESC) AS rn
        
        FROM STUDENT_TERMS_VIEW AS STV
        JOIN PERSON AS P ON STV.STTR_STUDENT = P.ID
        JOIN PERSON_ADDRESSES_VIEW AS PAV  ON STV.STTR_STUDENT = PAV.ID
        JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
        WHERE STTR_TERM = '2024FA'
        AND ADDRESS_TYPE = 'CA'
        ) AS X WHERE rn = 1) AS X
        JOIN ADDRESS ON X.ADDRESS_ID = ADDRESS.ADDRESS_ID
        JOIN ADDRESS_LS ON X.ADDRESS_ID = ADDRESS_LS.ADDRESS_ID
        WHERE POS = 1
        """
        report = "2025-03-24-Data Packet"
        name = "Campus Residency"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getDemographics(self):
        query = f"""
                SELECT  STTR_STUDENT,
                LAST_NAME,
                FIRST_NAME,
                GENDER,
                RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
                CASE WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time' ELSE 'Part-Time' END AS LOAD,
                CASE
                    WHEN STTR_ACAD_LEVEL = 'GR' THEN 'Graduate'
                    WHEN STTR_ACAD_LEVEL = 'UG' THEN CASE
                    WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students' THEN 'Non-Degree Seeking Undergraduate'
                    WHEN FM.TERM = '2024FA' OR FM.TERM = '2025SP' THEN CASE
                        WHEN STPR_ADMIT_STATUS = 'FY' THEN 'First-time Undergraduate'
                        WHEN STPR_ADMIT_STATUS IN ('TR', 'RE') THEN 'Transfer-in Undergraduate' END
                    ELSE 'Continuing/Returning Undergraduate' END END AS STATUS
        
        FROM STUDENT_TERMS_VIEW AS STV
        JOIN PERSON ON STV.STTR_STUDENT = PERSON.ID
        JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
        LEFT JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STV.STTR_STUDENT = FM.ID
        LEFT JOIN (SELECT STPR_STUDENT, STPR_ADMIT_STATUS
                   FROM (
                       SELECT   STPR_STUDENT,
                                STPR_ADMIT_STATUS,
                                ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                                ORDER BY STUDENT_PROGRAMS_ADDDATE) AS rn
                       FROM STUDENT_PROGRAMS_VIEW
                       WHERE STPR_ADMIT_STATUS IN ('FY', 'TR', 'RE')
                       ) ranked
                       WHERE rn = 1) AS FIRST_ADMIT ON STV.STTR_STUDENT = FIRST_ADMIT.STPR_STUDENT
        JOIN (SELECT *
                   FROM (SELECT STUDENT_ID,
                                STP_ACADEMIC_PROGRAM,
                                STP_PROGRAM_TITLE,
                                STP_CURRENT_STATUS,
                                ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                                    ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
                         FROM STUDENT_ACAD_PROGRAMS_VIEW
                         WHERE STP_CURRENT_STATUS != 'Changed Program'
                         AND STP_START_DATE <= (SELECT TOP 1 TERMS.TERM_END_DATE
                                                FROM TERMS
                                                WHERE TERMS_ID = '2024FA')
                         ) ranked
                    WHERE rn = 1) AS SAPV ON STV.STTR_STUDENT = SAPV.STUDENT_ID
        WHERE STTR_TERM = '2024FA'
        """
        report = "2025-03-24-Data Packet"
        name = "Demographics"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getEnrollmentOver10Years(self):
        query = f"""
        SELECT ENROLL_TERM,
        COUNT(STUDENT_ID) AS STUDENT_COUNT
        FROM (
        SELECT DISTINCT STUDENT_ID, ENROLL_TERM
        FROM STUDENT_ENROLLMENT_VIEW AS SEV
        JOIN TERMS ON SEV.ENROLL_TERM = TERMS.TERMS_ID
        WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        AND  (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
        AND TERM_START_DATE >= '2014-08-01'
        AND ENROLL_TERM LIKE '%FA'
        ) AS X
        GROUP BY ENROLL_TERM
        """
        report = "2025-03-24-Data Packet"
        name = "Enrollment (10 Years)"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getGeographicOrigins(self):
        query = f"""
            SELECT STTR_STUDENT,
           LAST_NAME,
           FIRST_NAME,
           ADDRESS.ADDRESS_ID,
           CITY,
           STATE,
           ZIP,
           ADDRESS_LINES
        FROM (
        SELECT STTR_STUDENT,
               LAST_NAME,
               FIRST_NAME,
               ADDRESS_ID
        FROM (
        SELECT STTR_STUDENT,
               P.LAST_NAME,
               P.FIRST_NAME,
               ADDRESS.ADDRESS_ID,
               ROW_NUMBER() OVER (PARTITION BY STTR_STUDENT ORDER BY ADDRESS_ADD_DATE DESC) AS rn
        
        FROM STUDENT_TERMS_VIEW AS STV
        JOIN PERSON AS P ON STV.STTR_STUDENT = P.ID
        JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STV.STTR_STUDENT = FM.ID
        JOIN TERMS AS STARTING_TERM ON FM.TERM = STARTING_TERM.TERMS_ID
        JOIN PERSON_ADDRESSES_VIEW AS PAV  ON STV.STTR_STUDENT = PAV.ID
        JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
        WHERE STTR_TERM = '2024FA'
        AND ADDRESS_TYPE = 'H'
        AND ADDRESS_ADD_DATE < STARTING_TERM.TERM_START_DATE) AS X WHERE rn = 1) AS X
        JOIN ADDRESS ON X.ADDRESS_ID = ADDRESS.ADDRESS_ID
        JOIN ADDRESS_LS ON X.ADDRESS_ID = ADDRESS_LS.ADDRESS_ID
        WHERE POS = 1
        """
        report = "2025-03-24-Data Packet"
        name = "Geographic Origins"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-04-01-Carroll Retention Rates
    Person: Kathleen O'Leary
    Start Date: 2025-04-01
    End Date: 2025-04-02
    Description:
        I needed to calculate the retention rates.
    '''
    def getCCRetentionRates(self):
        query = f"""
        SELECT ID,
       CASE WHEN EXISTS (
           SELECT 1
           FROM STUDENT_ENROLLMENT_VIEW
           WHERE ENROLL_TERM = '2024FA'
           AND STUDENT_ID = ID
           AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
           AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
           AND ENROLL_CREDITS > 0
       ) THEN 1 ELSE 0 END AS STILL_ENROLLED
        FROM Z01_AAV_STUDENT_FIRST_MATRIC AS FM
        JOIN (SELECT STPR_STUDENT
                   FROM (
                       SELECT   STPR_STUDENT,
                                STPR_ADMIT_STATUS,
                                ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                                ORDER BY STUDENT_PROGRAMS_ADDDATE) AS ADMIT_RANK
                       FROM STUDENT_PROGRAMS_VIEW
                       WHERE STPR_ADMIT_STATUS IN ('FY', 'TR', 'RE')
                       ) AS X
                       WHERE ADMIT_RANK = 1
                       AND STPR_ADMIT_STATUS = 'FY'
                       ) AS FIRST_ADMIT ON FM.ID = FIRST_ADMIT.STPR_STUDENT
        WHERE FM.TERM = '2023FA'
        """
        report = "2025-04-01-Carroll Retention Rates"
        name = "Retention"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-04-02-Retention By Athletic Team
    Person: Charles Gross
    Start Date: 2025-04-02
    End Date: 2025-04-30
    Description:
        I need to find the retention rate by athletic team.
    '''
    def getRetentionAndStudentCountsByAthleticTeam(self):
        query = f"""
         --(Begin 4)------------------------------------------------------------------------------------------------------------
                       SELECT X.*,
                              CAST(ROUND(NUMBER_RETAINED * 1.0 / STUDENT_COUNT, 3) AS FLOAT) AS RETENTION_PERCENTAGE
                       FROM (
        --(Begin 3)------------------------------------------------------------------------------------------------------------
                                SELECT SPORT,
                                       TERM,
                                       NEXT_TERM,
                                       COUNT(STUDENT) AS STUDENT_COUNT,
                                       SUM(RETAINED)  AS NUMBER_RETAINED
                                FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                                         SELECT SPORT,
                                                TERM,
                                                NEXT_TERM,
                                                STUDENT,
                                                CASE WHEN STILL_ENROLLED = 1 OR SINCE_GRADUATED = 1 THEN 1 ELSE 0 END AS RETAINED
                                         FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                                                  SELECT VAL_EXTERNAL_REPRESENTATION AS SPORT,
                                                         TERMS_ID                    AS TERM,
                                                         NEXT_TERM.END_TERM          AS NEXT_TERM,
                                                         STA_STUDENT                 AS STUDENT,
                                                         CASE
                                                             WHEN EXISTS (SELECT 1
                                                                          FROM STUDENT_ENROLLMENT_VIEW
                                                                          WHERE ENROLL_TERM = NEXT_TERM.END_TERM
                                                                            AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                                                            AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
                                                                            AND STUDENT_ID = STA_STUDENT) THEN 1
                                                             ELSE 0 END              AS STILL_ENROLLED,
                                                         CASE
                                                             WHEN EXISTS (SELECT 1
                                                                          FROM STUDENT_ACAD_PROGRAMS_VIEW
                                                                          WHERE STP_CURRENT_STATUS = 'Graduated'
                                                                            AND (
                                                                              STP_END_DATE >= TERMS.TERM_START_DATE
                                                                                  OR STP_END_DATE IS NULL
                                                                              )
                                                                            AND STUDENT_ID = STA_STUDENT)
                                                                 THEN 1
                                                             ELSE 0 END              AS SINCE_GRADUATED
                                                  FROM STA_OTHER_COHORTS_VIEW
                                                           CROSS JOIN (SELECT TERMS_ID, TERM_START_DATE, TERM_END_DATE
                                                                       FROM TERMS
                                                                       WHERE TERMS_ID IN ('2023FA', '2024FA')) AS TERMS
                                                           JOIN (SELECT VAL_INTERNAL_CODE, VAL_EXTERNAL_REPRESENTATION
                                                                 FROM VALS
                                                                 WHERE VALCODE_ID = 'INSTITUTION.COHORTS') AS SPORTS
                                                                ON STA_OTHER_COHORTS_VIEW.STA_OTHER_COHORT_GROUPS =
                                                                   SPORTS.VAL_INTERNAL_CODE
                                                           JOIN (VALUES ('2024FA', '2025SP'), ('2023FA', '2024FA'))
                                                      AS NEXT_TERM(START_TERM, END_TERM)
                                                                ON TERMS.TERMS_ID = NEXT_TERM.START_TERM
                                                  WHERE STA_OTHER_COHORT_START_DATES <= TERM_END_DATE
                                                    AND (
                                                      STA_OTHER_COHORT_END_DATES >= TERM_START_DATE
                                                          OR STA_OTHER_COHORT_END_DATES IS NULL
                                                      )
                                                    AND VAL_EXTERNAL_REPRESENTATION IN (
                                                                                        'Men''s Basketball',
                                                                                        'Women''s Basketball',
                                                                                        'Cheerleading',
                                                                                        'Men''s Cross Country',
                                                                                        'Women''s Cross Country',
                                                                                        'Dance',
                                                                                        'Football',
                                                                                        'Men''s Golf',
                                                                                        'Women''s Golf',
                                                                                        'Women''s Soccer',
                                                                                        'Men''s Soccer',
                                                                                        'Women''s Softball',
                                                                                        'Outdoor Women''s Track',
                                                                                        'Indoor Women''s Track',
                                                                                        'Outdoor Men''s Track',
                                                                                        'Indoor Men''s Track',
                                                                                        'Women''s Volleyball',
                                                                                        'Men''s Basketball'
                                                      )
        --(End 1)---------------------------------------------------------------------------------------------------------------
                                              ) AS X
        --(End 2)---------------------------------------------------------------------------------------------------------------
                                     ) AS X
                                GROUP BY SPORT, TERM, NEXT_TERM
        --(End 3)---------------------------------------------------------------------------------------------------------------
                            ) AS X
        --(End 4)---------------------------------------------------------------------------------------------------------------
        ORDER BY SPORT, TERM DESC   
        """
        report = "2025-04-02-Retention By Athletic Team"
        name = "Retention and Student Counts By Athletic Team"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getRetentionByAthleticTeam(self):
        query = f"""
                --(Begin 5)------------------------------------------------------------------------------------------------------------
        SELECT SPORT,
                     [2024FA] AS RETENTION_2024FA_TO_2025SP,
                     [2023FA] AS RETENTION_2023FA_TO_2024FA
              FROM (
        --(Begin 4)------------------------------------------------------------------------------------------------------------
                       SELECT SPORT,
                              TERM,
                              CAST(ROUND(NUMBER_RETAINED * 1.0 / STUDENT_COUNT, 3) AS FLOAT) AS RETENTION_PERCENTAGE
                       FROM (
        --(Begin 3)------------------------------------------------------------------------------------------------------------
                                SELECT SPORT,
                                       TERM,
                                       COUNT(STUDENT) AS STUDENT_COUNT,
                                       SUM(RETAINED)  AS NUMBER_RETAINED
                                FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                                         SELECT SPORT,
                                                TERM,
                                                STUDENT,
                                                CASE WHEN STILL_ENROLLED = 1 OR SINCE_GRADUATED = 1 THEN 1 ELSE 0 END AS RETAINED
                                         FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                                                  SELECT VAL_EXTERNAL_REPRESENTATION AS SPORT,
                                                         TERMS_ID                    AS TERM,
                                                         STA_STUDENT                 AS STUDENT,
                                                         CASE
                                                             WHEN EXISTS (SELECT 1
                                                                          FROM STUDENT_ENROLLMENT_VIEW
                                                                          WHERE ENROLL_TERM = NEXT_TERM.END_TERM
                                                                            AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                                                            AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
                                                                            AND STUDENT_ID = STA_STUDENT) THEN 1
                                                             ELSE 0 END              AS STILL_ENROLLED,
                                                         CASE
                                                             WHEN EXISTS (SELECT 1
                                                                          FROM STUDENT_ACAD_PROGRAMS_VIEW
                                                                          WHERE STP_CURRENT_STATUS = 'Graduated'
                                                                            AND (
                                                                              STP_END_DATE >= TERMS.TERM_START_DATE
                                                                                  OR STP_END_DATE IS NULL
                                                                              )
                                                                            AND STUDENT_ID = STA_STUDENT)
                                                                 THEN 1
                                                             ELSE 0 END              AS SINCE_GRADUATED
                                                  FROM STA_OTHER_COHORTS_VIEW
                                                           CROSS JOIN (SELECT TERMS_ID, TERM_START_DATE, TERM_END_DATE
                                                                       FROM TERMS
                                                                       WHERE TERMS_ID IN ('2023FA', '2024FA')) AS TERMS
                                                           JOIN (SELECT VAL_INTERNAL_CODE, VAL_EXTERNAL_REPRESENTATION
                                                                 FROM VALS
                                                                 WHERE VALCODE_ID = 'INSTITUTION.COHORTS') AS SPORTS
                                                                ON STA_OTHER_COHORTS_VIEW.STA_OTHER_COHORT_GROUPS =
                                                                   SPORTS.VAL_INTERNAL_CODE
                                                           JOIN (VALUES ('2024FA', '2025SP'), ('2023FA', '2024FA'))
                                                      AS NEXT_TERM(START_TERM, END_TERM)
                                                                ON TERMS.TERMS_ID = NEXT_TERM.START_TERM
                                                  WHERE STA_OTHER_COHORT_START_DATES <= TERM_END_DATE
                                                    AND (
                                                      STA_OTHER_COHORT_END_DATES >= TERM_START_DATE
                                                          OR STA_OTHER_COHORT_END_DATES IS NULL
                                                      )
                                                    AND VAL_EXTERNAL_REPRESENTATION IN (
                                                                                        'Men''s Basketball',
                                                                                        'Women''s Basketball',
                                                                                        'Cheerleading',
                                                                                        'Men''s Cross Country',
                                                                                        'Women''s Cross Country',
                                                                                        'Dance',
                                                                                        'Football',
                                                                                        'Men''s Golf',
                                                                                        'Women''s Golf',
                                                                                        'Women''s Soccer',
                                                                                        'Men''s Soccer',
                                                                                        'Women''s Softball',
                                                                                        'Outdoor Women''s Track',
                                                                                        'Indoor Women''s Track',
                                                                                        'Outdoor Men''s Track',
                                                                                        'Indoor Men''s Track',
                                                                                        'Women''s Volleyball',
                                                                                        'Men''s Basketball'
                                                      )
        --(End 1)---------------------------------------------------------------------------------------------------------------
                                              ) AS X
        --(End 2)---------------------------------------------------------------------------------------------------------------
                                     ) AS X
                                GROUP BY SPORT, TERM
        --(End 3)---------------------------------------------------------------------------------------------------------------
                            ) AS X
        --(End 4)---------------------------------------------------------------------------------------------------------------
                   ) AS X
                       PIVOT (MAX(RETENTION_PERCENTAGE) FOR TERM IN (
                      [2024FA], [2023FA]
                      )) AS X
        --(End 5)---------------------------------------------------------------------------------------------------------------
        ORDER BY SPORT
        """
        report = "2025-04-02-Retention By Athletic Team"
        name = "Retention By Athletic Team"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-04-03-Past Enrollment Data
    Person: Patrick Schmidt
    Start Date: 2025-04-03
    End Date: 2025-04-08
    Description:
        I needed to get past enrollment data.
    '''
    def getStudentCreditHours_2024FA(self):
        query = f"""
        SELECT ENROLL_TERM AS TERM,
           SUBJ_DESC AS SUBJECT,
           CAST(SUM(ENROLL_CREDITS) AS INT) AS SCH
        FROM STUDENT_ENROLLMENT_VIEW AS SEV
        JOIN SUBJECTS ON SEV.SECTION_SUBJECT = SUBJECTS.SUBJECTS_ID
        WHERE ENROLL_TERM = '2024FA'
        AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
        GROUP BY ENROLL_TERM, SUBJ_DESC
        ORDER BY SUBJ_DESC
        """
        report = "2025-04-03-Past Enrollment Data"
        name = "Student Credit Hours (2024FA)"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getStudentCreditHours_2025SP(self):
        query = f"""
        SELECT ENROLL_TERM AS TERM,
        SUBJ_DESC AS SUBJECT,
        CAST(SUM(ENROLL_CREDITS) AS INT) AS SCH
        FROM STUDENT_ENROLLMENT_VIEW AS SEV
        JOIN SUBJECTS ON SEV.SECTION_SUBJECT = SUBJECTS.SUBJECTS_ID
        WHERE ENROLL_TERM = '2025SP'
        AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
        GROUP BY ENROLL_TERM, SUBJ_DESC
        ORDER BY SUBJ_DESC
        """
        report = "2025-04-03-Past Enrollment Data"
        name = "Student Credit Hours (2025SP)"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-04-10-Enrollment By County
    Person: Rebecca Schwartz
    Start Date: 2025-04-10
    End Date: 2025-04-15
    Description:
        I needed to get enrollment by county. 
    '''
    def getEnrollmentByCounty(self):
        query = f"""
        --(Begin 4)-----------------------------------------------------------------------------------------
        SELECT 'All' AS COUNTY,
                COUNT(DISTINCT STUDENT_ID) AS STUDENT_COUNT_2024FA
        FROM STUDENT_ENROLLMENT_VIEW AS SEV
        WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        AND  (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
        AND ENROLL_TERM = '2024FA'
        UNION
        --(Begin 3)-----------------------------------------------------------------------------------------
        SELECT COUNTY,
               SUM(IN_COUNTY) AS STUDENT_COUNT_2024FA
        FROM (
        --(Begin 2)-----------------------------------------------------------------------------------------
        SELECT CNTY_DESC  AS COUNTY,
        CASE WHEN CNTY_DESC = STUDENT_COUNTY.COUNTY THEN 1 ELSE 0 END AS IN_COUNTY
        FROM COUNTIES
        CROSS JOIN (
        --(Begin 1)-----------------------------------------------------------------------------------------
        SELECT DISTINCT STUDENT_ID,
               CNTY_DESC AS COUNTY
        FROM STUDENT_ENROLLMENT_VIEW AS SEV
        JOIN PERSON_ADDRESSES_VIEW AS PAV ON SEV.STUDENT_ID = PAV.ID
        JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
        JOIN COUNTIES ON ADDRESS.COUNTY = COUNTIES_ID
        WHERE ADDRESS_TYPE = 'H'
        AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
        AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
        AND ENROLL_TERM = '2024FA'
        --(End 1)-----------------------------------------------------------------------------------------
        ) AS STUDENT_COUNTY
        WHERE CNTY_DESC IN ('Cascade', 'Glacier', 'Lewis and Clark', 'Pondera', 'Teton', 'Toole')
        --(End 2)-----------------------------------------------------------------------------------------
        ) AS X
        GROUP BY COUNTY
        --(End 3)-----------------------------------------------------------------------------------------
        --(End 4)-----------------------------------------------------------------------------------------
        """
        report = "2025-04-10-Enrollment By County"
        name = "Enrollment By County"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-04-10-Program Review
    Person: Rebecca Schwartz
    Start Date: 2025-04-10
    End Date: 2025-04-24
    Description:
        I need to generate a bunch of data to help with program review.
    '''
    def getGraduationRateByCohort(self):
        query = f"""
        --(Begin 7)------------------------------------------------------------------------------------------------------------
            SELECT MAJOR,
                   MAJOR_COHORT,
                   FORMAT(COMPLETION_RATE, 'P') AS COMPLETION_RATE,
                   FORMAT(FOUR_YEAR_GRADUATION_RATE, 'P') AS FOUR_YEAR_GRADUATION_RATE,
                   FORMAT(SIX_YEAR_GRADUATION_RATE, 'P') AS SIX_YEAR_GRADUATION_RATE,
                   STUDENT_COUNT
            FROM (
            --(Begin 6)------------------------------------------------------------------------------------------------------------
                     SELECT MAJOR,
                            MAJOR_COHORT,
                            AVG(MAJOR_COMPLETED * 1.0)    AS COMPLETION_RATE,
                            AVG(FOUR_YEAR_GRADUATE * 1.0) AS FOUR_YEAR_GRADUATION_RATE,
                            AVG(SIX_YEAR_GRADUATE * 1.0)  AS SIX_YEAR_GRADUATION_RATE,
                            COUNT(*)                      AS STUDENT_COUNT,
                            START
                     FROM (
            --(Begin 5)------------------------------------------------------------------------------------------------------------
                              SELECT MAJOR,
                                     STUDENT_ID,
                                     MAJOR_COHORT,
                                     MAJOR_COMPLETED,
                                     CASE
                                         WHEN MAJOR_COMPLETED = 1 AND ACAD_END_DATE < DATEADD(YEAR, 4, START) THEN 1
                                         ELSE 0 END AS FOUR_YEAR_GRADUATE,
                                     CASE
                                         WHEN MAJOR_COMPLETED = 1 AND ACAD_END_DATE < DATEADD(YEAR, 4, START) THEN 1
                                         ELSE 0 END AS SIX_YEAR_GRADUATE,
                                        START
                              FROM (
            --(Begin 4)------------------------------------------------------------------------------------------------------------
                                       SELECT X.MAJOR,
                                              X.STUDENT_ID,
                                              COHORTS.TERM            AS MAJOR_COHORT,
                                              MAX(COMPLETE)           AS MAJOR_COMPLETED,
                                              COHORTS.TERM_START_DATE AS START,
                                              ACAD_END_DATE
                                       FROM (
            --(Begin 3)------------------------------------------------------------------------------------------------------------
                                                SELECT MAJOR,
                                                       STUDENT_ID,
                                                       CASE
                                                           WHEN (MAJOR_END >= ACAD_END_DATE OR MAJOR_END IS NULL)
                                                               AND STATUS = 'Graduated' THEN 1
                                                           ELSE 0 END AS COMPLETE,
                                                       ACAD_END_DATE
                                                FROM (
            --(Begin 2)------------------------------------------------------------------------------------------------------------
                                                         SELECT MAJOR,
                                                                STUDENT_ID,
                                                                STATUS,
                                                                CASE WHEN MAJOR = MAIN THEN MAIN_END ELSE ADDNL_END END AS MAJOR_END,
                                                                ACAD_END_DATE
                                                         FROM (
            --(Begin 1)------------------------------------------------------------------------------------------------------------
                                                                  SELECT MAJORS.MAJ_DESC           AS MAJOR,
                                                                         SAPV.STUDENT_ID,
                                                                         STP_CURRENT_STATUS        AS STATUS,
                                                                         MAIN_MAJOR.MAJ_DESC       AS MAIN,
                                                                         STP_END_DATE              AS MAIN_END,
                                                                         STPR_ADDNL_MAJOR_END_DATE AS ADDNL_END,
                                                                         AC.ACAD_END_DATE
                                                                  FROM MAJORS
                                                                           CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                                           JOIN ACAD_CREDENTIALS AS AC
                                                                                ON SAPV.STUDENT_ID = AC.ACAD_PERSON_ID AND
                                                                                   SAPV.STP_DEGREE = AC.ACAD_DEGREE
            
                                                                           LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                                                                     ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                                                        STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                                                           LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                                                           LEFT JOIN MAJORS AS ADDNL_MAJOR
                                                                                     ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                                                                  WHERE STP_CURRENT_STATUS != 'Did Not Enroll'
                                                                    AND STP_START_DATE >= '2019-08-01'
                                                                    AND (
                                                                      (
                                                                          MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                                                                          )
                                                                          OR (
                                                                          MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                                                          )
                                                                      )
                                                                    AND MAJORS.MAJ_DESC = 'Master of Social Work'
            --(End 1)------------------------------------------------------------------------------------------------------------
                                                              ) AS X
            --(End 2)------------------------------------------------------------------------------------------------------------
                                                     ) AS X
            --(End 3)------------------------------------------------------------------------------------------------------------
                                            ) AS X
                                                JOIN (
            --(Begin B2)-----------------------------------------------------------------------------------------------------------
                                           SELECT MAJOR,
                                                  STUDENT_ID,
                                                  TERM,
                                                  TERM_START_DATE
                                           FROM (
            --(Begin B1)-----------------------------------------------------------------------------------------------------------
                                                    SELECT DISTINCT TERMS.TERMS_ID                AS TERM,
                                                                    TERMS.TERM_START_DATE,
                                                                    MAJORS.MAJ_DESC               AS MAJOR,
                                                                    SAPV.STUDENT_ID,
                                                                    ROW_NUMBER() OVER (PARTITION BY STUDENT_ID, MAJORS.MAJ_DESC
                                                                        ORDER BY TERM_START_DATE) AS TERM_RANK
                                                    FROM MAJORS
                                                             CROSS JOIN TERMS
                                                             CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
            
                                                             LEFT JOIN STPR_MAJOR_LIST_VIEW AS SMLV
                                                                       ON SAPV.STUDENT_ID = SMLV.STPR_STUDENT AND
                                                                          SAPV.STP_ACADEMIC_PROGRAM = SMLV.STPR_ACAD_PROGRAM
                                                             LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                                             LEFT JOIN MAJORS AS ADDNL_MAJOR ON SMLV.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
            
                                                    WHERE TERMS.TERM_START_DATE >= DATEADD(YEAR, -10, '2019-08-01')
                                                      AND TERMS.TERM_END_DATE < '2025-06-01'
                                                      AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                                                      AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
            
                                                      AND (
                                                        (
                                                            MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                                                                AND SAPV.STP_START_DATE <= TERMS.TERM_END_DATE
                                                                AND
                                                            (SAPV.STP_END_DATE >= TERMS.TERM_START_DATE OR SAPV.STP_END_DATE IS NULL)
                                                            )
                                                            OR (
                                                            MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                                                AND SMLV.STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                                                AND
                                                            (SMLV.STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                                             SMLV.STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                                            )
                                                        )
            --(End B1)-------------------------------------------------------------------------------------------------------------
                                                ) AS X
                                           WHERE TERM_RANK = 1
                                             AND TERM_START_DATE >= '2019-08-01'
            --(End B2)-------------------------------------------------------------------------------------------------------------
                                       ) AS COHORTS ON X.MAJOR = COHORTS.MAJOR AND X.STUDENT_ID = COHORTS.STUDENT_ID
                                       GROUP BY X.MAJOR, X.STUDENT_ID, COHORTS.TERM, COHORTS.TERM_START_DATE, ACAD_END_DATE
            --(End 4)------------------------------------------------------------------------------------------------------------
                                   ) AS X
            --(End 5)------------------------------------------------------------------------------------------------------------
                          ) AS X
                     GROUP BY MAJOR, MAJOR_COHORT, START
            --(End 6)------------------------------------------------------------------------------------------------------------
                 ) AS X
            --(End 7)------------------------------------------------------------------------------------------------------------
            ORDER BY START, X.COMPLETION_RATE DESC, X.FOUR_YEAR_GRADUATION_RATE DESC, X.SIX_YEAR_GRADUATION_RATE DESC
        """
        report = "2025-04-10-Program Review"
        name = "Graduation Rate By Cohort"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getMajorCompletionRates(self):
        query = f"""
        --(Begin 6)------------------------------------------------------------------------------------------------------------
        SELECT MAJOR,
        FORMAT(COMPLETION_RATE, 'P') AS COMPLETION_RATE,
        STUDENT_COUNT
        FROM (
        --(Begin 5)------------------------------------------------------------------------------------------------------------
        SELECT MAJOR,
        AVG(MAJOR_COMPLETED * 1.0) AS COMPLETION_RATE,
        COUNT(*)                   AS STUDENT_COUNT
        FROM (
        --(Begin 4)------------------------------------------------------------------------------------------------------------
        SELECT MAJOR,
        STUDENT_ID,
        MAX(COMPLETE) AS MAJOR_COMPLETED
        FROM (
        --(Begin 3)------------------------------------------------------------------------------------------------------------
        SELECT MAJOR,
        STUDENT_ID,
        CASE
        WHEN (MAJOR_END >= ACAD_END_DATE OR MAJOR_END IS NULL)
        AND STATUS = 'Graduated' THEN 1
        ELSE 0 END AS COMPLETE
        FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT MAJOR,
        STUDENT_ID,
        STATUS,
        CASE WHEN MAJOR = MAIN THEN MAIN_END ELSE ADDNL_END END AS MAJOR_END,
        ACAD_END_DATE
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
        SELECT MAJORS.MAJ_DESC           AS MAJOR,
        STUDENT_ID,
        STP_CURRENT_STATUS        AS STATUS,
        MAIN_MAJOR.MAJ_DESC       AS MAIN,
        STP_END_DATE              AS MAIN_END,
        STPR_ADDNL_MAJOR_END_DATE AS ADDNL_END,
        AC.ACAD_END_DATE
        FROM MAJORS
        CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        JOIN ACAD_CREDENTIALS AS AC
           ON SAPV.STUDENT_ID = AC.ACAD_PERSON_ID AND
              SAPV.STP_DEGREE = AC.ACAD_DEGREE
        LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                ON SAPV.STUDENT_ID = STPR_STUDENT AND
                   STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
        LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
        LEFT JOIN MAJORS AS ADDNL_MAJOR
                ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
        WHERE STP_CURRENT_STATUS != 'Did Not Enroll'
        AND STP_START_DATE >= '2019-08-01'
        AND (
        (
        MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
        )
        OR (
        MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
        )
        )
        --(End 1)------------------------------------------------------------------------------------------------------------
        ) AS X
        --(End 2)------------------------------------------------------------------------------------------------------------
        ) AS X
        --(End 3)------------------------------------------------------------------------------------------------------------
        ) AS X
        GROUP BY MAJOR, STUDENT_ID
        --(End 4)------------------------------------------------------------------------------------------------------------
        ) AS X
        GROUP BY MAJOR
        --(End 5)------------------------------------------------------------------------------------------------------------
        ) AS X
        WHERE MAJOR = 'Master of Social Work'
        --(End 6)------------------------------------------------------------------------------------------------------------
        ORDER BY X.COMPLETION_RATE DESC
        """
        report = "2025-04-10-Program Review"
        name = "Major Completion Rates"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getAvgEnrollmentPerCourse(self):
        query = f"""
        --(Begin 3)-------------------------------------------------------------------------------------------------------------
        SELECT COURSE_TITLE,
               COURSE_NAME,
               AVG(TOTAL_ENROLLMENT) AS AVG_ENROLLMENT
        FROM (
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        COURSE_TITLE,
                        COURSE_NAME,
                        COUNT(STUDENT_ID) AS TOTAL_ENROLLMENT
                 FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT TERMS.TERMS_ID           AS TERM,
                                          TERM_START_DATE,
                                          SAPV.STUDENT_ID,
                                          SEV.SECTION_COURSE_NAME AS COURSE_NAME,
                                          SEV.SECTION_COURSE_TITLE AS COURSE_TITLE,
                                          SEV.ENROLL_CREDITS
                          FROM MAJORS
                                   CROSS JOIN TERMS
                                   CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                   LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                             ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                   LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                   LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                                   JOIN STUDENT_ENROLLMENT_VIEW AS SEV
                                        ON SAPV.STUDENT_ID = SEV.STUDENT_ID AND TERMS_ID = SEV.ENROLL_TERM
                          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                            AND TERMS.TERM_END_DATE < '2025-06-01'
                            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                            AND STP_CURRENT_STATUS != 'Did Not Enroll'
                            AND (
                              (
                                  MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                                      AND STP_START_DATE <= TERMS.TERM_END_DATE
                                      AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                                  )
                                  OR (
                                  MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                      AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                      AND
                                  (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                  )
                              )
                            AND MAJORS.MAJ_DESC = 'Master of Social Work'
                            -------------------------------------------------------------------------------------------------
                            AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
        --(End 1)-------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY TERM, TERM_START_DATE, COURSE_TITLE, COURSE_NAME
        --(End 2)-------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY COURSE_TITLE, COURSE_NAME
        --(End 3)-------------------------------------------------------------------------------------------------------------
        """
        report = "2025-04-10-Program Review"
        name = "Avg Enrollment Per Course"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getCourseCompletionRates(self):
        query = f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT COURSE_TITLE,
               COURSE_NAME,
               FORMAT(AVG(COMPLETED * 1.0), 'P') AS COMPLETION_RATE,
               COUNT(*) AS ENROLLMENT_COUNT
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
                 SELECT STUDENTS.STUDENT_ID,
                        SEV.SECTION_COURSE_NAME          AS COURSE_NAME,
                        SEV.SECTION_COURSE_TITLE         AS COURSE_TITLE,
                        CASE WHEN ENROLL_CURRENT_STATUS IN ('New', 'Add') THEN 1 ELSE 0 END AS COMPLETED
                 FROM (SELECT DISTINCT TERMS.TERMS_ID AS TERM,
                                       TERMS.TERM_START_DATE,
                                       SAPV.STUDENT_ID
                       FROM MAJORS
                                CROSS JOIN TERMS
                                CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                          ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                       WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                         AND TERMS.TERM_END_DATE < GETDATE()
                         AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                         AND (
                           (
                               MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                                   AND STP_START_DATE <= TERMS.TERM_END_DATE
                                   AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                               )
                               OR (
                               MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                   AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                   AND
                               (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                               )
                           )
                         AND MAJORS.MAJ_DESC = 'Master of Social Work') AS STUDENTS
                          JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON STUDENTS.STUDENT_ID = SEV.STUDENT_ID AND TERM = ENROLL_TERM
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY COURSE_TITLE, COURSE_NAME
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY COURSE_NAME, COURSE_TITLE
        """
        report = "2025-04-10-Program Review"
        name = "Course Completion Rates"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    '''
    ID: Unknown
    Name: 2025-04-22-Honors Convocation Health Science Student Summaries
    Person: Gerald Schafer
    Start Date: 2025-04-22
    End Date: 2025-04-29
    Description:
        I needed to find summaries of students who are graduating with honors in the health sciences.
    '''
    def getHonorsConvocationStudentsCourses(self):
        query = f"""
                --(Begin 3)-------------------------------------------------------------------------------------------------------------
                 SELECT X.*,
                        SECTION_COURSE_TITLE  AS HONORS_CONVOCATION_MASTER_LIST_COURSE_TITLE,
                        ENROLL_GPA_CREDITS    AS HONORS_CONVOCATION_MASTER_LIST_CREDITS,
                        ENROLL_VERIFIED_GRADE AS HONORS_CONVOCATION_MASTER_LIST_GRADE_VERIFIED,
                        ENROLL_GRADE_POINTS   AS TOTAL_GRADE_POINTS_FOR_COURSE
                 FROM (
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
                          SELECT STUDENT_ID,
                                 NAME_LAST,
                                 NAME_FIRST,
                                 CLASS_LEVEL_DESC,
                                 GPA_FOR_ACAD_LEVEL,
                                 CASE
                                     WHEN MAX(CASE
                                                  WHEN MAIN_MAJOR = 'PUBH' OR (ADDNL_MAJOR = 'PUBH' AND MAJOR_END_DATE IS NULL)
                                                      THEN 1
                                                  ELSE 0 END) = 1
                                         THEN 'Y' END AS PH,
                                 CASE
                                     WHEN MAX(CASE
                                                  WHEN MAIN_MAJOR = 'HSCI' OR (ADDNL_MAJOR = 'HSCI' AND MAJOR_END_DATE IS NULL)
                                                      THEN 1
                                                  ELSE 0 END) = 1
                                         THEN 'Y' END AS HS,
                                 MAJOR1
                          FROM (
        --(Begin 1)----------------------------------------------------------------------------------------------
                                   SELECT STUDENT_ID,
                                          STUDENT_LAST_NAME         AS NAME_LAST,
                                          STUDENT_FIRST_NAME        AS NAME_FIRST,
                                          STUDENT_CLASS_LEVEL       AS CLASS_LEVEL_DESC,
                                          STP_EVAL_COMBINED_GPA     AS GPA_FOR_ACAD_LEVEL,
                                          MAIN_MAJOR.MAJORS_ID      AS MAIN_MAJOR,
                                          ADDNL_MAJOR.MAJORS_ID     AS ADDNL_MAJOR,
                                          STPR_ADDNL_MAJOR_END_DATE AS MAJOR_END_DATE,
                                          STP_PROGRAM_TITLE         AS MAJOR1
                                   FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                            LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                                      ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                         STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                            LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                            LEFT JOIN MAJORS AS ADDNL_MAJOR
                                                      ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                                   WHERE STP_PROGRAM_TITLE IN ('Health Sciences', 'Public Health')
                                     AND STP_START_DATE <= GETDATE()
                                     AND STP_END_DATE IS NULL
                                     AND STP_EVAL_COMBINED_GPA >= 3.5
        --(End 1)---------------------------------------------------------------------------------------------------------------
                               ) AS X
                          GROUP BY X.STUDENT_ID,
                                   NAME_LAST,
                                   NAME_FIRST,
                                   CLASS_LEVEL_DESC,
                                   GPA_FOR_ACAD_LEVEL,
                                   MAJOR1
        --(End 2)-------------------------------------------------------------------------------------------------------------
                      ) AS X
                          JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON X.STUDENT_ID = SEV.STUDENT_ID
                 WHERE ENROLL_GPA_CREDITS IS NOT NULL
                AND ENROLL_CREDIT_TYPE = 'Institutional'
        --(End 3)-------------------------------------------------------------------------------------------------------------
        ORDER BY NAME_FIRST
        """
        report = "2025-04-22-Honors Convocation Health Science Student Summaries"
        name = "Honors Convocation Students (Courses)"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getHonorsConvocationStudentsList(self):
        query = f"""
                --(Begin 2)-------------------------------------------------------------------------------------------------------------
                 SELECT STUDENT_ID,
                        NAME_LAST,
                        NAME_FIRST,
                        CLASS_LEVEL_DESC,
                        PROGRAM_START_DATE,
                        CATALOG_YEAR,
                        ANTIC_COMPLETION_DATE,
                        EVAL_COMB_CRED,
                        GPA_FOR_ACAD_LEVEL,
                        CASE
                            WHEN MAX(CASE
                                         WHEN MAIN_MAJOR = 'PUBH' OR (ADDNL_MAJOR = 'PUBH' AND MAJOR_END_DATE IS NULL)
                                             THEN 1
                                         ELSE 0 END) = 1
                                THEN 'Y' END AS PH,
                        CASE
                            WHEN MAX(CASE
                                         WHEN MAIN_MAJOR = 'HSCI' OR (ADDNL_MAJOR = 'HSCI' AND MAJOR_END_DATE IS NULL)
                                             THEN 1
                                         ELSE 0 END) = 1
                                THEN 'Y' END AS HS,
                        MAJOR1,
                        (
                        SELECT TOP 1 ADDNL_MAJOR.MAJ_DESC AS MAJOR2
                        FROM STPR_MAJOR_LIST_VIEW AS MJ
                            LEFT JOIN MAJORS AS ADDNL_MAJOR ON MJ.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                            WHERE MJ.STPR_STUDENT = X.STUDENT_ID
                              AND STPR_ADDNL_MAJOR_END_DATE IS NULL
                            ORDER BY CASE WHEN ADDNL_MAJOR.MAJ_DESC NOT IN ('Public Health', 'Health Sciences') THEN 0 ELSE 1 END
                        ) AS MAJOR2
                 FROM (
        --(Begin 1)----------------------------------------------------------------------------------------------
                          SELECT STUDENT_ID,
                                 STUDENT_LAST_NAME            AS NAME_LAST,
                                 STUDENT_FIRST_NAME           AS NAME_FIRST,
                                 STUDENT_CLASS_LEVEL          AS CLASS_LEVEL_DESC,
                                 CAST(STP_START_DATE AS DATE)        AS PROGRAM_START_DATE,
                                 STP_CATALOG                   AS CATALOG_YEAR,
                                 STP_ANT_CMPL_DATE              AS ANTIC_COMPLETION_DATE,
                                 STP_EVAL_COMBINED_CREDITS      AS EVAL_COMB_CRED,
                                 STP_EVAL_COMBINED_GPA        AS GPA_FOR_ACAD_LEVEL,
                                 MAIN_MAJOR.MAJORS_ID         AS MAIN_MAJOR,
                                 ADDNL_MAJOR.MAJORS_ID        AS ADDNL_MAJOR,
                                 STPR_ADDNL_MAJOR_END_DATE    AS MAJOR_END_DATE,
                                 MAIN_MAJOR.MAJ_DESC          AS MAJOR1
                          FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                   LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                             ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                   LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                   LEFT JOIN MAJORS AS ADDNL_MAJOR
                                             ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                          WHERE STP_PROGRAM_TITLE IN ('Health Sciences', 'Public Health')
                            AND STP_START_DATE <= GETDATE()
                            AND STP_END_DATE IS NULL
                            AND STP_EVAL_COMBINED_GPA >= 3.5
        --(End 1)---------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY STUDENT_ID,
                        NAME_LAST,
                        NAME_FIRST,
                        CLASS_LEVEL_DESC,
                        PROGRAM_START_DATE,
                        CATALOG_YEAR,
                        ANTIC_COMPLETION_DATE,
                        EVAL_COMB_CRED,
                          GPA_FOR_ACAD_LEVEL,
                          MAJOR1
        --(End 2)-------------------------------------------------------------------------------------------------------------
        ORDER BY NAME_FIRST
        """
        report = "2025-04-22-Honors Convocation Health Science Student Summaries"
        name = "Honors Convocation Students (List)"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

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

    '''
    ID: Unknown
    Name: 2025-04-29-New Transfer and Graduate Count for Next Fall (ODS)
    Person: Rebecca Schwartz
    Start Date: 2025-04-29
    End Date: 2025-05-12
    Description:
        I needed to get a list of new transfers and graduates for next fall using the ODS.
    '''
    def getNewTransferAndGraduates_2025FA(self):
        query = f"""
        --(Begin 3)-------------------------------------------------------------------------------------------------------------
        SELECT SUM(NEW_TRANSFER) AS TOTAL_NEW_TRANSFERS,
               SUM(NEW_GRADUATE) AS TOTAL_NEW_GRADUATES
        FROM (
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
                 SELECT STUDENT,
                        CASE WHEN ADMIT = 'TR' THEN 1 ELSE 0 END AS NEW_TRANSFER,
                        CASE WHEN LEVEL = 'GR' THEN 1 ELSE 0 END AS NEW_GRADUATE
                 FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
                          SELECT STPR_STUDENT                                                                       AS STUDENT,
                                 STPR_ACAD_LEVEL                                                                    AS LEVEL,
                                 STPR_ADMIT_STATUS                                                                  AS ADMIT,
                                 START_DATE,
                                 END_DATE,
                                 ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT, STPR_ACAD_LEVEL ORDER BY START_DATE) AS PROGRAM_RANK
                          FROM ODS_STUDENT_PROGRAMS AS SP
                          WHERE START_DATE IS NOT NULL
                            AND STPR_ACAD_LEVEL != 'CE'
                            AND TITLE != 'Non-Degree Seeking Students'
        --(End 1)-------------------------------------------------------------------------------------------------------------
                      ) AS X
                          CROSS JOIN ODS_TERMS
                 WHERE PROGRAM_RANK = 1
                   AND (ADMIT = 'TR' OR LEVEL = 'GR')
                   AND TERMS_ID = '2025FA'
                   AND START_DATE >= TERM_START_DATE
                   AND START_DATE <= TERM_END_DATE
        --(End 2)-------------------------------------------------------------------------------------------------------------
             ) AS X
        --(End 3)-------------------------------------------------------------------------------------------------------------
        """
        report = '2025-04-29-New Transfer and Graduate Count for Next Fall (ODS)'
        name = "New Transfer and Graduate Count for Next Fall"
        self.save_query_results(query, db="ODS")(report, name)

    '''
    ID: Unknown
    Name: 2025-05-08-Hispanic Student Enrollment
    Person: Rebecca Schwartz
    Start Date: 2025-05-08
    End Date: 2025-05-08
    Description:
        I needed to find the student enrollment of Hispanics.
    '''
    def getHispanicStudentEnrollment(self):
        query = f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT TERM,
                COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
                 SELECT DISTINCT TERMS.TERMS_ID AS TERM,
                                 TERMS.TERM_START_DATE,
                                 STUDENT_ID,
                                 STUDENT_LAST_NAME,
                                 STUDENT_FIRST_NAME
                 FROM STUDENT_ENROLLMENT_VIEW AS SEV
                          JOIN TERMS ON SEV.ENROLL_TERM = TERMS.TERMS_ID
                          JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON SEV.STUDENT_ID = RACE.ID
                 WHERE TERMS.TERM_START_DATE >= DATEADD(YEAR, -10, GETDATE())
                   AND TERMS.TERM_END_DATE < '2025-06-01'
                   AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                   AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                   AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
                   AND RACE.IPEDS_RACE_ETHNIC_DESC = 'Hispanic/Latino'
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        report = "2025-05-08-Hispanic Student Enrollment"
        name = "Hispanic Student Enrollment"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

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









