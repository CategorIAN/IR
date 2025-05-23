SELECT RACE,
       [Full-Time],
       [Part-Time]
FROM (SELECT STTR_STUDENT,
             RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
             CASE
                 WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time'
                 ELSE 'Part-Time'
                 END                     AS STATUS,
          STTR_STUDENT_LOAD

      FROM STUDENT_TERMS_VIEW
               JOIN PERSON ON STTR_STUDENT = PERSON.ID
               JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
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
      WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
        AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
        AND STTR_ACAD_LEVEL = 'GR'
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
            '6189973'))) AS X
PIVOT (COUNT(STTR_STUDENT) FOR STATUS IN ([Full-Time], [Part-Time])) AS Y --Men



SELECT RACE,
       [Full-Time],
       [Part-Time]
FROM (SELECT STTR_STUDENT,
             RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
             CASE
                 WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time'
                 ELSE 'Part-Time'
                 END AS STATUS

      FROM STUDENT_TERMS_VIEW
               JOIN PERSON ON STTR_STUDENT = PERSON.ID
               JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
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
      WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
        AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
        AND STTR_ACAD_LEVEL = 'GR'
        AND (PERSON.GENDER = 'F'
    OR STTR_STUDENT IN ('6184697',
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
            '6190234',
            '6188723'))) AS X
PIVOT (COUNT(STTR_STUDENT) FOR STATUS IN ([Full-Time], [Part-Time])) AS Y --Women


SELECT STTR_STUDENT,
             RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
             CASE
                 WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time'
                 ELSE 'Part-Time'
                 END AS STATUS

      FROM STUDENT_TERMS_VIEW
               JOIN PERSON ON STTR_STUDENT = PERSON.ID
               JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
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
      WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
        AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
        AND STTR_ACAD_LEVEL = 'GR'
        AND GENDER IS NULL
        AND (STTR_STUDENT NOT IN ('6184697',
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
            '6190234')
            AND STTR_STUDENT NOT IN ('6189200',
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


SELECT LAST_NAME, FIRST_NAME
FROM PERSON
WHERE ID = '6188723'