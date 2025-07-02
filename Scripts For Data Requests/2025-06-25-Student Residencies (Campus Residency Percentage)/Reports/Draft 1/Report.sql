--(Begin 4)-----------------------------------------------------------------------------------
         SELECT FORMAT(AVG(1.0 * CAMPUS_STATUS), 'P') AS CAMPUS_RESIDENCY_RATE
         FROM (
--(Begin 3)-----------------------------------------------------------------------------------
                  SELECT DISTINCT STUDENT_ID,
                                  CASE WHEN ADDRESS_TYPE = 'CA' THEN 1 ELSE 0 END AS CAMPUS_STATUS
                  FROM STUDENT_ENROLLMENT_VIEW AS SEV
                           JOIN (
--(Begin 2)-----------------------------------------------------------------------------------
                      SELECT ID,
                             ADDRESS_TYPE
                      FROM (
--(Begin 1)-----------------------------------------------------------------------------------
                               SELECT PAV.ID,
                                      ADDRESS_TYPE,
                                      ROW_NUMBER() OVER (PARTITION BY PAV.ID
                                          ORDER BY CASE WHEN ADDRESS_TYPE = 'CA' THEN 0 ELSE 1 END) AS ADDRESS_RANK
                               FROM PERSON_ADDRESSES_VIEW AS PAV
                               JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
--(End 1)-------------------------------------------------------------------------------------
                           ) AS X
                      WHERE ADDRESS_RANK = 1
--(End 2)-------------------------------------------------------------------------------------
                  ) AS STUDENT_STATE ON SEV.STUDENT_ID = STUDENT_STATE.ID
                  WHERE ENROLL_CREDIT_TYPE = 'Institutional'
                    AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                    AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                    AND ENROLL_TERM IN ('2024FA', '2025SP', '2024SU')
--(End 3)-------------------------------------------------------------------------------------
              ) AS X
--(End 4)-------------------------------------------------------------------------------------
