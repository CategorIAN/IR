import pyodbc
import os
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, FuncFormatter

class IPEDS_DB:
    def __init__(self, folder):
        self.folder = folder
        self.varmap = pd.read_csv(os.path.join(self.folder, "varmap.csv"), index_col=0)
        self.data_path = "\\".join([os.getcwd(), self.folder, "Data"])
        self.chart_path = "\\".join([os.getcwd(), self.folder, "Charts"])
        self.school_df = pd.read_csv(os.path.join(self.folder, "schools.csv"))

    def queried_df(self, cursor, query, index_col = False):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        df = pd.DataFrame(data=data, columns=columns)
        return df.set_index(columns[0]) if index_col else df

    def academic_year(self, start):
        def f(year):
            return f"{str(year)[2:]}-{str(year + 1)[2:]}" if (start == "This Fall" or pd.isna(start)) \
                else f"{str(year - 1)[2:]}-{str(year)[2:]}"
        return f

    def value_df(self, name):
        table, variable, start = self.varmap.loc[name, :]
        print(start)
        def execute(year, cursor):
            year_table = table.replace("yyyy", str(year)).replace("xxxx", str(year - 1)[2:] + str(year)[2:])
            stmt = f"""
            SELECT [HD{year}.INSTNM] AS School,
                    '{self.academic_year(start)(year)}' AS Academic_Year,
                    [{year_table}].[{variable}] AS [{name}]
            FROM [HD{year}]
            INNER JOIN [{year_table}] ON HD{year}.UNITID = {year_table}.UNITID
            WHERE INSTNM IN ({",\n".join([f"'{school}'" for school in self.school_df['School']])})
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
    def save_df(self, name, base_year, end_year = None):
        my_end_year = base_year if end_year is None else end_year
        year_subtitle = f"{base_year}{(" to " + str(my_end_year)) if end_year is not None else ''}"
        years = list(range(base_year, my_end_year + 1))
        tables = [self.readSQL(year)(self.value_df(name)) for year in years]
        df = pd.concat(tables)
        df[name] = df[name].map(lambda x: x if x == "None" else int(x))
        df = pd.merge(self.school_df, df, on="School")
        df = df.groupby(["Group", "Academic_Year"])[name].mean().map(lambda x: round(x, 2)).reset_index()
        title = name + " - " + year_subtitle
        df.to_csv(os.path.join(self.data_path, f"{title}.csv"), index=True)

    #=================================================================================================================
    def remove_boundaries(self):
        for boundary in ["top", "bottom", "left", "right"]:
            plt.gca().spines[boundary].set_visible(False)

    def line_graph(self, file, title = None, percent = False):
        title = file.strip(".csv") if title is None else title
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        name = file.partition(' -')[0]
        df = df.pivot(index='Academic_Year', columns='Group', values=name)
        plt.figure(figsize=(8, 4))
        if percent:
            df = df.map(lambda x: round(x / 100, 2))
        df.plot(kind="line")
        self.remove_boundaries()
        if percent:
            plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        plt.gca().set_title(title, fontsize=18)
        plt.tight_layout()
        plt.tick_params(axis='both', labelsize=12)
        plt.grid(axis="y", linestyle="--")
        plt.savefig(os.path.join(self.chart_path, title + ".png"))
        plt.show()