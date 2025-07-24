SELECT STA_STUDENT,
       STA_ACAD_LEVEL,
       STA_OTHER_COHORT_START_DATES,
       STA_OTHER_COHORT_END_DATES,
       VAL_EXTERNAL_REPRESENTATION AS COHORT
FROM STA_OTHER_COHORTS_VIEW
JOIN VALS ON VALCODE_ID = 'INSTITUTION.COHORTS'
AND STA_OTHER_COHORT_GROUPS = VALS.VAL_INTERNAL_CODE
WHERE VAL_EXTERNAL_REPRESENTATION IN (
                                        'Cheerleading',
                                        'Dance',
                                        'Football',
                                        'Indoor Men''s Track',
                                        'Indoor Women''s Track',
                                        'Men''s Basketball',
                                        'Men''s Basketball - JV',
                                        'Men''s Cross Country',
                                        'Men''s Golf',
                                        'Men''s Soccer',
                                        'Men''s Soccer - JV',
                                        'Outdoor Men''s Track',
                                        'Outdoor Women''s Track',
                                        'Women''s Basketball',
                                        'Women''s Basketball - JV',
                                        'Women''s Cross Country',
                                        'Women''s Golf',
                                        'Women''s Soccer',
                                        'Women''s  Softball',
                                        'Women''s Volleyball',
                                        'Women''s Volleyball - JV'
    )