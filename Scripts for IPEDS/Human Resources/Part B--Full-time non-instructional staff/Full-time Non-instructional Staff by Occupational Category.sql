SELECT RACE_ETHNICITY,
       [Archivists, Curators, and Museum Technicians],
       [Librarians and Media Collections Specialists],
       [Student and Academic Affairs and Other Education Services Occupations],
       [Business and Financial Operations Occupations],
       [Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations],
       [Computer, Engineering, and Science Occupations],
       [Healthcare Practitioners and Technical Occupations],
       [Management Occupations],
       [Natural Resources, Construction, and Maintenance Occupations],
       [Office and Administrative Support Occupations],
       [Production, Transportation, and Material Moving Occupations],
       [Service Occupations]

FROM (
SELECT
        PERSTAT_HRP_ID,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE_ETHNICITY,
        CASE
            WHEN POS_SOC_CODE LIKE '25-401%' THEN 'Archivists, Curators, and Museum Technicians'
            WHEN POS_SOC_CODE LIKE '25-402%' THEN 'Librarians and Media Collections Specialists'
            WHEN POS_SOC_CODE LIKE '25-403%' THEN 'Library Technicians'
            WHEN (
                POS_SOC_CODE LIKE '25-2%'
                    OR POS_SOC_CODE LIKE '25-3%'
                    OR POS_SOC_CODE LIKE '25-9%'
                ) THEN 'Student and Academic Affairs and Other Education Services Occupations'
            WHEN POS_SOC_CODE LIKE '11%' THEN 'Management Occupations'
            WHEN POS_SOC_CODE LIKE '13%' THEN 'Business and Financial Operations Occupations'
            WHEN (
                POS_SOC_CODE LIKE '15%'
                    OR POS_SOC_CODE LIKE '17%'
                    OR POS_SOC_CODE LIKE '19%'
                ) THEN 'Computer, Engineering, and Science Occupations'
            WHEN (
                POS_SOC_CODE LIKE '21%'
                OR POS_SOC_CODE LIKE '23%'
                 OR POS_SOC_CODE LIKE '27%'
                ) THEN 'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_SOC_CODE LIKE '29%' THEN 'Healthcare Practitioners and Technical Occupations'
            WHEN (
                POS_SOC_CODE LIKE '31%'
                OR POS_SOC_CODE LIKE '33%'
                OR POS_SOC_CODE LIKE '35%'
                 OR POS_SOC_CODE LIKE '37%'
                OR POS_SOC_CODE LIKE '39%'
                ) THEN 'Service Occupations'
            WHEN POS_SOC_CODE LIKE '41%' THEN 'Sales and Related Occupations'
            WHEN POS_SOC_CODE LIKE '43%' THEN 'Office and Administrative Support Occupations'
            WHEN (
                POS_SOC_CODE LIKE '45%'
                OR POS_SOC_CODE LIKE '47%'
                OR POS_SOC_CODE LIKE '49%'
                ) THEN 'Natural Resources, Construction, and Maintenance Occupations'
            WHEN (
                POS_SOC_CODE LIKE '51%'
                OR POS_SOC_CODE LIKE '53%'
                ) THEN 'Production, Transportation, and Material Moving Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Academic Support',
                    'Assistant Director of Institutional Research',
                    'Director of Academic Technology',
                    'Director of Auxiliary Services',
                    'Director of Global Education') THEN 'Management Occupations'
            WHEN POS_TITLE IN ('Athletic Operations Assistant',
                              'Digital Marketing Strategist',
                              'Accounting Techician',
                              'Marketing Technology Specialist',
                              'Prospect Research Specialist',
                              'Saints Shoppe Coordinator') THEN 'Business and Financial Operations Occupations'
            WHEN POS_TITLE IN ('IT Business System Analyst') THEN 'Computer, Engineering, and Science Occupations'
            WHEN POS_TITLE IN ('Athletic Eligibility Coordinator',
                              'Sports Information Director'
                                ) THEN
                'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Residential Life & Housing')
            THEN 'Service Occupations'
            WHEN POS_TITLE IN ('Administrative Assistant - Registrar')
                THEN 'Office and Administrative Support Occupations'
        END AS IPEDS_OCCUPATION_CATEGORY

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
LEFT JOIN SOC_CODES ON POSITION.POS_SOC_CODE = SOC_CODES.SOC_CODES_ID
WHERE PERSTAT_END_DATE IS NULL
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS != 'FAC'
AND GENDER = 'M') AS Q1
PIVOT (COUNT(PERSTAT_HRP_ID) FOR IPEDS_OCCUPATION_CATEGORY IN (
        [Archivists, Curators, and Museum Technicians],
       [Business and Financial Operations Occupations],
       [Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations],
       [Computer, Engineering, and Science Occupations],
       [Healthcare Practitioners and Technical Occupations],
       [Librarians and Media Collections Specialists],
        [Library Technicians],
       [Management Occupations],
       [Natural Resources, Construction, and Maintenance Occupations],
       [Office and Administrative Support Occupations],
       [Production, Transportation, and Material Moving Occupations],
       [Service Occupations],
       [Student and Academic Affairs and Other Education Services Occupations]
        )) AS Q2

