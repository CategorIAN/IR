SELECT STTR_STUDENT,
       PERSON.LAST_NAME,
       PERSON.FIRST_NAME,
       GENDER,
       STTR_ACAD_LEVEL
FROM STUDENT_TERMS_VIEW
JOIN PERSON ON STTR_STUDENT = PERSON.ID
WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
AND GENDER IS NULL
-----------------------------------------------------------------------------------------------------------------------



