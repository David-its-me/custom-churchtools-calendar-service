
from datetime import datetime, timedelta
from repository_classes.calendar_date import CalendarDate
from services.calendar_manager import CalendarManager
from services.polling_service import PollingService
from functools import cmp_to_key


class DateDataService():

    def __init__(self, polling_service: PollingService, calendar_manager: CalendarManager) -> None:
        self.polling_service = polling_service
        self.calendar_manager = calendar_manager
        pass

    def sort_dates(self, dates: [CalendarDate]) -> [CalendarDate]:
        sorted_dates: [CalendarDate] = sorted(dates, key=cmp_to_key(lambda date1, date2: date2.is_start_before(date1)))
        return sorted_dates
    
    def merge_dates(self, dates: [CalendarDate]) -> [CalendarDate]:
        # TODO merge the entries that are equal. This occours, becaus calendar entries AND events are polled together.
        return dates
    
    def prettify_dates(self, dates: [CalendarDate]) -> [CalendarDate]:
        # TODO build customizable rules, to filter event and/or add customizable texts.
        return dates


    def get_upcomming_date(self, number_upcomming) -> [CalendarDate]:
        # TODO use caching to make this more efficient. E.g. for day 6 the whole list until day 6 is prepared
        dates: [CalendarDate] = self.polling_service.get_events(number_upcomming)
        tomorrow = datetime.now() + timedelta(days=1)
        date_string: str = tomorrow.strftime('%Y-%m-%d')
        dates.extend(self.polling_service.get_calendar_dates(from_=date_string, calendar_ids=self.calendar_manager.get_visible_calendar_ids()))
        
        sorted_dates: [CalendarDate] = self.sort_dates(dates)
        merged_dates: [CalendarDate] = self.merge_dates(sorted_dates)
        prettified_dates: [CalendarDate] = self.prettify_dates(merged_dates)
        
        return prettified_dates[number_upcomming - 1].to_dictionary()
