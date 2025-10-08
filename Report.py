from datetime import date

class Report:
    def __init__(self, id: int, name: str, person: str, start: date, due: date, finish: date):
        self.id = id
        self.name = name
        self.person = person
        self.start = start
        self.due = due
        self.finish = finish
        self.tables = {}