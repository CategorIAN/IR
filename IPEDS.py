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

