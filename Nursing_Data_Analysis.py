import pandas as pd
import os
import pyodbc, environ
from pathlib import Path
BASE_DIR = Path(__file__).resolve()

class Nursing_Data_Analysis:
    def __init__(self):
        path = "\\".join([os.getcwd(), "NursingDataAnalysis", "Data", "Survey Responses.csv"])
        self.responses = pd.read_csv(path,  index_col=0)

    def x(self):
        emails = self.responses['Email Address']
        print(len(set(emails)))
        query = f"""
        SELECT DISTINCT FIRST_NAME, LAST_NAME, PERSON_EMAIL_ADDRESSES AS EMAIL
        FROM PEOPLE_EMAIL
        JOIN PERSON ON PEOPLE_EMAIL.ID = PERSON.ID
        WHERE PERSON_EMAIL_ADDRESSES IN ({",\n        ".join([f"'{email}'" for email in emails])})
        AND LAST_NAME != 'Scheerer-Ws'
        """
        print(query)
        found_emails = self.readSQL(query)
        print(found_emails)
        df = self.responses.loc[lambda df: df['Email Address'] == 'ascheerer@carroll.edu']
        print(df)

    def queried_df(self, cursor, query):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        return pd.DataFrame(data=data, columns=columns)

    def readSQL(self, query):
        try:
            env = environ.Env()
            environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
            my_str = (
                f"DRIVER={{{env('DATABASE_DRIVER')}}};"
                f"SERVER={env('DATABASE_HOST')};"
                f"DATABASE={env('DATABASE_NAME')};"
                "Trusted_Connection=yes;"
            )
            connection = pyodbc.connect(my_str)
            cursor = connection.cursor()
            return self.queried_df(cursor, query)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
            print("MSSQL Connection Closed")
