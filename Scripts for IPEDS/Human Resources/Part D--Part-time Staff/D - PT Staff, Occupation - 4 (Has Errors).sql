SELECT RACE,
       [Service Occupations],
       [Sales and Related Occupations],
       [Office and Administrative Support Occupations],
       [Natural Resources, Construction, and Maintenance Occupations],
       [Production, Transportation, and Material Moving Occupations]

FROM (SELECT PERSON.ID,
             IPEDS_RACE_ETHNIC_DESC AS RACE,
             CASE
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '25-401%' THEN 'Archivists, Curators, and Museum Technicians'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '25-402%' THEN 'Librarians and Media Collections Specialists'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '25-403%' THEN 'Library Technicians'
----------------------------------------------------------------------------------------------------------------------
            WHEN (
                POS_SOC_CODE LIKE '25-2%'
                    OR POS_SOC_CODE LIKE '25-3%'
                    OR POS_SOC_CODE LIKE '25-9%'
                ) THEN 'Student and Academic Affairs and Other Education Services Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '11%' THEN 'Management Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '13%' THEN 'Business and Financial Operations Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN (
                POS_SOC_CODE LIKE '15%'
                    OR POS_SOC_CODE LIKE '17%'
                    OR POS_SOC_CODE LIKE '19%'
                ) THEN 'Computer, Engineering, and Science Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN (
                POS_SOC_CODE LIKE '21%'
                OR POS_SOC_CODE LIKE '23%'
                 OR POS_SOC_CODE LIKE '27%'
                ) THEN 'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '29%' THEN 'Healthcare Practitioners and Technical Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN (
                POS_SOC_CODE LIKE '31%'
                OR POS_SOC_CODE LIKE '33%'
                OR POS_SOC_CODE LIKE '35%'
                 OR POS_SOC_CODE LIKE '37%'
                OR POS_SOC_CODE LIKE '39%'
                ) THEN 'Service Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '41%' THEN 'Sales and Related Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '43%' THEN 'Office and Administrative Support Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN (
                POS_SOC_CODE LIKE '45%'
                OR POS_SOC_CODE LIKE '47%'
                OR POS_SOC_CODE LIKE '49%'
                ) THEN 'Natural Resources, Construction, and Maintenance Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN (
                POS_SOC_CODE LIKE '51%'
                OR POS_SOC_CODE LIKE '53%'
                ) THEN 'Production, Transportation, and Material Moving Occupations'
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_TITLE IN ('Assistant Director of Academic Support',
                    'Assistant Director of Institutional Research',
                    'Director of Academic Technology',
                    'Director of Auxiliary Services',
                    'Director of Global Education') THEN 'Management Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_TITLE IN ('Athletic Operations Assistant',
                              'Digital Marketing Strategist',
                              'Accounting Techician',
                              'Marketing Technology Specialist',
                              'Prospect Research Specialist',
                              'Saints Shoppe Coordinator',
                              'Digital Marketing Specialist') THEN 'Business and Financial Operations Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_TITLE IN ('IT Business System Analyst',
                              'Senior Designer/Web Manager') THEN 'Computer, Engineering, and Science Occupations'
----------------------------------------------------------------------------------------------------------------------
                 WHEN POS_TITLE IN ('Athletic Eligibility Coordinator',
                                    'Sports Information Director',
                                    'Special Populations Coordinator - Registrar'
                     ) THEN
                     'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_TITLE IN ('Assistant Director of Residential Life & Housing')
            THEN 'Service Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_TITLE IN ('Administrative Assistant - Registrar')
                THEN 'Office and Administrative Support Occupations'
----------------------------------------------------------------------------------------------------------------------
                 WHEN POS_TITLE LIKE '%Coach%'
                THEN 'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
-----------------------------------------------------------------------------------------------------------------------
                 END                AS IPEDS_OCCUPATION_CATEGORY

      FROM PERSTAT
               JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
               JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
               JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
      WHERE (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= (
          SELECT TOP 1 TERM_START_DATE
          FROM TERMS
          WHERE TERMS_ID = '2024FA'
          ))
        AND PERSTAT_START_DATE <= '2024-11-01'
        AND PERSTAT_STATUS NOT IN ('FT', 'VOL', 'STU')
        AND POS_TYPE != 'TPT'
        AND POS_TITLE NOT IN ('Part Time Grounds Worker', 'Fitness Instructor', 'PT Librarian')
        AND POS_TITLE NOT LIKE '%Lab Coordinator%'
        AND POS_TITLE NOT LIKE '%Announcer%'
        AND POS_TITLE NOT LIKE '%Administrative Assistant%'
        AND GENDER = 'M') AS X

PIVOT (COUNT(ID) FOR IPEDS_OCCUPATION_CATEGORY IN ([Service Occupations],
       [Sales and Related Occupations],
       [Office and Administrative Support Occupations],
       [Natural Resources, Construction, and Maintenance Occupations],
       [Production, Transportation, and Material Moving Occupations])) AS Y --Men
