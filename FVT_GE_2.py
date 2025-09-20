import os
import pandas as pd
import pyodbc, environ
from pathlib import Path
from tabulate import tabulate
BASE_DIR = Path(__file__).resolve()
from functools import reduce

class FVT_GE_2:
    def __init__(self):
        self.folder = '\\'.join([os.getcwd(), 'FVT_GE_2'])
        self.output = os.path.join(self.folder, 'Output')
        self.given_data = pd.read_csv(os.path.join(self.folder, 'Given Data.csv'))
        self.key_df = pd.read_csv(os.path.join(self.folder, 'Keys.csv'))
        self.joined_data = pd.read_csv(os.path.join(self.folder, 'Joined Data.csv'))
        self.acad_programs = pd.read_csv(os.path.join(self.folder, 'ACAD_PROGRAMS.csv'))
        self.prog_match_df = pd.read_csv(os.path.join(self.folder, 'My Program Matches.csv'))
        self.calc_cols = {
            'L': 'Programmatically Accredited Indicator',
            'M': 'Accrediting Agency Name',
            'N': 'Liberal Arts Bachelor''s Degree Program at Propriety Institution',
            'O': 'Count of Program Graduates who Attempted Licensure Exam',
            'P': 'Count of Program Graduates who Passed Licensure Exam',
            'S': 'Program Prepares Students for Licensure in State of Main Campus',
            'T': 'State Two in MSA of Main Campus',
            'U': 'Program Prepares Students for Licensure in MSA State Two',
            'V': 'State Three in MSA of Main Campus',
            'W': 'Program Prepares Students for Licensure in MSA State Three',
            'X': 'State Four in MSA of Main Campus',
            'Y': 'Program Prepares Students for Licensure in MSA State Four',
            'Z': 'State Five in MSA of Main Campus',
            'AA': 'Program Prepares Students for Licensure in MSA State Five',
            'AB': 'Invalid Flag',
            'AC': 'Error Codes'
        }

    def print_table(self, query):
        df = self.ODS_SQL(query)
        print(tabulate(df.head(1000), headers='keys', tablefmt='psql'))

    def queried_df(self, cursor, query):
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = [["" if x is None else str(x) for x in tuple(y)] for y in cursor.fetchall()]
        return pd.DataFrame(data=data, columns=columns)

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
            environ.Env.read_env(os.path.join(BASE_DIR, "2024FA.env"))
            my_str = (
                f"DRIVER={{{env('ODS_DRIVER')}}};"
                f"SERVER={env('ODS_HOST')};"
                f"DATABASE={env('ODS_NAME')};"
                "Trusted_Connection=yes;"
            )
            connection = pyodbc.connect(my_str)
            cursor = connection.cursor()
            df = self.queried_df(cursor, query)
            return df
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

    def col_string(self, columns, table = None):
        return ",\n".join([f"[{col}]" if table is None else f"{table}.[{col}]" for col in columns])

    def createDF(self, col, query):
        title = self.calc_cols[col]
        print(title)
        df = self.ODS_SQL(query)
        print(tabulate(df.head(1000), headers='keys', tablefmt='psql'))
        df.to_csv(os.path.join(self.output, f'{col}. {title}.csv'), index=False)
        return df

    def big_join(self):
        query = f"""
        SELECT {self.col_string(self.given_data, 'DATA')},
              CASE WHEN [Published Length of Program Measurement] = 'M' THEN CAST([Published Length of Program] AS FLOAT) / 1000
              WHEN [Published Length of Program Measurement] = 'Y' THEN CAST([Published Length of Program] AS FLOAT) / 1000 * 12
              END AS MONTHS,
              ACAD_PROGRAMS_ID,
              ACPG_TITLE,
              ACPG_CMPL_MONTHS,
              ACPG_CIP,
              NULL AS MATCH
        FROM ({self.df_query(self.given_data)}) AS DATA
        CROSS JOIN ({self.df_query(self.acad_programs)}) AS PROGRAMS
        """
        self.print_table(query)
        self.ODS_SQL(query).to_csv(os.path.join(self.folder, 'Big Join.csv'), index=False)

    def match_check(self):
        query = f"""
        SELECT {self.col_string(self.key_df, 'DATA')},
                SUM(CAST(MATCH AS INT)) AS TOTAL_MATCHES
        FROM (
        SELECT {self.col_string(self.key_df.columns, 'DATA')},
        PROG_MATCHES.ACAD_PROGRAMS_ID,
        PROG_MATCHES.MATCH
        FROM ({self.df_query(self.key_df)}) AS DATA
        JOIN ({self.df_query(self.prog_match_df)}) AS PROG_MATCHES
        ON {"\nAND ".join([f"DATA.[{key}] = PROG_MATCHES.[{key}]" for key in ["Program Name", 
                                                                              "Published Length of Program",
                                                                              "Published Length of Program Measurement"]])})
        AS DATA GROUP BY  {self.col_string(self.key_df.columns, 'DATA')}
        ORDER BY TOTAL_MATCHES DESC
        """
        self.print_table(query)

    def create_transformed_data(self):
        query = f"""
        SELECT {self.col_string(self.key_df.columns, 'DATA')},
        PROG_MATCHES.ACAD_PROGRAMS_ID
        FROM ({self.df_query(self.key_df)}) AS DATA
        LEFT JOIN ({self.df_query(self.prog_match_df)}) AS PROG_MATCHES
        ON {"\nAND ".join([f"DATA.[{key}] = PROG_MATCHES.[{key}]" for key in self.key_df.columns])}
        WHERE PROG_MATCHES.MATCH = 1
        """
        self.print_table(query)
        self.ODS_SQL(query).to_csv(os.path.join(self.folder, 'Joined Data.csv'), index=False)


    '''
    'Programmatically Accredited Indicator'
    
    Status: Completed
    '''
    def getColumn_L(self):
        '''
        Indicates whether the program is programmatically accredited.
        Valid values are:
        • ‘Y’ (Yes)
        • ‘N’ (No)
        • Space (N/A)
        '''
        query = f"""
        SELECT {self.col_string(self.key_df.columns)},
                CASE WHEN ACAD_PROGRAMS_ID IN (
                'BSMM.BA',
                'NURS.BS',
                'ANUR.BS',
                'SOWK.MSW'
                ) THEN 'Y' ELSE 'N' END AS L
        FROM ({self.df_query(self.joined_data)}) AS X
        """
        return self.createDF('L', query)


    '''
    'Accrediting Agency Name'
    
    Status: This will be completed by someone else.
    '''
    def getColumn_M(self):
        '''
        The name of the agency that accredits the program.
        '''
        query = f"""
        SELECT {self.col_string(self.key_df.columns)},
                NULL AS M
        FROM ({self.df_query(self.joined_data)}) AS X
        """
        return self.createDF('M', query)

    '''
    'Liberal Arts Bachelor's Degree Program at Proprietary Institution'
    
    Status: Completed
    '''
    def getColumn_N(self):
        '''
        Indicates if the program is a bachelor’s degree program in liberal arts and 1) the institution has been
        regionally accredited since October 2007; 2) the program has been offered by the institution since January 2009;
         and 3) the institution offering the program is a proprietary institution.
        Valid values are:
        • ‘Y’ (Yes)
        • ‘N’ (No)
        • Space (N/A)
        Note: If this field is reported with a ‘Y’, the Credential Level for the program must equal ‘03’ (Bachelor’s degree).
        '''
        query = f"""
        SELECT {self.col_string(self.key_df.columns, 'DATA')},
                CASE WHEN ACPG_ACAD_LEVEL = 'UG' AND ACPG_START_DATE <= '2009-01-01' THEN 'Y' ELSE 'N' END AS N,
                AP.*
        FROM ({self.df_query(self.joined_data)}) AS DATA
        JOIN ODS_ACAD_PROGRAMS AS AP ON DATA.ACAD_PROGRAMS_ID = AP.ACAD_PROGRAMS_ID
        """
        self.print_table(query)
        #return self.createDF('N', query)

    '''
    'Count of Program Graduates who Attempted Licensure Exam'
    
    Status: This will be completed by someone else.
    '''
    def getColumn_O(self):
        '''
        The total number of program graduates who took a licensure exam as most recently reported to the institution’s
        accrediting agency.
        '''
        query = f"""
        SELECT {self.col_string(self.key_df.columns)},
                NULL AS O
        FROM ({self.df_query(self.joined_data)}) AS X
        """
        return self.createDF('O', query)

    '''
    'Count of Program Gradautes who Passed Licensure Exam'
    
    Status: This will be completed by someone else.
    '''
    def getColumn_P(self):
        '''
        The total number of program graduates who passed a licensure exam as most recently reported to the institution’s
         accrediting agency.
        '''
        query = f"""
        SELECT {self.col_string(self.key_df.columns)},
                NULL AS P
        FROM ({self.df_query(self.joined_data)}) AS X
        """
        return self.createDF('P', query)

    '''
    'Program Prepares Students for Licensure in State of Main Campus'
    
    Status: This will be completed by someone else.
    '''
    def getColumn_S(self):
        '''
        Indicates if the program does or does not prepare students for licensure in the state where the main campus is
        located.
        Valid values are:
        • 'Y' (Yes)
        • 'N' (No)
        • 'X' (Not Applicable)
        '''
        query = f"""
        SELECT {self.col_string(self.key_df.columns)},
                NULL AS S
        FROM ({self.df_query(self.joined_data)}) AS X
        """
        return self.createDF('S', query)

    '''
    'State Two in MSA of Main Campus'
    
    Status: This will be completed by someone else.
    '''
    def getColumn_T(self):
        '''
        The second State in the metropolitan statistical area (MSA) in which the main campus is located, if applicable.
        '''
        query = f"""
        SELECT {self.col_string(self.key_df.columns)},
                NULL AS T
        FROM ({self.df_query(self.joined_data)}) AS X
        """
        return self.createDF('T', query)

    '''
    'Program Prepares Students for Licensure in MSA State Two'
    
    Status: In Progress
    '''
    def getColumn_U(self):
        '''
         Indicates if the program does or does not prepare students for licensure in the second State in the MSA of the
         main campus.
        Valid values are:
        • ‘Y’ (Yes)
        • ‘N’ (No)
        • ‘X’ (Not Applicable)
        • ‘Space’ (No State Two in MSA)
        '''
        query = f"""
        SELECT {self.col_string(self.key_df.columns)},
                NULL AS T
        FROM ({self.df_query(self.joined_data)}) AS X
        """
        return self.createDF('U', query)

    '''
    'State Three in MSA of Main Campus'
    
    Status: In Progress
    '''
    def getColumn_V(self):
        '''
        The third State in the metropolitan statistical area (MSA) in which the main campus is located, if applicable.
        '''

    '''
    'Program Prepares Students for Licensure in MSA State Three'
    
    Status: In Progress
    '''
    def getColumn_W(self):
        '''
        Indicates if the program does or does not prepare students for licensure in the third State in the MSA of the
        main campus.
        Valid values are:
        • 'Y' (Yes)
        • 'N' (No)
        • 'X' (Not Applicable)
        • 'Space' (No State Three in MSA)
        '''
        pass

    '''
    'State Four in MSA of Main Campus'
    
    Status: In Progress
    '''
    def getColumn_X(self):
        '''
        The fourth State in the metropolitan statistical area (MSA) in which the main campus is located, if applicable.
        '''

    '''
    'Program Prepares Students for Licensure in MSA State Four'
    
    Status: In Progress
    '''
    def getColumn_Y(self):
        '''
        Indicates if the program does or does not prepare students for licensure in the fourth State in the MSA of the
        main campus.
        Valid values are:
        • ‘Y’ (Yes)
        • ‘N’ (No)
        • ‘X’ (Not Applicable)
        • ‘Space’ (No State Four in MSA)
        '''
        pass

    '''
    'State Five in MSA of Main Campus'
    
    Status: In Progress
    '''
    def getColumn_Z(self):
        '''
        The fifth State in the metropolitan statistical area (MSA) in which the main campus is located, if applicable.
        '''
        pass

    '''
    'Program Prepares Students for Licensure in MSA State Five'
    
    Status: In Progress
    '''
    def getColumn_AA(self):
        '''
        Indicates if the program does or does not prepare students for licensure in the fifth State in the MSA of the
        main campus.
        Valid values are:
        • 'Y' (Yes)
        • 'N' (No)
        • 'X' (Not Applicable)
        • 'Space' (No State Five in the MSA)
        '''
        pass

    '''
    'Invalid Flag'
    
    Status: In Progress
    '''
    def getColumn_AB(self):
        '''
        Flag that indicates if the school is submitting the record to invalidate an existing FVT/GE Record in NSLDS.
        Valid values are:
        • ‘Y’ (Yes)
        • 'N’ (No)
        • Space (No)
        '''
        pass

    '''
    'Error Codes'
    
    Status: In Progress
    '''
    def getColumn_AC(self):
        '''
        Code(s) of error(s) returned to school by NSLDS
        '''
        pass


