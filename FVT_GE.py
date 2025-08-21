import os
import pandas as pd
import pyodbc, environ
from pathlib import Path
from tabulate import tabulate
BASE_DIR = Path(__file__).resolve()

class FVT_GE:
    def __init__(self):
        self.folder = '\\'.join([os.getcwd(), 'FVT_GE'])
        self.given_data = pd.read_csv(os.path.join(self.folder, 'Given Data.csv'))
        self.key_df = pd.read_csv(os.path.join(self.folder, 'Keys.csv'))
        self.keys = ['Record Type', 'College Student ID', 'CIP Code', 'Credential Level']

    def print(self, df):
        print(tabulate(df, headers='keys', tablefmt='psql'))

    def queried_df(self, cursor, query):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [["" if x is None else str(x) for x in tuple(y)] for y in cursor.fetchall()]
        return pd.DataFrame(data=data, columns=columns)

    def df_query_2(self, df, cols = None):
        cols = df.columns if cols is None else cols
        trans_dict = {" ": "_"} | {c: "" for c in ":()"}
        query = f"""
        SELECT *
        FROM (VALUES {",\n".join([f"({", ".join([f"'{str(val).replace("'", "''")}'" for val in df.loc[i, cols]])})"
                                  for i in df.index])})
        AS DF({", ".join([str(col).translate(str.maketrans(trans_dict)) for col in cols])})
        """.replace("'nan'", "NULL")
        return query

    def df_query(self, df, cols=None):
        cols = df.columns if cols is None else cols
        query = f"""
        SELECT *
        FROM (VALUES {",\n".join([f"({", ".join([f"'{str(val).replace("'", "''")}'" for val in df.loc[i, cols]])})"
                                  for i in df.index])})
        AS DF({", ".join([f'[{col}]' for col in cols])})
        """.replace("'nan'", "NULL")
        return query

    def ODS_SQL(self, query):
        try:
            env = environ.Env()
            environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
            my_str = (
                f"DRIVER={{{env('ODS_DRIVER')}}};"
                f"SERVER={env('ODS_HOST')};"
                f"DATABASE={env('ODS_NAME')};"
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

##======================================================================================================================
#----------Find Primary Key---------------------------------------------------------------------------------------------
    def col_string(self, columns):
        return ",\n".join([f"[{col}]" for col in columns])

    def col_count(self, columns):
        query = f"""
        SELECT {self.col_string(columns)},
        COUNT(*) AS COL_COUNT
        FROM ({self.df_query(self.given_data)}) 
        AS X GROUP BY {self.col_string(columns)}
        ORDER BY COL_COUNT DESC
        """
        print(query)
        self.print(self.ODS_SQL(query))

    def col_count_check(self, i):
        if i == 1:
            columns = ['College Student ID']
            self.col_count(columns)
        if i == 2:
            columns = ['College_Student_ID', 'CIP_Code']
            self.col_count(columns)
        if i == 3:
            columns = ['Record_Type', 'College_Student_ID', 'CIP_Code']
            self.col_count(columns)
        if i == 4:
            columns = ['Record_Type', 'College_Student_ID', 'CIP_Code', 'Credential_Level']
            self.col_count(columns)

    def save_keys(self):
        columns = ['Record Type', 'College Student ID', 'CIP Code', 'Credential Level']
        query = self.df_query(self.given_data, columns)
        print(query)
        df = self.ODS_SQL(query)
        df.to_csv(os.path.join(self.folder, 'Keys.csv'), index=False)

#-----------------------------------------------------------------------------------------------------------------------
    def getColumn_N(self):
        title = 'Comprehensive Transition and Postsecondary (CTP) Program Indicator'
        query = f"""
        SELECT {self.col_string(self.keys)},
                CASE WHEN [Record Type] = 'TA' THEN 'N' 
                END AS [{title}]
        FROM ({self.df_query(self.key_df)}) AS X
        """
        self.ODS_SQL(query).to_csv(os.path.join(self.folder, f'N. {title}.csv'), index=False)

    def getColumn_O(self):
        title = 'Approved Prison Education Program Indicator'
        query = f"""
        SELECT {self.col_string(self.keys)},
                CASE WHEN [Record Type] = 'TA' THEN 'N' 
                END AS [{title}]
        FROM ({self.df_query(self.key_df)}) AS X
        """
        self.ODS_SQL(query).to_csv(os.path.join(self.folder, f'O. {title}.csv'), index=False)



