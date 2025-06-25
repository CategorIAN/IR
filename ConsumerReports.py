import pyodbc
import os
import pandas as pd
from functools import reduce

class ConsumerReports:
    def __init__(self, folder):
        self.folder = folder
        self.schools = (
            "Carroll College",
            "Gonzaga University",
            "Montana State University",
            "Rocky Mountain College",
            "Seattle University",
            "The University of Montana",
            "Whitworth University"
    #------------------------------------------------------------------------------------------------------------------
        )
        self.varmap = pd.read_csv(os.path.join(self.folder, "varmap.csv"), index_col=0)
        self.data_path = "\\".join([os.getcwd(), self.folder, "Data"])

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

    def value_df(self, year, name, alias = None):
        table, variable, start = self.varmap.loc[name, :]
        alias = self.academic_year(start)(year) if alias is None else alias
        year_table = table.replace("yyyy", str(year)).replace("xxxx", str(year - 1)[2:] + str(year)[2:])
        def execute(cursor):
            stmt = f"""
            SELECT [HD{year}.INSTNM], [{year_table}].[{variable}] AS [{alias}]
            FROM [HD{year}] INNER JOIN [{year_table}] ON HD{year}.UNITID = {year_table}.UNITID
            WHERE INSTNM IN {self.schools}
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
                df = command(cursor)
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



