import pandas as pd
import os
import pyodbc, environ
from pathlib import Path
BASE_DIR = Path(__file__).resolve()

class Nursing_Data_Analysis:
    def __init__(self):
        self.folder = "\\".join([os.getcwd(), "NursingDataAnalysis", "Data"])
        path = os.path.join(self.folder, "Survey Responses.csv")
        self.responses = pd.read_csv(path)

    def save_cleaned_data(self):
        responses = f"""
        SELECT EMAIL, BI_201, BI_202, CH_111, CH_112, BI_214
        FROM (
        SELECT *,
                ROW_NUMBER() OVER (PARTITION BY EMAIL ORDER BY CONVERT(DATETIME, TIMESTAMP) DESC) AS TIME_RANK
        FROM (VALUES {",\n".join([f"({", ".join([f"'{val}'" for val in self.responses.loc[i, :]])})"
                                  for i in self.responses.index])})
        AS RESPONSES(
                    TIMESTAMP,
                    EMAIL,
                    BI_201,
                    BI_202,
                    CH_111,
                    CH_112,
                    BI_214,
                    NAME
                    )
        ) AS RANKED
        WHERE TIME_RANK = 1
        """
        query = f"""
        SELECT DISTINCT P.ID, BI_201, BI_202, CH_111, CH_112, BI_214
        FROM ({responses}) AS R
        JOIN PEOPLE_EMAIL ON R.EMAIL = PEOPLE_EMAIL.PERSON_EMAIL_ADDRESSES
        JOIN PERSON AS P ON PEOPLE_EMAIL.ID = P.ID
        WHERE P.ID NOT IN ('6181895', '6188540')
        """
        df = self.readSQL(query)
        df.to_csv(os.path.join(self.folder, "Cleaned_Survey_Data.csv"))

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
