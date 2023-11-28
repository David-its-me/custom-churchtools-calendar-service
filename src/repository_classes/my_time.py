
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
    
    def is_before(self, other) -> int:
        if self.hour < other.hour:
            return 1
        if other.hour < self.hour:
            return -1
        if self.minute < other.minute:
            return 1
        if other.minute < self.minute:
            return -1
        return 0

    def equals(self, other):
        if self.hour == other.hour and self.minute == other.minute:
            return True
        return False