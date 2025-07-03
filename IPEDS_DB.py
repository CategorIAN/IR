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
        self.school_df = pd.read_csv(os.path.join(self.folder, "Schools.csv"))
        self.color_df = pd.read_csv(os.path.join(self.folder, "Colors.csv"), index_col=0)
        self.color_map = {group: tuple(self.color_df.loc[group, :]) for group in self.color_df.index}
        self.metrics = [
            "Graduation Rate (4 Years)",
            "Retention Rate",
            "Women Percentage",
            "Race Percentage (American Indian or Alaska Native)",
            "Race Percentage (Asian)",
            "Race Percentage (Asian or Native Hawaiian or Pacific Islander)",
            "Race Percentage (Black or African American)",
            "Race Percentage (Hispanic or Latino)",
            "Race Percentage (Native Hawaiian or Other Pacific Islander)",
            "Race Percentage (Two or More Races)",
            "Race Percentage (US Nonresident)",
            "Race Percentage (White)",
            "Pell Percentage"
        ]

    def queried_df(self, cursor, query, index_col = False):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        df = pd.DataFrame(data=data, columns=columns)
        return df.set_index(columns[0]) if index_col else df

    def academic_year(self, start, year):
        if start == "This Fall":
            return f"{str(year)[2:]}-{str(year + 1)[2:]}"
        if start == "Next Fall":
            return f"{str(year - 1)[2:]}-{str(year)[2:]}"
        else:
            return year

    def value_df(self, name):
        table, variable, start = self.varmap.loc[name, :]
        def execute(year, cursor):
            year_table = table.replace("yyyy", str(year)).replace("xxxx", str(year - 1)[2:] + str(year)[2:])
            stmt = f"""
            SELECT [HD{year}.INSTNM] AS School,
                    '{self.academic_year(start, year)}' AS Year,
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
        df = df.groupby(["Group", "Year"])[name].mean().map(lambda x: round(x, 2)).reset_index()
        title = name + " - " + year_subtitle
        print(title)
        df.to_csv(os.path.join(self.data_path, f"{title}.csv"), index=True)

    #=================================================================================================================
    def remove_boundaries(self):
        for boundary in ["top", "bottom", "left", "right"]:
            plt.gca().spines[boundary].set_visible(False)

    def line_graph(self, file, percent = False):
        title = file.strip(".csv")
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        name = file.partition(' -')[0]
        df = df.pivot(index='Year', columns='Group', values=name)
        colors = [tuple([x / 255 for x in self.color_map[group]]) for group in df.columns]
        plt.figure(figsize=(8, 4))
        if percent:
            df = df.map(lambda x: round(x / 100, 2))
        df.plot(kind="line", color=colors)
        self.remove_boundaries()
        if percent:
            plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        plt.gca().set_title(title, fontsize=18)
        plt.tight_layout()
        plt.tick_params(axis='both', labelsize=12)
        plt.grid(axis="y", linestyle="--")
        plt.savefig(os.path.join(self.chart_path, title + ".png"), bbox_inches='tight')
        plt.show()
        plt.close()

    def chart(self, type):
        def f(file, percent = False):
            if type == "line":
                self.line_graph(file, percent)
        return f

    def save_df_chart(self, name, base_year, end_year = None):
        self.save_df(name, base_year, end_year)
        my_end_year = base_year if end_year is None else end_year
        year_subtitle = f"{base_year}{(" to " + str(my_end_year)) if end_year is not None else ''}"
        title = name + " - " + year_subtitle
        file = f"{title}.csv"
        def f(type, percent):
            return self.chart(type)(file, percent)
        return f

    def save_data(self, base_year, end_year = None):
        for name in self.metrics:
            self.save_df_chart(name, base_year, end_year)("line", True)
