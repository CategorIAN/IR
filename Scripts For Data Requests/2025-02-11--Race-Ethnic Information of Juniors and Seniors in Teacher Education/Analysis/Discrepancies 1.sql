SELECT *
FROM (
--(Begin 1)--------------------------------------------------------------------------
SELECT PERSON.ID,
             Z01.IPEDS_RACE_ETHNIC_DESC AS RACE_1,
             Z01.IPEDS_RACE_ETHNIC_DESC AS RACE_2
      FROM [2025SP_SNAPSHOT].[dbo].[Z01_ALL_RACE_ETHNIC_W_FLAGS] AS Z01
               JOIN PERSON ON Z01.ID = PERSON.ID
               JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV ON PERSON.ID = SAPV.STUDENT_ID
      WHERE PERSON.ID IN (
                          6178698,
                          6178698,
                          6180822,
                          6180822,
                          6180822,
                          6180748,
                          6180748,
                          6180748,
                          6175794,
                          6175794,
                          6175794,
                          6174545,
                          6174545,
                          6174545,
                          6174568,
                          6174568,
                          6174568,
                          6174568,
                          6178607,
                          6180612,
                          6180612,
                          6180612,
                          6179174,
                          6179174,
                          5495671,
                          5495671,
                          6179416,
                          6179416,
                          6179416,
                          6179868,
                          6179869,
                          6179868,
                          6179868,
                          6179869,
                          6179869,
                          6179868,
                          6179869,
                          6179901,
                          6179901,
                          6179901,
                          6179901,
                          6178666
          )
--(End 1)----------------------------------------------------------------------------
      ) AS X
WHERE RACE_1 != RACE_2


SELECT *
FROM STUDENT_ENROLLMENT_VIEW


SELECT *
FROM STUDENT_ACAD_PROGRAMS_VIEW