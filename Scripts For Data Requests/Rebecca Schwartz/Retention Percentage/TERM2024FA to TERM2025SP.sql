SELECT *
FROM (
	SELECT	PERSON.ID
			,PERSON.LAST_NAME
			,PERSON.FIRST_NAME
			,LATEST_STATUS.STP_PROGRAM_TITLE AS LATEST_PROGRAM
			,LATEST_STATUS.STP_CURRENT_STATUS AS LATEST_STATUS
			,LATEST_STATUS.STP_END_DATE AS LATEST_STATUS_DATE
			,TERM_2024FA.STUDENT_ID AS TERM_2024FA
			,TERM_2025SP.STUDENT_ID AS TERM_2025SP
	FROM PERSON
	JOIN (
			SELECT STUDENT_ID, STP_PROGRAM_TITLE, STP_CURRENT_STATUS, STP_END_DATE
			FROM (
				SELECT STUDENT_ID
				,STP_CURRENT_STATUS
				,STP_END_DATE
				,STP_PROGRAM_TITLE
				,ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
				FROM STUDENT_ACAD_PROGRAMS_VIEW
				WHERE STP_CURRENT_STATUS != 'Changed Program'
				AND STP_START_DATE IS NOT NULL
			) ranked
			WHERE rn = 1
			) AS LATEST_STATUS ON LATEST_STATUS.STUDENT_ID = PERSON.ID
	JOIN (
		SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
		WHERE ENROLL_TERM = '2024FA'
		AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
	) AS TERM_2024FA ON PERSON.ID = TERM_2024FA.STUDENT_ID
	LEFT JOIN (
		SELECT DISTINCT STUDENT_ID FROM STUDENT_ENROLLMENT_VIEW
		WHERE ENROLL_TERM = '2025SP'
		AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
	) AS TERM_2025SP ON PERSON.ID = TERM_2025SP.STUDENT_ID
	

	WHERE TERM_2025SP.STUDENT_ID IS NULL
) AS LOST
ORDER BY LATEST_STATUS, LATEST_PROGRAM, LATEST_STATUS_DATE, LAST_NAME, FIRST_NAME
