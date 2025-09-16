from Reports import Reports
import os
from pathlib import Path
from tabulate import tabulate
BASE_DIR = Path(__file__).resolve()

class IPEDS (Reports):
    def __init__(self, folder, report):
        super().__init__()
        self.folder = '\\'.join([os.getcwd(), folder])
        self.report = report
        self.report_path = ["Q:", "IR", "Reports", "Reports 2024-25 AY", "Data Provided Grouped By Request",self.report]

    def makedirs(self, *paths):
        for path in paths:
            Path(path).mkdir(parents=True, exist_ok=True)

    def save(self, prompt, query, section, page, name, func_dict = None, snapshot_term = "2025FA", comments = None):
        page_folder = "\\".join(self.report_path + [section, page])
        report_folder = os.path.join(page_folder, name)
        report_prompt_folder = os.path.join(page_folder, "[Prompts]")
        report_code_folder = os.path.join(page_folder, "[Code]")
        report_agg_folder = os.path.join(page_folder, "[Reports (Agg)]")
        report_names_folder = os.path.join(page_folder, "[Reports (Names)]")
        report_comments_folder = os.path.join(page_folder, "[Comments]")
        self.makedirs(report_folder, report_prompt_folder, report_code_folder,
                      report_agg_folder, report_names_folder, report_comments_folder)
        with open(os.path.join(report_folder, f"{name} (Prompt).txt"), "w") as text_file:
            text_file.write(prompt)
        with open(os.path.join(report_prompt_folder, f"{name}.txt"), "w") as text_file:
            text_file.write(prompt)
        if comments is not None:
            with open(os.path.join(report_folder, f"{name} (Comments).txt"), "w") as text_file:
                text_file.write(comments)
            with open(os.path.join(report_comments_folder, f"{name}.txt"), "w") as text_file:
                text_file.write(comments)
        if func_dict is None:
            df = self.db_table(query, db = 'MSSQL', snapshot_term = snapshot_term)
            print(tabulate(df.head(1000), headers='keys', tablefmt='psql'))
            df.to_csv(os.path.join(report_folder, f"{name}.csv"), index=False)
            with open(os.path.join(report_folder, f"{name} (Code).txt"), "w") as text_file:
                text_file.write(query)
            with open(os.path.join(report_code_folder, f"{name}.txt"), "w") as text_file:
                text_file.write(query)
            df.to_csv(os.path.join(report_agg_folder, f"{name}.csv"))

        else:
            for key in func_dict:
                transformed_query = func_dict[key](query)
                df = self.db_table(transformed_query, db = 'MSSQL', snapshot_term = snapshot_term)
                print(tabulate(df.head(1000), headers='keys', tablefmt='psql'))
                df.to_csv(os.path.join(report_folder, f"{name} ({key}).csv"))
                with open(os.path.join(report_folder, f"{name} ({key}).txt"), "w") as text_file:
                    text_file.write(transformed_query)
                with open(os.path.join(report_code_folder, f"{name} ({key}).txt"), "w") as text_file:
                    text_file.write(transformed_query)
                if key == "Agg":
                    df.to_csv(os.path.join(report_agg_folder, f"{name}.csv"))
                if key == "Names":
                    df.to_csv(os.path.join(report_names_folder, f"{name}.csv"))

    def students(self, term = '2025FA'):
        query = f"""
        SELECT DISTINCT STC_PERSON_ID AS ID
        FROM STUDENT_ACAD_CRED AS STC
        LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
        LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
        WHERE STATUS.STC_STATUS IN ('N', 'A')
        AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
        AND STC_TERM = '{term}'
        """
        return query
