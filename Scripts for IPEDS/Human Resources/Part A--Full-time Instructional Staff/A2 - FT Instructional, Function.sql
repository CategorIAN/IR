SELECT CREDIT_STATUS,
       [T] AS TENURED,
       [O] AS ON_TENURE_TRACK,
       [N] AS ANNUAL_CONTRACT
FROM (
SELECT PERSTAT_HRP_ID,
       PERSTAT_TENURE_TYPE,
       CASE
           WHEN FOR_CREDIT = 1 AND NOT_FOR_CREDIT = 0 THEN 'Exclusively credit'
            WHEN FOR_CREDIT = 0 AND NOT_FOR_CREDIT = 1 THEN 'Exclusively not-for-credit'
            ELSE 'Combined credit/not-for-credit' END AS CREDIT_STATUS
FROM (SELECT PERSTAT_HRP_ID,
             PERSTAT_TENURE_TYPE,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM FACULTY_SECTIONS_DETAILS_VIEW
                    WHERE FACULTY_ID = PERSTAT_HRP_ID
                    AND FAC_CS_LOAD > 0
                ) THEN 1 ELSE 0 END AS FOR_CREDIT,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM FACULTY_SECTIONS_DETAILS_VIEW
                    WHERE FACULTY_ID = PERSTAT_HRP_ID
                        AND (FAC_CS_LOAD IS NULL
                       OR FAC_CS_LOAD = 0)
                ) THEN 1 ELSE 0 END AS NOT_FOR_CREDIT

            FROM PERSTAT
             JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
             JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
            WHERE PERSTAT_END_DATE IS NULL
              AND PERSTAT_START_DATE <= '2024-11-01'
              AND PERSTAT_STATUS = 'FT'
              AND POS_CLASS = 'FAC') AS X) AS X
PIVOT (
    COUNT(PERSTAT_HRP_ID) FOR PERSTAT_TENURE_TYPE IN ([T], [O], [N])
    ) AS X