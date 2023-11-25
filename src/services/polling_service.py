import os
import time
import logging
from datetime import datetime, timedelta
import json
from churchtools_api.churchtools_api import ChurchToolsApi
from repository_classes.calendar_date import CalendarDate
from repository_classes.my_date import MyDate
from repository_classes.my_time import MyTime


class PollingService():
    
    
    def __init__(self):
        if 'CT_TOKEN' in os.environ:
            self.ct_token = os.environ['CT_TOKEN']
            self.ct_domain = os.environ['CT_DOMAIN']
            users_string = os.environ['CT_USERS']
            self.ct_users = ast.literal_eval(users_string)
            logging.info('using connection details provided with ENV variables')
        else:
            with open("../secret/churchtools_credentials.json") as credential_file:
                secret_data = json.load(credential_file)
                self.ct_token = secret_data["ct_token"]
                self.ct_domain = secret_data["ct_domain"]
                self.ct_users = secret_data["ct_users"]
            logging.info('using connection details provided from secrets folder')

        self.api = ChurchToolsApi(domain=self.ct_domain, ct_token=self.ct_token)
        logging.basicConfig(filename='../logs/TestsChurchToolsApi.log', encoding='utf-8',
                            format="%(asctime)s %(name)-10s %(levelname)-8s %(message)s",
                            level=logging.DEBUG)
        logging.info("Executing Tests RUN")

    
    def _extract_date(self, isoDateString: str) -> MyDate:
        result_date = datetime.strptime(isoDateString, '%Y-%m-%dT%H:%M:%S%z').astimezone().date()
        return MyDate(
            day=result_date.day,
            month=result_date.month,
            year=result_date.year)
            #weekday=result_date.weekday)
    
    def _extract_time(self, isoDateString: str) -> MyTime:
        today_date = datetime.today().date()
        result_date = datetime.strptime(isoDateString, '%Y-%m-%dT%H:%M:%S%z').astimezone()
        return MyTime(
            hour=result_date.hour,
            minute=result_date.minute)

    def get_events(self, number_upcomming: int) -> [CalendarDate]:
        # load next event (limit)
        result = self.api.get_events(limit=number_upcomming, direction='forward')

        events: [CalendarDate] = []

        for event in result:
            new_entry: CalendarDate = CalendarDate(
                start_date=self._extract_date(event['startDate']),
                start_time=self._extract_time(event['startDate']),
                start_iso_datetime=event['startDate'],
                end_iso_datetime=event['endDate'],
                description=event['description'],
                end_date=self._extract_date(event['endDate']),
                end_time=self._extract_time(event['endDate']),
                title=event['name'],
                category=event['calendar']['title'],
                is_event=True,
                #category_color = event['calendar']['color']
            )
            events.append(new_entry)
        
        return events

        
        '''
        # load last event (direction, limit)
        result = self.api.get_events(limit=1, direction='backward')
        result_date = datetime.strptime(result[0]['startDate'], '%Y-%m-%dT%H:%M:%S%z').astimezone().date()

        # Load events after 7 days (from)
        next_week_date = today_date + timedelta(days=7)
        next_week_formatted = next_week_date.strftime('%Y-%m-%d')
        result = self.api.get_events(from_=next_week_formatted)
        result_min_date = min([datetime.strptime(item['startDate'], '%Y-%m-%dT%H:%M:%S%z').astimezone().date() for item in result])
        result_max_date = max([datetime.strptime(item['startDate'], '%Y-%m-%dT%H:%M:%S%z').astimezone().date() for item in result])
        
        # load events for next 14 days (to)
        next2_week_date = today_date + timedelta(days=14)
        next2_week_formatted = next2_week_date.strftime('%Y-%m-%d')
        today_date_formatted = today_date.strftime('%Y-%m-%d')

        result = self.api.get_events(from_=today_date_formatted, to_=next2_week_formatted)
        result_min = min([datetime.strptime(item['startDate'], '%Y-%m-%dT%H:%M:%S%z').astimezone().date() for item in result])
        result_max = max([datetime.strptime(item['startDate'], '%Y-%m-%dT%H:%M:%S%z').astimezone().date() for item in result])
        '''
    
    def get_calendar_list(self) -> dict:
        """
        Tries to retrieve a list of calendars
        """
        result: dict = self.api.get_calendars()
        return result

    #TODO
    def get_calendar_dates(
            self, 
            from_: str, 
            #to_: str, 
            calendar_ids: list) -> [CalendarDate]:
        
        result: dict = self.api.get_calendar_appointments(
            calendar_ids=calendar_ids,
            from_=from_,
            #to_=to_
            )
        
        dates: [CalendarDate] = []

        for date in result:
            address: str = date["address"] 
            if address is None:
                address = ""

            newDate: CalendarDate = CalendarDate(
                start_date=self._extract_date(date['startDate']),
                start_time=self._extract_time(date['startDate']),
                start_iso_datetime=date['startDate'],
                end_iso_datetime=date['endDate'],
                description=date['information'],
                end_date=self._extract_date(date['endDate']),
                end_time=self._extract_time(date['endDate']),
                title=date['caption'],
                category=date['calendar']['name'],
                is_event=False,
                has_livestream=False,
                has_childrenschurch=False,
                has_communion=False,
                location = address,
                sermontext = "",
                speaker = "",
                category_color = date['calendar']['color']
            )
            dates.append(newDate)
        
        return dates
        

    def tearDown(self):
            """
            Destroy the session after test execution to avoid resource issues
            :return:
            """
            self.api.session.close()




