--(Begin 3)-------------------------------------------------------------------------------------------------------------
SELECT FORMAT(AVG(1.0 * FFUG_RETAINED), 'P') AS FFUG_RETENTION_2023FA_TO_2024FA
FROM (
--(Begin 2)-------------------------------------------------------------------------------------------------------------
         SELECT ID,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM SPT_STUDENT_ACAD_CRED
                                 WHERE STC_CURRENT_STATUS IN ('N', 'A')
                                   AND STC_TERM = '2024FA'
                                   AND STC_PERSON_ID = ID
                                 ) THEN 1
                    ELSE 0 END AS FFUG_RETAINED
         FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
                  SELECT APPL_APPLICANT                                                           AS ID,
                         APPL_START_TERM                                                          AS TERM,
                         ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS RANK
                  FROM Z01_APPLICATIONS AS AP
                       JOIN SPT_STUDENT_ACAD_CRED AS STC
                        ON AP.APPL_APPLICANT = STC.STC_PERSON_ID AND AP.APPL_START_TERM = STC.STC_TERM
                           JOIN ODS_TERMS ON APPL_START_TERM = TERMS_ID
                  WHERE STC_CURRENT_STATUS IN ('N', 'A')
                    AND STC_CRED_TYPE = 'INST'
                    AND APPL_START_TERM IS NOT NULL
                    AND (
                      --FFUG-----------------------
                      APPL_ADMIT_STATUS = 'FY'
                          AND APPL_STUDENT_LOAD_INTENT = 'F'
                          AND APPL_STUDENT_TYPE = 'UG'
                      )
--(End 1)---------------------------------------------------------------------------------------------------------------
              ) AS X
         WHERE RANK = 1
           AND TERM = '2023FA'
--(End 2)---------------------------------------------------------------------------------------------------------------
     ) AS X
--(End 3)---------------------------------------------------------------------------------------------------------------





SELECT *
FROM Z01_APPLICATIONS

SELECT *
FROM SPT_STUDENT_ACAD_CRED


SELECT DISTINCT STC_CRED_TYPE
FROM SPT_STUDENT_ACAD_CRED