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
                    AND (STUDENT_PRIVACY_FLAG != 'Demo Student' OR STUDENT_PRIVACY_FLAG IS NULL)
--(End 1)---------------------------------------------------------------------------------------------------------------
              ) AS X
         WHERE RANK = 1
--(End 2)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY PROGRAM, STATE
--(End 3)---------------------------------------------------------------------------------------------------------------
ORDER BY PROGRAM, STATE
