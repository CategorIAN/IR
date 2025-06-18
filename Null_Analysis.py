import pandas as pd
import os
import pyodbc, environ
from pathlib import Path
BASE_DIR = Path(__file__).resolve()



class Null_Analysis:
    def __init__(self):
        self.folder = '\\'.join([os.getcwd(), 'NullAnalysis'])

    def queried_df(self, cursor, query):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        return pd.DataFrame(data=data, columns=columns)

    def irSQL(self, query):
        try:
            env = environ.Env()
            environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
            my_str = (f'DRIVER={{SQL Server}};'
                              f'SERVER={env("DB_HOST")};'
                              f'DATABASE={env("DB_Name")};'
                              f'UID={env("DB_USER")};'
                              f'PWD={env("DB_PASSWORD")}')
            connection = pyodbc.connect(my_str)
            cursor = connection.cursor()
            return self.queried_df(cursor, query)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
            print("MSSQL Connection Closed")

    def snapshotSQL(self, query):
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

    def null_percentage(self, varname, tablename):
        print(f"Counting Nulls in {varname}")
        query = f"""
        SELECT ROUND(AVG(CAST(IS_NULL AS FLOAT)), 3) AS NULL_PERCENTAGE
        FROM (
            SELECT CASE WHEN {varname.upper()} IS NULL THEN 1 ELSE 0 END AS IS_NULL
            FROM {tablename}
        ) AS X
        """
        df = self.snapshotSQL(query)
        print(df.at[0, 'NULL_PERCENTAGE'])
        return df.at[0, 'NULL_PERCENTAGE']

    def nulls(self, request_id):
        query = f"""
        SELECT VarName, TableName
        FROM REQUEST_VARIABLES
        JOIN VARIABLES ON REQUEST_VARIABLES.VARNAME = VARIABLES.NAME
        WHERE Request_ID = {request_id}
        """
        vars_tables = self.irSQL(query).set_index('VarName')['TableName'].to_dict().items()
        data = {var: [table, self.null_percentage(var, table)] for var, table in vars_tables}
        df = pd.DataFrame.from_dict(data, orient='index', columns = ['Table', 'Null Percentage']).rename_axis('Var')
        df.to_csv(os.path.join(self.folder, f'Request_{request_id}_Nulls.csv'))
        return df
