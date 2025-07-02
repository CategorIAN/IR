--(Begin 2)-----------------------------------------------------------------------------------
                      SELECT *
                      FROM (
--(Begin 1)-----------------------------------------------------------------------------------
                               SELECT
                                      PAV.*,
                                      ROW_NUMBER() OVER (PARTITION BY PAV.ID ORDER BY ADDRESS_ADD_DATE) AS ADDRESS_RANK
                               FROM PERSON_ADDRESSES_VIEW AS PAV
                               JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                               WHERE ADDRESS_TYPE = 'H'
--(End 1)-------------------------------------------------------------------------------------
                           ) AS X
                      WHERE ADDRESS_RANK = 1
                      AND STATE IS NULL
--(End 2)-------------------------------------------------------------------------------------