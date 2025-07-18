--(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT ID,
       FIRST_NAME,
       LAST_NAME
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT PERSTAT_HRP_ID                                                        AS ID,
                         FIRST_NAME,
                         LAST_NAME,
                         CASE WHEN PERSTAT_STATUS = 'FT' THEN 'Full-Time' ELSE 'Part-Time' END AS STATUS,
                         POS_TITLE
         FROM PERSTAT
                  JOIN POSITION ON PERSTAT_PRIMARY_POS_ID = POSITION_ID
                  JOIN PERSON ON PERSTAT_HRP_ID = PERSON.ID
         WHERE POS_CLASS = 'FAC'
           AND (COALESCE(POS_RANK, '') != 'A'
             OR EXISTS (SELECT 1
                        FROM FACULTY_SECTIONS_DETAILS_VIEW AS FS
                                 JOIN COURSE_SECTIONS AS CS ON FS.COURSE_SECTION_ID = CS.COURSE_SECTIONS_ID
                        WHERE CS_TERM IN ('2024SU', '2024FA', '2025SP')
                          AND SEC_BILLING_CRED > 0
                          AND FACULTY_ID = PERSTAT_HRP_ID))
           AND PERSTAT_START_DATE <= (SELECT TOP 1 TERM_END_DATE
                                      FROM TERMS
                                      WHERE TERMS_ID = '2025SP')
           AND (PERSTAT_END_DATE >= (SELECT TOP 1 TERM_START_DATE
                                     FROM TERMS
                                     WHERE TERMS_ID = '2024SU') OR PERSTAT_END_DATE IS NULL)
--(End 1)--------------------------------------------------------------------------------------------------------------
     ) AS X
WHERE STATUS = 'Full-Time'
--(End 2)--------------------------------------------------------------------------------------------------------------
ORDER BY LAST_NAME, FIRST_NAME
