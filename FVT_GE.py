import os
import pandas as pd
import pyodbc, environ
from pathlib import Path
from tabulate import tabulate
BASE_DIR = Path(__file__).resolve()

class FVT_GE:
    def __init__(self):
        self.folder = '\\'.join([os.getcwd(), 'FVT_GE'])
        self.given_data = pd.read_csv(os.path.join(self.folder, 'Given Data.csv'))
        self.key_df = pd.read_csv(os.path.join(self.folder, 'Keys.csv'))
        self.keys = ['Record Type', 'College Student ID', 'CIP Code', 'Credential Level']
        self.cred_df = pd.read_csv(os.path.join(self.folder, 'Credential Levels.csv'))
        self.cip_df = pd.read_csv(os.path.join(self.folder, 'CIP.csv'))
        self.prog_df = pd.read_csv(os.path.join(self.folder, 'ACAD_PROGRAMS.csv'))

    def print_table(self, query):
        df = self.ODS_SQL(query)
        print(tabulate(df, headers='keys', tablefmt='psql'))

    def queried_df(self, cursor, query):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [["" if x is None else str(x) for x in tuple(y)] for y in cursor.fetchall()]
        return pd.DataFrame(data=data, columns=columns)

    def df_query_2(self, df, cols = None):
        cols = df.columns if cols is None else cols
        trans_dict = {" ": "_"} | {c: "" for c in ":()"}
        query = f"""
        SELECT *
        FROM (VALUES {",\n".join([f"({", ".join([f"'{str(val).replace("'", "''")}'" for val in df.loc[i, cols]])})"
                                  for i in df.index])})
        AS DF({", ".join([str(col).translate(str.maketrans(trans_dict)) for col in cols])})
        """.replace("'nan'", "NULL")
        return query

    def df_query(self, df, cols=None):
        cols = df.columns if cols is None else cols
        query = f"""
        SELECT *
        FROM (VALUES {",\n".join([f"({", ".join([f"'{str(val).replace("'", "''")}'" for val in df.loc[i, cols]])})"
                                  for i in df.index])})
        AS DF({", ".join([f'[{col}]' for col in cols])})
        """.replace("'nan'", "NULL")
        return query

    def ODS_SQL(self, query):
        try:
            env = environ.Env()
            environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
            my_str = (
                f"DRIVER={{{env('ODS_DRIVER')}}};"
                f"SERVER={env('ODS_HOST')};"
                f"DATABASE={env('ODS_NAME')};"
                "Trusted_Connection=yes;"
            )
            connection = pyodbc.connect(my_str)
            cursor = connection.cursor()
            return self.queried_df(cursor, query)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
            print("MSSQL Connection Closed")

    def student_count(self, query, name = 'College Student ID'):
        new_query = f"""
        SELECT COUNT(DISTINCT [{name}]) AS STUDENT_COUNT FROM ({query}) AS X
        """
        return self.ODS_SQL(new_query).iat[0, 0]

    def order_by(self, query, name):
        new_query = f"""
        SELECT * FROM ({query}) AS X ORDER BY [{name}]
        """
        return new_query

