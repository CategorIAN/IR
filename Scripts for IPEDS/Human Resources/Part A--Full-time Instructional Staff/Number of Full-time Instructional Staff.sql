SELECT CREDIT_STATUS,
       [T] AS TENURED,
       [O] AS ON_TENURE_TRACK,
       [N] AS ANNUAL_CONTRACT
FROM (SELECT CREDIT_STATUS,
             PERSTAT_TENURE_TYPE,
             COUNT(*) AS COUNT
      FROM (SELECT PERSTAT_HRP_ID,
                   PERSON.LAST_NAME,
                   PERSON.FIRST_NAME,
                   PERSTAT_TENURE_TYPE,
                   CASE
                       WHEN FOR_CREDIT.FACULTY_ID IS NOT NULL AND NOT_FOR_CREDIT.FACULTY_ID IS NULL
                           THEN 'Exclusively_Credit'
                       WHEN FOR_CREDIT.FACULTY_ID IS NULL AND NOT_FOR_CREDIT.FACULTY_ID IS NOT NULL
                           THEN 'Exclusively_Not_Credit'
                       ELSE 'Combined_Credit_Not_Credit'
                       END AS CREDIT_STATUS

            FROM PERSTAT
                     JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                     JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                     LEFT JOIN (SELECT FACULTY_ID
                                FROM FACULTY_SECTIONS_DETAILS_VIEW
                                WHERE FAC_CS_LOAD > 0) AS FOR_CREDIT ON PERSTAT_HRP_ID = FOR_CREDIT.FACULTY_ID
                     LEFT JOIN (SELECT FACULTY_ID
                                FROM FACULTY_SECTIONS_DETAILS_VIEW
                                WHERE FAC_CS_LOAD IS NULL
                                   OR FAC_CS_LOAD = 0) AS NOT_FOR_CREDIT ON PERSTAT_HRP_ID = NOT_FOR_CREDIT.FACULTY_ID
            WHERE PERSTAT_END_DATE IS NULL
              AND PERSTAT_START_DATE <= '2024-11-01'
              AND PERSTAT_STATUS = 'FT'
              AND POS_CLASS = 'FAC'
            GROUP BY PERSTAT_HRP_ID,
                     PERSON.LAST_NAME,
                     PERSON.FIRST_NAME,
                     PERSTAT_TENURE_TYPE,
                     FOR_CREDIT.FACULTY_ID,
                     NOT_FOR_CREDIT.FACULTY_ID) AS X
      GROUP BY CREDIT_STATUS, PERSTAT_TENURE_TYPE) AS Y
PIVOT (
    SUM(COUNT) FOR PERSTAT_TENURE_TYPE IN ([T], [O], [N])
    ) AS Z