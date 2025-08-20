import pyodbc
import os
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib import cm
import numpy as np
from matplotlib.patches import Patch, Rectangle
from itertools import product

class IPEDS_DB:
    def __init__(self, folder):
        self.folder = folder
        self.guides = os.path.join(self.folder, "Guides")
        self.varmap = pd.read_csv(os.path.join(self.guides, "varmap.csv"), index_col=0)
        self.data_path = "\\".join([os.getcwd(), self.folder, "Data"])
        self.chart_path = "\\".join([os.getcwd(), self.folder, "Charts"])
        self.schools = pd.read_csv(os.path.join(self.guides, "Schools.csv"), index_col=0)
        self.school_groups = pd.read_csv(os.path.join(self.guides, "School_Groups.csv"))
        self.groups = pd.read_csv(os.path.join(self.guides, "Groups.csv"), index_col=0)
        self.metrics = pd.read_csv(os.path.join(self.guides, "Metrics.csv"))
        self.cat_metrics = pd.read_csv(os.path.join(self.guides, "Categorized Metrics.csv"))
        self.cat_metric_names = pd.read_csv(os.path.join(self.guides, "Categorized Metrics Joined.csv"))
        self.complements = pd.read_csv(os.path.join(self.guides, "Complements.csv"), index_col=0)
        self.sch_abbrev_df = pd.read_csv(os.path.join(self.guides, "School_Abbreviations.csv"), index_col=0)
        self.school_colors_multi = pd.read_csv(os.path.join(self.guides, "School_Colors_Multi.csv"), index_col=[0, 1])
        self.group_colors_multi = pd.read_csv(os.path.join(self.guides, "Group_Colors_Multi.csv"), index_col=[0, 1])

    def color_dict(self, my_df):
        return {i: tuple([x / 255 for x in my_df.loc[i, ['Red', 'Blue', 'Green']]]) for i in my_df.index}

    def queried_df(self, cursor, query, index_col = False):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        df = pd.DataFrame(data=data, columns=columns)
        return df.set_index(columns[0]) if index_col else df

    def value_df(self, name):
        table, variable, start = self.varmap.loc[name, :]
        def execute(year, cursor):
            year_table = (table
                          .replace("yyyy", str(year))
                          .replace("xxxx", str(year - 1)[2:] + str(year)[2:])
                          .replace("zz", str(year)[2:]))
            stmt = f"""
            SELECT [{year_table}].UNITID AS School_ID,
                    '{year}' AS Year,
                    [{year_table}].[{variable}] AS [{name}]
            FROM [{year_table}]
            WHERE [{year_table}].UNITID IN ({",\n".join([f"{sch_id}" for sch_id in self.schools.index])})
            """
            print(100 * "-" + "Executing" + 100 * "-" + "\n" + stmt + "\n" + 2 * 100 * "-")
            try:
                df = self.queried_df(cursor, stmt, index_col=True)
                return df
            except Exception as e:
                stmt = f"""
                SELECT [{year_table}].UNITID AS School_ID,
                        '{year}' AS Year,
                        [{year_table}].[{variable}] AS [{name}]
                FROM [{year_table}]
                WHERE [{year_table}].UNITID IN ({",\n".join([f"{sch_id}" for sch_id in self.schools.index])})
                """
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

    def title_with_grouping(self, grouped):
        def f(title):
            return title + " - Peer Grouping Average" if grouped else title
        return f

    def year_values_df(self, name, base_year, end_year, grouped = True):
        years = list(range(base_year, end_year + 1))
        tables = [self.readSQL(year)(self.value_df(name)) for year in years]
        df = pd.concat(tables)
        df[name] = df[name].map(lambda x: None if pd.isna(x) or x in [None, "None", "", "0", 0] else int(x))
        df.index, self.schools.index  = df.index.astype(str), self.schools.index.astype(str)
        df = pd.merge(df, self.schools, left_on = "School_ID", right_on = "IPEDS_ID").loc[:, ["School", "Year", name]]
        if grouped:
            df = pd.merge(self.school_groups, df, on="School").groupby(["Group", "Year"])[name].mean().map(lambda x: round(x, 2))
        df = df.reset_index()
        title = self.title_with_grouping(grouped)(f"{name} ({base_year}-{end_year})")
        print(f"Saving {title}")
        df.to_csv(os.path.join(self.data_path, f"{title}.csv"), index=True)

    def remove_boundaries(self, *axes):
        if len(axes) == 0:
            axes = [plt.gca()]
        for ax in axes:
            for boundary in ["top", "bottom", "left", "right"]:
                ax.spines[boundary].set_visible(False)

    def get_metrics(self, cat_metric):
        guide = self.cat_metric_names.merge(self.cat_metrics, left_on='Categorized Metric', right_on='Name')
        guide = guide.loc[lambda df: df['Categorized Metric'] == cat_metric].set_index('Name_x')
        category = list(guide['Category'])[0]
        complement = list(guide['Complement'])[0]
        names = guide.index
        types = [guide.at[n, 'Type'] for n in names]
        return names, types, category, complement

    def df_agg(self, names, types, category, complement, base_year, end_year, grouped):
        def f(n, t):
            file = self.title_with_grouping(grouped)(f"{n} ({base_year}-{end_year})") + ".csv"
            df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
            df = df.rename(columns={n: 'Value', 'School': 'Group'})
            df[category] = len(df.index) * [t]
            return df
        df = pd.concat([f(n, t) for n, t in zip(names, types)])
        if complement:
            comp_df = df.groupby(by=['Year', 'Group'])['Value'].agg(lambda x: 100 - x.sum()).reset_index()
            comp_df[category] = len(comp_df.index) * [self.complements.at[category, 'Complement']]
            df = pd.concat([df, comp_df])
        return df

    def make_diag_marks(self, ax1, ax2):
        kwargs_1 = {'marker': [(-1, -1), (1, 1)], 'markersize': 10, 'linestyle':'none', 'color':'k'}
        kwargs_2 = {'mec':'k', 'mew':1, 'clip_on':False}
        kwargs = kwargs_1 | kwargs_2
        ax1.plot([0, 1], [1, 1], transform=ax1.transAxes, **kwargs)
        ax2.plot([0, 1], [0, 0], transform=ax2.transAxes, **kwargs)

    def make_dashed_lines(self, ax1, ax2):
        ax2.plot([0, 1], [0, 0], transform=ax2.transAxes, color='black', linewidth=2, linestyle='--', clip_on=False)
        ax1.plot([0, 1], [1, 1], transform=ax1.transAxes, color='black', linewidth=2, linestyle='--', clip_on=False)

    def make_gray_rectangle(self, fig, ax1, ax2):
        bbox_ax1, bbox_ax2 = ax1.get_position(), ax2.get_position()
        x0, x1 = bbox_ax2.x0, bbox_ax2.x1
        y0 = bbox_ax1.y1
        height = bbox_ax2.y0 - bbox_ax1.y1
        rec = Rectangle((x0, y0), x1 - x0, height, transform=fig.transFigure,color='lightgray',alpha=0.5,zorder=0)
        fig.patches.append(rec)

    def line_graph(self, name, grouped, make_df, lines = None, cat_metric = False):
        color_dict = self.color_dict(self.group_colors_multi if grouped else self.school_colors_multi)
        if not cat_metric:
            meta_data = self.metrics.loc[lambda df: df['Name'] == name].iloc[0, :]
            base_year, end_year = meta_data['Base Year'], meta_data['End Year']
            title = self.title_with_grouping(grouped)(f"{name} ({base_year}-{end_year})")
            percent = meta_data['Percent']
            self.check_dfs([name], base_year, end_year, grouped, make_df)
            df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", title + ".csv"]), index_col=0)
            pivot_by = 'Group' if grouped else 'School'
            values_col = name
            first_group = df[pivot_by].iloc[0]
            color_func = lambda group: color_dict[(group, 0)]
        else:
            meta_data = self.cat_metrics.loc[lambda df: df['Name'] == name].iloc[0, :]
            base_year, end_year = meta_data['Base Year'], meta_data['End Year']
            title = self.title_with_grouping(grouped)(f"{name} ({base_year}-{end_year})")
            percent = meta_data['Percent']
            names, types, category, complement = self.get_metrics(name)
            self.check_dfs(names, base_year, end_year, grouped, make_df)
            df = self.df_agg(names, types, category, complement, base_year, end_year, grouped)
            pivot_by = category
            values_col = 'Value'
            type_dict = {type: i for i, type in enumerate(types)}
            first_group = df['Group'].iloc[0]
            color_func = lambda type: color_dict[(first_group, type_dict[type])]
        df = df.pivot(index='Year', columns=pivot_by, values=values_col)
        df = df.reindex(columns=self.groups.index) if grouped else df
        df = df.map(lambda x: round(x / 100, 4)) if percent else df
        #---
        lines = list(range(len(df.columns))) if lines is None else lines
        df = df.iloc[:, lines]
        #---
        my_max = 1.1 * np.nanmax(df)
        if grouped:
            begin_break, end_break = meta_data['Begin Break (for groups)'], meta_data['End Break (for groups)']
        else:
            begin_break, end_break = meta_data['Begin Break (for schools)'], meta_data['End Break (for schools)']
        if pd.isna(begin_break):
            lims = [(0- 0.001, my_max)]
            extra_args = {}
        else:
            lims = [(end_break, my_max), (0 - 0.001, begin_break)]
            extra_args = {'gridspec_kw': {'height_ratios': [lim[1] - lim[0] for lim in lims]}}
        args = {'nrows': len(lims), 'ncols': 1, 'sharex': True, 'figsize': (16, 9), 'squeeze': False}
        fig, axes = plt.subplots(**args, **extra_args)
        axes = axes.ravel()
        fig.subplots_adjust(left=0.3, hspace=0.1, top=0.85)
        for ax, lim in zip(axes, lims):
            ax.set_ylim(*lim)
        for ax in axes:
            for col in df.columns:
                z = int(col == "Carroll College")
                df[col].plot(kind="line", color='black', figsize=(16, 9), linewidth=4, ax=ax, zorder=z)
                df[col].plot(kind="line", color=color_func(col), figsize=(16, 9), linewidth=3, ax=ax, zorder=z)
            ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0)) if percent else None
            ax.grid(axis="y", linestyle="--")
            ax.set_xlabel("")
        self.remove_boundaries(*axes)
        plt.tick_params(axis='both', labelsize=12)
        fig.text(0.6, 0.04, "Year", ha='center', fontsize=14)
        fig.text(0.25, 0.5, "Student Count", va="center", rotation="vertical", fontsize=14) if not percent else None
        plt.tick_params(axis='both', labelsize=12)
        colors = [color_func(col) for col in df.columns]
        if len(df.columns) > 1:
            leg_elems = [Patch(facecolor=colors[i], label=df.columns[i]) for i in range(len(df.columns))]
            fig.legend(handles=leg_elems, title=pivot_by, loc='upper left', bbox_to_anchor=(0, 1), borderaxespad=0.)
        else:
            plt.legend().remove()
        title = f"{first_group} {title}" if (len(df.columns) == 1 or cat_metric) else title
        wrapped_title = "\n".join(title.split(" - "))
        plt.suptitle(wrapped_title, fontsize=20)
        if not pd.isna(begin_break):
            (ax2, ax1) = axes
            self.make_diag_marks(ax1, ax2)
            self.make_dashed_lines(ax1, ax2)
            self.make_gray_rectangle(fig, ax1, ax2)
        by_path = ['By Peer Grouping'] if grouped else ['By School']
        path = [self.chart_path, 'Line Charts'] + by_path + [title + ".png"]
        plt.savefig(os.path.join(*path), dpi=300)
        plt.show()
        plt.close()

    def filter_and_sort(self, df, groups, years):
        def f(i, j):
            return df.loc[(df['Group'] == groups[i]) & (df['Year'] == years[j])].sort_values(by='Value').reset_index()
        return f

    def bar_chart_grouped_stacked(self, name, grouped = True, make_df = True):
        color_dict = self.color_dict(self.group_colors_multi if grouped else self.school_colors_multi)
        meta_data = self.cat_metrics.loc[lambda df: df['Name'] == name].iloc[0]
        category, percent, pie, base_year, end_year = meta_data[['Category', 'Percent', 'Pie', 'Base Year', 'End Year']]
        title = self.title_with_grouping(grouped)(f"{name} ({base_year}-{end_year})")
        names, types, category, complement = self.get_metrics(name)
        self.check_dfs(names, base_year, end_year, grouped, make_df)
        df = self.df_agg(names, types, category, complement, base_year, end_year, grouped)
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
        my_max = 1 if pie else np.nanmax(df['Value'])
        if grouped:
            begin_break, end_break = meta_data['Begin Break (for groups)'], meta_data['End Break (for groups)']
        else:
            begin_break, end_break = meta_data['Begin Break (for schools)'], meta_data['End Break (for schools)']
        if pd.isna(begin_break):
            lims = [(0- 0.001, my_max)]
            extra_args = {}
        else:
            lims = [(end_break, my_max), (0 - 0.001, begin_break)]
            extra_args = {'gridspec_kw': {'height_ratios': [lim[1] - lim[0] for lim in lims]}}
        args = {'nrows': len(lims), 'ncols': 1, 'sharex': True, 'figsize': (16, 9), 'squeeze': False}
        fig, axes = plt.subplots(**args, **extra_args)
        axes = axes.ravel()
        fig.subplots_adjust(left=0.4, hspace=0.05, top=0.85)
        self.remove_boundaries(*axes)
        #--------------------------
        for ax, lim in zip(axes, lims):
            ax.set_ylim(*lim)
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
                        for ax in axes:
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
                        for ax in axes:
                            ax.bar(**args)
                        bottom = df_part.at[k, 'Value']
        labels = groups if grouped else [self.sch_abbrev_df.at[school, 'Abbreviation'] for school in groups]
        fig.text(0.35, 0.5, "Student Count", va="center", rotation="vertical", fontsize=14) if not percent else None
        if len(groups) > 1:
            label_positions = np.arange(0, num_groups, 1) + group_width / 2
            for ax in axes:
                ax.set_xticks(label_positions)
                ax.set_xticklabels(labels, rotation=0, fontsize=12)
            fig.text(0.6, 0.04, f"Schools Chronologically ({base_year}-{end_year})", ha='center',
                     fontsize=14) if not grouped else None
        else:
            title = f"{groups[0]} {title}"
            for ax in axes:
                ax.set_xticks(x_positions)
                ax.set_xticklabels(years)
        wrapped_title = "\n".join(title.split(" - "))
        plt.suptitle(wrapped_title, fontsize=20)
        for ax in axes:
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.set_xlabel("")
            ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0)) if percent else None
        str_func = lambda x, t: f"{x} - {t}" if grouped else f"{x} ({self.sch_abbrev_df.at[x, "Abbreviation"]}) - {t}"
        leg_labels = [str_func(x, type) for (x, type) in product(groups, types)]
        leg_colors = reduce(lambda x, y: x + y, [[color_dict[(j, i)] for i in range(len(types))] for j in groups])
        leg_elems = [Patch(facecolor=color, label=leg_label) for color, leg_label in zip(leg_colors, leg_labels)]
        fig.legend(handles=leg_elems, title=category, loc='upper left', bbox_to_anchor=(0, 1), borderaxespad=0.)
        if not pd.isna(begin_break):
            ax2, ax1 = axes
            self.make_diag_marks(ax1, ax2)
            self.make_dashed_lines(ax1, ax2)
            self.make_gray_rectangle(fig, ax1, ax2)
        by_path = ['By Peer Grouping'] if grouped else ['By School']
        path = [self.chart_path, 'Grouped, Stacked Bar Charts'] + by_path + [title + ".png"]
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
            plt.legend(legend_labels, loc='center left', bbox_to_anchor=(-0.3, 0.5),
                       title=title.partition(" Percentage")[0])
            group_title = title + f" ({group})"
            plt.title(group_title, fontsize=18)
            plt.tight_layout()
            plt.savefig(os.path.join(self.chart_path, title, group_title + ".png"), bbox_inches='tight')
            plt.show()
            plt.close()

    def check_dfs(self, names, base_year, end_year, grouped, make):
        if make:
            for name in names:
                self.year_values_df(name, base_year, end_year=end_year, grouped=grouped)
        else:
            for name in names:
                try:
                    file = self.title_with_grouping(grouped)(f"{name} ({base_year}-{end_year})") + ".csv"
                    df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
                except FileNotFoundError:
                    print(f"Creating {name}")
                    self.year_values_df(name, base_year, end_year, grouped)

    def save_dfs_line_charts_all(self, make_df = True, is_grouped = (False, True)):
        names = self.metrics.loc[lambda df: df['Line'] == True]['Name']
        for (grouped, name) in product(is_grouped, names):
            self.line_graph(name, grouped, make_df=make_df, cat_metric=False)
        names = self.cat_metrics.loc[lambda df: df['Line'] == True]['Name']
        for (grouped, name) in product(is_grouped, names):
            self.line_graph(name, grouped, make_df=make_df, cat_metric=True)

    def save_dfs_gsb_charts_all(self, make_df = True, is_grouped = (False, True)):
        cat_mets = self.cat_metrics.loc[lambda df: df['Bar'] == True]
        for (grouped, name) in product(is_grouped, cat_mets['Name']):
            self.bar_chart_grouped_stacked(name, grouped, make_df)

    def make_all_dfs_charts(self, make_df):
        self.save_dfs_line_charts_all(make_df)
        self.save_dfs_gsb_charts_all(make_df)
