SELECT RACE_ETHNICITY,
       [Archivists, Curators, and Museum Technicians],
       [Librarians and Media Collections Specialists],
       [Library Technicians],
       [Student and Academic Affairs and Other Education Services Occupations]

FROM (
SELECT
        PERSTAT_HRP_ID,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE_ETHNICITY,
        CASE
            WHEN POS_SOC_CODE LIKE '25-401%' THEN 'Archivists, Curators, and Museum Technicians'
            WHEN POS_SOC_CODE LIKE '25-402%' THEN 'Librarians and Media Collections Specialists'
            WHEN POS_SOC_CODE LIKE '25-403%' THEN 'Library Technicians'
            WHEN (
                POS_SOC_CODE LIKE '25-2%'
                    OR POS_SOC_CODE LIKE '25-3%'
                    OR POS_SOC_CODE LIKE '25-9%'
                ) THEN 'Student and Academic Affairs and Other Education Services Occupations'
            WHEN POS_SOC_CODE LIKE '11%' THEN 'Management Occupations'
            WHEN POS_SOC_CODE LIKE '13%' THEN 'Business and Financial Operations Occupations'
            WHEN (
                POS_SOC_CODE LIKE '15%'
                    OR POS_SOC_CODE LIKE '17%'
                    OR POS_SOC_CODE LIKE '19%'
                ) THEN 'Computer, Engineering, and Science Occupations'
            WHEN (
                POS_SOC_CODE LIKE '21%'
                OR POS_SOC_CODE LIKE '23%'
                 OR POS_SOC_CODE LIKE '27%'
                ) THEN 'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_SOC_CODE LIKE '29%' THEN 'Healthcare Practitioners and Technical Occupations'
            WHEN (
                POS_SOC_CODE LIKE '31%'
                OR POS_SOC_CODE LIKE '33%'
                OR POS_SOC_CODE LIKE '35%'
                 OR POS_SOC_CODE LIKE '37%'
                OR POS_SOC_CODE LIKE '39%'
                ) THEN 'Service Occupations'
            WHEN POS_SOC_CODE LIKE '41%' THEN 'Sales and Related Occupations'
            WHEN POS_SOC_CODE LIKE '43%' THEN 'Office and Administrative Support Occupations'
            WHEN (
                POS_SOC_CODE LIKE '45%'
                OR POS_SOC_CODE LIKE '47%'
                OR POS_SOC_CODE LIKE '49%'
                ) THEN 'Natural Resources, Construction, and Maintenance Occupations'
            WHEN (
                POS_SOC_CODE LIKE '51%'
                OR POS_SOC_CODE LIKE '53%'
                ) THEN 'Production, Transportation, and Material Moving Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Academic Support',
                    'Assistant Director of Institutional Research',
                    'Director of Academic Technology',
                    'Director of Auxiliary Services',
                    'Director of Global Education') THEN 'Management Occupations'
            WHEN POS_TITLE IN ('Athletic Operations Assistant',
                              'Digital Marketing Strategist',
                              'Accounting Techician',
                              'Marketing Technology Specialist',
                              'Prospect Research Specialist',
                              'Saints Shoppe Coordinator') THEN 'Business and Financial Operations Occupations'
            WHEN POS_TITLE IN ('IT Business System Analyst') THEN 'Computer, Engineering, and Science Occupations'
            WHEN POS_TITLE IN ('Athletic Eligibility Coordinator',
                              'Sports Information Director'
                                ) THEN
                'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Residential Life & Housing')
            THEN 'Service Occupations'
            WHEN POS_TITLE IN ('Administrative Assistant - Registrar')
                THEN 'Office and Administrative Support Occupations'
        END AS IPEDS_OCCUPATION_CATEGORY

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
LEFT JOIN SOC_CODES ON POSITION.POS_SOC_CODE = SOC_CODES.SOC_CODES_ID
WHERE PERSTAT_END_DATE IS NULL
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS != 'FAC'
AND GENDER = 'M') AS Q1
PIVOT (COUNT(PERSTAT_HRP_ID) FOR IPEDS_OCCUPATION_CATEGORY IN (
        [Archivists, Curators, and Museum Technicians],
       [Business and Financial Operations Occupations],
       [Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations],
       [Computer, Engineering, and Science Occupations],
       [Healthcare Practitioners and Technical Occupations],
       [Librarians and Media Collections Specialists],
        [Library Technicians],
       [Management Occupations],
       [Natural Resources, Construction, and Maintenance Occupations],
       [Office and Administrative Support Occupations],
       [Production, Transportation, and Material Moving Occupations],
       [Service Occupations],
       [Student and Academic Affairs and Other Education Services Occupations]
        )) AS Q2  --Page 2 (Men)


