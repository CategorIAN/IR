SELECT SEC_TERM,
       SEC_NAME,
       SEC_SHORT_TITLE,
       SEC_FACULTY_INFO
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
         Select CS.SEC_TERM,
                CS.SEC_NAME,
                CS.SEC_SHORT_TITLE,
                CS.SEC_FACULTY_INFO,
                CSCV.COUNT_ACTIVE_STUDENTS
         FROM COURSE_SECTIONS AS CS
                  JOIN COURSE_SECTIONS_COUNT_VIEW AS CSCV ON CS.COURSE_SECTIONS_ID = CSCV.COURSE_SECTIONS_ID
         WHERE SEC_START_DATE >= '2021-08-01'
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X

