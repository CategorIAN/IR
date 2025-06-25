
--(Begin 1)------------------------------------------------------------------------------------------------------------
SELECT  DISTINCT SA_STUDENT_ID,
        PERSON.GENDER,
                RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
                CASE WHEN (AW_DESCRIPTION LIKE '%Basketball%' OR
                           AW_DESCRIPTION LIKE '%BB%') THEN 'Basketball'
                    WHEN AW_DESCRIPTION LIKE '%Cross Country%' THEN 'Cross Country'
                    WHEN AW_DESCRIPTION LIKE '%Football%' THEN 'Football'
                    WHEN AW_DESCRIPTION LIKE '%Golf%' THEN 'Golf'
                    WHEN AW_DESCRIPTION LIKE '%Soccer%' THEN 'Soccer'
                    WHEN AW_DESCRIPTION LIKE '%Softball%' THEN 'Softball'
                    WHEN AW_DESCRIPTION LIKE '%Track%' THEN 'Track and Field'
                    WHEN AW_DESCRIPTION LIKE '%Volleyball%' THEN 'Volleyball'
                    WHEN AW_DESCRIPTION LIKE '%Cheer%' THEN 'Cheerleading'
                    WHEN AW_DESCRIPTION LIKE '%Dance%' THEN 'Dance'
                END AS SPORT
FROM F24_AWARD_LIST AS AL
JOIN AWARDS ON AL.SA_AWARD = AWARDS.AW_ID
JOIN AWARD_CATEGORIES AS AC ON AWARDS.AW_CATEGORY = AC.AC_ID
JOIN PERSON ON AL.SA_STUDENT_ID = PERSON.ID
LEFT JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
WHERE SA_ACTION = 'A'
AND AC_DESCRIPTION = 'Athletic Grants'
--(End 1)--------------------------------------------------------------------------------------------------------------

SELECT *
FROM Z01_ALL_RACE_ETHNIC_W_FLAGS