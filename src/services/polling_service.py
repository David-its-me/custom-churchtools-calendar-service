import os
import time
import logging
from datetime import datetime, timedelta, timezone
import pytz
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
        
        # On startup load all available services
        with open("../custom-configuration/services.json", "w+") as services_file:
            json.dump(self.api.get_services(), services_file, indent=4)

    
    def _extract_date(self, isoDateString: str) -> MyDate:
        result_date = datetime.strptime(isoDateString, '%Y-%m-%dT%H:%M:%S%z').astimezone().date()
        return MyDate(
            day=result_date.day,
            month=result_date.month,
            year=result_date.year)
            #weekday=result_date.weekday)

    @staticmethod
    def _resolve_address_to_string(address: dict, note: str="") -> str:
        if note is None:
            note = ""
        note.lstrip().rstrip()
        if address is None:
            return note
        
        result: str = ""
        if "meetingAt" in address:
            if not address["meetingAt"] is None:
                if address["meetingAt"] == "":
                    result = result + note
                else:
                    result = result + address["meetingAt"]
        if "street" in address:
            if not address["street"] is None:
                result = result + ", " + address["street"]
        if "addition" in address:
            if not address["addition"] is None:
                result = result + " " + address["addition"]
        if "district" in address:
            if not address["district"] is None:
                result = result + " " + address["district"]
        if "zip" in address:
            if not address["zip"] is None:
                result = result + ", " + address["zip"]
        if "city" in address:
            if not address["city"] is None:
                result = result + " " + address["city"]
        if "country" in address:
            if not address["country"] is None:
                result = result + ", " + address["country"]
        return result
    
    def _extract_time(self, isoDateString: str) -> MyTime:
        result_time = datetime.strptime(isoDateString, '%Y-%m-%dT%H:%M:%S%z').astimezone(tz=timezone.utc)
        local_time = result_time.astimezone(pytz.timezone('Europe/Madrid'))
        return MyTime(
            hour=local_time.hour,
            minute=local_time.minute)

    def get_services(self) -> dict:
        with open("../custom-configuration/services.json") as services_file:
            try:
                return json.load(services_file)
            except: 
                pass
        return []
    
    def get_service_id_of(self, input_service_title: str) -> int:
        input_service_title = input_service_title.lower().rstrip().lstrip()
        for service in self.get_services():
            service_title = service['name']
            service_title = service_title.lower().rstrip().lstrip()
            if input_service_title in service_title:
                return service["id"]
            if service_title in input_service_title:
                return service["id"]
        return -1
    
    def has_livestream(self, event_id: int) -> bool:
        potential_service_names = ["stream", "live", "übertragung"]
        for service_name in potential_service_names:
            service_name_id: int = self.get_service_id_of(service_name)
            if service_name_id > -1:
                try:
                    service_count: int = self.api.get_event_services_counts_ajax(eventId=event_id, serviceId=service_name_id)[service_name_id]
                    if service_count > 0:
                        return True
                except:
                    pass
        return False
    
    def has_childreenschurch(self, event_id: int) -> bool:
        potential_service_names = ["kinder", "kids"]
        for service_name in potential_service_names:
            service_name_id: int = self.get_service_id_of(service_name)
            if service_name_id > -1:
                try:
                    service_count: int = self.api.get_event_services_counts_ajax(eventId=event_id, serviceId=service_name_id)[service_name_id]
                    if service_count > 0:
                        return True
                except:
                    pass
        return False

    def get_speaker(self, event_id: int):
        event_data: dict = self.api.get_AllEventData_ajax(event_id)

        potential_service_names = ["predigt", "referent", "speaker", "vortrag", "sprecher", "program", "liturgie", "moderation"]

        for service_name in potential_service_names:
            service_name_id: int = self.get_service_id_of(service_name)
            if service_name_id > -1:
                for service in event_data["services"]:
                    service_id: int = int(service["service_id"])
                    if service_id == service_name_id:
                        if service["name"] is not None:
                            return service["name"]
        
        return ""
        

    def get_events(self, number_upcomming: int) -> [CalendarDate]:
        # load next event (limit)
        result = self.api.get_events(limit=number_upcomming, direction='forward')

        events: [CalendarDate] = []

        for event in result:
            new_entry: CalendarDate = CalendarDate(
                id=event["appointmentId"],
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
                speaker=self.get_speaker(event_id=event["id"]),
                sermontext="",
                has_childrenschurch=self.has_childreenschurch(event_id=event["id"]),
                has_livestream=self.has_livestream(event_id=event["id"]),
            )
            events.append(new_entry)
        
        return events

    
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
            to_: str, 
            calendar_ids: list) -> [CalendarDate]:
        
        result: dict = self.api.get_calendar_appointments(
            calendar_ids=calendar_ids,
            from_=from_,
            to_=to_)
        
        dates: [CalendarDate] = []

        for date in result:
            if not date["allDay"]: # Ignore dates without time (Ganztägig termine)
                description: str = date['information']
                if description is None:
                    description = ""
                newDate: CalendarDate = CalendarDate(
                    id=date["id"],
                    start_date=self._extract_date(date['startDate']),
                    start_time=self._extract_time(date['startDate']),
                    start_iso_datetime=date['startDate'],
                    end_iso_datetime=date['endDate'],
                    description=description,
                    end_date=self._extract_date(date['endDate']),
                    end_time=self._extract_time(date['endDate']),
                    title=date['caption'],
                    category=date['calendar']['name'],
                    is_event=False,
                    has_livestream=False,
                    has_childrenschurch=False,
                    has_communion=False,
                    location = PollingService._resolve_address_to_string(address=date["address"], note=date["note"]),
                    sermontext = "",
                    speaker = "",
                    category_color = date['calendar']['color'],
                    category_id=date['calendar']['id']
                )
                dates.append(newDate)
            
        return dates
        

    def tearDown(self):
            """
            Destroy the session after test execution to avoid resource issues
            :return:
            """
            self.api.session.close()




