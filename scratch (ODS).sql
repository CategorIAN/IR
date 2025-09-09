SELECT *
FROM ODS_FA_TERM_AWARDS
------------------------------------------------------------------------------------------------------------------------
SELECT DISTINCT AWARD_TYPE_DESC
FROM ODS_FA_TERM_AWARDS


SELECT *
FROM ODS_FA_TERM_AWARDS
WHERE AWARD_TYPE_DESC IN ('State', 'Other')
AND AWARD_ACTION_CATEGORY = 'A'


SELECT *
FROM ODS_FA_TERM_AWARDS
WHERE AWARD_CATEGORY_ID IN ('OUTSI', 'THRD')


------------------------------------------------------------------------------------------------------------------------



