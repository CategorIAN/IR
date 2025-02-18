import pyodbc
import pandas as pd
import environ
import os

class Carroll_DB:
    def insert_rows(self, cursor):
        df = pd.read_csv("\\".join([os.getcwd(), "Tables.csv"]))
        print(df)
        def insert_row(row):
            return f"""
                    INSERT INTO Tables (Name, Description, Used, Empty, Reviewed, Not_Applicable) VALUES (
                    '{row['Name']}', 
                    '{row['Description']}',
                    '{row['Used']}',
                    '{row['Empty']}',
                    '{row['Reviewed']}',
                    '{row['Not_Applicable']}'
                    )
                    """.replace("'nan'", "NULL")

        for index, row in df.iterrows():
            print(insert_row(row))
            cursor.execute(insert_row(row))

    def insert_rows2(self, cursor):
        df = pd.read_csv("\\".join([os.getcwd(), "2025SP_SNAPSHOT Metadata Guide.csv"]))
        print(df)
        def insert_row(row):
            return f"""
                    INSERT INTO Variables (Name, TableName, DataType) VALUES (
                    '{row['TABLE_NAME']}.{row['COLUMN_NAME']}',
                    '{row['TABLE_NAME']}',
                    '{row['DATA_TYPE']}'
                    )
                    """.replace("'nan'", "NULL")

        for index, row in df.iterrows():
            print(insert_row(row))
            cursor.execute(insert_row(row))

    def queried_df(self, cursor, query, index_col=False):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        df = pd.DataFrame(data=data, columns=columns)
        return df.set_index(columns[0]) if index_col else df

    def executeSQL(self, commands):
        try:
            env = environ.Env()
            mssql_conn_str = (f'DRIVER={{SQL Server}};'
                              f'SERVER={env("DB_HOST")};'
                              f'DATABASE={env("DB_Name")};'
                              f'UID={env("DB_USER")};'
                              f'PWD={env("DB_PASSWORD")}')
            connection = pyodbc.connect(mssql_conn_str)
            cursor = connection.cursor()
            for command in commands:
                command(cursor)
            connection.commit()
            cursor.close()
            connection.close()
            print("Connection is closed.")
        except pyodbc.Error as e:
            print("Error:", e)

    def readSQL(self, year):
        def execute(command):
            try:
                env = environ.Env()
                mssql_conn_str = (f'DRIVER={{SQL Server}};'
                                  f'SERVER={env("DB_HOST")};'
                                  f'DATABASE={env("DB_Name")};'
                                  f'UID={env("DB_USER")};'
                                  f'PWD={env("DB_PASSWORD")}')
                connection = pyodbc.connect(mssql_conn_str)
                cursor = connection.cursor()
                df = command(cursor)
                cursor.close()
                connection.close()
                print("Connection is closed.")
                return df
            except pyodbc.Error as e:
                print("Error:", e)
        return execute

