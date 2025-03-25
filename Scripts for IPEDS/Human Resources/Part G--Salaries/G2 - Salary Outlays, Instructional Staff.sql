SELECT POS_EEO_RANK,
       [9 Months],
       [10 Months],
       [11 Months],
       [12 Months]
FROM (
SELECT  PPWG_ANNUALIZED_AMT,
        POS_EEO_RANK,
         CASE
           WHEN FIRST_NAME = 'Erin' and LAST_NAME = 'Butts' THEN '10 Months'
           WHEN FIRST_NAME = 'Zuleyha' and LAST_NAME = 'Inceoz' THEN '11 Months' --Not in Count
           WHEN FIRST_NAME = 'Melissa' and LAST_NAME = 'Lewis' THEN '11 Months'
           WHEN FIRST_NAME = 'Rachel' and LAST_NAME = 'Mattern' THEN '12 Months'
           WHEN FIRST_NAME = 'Molly' and LAST_NAME = 'Molloy' THEN '12 Months'
           WHEN FIRST_NAME = 'James' and LAST_NAME = 'Petrovich'  THEN '12 Months'
           WHEN FIRST_NAME = 'Katherine' and LAST_NAME = 'Pieper' THEN '11 Months'
           WHEN FIRST_NAME = 'Lauren' and LAST_NAME = 'Swant' THEN '12 Months'
           WHEN FIRST_NAME = 'Deanna' and LAST_NAME = 'Thompson' THEN '11 Months'
            ELSE '9 Months' END AS MONTHS_WORKED

FROM PERSON
JOIN (
    SELECT *
    FROM (SELECT PERSTAT_HRP_ID,
                 PERSTAT_PRIMARY_POS_ID,
                 ROW_NUMBER() OVER (PARTITION BY PERSTAT_HRP_ID
                     ORDER BY CASE
                                  WHEN PERSTAT_END_DATE IS NULL THEN 0
                                  ELSE 1 END,
               PERSTAT_END_DATE DESC) AS rn
          FROM PERSTAT
          WHERE PERSTAT_START_DATE <= '2024-11-01'
            AND PERSTAT_STATUS = 'FT'
            AND (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= (SELECT TOP 1 TERM_START_DATE
                                                                  FROM TERMS
                                                                  WHERE TERMS_ID = '2024FA'
                                                                  )))
    ranked
    WHERE rn = 1) as PERSTAT_X ON PERSON.ID = PERSTAT_X.PERSTAT_HRP_ID
JOIN POSITION ON PERSTAT_X.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
JOIN (
    SELECT *
    FROM (
    SELECT PPWG_HRP_ID,
           PPWG_POSITION_ID,
           PPWG_ANNUALIZED_AMT,
           PPWG_START_DATE,
           PPWG_END_DATE,
           ROW_NUMBER() OVER (PARTITION BY PPWG_HRP_ID
               ORDER BY CASE WHEN PPWG_END_DATE IS NULL THEN 0 ELSE 1 END, PPWG_END_DATE DESC) AS rn
            FROM PERPOSWG
            WHERE
            PPWG_START_DATE <
            (
              SELECT TOP 1 TERM_END_DATE
              FROM TERMS
              WHERE TERMS_ID = '2024FA'
            )
            AND PPWG_PAYCLASS_ID IS NOT NULL
    ) ranked
    WHERE rn = 1
    ) AS PERPOSWG_X ON
        PERSTAT_X.PERSTAT_HRP_ID = PERPOSWG_X.PPWG_HRP_ID
AND POSITION.POS_CLASS = 'FAC'
AND GENDER = 'M'
) AS X
PIVOT (SUM(PPWG_ANNUALIZED_AMT) FOR MONTHS_WORKED IN (
      [9 Months],
       [10 Months],
       [11 Months],
       [12 Months])) AS X


SELECT POS_EEO_RANK,
       [9 Months],
       [10 Months],
       [11 Months],
       [12 Months]
FROM (
SELECT  PPWG_ANNUALIZED_AMT,
        POS_EEO_RANK,
         CASE
           WHEN FIRST_NAME = 'Erin' and LAST_NAME = 'Butts' THEN '10 Months'
           WHEN FIRST_NAME = 'Zuleyha' and LAST_NAME = 'Inceoz' THEN '11 Months' --Not in Count
           WHEN FIRST_NAME = 'Melissa' and LAST_NAME = 'Lewis' THEN '11 Months'
           WHEN FIRST_NAME = 'Rachel' and LAST_NAME = 'Mattern' THEN '12 Months'
           WHEN FIRST_NAME = 'Molly' and LAST_NAME = 'Molloy' THEN '12 Months'
           WHEN FIRST_NAME = 'James' and LAST_NAME = 'Petrovich'  THEN '12 Months'
           WHEN FIRST_NAME = 'Katherine' and LAST_NAME = 'Pieper' THEN '11 Months'
           WHEN FIRST_NAME = 'Lauren' and LAST_NAME = 'Swant' THEN '12 Months'
           WHEN FIRST_NAME = 'Deanna' and LAST_NAME = 'Thompson' THEN '11 Months'
            ELSE '9 Months' END AS MONTHS_WORKED

FROM PERSON
JOIN (
    SELECT *
    FROM (SELECT PERSTAT_HRP_ID,
                 PERSTAT_PRIMARY_POS_ID,
                 ROW_NUMBER() OVER (PARTITION BY PERSTAT_HRP_ID
                     ORDER BY CASE
                                  WHEN PERSTAT_END_DATE IS NULL THEN 0
                                  ELSE 1 END,
               PERSTAT_END_DATE DESC) AS rn
          FROM PERSTAT
          WHERE PERSTAT_START_DATE <= '2024-11-01'
            AND PERSTAT_STATUS = 'FT'
            AND (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= (SELECT TOP 1 TERM_START_DATE
                                                                  FROM TERMS
                                                                  WHERE TERMS_ID = '2024FA'
                                                                  )))
    ranked
    WHERE rn = 1) as PERSTAT_X ON PERSON.ID = PERSTAT_X.PERSTAT_HRP_ID
JOIN POSITION ON PERSTAT_X.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
JOIN (
    SELECT *
    FROM (
    SELECT PPWG_HRP_ID,
           PPWG_POSITION_ID,
           PPWG_ANNUALIZED_AMT,
           PPWG_START_DATE,
           PPWG_END_DATE,
           ROW_NUMBER() OVER (PARTITION BY PPWG_HRP_ID
               ORDER BY CASE WHEN PPWG_END_DATE IS NULL THEN 0 ELSE 1 END, PPWG_END_DATE DESC) AS rn
            FROM PERPOSWG
            WHERE
            PPWG_START_DATE <
            (
              SELECT TOP 1 TERM_END_DATE
              FROM TERMS
              WHERE TERMS_ID = '2024FA'
            )
            AND PPWG_PAYCLASS_ID IS NOT NULL
    ) ranked
    WHERE rn = 1
    ) AS PERPOSWG_X ON
        PERSTAT_X.PERSTAT_HRP_ID = PERPOSWG_X.PPWG_HRP_ID
AND POSITION.POS_CLASS = 'FAC'
AND GENDER = 'F'
) AS X
PIVOT (SUM(PPWG_ANNUALIZED_AMT) FOR MONTHS_WORKED IN (
      [9 Months],
       [10 Months],
       [11 Months],
       [12 Months])) AS X