-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
SELECT RACE,
       [Service Occupations],
       [Sales and Related Occupations],
       [Office and Administrative Support Occupations],
       [Natural Resources, Construction, and Maintenance Occupations],
       [Production, Transportation, and Material Moving Occupations]
FROM (SELECT PERSON.ID,
             IPEDS_RACE_ETHNIC_DESC AS RACE,
             CASE
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '25-401%' THEN 'Archivists, Curators, and Museum Technicians'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '25-402%' THEN 'Librarians and Media Collections Specialists'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '25-403%' THEN 'Library Technicians'
----------------------------------------------------------------------------------------------------------------------
            WHEN (
                POS_SOC_CODE LIKE '25-2%'
                    OR POS_SOC_CODE LIKE '25-3%'
                    OR POS_SOC_CODE LIKE '25-9%'
                ) THEN 'Student and Academic Affairs and Other Education Services Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '11%' THEN 'Management Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '13%' THEN 'Business and Financial Operations Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN (
                POS_SOC_CODE LIKE '15%'
                    OR POS_SOC_CODE LIKE '17%'
                    OR POS_SOC_CODE LIKE '19%'
                ) THEN 'Computer, Engineering, and Science Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN (
                POS_SOC_CODE LIKE '21%'
                OR POS_SOC_CODE LIKE '23%'
                 OR POS_SOC_CODE LIKE '27%'
                ) THEN 'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '29%' THEN 'Healthcare Practitioners and Technical Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN (
                POS_SOC_CODE LIKE '31%'
                OR POS_SOC_CODE LIKE '33%'
                OR POS_SOC_CODE LIKE '35%'
                 OR POS_SOC_CODE LIKE '37%'
                OR POS_SOC_CODE LIKE '39%'
                ) THEN 'Service Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '41%' THEN 'Sales and Related Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_SOC_CODE LIKE '43%' THEN 'Office and Administrative Support Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN (
                POS_SOC_CODE LIKE '45%'
                OR POS_SOC_CODE LIKE '47%'
                OR POS_SOC_CODE LIKE '49%'
                ) THEN 'Natural Resources, Construction, and Maintenance Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN (
                POS_SOC_CODE LIKE '51%'
                OR POS_SOC_CODE LIKE '53%'
                ) THEN 'Production, Transportation, and Material Moving Occupations'
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_TITLE IN ('Assistant Director of Academic Support',
                    'Assistant Director of Institutional Research',
                    'Director of Academic Technology',
                    'Director of Auxiliary Services',
                    'Director of Global Education') THEN 'Management Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_TITLE IN ('Athletic Operations Assistant',
                              'Digital Marketing Strategist',
                              'Accounting Techician',
                              'Marketing Technology Specialist',
                              'Prospect Research Specialist',
                              'Saints Shoppe Coordinator',
                              'Digital Marketing Specialist') THEN 'Business and Financial Operations Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_TITLE IN ('IT Business System Analyst',
                              'Senior Designer/Web Manager') THEN 'Computer, Engineering, and Science Occupations'
----------------------------------------------------------------------------------------------------------------------
                 WHEN POS_TITLE IN ('Athletic Eligibility Coordinator',
                                    'Sports Information Director',
                                    'Special Populations Coordinator - Registrar'
                     ) THEN
                     'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_TITLE IN ('Assistant Director of Residential Life & Housing')
            THEN 'Service Occupations'
----------------------------------------------------------------------------------------------------------------------
            WHEN POS_TITLE IN ('Administrative Assistant - Registrar')
                THEN 'Office and Administrative Support Occupations'
----------------------------------------------------------------------------------------------------------------------
                 WHEN POS_TITLE LIKE '%Coach%'
                THEN 'Community, Social Service, Legal, Arts, Design, Entertainment, Sports, and Media Occupations'
-----------------------------------------------------------------------------------------------------------------------
                 END                AS IPEDS_OCCUPATION_CATEGORY

      FROM PERSTAT
               JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
               JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
               JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
      WHERE (PERSTAT_END_DATE IS NULL OR PERSTAT_END_DATE >= (
          SELECT TOP 1 TERM_START_DATE
          FROM TERMS
          WHERE TERMS_ID = '2024FA'
          ))
        AND PERSTAT_START_DATE <= '2024-11-01'
        AND PERSTAT_STATUS NOT IN ('FT', 'VOL', 'STU')
        AND POS_TYPE != 'TPT'
        AND POS_TITLE NOT IN ('Part Time Grounds Worker', 'Fitness Instructor', 'PT Librarian')
        AND POS_TITLE NOT LIKE '%Lab Coordinator%'
        AND POS_TITLE NOT LIKE '%Announcer%'
        AND POS_TITLE NOT LIKE '%Administrative Assistant%'
        AND GENDER = 'F') AS X

PIVOT (COUNT(ID) FOR IPEDS_OCCUPATION_CATEGORY IN ([Service Occupations],
       [Sales and Related Occupations],
       [Office and Administrative Support Occupations],
       [Natural Resources, Construction, and Maintenance Occupations],
       [Production, Transportation, and Material Moving Occupations])) AS Y --Women