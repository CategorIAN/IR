--(Begin 2)------------------------------------------------------------------------------------------------------------
         SELECT TERM,
                ID,
                LAST_NAME,
                FIRST_NAME,
                SUM(CREDITS) AS ADJUNCT_CREDIT_LOAD
         FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
                  SELECT DISTINCT TERMS.TERMS_ID         AS TERM,
                                  TERM_START_DATE,
                                  PERSTAT.PERSTAT_HRP_ID AS ID,
                                  PERSON.LAST_NAME,
                                  PERSON.FIRST_NAME,
                                  CS.COURSE_SECTIONS_ID,
                                  CS_BILLING_CREDITS     AS CREDITS
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
                    AND POSITION.POS_RANK = 'A'
                    AND POSITION.POS_DEPT = 'SWK'
                    AND CS_BILLING_CREDITS IS NOT NULL
--(End 1)--------------------------------------------------------------------------------------------------------------
              ) AS X
         GROUP BY TERM, ID, LAST_NAME, FIRST_NAME, TERM_START_DATE
--(End 2)--------------------------------------------------------------------------------------------------------------