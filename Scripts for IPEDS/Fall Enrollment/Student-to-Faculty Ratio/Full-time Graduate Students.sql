SELECT STTR_STUDENT
      FROM STUDENT_TERMS_VIEW
               JOIN PERSON ON STTR_STUDENT = PERSON.ID
               JOIN (SELECT *
                     FROM (SELECT STUDENT_ID,
                                  STP_ACADEMIC_PROGRAM,
                                  STP_PROGRAM_TITLE,
                                  STP_START_DATE,
                                  STP_CURRENT_STATUS,
                                  ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                                      ORDER BY STP_START_DATE DESC) AS rn
                           FROM STUDENT_ACAD_PROGRAMS_VIEW
                           WHERE STP_CURRENT_STATUS != 'Changed Program'
                             AND STP_START_DATE <= '2024-12-12') ranked
                     WHERE rn = 1)

          AS SAPV ON STUDENT_TERMS_VIEW.STTR_STUDENT = SAPV.STUDENT_ID
      JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
      WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
        AND SAPV.STP_CURRENT_STATUS NOT IN ('Not Returned', 'Withdrawn', 'Did Not Enroll')
        AND STTR_ACAD_LEVEL = 'GR'
        AND (
            STTR_STUDENT_LOAD IN ('F', 'O')
          )
--Of the full-time students reported in Line F1, the number enrolled in stand-alone graduate or professional programs


SELECT STTR_STUDENT
      FROM STUDENT_TERMS_VIEW
               JOIN PERSON ON STTR_STUDENT = PERSON.ID
               JOIN (SELECT *
                     FROM (SELECT STUDENT_ID,
                                  STP_ACADEMIC_PROGRAM,
                                  STP_PROGRAM_TITLE,
                                  STP_START_DATE,
                                  STP_CURRENT_STATUS,
                                  ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                                      ORDER BY STP_START_DATE DESC) AS rn
                           FROM STUDENT_ACAD_PROGRAMS_VIEW
                           WHERE STP_CURRENT_STATUS != 'Changed Program'
                             AND STP_START_DATE <= '2024-12-12') ranked
                     WHERE rn = 1)

          AS SAPV ON STUDENT_TERMS_VIEW.STTR_STUDENT = SAPV.STUDENT_ID
      JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
      WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
        AND SAPV.STP_CURRENT_STATUS NOT IN ('Not Returned', 'Withdrawn', 'Did Not Enroll')
        AND STTR_ACAD_LEVEL = 'GR'
        AND (
            STTR_STUDENT_LOAD NOT IN ('F', 'O')
            OR STTR_STUDENT_LOAD IS NULL
          )


