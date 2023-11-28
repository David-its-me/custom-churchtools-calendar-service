
from datetime import datetime, timedelta
import json
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
        # assume that the dates are already sorted, so only the neighbouring entries are compared.
        # Comparison is based on (1) date, (2) time and (3) title of the event.
        result: [CalendarDate] = []
        for i in range(len(dates) - 1):
            if dates[i].start_date.equals(dates[i+1].start_date) \
                        and dates[i].start_time.equals(dates[i+1].start_time) \
                        and dates[i].title == dates[i+1].title:
                
                # merge details
                # if details different concatenate and hope that the prettifier cleans it up
                if not dates[i].description == dates[i+1].description: 
                    dates[i+1].description = "{} {}".format(dates[i].description, dates[i+1].description)
                # if details different concatenate and hope that the prettifier cleans it up
                if not dates[i].speaker == dates[i+1].speaker:
                    dates[i+1].speaker = "{} {}".format(dates[i].speaker, dates[i+1].speaker)
                # if details different concatenate and hope that the prettifier cleans it up
                if not dates[i].location == dates[i+1].location:
                    dates[i+1].location = "{} {}".format(dates[i].location, dates[i+1].location)
                # if details different concatenate and hope that the prettifier cleans it up
                if not dates[i].sermontext == dates[i+1].sermontext:
                    dates[i+1].sermontext = "{} {}".format(dates[i].sermontext, dates[i+1].sermontext)
                # if one entry has the defalt color, use the other (more specific) one
                if dates[i+1].category_color == "#0560ab":
                    dates[i+1].category_color == dates[i].category_color
                # if both entries have different colors the entry i+1 wins.

                # Booleans are concatenated with OR becaus the default value is always False
                dates[i+1].is_event = dates[i].is_event or dates[i+1].is_event
                dates[i+1].has_livestream = dates[i].has_livestream or dates[i+1].has_livestream
                dates[i+1].has_childrenschurch = dates[i].has_childrenschurch or dates[i+1].has_childrenschurch
                dates[i+1].has_communion = dates[i].has_communion or dates[i+1].has_communion
            else:
                result.append(dates[i])
        
        result.append(dates[len(dates)-1])
        return result
    
    @staticmethod
    def _match_sequence(text: str, sequence: [str]) -> bool:
        text_copy = text.lower() # because the text is manipulated
        for fragment in sequence:
            if fragment.lower().lstrip().rstrip() in text_copy:
                text_copy = text_copy[text_copy.find(fragment):]
            else:
                return False
        return True
    
    def filter_dates(self, dates: [CalendarDate]) -> [CalendarDate]:
        result: [CalendarDate] = []
        for date in dates:
            included: bool = True # per default include events
            calendar_data = self.calendar_manager.get_calendar_by_id(date.category_id)
            if "filterRules" in calendar_data:
                if "includeTitles" in calendar_data["filterRules"]:
                    for titleIncludeRule in calendar_data["filterRules"]["includeTitles"]:
                        if self._match_sequence(date.title, titleIncludeRule):
                            included = True
                            break
                
                if "excludeTitles" in calendar_data["filterRules"]:
                    for titleExcludeRule in calendar_data["filterRules"]["excludeTitles"]:
                        if self._match_sequence(date.title, titleExcludeRule):
                            included = False
                            break

            else: # if no rules are specified, then keep the date in the list per default
                included = True
            
            if included:
                result.append(date)
        
        return result

    @staticmethod
    def _apply_rule_manipulation(value: str|bool, rule: dict) -> str|bool:
        if "replacement" in rule:
            value = rule["replacement"]
        if "addition" in rule:
            value = value + rule["addition"] 
        if "value" in rule:
            value = rule["value"] 
        
        return value

    @staticmethod
    def _process_rule(value: str|bool, rule: dict, date: CalendarDate) -> str|bool:
        if "titleSequence" in rule:
            if DateDataService._match_sequence(date.title, rule["titleSequence"]):
                value = DateDataService._apply_rule_manipulation(value=value, rule=rule)
        if "descriptionSequence" in rule:
            if DateDataService._match_sequence(date.description, rule["descriptionSequence"]):
                value = DateDataService._apply_rule_manipulation(value=value, rule=rule)
        if "categorySequence" in rule:
            if DateDataService._match_sequence(date.category, rule["categorySequence"]):
                value = DateDataService._apply_rule_manipulation(value=value, rule=rule)
        
        return value

    @staticmethod
    def prettify_date(date: CalendarDate, rules: dict) -> CalendarDate:
        # Title rules
        title_after_processing: str = date.title
        if "titleRules" in rules:
            for rule in rules["titleRules"]:
                title_after_processing = DateDataService._process_rule(title_after_processing, rule=rule, date=date)
        # Description Rules
        description_after_processing: str = date.description
        if "descriptionRules" in rules:
            for rule in rules["descriptionRules"]:
                description_after_processing = DateDataService._process_rule(description_after_processing, rule=rule, date=date)
        # Sermontext Rules
        sermontext_after_processing: str = date.sermontext
        if "sermontextRules" in rules:
            for rule in rules["sermontextRules"]:
                sermontext_after_processing = DateDataService._process_rule(sermontext_after_processing, rule=rule, date=date)
        # Location Rules
        location_after_processing: str = date.location
        if "locationRules" in rules:
            for rule in rules["locationRules"]:
                location_after_processing = DateDataService._process_rule(location_after_processing, rule=rule, date=date)
        # Category Rules
        category_after_processing: str = date.category
        if "categoryRules" in rules:
            for rule in rules["categoryRules"]:
                category_after_processing = DateDataService._process_rule(category_after_processing, rule=rule, date=date)
        # Category Color Rules
        category_color_after_processing: str = date.category_color
        if "categoryColorRules" in rules:
            for rule in rules["categoryColorRules"]:
                category_color_after_processing = DateDataService._process_rule(category_color_after_processing, rule=rule, date=date)
        
        # TODO Livestream Rules
        # TODO Childrenschurch Rules
        # Communion Rules
        communion_after_processing: bool = date.has_communion
        if "hasCommunionRules" in rules:
            for rule in rules["hasCommunionRules"]:
                communion_after_processing = DateDataService._process_rule(communion_after_processing, rule=rule, date=date)
        
        # After all rules are processed we can now apply the changes to the date
        date.title = title_after_processing
        date.description = description_after_processing
        date.sermontext = sermontext_after_processing
        date.location = location_after_processing
        date.category = category_after_processing
        date.category_color = category_color_after_processing
        # TODO Livestream
        # TODO Childrenschurch
        date.has_communion = communion_after_processing
        
        return date
    
    def prettify_dates(self, dates: [CalendarDate]) -> [CalendarDate]:

        with open("../custom-configuration/prettify_rules.json") as file:
            rules: dict = json.load(file)
            for date in dates:
                date = DateDataService.prettify_date(date, rules=rules)

        return dates


    def get_upcomming_date(self, number_upcomming) -> [CalendarDate]:
        # TODO this is not efficient to caculate everthing from the beginning for each entry.
        # TODO use caching to make this more efficient. E.g. for day 6 the whole list until day 6 is prepared
        dates: [CalendarDate] = self.polling_service.get_events(number_upcomming)
        tomorrow = datetime.now() + timedelta(days=1)
        two_weeks = tomorrow + timedelta(days=14)
        date_string_tomorrow: str = tomorrow.strftime('%Y-%m-%d')
        date_string_two_weeks: str = two_weeks.strftime('%Y-%m-%d')
        dates.extend(self.polling_service.get_calendar_dates(
            from_=date_string_tomorrow, 
            to_=date_string_two_weeks,
            calendar_ids=self.calendar_manager.get_visible_calendar_ids()))
        
        sorted_dates: [CalendarDate] = self.sort_dates(dates)
        merged_dates: [CalendarDate] = self.merge_dates(sorted_dates)
        filtered_dates: [CalendarDate] = self.filter_dates(merged_dates)
        prettified_dates: [CalendarDate] = self.prettify_dates(filtered_dates)
        
        return prettified_dates[number_upcomming - 1].to_dictionary()
