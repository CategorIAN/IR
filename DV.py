import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, FuncFormatter
import numpy as np
from textwrap import wrap
from matplotlib import cm
from matplotlib.patches import Patch
from functools import reduce
from itertools import product
import pyodbc


class DV:
    def __init__(self, folder):
        self.folder = folder
        self.guides = os.path.join(self.folder, "Guides")
        self.varmap = pd.read_csv(os.path.join(self.guides, "varmap.csv"), index_col=0)
        self.data_path = "\\".join([os.getcwd(), self.folder, "Data"])
        self.chart_path = "\\".join([os.getcwd(), self.folder, "Charts"])
        self.school_df = pd.read_csv(os.path.join(self.guides, "Schools.csv"))
        self.groups = pd.read_csv(os.path.join(self.guides, "Groups.csv"), index_col=0)
        self.group_colors = pd.read_csv(os.path.join(self.guides, "Group_Colors.csv"), index_col=0)
        self.school_colors = pd.read_csv(os.path.join(self.guides, "School_Colors.csv"), index_col=0)
        self.stack_colors = pd.read_csv(os.path.join(self.guides, "Stack_Colors.csv"), index_col=0)
        self.gen_metrics = pd.read_csv(os.path.join(self.guides, "General Metrics.csv"))
        self.metrics = pd.read_csv(os.path.join(self.guides, "Metrics.csv"))
        cat_metrics = pd.read_csv(os.path.join(self.guides, "Categorized Metrics.csv"))
        self.cat_metrics = cat_metrics.merge(self.metrics, left_on = "Metric", right_on = "Name", suffixes = ('', '_'))
        self.cat_metric_names = pd.read_csv(os.path.join(self.guides, "Categorized Metrics Joined.csv"))
        self.complements = pd.read_csv(os.path.join(self.guides, "Complements.csv"), index_col=0)
        self.sch_abbrev = pd.read_csv(os.path.join(self.guides, "School_Abbreviations.csv"), index_col=0)
        self.year_colors = pd.read_csv(os.path.join(self.guides, "Year_Colors.csv"), index_col = [0, 1])
        self.school_colors_multi = pd.read_csv(os.path.join(self.guides, "School_Colors_Multi.csv"), index_col=[0, 1])
        self.group_colors_multi = pd.read_csv(os.path.join(self.guides, "Group_Colors_Multi.csv"), index_col=[0, 1])
        self.line_chart_df = pd.read_csv(os.path.join(self.guides, "Line Charts.csv"), index_col=0)

    def remove_boundaries(self):
        for boundary in ["top", "bottom", "left", "right"]:
            plt.gca().spines[boundary].set_visible(False)

    def bar_chart_h(self, file, title = None, percent = False):
        title = file.strip(".csv") if title is None else title
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        target = df.columns[0]
        df = df.sort_values(by=target, ascending=True)
        df.plot(kind="barh", legend=False)  #Change
        plt.gca().set_xlabel("")
        plt.gca().set_ylabel("")
        plt.gca().xaxis.set_visible(False)   #Change
        display = lambda v: str(int(100 * v)) + "%" if percent else str(round(v, 1))
        for i, v in enumerate(df[target]):
            plt.text(v + (v / abs(v) if v != 0 else 0) * .08 * max(df[target]), i, display(v), va='center', ha='center')
        self.remove_boundaries()
        plt.gca().set_title("\n".join(wrap(title, width=20)), fontsize=18)
        plt.xlim(min(df[target]) - .1 * max(df[target]), max(df[target]) + .08 * max(df[target])) #Change
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_path, title + ".png"))
        plt.show()

    def bar_chart_v(self, file, title = None, percent = False):
        title = file.strip(".csv") if title is None else title
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        target = df.columns[0]
        df.plot(kind="bar", legend=False, color = "purple")
        plt.gca().set_xlabel("")
        plt.gca().set_ylabel("")
        plt.gca().yaxis.set_visible(False)
        display = lambda v: str(int(100 * v)) + "%" if percent else str(round(v, 1))
        for i, v in enumerate(df[target]):
            plt.text(i, v + v / abs(v) * .01 * max(df[target]), display(v), va='center', ha='center')
        self.remove_boundaries()
        plt.gca().set_title(title, fontsize=18)
        plt.ylim(min(df[target]) - .1 * max(df[target]), max(df[target]) + .08 * max(df[target]))
        plt.gca().tick_params(axis='both', labelsize=6)
        plt.xticks(rotation=10, ha='right')
        plt.savefig(os.path.join(self.output_path, title + ".png"))
        plt.show()

    def bar_chart_grouped(self, file, title = None, colors = plt.cm.tab10.colors, money=False, percent = False):
        title = file.strip(".csv") if title is None else title
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        num_groups = len(df.index)
        num_bars = len(df.columns)
        bar_width = 0.6 / num_bars
        x_positions = np.arange(num_groups)
        colors = colors[:num_bars]
        plt.figure(figsize=(10, 6))
        self.remove_boundaries()
        display = lambda v: "" if pd.isna(v) else f"${round(v / 1000)}k" \
            if money else str(int(100 * v)) + "%" if percent else str(round(v, 1))
        for i in range(num_bars):
            bar_positions = x_positions + i * bar_width
            plt.bar(bar_positions, df.loc[:, df.columns[i]], width=bar_width, color=colors[i], label=df.columns[i])
            if i in {0, num_bars - 1}:
                for j, v in zip(bar_positions, df[df.columns[i]]):
                    plt.text(j, v + v / abs(v) * 0.01, display(v), ha='center', fontsize=10)
        labels = [df.index[i] for i in range(num_groups)]
        plt.ylim(df.min().min() - .1 * df.max().max(), df.max().max() + .08 * df.max().max())
        plt.xticks(x_positions + bar_width * (num_bars - 1) / 2, labels)
        plt.gca().yaxis.set_visible(False)
        plt.gca().set_title(title, fontsize=18)
        plt.xlabel(df.index.name, fontsize=14)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig(os.path.join(self.output_path, title + ".png"))
        plt.show()

    def pie_chart(self, file, title = None):
        title = file.removesuffix(".csv") if title is None else title
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        target = df.columns[0]
        df = df.sort_values(by=target, ascending=False)
        plt.figure(figsize=(10, 5))
        params = {"y": df.columns[0], "legend": True, "labels": None}
        label_length = len(df.index)
        colors = cm.Purples(np.linspace(0.9, 0.3, label_length))
        df.plot.pie(**(params | {"colors": colors}))
        labels_values = list(zip(df.index, df[df.columns[0]]))[:label_length]
        legend_labels = [f"{label} ({round(100 * x, 1)}%)" for (label, x) in labels_values]
        plt.legend(legend_labels, loc='center left', bbox_to_anchor=(-1, 0.5))
        plt.xlabel('')
        plt.ylabel('')
        plt.tight_layout()
        plt.suptitle(title, x=0.5, y = 0.8, fontsize=20)
        plt.savefig(os.path.join(self.output_path, title + ".png"))
        plt.show()

    def color_dict(self, my_df):
        return {i: tuple([x / 255 for x in my_df.loc[i, ['Red', 'Blue', 'Green']]]) for i in my_df.index}

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
            year_table = (table
                          .replace("yyyy", str(year))
                          .replace("xxxx", str(year - 1)[2:] + str(year)[2:])
                          .replace("zz", str(year)[2:]))
            stmt = f"""
            SELECT [HD{year}].[INSTNM] AS School,
                    '{self.academic_year(start, year)}' AS Year,
                    [{year_table}].[{variable}] AS [{name}]
            FROM [HD{year}]
            LEFT OUTER JOIN [{year_table}] ON HD{year}.UNITID = {year_table}.UNITID
            WHERE [HD{year}].[INSTNM] IN ({",\n".join([f"'{school}'" for school in self.school_df['School']])})
            """
            print(100 * "-" + "Executing" + 100 * "-" + "\n" + stmt + "\n" + 2 * 100 * "-")
            try:
                df = self.queried_df(cursor, stmt, index_col=True)
                print(df)
                return df
            except Exception as e:
                print(e)
                stmt = f"""
                 SELECT [HD{year}].[INSTNM] AS School,
                    '{self.academic_year(start, year)}' AS Year,
                    NULL AS [{name}]
                    FROM [HD{year}]
                    WHERE [HD{year}].[INSTNM] IN ({",\n".join([f"'{school}'" for school in self.school_df['School']])})
                """
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
    def year_values_df(self, name, base_year, end_year, grouped = True):
        years = list(range(base_year, end_year + 1))
        tables = [self.readSQL(year)(self.value_df(name)) for year in years]
        df = pd.concat(tables)
        df[name] = df[name].map(lambda x: None if pd.isna(x) or x in [None, "None", "", 0] else int(x))
        if grouped:
            df = pd.merge(self.school_df, df, on="School")
            df = df.groupby(["Group", "Year"])[name].mean().map(lambda x: round(x, 2)).reset_index()
            title = name + " Average By Peer Grouping"
        else:
            title = name + " By School"
            df = df.reset_index()
        title = f"{title} ({base_year}-{end_year})"
        print(f"Saving {title}")
        df.to_csv(os.path.join(self.data_path, f"{title}.csv"), index=True)
    #=================================================================================================================
    def line_graph(self, name, base_year, end_year, grouped = True):
        type = self.line_chart_df.at[name, 'Type']
        if type == "Simple":
            category = None
            percent = self.metrics.loc[lambda df: df['Name'] == name]['Percent'].iloc[0]
        else:
            cat_name = self.cat_metric_names.loc[lambda df: df['Name'] == name]['Categorized Metric'].iloc[0]
            category = self.cat_metrics.loc[lambda df: df['Name'] == cat_name]['Category'].iloc[0]
            percent = self.cat_metrics.loc[lambda df: df['Name'] == cat_name]['Percent'].iloc[0]
        file = f"{name} {"Average By Peer Grouping" if grouped else "By School"} ({base_year}-{end_year}).csv"  #Wrong
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        columns = 'Group' if grouped else 'School'
        df = df.pivot(index='Year', columns=columns, values=name)
        df = df.reindex(columns=self.groups.index) if grouped else df
        color_df = self.group_colors if grouped else self.school_colors
        color_dict = self.color_dict(color_df)
        fig, ax = plt.subplots(figsize=(16, 9))
        df = df.map(lambda x: round(x / 100, 3)) if percent else df
        colors = [color_dict[group] for group in df.columns]
        df.plot(kind="line", color='black', figsize=(16,9), linewidth=4, ax=ax)
        df.plot(kind="line", color=colors, figsize=(16, 9), linewidth=3, ax=ax)
        self.remove_boundaries()
        plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1.0)) if percent else None
        plt.tick_params(axis='both', labelsize=12)
        plt.grid(axis="y", linestyle="--")
        title = file.strip(".csv")
        if len(df.columns) > 1:
            leg_elems = [Patch(facecolor=colors[i], label=df.columns[i]) for i in range(len(df.columns))]
            ax.legend(handles=leg_elems, title=category, loc='upper left', bbox_to_anchor=(-0.3, 1), borderaxespad=0.)
        else:
            name, _, years = title.partition("By School ")
            title = f"{df.columns[0]} {name}{years}"
            plt.legend().remove()
        plt.suptitle(title, fontsize=20)
        plt.tight_layout()
        by_path = ['By Peer Grouping'] if grouped else ['By School']
        category_path = [] if (category is None) else [category]
        path = [self.chart_path, 'Line Charts'] + by_path + category_path + [title + ".png"]
        plt.savefig(os.path.join(*path), dpi=300)
        plt.show()
        plt.close()

    def df_agg(self, name, base_year, end_year, grouped):
        guide = self.cat_metric_names.merge(self.cat_metrics, left_on='Categorized Metric', right_on='Name')
        guide = guide.loc[lambda df: df['Categorized Metric'] == name].set_index('Name_x')
        category = list(guide['Category'])[0]
        complement = list(guide['Complement'])[0]
        names = guide.index
        def f(n):
            file = f"{n} {"Average By Peer Grouping" if grouped else "By School"} ({base_year}-{end_year}).csv"
            df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
            df = df.rename(columns={n: 'Value', 'School': 'Group'})
            my_type = guide.at[n, 'Type']
            df[category] = len(df.index) * [my_type]
            return df
        df = pd.concat([f(n) for n in names])
        if complement:
            comp_df = df.groupby(by=['Year', 'Group'])['Value'].agg(lambda x: 100 - x.sum()).reset_index()
            comp_df[category] = len(comp_df.index) * [self.complements.at[category, 'Complement']]
            df = pd.concat([df, comp_df])
        return df


    def filter_and_sort(self, df, groups, years):
        def f(i, j):
            return df.loc[(df['Group'] == groups[i]) & (df['Year'] == years[j])].sort_values(by='Value').reset_index()
        return f


    def bar_chart_grouped_stacked(self, name, base_year, end_year, grouped = True):
        title = f"{name} By {"Average Peer Grouping" if grouped else "School"} ({base_year}-{end_year})"
        file_title = f"{name} {"Average By Peer Grouping" if grouped else "By School"} ({base_year}-{end_year})"
        cat_metric = self.cat_metrics.loc[lambda df: df['Name'] == name].iloc[0]
        category, percent, pie = cat_metric[['Category', 'Percent', 'Pie']]
        df = self.df_agg(name, base_year, end_year, grouped)
        df['Value'] = df['Value'].map(lambda x: round(x / 100, 3)) if percent else df['Value']
        groups = list(self.groups.index) if grouped else sorted(list(df['Group'].unique()))
        years = sorted(list(df['Year'].unique()))
        types = sorted(list(df[category].unique()))
        type_dict = {type: i for i, type in enumerate(types)}
        #-------------------------
        num_groups, num_bars = len(groups), len(years)
        group_width = 0.7
        bar_width = group_width / num_bars
        x_positions = np.linspace(0, group_width, num_bars)
        fig, ax = plt.subplots(figsize=(16, 9))
        color_dict = self.color_dict(self.group_colors_multi if grouped else self.school_colors_multi)
        self.remove_boundaries()
        #--------------------------
        my_max = 1 if pie else np.nanmax(df['Value'])
        ax.set_ylim(0, my_max)
        filter_sort_func = self.filter_and_sort(df, groups, years)
        if pie:
            for i in range(num_groups):
                bar_positions = x_positions + i
                for j in range(len(years)):
                    df_part = filter_sort_func(i, j)
                    bottom = 0
                    for k in range(len(types)):
                        type = types[k]
                        try:
                            value = list(df_part.loc[lambda df: df[category] == type]['Value'])[0]
                        except Exception:
                            print(df_part)
                        args = {"x": bar_positions[j], "height": value, "width": bar_width,
                                "color": color_dict[(groups[i], k)], "bottom": bottom, "edgecolor": 'black'}
                        ax.bar(**args)
                        bottom = bottom + value
        else:
            for i in range(num_groups):
                bar_positions = x_positions + i
                for j in range(len(years)):
                    df_part = filter_sort_func(i, j)
                    bottom = 0
                    for k in df_part.index:
                        type_index = type_dict[df_part.at[k, category]]
                        args = {"x": bar_positions[j], "height": df_part.at[k, 'Value'] - bottom, "width": bar_width,
                                "color":color_dict[(groups[i], type_index)] , "bottom": bottom, "edgecolor": 'black'}
                        ax.bar(**args)
                        bottom = df_part.at[k, 'Value']
        #---------------------------------------------------------------------------------------------------------------
        if len(groups) > 1:
            label_positions = np.arange(0, num_groups, 1) + group_width / 2
            labels = groups
            ax.set_xticks(label_positions)
            ax.set_xticklabels(labels, rotation=20, fontsize=8)
        else:
            name, _, year_str = title.partition("By School ")
            title = f"{groups[0]} {name}{year_str}"
            ax.set_xticks(x_positions)
            ax.set_xticklabels(years)
        plt.suptitle(title, fontsize=20)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        leg_labels = [f"{group} - {type}" for (group, type) in product(groups, types)]
        leg_colors = reduce(lambda x, y: x + y, [[color_dict[(j, i)] for i in range(len(types))] for j in groups])
        leg_elems = [Patch(facecolor=color, label=label) for color, label in zip(leg_colors, leg_labels)]
        ax.legend(handles=leg_elems, title=category, loc='upper left', bbox_to_anchor=(-0.2, 1), borderaxespad=0.)
        by_path = ['By Peer Grouping'] if grouped else ['By School']
        path = [self.chart_path, 'Grouped, Stacked Bar Charts'] + by_path + [file_title + ".png"]
        plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1.0)) if percent else None
        plt.tight_layout(pad=2.0)
        plt.savefig(os.path.join(*path), dpi=300)
        plt.show()
        plt.close()


    def save_df_line_graph(self, base_year, end_year = None, make_df = True):
        def f(name, grouped = True):
            if make_df:
                self.year_values_df(name, base_year, end_year = end_year, grouped = grouped)
                self.line_graph(name, base_year, end_year, grouped = grouped)
            else:
                try:
                    self.line_graph(name, base_year, end_year, grouped=grouped)
                except FileNotFoundError:
                    self.year_values_df(name, base_year, end_year=end_year, grouped=grouped)
                    self.line_graph(name, base_year, end_year, grouped=grouped)
        return f

    def save_dfs_line_charts_all(self, base_year, end_year = None, make_df = True):
        is_grouped = [False]
        names = list(self.line_chart_df.index)
        for (grouped, name) in product(is_grouped, names):
            self.save_df_line_graph(base_year, end_year, make_df)(name, grouped)

    def save_df_gsb_graph(self, base_year, end_year = None, make_df = True):
        def f(name, grouped = True):
            names = self.cat_metric_names.loc[lambda df: df['Categorized Metric'] == name]['Name']
            by_func = lambda n: f"{n} {"Average By Peer Grouping" if grouped else "By School"} ({base_year}-{end_year})"
            for n in names:
                if make_df:
                    self.year_values_df(n, base_year, end_year, grouped)
                else:
                    try:
                        file = by_func(n) + ".csv"
                        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
                    except FileNotFoundError:
                        print("Creating Data")
                        self.year_values_df(n, base_year, end_year, grouped)
            self.bar_chart_grouped_stacked(name, base_year, end_year, grouped)
        return f

    def save_dfs_gsb_charts_all(self, base_year, end_year = None, make_df = True):
        is_grouped = [False]
        cat_mets = self.cat_metrics.loc[lambda df: df['Bar'] == True]
        for (grouped, name) in product(is_grouped, cat_mets['Name']):
            print(name)
            self.save_df_gsb_graph(base_year, end_year, make_df)(name, grouped)

    def make_all_dfs_charts(self, base_year, end_year, make_df):
        self.save_dfs_line_charts_all(base_year, end_year, make_df)
        self.save_dfs_gsb_charts_all(base_year, end_year, make_df)
