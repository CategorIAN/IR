import pandas as pd
import os

class IPEDS:
    def __init__(self):
        pass

    def f(self):
        residence_df = pd.read_csv("\\".join([os.getcwd(), "MyData", "24-25", "FTUG_Residence.csv"]))
        graddates_df = pd.read_csv("\\".join([os.getcwd(), "MyData", "24-25", "FTUG_HighGradDates.csv"]))
        graddates_df['To'] = pd.to_datetime(graddates_df['To'])
        graddates_df_grouped = graddates_df.groupby(['Colleague ID']).agg({'To': 'max'})
        df = residence_df.merge(graddates_df_grouped, left_on='STTR_STUDENT', right_on = "Colleague ID", how="left")
        state_count = df.groupby(['STATE']).agg({'STTR_STUDENT': 'count', 'To': lambda x: (x >= '2023-08-21').sum()})
        state_count = state_count.rename(columns = {"STTR_STUDENT": 'Total',
                                          "To":'Recently Graduated From High School'})
        state_count.to_excel('\\'.join([os.getcwd(), 'MyData', 'state_count.xlsx']))
        print(state_count)

    def g(self):
        my_students_df = pd.read_csv("\\".join([os.getcwd(), "MyData", "My_Queried_Students.csv"]))
        eric_students_df = pd.read_csv("\\".join([os.getcwd(), "MyData", "2024FA FY Cohort.csv"])).loc[:, ['STUDENT_ID']]
        print(my_students_df)
        print(eric_students_df)
        ian_eric_df = my_students_df.merge(eric_students_df, "left", left_on='STTR_STUDENT', right_on='STUDENT_ID')
        print(ian_eric_df)
        eric_ian_df = eric_students_df.merge(my_students_df, 'left', left_on='STUDENT_ID', right_on='STTR_STUDENT')
        print(eric_ian_df)
        ian_eric_df.to_csv("\\".join([os.getcwd(), "MyData", "Ian_Eric_Students.csv"]))
        eric_ian_df.to_csv("\\".join([os.getcwd(), "MyData", "Eric_Ian_Students.csv"]))
