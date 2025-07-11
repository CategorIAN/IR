--(Begin 2)------------------------------------------------------------------------------------------------------------
SELECT PERSTAT_HRP_ID,
       LAST_NAME,
       FIRST_NAME,
       STUDENT_GENDER,
       COUNT(*) AS COUNT
FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT PERSTAT.PERSTAT_HRP_ID,
                         PERSON.LAST_NAME,
                         PERSON.FIRST_NAME,
                         SEV.STUDENT_ID,
                         CASE
                             WHEN SEV.STUDENT_GENDER = 'M' THEN 'Male'
                             WHEN SEV.STUDENT_GENDER = 'F' THEN 'Female'
                             ELSE 'Unknown' END AS STUDENT_GENDER
         FROM TERMS
                  CROSS JOIN PERSTAT
                  JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
                  JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
                 JOIN FACULTY_SECTIONS_DETAILS_VIEW AS FS
                    ON PERSTAT.PERSTAT_HRP_ID = FS.FACULTY_ID AND TERMS.TERMS_ID = FS.CS_TERM
                    JOIN COURSE_SECTIONS_DETAILS_VIEW AS CS
                    ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
                JOIN STUDENT_ENROLLMENT_VIEW AS SEV
                    ON CS.COURSE_SECTIONS_ID = SEV.SECTION_COURSE_SECTION_ID
         WHERE TERMS.TERM_START_DATE >= '2019-08-01'
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND PERSTAT_START_DATE <= TERMS.TERM_END_DATE
           AND (PERSTAT_END_DATE >= TERMS.TERM_START_DATE OR PERSTAT_END_DATE IS NULL)
           AND POSITION.POS_CLASS = 'FAC'
         AND POSITION.POS_DEPT = 'SWK'
         AND SEV.ENROLL_CURRENT_STATUS IN ('New', 'Add')
         AND COALESCE(SEV.ENROLL_SCS_PASS_AUDIT, '') != 'A'
--(End 1)--------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY PERSTAT_HRP_ID, LAST_NAME, FIRST_NAME, STUDENT_GENDER
--(End 2)--------------------------------------------------------------------------------------------------------------


SELECT *
FROM STUDENT_ENROLLMENT_VIEW