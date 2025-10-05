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
        print(tabulate(df.head(100), headers='keys', tablefmt='psql'))

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
        folder_1b = ["Ian's Reports", "Data Provided Grouped By Request"]
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
    Name: 2025-03-31-Enrollment Summary & Class Distribution
    Person: Cindy Trimp
    Start Date: 2025-03-31
    End Date: 2025-04-04
    Description:
        I needed to get the enrollment summary by student type.
    '''
    def getEnrollmentSummary_2024FA(self):
        query = f"""
          SELECT DISTINCT SEV.STUDENT_ID,
                  CASE WHEN (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL) THEN
                  CASE
                      WHEN STUDENT_ACAD_LEVEL = 'UG' THEN CASE
                        WHEN STUDENT_CURRENT_TYPE = 'ACE'
                          THEN 'Early High School'
                        WHEN STUDENT_CURRENT_TYPE = 'NDFTV'
                          THEN 'International Exchange'
                      WHEN PROGRAM = 'Accelerated Nursing'
                          THEN 'Accelerated Nursing'
                      WHEN PROGRAM = 'Non-Degree Seeking Students'
                          THEN 'Non-Degree UG'
                    WHEN STUDENT_CURRENT_TYPE = 'PB'
                            THEN 'Post-Baccalaureate'

                      WHEN STUDENT_CLASS_LEVEL = 'Freshman'
                          THEN CASE
                                   WHEN FIRST_ADMIT.STPR_ADMIT_STATUS = 'FY'
                                       THEN 'First-Time Beginning Freshman'
                                   ELSE 'Other Freshman' END
                      WHEN STUDENT_CLASS_LEVEL = 'Sophomore'
                          THEN 'Sophomores'
                      WHEN STUDENT_CLASS_LEVEL = 'Junior'
                          THEN 'Juniors'
                      WHEN STUDENT_CLASS_LEVEL = 'Senior'
                          THEN 'Seniors'
                      ELSE 'Non-Degree UG' END
                      WHEN STUDENT_ACAD_LEVEL = 'GR'
                          THEN 'Master''s Candidates'
                      WHEN STUDENT_ACAD_LEVEL = 'CE'
                          THEN 'Continuing Education'
                      END
                      ELSE 'Senior Citizen Auditor' END AS STUDENT_SUB_CLASSIFICATION,
                  CASE
                      WHEN STUDENT_LOAD IN ('F', 'O') THEN CASE
                                                               WHEN 'M' IN (STUDENT_GENDER, ASSIGNED_GENDER)
                                                                   THEN 'Full-Time Male'
                                                               WHEN 'F' IN (STUDENT_GENDER, ASSIGNED_GENDER)
                                                                   THEN 'Full-Time Female'
                                                                ELSE 'Unknown' END
                      ELSE CASE
                               WHEN 'M' IN (STUDENT_GENDER, ASSIGNED_GENDER)
                                   THEN 'Part-Time Male'
                               WHEN 'F' IN (STUDENT_GENDER, ASSIGNED_GENDER)
                                   THEN 'Part-Time Female'
                                ELSE 'Unknown' END END AS LOAD_GENDER
            FROM STUDENT_ENROLLMENT_VIEW AS SEV
           LEFT JOIN (SELECT STPR_STUDENT, STPR_ADMIT_STATUS
                      FROM (SELECT STPR_STUDENT,
                                   STPR_ADMIT_STATUS,
                                   ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                                       ORDER BY STUDENT_PROGRAMS_ADDDATE) AS ADMIT_RANK
                            FROM STUDENT_PROGRAMS_VIEW
                            WHERE STPR_ADMIT_STATUS IN ('FY', 'TR', 'RE')) ranked
                      WHERE ADMIT_RANK = 1) AS FIRST_ADMIT
                     ON SEV.STUDENT_ID = FIRST_ADMIT.STPR_STUDENT
           LEFT JOIN (SELECT *
                 FROM (SELECT STUDENT_ID,
                              STP_PROGRAM_TITLE                                                                 AS PROGRAM,
                              STP_CURRENT_STATUS,
                              ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                                  ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS PROGRAM_RANK
                       FROM STUDENT_ACAD_PROGRAMS_VIEW
                       WHERE STP_START_DATE <=
                             (SELECT TOP 1 TERMS.TERM_END_DATE
                              FROM TERMS
                              WHERE TERMS_ID = '2024FA')) ranked
                 WHERE PROGRAM_RANK = 1) AS SAPV
                ON SEV.STUDENT_ID = SAPV.STUDENT_ID
            LEFT JOIN (VALUES
                           ('6184447', 'F'),
                            ('6184697', 'F'),
                            ('6184977', 'F'),
                            ('6185039', 'F'),
                            ('6186217', 'M'),
                            ('6186670', 'F'),
                            ('6187467', 'F'),
                            ('6187468', 'M'),
                            ('6187470', 'F'),
                            ('6188264', 'F'),
                            ('6188541', 'F'),
                            ('6188544', 'F'),
                            ('6188723', 'F'),
                            ('6188731', 'F'),
                            ('6188797', 'F'),
                            ('6188940', 'F'),
                            ('6189182', 'M'),
                            ('6189200', 'M'),
                            ('6189204', 'M'),
                            ('6189250', 'F'),
                            ('6189252', 'M'),
                            ('6189317', 'F'),
                            ('6189318', 'M'),
                            ('6189523', 'F'),
                            ('6189571', 'F'),
                            ('6189572', 'M'),
                            ('6189575', 'F'),
                            ('6189620', 'F'),
                            ('6189635', 'M'),
                            ('6189662', 'M')) AS Y(ID, ASSIGNED_GENDER)
                            ON SEV.STUDENT_ID = Y.ID
  WHERE ENROLL_TERM = '2024FA'
    AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
    AND ((ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL) OR STUDENT_CURRENT_TYPE = 'SC') --Original Data
        """
        agg = lambda query: f"""
        --(Begin 7)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        SELECT X.*
        FROM (
        --(Begin 6)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                 SELECT Y.STUDENT_CLASSIFICATION,
                        X.*
                 FROM (
        --(Begin 5)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                          SELECT CASE
                                     WHEN GROUPING(STUDENT_SUB_CLASSIFICATION) = 1
                                        AND GROUPING(FRESHMAN) = 1
                                        AND GROUPING(STUDENT_CLASSIFICATION) = 0
                                         THEN CASE
                                                  WHEN STUDENT_CLASSIFICATION = 'Undergraduate'
                                                      THEN 'Total Undergraduates'
                                                  WHEN STUDENT_CLASSIFICATION = 'Graduate and Special'
                                                      THEN 'Total Graduates and Special'
                                                  WHEN STUDENT_CLASSIFICATION = 'Miscellaneous'
                                                      THEN 'Total Miscellaneous' END
                                    WHEN GROUPING(STUDENT_SUB_CLASSIFICATION) = 1
                                    AND GROUPING(FRESHMAN) = 0
                                    AND GROUPING(STUDENT_CLASSIFICATION) = 1
                                        THEN CASE
                                            WHEN FRESHMAN = 'Freshman' THEN 'Total Freshman' END
                                     WHEN GROUPING(STUDENT_SUB_CLASSIFICATION) = 1
                                        AND GROUPING(STUDENT_CLASSIFICATION) = 1
                                         AND GROUPING(FRESHMAN) = 1 THEN 'Grand Total'
                                     ELSE STUDENT_SUB_CLASSIFICATION END AS STUDENT_SUB_CLASSIFICATION,
                                 SUM(PART_TIME_MALE)                     AS PART_TIME_MALE,
                                 SUM(PART_TIME_FEMALE)                   AS PART_TIME_FEMALE,
                                 SUM(PART_TIME_TOTAL)                    AS PART_TIME_TOTAL,
                                 SUM(FULL_TIME_MALE)                     AS FULL_TIME_MALE,
                                 SUM(FULL_TIME_FEMALE)                   AS FULL_TIME_FEMALE,
                                 SUM(FULL_TIME_TOTAL)                    AS FULL_TIME_TOTAL,
                                 SUM(MALE_TOTAL)                         AS MALE_TOTAL,
                                 SUM(FEMALE_TOTAL)                       AS FEMALE_TOTAL,
                                 SUM(TOTAL)                              AS TOTAL
                          FROM (
        --(Begin 4)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                   SELECT STUDENT_CLASSIFICATION,
                                          FRESHMAN,
                                          STUDENT_SUB_CLASSIFICATION,
                                          PART_TIME_MALE,
                                          PART_TIME_FEMALE,
                                          (PART_TIME_MALE + PART_TIME_FEMALE)                                     AS PART_TIME_TOTAL,
                                          FULL_TIME_MALE,
                                          FULL_TIME_FEMALE,
                                          (FULL_TIME_MALE + FULL_TIME_FEMALE)                                     AS FULL_TIME_TOTAL,
                                          (PART_TIME_MALE + FULL_TIME_MALE)                                       AS MALE_TOTAL,
                                          (PART_TIME_FEMALE + FULL_TIME_FEMALE)                                   AS FEMALE_TOTAL,
                                          (PART_TIME_MALE + PART_TIME_FEMALE + FULL_TIME_MALE + FULL_TIME_FEMALE) AS TOTAL,
                                          UNKNOWN
                                   FROM (
        --(Begin 3)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                            SELECT STUDENT_CLASSIFICATION,
                                                   FRESHMAN,
                                                   STUDENT_SUB_CLASSIFICATION,
                                                   [Part-Time Male]   AS PART_TIME_MALE,
                                                   [Part-Time Female] AS PART_TIME_FEMALE,
                                                   [Full-Time Male]   AS FULL_TIME_MALE,
                                                   [Full-Time Female] AS FULL_TIME_FEMALE,
                                                   [Unknown] AS UNKNOWN
                                            FROM (
        --(Begin 2)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                     SELECT X.STUDENT_ID,
                                                            Y.STUDENT_CLASSIFICATION,
                                                            Z.FRESHMAN,
                                                            X.STUDENT_SUB_CLASSIFICATION,
                                                            X.LOAD_GENDER
                                                     FROM (
        ---(Begin 1)-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                        {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                          ) AS X
                                            JOIN (VALUES ('First-Time Beginning Freshman', 'Undergraduate'),
                                                         ('Other Freshman', 'Undergraduate'),
                                                         ('Sophomores', 'Undergraduate'),
                                                         ('Juniors', 'Undergraduate'),
                                                         ('Seniors', 'Undergraduate'),
                                                         ('Master''s Candidates', 'Graduate and Special'),
                                                         ('Accelerated Nursing', 'Graduate and Special'),
                                                         ('Continuing Education', 'Miscellaneous'),
                                                         ('Post-Baccalaureate', 'Miscellaneous'),
                                                         ('Early High School', 'Miscellaneous'),
                                                         ('Non-Degree UG', 'Miscellaneous'),
                                                         ('International Exchange', 'Miscellaneous'),
                                                         ('Senior Citizen Auditor', 'Miscellaneous')
                                                  ) AS Y(STUDENT_SUB_CLASSIFICATION, STUDENT_CLASSIFICATION)
                                                     ON X.STUDENT_SUB_CLASSIFICATION = Y.STUDENT_SUB_CLASSIFICATION
                                            LEFT JOIN (VALUES ('First-Time Beginning Freshman', 'Freshman'),
                                                              ('Other Freshman', 'Freshman')
                                                       ) AS Z(STUDENT_SUB_CLASSIFICATION, FRESHMAN)
                                                ON X.STUDENT_SUB_CLASSIFICATION = Z.STUDENT_SUB_CLASSIFICATION
                                                     -- Added Student Classification
        --(End 2)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                 ) AS X PIVOT (COUNT(STUDENT_ID) FOR LOAD_GENDER IN (
                                                [Part-Time Male],
                                                [Part-Time Female],
                                                [Full-Time Male],
                                                [Full-Time Female],
                                                [Unknown]
                                                )) AS X --Original Pivot Table
        --(End 3)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                        ) AS X --With Column Totals
        --(End 4)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                               ) AS X
                          GROUP BY GROUPING SETS ((STUDENT_SUB_CLASSIFICATION), (STUDENT_CLASSIFICATION), (FRESHMAN), ())
        --(End 5)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                      ) AS X
                 JOIN (VALUES ('First-Time Beginning Freshman', 'Undergraduate'),
                               ('Other Freshman', 'Undergraduate'),
                               ('Sophomores', 'Undergraduate'),
                             ('Juniors', 'Undergraduate'),
                             ('Seniors', 'Undergraduate'),
                             ('Master''s Candidates', 'Graduate and Special'),
                             ('Accelerated Nursing', 'Graduate and Special'),
                             ('Continuing Education', 'Miscellaneous'),
                             ('Post-Baccalaureate', 'Miscellaneous'),
                             ('Early High School', 'Miscellaneous'),
                             ('Non-Degree UG', 'Miscellaneous'),
                             ('International Exchange', 'Miscellaneous'),
                             ('Senior Citizen Auditor', 'Miscellaneous'),
                     --------------------------------------------------------------------
                            ('Total Freshman', 'Undergraduate'),
                            ('Total Undergraduates', 'Undergraduate'),
                            ('Total Graduates and Special', 'Graduate and Special'),
                            ('Total Miscellaneous', 'Miscellaneous'),
                            ('Grand Total', 'Grand Total')
                                                  ) AS Y(STUDENT_SUB_CLASSIFICATION, STUDENT_CLASSIFICATION)
                                                     ON X.STUDENT_SUB_CLASSIFICATION = Y.STUDENT_SUB_CLASSIFICATION
                 --Appended on Student Classification Again
        --(End 6)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
             ) AS X
        LEFT JOIN (VALUES ('Undergraduate', 1),
                          ('Graduate and Special', 2),
                          ('Miscellaneous', 3),
                            ('Grand Total', 4))
            AS ORDER_1(LABEL, N)
        ON X.STUDENT_CLASSIFICATION = ORDER_1.LABEL
        LEFT JOIN (VALUES
                ('First-Time Beginning Freshman', 1),
                ('Other Freshman', 2),
                ('Total Freshman', 3),
                ('Sophomores', 4),
                ('Juniors', 5),
                ('Seniors', 6),
                ('Total Undergraduates', 7),
        ----------------------------------------
                ('Master''s Candidates', 1),
                ('Accelerated Nursing', 2),
                ('Total Graduates and Special', 3),
        ----------------------------------------
                ('Continuing Education', 1),
                ('Post-Baccalaureate', 2),
                ('Early High School', 3),
                ('Non-Degree UG', 4),
                ('International Exchange', 5),
                ('Senior Citizen Auditor', 6),
                ('Total Miscellaneous', 7)
                   ) AS ORDER_2(LABEL, N) ON X.STUDENT_SUB_CLASSIFICATION = ORDER_2.LABEL
        ORDER BY ORDER_1.N, ORDER_2.N --Gave it an ordering
        --(End 7)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        ------------------------------------------------------------------------------------------------------------------
        ------------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-03-31-Enrollment Summary & Class Distribution"
        name = "Enrollment Summary & Class Distribution (Fall 2024)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getEnrollmentSummary_2025SP(self):
        query = f"""
                                                              SELECT DISTINCT SEV.STUDENT_ID,
                                                                      CASE WHEN (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL) THEN
                                                                      CASE
                                                                          WHEN STUDENT_ACAD_LEVEL = 'UG' THEN CASE
                                                                            WHEN STUDENT_CURRENT_TYPE = 'ACE'
                                                                              THEN 'Early High School'
                                                                            WHEN STUDENT_CURRENT_TYPE = 'NDFTV'
                                                                              THEN 'International Exchange'
                                                                          WHEN PROGRAM = 'Accelerated Nursing'
                                                                              THEN 'Accelerated Nursing'
                                                                          WHEN PROGRAM = 'Non-Degree Seeking Students'
                                                                              THEN 'Non-Degree UG'
                                                                        WHEN STUDENT_CURRENT_TYPE = 'PB'
                                                                                THEN 'Post-Baccalaureate'

                                                                          WHEN STUDENT_CLASS_LEVEL = 'Freshman'
                                                                              THEN CASE
                                                                                       WHEN FIRST_ADMIT.STPR_ADMIT_STATUS = 'FY'
                                                                                           THEN 'First-Time Beginning Freshman'
                                                                                       ELSE 'Other Freshman' END
                                                                          WHEN STUDENT_CLASS_LEVEL = 'Sophomore'
                                                                              THEN 'Sophomores'
                                                                          WHEN STUDENT_CLASS_LEVEL = 'Junior'
                                                                              THEN 'Juniors'
                                                                          WHEN STUDENT_CLASS_LEVEL = 'Senior'
                                                                              THEN 'Seniors'
                                                                          ELSE 'Non-Degree UG' END
                                                                          WHEN STUDENT_ACAD_LEVEL = 'GR'
                                                                              THEN 'Master''s Candidates'
                                                                          WHEN STUDENT_ACAD_LEVEL = 'CE'
                                                                              THEN 'Continuing Education'
                                                                          END
                                                                          ELSE 'Senior Citizen Auditor' END AS STUDENT_SUB_CLASSIFICATION,
                                                                      CASE
                                                                          WHEN STUDENT_LOAD IN ('F', 'O') THEN CASE
                                                                                                                   WHEN 'M' IN (STUDENT_GENDER, ASSIGNED_GENDER)
                                                                                                                       THEN 'Full-Time Male'
                                                                                                                   WHEN 'F' IN (STUDENT_GENDER, ASSIGNED_GENDER)
                                                                                                                       THEN 'Full-Time Female'
                                                                                                                    ELSE 'Unknown' END
                                                                          ELSE CASE
                                                                                   WHEN 'M' IN (STUDENT_GENDER, ASSIGNED_GENDER)
                                                                                       THEN 'Part-Time Male'
                                                                                   WHEN 'F' IN (STUDENT_GENDER, ASSIGNED_GENDER)
                                                                                       THEN 'Part-Time Female'
                                                                                    ELSE 'Unknown' END END AS LOAD_GENDER
                                                      FROM STUDENT_ENROLLMENT_VIEW AS SEV
                                                               LEFT JOIN (SELECT STPR_STUDENT, STPR_ADMIT_STATUS
                                                                          FROM (SELECT STPR_STUDENT,
                                                                                       STPR_ADMIT_STATUS,
                                                                                       ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                                                                                           ORDER BY STUDENT_PROGRAMS_ADDDATE) AS ADMIT_RANK
                                                                                FROM STUDENT_PROGRAMS_VIEW
                                                                                WHERE STPR_ADMIT_STATUS IN ('FY', 'TR', 'RE')) ranked
                                                                          WHERE ADMIT_RANK = 1) AS FIRST_ADMIT
                                                                         ON SEV.STUDENT_ID = FIRST_ADMIT.STPR_STUDENT
                                                               LEFT JOIN (SELECT *
                                                                     FROM (SELECT STUDENT_ID,
                                                                                  STP_PROGRAM_TITLE                                                                 AS PROGRAM,
                                                                                  STP_CURRENT_STATUS,
                                                                                  ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                                                                                      ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS PROGRAM_RANK
                                                                           FROM STUDENT_ACAD_PROGRAMS_VIEW
                                                                           WHERE STP_START_DATE <=
                                                                                 (SELECT TOP 1 TERMS.TERM_END_DATE
                                                                                  FROM TERMS
                                                                                  WHERE TERMS_ID = '2025SP')) ranked
                                                                     WHERE PROGRAM_RANK = 1) AS SAPV
                                                                    ON SEV.STUDENT_ID = SAPV.STUDENT_ID
                                                                LEFT JOIN (VALUES
                                                                                ('6184447', 'F'),
                                                                                ('6184697', 'F'),
                                                                                ('6184977', 'F'),
                                                                                ('6185039', 'F'),
                                                                                ('6186217', 'M'),
                                                                                ('6186670', 'F'),
                                                                                ('6187467', 'F'),
                                                                                ('6187468', 'M'),
                                                                                ('6187470', 'F'),
                                                                                ('6188264', 'F'),
                                                                                ('6188541', 'F'),
                                                                                ('6188544', 'F'),
                                                                                ('6188731', 'F'),
                                                                                ('6188797', 'F'),
                                                                                ('6188940', 'F'),
                                                                                ('6189200', 'M'),
                                                                                ('6189252', 'M'),
                                                                                ('6189523', 'F'),
                                                                                ('6189571', 'F'),
                                                                                ('6189572', 'M'),
                                                                                ('6190155', 'F'),
                                                                                ('6191064', 'F'),
                                                                                ('6191066', 'F'),
                                                                                ('6191067', 'M'),
                                                                                ('6191303', 'M')
                                                                                ) AS Y(ID, ASSIGNED_GENDER)
                                                                                ON SEV.STUDENT_ID = Y.ID
                                                      WHERE ENROLL_TERM = '2025SP'
                                                        AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                                                        AND ((ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL) OR STUDENT_CURRENT_TYPE = 'SC') --Original Data
        """
        agg = lambda query: f"""
        --(Begin 7)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
SELECT X.*
FROM (
--(Begin 6)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
         SELECT Y.STUDENT_CLASSIFICATION,
                X.*
         FROM (
--(Begin 5)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  SELECT CASE
                             WHEN GROUPING(STUDENT_SUB_CLASSIFICATION) = 1
                                AND GROUPING(FRESHMAN) = 1
                                AND GROUPING(STUDENT_CLASSIFICATION) = 0
                                 THEN CASE
                                          WHEN STUDENT_CLASSIFICATION = 'Undergraduate'
                                              THEN 'Total Undergraduates'
                                          WHEN STUDENT_CLASSIFICATION = 'Graduate and Special'
                                              THEN 'Total Graduates and Special'
                                          WHEN STUDENT_CLASSIFICATION = 'Miscellaneous'
                                              THEN 'Total Miscellaneous' END
                            WHEN GROUPING(STUDENT_SUB_CLASSIFICATION) = 1
                            AND GROUPING(FRESHMAN) = 0
                            AND GROUPING(STUDENT_CLASSIFICATION) = 1
                                THEN CASE
                                    WHEN FRESHMAN = 'Freshman' THEN 'Total Freshman' END
                             WHEN GROUPING(STUDENT_SUB_CLASSIFICATION) = 1
                                AND GROUPING(STUDENT_CLASSIFICATION) = 1
                                 AND GROUPING(FRESHMAN) = 1 THEN 'Grand Total'
                             ELSE STUDENT_SUB_CLASSIFICATION END AS STUDENT_SUB_CLASSIFICATION,
                         SUM(PART_TIME_MALE)                     AS PART_TIME_MALE,
                         SUM(PART_TIME_FEMALE)                   AS PART_TIME_FEMALE,
                         SUM(PART_TIME_TOTAL)                    AS PART_TIME_TOTAL,
                         SUM(FULL_TIME_MALE)                     AS FULL_TIME_MALE,
                         SUM(FULL_TIME_FEMALE)                   AS FULL_TIME_FEMALE,
                         SUM(FULL_TIME_TOTAL)                    AS FULL_TIME_TOTAL,
                         SUM(MALE_TOTAL)                         AS MALE_TOTAL,
                         SUM(FEMALE_TOTAL)                       AS FEMALE_TOTAL,
                         SUM(TOTAL)                              AS TOTAL
                  FROM (
--(Begin 4)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                           SELECT STUDENT_CLASSIFICATION,
                                  FRESHMAN,
                                  STUDENT_SUB_CLASSIFICATION,
                                  PART_TIME_MALE,
                                  PART_TIME_FEMALE,
                                  (PART_TIME_MALE + PART_TIME_FEMALE)                                     AS PART_TIME_TOTAL,
                                  FULL_TIME_MALE,
                                  FULL_TIME_FEMALE,
                                  (FULL_TIME_MALE + FULL_TIME_FEMALE)                                     AS FULL_TIME_TOTAL,
                                  (PART_TIME_MALE + FULL_TIME_MALE)                                       AS MALE_TOTAL,
                                  (PART_TIME_FEMALE + FULL_TIME_FEMALE)                                   AS FEMALE_TOTAL,
                                  (PART_TIME_MALE + PART_TIME_FEMALE + FULL_TIME_MALE + FULL_TIME_FEMALE) AS TOTAL,
                                  UNKNOWN
                           FROM (
--(Begin 3)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                    SELECT STUDENT_CLASSIFICATION,
                                           FRESHMAN,
                                           STUDENT_SUB_CLASSIFICATION,
                                           [Part-Time Male]   AS PART_TIME_MALE,
                                           [Part-Time Female] AS PART_TIME_FEMALE,
                                           [Full-Time Male]   AS FULL_TIME_MALE,
                                           [Full-Time Female] AS FULL_TIME_FEMALE,
                                           [Unknown] AS UNKNOWN
                                    FROM (
--(Begin 2)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                             SELECT X.STUDENT_ID,
                                                    Y.STUDENT_CLASSIFICATION,
                                                    Z.FRESHMAN,
                                                    X.STUDENT_SUB_CLASSIFICATION,
                                                    X.LOAD_GENDER
                                             FROM (
---(Begin 1)-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                        {query}
--(End 1)--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                  ) AS X
                                    JOIN (VALUES ('First-Time Beginning Freshman', 'Undergraduate'),
                                                 ('Other Freshman', 'Undergraduate'),
                                                 ('Sophomores', 'Undergraduate'),
                                                 ('Juniors', 'Undergraduate'),
                                                 ('Seniors', 'Undergraduate'),
                                                 ('Master''s Candidates', 'Graduate and Special'),
                                                 ('Accelerated Nursing', 'Graduate and Special'),
                                                 ('Continuing Education', 'Miscellaneous'),
                                                 ('Post-Baccalaureate', 'Miscellaneous'),
                                                 ('Early High School', 'Miscellaneous'),
                                                 ('Non-Degree UG', 'Miscellaneous'),
                                                 ('International Exchange', 'Miscellaneous'),
                                                 ('Senior Citizen Auditor', 'Miscellaneous')
                                          ) AS Y(STUDENT_SUB_CLASSIFICATION, STUDENT_CLASSIFICATION)
                                             ON X.STUDENT_SUB_CLASSIFICATION = Y.STUDENT_SUB_CLASSIFICATION
                                    LEFT JOIN (VALUES ('First-Time Beginning Freshman', 'Freshman'),
                                                      ('Other Freshman', 'Freshman')
                                               ) AS Z(STUDENT_SUB_CLASSIFICATION, FRESHMAN)
                                        ON X.STUDENT_SUB_CLASSIFICATION = Z.STUDENT_SUB_CLASSIFICATION
                                             -- Added Student Classification
--(End 2)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                         ) AS X PIVOT (COUNT(STUDENT_ID) FOR LOAD_GENDER IN (
                                        [Part-Time Male],
                                        [Part-Time Female],
                                        [Full-Time Male],
                                        [Full-Time Female],
                                        [Unknown]
                                        )) AS X --Original Pivot Table
--(End 3)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                ) AS X --With Column Totals
--(End 4)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                       ) AS X
                  GROUP BY GROUPING SETS ((STUDENT_SUB_CLASSIFICATION), (STUDENT_CLASSIFICATION), (FRESHMAN), ())
--(End 5)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
              ) AS X
         JOIN (VALUES ('First-Time Beginning Freshman', 'Undergraduate'),
                       ('Other Freshman', 'Undergraduate'),
                       ('Sophomores', 'Undergraduate'),
                     ('Juniors', 'Undergraduate'),
                     ('Seniors', 'Undergraduate'),
                     ('Master''s Candidates', 'Graduate and Special'),
                     ('Accelerated Nursing', 'Graduate and Special'),
                     ('Continuing Education', 'Miscellaneous'),
                     ('Post-Baccalaureate', 'Miscellaneous'),
                     ('Early High School', 'Miscellaneous'),
                     ('Non-Degree UG', 'Miscellaneous'),
                     ('International Exchange', 'Miscellaneous'),
                     ('Senior Citizen Auditor', 'Miscellaneous'),
             --------------------------------------------------------------------
                    ('Total Freshman', 'Undergraduate'),
                    ('Total Undergraduates', 'Undergraduate'),
                    ('Total Graduates and Special', 'Graduate and Special'),
                    ('Total Miscellaneous', 'Miscellaneous'),
                    ('Grand Total', 'Grand Total')
                                          ) AS Y(STUDENT_SUB_CLASSIFICATION, STUDENT_CLASSIFICATION)
                                             ON X.STUDENT_SUB_CLASSIFICATION = Y.STUDENT_SUB_CLASSIFICATION
         --Appended on Student Classification Again
--(End 6)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
     ) AS X
LEFT JOIN (VALUES ('Undergraduate', 1),
                  ('Graduate and Special', 2),
                  ('Miscellaneous', 3),
                    ('Grand Total', 4))
    AS ORDER_1(LABEL, N)
ON X.STUDENT_CLASSIFICATION = ORDER_1.LABEL
LEFT JOIN (VALUES
        ('First-Time Beginning Freshman', 1),
        ('Other Freshman', 2),
        ('Total Freshman', 3),
        ('Sophomores', 4),
        ('Juniors', 5),
        ('Seniors', 6),
        ('Total Undergraduates', 7),
----------------------------------------
        ('Master''s Candidates', 1),
        ('Accelerated Nursing', 2),
        ('Total Graduates and Special', 3),
----------------------------------------
        ('Continuing Education', 1),
        ('Post-Baccalaureate', 2),
        ('Early High School', 3),
        ('Non-Degree UG', 4),
        ('International Exchange', 5),
        ('Senior Citizen Auditor', 6),
        ('Total Miscellaneous', 7)
           ) AS ORDER_2(LABEL, N) ON X.STUDENT_SUB_CLASSIFICATION = ORDER_2.LABEL
ORDER BY ORDER_1.N, ORDER_2.N --Gave it an ordering
--(End 7)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-03-31-Enrollment Summary & Class Distribution"
        name = "Enrollment Summary & Class Distribution (Spring 2025)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)


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
    Name: 2025-05-14-NC-SARA Collection
    Person: Amy Honchell
    Start Date: 2025-05-14
    End Date: 2025-05-14
    Description:
        I needed to get residencies of Master students.
    '''
    def getResidenciesOfMasterStudents(self):
        query = f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
                 SELECT STUDENT_ID,
                        STUDENT_LAST_NAME,
                        STUDENT_FIRST_NAME,
                        PROGRAM,
                        STATE
                 FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
                          SELECT SAPV.STUDENT_ID,
                                 SAPV.STUDENT_LAST_NAME,
                                 SAPV.STUDENT_FIRST_NAME,
                                 SAPV.STP_PROGRAM_TITLE         AS PROGRAM,
                                 PAV.STATE,
                                 ROW_NUMBER() OVER (PARTITION BY SAPV.STUDENT_ID
                                     ORDER BY ADDRESS_ADD_DATE DESC) AS RANK
                            FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                            JOIN PERSON_ADDRESSES_VIEW AS PAV ON SAPV.STUDENT_ID = PAV.ID
                            JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                            WHERE STP_PROGRAM_TITLE IN ('Master of Accountancy', 'Master of Social Work')
                            AND STP_START_DATE < '2025-01-01'
                            AND (STP_END_DATE IS NULL OR STP_END_DATE >= '2024-01-01')
                            AND PAV.ADDRESS_TYPE = 'H'
                            AND (STUDENT_PRIVACY_FLAG != 'Demo Student' OR STUDENT_PRIVACY_FLAG IS NULL)
        --(End 1)---------------------------------------------------------------------------------------------------------------
                      ) AS X
                 WHERE RANK = 1
        --(End 2)---------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 3)-------------------------------------------------------------------------------------------------------------
        SELECT PROGRAM,
               STATE,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        {query}
        --(End 2)---------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY PROGRAM, STATE
        --(End 3)---------------------------------------------------------------------------------------------------------------
        ORDER BY PROGRAM, STATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-05-14-NC-SARA Collection"
        name = "Residencies of Master Students"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    '''
    ID: Unknown
    Name: 2025-06-04-Active Degree Seeking Students Without Advisor
    Person: Carol Schopfer
    Start Date: 2025-06-04
    End Date: 2025-06-04
    Description:
        I needed to find out students who do not yet have an advisor.
    '''
    def getActiveStudentsWithoutAdvisor(self):
        query = f"""
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        SELECT DISTINCT STPR_STUDENT AS ID,
               FIRST_NAME,
               LAST_NAME
        FROM ODS_STUDENT_PROGRAMS AS SP
        LEFT JOIN Z01_PERSON ON SP.STPR_STUDENT = ID
        WHERE CURRENT_STATUS_DESC = 'Active'
        AND TITLE != 'Continuing Education'
        AND TITLE != 'Non-Degree Seeking Students'
        AND NOT EXISTS (
            SELECT 1
            FROM ODS_STUDENT_ADVISEMENT
            WHERE STAD_STUDENT = STPR_STUDENT
            AND (STAD_END_DATE IS NULL OR STAD_END_DATE > GETDATE())
        )
        --(End 1)-------------------------------------------------------------------------------------------------------
        ORDER BY ID
        """
        report = "2025-06-04-Active Degree Seeking Students Without Advisor"
        name = "Active Degree Seeking Students Without Advisor"
        self.save_query_results(query, db="ODS", func_dict=None)(report, name)

    '''
    ID: Unknown
    Name: 2025-06-13-MSW Program Review
    Person: Rebecca Schwartz
    Start Date: 2025-06-13
    End Date: 2025-06-13
    Description:
        I needed to calculate things for the program review of the MSW program.
    '''
    #---------Declared Majors and Minors--------------------------------------------------------------------------------
    def getMSWTermHeadcount(self):
        query = f"""
                 SELECT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID,
                STUDENT_LAST_NAME,
                STUDENT_FIRST_NAME
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND STP_START_DATE <= TERMS.TERM_END_DATE
           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
           AND (
             (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                 OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                 AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS MSW_STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Term Headcount"
        self.save_query_results(query, snapshot_term="2025SP", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getTermHeadcountByLoad(self):
        query = f"""
        SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
        TERMS.TERM_START_DATE,
        MAJORS.MAJ_DESC AS MAJOR,
        SAPV.STUDENT_ID,
        CASE
            WHEN STUDENT_LOAD IN ('F', 'O') THEN 'FT'
            WHEN STUDENT_LOAD IS NOT NULL THEN 'PT'
            ELSE 'Unknown' END AS LOAD
        FROM MAJORS
          CROSS JOIN TERMS
          CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
          LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                    ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
          LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
          LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
          LEFT JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON SEV.STUDENT_ID = SAPV.STUDENT_ID AND SEV.ENROLL_TERM = TERMS_ID
        WHERE TERMS.TERM_START_DATE >= '2019-08-01'
        AND TERMS.TERM_END_DATE < '2025-06-01'
        AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
        AND STP_START_DATE <= TERMS.TERM_END_DATE
        AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
        AND STP_CURRENT_STATUS != 'Did Not Enroll'
        AND (
        (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
         OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
         AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
         AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
         )
        )
        AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               LOAD,
               COUNT(*) AS MSW_STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE, LOAD
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Term Headcount By Load"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTermHeadcountByLevel(self):
        query = f"""
                 SELECT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID,
                STP_ACAD_LEVEL AS LEVEL
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND STP_START_DATE <= TERMS.TERM_END_DATE
           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
           AND (
             (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                 OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                 AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               LEVEL,
               COUNT(*) AS MSW_STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE, LEVEL
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Term Headcount By Level"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTermHeadcountByRace(self):
        query = f"""
                 SELECT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID,
                SAPV.IPEDS_RACE_ETHNIC_DESC AS RACE
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND STP_START_DATE <= TERMS.TERM_END_DATE
           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
           AND (
             (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                 OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                 AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               RACE,
               COUNT(*) AS MSW_STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
        {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE, RACE
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Term Headcount By Race"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTermHeadcountByVeteranStatus(self):
        query = f"""
                 SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM STA_OTHER_COHORTS_VIEW
                    WHERE STA_OTHER_COHORT_GROUPS = 'VETS'
                    AND STA_STUDENT = STUDENT_ID
                    AND (STP_START_DATE <= STA_OTHER_COHORT_END_DATES OR STA_OTHER_COHORT_END_DATES IS NULL)
                    AND (STP_END_DATE >= STA_OTHER_COHORT_START_DATES OR STP_END_DATE IS NULL)
                ) THEN 'Veteran' ELSE 'Not Veteran' END AS VET_STATUS
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND STP_START_DATE <= TERMS.TERM_END_DATE
           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
           AND (
             (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                 OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                 AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               VET_STATUS,
               COUNT(*) AS MSW_STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                 SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
                        TERMS.TERM_START_DATE,
                        MAJORS.MAJ_DESC AS MAJOR,
                        STUDENT_ID,
                        CASE WHEN EXISTS (
                            SELECT 1
                            FROM STA_OTHER_COHORTS_VIEW
                            WHERE STA_OTHER_COHORT_GROUPS = 'VETS'
                            AND STA_STUDENT = STUDENT_ID
                            AND (STP_START_DATE <= STA_OTHER_COHORT_END_DATES OR STA_OTHER_COHORT_END_DATES IS NULL)
                            AND (STP_END_DATE >= STA_OTHER_COHORT_START_DATES OR STP_END_DATE IS NULL)
                        ) THEN 'Veteran' ELSE 'Not Veteran' END AS VET_STATUS
                 FROM MAJORS
                          CROSS JOIN TERMS
                          CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                          LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                    ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                          LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                          LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                 WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                   AND TERMS.TERM_END_DATE < '2025-06-01'
                   AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                   AND STP_START_DATE <= TERMS.TERM_END_DATE
                   AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                   AND STP_CURRENT_STATUS != 'Did Not Enroll'
                   AND (
                     (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                         OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                         AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                         AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                         )
                     )
                   AND MAJORS.MAJ_DESC = 'Master of Social Work'
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE, VET_STATUS
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Term Headcount By Veteran Status"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTermHeadcountByAthleteStatus(self):
        query = f"""
                 SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM STA_OTHER_COHORTS_VIEW
                    JOIN (SELECT VAL_INTERNAL_CODE AS CODE, VAL_EXTERNAL_REPRESENTATION AS COHORT
                          FROM VALS
                          WHERE VALCODE_ID = 'INSTITUTION.COHORTS') AS COHORT_CODES
                    ON STA_OTHER_COHORTS_VIEW.STA_OTHER_COHORT_GROUPS = COHORT_CODES.CODE
                    WHERE COHORT IN (
                                        'Cheerleading',
                                        'Dance',
                                        'Football',
                                        'Indoor Men''s Track',
                                        'Indoor Women''s Track',
                                        'Men''s Basketball',
                                        'Men''s Cross Country',
                                        'Men''s Golf',
                                        'Men''s Soccer',
                                        'Outdoor Men''s Track',
                                        'Outdoor Women''s Track',
                                        'Women''s Basketball',
                                        'Women''s Cross Country',
                                        'Women''s Golf',
                                        'Women''s Soccer',
                                        'Women''s Softball',
                                        'Women''s Volleyball'
                                     )
                    AND STA_STUDENT = STUDENT_ID
                    AND (STP_START_DATE <= STA_OTHER_COHORT_END_DATES OR STA_OTHER_COHORT_END_DATES IS NULL)
                    AND (STP_END_DATE >= STA_OTHER_COHORT_START_DATES OR STP_END_DATE IS NULL)
                ) THEN 'Athlete' ELSE 'Not Athlete' END AS ATHLETE_STATUS
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND STP_START_DATE <= TERMS.TERM_END_DATE
           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
           AND (
             (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                 OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                 AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               ATHLETE_STATUS,
               COUNT(*) AS MSW_STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE, ATHLETE_STATUS
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Term Headcount By Athlete Status"
        self.save_query_results(query, snapshot_term="2025SP", func_dict = {"Agg": agg, "Names": names})(report, name)

    #---------New Students----------------------------------------------------------------------------------------------

    def getMSWNewStudentCountPerTerm(self):
            query = f"""
    --(Begin 2)------------------------------------------------------------------------------------------------------------
             SELECT TERM,
                    TERM_START_DATE,
                    MAJOR,
                    STUDENT_ID
             FROM (
    --(Begin 1)------------------------------------------------------------------------------------------------------------
                      SELECT DISTINCT TERMS.TERMS_ID                AS TERM,
                                      TERMS.TERM_START_DATE,
                                      MAJORS.MAJ_DESC               AS MAJOR,
                                      SAPV.STUDENT_ID,
                                      ROW_NUMBER() OVER (PARTITION BY STUDENT_ID, MAJORS.MAJ_DESC
                                          ORDER BY TERM_START_DATE) AS TERM_RANK
                      FROM MAJORS
                               CROSS JOIN TERMS
                               CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
    ------------------------------------------------------------------------------------------------------------------------
                               LEFT JOIN STPR_MAJOR_LIST_VIEW AS SMLV
                                         ON SAPV.STUDENT_ID = SMLV.STPR_STUDENT AND
                                            SAPV.STP_ACADEMIC_PROGRAM = SMLV.STPR_ACAD_PROGRAM
                               LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                               LEFT JOIN MAJORS AS ADDNL_MAJOR ON SMLV.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
    -----------------------------------------------------------------------------------------------------------------------
                      WHERE TERMS.TERM_START_DATE >= DATEADD(YEAR, -10, '2019-08-01')
                        AND TERMS.TERM_END_DATE < '2025-06-01'
                        AND (TERMS.TERMS_ID LIKE '%FA')
    ------------------------------------------------------------------------------------------------------------------------
                        AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
    ------------------------------------------------------------------------------------------------------------------------
                        AND (
                          (
                              MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                                  AND SAPV.STP_START_DATE <= TERMS.TERM_END_DATE
                                  AND (SAPV.STP_END_DATE >= TERMS.TERM_START_DATE OR SAPV.STP_END_DATE IS NULL)
                              )
                              OR (
                              MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                  AND SMLV.STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                  AND
                              (SMLV.STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                               SMLV.STPR_ADDNL_MAJOR_END_DATE IS NULL)
                              )
                          )
    ------------------------------------------------------------------------------------------------------------------------
                        AND MAJORS.MAJ_DESC = 'Master of Social Work'
    --(End 1)------------------------------------------------------------------------------------------------------------
                  ) AS X
             WHERE TERM_RANK = 1
               AND TERM_START_DATE >= '2019-08-01'
    --(End 2)------------------------------------------------------------------------------------------------------------
            """
            agg = lambda query: f"""
            --(Begin 3)------------------------------------------------------------------------------------------------------------
            SELECT TERM,
                   COUNT(*) AS MSW_STUDENT_COUNT
            FROM (
            --(Begin 2)------------------------------------------------------------------------------------------------------------
                {query}
            --(End 2)------------------------------------------------------------------------------------------------------------
                 ) AS X
            GROUP BY TERM, TERM_START_DATE
            --(End 3)------------------------------------------------------------------------------------------------------------
            ORDER BY TERM_START_DATE
            """
            names = lambda query: f"""
            SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
            ORDER BY LAST_NAME, FIRST_NAME
            """
            report = "2025-06-13-MSW Program Review"
            name = "New Student Count Per Term"
            self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getMSWNewStudentPercentChange(self):
        query = f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                  SELECT TERM,
                         TERM_START_DATE,
                         MAJOR,
                         STUDENT_ID
                  FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                                   SELECT DISTINCT TERMS.TERMS_ID                AS TERM,
                                                   TERMS.TERM_START_DATE,
                                                   MAJORS.MAJ_DESC               AS MAJOR,
                                                   SAPV.STUDENT_ID,
                                                   ROW_NUMBER() OVER (PARTITION BY STUDENT_ID, MAJORS.MAJ_DESC
                                                       ORDER BY TERM_START_DATE) AS TERM_RANK
                                   FROM MAJORS
                                            CROSS JOIN TERMS
                                            CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        ------------------------------------------------------------------------------------------------------------------------
                                            LEFT JOIN STPR_MAJOR_LIST_VIEW AS SMLV
                                                      ON SAPV.STUDENT_ID = SMLV.STPR_STUDENT AND
                                                         SAPV.STP_ACADEMIC_PROGRAM = SMLV.STPR_ACAD_PROGRAM
                                            LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                            LEFT JOIN MAJORS AS ADDNL_MAJOR ON SMLV.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
        -----------------------------------------------------------------------------------------------------------------------
                                   WHERE TERMS.TERM_START_DATE >= DATEADD(YEAR, -10, '2019-08-01')
                                     AND TERMS.TERM_END_DATE < '2025-06-01'
                                     AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS_ID LIKE '%SP')
        ------------------------------------------------------------------------------------------------------------------------
                                     AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
        ------------------------------------------------------------------------------------------------------------------------
                                     AND (
                                       (
                                           MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                                               AND SAPV.STP_START_DATE <= TERMS.TERM_END_DATE
                                               AND (SAPV.STP_END_DATE >= TERMS.TERM_START_DATE OR SAPV.STP_END_DATE IS NULL)
                                           )
                                           OR (
                                           MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                               AND SMLV.STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                               AND
                                           (SMLV.STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                            SMLV.STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                           )
                                       )
        ------------------------------------------------------------------------------------------------------------------------
                                     AND MAJORS.MAJ_DESC = 'Master of Social Work'
        --(End 1)------------------------------------------------------------------------------------------------------------
                               ) AS X
                          WHERE TERM_RANK = 1
                            AND TERM_START_DATE >= '2019-08-01'
        --(End 2)------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 4)------------------------------------------------------------------------------------------------------------
        WITH X AS (
        --(Begin 3)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        COUNT(*) AS MSW_STUDENT_COUNT
                 FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 2)------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY TERM, TERM_START_DATE
        --(End 3)------------------------------------------------------------------------------------------------------------
             )
            SELECT CONCAT(X.TERM, ' TO ', NEXT_TERM.SECOND) AS TERM_CHANGE,
                   X.MSW_STUDENT_COUNT AS FIRST_COUNT,
                   Y.MSW_STUDENT_COUNT AS NEXT_TERM_COUNT,
                   FORMAT(Y.MSW_STUDENT_COUNT * 1.0 / X.MSW_STUDENT_COUNT - 1, 'P') AS PERCENT_CHANGE
            FROM X LEFT JOIN (VALUES ('2019FA', '2020FA'),
                                 ('2020FA', '2021FA'),
                                 ('2021FA', '2022FA'),
                                 ('2022FA', '2023FA'),
                                 ('2023FA', '2024FA')
            ) AS NEXT_TERM(FIRST, SECOND) ON X.TERM = NEXT_TERM.FIRST
            JOIN X AS Y ON NEXT_TERM.SECOND = Y.TERM
        --(End 4)------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "New Student Percent Change"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getChangeMajor(self):
        query = f"""
                                            SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
                                                    TERMS.TERM_START_DATE,
                                                    MAJORS.MAJ_DESC AS MAJOR,
                                                    STUDENT_ID
                                    FROM MAJORS
                                             CROSS JOIN TERMS
                                             CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                             LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                                       ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                          STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                             LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                             LEFT JOIN MAJORS AS ADDNL_MAJOR
                                                       ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                                    WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                                      AND TERMS.TERM_END_DATE < '2025-06-01'
                                      AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                                      AND STP_START_DATE <= TERMS.TERM_END_DATE
                                      AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                                      AND STP_CURRENT_STATUS != 'Did Not Enroll'
                                      AND (
                                        (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                                            OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                            AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                            AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                                 STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                            )
                                        )
        """
        agg = lambda query: f"""
        --(Begin 5)-------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               MAJOR,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 4)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        TERM_START_DATE,
                        MAJOR,
                        STUDENT_ID
                 FROM (
        --(Begin 3)------------------------------------------------------------------------------------------------------------
                          SELECT TERM,
                                 TERM_START_DATE,
                                 MAJOR,
                                 STUDENT_ID,
                                 CASE
                                     WHEN MAX(CASE WHEN MAJOR_2 = MAJOR THEN 1 ELSE 0 END) = 0 THEN 'Changed Major'
                                     ELSE 'Kept Major' END AS MAJOR_CHANGE
                          FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                                   SELECT X.TERM,
                                          X.TERM_START_DATE,
                                          X.MAJOR,
                                          X.STUDENT_ID,
                                          Y.MAJOR AS MAJOR_2
                                   FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
                                        ) AS X
                                            LEFT JOIN (VALUES ('2019FA', '2020SP'),
                                                              ('2020SP', '2020FA'),
                                                              ('2020FA', '2021SP'),
                                                              ('2021SP', '2021FA'),
                                                              ('2021FA', '2022SP'),
                                                              ('2022SP', '2022FA'),
                                                              ('2022FA', '2023SP'),
                                                              ('2023SP', '2023FA'),
                                                              ('2023FA', '2024SP'),
                                                              ('2024SP', '2024FA'),
                                                              ('2024FA', '2025SP')) AS NEXT_TERM(FIRST, SECOND)
                                                      ON X.TERM = NEXT_TERM.FIRST
                                            JOIN (SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
                                                                  TERMS.TERM_START_DATE,
                                                                  MAJORS.MAJ_DESC AS MAJOR,
                                                                  STUDENT_ID
                                                  FROM MAJORS
                                                           CROSS JOIN TERMS
                                                           CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                           LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                                                     ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                                        STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                                           LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                                           LEFT JOIN MAJORS AS ADDNL_MAJOR
                                                                     ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                                                  WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                                                    AND TERMS.TERM_END_DATE < '2025-06-01'
                                                    AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                                                    AND STP_START_DATE <= TERMS.TERM_END_DATE
                                                    AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                                                    AND STP_CURRENT_STATUS != 'Did Not Enroll'
                                                    AND (
                                                      (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                                                          OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                                          AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                                          AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                                               STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                                          )
                                                      )) AS Y ON X.STUDENT_ID = Y.STUDENT_ID AND NEXT_TERM.SECOND = Y.TERM
                                   WHERE X.MAJOR IN (
                                                     'Master of Social Work'
                                       )
        --(End 2)------------------------------------------------------------------------------------------------------------
                               ) AS X
                          GROUP BY TERM, TERM_START_DATE, MAJOR, STUDENT_ID
        --(End 3)------------------------------------------------------------------------------------------------------------
                      ) AS X
                WHERE MAJOR_CHANGE = 'Changed Major'
        --(End 4)------------------------------------------------------------------------------------------------------------
            ) AS X
        GROUP BY TERM, TERM_START_DATE, MAJOR
        --(End 5)-------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Change Major"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getDeclareMajor(self):
        query = f"""
                 SELECT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS SMLV
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON SMLV.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND STP_START_DATE <= TERMS.TERM_END_DATE
           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
            AND (
              (
                  MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                      AND SAPV.STP_START_DATE <= TERMS.TERM_END_DATE
                      AND SAPV.STP_START_DATE >= TERMS.TERM_START_DATE
                  )
                  OR (
                      MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                      AND SMLV.STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                      AND SMLV.STPR_ADDNL_MAJOR_START_DATE >= TERMS.TERM_START_DATE
                  )
              )
            AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS MSW_STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
        {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Declare Major"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    #----------Course Enrollments---------------------------------------------------------------------------------------

    def getMSWSCHPerTerm(self):
        query = f"""
                 SELECT DISTINCT TERMS.TERMS_ID    AS TERM,
                TERM_START_DATE,
                SAPV.STUDENT_ID,
                SEV.SECTION_COURSE_TITLE,
                SEV.SECTION_COURSE_NAME,
                SEV.ENROLL_CREDITS
         FROM MAJORS
         CROSS JOIN TERMS
         CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
         LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
         LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
         LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON SAPV.STUDENT_ID = SEV.STUDENT_ID AND TERMS_ID = SEV.ENROLL_TERM
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
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
                 SELECT DISTINCT TERMS.TERMS_ID    AS TERM,
                TERM_START_DATE,
                SAPV.STUDENT_ID,
                SEV.SECTION_COURSE_TITLE,
                SEV.SECTION_COURSE_NAME,
                SEV.ENROLL_CREDITS
         FROM MAJORS
         CROSS JOIN TERMS
         CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
         LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
         LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
         LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON SAPV.STUDENT_ID = SEV.STUDENT_ID AND TERMS_ID = SEV.ENROLL_TERM
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
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Master of Social Work'
           -------------------------------------------------------------------------------------------------------------
           AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "SCH Per Term"
        self.save_query_results(query, snapshot_term="2025SP", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getMSWAvgEnrollmentPerCourse(self):
        query = f"""
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
        """
        agg = lambda query: f"""
        --(Begin 3)-------------------------------------------------------------------------------------------------------------
        SELECT COURSE_TITLE,
               COURSE_NAME,
               AVG(TOTAL_ENROLLMENT) AS AVG_ENROLLMENT
        FROM (
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
                 SELECT COURSE_TITLE,
                        COURSE_NAME,
                        COUNT(STUDENT_ID) AS TOTAL_ENROLLMENT
                 FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)-------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY TERM, TERM_START_DATE, COURSE_TITLE, COURSE_NAME
        --(End 2)-------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY COURSE_TITLE, COURSE_NAME
        --(End 3)-------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Avg Enrollment Per Course"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getMSWPercentUnderenrolled(self):
        query = f"""
                                                    SELECT DISTINCT TERMS.TERMS_ID           AS TERM,
                                                            TERM_START_DATE,
                                                            SAPV.STUDENT_ID,
                                                            SEV.SECTION_COURSE_NAME  AS COURSE_NAME,
                                                            SEV.SECTION_COURSE_TITLE AS COURSE_TITLE,
                                                            SEV.ENROLL_CREDITS
                                            FROM MAJORS
                                                     CROSS JOIN TERMS
                                                     CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                     LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                                               ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                                  STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                                     LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                                     LEFT JOIN MAJORS AS ADDNL_MAJOR
                                                               ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
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
                                                    (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                                     STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                                    )
                                                )
                                              AND MAJORS.MAJ_DESC = 'Master of Social Work'
                                              ---------------------------------------------------------------------------------
                                              AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                """
        agg = lambda query: f"""
                --(Begin 5)------------------------------------------------------------------------------------------------------------
        SELECT FORMAT(SUM(UNDER_ENROLLED) * 1.0 / COUNT(*), 'P') AS PERCENT_UNDER_ENROLLED
        FROM (
        --(Begin 4)-------------------------------------------------------------------------------------------------------------
                 SELECT COURSE_TITLE,
                        COURSE_NAME,
                        CASE WHEN AVG_ENROLLMENT < 7 THEN 1 ELSE 0 END AS UNDER_ENROLLED
                 FROM (
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
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
                                        ) AS X
                                   GROUP BY TERM, TERM_START_DATE, COURSE_TITLE, COURSE_NAME
        --(End 2)--------------------------------------------------------------------------------------------------------------
                               ) AS X
                          GROUP BY COURSE_TITLE, COURSE_NAME
        --(End 3)--------------------------------------------------------------------------------------------------------------
                      ) AS X
        --(End 4)---------------------------------------------------------------------------------------------------------------
             ) AS X
        --(End 5)---------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Percent Underenrolled"
        self.save_query_results(query, snapshot_term="2025SP", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getMSWFacultyCourseEnrollments(self):
        query = f"""
        --(Begin 1)--------------------------------------------------------------------------------------
                 SELECT STUDENTS.*,
                        SEV.SECTION_COURSE_NAME          AS COURSE_NAME,
                        SEV.SECTION_COURSE_TITLE         AS COURSE_TITLE,
                        COURSE_SECTIONS.SEC_FACULTY_INFO AS FACULTY
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
                         AND TERMS.TERM_END_DATE < '2025-06-01'
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
                          JOIN COURSE_SECTIONS ON SEV.SECTION_COURSE_SECTION_ID = COURSE_SECTIONS_ID
                 WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT FACULTY,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
         ) AS X
        GROUP BY FACULTY
        --(End 2)-----------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Faculty Course Enrollments"
        self.save_query_results(query, snapshot_term="2025SP", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getMSWFacultyCourseEnrollmentsByLoad(self):
        query = f"""
                 SELECT STUDENTS.*,
                SEV.SECTION_COURSE_NAME          AS COURSE_NAME,
                SEV.SECTION_COURSE_TITLE         AS COURSE_TITLE,
                COURSE_SECTIONS.SEC_FACULTY_INFO AS FACULTY,
                CASE WHEN SEV.STUDENT_LOAD IN ('F', 'O') THEN 'FT' ELSE 'PT' END AS LOAD
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
                 AND TERMS.TERM_END_DATE < '2025-06-01'
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
                  JOIN COURSE_SECTIONS ON SEV.SECTION_COURSE_SECTION_ID = COURSE_SECTIONS_ID
         WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT FACULTY,
               LOAD,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
        {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY FACULTY, LOAD
        --(End 2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Faculty Course Enrollments By Load"
        self.save_query_results(query, snapshot_term="2025SP", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getMSWFacultyCourseEnrollmentsByLevel(self):
        query = f"""
                 SELECT STUDENTS.*,
                SEV.SECTION_COURSE_NAME          AS COURSE_NAME,
                SEV.SECTION_COURSE_TITLE         AS COURSE_TITLE,
                COURSE_SECTIONS.SEC_FACULTY_INFO AS FACULTY,
                SEV.STUDENT_ACAD_LEVEL AS LEVEL
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
                 AND TERMS.TERM_END_DATE < '2025-06-01'
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
                  JOIN COURSE_SECTIONS ON SEV.SECTION_COURSE_SECTION_ID = COURSE_SECTIONS_ID
         WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT FACULTY,
               LEVEL,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
        {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY FACULTY, LEVEL
        --(End 2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Faculty Course Enrollments By Level"
        self.save_query_results(query, snapshot_term="2025SP", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getMSWFacultyCourseEnrollmentsByRace(self):
        query = f"""
                 SELECT STUDENTS.STUDENT_ID,
                SEV.SECTION_COURSE_NAME          AS COURSE_NAME,
                SEV.SECTION_COURSE_TITLE         AS COURSE_TITLE,
                COURSE_SECTIONS.SEC_FACULTY_INFO AS FACULTY,
                STUDENTS.RACE
         FROM (SELECT DISTINCT TERMS.TERMS_ID AS TERM,
                               TERMS.TERM_START_DATE,
                               SAPV.STUDENT_ID,
                               SAPV.IPEDS_RACE_ETHNIC_DESC AS RACE
               FROM MAJORS
                        CROSS JOIN TERMS
                        CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                        LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                  ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                        LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                        LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
               WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                 AND TERMS.TERM_END_DATE < '2025-06-01'
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
                  JOIN COURSE_SECTIONS ON SEV.SECTION_COURSE_SECTION_ID = COURSE_SECTIONS_ID
         WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT FACULTY,
               RACE,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY FACULTY, RACE
        --(End 2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Faculty Course Enrollments By Race"
        self.save_query_results(query, snapshot_term="2025SP", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getMSWCourseCompletionRates(self):
        query = f"""
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
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT COURSE_TITLE,
               COURSE_NAME,
               FORMAT(AVG(COMPLETED * 1.0), 'P') AS COMPLETION_RATE,
               COUNT(*) AS ENROLLMENT_COUNT
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY COURSE_TITLE, COURSE_NAME
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY COURSE_NAME, COURSE_TITLE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Course Completion Rates"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    # ----------Completion Rates---------------------------------------------------------------------------------------

    def getMSWGraduationRateByCohort(self):
        query = f"""
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
        """
        agg = lambda query: f"""
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
                {query}
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
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Graduation Rate By Cohort"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    #-------------------------------------------------------------------------------------------------------------------

    def getMSWFacultyCourseEnrollmentsByLevel_Pivoted(self):
        query = f"""
                 SELECT STUDENTS.STUDENT_ID,
                COURSE_SECTIONS.SEC_FACULTY_INFO AS FACULTY,
                SEV.STUDENT_ACAD_LEVEL AS LEVEL
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
                 AND TERMS.TERM_END_DATE < '2025-06-01'
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
                  JOIN COURSE_SECTIONS ON SEV.SECTION_COURSE_SECTION_ID = COURSE_SECTIONS_ID
         WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT FACULTY,
               [GR]
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
        {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(STUDENT_ID) FOR LEVEL IN ([GR])) AS X
        --(End 2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Faculty Course Enrollments By Level (Pivoted)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getMSWFacultyCourseEnrollmentsByLoad_Pivoted(self):
        query = f"""
                 SELECT STUDENTS.STUDENT_ID,
                COURSE_SECTIONS.SEC_FACULTY_INFO AS FACULTY,
                CASE WHEN SEV.STUDENT_LOAD IN ('F', 'O') THEN 'FT' ELSE 'PT' END AS LOAD
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
                 AND TERMS.TERM_END_DATE < '2025-06-01'
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
                  JOIN COURSE_SECTIONS ON SEV.SECTION_COURSE_SECTION_ID = COURSE_SECTIONS_ID
         WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT FACULTY,
               [FT],
               [PT]
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
        {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(STUDENT_ID) FOR LOAD IN ([FT], [PT])) AS X
        --(End 2)--------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Faculty Course Enrollments By Load (Pivoted)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getMSWFacultyCourseEnrollmentsByRace_Pivoted(self):
        query = f"""
                 SELECT STUDENTS.STUDENT_ID,
                COURSE_SECTIONS.SEC_FACULTY_INFO AS FACULTY,
                STUDENTS.RACE
         FROM (SELECT DISTINCT TERMS.TERMS_ID AS TERM,
                               TERMS.TERM_START_DATE,
                               SAPV.STUDENT_ID,
                               SAPV.IPEDS_RACE_ETHNIC_DESC AS RACE
               FROM MAJORS
                        CROSS JOIN TERMS
                        CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                        LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                  ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                        LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                        LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
               WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                 AND TERMS.TERM_END_DATE < '2025-06-01'
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
                  JOIN COURSE_SECTIONS ON SEV.SECTION_COURSE_SECTION_ID = COURSE_SECTIONS_ID
         WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT FACULTY,
               [American Indian],
               [Hispanic/Latino],
               [Two or More Races],
               [Unknown],
               [White]
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
        {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(STUDENT_ID) FOR RACE IN (
               [American Indian],
               [Hispanic/Latino],
               [Two or More Races],
               [Unknown],
               [White])) AS X
        --(End 2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Faculty Course Enrollments By Race (Pivoted)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getTermHeadcountByAthleteStatus_Pivoted(self):
        query = f"""
                          SELECT DISTINCT TERMS.TERMS_ID             AS TERM,
                                  STUDENT_ID,
                                  CASE
                                      WHEN EXISTS (SELECT 1
                                                   FROM STA_OTHER_COHORTS_VIEW
                                                            JOIN (SELECT VAL_INTERNAL_CODE AS CODE, VAL_EXTERNAL_REPRESENTATION AS COHORT
                                                                  FROM VALS
                                                                  WHERE VALCODE_ID = 'INSTITUTION.COHORTS') AS COHORT_CODES
                                                                 ON STA_OTHER_COHORTS_VIEW.STA_OTHER_COHORT_GROUPS = COHORT_CODES.CODE
                                                   WHERE COHORT IN (
                                                                    'Cheerleading',
                                                                    'Dance',
                                                                    'Football',
                                                                    'Indoor Men''s Track',
                                                                    'Indoor Women''s Track',
                                                                    'Men''s Basketball',
                                                                    'Men''s Cross Country',
                                                                    'Men''s Golf',
                                                                    'Men''s Soccer',
                                                                    'Outdoor Men''s Track',
                                                                    'Outdoor Women''s Track',
                                                                    'Women''s Basketball',
                                                                    'Women''s Cross Country',
                                                                    'Women''s Golf',
                                                                    'Women''s Soccer',
                                                                    'Women''s Softball',
                                                                    'Women''s Volleyball'
                                                       )
                                                     AND STA_STUDENT = STUDENT_ID
                                                     AND (STP_START_DATE <= STA_OTHER_COHORT_END_DATES OR
                                                          STA_OTHER_COHORT_END_DATES IS NULL)
                                                     AND (STP_END_DATE >= STA_OTHER_COHORT_START_DATES OR STP_END_DATE IS NULL))
                                          THEN 'Athlete'
                                      ELSE 'Not Athlete' END AS ATHLETE_STATUS
                  FROM MAJORS
                           CROSS JOIN TERMS
                           CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                           LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                     ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                           LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                           LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                  WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                    AND TERMS.TERM_END_DATE < '2025-06-01'
                    AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                    AND STP_START_DATE <= TERMS.TERM_END_DATE
                    AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                    AND STP_CURRENT_STATUS != 'Did Not Enroll'
                    AND (
                      (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                          OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                          AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                          AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                          )
                      )
                    AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
        --(Begin 3)------------------------------------------------------------------------------------------------------------
        SELECT X.*
        FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        [Athlete],
                        [Not Athlete]
                 FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
                      ) AS X
                          PIVOT (COUNT(STUDENT_ID) FOR ATHLETE_STATUS IN ([Athlete], [Not Athlete])) AS X
        --(End 2)------------------------------------------------------------------------------------------------------------
             ) AS X
        JOIN TERMS ON TERM = TERMS_ID
        --(End 3)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Term Headcount By Athlete Status (Pivoted)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTermHeadcountByLevel_Pivoted(self):
        query = f"""
                  SELECT TERMS.TERMS_ID AS TERM,
                         STUDENT_ID,
                         STP_ACAD_LEVEL AS LEVEL
                  FROM MAJORS
                           CROSS JOIN TERMS
                           CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                           LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                     ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                           LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                           LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                  WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                    AND TERMS.TERM_END_DATE < '2025-06-01'
                    AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                    AND STP_START_DATE <= TERMS.TERM_END_DATE
                    AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                    AND STP_CURRENT_STATUS != 'Did Not Enroll'
                    AND (
                      (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                          OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                          AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                          AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                          )
                      )
                    AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
        --(Begin 3)-----------------------------------------------------------------------------------------------------------
        SELECT X.*
        FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        [GR]
                 FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
                      ) AS X
                          PIVOT (COUNT(STUDENT_ID) FOR LEVEL IN ([GR])) AS X
        --(End 2)------------------------------------------------------------------------------------------------------------
             ) AS X
        JOIN TERMS ON X.TERM = TERMS.TERMS_ID
        --(End 3)------------------------------------------------------------------------------------------------------------
        ORDER BY TERMS.TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Term Headcount By Level (Pivoted)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTermHeadcountByLoad_Pivoted(self):
        query = f"""
                  SELECT DISTINCT TERMS.TERMS_ID         AS TERM,
                                  SAPV.STUDENT_ID,
                                  CASE
                                      WHEN STUDENT_LOAD IN ('F', 'O') THEN 'FT'
                                      WHEN STUDENT_LOAD IS NOT NULL THEN 'PT'
                                      ELSE 'Unknown' END AS LOAD
                  FROM MAJORS
                           CROSS JOIN TERMS
                           CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                           LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                     ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                           LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                           LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                           LEFT JOIN STUDENT_ENROLLMENT_VIEW AS SEV
                                     ON SEV.STUDENT_ID = SAPV.STUDENT_ID AND SEV.ENROLL_TERM = TERMS_ID
                  WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                    AND TERMS.TERM_END_DATE < '2025-06-01'
                    AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                    AND STP_START_DATE <= TERMS.TERM_END_DATE
                    AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                    AND STP_CURRENT_STATUS != 'Did Not Enroll'
                    AND (
                      (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                          OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                          AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                          AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                          )
                      )
                    AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
        --(Begin 3)------------------------------------------------------------------------------------------------------------
        SELECT X.*
        FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        [FT],
                        [PT],
                        [Unknown]
                 FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT TERMS.TERMS_ID         AS TERM,
                                          SAPV.STUDENT_ID,
                                          CASE
                                              WHEN STUDENT_LOAD IN ('F', 'O') THEN 'FT'
                                              WHEN STUDENT_LOAD IS NOT NULL THEN 'PT'
                                              ELSE 'Unknown' END AS LOAD
                          FROM MAJORS
                                   CROSS JOIN TERMS
                                   CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                   LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                             ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                   LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                   LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                                   LEFT JOIN STUDENT_ENROLLMENT_VIEW AS SEV
                                             ON SEV.STUDENT_ID = SAPV.STUDENT_ID AND SEV.ENROLL_TERM = TERMS_ID
                          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                            AND TERMS.TERM_END_DATE < '2025-06-01'
                            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                            AND STP_START_DATE <= TERMS.TERM_END_DATE
                            AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                            AND STP_CURRENT_STATUS != 'Did Not Enroll'
                            AND (
                              (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                                  OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                  AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                  AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                  )
                              )
                            AND MAJORS.MAJ_DESC = 'Master of Social Work'
        --(End 1)------------------------------------------------------------------------------------------------------------
                      ) AS X
                          PIVOT (COUNT(STUDENT_ID) FOR LOAD IN (
                         [FT],
                         [PT],
                         [Unknown])) AS X
        --(End 2)------------------------------------------------------------------------------------------------------------
             ) AS X
        JOIN TERMS ON TERM = TERMS_ID
        --(End 3)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Term Headcount By Load (Pivoted)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTermHeadcountByLoad_Unknowns(self):
        query = f"""
        SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
        MAJORS.MAJ_DESC AS MAJOR,
        SAPV.*
        FROM MAJORS
          CROSS JOIN TERMS
          CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
          LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                    ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
          LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
          LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
          LEFT JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON SEV.STUDENT_ID = SAPV.STUDENT_ID AND SEV.ENROLL_TERM = TERMS_ID
        WHERE TERMS.TERM_START_DATE >= '2019-08-01'
        AND TERMS.TERM_END_DATE < '2025-06-01'
        AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
        AND STP_START_DATE <= TERMS.TERM_END_DATE
        AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
        AND STP_CURRENT_STATUS != 'Did Not Enroll'
        AND (
        (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
         OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
         AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
         AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
         )
        )
        AND MAJORS.MAJ_DESC = 'Master of Social Work'
        AND STUDENT_LOAD IS NULL
        """
        report = "2025-06-13-MSW Program Review"
        name = "Term Headcount By Load (Unknowns)"
        self.save_query_results(query, snapshot_term="2025SP")(report, name)

    def getTermHeadcountByRace_Pivoted(self):
        query = f"""
          SELECT TERMS.TERMS_ID         AS TERM,
            STUDENT_ID,
             IPEDS_RACE_ETHNIC_DESC AS RACE
          FROM MAJORS
                   CROSS JOIN TERMS
                   CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                   LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                             ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                   LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                   LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND STP_START_DATE <= TERMS.TERM_END_DATE
            AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
            AND STP_CURRENT_STATUS != 'Did Not Enroll'
            AND (
              (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                  OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                  AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                  AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                  )
              )
            AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
        --(Begin 3)------------------------------------------------------------------------------------------------------------
        SELECT X.*
        FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        [American Indian],
                        [Hispanic/Latino],
                        [Two or More Races],
                        [Unknown],
                        [White]
                 FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
        {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
                      ) AS X
                          PIVOT (COUNT(STUDENT_ID) FOR RACE IN (
                         [American Indian],
                         [Hispanic/Latino],
                         [Two or More Races],
                         [Unknown],
                         [White]
                         )) AS X
        --(End 2)------------------------------------------------------------------------------------------------------------
             ) AS X
        JOIN TERMS ON TERM = TERMS_ID
        --(Begin 3)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Term Headcount By Race (Pivoted)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTermHeadcountByVeteranStatus_Pivoted(self):
        query = f"""
                          SELECT DISTINCT TERMS.TERMS_ID             AS TERM,
                         STUDENT_ID,
                         CASE
                             WHEN EXISTS (SELECT 1
                                          FROM STA_OTHER_COHORTS_VIEW
                                          WHERE STA_OTHER_COHORT_GROUPS = 'VETS'
                                            AND STA_STUDENT = STUDENT_ID
                                            AND (STP_START_DATE <= STA_OTHER_COHORT_END_DATES OR
                                                 STA_OTHER_COHORT_END_DATES IS NULL)
                                            AND (STP_END_DATE >= STA_OTHER_COHORT_START_DATES OR STP_END_DATE IS NULL))
                                 THEN 'Veteran'
                             ELSE 'Not Veteran' END AS VET_STATUS
                  FROM MAJORS
                           CROSS JOIN TERMS
                           CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                           LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                     ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                           LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                           LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                  WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                    AND TERMS.TERM_END_DATE < '2025-06-01'
                    AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                    AND STP_START_DATE <= TERMS.TERM_END_DATE
                    AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                    AND STP_CURRENT_STATUS != 'Did Not Enroll'
                    AND (
                      (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                          OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                          AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                          AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                          )
                      )
                    AND MAJORS.MAJ_DESC = 'Master of Social Work'
        """
        agg = lambda query: f"""
        --(Begin 3)------------------------------------------------------------------------------------------------------------
        SELECT X.*
        FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        [Veteran],
                        [Not Veteran]
                 FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT TERMS.TERMS_ID             AS TERM,
                                 STUDENT_ID,
                                 CASE
                                     WHEN EXISTS (SELECT 1
                                                  FROM STA_OTHER_COHORTS_VIEW
                                                  WHERE STA_OTHER_COHORT_GROUPS = 'VETS'
                                                    AND STA_STUDENT = STUDENT_ID
                                                    AND (STP_START_DATE <= STA_OTHER_COHORT_END_DATES OR
                                                         STA_OTHER_COHORT_END_DATES IS NULL)
                                                    AND (STP_END_DATE >= STA_OTHER_COHORT_START_DATES OR STP_END_DATE IS NULL))
                                         THEN 'Veteran'
                                     ELSE 'Not Veteran' END AS VET_STATUS
                          FROM MAJORS
                                   CROSS JOIN TERMS
                                   CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                   LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                             ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                   LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                   LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                            AND TERMS.TERM_END_DATE < '2025-06-01'
                            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                            AND STP_START_DATE <= TERMS.TERM_END_DATE
                            AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                            AND STP_CURRENT_STATUS != 'Did Not Enroll'
                            AND (
                              (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                                  OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                  AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                  AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                  )
                              )
                            AND MAJORS.MAJ_DESC = 'Master of Social Work'
        --(End 1)------------------------------------------------------------------------------------------------------------
                      ) AS X
                          PIVOT (COUNT(STUDENT_ID) FOR VET_STATUS IN ([Veteran], [Not Veteran])) AS X
        --(End 2)------------------------------------------------------------------------------------------------------------
             ) AS X
        JOIN TERMS ON TERM = TERMS_ID
        --(End 3)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Term Headcount By Veteran Status (Pivoted)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getStudentMajorCount(self):
        query = f"""
                 SELECT DISTINCT YEAR_ID         AS YEAR,
                         MAJORS.MAJ_DESC AS MAJOR,
                         STUDENT_ID
         FROM MAJORS
                  CROSS JOIN (VALUES ('2025', CAST('2025-01-01 00:00:00' AS DATETIME)),
                                     ('2024', CAST('2024-01-01 00:00:00' AS DATETIME)),
                                     ('2023', CAST('2023-01-01 00:00:00' AS DATETIME)),
                                     ('2022', CAST('2022-01-01 00:00:00' AS DATETIME)),
                                     ('2021', CAST('2021-01-01 00:00:00' AS DATETIME))) AS YEARS(YEAR_ID, START)
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE STP_START_DATE < DATEADD(YEAR, 1, START)
           AND (STP_END_DATE >= START OR STP_END_DATE IS NULL)
           AND (
             (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                 OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                 AND STPR_ADDNL_MAJOR_START_DATE < DATEADD(YEAR, 1, START)
                 AND (STPR_ADDNL_MAJOR_END_DATE >= START OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT MAJOR,
               [2021],
               [2022],
               [2023],
               [2024],
               [2025]
        FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(STUDENT_ID) FOR YEAR IN ([2021],
                                               [2022],
                                               [2023],
                                               [2024],
                                               [2025])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Student Major Counts"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getCountPerYear(self):
        query = f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
         SELECT TERM,
                TERM_START_DATE,
                MAJOR,
                STUDENT_ID
         FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT TERMS.TERMS_ID                AS TERM,
                                          TERMS.TERM_START_DATE,
                                          MAJORS.MAJ_DESC               AS MAJOR,
                                          SAPV.STUDENT_ID,
                                          ROW_NUMBER() OVER (PARTITION BY STUDENT_ID, MAJORS.MAJ_DESC
                                              ORDER BY TERM_START_DATE) AS TERM_RANK
                          FROM MAJORS
                                   CROSS JOIN TERMS
                                   CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        ------------------------------------------------------------------------------------------------------------------------
                                   LEFT JOIN STPR_MAJOR_LIST_VIEW AS SMLV
                                             ON SAPV.STUDENT_ID = SMLV.STPR_STUDENT AND
                                                SAPV.STP_ACADEMIC_PROGRAM = SMLV.STPR_ACAD_PROGRAM
                                   LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                   LEFT JOIN MAJORS AS ADDNL_MAJOR ON SMLV.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
        -----------------------------------------------------------------------------------------------------------------------
                          WHERE TERMS.TERM_START_DATE >= DATEADD(YEAR, -10, '2019-08-01')
                            AND TERMS.TERM_END_DATE < '2025-06-01'
                            AND (TERMS.TERMS_ID LIKE '%FA')
        ------------------------------------------------------------------------------------------------------------------------
                            AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
        ------------------------------------------------------------------------------------------------------------------------
                            AND (
                              (
                                  MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                                      AND SAPV.STP_START_DATE <= TERMS.TERM_END_DATE
                                      AND (SAPV.STP_END_DATE >= TERMS.TERM_START_DATE OR SAPV.STP_END_DATE IS NULL)
                                  )
                                  OR (
                                  MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                      AND SMLV.STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                      AND
                                  (SMLV.STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                   SMLV.STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                  )
                              )
        ------------------------------------------------------------------------------------------------------------------------
                            AND MAJORS.MAJ_DESC = 'Master of Social Work'
        --(End 1)------------------------------------------------------------------------------------------------------------
                      ) AS X
                 WHERE TERM_RANK = 1
                   AND TERM_START_DATE >= '2019-08-01'
        --(End 2)------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 3)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS MSW_STUDENT_COUNT
        FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                {query}
        --(End 2)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 3)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Count Per Year"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getPercentChangeYearToYear(self):
        query = f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                  SELECT TERM,
                         TERM_START_DATE,
                         MAJOR,
                         STUDENT_ID
                  FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                                   SELECT DISTINCT TERMS.TERMS_ID                AS TERM,
                                                   TERMS.TERM_START_DATE,
                                                   MAJORS.MAJ_DESC               AS MAJOR,
                                                   SAPV.STUDENT_ID,
                                                   ROW_NUMBER() OVER (PARTITION BY STUDENT_ID, MAJORS.MAJ_DESC
                                                       ORDER BY TERM_START_DATE) AS TERM_RANK
                                   FROM MAJORS
                                            CROSS JOIN TERMS
                                            CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        ------------------------------------------------------------------------------------------------------------------------
                                            LEFT JOIN STPR_MAJOR_LIST_VIEW AS SMLV
                                                      ON SAPV.STUDENT_ID = SMLV.STPR_STUDENT AND
                                                         SAPV.STP_ACADEMIC_PROGRAM = SMLV.STPR_ACAD_PROGRAM
                                            LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                            LEFT JOIN MAJORS AS ADDNL_MAJOR ON SMLV.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
        -----------------------------------------------------------------------------------------------------------------------
                                   WHERE TERMS.TERM_START_DATE >= DATEADD(YEAR, -10, '2019-08-01')
                                     AND TERMS.TERM_END_DATE < '2025-06-01'
                                     AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS_ID LIKE '%SP')
        ------------------------------------------------------------------------------------------------------------------------
                                     AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
        ------------------------------------------------------------------------------------------------------------------------
                                     AND (
                                       (
                                           MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                                               AND SAPV.STP_START_DATE <= TERMS.TERM_END_DATE
                                               AND (SAPV.STP_END_DATE >= TERMS.TERM_START_DATE OR SAPV.STP_END_DATE IS NULL)
                                           )
                                           OR (
                                           MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                               AND SMLV.STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                               AND
                                           (SMLV.STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                            SMLV.STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                           )
                                       )
        ------------------------------------------------------------------------------------------------------------------------
                                     AND MAJORS.MAJ_DESC = 'Master of Social Work'
        --(End 1)------------------------------------------------------------------------------------------------------------
                               ) AS X
                          WHERE TERM_RANK = 1
                            AND TERM_START_DATE >= '2019-08-01'
        --(End 2)------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 4)------------------------------------------------------------------------------------------------------------
        WITH X AS (
        --(Begin 3)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        COUNT(*) AS MSW_STUDENT_COUNT
                 FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 2)------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY TERM, TERM_START_DATE
        --(End 3)------------------------------------------------------------------------------------------------------------
             )
            SELECT CONCAT(X.TERM, ' TO ', NEXT_TERM.SECOND) AS TERM_CHANGE,
                   X.MSW_STUDENT_COUNT AS FIRST_COUNT,
                   Y.MSW_STUDENT_COUNT AS NEXT_TERM_COUNT,
                   FORMAT(Y.MSW_STUDENT_COUNT * 1.0 / X.MSW_STUDENT_COUNT - 1, 'P') AS PERCENT_CHANGE
            FROM X LEFT JOIN (VALUES ('2019FA', '2020FA'),
                                 ('2020FA', '2021FA'),
                                 ('2021FA', '2022FA'),
                                 ('2022FA', '2023FA'),
                                 ('2023FA', '2024FA')
            ) AS NEXT_TERM(FIRST, SECOND) ON X.TERM = NEXT_TERM.FIRST
            JOIN X AS Y ON NEXT_TERM.SECOND = Y.TERM
        --(End 4)------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Percent Change Year to Year"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getStaffDemographics(self):
        query = f"""
        --(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT
                PERSTAT.PERSTAT_HRP_ID,
                PERSON.LAST_NAME,
                PERSON.FIRST_NAME,
                COALESCE(PERSON.GENDER, 'Unknown') AS GENDER,
                RACE.IPEDS_RACE_ETHNIC_DESC AS RACE
         FROM TERMS
             CROSS JOIN PERSTAT
              JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
              JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
              JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND (POSITION.POS_CLASS != 'FAC' OR POSITION.POS_CLASS IS NULL)
           AND (POSITION.POS_RANK != 'A' OR POSITION.POS_RANK IS NULL)
           AND (POSITION.POS_EEO_RANK != 'INS' OR POSITION.POS_EEO_RANK IS NULL)
          AND PERSTAT.PERSTAT_STATUS != 'STU'
        --(End 1)--------------------------------------------------------------------------------------------------------------
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Staff Demographics"
        self.save_query_results(query, snapshot_term="2025SP", func_dict=None)(report, name)

    def getStaffLoad(self):
        query = f"""
        --(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT TERMS.TERMS_ID AS TERM,
                PERSTAT.PERSTAT_HRP_ID,
                PERSON.LAST_NAME,
                PERSON.FIRST_NAME,
                CASE WHEN PERSTAT.PERSTAT_STATUS = 'FT' THEN 'FT' ELSE 'PT' END AS STATUS
         FROM TERMS
             CROSS JOIN PERSTAT
              JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
              JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND (POSITION.POS_CLASS != 'FAC' OR POSITION.POS_CLASS IS NULL)
           AND (POSITION.POS_RANK != 'A' OR POSITION.POS_RANK IS NULL)
           AND (POSITION.POS_EEO_RANK != 'INS' OR POSITION.POS_EEO_RANK IS NULL)
            AND PERSTAT.PERSTAT_STATUS != 'STU'
        --(End 1)--------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE, LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Staff Load"
        self.save_query_results(query, snapshot_term="2025SP", func_dict=None)(report, name)

    def getTotalStaff(self):
        query = f"""
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                 SELECT TERMS.TERMS_ID AS TERM,
                        TERM_START_DATE,
                        PERSTAT.PERSTAT_HRP_ID,
                        PERSON.LAST_NAME,
                        PERSON.FIRST_NAME
                 FROM TERMS
                     CROSS JOIN PERSTAT
                      JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                      JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                 WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                    AND TERMS.TERM_END_DATE < '2025-06-01'
                    AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                    AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
                    AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
                   AND (POSITION.POS_CLASS != 'FAC' OR POSITION.POS_CLASS IS NULL)
                   AND (POSITION.POS_RANK != 'A' OR POSITION.POS_RANK IS NULL)
                   AND (POSITION.POS_EEO_RANK != 'INS' OR POSITION.POS_EEO_RANK IS NULL)
                  AND PERSTAT.PERSTAT_STATUS != 'STU'
        --(End 1)--------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS TOTAL_ADMIN_STAFF
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        {query}
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Total Staff"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getAdjunctsAndCourseLoad(self):
        query = f"""
                 SELECT DISTINCT TERMS.TERMS_ID         AS TERM,
                PERSTAT.PERSTAT_HRP_ID AS ID,
                PERSON.LAST_NAME,
                PERSON.FIRST_NAME,
                CS.COURSE_SECTIONS_ID,
                CS_BILLING_CREDITS AS CREDITS
         FROM TERMS
                  CROSS JOIN PERSTAT
                  JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                  JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                  JOIN FACULTY_SECTIONS_DETAILS_VIEW AS FS
                       ON PERSTAT.PERSTAT_HRP_ID = FS.FACULTY_ID AND TERMS.TERMS_ID = FS.CS_TERM
                  JOIN COURSE_SECTIONS_DETAILS_VIEW AS CS
                        ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
           AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND POSITION.POS_RANK = 'A'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               ID,
               LAST_NAME,
               FIRST_NAME,
               SUM(CREDITS) AS ADJUNCT_CREDIT_LOAD
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, ID, LAST_NAME, FIRST_NAME
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY TERM, LAST_NAME, FIRST_NAME
        """
        names = lambda query: f"""
        {query}
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Adjuncts and Course Load"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getAverageCreditLoad(self):
        query = f"""
                  SELECT DISTINCT TERMS.TERMS_ID                           AS TERM,
                          PERSTAT.PERSTAT_HRP_ID                   AS ID,
                          PERSON.LAST_NAME,
                          PERSON.FIRST_NAME,
                          CS.COURSE_SECTIONS_ID,
                          CS_BILLING_CREDITS AS CREDITS
          FROM TERMS
                   CROSS JOIN PERSTAT
                   JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                   JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                   JOIN FACULTY_SECTIONS_DETAILS_VIEW AS FS
                        ON PERSTAT.PERSTAT_HRP_ID = FS.FACULTY_ID AND TERMS.TERMS_ID = FS.CS_TERM
                   JOIN COURSE_SECTIONS_DETAILS_VIEW AS CS
                        ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
            AND POSITION.POS_CLASS = 'FAC'
          AND POSITION.POS_DEPT = 'SWK'
        """
        agg = lambda query: f"""
        --(Begin 3)------------------------------------------------------------------------------------------------------------
        SELECT ID,
               LAST_NAME,
               FIRST_NAME,
               AVG(FACULTY_CREDIT_LOAD) AS AVG_CREDIT_LOAD
        FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        ID,
                        LAST_NAME,
                        FIRST_NAME,
                        SUM(CREDITS) AS FACULTY_CREDIT_LOAD
                 FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT TERMS.TERMS_ID                           AS TERM,
                                          PERSTAT.PERSTAT_HRP_ID                   AS ID,
                                          PERSON.LAST_NAME,
                                          PERSON.FIRST_NAME,
                                          CS.COURSE_SECTIONS_ID,
                                          CS_BILLING_CREDITS AS CREDITS
                          FROM TERMS
                                   CROSS JOIN PERSTAT
                                   JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                                   JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                                   JOIN FACULTY_SECTIONS_DETAILS_VIEW AS FS
                                        ON PERSTAT.PERSTAT_HRP_ID = FS.FACULTY_ID AND TERMS.TERMS_ID = FS.CS_TERM
                                   JOIN COURSE_SECTIONS_DETAILS_VIEW AS CS
                                        ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
                          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                            AND TERMS.TERM_END_DATE < '2025-06-01'
                            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
                            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
                            AND POSITION.POS_CLASS = 'FAC'
                          AND POSITION.POS_DEPT = 'SWK'
        --(End 1)--------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY TERM, ID, LAST_NAME, FIRST_NAME
        --(End 2)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY ID, LAST_NAME, FIRST_NAME
        --(End 3)--------------------------------------------------------------------------------------------------------------
        ORDER BY LAST_NAME, FIRST_NAME
        """
        names = lambda query: f"""
        {query}
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Average Credit Load"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getAverageEnrollmentSize(self):
        query = f"""
                  SELECT DISTINCT TERMS.TERMS_ID                           AS TERM,
                          PERSTAT.PERSTAT_HRP_ID                   AS ID,
                          PERSON.LAST_NAME,
                          PERSON.FIRST_NAME,
                          CS.COURSE_SECTIONS_ID,
                          CS.CS_COUNT_ACTIVE_STUDENTS AS ENROLLMENT
          FROM TERMS
                   CROSS JOIN PERSTAT
                   JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                   JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                   JOIN FACULTY_SECTIONS_DETAILS_VIEW AS FS
                        ON PERSTAT.PERSTAT_HRP_ID = FS.FACULTY_ID AND TERMS.TERMS_ID = FS.CS_TERM
                   JOIN COURSE_SECTIONS_DETAILS_VIEW AS CS
                        ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
            AND POSITION.POS_CLASS = 'FAC'
            AND POSITION.POS_DEPT = 'SWK'
        """
        agg = lambda query: f"""
        --(Begin 3)------------------------------------------------------------------------------------------------------------
        SELECT ID,
               LAST_NAME,
               FIRST_NAME,
               AVG(FACULTY_ENROLLMENT) AS AVG_FACULTY_ENROLLMENT
        FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        ID,
                        LAST_NAME,
                        FIRST_NAME,
                        SUM(ENROLLMENT) AS FACULTY_ENROLLMENT
                 FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY TERM, ID, LAST_NAME, FIRST_NAME
        --(End 2)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY ID, LAST_NAME, FIRST_NAME
        --(End 3)--------------------------------------------------------------------------------------------------------------
        ORDER BY LAST_NAME, FIRST_NAME
        """
        names = lambda query: f"""
        {query}
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Average Enrollment Size"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getFacultyDemographics(self):
        query = f"""
        --(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT
                PERSTAT.PERSTAT_HRP_ID,
                PERSON.LAST_NAME,
                PERSON.FIRST_NAME,
                COALESCE(PERSON.GENDER, 'Unknown') AS GENDER,
                RACE.IPEDS_RACE_ETHNIC_DESC AS RACE
         FROM TERMS
          CROSS JOIN PERSTAT
          JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
          JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
          JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
          LEFT JOIN (VALUES
            ('T', 'Tenured'), ('O', 'On Tenure Track'), ('N', 'Not Tenure Track'))
            AS TENURE_STATUS(ID, NAME) ON PERSTAT_TENURE_TYPE = TENURE_STATUS.ID
          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND POSITION.POS_CLASS = 'FAC'
        --(End 1)--------------------------------------------------------------------------------------------------------------
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Faculty Demographics"
        self.save_query_results(query, snapshot_term="2025SP", func_dict=None)(report, name)

    def getTenureStatus(self):
        query = f"""
        --(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT TERMS.TERMS_ID AS TERM,
                PERSTAT.PERSTAT_HRP_ID,
                PERSON.LAST_NAME,
                PERSON.FIRST_NAME,
                COALESCE(TENURE_STATUS.NAME, 'Unknown') AS TENURE_STATUS
         FROM TERMS
          CROSS JOIN PERSTAT
          JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
          JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
          LEFT JOIN (VALUES
            ('T', 'Tenured'), ('O', 'On Tenure Track'), ('N', 'Not Tenure Track'))
            AS TENURE_STATUS(ID, NAME) ON PERSTAT_TENURE_TYPE = TENURE_STATUS.ID
          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND POSITION.POS_CLASS = 'FAC'
        --(End 1)--------------------------------------------------------------------------------------------------------------
        ORDER BY TERM, LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Tenure Status"
        self.save_query_results(query, snapshot_term="2025SP", func_dict=None)(report, name)

    def getTotalFilledFacultyPositions(self):
        query = f"""
                 SELECT TERMS.TERMS_ID AS TERM,
                TERM_START_DATE,
                PERSTAT.PERSTAT_HRP_ID,
                PERSON.LAST_NAME,
                PERSON.FIRST_NAME
         FROM TERMS
             CROSS JOIN PERSTAT
              JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
              JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND POSITION.POS_CLASS = 'FAC'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS TOTAL_FACULTY
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        {query}
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Total Filled Faculty Positions"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getMSWGraduationRate(self):
        query = f"""
                  SELECT MAJORS.MAJ_DESC           AS MAJOR,
                 SAPV.STUDENT_ID,
                 SAPV.STUDENT_FIRST_NAME,
                 SAPV.STUDENT_LAST_NAME,
                 STP_CURRENT_STATUS        AS STATUS,
                 MAIN_MAJOR.MAJ_DESC       AS MAIN,
                 STP_END_DATE              AS MAIN_END,
                 STPR_ADDNL_MAJOR_END_DATE AS ADDNL_END,
                 AC.ACAD_END_DATE
          FROM MAJORS
                   CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                   LEFT JOIN ACAD_CREDENTIALS AS AC
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
        """
        agg = lambda query: f"""
        --(Begin C4)------------------------------------------------------------------------------------------------------------
        SELECT MAJOR,
               FORMAT(COMPLETION_RATE, 'P') AS COMPLETION_RATE,
               STUDENT_COUNT
        FROM (
        --(Begin C3)------------------------------------------------------------------------------------------------------------
                 SELECT MAJOR,
                        AVG(MAJOR_COMPLETED * 1.0)    AS COMPLETION_RATE,
                        COUNT(*)                      AS STUDENT_COUNT
                 FROM (
        --(Begin C2)------------------------------------------------------------------------------------------------------------
                          SELECT MAJOR,
                                 STUDENT_ID,
                                 MAJOR_COMPLETED
                          FROM (
        --(Begin C1)------------------------------------------------------------------------------------------------------------
                                   SELECT X.MAJOR,
                                          X.STUDENT_ID,
                                          MAX(COMPLETE)           AS MAJOR_COMPLETED,
                                          ACAD_END_DATE
                                   FROM (
        --(Begin A3)------------------------------------------------------------------------------------------------------------
                                            SELECT MAJOR,
                                                   STUDENT_ID,
                                                   CASE
                                                       WHEN (MAJOR_END >= ACAD_END_DATE OR MAJOR_END IS NULL)
                                                           AND STATUS = 'Graduated' THEN 1
                                                       ELSE 0 END AS COMPLETE,
                                                   ACAD_END_DATE
                                            FROM (
        --(Begin A2)------------------------------------------------------------------------------------------------------------
                                                     SELECT MAJOR,
                                                            STUDENT_ID,
                                                            STATUS,
                                                            CASE WHEN MAJOR = MAIN THEN MAIN_END ELSE ADDNL_END END AS MAJOR_END,
                                                            ACAD_END_DATE
                                                     FROM (
        --(Begin A1)------------------------------------------------------------------------------------------------------------
        {query}
        --(End A1)------------------------------------------------------------------------------------------------------------
                                                          ) AS X
        --(End A2)------------------------------------------------------------------------------------------------------------
                                                 ) AS X
        --(End A3)------------------------------------------------------------------------------------------------------------
                                        ) AS X
                                   GROUP BY X.MAJOR, X.STUDENT_ID, ACAD_END_DATE
        --(End C1)------------------------------------------------------------------------------------------------------------
                               ) AS X
        --(End C2)------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY MAJOR
        --(End C3)------------------------------------------------------------------------------------------------------------
             ) AS X
        --(End C4)------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X ORDER BY STUDENT_LAST_NAME
        """
        report = "2025-06-13-MSW Program Review"
        name = "Graduation Rate"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)










    '''
    ID: Unknown
    Name: 2025-06-19-Consumer Reports
    Person: Annette Farley
    Start Date: 2025-06-19
    End Date: 2025-06-19
    Description:
        I needed to get data for consumer reports.
    '''
    def getAthleticAidRecipientsByRaceAndGender(self):
        query = f"""
                 SELECT DISTINCT SA_STUDENT_ID,
                         PERSON.GENDER,
                         RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
                         CASE
                             WHEN (AW_DESCRIPTION LIKE '%Basketball%' OR
                                   AW_DESCRIPTION LIKE '%BB%') THEN 'Basketball'
                             WHEN AW_DESCRIPTION LIKE '%Cross Country%' THEN 'Cross Country'
                             WHEN AW_DESCRIPTION LIKE '%Football%' THEN 'Football'
                             WHEN AW_DESCRIPTION LIKE '%Golf%' THEN 'Golf'
                             WHEN AW_DESCRIPTION LIKE '%Soccer%' THEN 'Soccer'
                             WHEN AW_DESCRIPTION LIKE '%Softball%' THEN 'Softball'
                             WHEN AW_DESCRIPTION LIKE '%Track%' THEN 'Track and Field'
                             WHEN AW_DESCRIPTION LIKE '%Volleyball%' THEN 'Volleyball'
                             WHEN AW_DESCRIPTION LIKE '%Cheer%' THEN 'Cheerleading'
                             WHEN AW_DESCRIPTION LIKE '%Dance%' THEN 'Dance'
                             END                     AS SPORT
         FROM F24_AWARD_LIST AS AL
                  JOIN AWARDS ON AL.SA_AWARD = AWARDS.AW_ID
                  JOIN AWARD_CATEGORIES AS AC ON AWARDS.AW_CATEGORY = AC.AC_ID
                  JOIN PERSON ON AL.SA_STUDENT_ID = PERSON.ID
                  LEFT JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
         WHERE SA_ACTION = 'A'
           AND AC_DESCRIPTION = 'Athletic Grants'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT GENDER,
               RACE,
               [Basketball],
               [Cross Country],
               [Football],
               [Golf],
               [Soccer],
               [Softball],
               [Track and Field],
               [Volleyball],
               [Cheerleading],
               [Dance],
               --------
               ([Basketball] +
               [Cross Country] +
               [Football] +
               [Golf] +
               [Soccer] +
               [Softball] +
               [Track and Field] +
               [Volleyball] +
               [Cheerleading] +
               [Dance]) AS GRAND_TOTAL
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(SA_STUDENT_ID) FOR SPORT IN (
               [Basketball],
               [Cross Country],
               [Football],
               [Golf],
               [Soccer],
               [Softball],
               [Track and Field],
               [Volleyball],
               [Cheerleading],
               [Dance]
                )) AS X
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY GENDER, RACE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.SA_STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Athletic Aid Recipients By Race and Gender"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRateOfAthleticAidRecipientsByRaceAndGender(self):
        query = f"""
        --(Begin C1)------------------------------------------------------------------------------------------------------------
                     SELECT DISTINCT AW_TERM                     AS COHORT,
                                     SA_STUDENT_ID               AS ID,
                                     CASE
                                         WHEN PERSON.GENDER = 'F' THEN 'Female'
                                         WHEN GENDER = 'M'
                                             THEN 'Male' END     AS GENDER,
                                     RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
                                     CASE
                                         WHEN (AW_DESCRIPTION LIKE '%Basketball%' OR
                                               AW_DESCRIPTION LIKE '%BB%') THEN 'Basketball'
                                         WHEN AW_DESCRIPTION LIKE '%Cross Country%' THEN 'Cross Country'
                                         WHEN AW_DESCRIPTION LIKE '%Football%' THEN 'Football'
                                         WHEN AW_DESCRIPTION LIKE '%Golf%' THEN 'Golf'
                                         WHEN AW_DESCRIPTION LIKE '%Soccer%' THEN 'Soccer'
                                         WHEN AW_DESCRIPTION LIKE '%Softball%' THEN 'Softball'
                                         WHEN AW_DESCRIPTION LIKE '%Track%' THEN 'Track and Field'
                                         WHEN AW_DESCRIPTION LIKE '%Volleyball%' THEN 'Volleyball'
                                         WHEN AW_DESCRIPTION LIKE '%Cheer%' THEN 'Cheerleading'
                                         WHEN AW_DESCRIPTION LIKE '%Dance%' THEN 'Dance'
                                         END                     AS SPORT,
                                     CASE
                                         WHEN EXISTS (SELECT 1
                                                      FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                      WHERE STUDENT_ID = SA_STUDENT_ID
                                                        AND STP_CURRENT_STATUS = 'Graduated'
                                                        AND STP_END_DATE >= FM.TERM_START_DATE
                                                        AND STP_END_DATE < DATEADD(YEAR, 6, FM.TERM_START_DATE))
                                             THEN 1
                                         ELSE 0 END              AS SIX_YEAR_GRADUATED
                     FROM (
        --(Begin A2)--------------------------------------------------------------------------------
                              SELECT AW_TERM, SA_AWARD, SA_STUDENT_ID, AW_DESCRIPTION
                              FROM (
        --(Begin A1)--------------------------------------------------------------------------------
                                       SELECT '2015FA' AS AW_TERM, *
                                       FROM F15_AWARD_LIST
                                       UNION
                                       SELECT '2016FA' AS AW_TERM, *
                                       FROM F16_AWARD_LIST
                                       UNION
                                       SELECT '2017FA' AS AW_TERM, *
                                       FROM F17_AWARD_LIST
                                       UNION
                                       SELECT '2018FA' AS AW_TERM, *
                                       FROM F18_AWARD_LIST
        --(End A1)---------------------------------------------------------------------------------
                                   ) AS X
                                       JOIN AWARDS ON X.SA_AWARD = AWARDS.AW_ID
                                       JOIN AWARD_CATEGORIES AS AC ON AWARDS.AW_CATEGORY = AC.AC_ID
                              WHERE SA_ACTION = 'A'
                                AND AC_DESCRIPTION = 'Athletic Grants'
        --(End A2)----------------------------------------------------------------------------------
                          ) AS AL
                              JOIN PERSON ON AL.SA_STUDENT_ID = PERSON.ID
                              JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
                              JOIN (
        --(Begin B2)-------------------------------------------------------------------------------
                         SELECT ID, TERM, TERM_START_DATE
                         FROM (
        --(Begin B1)-------------------------------------------------------------------------------
                                  SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                                  APPL_START_TERM                                                          AS TERM,
                                                  TERM_START_DATE,
                                                  ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                                  FROM APPLICATIONS AS AP
                                           JOIN STUDENT_ACAD_CRED AS AC
                                                ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND
                                                   AP.APPL_START_TERM = AC.STC_TERM
                                           JOIN STC_STATUSES AS STAT
                                                ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                           JOIN TERMS ON APPL_START_TERM = TERMS_ID
                                  WHERE APPL_DATE IS NOT NULL
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                                    AND STC_STATUS IN ('A', 'N')
                                    AND STC_CRED_TYPE IN ('INST')
        --(End B1)----------------------------------------------------------------------------------
                              ) AS X
                         WHERE TERM_ORDER = 1
        --(End B2)----------------------------------------------------------------------------------
                     ) AS FM ON PERSON.ID = FM.ID AND AW_TERM = FM.TERM
        --(End C1)-------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin C3)------------------------------------------------------------------------------------------------------------
        SELECT COHORTS.COHORT,
               GENDERS.GENDER,
               RACES.RACE,
               SPORTS.SPORT,
               NON_COMPLETER,
               COMPLETER,
               TOTAL,
               GRADUATION_RATE
        FROM (VALUES ('2015FA'), ('2016FA'), ('2017FA'), ('2018FA')) AS COHORTS(COHORT)
        CROSS JOIN
            (VALUES ('Female'), ('Male')) AS GENDERS(GENDER)
        CROSS JOIN
            (VALUES ('White'),
                    ('Unknown'),
                    ('Two or More Races'),
                    ('Non-Resident Alien'),
                    ('Hispanic/Latino'),
                    ('Black or African American'),
                    ('Asian')) AS RACES(RACE)
        CROSS JOIN
            (VALUES ('Basketball'),
                    ('Cross Country'),
                    ('Football'),
                    ('Golf'),
                    ('Soccer'),
                    ('Softball'),
                    ('Track and Field'),
                    ('Volleyball')) AS SPORTS(SPORT)
        LEFT JOIN (
        --(Begin C2)------------------------------------------------------------------------------------------------------------
            SELECT COHORT,
                   GENDER,
                   RACE,
                   SPORT,
                   SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NON_COMPLETER,
                   SUM(SIX_YEAR_GRADUATED)                                 AS COMPLETER,
                   COUNT(*)                                                AS TOTAL,
                   AVG(1.0 * SIX_YEAR_GRADUATED)                           AS GRADUATION_RATE
            FROM (
        --(Begin C1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End C1)-------------------------------------------------------------------------------------------------------------
                 ) AS X
            GROUP BY COHORT, GENDER, RACE, SPORT
        --(End C2)-------------------------------------------------------------------------------------------------------------
        ) AS X
        ON COHORTS.COHORT = X.COHORT
        AND GENDERS.GENDER = X.GENDER
        AND RACES.RACE = X.RACE
        AND SPORTS.SPORT = X.SPORT
        --(End C2)-------------------------------------------------------------------------------------------------------------
        ORDER BY SPORT, COHORT, GENDER, RACE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Graduation Rate of Athletic Aid Recipients by Race and Gender"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRateOfAthleticAidRecipientsByRaceAndGender_Basketball(self):
        query = f"""
        --(Begin C1)------------------------------------------------------------------------------------------------------------
                     SELECT DISTINCT AW_TERM                     AS COHORT,
                                     SA_STUDENT_ID               AS ID,
                                     CASE
                                         WHEN PERSON.GENDER = 'F' THEN 'Female'
                                         WHEN GENDER = 'M'
                                             THEN 'Male' END     AS GENDER,
                                     RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
                                     CASE
                                         WHEN (AW_DESCRIPTION LIKE '%Basketball%' OR
                                               AW_DESCRIPTION LIKE '%BB%') THEN 'Basketball'
                                         WHEN AW_DESCRIPTION LIKE '%Cross Country%' THEN 'Cross Country'
                                         WHEN AW_DESCRIPTION LIKE '%Football%' THEN 'Football'
                                         WHEN AW_DESCRIPTION LIKE '%Golf%' THEN 'Golf'
                                         WHEN AW_DESCRIPTION LIKE '%Soccer%' THEN 'Soccer'
                                         WHEN AW_DESCRIPTION LIKE '%Softball%' THEN 'Softball'
                                         WHEN AW_DESCRIPTION LIKE '%Track%' THEN 'Track and Field'
                                         WHEN AW_DESCRIPTION LIKE '%Volleyball%' THEN 'Volleyball'
                                         WHEN AW_DESCRIPTION LIKE '%Cheer%' THEN 'Cheerleading'
                                         WHEN AW_DESCRIPTION LIKE '%Dance%' THEN 'Dance'
                                         END                     AS SPORT,
                                     CASE
                                         WHEN EXISTS (SELECT 1
                                                      FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                      WHERE STUDENT_ID = SA_STUDENT_ID
                                                        AND STP_CURRENT_STATUS = 'Graduated'
                                                        AND STP_END_DATE >= FM.TERM_START_DATE
                                                        AND STP_END_DATE < DATEADD(YEAR, 6, FM.TERM_START_DATE))
                                             THEN 1
                                         ELSE 0 END              AS SIX_YEAR_GRADUATED
                     FROM (
        --(Begin A2)--------------------------------------------------------------------------------
                              SELECT AW_TERM, SA_AWARD, SA_STUDENT_ID, AW_DESCRIPTION
                              FROM (
        --(Begin A1)--------------------------------------------------------------------------------
                                       SELECT '2015FA' AS AW_TERM, *
                                       FROM F15_AWARD_LIST
                                       UNION
                                       SELECT '2016FA' AS AW_TERM, *
                                       FROM F16_AWARD_LIST
                                       UNION
                                       SELECT '2017FA' AS AW_TERM, *
                                       FROM F17_AWARD_LIST
                                       UNION
                                       SELECT '2018FA' AS AW_TERM, *
                                       FROM F18_AWARD_LIST
        --(End A1)---------------------------------------------------------------------------------
                                   ) AS X
                                       JOIN AWARDS ON X.SA_AWARD = AWARDS.AW_ID
                                       JOIN AWARD_CATEGORIES AS AC ON AWARDS.AW_CATEGORY = AC.AC_ID
                              WHERE SA_ACTION = 'A'
                                AND AC_DESCRIPTION = 'Athletic Grants'
        --(End A2)----------------------------------------------------------------------------------
                          ) AS AL
                              JOIN PERSON ON AL.SA_STUDENT_ID = PERSON.ID
                              JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
                              JOIN (
        --(Begin B2)-------------------------------------------------------------------------------
                         SELECT ID, TERM, TERM_START_DATE
                         FROM (
        --(Begin B1)-------------------------------------------------------------------------------
                                  SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                                  APPL_START_TERM                                                          AS TERM,
                                                  TERM_START_DATE,
                                                  ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                                  FROM APPLICATIONS AS AP
                                           JOIN STUDENT_ACAD_CRED AS AC
                                                ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND
                                                   AP.APPL_START_TERM = AC.STC_TERM
                                           JOIN STC_STATUSES AS STAT
                                                ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                           JOIN TERMS ON APPL_START_TERM = TERMS_ID
                                  WHERE APPL_DATE IS NOT NULL
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                                    AND STC_STATUS IN ('A', 'N')
                                    AND STC_CRED_TYPE IN ('INST')
        --(End B1)----------------------------------------------------------------------------------
                              ) AS X
                         WHERE TERM_ORDER = 1
        --(End B2)----------------------------------------------------------------------------------
                     ) AS FM ON PERSON.ID = FM.ID AND AW_TERM = FM.TERM
        --(End C1)-------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin C3)------------------------------------------------------------------------------------------------------------
        SELECT COHORTS.COHORT,
               GENDERS.GENDER,
               RACES.RACE,
               NON_COMPLETER,
               COMPLETER,
               TOTAL,
               GRADUATION_RATE
        FROM (VALUES ('2015FA'), ('2016FA'), ('2017FA'), ('2018FA')) AS COHORTS(COHORT)
        CROSS JOIN
            (VALUES ('Female'), ('Male')) AS GENDERS(GENDER)
        CROSS JOIN
            (VALUES ('White'),
                    ('Unknown'),
                    ('Two or More Races'),
                    ('Non-Resident Alien'),
                    ('Hispanic/Latino'),
                    ('Black or African American'),
                    ('Asian')) AS RACES(RACE)
        CROSS JOIN
            (VALUES ('Basketball')
                    ) AS SPORTS(SPORT)
        LEFT JOIN (
        --(Begin C2)------------------------------------------------------------------------------------------------------------
            SELECT COHORT,
                   GENDER,
                   RACE,
                   SPORT,
                   SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NON_COMPLETER,
                   SUM(SIX_YEAR_GRADUATED)                                 AS COMPLETER,
                   COUNT(*)                                                AS TOTAL,
                   AVG(1.0 * SIX_YEAR_GRADUATED)                           AS GRADUATION_RATE
            FROM (
        --(Begin C1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End C1)-------------------------------------------------------------------------------------------------------------
                 ) AS X
            GROUP BY COHORT, GENDER, RACE, SPORT
        --(End C2)-------------------------------------------------------------------------------------------------------------
        ) AS X
        ON COHORTS.COHORT = X.COHORT
        AND GENDERS.GENDER = X.GENDER
        AND RACES.RACE = X.RACE
        AND SPORTS.SPORT = X.SPORT
        --(End C2)-------------------------------------------------------------------------------------------------------------
        ORDER BY COHORT, GENDER, RACE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Graduation Rate of Athletic Aid Recipients by Race and Gender (Basketball)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRateOfFederalAidRecipientsByIncomingMajor(self):
        query = f"""
        --(Begin C1)------------------------------------------------------------------------------------------------------------
                                   SELECT AW_TERM,
                                          SA_STUDENT_ID                                               AS ID,
                                          TERM_START_DATE,
                                          STP_PROGRAM_TITLE                                           AS PROGRAM,
                                          ROW_NUMBER() OVER (PARTITION BY ID ORDER BY STP_START_DATE) AS PROGRAM_ORDER
                                   FROM (
        --(Begin A2)--------------------------------------------------------------------------------
                                            SELECT AW_TERM, SA_AWARD, SA_STUDENT_ID, AW_DESCRIPTION
                                            FROM (
        --(Begin A1)--------------------------------------------------------------------------------
                                                     SELECT '2018FA' AS AW_TERM, *
                                                     FROM F18_AWARD_LIST
        --(End A1)----------------------------------------------------------------------------------
                                                 ) AS X
                                                     JOIN AWARDS ON X.SA_AWARD = AWARDS.AW_ID
                                            WHERE SA_ACTION = 'A'
                                              AND AW_TYPE = 'F'
        --(End A2)----------------------------------------------------------------------------------
                                        ) AS AL
                                            JOIN (
        --(Begin B2)--------------------------------------------------------------------------------
                                       SELECT ID, TERM, TERM_START_DATE, TERM_END_DATE
                                       FROM (
        --(Begin B1)-------------------------------------------------------------------------------
                                                SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                                                APPL_START_TERM                                                          AS TERM,
                                                                TERM_START_DATE,
                                                                TERM_END_DATE,
                                                                ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                                                FROM APPLICATIONS AS AP
                                                         JOIN STUDENT_ACAD_CRED AS AC
                                                              ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND
                                                                 AP.APPL_START_TERM = AC.STC_TERM
                                                         JOIN STC_STATUSES AS STAT
                                                              ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                                         JOIN TERMS ON APPL_START_TERM = TERMS_ID
                                                         JOIN ACAD_PROGRAMS AS PROG ON AP.APPL_ACAD_PROGRAM = PROG.ACAD_PROGRAMS_ID
                                                WHERE APPL_DATE IS NOT NULL
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                                                  AND STC_STATUS IN ('A', 'N')
                                                  AND STC_CRED_TYPE IN ('INST')
        --(End B1)---------------------------------------------------------------------------------
                                            ) AS X
                                       WHERE TERM_ORDER = 1
        --(End B2)----------------------------------------------------------------------------------
                                   ) AS FM ON SA_STUDENT_ID = FM.ID AND AW_TERM = FM.TERM
                                            JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV ON FM.ID = SAPV.STUDENT_ID
                                   WHERE SAPV.STP_START_DATE <= FM.TERM_END_DATE
                                     AND SAPV.STP_START_DATE >= FM.TERM_START_DATE
        --(End C1)--------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin C4)------------------------------------------------------------------------------------------------------------
        SELECT INCOMING_FIRST_MAJOR,
               CASE WHEN COMPLETER < 5 THEN '<5' ELSE CAST(COMPLETER AS VARCHAR) END AS COMPLETER,
               CASE WHEN NON_COMPLETER < 5 THEN '<5' ELSE CAST(NON_COMPLETER AS VARCHAR) END AS NON_COMPLETER,
               CASE WHEN GRAND_TOTAL < 5 THEN '<5' ELSE CAST(GRAND_TOTAL AS VARCHAR) END AS GRAND_TOTAL,
               GRADUATION_RATES
        FROM (
        --(Begin C3)------------------------------------------------------------------------------------------------------------
                 SELECT PROGRAM                                                 AS INCOMING_FIRST_MAJOR,
                        SUM(SIX_YEAR_GRADUATED)                                 AS COMPLETER,
                        SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NON_COMPLETER,
                        COUNT(*)                                                AS GRAND_TOTAL,
                        FORMAT(AVG(1.0 * SIX_YEAR_GRADUATED), 'P')              AS GRADUATION_RATES
                 FROM (
        --(Begin C2)------------------------------------------------------------------------------------------------------------
                          SELECT AW_TERM,
                                 ID,
                                 PROGRAM,
                                 CASE
                                     WHEN EXISTS (SELECT 1
                                                  FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                  WHERE STUDENT_ID = ID
                                                    AND STP_CURRENT_STATUS = 'Graduated'
                                                    AND STP_END_DATE >= TERM_START_DATE
                                                    AND STP_END_DATE < DATEADD(YEAR, 6, TERM_START_DATE)) THEN 1
                                     ELSE 0 END AS SIX_YEAR_GRADUATED
                          FROM (
        --(Begin C1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End C1)--------------------------------------------------------------------------------------------------------------
                               ) AS X
                          WHERE PROGRAM_ORDER = 1
        --(End C2)--------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY PROGRAM
        --(End C3)--------------------------------------------------------------------------------------------------------------
             ) AS X
        --(End C4)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Graduation Rate of Federal Aid Recipients by Incoming Major"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRateOfFederalAidRecipientsByPellAndDSL(self):
        query = f"""
        --(Begin C1)------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT AW_TERM,
                         SA_STUDENT_ID  AS ID,
                         FEDERAL_AID,
                         CASE
                             WHEN EXISTS (SELECT 1
                                          FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                          WHERE STUDENT_ID = SA_STUDENT_ID
                                            AND STP_CURRENT_STATUS = 'Graduated'
                                            AND STP_END_DATE >= TERM_START_DATE
                                            AND STP_END_DATE < DATEADD(YEAR, 6, TERM_START_DATE)) THEN 1
                             ELSE 0 END AS SIX_YEAR_GRADUATED
                 FROM (
        --(Begin A4)--------------------------------------------------------------------------------
                          SELECT AW_TERM,
                                 SA_STUDENT_ID,
                                 CASE
                                     WHEN PELL = 1 THEN 'Recipients of a Pell Grant (within entering a year)'
                                     WHEN DSL = 1 THEN 'Recipients of a Direct Subsidized Loan (within entering year) ' +
                                                       'that did not receive a Pell Grant'
                                     ELSE 'Did not receive either a Pell Grant or Direct Subsidized ' +
                                          'Loan (within entering year)' END AS FEDERAL_AID
                          FROM (
        --(Begin A3)--------------------------------------------------------------------------------
                                   SELECT AW_TERM,
                                          SA_STUDENT_ID,
                                          MAX(CASE WHEN AW_DESCRIPTION = 'Federal Pell Grant' THEN 1 ELSE 0 END)              AS PELL,
                                          MAX(CASE
                                                  WHEN AW_DESCRIPTION = 'Stafford Loan Subsidized Direct' THEN 1
                                                  ELSE 0 END)                                                                 AS DSL
                                   FROM (
        --(Begin A2)--------------------------------------------------------------------------------
                                            SELECT AW_TERM, SA_STUDENT_ID, AW_DESCRIPTION
                                            FROM (
        --(Begin A1)--------------------------------------------------------------------------------
                                                     SELECT '2018FA' AS AW_TERM, *
                                                     FROM F18_AWARD_LIST
        --(End A1)----------------------------------------------------------------------------------
                                                 ) AS X
                                                     JOIN AWARDS ON X.SA_AWARD = AWARDS.AW_ID
                                            WHERE SA_ACTION = 'A'
                                              AND AW_TYPE = 'F'
        --(End A2)----------------------------------------------------------------------------------
                                        ) AS X
                                   GROUP BY AW_TERM, SA_STUDENT_ID
        --(End A3)----------------------------------------------------------------------------------
                               ) AS X
        --(End A4)----------------------------------------------------------------------------------
                      ) AS AL
                          JOIN (
        --(Begin B2)--------------------------------------------------------------------------------
                     SELECT ID, TERM, TERM_START_DATE
                     FROM (
        --(Begin B1)-------------------------------------------------------------------------------
                              SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                              APPL_START_TERM                                                          AS TERM,
                                              TERM_START_DATE,
                                              ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                              FROM APPLICATIONS AS AP
                                       JOIN STUDENT_ACAD_CRED AS AC
                                            ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                       JOIN STC_STATUSES AS STAT
                                            ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                       JOIN TERMS ON APPL_START_TERM = TERMS_ID
                              WHERE APPL_DATE IS NOT NULL
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                                AND STC_STATUS IN ('A', 'N')
                                AND STC_CRED_TYPE IN ('INST')
        --(End B1)---------------------------------------------------------------------------------
                          ) AS X
                     WHERE TERM_ORDER = 1
        --(End B2)----------------------------------------------------------------------------------
                 ) AS FM ON AL.SA_STUDENT_ID = FM.ID AND AW_TERM = FM.TERM
        --(End C1)--------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin C2)------------------------------------------------------------------------------------------------------------
        SELECT FEDERAL_AID,
               SUM(SIX_YEAR_GRADUATED) AS COMPLETER,
               SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NON_COMPLETER,
               COUNT(*) AS GRAND_TOTAL,
               FORMAT(AVG(1.0 * SIX_YEAR_GRADUATED), 'P') AS GRADUATION_RATES
        FROM (
        --(Begin C1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End C1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        JOIN (VALUES
                  ('Recipients of a Pell Grant (within entering a year)', 1),
                  ('Recipients of a Direct Subsidized Loan (within entering year) ' +
                                                       'that did not receive a Pell Grant', 2),
                  ('Did not receive either a Pell Grant or Direct Subsidized ' +
                                          'Loan (within entering year)', 3)
                  ) AS AID_ORDER(X, Y) ON X.FEDERAL_AID = X
        GROUP BY FEDERAL_AID, AID_ORDER.Y
        ORDER BY AID_ORDER.Y
        --(End C2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Graduation Rate of Federal Aid Recipients by Pell Status and DSL Status"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRateOfFederalAidRecipientsByRaceAndGender(self):
        query = f"""
        --(Begin C1)------------------------------------------------------------------------------------------------------------
                  SELECT DISTINCT AW_TERM,
                                  SA_STUDENT_ID                                                                 AS ID,
                                  CASE
                                      WHEN PERSON.GENDER = 'F' THEN 'Female'
                                      WHEN GENDER = 'M'
                                          THEN 'Male' END                                                       AS GENDER,
                                  RACE.IPEDS_RACE_ETHNIC_DESC                                                   AS RACE,
                                  CASE
                                      WHEN EXISTS (SELECT 1
                                                   FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                   WHERE STUDENT_ID = SA_STUDENT_ID
                                                     AND STP_CURRENT_STATUS = 'Graduated'
                                                     AND STP_END_DATE >= TERM_START_DATE
                                                     AND STP_END_DATE < DATEADD(YEAR, 6, TERM_START_DATE)) THEN 1
                                      ELSE 0 END                                                                AS SIX_YEAR_GRADUATED
                  FROM (
        --(Begin A2)--------------------------------------------------------------------------------
                                   SELECT AW_TERM, SA_AWARD, SA_STUDENT_ID, AW_DESCRIPTION
                                   FROM (
        --(Begin A1)--------------------------------------------------------------------------------
                                            SELECT '2018FA' AS AW_TERM, *
                                            FROM F18_AWARD_LIST
        --(End A1)----------------------------------------------------------------------------------
                                        ) AS X
                                            JOIN AWARDS ON X.SA_AWARD = AWARDS.AW_ID
                                   WHERE SA_ACTION = 'A'
                                     AND AW_TYPE = 'F'
        --(End A2)----------------------------------------------------------------------------------
                               ) AS AL
                                   JOIN PERSON ON AL.SA_STUDENT_ID = PERSON.ID
                                   JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
                                   JOIN (
        --(Begin B2)--------------------------------------------------------------------------------
                              SELECT ID, TERM, TERM_START_DATE
                              FROM (
        --(Begin B1)-------------------------------------------------------------------------------
                                       SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                                       APPL_START_TERM                                                          AS TERM,
                                                       TERM_START_DATE,
                                                       ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                                       FROM APPLICATIONS AS AP
                                                JOIN STUDENT_ACAD_CRED AS AC
                                                     ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND
                                                        AP.APPL_START_TERM = AC.STC_TERM
                                                JOIN STC_STATUSES AS STAT
                                                     ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                                JOIN TERMS ON APPL_START_TERM = TERMS_ID
                                       WHERE APPL_DATE IS NOT NULL
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                                         AND STC_STATUS IN ('A', 'N')
                                         AND STC_CRED_TYPE IN ('INST')
        --(End B1)---------------------------------------------------------------------------------
                                   ) AS X
                              WHERE TERM_ORDER = 1
        --(End B2)----------------------------------------------------------------------------------
                          ) AS FM ON PERSON.ID = FM.ID AND AW_TERM = FM.TERM
        --(End C1)--------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin C3)------------------------------------------------------------------------------------------------------------
        SELECT GENDER,
               RACE,
               CASE WHEN COMPLETER < 5 THEN '<5' ELSE CAST(COMPLETER AS VARCHAR) END AS COMPLETER,
               CASE WHEN NON_COMPLETER < 5 THEN '<5' ELSE CAST(NON_COMPLETER AS VARCHAR) END AS NON_COMPLETER,
               CASE WHEN GRAND_TOTAL < 5 THEN '<5' ELSE CAST(GRAND_TOTAL AS VARCHAR) END AS GRAND_TOTAL,
               GRADUATION_RATES
        FROM (
        --(Begin C2)------------------------------------------------------------------------------------------------------------
                 SELECT GENDER,
                        RACE,
                        SUM(SIX_YEAR_GRADUATED)                                 AS COMPLETER,
                        SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NON_COMPLETER,
                        COUNT(*)                                                AS GRAND_TOTAL,
                        FORMAT(AVG(1.0 * SIX_YEAR_GRADUATED), 'P')              AS GRADUATION_RATES
                 FROM (
        --(Begin C1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End C1)--------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY GENDER, RACE
        --(End C2)--------------------------------------------------------------------------------------------------------------
             ) AS X
        --(End C3)--------------------------------------------------------------------------------------------------------------
        ORDER BY GENDER, RACE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Graduation Rate of Federal Aid Recipients by Race and Gender"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getOverallRetentionRate_2021FA_TO_2024FA(self):
        query = f"""
                 SELECT COHORT.ID,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ENROLLMENT_VIEW AS SEV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                   AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                                   AND ENROLL_TERM = '2024FA') THEN 1
                    ELSE 0 END AS RETURNED
         FROM (
---------------------------------------------------COHORT---------------------------------------------------------------
                  SELECT ID,
                         TERM
                  FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                        APPL_START_TERM                                                          AS TERM,
                                        TERM_START_DATE,
                                        ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                        FROM APPLICATIONS AS AP
                                 JOIN STUDENT_ACAD_CRED AS AC
                                      ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                 JOIN STC_STATUSES AS STAT
                                      ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                 JOIN TERMS ON APPL_START_TERM = TERMS_ID
                        WHERE APPL_DATE IS NOT NULL
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                          AND STC_STATUS IN ('A', 'N')
                          AND STC_CRED_TYPE IN ('INST')
                          ----------FFUG------------------
                        AND APPL_STUDENT_TYPE = 'UG'
                        AND APPL_STUDENT_LOAD_INTENT = 'F'
                        AND APPL_ADMIT_STATUS = 'FY'
                 ) AS X
                  WHERE TERM_ORDER = 1
------------------------------------------------------------------------------------------------------------------------
              ) AS COHORT
------------------------------------------------------------------------------------------------------------------------
         WHERE TERM = '2021FA'
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT FORMAT(AVG(1.0 * RETURNED), 'P') AS RATE
        FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        --(End 2)---------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Overall Retention Rate (2021FA to 2024FA)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getOverallRetentionRate_2022FA_TO_2024FA(self):
        query = f"""
         SELECT COHORT.ID,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ENROLLMENT_VIEW AS SEV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                   AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                                   AND ENROLL_TERM = '2024FA') THEN 1
                    ELSE 0 END AS RETURNED
         FROM (
---------------------------------------------------COHORT---------------------------------------------------------------
                  SELECT ID,
                         TERM
                  FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                        APPL_START_TERM                                                          AS TERM,
                                        TERM_START_DATE,
                                        ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                        FROM APPLICATIONS AS AP
                                 JOIN STUDENT_ACAD_CRED AS AC
                                      ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                 JOIN STC_STATUSES AS STAT
                                      ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                 JOIN TERMS ON APPL_START_TERM = TERMS_ID
                        WHERE APPL_DATE IS NOT NULL
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                          AND STC_STATUS IN ('A', 'N')
                          AND STC_CRED_TYPE IN ('INST')
                          ----------FFUG------------------
                        AND APPL_STUDENT_TYPE = 'UG'
                        AND APPL_STUDENT_LOAD_INTENT = 'F'
                        AND APPL_ADMIT_STATUS = 'FY'
                 ) AS X
                  WHERE TERM_ORDER = 1
------------------------------------------------------------------------------------------------------------------------
              ) AS COHORT
------------------------------------------------------------------------------------------------------------------------
         WHERE TERM = '2022FA'
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT FORMAT(AVG(1.0 * RETURNED), 'P') AS RATE
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
        {query}
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
--(End 2)---------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Overall Retention Rate (2022FA to 2024FA)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getOverallRetentionRate_2023FA_TO_2024FA(self):
        query = f"""
                 SELECT COHORT.ID,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ENROLLMENT_VIEW AS SEV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                   AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                                   AND ENROLL_TERM = '2024FA') THEN 1
                    ELSE 0 END AS RETURNED
         FROM (
---------------------------------------------------COHORT---------------------------------------------------------------
                  SELECT ID,
                         TERM
                  FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                        APPL_START_TERM                                                          AS TERM,
                                        TERM_START_DATE,
                                        ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                        FROM APPLICATIONS AS AP
                                 JOIN STUDENT_ACAD_CRED AS AC
                                      ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                 JOIN STC_STATUSES AS STAT
                                      ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                 JOIN TERMS ON APPL_START_TERM = TERMS_ID
                        WHERE APPL_DATE IS NOT NULL
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                          AND STC_STATUS IN ('A', 'N')
                          AND STC_CRED_TYPE IN ('INST')
                          ----------FFUG------------------
                        AND APPL_STUDENT_TYPE = 'UG'
                        AND APPL_STUDENT_LOAD_INTENT = 'F'
                        AND APPL_ADMIT_STATUS = 'FY'
                 ) AS X
                  WHERE TERM_ORDER = 1
------------------------------------------------------------------------------------------------------------------------
              ) AS COHORT
------------------------------------------------------------------------------------------------------------------------
         WHERE TERM = '2023FA'
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT FORMAT(AVG(1.0 * RETURNED), 'P') AS RATE
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
        {query}
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
--(End 2)---------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Overall Retention Rate (2023FA to 2024FA)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getOverallRetentionRate_2024FA_TO_2025SP(self):
        query = f"""
                 SELECT COHORT.ID,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ENROLLMENT_VIEW AS SEV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                   AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                                   AND ENROLL_TERM = '2025SP') THEN 1
                    ELSE 0 END AS RETURNED
         FROM (
---------------------------------------------------COHORT---------------------------------------------------------------
                  SELECT ID,
                         TERM
                  FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                        APPL_START_TERM                                                          AS TERM,
                                        TERM_START_DATE,
                                        ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                        FROM APPLICATIONS AS AP
                                 JOIN STUDENT_ACAD_CRED AS AC
                                      ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                 JOIN STC_STATUSES AS STAT
                                      ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                 JOIN TERMS ON APPL_START_TERM = TERMS_ID
                        WHERE APPL_DATE IS NOT NULL
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                          AND STC_STATUS IN ('A', 'N')
                          AND STC_CRED_TYPE IN ('INST')
                          ----------FFUG------------------
                        AND APPL_STUDENT_TYPE = 'UG'
                        AND APPL_STUDENT_LOAD_INTENT = 'F'
                        AND APPL_ADMIT_STATUS = 'FY'
                 ) AS X
                  WHERE TERM_ORDER = 1
------------------------------------------------------------------------------------------------------------------------
              ) AS COHORT
------------------------------------------------------------------------------------------------------------------------
         WHERE TERM = '2024FA'
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT FORMAT(AVG(1.0 * RETURNED), 'P') AS RATE
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
        {query}
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
--(End 2)---------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Overall Retention Rate (2024FA to 2025SP)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getPersistenceRateOfCarrollCollege(self):
        query = f"""
        SELECT COHORT.ID,
             COHORT.TERM,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS PERSISTED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES ('2021FA', '2022SP'),
                            ('2022FA', '2023SP'),
                            ('2023FA', '2024SP')) AS NEXT_TERM(X, Y) ON TERM = X
      WHERE TERM_ORDER = 1
        """
        agg = lambda query: f"""
        --(Begin 2)---------------------------------------------------------------------------------
SELECT TERM,
       AVG(1.0 * PERSISTED) AS PERSISTENCE_RATE
    FROM (
--(Begin 1)---------------------------------------------------------------------------------
        {query}
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Persistence Rate of Carroll College"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getPersistenceRateOfCarrollCollege_Disaggregated(self):
        query = f"""
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN PERSISTED = 1 THEN 0 ELSE 1 END) AS NOT_PERSISTED,
       SUM(PERSISTED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * PERSISTED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             CASE WHEN (STUDENT_AGE >= 17 AND STUDENT_AGE <= 19) THEN '17-19'
                  WHEN (STUDENT_AGE >= 20) THEN '20 and Over' END AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS PERSISTED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024SP')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN STUDENT_ENROLLMENT_VIEW ON COHORT.ID = STUDENT_ID
      WHERE TERM_ORDER = 1
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
------------------------------------------------------------------------------------------------------------------------
UNION
------------------------------------------------------------------------------------------------------------------------
SELECT TERM,
        CATEGORY,
       SUM(CASE WHEN PERSISTED = 1 THEN 0 ELSE 1 END) AS NOT_PERSISTED,
       SUM(PERSISTED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * PERSISTED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             CASE WHEN GENDER = 'F' THEN 'Female' WHEN GENDER = 'M' THEN 'Male' END AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS PERSISTED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024SP')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN PERSON ON COHORT.ID = PERSON.ID
      WHERE TERM_ORDER = 1
      AND GENDER IS NOT NULL
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
------------------------------------------------------------------------------------------------------------------------
UNION
------------------------------------------------------------------------------------------------------------------------
--(Begin 2)---------------------------------------------------------------------------------
SELECT TERM,
       'Pell' AS CATEGORY,
       SUM(CASE WHEN PERSISTED = 1 THEN 0 ELSE 1 END) AS NOT_PERSISTED,
       SUM(PERSISTED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * PERSISTED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT COHORT.ID,
             COHORT.TERM,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS PERSISTED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024SP')) AS NEXT_TERM(X, Y) ON TERM = X
      WHERE TERM_ORDER = 1
      AND EXISTS (
          SELECT 1
          FROM (
              SELECT SA_STUDENT_ID, AW_TERM
                FROM (
                      SELECT '2023FA' AS AW_TERM, *
                      FROM F23_AWARD_LIST) AS X
                WHERE SA_AWARD = 'FPELL'
                AND SA_ACTION = 'A'
               ) AS X
          WHERE COHORT.ID = SA_STUDENT_ID AND COHORT.TERM = AW_TERM
      )
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM
--(End 2)------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
UNION
------------------------------------------------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN PERSISTED = 1 THEN 0 ELSE 1 END) AS NOT_PERSISTED,
       SUM(PERSISTED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * PERSISTED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             RACE.IPEDS_RACE_ETHNIC_DESC AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS PERSISTED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024SP')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON RACE.ID = COHORT.ID
      WHERE TERM_ORDER = 1
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
------------------------------------------------------------------------------------------------------------------------
UNION
------------------------------------------------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN PERSISTED = 1 THEN 0 ELSE 1 END) AS NOT_PERSISTED,
       SUM(PERSISTED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * PERSISTED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             CASE WHEN STATE = 'MT' THEN 'In State' ELSE 'Out of State' END AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS PERSISTED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024SP')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN (
                    SELECT ID,
                           STATE
                    FROM (SELECT ID,
                                 PAV.STATE,
                                 ROW_NUMBER() OVER (PARTITION BY ID ORDER BY ADDRESS_ADD_DATE) AS RANK
                          FROM PERSON_ADDRESSES_VIEW AS PAV
                                   JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                          WHERE ADDRESS_TYPE = 'H') AS X
                    WHERE RANK = 1
                ) AS STUDENT_STATE ON COHORT.ID = STUDENT_STATE.ID
      WHERE TERM_ORDER = 1
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
        """
        report = "2025-06-19-Consumer Reports"
        name = "Persistence Rate of Carroll College (Disaggregated)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict=None)(report, name)

    def getPersistenceRateOfCarrollCollege_Disaggregated_Age(self):
        query = f"""
        SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             CASE WHEN (STUDENT_AGE >= 17 AND STUDENT_AGE <= 19) THEN '17-19'
                  WHEN (STUDENT_AGE >= 20) THEN '20 and Over' END AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS PERSISTED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024SP')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN STUDENT_ENROLLMENT_VIEW ON COHORT.ID = STUDENT_ID
      WHERE TERM_ORDER = 1
        """
        agg = lambda query: f"""
        SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN PERSISTED = 1 THEN 0 ELSE 1 END) AS NOT_PERSISTED,
       SUM(PERSISTED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * PERSISTED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM ({query}
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Persistence Rate of Carroll College (Disaggregated-Age)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getPersistenceRateOfCarrollCollege_Disaggregated_Gender(self):
        query = f"""
        SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             COALESCE(GENDER, 'Unknown') AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS PERSISTED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024SP')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN PERSON ON COHORT.ID = PERSON.ID
      WHERE TERM_ORDER = 1
        """
        agg = lambda query: f"""
        SELECT TERM,
        CATEGORY,
       SUM(CASE WHEN PERSISTED = 1 THEN 0 ELSE 1 END) AS NOT_PERSISTED,
       SUM(PERSISTED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * PERSISTED) AS RATE
        --(Begin 1)---------------------------------------------------------------------------------
        FROM ({query}
        --(End 1)------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Persistence Rate of Carroll College (Disaggregated-Gender)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getPersistenceRateOfCarrollCollege_Disaggregated_Pell(self):
        query = f"""
        SELECT COHORT.ID,
             COHORT.TERM,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS PERSISTED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024SP')) AS NEXT_TERM(X, Y) ON TERM = X
      WHERE TERM_ORDER = 1
      AND EXISTS (
          SELECT 1
          FROM (
              SELECT SA_STUDENT_ID, AW_TERM
                FROM (
                      SELECT '2023FA' AS AW_TERM, *
                      FROM F23_AWARD_LIST) AS X
                WHERE SA_AWARD = 'FPELL'
                AND SA_ACTION = 'A'
               ) AS X
          WHERE COHORT.ID = SA_STUDENT_ID AND COHORT.TERM = AW_TERM
      )
        """
        agg = lambda query: f"""
        --(Begin 2)---------------------------------------------------------------------------------
SELECT TERM,
       'Pell' AS CATEGORY,
       SUM(CASE WHEN PERSISTED = 1 THEN 0 ELSE 1 END) AS NOT_PERSISTED,
       SUM(PERSISTED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * PERSISTED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM ({query}
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM
--(End 2)------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Persistence Rate of Carroll College (Disaggregated-Pell)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getPersistenceRateOfCarrollCollege_Disaggregated_Race(self):
        query = f"""
        SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             RACE.IPEDS_RACE_ETHNIC_DESC AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS PERSISTED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024SP')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON RACE.ID = COHORT.ID
      WHERE TERM_ORDER = 1
        """
        agg = lambda query: f"""
        SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN PERSISTED = 1 THEN 0 ELSE 1 END) AS NOT_PERSISTED,
       SUM(PERSISTED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * PERSISTED) AS RATE
        --(Begin 1)---------------------------------------------------------------------------------
        FROM ({query}
        --(End 1)------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Persistence Rate of Carroll College (Disaggregated-Race)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getPersistenceRateOfCarrollCollege_Disaggregated_ResidencyStatus(self):
        query = f"""
        SELECT DISTINCT COHORT.ID,
                     COHORT.TERM,
                     CASE WHEN STATE = 'MT' THEN 'In State' ELSE 'Out of State' END AS CATEGORY,
                     CASE
                         WHEN EXISTS (SELECT 1
                                      FROM STUDENT_ENROLLMENT_VIEW
                                      WHERE STUDENT_ID = COHORT.ID
                                        AND ENROLL_TERM = NEXT_TERM.Y
                                        AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                        AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                         ELSE 0 END AS PERSISTED
              FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                    APPL_START_TERM                                                          AS TERM,
                                    TERM_START_DATE,
                                    ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                    FROM APPLICATIONS AS AP
                             JOIN STUDENT_ACAD_CRED AS AC
                                  ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                             JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                             JOIN TERMS ON APPL_START_TERM = TERMS_ID
                            WHERE APPL_DATE IS NOT NULL
                            AND APPL_ACAD_PROGRAM != 'NDEG'
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                      AND STC_STATUS IN ('A', 'N')
                      AND STC_CRED_TYPE IN ('INST')) AS COHORT
                       JOIN (VALUES
                                    ('2023FA', '2024SP')) AS NEXT_TERM(X, Y) ON TERM = X
                        JOIN (
                            SELECT ID,
                                   STATE
                            FROM (SELECT ID,
                                         PAV.STATE,
                                         ROW_NUMBER() OVER (PARTITION BY ID ORDER BY ADDRESS_ADD_DATE) AS RANK
                                  FROM PERSON_ADDRESSES_VIEW AS PAV
                                           JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                                  WHERE ADDRESS_TYPE = 'H') AS X
                            WHERE RANK = 1
                        ) AS STUDENT_STATE ON COHORT.ID = STUDENT_STATE.ID
              WHERE TERM_ORDER = 1
                """
        agg = lambda query: f"""
                SELECT TERM,
               CATEGORY,
               SUM(CASE WHEN PERSISTED = 1 THEN 0 ELSE 1 END) AS NOT_PERSISTED,
               SUM(PERSISTED) AS PERSISTED,
               COUNT(*) AS TOTAL,
               AVG(1.0 * PERSISTED) AS RATE
               FROM (
        --(Begin 1)---------------------------------------------------------------------------------
        {query}
        --(End 1)------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Persistence Rate of Carroll College (Disaggregated-Residency Status)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getRetentionRateOfCarrollCollege_Disaggregated(self):
        query = f"""
        SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN RETAINED = 1 THEN 0 ELSE 1 END) AS NOT_RETAINED,
       SUM(RETAINED) AS RETAINED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * RETAINED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             CASE WHEN (STUDENT_AGE >= 17 AND STUDENT_AGE <= 19) THEN '17-19'
                  WHEN (STUDENT_AGE >= 20) THEN '20 and Over' END AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN STUDENT_ENROLLMENT_VIEW ON COHORT.ID = STUDENT_ID
      WHERE TERM_ORDER = 1
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
------------------------------------------------------------------------------------------------------------------------
UNION
------------------------------------------------------------------------------------------------------------------------
SELECT TERM,
        CATEGORY,
       SUM(CASE WHEN RETAINED = 1 THEN 0 ELSE 1 END) AS NOT_RETAINED,
       SUM(RETAINED) AS RETAINED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * RETAINED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             CASE WHEN GENDER = 'F' THEN 'Female' WHEN GENDER = 'M' THEN 'Male' END AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN PERSON ON COHORT.ID = PERSON.ID
      WHERE TERM_ORDER = 1
      AND GENDER IS NOT NULL
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
------------------------------------------------------------------------------------------------------------------------
UNION
------------------------------------------------------------------------------------------------------------------------
--(Begin 2)---------------------------------------------------------------------------------
SELECT TERM,
       'Pell' AS CATEGORY,
       SUM(CASE WHEN RETAINED = 1 THEN 0 ELSE 1 END) AS NOT_RETAINED,
       SUM(RETAINED) AS RETAINED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * RETAINED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT COHORT.ID,
             COHORT.TERM,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
      WHERE TERM_ORDER = 1
      AND EXISTS (
          SELECT 1
          FROM (
              SELECT SA_STUDENT_ID, AW_TERM
                FROM (
                      SELECT '2023FA' AS AW_TERM, *
                      FROM F23_AWARD_LIST) AS X
                WHERE SA_AWARD = 'FPELL'
                AND SA_ACTION = 'A'
               ) AS X
          WHERE COHORT.ID = SA_STUDENT_ID AND COHORT.TERM = AW_TERM
      )
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM
--(End 2)------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
UNION
------------------------------------------------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN RETAINED = 1 THEN 0 ELSE 1 END) AS NOT_RETAINED,
       SUM(RETAINED) AS RETAINED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * RETAINED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             RACE.IPEDS_RACE_ETHNIC_DESC AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON RACE.ID = COHORT.ID
      WHERE TERM_ORDER = 1
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
------------------------------------------------------------------------------------------------------------------------
UNION
------------------------------------------------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN RETAINED = 1 THEN 0 ELSE 1 END) AS NOT_RETAINED,
       SUM(RETAINED) AS RETAINED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * RETAINED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             CASE WHEN STATE = 'MT' THEN 'In State' ELSE 'Out of State' END AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN (
                    SELECT ID,
                           STATE
                    FROM (SELECT ID,
                                 PAV.STATE,
                                 ROW_NUMBER() OVER (PARTITION BY ID ORDER BY ADDRESS_ADD_DATE) AS RANK
                          FROM PERSON_ADDRESSES_VIEW AS PAV
                                   JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                          WHERE ADDRESS_TYPE = 'H') AS X
                    WHERE RANK = 1
                ) AS STUDENT_STATE ON COHORT.ID = STUDENT_STATE.ID
      WHERE TERM_ORDER = 1
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
        """
        report = "2025-06-19-Consumer Reports"
        name = "Retention Rate of Carroll College (Disaggregated)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict=None)(report, name)

    def getRetentionRateOfCarrollCollege_Disaggregated_Age(self):
        query = f"""
        SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             CASE WHEN (STUDENT_AGE >= 17 AND STUDENT_AGE <= 19) THEN '17-19'
                  WHEN (STUDENT_AGE >= 20) THEN '20 and Over' END AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN STUDENT_ENROLLMENT_VIEW ON COHORT.ID = STUDENT_ID
      WHERE TERM_ORDER = 1
        """
        agg = lambda query: f"""
        SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN RETAINED = 1 THEN 0 ELSE 1 END) AS NOT_RETAINED,
       SUM(RETAINED) AS RETAINED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * RETAINED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM ({query}
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Retention Rate of Carroll College (Disaggregated-Age)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getRetentionRateOfCarrollCollege_Disaggregated_Gender(self):
        query = f"""
        SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             CASE WHEN GENDER = 'F' THEN 'Female' WHEN GENDER = 'M' THEN 'Male' END AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN PERSON ON COHORT.ID = PERSON.ID
      WHERE TERM_ORDER = 1
      AND GENDER IS NOT NULL
        """
        agg = lambda query: f"""
        SELECT TERM,
        CATEGORY,
       SUM(CASE WHEN RETAINED = 1 THEN 0 ELSE 1 END) AS NOT_RETAINED,
       SUM(RETAINED) AS RETAINED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * RETAINED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM ({query}
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Retention Rate of Carroll College (Disaggregated-Gender)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getRetentionRateOfCarrollCollege_Disaggregated_Pell(self):
        query = f"""
        SELECT COHORT.ID,
             COHORT.TERM,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
      WHERE TERM_ORDER = 1
      AND EXISTS (
          SELECT 1
          FROM (
              SELECT SA_STUDENT_ID, AW_TERM
                FROM (
                      SELECT '2023FA' AS AW_TERM, *
                      FROM F23_AWARD_LIST) AS X
                WHERE SA_AWARD = 'FPELL'
                AND SA_ACTION = 'A'
               ) AS X
          WHERE COHORT.ID = SA_STUDENT_ID AND COHORT.TERM = AW_TERM
      )
        """
        agg = lambda query: f"""
        --(Begin 2)---------------------------------------------------------------------------------
SELECT TERM,
       'Pell' AS CATEGORY,
       SUM(CASE WHEN RETAINED = 1 THEN 0 ELSE 1 END) AS NOT_RETAINED,
       SUM(RETAINED) AS RETAINED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * RETAINED) AS RATE
       FROM (
--(Begin 1)---------------------------------------------------------------------------------
        {query}
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM
--(End 2)------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Retention Rate of Carroll College (Disaggregated-Pell)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getRetentionRateOfCarrollCollege_Disaggregated_Race(self):
        query = f"""
        SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             RACE.IPEDS_RACE_ETHNIC_DESC AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON RACE.ID = COHORT.ID
      WHERE TERM_ORDER = 1
        """
        agg = lambda query: f"""
        SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN RETAINED = 1 THEN 0 ELSE 1 END) AS NOT_RETAINED,
       SUM(RETAINED) AS RETAINED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * RETAINED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM ({query}
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Retention Rate of Carroll College (Disaggregated-Race)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getRetentionRateOfCarrollCollege_Disaggregated_ResidencyStatus(self):
        query = f"""
        SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             CASE WHEN STATE = 'MT' THEN 'In State' ELSE 'Out of State' END AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN (
                    SELECT ID,
                           STATE
                    FROM (SELECT ID,
                                 PAV.STATE,
                                 ROW_NUMBER() OVER (PARTITION BY ID ORDER BY ADDRESS_ADD_DATE) AS RANK
                          FROM PERSON_ADDRESSES_VIEW AS PAV
                                   JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                          WHERE ADDRESS_TYPE = 'H') AS X
                    WHERE RANK = 1
                ) AS STUDENT_STATE ON COHORT.ID = STUDENT_STATE.ID
      WHERE TERM_ORDER = 1
        """
        agg = lambda query: f"""
        SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN RETAINED = 1 THEN 0 ELSE 1 END) AS NOT_RETAINED,
       SUM(RETAINED) AS RETAINED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * RETAINED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM ({query}
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-19-Consumer Reports"
        name = "Retention Rate of Carroll College (Disaggregated-Residency Status)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTotalPellRecipients(self):
        query = f"""
        SELECT COUNT(DISTINCT SA_STUDENT_ID) AS PELL_RECIPIENTS
        FROM F24_AWARD_LIST
        WHERE SA_ACTION = 'A'
        AND SA_AWARD = 'FPELL'
        """
        report = "2025-06-19-Consumer Reports"
        name = "Total Pell Recipients"
        self.save_query_results(query, snapshot_term="2025SP", func_dict=None)(report, name)


    '''
    ID: Unknown
    Name: 2025-06-25-Faculty
    Person: Rebecca Schwartz
    Start Date: 2025-06-25
    End Date: 2025-06-25
    Description:
        I needed to get the faculty by last academic year grouped by load. 
    '''
    def getFaculty(self):
        query = f"""
        SELECT DISTINCT PERSTAT_HRP_ID AS ID,
                FIRST_NAME,
                LAST_NAME,
       CASE WHEN PERSTAT_STATUS = 'FT' THEN 'Full-Time' ELSE 'Part-Time' END AS STATUS
        FROM PERSTAT
        JOIN POSITION ON PERSTAT_PRIMARY_POS_ID = POSITION_ID
        JOIN PERSON ON PERSTAT_HRP_ID = PERSON.ID
        WHERE POS_CLASS = 'FAC'
        AND (COALESCE(POS_RANK, '') != 'A'
            OR EXISTS (
                SELECT 1
                FROM FACULTY_SECTIONS_DETAILS_VIEW AS FS
                JOIN COURSE_SECTIONS AS CS ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
                WHERE CS_TERM IN ('2024SU', '2024FA', '2025SP')
                AND SEC_BILLING_CRED > 0
                AND FACULTY_ID = PERSTAT_HRP_ID
            ))
        AND PERSTAT_START_DATE <= (
            SELECT TOP 1 TERM_END_DATE
            FROM TERMS
            WHERE TERMS_ID = '2025SP'
            )
        AND (PERSTAT_END_DATE >= (
            SELECT TOP 1 TERM_START_DATE
            FROM TERMS
            WHERE TERMS_ID = '2024SU'
            ) OR PERSTAT_END_DATE IS NULL)
        """
        report = "2025-06-25-Faculty"
        name = "Faculty"
        self.save_query_results(query, snapshot_term="2025SP", func_dict=None)(report, name)

    '''
    ID: Unknown
    Name: 2025-06-25-Student Residencies
    Person: Rebecca Schwartz
    Start Date: 2025-06-25
    End Date: 2025-06-25
    Description:
        I needed to calculate student residencies.
    '''
    def getCampusResidencyPercentage(self):
        query = f"""
        --(Begin 3)-----------------------------------------------------------------------------------
                  SELECT DISTINCT STUDENT_ID,
                                  CASE WHEN ADDRESS_TYPE = 'CA' THEN 1 ELSE 0 END AS CAMPUS_STATUS
                  FROM STUDENT_ENROLLMENT_VIEW AS SEV
                           JOIN (
        --(Begin 2)-----------------------------------------------------------------------------------
                              SELECT ID,
                                     ADDRESS_TYPE
                              FROM (
        --(Begin 1)-----------------------------------------------------------------------------------
                                       SELECT PAV.ID,
                                              ADDRESS_TYPE,
                                              ROW_NUMBER() OVER (PARTITION BY PAV.ID
                                                  ORDER BY CASE WHEN ADDRESS_TYPE = 'CA' THEN 0 ELSE 1 END) AS ADDRESS_RANK
                                       FROM PERSON_ADDRESSES_VIEW AS PAV
                                       JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
        --(End 1)-------------------------------------------------------------------------------------
                                   ) AS X
                              WHERE ADDRESS_RANK = 1
        --(End 2)-------------------------------------------------------------------------------------
                          ) AS STUDENT_STATE ON SEV.STUDENT_ID = STUDENT_STATE.ID
                          WHERE ENROLL_CREDIT_TYPE = 'Institutional'
                            AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                            AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                            AND ENROLL_TERM IN ('2024FA', '2025SP', '2024SU')
        --(End 3)-------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 4)-----------------------------------------------------------------------------------
         SELECT FORMAT(AVG(1.0 * CAMPUS_STATUS), 'P') AS CAMPUS_RESIDENCY_RATE
         FROM (
        --(Begin 3)-----------------------------------------------------------------------------------
        {query}
        --(End 3)-------------------------------------------------------------------------------------
                      ) AS X
        --(End 4)-------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-25-Student Residencies"
        name = "Campus Residency Percentage"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getStudentResidencyCount(self):
        query = f"""
        --(Begin 3)-----------------------------------------------------------------------------------
                  SELECT DISTINCT STUDENT_ID,
                                  CASE WHEN STATE = 'MT' THEN 'In-State' ELSE 'Out of State' END AS RESIDENCY_STATUS
                  FROM STUDENT_ENROLLMENT_VIEW AS SEV
                           JOIN (
        --(Begin 2)-----------------------------------------------------------------------------------
        
                              SELECT ID,
                                     STATE
                              FROM (
        --(Begin 1)-----------------------------------------------------------------------------------
                                       SELECT PAV.ID,
                                              PAV.STATE,
                                              ROW_NUMBER() OVER (PARTITION BY PAV.ID ORDER BY ADDRESS_ADD_DATE) AS ADDRESS_RANK
                                       FROM PERSON_ADDRESSES_VIEW AS PAV
                                       JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                                       WHERE ADDRESS_TYPE = 'H'
        --(End 1)-------------------------------------------------------------------------------------
                                   ) AS X
                              WHERE ADDRESS_RANK = 1
        --(End 2)-------------------------------------------------------------------------------------
                          ) AS STUDENT_STATE ON SEV.STUDENT_ID = STUDENT_STATE.ID
                          WHERE ENROLL_CREDIT_TYPE = 'Institutional'
                            AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                            AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                            AND ENROLL_TERM IN ('2024FA', '2025SP', '2024SU')
        --(End 3)-------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 4)-----------------------------------------------------------------------------------
         SELECT COUNT(*) AS TOTAL
         FROM (
        --(Begin 3)-----------------------------------------------------------------------------------
                {query}
        --(End 3)-------------------------------------------------------------------------------------
                      ) AS X
        --(End 4)-------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-25-Student Residencies"
        name = "Campus Residency Count"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getCountryCount(self):
        query = f"""
        --(Begin 2)-----------------------------------------------------------------------------------
                      SELECT ID,
                             COUNTRY
                      FROM (
        --(Begin 1)-----------------------------------------------------------------------------------
                                       SELECT PAV.ID,
                                              PAV.COUNTRY,
                                              ROW_NUMBER() OVER (PARTITION BY PAV.ID ORDER BY ADDRESS_ADD_DATE) AS ADDRESS_RANK
                                       FROM PERSON_ADDRESSES_VIEW AS PAV
                                       JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                                       WHERE ADDRESS_TYPE = 'H'
        --(End 1)-------------------------------------------------------------------------------------
                                   ) AS X
                              WHERE ADDRESS_RANK = 1
        --(End 2)-------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 4)-----------------------------------------------------------------------------------
         SELECT COUNT(*) AS TOTAL_COUNTRIES
         FROM (
        --(Begin 3)-----------------------------------------------------------------------------------
                          SELECT DISTINCT COUNTRY,
                                          COUNTRIES.CTRY_DESC
                          FROM STUDENT_ENROLLMENT_VIEW AS SEV
                                   JOIN (
        --(Begin 2)-----------------------------------------------------------------------------------
            {query}
        --(End 2)-------------------------------------------------------------------------------------
                          ) AS STUDENT_COUNTRY ON SEV.STUDENT_ID = STUDENT_COUNTRY.ID
                          JOIN COUNTRIES ON STUDENT_COUNTRY.COUNTRY = COUNTRIES_ID
                          WHERE ENROLL_CREDIT_TYPE = 'Institutional'
                            AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                            AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                            AND ENROLL_TERM IN ('2024FA', '2025SP', '2024SU')
        --(End 3)-------------------------------------------------------------------------------------
                      ) AS X
        --(End 4)-------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-25-Student Residencies"
        name = "Country Count"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getStudentResidencyPercent(self):
        query = f"""
        --(Begin 3)-----------------------------------------------------------------------------------
                  SELECT DISTINCT STUDENT_ID,
                                  CASE WHEN STATE = 'MT' THEN 'In-State' ELSE 'Out of State' END AS RESIDENCY_STATUS
                  FROM STUDENT_ENROLLMENT_VIEW AS SEV
                           JOIN (
        --(Begin 2)-----------------------------------------------------------------------------------
        
                              SELECT ID,
                                     STATE
                              FROM (
        --(Begin 1)-----------------------------------------------------------------------------------
                                       SELECT PAV.ID,
                                              PAV.STATE,
                                              ROW_NUMBER() OVER (PARTITION BY PAV.ID ORDER BY ADDRESS_ADD_DATE) AS ADDRESS_RANK
                                       FROM PERSON_ADDRESSES_VIEW AS PAV
                                       JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                                       WHERE ADDRESS_TYPE = 'H'
        --(End 1)-------------------------------------------------------------------------------------
                                   ) AS X
                              WHERE ADDRESS_RANK = 1
        --(End 2)-------------------------------------------------------------------------------------
                          ) AS STUDENT_STATE ON SEV.STUDENT_ID = STUDENT_STATE.ID
                          WHERE ENROLL_CREDIT_TYPE = 'Institutional'
                            AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                            AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                            AND ENROLL_TERM IN ('2024FA', '2025SP', '2024SU')
        --(End 3)-------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 4)-----------------------------------------------------------------------------------
         SELECT RESIDENCY_STATUS,
                FORMAT(CAST(COUNT(*) AS FLOAT) /  SUM(COUNT(*)) OVER (), 'P')  AS STATUS_PERCENT
         FROM (
        --(Begin 3)-----------------------------------------------------------------------------------
            {query}
        --(End 3)-------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY RESIDENCY_STATUS
        --(End 4)-------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-25-Student Residencies"
        name = "Student Residency Percent"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getStateCount(self):
        query = f"""
        --(Begin 2)-----------------------------------------------------------------------------------

                      SELECT ID,
                             STATE
                      FROM (
        --(Begin 1)-----------------------------------------------------------------------------------
                                       SELECT PAV.ID,
                                              PAV.STATE,
                                              ROW_NUMBER() OVER (PARTITION BY PAV.ID ORDER BY ADDRESS_ADD_DATE) AS ADDRESS_RANK
                                       FROM PERSON_ADDRESSES_VIEW AS PAV
                                       JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                                       WHERE ADDRESS_TYPE = 'H'
        --(End 1)-------------------------------------------------------------------------------------
                                   ) AS X
                              WHERE ADDRESS_RANK = 1
        --(End 2)-------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 4)-----------------------------------------------------------------------------------
         SELECT COUNT(*) AS TOTAL_STATES
         FROM (
        --(Begin 3)-----------------------------------------------------------------------------------
                          SELECT DISTINCT STATE
                          FROM STUDENT_ENROLLMENT_VIEW AS SEV
                                   JOIN (
        --(Begin 2)-----------------------------------------------------------------------------------
                {query}
        --(End 2)-------------------------------------------------------------------------------------
                          ) AS STUDENT_STATE ON SEV.STUDENT_ID = STUDENT_STATE.ID
                          JOIN STATES ON STUDENT_STATE.STATE = STATES.STATES_ID
                          WHERE ENROLL_CREDIT_TYPE = 'Institutional'
                            AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                            AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                            AND ENROLL_TERM IN ('2024FA', '2025SP', '2024SU')
                            AND STATES.ST_USER1 = 1
        --(End 3)-------------------------------------------------------------------------------------
                      ) AS X
        --(End 4)-------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-25-Student Residencies"
        name = "State Count"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTopOtherStates(self):
        query = f"""
        --(Begin 3)-----------------------------------------------------------------------------------
                  SELECT DISTINCT STUDENT_ID,
                                  STATE
                  FROM STUDENT_ENROLLMENT_VIEW AS SEV
                           JOIN (
        --(Begin 2)-----------------------------------------------------------------------------------
        
                              SELECT ID,
                                     STATE
                              FROM (
        --(Begin 1)-----------------------------------------------------------------------------------
                                       SELECT PAV.ID,
                                              PAV.STATE,
                                              ROW_NUMBER() OVER (PARTITION BY PAV.ID ORDER BY ADDRESS_ADD_DATE) AS ADDRESS_RANK
                                       FROM PERSON_ADDRESSES_VIEW AS PAV
                                       JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                                       WHERE ADDRESS_TYPE = 'H'
        --(End 1)-------------------------------------------------------------------------------------
                                   ) AS X
                              WHERE ADDRESS_RANK = 1
        --(End 2)-------------------------------------------------------------------------------------
                          ) AS STUDENT_STATE ON SEV.STUDENT_ID = STUDENT_STATE.ID
                          WHERE ENROLL_CREDIT_TYPE = 'Institutional'
                            AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                            AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                            AND ENROLL_TERM IN ('2024FA', '2025SP', '2024SU')
                          AND STATE IS NOT NULL
                          AND STATE != 'MT'
        --(End 3)-------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 4)-----------------------------------------------------------------------------------
                 SELECT TOP 4 STATE,
                        COUNT(*) AS STATE_COUNT
                 FROM (
        --(Begin 3)-----------------------------------------------------------------------------------
            {query}
        --(End 3)-------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY STATE
        --(End 4)-------------------------------------------------------------------------------------
        ORDER BY STATE_COUNT DESC
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-25-Student Residencies"
        name = "Top Other States"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    '''
    ID: Unknown
    Name: 2025-06-30-NWCCU
    Person: Amy Honchell
    Start Date: 2025-06-30
    End Date: 2025-06-30
    '''
    #===================================================================================================================
    '''
    Code is in another file.
    '''
    # ===================================================================================================================

    '''
    ID: Unknown
    Name: 2025-06-30-NWCCU Carroll
    Person: Amy Honchell
    Start Date: 2025-06-30
    End Date: 2025-06-30
    Description:
        I needed to generate data for NWCCU accreditation.
    '''

    def getGraduationRate_4Year_ByAge(self):
        query = f"""
        --(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                 CASE WHEN (STUDENT_AGE >= (17 + DATEDIFF(YEAR, 2017, 2024)) AND STUDENT_AGE <= + DATEDIFF(YEAR, 2017, 2024)) THEN '17-19'
                  WHEN (STUDENT_AGE >= 20) THEN '20 and Over' END AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 4, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS FOUR_YEAR_GRADUATED
         FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                          APPL_START_TERM                                                          AS TERM,
                                          TERM_START_DATE,
                                          ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
        -------------------------------------------------------------------------------------------------------------------
                          FROM APPLICATIONS AS AP
                                   JOIN STUDENT_ACAD_CRED AS AC
                                        ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                   JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                   JOIN TERMS ON APPL_START_TERM = TERMS_ID
                          WHERE APPL_DATE IS NOT NULL
                            AND APPL_ACAD_PROGRAM != 'NDEG'
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                            AND STC_STATUS IN ('A', 'N')
                            AND STC_CRED_TYPE IN ('INST')
        --(End 1)---------------------------------------------------------------------------------------------------------
                      ) AS COHORT
                          JOIN (VALUES
                                       ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                            JOIN STUDENT_ENROLLMENT_VIEW ON COHORT.ID = STUDENT_ID
                 WHERE TERM_ORDER = 1
        --(End 2)------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        --(Begin 3)---------------------------------------------------------------------------------
        SELECT TERM,
               CATEGORY,
               SUM(CASE WHEN FOUR_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_FOUR_YEAR_GRADUATED,
               SUM(FOUR_YEAR_GRADUATED) AS PERSISTED,
               COUNT(*) AS TOTAL,
               AVG(1.0 * FOUR_YEAR_GRADUATED) AS RATE
        FROM (
        --(Begin 2)---------------------------------------------------------------------------------
            {query}
        --(End 2)------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-30-NWCCU Carroll"
        name = "Graduation Rate (Four Year) (Disaggregated-Age)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRate_4Year_ByGender(self):
        query = f"""
        --(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                 CASE WHEN GENDER = 'M' THEN 'Male' WHEN GENDER = 'F' THEN 'Female' END AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 4, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS FOUR_YEAR_GRADUATED
         FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                          APPL_START_TERM                                                          AS TERM,
                                          TERM_START_DATE,
                                          ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
        -------------------------------------------------------------------------------------------------------------------
                          FROM APPLICATIONS AS AP
                                   JOIN STUDENT_ACAD_CRED AS AC
                                        ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                   JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                   JOIN TERMS ON APPL_START_TERM = TERMS_ID
                          WHERE APPL_DATE IS NOT NULL
                            AND APPL_ACAD_PROGRAM != 'NDEG'
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                            AND STC_STATUS IN ('A', 'N')
                            AND STC_CRED_TYPE IN ('INST')
        --(End 1)---------------------------------------------------------------------------------------------------------
                      ) AS COHORT
                          JOIN (VALUES
                                       ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                            JOIN PERSON ON COHORT.ID = PERSON.ID
                 WHERE TERM_ORDER = 1
                AND GENDER IS NOT NULL
        --(End 2)------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
--(Begin 3)---------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN FOUR_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_FOUR_YEAR_GRADUATED,
       SUM(FOUR_YEAR_GRADUATED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * FOUR_YEAR_GRADUATED) AS RATE
        FROM (
        --(Begin 2)---------------------------------------------------------------------------------
            {query}
        --(End 2)------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-30-NWCCU Carroll"
        name = "Graduation Rate (Four Year) (Disaggregated-Gender)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRate_4Year_Pell(self):
        query = f"""
        --(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 4, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS FOUR_YEAR_GRADUATED
         FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                          APPL_START_TERM                                                          AS TERM,
                                          TERM_START_DATE,
                                          ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
        -------------------------------------------------------------------------------------------------------------------
                          FROM APPLICATIONS AS AP
                                   JOIN STUDENT_ACAD_CRED AS AC
                                        ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                   JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                   JOIN TERMS ON APPL_START_TERM = TERMS_ID
                          WHERE APPL_DATE IS NOT NULL
                            AND APPL_ACAD_PROGRAM != 'NDEG'
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                            AND STC_STATUS IN ('A', 'N')
                            AND STC_CRED_TYPE IN ('INST')
        --(End 1)---------------------------------------------------------------------------------------------------------
                      ) AS COHORT
                          JOIN (VALUES
                                       ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                 WHERE TERM_ORDER = 1
                      AND EXISTS (
                  SELECT 1
                  FROM (
                      SELECT SA_STUDENT_ID, AW_TERM
                        FROM (
                              SELECT '2017FA' AS AW_TERM, *
                              FROM F17_AWARD_LIST) AS X
                        WHERE SA_AWARD = 'FPELL'
                        AND SA_ACTION = 'A'
                       ) AS X
                  WHERE COHORT.ID = SA_STUDENT_ID AND COHORT.TERM = AW_TERM
              )
        --(End 2)------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        --(Begin 3)---------------------------------------------------------------------------------
        SELECT TERM,
               'Pell' AS CATEGORY,
               SUM(CASE WHEN FOUR_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_FOUR_YEAR_GRADUATED,
               SUM(FOUR_YEAR_GRADUATED) AS PERSISTED,
               COUNT(*) AS TOTAL,
               AVG(1.0 * FOUR_YEAR_GRADUATED) AS RATE
        FROM (
--(Begin 2)---------------------------------------------------------------------------------
            {query}
        --(End 2)------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-30-NWCCU Carroll"
        name = "Graduation Rate (Four Year) (Disaggregated-Pell)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRate_4Year_Race(self):
        query = f"""
        --(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                 RACE.IPEDS_RACE_ETHNIC_DESC  AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 4, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS FOUR_YEAR_GRADUATED
         FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                          APPL_START_TERM                                                          AS TERM,
                                          TERM_START_DATE,
                                          ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
        -------------------------------------------------------------------------------------------------------------------
                          FROM APPLICATIONS AS AP
                                   JOIN STUDENT_ACAD_CRED AS AC
                                        ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                   JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                   JOIN TERMS ON APPL_START_TERM = TERMS_ID
                          WHERE APPL_DATE IS NOT NULL
                            AND APPL_ACAD_PROGRAM != 'NDEG'
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                            AND STC_STATUS IN ('A', 'N')
                            AND STC_CRED_TYPE IN ('INST')
        --(End 1)---------------------------------------------------------------------------------------------------------
                      ) AS COHORT
                          JOIN (VALUES
                                       ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                            JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON COHORT.ID = RACE.ID
                 WHERE TERM_ORDER = 1
        --(End 2)------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        --(Begin 3)---------------------------------------------------------------------------------
        SELECT TERM,
               CATEGORY,
               SUM(CASE WHEN FOUR_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_FOUR_YEAR_GRADUATED,
               SUM(FOUR_YEAR_GRADUATED) AS PERSISTED,
               COUNT(*) AS TOTAL,
               AVG(1.0 * FOUR_YEAR_GRADUATED) AS RATE
        FROM (
        --(Begin 2)---------------------------------------------------------------------------------
            {query}
        --(End 2)------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-30-NWCCU Carroll"
        name = "Graduation Rate (Four Year) (Disaggregated-Race)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRate_4Year_ResidencyStatus(self):
        query = f"""
        --(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                CASE WHEN STATE = 'MT' THEN 'In State' ELSE 'Out of State' END AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 4, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS FOUR_YEAR_GRADUATED
         FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                          APPL_START_TERM                                                          AS TERM,
                                          TERM_START_DATE,
                                          ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
        -------------------------------------------------------------------------------------------------------------------
                          FROM APPLICATIONS AS AP
                                   JOIN STUDENT_ACAD_CRED AS AC
                                        ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                   JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                   JOIN TERMS ON APPL_START_TERM = TERMS_ID
                          WHERE APPL_DATE IS NOT NULL
                            AND APPL_ACAD_PROGRAM != 'NDEG'
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                            AND STC_STATUS IN ('A', 'N')
                            AND STC_CRED_TYPE IN ('INST')
        --(End 1)---------------------------------------------------------------------------------------------------------
                      ) AS COHORT
                          JOIN (VALUES
                                       ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                     JOIN (
                            SELECT ID,
                                   STATE
                            FROM (SELECT ID,
                                         PAV.STATE,
                                         ROW_NUMBER() OVER (PARTITION BY ID ORDER BY ADDRESS_ADD_DATE) AS RANK
                                  FROM PERSON_ADDRESSES_VIEW AS PAV
                                           JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                                  WHERE ADDRESS_TYPE = 'H') AS X
                            WHERE RANK = 1
                        ) AS STUDENT_STATE ON COHORT.ID = STUDENT_STATE.ID
                 WHERE TERM_ORDER = 1
        --(End 2)------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
--(Begin 3)---------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN FOUR_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_FOUR_YEAR_GRADUATED,
       SUM(FOUR_YEAR_GRADUATED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * FOUR_YEAR_GRADUATED) AS RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
            {query}
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-30-NWCCU Carroll"
        name = "Graduation Rate (Four Year) (Disaggregated-Residency Status)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRate_6Year(self):
        query = f"""
        --(Begin 2)---------------------------------------------------------------------------------
         SELECT COHORT.ID,
                COHORT.TERM,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 6, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS SIX_YEAR_GRADUATED
         FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                          APPL_START_TERM                                                          AS TERM,
                                          TERM_START_DATE,
                                          ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
        -------------------------------------------------------------------------------------------------------------------
                          FROM APPLICATIONS AS AP
                                   JOIN STUDENT_ACAD_CRED AS AC
                                        ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                   JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                   JOIN TERMS ON APPL_START_TERM = TERMS_ID
                          WHERE APPL_DATE IS NOT NULL
                            AND APPL_ACAD_PROGRAM != 'NDEG'
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                            AND STC_STATUS IN ('A', 'N')
                            AND STC_CRED_TYPE IN ('INST')
        --(End 1)---------------------------------------------------------------------------------------------------------
                      ) AS COHORT
                          JOIN (VALUES
                                       ('2015FA'),
                                       ('2016FA'),
                                       ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                 WHERE TERM_ORDER = 1
        --(End 2)------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 3)---------------------------------------------------------------------------------
        SELECT TERM,
               AVG(1.0 * SIX_YEAR_GRADUATED) AS SIX_YEAR_GRADUATION_RATE
        FROM (
        --(Begin 2)---------------------------------------------------------------------------------
                {query}
        --(End 2)------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-30-NWCCU Carroll"
        name = "Graduation Rate (Six Year)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRate_6Year_ByAge(self):
        query = f"""
        --(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                 CASE WHEN (DATEDIFF(YEAR, PERSON.BIRTH_DATE, TERM_START_DATE) >= 17)
                    AND (DATEDIFF(YEAR, PERSON.BIRTH_DATE, TERM_START_DATE) <= 19) THEN '17-19'
                  WHEN (DATEDIFF(YEAR, PERSON.BIRTH_DATE, TERM_START_DATE) >= 20) THEN '20 and Over' END AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 6, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS SIX_YEAR_GRADUATED
         FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                          APPL_START_TERM                                                          AS TERM,
                                          TERM_START_DATE,
                                          ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
        -------------------------------------------------------------------------------------------------------------------
                          FROM APPLICATIONS AS AP
                                   JOIN STUDENT_ACAD_CRED AS AC
                                        ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                   JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                   JOIN TERMS ON APPL_START_TERM = TERMS_ID
                          WHERE APPL_DATE IS NOT NULL
                            AND APPL_ACAD_PROGRAM != 'NDEG'
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                            AND STC_STATUS IN ('A', 'N')
                            AND STC_CRED_TYPE IN ('INST')
        --(End 1)---------------------------------------------------------------------------------------------------------
                      ) AS COHORT
                          JOIN (VALUES ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                          JOIN PERSON ON COHORT.ID = PERSON.ID
                          WHERE TERM_ORDER = 1
        --(End 2)------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 3)---------------------------------------------------------------------------------
        SELECT TERM,
               CATEGORY,
               SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_SIX_YEAR_GRADUATED,
               SUM(SIX_YEAR_GRADUATED) AS GRADUATED,
               COUNT(*) AS TOTAL,
               AVG(1.0 * SIX_YEAR_GRADUATED) AS RATE
        FROM (
        --(Begin 2)---------------------------------------------------------------------------------
        {query}
        --(End 2)------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, CATEGORY
        --(End 3)------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-30-NWCCU Carroll"
        name = "Graduation Rate (Six Year) (Disaggregated-Age)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRate_6Year_ByGender(self):
        query = f"""
        --(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                 CASE WHEN GENDER = 'M' THEN 'Male' WHEN GENDER = 'F' THEN 'Female' END AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 6, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS SIX_YEAR_GRADUATED
         FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------
                  SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                  APPL_START_TERM                                                          AS TERM,
                                  TERM_START_DATE,
                                  ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
-------------------------------------------------------------------------------------------------------------------
                  FROM APPLICATIONS AS AP
                           JOIN STUDENT_ACAD_CRED AS AC
                                ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                           JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                           JOIN TERMS ON APPL_START_TERM = TERMS_ID
                  WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                    AND STC_STATUS IN ('A', 'N')
                    AND STC_CRED_TYPE IN ('INST')
--(End 1)---------------------------------------------------------------------------------------------------------
              ) AS COHORT
                  JOIN (VALUES
                               ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                    JOIN PERSON ON COHORT.ID = PERSON.ID
         WHERE TERM_ORDER = 1
        AND GENDER IS NOT NULL
--(End 2)------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 3)---------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_SIX_YEAR_GRADUATED,
       SUM(SIX_YEAR_GRADUATED) AS SIX_YEAR_GRADUATED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * SIX_YEAR_GRADUATED) AS RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
        {query}
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
--(End 3)------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-30-NWCCU Carroll"
        name = "Graduation Rate (Six Year) (Disaggregated-Gender)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRate_6Year_ByPell(self):
        query = f"""
        --(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 6, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS SIX_YEAR_GRADUATED
         FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------
                  SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                  APPL_START_TERM                                                          AS TERM,
                                  TERM_START_DATE,
                                  ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
-------------------------------------------------------------------------------------------------------------------
                  FROM APPLICATIONS AS AP
                           JOIN STUDENT_ACAD_CRED AS AC
                                ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                           JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                           JOIN TERMS ON APPL_START_TERM = TERMS_ID
                  WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                    AND STC_STATUS IN ('A', 'N')
                    AND STC_CRED_TYPE IN ('INST')
--(End 1)---------------------------------------------------------------------------------------------------------
              ) AS COHORT
                  JOIN (VALUES
                               ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
         WHERE TERM_ORDER = 1
              AND EXISTS (
          SELECT 1
          FROM (
              SELECT SA_STUDENT_ID, AW_TERM
                FROM (
                      SELECT '2017FA' AS AW_TERM, *
                      FROM F17_AWARD_LIST) AS X
                WHERE SA_AWARD = 'FPELL'
                AND SA_ACTION = 'A'
               ) AS X
          WHERE COHORT.ID = SA_STUDENT_ID AND COHORT.TERM = AW_TERM
      )
--(End 2)------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 3)---------------------------------------------------------------------------------
SELECT TERM,
       'Pell' AS CATEGORY,
       SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_SIX_YEAR_GRADUATED,
       SUM(SIX_YEAR_GRADUATED) AS SIX_YEAR_GRADUATED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * SIX_YEAR_GRADUATED) AS RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
            {query}
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM
--(End 3)------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-30-NWCCU Carroll"
        name = "Graduation Rate (Six Year) (Disaggregated-Pell)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRate_6Year_ByRace(self):
        query = f"""
        --(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                 RACE.IPEDS_RACE_ETHNIC_DESC  AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 6, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS SIX_YEAR_GRADUATED
         FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------
                          SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                          APPL_START_TERM                                                          AS TERM,
                                          TERM_START_DATE,
                                          ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
        -------------------------------------------------------------------------------------------------------------------
                          FROM APPLICATIONS AS AP
                                   JOIN STUDENT_ACAD_CRED AS AC
                                        ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                   JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                   JOIN TERMS ON APPL_START_TERM = TERMS_ID
                          WHERE APPL_DATE IS NOT NULL
                            AND APPL_ACAD_PROGRAM != 'NDEG'
        --     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                            AND STC_STATUS IN ('A', 'N')
                            AND STC_CRED_TYPE IN ('INST')
        --(End 1)---------------------------------------------------------------------------------------------------------
                      ) AS COHORT
                          JOIN (VALUES
                                       ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                            JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON COHORT.ID = RACE.ID
                 WHERE TERM_ORDER = 1
        --(End 2)------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 3)---------------------------------------------------------------------------------
        SELECT TERM,
               CATEGORY,
               SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_SIX_YEAR_GRADUATED,
               SUM(SIX_YEAR_GRADUATED) AS SIX_YEAR_GRADUATED,
               COUNT(*) AS TOTAL,
               AVG(1.0 * SIX_YEAR_GRADUATED) AS RATE
        FROM (
        --(Begin 2)---------------------------------------------------------------------------------
            {query}
        --(End 2)------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, CATEGORY
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-30-NWCCU Carroll"
        name = "Graduation Rate (Six Year) (Disaggregated-Race)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduationRate_6Year_ByResidencyStatus(self):
        query = f"""
        --(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                CASE WHEN STATE = 'MT' THEN 'In State' ELSE 'Out of State' END AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 6, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS SIX_YEAR_GRADUATED
         FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------
                  SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                  APPL_START_TERM                                                          AS TERM,
                                  TERM_START_DATE,
                                  ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                  FROM APPLICATIONS AS AP
                           JOIN STUDENT_ACAD_CRED AS AC
                                ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                           JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                           JOIN TERMS ON APPL_START_TERM = TERMS_ID
                  WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                    AND STC_STATUS IN ('A', 'N')
                    AND STC_CRED_TYPE IN ('INST')
--(End 1)---------------------------------------------------------------------------------------------------------
              ) AS COHORT
                  JOIN (VALUES
                               ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
             JOIN (
                    SELECT ID,
                           STATE
                    FROM (SELECT ID,
                                 PAV.STATE,
                                 ROW_NUMBER() OVER (PARTITION BY ID ORDER BY ADDRESS_ADD_DATE) AS RANK
                          FROM PERSON_ADDRESSES_VIEW AS PAV
                                   JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                          WHERE ADDRESS_TYPE = 'H') AS X
                    WHERE RANK = 1
                ) AS STUDENT_STATE ON COHORT.ID = STUDENT_STATE.ID
         WHERE TERM_ORDER = 1
--(End 2)------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 3)---------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_SIX_YEAR_GRADUATED,
       SUM(SIX_YEAR_GRADUATED) AS SIX_YEAR_GRADUATED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * SIX_YEAR_GRADUATED) AS RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
        {query}
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
--(End 3)------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-06-30-NWCCU Carroll"
        name = "Graduation Rate (Six Year) (Disaggregated-Residency Status)"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    '''
    ID: Unknown
    Name: 2025-07-07-MSW Faculty-Staff Program Review
    Person: Rebecca Schwartz
    Start Date: 2025-07-07
    End Date: 2025-07-07
    Description:
        Need statistics for the MSW Faculty and Staff.
    '''

    def getFacultyStudentDemographicsByGender(self):
        query = f"""
                 SELECT DISTINCT PERSTAT.PERSTAT_HRP_ID,
                         PERSON.LAST_NAME,
                         PERSON.FIRST_NAME,
                         SEV.STUDENT_ID,
                         CASE
                             WHEN SEV.STUDENT_GENDER = 'M' THEN 'Male'
                             WHEN SEV.STUDENT_GENDER = 'F' THEN 'Female'
                             ELSE 'Unknown' END AS STUDENT_GENDER
         FROM TERMS
                  CROSS JOIN PERSTAT
                  JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                  JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                 JOIN FACULTY_SECTIONS_DETAILS_VIEW AS FS
                    ON PERSTAT.PERSTAT_HRP_ID = FS.FACULTY_ID AND TERMS.TERMS_ID = FS.CS_TERM
                    JOIN COURSE_SECTIONS_DETAILS_VIEW AS CS
                    ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
                JOIN STUDENT_ENROLLMENT_VIEW AS SEV
                    ON CS.COURSE_SECTIONS_ID = SEV.SECTION_COURSE_SECTION_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
           AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND POSITION.POS_CLASS = 'FAC'
         AND POSITION.POS_DEPT = 'SWK'
         AND SEV.ENROLL_CURRENT_STATUS IN ('New', 'Add')
         AND COALESCE(SEV.ENROLL_SCS_PASS_AUDIT, '') != 'A'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT PERSTAT_HRP_ID,
               LAST_NAME,
               FIRST_NAME,
               STUDENT_GENDER,
               COUNT(*) AS COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                 SELECT DISTINCT PERSTAT.PERSTAT_HRP_ID,
                                 PERSON.LAST_NAME,
                                 PERSON.FIRST_NAME,
                                 SEV.STUDENT_ID,
                                 CASE
                                     WHEN SEV.STUDENT_GENDER = 'M' THEN 'Male'
                                     WHEN SEV.STUDENT_GENDER = 'F' THEN 'Female'
                                     ELSE 'Unknown' END AS STUDENT_GENDER
                 FROM TERMS
                          CROSS JOIN PERSTAT
                          JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                          JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                         JOIN FACULTY_SECTIONS_DETAILS_VIEW AS FS
                            ON PERSTAT.PERSTAT_HRP_ID = FS.FACULTY_ID AND TERMS.TERMS_ID = FS.CS_TERM
                            JOIN COURSE_SECTIONS_DETAILS_VIEW AS CS
                            ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
                        JOIN STUDENT_ENROLLMENT_VIEW AS SEV
                            ON CS.COURSE_SECTIONS_ID = SEV.SECTION_COURSE_SECTION_ID
                 WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                   AND TERMS.TERM_END_DATE < '2025-06-01'
                   AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                   AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
                   AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
                   AND POSITION.POS_CLASS = 'FAC'
                 AND POSITION.POS_DEPT = 'SWK'
                 AND SEV.ENROLL_CURRENT_STATUS IN ('New', 'Add')
                 AND COALESCE(SEV.ENROLL_SCS_PASS_AUDIT, '') != 'A'
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY PERSTAT_HRP_ID, LAST_NAME, FIRST_NAME, STUDENT_GENDER
        --(End 2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-07-MSW Faculty-Staff Program Review"
        name = "Faculty Student Demographics By Gender"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getFacultyStudentDemographicByRace(self):
        query = f"""
                 SELECT DISTINCT PERSTAT.PERSTAT_HRP_ID,
                         PERSON.LAST_NAME,
                         PERSON.FIRST_NAME,
                         SEV.STUDENT_ID,
                         STUDENT_RACE.IPEDS_RACE_ETHNIC_DESC AS STUDENT_RACE
         FROM TERMS
                  CROSS JOIN PERSTAT
                  JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                  JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                  JOIN FACULTY_SECTIONS_DETAILS_VIEW AS FS
                       ON PERSTAT.PERSTAT_HRP_ID = FS.FACULTY_ID AND TERMS.TERMS_ID = FS.CS_TERM
                  JOIN COURSE_SECTIONS_DETAILS_VIEW AS CS
                       ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
                  JOIN STUDENT_ENROLLMENT_VIEW AS SEV
                       ON CS.COURSE_SECTIONS_ID = SEV.SECTION_COURSE_SECTION_ID
                  JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS STUDENT_RACE ON SEV.STUDENT_ID = STUDENT_RACE.ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
           AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND POSITION.POS_CLASS = 'FAC'
           AND POSITION.POS_DEPT = 'SWK'
           AND SEV.ENROLL_CURRENT_STATUS IN ('New', 'Add')
           AND COALESCE(SEV.ENROLL_SCS_PASS_AUDIT, '') != 'A'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
SELECT PERSTAT_HRP_ID,
       LAST_NAME,
       FIRST_NAME,
       STUDENT_RACE,
       COUNT(*) AS COUNT
FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
        {query}
--(End 1)--------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY PERSTAT_HRP_ID, LAST_NAME, FIRST_NAME, STUDENT_RACE
--(End 2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-07-MSW Faculty-Staff Program Review"
        name = "Faculty Student Demographics By Race"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getAdjunctsAndCourseLoad_2(self):
        query = f"""
                          SELECT DISTINCT TERMS.TERMS_ID         AS TERM,
                                  TERM_START_DATE,
                                  PERSTAT.PERSTAT_HRP_ID AS ID,
                                  PERSON.LAST_NAME,
                                  PERSON.FIRST_NAME,
                                  CS.COURSE_SECTIONS_ID,
                                  CS_BILLING_CREDITS     AS CREDITS
                  FROM TERMS
                           CROSS JOIN PERSTAT
                           JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                           JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                           JOIN FACULTY_SECTIONS_DETAILS_VIEW AS FS
                                ON PERSTAT.PERSTAT_HRP_ID = FS.FACULTY_ID AND TERMS.TERMS_ID = FS.CS_TERM
                           JOIN COURSE_SECTIONS_DETAILS_VIEW AS CS
                                ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
                  WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                    AND TERMS.TERM_END_DATE < '2025-06-01'
                    AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                    AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
                    AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
                    AND POSITION.POS_RANK = 'A'
                    AND POSITION.POS_DEPT = 'SWK'
                    AND CS_BILLING_CREDITS IS NOT NULL
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
         SELECT TERM,
                ID,
                LAST_NAME,
                FIRST_NAME,
                SUM(CREDITS) AS ADJUNCT_CREDIT_LOAD
         FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY TERM, ID, LAST_NAME, FIRST_NAME, TERM_START_DATE
        --(End 2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-07-MSW Faculty-Staff Program Review"
        name = "Adjuncts and Course Load"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getAvgCreditLoad(self):
        query = f"""
                          SELECT DISTINCT TERMS.TERMS_ID                           AS TERM,
                                  PERSTAT.PERSTAT_HRP_ID                   AS ID,
                                  PERSON.LAST_NAME,
                                  PERSON.FIRST_NAME,
                                  CS.COURSE_SECTIONS_ID,
                                  CS_BILLING_CREDITS AS CREDITS
                  FROM TERMS
                           CROSS JOIN PERSTAT
                           JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                           JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                           JOIN FACULTY_SECTIONS_DETAILS_VIEW AS FS
                                ON PERSTAT.PERSTAT_HRP_ID = FS.FACULTY_ID AND TERMS.TERMS_ID = FS.CS_TERM
                           JOIN COURSE_SECTIONS_DETAILS_VIEW AS CS
                                ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
                  WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                    AND TERMS.TERM_END_DATE < '2025-06-01'
                    AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                    AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
                    AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
                    AND POSITION.POS_CLASS = 'FAC'
                  AND POSITION.POS_DEPT = 'SWK'
        """
        agg = lambda query: f"""
        --(Begin 3)------------------------------------------------------------------------------------------------------------
        SELECT ID,
               LAST_NAME,
               FIRST_NAME,
               AVG(FACULTY_CREDIT_LOAD) AS AVG_CREDIT_LOAD
        FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        ID,
                        LAST_NAME,
                        FIRST_NAME,
                        SUM(CREDITS) AS FACULTY_CREDIT_LOAD
                 FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY TERM, ID, LAST_NAME, FIRST_NAME
        --(End 2)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY ID, LAST_NAME, FIRST_NAME
        --(End 3)--------------------------------------------------------------------------------------------------------------
        ORDER BY LAST_NAME, FIRST_NAME
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-07-MSW Faculty-Staff Program Review"
        name = "Average Credit Load"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getAvgEnrollmentSize(self):
        query = f"""
                          SELECT DISTINCT TERMS.TERMS_ID                           AS TERM,
                                  PERSTAT.PERSTAT_HRP_ID                   AS ID,
                                  PERSON.LAST_NAME,
                                  PERSON.FIRST_NAME,
                                  CS.COURSE_SECTIONS_ID,
                                  CS.CS_COUNT_ACTIVE_STUDENTS AS ENROLLMENT
                  FROM TERMS
                           CROSS JOIN PERSTAT
                           JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                           JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                           JOIN FACULTY_SECTIONS_DETAILS_VIEW AS FS
                                ON PERSTAT.PERSTAT_HRP_ID = FS.FACULTY_ID AND TERMS.TERMS_ID = FS.CS_TERM
                           JOIN COURSE_SECTIONS_DETAILS_VIEW AS CS
                                ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
                  WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                    AND TERMS.TERM_END_DATE < '2025-06-01'
                    AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                    AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
                    AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
                    AND POSITION.POS_CLASS = 'FAC'
                    AND POSITION.POS_DEPT = 'SWK'
        """
        agg = lambda query: f"""
        --(Begin 3)------------------------------------------------------------------------------------------------------------
        SELECT ID,
               LAST_NAME,
               FIRST_NAME,
               AVG(FACULTY_ENROLLMENT) AS AVG_FACULTY_ENROLLMENT
        FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        ID,
                        LAST_NAME,
                        FIRST_NAME,
                        SUM(ENROLLMENT) AS FACULTY_ENROLLMENT
                 FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY TERM, ID, LAST_NAME, FIRST_NAME
        --(End 2)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY ID, LAST_NAME, FIRST_NAME
        --(End 3)--------------------------------------------------------------------------------------------------------------
        ORDER BY LAST_NAME, FIRST_NAME
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-07-MSW Faculty-Staff Program Review"
        name = "Average Enrollment Size"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getStaffDemographicsByGender(self):
        query = f"""
                 SELECT DISTINCT PERSTAT.PERSTAT_HRP_ID AS ID,
                         PERSON.LAST_NAME,
                         PERSON.FIRST_NAME,
                         CASE WHEN GENDER = 'M' THEN 'Male'
                             WHEN GENDER = 'F' THEN 'Female'
                             ELSE 'Unknown' END AS GENDER
         FROM TERMS
                  CROSS JOIN PERSTAT
                  JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                  JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
           AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND (POSITION.POS_CLASS != 'FAC' OR POSITION.POS_CLASS IS NULL)
           AND (POSITION.POS_RANK != 'A' OR POSITION.POS_RANK IS NULL)
           AND (POSITION.POS_EEO_RANK != 'INS' OR POSITION.POS_EEO_RANK IS NULL)
           AND PERSTAT.PERSTAT_STATUS != 'STU'
           AND POSITION.POS_DEPT = 'SWK'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
SELECT GENDER,
       COUNT(*) AS COUNT
FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT PERSTAT.PERSTAT_HRP_ID AS ID,
                         PERSON.LAST_NAME,
                         PERSON.FIRST_NAME,
                         CASE WHEN GENDER = 'M' THEN 'Male'
                             WHEN GENDER = 'F' THEN 'Female'
                             ELSE 'Unknown' END AS GENDER
         FROM TERMS
                  CROSS JOIN PERSTAT
                  JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                  JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
           AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND (POSITION.POS_CLASS != 'FAC' OR POSITION.POS_CLASS IS NULL)
           AND (POSITION.POS_RANK != 'A' OR POSITION.POS_RANK IS NULL)
           AND (POSITION.POS_EEO_RANK != 'INS' OR POSITION.POS_EEO_RANK IS NULL)
           AND PERSTAT.PERSTAT_STATUS != 'STU'
           AND POSITION.POS_DEPT = 'SWK'
--(End 1)--------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY GENDER
--(End 2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-07-MSW Faculty-Staff Program Review"
        name = "Staff Demographics By Gender"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getStaffDemographicsByRace(self):
        query = f"""
                 SELECT DISTINCT PERSTAT.PERSTAT_HRP_ID,
                         PERSON.LAST_NAME,
                         PERSON.FIRST_NAME,
                         RACE.IPEDS_RACE_ETHNIC_DESC AS RACE
         FROM TERMS
                  CROSS JOIN PERSTAT
                  JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                  JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                  JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
           AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND (POSITION.POS_CLASS != 'FAC' OR POSITION.POS_CLASS IS NULL)
           AND (POSITION.POS_RANK != 'A' OR POSITION.POS_RANK IS NULL)
           AND (POSITION.POS_EEO_RANK != 'INS' OR POSITION.POS_EEO_RANK IS NULL)
           AND PERSTAT.PERSTAT_STATUS != 'STU'
           AND POSITION.POS_DEPT = 'SWK'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT RACE,
               COUNT(*) AS COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY RACE
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY RACE
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-07-MSW Faculty-Staff Program Review"
        name = "Staff Demographics By Race"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getStaffLoad_2(self):
        query = f"""
                 SELECT DISTINCT TERMS.TERMS_ID                                                  AS TERM,
                         TERMS.TERM_START_DATE,
                         PERSTAT.PERSTAT_HRP_ID,
                         PERSON.LAST_NAME,
                         PERSON.FIRST_NAME,
                         CASE WHEN PERSTAT.PERSTAT_STATUS = 'FT' THEN 'FT' ELSE 'PT' END AS STATUS
         FROM TERMS
                  CROSS JOIN PERSTAT
                  JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                  JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
           AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND (POSITION.POS_CLASS != 'FAC' OR POSITION.POS_CLASS IS NULL)
           AND (POSITION.POS_RANK != 'A' OR POSITION.POS_RANK IS NULL)
           AND (POSITION.POS_EEO_RANK != 'INS' OR POSITION.POS_EEO_RANK IS NULL)
           AND PERSTAT.PERSTAT_STATUS != 'STU'
           AND POSITION.POS_DEPT = 'SWK'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               STATUS,
               COUNT(*) AS COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, STATUS, TERM_START_DATE
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-07-MSW Faculty-Staff Program Review"
        name = "Staff Load"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTenureStatus_2(self):
        query = f"""
                 SELECT TERMS.TERMS_ID AS TERM,
                PERSTAT.PERSTAT_HRP_ID,
                PERSON.LAST_NAME,
                PERSON.FIRST_NAME,
                COALESCE(TENURE_STATUS.NAME, 'Unknown') AS TENURE_STATUS
         FROM TERMS
          CROSS JOIN PERSTAT
          JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
          JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
          LEFT JOIN (VALUES
            ('T', 'Tenured'), ('O', 'On Tenure Track'), ('N', 'Not Tenure Track'))
            AS TENURE_STATUS(ID, NAME) ON PERSTAT_TENURE_TYPE = TENURE_STATUS.ID
          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND POSITION.POS_CLASS = 'FAC'
          AND POSITION.POS_DEPT = 'SWK'
        """
        agg = lambda query: f"""
        --(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT TERMS.TERMS_ID AS TERM,
                PERSTAT.PERSTAT_HRP_ID,
                PERSON.LAST_NAME,
                PERSON.FIRST_NAME,
                COALESCE(TENURE_STATUS.NAME, 'Unknown') AS TENURE_STATUS
         FROM TERMS
          CROSS JOIN PERSTAT
          JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
          JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
          LEFT JOIN (VALUES
            ('T', 'Tenured'), ('O', 'On Tenure Track'), ('N', 'Not Tenure Track'))
            AS TENURE_STATUS(ID, NAME) ON PERSTAT_TENURE_TYPE = TENURE_STATUS.ID
          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND POSITION.POS_CLASS = 'FAC'
          AND POSITION.POS_DEPT = 'SWK'
        --(End 1)--------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE, LAST_NAME, FIRST_NAME
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-07-MSW Faculty-Staff Program Review"
        name = "Tenure Status"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTotalFilledFacultyPositions_2(self):
        query = f"""
                 SELECT TERMS.TERMS_ID AS TERM,
                TERM_START_DATE,
                PERSTAT.PERSTAT_HRP_ID,
                PERSON.LAST_NAME,
                PERSON.FIRST_NAME
         FROM TERMS
             CROSS JOIN PERSTAT
              JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
              JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND POSITION.POS_CLASS = 'FAC'
            AND POSITION.POS_DEPT = 'SWK'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS TOTAL_FACULTY
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                 SELECT TERMS.TERMS_ID AS TERM,
                        TERM_START_DATE,
                        PERSTAT.PERSTAT_HRP_ID,
                        PERSON.LAST_NAME,
                        PERSON.FIRST_NAME
                 FROM TERMS
                     CROSS JOIN PERSTAT
                      JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                      JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                 WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                    AND TERMS.TERM_END_DATE < '2025-06-01'
                    AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                    AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
                    AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
                   AND POSITION.POS_CLASS = 'FAC'
                    AND POSITION.POS_DEPT = 'SWK'
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-07-MSW Faculty-Staff Program Review"
        name = "Total Filled Faculty Positions"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTotalStaff_2(self):
        query = f"""
                 SELECT TERMS.TERMS_ID AS TERM,
                TERM_START_DATE,
                PERSTAT.PERSTAT_HRP_ID,
                PERSON.LAST_NAME,
                PERSON.FIRST_NAME
         FROM TERMS
             CROSS JOIN PERSTAT
              JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
              JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND (POSITION.POS_CLASS != 'FAC' OR POSITION.POS_CLASS IS NULL)
           AND (POSITION.POS_RANK != 'A' OR POSITION.POS_RANK IS NULL)
           AND (POSITION.POS_EEO_RANK != 'INS' OR POSITION.POS_EEO_RANK IS NULL)
          AND PERSTAT.PERSTAT_STATUS != 'STU'
         AND POSITION.POS_DEPT = 'SWK'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS TOTAL_ADMIN_STAFF
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-07-MSW Faculty-Staff Program Review"
        name = "Total Staff"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    '''
    ID: Unknown
    Name: 2025-07-10-FTE for Fall 2025
    Person: Rebecca Schwartz
    Start Date: 2025-07-10
    End Date: 2025-07-10
    Description:
    '''

    def getFTE_2025FA(self):
        query = f"""
                 SELECT STTR_STUDENT,
                CASE
                    WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time'
                    ELSE 'Part-Time' END AS LOAD
         FROM ODS_STUDENT_TERMS
         WHERE STTR_TERM = '2025FA'
           AND STATUS_DESC = 'Registered'
        """
        agg = lambda query: f"""
        --(Begin 2)---------------------------------------------------------------------------------------------
        SELECT COALESCE(LOAD, 'FTE') AS LOAD,
               COUNT(*) AS COUNT,
               CAST(SUM(CASE WHEN LOAD = 'Full-Time' THEN 1.0 ELSE 1.0 / 3 END) AS INT) AS WEIGHTED_COUNT
        FROM (
        --(Begin 1)---------------------------------------------------------------------------------------------
                 SELECT STTR_STUDENT,
                        CASE
                            WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time'
                            ELSE 'Part-Time' END AS LOAD
                 FROM ODS_STUDENT_TERMS
                 WHERE STTR_TERM = '2025FA'
                   AND STATUS_DESC = 'Registered'
        --(End 1)------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY LOAD WITH ROLLUP
        --(End 2)------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN ODS_PERSON P ON X.STTR_STUDENT = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-10-FTE for Fall 2025"
        name = "2025-07-10-FTE for Fall 2025"
        self.save_query_results(query, db="ODS", func_dict={"Agg": agg, "Names": names})(report, name)

    '''
    ID: Unknown
    Name: 2025-07-21-Three-Year Average of Retention and Persistence
    Person: Amy Honchell
    Start Date: 2025-07-21
    End Date: 2025-07-21
    Description:
    '''
    def getPersistence(self):
        query = f"""
        SELECT DISTINCT STC_PERSON_ID AS STUDENT_ID,
       STC_TERM AS START_TERM,
        PERSISTENCE.Y AS NEXT_TERM,
        CASE WHEN EXISTS (
            SELECT 1
            FROM STUDENT_ACAD_CRED AS STC_INNER
            LEFT JOIN STC_STATUSES AS STATUS_INNER ON STC_INNER.STUDENT_ACAD_CRED_ID = STATUS_INNER.STUDENT_ACAD_CRED_ID
                                                          AND STATUS_INNER.POS = 1
            LEFT JOIN STUDENT_COURSE_SEC AS SEC_INNER
                ON STC_INNER.STC_STUDENT_COURSE_SEC = SEC_INNER.STUDENT_COURSE_SEC_ID
            WHERE STC.STC_PERSON_ID = STC_INNER.STC_PERSON_ID
            AND STC_INNER.STC_TERM = PERSISTENCE.Y
            AND STATUS_INNER.STC_STATUS IN ('N', 'A')
            AND COALESCE(SEC_INNER.SCS_PASS_AUDIT, '') != 'A'
        ) THEN 1 ELSE 0 END AS STAYED,
       CASE
       WHEN EXISTS (SELECT 1
                    FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                    WHERE SAPV.STUDENT_ID = STC.STC_PERSON_ID
                      AND STP_CURRENT_STATUS = 'Graduated'
                      AND (STP_END_DATE > TERMS.TERM_START_DATE OR STP_END_DATE IS NULL))
           THEN 1
       ELSE 0 END AS GRADUATED

        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN (VALUES ('2022FA', '2023SP'),
                     ('2023FA', '2024SP'),
                     ('2024FA', '2025SP')) AS PERSISTENCE(X, Y) ON STC.STC_TERM = X
        JOIN TERMS ON STC.STC_TERM = TERMS_ID
        WHERE STATUS.STC_STATUS IN ('N', 'A')
        AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
        """
        agg = lambda query: f"""
        --(Begin 4)------------------------------------------------------------------------------------------------------
        SELECT AVG(PERSISTENCE_RATE) AS THREE_YEAR_AVG_PERSISTENCE_RATE
        FROM (
        --(Begin 3)------------------------------------------------------------------------------------------------------
                 SELECT PERIOD,
                        AVG(1.0 * PERSISTED) AS PERSISTENCE_RATE
                 FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------
                          SELECT STUDENT_ID,
                                 START_TERM + '-' + NEXT_TERM                            AS PERIOD,
                                 CASE WHEN STAYED = 1 OR GRADUATED = 1 THEN 1 ELSE 0 END AS PERSISTED
                          FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
                               ) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY PERIOD
        --(End 3)-------------------------------------------------------------------------------------------------------
             ) AS X
        --(End 4)-------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-21-Three-Year Average of Retention and Persistence"
        name = "Persistence"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getRetention(self):
        query = f"""
        SELECT DISTINCT STC_PERSON_ID AS STUDENT_ID,
       STC_TERM AS START_TERM,
        PERSISTENCE.Y AS NEXT_TERM,
        CASE WHEN EXISTS (
            SELECT 1
            FROM STUDENT_ACAD_CRED AS STC_INNER
            LEFT JOIN STC_STATUSES AS STATUS_INNER ON STC_INNER.STUDENT_ACAD_CRED_ID = STATUS_INNER.STUDENT_ACAD_CRED_ID
                                                          AND STATUS_INNER.POS = 1
            LEFT JOIN STUDENT_COURSE_SEC AS SEC_INNER
                ON STC_INNER.STC_STUDENT_COURSE_SEC = SEC_INNER.STUDENT_COURSE_SEC_ID
            WHERE STC.STC_PERSON_ID = STC_INNER.STC_PERSON_ID
            AND STC_INNER.STC_TERM = PERSISTENCE.Y
            AND STATUS_INNER.STC_STATUS IN ('N', 'A')
            AND COALESCE(SEC_INNER.SCS_PASS_AUDIT, '') != 'A'
        ) THEN 1 ELSE 0 END AS STAYED,
       CASE
       WHEN EXISTS (SELECT 1
                    FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                    WHERE SAPV.STUDENT_ID = STC.STC_PERSON_ID
                      AND STP_CURRENT_STATUS = 'Graduated'
                      AND (STP_END_DATE > TERMS.TERM_START_DATE OR STP_END_DATE IS NULL))
           THEN 1
       ELSE 0 END AS GRADUATED

FROM STUDENT_ACAD_CRED AS STC
LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
JOIN (VALUES ('2021FA', '2022FA'),
             ('2022FA', '2023FA'),
             ('2023FA', '2024FA')) AS PERSISTENCE(X, Y) ON STC.STC_TERM = X
JOIN TERMS ON STC.STC_TERM = TERMS_ID
WHERE STATUS.STC_STATUS IN ('N', 'A')
AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
        """
        agg = lambda query: f"""
        --(Begin 4)------------------------------------------------------------------------------------------------------
        SELECT AVG(RETENTION_RATE) AS THREE_YEAR_AVG_RETENTION_RATE
        FROM (
        --(Begin 3)------------------------------------------------------------------------------------------------------
                 SELECT PERIOD,
                        AVG(1.0 * RETAINED) AS RETENTION_RATE
                 FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------
                          SELECT STUDENT_ID,
                                 START_TERM + '-' + NEXT_TERM                            AS PERIOD,
                                 CASE WHEN STAYED = 1 OR GRADUATED = 1 THEN 1 ELSE 0 END AS RETAINED
                          FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
                               ) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY PERIOD
        --(End 3)-------------------------------------------------------------------------------------------------------
             ) AS X
        --(End 4)-------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-21-Three-Year Average of Retention and Persistence"
        name = "Retention"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    '''
    ID: Unknown
    Name: 2025-07-29-FISAP
    Person: Rebecca Schwartz
    Start Date: 2025-07-29
    End Date: 2025-07-29
    Description
    '''

    def getUnduplicatedHeadcount(self):
        query = f"""
                 SELECT DISTINCT LEFT(STC_STUDENT_ACAD_LEVELS_ID, 7) AS STUDENT_ID,
                         SPT_STUDENT_ACAD_CRED.ACAD_LEVEL_DESC AS ACAD_LEVEL
         FROM SPT_STUDENT_ACAD_CRED
         WHERE STC_START_DATE >= '2024-07-01'
           AND STC_END_DATE < '2025-07-01'
           AND STC_CRED_TYPE = 'INST'
           AND CURRENT_STATUS_DESC IN ('New', 'Add')
           AND STC_GRADE != 'Audit'
           AND STC_CRED > 0
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT ACAD_LEVEL,
               COUNT(*) AS UNDUPLICATED_HEADCOUNT
        FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
                    {query}
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY ACAD_LEVEL
        --(End 2)---------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN ODS_PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-29-FISAP"
        name = "Unduplicated Headcount"
        self.save_query_results(query, db="ODS", func_dict={"Agg": agg, "Names": names})(report, name)


    '''
    ID: Unknown
    Name: 2025-07-29-Summer Enrollments
    Person: Rebecca Schwartz
    Start Date: 2025-07-29
    End Date: 2025-07-29
    Description:
    '''

    def getSummerEnrollments(self):
        query = f"""
                 SELECT
                DISTINCT COURSES.CRS_NAME AS COURSE,
                STC_TERM AS TERM,
                STC_PERSON_ID
         FROM STUDENT_ACAD_CRED AS STC
                  LEFT JOIN STC_STATUSES AS STATUS
                            ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                  LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                    LEFT JOIN COURSES ON STC.STC_COURSE = COURSES_ID
         WHERE STATUS.STC_STATUS IN ('N', 'A')
           AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
           AND STC_CRED_TYPE = 'INST'
           AND STC_START_DATE BETWEEN DATEADD(YEAR, -5, '2025-01-01') AND '2025-01-01'
           AND STC_TERM LIKE '%SU'
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT COURSE,
               TERM,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
                 SELECT
                        DISTINCT COURSES.CRS_NAME AS COURSE,
                        STC_TERM AS TERM,
                        STC_PERSON_ID
                 FROM STUDENT_ACAD_CRED AS STC
                          LEFT JOIN STC_STATUSES AS STATUS
                                    ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                          LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                            LEFT JOIN COURSES ON STC.STC_COURSE = COURSES_ID
                 WHERE STATUS.STC_STATUS IN ('N', 'A')
                   AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
                   AND STC_CRED_TYPE = 'INST'
                   AND STC_START_DATE BETWEEN DATEADD(YEAR, -5, '2025-01-01') AND '2025-01-01'
                   AND STC_TERM LIKE '%SU'
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY COURSE, TERM
        --(End 2)---------------------------------------------------------------------------------------------------------------
        ORDER BY COURSE, TERM
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STC_PERSON_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-07-29-Summer Enrollments"
        name = "Summer Enrollments"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    '''
    ID: Unknown
    Name: 2025-08-01-FTE for Global Music Rights
    Person: Rebecca Schwartz
    Start Date: 2025-08-01
    End Date: 2025-08-01
    Description:
    '''
    def getFTE(self):
        query = f"""
              SELECT DISTINCT STC_PERSON_ID                                                                       AS ID,
                      STC_ACAD_LEVEL                                                                      AS LEVEL,
                      CASE
                          WHEN STV.STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time'
                          ELSE 'Part-Time' END                                                            AS LOAD
      FROM STUDENT_ACAD_CRED AS STC
               LEFT JOIN STC_STATUSES AS STATUS
                         ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
               LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
               LEFT JOIN STUDENT_TERMS_VIEW AS STV
                         ON STC.STC_PERSON_ID = STV.STTR_STUDENT AND STC.STC_TERM = STV.STTR_TERM AND
                            STC.STC_ACAD_LEVEL = STV.STTR_ACAD_LEVEL
      WHERE STATUS.STC_STATUS IN ('N', 'A')
        AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
        AND STC.STC_TERM = '2024FA'
        """
        agg = lambda query: f"""
        --(Begin 3)-------------------------------------------------------------------------------------------------------------
        SELECT CAST(SUM(WEIGHT) AS INT) AS FTE
        FROM (
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
                 SELECT DISTINCT ID,
                                 CASE
                                     WHEN LEVEL = 'UG' AND LOAD = 'Full-Time' THEN 1.0
                                     WHEN LEVEL = 'GR' OR LOAD = 'Part-Time' THEN 1.0 / 3 END AS WEIGHT
                 FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)---------------------------------------------------------------------------------------------------------------
                      ) AS X
        --(End 2)---------------------------------------------------------------------------------------------------------------
             ) AS X
        --(End 3)---------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STC_PERSON_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-01-FTE for Global Music Rights"
        name = "FTE"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getStudentCountsByType(self):
        query = f"""
        --(Begin C1)-------------------------------------------------------------------------------------------------------------
                  SELECT DISTINCT STC_PERSON_ID                      AS STUDENT_ID,
                                  CASE
                                      WHEN STUDENT_CURRENT_TYPE = 'ACE' THEN 'High School'
                                      WHEN STUDENT_CURRENT_TYPE = 'SC' THEN 'Senior Citizen'
                                      WHEN STUDENT_CURRENT_TYPE = 'UG' AND PROGRAM = 'Non-Degree Seeking Students'
                                          THEN 'Non-Degree UG'
                                      WHEN STUDENT_CURRENT_TYPE = 'PB' THEN 'Post-Bacc'
                                      WHEN STUDENT_CURRENT_TYPE = 'ACNU' THEN 'Accelerated Nursing'
                                      WHEN STC_ACAD_LEVEL = 'GR' THEN PROGRAM
                                      WHEN STC_ACAD_LEVEL = 'UG' THEN 'Undergrad'
                                      END                            AS TYPE,
                                  CASE
                                      WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time or Over'
                                      ELSE 'Less Than Full-Time' END AS LOAD

                  FROM STUDENT_ACAD_CRED AS STC
                           LEFT JOIN STC_STATUSES AS STATUS
                                     ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
                           LEFT JOIN STUDENT_TERMS
                                     ON STUDENT_TERMS.STUDENT_TERMS_ID =
                                        STC_PERSON_ID + '*' + STC_TERM + '*' + STC_ACAD_LEVEL
                           LEFT JOIN (
                    --(Begin A2)-------------------------------------------------------------------------------------------------------------
                                          SELECT STUDENTS_ID AS ID,
                                                 STU_TYPES   AS STUDENT_CURRENT_TYPE
                                          FROM (
                    --(Begin A1)-------------------------------------------------------------------------------------------------------------
                                                   SELECT STUDENTS_ID,
                                                          STU_TYPES,
                                                          ROW_NUMBER() OVER (PARTITION BY STUDENTS_ID ORDER BY STU_TYPE_DATES DESC) AS RANK
                                                   FROM STU_TYPE_INFO
                    --(End A1)---------------------------------------------------------------------------------------------------------------
                                               ) AS X
                                          WHERE RANK = 1
                    --(End A2)---------------------------------------------------------------------------------------------------------------
                                      ) AS STUDENT_TYPES ON STC.STC_PERSON_ID = STUDENT_TYPES.ID
                                               LEFT JOIN (
                    --(Begin B2)------------------------------------------------------------------------------------------------------------
                                          SELECT *
                                          FROM (
                    --(Begin B1)------------------------------------------------------------------------------------------------------------
                                                   SELECT STUDENT_ID,
                                                          STP_PROGRAM_TITLE                                                                 AS PROGRAM,
                                                          STP_CURRENT_STATUS,
                                                          ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                                                              ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS PROGRAM_RANK
                                                   FROM STUDENT_ACAD_PROGRAMS_VIEW
                                                   WHERE STP_START_DATE <=
                                                         (SELECT TOP 1 TERMS.TERM_END_DATE
                                                          FROM TERMS
                                                          WHERE TERMS_ID = '2024FA')
                    --(End B1)---------------------------------------------------------------------------------------------------------------
                                               ) AS X
                                          WHERE PROGRAM_RANK = 1
                    --(End B2)---------------------------------------------------------------------------------------------------------------
                                      ) AS SAPV
                                                         ON STC.STC_PERSON_ID = SAPV.STUDENT_ID
                                      WHERE STC_TERM = '2024FA'
                                        AND STATUS.STC_STATUS IN ('N', 'A')
                                        AND STC_CRED_TYPE = 'INST'
                    --(End C1)---------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin C3)-------------------------------------------------------------------------------------------------------------
SELECT X.TYPE,
       [Less Than Full-Time],
        [Full-Time or Over],
        [Total]
FROM (
--(Begin C2)-------------------------------------------------------------------------------------------------------------
         SELECT TYPE,
                [Less Than Full-Time],
                [Full-Time or Over],
                [Less Than Full-Time] + [Full-Time or Over] as [Total]
         FROM (
--(Begin C1)-------------------------------------------------------------------------------------------------------------
            {query}
--(End C1)---------------------------------------------------------------------------------------------------------------
              ) AS X
                  PIVOT (COUNT(STUDENT_ID) FOR LOAD IN (
                 [Less Than Full-Time],
                 [Full-Time or Over]
                 )) AS X
--(End C2)---------------------------------------------------------------------------------------------------------------
     ) AS X
JOIN (VALUES ('High School', 1),
             ('Senior Citizen', 2),
             ('Non-Degree UG', 3),
             ('Post-Bacc', 4),
             ('Accelerated Nursing', 5),
             ('Master of Social Work', 6),
             ('Undergrad', 7)
) AS TYPE_ORDER(TYPE, N) ON X.TYPE = TYPE_ORDER.TYPE
--(End C3)---------------------------------------------------------------------------------------------------------------
ORDER BY TYPE_ORDER.N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-01-FTE for Global Music Rights"
        name = "Student Counts"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    '''
    ID: Unknown
    Name: 2025-08-05-AY 23-24 Headcounts
    Person: Rebecca Schwartz
    Start Date: 2025-08-05
    End Date: 2025-08-05
    '''

    def getGraduateFTHeadcount(self):
        query = f"""
                 SELECT DISTINCT STC_TERM          AS TERM,
                         TERM_START_DATE,
                         STC.STC_PERSON_ID AS ID
         FROM STUDENT_ACAD_CRED AS STC
                  LEFT JOIN STC_STATUSES AS STATUS
                            ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                  LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  LEFT JOIN STUDENT_TERMS
                            ON STUDENT_TERMS_ID = STC.STC_PERSON_ID + '*' + STC.STC_TERM + '*' + STC.STC_ACAD_LEVEL
                  LEFT JOIN TERMS ON STC_TERM = TERMS_ID
         WHERE STC_TERM IN ('2023FA', '2024SP', '2024SU')
           AND STATUS.STC_STATUS IN ('N', 'A')
           AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
           AND STC.STC_CRED > 0
           AND STC.STC_CRED_TYPE = 'INST'
           AND STC.STC_ACAD_LEVEL = 'GR'
           AND STUDENT_TERMS.STTR_STUDENT_LOAD IN ('F', 'O')
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS [Graduate FT Headcount]
        FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)---------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-05-AY 23-24 Headcounts"
        name = "Graduate FT Headcount"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduateFTE(self):
        query = f"""
                 SELECT DISTINCT STC_TERM                                                                        AS TERM,
                         TERM_START_DATE,
                         STC.STC_PERSON_ID                                                               AS ID,
                         CASE WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 1.0 ELSE 1.0/3 END AS WEIGHT
         FROM STUDENT_ACAD_CRED AS STC
                  LEFT JOIN STC_STATUSES AS STATUS
                            ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                  LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  LEFT JOIN STUDENT_TERMS
                            ON STUDENT_TERMS_ID = STC.STC_PERSON_ID + '*' + STC.STC_TERM + '*' + STC.STC_ACAD_LEVEL
         LEFT JOIN TERMS ON STC_TERM = TERMS_ID
         WHERE STC_TERM IN ('2023FA', '2024SP', '2024SU')
           AND STATUS.STC_STATUS IN ('N', 'A')
           AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
           AND STC.STC_CRED > 0
           AND STC.STC_CRED_TYPE = 'INST'
            AND STC.STC_ACAD_LEVEL = 'GR'
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               CAST(ROUND(SUM(WEIGHT), 0) AS INT) AS [Graduate Full-Time-Equivalent]
        FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)---------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-05-AY 23-24 Headcounts"
        name = "Graduate FTE"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getGraduatePTHeadcount(self):
        query = f"""
                 SELECT DISTINCT STC_TERM          AS TERM,
                         TERM_START_DATE,
                         STC.STC_PERSON_ID AS ID
         FROM STUDENT_ACAD_CRED AS STC
                  LEFT JOIN STC_STATUSES AS STATUS
                            ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                  LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  LEFT JOIN STUDENT_TERMS
                            ON STUDENT_TERMS_ID = STC.STC_PERSON_ID + '*' + STC.STC_TERM + '*' + STC.STC_ACAD_LEVEL
                  LEFT JOIN TERMS ON STC_TERM = TERMS_ID
         WHERE STC_TERM IN ('2023FA', '2024SP', '2024SU')
           AND STATUS.STC_STATUS IN ('N', 'A')
           AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
           AND STC.STC_CRED > 0
           AND STC.STC_CRED_TYPE = 'INST'
           AND STC.STC_ACAD_LEVEL = 'GR'
           AND STUDENT_TERMS.STTR_STUDENT_LOAD NOT IN ('F', 'O')
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT TERM,
       COUNT(*) AS [Graduate PT Headcount]
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
        {query}
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, TERM_START_DATE
--(End 2)---------------------------------------------------------------------------------------------------------------
ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-05-AY 23-24 Headcounts"
        name = "Graduate PT Headcount"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTotalFTE(self):
        query = f"""
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT STC_TERM                                                                        AS TERM,
                         TERM_START_DATE,
                         STC.STC_PERSON_ID                                                               AS ID,
                         CASE WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 1.0 ELSE 1.0/3 END AS WEIGHT
         FROM STUDENT_ACAD_CRED AS STC
                  LEFT JOIN STC_STATUSES AS STATUS
                            ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                  LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  LEFT JOIN STUDENT_TERMS
                            ON STUDENT_TERMS_ID = STC.STC_PERSON_ID + '*' + STC.STC_TERM + '*' + STC.STC_ACAD_LEVEL
         LEFT JOIN TERMS ON STC_TERM = TERMS_ID
         WHERE STC_TERM IN ('2023FA', '2024SP', '2024SU')
           AND STATUS.STC_STATUS IN ('N', 'A')
           AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
           AND STC.STC_CRED > 0
           AND STC.STC_CRED_TYPE = 'INST'
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               CAST(ROUND(SUM(WEIGHT), 0) AS INT) AS [Total Full-Time-Equivalent]
        FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)---------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-05-AY 23-24 Headcounts"
        name = "Total FTE"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getTotalHeadcount(self):
        query = f"""
        SELECT COUNT(DISTINCT STC.STC_PERSON_ID) AS [Unduplicated Student Count]
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        WHERE STC_TERM IN ('2023FA', '2024SP', '2024SU')
        AND STATUS.STC_STATUS IN ('N', 'A')
        AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
        AND STC.STC_CRED > 0
        AND STC.STC_CRED_TYPE = 'INST'
        """
        report = "2025-08-05-AY 23-24 Headcounts"
        name = "Total Headcount"
        self.save_query_results(query, snapshot_term="2025SP", func_dict=None)(report, name)

    def getUGFTHeadcount(self):
        query = f"""
                 SELECT DISTINCT STC_TERM          AS TERM,
                         TERM_START_DATE,
                         STC.STC_PERSON_ID AS ID
         FROM STUDENT_ACAD_CRED AS STC
                  LEFT JOIN STC_STATUSES AS STATUS
                            ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                  LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  LEFT JOIN STUDENT_TERMS
                            ON STUDENT_TERMS_ID = STC.STC_PERSON_ID + '*' + STC.STC_TERM + '*' + STC.STC_ACAD_LEVEL
                  LEFT JOIN TERMS ON STC_TERM = TERMS_ID
         WHERE STC_TERM IN ('2023FA', '2024SP', '2024SU')
           AND STATUS.STC_STATUS IN ('N', 'A')
           AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
           AND STC.STC_CRED > 0
           AND STC.STC_CRED_TYPE = 'INST'
           AND STC.STC_ACAD_LEVEL = 'UG'
           AND STUDENT_TERMS.STTR_STUDENT_LOAD IN ('F', 'O')
        """
        agg = lambda query: f"""
            --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS [Undergraduate FT Headcount]
        FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)---------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-05-AY 23-24 Headcounts"
        name = "Undergraduate FT Headcount"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getUGPTHeadcount(self):
        query = f"""
                 SELECT DISTINCT STC_TERM          AS TERM,
                         TERM_START_DATE,
                         STC.STC_PERSON_ID AS ID
         FROM STUDENT_ACAD_CRED AS STC
                  LEFT JOIN STC_STATUSES AS STATUS
                            ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                  LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  LEFT JOIN STUDENT_TERMS
                            ON STUDENT_TERMS_ID = STC.STC_PERSON_ID + '*' + STC.STC_TERM + '*' + STC.STC_ACAD_LEVEL
                  LEFT JOIN TERMS ON STC_TERM = TERMS_ID
         WHERE STC_TERM IN ('2023FA', '2024SP', '2024SU')
           AND STATUS.STC_STATUS IN ('N', 'A')
           AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
           AND STC.STC_CRED > 0
           AND STC.STC_CRED_TYPE = 'INST'
           AND STC.STC_ACAD_LEVEL = 'UG'
           AND STUDENT_TERMS.STTR_STUDENT_LOAD NOT IN ('F', 'O')
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS [Undergraduate PT Headcount]
        FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)---------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-05-AY 23-24 Headcounts"
        name = "Undergraduate PT Headcount"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    def getUGFTE(self):
        query = f"""
                 SELECT DISTINCT STC_TERM                                                                        AS TERM,
                         TERM_START_DATE,
                         STC.STC_PERSON_ID                                                               AS ID,
                         CASE WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 1.0 ELSE 1.0/3 END AS WEIGHT
         FROM STUDENT_ACAD_CRED AS STC
                  LEFT JOIN STC_STATUSES AS STATUS
                            ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                  LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  LEFT JOIN STUDENT_TERMS
                            ON STUDENT_TERMS_ID = STC.STC_PERSON_ID + '*' + STC.STC_TERM + '*' + STC.STC_ACAD_LEVEL
         LEFT JOIN TERMS ON STC_TERM = TERMS_ID
         WHERE STC_TERM IN ('2023FA', '2024SP', '2024SU')
           AND STATUS.STC_STATUS IN ('N', 'A')
           AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
           AND STC.STC_CRED > 0
           AND STC.STC_CRED_TYPE = 'INST'
            AND STC.STC_ACAD_LEVEL = 'UG'
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               CAST(ROUND(SUM(WEIGHT), 0) AS INT) AS [Undergraduate Full-Time-Equivalent]
        FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)---------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-05-AY 23-24 Headcounts"
        name = "Undergraduate FTE"
        self.save_query_results(query, snapshot_term="2025SP", func_dict={"Agg": agg, "Names": names})(report, name)

    '''
    ID: Unknown
    Name: 2025-08-13-Top Enrollment Numbers
    Person: Amy Honchell
    Start Date: 2025-08-13
    End Date: 2025-08-13
    Description:
    '''

    def getTopEnrollmentNumbers(self):
        query = f"""
                 SELECT DISTINCT AC.STC_PERSON_ID AS ID,
                         STUDENT_MAJORS.MAJOR
         FROM SPT_STUDENT_ACAD_CRED AS AC
                  LEFT JOIN SPT_STUDENT_COURSE_SEC AS SEC ON AC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  JOIN SPT_STUDENT_PROGRAMS AS SP ON AC.STC_PERSON_ID = SP.STPR_STUDENT
                  JOIN (SELECT STUDENT_PROGRAMS_ID AS ID,
                               MAJOR_DESC          AS MAJOR
                        FROM SPT_STUDENT_PROGRAM_MAJORS
                        UNION
                        SELECT STUDENT_PROGRAMS_ID,
                               ADDNL_MAJOR_DESC
                        FROM SPT_STU_PROG_ADDNL_MAJORS
                        WHERE COALESCE(STPR_ADDNL_MAJOR_END_DATE, GETDATE()) >= GETDATE()) AS STUDENT_MAJORS
                       ON SP.STUDENT_PROGRAMS_ID = ID
         WHERE AC.CURRENT_STATUS_DESC IN ('New', 'Add')
           AND STC_TERM = '2025FA'
           AND STC_CRED_TYPE = 'INST'
           AND COALESCE(SEC.Z01_SCS_PASS_AUDIT, '') != 'A'
           AND SP.CURRENT_STATUS_DESC = 'Active'
        """
        agg = lambda query: f"""
        --(Begin 2)---------------------------------------------------------------------------------------------------------
SELECT TOP 9
       MAJOR,
       COUNT(*) AS STUDENT_COUNT
FROM (
--(Begin 1)---------------------------------------------------------------------------------------------------------
        {query}
--(End 1)----------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY MAJOR
--(End 2)----------------------------------------------------------------------------------------------------------
ORDER BY STUDENT_COUNT DESC
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN ODS_PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-13-Top Enrollment Numbers"
        name = "Top Enrollment Numbers"
        self.save_query_results(query, db="ODS", func_dict={"Agg": agg, "Names": names})(report, name)


    '''
    ID: Unknown
    Name: 2025-08-15-FVT-GE
    Person: Rebecca Schwartz
    Start Date: 2025-08-15
    End Date: 2025-08-15
    Description:
    '''
    #===================================================================================================================
    '''
    Code is in another file.
    '''
    # ===================================================================================================================

    '''
    ID: Unknown
    Name: 2025-08-20-All 2025FA Students For Gaming Events
    Person: Charles Gross
    Start Date: 2025-08-20
    End Date: 2025-08-20
    Description:
    '''

    def get2025FAStudents(self):
        query = f"""
--(Begin 1)-------------------------------------------------------------------------------------------------------------
SELECT DISTINCT ID,
       FIRST_NAME,
       LAST_NAME
FROM SPT_STUDENT_ACAD_CRED STC
JOIN ODS_PERSON PERSON ON STC.STC_PERSON_ID = PERSON.ID
WHERE STC_TERM = '2025FA'
AND CURRENT_STATUS_DESC IN ('New', 'Add')
AND STC_CRED_TYPE = 'INST'
--(End 1)---------------------------------------------------------------------------------------------------------------
ORDER BY LAST_NAME
        """
        report = "2025-08-20-All 2025FA Students For Gaming Events"
        name = "Top Enrollment Numbers"
        self.save_query_results(query, db="ODS", func_dict=None)(report, name)

    '''
    ID: Unknown
    Name: 2025-08-20-First Day Numbers
    Person: Rebecca Schwartz
    Start Date: 2025-08-20
    End Date: 2025-08-20
    Description:
    '''

    def getAcceleratedNursingList(self):
        query = f"""
        --(Begin C1)-------------------------------------------------------------------------------------------------------------
        SELECT  TABLE_1.*,
                TABLE_2.PROGRAM,
                TABLE_2.MAJOR_OR_MINOR,
                TABLE_2.TYPE
        FROM (
        --(Begin A1)-------------------------------------------------------------------------------------------------------------
                 SELECT DISTINCT STC_PERSON_ID                 AS ID,
                                 FIRST_NAME,
                                 LAST_NAME,
                                 ST.STTR_STUDENT_LOAD          AS LOAD,
                                 COALESCE(STT_DESC, 'Unknown') AS STUDENT_TYPE,
                                 ACADEMIC_LEVEL_DESC           AS ACADEMIC_LEVEL,
                                 STATUS_DESC                   AS TERM_STATUS
                 FROM SPT_STUDENT_ACAD_CRED AS STC
                          JOIN ODS_PERSON ON STC.STC_PERSON_ID = ODS_PERSON.ID
                          JOIN ODS_STUDENT_TERMS AS ST
                               ON STC.STC_PERSON_ID + '*' + STC.STC_TERM + '*' + STC.STC_ACAD_LEVEL = STUDENT_TERMS_ID
                          LEFT JOIN (SELECT STUDENTS_ID,
                                            STU_TYPES,
                                            ROW_NUMBER() OVER (PARTITION BY STUDENTS_ID ORDER BY STU_TYPE_DATES DESC) AS RANK
                                     FROM Z01_STU_TYPE_INFO) AS Z01_STU_TYPE_INFO ON STC_PERSON_ID = STUDENTS_ID AND RANK = 1
                          LEFT JOIN Z01_STUDENT_TYPES ON Z01_STU_TYPE_INFO.STU_TYPES = Z01_STUDENT_TYPES.STUDENT_TYPES_ID
                 WHERE STC_TERM = '2025FA'
                   AND STC_CRED_TYPE = 'INST'
        --(End A1)---------------------------------------------------------------------------------------------------------------
             ) AS TABLE_1
        LEFT JOIN (
        --(Begin B1)------------------------------------------------------------------------------------------------------------
                 SELECT DISTINCT AC.STC_PERSON_ID AS ID,
                                 FIRST_NAME,
                                 LAST_NAME,
                                 SP.STPR_ACAD_PROGRAM AS PROGRAM,
                                 STUDENT_MAJORS_MINORS.MAJOR_OR_MINOR,
                                 STUDENT_MAJORS_MINORS.TYPE
                 FROM SPT_STUDENT_ACAD_CRED AS AC
                     JOIN ODS_PERSON ON AC.STC_PERSON_ID = ODS_PERSON.ID
                          LEFT JOIN SPT_STUDENT_COURSE_SEC AS SEC ON AC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                          JOIN SPT_STUDENT_PROGRAMS AS SP ON AC.STC_PERSON_ID = SP.STPR_STUDENT
                          JOIN (SELECT STUDENT_PROGRAMS_ID AS ID,
                                       MAJOR_DESC         AS MAJOR_OR_MINOR,
                                       'Program Major' AS TYPE
                                FROM SPT_STUDENT_PROGRAM_MAJORS
                                WHERE MAJOR_DESC IS NOT NULL
                                UNION
                                SELECT STUDENT_PROGRAMS_ID,
                                       ADDNL_MAJOR_DESC,
                                       'Additional Major'
                                FROM SPT_STU_PROG_ADDNL_MAJORS
                                WHERE COALESCE(STPR_ADDNL_MAJOR_END_DATE, GETDATE()) >= GETDATE()
                                UNION
                                SELECT STUDENT_PROGRAMS_ID,
                                       ADDNL_MINOR_DESC,
                                       'Minor'
                                FROM SPT_STU_PROG_ADDNL_MINORS
                                WHERE COALESCE(STPR_MINOR_END_DATE, GETDATE()) >= GETDATE()
                                ) AS STUDENT_MAJORS_MINORS
                               ON SP.STUDENT_PROGRAMS_ID = STUDENT_MAJORS_MINORS.ID
                 WHERE AC.CURRENT_STATUS_DESC IN ('New', 'Add')
                   AND STC_TERM = '2025FA'
                   AND STC_CRED_TYPE = 'INST'
                   AND COALESCE(SEC.Z01_SCS_PASS_AUDIT, '') != 'A'
                   AND SP.CURRENT_STATUS_DESC = 'Active'
        --(End B1)--------------------------------------------------------------------------------------------------------------
        ) AS TABLE_2 ON TABLE_1.ID = TABLE_2.ID
        WHERE PROGRAM = 'ANUR.BS'
        --(End C1)---------------------------------------------------------------------------------------------------------------
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-20-First Day Numbers"
        name = "Accelerated Nursing"
        self.save_query_results(query, db="ODS", func_dict=None)(report, name)

    def getStudentMajorsAndMinors(self):
        query = f"""
        --(Begin 1)---------------------------------------------------------------------------------------------------------
         SELECT DISTINCT AC.STC_PERSON_ID AS ID,
                         FIRST_NAME,
                         LAST_NAME,
                         SP.STPR_ACAD_PROGRAM AS PROGRAM,
                         STUDENT_MAJORS_MINORS.MAJOR_OR_MINOR,
                         STUDENT_MAJORS_MINORS.TYPE
         FROM SPT_STUDENT_ACAD_CRED AS AC
             JOIN ODS_PERSON ON AC.STC_PERSON_ID = ODS_PERSON.ID
                  LEFT JOIN SPT_STUDENT_COURSE_SEC AS SEC ON AC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  JOIN SPT_STUDENT_PROGRAMS AS SP ON AC.STC_PERSON_ID = SP.STPR_STUDENT
                  JOIN (SELECT STUDENT_PROGRAMS_ID AS ID,
                               MAJOR_DESC         AS MAJOR_OR_MINOR,
                               'Program Major' AS TYPE
                        FROM SPT_STUDENT_PROGRAM_MAJORS
                        WHERE MAJOR_DESC IS NOT NULL
                        UNION
                        SELECT STUDENT_PROGRAMS_ID,
                               ADDNL_MAJOR_DESC,
                               'Additional Major'
                        FROM SPT_STU_PROG_ADDNL_MAJORS
                        WHERE COALESCE(STPR_ADDNL_MAJOR_END_DATE, GETDATE()) >= GETDATE()
                        UNION
                        SELECT STUDENT_PROGRAMS_ID,
                               ADDNL_MINOR_DESC,
                               'Minor'
                        FROM SPT_STU_PROG_ADDNL_MINORS
                        WHERE COALESCE(STPR_MINOR_END_DATE, GETDATE()) >= GETDATE()
                        ) AS STUDENT_MAJORS_MINORS
                       ON SP.STUDENT_PROGRAMS_ID = STUDENT_MAJORS_MINORS.ID
         WHERE AC.CURRENT_STATUS_DESC IN ('New', 'Add')
           AND STC_TERM = '2025FA'
           AND STC_CRED_TYPE = 'INST'
           AND COALESCE(SEC.Z01_SCS_PASS_AUDIT, '') != 'A'
           AND SP.CURRENT_STATUS_DESC = 'Active'
--(End 1)----------------------------------------------------------------------------------------------------------
ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-20-First Day Numbers"
        name = "Student Majors and Minors"
        self.save_query_results(query, db="ODS", func_dict=None)(report, name)

    '''
    ID: Unknown
    Name: 2025-08-21-New Fall 2025 and Summer 2025 By Student and Acad Level
    Person: Rebecca Schwartz
    Start Date: 2025-08-21
    End Date: 2025-08-21
    Description:
    '''

    def getNew2025FA2025SU_StudentAcadLevel(self):
        query = f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
         SELECT X.ID,
                FIRST_NAME,
                LAST_NAME,
                LEVEL,
                TERM
         FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
                  SELECT APPL_APPLICANT                                                           AS ID,
                         ACAD_PR.ACADEMIC_LEVEL_DESC                                              AS LEVEL,
                         APPL_START_TERM                                                          AS TERM,
                         ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT, ACADEMIC_LEVEL_DESC ORDER BY TERM_START_DATE) AS RANK
                  FROM Z01_APPLICATIONS AS AP
                      JOIN ODS_ACAD_PROGRAMS AS ACAD_PR ON AP.APPL_ACAD_PROGRAM = ACAD_PR.ACAD_PROGRAMS_ID
                       JOIN SPT_STUDENT_ACAD_CRED AS STC
                        ON AP.APPL_APPLICANT = STC.STC_PERSON_ID AND AP.APPL_START_TERM = STC.STC_TERM
                           JOIN ODS_TERMS ON APPL_START_TERM = TERMS_ID
                  WHERE STC_CURRENT_STATUS IN ('N', 'A')
                    AND STC_CRED_TYPE = 'INST'
                    AND APPL_START_TERM IS NOT NULL
--(End 1)---------------------------------------------------------------------------------------------------------------
              ) AS X
         JOIN ODS_PERSON ON X.ID = ODS_PERSON.ID
         WHERE RANK = 1
        AND TERM IN ('2025FA', '2025SU')
--(End 2)---------------------------------------------------------------------------------------------------------------
ORDER BY LAST_NAME
        """
        report = "2025-08-21-New Fall 2025 and Summer 2025 By Student and Acad Level"
        name = "New Fall 2025 and Summer 2025 By Student and Acad Level"
        self.save_query_results(query, db="ODS", func_dict=None)(report, name)

    '''
    ID: Unknown
    Name: 2025-08-21-Total Enrollment By FT, PT, SC Status
    Person: Rebecca Schwartz
    Start Date: 2025-08-21
    End Date: 2025-08-21
    Description:
    '''

    def getEnrollmentByFTPTSC(self):
        query = f"""
                          SELECT DISTINCT STTR_STUDENT                  AS ID,
                                  FIRST_NAME,
                                  LAST_NAME,
                                  ST.STTR_STUDENT_LOAD          AS LOAD,
                                  COALESCE(STT_DESC, 'Unknown') AS STUDENT_TYPE,
                                  CASE
                                      WHEN EXISTS (SELECT 1
                                                   FROM SPT_STUDENT_ACAD_CRED AS STC
                                                   WHERE STC_TERM = '2025FA'
                                                     AND STC_PERSON_ID = STTR_STUDENT
                                                     AND STC_CRED_TYPE = 'INST'
                                                     AND STC_CRED > 0) THEN 1
                                      ELSE 0 END                AS FOR_CREDIT
                  FROM ODS_STUDENT_TERMS AS ST
                           JOIN ODS_PERSON ON ST.STTR_STUDENT = ODS_PERSON.ID
                           LEFT JOIN (SELECT STUDENTS_ID,
                                             STU_TYPES,
                                             ROW_NUMBER() OVER (PARTITION BY STUDENTS_ID ORDER BY STU_TYPE_DATES DESC) AS RANK
                                      FROM Z01_STU_TYPE_INFO) AS Z01_STU_TYPE_INFO
                                     ON STTR_STUDENT = STUDENTS_ID AND RANK = 1
                           LEFT JOIN Z01_STUDENT_TYPES
                                     ON Z01_STU_TYPE_INFO.STU_TYPES = Z01_STUDENT_TYPES.STUDENT_TYPES_ID
                  WHERE STTR_TERM = '2025FA'
                    AND STATUS_DESC = 'Registered'
        """
        agg = lambda query: f"""
        --(Begin 3)-------------------------------------------------------------------------------------------------------------
SELECT STATUS,
       COUNT(*) AS STUDENT_COUNT_2025FA
FROM (
--(Begin 2)-------------------------------------------------------------------------------------------------------------
         SELECT ID,
                FIRST_NAME,
                LAST_NAME,
                CASE
                    WHEN STUDENT_TYPE = 'Senior Citizen' AND FOR_CREDIT = 1 THEN 'Senior Citizen For Credit'
                    WHEN LOAD IN ('F', 'O') THEN 'Full-Time'
                    ELSE 'Part-Time' END AS STATUS
         FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
            {query}
--(End 1)---------------------------------------------------------------------------------------------------------------
              ) AS X
--(End 2)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY STATUS
--(End 3)---------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT X.* FROM ({query}) AS X JOIN ODS_PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-08-21-Total Enrollment By FT, PT, SC Status"
        name = "Total Enrollment By FT, PT, SC Status"
        self.save_query_results(query, db="ODS", func_dict={"Agg": agg, "Names": names})(report, name)


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

    '''
    ID: Unknown
    Name: 2025-09-15-Update IPEDS IC Survey
    Person: IPEDS
    Start Date: 2025-09-15
    End Date: 2025-09-15
    '''
    #===================================================================================================================
    '''
    Code is in another file.
    '''
    # ===================================================================================================================

    '''
    ID: Unknown
    Name: 2025-09-17-IPEDS Fall Survey
    Person: IPEDS
    Start Date: 2025-09-15
    End Date: 2025-09-15
    '''
    #===================================================================================================================
    '''
    Code is in another file.
    '''
    # ===================================================================================================================


    '''
    ID: Unknown
    Name: 2025-09-18-Average Class Size
    Person: Rebecca Schwartz
    Start Date: 2025-09-18
    End Date:
    Due Date:
    Description:
    "Can you figure out what the average class size for fall 2025?  I'd also like the total number of classes being 
    taught, and the list of faculty teaching those classes, if possible."
    '''
    def getAverageClassSize(self):
        query = f"""
        SELECT DISTINCT SCS_STUDENT,
                SCS_COURSE_SECTION,
                SEC_SHORT_TITLE
        FROM STUDENT_COURSE_SEC AS SCS
        JOIN COURSE_SECTIONS CS ON SCS.SCS_COURSE_SECTION = CS.COURSE_SECTIONS_ID
        JOIN STUDENT_ACAD_CRED AS STC ON SCS.SCS_STUDENT_ACAD_CRED = STC.STUDENT_ACAD_CRED_ID
        JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
        WHERE CS.SEC_TERM = '2025FA'
        AND STATUS.STC_STATUS IN ('N', 'A')
        """
        agg = lambda query: f"""
        --(Begin 3)-----------------------------------------------------------------------------------------------------
        SELECT AVG(1.0 * STUDENT_COUNT) AS AVERAGE_CLASSROOM_SIZE
        FROM (
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT SCS_COURSE_SECTION,
                SEC_SHORT_TITLE,
                COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
        ) AS X GROUP BY SCS_COURSE_SECTION, SEC_SHORT_TITLE
        --(End 2)-------------------------------------------------------------------------------------------------------
        ) AS X
        --(End 3)-------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.SCS_STUDENT = P.ID
        ORDER BY X.SEC_SHORT_TITLE, SCS_COURSE_SECTION, LAST_NAME, FIRST_NAME
        """
        report = "2025-09-18-Average Class Size"
        name = "Average Class Size"
        self.save_query_results(query, {"Agg": agg, "Names": names}, snapshot_term="2025FA")(report, name)

    def getTotalClassesWithFacultyNames(self):
        query = f"""
        SELECT DISTINCT COURSE_SECTIONS_ID,
                        SEC_NAME,
                        SEC_SHORT_TITLE,
                        SEC_FACULTY_INFO
        FROM COURSE_SECTIONS
        WHERE SEC_TERM = '2025FA'
        """
        agg = lambda query: f"""
        SELECT COUNT(*) AS TOTAL_CLASSES
        FROM (
        {query}
        ) AS X
        """
        names = lambda query: f"""
        SELECT * FROM ({query}) AS X ORDER BY SEC_NAME, SEC_FACULTY_INFO
        """
        report = "2025-09-18-Average Class Size"
        name = "Total Number of Classes Being Taught Along With Class-Faculty List"
        self.save_query_results(query, {"Agg": agg, "Names": names}, snapshot_term="2025FA")(report, name)

    '''
    ID: Unknown
    Name: 2025-09-19-Graduation Rates
    Person: Rebecca Schwartz
    Start Date: 2025-09-19
    End Date: 
    Due Date: 
    Description:
    "Can you please look up the 4 year, first time, fulltime graduation rate for the 2021 cohort?  They should have 
    graduated in May, and marketing would like to know the number."
    '''
    def get2025SP_TermGraduationRate(self):
        query = f"""
        SELECT STUDENT_ID,
        CASE WHEN STUDENT_START_DATE >= DATEADD(YEAR, -4, GRADUATION_TERM.TERM_END_DATE) THEN 1 ELSE 0 END AS 
        FOUR_YEAR_GRADUATED
        FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        JOIN TERMS AS GRADUATION_TERM ON TERMS_ID = '2025SP'
        LEFT JOIN (
            SELECT APPL_APPLICANT AS ID,
                   TERM_START_DATE AS STUDENT_START_DATE,
                   ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE DESC) AS RANK
            FROM APPLICATIONS AS AP
            JOIN STUDENT_ACAD_CRED AS STC ON AP.APPL_APPLICANT = STC.STC_PERSON_ID AND AP.APPL_START_TERM = STC.STC_TERM
            JOIN STC_STATUSES AS STAT ON STC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
            JOIN TERMS ON APPL_START_TERM = TERMS_ID
            WHERE APPL_DATE IS NOT NULL
            AND STC_STATUS IN ('A', 'N')
            AND STC_CRED_TYPE = 'INST'
        ) AS COHORT ON SAPV.STUDENT_ID = COHORT.ID AND RANK = 1
        WHERE STP_CURRENT_STATUS = 'Graduated'
        AND STP_END_DATE BETWEEN GRADUATION_TERM.TERM_START_DATE AND GRADUATION_TERM.TERM_END_DATE
        """
        self.print_table(query)
        agg = lambda query: f"""
        SELECT FORMAT(AVG(1.0 * FOUR_YEAR_GRADUATED), 'P') AS FOUR_YEAR_GRADUATION_RATE
        FROM (
        {query}
        ) AS X
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME
        """
        report = "2025-09-19-Graduation Rates"
        name = "2025SP Term Four-Year Graduation Rate"
        self.save_query_results(query, {"Agg": agg, "Names": names}, snapshot_term="2025FA")(report, name)

    def get2021FA_CohortGraduationRate(self):
        query = f"""
        SELECT ID,
               CASE WHEN EXISTS (
                    SELECT 1
                    FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                    WHERE STP_CURRENT_STATUS = 'Graduated'
                    AND STUDENT_ID = COHORT.ID
                    AND STP_END_DATE <= DATEADD(YEAR, 4, COHORT.STUDENT_START_DATE)
                    ) THEN 1 ELSE 0 END AS FOUR_YEAR_GRADUATED
        FROM (
            SELECT ID,
                   STUDENT_START_DATE
            FROM (
            SELECT APPL_APPLICANT AS ID,
                   APPL_START_TERM AS COHORT_TERM,
                   TERM_START_DATE AS STUDENT_START_DATE,
                   ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE DESC) AS RANK
            FROM APPLICATIONS AS AP
            JOIN STUDENT_ACAD_CRED AS STC ON AP.APPL_APPLICANT = STC.STC_PERSON_ID AND AP.APPL_START_TERM = STC.STC_TERM
            JOIN STC_STATUSES AS STAT ON STC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
            JOIN TERMS ON APPL_START_TERM = TERMS_ID
            WHERE APPL_DATE IS NOT NULL
            AND STC_STATUS IN ('A', 'N')
            AND STC_CRED_TYPE = 'INST'
            ) AS X
            WHERE RANK = 1 AND COHORT_TERM = '2021FA'
        ) AS COHORT
        """
        agg = lambda query: f"""
        SELECT FORMAT(AVG(1.0 * FOUR_YEAR_GRADUATED), 'P') AS FOUR_YEAR_GRADUATION_RATE
        FROM (
        {query}
        ) AS X
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        report = "2025-09-19-Graduation Rates"
        name = "2021FA Cohort Four-Year Graduation Rate"
        self.save_query_results(query, {"Agg": agg, "Names": names}, snapshot_term="2025FA")(report, name)

    '''
    ID: Unknown
    Name: 2025-09-24-Review IPEDS Spring Survey
    Person: IPEDS
    Start Date: 2025-09-24
    End Date: 
    Description:
    '''
    #===================================================================================================================
    '''
    Code is in another file.
    '''
    # ===================================================================================================================

    '''
    ID: Unknown
    Name: 2025-09-30-Another Nursing Data Request
    Person: Lauren Swant
    Start Date: 2025-09-30
    End Date:
    Due Date:
    Description:
    "For our annual report to AACN, I need to provide the following information by October 17th.
    Use official TOTAL enrollment figures (both continued and new students) for Fall 2025.
    Use official graduation figures from  August 1, 2024 through July 31, 2025.
    Nursing students are defined as students who have been formally accepted into the nursing program whether or not 
    they have taken any nursing courses. (For us - these are all NUR and ACNU coded students. These are NOT students 
    coded as PNUR or DNUR).
    Exclude pre-nursing students (students who have not been formally accepted into the nursing program).
    Include admissions and transfer students.
    Use your institution's definition of full- and part-time. (I'm not sure how to address this - perhaps we go based 
    off their status in Fall 2025).
    If you offer this program, but do not currently have any students or graduates, please enter zero in the full- and 
    part-time students and total graduates boxes on the following pages.
    Generic baccalaureate students do not have previous nursing experience as a registered nurse; this category includes
     students in any of the following programs:

    Generic (basic, entry-level) baccalaureate
    Baccalaureate for non-nursing college graduates (2nd Degree)
    LPN to baccalaureate"
    '''
    def getNursingStudentsByLoad(self):
        query = f"""
         SELECT DISTINCT STUDENT_ID,
                         LOADS.NAME AS LOAD
         FROM STUDENT_ACAD_CRED AS STC
                  JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
                  JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV ON STC.STC_PERSON_ID = SAPV.STUDENT_ID
                  JOIN STUDENT_TERMS_VIEW AS STV ON STC_PERSON_ID = STV.STTR_STUDENT AND STC_TERM = STV.STTR_TERM
                  JOIN (VALUES ('F', 'Full-Time'),
                               ('O', 'Full-Time'),
                               ('L', 'Part-Time')) AS LOADS(ID, NAME) ON STV.STTR_STUDENT_LOAD = LOADS.ID
            WHERE STC_TERM = '2025FA'
           AND STP_START_DATE <= STC_END_DATE
           AND COALESCE(STP_END_DATE, STC_START_DATE) >= STC_START_DATE
           AND STP_PROGRAM_TITLE IN ('Nursing', 'Accelerated Nursing')
           AND STC_STATUS IN ('N', 'A')
           AND COALESCE(SCS_PASS_AUDIT, '') != 'A'
        """
        agg = lambda query: f"""
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
        SELECT LOAD,
               COUNT(*) AS STUDENTS
        FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)---------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY LOAD
        --(End 2)---------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-30-Another Nursing Data Request"
        name = "2025FA Enrollment By Load"
        self.save_query_results(query, {"Agg": agg, "Names": names}, snapshot_term="2025FA")(report, name)

    def getNursingStudentGraduates(self):
        query = f"""
        SELECT DISTINCT STUDENT_ID,
                STP_PROGRAM_TITLE,
                STP_END_DATE
        FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        CROSS JOIN (VALUES ('2024-08-01', '2025-07-31')) AS REPORTING_PERIOD(RP_START, RP_END)
        WHERE  STP_CURRENT_STATUS = 'Graduated'
           AND STP_END_DATE >= REPORTING_PERIOD.RP_START
           AND STP_END_DATE <= REPORTING_PERIOD.RP_END
           AND STP_PROGRAM_TITLE IN ('Nursing', 'Accelerated Nursing')
        """
        agg = lambda query: f"""
        SELECT COUNT(*) AS TOTAL_GRADUATES FROM ({query}) AS X
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-30-Another Nursing Data Request"
        name = "Total Graduates (24-08-01 to 25-07-31)"
        self.save_query_results(query, {"Agg": agg, "Names": names}, snapshot_term="2025FA")(report, name)

    def getNursingStudentsByRace(self):
        query = f"""
         SELECT DISTINCT STUDENT_ID,
                IPEDS_RACE_ETHNIC_DESC AS RACE,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM STUDENT_ACAD_CRED AS STC
                    JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
                    JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                    WHERE STC_TERM = '2025FA'
                     AND SAPV.STP_START_DATE <= STC_END_DATE
                    AND COALESCE(SAPV.STP_END_DATE, STC_START_DATE) >= STC_START_DATE
                    AND STC_STATUS IN ('N', 'A')
                    AND COALESCE(SCS_PASS_AUDIT, '') != 'A'
                    AND STC_PERSON_ID = SAPV.STUDENT_ID
                ) THEN 1 ELSE 0 END AS ENROLLED_2025FA,
                CASE WHEN SAPV.STP_END_DATE >= REPORTING_PERIOD.RP_START
                        AND SAPV.STP_END_DATE <= REPORTING_PERIOD.RP_END
                        AND STP_CURRENT_STATUS = 'Graduated'
                     THEN 1 ELSE 0 END AS GRADUATED
         FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
         CROSS JOIN (VALUES ('2024-08-01', '2025-07-31')) AS REPORTING_PERIOD(RP_START, RP_END)
         WHERE STP_PROGRAM_TITLE IN ('Nursing', 'Accelerated Nursing')
        """
        agg = lambda query: f"""
        SELECT RACE,
                SUM(ENROLLED_2025FA) AS [Students (Fall 2025)],
                SUM(GRADUATED) AS [Graduates (8/1/24-7/31/25)]  
        FROM (
        {query}
        ) AS X
        GROUP BY RACE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-30-Another Nursing Data Request"
        name = "Nursing Students By Race"
        self.save_query_results(query, {"Agg": agg, "Names": names}, snapshot_term="2025FA")(report, name)

    def getNursingStudentsByGender(self):
        query = f"""
         SELECT DISTINCT STUDENT_ID,
                STUDENT_GENDER AS GENDER,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM STUDENT_ACAD_CRED AS STC
                    JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
                    JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                    WHERE STC_TERM = '2025FA'
                     AND SAPV.STP_START_DATE <= STC_END_DATE
                    AND COALESCE(SAPV.STP_END_DATE, STC_START_DATE) >= STC_START_DATE
                    AND STC_STATUS IN ('N', 'A')
                    AND COALESCE(SCS_PASS_AUDIT, '') != 'A'
                    AND STC_PERSON_ID = SAPV.STUDENT_ID
                ) THEN 1 ELSE 0 END AS ENROLLED_2025FA,
                CASE WHEN SAPV.STP_END_DATE >= REPORTING_PERIOD.RP_START
                        AND SAPV.STP_END_DATE <= REPORTING_PERIOD.RP_END
                        AND STP_CURRENT_STATUS = 'Graduated'
                     THEN 1 ELSE 0 END AS GRADUATED
         FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
         CROSS JOIN (VALUES ('2024-08-01', '2025-07-31')) AS REPORTING_PERIOD(RP_START, RP_END)
         WHERE STP_PROGRAM_TITLE IN ('Nursing', 'Accelerated Nursing')
        """
        agg = lambda query: f"""
        SELECT GENDER,
                SUM(ENROLLED_2025FA) AS [Students (Fall 2025)],
                SUM(GRADUATED) AS [Graduates (8/1/24-7/31/25)]  
        FROM (
        {query}
        ) AS X
        WHERE GENDER IS NOT NULL
        GROUP BY GENDER
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-09-30-Another Nursing Data Request"
        name = "Nursing Students By Gender"
        self.save_query_results(query, {"Agg": agg, "Names": names}, snapshot_term="2025FA")(report, name)

    '''
    ID: Unknown
    Name: 2025-10-01-IPEDS Database Standard Deviation
    Person: Rebecca Schwartz
    Start Date: 2025-10-01
    End Date: 2025-10-01
    Description: 
    '''
    #===================================================================================================================
    '''
    Code is in another file.
    '''
    # ===================================================================================================================

    '''
    ID: Unknown
    Name: 2025-10-05-Elementary Education Program Review
    Person: Rebecca Schwartz
    Start Date: 2025-10-05
    End Date:
    Description:
    '''
    #---------Declared Majors and Minors--------------------------------------------------------------------------------

    def getElemEdTermHeadcount(self):
        query = f"""
                 SELECT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID,
                STUDENT_LAST_NAME,
                STUDENT_FIRST_NAME
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND STP_START_DATE <= TERMS.TERM_END_DATE
           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
           AND (
             (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                 OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                 AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Elementary Education'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Term Headcount"
        self.save_query_results(query, snapshot_term="2025FA", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getElemEdTermHeadcountByLoad(self):
        query = f"""
        SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
        TERMS.TERM_START_DATE,
        MAJORS.MAJ_DESC AS MAJOR,
        SAPV.STUDENT_ID,
        CASE
            WHEN STUDENT_LOAD IN ('F', 'O') THEN 'FT'
            WHEN STUDENT_LOAD IS NOT NULL THEN 'PT'
            ELSE 'Unknown' END AS LOAD
        FROM MAJORS
          CROSS JOIN TERMS
          CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
          LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                    ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
          LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
          LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
          LEFT JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON SEV.STUDENT_ID = SAPV.STUDENT_ID AND SEV.ENROLL_TERM = TERMS_ID
        WHERE TERMS.TERM_START_DATE >= '2019-08-01'
        AND TERMS.TERM_END_DATE < '2025-06-01'
        AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
        AND STP_START_DATE <= TERMS.TERM_END_DATE
        AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
        AND STP_CURRENT_STATUS != 'Did Not Enroll'
        AND (
        (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
         OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
         AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
         AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
         )
        )
        AND MAJORS.MAJ_DESC = 'Elementary Education'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               LOAD,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE, LOAD
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Term Headcount By Load"
        self.save_query_results(query, snapshot_term="2025FA", func_dict={"Agg": agg, "Names": names})(report, name)

    def getElemEdTermHeadcountByLevel(self):
        query = f"""
                 SELECT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID,
                STP_ACAD_LEVEL AS LEVEL
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND STP_START_DATE <= TERMS.TERM_END_DATE
           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
           AND (
             (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                 OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                 AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Elementary Education'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               LEVEL,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE, LEVEL
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Term Headcount By Level"
        self.save_query_results(query, snapshot_term="2025FA", func_dict={"Agg": agg, "Names": names})(report, name)

    def getElemEdTermHeadcountByRace(self):
        query = f"""
                 SELECT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID,
                SAPV.IPEDS_RACE_ETHNIC_DESC AS RACE
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND STP_START_DATE <= TERMS.TERM_END_DATE
           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
           AND (
             (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                 OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                 AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Elementary Education'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               RACE,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
        {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE, RACE
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Term Headcount By Race"
        self.save_query_results(query, snapshot_term="2025FA", func_dict={"Agg": agg, "Names": names})(report, name)

    def getElemEdTermHeadcountByVeteranStatus(self):
        query = f"""
                 SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM STA_OTHER_COHORTS_VIEW
                    WHERE STA_OTHER_COHORT_GROUPS = 'VETS'
                    AND STA_STUDENT = STUDENT_ID
                    AND (STP_START_DATE <= STA_OTHER_COHORT_END_DATES OR STA_OTHER_COHORT_END_DATES IS NULL)
                    AND (STP_END_DATE >= STA_OTHER_COHORT_START_DATES OR STP_END_DATE IS NULL)
                ) THEN 'Veteran' ELSE 'Not Veteran' END AS VET_STATUS
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND STP_START_DATE <= TERMS.TERM_END_DATE
           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
           AND (
             (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                 OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                 AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Elementary Education'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               VET_STATUS,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE, VET_STATUS
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Term Headcount By Veteran Status"
        self.save_query_results(query, snapshot_term="2025FA", func_dict={"Agg": agg, "Names": names})(report, name)

    def getElemEdTermHeadcountByAthleteStatus(self):
        query = f"""
                 SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM STA_OTHER_COHORTS_VIEW
                    JOIN (SELECT VAL_INTERNAL_CODE AS CODE, VAL_EXTERNAL_REPRESENTATION AS COHORT
                          FROM VALS
                          WHERE VALCODE_ID = 'INSTITUTION.COHORTS') AS COHORT_CODES
                    ON STA_OTHER_COHORTS_VIEW.STA_OTHER_COHORT_GROUPS = COHORT_CODES.CODE
                    WHERE COHORT IN (
                                        'Cheerleading',
                                        'Dance',
                                        'Football',
                                        'Indoor Men''s Track',
                                        'Indoor Women''s Track',
                                        'Men''s Basketball',
                                        'Men''s Cross Country',
                                        'Men''s Golf',
                                        'Men''s Soccer',
                                        'Outdoor Men''s Track',
                                        'Outdoor Women''s Track',
                                        'Women''s Basketball',
                                        'Women''s Cross Country',
                                        'Women''s Golf',
                                        'Women''s Soccer',
                                        'Women''s Softball',
                                        'Women''s Volleyball'
                                     )
                    AND STA_STUDENT = STUDENT_ID
                    AND (STP_START_DATE <= STA_OTHER_COHORT_END_DATES OR STA_OTHER_COHORT_END_DATES IS NULL)
                    AND (STP_END_DATE >= STA_OTHER_COHORT_START_DATES OR STP_END_DATE IS NULL)
                ) THEN 'Athlete' ELSE 'Not Athlete' END AS ATHLETE_STATUS
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND STP_START_DATE <= TERMS.TERM_END_DATE
           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
           AND (
             (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                 OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                 AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Elementary Education'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               ATHLETE_STATUS,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE, ATHLETE_STATUS
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Term Headcount By Athlete Status"
        self.save_query_results(query, snapshot_term="2025FA", func_dict = {"Agg": agg, "Names": names})(report, name)

    #---------New Students----------------------------------------------------------------------------------------------

    def getElemEdNewStudentCountPerTerm(self):
        query = f"""
--(Begin 2)------------------------------------------------------------------------------------------------------------
         SELECT TERM,
                TERM_START_DATE,
                MAJOR,
                STUDENT_ID
         FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
                  SELECT DISTINCT TERMS.TERMS_ID                AS TERM,
                                  TERMS.TERM_START_DATE,
                                  MAJORS.MAJ_DESC               AS MAJOR,
                                  SAPV.STUDENT_ID,
                                  ROW_NUMBER() OVER (PARTITION BY STUDENT_ID, MAJORS.MAJ_DESC
                                      ORDER BY TERM_START_DATE) AS TERM_RANK
                  FROM MAJORS
                           CROSS JOIN TERMS
                           CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
------------------------------------------------------------------------------------------------------------------------
                           LEFT JOIN STPR_MAJOR_LIST_VIEW AS SMLV
                                     ON SAPV.STUDENT_ID = SMLV.STPR_STUDENT AND
                                        SAPV.STP_ACADEMIC_PROGRAM = SMLV.STPR_ACAD_PROGRAM
                           LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                           LEFT JOIN MAJORS AS ADDNL_MAJOR ON SMLV.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
-----------------------------------------------------------------------------------------------------------------------
                  WHERE TERMS.TERM_START_DATE >= DATEADD(YEAR, -10, '2019-08-01')
                    AND TERMS.TERM_END_DATE < '2025-06-01'
                    AND (TERMS.TERMS_ID LIKE '%FA')
------------------------------------------------------------------------------------------------------------------------
                    AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
------------------------------------------------------------------------------------------------------------------------
                    AND (
                      (
                          MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                              AND SAPV.STP_START_DATE <= TERMS.TERM_END_DATE
                              AND (SAPV.STP_END_DATE >= TERMS.TERM_START_DATE OR SAPV.STP_END_DATE IS NULL)
                          )
                          OR (
                          MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                              AND SMLV.STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                              AND
                          (SMLV.STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                           SMLV.STPR_ADDNL_MAJOR_END_DATE IS NULL)
                          )
                      )
------------------------------------------------------------------------------------------------------------------------
                    AND MAJORS.MAJ_DESC = 'Elementary Education'
--(End 1)------------------------------------------------------------------------------------------------------------
              ) AS X
         WHERE TERM_RANK = 1
           AND TERM_START_DATE >= '2019-08-01'
--(End 2)------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 3)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 2)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 3)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "New Student Count Per Term"
        self.save_query_results(query, snapshot_term="2025FA", func_dict={"Agg": agg, "Names": names})(report, name)

    def getElemEdNewStudentPercentChange(self):
        query = f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                  SELECT TERM,
                         TERM_START_DATE,
                         MAJOR,
                         STUDENT_ID
                  FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                                   SELECT DISTINCT TERMS.TERMS_ID                AS TERM,
                                                   TERMS.TERM_START_DATE,
                                                   MAJORS.MAJ_DESC               AS MAJOR,
                                                   SAPV.STUDENT_ID,
                                                   ROW_NUMBER() OVER (PARTITION BY STUDENT_ID, MAJORS.MAJ_DESC
                                                       ORDER BY TERM_START_DATE) AS TERM_RANK
                                   FROM MAJORS
                                            CROSS JOIN TERMS
                                            CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        ------------------------------------------------------------------------------------------------------------------------
                                            LEFT JOIN STPR_MAJOR_LIST_VIEW AS SMLV
                                                      ON SAPV.STUDENT_ID = SMLV.STPR_STUDENT AND
                                                         SAPV.STP_ACADEMIC_PROGRAM = SMLV.STPR_ACAD_PROGRAM
                                            LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                            LEFT JOIN MAJORS AS ADDNL_MAJOR ON SMLV.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
        -----------------------------------------------------------------------------------------------------------------------
                                   WHERE TERMS.TERM_START_DATE >= DATEADD(YEAR, -10, '2019-08-01')
                                     AND TERMS.TERM_END_DATE < '2025-06-01'
                                     AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS_ID LIKE '%SP')
        ------------------------------------------------------------------------------------------------------------------------
                                     AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
        ------------------------------------------------------------------------------------------------------------------------
                                     AND (
                                       (
                                           MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                                               AND SAPV.STP_START_DATE <= TERMS.TERM_END_DATE
                                               AND (SAPV.STP_END_DATE >= TERMS.TERM_START_DATE OR SAPV.STP_END_DATE IS NULL)
                                           )
                                           OR (
                                           MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                               AND SMLV.STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                               AND
                                           (SMLV.STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                            SMLV.STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                           )
                                       )
        ------------------------------------------------------------------------------------------------------------------------
                                     AND MAJORS.MAJ_DESC = 'Elementary Education'
        --(End 1)------------------------------------------------------------------------------------------------------------
                               ) AS X
                          WHERE TERM_RANK = 1
                            AND TERM_START_DATE >= '2019-08-01'
        --(End 2)------------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 4)------------------------------------------------------------------------------------------------------------
        WITH X AS (
        --(Begin 3)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        COUNT(*) AS STUDENT_COUNT
                 FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
            {query}
        --(End 2)------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY TERM, TERM_START_DATE
        --(End 3)------------------------------------------------------------------------------------------------------------
             )
            SELECT CONCAT(X.TERM, ' TO ', NEXT_TERM.SECOND) AS TERM_CHANGE,
                   X.STUDENT_COUNT AS FIRST_COUNT,
                   Y.STUDENT_COUNT AS NEXT_TERM_COUNT,
                   FORMAT(Y.STUDENT_COUNT * 1.0 / X.STUDENT_COUNT - 1, 'P') AS PERCENT_CHANGE
            FROM X LEFT JOIN (VALUES ('2019FA', '2020FA'),
                                 ('2020FA', '2021FA'),
                                 ('2021FA', '2022FA'),
                                 ('2022FA', '2023FA'),
                                 ('2023FA', '2024FA')
            ) AS NEXT_TERM(FIRST, SECOND) ON X.TERM = NEXT_TERM.FIRST
            JOIN X AS Y ON NEXT_TERM.SECOND = Y.TERM
        --(End 4)------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "New Student Percent Change"
        self.save_query_results(query, snapshot_term="2025FA", func_dict={"Agg": agg, "Names": names})(report, name)

    def getElemEdChangeMajor(self):
        query = f"""
                                            SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
                                                    TERMS.TERM_START_DATE,
                                                    MAJORS.MAJ_DESC AS MAJOR,
                                                    STUDENT_ID
                                    FROM MAJORS
                                             CROSS JOIN TERMS
                                             CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                             LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                                       ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                          STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                             LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                             LEFT JOIN MAJORS AS ADDNL_MAJOR
                                                       ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                                    WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                                      AND TERMS.TERM_END_DATE < '2025-06-01'
                                      AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                                      AND STP_START_DATE <= TERMS.TERM_END_DATE
                                      AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                                      AND STP_CURRENT_STATUS != 'Did Not Enroll'
                                      AND (
                                        (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                                            OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                            AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                            AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                                 STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                            )
                                        )
        """
        agg = lambda query: f"""
        --(Begin 5)-------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               MAJOR,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 4)------------------------------------------------------------------------------------------------------------
                 SELECT TERM,
                        TERM_START_DATE,
                        MAJOR,
                        STUDENT_ID
                 FROM (
        --(Begin 3)------------------------------------------------------------------------------------------------------------
                          SELECT TERM,
                                 TERM_START_DATE,
                                 MAJOR,
                                 STUDENT_ID,
                                 CASE
                                     WHEN MAX(CASE WHEN MAJOR_2 = MAJOR THEN 1 ELSE 0 END) = 0 THEN 'Changed Major'
                                     ELSE 'Kept Major' END AS MAJOR_CHANGE
                          FROM (
        --(Begin 2)------------------------------------------------------------------------------------------------------------
                                   SELECT X.TERM,
                                          X.TERM_START_DATE,
                                          X.MAJOR,
                                          X.STUDENT_ID,
                                          Y.MAJOR AS MAJOR_2
                                   FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
                {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
                                        ) AS X
                                            LEFT JOIN (VALUES ('2019FA', '2020SP'),
                                                              ('2020SP', '2020FA'),
                                                              ('2020FA', '2021SP'),
                                                              ('2021SP', '2021FA'),
                                                              ('2021FA', '2022SP'),
                                                              ('2022SP', '2022FA'),
                                                              ('2022FA', '2023SP'),
                                                              ('2023SP', '2023FA'),
                                                              ('2023FA', '2024SP'),
                                                              ('2024SP', '2024FA'),
                                                              ('2024FA', '2025SP')) AS NEXT_TERM(FIRST, SECOND)
                                                      ON X.TERM = NEXT_TERM.FIRST
                                            JOIN (SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
                                                                  TERMS.TERM_START_DATE,
                                                                  MAJORS.MAJ_DESC AS MAJOR,
                                                                  STUDENT_ID
                                                  FROM MAJORS
                                                           CROSS JOIN TERMS
                                                           CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                           LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                                                     ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                                        STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                                           LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                                           LEFT JOIN MAJORS AS ADDNL_MAJOR
                                                                     ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                                                  WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                                                    AND TERMS.TERM_END_DATE < '2025-06-01'
                                                    AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                                                    AND STP_START_DATE <= TERMS.TERM_END_DATE
                                                    AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                                                    AND STP_CURRENT_STATUS != 'Did Not Enroll'
                                                    AND (
                                                      (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                                                          OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                                          AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                                          AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                                               STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                                          )
                                                      )) AS Y ON X.STUDENT_ID = Y.STUDENT_ID AND NEXT_TERM.SECOND = Y.TERM
                                   WHERE X.MAJOR IN (
                                                     'Elementary Education'
                                       )
        --(End 2)------------------------------------------------------------------------------------------------------------
                               ) AS X
                          GROUP BY TERM, TERM_START_DATE, MAJOR, STUDENT_ID
        --(End 3)------------------------------------------------------------------------------------------------------------
                      ) AS X
                WHERE MAJOR_CHANGE = 'Changed Major'
        --(End 4)------------------------------------------------------------------------------------------------------------
            ) AS X
        GROUP BY TERM, TERM_START_DATE, MAJOR
        --(End 5)-------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Change Major"
        self.save_query_results(query, snapshot_term="2025FA", func_dict={"Agg": agg, "Names": names})(report, name)

    def getElemEdDeclareMajor(self):
        query = f"""
                 SELECT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS SMLV
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON SMLV.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND STP_START_DATE <= TERMS.TERM_END_DATE
           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
            AND (
              (
                  MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                      AND SAPV.STP_START_DATE <= TERMS.TERM_END_DATE
                      AND SAPV.STP_START_DATE >= TERMS.TERM_START_DATE
                  )
                  OR (
                      MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                      AND SMLV.STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                      AND SMLV.STPR_ADDNL_MAJOR_START_DATE >= TERMS.TERM_START_DATE
                  )
              )
            AND MAJORS.MAJ_DESC = 'Elementary Education'
        """
        agg = lambda query: f"""
        --(Begin 2)------------------------------------------------------------------------------------------------------------
        SELECT TERM,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)------------------------------------------------------------------------------------------------------------
        {query}
        --(End 1)------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY TERM, TERM_START_DATE
        --(End 2)------------------------------------------------------------------------------------------------------------
        ORDER BY TERM_START_DATE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Declare Major"
        self.save_query_results(query, snapshot_term="2025FA", func_dict={"Agg": agg, "Names": names})(report, name)

    #----------Course Enrollments---------------------------------------------------------------------------------------

    def getElemEdAvgEnrollmentPerCourse(self):
        query = f"""
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
                    AND MAJORS.MAJ_DESC = 'Elementary Education'
                    -------------------------------------------------------------------------------------------------
                    AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
        """
        agg = lambda query: f"""
        --(Begin 3)-------------------------------------------------------------------------------------------------------------
        SELECT COURSE_TITLE,
               COURSE_NAME,
               AVG(TOTAL_ENROLLMENT) AS AVG_ENROLLMENT
        FROM (
        --(Begin 2)-------------------------------------------------------------------------------------------------------------
                 SELECT COURSE_TITLE,
                        COURSE_NAME,
                        COUNT(STUDENT_ID) AS TOTAL_ENROLLMENT
                 FROM (
        --(Begin 1)-------------------------------------------------------------------------------------------------------------
            {query}
        --(End 1)-------------------------------------------------------------------------------------------------------------
                      ) AS X
                 GROUP BY TERM, TERM_START_DATE, COURSE_TITLE, COURSE_NAME
        --(End 2)-------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY COURSE_TITLE, COURSE_NAME
        --(End 3)-------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Avg Enrollment Per Course"
        self.save_query_results(query, snapshot_term="2025FA", func_dict={"Agg": agg, "Names": names})(report, name)

    def getElemEdPercentUnderenrolled(self):
        query = f"""
                                                    SELECT DISTINCT TERMS.TERMS_ID           AS TERM,
                                                            TERM_START_DATE,
                                                            SAPV.STUDENT_ID,
                                                            SEV.SECTION_COURSE_NAME  AS COURSE_NAME,
                                                            SEV.SECTION_COURSE_TITLE AS COURSE_TITLE,
                                                            SEV.ENROLL_CREDITS
                                            FROM MAJORS
                                                     CROSS JOIN TERMS
                                                     CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                     LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                                               ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                                  STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                                     LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                                     LEFT JOIN MAJORS AS ADDNL_MAJOR
                                                               ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
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
                                                    (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                                     STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                                    )
                                                )
                                              AND MAJORS.MAJ_DESC = 'Elementary Education'
                                              ---------------------------------------------------------------------------------
                                              AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                """
        agg = lambda query: f"""
                --(Begin 5)------------------------------------------------------------------------------------------------------------
        SELECT FORMAT(SUM(UNDER_ENROLLED) * 1.0 / COUNT(*), 'P') AS PERCENT_UNDER_ENROLLED
        FROM (
        --(Begin 4)-------------------------------------------------------------------------------------------------------------
                 SELECT COURSE_TITLE,
                        COURSE_NAME,
                        CASE WHEN AVG_ENROLLMENT < 7 THEN 1 ELSE 0 END AS UNDER_ENROLLED
                 FROM (
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
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
                                        ) AS X
                                   GROUP BY TERM, TERM_START_DATE, COURSE_TITLE, COURSE_NAME
        --(End 2)--------------------------------------------------------------------------------------------------------------
                               ) AS X
                          GROUP BY COURSE_TITLE, COURSE_NAME
        --(End 3)--------------------------------------------------------------------------------------------------------------
                      ) AS X
        --(End 4)---------------------------------------------------------------------------------------------------------------
             ) AS X
        --(End 5)---------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Percent Underenrolled"
        self.save_query_results(query, snapshot_term="2025FA", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getElemEdFacultyCourseEnrollments(self):
        query = f"""
        --(Begin 1)--------------------------------------------------------------------------------------
                 SELECT STUDENTS.*,
                        SEV.SECTION_COURSE_NAME          AS COURSE_NAME,
                        SEV.SECTION_COURSE_TITLE         AS COURSE_TITLE,
                        COURSE_SECTIONS.SEC_FACULTY_INFO AS FACULTY
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
                         AND TERMS.TERM_END_DATE < '2025-06-01'
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
                         AND MAJORS.MAJ_DESC = 'Elementary Education') AS STUDENTS
                          JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON STUDENTS.STUDENT_ID = SEV.STUDENT_ID AND TERM = ENROLL_TERM
                          JOIN COURSE_SECTIONS ON SEV.SECTION_COURSE_SECTION_ID = COURSE_SECTIONS_ID
                 WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        --(End 1)-------------------------------------------------------------------------------------------------------
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT FACULTY,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
         ) AS X
        GROUP BY FACULTY
        --(End 2)-----------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Faculty Course Enrollments"
        self.save_query_results(query, snapshot_term="2025FA", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getElemEdFacultyCourseEnrollmentsByLoad(self):
        query = f"""
                 SELECT STUDENTS.*,
                SEV.SECTION_COURSE_NAME          AS COURSE_NAME,
                SEV.SECTION_COURSE_TITLE         AS COURSE_TITLE,
                COURSE_SECTIONS.SEC_FACULTY_INFO AS FACULTY,
                CASE WHEN SEV.STUDENT_LOAD IN ('F', 'O') THEN 'FT' ELSE 'PT' END AS LOAD
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
                 AND TERMS.TERM_END_DATE < '2025-06-01'
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
                 AND MAJORS.MAJ_DESC = 'Elementary Education') AS STUDENTS
                  JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON STUDENTS.STUDENT_ID = SEV.STUDENT_ID AND TERM = ENROLL_TERM
                  JOIN COURSE_SECTIONS ON SEV.SECTION_COURSE_SECTION_ID = COURSE_SECTIONS_ID
         WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT FACULTY,
               LOAD,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
        {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY FACULTY, LOAD
        --(End 2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Faculty Course Enrollments By Load"
        self.save_query_results(query, snapshot_term="2025FA", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getElemEdFacultyCourseEnrollmentsByLevel(self):
        query = f"""
                 SELECT STUDENTS.*,
                SEV.SECTION_COURSE_NAME          AS COURSE_NAME,
                SEV.SECTION_COURSE_TITLE         AS COURSE_TITLE,
                COURSE_SECTIONS.SEC_FACULTY_INFO AS FACULTY,
                SEV.STUDENT_ACAD_LEVEL AS LEVEL
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
                 AND TERMS.TERM_END_DATE < '2025-06-01'
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
                 AND MAJORS.MAJ_DESC = 'Elementary Education') AS STUDENTS
                  JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON STUDENTS.STUDENT_ID = SEV.STUDENT_ID AND TERM = ENROLL_TERM
                  JOIN COURSE_SECTIONS ON SEV.SECTION_COURSE_SECTION_ID = COURSE_SECTIONS_ID
         WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT FACULTY,
               LEVEL,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
        {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY FACULTY, LEVEL
        --(End 2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Faculty Course Enrollments By Level"
        self.save_query_results(query, snapshot_term="2025FA", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getElemEdFacultyCourseEnrollmentsByRace(self):
        query = f"""
                 SELECT STUDENTS.STUDENT_ID,
                SEV.SECTION_COURSE_NAME          AS COURSE_NAME,
                SEV.SECTION_COURSE_TITLE         AS COURSE_TITLE,
                COURSE_SECTIONS.SEC_FACULTY_INFO AS FACULTY,
                STUDENTS.RACE
         FROM (SELECT DISTINCT TERMS.TERMS_ID AS TERM,
                               TERMS.TERM_START_DATE,
                               SAPV.STUDENT_ID,
                               SAPV.IPEDS_RACE_ETHNIC_DESC AS RACE
               FROM MAJORS
                        CROSS JOIN TERMS
                        CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                        LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                  ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                        LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                        LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
               WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                 AND TERMS.TERM_END_DATE < '2025-06-01'
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
                 AND MAJORS.MAJ_DESC = 'Elementary Education') AS STUDENTS
                  JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON STUDENTS.STUDENT_ID = SEV.STUDENT_ID AND TERM = ENROLL_TERM
                  JOIN COURSE_SECTIONS ON SEV.SECTION_COURSE_SECTION_ID = COURSE_SECTIONS_ID
         WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT FACULTY,
               RACE,
               COUNT(*) AS STUDENT_COUNT
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY FACULTY, RACE
        --(End 2)--------------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        {query}
        ) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Faculty Course Enrollments By Race"
        self.save_query_results(query, snapshot_term="2025FA", func_dict = {"Agg": agg, "Names": names})(report, name)

    def getElemEdCourseCompletionRates(self):
        query = f"""
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
                 AND MAJORS.MAJ_DESC = 'Elementary Education') AS STUDENTS
                  JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON STUDENTS.STUDENT_ID = SEV.STUDENT_ID AND TERM = ENROLL_TERM
        """
        agg = lambda query: f"""
        --(Begin 2)--------------------------------------------------------------------------------------
        SELECT COURSE_TITLE,
               COURSE_NAME,
               FORMAT(AVG(COMPLETED * 1.0), 'P') AS COMPLETION_RATE,
               COUNT(*) AS ENROLLMENT_COUNT
        FROM (
        --(Begin 1)--------------------------------------------------------------------------------------
            {query}
        --(End 1)--------------------------------------------------------------------------------------------------------------
             ) AS X
        GROUP BY COURSE_TITLE, COURSE_NAME
        --(End 2)--------------------------------------------------------------------------------------------------------------
        ORDER BY COURSE_NAME, COURSE_TITLE
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Course Completion Rates"
        self.save_query_results(query, snapshot_term="2025FA", func_dict={"Agg": agg, "Names": names})(report, name)

    # ----------Completion Rates---------------------------------------------------------------------------------------

    def getElemEdGraduationRateByCohort(self):
        query = f"""
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
                AND MAJORS.MAJ_DESC = 'Elementary Education'
        """
        agg = lambda query: f"""
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
                {query}
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
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.* FROM ({query}) AS X JOIN PERSON P ON X.STUDENT_ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        report = "2025-10-05-Elementary Education Program Review"
        name = "Graduation Rate By Cohort"
        self.save_query_results(query, snapshot_term="2025FA", func_dict={"Agg": agg, "Names": names})(report, name)








