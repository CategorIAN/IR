--(Begin 2)------------------------------------------------------------------------------------------------------------
SELECT TERM,
       STATUS,
       COUNT(*) AS COUNT
FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT TERMS.TERMS_ID                                                  AS TERM,
                         TERMS.TERM_START_DATE,
                         PERSTAT.PERSTAT_HRP_ID,
                         PERSON.LAST_NAME,
                         PERSON.FIRST_NAME,
                         CASE WHEN PERSTAT.PERSTAT_STATUS = 'FT' THEN 'FT' ELSE 'PT' END AS STATUS
         FROM TERMS
                  CROSS JOIN PERSTAT
                  JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                  JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
           AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND (POSITION.POS_CLASS != 'FAC' OR POSITION.POS_CLASS IS NULL)
           AND (POSITION.POS_RANK != 'A' OR POSITION.POS_RANK IS NULL)
           AND (POSITION.POS_EEO_RANK != 'INS' OR POSITION.POS_EEO_RANK IS NULL)
           AND PERSTAT.PERSTAT_STATUS != 'STU'
           AND POSITION.POS_DEPT = 'SWK'
--(End 1)--------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, STATUS, TERM_START_DATE
--(End 2)--------------------------------------------------------------------------------------------------------------
ORDER BY TERM_START_DATE