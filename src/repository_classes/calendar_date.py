from repository_classes.my_date import MyDate
from repository_classes.my_time import MyTime

class CalendarDate():

    def __init__(self,
                 start_date: MyDate,
                 start_time: MyTime,
                 end_date: MyDate,
                 end_time: MyTime,
                 start_iso_datetime: str,
                 end_iso_datetime: str,
                 category: str = "",
                 description: str = "",
                 title: str = "",
                 has_livestream: bool = False,
                 has_childrenschurch: bool = False,
                 has_communion: bool = False,
                 location: str = "",
                 sermontext: str = "",
                 speaker: str = "",
                 is_event: bool = False,
                 category_color: str = "#0560ab",
                 category_id: int = 0):
        self.start_date: MyDate = start_date
        self.end_date: MyDate = end_date
        self.start_time: MyTime = start_time
        self.end_time: MyTime = end_time
        self.category: str = category
        self.description: str = description
        self.title: str = title
        self.has_livestream: bool = has_livestream
        self.has_childrenschurch: bool = has_childrenschurch
        self.has_communion: bool = has_communion
        self.location: str = location
        self.sermontext: str = sermontext
        self.speaker: str = speaker
        self.is_event: bool = is_event
        self.category_color: str = category_color
        self.start_iso_datetime: str = start_iso_datetime
        self.end_iso_datetime: str = end_iso_datetime
        self.category_id: int = category_id

    @staticmethod
    def calendar_entry_from_dictionary(obj: dict):
        return CalendarDate(start_date=MyDate.date_from_dictionary(obj["start_date"]),
                            end_date=MyDate.date_from_dictionary(obj["end_date"]),
                            start_time=MyTime.time_from_dictionary(obj["start_time"]),
                            end_time=MyTime.time_from_dictionary(obj["end_time"]),
                            category=obj["category"],
                            description=obj["description"],
                            title=obj["title"],
                            has_livestream=obj["has_livestream"],
                            has_childrenschurch=obj["has_childrenschurch"],
                            has_communion=obj["has_communion"],
                            location=obj["location"],
                            sermontext=obj["sermontext"],
                            speaker=obj["speaker"],
                            is_event=obj["is_event"],
                            category_color=obj["category_color"],
                            category_id=obj["category_id"])
    
    def to_dictionary(self) -> dict:
        return {
            "start_date": self.start_date.to_dictionary(),
            "end_date": self.end_date.to_dictionary(),
            "start_time": self.start_time.to_dictionary(),
            "end_time": self.end_time.to_dictionary(),
            "category": self.category,
            "description": self.description,
            "title": self.title,
            "has_livestream": self.has_livestream,
            "has_childrenschurch": self.has_childrenschurch,
            "has_communion": self.has_communion,
            "location": self.location,
            "sermontext": self.sermontext,
            "speaker": self.speaker,
            "is_event": self.is_event,
            "category_color": self.category_color,
            "category_id": self.category_id
        }
    
    def is_start_before(self, other) -> int:
        if self.start_date.is_before(other.start_date) != 0:
            return self.start_date.is_before(other.start_date)
        if self.start_time.is_before(other.start_time) != 0:
            return self.start_time.is_before(other.start_time)
        return 0

