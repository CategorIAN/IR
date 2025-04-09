SELECT ENROLL_TERM AS TERM,
       SUBJ_DESC AS SUBJECT,
       CAST(SUM(ENROLL_CREDITS) AS INT) AS SCH
FROM STUDENT_ENROLLMENT_VIEW AS SEV
JOIN SUBJECTS ON SEV.SECTION_SUBJECT = SUBJECTS.SUBJECTS_ID
WHERE ENROLL_TERM = '2025SP'
AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
GROUP BY ENROLL_TERM, SUBJ_DESC
ORDER BY SUBJ_DESC