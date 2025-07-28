SELECT *
FROM Z01_TA_ACYR_PLUS
WHERE AWARD_DESCRIPTION IN (
                            'VA Allowances (Books, Supplies, Housing)',
                            'VA Ben/Stipend',
                            'VA Ben/Tuition',
                            'VA Yellow Ribbon Carroll Ribbon Match',
                            'VA Yellow Ribbon Fees',
                            'VA Yellow Ribbon Match'
    )
AND TA_TERM_ACTION = 'A'