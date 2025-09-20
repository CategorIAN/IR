from Reports import Reports
import os
from IPEDS import IPEDS

class IPEDS_Fall (IPEDS):
    def __init__(self):
        super().__init__(folder='IPEDS_Fall', report="2025-09-17-IPEDS Fall Survey")
#==============================Cost 1=================================================================================
#==============================Screening Questions=====================================================================
    '''
    Status: Completed
    '''
    def getScreeningQuestions_1(self):
        prompt = f"""
        1. Does your institution offer institutionally-controlled housing (on-campus and/or off-campus)?
        If you answer Yes to this question, you will be expected to specify a housing capacity, and to report a housing 
        charge or a combined food and housing charge.
        """
        comments = """
        Yes, we offer institutionally-controlled housing. Our housing capacity for the 2025-26 academic year is 952.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Screening Questions",
                  "page": "Screening Questions",
                  "name": "Question 1",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getScreeningQuestions_2(self):
        prompt = f"""
        2. Are all full-time, first-time degree/certificate-seeking students required to live on campus or in 
        institutionally controlled housing?
        This is only a screening question, and your response does not show up on College Navigator.

        If you answer Yes to this question, you will not be asked to report off-campus food and housing in the cost of 
        attendance. If you make ANY exceptions to this rule, please answer No so that this does not cause conflicts with
         the average net price calculation. Misreporting may lead to an inaccurate average net price calculation for 
         your institution.
        """
        comments = """
        No
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Screening Questions",
                  "page": "Screening Questions",
                  "name": "Question 2",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getScreeningQuestions_3(self):
        prompt = f"""
        3. Does your institution charge different tuition rates for in-district, in-state, or out-of-state students?
        If you answer Yes to this question, you will be expected to report different tuition amounts for in-district, 
        in-state, and out-of-state students (as applicable).

        Only select YES if you charge different tuition by students’ residence status. You should not select YES and 
        then report the same tuition rate 3 times.
        """
        comments = """
        No
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Screening Questions",
                  "page": "Screening Questions",
                  "name": "Question 3",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getScreeningQuestions_4(self):
        prompt = f"""
        4. Do you offer food or meal plans to your students?
        If you answer Yes to this question, you will be expected to report a food charge or combined food and housing 
        charge (C10).
        """
        comments = """
        Yes - Number of meals per week can vary (e.g., students charge meals against a meal card)
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Screening Questions",
                  "page": "Screening Questions",
                  "name": "Question 4",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getScreeningQuestions_5(self):
        prompt = f"""
        5. Does your institution charge an application fee?
        """
        comments = """
        No
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Screening Questions",
                  "page": "Screening Questions",
                  "name": "Question 5",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getScreeningQuestions_7(self):
        prompt = f"""
        7. Indicate whether or not your institution participates in a Promise program.
        """
        comments = """
        No
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Screening Questions",
                  "page": "Screening Questions",
                  "name": "Question 7",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getScreeningQuestions_8(self):
        prompt = f"""
        8. Indicate whether or not any of the following alternative tuition plans are offered by your institution.
        """
        comments = """
        Yes, we offer the Tuition payment plan.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Screening Questions",
                  "page": "Screening Questions",
                  "name": "Question 8",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getScreeningQuestions_9(self):
        prompt = f"""
        9. For the purposes of awarding institutional financial aid, does your institution require asset information from 
        students who qualify for the exemption from asset reporting on the FAFSA form?
        """
        comments = """
        No
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Screening Questions",
                  "page": "Screening Questions",
                  "name": "Question 9",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getScreeningQuestions_10(self):
        prompt = f"""
        10. For the purpose of awarding institutional financial aid, does your institution require additional financial 
        information separate from the FAFSA form?
        """
        comments = """
        No
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Screening Questions",
                  "page": "Screening Questions",
                  "name": "Question 10",
                  "func_dict": None,
                  }
        self.save(**params)
#=======================================Section 1 - Student Charges (Part B)============================================
    '''
    Status: Completed
    '''
    def getTuition(self):
        prompt = f"""
        Tuition for the 2025-26 Academic Year
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs, the annual tuition is $41,670.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part B - Cost of Attendance for FTFTUG",
                  "name": "1. Tuition",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getTuition_Guarantee(self):
        prompt = f"""
        Is there a program where the institution guarantees, to entering first-time students, that tuition will not 
        increase for the years they are enrolled. These guarantees are generally time-bound for four or five years.
        """
        comments = """
        No, there is not. Do not check the box. Do not fill in the 'Guaranteed increase %' box.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part B - Cost of Attendance for FTFTUG",
                  "name": "2. Is There A Tuition Guarantee",
                  "func_dict": None,
                  }
        self.save(**params)


    '''
    Status: Completed
    '''
    def getRequiredFees(self):
        prompt = f"""
        Required Fees for the 2025-26 Academic Year
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs, the fixed fees is $1,400.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part B - Cost of Attendance for FTFTUG",
                  "name": "3. Required Fees",
                  "func_dict": None,
                  }
        self.save(**params)


    '''
    Status: Completed
    '''
    def getRequiredFees_Guarantee(self):
        prompt = f"""
        Is there a program where the institution guarantees, to entering first-time students, that tuition will not 
        increase for the years they are enrolled. These guarantees are generally time-bound for four or five years.
        """
        comments = """
        No, there is not. Do not check the box. Do not fill in the 'Guaranteed increase %' box.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part B - Cost of Attendance for FTFTUG",
                  "name": "4. Is There A Required Fees Guarantee",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getBooksAndSupplies(self):
        prompt = f"""
        Books and Supplies for the 2025-26 Academic Year
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs, the allowance for Books and Supplies is $800.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part B - Cost of Attendance for FTFTUG",
                  "name": "5. Books and Supplies",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getFoodAndHousing(self):
        prompt = f"""
        Food and housing for the 2025-26 Academic Year
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs, the annual housing and food is $12,060.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part B - Cost of Attendance for FTFTUG",
                  "name": "6. Food and Housing",
                  "func_dict": None,
                  }
        self.save(**params)


    '''
    Status: Completed
    '''
    def getOtherExpenses(self):
        prompt = f"""
        The amount of money (estimated by the financial aid office) needed by a student to cover expenses such as 
        laundry, transportation, and entertainment.
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs, the other expenses totals $1,900 
        (Personal Expenses) + $1,400 (Transportation Expenses) + $72 (Loan Fees) = $3,372
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part B - Cost of Attendance for FTFTUG",
                  "name": "7. Other Expenses",
                  "func_dict": None,
                  }
        self.save(**params)


    '''
    Status: Completed
    '''
    def getFoodAndHousing_Off_Campus(self):
        prompt = f"""
        Food and housing (Off-Campus) for the 2025-26 Academic Year
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs, the annual housing and food is is $12,060.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part B - Cost of Attendance for FTFTUG",
                  "name": "8. Food and Housing Off-Campus",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getOtherExpenses_Off_Campus(self):
        prompt = f"""
        The amount of money (estimated by the financial aid office) needed by a student to cover expenses such as 
        laundry, transportation, and entertainment.
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs, the other expenses totals $1,900 
        (Personal Expenses) + $1,400 (Transportation Expenses) + $72 (Loan Fees) = $3,372
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part B - Cost of Attendance for FTFTUG",
                  "name": "9. Other Expenses (Off-Campus)",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getFoodAndHousing_Off_Campus_W_Family(self):
        prompt = f"""
        Food and housing (Off-Campus with Family) for the 2025-26 Academic Year
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs, the annual housing and food if a student 
        lives with parents is $2,474.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part B - Cost of Attendance for FTFTUG",
                  "name": "10. F and H Off-Campus With Family",
                  "func_dict": None,
                  }
        self.save(**params)


    '''
    Status: Completed
    '''
    def getOtherExpenses_Off_Campus_W_Family(self):
        prompt = f"""
        The amount of money (estimated by the financial aid office) needed by a student to cover expenses such as 
        laundry, transportation, and entertainment.
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs, the other expenses totals $1,900 
        (Personal Expenses) + $1,400 (Transportation Expenses) + $72 (Loan Fees) = $3,372
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part B - Cost of Attendance for FTFTUG",
                  "name": "11. Other Exp. Off-Campus With Family",
                  "func_dict": None,
                  }
        self.save(**params)


    '''
    Status: Completed
    '''
    def provideAdditionalInfo(self):
        prompt = f"""
        You may use the box below to provide additional context for the data you have reported above. Context notes will
        be posted on the College Navigator website. Therefore, you should write all context notes using proper grammar
        (e.g., complete sentences with punctuation) and common language that can be easily understood by students and
        parents (e.g., spell out acronyms).
        """
        comments = """
        Do not check any of the boxes.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part B - Cost of Attendance for FTFTUG",
                  "name": "12. Provide Additional Info",
                  "func_dict": None,
                  }
        self.save(**params)

#===============================Section 1 - Student Charges (Part C)====================================================

    '''
    Status: Completed
    '''
    def getUG_FT_Tuition(self):
        prompt = f"""
        Average tuition to all students in (Undergraduate Full-Time) category for the full academic year 2025-26.
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs, the Annual Full-Time Tuition is $41,670.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part C - Tuition and Required Fees for UG and G",
                  "name": "1. Tuition for FT UG",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getUG_FT_RequiredFees(self):
        prompt = f"""
        Required fees to all students in (Undergraduate Full-Time) category for the full academic year 2025-26.
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs, the Fixed Fees is $1400.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part C - Tuition and Required Fees for UG and G",
                  "name": "2. Required Fees for FT UG",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getUG_PT_TuitionPerCredit(self):
        prompt = f"""
        Tuition per credit to all students in (Undergraduate Part-Time) category for the full academic year 2025-26.
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs/cost-attendance, the 
        'Tuition Part Time under 12 credits' rate is $1,736.00.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part C - Tuition and Required Fees for UG and G",
                  "name": "3. Tuition Rate for PT UG",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getUG_PT_RequiredFees(self):
        prompt = f"""
        Required fees to all students in (Undergraduate Part-Time) category for the full academic year 2025-26.
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs/cost-attendance, the Student Part-Time Fee is 
        2 * $350 = $700.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part C - Tuition and Required Fees for UG and G",
                  "name": "4. Required Fees for PT UG",
                  "func_dict": None,
                  }
        self.save(**params)


    '''
    Status: Completed
    '''
    def getGR_FT_Tuition(self):
        prompt = f"""
        Average tuition to all students in (Graduate Full-Time) category for the full academic year 2025-26.
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs/cost-attendance, the full-time tuition for 
        MSW students for the year is ($750 / credit) * (18 credits / year) = $13,500.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part C - Tuition and Required Fees for UG and G",
                  "name": "5. Tuition for FT GR",
                  "func_dict": None,
                  }
        self.save(**params)


    '''
    Status: Completed
    '''
    def getGR_FT_RequiredFees(self):
        prompt = f"""
        Required fees to all students in (Graduate Full-Time) category for the full academic year 2025-26.
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs/cost-attendance, the required fees for the 
        full-time MSW students is 2 * (Master Fee (8 credits or more)) = 2 * ($700) = $1400. 
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part C - Tuition and Required Fees for UG and G",
                  "name": "6. Required Fees for FT GR",
                  "func_dict": None,
                  }
        self.save(**params)


    '''
    Status: Completed
    '''
    def getGR_PT_TuitionPerCredit(self):
        prompt = f"""
        Average tuition rate to all students in (Graduate Part-Time) category for the full academic year 2025-26.
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs/cost-attendance, the part-time tuition rate for 
        MSW students for the year is $750 / credit.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part C - Tuition and Required Fees for UG and G",
                  "name": "7. Tuition Rate for PT GR",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getGR_PT_RequiredFees(self):
        prompt = f"""
        Required fees to all students in (Graduate Part-Time) category for the full academic year 2025-26.
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs/cost-attendance, the required fees for the 
        part-time MSW students is 2 * (Master Fee (7 credits or less)) = 2 * ($350) = $700. 
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part C - Tuition and Required Fees for UG and G",
                  "name": "8. Required Fees for PT GR",
                  "func_dict": None,
                  }
        self.save(**params)


#===============================Section 1 - Student Charges (Part E)====================================================

    '''
    Status: Completed
    '''
    def getHousingCharge(self):
        prompt = f"""
        Housing charge (Double occupancy)
        """
        comments = """
        According to https://www.carroll.edu/admission-aid/tuition-costs/cost-attendance, the Housing charge with double
        occupancy for the academic year is 2 * ($2,955) = $5,910.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part E - Food and Housing",
                  "name": "1. Housing Charge (Double Occupancy)",
                  "func_dict": None,
                  }
        self.save(**params)

    '''
    Status: Completed
    '''
    def getFoodCharge(self):
        prompt = f"""
        Food charge (Maximum Plan)
        """
        comments = """
        According to https://www.carroll.edu/student-life/housing-dining/dining-meal-plans, the Food plan for the
        maximum plan (Platinum) for the academic year is 2 * ($3,296) = $6,592.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part E - Food and Housing",
                  "name": "2. Food Charge (Maximum Plan)",
                  "func_dict": None,
                  }
        self.save(**params)


    '''
    Status: Completed
    '''
    def getCombinedFoodAndHousingCharge(self):
        prompt = f"""
        Combined food and housing charge
        (Answer only if you CANNOT separate food and housing charges.)
        """
        comments = """
        Leave this box blank because we are able to separate the food and housing charges.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Cost 1",
                  "section": "Section 1 - Student Charges",
                  "page": "Part E - Food and Housing",
                  "name": "3. Combined Food and Housing Charge",
                  "func_dict": None,
                  }
        self.save(**params)
