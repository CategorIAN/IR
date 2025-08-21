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