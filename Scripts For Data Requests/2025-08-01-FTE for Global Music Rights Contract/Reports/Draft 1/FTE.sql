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
--(End 1)---------------------------------------------------------------------------------------------------------------
              ) AS X
--(End 2)---------------------------------------------------------------------------------------------------------------
     ) AS X
--(End 3)---------------------------------------------------------------------------------------------------------------
