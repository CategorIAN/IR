import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, FuncFormatter
import numpy as np
from textwrap import wrap
from matplotlib import cm


class DV:
    def __init__(self, folder):
        self.folder = folder
        self.output_path = "\\".join([os.getcwd(), self.folder, "Charts"])
        #self.abbrev = pd.read_csv("\\".join([os.getcwd(), self.folder, "Abbreviations.csv"]), index_col=0).iloc[:,0]


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
        if len(df.index) > 5:
            params = {"y": df.columns[0], "legend": True, "labels": None}
            label_length = 5
        else:
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
