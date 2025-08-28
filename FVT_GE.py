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
        self.cred_df = pd.read_csv(os.path.join(self.folder, 'Credential Levels.csv'))
        self.cip_df = pd.read_csv(os.path.join(self.folder, 'CIP.csv'))
        self.prog_df = pd.read_csv(os.path.join(self.folder, 'ACAD_PROGRAMS.csv'))
        self.prog_match_df = pd.read_csv(os.path.join(self.folder, 'My Program Matches.csv'))
        self.joined_data = pd.read_csv(os.path.join(self.folder, 'Joined Data.csv'))

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

    def order_by(self, *names):
        def f(query):
            return f"""
            SELECT * FROM ({query}) AS X ORDER BY {self.col_string(names)}
            """
        return f

##======================================================================================================================
#----------Find Primary Key---------------------------------------------------------------------------------------------
    def col_string(self, columns, table = None):
        return ",\n".join([f"[{col}]" if table is None else f"{table}.[{col}]" for col in columns])

    def col_count(self, columns):
        query = f"""
        SELECT {self.col_string(columns)},
        COUNT(*) AS COL_COUNT
        FROM ({self.df_query(self.given_data)}) 
        AS X GROUP BY {self.col_string(columns)}
        ORDER BY COL_COUNT DESC
        """
        self.print_table(query)

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

    def match_check(self):
        query = f"""
        SELECT {self.col_string(self.key_df.columns, 'DATA')},
                SUM(CAST(PROGRAM_MATCH AS INT)) AS TOTAL_MATCHES
        FROM (
        SELECT {self.col_string(self.key_df.columns, 'DATA')},
        PROG_MATCHES.STUDENT_PROGRAMS_ID,
        PROG_MATCHES.PROGRAM_MATCH
        FROM ({self.df_query(self.key_df)}) AS DATA
        JOIN ({self.df_query(self.prog_match_df)}) AS PROG_MATCHES
        ON DATA.[Record Type] = PROG_MATCHES.[Record Type]
        AND DATA.[College Student ID] = PROG_MATCHES.[College Student ID]
        AND DATA.[CIP Code] = PROG_MATCHES.[CIP Code]
        ) AS DATA
        GROUP BY  {self.col_string(self.key_df.columns, 'DATA')}
        ORDER BY TOTAL_MATCHES DESC
        """
        self.print_table(query)

    def create_transformed_data(self):
        query = f"""
        SELECT {self.col_string(self.key_df.columns, 'DATA')},
        PROG_MATCHES.STUDENT_PROGRAMS_ID
        FROM ({self.df_query(self.key_df)}) AS DATA
        LEFT JOIN ({self.df_query(self.prog_match_df)}) AS PROG_MATCHES
        ON DATA.[Record Type] = PROG_MATCHES.[Record Type]
        AND DATA.[College Student ID] = PROG_MATCHES.[College Student ID]
        AND DATA.[CIP Code] = PROG_MATCHES.[CIP Code]
        WHERE PROG_MATCHES.PROGRAM_MATCH = 1
        """
        self.print_table(query)
        self.ODS_SQL(query).to_csv(os.path.join(self.folder, 'Joined Data.csv'), index=False)

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
        SELECT {self.col_string(self.key_df.columns)},
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
        SELECT {self.col_string(self.key_df.columns)},
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
        title = ('Total Amount Student Received in Private Education Loans During Student''s Entire Enrollment'
                 'in the Program')
        query = f"""
        SELECT {self.col_string(self.key_df.columns, 'X')},
                CASE WHEN [Record Type] = 'TA' THEN CAST(COALESCE(SUM(TA_TERM_AMOUNT), 0) AS INT)
                END AS [{title}]
        FROM (
        SELECT DISTINCT 
                {self.col_string(self.joined_data.columns, 'DATA')},
                COMPOUND_ID,
                TA_TERM_AMOUNT
        FROM ({self.df_query(self.joined_data)}) AS DATA
        LEFT JOIN SPT_STUDENT_PROGRAMS AS RECORD_STUDENT_PROGRAM 
        ON DATA.[STUDENT_PROGRAMS_ID] = RECORD_STUDENT_PROGRAM.STUDENT_PROGRAMS_ID
        LEFT JOIN SPT_STUDENT_PROGRAMS AS ALL_SP_AT_CRED 
            ON ALL_SP_AT_CRED.STPR_STUDENT = RECORD_STUDENT_PROGRAM.STPR_STUDENT
                AND ALL_SP_AT_CRED.STPR_ACAD_LEVEL = RECORD_STUDENT_PROGRAM.STPR_ACAD_LEVEL
        LEFT JOIN ODS_FA_TERM_AWARDS AS STU_AWARDS 
                ON LEFT(COMPOUND_ID, 7) = DATA.[College Student ID]
                AND ACADEMIC_YEAR = '2024' 
                AND TA_ACAD_LEVEL = RECORD_STUDENT_PROGRAM.STPR_ACAD_LEVEL
                AND TA_TERM_ACTION = 'A'
                AND AWARD_PERIOD_START_DATE <= COALESCE(ALL_SP_AT_CRED.END_DATE, GETDATE())
                AND AWARD_PERIOD_END_DATE >= ALL_SP_AT_CRED.START_DATE
                AND AWARD_CATEGORY_ID = 'ALT'
        ) AS X
        GROUP BY {self.col_string(self.joined_data.columns)}
        ORDER BY [Record Type] DESC, [College Student ID], [CIP Code]
        """
        self.print_table(query)
        self.ODS_SQL(query).to_csv(os.path.join(self.folder, f'Q. {title}.csv'), index=False)

    def getColumn_R(self):
        '''
        For GE programs, the total amount of institutional debt owned by the student for attendance in any GE program
        at the institution as of the day the student graduated or withdrew from the program, not just for this award
        year.

        For eligible non-GE programs, the total amount of institutional debt owned by the student for attendance in all
        eligible non-GE programs at the same credential level, at the institution as of the day the student graduated
        or withdrew from the program, not just award year.

        If the student did not have any institutional debt, enter a zero or all zeros. Value must be numeric and 0-9.

        Total amount is required unless one of the following conditions is met:
        - Program is flagged as CTP.
        - Program is flagged as Prison Education.
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
        title = 'Total Amount of Institutional Debt During Student''s Entire Enrollment in the Program'
        query = f"""
        SELECT {self.col_string(self.key_df.columns)},
                CASE WHEN [Record Type] = 'TA' THEN 0 
                END AS [{title}]
        FROM ({self.df_query(self.key_df)}) AS X
        """
        self.ODS_SQL(query).to_csv(os.path.join(self.folder, f'R. {title}.csv'), index=False)

    def getColumn_S(self):
        '''
        For GE Programs, the total amount of tuition and fees student incurred during their enrollment in the reported
        GE program.

        For eligible non-GE programs, total amount of tuition and fees student incurred during their enrollment in all
        reported eligible non-GE programs at the same credential level.

        Total amount is required unless one of the following conditions is met:
        - Program is flagged as CTP.
        - Program is flagged as Prison Education.
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
        title = 'Total Amount of Tution & Fees Assessed During Student''s Entire Enrollment in the Program'
        query = f"""
        SELECT DISTINCT 
        {self.col_string(self.joined_data.columns, 'DATA')},
        STU_AWARDS.*
        FROM ({self.df_query(self.joined_data)}) AS DATA
        LEFT JOIN SPT_STUDENT_PROGRAMS AS RECORD_STUDENT_PROGRAM 
        ON DATA.[STUDENT_PROGRAMS_ID] = RECORD_STUDENT_PROGRAM.STUDENT_PROGRAMS_ID
        LEFT JOIN SPT_STUDENT_PROGRAMS AS ALL_SP_AT_CRED 
            ON ALL_SP_AT_CRED.STPR_STUDENT = RECORD_STUDENT_PROGRAM.STPR_STUDENT
                AND ALL_SP_AT_CRED.STPR_ACAD_LEVEL = RECORD_STUDENT_PROGRAM.STPR_ACAD_LEVEL
        LEFT JOIN ODS_FA_TERM_AWARDS AS STU_AWARDS 
                ON LEFT(COMPOUND_ID, 7) = DATA.[College Student ID]
                AND ACADEMIC_YEAR = '2024' 
                AND TA_ACAD_LEVEL = RECORD_STUDENT_PROGRAM.STPR_ACAD_LEVEL
                AND TA_TERM_ACTION = 'A'
                AND AWARD_PERIOD_START_DATE <= COALESCE(ALL_SP_AT_CRED.END_DATE, GETDATE())
                AND AWARD_PERIOD_END_DATE >= ALL_SP_AT_CRED.START_DATE
        """
        self.print_table(query)

    def getColumn_T(self):
        '''
        For GE programs, the total amount in Cost of Attendance (COA) for books, supplies, and equipment charged the
        student for the entire GE program the student for the entire GE program (not just for this award year).

        For eligible non-GE programs, total amount in Cost of Attendance (COA) for books, supplies, and equipment
        charged the student for enrollment in all reported eligible non-GE programs at the same credential level
        (not just for this award year).

        If institution assessed student a higher amount than the allowance in COA, report the higher amount. Value must
        be numeric and 0-9.

        Total amount is required unless one of the following conditions is met:
        - Program is flagged as CTP.
        - Program is flagged as Prison Education.
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
        title = ('Total Amount of Allowance for books, supplies, and equipment included in the student''s title IV, HEA'
        'COA During Student''s Entire Enrollment in the Program')

    def getColumn_U(self):
        '''
        For GE programs, the total amount of institutional grants and scholarships received by the student at any time
        for attendance in the GE program.

        For eligible non-GE programs, total amount of institutional grants and scholarships received by the student at
        any time for attendance in all eligible non-GE programs at the same credential level.

        If the student did not receive any grants or scholarships, enter a zero or all zeros. Value must be numeric and
        0-9.

        Total amount is required unless one of the following conditions is met:
        - Program is flagged as CTP.
        - Program is flagged as Prison Education.
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
        title = ('Total Amount of Grants and Scholarships the student received During Student''s Entire Enrollment '
                 'in the Program')
        query = f"""
        SELECT {self.col_string(self.key_df.columns, 'X')},
        CASE WHEN [Record Type] = 'TA' THEN CAST(COALESCE(SUM(TA_TERM_AMOUNT), 0) AS INT)
        END AS [{title}]
        FROM (
        SELECT DISTINCT 
                {self.col_string(self.joined_data.columns, 'DATA')},
                COMPOUND_ID,
                TA_TERM_AMOUNT
        FROM ({self.df_query(self.joined_data)}) AS DATA
        LEFT JOIN SPT_STUDENT_PROGRAMS AS RECORD_STUDENT_PROGRAM 
        ON DATA.[STUDENT_PROGRAMS_ID] = RECORD_STUDENT_PROGRAM.STUDENT_PROGRAMS_ID
        LEFT JOIN SPT_STUDENT_PROGRAMS AS ALL_SP_AT_CRED 
            ON ALL_SP_AT_CRED.STPR_STUDENT = RECORD_STUDENT_PROGRAM.STPR_STUDENT
                AND ALL_SP_AT_CRED.STPR_ACAD_LEVEL = RECORD_STUDENT_PROGRAM.STPR_ACAD_LEVEL
        LEFT JOIN ODS_FA_TERM_AWARDS AS STU_AWARDS 
                ON LEFT(COMPOUND_ID, 7) = DATA.[College Student ID]
                AND ACADEMIC_YEAR = '2024' 
                AND TA_ACAD_LEVEL = RECORD_STUDENT_PROGRAM.STPR_ACAD_LEVEL
                AND TA_TERM_ACTION = 'A'
                AND AWARD_PERIOD_START_DATE <= COALESCE(ALL_SP_AT_CRED.END_DATE, GETDATE())
                AND AWARD_PERIOD_END_DATE >= ALL_SP_AT_CRED.START_DATE
                AND AWARD_CATEGORY_ID IN (
                    'ACTIV',
                    'ATHL',
                    'CASH',
                    'ENDW',
                    'IGRNT',
                    'ISCHO',
                    'TUIT'
                )
        ) AS X
        GROUP BY {self.col_string(self.joined_data.columns)}
        ORDER BY [Record Type] DESC, [College Student ID], [CIP Code]
        """
        self.print_table(query)
        self.ODS_SQL(query).to_csv(os.path.join(self.folder, f'U. {title}.csv'), index=False)
