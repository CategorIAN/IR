import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, FuncFormatter
import numpy as np
from textwrap import wrap

class CompIntel_DV:
    def __init__(self, folder):
        self.folder = folder
        self.output_path = "\\".join([os.getcwd(), self.folder, "Charts"])
        self.abbrev = pd.read_csv("\\".join([os.getcwd(), self.folder, "Abbreviations.csv"]), index_col=0).iloc[:,0]

    def print_latex(self, x):
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", x]))
        column_format = "c".join((df.shape[1] + 1) * ["|"])
        latex = df.to_latex(index=False, column_format=column_format)
        latex = latex.replace("%", "\%").replace("#", "\#")
        print(latex)

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
        df = df.sort_values(by=target, ascending=True)
        df.plot(kind="bar", legend=False)
        plt.gca().set_xlabel("")
        plt.gca().set_ylabel("")
        plt.gca().yaxis.set_visible(False)
        display = lambda v: str(int(100 * v)) + "%" if percent else str(round(v, 1))
        for i, v in enumerate(df[target]):
            plt.text(i, v + v / abs(v) * .08 * max(df[target]), display(v), va='center', ha='center')
        self.remove_boundaries()
        plt.gca().set_title(title, fontsize=18)
        plt.ylim(min(df[target]) - .1 * max(df[target]), max(df[target]) + .08 * max(df[target]))
        plt.gca().tick_params(axis='both', labelsize=6)
        plt.xticks(rotation=10, ha='right')
        plt.savefig(os.path.join(self.output_path, title + ".png"))
        plt.show()

    def bar_chart_grouped(self, file, title = None, colors = plt.cm.tab10.colors, money=False):
        title = file.strip(".csv") if title is None else title
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        df = df.sort_values(by=df.columns[-1])
        num_groups = len(df.index)
        num_bars = len(df.columns)
        bar_width = 0.8 / num_bars
        x_positions = np.arange(num_groups)
        colors = colors[:num_bars]
        plt.figure(figsize=(10, 6))
        self.remove_boundaries()
        display = lambda v: "" if pd.isna(v) else f"${round(v / 1000)}k" if money else str(v)
        for i in range(num_bars):
            bar_positions = x_positions + i * bar_width
            plt.bar(bar_positions, df.loc[:, df.columns[i]], width=bar_width, color=colors[i], label=df.columns[i])
            if i in {0, num_bars - 1}:
                for j, v in zip(bar_positions, df[df.columns[i]]):
                    plt.text(j, v + v / abs(v) * 0.1, display(v), ha='center', fontsize=10)
        labels = [self.abbrev[df.index[i]] for i in range(num_groups)]
        plt.xticks(x_positions + bar_width * (num_bars - 1) / 2, labels)
        plt.gca().yaxis.set_visible(False)
        plt.gca().set_title(title, fontsize=18)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig(os.path.join(self.output_path, title + ".png"))
        plt.show()

    def bar_chart_stacked(self, file, title = None, colors = plt.cm.tab10.colors, text_colors = None):
        title = file.strip(".csv") if title is None else title
        text_colors = len(colors) * ['black'] if text_colors is None else text_colors
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        df = df.sort_values(by=df.columns[0], ascending=True)
        matrix = df.to_numpy()
        groups = df.index
        bottoms = np.zeros(matrix.shape[0])
        for i in range(matrix.shape[1]):
            params = {"x": groups, "height": matrix[:, i], "color": colors[i], "bottom": bottoms, "label": df.columns[i]}
            plt.bar(**params)
            for j in range(matrix.shape[0]):
                plt.text(j, bottoms[j] + matrix[j, i] / 2, str(matrix[j, i]), ha='center', va='center', color=text_colors[i])
            bottoms += matrix[:, i]
        plt.gca().yaxis.set_visible(False)
        self.remove_boundaries()
        plt.gca().set_title(title, fontsize=18)
        plt.gca().tick_params(axis='both', labelsize=6)
        plt.xticks(rotation=10, ha='right')
        plt.legend()
        plt.savefig(os.path.join(self.output_path, title + ".png"))
        plt.show()

    def line_graph(self, file, title = None, percent = False):
        title = file.strip(".csv") if title is None else title
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        df = df.transpose()
        plt.figure(figsize=(8, 4))
        df.plot(kind="line")
        self.remove_boundaries()
        if percent:
            plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        plt.gca().set_title(title, fontsize=18)
        plt.tight_layout()
        plt.tick_params(axis='both', labelsize=12)
        plt.grid(axis="y", linestyle="--")
        plt.savefig(os.path.join(self.output_path, title + ".png"))
        plt.show()

    def scatter(self, file, title = None, percent = False):
        title = file.strip(".csv") if title is None else title
        df = pd.read_csv("\\".join([os.getcwd(), self.folder, "Data", file]), index_col=0)
        plt.scatter(df.iloc[:, 0], df.iloc[:, 1], color='blue', marker='o')
        for i in range(len(df)):
            args = {
                "text": self.abbrev[df.index[i]],
                'xy': (df.iat[i, 0], df.iat[i, 1]),
                'xytext': (5, 5),
                'textcoords': 'offset points',
                'ha': 'center'
            }
            plt.annotate(**args)
        if percent:
            plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{round(x * 100)}%"))
            plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{round(x * 100)}%"))
        plt.grid(linestyle="--")
        plt.ylim(bottom=0)
        plt.gca().set_title(title, fontsize=18)
        plt.xlabel(df.columns[0])
        plt.ylabel(df.columns[1])
        plt.savefig(os.path.join(self.output_path, title + ".png"))
        plt.show()


