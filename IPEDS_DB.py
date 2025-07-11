import pyodbc
import os
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, FuncFormatter
from matplotlib import cm
import numpy as np
from matplotlib.patches import Patch
from itertools import product

class IPEDS_DB:
    def __init__(self, folder):
        self.folder = folder
        self.varmap = pd.read_csv(os.path.join(self.folder, "varmap.csv"), index_col=0)
        self.data_path = "\\".join([os.getcwd(), self.folder, "Data"])
        self.chart_path = "\\".join([os.getcwd(), self.folder, "Charts"])
        self.school_df = pd.read_csv(os.path.join(self.folder, "Schools.csv"))
        self.groups = pd.read_csv(os.path.join(self.folder, "Groups.csv"))
        self.group_colors = pd.read_csv(os.path.join(self.folder, "Group_Colors.csv"), index_col=0)
        self.school_colors = pd.read_csv(os.path.join(self.folder, "School_Colors.csv"), index_col=0)
        self.stack_colors = pd.read_csv(os.path.join(self.folder, "Stack_Colors.csv"), index_col=0)
        self.gen_metrics = pd.read_csv(os.path.join(self.folder, "General Metrics.csv"))
        self.cat_metrics = pd.read_csv(os.path.join(self.folder, "Categorized Metrics.csv"))
        self.complements = pd.read_csv(os.path.join(self.folder, "Complements.csv"), index_col=0)

    def df_dict(self, my_df, default):
        return lambda i: tuple(my_df.loc[i, :]) if i in my_df.index else default

    def queried_df(self, cursor, query, index_col = False):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        df = pd.DataFrame(data=data, columns=columns)
        return df.set_index(columns[0]) if index_col else df

    def academic_year(self, start, year):
        if start == "This Fall":
            return f"AY {str(year)}-{str(year + 1)[2:]}"
        if start == "Next Fall":
            return f"AY {str(year - 1)}-{str(year)[2:]}"
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
    def year_values_df(self, name, base_year, end_year = None, grouped = True):
        my_end_year = base_year if end_year is None else end_year
        years = list(range(base_year, my_end_year + 1))
        tables = [self.readSQL(year)(self.value_df(name)) for year in years]
        df = pd.concat(tables)
        df[name] = df[name].map(lambda x: x if x == "None" else int(x))
        if grouped:
            df = pd.merge(self.school_df, df, on="School")
            df = df.groupby(["Group", "Year"])[name].mean().map(lambda x: round(x, 2)).reset_index()
            title = name + " By Peer Grouping"
        else:
            title = name + " By School"
            df = df.reset_index()
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

    def line_graph(self, file, percent = False, grouped = True, category = None):
        title = file.strip(".csv")
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        name = file.partition(' By')[0]
        columns = 'Group' if grouped else 'School'
        df = df.pivot(index='Year', columns=columns, values=name)
        df = df.reindex(columns=self.groups['Group']) if grouped else df
        color_df = self.group_colors if grouped else self.school_colors
        colors = [tuple([x / 255 for x in self.df_dict(color_df, None)(group)]) for group in df.columns]
        plt.figure(figsize=(16, 9))
        if percent:
            df = df.map(lambda x: round(x / 100, 2))
        df.plot(kind="line", color=colors, figsize=(16, 9))
        self.remove_boundaries()
        if percent:
            plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        plt.gca().set_title(title, fontsize=20)
        plt.legend(loc="upper left", bbox_to_anchor=(-0.2, 1), borderaxespad=0.)
        plt.tight_layout()
        plt.tick_params(axis='both', labelsize=12)
        plt.grid(axis="y", linestyle="--")
        by_path = ['By Group'] if grouped else ['By School']
        category_path = [] if (category is None) else [category]
        path = [self.chart_path] + by_path + category_path + [title + ".png"]
        plt.savefig(os.path.join(*path), dpi=300)
        plt.show()
        plt.close()

    def bar_chart_grouped_stacked(self, file, grouped = True):
        file_title = file.strip(".csv")
        type = file_title.partition("(")[2].partition(")")[0]
        category = file_title.partition(" ")[0]
        types = [type, self.complements.at[type, 'Complement']]
        chart_title = f"{category} Percentage By {"Peer Grouping" if grouped else "School"}"
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        name = file.partition(' By')[0]
        columns = 'Group' if grouped else 'School'
        df = df.pivot(index='Year', columns=columns, values=name)
        df = df.reindex(columns=self.groups['Group']) if grouped else df
        num_groups = len(df.index)
        num_bars = len(df.columns)
        bar_width = 0.8 / num_bars
        x_positions = np.arange(num_groups)
        fig, ax = plt.subplots(figsize=(16, 9))
        colors = [tuple([x / 255 for x in self.df_dict(self.stack_colors, None)(y)]) for y in [0, 1]]
        self.remove_boundaries()
        for i in range(num_bars):
            bar_positions = x_positions + i * bar_width
            text_pos = 100
            bottoms = np.array(num_groups * [0])
            complements = [(100 - x) for x in df[df.columns[i]]]
            ax.bar(bar_positions, complements, width=bar_width, color=colors[1], bottom=bottoms, edgecolor='white')
            for j, b, v in zip(bar_positions, bottoms, complements):
                ax.text(j, 100, str(int(round(v, 0))), ha='center', fontsize=10, color=colors[1])
            bottoms = bottoms + complements
            text_pos = text_pos + 2
            for m in range(1):
                ax.bar(x = bar_positions, height = df.loc[:, df.columns[i]], width=bar_width, color=colors[0], bottom=bottoms,
                       label=df.columns[i], edgecolor='white')
                for j, v in zip(bar_positions, df[df.columns[i]]):
                    ax.text(j, text_pos, str(int(round(v, 0))), ha='center', fontsize=10, color=colors[0])

        label_positions = reduce(lambda x, y: x + y, [list(x_positions + i * bar_width) for i in range(num_bars)])
        labels = reduce(lambda x, y: x + y, [num_groups * [self.groups.at[i, 'Abbreviation']] for i in range(num_bars)])
        ax.set_xticks(label_positions)
        ax.set_xticklabels(labels, rotation=40)
        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        label_positions_2 = x_positions + (bar_width * (num_bars - 1) / 2)
        labels_2 = df.index
        ax2.set_xticks(label_positions_2)
        ax2.set_xticklabels(labels_2)
        ax.yaxis.set_visible(False)
        ax.set_title(chart_title, fontsize=20)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        legend_elements = [Patch(facecolor=colors[i], label=types[i]) for i in range(len(types))]
        ax.legend(handles=legend_elements, title=category, loc='upper left', bbox_to_anchor=(-0.1, 1), borderaxespad=0.)
        fig.savefig(os.path.join(self.chart_path, chart_title + ".png"))
        fig.show()

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
        def f(file, percent = False, grouped = True, category = None):
            if type == "line":
                self.line_graph(file, percent, grouped, category)
        return f

    def save_df_chart(self, name, base_year, end_year = None, percent = True, grouped = True, category = None):
        self.year_values_df(name, base_year, end_year = end_year, grouped = grouped)
        title = name + " By Peer Grouping" if grouped else name + " By School"
        file = f"{title}.csv"
        self.chart('line')(file, percent = percent, grouped = grouped, category = category)

    def save_df_graph_pairs(self, base_year, end_year = None, grouped = True, category = None):
        df = self.gen_metrics if category is None else self.cat_metrics.loc[lambda df: df['Category'] == category]
        for name, percent in zip(df['Name'], df['Percent']):
            self.save_df_chart(name, base_year, end_year, percent = percent, grouped = grouped, category = category)

    def save(self, base_year, end_year = None):
        is_grouped = [False]
        category = [None, 'Gender', 'Race', 'Level']
        for g, c in product(is_grouped, category):
            print("-------------------------------------")
            print(f"Grouped: {g}; Category: {c}")
            self.save_df_graph_pairs(base_year, end_year, g, c)

