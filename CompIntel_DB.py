import pyodbc
import os
import pandas as pd
from functools import reduce

class CompIntel_DB:
    def __init__(self, folder):
        self.folder = folder
        self.schools = (
            "Carroll College",
            "Grand Canyon University",
            "University of Washington-Seattle Campus",
            "Boise State University",
            "Montana State University",
            "University of Idaho",
            "The University of Montana",
            "Gonzaga University",
            "Montana Technological University",
            "Rocky Mountain College",
            "Washington State University"
        )
        self.varmap = pd.read_csv(os.path.join(self.folder, "varmap.csv"), index_col=0)
        self.output_path = "\\".join([os.getcwd(), self.folder, "Data"])
        self.analysis_path = "\\".join([os.getcwd(), "Analysis"])

    def queried_df(self, cursor, query, index_col = False):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
        df = pd.DataFrame(data=data, columns=columns)
        return df.set_index(columns[0]) if index_col else df

    def getSchools(self, year):
        def execute(cursor):
            stmt = f"""
            SELECT UNITID, INSTNM
            FROM HD{year}
            WHERE INSTNM IN {self.schools}
            """
            print(self.queried_df(cursor, stmt))
        return execute

    def academic_year(self, start):
        def f(year):
            return f"{year}-{str(year + 1)[2:]}" if start == "This Fall" else f"{year - 1}-{str(year)[2:]}"
        return f

    def value_df(self, year, name, alias = None):
        table, variable, start = self.varmap.loc[name, :]
        alias = self.academic_year(start)(year) if alias is None else alias
        year_table = table.replace("yyyy", str(year)).replace("xxxx", str(year - 1)[2:] + str(year)[2:])
        def execute(cursor):
            stmt = f"""
            SELECT [HD{year}.INSTNM], [{year_table}].[{variable}] AS [{alias}]
            FROM [HD{year}] INNER JOIN [{year_table}] ON HD{year}.UNITID = {year_table}.UNITID
            WHERE INSTNM IN {self.schools}
            """
            print(100 * "-" + "Executing" + 100 * "-" + "\n" + stmt + "\n" + 2 * 100 * "-")
            df = self.queried_df(cursor, stmt, index_col=True)
            return df
        return execute

    def executeSQL(self, year):
        def execute(commands):
            try:
                database_path = "\\".join(["Q:\\IR\\IPEDS Databases", f"{year}.accdb"])
                conn_str = (
                        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                        r"Dbq=" + database_path + ";"
                )
                connection = pyodbc.connect(conn_str)
                cursor = connection.cursor()
                for command in commands:
                    command(cursor)
                connection.commit()
                cursor.close()
                connection.close()
                print("Connection is closed.")
            except pyodbc.Error as e:
                print("Error:", e)
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
                df = command(cursor)
                cursor.close()
                connection.close()
                print("Connection is closed.")
                return df
            except pyodbc.Error as e:
                print("Error:", e)
        return execute

    #=================================================================================================================


    def x(self, name):
        years = list(range(2018, 2022 + 1))
        tables = [self.readSQL(year)(self.value_df(year, name)) for year in years]
        df = reduce(lambda df1, df2: pd.merge(df1, df2, on='INSTNM'), tables)
        print(df)
        df = df.map(lambda x: x if x == "None" else int(x))
        df.to_csv(os.path.join(self.analysis_path, f"{name}.csv"), index=True)


    def saveInstitutionSize(self, year):
        df = self.readSQL(year)(self.value_df(year, 'Undergraduate Size', year))
        df.to_csv(os.path.join(self.output_path, f"Degree Seeking Undergraduates - {year}.csv"))

    def saveUGEnrollmentChange(self, base_year):
        years = list(range(base_year, 2021 + 1))
        tables = [self.readSQL(year)(self.value_df(year, 'Undergraduate Size', year)) for year in years]
        df = reduce(lambda df1, df2: pd.merge(df1, df2, on='INSTNM'), tables).map(lambda x: int(x))
        df = pd.DataFrame(
            data=[{col: round(df.at[i, col] / df.at[i, str(base_year)] - 1, 2) for col in df.columns} for i in df.index],
            index=df.index
        )
        df.to_csv(os.path.join(self.output_path, f"UG Enrollment Percent Change Since {base_year}.csv"), index=True)

    def saveIncomingFreshmanSize(self, year):
        df = self.readSQL(year)(self.value_df(year, 'Incoming Freshman Size', year))
        df.to_csv(os.path.join(self.output_path, f"Incoming Freshman Class - {year}.csv"), index=True)

    def saveIncomingFreshmanChange(self, base_year):
        start, end = [self.readSQL(year)(
                      self.value_df(year, 'Incoming Freshman Size', year)).map(lambda x: float(x))
                      for year in [base_year, 2021]]
        schools = start.index
        df = pd.DataFrame(
            data=[{'Change': end.at[school, '2021'] / start.at[school, str(base_year)] - 1} for school in schools],
            index=schools
        )
        df.to_csv(os.path.join(self.output_path, f'Change in Freshman Class Size {base_year} to 2021.csv'), index=True)

    def saveFreshmanToTransferRatio(self, year):
        freshman = self.readSQL(year)(self.value_df(year, 'Incoming Freshman Size', year)).map(lambda x: float(x))
        transfer = self.readSQL(year)(self.value_df(year, 'Incoming Transfer Size', year)).map(lambda x: float(x))
        schools = freshman.index
        df = pd.DataFrame(
            data=[{'Ratio': freshman.at[school, str(year)] / transfer.at[school, str(year)]} for school in schools],
            index=schools
        )
        df.to_csv(os.path.join(self.output_path, f'Freshman to Transfer Ratio - {year}.csv'), index=True)

    def saveRacialDiversity(self, year):
        table = self.readSQL(year)(self.value_df(year, 'Percentage of White', year)).map(lambda x: int(x))
        schools = table.index
        df = pd.DataFrame(
            data=[{'White': table.at[school, str(year)], 'Non-White': 100 - table.at[school, str(year)]}
                  for school in schools],
            index=schools
        )
        df.to_csv(os.path.join(self.output_path, f'Percent of White and Non-White - {year}.csv'), index=True)

    def saveGender(self, year):
        table = self.readSQL(year)(self.value_df(year, 'Percentage of Women', year)).map(lambda x: int(x))
        schools = table.index
        df = pd.DataFrame(
            data=[{'Female': table.at[school, str(year)], 'Male': 100 - table.at[school, str(year)]}
                  for school in schools],
            index=schools
        )
        df.to_csv(os.path.join(self.output_path, f'Percent of Students who are Female or Male - {year}.csv'), index=True)

    def savePell(self, base_year):
        start, end = [self.readSQL(year)(
            self.value_df(year, 'Percentage of Pell', year)).map(lambda x: float(x))
                      for year in [base_year, 2021]]
        schools = start.index
        df = pd.DataFrame(
            data=[{f'Percent Change Since {base_year}': end.at[school, '2021'] / start.at[school, str(base_year)] - 1,
                   'Percent Receiving Pell': end.at[school, '2021'] / 100}
                  for school in schools],
            index=schools
        )
        file = f'Percent of 2020-21 Student Body Receiving Pell and Change Since {base_year}.csv'
        df.to_csv(os.path.join(self.output_path, file), index=True)

    def saveRetention(self, base_year, end_year):
        years = list(range(base_year, end_year + 1))
        tables = [self.readSQL(year)(self.value_df(year, 'Retention Rate', year)) for year in years]
        df = reduce(lambda df1, df2: pd.merge(df1, df2, on='INSTNM'), tables).map(lambda x: int(x))
        file = f"Freshman to Sophomore Retention Rates - {base_year} to {end_year}.csv"
        df.to_csv(os.path.join(self.output_path, file), index=True)

    def saveGrad4(self, base_year):
        years = list(range(base_year, 2021 + 1))
        tables = [self.readSQL(year)(self.value_df(year, 'Graduate Rate - 4 Years', year)) for year in years]
        df = reduce(lambda df1, df2: pd.merge(df1, df2, on='INSTNM'), tables).map(lambda x: int(x))
        file = f"4-YR Graduation Rates - {base_year} to 2021.csv"
        df.to_csv(os.path.join(self.output_path, file), index=True)

    def saveGrad6(self, base_year):
        years = list(range(base_year, 2021 + 1))
        tables = [self.readSQL(year)(self.value_df(year, 'Graduate Rate - 6 Years', year)) for year in years]
        df = reduce(lambda df1, df2: pd.merge(df1, df2, on='INSTNM'), tables).map(lambda x: int(x))
        file = f"6-YR Graduation Rates - {base_year} to 2021.csv"
        df.to_csv(os.path.join(self.output_path, file), index=True)

    def savePrice(self, year):
        out_of_state = self.readSQL(year)(self.value_df(year, 'Out-of-State'))
        in_state = self.readSQL(year)(self.value_df(year, 'In-State'))
        df = pd.merge(out_of_state, in_state, on='INSTNM').map(lambda x: int(x))
        file = f"Total Annual Price (Sticker Price) {year}-{str(year + 1)[2:]}.csv"
        df.to_csv(os.path.join(self.output_path, file), index=True)

    def savePriceChange(self, start, end):
        start_df = self.readSQL(start)(self.value_df(start, 'Out-of-State')).map(lambda x: int(x))
        end_df = self.readSQL(end)(self.value_df(end, 'Out-of-State')).map(lambda x: int(x))
        schools = start_df.index
        df = pd.DataFrame(
            data=[{f'Change': end_df.at[school, 'Out-of-State'] / start_df.at[school, 'Out-of-State'] - 1}
                  for school in schools],
            index=schools
        )
        ay_plus = lambda year: f"{year}-{str(year + 1)[2:]}"
        file = f"Percent Change in Total Price (Out-of-State) from {ay_plus(start)} to {ay_plus(end)}.csv"
        df.to_csv(os.path.join(self.output_path, file), index=True)









