SELECT *
FROM AWARDS
WHERE AW_DESCRIPTION IN (
                            'VA Allowances (Books, Supplies, Housing)',
                            'VA Ben/Stipend',
                            'VA Ben/Tuition',
                            'VA Yellow Ribbon Carroll Match',
                            'VA Yellow Ribbon Fees',
                            'VA Yellow Ribbon Match'
    )

SELECT *
FROM F22_AWARD_LIST
JOIN AWARDS ON SA_AWARD = AW_ID
WHERE AW_DESCRIPTION IN (
                            'VA Allowances (Books, Supplies, Housing)',
                            'VA Ben/Stipend',
                            'VA Ben/Tuition',
                            'VA Yellow Ribbon Carroll Match',
                            'VA Yellow Ribbon Fees',
                            'VA Yellow Ribbon Match'
    )


SELECT *
FROM STUDENT_ACAD_PROGRAMS_VIEW
WHERE STUDENT_ID = '6184539'


