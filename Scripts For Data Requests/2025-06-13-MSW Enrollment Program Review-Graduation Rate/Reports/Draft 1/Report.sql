--(Begin C4)------------------------------------------------------------------------------------------------------------
SELECT MAJOR,
       FORMAT(COMPLETION_RATE, 'P') AS COMPLETION_RATE,
       STUDENT_COUNT
FROM (
--(Begin C3)------------------------------------------------------------------------------------------------------------
         SELECT MAJOR,
                AVG(MAJOR_COMPLETED * 1.0)    AS COMPLETION_RATE,
                COUNT(*)                      AS STUDENT_COUNT
         FROM (
--(Begin C2)------------------------------------------------------------------------------------------------------------
                  SELECT MAJOR,
                         STUDENT_ID,
                         MAJOR_COMPLETED
                  FROM (
--(Begin C1)------------------------------------------------------------------------------------------------------------
                           SELECT X.MAJOR,
                                  X.STUDENT_ID,
                                  MAX(COMPLETE)           AS MAJOR_COMPLETED,
                                  ACAD_END_DATE
                           FROM (
--(Begin A3)------------------------------------------------------------------------------------------------------------
                                    SELECT MAJOR,
                                           STUDENT_ID,
                                           CASE
                                               WHEN (MAJOR_END >= ACAD_END_DATE OR MAJOR_END IS NULL)
                                                   AND STATUS = 'Graduated' THEN 1
                                               ELSE 0 END AS COMPLETE,
                                           ACAD_END_DATE
                                    FROM (
--(Begin A2)------------------------------------------------------------------------------------------------------------
                                             SELECT MAJOR,
                                                    STUDENT_ID,
                                                    STATUS,
                                                    CASE WHEN MAJOR = MAIN THEN MAIN_END ELSE ADDNL_END END AS MAJOR_END,
                                                    ACAD_END_DATE
                                             FROM (
--(Begin A1)------------------------------------------------------------------------------------------------------------
                                                      SELECT MAJORS.MAJ_DESC           AS MAJOR,
                                                             SAPV.STUDENT_ID,
                                                             SAPV.STUDENT_FIRST_NAME,
                                                             SAPV.STUDENT_LAST_NAME,
                                                             STP_CURRENT_STATUS        AS STATUS,
                                                             MAIN_MAJOR.MAJ_DESC       AS MAIN,
                                                             STP_END_DATE              AS MAIN_END,
                                                             STPR_ADDNL_MAJOR_END_DATE AS ADDNL_END,
                                                             AC.ACAD_END_DATE
                                                      FROM MAJORS
                                                               CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                               LEFT JOIN ACAD_CREDENTIALS AS AC
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
--(End A1)------------------------------------------------------------------------------------------------------------
                                                  ) AS X
--(End A2)------------------------------------------------------------------------------------------------------------
                                         ) AS X
--(End A3)------------------------------------------------------------------------------------------------------------
                                ) AS X
                           GROUP BY X.MAJOR, X.STUDENT_ID, ACAD_END_DATE
--(End C1)------------------------------------------------------------------------------------------------------------
                       ) AS X
--(End C2)------------------------------------------------------------------------------------------------------------
              ) AS X
         GROUP BY MAJOR
--(End C3)------------------------------------------------------------------------------------------------------------
     ) AS X
--(End C4)------------------------------------------------------------------------------------------------------------