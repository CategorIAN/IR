from datetime import date
import pandas as pd
import pyodbc, environ
from pathlib import Path
from tabulate import tabulate
import os
from functools import reduce
from Report_Table import Report_Table
BASE_DIR = Path(__file__).resolve()

class Report:
    def __init__(self, id: int, name: str, person: str, start: date, due: date, finish: date):
        self.id = id
        self.name = name
        self.person = person
        self.start = start
        self.due = due
        self.finish = finish
        self.tables = {}
        command = f"""
        IF NOT EXISTS (
            SELECT 1 FROM REPORT
            WHERE ID = '{id}'
        )
        BEGIN
        INSERT INTO REPORT (ID, NAME, PERSON, START, DUE, FINISH, UPDATED)
        VALUES ('{id}', '{name}', '{person}', '{start}', '{due}', '{finish}', NULL)
        END
        """
        self.executeAWSSQL(command)

    def executeAWSSQL(self, command):
        try:
            env = environ.Env()
            my_str = (f'DRIVER={{SQL Server}};'
                              f'SERVER={env("AWS_HOST")};'
                              f'DATABASE={env("AWS_Name")};'
                              f'UID={env("AWS_USER")};'
                              f'PWD={env("AWS_PASSWORD")}')
            connection = pyodbc.connect(my_str)
            cursor = connection.cursor()
            command = command.replace("'None'", "NULL")
            print(10 * "=" + "\nExecuting\n" + 10 * "=" + ("\n" + command + "\n") + + 10 * "=")
            cursor.execute(command)
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
            print("Connection Closed")

    def getTable(self, id):
        table_data = self.tables[id]
        return Report_Table(**{"report": self.id, "table": id, "name": table_data["name"]})

    def saveDraft(self, id, overwrite = True):
        table_data = self.tables[id]
        table = Report_Table(**{"report": self.id, "table": id, "name": table_data["name"]})
        bundle = table.query_bundle(table_data["query"], table_data["snapshot_term"], table_data["func_dict"])
        table.save_draft(bundle, overwrite)