SELECT RACE_ETHNICITY,
       [Archivists, Curators, and Museum Technicians],
       [Librarians and Media Collections Specialists],
       [Library Technicians],
       [Student and Academic Affairs and Other Education Services Occupations]

FROM (
SELECT
        PERSTAT_HRP_ID,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE_ETHNICITY,
        CASE
            WHEN POS_SOC_CODE LIKE '25-401%' THEN 'Archivists, Curators, and Museum Technicians'
            WHEN POS_SOC_CODE LIKE '25-402%' THEN 'Librarians and Media Collections Specialists'
            WHEN POS_SOC_CODE LIKE '25-403%' THEN 'Library Technicians'
            WHEN (
                POS_SOC_CODE LIKE '25-2%'
                    OR POS_SOC_CODE LIKE '25-3%'
                    OR POS_SOC_CODE LIKE '25-9%'
                ) THEN 'Student and Academic Affairs and Other Education Services Occupations'
            WHEN POS_SOC_CODE LIKE '11%' THEN 'Management Occupations'
            WHEN POS_SOC_CODE LIKE '13%' THEN 'Business and Financial Operations Occupations'
            WHEN (
                POS_SOC_CODE LIKE '15%'
                    OR POS_SOC_CODE LIKE '17%'
                    OR POS_SOC_CODE LIKE '19%'
                ) THEN 'Computer, Engineering, and Science Occupations'
            WHEN (
                POS_SOC_CODE LIKE '21%'
                OR POS_SOC_CODE LIKE '23%'
                 OR POS_SOC_CODE LIKE '27%'
                ) THEN 'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_SOC_CODE LIKE '29%' THEN 'Healthcare Practitioners and Technical Occupations'
            WHEN (
                POS_SOC_CODE LIKE '31%'
                OR POS_SOC_CODE LIKE '33%'
                OR POS_SOC_CODE LIKE '35%'
                 OR POS_SOC_CODE LIKE '37%'
                OR POS_SOC_CODE LIKE '39%'
                ) THEN 'Service Occupations'
            WHEN POS_SOC_CODE LIKE '41%' THEN 'Sales and Related Occupations'
            WHEN POS_SOC_CODE LIKE '43%' THEN 'Office and Administrative Support Occupations'
            WHEN (
                POS_SOC_CODE LIKE '45%'
                OR POS_SOC_CODE LIKE '47%'
                OR POS_SOC_CODE LIKE '49%'
                ) THEN 'Natural Resources, Construction, and Maintenance Occupations'
            WHEN (
                POS_SOC_CODE LIKE '51%'
                OR POS_SOC_CODE LIKE '53%'
                ) THEN 'Production, Transportation, and Material Moving Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Academic Support',
                    'Assistant Director of Institutional Research',
                    'Director of Academic Technology',
                    'Director of Auxiliary Services',
                    'Director of Global Education') THEN 'Management Occupations'
            WHEN POS_TITLE IN ('Athletic Operations Assistant',
                              'Digital Marketing Strategist',
                              'Accounting Techician',
                              'Marketing Technology Specialist',
                              'Prospect Research Specialist',
                              'Saints Shoppe Coordinator') THEN 'Business and Financial Operations Occupations'
            WHEN POS_TITLE IN ('IT Business System Analyst') THEN 'Computer, Engineering, and Science Occupations'
            WHEN POS_TITLE IN ('Athletic Eligibility Coordinator',
                              'Sports Information Director'
                                ) THEN
                'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Residential Life & Housing')
            THEN 'Service Occupations'
            WHEN POS_TITLE IN ('Administrative Assistant - Registrar')
                THEN 'Office and Administrative Support Occupations'
        END AS IPEDS_OCCUPATION_CATEGORY

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
LEFT JOIN SOC_CODES ON POSITION.POS_SOC_CODE = SOC_CODES.SOC_CODES_ID
WHERE PERSTAT_END_DATE IS NULL
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS != 'FAC'
AND GENDER = 'F') AS Q1
PIVOT (COUNT(PERSTAT_HRP_ID) FOR IPEDS_OCCUPATION_CATEGORY IN (
        [Archivists, Curators, and Museum Technicians],
       [Business and Financial Operations Occupations],
       [Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations],
       [Computer, Engineering, and Science Occupations],
       [Healthcare Practitioners and Technical Occupations],
       [Librarians and Media Collections Specialists],
        [Library Technicians],
       [Management Occupations],
       [Natural Resources, Construction, and Maintenance Occupations],
       [Office and Administrative Support Occupations],
       [Production, Transportation, and Material Moving Occupations],
       [Service Occupations],
       [Student and Academic Affairs and Other Education Services Occupations]
        )) AS Q2  --Page 2 (Women)


