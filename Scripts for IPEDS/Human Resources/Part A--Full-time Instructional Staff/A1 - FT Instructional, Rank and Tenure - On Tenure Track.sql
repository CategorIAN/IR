------------------------------------------------------------------------------------------------------------------
SELECT IPEDS_RACE_ETHNIC_DESC AS Race_Ethnicity,
        [PRO] AS Professors,
        [ASO] AS Associate_Professors,
        [ASR] AS Assistant_Professors,
        [INS] AS Instructors
FROM (
SELECT       PERSTAT.PERSTAT_HRP_ID,
             IPEDS_RACE_ETHNIC_DESC,
             POS_EEO_RANK
      FROM PERSTAT
       JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
       JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
       JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSTAT_HRP_ID = RACE.ID
      WHERE (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= (
          SELECT TOP 1 TERM_START_DATE
          FROM TERMS
          WHERE TERMS_ID = '2024FA'
          ))
        AND PERSTAT_START_DATE <= '2024-11-01'
        AND PERSTAT_STATUS = 'FT'
        AND POS_CLASS = 'FAC'
        AND PERSTAT_TENURE_TYPE = 'O'
        AND GENDER = 'M') AS X
PIVOT (
    COUNT(PERSTAT_HRP_ID) FOR POS_EEO_RANK IN ([PRO], [ASO], [ASR], [INS])
) AS Y; --Men

------------------------------------------------------------------------------------------------------------------
SELECT IPEDS_RACE_ETHNIC_DESC AS Race_Ethnicity,
        [PRO] AS Professors,
        [ASO] AS Associate_Professors,
        [ASR] AS Assistant_Professors,
        [INS] AS Instructors
FROM (
SELECT       PERSTAT.PERSTAT_HRP_ID,
             IPEDS_RACE_ETHNIC_DESC,
             POS_EEO_RANK
      FROM PERSTAT
       JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
       JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
       JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSTAT_HRP_ID = RACE.ID
      WHERE (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= (
          SELECT TOP 1 TERM_START_DATE
          FROM TERMS
          WHERE TERMS_ID = '2024FA'
          ))
        AND PERSTAT_START_DATE <= '2024-11-01'
        AND PERSTAT_STATUS = 'FT'
        AND POS_CLASS = 'FAC'
        AND PERSTAT_TENURE_TYPE = 'O'
        AND GENDER = 'F') AS X
PIVOT (
    COUNT(PERSTAT_HRP_ID) FOR POS_EEO_RANK IN ([PRO], [ASO], [ASR], [INS])
) AS Y; --Women