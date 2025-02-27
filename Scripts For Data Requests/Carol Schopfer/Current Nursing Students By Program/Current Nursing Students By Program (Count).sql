SELECT NURSING_PROGRAM
		, Count(*) as STUDENT_COUNT
FROM ( 
		SELECT CURRENT_MAJORS.MAJ_DESC AS MAJOR,
			   STUDENT_ID,
			   SAPV.STP_PROGRAM_TITLE AS NURSING_PROGRAM
		FROM MAJORS AS CURRENT_MAJORS
		CROSS JOIN (SELECT * FROM STUDENT_ACAD_PROGRAMS_VIEW WHERE STP_CURRENT_STATUS = 'Active') AS SAPV
		LEFT JOIN STPR_MAJOR_LIST_VIEW ON SAPV.STUDENT_ID = STPR_MAJOR_LIST_VIEW.STPR_STUDENT AND SAPV.STP_ACADEMIC_PROGRAM = STPR_MAJOR_LIST_VIEW.STPR_ACAD_PROGRAM
		LEFT JOIN MAJORS AS ADDNL_MAJOR ON STPR_MAJOR_LIST_VIEW.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
		LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
		WHERE CURRENT_MAJORS.MAJ_DESC = 'Nursing'
		AND (
		CURRENT_MAJORS.MAJ_DESC = MAIN_MAJOR.MAJ_DESC
		OR (
			CURRENT_MAJORS.MAJ_DESC = ADDNL_MAJOR.MAJ_DESC
			AND STPR_MAJOR_LIST_VIEW.STPR_ADDNL_MAJOR_END_DATE IS NULL
			)
		)
		GROUP BY CURRENT_MAJORS.MAJ_DESC, STUDENT_ID, SAPV.STP_PROGRAM_TITLE
	) AS STUDENT_MAJORS
GROUP BY NURSING_PROGRAM
ORDER BY NURSING_PROGRAM
				
