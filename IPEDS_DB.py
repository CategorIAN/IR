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
        self.sch_abbrev = pd.read_csv(os.path.join(self.folder, "School_Abbreviations.csv"))

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
            SELECT [HD{year}].[INSTNM] AS School,
                    '{self.academic_year(start, year)}' AS Year,
                    [{year_table}].[{variable}] AS [{name}]
            FROM [HD{year}]
            LEFT OUTER JOIN [{year_table}] ON HD{year}.UNITID = {year_table}.UNITID
            WHERE [HD{year}].[INSTNM] IN ({",\n".join([f"'{school}'" for school in self.school_df['School']])})
            """
            print(100 * "-" + "Executing" + 100 * "-" + "\n" + stmt + "\n" + 2 * 100 * "-")
            df = self.queried_df(cursor, stmt, index_col=True)
            print(df)
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
        print(f"Saving {title}")
        df.to_csv(os.path.join(self.data_path, f"{title}.csv"), index=True)
    #=================================================================================================================
    def remove_boundaries(self):
        for boundary in ["top", "bottom", "left", "right"]:
            plt.gca().spines[boundary].set_visible(False)

    def line_graph(self, name, percent = False, grouped = True, category = None):
        file = f"{name} By {"Peer Grouping" if grouped else "School"}.csv"
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
        df.plot(kind="line", color=colors, figsize=(16, 9), linewidth=3)
        self.remove_boundaries()
        if percent:
            plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        plt.gca().set_title(title, fontsize=20)
        plt.legend(loc="upper left", bbox_to_anchor=(-0.2, 1), borderaxespad=0.)
        plt.tight_layout()
        plt.tick_params(axis='both', labelsize=12)
        plt.grid(axis="y", linestyle="--")
        by_path = ['By Peer Grouping'] if grouped else ['By School']
        category_path = [] if (category is None) else [category]
        path = [self.chart_path, 'Line Charts'] + by_path + category_path + [title + ".png"]
        plt.savefig(os.path.join(*path), dpi=300)
        plt.show()
        plt.close()

    def df_map(self, grouped, names):
        def f(name):
            file = f"{name} By {"Peer Grouping" if grouped else "School"}.csv"
            df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
            columns = 'Group' if grouped else 'School'
            df = df.pivot(index='Year', columns=columns, values=name)
            df = df.reindex(columns=self.groups['Group']) if grouped else df
            return df
        return {name: f(name) for name in names}

    def format_num(self, x):
        return x if pd.isna(x) else str(int(round(x, 0)))

    def bar_chart_grouped_stacked(self, category, metric, grouped = True, complement = False):
        title = f"{metric} By {"Peer Grouping" if grouped else "School"}"
        file_title = f"{metric} By {category} By {"Peer Grouping" if grouped else "School"}"
        cat_df = self.cat_metrics.loc[lambda df: (df['Category'] == category) & (df['Metric'] == metric)]
        names, types = list(cat_df['Name']), list(cat_df['Type'])
        df_map = self.df_map(grouped, names)
        #-------------------------
        base_df = df_map[names[0]]
        num_groups = len(base_df.index)
        num_bars = len(base_df.columns)
        bar_width = 0.8 / num_bars
        x_positions = np.arange(num_groups)
        fig, ax = plt.subplots(figsize=(16, 9))
        colors = [tuple([x / 255 for x in self.df_dict(self.stack_colors, None)(y)]) for y in [0, 1]]
        self.remove_boundaries()
        #--------------------------
        bottoms = np.zeros((num_groups, num_bars))
        sum_mat = reduce(lambda x, y: x + y, [df_map[name].to_numpy() for name in names])
        delta = np.nanmax(sum_mat) / 50
        text_pos = sum_mat
        if complement:
            df_mat = 100 * np.ones((num_groups, num_bars)) - sum_mat
            text_pos = text_pos + df_mat
            for i in range(num_bars):
                bar_positions = x_positions + i * bar_width
                ax.bar(x = bar_positions, height = df_mat[:, i], width=bar_width, color=colors[-1],
                       bottom=bottoms[:, i], label=base_df.columns[i], edgecolor='white')
                for j, x, v in zip(range(num_groups), bar_positions, df_mat[:, i]):
                    ax.text(x, text_pos[j, i], self.format_num(v), ha='center', fontsize=7, color=colors[-1])
            bottoms = bottoms + df_mat
            text_pos = text_pos + delta
        for n in range(len(names)):
            df_mat = df_map[names[n]].to_numpy()
            for i in range(num_bars):
                bar_positions = x_positions + i * bar_width
                ax.bar(x = bar_positions, height = df_mat[:, i], width=bar_width, color=colors[n],
                       bottom=bottoms[:, i], label=base_df.columns[i], edgecolor='white')
                for j, x, v in zip(range(num_groups), bar_positions, df_mat[:, i]):
                    ax.text(x, text_pos[j, i], self.format_num(v), ha='center', fontsize=7, color=colors[n])
            bottoms = bottoms + df_mat
            text_pos = text_pos + delta
        label_positions = reduce(lambda x, y: x + y, [list(x_positions + i * bar_width) for i in range(num_bars)])
        abbrev_df = self.groups if grouped else self.sch_abbrev
        labels = reduce(lambda x, y: x + y, [num_groups * [abbrev_df.at[i, 'Abbreviation']] for i in range(num_bars)])
        ax.set_xticks(label_positions)
        ax.set_xticklabels(labels, rotation=40)
        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        label_positions_2 = x_positions + (bar_width * (num_bars - 1) / 2)
        labels_2 = base_df.index
        ax2.set_xticks(label_positions_2)
        ax2.set_xticklabels(labels_2)
        ax.yaxis.set_visible(False)
        ax.set_title(title, fontsize=20)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        leg_elems = [Patch(facecolor=colors[i], label=types[i]) for i in reversed(range(len(names)))]
        if complement:
            leg_elems += [Patch(facecolor=colors[-1], label = self.complements.at[category, 'Complement'])]
        ax.legend(handles=leg_elems, title=category, loc='upper left', bbox_to_anchor=(-0.15, 1), borderaxespad=0.)
        by_path = ['By Peer Grouping'] if grouped else ['By School']
        path = [self.chart_path, 'Grouped, Stacked Bar Charts'] + by_path + [file_title + ".png"]
        plt.savefig(os.path.join(*path), dpi=300)
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

    def df_line_graph(self, base_year, end_year = None):
        def f(name, percent = True, grouped = True, category = None):
            self.year_values_df(name, base_year, end_year = end_year, grouped = grouped)
            title = name + " By Peer Grouping" if grouped else name + " By School"
            file = f"{title}.csv"
            self.line_graph(file, percent = percent, grouped = grouped, category = category)
        return f

    def save_dfs_line_charts(self, base_year, end_year = None, grouped = True, category = None, metric = None, make_df = True):
        if category is None:
            df = self.gen_metrics
        else:
            df = self.cat_metrics.loc[lambda df: (df['Category'] == category) & (df['Metric'] == metric)]
        save_func = self.df_line_graph(base_year, end_year) if make_df else self.line_graph
        for name, percent in zip(df['Name'], df['Percent']):
            save_func(name, percent = percent, grouped = grouped, category = category)

    def save_dfs_line_charts_all(self, base_year, end_year = None, make_df = True):
        is_grouped = [True, False]
        cat_met = [
            (None, None),
            ('Gender', 'Enrollment Percentage'),
            ('Race', 'Enrollment Percentage'),
            ('Level', 'Enrollment'),
            ('Gender', 'Graduation Rate (6 Years)'),
            ('Gender', 'Graduation Rate')
        ]
        for (g, (cat, met)) in product(is_grouped, cat_met):
            print("-------------------------------------")
            print(f"Grouped: {g}; Category: {cat}; Metric: {met}")
            self.save_dfs_line_charts(base_year, end_year, g, cat, met, make_df)

    def save_df_gsb_graph(self, base_year, end_year = None, make_df = True):
        def f(category, metric, grouped = True, complement = False):
            names = self.cat_metrics.loc[lambda df: (df['Category'] == category) & (df['Metric'] == metric)]['Name']
            by_func = lambda name: f"{name} By {"Peer Grouping" if grouped else "School"}"
            for name in names:
                if make_df:
                    self.year_values_df(name, base_year, end_year, grouped)
                else:
                    try:
                        file = by_func(name) + ".csv"
                        print(file)
                        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
                    except FileNotFoundError:
                        self.year_values_df(name, base_year, end_year, grouped)
            self.bar_chart_grouped_stacked(category, metric, grouped, complement)
        return f

    def save_dfs_gsb_charts_all(self, base_year, end_year = None, make_df = True):
        is_grouped = [True, False]
        cat_met = [
                    ('Gender', 'Enrollment Percentage', True),
                    ('Race (W-NW)', 'Enrollment Percentage', True),
                    ('Gender', 'Graduation Rate (6 Years)', False),
                    ('Level', 'Enrollment', False),
                    ('Gender', 'Graduation Rate', False),
                ]
        for (g, (cat, met, comp)) in product(is_grouped, cat_met):
            self.save_df_gsb_graph(base_year, end_year, make_df)(cat, met, g, comp)





