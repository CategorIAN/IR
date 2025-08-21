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
--(End 1)---------------------------------------------------------------------------------------------------------------
              ) AS X
--(End 2)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY STATUS
--(End 3)---------------------------------------------------------------------------------------------------------------





SELECT *
FROM ODS_STUDENT_TERMS

SELECT *
FROM SPT_STUDENT_ACAD_CRED