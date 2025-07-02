--(Begin 4)-----------------------------------------------------------------------------------
         SELECT COUNT(*) AS TOTAL_COUNTRIES
         FROM (
--(Begin 3)-----------------------------------------------------------------------------------
                  SELECT DISTINCT COUNTRY,
                                  COUNTRIES.CTRY_DESC
                  FROM STUDENT_ENROLLMENT_VIEW AS SEV
                           JOIN (
--(Begin 2)-----------------------------------------------------------------------------------
                      SELECT ID,
                             COUNTRY
                      FROM (
--(Begin 1)-----------------------------------------------------------------------------------
                               SELECT PAV.ID,
                                      PAV.COUNTRY,
                                      ROW_NUMBER() OVER (PARTITION BY PAV.ID ORDER BY ADDRESS_ADD_DATE) AS ADDRESS_RANK
                               FROM PERSON_ADDRESSES_VIEW AS PAV
                               JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                               WHERE ADDRESS_TYPE = 'H'
--(End 1)-------------------------------------------------------------------------------------
                           ) AS X
                      WHERE ADDRESS_RANK = 1
--(End 2)-------------------------------------------------------------------------------------
                  ) AS STUDENT_COUNTRY ON SEV.STUDENT_ID = STUDENT_COUNTRY.ID
                  JOIN COUNTRIES ON STUDENT_COUNTRY.COUNTRY = COUNTRIES_ID
                  WHERE ENROLL_CREDIT_TYPE = 'Institutional'
                    AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                    AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                    AND ENROLL_TERM IN ('2024FA', '2025SP', '2024SU')
--(End 3)-------------------------------------------------------------------------------------
              ) AS X
--(End 4)-------------------------------------------------------------------------------------