SELECT RACE_ETHNICITY,
       [Management Occupations],
       [Business and Financial Operations Occupations],
       [Computer, Engineering, and Science Occupations],
       [Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations],
       [Healthcare Practitioners and Technical Occupations]

FROM (
SELECT
        PERSTAT_HRP_ID,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE_ETHNICITY,
        CASE
            WHEN POS_SOC_CODE LIKE '25-401%' THEN 'Archivists, Curators, and Museum Technicians'
            WHEN POS_SOC_CODE LIKE '25-402%' THEN 'Librarians and Media Collections Specialists'
            WHEN POS_SOC_CODE LIKE '25-403%' THEN 'Library Technicians'
            WHEN (
                POS_SOC_CODE LIKE '25-2%'
                    OR POS_SOC_CODE LIKE '25-3%'
                    OR POS_SOC_CODE LIKE '25-9%'
                ) THEN 'Student and Academic Affairs and Other Education Services Occupations'
            WHEN POS_SOC_CODE LIKE '11%' THEN 'Management Occupations'
            WHEN POS_SOC_CODE LIKE '13%' THEN 'Business and Financial Operations Occupations'
            WHEN (
                POS_SOC_CODE LIKE '15%'
                    OR POS_SOC_CODE LIKE '17%'
                    OR POS_SOC_CODE LIKE '19%'
                ) THEN 'Computer, Engineering, and Science Occupations'
            WHEN (
                POS_SOC_CODE LIKE '21%'
                OR POS_SOC_CODE LIKE '23%'
                 OR POS_SOC_CODE LIKE '27%'
                ) THEN 'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_SOC_CODE LIKE '29%' THEN 'Healthcare Practitioners and Technical Occupations'
            WHEN (
                POS_SOC_CODE LIKE '31%'
                OR POS_SOC_CODE LIKE '33%'
                OR POS_SOC_CODE LIKE '35%'
                 OR POS_SOC_CODE LIKE '37%'
                OR POS_SOC_CODE LIKE '39%'
                ) THEN 'Service Occupations'
            WHEN POS_SOC_CODE LIKE '41%' THEN 'Sales and Related Occupations'
            WHEN POS_SOC_CODE LIKE '43%' THEN 'Office and Administrative Support Occupations'
            WHEN (
                POS_SOC_CODE LIKE '45%'
                OR POS_SOC_CODE LIKE '47%'
                OR POS_SOC_CODE LIKE '49%'
                ) THEN 'Natural Resources, Construction, and Maintenance Occupations'
            WHEN (
                POS_SOC_CODE LIKE '51%'
                OR POS_SOC_CODE LIKE '53%'
                ) THEN 'Production, Transportation, and Material Moving Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Academic Support',
                    'Assistant Director of Institutional Research',
                    'Director of Academic Technology',
                    'Director of Auxiliary Services',
                    'Director of Global Education') THEN 'Management Occupations'
            WHEN POS_TITLE IN ('Athletic Operations Assistant',
                              'Digital Marketing Strategist',
                              'Accounting Techician',
                              'Marketing Technology Specialist',
                              'Prospect Research Specialist',
                              'Saints Shoppe Coordinator') THEN 'Business and Financial Operations Occupations'
            WHEN POS_TITLE IN ('IT Business System Analyst') THEN 'Computer, Engineering, and Science Occupations'
            WHEN POS_TITLE IN ('Athletic Eligibility Coordinator',
                              'Sports Information Director'
                                ) THEN
                'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Residential Life & Housing')
            THEN 'Service Occupations'
            WHEN POS_TITLE IN ('Administrative Assistant - Registrar')
                THEN 'Office and Administrative Support Occupations'
        END AS IPEDS_OCCUPATION_CATEGORY

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
LEFT JOIN SOC_CODES ON POSITION.POS_SOC_CODE = SOC_CODES.SOC_CODES_ID
WHERE PERSTAT_END_DATE IS NULL
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS != 'FAC'
AND GENDER = 'M') AS Q1
PIVOT (COUNT(PERSTAT_HRP_ID) FOR IPEDS_OCCUPATION_CATEGORY IN (
        [Archivists, Curators, and Museum Technicians],
       [Business and Financial Operations Occupations],
       [Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations],
       [Computer, Engineering, and Science Occupations],
       [Healthcare Practitioners and Technical Occupations],
       [Librarians and Media Collections Specialists],
        [Library Technicians],
       [Management Occupations],
       [Natural Resources, Construction, and Maintenance Occupations],
       [Office and Administrative Support Occupations],
       [Production, Transportation, and Material Moving Occupations],
       [Service Occupations],
       [Student and Academic Affairs and Other Education Services Occupations]
        )) AS Q2  --Page 3 (Men)


