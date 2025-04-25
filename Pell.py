import pandas as pd
import os
import pyodbc, environ
from pathlib import Path
BASE_DIR = Path(__file__).resolve()


class Pell:
    def __init__(self):
        self.folder = "\\".join([os.getcwd(), "Pell", "Data"])
        self.years = [19, 20, 21, 22, 23, 24]


    def fall_term(self, year):
        return f"20{year}FA"

    def spring_term(self, year):
        return f"20{year + 1}SP"

    def year_query(self, year):
        query = f"""
        SELECT TERMS.ID AS TERM,
                SA_STUDENT_ID AS STUDENT_ID
        FROM (VALUES ('{self.fall_term(year)}'), ('{self.spring_term(year)}')) AS TERMS(ID)
        CROSS JOIN F{year}_AWARD_LIST
        WHERE SA_AWARD = 'FPELL'
        AND SA_ACTION = 'A'
        """
        return query

    def pell(self):
        query = "\nUNION ALL\n".join([self.year_query(year) for year in self.years])
        return query

    def df_query(self, df, cols=None):
        cols = df.columns if cols is None else cols
        query = f"""
        SELECT *
        FROM (VALUES {",\n".join([f"({", ".join([f"'{str(val).replace("'", "''")}'" for val in df.loc[i, :]])})"
                                  for i in df.index])})
        AS DF({", ".join([str(col).replace(" ", "_").replace(":", "") for col in cols])})
        """.replace("'nan'", "NULL")
        return query

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

    def saveDF(self, query, name, save_sql = True):
        df = self.readSQL(query)
        df.to_csv(os.path.join(self.folder, f'{name}.csv'))
        if save_sql:
            with open(os.path.join(self.folder, f'{name}.txt'), "w", encoding="utf-8") as file:
                file.write(query)

    def SQL_values(self, query):
        df = self.readSQL(query)
        return self.df_query(df)
