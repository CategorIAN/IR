--(Begin 3)-------------------------------------------------------------------------------------------------------------
SELECT PROGRAM,
       STATE,
       COUNT(*) AS STUDENT_COUNT
FROM (
--(Begin 2)-------------------------------------------------------------------------------------------------------------
         SELECT STUDENT_ID,
                STUDENT_LAST_NAME,
                STUDENT_FIRST_NAME,
                PROGRAM,
                STATE
         FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
                  SELECT SAPV.STUDENT_ID,
                         SAPV.STUDENT_LAST_NAME,
                         SAPV.STUDENT_FIRST_NAME,
                         SAPV.STP_PROGRAM_TITLE         AS PROGRAM,
                         PAV.STATE,
                         ROW_NUMBER() OVER (PARTITION BY SAPV.STUDENT_ID
                             ORDER BY ADDRESS_ADD_DATE DESC) AS RANK
                    FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                    JOIN PERSON_ADDRESSES_VIEW AS PAV ON SAPV.STUDENT_ID = PAV.ID
                    JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                    WHERE STP_PROGRAM_TITLE IN ('Master of Accountancy', 'Master of Social Work')
                    AND STP_START_DATE < '2025-01-01'
                    AND (STP_END_DATE IS NULL OR STP_END_DATE >= '2024-01-01')
                    AND PAV.ADDRESS_TYPE = 'H'
--(End 1)---------------------------------------------------------------------------------------------------------------
              ) AS X
         WHERE RANK = 1
--(End 2)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY PROGRAM, STATE
--(End 3)---------------------------------------------------------------------------------------------------------------
ORDER BY PROGRAM, STATE



--(Begin 3)-------------------------------------------------------------------------------------------------------------
SELECT PROGRAM,
       STATE,
       COUNT(*) AS STUDENT_COUNT
FROM (
--(Begin 2)-------------------------------------------------------------------------------------------------------------
         SELECT ID,
                LAST_NAME,
                FIRST_NAME,
                PROGRAM,
                STATE
         FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
  SELECT PAV.ID,
         PAV.LAST_NAME,
         PAV.FIRST_NAME,
         AP.ACAD_PROGRAMS_ID,
         AP.ACPG_TITLE AS PROGRAM,
         PAV.STATE,
         ROW_NUMBER() OVER (PARTITION BY PAV.ID
                ORDER BY ADDRESS_ADD_DATE DESC) AS RANK
    FROM STUDENT_PROGRAMS AS STP
    JOIN PERSON_ADDRESSES_VIEW AS PAV
    ON left(STP.STUDENT_PROGRAMS_ID,7) = PAV.ID
    JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
    JOIN ACAD_PROGRAMS AS AP
    ON substring(STP.STUDENT_PROGRAMS_ID, 9, LEN(STP.STUDENT_PROGRAMS_ID)) = AP.ACAD_PROGRAMS_ID
    JOIN STPR_DATES ON STP.STUDENT_PROGRAMS_ID = STPR_DATES.STUDENT_PROGRAMS_ID AND STPR_DATES.POS = 1
    WHERE ACPG_TITLE IN ('Master of Accountancy', 'Master of Social Work')
    AND STPR_DATES.STPR_START_DATE < '2025-01-01'
    AND (STPR_DATES.STPR_END_DATE IS NULL OR STPR_DATES.STPR_END_DATE >= '2024-01-01')
    AND PAV.ADDRESS_TYPE = 'H'
--(End 1)---------------------------------------------------------------------------------------------------------------
              ) AS X
         WHERE RANK = 1
--(End 2)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY PROGRAM, STATE
--(End 3)---------------------------------------------------------------------------------------------------------------
ORDER BY PROGRAM, STATE


SELECT *
FROM STUDENT_PROGRAMS


SELECT DISTINCT STPR_TITLE
FROM STUDENT_PROGRAMS