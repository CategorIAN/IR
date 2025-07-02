
--(Begin 4)-----------------------------------------------------------------------------------
         SELECT TOP 4 STATE,
                COUNT(*) AS STATE_COUNT
         FROM (
--(Begin 3)-----------------------------------------------------------------------------------
                  SELECT DISTINCT STUDENT_ID,
                                  STATE
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
                  WHERE ENROLL_CREDIT_TYPE = 'Institutional'
                    AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                    AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                    AND ENROLL_TERM IN ('2024FA', '2025SP', '2024SU')
                  AND STATE IS NOT NULL
                  AND STATE != 'MT'
--(End 3)-------------------------------------------------------------------------------------
              ) AS X
         GROUP BY STATE
--(End 4)-------------------------------------------------------------------------------------
ORDER BY STATE_COUNT DESC

