--(Begin 1)------------------------------------------------------------------------------------------------------------
SELECT MAJORS.MAJ_DESC           AS MAJOR,
     SAPV.STUDENT_ID,
     STP_CURRENT_STATUS        AS STATUS,
     MAIN_MAJOR.MAJ_DESC       AS MAIN,
     STP_END_DATE              AS MAIN_END,
     STPR_ADDNL_MAJOR_END_DATE AS ADDNL_END,
     AC.ACAD_END_DATE
FROM MAJORS
       CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
       JOIN ACAD_CREDENTIALS AS AC
            ON SAPV.STUDENT_ID = AC.ACAD_PERSON_ID AND
               SAPV.STP_DEGREE = AC.ACAD_DEGREE

       LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                 ON SAPV.STUDENT_ID = STPR_STUDENT AND
                    STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
       LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
       LEFT JOIN MAJORS AS ADDNL_MAJOR
                 ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
WHERE STP_CURRENT_STATUS != 'Did Not Enroll'
AND STP_START_DATE >= '2019-08-01'
AND (
  (
      MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
      )
      OR (
      MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
      )
  )
AND MAJORS.MAJ_DESC = 'Master of Social Work'
--(End 1)------------------------------------------------------------------------------------------------------------