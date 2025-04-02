SELECT STATE,
       FORMAT(SUM(STUDENT_PERCENTAGE), '0.###') AS STUDENT_PERCENTAGE
FROM (
SELECT CASE
        WHEN RANK <= 5 THEN STATE ELSE 'Other' END AS STATE,
        STUDENT_PERCENTAGE
FROM (
SELECT STATE,
       STUDENT_PERCENTAGE,
       RANK() OVER (ORDER BY STUDENT_PERCENTAGE DESC) AS RANK
FROM (SELECT STATE,
             (STUDENT_COUNT * 1.0) / SUM(STUDENT_COUNT) OVER () AS STUDENT_PERCENTAGE
      FROM (SELECT CASE WHEN STATE IS NULL THEN 'Unknown' ELSE STATE END AS STATE,
                   COUNT(*)                                              AS STUDENT_COUNT
            FROM (SELECT STTR_STUDENT,
                         STATE
                  FROM (SELECT STTR_STUDENT,
                               LAST_NAME,
                               FIRST_NAME,
                               ADDRESS_ID
                        FROM (SELECT STTR_STUDENT,
                                     P.LAST_NAME,
                                     P.FIRST_NAME,
                                     ADDRESS.ADDRESS_ID,
                                     ROW_NUMBER() OVER (PARTITION BY STTR_STUDENT ORDER BY ADDRESS_ADD_DATE DESC) AS rn

                              FROM STUDENT_TERMS_VIEW AS STV
                                       JOIN PERSON AS P ON STV.STTR_STUDENT = P.ID
                                       JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STV.STTR_STUDENT = FM.ID
                                       JOIN TERMS AS STARTING_TERM ON FM.TERM = STARTING_TERM.TERMS_ID
                                       JOIN PERSON_ADDRESSES_VIEW AS PAV ON STV.STTR_STUDENT = PAV.ID
                                       JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                              WHERE STTR_TERM = '2024FA'
                                AND ADDRESS_TYPE = 'H'
                                AND ADDRESS_ADD_DATE < STARTING_TERM.TERM_START_DATE) AS X
                        WHERE rn = 1) AS X
                           JOIN ADDRESS ON X.ADDRESS_ID = ADDRESS.ADDRESS_ID
                           JOIN ADDRESS_LS ON X.ADDRESS_ID = ADDRESS_LS.ADDRESS_ID
                  WHERE POS = 1) AS X
            GROUP BY STATE) AS X) AS X) AS X) AS X
GROUP BY STATE
ORDER BY STUDENT_PERCENTAGE DESC
---------------------------------------------------------------------------------------------------------------------------
SELECT STATE,
       FORMAT(SUM(STUDENT_PERCENTAGE), '0.###') AS STUDENT_PERCENTAGE
FROM (
SELECT CASE
        WHEN RANK <= 5 THEN STATE ELSE 'Other' END AS STATE,
        STUDENT_PERCENTAGE
FROM (
SELECT STATE,
       STUDENT_PERCENTAGE,
       RANK() OVER (ORDER BY STUDENT_PERCENTAGE DESC) AS RANK
FROM (SELECT STATE,
             (STUDENT_COUNT * 1.0) / SUM(STUDENT_COUNT) OVER () AS STUDENT_PERCENTAGE
      FROM (SELECT CASE WHEN STATE IS NULL THEN 'Unknown' ELSE STATE END AS STATE,
                   COUNT(*)                                              AS STUDENT_COUNT
            FROM (SELECT STUDENT_ID,
                         STATE
                  FROM (SELECT STUDENT_ID,
                               ADDRESS_ID
                        FROM (
                                SELECT DISTINCT STUDENT_ID,
                                        ADDRESS.ADDRESS_ID,
                                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY ADDRESS_ADD_DATE DESC) AS ADDRESS_RANK

                                FROM STUDENT_ENROLLMENT_VIEW AS SEV
                                JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON SEV.STUDENT_ID = FM.ID
                                JOIN TERMS AS STARTING_TERM ON FM.TERM = STARTING_TERM.TERMS_ID
                                JOIN PERSON_ADDRESSES_VIEW AS PAV ON SEV.STUDENT_ID = PAV.ID
                                JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                                WHERE ENROLL_TERM = '2024FA'
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND  (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
                                AND ADDRESS_TYPE = 'H'
                                AND ADDRESS_ADD_DATE < STARTING_TERM.TERM_START_DATE
                                ) AS X
                            WHERE ADDRESS_RANK = 1
                            ) AS X
                    JOIN ADDRESS ON X.ADDRESS_ID = ADDRESS.ADDRESS_ID
                  ) AS X
            GROUP BY STATE
            ) AS X
      ) AS X
) AS X
) AS X
GROUP BY STATE
ORDER BY STUDENT_PERCENTAGE DESC