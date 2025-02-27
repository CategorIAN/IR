SELECT ENROLL_TERM  as Term, [Freshman], [Sophomore], [Junior], [Senior], [Non-Cohort],
		[Freshman] + [Sophomore] + [Junior] + [Senior] + [Non-Cohort] as Total
FROM (
SELECT ENROLL_TERM
		,CLASS_LEVEL
		,COUNT(*) AS STUDENT_COUNT
	FROM (
	SELECT ENROLL_TERM
		  ,CASE 
				WHEN STUDENT_CLASS_LEVEL IN ('Freshman', 'Sophomore', 'Junior', 'Senior')
				THEN STUDENT_CLASS_LEVEL
				ELSE 'Non-Cohort'
				END AS CLASS_LEVEL
			,STUDENT_ID
	FROM STUDENT_ENROLLMENT_VIEW
	WHERE ENROLL_TERM IN ('2018SP', '2019SP', '2020SP', '2021SP', '2022SP', '2023SP', '2024SP', '2025SP')
	GROUP BY ENROLL_TERM, STUDENT_CLASS_LEVEL, STUDENT_ID
	) AS X
GROUP BY ENROLL_TERM, CLASS_LEVEL
) AS Y
PIVOT (
	SUM(STUDENT_COUNT) FOR CLASS_LEVEL IN ([Freshman], [Sophomore], [Junior], [Senior], [Non-Cohort])
	) AS PivotTable