#=======================================================================================================================
    def getColumn_Z(self):
        '''
        The total cost of attendance for the reported award year. Value must be numeric and 0-9.

        Amount if required unless one of the following conditions is met:
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
        title = 'Annual Cost of Attendance (COA)'
        query = f"""
        SELECT {self.col_string(self.key_df.columns)},
                CASE WHEN [Record Type] = 'AA' THEN 59302 
                END AS [{title}]
        FROM ({self.df_query(self.key_df)}) AS X
        """
        self.print_table(query)
        self.ODS_SQL(query).to_csv(os.path.join(self.folder, f'Z. {title}.csv'), index=False)

    def getColumn_AA(self):
        '''
        Report total amount of tuition and fees charged to the student for the reported award year.

        Value must be numeric and 0-9.

        Amount is required unless one of the following conditions is met:
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
        pass

    def getColumn_AB(self):
        '''
        This field is used as an indicator to show student's residency status.

        Valid values:
        - IS: In-State Tuition
        - ID: In-District Tuition
        - OS: Out-of-State Tuition

        If you institution does not consider residency status when charging tuition, populate OS.

        Amount is required unless one of the following conditions are met:
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
        pass

    def getColumn_AC(self):
        '''
        Allowance amount in Cost of Attendance (COA) for books, supplies, and equipment for the reported award year.

        If institution assessed the student a higher amount than the allowance in COA, report the higher amount. Value
        must be numeric and 0-9.

        Amount is required unless one of the following conditions are met:
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
        pass

    def getColumn_AD(self):
        '''
        Allowance amount in Cost of Attendance (COA) for Housing and Food for this award year.

        If institution assessed student a higher amount than the allowance in COA, report the higher amount. Value must
        be numeric and 0-9.

        Amount is required unless one of the following conditions are met:
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
        pass

    def getColumn_AE(self):
        '''
        Amount of institutional grants and scholarships received by the student for the award year that is being
        reported.

        If the student did not receive any grants or scholarships, enter zero(s).

        Amount is required unless one of the following conditions are met:
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
        pass

    def getColumn_AF(self):
        '''
        Amount of other state, tribal or private grants the student received for the reported award year.

        If the student did not receive any state, tribal, or private grants, enter zero(s).

        Amount is required unless one of the following conditions are met:
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
        pass

    def getColumn_AG(self):
        '''
        Amount of private educational loans received by the student for the reported award year.

        If the student did not receive any private educational loans, enter zero(s).

        Amount is required unless one of the following conditions are met:
        - Student did not receive Title IV Aid for the program.
        - Student withdrew from an eligible non-GE program and should be excluded from the cohort.
        - Program is neither a GE nor eligible non-GE program.
        '''
#=======================================================================================================================
    def getColumn_AH(self):
        '''
        Flag that indicates if the school is invalidating an existing FVT/GE record.

        Valid values are:
        - T: Title IV Aid not received for the program (for NSC use only)
        - R: Not a GE program and student is in a Withdrawn status (for NSC use only)
        - C: Neither GE nor eligible non-GE program (for NSC use only)
        - Y: Yes
        - N: No
        - Space: No
        '''

    def getColumn_AI(self):
        '''
        Flag that indicates if the program is considered a Gainful Employment (GE) program. The GE Program Flag is for
        NSC use only and will not be sent to NSLDS. Please refer to the "Per NSLDS, for GE programs only" and "Per
        NSLDS, for eligible non-GE programs only" sections above.

        Valid values are:
        - Y: Yes
        - N: No
        - Space: No
        '''


    def getColumn(self, col):
        if col == 'N': self.getColumn_N()  #Done
        if col == 'O': self.getColumn_O()  #Done
        if col == 'Q': self.getColumn_Q()  #Done
        if col == 'R': self.getColumn_R()  #Done
        if col == 'S': self.getColumn_S()
        if col == 'T': self.getColumn_T()
        if col == 'U': self.getColumn_U()  #Done
        #================================
        if col == 'Z': self.getColumn_Z()  #Done
        if col == 'AA': self.getColumn_AA()
        if col == 'AB': self.getColumn_AB()
        if col == 'AC': self.getColumn_AC()
        if col == 'AD': self.getColumn_AD()
        if col == 'AE': self.getColumn_AE()
        if col == 'AF': self.getColumn_AF()
        if col == 'AG': self.getColumn_AG()
        #=================================
        if col == 'AH': self.getColumn_AH()
        if col == 'AI': self.getColumn_AI()





