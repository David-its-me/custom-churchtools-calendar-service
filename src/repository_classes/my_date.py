import json

class MyDate():

    def __init__(self,
            month: int,
            day: int,
            year: int=-1,
            weekday: int=-1
    ):
        self.year: int = year
        self.month: int = month
        self.day: int = day
        self.weekday: int = weekday

    @staticmethod
    def date_from_dictionary(obj: dict):
        return MyDate(year=obj["year"],
                    month=obj["month"],
                    day=obj["day"],
                    weekday=obj["weekday"])

    def get_month_abbreviaton(self) -> str:
        result:str = ""
        with open("../custom-configuration/month_abbreviations.json") as file:
            abbreviations: dict = json.load(file)
            result = abbreviations["{}".format(self.month)]
        return result

    
    def to_dictionary(self) -> dict:
        return {
            "year": self.year,
            "month": self.month,
            "month_abbreviation": self.get_month_abbreviaton(),
            "day": self.day,
            "weekday": self.weekday
        }
    
    def is_before(self, other) -> int:
        if self.year < other.year:
            return 1
        if other.year < self.year:
            return -1
        if self.month < other.month:
            return 1
        if other.month < self.month:
            return -1
        if self.day < other.day:
            return 1
        if other.day < self.day:
            return -1
        return 0
    
    def equals(self, other) -> bool:
        if self.year == other.year and self.month == other.month and self.day == other.day:
            return True
        return False