##======================================================================================================================
#----------Find Primary Key---------------------------------------------------------------------------------------------
    def col_string(self, columns, table = None):
        table_str = "" if table is None else table + "."
        return ",\n".join([f"{table_str}[{col}]" for col in columns])

    def col_count(self, columns):
        query = f"""
        SELECT {self.col_string(columns)},
        COUNT(*) AS COL_COUNT
        FROM ({self.df_query(self.given_data)}) 
        AS X GROUP BY {self.col_string(columns)}
        ORDER BY COL_COUNT DESC
        """
        print(query)
        self.print(self.ODS_SQL(query))

    def col_count_check(self, i):
        if i == 1:
            columns = ['College Student ID']
            self.col_count(columns)
        if i == 2:
            columns = ['College Student ID', 'CIP Code']
            self.col_count(columns)
        if i == 3:
            columns = ['Record Type', 'College Student ID', 'CIP Code']
            self.col_count(columns)
        if i == 4:
            columns = ['Record Type', 'College Student ID', 'CIP Code', 'Credential Level']
            self.col_count(columns)

    def save_keys(self):
        columns = ['Record Type', 'College Student ID', 'CIP Code', 'Credential Level']
        query = self.df_query(self.given_data, columns)
        print(query)
        df = self.ODS_SQL(query)
        df.to_csv(os.path.join(self.folder, 'Keys.csv'), index=False)

    #------------------------------------------------------------------------------------------------------------------

    def big_join(self):
        query_1 = f"""
        SELECT {self.col_string(self.given_data.columns, 'DATA')},
        CIP_DESC,
        CIP_PROGRAMS.ACAD_PROGRAMS_ID AS CIP_PROGRAM_ID,
        CIP_PROGRAMS.ACPG_TITLE AS CIP_PROGRAM_TITLE,
        CRED.[Acad Level],
        SP.[STPR_ACAD_PROGRAM],
        AP.[ACPG_TITLE],
        SP.[START_DATE],
        SP.[END_DATE],
        AP.[ACPG_ACAD_LEVEL]
        FROM ({self.df_query(self.given_data)}) AS DATA
        JOIN ({self.df_query(self.cip_df)}) AS CIP 
        ON LEFT(DATA.[CIP Code], 2) + '.' + SUBSTRING(DATA.[CIP Code], 3, 4) = CIP.CIP_ID
        JOIN ({self.df_query(self.prog_df)}) AS CIP_PROGRAMS ON ACPG_CIP = CIP.CIP_ID
        JOIN ({self.df_query(self.cred_df)}) AS CRED ON DATA.[Credential Level] = CRED.[Credential Level]
        JOIN SPT_STUDENT_PROGRAMS AS SP ON DATA.[College Student ID] = SP.STPR_STUDENT
        JOIN ODS_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
        """
        query_2 = f"""
        SELECT {self.col_string(self.given_data.columns, 'DATA')},
        CIP_DESC,
        CRED.[Acad Level],
        SP.[STUDENT_PROGRAMS_ID],
        SP.[STPR_ACAD_PROGRAM],
        AP.[ACPG_TITLE],
        SP.[START_DATE],
        SP.[END_DATE],
        AP.[ACPG_ACAD_LEVEL],
        NULL AS PROGRAM_MATCH
        FROM ({self.df_query(self.given_data)}) AS DATA
        LEFT JOIN ({self.df_query(self.cip_df)}) AS CIP 
        ON LEFT(DATA.[CIP Code], 2) + '.' + SUBSTRING(DATA.[CIP Code], 3, 4) = CIP.CIP_ID
        LEFT JOIN ({self.df_query(self.cred_df)}) AS CRED ON DATA.[Credential Level] = CRED.[Credential Level]
        LEFT JOIN SPT_STUDENT_PROGRAMS AS SP ON DATA.[College Student ID] = SP.STPR_STUDENT
        LEFT JOIN ODS_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
        ORDER BY [Record Type], [College Student ID], [CIP Code]
        """
        self.print_table(query_2)
        self.ODS_SQL(query_2).to_csv(os.path.join(self.folder, 'Big Join.csv'), index=False)


    #------------------------------------------------------------------------------------------------------------------
    def getColumn_N(self):
        '''
        Flag to indicate if the program is a Comprehensive Transition and Postsecondary (CTP) Program.

        Valid values are:
        - Y: Yes
        - N: No
        - Space: No
        '''
        title = 'Comprehensive Transition and Postsecondary (CTP) Program Indicator'
        query = f"""
        SELECT {self.col_string(self.keys)},
                CASE WHEN [Record Type] = 'TA' THEN 'N' 
                END AS [{title}]
        FROM ({self.df_query(self.key_df)}) AS X
        """
        self.ODS_SQL(query).to_csv(os.path.join(self.folder, f'N. {title}.csv'), index=False)

    def getColumn_O(self):
        '''
        Flag to indicate if the program is an Approved Prison Program.

        Valid values are:
        - Y: Yes
        - N: No
        - Space: No
        '''
        title = 'Approved Prison Education Program Indicator'
        query = f"""
        SELECT {self.col_string(self.keys)},
                CASE WHEN [Record Type] = 'TA' THEN 'N' 
                END AS [{title}]
        FROM ({self.df_query(self.key_df)}) AS X
        """
        self.ODS_SQL(query).to_csv(os.path.join(self.folder, f'O. {title}.csv'), index=False)

    def getColumn_Q(self):
        '''
        For GE Programs, the total amount of private education loans the student received for enrollment in the program.

        For eligible non-GE programs, the total amount of private education loans the student received for enrollment
        in all eligible non-GE programs at the same credential level at the institution.

        If the student did not received any private educational loans, enter a zero or all zeros. Value must be
        numeric and 0-9.

        Total amount is required unless one of the following conditions is met:
        - Program is flagged as CTP.
        - Program is flagged as Prison Education.
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
        query_1 = f"""
        SELECT {self.col_string(self.keys, 'DATA')},
                CRED.[Acad Level],
                SP.[STPR_ACAD_PROGRAM],
                AP.[ACPG_TITLE],
                SP.[START_DATE],
                SP.[END_DATE],
                AP.[ACPG_ACAD_LEVEL]
        FROM ({self.df_query(self.key_df)}) AS DATA
        JOIN ({self.df_query(self.cred_df)}) AS CRED ON DATA.[Credential Level] = CRED.[Credential Level]
        JOIN SPT_STUDENT_PROGRAMS AS SP ON DATA.[College Student ID] = SP.STPR_STUDENT
        JOIN ODS_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
        WHERE (
        START_DATE <= '2025-05-19'
        AND COALESCE(END_DATE, GETDATE()) >= '2024-08-09'
        ) OR (
        
        )
        """
        query_2 = f"""
        SELECT [College Student ID],
                MAX(COALESCE(END_DATE, GETDATE())) AS MAX_END_DATE,
                MIN(START_DATE) AS MIN_START_DATE
        FROM (
        SELECT {self.col_string(self.keys, 'DATA')},
                CRED.[Acad Level],
                SP.[STPR_ACAD_PROGRAM],
                AP.[ACPG_TITLE],
                SP.[START_DATE],
                SP.[END_DATE],
                AP.[ACPG_ACAD_LEVEL]
        FROM ({self.df_query(self.key_df)}) AS DATA
        JOIN ({self.df_query(self.cred_df)}) AS CRED ON DATA.[Credential Level] = CRED.[Credential Level]
        JOIN SPT_STUDENT_PROGRAMS AS SP ON DATA.[College Student ID] = SP.STPR_STUDENT
        JOIN ODS_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
        ) AS X
        GROUP BY [College Student ID]
        """
        query_3 = f"""
        SELECT {self.col_string(self.keys, 'DATA')},
                CRED.[Acad Level]
        FROM ({self.df_query(self.key_df)}) AS DATA
        JOIN ({self.df_query(self.cred_df)}) AS CRED ON DATA.[Credential Level] = CRED.[Credential Level]
        """

        print(self.student_count(query_1))
        print(self.student_count(query_2))
        print(self.student_count(query_3))
        self.print(self.ODS_SQL(self.order_by(query_2, 'MIN_START_DATE')))

    def getColumn(self, col):
        if col == 'N': self.getColumn_N()
        if col == 'O': self.getColumn_O()
        if col == 'Q': self.getColumn_Q()




