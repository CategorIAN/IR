from Reports import Reports
import os
from IPEDS import IPEDS
import pandas as pd

class IPEDS_Fall (IPEDS):
    def __init__(self):
        super().__init__(folder='IPEDS_Fall', report="2025-09-17-IPEDS Fall Survey")
        self.gender_assignment = pd.read_csv(os.path.join(self.folder, 'Gender Assignment To Unknowns.csv'))
        self.gender_assignment_enrollment = pd.read_csv(os.path.join(self.folder, 'Gender Assignment To Unknowns '
                                                                                  '(12 Month Enrollment).csv'))
        self.status_str = ",\n".join([f"[{s}]" for s in ["First-time",
                                                       "Transfer-in",
                                                       "Continuing/Returning",
                                                       "Non-degree/non-certificate-seeking"]])
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

    def getCompletions(self, cip, major_rank = 1, level = 'UG'):
        query = f"""
                 SELECT IPEDS_RACE.THEIR_DESC AS RACE,
                 IPEDS_RACE.N,
                 STUDENT_ID             AS ID,
                 STUDENT_GENDER AS GENDER
        FROM ({self.ipeds_races()}) AS IPEDS_RACE
         LEFT JOIN (
                    SELECT STUDENT_ID,
                           COALESCE(STUDENT_GENDER, GENDER_ASSIGNMENT.GENDER) AS STUDENT_GENDER,
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
                    LEFT JOIN ({self.df_query(self.gender_assignment)}) AS GENDER_ASSIGNMENT ON STUDENT_ID = GENDER_ASSIGNMENT.ID
                    WHERE STP_CURRENT_STATUS = 'Graduated'
                    AND STP_END_DATE BETWEEN '2024-07-01' AND '2025-06-30'
                    AND ACPG_CIP = '{cip}'
                    AND STP_ACAD_LEVEL = '{level}'
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

    def getCompletions_131305(self):
        prompt = """
        "13.1305: English/Language Arts Teacher Education"
        """
        comments = None
        query = self.getCompletions('13.1305')
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
                  "page": "13.1305",
                  "name": "13.1305 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_131305_DE(self):
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
                  "page": "13.1305",
                  "name": "13.1305 (1st Major) (Distance Education)",
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

    def getCompletions_270301(self):
        prompt = """
        "27.0301: Applied Mathematics, General"
        """
        comments = None
        query = self.getCompletions('27.0301')
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
                  "page": "27.0301",
                  "name": "27.0301 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_270301_DE(self):
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
                  "page": "27.0301",
                  "name": "27.0301 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_279999(self):
        prompt = """
        "27.9999: Mathematics and Statistics, Other"
        """
        comments = None
        query = self.getCompletions('27.9999')
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
                  "page": "27.9999",
                  "name": "27.9999 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_279999_DE(self):
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
                  "page": "27.9999",
                  "name": "27.9999 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_309999(self):
        prompt = """
        "30.9999: Multi-/Interdisciplinary Studies, Other"
        """
        comments = None
        query = self.getCompletions('30.9999')
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
                  "page": "30.9999",
                  "name": "30.9999 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_309999_DE(self):
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
                  "page": "30.9999",
                  "name": "30.9999 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_310504(self):
        prompt = """
        "31.0504: Sport and Fitness Administration/Management"
        """
        comments = None
        query = self.getCompletions('31.0504')
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
                  "page": "31.0504",
                  "name": "31.0504 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_310504_DE(self):
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
                  "page": "31.0504",
                  "name": "31.0504 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_380101(self):
        prompt = """
        "38.0101: Philosophy"
        """
        comments = None
        query = self.getCompletions('38.0101')
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
                  "page": "38.0101",
                  "name": "38.0101 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_380101_DE(self):
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
                  "page": "38.0101",
                  "name": "38.0101 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_380101_2ND(self):
        prompt = """
        "38.0101: Philosophy"
        """
        comments = None
        query = self.getCompletions('38.0101', major_rank=2)
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
                  "page": "38.0101",
                  "name": "38.0101 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_380101_2ND_DE(self):
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
                  "page": "38.0101",
                  "name": "38.0101 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_380103(self):
        prompt = """
        "38.0103: Ethics"
        """
        comments = None
        query = self.getCompletions('38.0103')
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
                  "page": "38.0103",
                  "name": "38.0103 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_380103_DE(self):
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
                  "page": "38.0103",
                  "name": "38.0103 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_380203(self):
        prompt = """
        "38.0203: Christian Studies"
        """
        comments = None
        query = self.getCompletions('38.0203')
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
                  "page": "38.0203",
                  "name": "38.0203 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_380203_DE(self):
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
                  "page": "38.0203",
                  "name": "38.0203 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_380203_2ND(self):
        prompt = """
        "38.0203: Christian Studies"
        """
        comments = None
        query = self.getCompletions('38.0203', major_rank=2)
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
                  "page": "38.0203",
                  "name": "38.0203 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_380203_2ND_DE(self):
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
                  "page": "38.0203",
                  "name": "38.0203 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_390601(self):
        prompt = """
        "39.0601: Theology/Theological Studies"
        """
        comments = None
        query = self.getCompletions('39.0601')
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
                  "page": "39.0601",
                  "name": "39.0601 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_390601_DE(self):
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
                  "page": "39.0601",
                  "name": "39.0601 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_400501(self):
        prompt = """
        "40.0501: Chemistry, General"
        """
        comments = None
        query = self.getCompletions('40.0501')
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
                  "page": "40.0501",
                  "name": "40.0501 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_400501_DE(self):
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
                  "page": "40.0501",
                  "name": "40.0501 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_400801(self):
        prompt = """
        "40.0801: Physics, General"
        """
        comments = None
        query = self.getCompletions('40.0801')
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
                  "page": "40.0801",
                  "name": "40.0801 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_400801_DE(self):
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
                  "page": "40.0801",
                  "name": "40.0801 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_420101(self):
        prompt = """
        "42.0101: Psychology, General"
        """
        comments = None
        query = self.getCompletions('42.0101')
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
                  "page": "42.0101",
                  "name": "42.0101 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_420101_DE(self):
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
                  "page": "42.0101",
                  "name": "42.0101 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_420101_2ND(self):
        prompt = """
        "42.0101: Psychology, General"
        """
        comments = None
        query = self.getCompletions('42.0101', major_rank=2)
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
                  "page": "42.0101",
                  "name": "42.0101 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_420101_2ND_DE(self):
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
                  "page": "42.0101",
                  "name": "42.0101 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_440701(self):
        prompt = """
        "44.0701: Social Work"
        """
        comments = None
        query = self.getCompletions('44.0701', level='GR')
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
                  "page": "44.0701",
                  "name": "44.0701 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_440701_DE(self):
        prompt = """
        Is at least one program within this CIP code offered as a distance education program?
        """
        comments = ("All programs in this CIP code in this award level can be completed entirely via distance "
                    "education.")
        query = None

        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "Completions",
                  "section": "Completions by CIP",
                  "page": "44.0701",
                  "name": "44.0701 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_450901(self):
        prompt = """
        "45.0901: International Relations and Affairs"
        """
        comments = None
        query = self.getCompletions('45.0901')
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
                  "page": "45.0901",
                  "name": "45.0901 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_450901_DE(self):
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
                  "page": "45.0901",
                  "name": "45.0901 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_450901_2ND(self):
        prompt = """
        "45.0901: International Relations and Affairs"
        """
        comments = None
        query = self.getCompletions('45.0901', major_rank=2)
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
                  "page": "45.0901",
                  "name": "45.0901 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_450901_2ND_DE(self):
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
                  "page": "45.0901",
                  "name": "45.0901 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_451001(self):
        prompt = """
        "45.1001: Political Science and Government, General"
        """
        comments = None
        query = self.getCompletions('45.1001')
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
                  "page": "45.1001",
                  "name": "45.1001 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_451001_DE(self):
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
                  "page": "45.1001",
                  "name": "45.1001 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_451001_2ND(self):
        prompt = """
        "45.1001: Political Science and Government, General"
        """
        comments = None
        query = self.getCompletions('45.1001', major_rank=2)
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
                  "page": "45.1001",
                  "name": "45.1001 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_451001_2ND_DE(self):
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
                  "page": "45.1001",
                  "name": "45.1001 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_451101(self):
        prompt = """
        "45.1101: Sociology, General"
        """
        comments = None
        query = self.getCompletions('45.1101')
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
                  "page": "45.1101",
                  "name": "45.1101 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_451101_DE(self):
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
                  "page": "45.1101",
                  "name": "45.1101 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_451101_2ND(self):
        prompt = """
        "45.1101: Sociology, General"
        """
        comments = None
        query = self.getCompletions('45.1101', major_rank=2)
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
                  "page": "45.1101",
                  "name": "45.1101 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_451101_2ND_DE(self):
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
                  "page": "45.1101",
                  "name": "45.1101 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_500101(self):
        prompt = """
        "50.0101: Visual and Performing Arts, General"
        """
        comments = None
        query = self.getCompletions('50.0101')
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
                  "page": "50.0101",
                  "name": "50.0101 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_500101_DE(self):
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
                  "page": "50.0101",
                  "name": "50.0101 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_500101_2ND(self):
        prompt = """
        "50.0101: Visual and Performing Arts, General"
        """
        comments = None
        query = self.getCompletions('50.0101', major_rank=2)
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
                  "page": "50.0101",
                  "name": "50.0101 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_500101_2ND_DE(self):
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
                  "page": "50.0101",
                  "name": "50.0101 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_510000(self):
        prompt = """
        "51.0000: Health Services/Allied Health/Health Sciences, General"
        """
        comments = None
        query = self.getCompletions('51.0000')
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
                  "page": "51.0000",
                  "name": "51.0000 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_510000_DE(self):
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
                  "page": "51.0000",
                  "name": "51.0000 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_510000_2ND(self):
        prompt = """
        "51.0000: Health Services/Allied Health/Health Sciences, General"
        """
        comments = None
        query = self.getCompletions('51.0000', major_rank = 2)
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
                  "page": "51.0000",
                  "name": "51.0000 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_510000_2ND_DE(self):
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
                  "page": "51.0000",
                  "name": "51.0000 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_511504(self):
        prompt = """
        "51.1504: Community Health Services/Liaison/Counseling"
        """
        comments = None
        query = self.getCompletions('51.1504')
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
                  "page": "51.1504",
                  "name": "51.1504 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_511504_DE(self):
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
                  "page": "51.1504",
                  "name": "51.1504 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_512207(self):
        prompt = """
        "51.2207: Public Health Education and Promotion"
        """
        comments = None
        query = self.getCompletions('51.2207')
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
                  "page": "51.2207",
                  "name": "51.2207 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_512207_DE(self):
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
                  "page": "51.2207",
                  "name": "51.2207 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_512207_2ND(self):
        prompt = """
        "51.2207: Public Health Education and Promotion"
        """
        comments = None
        query = self.getCompletions('51.2207', major_rank = 2)
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
                  "page": "51.2207",
                  "name": "51.2207 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_512207_2ND_DE(self):
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
                  "page": "51.2207",
                  "name": "51.2207 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_512313(self):
        prompt = """
        "51.2313: Animal-Assisted Therapy"
        """
        comments = None
        query = self.getCompletions('51.2313')
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
                  "page": "51.2313",
                  "name": "51.2313 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_512313_DE(self):
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
                  "page": "51.2313",
                  "name": "51.2313 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_512313_2ND(self):
        prompt = """
        "51.2313: Animal-Assisted Therapy"
        """
        comments = None
        query = self.getCompletions('51.2313', major_rank=2)
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
                  "page": "51.2313",
                  "name": "51.2313 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_512313_2ND_DE(self):
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
                  "page": "51.2313",
                  "name": "51.2313 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_513801(self):
        prompt = """
        "51.3801: Registered Nursing/Registered Nurse"
        """
        comments = None
        query = self.getCompletions('51.3801')
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
                  "page": "51.3801",
                  "name": "51.3801 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_513801_DE(self):
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
                  "page": "51.3801",
                  "name": "51.3801 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_520201(self):
        prompt = """
        "52.0201: Business Administration and Management, General"
        """
        comments = None
        query = self.getCompletions('52.0201')
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
                  "page": "52.0201",
                  "name": "52.0201 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_520201_DE(self):
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
                  "page": "52.0201",
                  "name": "52.0201 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_520201_2ND(self):
        prompt = """
        "52.0201: Business Administration and Management, General"
        """
        comments = None
        query = self.getCompletions('52.0201', major_rank = 2)
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
                  "page": "52.0201",
                  "name": "52.0201 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_520201_2ND_DE(self):
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
                  "page": "52.0201",
                  "name": "52.0201 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_520301(self):
        prompt = """
        "52.0301: Accounting"
        """
        comments = None
        query = self.getCompletions('52.0301')
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
                  "page": "52.0301",
                  "name": "52.0301 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_520301_DE(self):
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
                  "page": "52.0301",
                  "name": "52.0301 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_520301_2ND(self):
        prompt = """
        "52.0301: Accounting"
        """
        comments = None
        query = self.getCompletions('52.0301', major_rank=2)
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
                  "page": "52.0301",
                  "name": "52.0301 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_520301_2ND_DE(self):
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
                  "page": "52.0301",
                  "name": "52.0301 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_520301_GR(self):
        prompt = """
        "52.0301: Accounting"
        """
        comments = None
        query = self.getCompletions('52.0301', level='GR')
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
                  "page": "52.0301",
                  "name": "52.0301 (Graduate) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_520301_GR_DE(self):
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
                  "page": "52.0301",
                  "name": "52.0301 (Graduate) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_520801(self):
        prompt = """
        "52.0801: Finance, General"
        """
        comments = None
        query = self.getCompletions('52.0801')
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
                  "page": "52.0801",
                  "name": "52.0801 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_520801_DE(self):
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
                  "page": "52.0801",
                  "name": "52.0801 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)


    def getCompletions_520804(self):
        prompt = """
        "52.0804: Financial Planning and Services"
        """
        comments = None
        query = self.getCompletions('52.0804')
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
                  "page": "52.0804",
                  "name": "52.0804 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_520804_DE(self):
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
                  "page": "52.0804",
                  "name": "52.0804 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_540101(self):
        prompt = """
        "54.0101: History, General"
        """
        comments = None
        query = self.getCompletions('54.0101')
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
                  "page": "54.0101",
                  "name": "54.0101 (1st Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_540101_DE(self):
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
                  "page": "54.0101",
                  "name": "54.0101 (1st Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompletions_540101_2ND(self):
        prompt = """
        "54.0101: History, General"
        """
        comments = None
        query = self.getCompletions('54.0101', major_rank = 2)
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
                  "page": "54.0101",
                  "name": "54.0101 (2nd Major) (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletions_540101_2ND_DE(self):
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
                  "page": "54.0101",
                  "name": "54.0101 (2nd Major) (Distance Education)",
                  "func_dict": None,
                  }
        self.save(**params)

    def getCompleters_All(self):
        prompt = """    
        All Completers
        Institutions must report the following information. (Some data will be pre-populated from the completions by CIP
         code data.)
        Number of students by sex and race and ethnicity earning an award between July 1, 2024 and June 30, 2025. Count 
        each student only once, regardless of how many awards he/she earned. The intent of this screen is to collect an 
        unduplicated count of total numbers of completers.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        """
        comments = None
        query = f"""
                 SELECT DISTINCT IPEDS_RACE.THEIR_DESC AS RACE,
                 IPEDS_RACE.N,
                 STUDENT_ID             AS ID,
                 STUDENT_GENDER AS GENDER
        FROM ({self.ipeds_races()}) AS IPEDS_RACE
         LEFT JOIN (
                    SELECT STUDENT_ID,
                           COALESCE(STUDENT_GENDER, GENDER_ASSIGNMENT.GENDER) AS STUDENT_GENDER,
                           IPEDS_RACE_ETHNIC_DESC
                    FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                    LEFT JOIN ACAD_PROGRAMS AS AP
                    ON SAPV.STP_ACADEMIC_PROGRAM = AP.ACAD_PROGRAMS_ID
                    LEFT JOIN ({self.df_query(self.gender_assignment)}) AS GENDER_ASSIGNMENT ON STUDENT_ID = GENDER_ASSIGNMENT.ID
                    WHERE STP_CURRENT_STATUS = 'Graduated'
                    AND STP_END_DATE BETWEEN '2024-07-01' AND '2025-06-30'
                    ) AS STUDENT_PROGRAMS
            ON IPEDS_RACE.OUR_DESC = STUDENT_PROGRAMS.IPEDS_RACE_ETHNIC_DESC
        """
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
                  "section": "All Completers",
                  "page": "All Completers",
                  "name": "All Completers (Data)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompleters_SexUnknown(self):
        prompt = """    
        Sex Unknown
        The purpose of this supplemental section is to determine whether institutions are able to report the number of 
        students for whom sex is unknown. Note that these students must still be allocated into the 'Male' and 'Female'
         categories in all other sections of the survey component.
        """
        comments = None
        query = f"""
                    SELECT DISTINCT STUDENT_ID AS ID,
                           STUDENT_GENDER,
                           IPEDS_RACE_ETHNIC_DESC,
                           STP_PROGRAM_TITLE,
                           ACPG_CIP,
                           STP_ACAD_LEVEL
                    FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                    LEFT JOIN ACAD_PROGRAMS AS AP
                    ON SAPV.STP_ACADEMIC_PROGRAM = AP.ACAD_PROGRAMS_ID
                    WHERE STP_CURRENT_STATUS = 'Graduated'
                    AND STP_END_DATE BETWEEN '2024-07-01' AND '2025-06-30'
                    AND STUDENT_GENDER IS NULL
        """
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT [UG] AS [Undergraduate Students],
                [GR] AS [Graduate Students]
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR STP_ACAD_LEVEL IN ([UG], [GR])) AS X
        --(End 2)-------------------------------------------------------------------------------------------------------
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
                  "section": "All Completers",
                  "page": "All Completers",
                  "name": "All Completers (Sex Unknown)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompletersSimple(self, level = 'UG'):
        query = f"""
                 SELECT IPEDS_RACE.THEIR_DESC AS RACE,
                 IPEDS_RACE.N,
                 STUDENT_ID             AS ID,
                 STUDENT_GENDER AS GENDER
        FROM ({self.ipeds_races()}) AS IPEDS_RACE
         LEFT JOIN (
                    SELECT DISTINCT STUDENT_ID,
                           COALESCE(STUDENT_GENDER, GENDER_ASSIGNMENT.GENDER) AS STUDENT_GENDER,
                           IPEDS_RACE_ETHNIC_DESC
                    FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                    LEFT JOIN ACAD_PROGRAMS AS AP
                    ON SAPV.STP_ACADEMIC_PROGRAM = AP.ACAD_PROGRAMS_ID
                    LEFT JOIN ({self.df_query(self.gender_assignment)}) AS GENDER_ASSIGNMENT ON STUDENT_ID = GENDER_ASSIGNMENT.ID
                    WHERE STP_CURRENT_STATUS = 'Graduated'
                    AND STP_END_DATE BETWEEN '2024-07-01' AND '2025-06-30'
                    AND STP_ACAD_LEVEL = '{level}'
                    ) AS STUDENT_PROGRAMS
            ON IPEDS_RACE.OUR_DESC = STUDENT_PROGRAMS.IPEDS_RACE_ETHNIC_DESC
        """
        return query


    def getCompleters_UG_BySex(self):
        prompt = """    
        Completers by Level
        Bachelor's degree
        Number of students by sex, by race and ethnicity, and by age earning this award between July 1, 2024 and 
        June 30, 2025. Each student should be counted once per award level. For example, if a student earned a master's 
        degree and a doctor's degree, he/she should be counted once in master's and once in doctor's. A student earning
         two master's degrees should be counted only once.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        """
        comments = None
        query = self.getCompletersSimple('UG')
        agg = lambda query: f"""
        SELECT GENDER AS [By Sex],
        COUNT(ID) AS [Number of Students]
        FROM ({query}) AS X
        WHERE ID IS NOT NULL
        GROUP BY GENDER
        ORDER BY GENDER
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
                  "section": "Completers by Level",
                  "page": "Bachelor's Degree",
                  "name": "By Sex",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompleters_UG_ByRace(self):
        prompt = """    
        Completers by Level
        Bachelor's degree
        Number of students by sex, by race and ethnicity, and by age earning this award between July 1, 2024 and 
        June 30, 2025. Each student should be counted once per award level. For example, if a student earned a master's 
        degree and a doctor's degree, he/she should be counted once in master's and once in doctor's. A student earning
         two master's degrees should be counted only once.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        """
        comments = None
        query = self.getCompletersSimple('UG')
        agg = lambda query: f"""
        SELECT RACE AS [By Race/Ethnicity],
        COUNT(ID) AS [Number of Students]
        FROM ({query}) AS X
        GROUP BY RACE, N
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
                  "section": "Completers by Level",
                  "page": "Bachelor's Degree",
                  "name": "By Race-Ethnicity",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompleters_UG_ByAge(self):
        prompt = """    
        Completers by Level
        Bachelor's degree
        Number of students by sex, by race and ethnicity, and by age earning this award between July 1, 2024 and 
        June 30, 2025. Each student should be counted once per award level. For example, if a student earned a master's 
        degree and a doctor's degree, he/she should be counted once in master's and once in doctor's. A student earning
         two master's degrees should be counted only once.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        """
        comments = None
        query = f"""
        SELECT X.*,
                AGE_CATEGORY_ORDER.N AS AGE_CATEGORY_ORDER
        FROM (
        SELECT X.*,
                CASE WHEN AGE < 18 THEN 'Under 18'
                WHEN AGE BETWEEN 18 AND 24 THEN '18-24'
                WHEN AGE BETWEEN 25 AND 39 THEN '25-39'
                WHEN AGE >= 40 THEN '40 and Above'
                ELSE 'Age Unknown'
                END AS AGE_CATEGORY
        FROM (
        SELECT X.*,
                DATEDIFF(DAY, P.BIRTH_DATE, '2024-07-01') / 365.25 AS AGE
        FROM ({self.getCompletersSimple('UG')}) AS X
        JOIN PERSON P ON X.ID = P.ID
        ) AS X
        ) AS X 
        JOIN (VALUES 
                ('Under 18', 1),
                ('18-24', 2),
                ('25-39', 3),
                ('40 and Above', 4),
                ('Age Unknown', 5)
                ) AS AGE_CATEGORY_ORDER(CAT, N) ON X.AGE_CATEGORY = AGE_CATEGORY_ORDER.CAT
        """
        agg = lambda query: f"""
        SELECT AGE_CATEGORY AS [By Age],
        COUNT(ID) AS [Number of Students]
        FROM ({query}) AS X
        GROUP BY AGE_CATEGORY, AGE_CATEGORY_ORDER
        ORDER BY AGE_CATEGORY_ORDER
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
                  "section": "Completers by Level",
                  "page": "Bachelor's Degree",
                  "name": "By Age",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompleters_GR_BySex(self):
        prompt = """    
        Completers by Level
        Bachelor's degree
        Number of students by sex, by race and ethnicity, and by age earning this award between July 1, 2024 and 
        June 30, 2025. Each student should be counted once per award level. For example, if a student earned a master's 
        degree and a doctor's degree, he/she should be counted once in master's and once in doctor's. A student earning
         two master's degrees should be counted only once.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        """
        comments = None
        query = self.getCompletersSimple('GR')
        agg = lambda query: f"""
        SELECT GENDER AS [By Sex],
        COUNT(ID) AS [Number of Students]
        FROM ({query}) AS X
        WHERE ID IS NOT NULL
        GROUP BY GENDER
        ORDER BY GENDER
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
                  "section": "Completers by Level",
                  "page": "Master's Degree",
                  "name": "By Sex",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompleters_GR_ByRace(self):
        prompt = """    
        Completers by Level
        Bachelor's degree
        Number of students by sex, by race and ethnicity, and by age earning this award between July 1, 2024 and 
        June 30, 2025. Each student should be counted once per award level. For example, if a student earned a master's 
        degree and a doctor's degree, he/she should be counted once in master's and once in doctor's. A student earning
         two master's degrees should be counted only once.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        """
        comments = None
        query = self.getCompletersSimple('GR')
        agg = lambda query: f"""
        SELECT RACE AS [By Race/Ethnicity],
        COUNT(ID) AS [Number of Students]
        FROM ({query}) AS X
        GROUP BY RACE, N
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
                  "section": "Completers by Level",
                  "page": "Master's Degree",
                  "name": "By Race-Ethnicity",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCompleters_GR_ByAge(self):
        prompt = """    
        Completers by Level
        Bachelor's degree
        Number of students by sex, by race and ethnicity, and by age earning this award between July 1, 2024 and 
        June 30, 2025. Each student should be counted once per award level. For example, if a student earned a master's 
        degree and a doctor's degree, he/she should be counted once in master's and once in doctor's. A student earning
         two master's degrees should be counted only once.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        """
        comments = None
        query = f"""
        SELECT X.*,
                AGE_CATEGORY_ORDER.N AS AGE_CATEGORY_ORDER
        FROM (
        SELECT X.*,
                CASE WHEN AGE < 18 THEN 'Under 18'
                WHEN AGE BETWEEN 18 AND 24 THEN '18-24'
                WHEN AGE BETWEEN 25 AND 39 THEN '25-39'
                WHEN AGE >= 40 THEN '40 and Above'
                ELSE 'Age Unknown'
                END AS AGE_CATEGORY
        FROM (
        SELECT X.*,
                DATEDIFF(DAY, P.BIRTH_DATE, '2024-07-01') / 365.25 AS AGE
        FROM ({self.getCompletersSimple('GR')}) AS X
        JOIN PERSON P ON X.ID = P.ID
        ) AS X
        ) AS X 
        JOIN (VALUES 
                ('Under 18', 1),
                ('18-24', 2),
                ('25-39', 3),
                ('40 and Above', 4),
                ('Age Unknown', 5)
                ) AS AGE_CATEGORY_ORDER(CAT, N) ON X.AGE_CATEGORY = AGE_CATEGORY_ORDER.CAT
        """
        agg = lambda query: f"""
        SELECT AGE_CATEGORY AS [By Age],
        COUNT(ID) AS [Number of Students]
        FROM ({query}) AS X
        GROUP BY AGE_CATEGORY, AGE_CATEGORY_ORDER
        ORDER BY AGE_CATEGORY_ORDER
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
                  "section": "Completers by Level",
                  "page": "Master's Degree",
                  "name": "By Age",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

#=====================================12-Month Enrollment Screening Questions===========================================
    def get12MonthEnrollmentScreeningQuestions_1(self):
        prompt = """
        1. Which instructional activity units will you use to report undergraduate instructional activity?
        Undergraduate instructional activity data in Part B may be reported in units of clock hours or credit hours.
        Please note that any graduate level instructional activity must be reported in credit hours. 
        (4-year institutions only)
        """
        comments = """
        Credit hours
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "12-month Enrollment",
                  "section": "Screening Questions",
                  "page": "Screening Questions",
                  "name": "1. Instructional Activity Units",
                  "func_dict": None,
                  }
        self.save(**params)

    def get12MonthEnrollmentScreeningQuestions_2(self):
        prompt = """
        2. Did your institution enroll high school students in college courses for credit during the 12-month Enrollment
         (E12) reporting period of July 1, 2024 - June 30, 2025?
        If you answer Yes to this question, you will be able to report the unduplicated count of high school students 
        enrolled in college courses for credit on Part C of the 12-month Enrollment (E12) survey component.
        """
        comments = """
        Yes, within a dual enrollment program.
        """
        query = None
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "12-month Enrollment",
                  "section": "Screening Questions",
                  "page": "Screening Questions",
                  "name": "2. High School Student College Credits",
                  "func_dict": None,
                  }
        self.save(**params)

    def enrolledStudents(self, level = None, load = None, gender = None, start = '2024-07-01'):
        query = f"""
        SELECT ID,
                LEVEL,
                LOAD,
                GENDER
        FROM (
        SELECT DISTINCT STC_PERSON_ID     AS ID,
                  STC_ACAD_LEVEL          AS LEVEL,
                  STTR_STUDENT_LOAD       AS LOAD,
                  COALESCE(PERSON.GENDER, ASSIGNED_GENDER.GENDER) AS GENDER,
                  ROW_NUMBER() OVER (PARTITION BY STC_PERSON_ID ORDER BY TERM_START_DATE) AS LL_RANK
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        LEFT JOIN STUDENT_TERMS_VIEW STV ON STC.STC_PERSON_ID = STV.STTR_STUDENT AND STC.STC_TERM = STV.STTR_TERM
        LEFT JOIN TERMS ON STC.STC_TERM = TERMS_ID
        LEFT JOIN PERSON ON STC_PERSON_ID = PERSON.ID
        LEFT JOIN ({self.df_query(self.gender_assignment_enrollment)}) AS ASSIGNED_GENDER ON STC_PERSON_ID = ASSIGNED_GENDER.ID
        WHERE STATUS.STC_STATUS IN ('N', 'A')
        AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
        AND TERM_START_DATE < '2025-07-01'
        AND TERM_END_DATE >= '{start}'
        AND STC.STC_CRED > 0
        ) AS X
        WHERE LL_RANK = 1
        AND {f"LEVEL = '{level}'" if level is not None else "LEVEL = LEVEL"}
        AND {"LOAD IN ('F', 'O')" if load == "FT" else "LOAD NOT IN ('F', 'O')" if load == "PT" else "LOAD = LOAD"}
        AND {f"GENDER = '{gender}'" if gender is not None else "GENDER = GENDER"}
        """
        return query

    def dist_status(self, start = '2024-07-01'):
        query = f"""
        SELECT ID,
                CASE WHEN ALL_DISTANCE_COURSES = 1 THEN 'Enrolled Exclusively in DE'
                WHEN EXIST_DISTANCE_COURSE = 1 THEN 'Enrolled in At Least One DE But Not All'
                ELSE 'Not Enrolled in Any DE' END AS STATUS
        FROM (
        SELECT ID,
               MAX(DISTANCE) AS EXIST_DISTANCE_COURSE,
               MIN(DISTANCE) AS ALL_DISTANCE_COURSES
        FROM (
        SELECT DISTINCT STC_PERSON_ID     AS ID,
               CASE WHEN CSM_INSTR_METHOD IN ('REMOT', 'CYBER', 'HYBRD') THEN 1 ELSE 0 END AS DISTANCE
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        LEFT JOIN TERMS ON STC.STC_TERM = TERMS_ID
        LEFT JOIN Z01_RHC_CLASS_SCHEDULE AS SCH ON SEC.SCS_COURSE_SECTION = SCH.COURSE_SECTIONS_ID
        WHERE STATUS.STC_STATUS IN ('N', 'A')
        AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
        AND (
              TERMS_ID LIKE '%FA'
              OR TERMS_ID LIKE '%SP'
              OR TERMS_ID LIKE '%SU'
          )
        AND TERM_START_DATE < DATEADD(YEAR, 1, '{start}')
        AND TERM_END_DATE >= '{start}'
        AND STC.STC_CRED > 0
        ) AS X
        GROUP BY ID
        ) AS X
        """
        return query

    def appl_status(self, start = '2024-07-01'):
        query = f"""
        SELECT ID,
               CASE WHEN TERM_END_DATE < '{start}' THEN 'Continuing/Returning'
               WHEN APPL_ADMIT_STATUS IN ('TR', 'PB') THEN 'Transfer-in'
               WHEN APPL_ADMIT_STATUS = 'FY' OR APPL_ADMIT_STATUS IS NULL THEN 'First-time'
               END AS STATUS
        FROM (
        SELECT APPL_APPLICANT AS ID,
                APPL_ADMIT_STATUS,
                TERM_END_DATE,
               ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS APPL_RANK
        FROM APPLICATIONS
        JOIN TERMS ON APPL_START_TERM = TERMS_ID
        WHERE APPL_DATE IS NOT NULL
        ) AS X
        WHERE APPL_RANK = 1
        """
        return query

    def deg_status(self, start ='2024-07-01'):
        query = f"""
        SELECT ID,
                CASE WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students' 
                THEN 'Degree-Seeking' ELSE 'Non-Degree-Seeking' END AS STATUS
        FROM (
        SELECT STUDENT_ID AS ID,
                STP_PROGRAM_TITLE,
                ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY
                CASE WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students' THEN 0 ELSE 1 END) AS PROGRAM_RANK
        FROM STUDENT_ACAD_PROGRAMS_VIEW
        WHERE STP_START_DATE < DATEADD(YEAR, 1, '{start}')
        AND COALESCE(STP_END_DATE, '{start}') >= '{start}'
        ) AS X
        WHERE PROGRAM_RANK = 1
        """
        return query

    def race_status(self):
        query = f"""
        SELECT ID,
                IPEDS_RACE_ETHNIC_DESC AS RACE
        FROM Z01_ALL_RACE_ETHNIC_W_FLAGS
        """
        return query

    def stu_type(self, start = '2024-07-01'):
        query = f"""
        SELECT  ID,
                TYPE
        FROM (
        SELECT STUDENTS_ID AS ID,
                STU_TYPES AS TYPE,
                ROW_NUMBER() OVER (PARTITION BY STUDENTS_ID ORDER BY STU_TYPE_DATES DESC) AS TYPE_RANK
        FROM STU_TYPE_INFO
        WHERE STU_TYPE_DATES < DATEADD(YEAR, 1, '{start}')
        ) AS X
        WHERE TYPE_RANK = 1
        """
        return query


    def getCount_FT_UG_Men(self):
        prompt = """
        12-month Unduplicated Count by Race/Ethnicity and Sex - Full-time Undergraduate Students
        July 1, 2024 – June 30, 2025
        Reporting Reminders:
        The 12-month unduplicated count must be equal or greater than the corresponding prior year fall enrollment.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        Even though Teacher Preparation certificate programs may require a bachelor's degree for admission, they are 
        considered subbaccalaureate undergraduate programs, and students in these programs are undergraduate students.
        """
        comments = None
        query = f"""
        SELECT IPEDS_RACE.THEIR_DESC AS RACE,
        IPEDS_RACE.N,
        TARGET_STUDENTS.ID,
        TARGET_STUDENTS.STATUS
        FROM ({self.ipeds_races()}) AS IPEDS_RACE
        LEFT JOIN (
        SELECT STUDENTS.ID,
        RACE,
        CASE WHEN STU_PROGRAM.STATUS = 'Non-Degree-Seeking' THEN 'Non-degree/non-certificate-seeking'
        ELSE STU_APPL.STATUS END AS STATUS
        FROM (
        {self.enrolledStudents(level = "UG", load = "FT", gender = "M")}
        ) AS STUDENTS
        JOIN (
        {self.race_status()}
        ) AS STU_RACE ON STUDENTS.ID = STU_RACE.ID
        JOIN (
        {self.appl_status()}
        ) AS STU_APPL ON STUDENTS.ID = STU_APPL.ID
        JOIN (
        {self.deg_status()}
        ) AS STU_PROGRAM ON STUDENTS.ID = STU_PROGRAM.ID
        ) AS TARGET_STUDENTS ON IPEDS_RACE.OUR_DESC = TARGET_STUDENTS.RACE
        """

        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               {self.status_str}
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR STATUS IN ({self.status_str})) AS X
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
                  "survey": "12-month Enrollment",
                  "section": "Unduplicated Count",
                  "page": "Full-time UG Students",
                  "name": "Full-time UG Students (Men)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCount_FT_UG_Women(self):
        prompt = """
        12-month Unduplicated Count by Race/Ethnicity and Sex - Full-time Undergraduate Students
        July 1, 2024 – June 30, 2025
        Reporting Reminders:
        The 12-month unduplicated count must be equal or greater than the corresponding prior year fall enrollment.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        Even though Teacher Preparation certificate programs may require a bachelor's degree for admission, they are 
        considered subbaccalaureate undergraduate programs, and students in these programs are undergraduate students.
        """
        comments = None
        query = f"""
        SELECT IPEDS_RACE.THEIR_DESC AS RACE,
        IPEDS_RACE.N,
        TARGET_STUDENTS.ID,
        TARGET_STUDENTS.STATUS
        FROM ({self.ipeds_races()}) AS IPEDS_RACE
        LEFT JOIN (
        SELECT STUDENTS.ID,
        RACE,
        CASE WHEN STU_PROGRAM.STATUS = 'Non-Degree-Seeking' THEN 'Non-degree/non-certificate-seeking'
        ELSE STU_APPL.STATUS END AS STATUS
        FROM (
        {self.enrolledStudents(level = "UG", load = "FT", gender = "F")}
        ) AS STUDENTS
        JOIN (
        {self.race_status()}
        ) AS STU_RACE ON STUDENTS.ID = STU_RACE.ID
        JOIN (
        {self.appl_status()}
        ) AS STU_APPL ON STUDENTS.ID = STU_APPL.ID
        JOIN (
        {self.deg_status()}
        ) AS STU_PROGRAM ON STUDENTS.ID = STU_PROGRAM.ID
        ) AS TARGET_STUDENTS ON IPEDS_RACE.OUR_DESC = TARGET_STUDENTS.RACE
        """
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               {self.status_str}
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR STATUS IN ({self.status_str})) AS X
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
                  "survey": "12-month Enrollment",
                  "section": "Unduplicated Count",
                  "page": "Full-time UG Students",
                  "name": "Full-time UG Students (Women)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCount_PT_UG_Men(self):
        prompt = """
        12-month Unduplicated Count by Race/Ethnicity and Sex - Part-time Undergraduate Students
        July 1, 2024 – June 30, 2025
        Reporting Reminders:
        The 12-month unduplicated count must be equal or greater than the corresponding prior year fall enrollment.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        Even though Teacher Preparation certificate programs may require a bachelor's degree for admission, they are 
        considered subbaccalaureate undergraduate programs, and students in these programs are undergraduate students.
        """
        comments = None
        query = f"""
        SELECT IPEDS_RACE.THEIR_DESC AS RACE,
        IPEDS_RACE.N,
        TARGET_STUDENTS.ID,
        TARGET_STUDENTS.STATUS
        FROM ({self.ipeds_races()}) AS IPEDS_RACE
        LEFT JOIN (
        SELECT STUDENTS.ID,
        RACE,
        CASE WHEN STU_PROGRAM.STATUS = 'Non-Degree-Seeking' THEN 'Non-degree/non-certificate-seeking'
        ELSE STU_APPL.STATUS END AS STATUS
        FROM (
        {self.enrolledStudents(level = "UG", load = "PT", gender = "M")}
        ) AS STUDENTS
        JOIN (
        {self.race_status()}
        ) AS STU_RACE ON STUDENTS.ID = STU_RACE.ID
        JOIN (
        {self.appl_status()}
        ) AS STU_APPL ON STUDENTS.ID = STU_APPL.ID
        JOIN (
        {self.deg_status()}
        ) AS STU_PROGRAM ON STUDENTS.ID = STU_PROGRAM.ID
        ) AS TARGET_STUDENTS ON IPEDS_RACE.OUR_DESC = TARGET_STUDENTS.RACE
        """
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               {self.status_str}
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR STATUS IN ({self.status_str})) AS X
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
                  "survey": "12-month Enrollment",
                  "section": "Unduplicated Count",
                  "page": "Part-time UG Students",
                  "name": "Part-time UG Students (Men)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCount_PT_UG_Women(self):
        prompt = """
        12-month Unduplicated Count by Race/Ethnicity and Sex - Part-time Undergraduate Students
        July 1, 2024 – June 30, 2025
        Reporting Reminders:
        The 12-month unduplicated count must be equal or greater than the corresponding prior year fall enrollment.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        Even though Teacher Preparation certificate programs may require a bachelor's degree for admission, they are 
        considered subbaccalaureate undergraduate programs, and students in these programs are undergraduate students.
        """
        comments = None
        query = f"""
        SELECT IPEDS_RACE.THEIR_DESC AS RACE,
        IPEDS_RACE.N,
        TARGET_STUDENTS.ID,
        TARGET_STUDENTS.STATUS
        FROM ({self.ipeds_races()}) AS IPEDS_RACE
        LEFT JOIN (
        SELECT STUDENTS.ID,
        RACE,
        CASE WHEN STU_PROGRAM.STATUS = 'Non-Degree-Seeking' THEN 'Non-degree/non-certificate-seeking'
        ELSE STU_APPL.STATUS END AS STATUS
        FROM (
        {self.enrolledStudents(level = "UG", load = "PT", gender = "F")}
        ) AS STUDENTS
        JOIN (
        {self.race_status()}
        ) AS STU_RACE ON STUDENTS.ID = STU_RACE.ID
        JOIN (
        {self.appl_status()}
        ) AS STU_APPL ON STUDENTS.ID = STU_APPL.ID
        JOIN (
        {self.deg_status()}
        ) AS STU_PROGRAM ON STUDENTS.ID = STU_PROGRAM.ID
        ) AS TARGET_STUDENTS ON IPEDS_RACE.OUR_DESC = TARGET_STUDENTS.RACE
        """
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               {self.status_str}
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR STATUS IN ({self.status_str})) AS X
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
                  "survey": "12-month Enrollment",
                  "section": "Unduplicated Count",
                  "page": "Part-time UG Students",
                  "name": "Part-time UG Students (Women)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCount_GR_Men(self):
        prompt = """
        12-month Unduplicated Count by Race/Ethnicity and Sex - Full-time and Part-time Graduate Students
        July 1, 2024 – June 30, 2025
        Reporting Reminders:
        The 12-month unduplicated count must be equal or greater than the corresponding prior year fall enrollment.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        Report all postbaccalaureate degree and certificate students as graduate students, including any doctor's - 
        professional practice students (formerly first-professional)
        """
        comments = None
        query = f"""
        SELECT IPEDS_RACE.THEIR_DESC AS RACE,
        IPEDS_RACE.N,
        TARGET_STUDENTS.ID,
        CASE WHEN TARGET_STUDENTS.LOAD IN ('F', 'O') THEN 'FT' ELSE 'PT' END AS LOAD
        FROM ({self.ipeds_races()}) AS IPEDS_RACE
        LEFT JOIN (
        SELECT STUDENTS.ID,
        RACE,
        LOAD
        FROM (
        {self.enrolledStudents(level = "GR", load = None, gender = "M")}
        ) AS STUDENTS
        JOIN (
        {self.race_status()}
        ) AS STU_RACE ON STUDENTS.ID = STU_RACE.ID
        ) AS TARGET_STUDENTS ON IPEDS_RACE.OUR_DESC = TARGET_STUDENTS.RACE
        """
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [FT] AS 'Total full-time',
               [PT] AS 'Total part-time'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR LOAD IN ([FT], [PT])) AS X
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
                  "survey": "12-month Enrollment",
                  "section": "Unduplicated Count",
                  "page": "Graduate Students",
                  "name": "Graduate (Men)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCount_GR_Women(self):
        prompt = """
        12-month Unduplicated Count by Race/Ethnicity and Sex - Full-time and Part-time Graduate Students
        July 1, 2024 – June 30, 2025
        Reporting Reminders:
        The 12-month unduplicated count must be equal or greater than the corresponding prior year fall enrollment.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        Report all postbaccalaureate degree and certificate students as graduate students, including any doctor's - 
        professional practice students (formerly first-professional)
        """
        comments = None
        query = f"""
        SELECT IPEDS_RACE.THEIR_DESC AS RACE,
        IPEDS_RACE.N,
        TARGET_STUDENTS.ID,
        CASE WHEN TARGET_STUDENTS.LOAD IN ('F', 'O') THEN 'FT' ELSE 'PT' END AS LOAD
        FROM ({self.ipeds_races()}) AS IPEDS_RACE
        LEFT JOIN (
        SELECT STUDENTS.ID,
        RACE,
        LOAD
        FROM (
        {self.enrolledStudents(level = "GR", load = None, gender = "F")}
        ) AS STUDENTS
        JOIN (
        {self.race_status()}
        ) AS STU_RACE ON STUDENTS.ID = STU_RACE.ID
        ) AS TARGET_STUDENTS ON IPEDS_RACE.OUR_DESC = TARGET_STUDENTS.RACE
        """
        agg = lambda query: f"""
        --(Begin 2)-----------------------------------------------------------------------------------------------------
        SELECT RACE,
               [FT] AS 'Total full-time',
               [PT] AS 'Total part-time'
        FROM (
        --(Begin 1)-----------------------------------------------------------------------------------------------------
        {query}
        --(End 1)-------------------------------------------------------------------------------------------------------
             ) AS X
        PIVOT (COUNT(ID) FOR LOAD IN ([FT], [PT])) AS X
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
                  "survey": "12-month Enrollment",
                  "section": "Unduplicated Count",
                  "page": "Graduate Students",
                  "name": "Graduate (Women)",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCount_SexUnknown(self):
        prompt = """
        12-month Unduplicated Count by Sex Unknown
        Reporting Reminders:
        The purpose of this supplemental section is to determine whether institutions are able to report the number of 
        students for whom sex is unknown. Note that these students must still be allocated into the 'Male' and 'Female' 
        categories in all other sections of the survey component.
        """
        comments = None
        start = '2024-07-01'
        query = f"""
        SELECT ID,
               LEVEL,
               LOAD,
               GENDER
        FROM (
        SELECT DISTINCT STC_PERSON_ID     AS ID,
                  STC_ACAD_LEVEL          AS LEVEL,
                  STTR_STUDENT_LOAD       AS LOAD,
                  PERSON.GENDER,
                  ROW_NUMBER() OVER (PARTITION BY STC_PERSON_ID ORDER BY TERM_START_DATE) AS LL_RANK
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        LEFT JOIN STUDENT_TERMS_VIEW STV ON STC.STC_PERSON_ID = STV.STTR_STUDENT AND STC.STC_TERM = STV.STTR_TERM
        LEFT JOIN TERMS ON STC.STC_TERM = TERMS_ID
        LEFT JOIN PERSON ON STC_PERSON_ID = PERSON.ID
        WHERE STATUS.STC_STATUS IN ('N', 'A')
        AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
        AND (
              TERMS_ID LIKE '%FA'
              OR TERMS_ID LIKE '%SP'
              OR TERMS_ID LIKE '%SU'
          )
        AND TERM_START_DATE < DATEADD(YEAR, 1, '{start}')
        AND TERM_END_DATE >= '{start}'
        AND STC.STC_CRED > 0
        ) AS X
        WHERE LL_RANK = 1
        AND GENDER IS NULL
        """
        agg = lambda query: f"""
        SELECT  'Sex Unknown' AS 'Grand Total',
                [UG] AS 'Undergraduate students',
                [GR] AS 'Graduate students'
        FROM (SELECT ID, LEVEL FROM ({query}) AS X) AS X
        PIVOT (COUNT(ID) FOR LEVEL IN ([UG], [GR])) AS X
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "12-month Enrollment",
                  "section": "Unduplicated Count",
                  "page": "Sex Unknown",
                  "name": "Sex Unknown",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCount_DEStatus(self):
        prompt = """
        12-month Unduplicated Count - Distance Education Status
        """
        comments = None
        query = f"""
        SELECT STUDENTS.ID,
                CASE WHEN LEVEL = 'GR' THEN 'Graduate Students'
                ELSE STU_PROGRAM.STATUS END AS DEGREE_STATUS,
                STU_DIST.STATUS AS DE_STATUS
        FROM (
        {self.enrolledStudents()}
        ) AS STUDENTS
        JOIN (
        {self.deg_status()}
        ) AS STU_PROGRAM ON STUDENTS.ID = STU_PROGRAM.ID
        JOIN (
        {self.dist_status()}
        ) AS STU_DIST ON STUDENTS.ID = STU_DIST.ID
        """
        agg = lambda query: f"""
        SELECT DE_STATUS,
            [Degree-Seeking],
            [Non-Degree-Seeking],
            [Graduate Students]
        FROM (
        {query}
        ) AS X
        PIVOT (COUNT(ID) FOR DEGREE_STATUS IN (
                            [Degree-Seeking],
                            [Non-Degree-Seeking],
                            [Graduate Students]
        )) AS X
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "12-month Enrollment",
                  "section": "Unduplicated Count",
                  "page": "Distance Education Status",
                  "name": "Distance Education Status",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCreditHourActivity(self):
        prompt = """
        12-month Instructional Activity
        July 1, 2024 - June 30, 2025
        Instructional Activity Reporting Reminder:
        Instructional activity is used to calculate an IPEDS FTE based on the institution’s reported calendar system.
        Graduate credit hour activity should not include any doctor’s – professional practice activity, the total of 
        those students’ FTE is entered separately instead.
        FTE Reporting Reminder:
        Institutions need not report their own calculations of undergraduate or graduate FTE unless IPEDS FTE 
        calculations would be misleading for comparison purposes among all IPEDS reporting institutions.
        """
        comments = None
        start = '2024-07-01'
        query = f"""
        SELECT DISTINCT STC_PERSON_ID AS ID,
                SCS_COURSE_SECTION,
                STC_CRED,
                STC_ACAD_LEVEL
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        LEFT JOIN TERMS ON STC.STC_TERM = TERMS_ID
        WHERE STATUS.STC_STATUS IN ('N', 'A')
        AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
        AND (
              TERMS_ID LIKE '%FA'
              OR TERMS_ID LIKE '%SP'
              OR TERMS_ID LIKE '%SU'
          )
        AND TERM_START_DATE < DATEADD(YEAR, 1, '{start}')
        AND TERM_END_DATE >= '{start}'
        AND STC.STC_CRED > 0
        """
        agg = lambda query: f"""
        SELECT STC_ACAD_LEVEL,
                SUM(STC_CRED) AS '2024-25 total activity'
        FROM ({query}) AS X GROUP BY STC_ACAD_LEVEL
        """
        names = lambda query: f"""
        SELECT FIRST_NAME, LAST_NAME, X.*
        FROM ({query}) AS X JOIN PERSON P ON X.ID = P.ID
        ORDER BY LAST_NAME
        """
        params = {"prompt": prompt,
                  "query": query,
                  "comments": comments,
                  "survey": "12-month Enrollment",
                  "section": "Instructional Activity",
                  "page": "Instructional Activity",
                  "name": "Instructional Activity",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)

    def getCount_HighSchool(self):
        prompt = """
        12-month Unduplicated Count of Dual Enrolled Students
        July 1, 2024 – June 30, 2025
        Reporting Reminders:
        The number of high school students enrolled in college courses for credit was reported in Part A as part of the 
        non-degree/non-certificate-seeking unduplicated enrollment.
        The number of high school students enrolled in college courses for credit reported in Part C will have some 
        duplication with the non-degree/non-certificate-seeking enrollment students reported in Part A.
        The number of high school students enrolled in college courses for credit reported in Part C should be less than
         the number of non-degree/non-certificate-seeking students reported in Part A unless all these students at your 
         institution are high school students enrolled in college courses for credit.
        Report Hispanic/Latino individuals of any race as Hispanic/Latino
        Report race for non-Hispanic/Latino individuals only
        """
        comments = None
        query = f"""
        SELECT IPEDS_RACE.THEIR_DESC AS RACE,
        IPEDS_RACE.N,
        TARGET_STUDENTS.ID,
        TARGET_STUDENTS.GENDER
        FROM ({self.ipeds_races()}) AS IPEDS_RACE
        LEFT JOIN (
        SELECT STUDENTS.ID,
        RACE,
        STUDENTS.GENDER,
        STU_TYPE.TYPE
        FROM (
        {self.enrolledStudents()}
        ) AS STUDENTS
        JOIN (
        {self.race_status()}
        ) AS STU_RACE ON STUDENTS.ID = STU_RACE.ID
        JOIN (
        {self.stu_type()}
        ) AS STU_TYPE ON STUDENTS.ID = STU_TYPE.ID
        WHERE STU_TYPE.TYPE = 'ACE'
        ) AS TARGET_STUDENTS ON IPEDS_RACE.OUR_DESC = TARGET_STUDENTS.RACE
        """
        self.print_table(query)
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
                  "survey": "12-month Enrollment",
                  "section": "Dual Enrolled Students",
                  "page": "Dual Enrolled Students",
                  "name": "Dual Enrolled Students",
                  "func_dict": {"Agg": agg, "Names": names},
                  }
        self.save(**params)













