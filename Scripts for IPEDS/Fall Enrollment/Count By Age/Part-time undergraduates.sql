SELECT AGE_CATEGORY,
       [M],
       [F]
FROM (SELECT DISTINCT STUDENT_ID,
                      GENDER,
                      CASE
                          WHEN STUDENT_AGE < 18 THEN 'Under 18'
                          WHEN STUDENT_AGE BETWEEN 18 AND 19 THEN '18-19'
                          WHEN STUDENT_AGE BETWEEN 20 AND 21 THEN '20-21'
                          WHEN STUDENT_AGE BETWEEN 22 AND 24 THEN '22-24'
                          WHEN STUDENT_AGE BETWEEN 25 AND 29 THEN '25-29'
                          WHEN STUDENT_AGE BETWEEN 30 AND 34 THEN '30-34'
                          WHEN STUDENT_AGE BETWEEN 35 AND 39 THEN '35-39'
                          WHEN STUDENT_AGE BETWEEN 40 AND 49 THEN '40-49'
                          WHEN STUDENT_AGE BETWEEN 50 AND 64 THEN '50-64'
                          WHEN STUDENT_AGE >= 65 THEN '65 and over'
                          WHEN STUDENT_AGE IS NULL THEN 'Age unknown/unreported'
                          END AS AGE_CATEGORY
      FROM STUDENT_ENROLLMENT_VIEW AS SEV
               JOIN PERSON ON STUDENT_ID = PERSON.ID
               JOIN STUDENT_TERMS_VIEW AS STV ON SEV.STUDENT_ID = STV.STTR_STUDENT AND SEV.ENROLL_TERM = STV.STTR_TERM
      WHERE SEV.ENROLL_TERM = '2024FA'
        AND STV.STTR_ACAD_LEVEL = 'UG'
        AND STV.STTR_STUDENT_LOAD NOT IN ('F', 'O')) AS X
PIVOT (COUNT(STUDENT_ID) FOR GENDER IN ([M], [F])) AS Y