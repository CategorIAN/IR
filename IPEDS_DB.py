import pyodbc
import os
import pandas as pd
from functools import reduce

class IPEDS_DB:
    def __init__(self, folder):
        self.folder = folder
        self.varmap = pd.read_csv(os.path.join(self.folder, "varmap.csv"), index_col=0)
        self.data_path = "\\".join([os.getcwd(), self.folder, "Data"])
        self.schools = pd.read_csv(os.path.join(self.folder, "schools.csv"))

    def df_vals(self, df, alias = None, cols=None):
        alias = 'DF' if alias is None else alias
        cols = df.columns if cols is None else cols
        query = f"""
        (VALUES {",\n".join([f"({", ".join([f"'{str(val).replace("'", "''")}'" for val in df.loc[i, :]])})"
                                  for i in df.index])})
        AS {alias}({", ".join([str(col).replace(" ", "_").replace(":", "") for col in cols])})
        """.replace("'nan'", "NULL")
        return query

    def df_access_vals(self, df, alias = None, cols=None):
        alias = 'DF' if alias is None else alias
        cols = df.columns if cols is None else cols
        first_row = df.loc[0, :]
        query = f"""
        (SELECT {"\nUNION ALL SELECT ".join([", ".join([f"'{val}'" for val, i 
                                                        in zip(df.loc[i, :], range(1, len(df.index + 1)))]) 
                                           for i in df.index])}) AS {alias}
        """.replace("'nan'", "NULL")
        return query

    def queried_df(self, cursor, query, index_col = False):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        df = pd.DataFrame(data=data, columns=columns)
        return df.set_index(columns[0]) if index_col else df

    def academic_year(self, start):
        def f(year):
            return f"{year}-{str(year + 1)[2:]}" if start == "This Fall" else f"{year - 1}-{str(year)[2:]}"
        return f

    def value_df(self, name):
        table, variable, start = self.varmap.loc[name, :]
        def execute(year, cursor):
            year_table = table.replace("yyyy", str(year)).replace("xxxx", str(year - 1)[2:] + str(year)[2:])
            stmt = f"""
            SELECT  DF.F1,
                    DF.F2,
                    '{self.academic_year(start)(year)}' AS ACADEMIC_YEAR,
                    {year_table}.{variable} AS [{name}]
            FROM {self.df_access_vals(self.schools)}
            JOIN HD{year} ON DF.F1 = HD{year}.INSTM
            JOIN {year_table} ON HD{year}.UNITID = {year_table}.UNITID
            """
            print(100 * "-" + "Executing" + 100 * "-" + "\n" + stmt + "\n" + 2 * 100 * "-")
            df = self.queried_df(cursor, stmt, index_col=True)
            return df
        return execute

    def readSQL(self, year):
        def execute(command):
            try:
                database_path = "\\".join(["Q:\\IR\\IPEDS Databases", f"{year}.accdb"])
                conn_str = (
                        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                        r"Dbq=" + database_path + ";"
                )
                connection = pyodbc.connect(conn_str)
                cursor = connection.cursor()
                df = command(year, cursor)
                cursor.close()
                connection.close()
                print("Connection is closed.")
                return df
            except pyodbc.Error as e:
                print("Error:", e)
        return execute

    #=================================================================================================================
    def x(self, name, base_year, end_year = None):
        my_end_year = base_year if end_year is None else end_year
        year_subtitle = f"{base_year}{(" to " + str(my_end_year)) if end_year is not None else ''}"
        years = list(range(base_year, my_end_year + 1))
        tables = [self.readSQL(year)(self.value_df(year, name)) for year in years]
        df = reduce(lambda df1, df2: pd.merge(df1, df2, on='INSTNM'), tables)
        print(df)
        df = df.map(lambda x: x if x == "None" else int(x))
        title = name + " - " + year_subtitle
        df.to_csv(os.path.join(self.data_path, f"{title}.csv"), index=True)