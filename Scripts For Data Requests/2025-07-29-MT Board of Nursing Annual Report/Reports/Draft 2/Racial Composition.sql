--(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT RACE,
       FORMAT(1.0 * COUNT(*) / TOTAL, 'P') AS [PERCENT]
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT STPR_STUDENT,
                                CASE WHEN ALIEN_STATUS_DESC = 'Non-resident Alien' THEN 'Non-resident Alien'
        WHEN PERSON_ETHNIC_1_DESC = 'Hispanic/Latino' THEN 'Hispanic/Latino'
        WHEN PERSON_RACE_2 IS NOT NULL THEN 'Two or More Races'
        ELSE COALESCE(PERSON_RACE_1_DESC, 'Unknown') END AS RACE,
                            COUNT(*) OVER () AS TOTAL
         FROM SPT_STUDENT_PROGRAMS AS SP
          JOIN SPT_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
          JOIN Z01_PERSON AS PERSON ON SP.STPR_STUDENT = PERSON.ID
         LEFT JOIN SPT_FOREIGN_PERSON ON PERSON.ID = FOREIGN_PERSON_ID
         WHERE ACPG_TITLE IN ('Nursing', 'Accelerated Nursing')
           AND SP.START_DATE <= '2024-07-01'
           AND COALESCE(SP.END_DATE, GETDATE()) >= '2024-07-01'
           AND CURRENT_STATUS_DESC != 'Did Not Enroll'
           AND (CURRENT_STATUS_DESC NOT IN ('Not Returned', 'Changed Program') OR CURRENT_STATUS_DATE > '2024-07-01')
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY RACE, TOTAL
--(End 2)---------------------------------------------------------------------------------------------------------------