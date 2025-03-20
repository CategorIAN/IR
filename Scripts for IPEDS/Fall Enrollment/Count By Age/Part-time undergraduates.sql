SELECT AGE_CATEGORY,
       [M],
       [F]
FROM (SELECT DISTINCT SEV.STUDENT_ID,
                      CASE
                        WHEN (GENDER = 'M'
                        OR STTR_STUDENT IN
                                ('6189200',
                                '6189204',
                                '6189252',
                                '6186217',
                                '6190237',
                                '6190238',
                                '6190246',
                                '6189572',
                                '6189318',
                                '6189974',
                                '6189975',
                                '6189977',
                                '6187468',
                                '6189635',
                                '6190236',
                                '6189662',
                                '6189973')) THEN 'M'
                        WHEN (GENDER = 'F'
                        OR STTR_STUDENT IN (
                                '6184697',
                                '6184977',
                                '6189250',
                                '6185039',
                                '6178065',
                                '6178068',
                                '6189523',
                                '6190232',
                                '6190233',
                                '6190235',
                                '6190242',
                                '6189571',
                                '6187470',
                                '6187467',
                                '6188541',
                                '6188544',
                                '6188940',
                                '6189317',
                                '6188731',
                                '6188797',
                                '6189969',
                                '6189970',
                                '6189971',
                                '6189972',
                                '6189978',
                                '6190240',
                                '6186670',
                                '6184447',
                                '6189976',
                                '6178066',
                                '6188264',
                                '6189575',
                                '6190234')) THEN 'F'
                      END AS ADJUSTED_GENDER,
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
      JOIN (SELECT *
           FROM (SELECT STUDENT_ID,
                        STP_ACADEMIC_PROGRAM,
                        STP_PROGRAM_TITLE,
                        STP_CURRENT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                            ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
                 FROM STUDENT_ACAD_PROGRAMS_VIEW
                 WHERE STP_CURRENT_STATUS != 'Changed Program'
                 AND STP_START_DATE <= (SELECT TOP 1 TERMS.TERM_END_DATE
                                        FROM TERMS
                                        WHERE TERMS_ID = '2024FA')
                 ) ranked
            WHERE rn = 1)
            AS SAPV ON STV.STTR_STUDENT = SAPV.STUDENT_ID
      WHERE SEV.ENROLL_TERM = '2024FA'
        AND STV.STTR_TERM = '2024FA'
        AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
        AND STV.STTR_ACAD_LEVEL = 'UG'
        AND STV.STTR_STUDENT_LOAD NOT IN ('F', 'O')) AS X
PIVOT (COUNT(STUDENT_ID) FOR ADJUSTED_GENDER IN ([M], [F])) AS X

-----------------------------------------------------------------------------------------------------------------------
SELECT *
FROM (
SELECT DISTINCT SEV.STUDENT_ID,
                      CASE
                        WHEN (GENDER = 'M'
                        OR STTR_STUDENT IN
                                ('6189200',
                                '6189204',
                                '6189252',
                                '6186217',
                                '6190237',
                                '6190238',
                                '6190246',
                                '6189572',
                                '6189318',
                                '6189974',
                                '6189975',
                                '6189977',
                                '6187468',
                                '6189635',
                                '6190236',
                                '6189662',
                                '6189973')) THEN 'M'
                        WHEN (GENDER = 'F'
                        OR STTR_STUDENT IN (
                                '6184697',
                                '6184977',
                                '6189250',
                                '6185039',
                                '6178065',
                                '6178068',
                                '6189523',
                                '6190232',
                                '6190233',
                                '6190235',
                                '6190242',
                                '6189571',
                                '6187470',
                                '6187467',
                                '6188541',
                                '6188544',
                                '6188940',
                                '6189317',
                                '6188731',
                                '6188797',
                                '6189969',
                                '6189970',
                                '6189971',
                                '6189972',
                                '6189978',
                                '6190240',
                                '6186670',
                                '6184447',
                                '6189976',
                                '6178066',
                                '6188264',
                                '6189575',
                                '6190234')) THEN 'F'
                      END AS ADJUSTED_GENDER,
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
      JOIN (SELECT *
           FROM (SELECT STUDENT_ID,
                        STP_ACADEMIC_PROGRAM,
                        STP_PROGRAM_TITLE,
                        STP_CURRENT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                            ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
                 FROM STUDENT_ACAD_PROGRAMS_VIEW
                 WHERE STP_CURRENT_STATUS != 'Changed Program'
                 AND STP_START_DATE <= (SELECT TOP 1 TERMS.TERM_END_DATE
                                        FROM TERMS
                                        WHERE TERMS_ID = '2024FA')
                 ) ranked
            WHERE rn = 1)
            AS SAPV ON STV.STTR_STUDENT = SAPV.STUDENT_ID
      WHERE SEV.ENROLL_TERM = '2024FA'
        AND STV.STTR_TERM = '2024FA'
        AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
        AND STV.STTR_ACAD_LEVEL = 'UG'
        AND STV.STTR_STUDENT_LOAD NOT IN ('F', 'O')) AS X
