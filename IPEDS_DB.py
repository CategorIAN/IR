import pyodbc
import os
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, FuncFormatter
from matplotlib import cm
import numpy as np

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
            "Gender Percentage (Women)",
            "Race Percentage (American Indian or Alaska Native)",
            "Race Percentage (Asian)",
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
    def year_values_df(self, name, base_year, end_year = None, save = True):
        my_end_year = base_year if end_year is None else end_year
        years = list(range(base_year, my_end_year + 1))
        tables = [self.readSQL(year)(self.value_df(name)) for year in years]
        df = pd.concat(tables)
        df[name] = df[name].map(lambda x: x if x == "None" else int(x))
        df = pd.merge(self.school_df, df, on="School")
        df = df.groupby(["Group", "Year"])[name].mean().map(lambda x: round(x, 2)).reset_index()
        if save:
            year_subtitle = f"{base_year}{(" to " + str(my_end_year)) if end_year is not None else ''}"
            title = name + " - " + year_subtitle
            df.to_csv(os.path.join(self.data_path, f"{title}.csv"), index=True)

    def gender_df(self, year, save = True):
        name = "Gender Percentage (Women)"
        df = self.readSQL(year)(self.value_df(name))
        df[name] = df[name].map(lambda x: x if x == "None" else int(x))
        df = pd.merge(self.school_df, df, on="School")
        df['Gender Percentage (Men)'] = 100 - df['Gender Percentage (Women)']
        names = [
            'Gender Percentage (Women)',
            'Gender Percentage (Men)'
        ]
        df = (df.groupby(["Group", "Year"])[names]
              .mean().map(lambda x: round(x, 2)).reset_index())
        if save:
            title = "Gender Percentage" + " - " + str(year)
            df.to_csv(os.path.join(self.data_path, f"{title}.csv"), index=True)

    def race_df(self, year, save = True):
        names = [
                "Race Percentage (American Indian or Alaska Native)",
            "Race Percentage (Asian)",
            "Race Percentage (Black or African American)",
            "Race Percentage (Hispanic or Latino)",
            "Race Percentage (Native Hawaiian or Other Pacific Islander)",
            "Race Percentage (Race-ethnicity unknown)",
            "Race Percentage (Two or More Races)",
            "Race Percentage (US Nonresident)",
            "Race Percentage (White)"
                ]
        tables = [self.readSQL(year)(self.value_df(name)) for name in names]
        df = reduce(lambda df1, df2: pd.merge(df1, df2, on=['School', 'Year']), tables)
        df = pd.merge(self.school_df, df, on="School")
        df[names] = df[names].apply(pd.to_numeric, errors='coerce')
        df = (df.groupby(["Group", "Year"])[names].mean().map(lambda x: round(x, 2)).reset_index())
        if save:
            title = "Race Percentage" + " - " + str(year)
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

    def pie_charts(self, file):
        title = file.strip(".csv")
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]),
                         index_col=0)
        df = df.drop('Year', axis=1).set_index("Group", drop=True)
        label_func = lambda x: x.partition(" (")[2].strip(")")
        for group in df.index:
            percentages = df.loc[group, df.columns].sort_values(ascending=False)
            labels = [label_func(x) for x in percentages.index]
            plt.figure(figsize=(10,5))
            label_length = len(df.columns)
            colors = cm.Purples(np.linspace(0.9, 0.3, label_length))
            plt.pie(percentages, labels=None, colors=colors)
            labels_values = list(zip(labels, percentages))[:label_length]
            legend_labels = [f"{label} ({x}%)" for (label, x) in labels_values]
            plt.legend(legend_labels, loc='center left', bbox_to_anchor=(-0.5, 0.5),
                       title=title.partition(" Percentage")[0])
            group_title = title + f" ({group})"
            plt.title(group_title, fontsize=18)
            plt.tight_layout()
            plt.savefig(os.path.join(self.chart_path, title, group_title + ".png"), bbox_inches='tight')
            plt.show()
            plt.close()

    def chart(self, type):
        def f(file, percent = False):
            if type == "line":
                self.line_graph(file, percent)
        return f

    def save_df_chart(self, name, base_year, end_year = None):
        self.year_values_df(name, base_year, end_year)
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
