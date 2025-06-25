SELECT DISTINCT STUDENT_ID,
                COALESCE(STUDENT_GENDER, ADJUSTED_GENDER.X) AS GENDER,
                RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
                CASE WHEN STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time' ELSE 'Part-Time' END AS LOAD
FROM STUDENT_ENROLLMENT_VIEW AS SEV
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON SEV.STUDENT_ID = RACE.ID
LEFT JOIN (
    VALUES
            ('6188731', 'F'),
            ('6188723', 'F'),
            ('6184977', 'F'),
            ('6189317', 'F'),
            ('6187467', 'F'),
            ('6188544', 'F'),
            ('6188665', 'F'),
            ('6186670', 'F'),
            ('6188541', 'F'),
            ('6187470', 'F'),
            ('6188940', 'F'),
            ('6184697', 'F'),
            ('6188264', 'F'),
            ('6189575', 'F'),
            ('6184447', 'F'),
            ('6189571', 'F'),
            ('6189250', 'F'),
            ('6189523', 'F'),
            ('6188797', 'F'),
            ('6189620', 'F'),
            ('6189620', 'F'),
            ('6185039', 'F'),
    ----------------------------------------------------------------------------------------------
            ('6189635', 'M'),
            ('6189572', 'M'),
            ('6186217', 'M'),
            ('6189662', 'M'),
            ('6189200', 'M'),
            ('6189182', 'M'),
            ('6189204', 'M'),
            ('6189318', 'M'),
            ('6189252', 'M'),
            ('6187468', 'M')
           ) AS ADJUSTED_GENDER(ID, X) ON ADJUSTED_GENDER.ID = STUDENT_ID
WHERE ENROLL_TERM = '2024FA'
AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)


SELECT *
FROM STUDENT_ENROLLMENT_VIEW