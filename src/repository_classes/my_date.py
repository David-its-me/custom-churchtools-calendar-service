
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


    
    def to_dictionary(self) -> dict:
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "weekday": self.weekday
        }