#===============================Completions============================================================================

    def getCompletions(self, cip, major_rank = 1):
        query = f"""
                 SELECT IPEDS_RACE.THEIR_DESC AS RACE,
                 IPEDS_RACE.N,
                 STUDENT_ID             AS ID,
                 STUDENT_GENDER AS GENDER
        FROM ({self.ipeds_races()}) AS IPEDS_RACE
         LEFT JOIN (
                    SELECT STUDENT_ID,
                           STUDENT_GENDER,
                           IPEDS_RACE_ETHNIC_DESC,
                           ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY MAJORS_ID) AS MAJOR_RANK
                    FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                    LEFT JOIN ACAD_PROGRAMS AS AP
                    ON SAPV.STP_ACADEMIC_PROGRAM = AP.ACAD_PROGRAMS_ID
                    LEFT JOIN (
                        SELECT MAJORS_ID,
                               'Program Major' AS MAJOR_TYPE,
                               NULL AS STUDENT_PROGRAMS_ID,
                               NULL AS STPR_ADDNL_MAJOR_END_DATE
                        FROM MAJORS
                        UNION
                        SELECT MAJORS_ID,
                               'Additional Major',
                               STUDENT_PROGRAMS_ID,
                               STPR_ADDNL_MAJOR_END_DATE
                        FROM STPR_MAJOR_LIST
                        JOIN MAJORS ON STPR_MAJOR_LIST.STPR_ADDNL_MAJORS = MAJORS.MAJORS_ID
                    ) AS ALL_MAJORS
                        ON (
                               MAJOR_TYPE = 'Program Major'
                                AND SAPV.STP_MAJOR1 = ALL_MAJORS.MAJORS_ID
                            )
                        OR (
                                MAJOR_TYPE = 'Additional Major'
                                AND SAPV.STUDENT_ID + '*' + SAPV.STP_ACADEMIC_PROGRAM = ALL_MAJORS.STUDENT_PROGRAMS_ID
                                AND COALESCE(STPR_ADDNL_MAJOR_END_DATE, STP_END_DATE) >= STP_END_DATE
                            )
                    WHERE STP_CURRENT_STATUS = 'Graduated'
                    AND STP_END_DATE BETWEEN '2024-07-01' AND '2025-06-30'
                    AND ACPG_CIP = '{cip}'
                    ) AS STUDENT_PROGRAMS
            ON IPEDS_RACE.OUR_DESC = STUDENT_PROGRAMS.IPEDS_RACE_ETHNIC_DESC
            AND MAJOR_RANK = {major_rank}
        """
        return query

    def getCompletions_030103(self):
        prompt = """
        "03.0103: Environmental Studies" Completers"
        """
        comments = None
        query = self.getCompletions('03.0103')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "03.0103",
                  "name": "03.0103 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_030103_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "03.0103",
                  "name": "03.0103 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_090101(self):
        prompt = """
        "09.0101: Speech Communication and Rhetoric"
        """
        comments = None
        query = self.getCompletions('09.0101')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "09.0101",
                  "name": "09.0101 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_090101_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "09.0101",
                  "name": "09.0101 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_090902(self):
        prompt = """
        "09.0902: Public Relations/Image Management"
        """
        comments = None
        query = self.getCompletions('09.0902')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "09.0902",
                  "name": "09.0902 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_090902_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "09.0902",
                  "name": "09.0902 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_110501(self):
        prompt = """
        "11.0501: Computer Systems Analysis/Analyst"
        """
        comments = None
        query = self.getCompletions('11.0501')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "11.0501",
                  "name": "11.0501 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)


    def getCompletions_110501_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "11.0501",
                  "name": "11.0501 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_110701(self):
        prompt = """
        "11.0701: Computer Science"
        """
        comments = None
        query = self.getCompletions('11.0701')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "11.0701",
                  "name": "11.0701 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)


    def getCompletions_110701_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "11.0701",
                  "name": "11.0701 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_110701_2ND(self):
        prompt = """
        "11.0701: Computer Science"
        """
        comments = None
        query = self.getCompletions('11.0701', major_rank=2)
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "11.0701",
                  "name": "11.0701 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_110701_2ND_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "11.0701",
                  "name": "11.0701 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_131202(self):
        prompt = """
        "13.1202: Elementary Education and Teaching"
        """
        comments = None
        query = self.getCompletions('13.1202')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1202",
                  "name": "13.1202 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_131202_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1202",
                  "name": "13.1202 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_131311(self):
        prompt = """
        "13.1311: Mathematics Teacher Education"
        """
        comments = None
        query = self.getCompletions('13.1311')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1311",
                  "name": "13.1311 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)


    def getCompletions_131311_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1311",
                  "name": "13.1311 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_131316(self):
        prompt = """
        "13.1316: Science Teacher Education/General Science Teacher Education"
        """
        comments = None
        query = self.getCompletions('13.1316')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1316",
                  "name": "13.1316 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)


    def getCompletions_131316_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1316",
                  "name": "13.1316 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_131317(self):
        prompt = """
        "13.1317: Social Science Teacher Education"
        """
        comments = None
        query = self.getCompletions('13.1317')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1317",
                  "name": "13.1317 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)


    def getCompletions_131317_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1317",
                  "name": "13.1317 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_131318(self):
        prompt = """
        "13.1317: Social Science Teacher Education"
        """
        comments = None
        query = self.getCompletions('13.1318')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1318",
                  "name": "13.1318 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)


    def getCompletions_131318_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1318",
                  "name": "13.1318 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_131322(self):
        prompt = """
        "13.1322: Biology Teacher Education"
        """
        comments = None
        query = self.getCompletions('13.1322')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1322",
                  "name": "13.1322 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_131322_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1322",
                  "name": "13.1322 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_131323(self):
        prompt = """
        "13.1323: Chemistry Teacher Education"
        """
        comments = None
        query = self.getCompletions('13.1323')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1323",
                  "name": "13.1323 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_131323_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1323",
                  "name": "13.1323 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_131328(self):
        prompt = """
        "13.1328: History Teacher Education"
        """
        comments = None
        query = self.getCompletions('13.1328')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1328",
                  "name": "13.1328 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)


    def getCompletions_131328_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1328",
                  "name": "13.1328 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_131330(self):
        prompt = """
        "13.1330: Spanish Language Teacher Education"
        """
        comments = None
        query = self.getCompletions('13.1330')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1330",
                  "name": "13.1330 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)


    def getCompletions_131330_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1330",
                  "name": "13.1330 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_131399(self):
        prompt = """
        "13.1399: Teacher Education and Professional Development, Specific Subject Areas, Other"
        """
        comments = None
        query = self.getCompletions('13.1399')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1399",
                  "name": "13.1399 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)


    def getCompletions_131399_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.1399",
                  "name": "13.1399 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_139999(self):
        prompt = """
        "13.9999: Education, Other"
        """
        comments = None
        query = self.getCompletions('13.9999')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.9999",
                  "name": "13.9999 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_139999_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "13.9999",
                  "name": "13.9999 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_140801(self):
        prompt = """
        "14.0801: Civil Engineering, General"
        """
        comments = None
        query = self.getCompletions('14.0801')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "14.0801",
                  "name": "14.0801 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)


    def getCompletions_140801_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "14.0801",
                  "name": "14.0801 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_141101(self):
        prompt = """
        "14.1101: Engineering Mechanics"
        """
        comments = None
        query = self.getCompletions('14.1101')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "14.1101",
                  "name": "14.1101 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_141101_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "14.1101",
                  "name": "14.1101 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_141301(self):
        prompt = """
        "14.1301: Engineering Science"
        """
        comments = None
        query = self.getCompletions('14.1301')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "14.1301",
                  "name": "14.1301 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)


    def getCompletions_141301_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "14.1301",
                  "name": "14.1301 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_141401(self):
        prompt = """
        "14.1401: Environmental/Environmental Health Engineering"
        """
        comments = None
        query = self.getCompletions('14.1401')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "14.1401",
                  "name": "14.1401 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_141401_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "14.1401",
                  "name": "14.1401 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_160905(self):
        prompt = """
        "16.0905: Spanish Language and Literature"
        """
        comments = None
        query = self.getCompletions('16.0905')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "16.0905",
                  "name": "16.0905 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_160905_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "16.0905",
                  "name": "16.0905 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_160905_2ND(self):
        prompt = """
        "16.0905: Spanish Language and Literature"
        """
        comments = None
        query = self.getCompletions('16.0905', major_rank=2)
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "16.0905",
                  "name": "16.0905 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)


    def getCompletions_160905_2ND_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "16.0905",
                  "name": "16.0905 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_161200(self):
        prompt = """
        "16.1200: Classics and Classical Languages, Literatures, and Linguistics, General"
        """
        comments = None
        query = self.getCompletions('16.1200')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "16.1200",
                  "name": "16.1200 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_161200_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "16.1200",
                  "name": "16.1200 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_230101(self):
        prompt = """
        "23.0101: English Language and Literature, General"
        """
        comments = None
        query = self.getCompletions('23.0101')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "23.0101",
                  "name": "23.0101 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_230101_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "23.0101",
                  "name": "23.0101 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_231301(self):
        prompt = """
        "23.1301: Writing, General"
        """
        comments = None
        query = self.getCompletions('23.1301')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "23.1301",
                  "name": "23.1301 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_231301_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "23.1301",
                  "name": "23.1301 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_231401(self):
        prompt = """
        "23.1401: General Literature"
        """
        comments = None
        query = self.getCompletions('23.1401')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "23.1401",
                  "name": "23.1401 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_231401_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "23.1401",
                  "name": "23.1401 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_260101(self):
        prompt = """
        "26.0101: Biology/Biological Sciences, General"
        """
        comments = None
        query = self.getCompletions('26.0101')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "26.0101",
                  "name": "26.0101 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_260101_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "26.0101",
                  "name": "26.0101 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_260101_2ND(self):
        prompt = """
        "26.0101: Biology/Biological Sciences, General"
        """
        comments = None
        query = self.getCompletions('26.0101', major_rank=2)
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "26.0101",
                  "name": "26.0101 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_260101_2ND_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "26.0101",
                  "name": "26.0101 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_260205(self):
        prompt = """
        "26.0205: Molecular Biochemistry"
        """
        comments = None
        query = self.getCompletions('26.0205')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "26.0205",
                  "name": "26.0205 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_260205_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "26.0205",
                  "name": "26.0205 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_270101(self):
        prompt = """
        "27.0101: Mathematics, General"
        """
        comments = None
        query = self.getCompletions('27.0101')
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [M] AS 'Male',
               [F] AS 'Female'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR GENDER IN ([M], [F])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
        ORDER BY N
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "27.0101",
                  "name": "27.0101 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_270101_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("None of the programs in this CIP code in this award level can be completed entirely via "
                    "distance education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "27.0101",
                  "name": "27.0101 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)










