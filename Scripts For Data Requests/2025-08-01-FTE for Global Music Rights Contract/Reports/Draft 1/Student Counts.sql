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