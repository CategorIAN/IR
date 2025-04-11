--(Begin 4)-----------------------------------------------------------------------------------------
SELECT 'All' AS COUNTY,
        COUNT(DISTINCT STUDENT_ID) AS STUDENT_COUNT_2024FA
FROM STUDENT_ENROLLMENT_VIEW AS SEV
WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
AND  (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
AND ENROLL_TERM = '2024FA'
UNION
--(Begin 3)-----------------------------------------------------------------------------------------
SELECT COUNTY,
       SUM(IN_COUNTY) AS STUDENT_COUNT_2024FA
FROM (
--(Begin 2)-----------------------------------------------------------------------------------------
SELECT CNTY_DESC  AS COUNTY,
CASE WHEN CNTY_DESC = STUDENT_COUNTY.COUNTY THEN 1 ELSE 0 END AS IN_COUNTY
FROM COUNTIES
CROSS JOIN (
--(Begin 1)-----------------------------------------------------------------------------------------
SELECT DISTINCT STUDENT_ID,
       CNTY_DESC AS COUNTY
FROM STUDENT_ENROLLMENT_VIEW AS SEV
JOIN PERSON_ADDRESSES_VIEW AS PAV ON SEV.STUDENT_ID = PAV.ID
JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
JOIN COUNTIES ON ADDRESS.COUNTY = COUNTIES_ID
WHERE ADDRESS_TYPE = 'H'
AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
AND ENROLL_TERM = '2024FA'
--(End 1)-----------------------------------------------------------------------------------------
) AS STUDENT_COUNTY
WHERE CNTY_DESC IN ('Cascade', 'Glacier', 'Lewis and Clark', 'Pondera', 'Teton', 'Toole')
--(End 2)-----------------------------------------------------------------------------------------
) AS X
GROUP BY COUNTY
--(End 3)-----------------------------------------------------------------------------------------
--(End 4)-----------------------------------------------------------------------------------------
