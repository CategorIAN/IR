--(Begin 4)-----------------------------------------------------------------------------------
         SELECT COUNT(*) AS TOTAL_STATES
         FROM (
--(Begin 3)-----------------------------------------------------------------------------------
                  SELECT DISTINCT STATE
                  FROM STUDENT_ENROLLMENT_VIEW AS SEV
                           JOIN (
--(Begin 2)-----------------------------------------------------------------------------------

                      SELECT ID,
                             STATE
                      FROM (
--(Begin 1)-----------------------------------------------------------------------------------
                               SELECT PAV.ID,
                                      PAV.STATE,
                                      ROW_NUMBER() OVER (PARTITION BY PAV.ID ORDER BY ADDRESS_ADD_DATE) AS ADDRESS_RANK
                               FROM PERSON_ADDRESSES_VIEW AS PAV
                               JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                               WHERE ADDRESS_TYPE = 'H'
--(End 1)-------------------------------------------------------------------------------------
                           ) AS X
                      WHERE ADDRESS_RANK = 1
--(End 2)-------------------------------------------------------------------------------------
                  ) AS STUDENT_STATE ON SEV.STUDENT_ID = STUDENT_STATE.ID
                  JOIN STATES ON STUDENT_STATE.STATE = STATES.STATES_ID
                  WHERE ENROLL_CREDIT_TYPE = 'Institutional'
                    AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                    AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                    AND ENROLL_TERM IN ('2024FA', '2025SP', '2024SU')
                    AND STATES.ST_USER1 = 1
--(End 3)-------------------------------------------------------------------------------------
              ) AS X
--(End 4)-------------------------------------------------------------------------------------


