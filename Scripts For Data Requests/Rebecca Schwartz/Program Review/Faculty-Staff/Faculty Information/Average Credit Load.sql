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

