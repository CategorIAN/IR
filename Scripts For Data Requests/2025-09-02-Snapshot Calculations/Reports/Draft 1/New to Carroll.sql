--(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT ID,
       TYPE,
       TERM
FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT APPL_APPLICANT                                                                              AS ID,
                         STUDENT_TYPES.STT_DESC AS TYPE,
                         APPL_START_TERM                                                                             AS TERM,
                         ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT, APPL_STUDENT_TYPE ORDER BY TERM_START_DATE) AS RANK
         FROM APPLICATIONS AS AP
                  JOIN STUDENT_ACAD_CRED AS AC
                       ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                  JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                  JOIN STUDENT_TERMS_VIEW AS STV
                       ON AP.APPL_APPLICANT = STV.STTR_STUDENT AND APPL_START_TERM = STV.STTR_TERM
                  JOIN TERMS ON APPL_START_TERM = TERMS_ID
                   LEFT JOIN STUDENT_TYPES ON APPL_STUDENT_TYPE = STUDENT_TYPES_ID
         WHERE APPL_DATE IS NOT NULL
           AND STC_STATUS IN ('A', 'N')
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
WHERE RANK = 1
AND TERM IN ('2024FA', '2024SU')
--(End 2)--------------------------------------------------------------------------------------------------------------
ORDER BY TERM, TYPE