--(Begin C3)------------------------------------------------------------------------------------------------------------
SELECT COHORTS.COHORT,
       GENDERS.GENDER,
       RACES.RACE,
       NON_COMPLETER,
       COMPLETER,
       TOTAL,
       GRADUATION_RATE
FROM (VALUES ('2015FA'), ('2016FA'), ('2017FA'), ('2018FA')) AS COHORTS(COHORT)
CROSS JOIN
    (VALUES ('Female'), ('Male')) AS GENDERS(GENDER)
CROSS JOIN
    (VALUES ('White'),
            ('Unknown'),
            ('Two or More Races'),
            ('Non-Resident Alien'),
            ('Hispanic/Latino'),
            ('Black or African American'),
            ('Asian')) AS RACES(RACE)
CROSS JOIN
    (VALUES ('Basketball')
            ) AS SPORTS(SPORT)
LEFT JOIN (
--(Begin C2)------------------------------------------------------------------------------------------------------------
    SELECT COHORT,
           GENDER,
           RACE,
           SPORT,
           SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NON_COMPLETER,
           SUM(SIX_YEAR_GRADUATED)                                 AS COMPLETER,
           COUNT(*)                                                AS TOTAL,
           AVG(1.0 * SIX_YEAR_GRADUATED)                           AS GRADUATION_RATE
    FROM (
--(Begin C1)------------------------------------------------------------------------------------------------------------
             SELECT DISTINCT AW_TERM                     AS COHORT,
                             SA_STUDENT_ID               AS ID,
                             CASE
                                 WHEN PERSON.GENDER = 'F' THEN 'Female'
                                 WHEN GENDER = 'M'
                                     THEN 'Male' END     AS GENDER,
                             RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
                             CASE
                                 WHEN (AW_DESCRIPTION LIKE '%Basketball%' OR
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
                                 END                     AS SPORT,
                             CASE
                                 WHEN EXISTS (SELECT 1
                                              FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                              WHERE STUDENT_ID = SA_STUDENT_ID
                                                AND STP_CURRENT_STATUS = 'Graduated'
                                                AND STP_END_DATE >= FM.TERM_START_DATE
                                                AND STP_END_DATE < DATEADD(YEAR, 6, FM.TERM_START_DATE))
                                     THEN 1
                                 ELSE 0 END              AS SIX_YEAR_GRADUATED
             FROM (
--(Begin A2)--------------------------------------------------------------------------------
                      SELECT AW_TERM, SA_AWARD, SA_STUDENT_ID, AW_DESCRIPTION
                      FROM (
--(Begin A1)--------------------------------------------------------------------------------
                               SELECT '2015FA' AS AW_TERM, *
                               FROM F15_AWARD_LIST
                               UNION
                               SELECT '2016FA' AS AW_TERM, *
                               FROM F16_AWARD_LIST
                               UNION
                               SELECT '2017FA' AS AW_TERM, *
                               FROM F17_AWARD_LIST
                               UNION
                               SELECT '2018FA' AS AW_TERM, *
                               FROM F18_AWARD_LIST
--(End A1)---------------------------------------------------------------------------------
                           ) AS X
                               JOIN AWARDS ON X.SA_AWARD = AWARDS.AW_ID
                               JOIN AWARD_CATEGORIES AS AC ON AWARDS.AW_CATEGORY = AC.AC_ID
                      WHERE SA_ACTION = 'A'
                        AND AC_DESCRIPTION = 'Athletic Grants'
--(End A2)----------------------------------------------------------------------------------
                  ) AS AL
                      JOIN PERSON ON AL.SA_STUDENT_ID = PERSON.ID
                      JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
                      JOIN (
--(Begin B2)-------------------------------------------------------------------------------
                 SELECT ID, TERM, TERM_START_DATE
                 FROM (
--(Begin B1)-------------------------------------------------------------------------------
                          SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                          APPL_START_TERM                                                          AS TERM,
                                          TERM_START_DATE,
                                          ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                          FROM APPLICATIONS AS AP
                                   JOIN STUDENT_ACAD_CRED AS AC
                                        ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND
                                           AP.APPL_START_TERM = AC.STC_TERM
                                   JOIN STC_STATUSES AS STAT
                                        ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                   JOIN TERMS ON APPL_START_TERM = TERMS_ID
                          WHERE APPL_DATE IS NOT NULL
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                            AND STC_STATUS IN ('A', 'N')
                            AND STC_CRED_TYPE IN ('INST')
--(End B1)----------------------------------------------------------------------------------
                      ) AS X
                 WHERE TERM_ORDER = 1
--(End B2)----------------------------------------------------------------------------------
             ) AS FM ON PERSON.ID = FM.ID AND AW_TERM = FM.TERM
--(End C1)-------------------------------------------------------------------------------------------------------------
         ) AS X
    GROUP BY COHORT, GENDER, RACE, SPORT
--(End C2)-------------------------------------------------------------------------------------------------------------
) AS X
ON COHORTS.COHORT = X.COHORT
AND GENDERS.GENDER = X.GENDER
AND RACES.RACE = X.RACE
AND SPORTS.SPORT = X.SPORT
--(End C2)-------------------------------------------------------------------------------------------------------------
ORDER BY COHORT, GENDER, RACE
