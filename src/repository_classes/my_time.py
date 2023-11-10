
class MyTime:

    def __init__(self,
            hour: int,
            minute: int
    ):
        self.hour: int = hour
        self.minute: int = minute

    @staticmethod
    def time_from_dictionary(obj: dict):
        return MyTime(hour=obj["hour"], minute=obj["minute"])


    def to_dictionary(self) -> dict:
        return {
            "hour":self.hour,
            "minute":self.minute
        }