SELECT RACE_ETHNICITY,
       [Management Occupations],
       [Business and Financial Operations Occupations],
       [Computer, Engineering, and Science Occupations],
       [Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations],
       [Healthcare Practitioners and Technical Occupations]

FROM (
SELECT
        PERSTAT_HRP_ID,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE_ETHNICITY,
        CASE
            WHEN POS_SOC_CODE LIKE '25-401%' THEN 'Archivists, Curators, and Museum Technicians'
            WHEN POS_SOC_CODE LIKE '25-402%' THEN 'Librarians and Media Collections Specialists'
            WHEN POS_SOC_CODE LIKE '25-403%' THEN 'Library Technicians'
            WHEN (
                POS_SOC_CODE LIKE '25-2%'
                    OR POS_SOC_CODE LIKE '25-3%'
                    OR POS_SOC_CODE LIKE '25-9%'
                ) THEN 'Student and Academic Affairs and Other Education Services Occupations'
            WHEN POS_SOC_CODE LIKE '11%' THEN 'Management Occupations'
            WHEN POS_SOC_CODE LIKE '13%' THEN 'Business and Financial Operations Occupations'
            WHEN (
                POS_SOC_CODE LIKE '15%'
                    OR POS_SOC_CODE LIKE '17%'
                    OR POS_SOC_CODE LIKE '19%'
                ) THEN 'Computer, Engineering, and Science Occupations'
            WHEN (
                POS_SOC_CODE LIKE '21%'
                OR POS_SOC_CODE LIKE '23%'
                 OR POS_SOC_CODE LIKE '27%'
                ) THEN 'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_SOC_CODE LIKE '29%' THEN 'Healthcare Practitioners and Technical Occupations'
            WHEN (
                POS_SOC_CODE LIKE '31%'
                OR POS_SOC_CODE LIKE '33%'
                OR POS_SOC_CODE LIKE '35%'
                 OR POS_SOC_CODE LIKE '37%'
                OR POS_SOC_CODE LIKE '39%'
                ) THEN 'Service Occupations'
            WHEN POS_SOC_CODE LIKE '41%' THEN 'Sales and Related Occupations'
            WHEN POS_SOC_CODE LIKE '43%' THEN 'Office and Administrative Support Occupations'
            WHEN (
                POS_SOC_CODE LIKE '45%'
                OR POS_SOC_CODE LIKE '47%'
                OR POS_SOC_CODE LIKE '49%'
                ) THEN 'Natural Resources, Construction, and Maintenance Occupations'
            WHEN (
                POS_SOC_CODE LIKE '51%'
                OR POS_SOC_CODE LIKE '53%'
                ) THEN 'Production, Transportation, and Material Moving Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Academic Support',
                    'Assistant Director of Institutional Research',
                    'Director of Academic Technology',
                    'Director of Auxiliary Services',
                    'Director of Global Education') THEN 'Management Occupations'
            WHEN POS_TITLE IN ('Athletic Operations Assistant',
                              'Digital Marketing Strategist',
                              'Accounting Techician',
                              'Marketing Technology Specialist',
                              'Prospect Research Specialist',
                              'Saints Shoppe Coordinator') THEN 'Business and Financial Operations Occupations'
            WHEN POS_TITLE IN ('IT Business System Analyst') THEN 'Computer, Engineering, and Science Occupations'
            WHEN POS_TITLE IN ('Athletic Eligibility Coordinator',
                              'Sports Information Director'
                                ) THEN
                'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Residential Life & Housing')
            THEN 'Service Occupations'
            WHEN POS_TITLE IN ('Administrative Assistant - Registrar')
                THEN 'Office and Administrative Support Occupations'
        END AS IPEDS_OCCUPATION_CATEGORY

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
LEFT JOIN SOC_CODES ON POSITION.POS_SOC_CODE = SOC_CODES.SOC_CODES_ID
WHERE PERSTAT_END_DATE IS NULL
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS != 'FAC'
AND GENDER = 'F') AS Q1
PIVOT (COUNT(PERSTAT_HRP_ID) FOR IPEDS_OCCUPATION_CATEGORY IN (
        [Archivists, Curators, and Museum Technicians],
       [Business and Financial Operations Occupations],
       [Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations],
       [Computer, Engineering, and Science Occupations],
       [Healthcare Practitioners and Technical Occupations],
       [Librarians and Media Collections Specialists],
        [Library Technicians],
       [Management Occupations],
       [Natural Resources, Construction, and Maintenance Occupations],
       [Office and Administrative Support Occupations],
       [Production, Transportation, and Material Moving Occupations],
       [Service Occupations],
       [Student and Academic Affairs and Other Education Services Occupations]
        )) AS Q2  --Page 3 (Women)

