from Reports import Reports
from IPEDS import IPEDS
import os
from pathlib import Path
from tabulate import tabulate
BASE_DIR = Path(__file__).resolve()

class IPEDS_IC (IPEDS):
    def __init__(self):
        super().__init__(folder='IPEDS_IC', report="2025-09-15-Update IPEDS IC Survey")

    '''
    Status: Completed
    '''
    def getStudentEnrollment_5(self):
        prompt = f"""
        5. Does your institution enroll any of the following types of students?
        Include all levels offered by your institution, even if there are no students currently enrolled at that level.
        Responses to these questions determine which screens will be generated for reporting academic year tuition 
        charges, and for reporting Fall Enrollment during the Spring collection. Additionally, checking Yes for 
        full-time, first-time, degree/certificate-seeking undergraduate students determines that your institution must 
        report cost of attendance data (on the Cost I component) and Student Financial Aid data for these students.
        """
        query_0 = f"""
                SELECT STUDENTS.ID,
                CASE WHEN STV.STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time' ELSE 'Part-Time' END AS LOAD,
                CASE WHEN STP_ACAD_LEVEL = 'UG' THEN 1 ELSE 0 END AS [Undergraduate],
                CASE WHEN (STUDENT_ADMIT.STATUS = 'FY') AND (STP_PROGRAM_TITLE != 'Non-Degree Seeking Students') 
                        THEN 1 ELSE 0 END AS [First-time, degree-seeking],
                CASE WHEN STP_ACAD_LEVEL = 'GR' THEN 1 ELSE 0 END AS [Graduate]
        FROM ({self.students()}) AS STUDENTS
        LEFT JOIN (
        SELECT *,
                ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
        FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        WHERE STP_CURRENT_STATUS = 'Active'
        ) AS STUDENT_CURRENT_PROGRAM ON STUDENTS.ID = STUDENT_CURRENT_PROGRAM.STUDENT_ID AND STUDENT_CURRENT_PROGRAM.RANK = 1
        JOIN STUDENT_TERMS_VIEW AS STV ON STUDENTS.ID = STV.STTR_STUDENT AND STTR_TERM = '2025FA'
        LEFT JOIN (
        SELECT DISTINCT APPL_APPLICANT AS ID,
                APPL_ADMIT_STATUS AS STATUS,
               ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE DESC) AS RANK
        FROM APPLICATIONS AS AP 
        JOIN STUDENT_ACAD_CRED AS STC ON AP.APPL_APPLICANT = STC.STC_PERSON_ID AND AP.APPL_START_TERM = STC.STC_TERM
        LEFT JOIN STC_STATUSES AS STAT ON STC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN TERMS ON APPL_START_TERM = TERMS_ID
        WHERE APPL_DATE IS NOT NULL
        AND STC_STATUS IN ('N', 'A')
        AND STC_CRED_TYPE = 'INST'
        AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
        ) AS STUDENT_ADMIT ON STUDENTS.ID = STUDENT_ADMIT.ID AND STUDENT_ADMIT.RANK = 1
        """
        agg = lambda query: f"""
        --(Begin 2)----------------------------------------------------------------------------------------------------
        SELECT LOAD,
                MAX([Undergraduate]) AS [Undergraduate],
                MAX([First-time, degree-seeking]) AS [First-time, degree-seeking],
                MAX([Graduate]) AS [Graduate]
        FROM (
        --(Begin 1)----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)------------------------------------------------------------------------------------------------------
        ) AS X
        GROUP BY LOAD
        --(End 2)------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        --(Begin 2)----------------------------------------------------------------------------------------------------
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        --(Begin 1)----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)------------------------------------------------------------------------------------------------------
        ) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        params = {"prompt": prompt,
                  "query": query_0,
                  "section": "Section 1 - Header information",
                  "page": "Part B - Student Enrollment",
                  "name": "Question 5",
                  "func_dict": {"Agg": agg, "Names": names}}
        self.save(**params)

    '''
    Status: Completed
    '''
    def getStudentEnrollment_7(self):
        prompt = """
        7. For Fall 2019, did your institution have any full-time, first-time degree/certificate-seeking students 
        enrolled in programs at the baccalaureate level or below?
        If you answer Yes to this question, you will be required to provide Graduation Rates data for the 2019-20 
        cohort in the winter collection. If you answer No to this question, indicate the reason you are not required to
         report Graduation Rates for the cohort year requested.
        If you reported any full-time, first-time degree/certificate-seeking undergraduates on the 2019-20 Enrollment 
        survey, the data will be preloaded below.
        """
        query_0 = f"""
                SELECT STUDENTS.ID,
                CASE WHEN STV.STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time' ELSE 'Part-Time' END AS LOAD,
                CASE WHEN STP_ACAD_LEVEL = 'UG' THEN 1 ELSE 0 END AS [Undergraduate],
                CASE WHEN (STUDENT_ADMIT.STATUS = 'FY') AND (STP_PROGRAM_TITLE != 'Non-Degree Seeking Students') 
                        THEN 1 ELSE 0 END AS [First-time, degree-seeking]
        FROM ({self.students('2019FA')}) AS STUDENTS
        LEFT JOIN (
        SELECT SAPV.*,
                ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY STP_START_DATE DESC) AS RANK
        FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        JOIN TERMS ON TERMS_ID = '2019FA'
        WHERE STP_START_DATE <= TERMS.TERM_END_DATE AND COALESCE(STP_END_DATE, GETDATE()) >= TERMS.TERM_START_DATE
        ) AS STUDENT_CURRENT_PROGRAM ON STUDENTS.ID = STUDENT_CURRENT_PROGRAM.STUDENT_ID AND STUDENT_CURRENT_PROGRAM.RANK = 1
        JOIN STUDENT_TERMS_VIEW AS STV ON STUDENTS.ID = STV.STTR_STUDENT AND STTR_TERM = '2019FA'
        LEFT JOIN (
        SELECT DISTINCT APPL_APPLICANT AS ID,
                APPL_ADMIT_STATUS AS STATUS,
               ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE DESC) AS RANK
        FROM APPLICATIONS AS AP 
        JOIN STUDENT_ACAD_CRED AS STC ON AP.APPL_APPLICANT = STC.STC_PERSON_ID AND AP.APPL_START_TERM = STC.STC_TERM
        LEFT JOIN STC_STATUSES AS STAT ON STC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        JOIN TERMS ON APPL_START_TERM = TERMS_ID
        WHERE APPL_DATE IS NOT NULL
        AND STC_STATUS IN ('N', 'A')
        AND STC_CRED_TYPE = 'INST'
        AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
        ) AS STUDENT_ADMIT ON STUDENTS.ID = STUDENT_ADMIT.ID AND STUDENT_ADMIT.RANK = 1
        """
        agg = lambda query: f"""
        --(Begin 2)----------------------------------------------------------------------------------------------------
        SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END AS EXIST
        FROM (
        --(Begin 1)----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)------------------------------------------------------------------------------------------------------
        ) AS X
        WHERE LOAD = 'Full-Time'
        AND [First-time, degree-seeking] = 1
        AND [Undergraduate] = 1
        --(End 2)------------------------------------------------------------------------------------------------------
        """
        names = lambda query: f"""
        --(Begin 2)----------------------------------------------------------------------------------------------------
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM (
        --(Begin 1)----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)------------------------------------------------------------------------------------------------------
        ) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME, FIRST_NAME
        """
        params = {"prompt": prompt,
                  "query": query_0,
                  "section": "Section 1 - Header information",
                  "page": "Part B - Student Enrollment",
                  "name": "Question 7",
                  "func_dict": {"Agg": agg, "Names": names}}
        self.save(**params)

    '''
    Status: Completed
    '''
    def getDisability_9(self):
        '''

        '''
        prompt = """
        9. Please indicate the percentage of all undergraduate students enrolled during Fall 2024 who were formally 
        registered as students with disabilities with the institution's office of disability services 
        (or the equivalent office).
        """
        comments = """
        Kelly told me there were 238 students registered with disabilities for the 2024-25 academic year.
        """
        query = f"""
        SELECT FORMAT(1.0 * 238 / COUNT(*), 'P') AS DISABILITY_PERCENTAGE
        FROM ({self.students('2024FA')}) AS STUDENTS
        """
        params = {
                  "prompt": prompt,
                  "query": query,
                  "section": "Section 2 - Institutional Characteristics",
                  "page": "Part B - Disability",
                  "name": "Question 9",
                  "func_dict": None,
                  "comments": comments
        }
        self.save(**params)









