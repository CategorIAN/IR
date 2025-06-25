--(Begin C1)------------------------------------------------------------------------------------------------------------
SELECT DISTINCT AW_TERM,
       SA_STUDENT_ID AS ID,
       PERSON.GENDER,
       RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
        CASE WHEN EXISTS (
        SELECT 1
        FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
        WHERE STUDENT_ID = SA_STUDENT_ID
        AND STP_CURRENT_STATUS = 'Graduated'
        AND STP_END_DATE >= TERM_START_DATE
        AND STP_END_DATE < DATEADD(YEAR, 6, TERM_START_DATE)
    ) THEN 1 ELSE 0 END AS SIX_YEAR_GRADUATED
FROM (
--(Begin A2)--------------------------------------------------------------------------------
SELECT AW_TERM, SA_AWARD, SA_STUDENT_ID, AW_DESCRIPTION
FROM (
--(Begin A1)--------------------------------------------------------------------------------
         SELECT '2018FA' AS AW_TERM, *
         FROM F18_AWARD_LIST
--(End A1)----------------------------------------------------------------------------------
     ) AS X
JOIN AWARDS ON X.SA_AWARD = AWARDS.AW_ID
WHERE SA_ACTION = 'A'
AND AW_TYPE = 'F'
--(End A2)----------------------------------------------------------------------------------
) AS AL
JOIN PERSON ON AL.SA_STUDENT_ID = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
JOIN (
--(Begin B2)--------------------------------------------------------------------------------
SELECT ID, TERM, TERM_START_DATE
FROM (
--(Begin B1)-------------------------------------------------------------------------------
SELECT DISTINCT APPL_APPLICANT     AS ID,
APPL_START_TERM                                                          AS TERM,
TERM_START_DATE,
ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
FROM APPLICATIONS AS AP
JOIN STUDENT_ACAD_CRED AS AC
ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
JOIN TERMS ON APPL_START_TERM = TERMS_ID
WHERE APPL_DATE IS NOT NULL
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
AND STC_STATUS IN ('A', 'N')
AND STC_CRED_TYPE IN ('INST')
--(End B1)---------------------------------------------------------------------------------
          ) AS X
    WHERE TERM_ORDER = 1
--(End B2)----------------------------------------------------------------------------------
) AS FM ON PERSON.ID = FM.ID AND AW_TERM = FM.TERM
--(End C1)--------------------------------------------------------------------------------------------------------------
