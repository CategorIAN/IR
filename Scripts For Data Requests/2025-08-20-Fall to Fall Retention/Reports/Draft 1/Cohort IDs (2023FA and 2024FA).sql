--(Begin 2)-------------------------------------------------------------------------------------------------------------
         SELECT ID,
                TERM AS COHORT_TERM
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
           AND TERM IN ('2023FA', '2024FA')
--(End 2)---------------------------------------------------------------------------------------------------------------
