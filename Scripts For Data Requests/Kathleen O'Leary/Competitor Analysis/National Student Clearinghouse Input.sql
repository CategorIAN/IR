SELECT 'D1' AS TYPE,
       '' AS SS,
       PERSON.FIRST_NAME,
       LEFT(PERSON.MIDDLE_NAME, 1) AS MI,
       PERSON.LAST_NAME,
       PERSON.SUFFIX,
       FORMAT(BIRTH_DATE, 'yyyymmdd') AS BD,
       FORMAT(CAST('10/01/2024' AS DATE),'yyyymmdd') AS SD,
       '' AS BLK,
       '002526' AS CODE,
       '00' AS BRANCH,
       PERSON.ID
FROM PERSON