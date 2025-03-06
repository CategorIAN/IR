SELECT
        PERSTAT_HRP_ID,
        PERSON.LAST_NAME,
        PERSON.FIRST_NAME,
        POSITION.POS_TITLE,
        POSITION.POS_SOC_CODE,
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
        END AS IPEDS_OCCUPATION_CATEGORY,
        SOC_CODES.SOC_DESC

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
LEFT JOIN SOC_CODES ON POSITION.POS_SOC_CODE = SOC_CODES.SOC_CODES_ID
WHERE PERSTAT_END_DATE IS NULL
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS != 'FAC'
ORDER BY POS_SOC_CODE, LAST_NAME, FIRST_NAME


SELECT POSITION_ID,
       POS_TITLE,
       POS_SOC_CODE

FROM PERSTAT
JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
LEFT JOIN SOC_CODES ON POSITION.POS_SOC_CODE = SOC_CODES.SOC_CODES_ID
WHERE PERSTAT_END_DATE IS NULL
AND PERSTAT_STATUS = 'FT'
AND POS_CLASS != 'FAC'
AND POS_SOC_CODE IS NULL
ORDER BY POS_TITLE