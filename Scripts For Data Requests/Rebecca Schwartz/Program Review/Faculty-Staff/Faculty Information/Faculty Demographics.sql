--(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT
                PERSTAT.PERSTAT_HRP_ID,
                PERSON.LAST_NAME,
                PERSON.FIRST_NAME,
                COALESCE(PERSON.GENDER, 'Unknown') AS GENDER,
                RACE.IPEDS_RACE_ETHNIC_DESC AS RACE
         FROM TERMS
          CROSS JOIN PERSTAT
          JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
          JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
          JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
          LEFT JOIN (VALUES
            ('T', 'Tenured'), ('O', 'On Tenure Track'), ('N', 'Not Tenure Track'))
            AS TENURE_STATUS(ID, NAME) ON PERSTAT_TENURE_TYPE = TENURE_STATUS.ID
          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
            AND TERMS.TERM_END_DATE < '2025-06-01'
            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
            AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
            AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND POSITION.POS_CLASS = 'FAC'
--(End 1)--------------------------------------------------------------------------------------------------------------
ORDER BY LAST_NAME, FIRST_NAME