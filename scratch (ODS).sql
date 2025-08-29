SELECT *
FROM ODS_FA_TERM_AWARDS
------------------------------------------------------------------------------------------------------------------------
SELECT *
FROM Z01_BE_TUITION_REVENUE
WHERE STTR_STUDENT = '5079083'

SELECT *
FROM Z01_BE_DINING_REVENUE
WHERE STTR_STUDENT = '5079083'

SELECT *
FROM Z01_BE_FEE_REVENUE
WHERE STTR_STUDENT = '5079083'

SELECT *
FROM Z01_BE_HOUSING_REVENUE_WITH_COHORTS
WHERE STTR_STUDENT = '5079083'
------------------------------------------------------------------------------------------------------------------------
SELECT *
FROM Z01_AR_CODES

SELECT *
FROM ODS_TERMS


SELECT *
FROM Z01_AR_INVOICE
WHERE PERSON_ID = '5079083'