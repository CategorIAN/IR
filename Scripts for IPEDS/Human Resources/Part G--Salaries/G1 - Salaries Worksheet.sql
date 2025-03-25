SELECT  POS_EEO_RANK,
        COUNT(*) AS NINE_MONTHS

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
WHERE (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= (
          SELECT TOP 1 TERM_START_DATE
          FROM TERMS
          WHERE TERMS_ID = '2024FA'
          ))
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS = 'FAC'
AND GENDER = 'M'
GROUP BY POS_EEO_RANK --Men
----------------------------------------------------------------------------------------------------------------------
SELECT  POS_EEO_RANK,
        COUNT(*) AS NINE_MONTHS

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
WHERE (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= (
          SELECT TOP 1 TERM_START_DATE
          FROM TERMS
          WHERE TERMS_ID = '2024FA'
          ))
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS = 'FAC'
AND GENDER = 'F'
GROUP BY POS_EEO_RANK --Women

----------------------------------------------------------------------------------------------------------------------
SELECT POS_EEO_RANK,
       [9 Months],
       [10 Months],
       [11 Months],
       [12 Months]
FROM (
SELECT ID,
       POSITION.POS_EEO_RANK,
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

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
WHERE (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= (
          SELECT TOP 1 TERM_START_DATE
          FROM TERMS
          WHERE TERMS_ID = '2024FA'
          ))
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS = 'FAC'
AND GENDER = 'M'
) AS X
PIVOT (COUNT(ID) FOR MONTHS_WORKED IN (
           [9 Months],
       [10 Months],
       [11 Months],
       [12 Months]
        )) AS X

SELECT POS_EEO_RANK,
       [9 Months],
       [10 Months],
       [11 Months],
       [12 Months]
FROM (
SELECT ID,
       LAST_NAME,
       POSITION.POS_EEO_RANK,
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

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
WHERE (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= (
          SELECT TOP 1 TERM_START_DATE
          FROM TERMS
          WHERE TERMS_ID = '2024FA'
          ))
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS = 'FAC'
AND GENDER = 'F'
) AS X
PIVOT (COUNT(ID) FOR MONTHS_WORKED IN (
           [9 Months],
       [10 Months],
       [11 Months],
       [12 Months]
        )) AS X


SELECT *
FROM (
SELECT *
FROM (
SELECT ID,
       POSITION.POS_EEO_RANK,
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

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
WHERE (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= (
          SELECT TOP 1 TERM_START_DATE
          FROM TERMS
          WHERE TERMS_ID = '2024FA'
          ))
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS = 'FAC'
AND GENDER = 'F') AS X
EXCEPT
(
    SELECT  ID,
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

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
JOIN PERPOSWG ON PERSTAT.PERSTAT_HRP_ID = PPWG_HRP_ID AND PERSTAT_PRIMARY_POS_ID = PERPOSWG.PPWG_POSITION_ID
WHERE (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= (
          SELECT TOP 1 TERM_START_DATE
          FROM TERMS
          WHERE TERMS_ID = '2024FA'
          ))
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POSITION.POS_CLASS = 'FAC'
AND GENDER = 'F'
AND PPWG_PAYCLASS_ID IS NOT NULL
AND (
    PPWG_END_DATE IS NULL
    OR PPWG_END_DATE > (
          SELECT TOP 1 TERM_START_DATE
          FROM TERMS
          WHERE TERMS_ID = '2024FA'
          )
    )
)) AS X JOIN PERPOSWG ON X.ID = PPWG_HRP_ID


