from Reports import Reports
import os
from IPEDS import IPEDS
import pandas as pd

class IPEDS_Spring(IPEDS):
    def __init__(self):
        super().__init__(folder='IPEDS_Spring', report="2025-09-24-Corrected IPEDS Spring Survey")
        self.gender_assignment_enrollment = pd.read_csv(os.path.join(self.folder, 'Gender Assignment To Unknowns '
                                                                                  '(Fall Enrollment).csv'))
        self.status_str = ",\n".join([f"[{s}]" for s in ["First-time",
                                                       "Transfer-in",
                                                       "Continuing/Returning",
                                                       "Non-degree/non-certificate-seeking"]])

    def enrolledStudents(self, level = None, load = None, gender = None, term = '2024FA'):
        query = f"""
        SELECT *
        FROM (
        SELECT DISTINCT STC_PERSON_ID     AS ID,
                  STC_ACAD_LEVEL          AS LEVEL,
                  STTR_STUDENT_LOAD       AS LOAD,
                  COALESCE(PERSON.GENDER, ASSIGNED_GENDER.GENDER) AS GENDER
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        LEFT JOIN STUDENT_TERMS_VIEW STV ON STC.STC_PERSON_ID = STV.STTR_STUDENT AND STC.STC_TERM = STV.STTR_TERM
        LEFT JOIN TERMS ON STC.STC_TERM = TERMS_ID
        LEFT JOIN PERSON ON STC_PERSON_ID = PERSON.ID
        LEFT JOIN ({self.df_query(self.gender_assignment_enrollment)}) AS ASSIGNED_GENDER ON STC_PERSON_ID = ASSIGNED_GENDER.ID
        WHERE STATUS.STC_STATUS IN ('N', 'A')
        AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
        AND TERMS_ID = '{term}'
        AND STC.STC_CRED > 0
        ) AS X
        WHERE  {f"LEVEL = '{level}'" if level is not None else "LEVEL = LEVEL"}
        AND {"LOAD IN ('F', 'O')" if load == "FT" else "LOAD NOT IN ('F', 'O')" if load == "PT" else "LOAD = LOAD"}
        AND {f"GENDER = '{gender}'" if gender is not None else "GENDER = GENDER"}
        """
        return query

    def deg_status(self, term = '2024FA'):
        query = f"""
        SELECT ID,
                CASE WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students' 
                THEN 'Degree-Seeking' ELSE 'Non-Degree-Seeking' END AS STATUS
        FROM (
        SELECT STUDENT_ID AS ID,
                STP_PROGRAM_TITLE,
                ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY
                CASE WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students' THEN 0 ELSE 1 END) AS PROGRAM_RANK
        FROM STUDENT_ACAD_PROGRAMS_VIEW
        JOIN TERMS ON TERMS_ID = '{term}'
        WHERE STP_START_DATE < TERM_END_DATE
        AND COALESCE(STP_END_DATE, TERM_START_DATE) >= TERM_START_DATE
        ) AS X
        WHERE PROGRAM_RANK = 1
        """
        return query

    def appl_status(self, term = '2024FA'):
        query = f"""
        SELECT ID,
               CASE WHEN X.TERM_END_DATE < TERMS.TERM_START_DATE THEN 'Continuing/Returning'
               WHEN APPL_ADMIT_STATUS IN ('TR', 'PB') THEN 'Transfer-in'
               WHEN APPL_ADMIT_STATUS = 'FY' OR APPL_ADMIT_STATUS IS NULL THEN 'First-time'
               END AS STATUS
        FROM (
        SELECT APPL_APPLICANT AS ID,
                APPL_ADMIT_STATUS,
                TERM_END_DATE,
               ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS APPL_RANK
        FROM APPLICATIONS
        JOIN TERMS ON APPL_START_TERM = TERMS_ID
        WHERE APPL_DATE IS NOT NULL
        ) AS X
        JOIN TERMS ON TERMS_ID = '{term}'
        WHERE APPL_RANK = 1
        """
        return query

    def race_status(self):
        query = f"""
        SELECT ID,
                IPEDS_RACE_ETHNIC_DESC AS RACE
        FROM Z01_ALL_RACE_ETHNIC_W_FLAGS
        """
        return query

    def getCount_FT_UG_Men_original(self):
        prompt = """
        Enrollment as of the institution's official fall reporting date or as of October 15, 2024
        Full-time Undergraduate Students
        Reporting Reminders:
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        Even though Teacher Preparation certificate programs may require a bachelor's degree for admission, they are 
        considered subbaccalaureate undergraduate programs, and students in these programs are undergraduate students.
        """
        comments = """
        This is how I originally calculated the ftug men count.
        """
        query = """
        SELECT STTR_STUDENT,
                RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
                CASE
                    WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students' THEN 'Non-Degree Seeking'
                    WHEN FM.TERM = '2024FA' THEN CASE
                        WHEN STPR_ADMIT_STATUS = 'FY' THEN 'First-time'
                        WHEN STPR_ADMIT_STATUS = 'TR' THEN 'Transfer-in' END
                    ELSE 'Continuing/Returning' END AS STATUS
        FROM STUDENT_TERMS_VIEW
        JOIN PERSON ON STTR_STUDENT = PERSON.ID
        JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
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
                    WHERE rn = 1)
                    AS SAPV ON STUDENT_TERMS_VIEW.STTR_STUDENT = SAPV.STUDENT_ID
        LEFT JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STUDENT_TERMS_VIEW.STTR_STUDENT = FM.ID
        LEFT JOIN (SELECT DISTINCT STPR_STUDENT, STPR_ADMIT_STATUS
                   FROM (
                       SELECT   STPR_STUDENT,
                                STPR_ADMIT_STATUS,
                                ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                                ORDER BY STPR_ADMIT_STATUS) AS rn
                       FROM STUDENT_PROGRAMS_VIEW
                       WHERE STPR_ADMIT_STATUS IN ('FY', 'TR')
                       ) ranked
                       WHERE rn = 1)
            AS FIRST_ADMIT ON STUDENT_TERMS_VIEW.STTR_STUDENT = FIRST_ADMIT.STPR_STUDENT
        WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
        AND STUDENT_TERMS_VIEW.STTR_ACAD_LEVEL = 'UG'
        AND STUDENT_TERMS_VIEW.STTR_STUDENT_LOAD IN ('F', 'O')
        AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
        AND (GENDER = 'M'
            OR STTR_STUDENT IN
                    ('6189200',
                    '6189204',
                    '6189252',
                    '6186217',
                    '6190237',
                    '6190238',
                    '6190246',
                    '6189572',
                    '6189318',
                    '6189974',
                    '6189975',
                    '6189977',
                    '6187468',
                    '6189635',
                    '6190236',
                    '6189662',
                    '6189973'))
        """
        agg = lambda query: f"""
        SELECT RACE,
               [First-time],
               [Transfer-in],
               [Continuing/Returning],
               [Non-Degree Seeking]
        FROM (
        {query}
        )  AS X
        PIVOT (COUNT(STTR_STUDENT)
        FOR STATUS IN ([First-time], [Transfer-in], [Continuing/Returning], [Non-Degree Seeking])) as Y --Men
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.STTR_STUDENT = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Fall Enrollment",
                  "section": "Count by RE",
                  "page": "Full-time undergraduates",
                  "name": "FTUG Men (Original)",
                  "func_dict": {"Agg": agg, "Names": names},
                  "snapshot_term": "2024FA"
                  }
        self.save(**params)

    def getCount_FT_UG_Men_new1(self):
        prompt = """
        Enrollment as of the institution's official fall reporting date or as of October 15, 2024
        Full-time Undergraduate Students
        Reporting Reminders:
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        Even though Teacher Preparation certificate programs may require a bachelor's degree for admission, they are 
        considered subbaccalaureate undergraduate programs, and students in these programs are undergraduate students.
        """
        comments = """
        This is how I would compute it now.
        """
        query = f"""
        SELECT IPEDS_RACE.THEIR_DESC AS RACE,
        IPEDS_RACE.N,
        TARGET_STUDENTS.ID,
        TARGET_STUDENTS.STATUS
        FROM ({self.ipeds_races()}) AS IPEDS_RACE
        LEFT JOIN (
        SELECT STUDENTS.ID,
                RACE,
                CASE WHEN STU_PROGRAM.STATUS = 'Non-Degree-Seeking' THEN 'Non-degree/non-certificate-seeking'
                ELSE STU_APPL.STATUS END AS STATUS
        FROM (
        {self.enrolledStudents(level='UG', load='FT', gender='M')}
        ) AS STUDENTS
        JOIN (
        {self.race_status()}
        ) AS STU_RACE ON STUDENTS.ID = STU_RACE.ID
        JOIN (
        {self.deg_status()}
        ) AS STU_PROGRAM ON STUDENTS.ID = STU_PROGRAM.ID
        JOIN (
        {self.appl_status()} 
        ) AS STU_APPL ON STUDENTS.ID = STU_APPL.ID
        ) AS TARGET_STUDENTS ON IPEDS_RACE.OUR_DESC = TARGET_STUDENTS.RACE
        """
        self.print_table(query)
        agg = lambda query: f"""
        SELECT RACE,
               {self.status_str}      
        FROM (
        {query}
        )  AS X
        PIVOT (COUNT(ID)
        FOR STATUS IN ({self.status_str})) as Y --Men
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Fall Enrollment",
                  "section": "Count by RE",
                  "page": "Full-time undergraduates",
                  "name": "FTUG Men (New)",
                  "func_dict": {"Agg": agg, "Names": names},
                  "snapshot_term": "2024FA"
                  }
        self.save(**params)