WHERE ADJUSTED_GENDER = 'M'

----------------------------------------------------------------------------------------------------------------------
SELECT STTR_STUDENT,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
        CASE
            WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students' THEN 'Non-Degree Seeking'
            WHEN FM.TERM = '2024FA' THEN CASE
                WHEN STPR_ADMIT_STATUS = 'FY' THEN 'First-time'
                WHEN STPR_ADMIT_STATUS = 'TR' THEN 'Transfer-in' END
            WHEN FM.TERM IS NOT NULL THEN 'Continuing/Returning' END AS STATUS

FROM STUDENT_TERMS_VIEW
JOIN PERSON ON STTR_STUDENT = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS  AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
JOIN (SELECT *
           FROM (SELECT STUDENT_ID,
                        STP_ACADEMIC_PROGRAM,
                        STP_PROGRAM_TITLE,
                        STP_CURRENT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                            ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
                 FROM STUDENT_ACAD_PROGRAMS_VIEW
                 WHERE STP_CURRENT_STATUS != 'Changed Program'
                 AND STP_START_DATE <= (SELECT TOP 1 TERMS.TERM_END_DATE
                                        FROM TERMS
                                        WHERE TERMS_ID = '2024FA')
                 ) ranked
            WHERE rn = 1)
            AS SAPV ON STUDENT_TERMS_VIEW.STTR_STUDENT = SAPV.STUDENT_ID
LEFT JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STUDENT_TERMS_VIEW.STTR_STUDENT = FM.ID
LEFT JOIN (SELECT DISTINCT STPR_STUDENT, STPR_ADMIT_STATUS
           FROM (
               SELECT   STPR_STUDENT,
                        STPR_ADMIT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                        ORDER BY STPR_ADMIT_STATUS) AS rn
               FROM STUDENT_PROGRAMS_VIEW
               WHERE STPR_ADMIT_STATUS IN ('FY', 'TR')
               ) ranked
               WHERE rn = 1)
    AS FIRST_ADMIT ON STUDENT_TERMS_VIEW.STTR_STUDENT = FIRST_ADMIT.STPR_STUDENT
WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
AND STUDENT_TERMS_VIEW.STTR_ACAD_LEVEL = 'UG'
AND STUDENT_TERMS_VIEW.STTR_STUDENT_LOAD NOT IN ('F', 'O')
AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
AND (GENDER = 'M'
    OR STTR_STUDENT IN
            ('6189200',
            '6189204',
            '6189252',
            '6186217',
            '6190237',
            '6190238',
            '6190246',
            '6189572',
            '6189318',
            '6189974',
            '6189975',
            '6189977',
            '6187468',
            '6189635',
            '6190236',
            '6189662',
            '6189973'))