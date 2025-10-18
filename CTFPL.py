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
from tabulate import tabulate
from pathlib import Path

class CTFPL:
    def __init__(self):
        self.folder = "CTFPL"
        self.guides = os.path.join(self.folder, "Guides")
        self.varmap = pd.read_csv(os.path.join(self.guides, "varmap.csv"), index_col=0)
        self.metrics = [
            "Endowment Asset Value",
            "12-Month FTE Enrollment",
            "Core Expenses (FASB)",
            "Instruction Expenses Per FTE (FASB)",
            "Academic Support Expenses Per FTE (FASB)",
            "Institutional Support Expenses Per FTE (FASB)",
            "Student Services Expenses Per FTE (FASB)",
        ]
        self.additional_info = [
            "School",
            "Carnegie Classification 2018",
            "Religious Affiliation"
        ]
        self.std = pd.read_csv(os.path.join(self.guides, "STD.csv"))
        self.carroll = pd.read_csv(os.path.join(self.guides, "Carroll Metrics.csv"))
        self.schools = pd.read_csv(os.path.join(self.guides, "Schools.csv"), dtype=str)
        self.distance_df = pd.read_csv(os.path.join(self.guides, "Distance.csv")).astype({"School_ID": "string"})

    def queried_df(self, cursor, query, index_col = False):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        df = pd.DataFrame(data=data, columns=columns)
        return df.set_index(columns[0]) if index_col else df

    def year_table(self, year, table):
        return (table.replace("yyyy", str(year)).replace("xxxx", str(year - 1)[2:] + str(year)[2:])
                .replace("zz", str(year)[2:]))

    def ipeds_table(self, query, year = 2023):
        '''
        :param db: The database I need to connect to.
        :param query: The query used for the database.
        :return: Pandas Dataframe to generate for the query.
        '''
        try:
            database_path = "\\".join(["Q:\\IR\\IPEDS Databases", f"{year}.accdb"])
            conn_str = (
                    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                    r"Dbq=" + database_path + ";"
            )
            connection = pyodbc.connect(conn_str)
            cursor = connection.cursor()
            df = self.queried_df(cursor, query)
            return df
        except pyodbc.Error as e:
            print("Error:", e)
        finally:
            cursor.close()
            connection.close()
            print("Connection Closed")

    def print_table(self, df):
        print(tabulate(df.head(100), headers='keys', tablefmt='psql'))

    def value_df(self, name, year = 2023):
        table, variable = self.varmap.loc[name, ["Table", "Variable"]]
        year_table = self.year_table(year, table)
        query = f"""
        SELECT [{year_table}].UNITID AS [School_ID],
                '{year}' AS YEAR,
                '{name}' AS METRIC_NAME,
                [{year_table}].[{variable}] AS METRIC_VALUE
        FROM [{year_table}]
        """
        df = self.ipeds_table(query, year)
        df["METRIC_VALUE"] = df["METRIC_VALUE"].map(lambda x: np.nan if x in {"None", None} else x)
        return df

    def all_school_metrics(self, year = 2023):
        return pd.concat([self.value_df(name, year) for name in self.metrics])

    def getSchools(self, year = 2023):
        df = pd.concat([self.value_df(name, year) for name in self.additional_info])
        df = df.pivot(index="School_ID", columns = "METRIC_NAME", values = "METRIC_VALUE").reset_index()
        df.to_csv(os.path.join(self.guides, "Schools.csv"), index=False)

    def getSTD_DF(self, year = 2023):
        df = self.all_school_metrics(year)
        agg_df = df.groupby(by="METRIC_NAME").agg(STD = ("METRIC_VALUE", "std"))
        agg_df.to_csv(os.path.join(self.guides, "STD.csv"))

    def get_carroll_metrics(self, year = 2023):
        df = self.all_school_metrics(year).loc[lambda df: df["School_ID"] == "180106"]
        df = df.rename(columns = {"METRIC_VALUE": "Carroll College"})[["METRIC_NAME", "Carroll College"]]
        df.to_csv(os.path.join(self.guides, "Carroll Metrics.csv"), index = False)

    def distance(self, df):
        def f(i):
            metric, carroll, std = [float(v) for v in df.loc[i, ["METRIC_VALUE", "Carroll College", "STD"]]]
            return np.nan if pd.isna(metric) else abs(metric - carroll) / std
        return f

    def get_data(self, year = 2023):
        df = self.all_school_metrics(year)
        df = pd.merge(df, self.std, on = "METRIC_NAME")
        df = pd.merge(df, self.carroll, on = "METRIC_NAME")
        df = pd.merge(df, self.schools, on = "School_ID")
        df["Distance"] = df.index.map(self.distance(df))
        df = df.loc[lambda df: pd.isna(df["Distance"]) == False]
        df.to_csv(os.path.join(self.guides, "Distance.csv"), index = False)

    def number_in_range(self, std_threshold):
        df = self.distance_df.loc[lambda df: df["School"] != "Carroll College"]
        df["In Range"] = df["Distance"].map(lambda x: int(x <= std_threshold))
        agg_df = df.groupby(by="School_ID").agg(Close_Metrics = ("In Range", "sum"))
        return agg_df.loc[lambda df: df["Close_Metrics"] >= 7].shape[0]

    def makeSTDCorrelation(self, start, stop):
        std_thresholds = np.linspace(start, stop, 500)
        my_func = np.vectorize(self.number_in_range)
        school_neighborhood_sizes = my_func(std_thresholds)
        df = pd.DataFrame({"STD Threshold": std_thresholds, "Neighborhood Size": school_neighborhood_sizes})
        plt.figure(figsize = (10, 10))
        plt.axhline(y = 50, color='red', linestyle='--', linewidth = 2, label = "50 Schools")
        plt.axhline(y=500, color='green', linestyle='--', linewidth = 2, label="100 Schools")
        plt.plot(df["STD Threshold"], df["Neighborhood Size"])
        plt.xlabel('Standard Deviation Threshold')
        plt.ylabel('Number of Schools Within STD Threshold From Carroll College For All 7 Metrics')
        plt.title('School Neighborhood Size Distribution')
        plt.grid(True)
        path_folder = Path(os.path.join(self.folder, f"From {start} to {stop}"))
        path_folder.mkdir(parents = True, exist_ok = True)
        df.to_csv(path_folder / f"From {start} to {stop}.csv")
        plt.savefig(path_folder / f"From {start} to {stop}.png")
        plt.show()
        plt.close()

    def getNeighborSchools(self):
        std_threshold = 0.5
        df = self.distance_df
        df["In Range"] = df["Distance"].map(lambda x: int(x <= std_threshold))
        df = df.groupby(by=["School_ID"]).agg(Close_Metrics=("In Range", "sum")).reset_index()
        df["School_ID"] = df["School_ID"].astype(str)
        df = df.loc[lambda df: df["Close_Metrics"] >= 7]
        df = pd.merge(df, self.distance_df, on = "School_ID")[["School_ID", "METRIC_NAME", "METRIC_VALUE"]
                                                              + self.additional_info]
        df.to_csv(os.path.join(self.folder, "Top Schools (0.5 STD).csv"), index = False)
        self.print_table(df)
        pivoted = df.pivot(index=["School_ID"] + self.additional_info,
                           columns="METRIC_NAME", values = "METRIC_VALUE").reset_index()
        pivoted.to_csv(os.path.join(self.folder, "Top Schools (0.5 STD) (Pivoted).csv"), index = False)
        self.print_table(pivoted)