SELECT RACE_ETHNICITY,
    [Service Occupations],
    [Sales and Related Occupations],
    [Office and Administrative Support Occupations],
    [Natural Resources, Construction, and Maintenance Occupations],
    [Production, Transportation, and Material Moving Occupations]


FROM (
SELECT
        PERSTAT_HRP_ID,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE_ETHNICITY,
        CASE
            WHEN POS_SOC_CODE LIKE '25-401%' THEN 'Archivists, Curators, and Museum Technicians'
            WHEN POS_SOC_CODE LIKE '25-402%' THEN 'Librarians and Media Collections Specialists'
            WHEN POS_SOC_CODE LIKE '25-403%' THEN 'Library Technicians'
            WHEN (
                POS_SOC_CODE LIKE '25-2%'
                    OR POS_SOC_CODE LIKE '25-3%'
                    OR POS_SOC_CODE LIKE '25-9%'
                ) THEN 'Student and Academic Affairs and Other Education Services Occupations'
            WHEN POS_SOC_CODE LIKE '11%' THEN 'Management Occupations'
            WHEN POS_SOC_CODE LIKE '13%' THEN 'Business and Financial Operations Occupations'
            WHEN (
                POS_SOC_CODE LIKE '15%'
                    OR POS_SOC_CODE LIKE '17%'
                    OR POS_SOC_CODE LIKE '19%'
                ) THEN 'Computer, Engineering, and Science Occupations'
            WHEN (
                POS_SOC_CODE LIKE '21%'
                OR POS_SOC_CODE LIKE '23%'
                 OR POS_SOC_CODE LIKE '27%'
                ) THEN 'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_SOC_CODE LIKE '29%' THEN 'Healthcare Practitioners and Technical Occupations'
            WHEN (
                POS_SOC_CODE LIKE '31%'
                OR POS_SOC_CODE LIKE '33%'
                OR POS_SOC_CODE LIKE '35%'
                 OR POS_SOC_CODE LIKE '37%'
                OR POS_SOC_CODE LIKE '39%'
                ) THEN 'Service Occupations'
            WHEN POS_SOC_CODE LIKE '41%' THEN 'Sales and Related Occupations'
            WHEN POS_SOC_CODE LIKE '43%' THEN 'Office and Administrative Support Occupations'
            WHEN (
                POS_SOC_CODE LIKE '45%'
                OR POS_SOC_CODE LIKE '47%'
                OR POS_SOC_CODE LIKE '49%'
                ) THEN 'Natural Resources, Construction, and Maintenance Occupations'
            WHEN (
                POS_SOC_CODE LIKE '51%'
                OR POS_SOC_CODE LIKE '53%'
                ) THEN 'Production, Transportation, and Material Moving Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Academic Support',
                    'Assistant Director of Institutional Research',
                    'Director of Academic Technology',
                    'Director of Auxiliary Services',
                    'Director of Global Education') THEN 'Management Occupations'
            WHEN POS_TITLE IN ('Athletic Operations Assistant',
                              'Digital Marketing Strategist',
                              'Accounting Techician',
                              'Marketing Technology Specialist',
                              'Prospect Research Specialist',
                              'Saints Shoppe Coordinator') THEN 'Business and Financial Operations Occupations'
            WHEN POS_TITLE IN ('IT Business System Analyst') THEN 'Computer, Engineering, and Science Occupations'
            WHEN POS_TITLE IN ('Athletic Eligibility Coordinator',
                              'Sports Information Director'
                                ) THEN
                'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Residential Life & Housing')
            THEN 'Service Occupations'
            WHEN POS_TITLE IN ('Administrative Assistant - Registrar')
                THEN 'Office and Administrative Support Occupations'
        END AS IPEDS_OCCUPATION_CATEGORY

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
LEFT JOIN SOC_CODES ON POSITION.POS_SOC_CODE = SOC_CODES.SOC_CODES_ID
WHERE PERSTAT_END_DATE IS NULL
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS != 'FAC'
AND GENDER = 'M') AS Q1
PIVOT (COUNT(PERSTAT_HRP_ID) FOR IPEDS_OCCUPATION_CATEGORY IN (
        [Archivists, Curators, and Museum Technicians],
       [Business and Financial Operations Occupations],
       [Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations],
       [Computer, Engineering, and Science Occupations],
       [Healthcare Practitioners and Technical Occupations],
       [Librarians and Media Collections Specialists],
        [Library Technicians],
       [Management Occupations],
       [Natural Resources, Construction, and Maintenance Occupations],
       [Office and Administrative Support Occupations],
       [Production, Transportation, and Material Moving Occupations],
    [Sales and Related Occupations],
       [Service Occupations],
       [Student and Academic Affairs and Other Education Services Occupations]
        )) AS Q2  --Page 4 (Men)

