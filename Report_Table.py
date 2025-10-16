import pandas as pd
import pyodbc, environ
from pathlib import Path
from tabulate import tabulate
import os
from functools import reduce
BASE_DIR = Path(__file__).resolve()

class Report_Table:
    def __init__(self, report: int, table: int, name: str):
        self.report = report
        self.table = table
        self.name = name
        self.report_name = self.get_report_name()
        self.carroll = Path("\\".join(["Q:", "IR", "Reports", "Ian's Reports", "Data Provided Grouped By Request"]))
        command = f"""
        INSERT INTO REPORT_TABLE (Report_ID, Table_ID, Name, Updated)
        SELECT '{report}', '{table}', '{name}', NULL
        WHERE NOT EXISTS (
            SELECT 1 FROM REPORT_TABLE 
            WHERE Report_ID = '{report}'
            AND Table_ID = '{table}'
        )
        """
        self.executeAWSSQL(command)

    def get_report_name(self):
        query = f"""
        SELECT TOP 1 NAME
        FROM REPORT
        WHERE ID = '{self.report}'
        """
        df = self.readAWSSQL(query)
        return df.iat[0, 0]

    '''
    I need to transform MSSQL query into pandas dataframe.
    '''
    def queried_df(self, cursor, query, index_col = False):
        '''
        :param cursor: Cursor for the database connection.
        :param query: String that is the MSSQL query.
        :param index_col: Boolean for the
        :return: Pandas DataFrame representing the table generated from the query.
        '''
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        df = pd.DataFrame(data=data, columns=columns)
        return df.set_index(columns[0]) if index_col else df

    '''
    I need to connect to a database to generate a Pandas DataFrame.
    '''
    def db_table(self, query, snapshot_term = '2025FA'):
        '''
        :param db: The database I need to connect to.
        :param query: The query used for the database.
        :return: Pandas Dataframe to generate for the query.
        '''
        try:
            env = environ.Env()
            db = "ODS" if snapshot_term is None else "MSSQL"
            db_name = env(f'{db}_NAME') if snapshot_term is None else f"{snapshot_term}_SNAPSHOT"
            environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
            my_str = (
                f"DRIVER={{ODBC DRIVER 17 for SQL Server}};"
                f"SERVER={env(f'{db}_HOST')};"
                f"DATABASE={db_name};"
                "Trusted_Connection=yes;"
            )
            connection = pyodbc.connect(my_str)
            cursor = connection.cursor()
            df = self.queried_df(cursor, query)
            print(tabulate(df.head(100), headers='keys', tablefmt='psql'))
            return df
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
            print("Connection Closed")

    def query_bundle(self, query, snapshot_term = '2025FA', func_dict = None):
        if func_dict is None:
            print(query)
            return {f"{self.name}.csv": self.db_table(query, snapshot_term), f"{self.name}.txt": query}
        else:
            dict_func = lambda key: {f"{self.name} ({key}).csv": self.db_table(func_dict[key](query), snapshot_term),
                                     f"{self.name} ({key}).txt": func_dict[key](query)}
            return reduce(lambda d, k: d | dict_func(k), func_dict.keys(), {})

    def save_bundle(self, path, bundle, include_code = True):
        path.mkdir(parents=True, exist_ok=True)
        for k, v in bundle.items():
            if k.endswith(".csv"):
                v.to_csv(path / k)
            else:
                if include_code:
                    with open(path / k, "w") as text_file:
                        text_file.write(v)
        table_command = f"""
        UPDATE REPORT_TABLE
        SET UPDATED = GETDATE()
        WHERE REPORT_ID = '{self.report}'
        AND TABLE_ID = '{self.table}'
        """
        self.executeAWSSQL(table_command)
        report_command = f"""
        UPDATE REPORT
        SET UPDATED = GETDATE()
        WHERE ID = '{self.report}'
        """
        self.executeAWSSQL(report_command)


    def save_draft(self, bundle, overwrite = True):
        query = f"""
        SELECT COALESCE(MAX(DRAFT_ID), 0) AS DRAFT_ID
        FROM TABLE_DRAFT
        WHERE REPORT_ID = '{self.report}'
        AND TABLE_ID = '{self.table}'
        """
        draft_number = int(self.readAWSSQL(query).iat[0, 0])
        if overwrite and draft_number > 0:
            path = self.carroll / self.report_name / self.name / f"Draft {draft_number}"
            self.save_bundle(path, bundle)
            command = f"""
            UPDATE TABLE_DRAFT
            SET DATE = GETDATE()
            WHERE REPORT_ID = '{self.report}'
            AND TABLE_ID = '{self.table}'
            AND DRAFT_ID = '{draft_number}'
            """
            self.executeAWSSQL(command)
        else:
            new_draft = draft_number + 1
            path = self.carroll / self.report_name / self.name / f"Draft {new_draft}"
            self.save_bundle(path, bundle)
            command = f"""
            INSERT INTO TABLE_DRAFT (Report_ID, Table_ID, Draft_ID, Date)
            VALUES ('{self.report}', {self.table}, '{new_draft}', GETDATE())
            """
            self.executeAWSSQL(command)


    def readAWSSQL(self, query):
        try:
            env = environ.Env()
            my_str = (f'DRIVER={{SQL Server}};'
                              f'SERVER={env("AWS_HOST")};'
                              f'DATABASE={env("AWS_Name")};'
                              f'UID={env("AWS_USER")};'
                              f'PWD={env("AWS_PASSWORD")}')
            connection = pyodbc.connect(my_str)
            cursor = connection.cursor()
            df = self.queried_df(cursor, query)
            return df
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
            print("Connection Closed")

    def executeAWSSQL(self, command):
        try:
            env = environ.Env()
            my_str = (f'DRIVER={{SQL Server}};'
                              f'SERVER={env("AWS_HOST")};'
                              f'DATABASE={env("AWS_Name")};'
                              f'UID={env("AWS_USER")};'
                              f'PWD={env("AWS_PASSWORD")}')
            connection = pyodbc.connect(my_str)
            cursor = connection.cursor()
            command = command.replace("'None'", "NULL")
            print(10 * "=" + "\nExecuting\n" + 10 * "=" + ("\n" + command + "\n") + + 10 * "=")
            cursor.execute(command)
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
            print("Connection Closed")

    '''
    I need a way to transform a dataframe into SQL query.
    '''
    def df_query(self, df, cols=None):
        cols = df.columns if cols is None else cols
        query = f"""
        SELECT *
        FROM (VALUES {",\n".join([f"({", ".join([f"'{str(val).replace("'", "''")}'" for val in df.loc[i, cols]])})"
                                  for i in df.index])})
        AS DF({", ".join([f'[{col}]' for col in cols])})
        """.replace("'nan'", "NULL")
        return query