SELECT RACE_ETHNICITY,
    [Service Occupations],
    [Sales and Related Occupations],
    [Office and Administrative Support Occupations],
    [Natural Resources, Construction, and Maintenance Occupations],
    [Production, Transportation, and Material Moving Occupations]


FROM (
SELECT
        PERSTAT_HRP_ID,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE_ETHNICITY,
        CASE
            WHEN POS_SOC_CODE LIKE '25-401%' THEN 'Archivists, Curators, and Museum Technicians'
            WHEN POS_SOC_CODE LIKE '25-402%' THEN 'Librarians and Media Collections Specialists'
            WHEN POS_SOC_CODE LIKE '25-403%' THEN 'Library Technicians'
            WHEN (
                POS_SOC_CODE LIKE '25-2%'
                    OR POS_SOC_CODE LIKE '25-3%'
                    OR POS_SOC_CODE LIKE '25-9%'
                ) THEN 'Student and Academic Affairs and Other Education Services Occupations'
            WHEN POS_SOC_CODE LIKE '11%' THEN 'Management Occupations'
            WHEN POS_SOC_CODE LIKE '13%' THEN 'Business and Financial Operations Occupations'
            WHEN (
                POS_SOC_CODE LIKE '15%'
                    OR POS_SOC_CODE LIKE '17%'
                    OR POS_SOC_CODE LIKE '19%'
                ) THEN 'Computer, Engineering, and Science Occupations'
            WHEN (
                POS_SOC_CODE LIKE '21%'
                OR POS_SOC_CODE LIKE '23%'
                 OR POS_SOC_CODE LIKE '27%'
                ) THEN 'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_SOC_CODE LIKE '29%' THEN 'Healthcare Practitioners and Technical Occupations'
            WHEN (
                POS_SOC_CODE LIKE '31%'
                OR POS_SOC_CODE LIKE '33%'
                OR POS_SOC_CODE LIKE '35%'
                 OR POS_SOC_CODE LIKE '37%'
                OR POS_SOC_CODE LIKE '39%'
                ) THEN 'Service Occupations'
            WHEN POS_SOC_CODE LIKE '41%' THEN 'Sales and Related Occupations'
            WHEN POS_SOC_CODE LIKE '43%' THEN 'Office and Administrative Support Occupations'
            WHEN (
                POS_SOC_CODE LIKE '45%'
                OR POS_SOC_CODE LIKE '47%'
                OR POS_SOC_CODE LIKE '49%'
                ) THEN 'Natural Resources, Construction, and Maintenance Occupations'
            WHEN (
                POS_SOC_CODE LIKE '51%'
                OR POS_SOC_CODE LIKE '53%'
                ) THEN 'Production, Transportation, and Material Moving Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Academic Support',
                    'Assistant Director of Institutional Research',
                    'Director of Academic Technology',
                    'Director of Auxiliary Services',
                    'Director of Global Education') THEN 'Management Occupations'
            WHEN POS_TITLE IN ('Athletic Operations Assistant',
                              'Digital Marketing Strategist',
                              'Accounting Techician',
                              'Marketing Technology Specialist',
                              'Prospect Research Specialist',
                              'Saints Shoppe Coordinator') THEN 'Business and Financial Operations Occupations'
            WHEN POS_TITLE IN ('IT Business System Analyst') THEN 'Computer, Engineering, and Science Occupations'
            WHEN POS_TITLE IN ('Athletic Eligibility Coordinator',
                              'Sports Information Director'
                                ) THEN
                'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
            WHEN POS_TITLE IN ('Assistant Director of Residential Life & Housing')
            THEN 'Service Occupations'
            WHEN POS_TITLE IN ('Administrative Assistant - Registrar')
                THEN 'Office and Administrative Support Occupations'
        END AS IPEDS_OCCUPATION_CATEGORY

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
LEFT JOIN SOC_CODES ON POSITION.POS_SOC_CODE = SOC_CODES.SOC_CODES_ID
WHERE PERSTAT_END_DATE IS NULL
AND PERSTAT_START_DATE <= '2024-11-01'
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS != 'FAC'
AND GENDER = 'F') AS Q1
PIVOT (COUNT(PERSTAT_HRP_ID) FOR IPEDS_OCCUPATION_CATEGORY IN (
        [Archivists, Curators, and Museum Technicians],
       [Business and Financial Operations Occupations],
       [Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations],
       [Computer, Engineering, and Science Occupations],
       [Healthcare Practitioners and Technical Occupations],
       [Librarians and Media Collections Specialists],
        [Library Technicians],
       [Management Occupations],
       [Natural Resources, Construction, and Maintenance Occupations],
       [Office and Administrative Support Occupations],
       [Production, Transportation, and Material Moving Occupations],
    [Sales and Related Occupations],
       [Service Occupations],
       [Student and Academic Affairs and Other Education Services Occupations]
        )) AS Q2  --Page 4 (Women)