from services.polling_service import PollingService
import json

class CalendarManager:
     
    def __init__(self, polling_service: PollingService) -> None:
        self.polling_service = polling_service
        self.update_local_calendar_data()

    def get_local_calendar_data(self) -> dict:
        with open("../custom-configuration/calendar_settings.json") as settings_file:
            try:
                return json.load(settings_file)
            except: 
                pass
        return []

    def get_calendar_ids(self) -> [int]:
        local_data: dict = self.get_local_calendar_data()
        result: [] = []
        for calendar in local_data:
            if "id" in calendar:
                result.append(calendar["id"])
        
        return result
    
    def get_visible_calendar_ids(self) -> [int]:
        ids: [int] = self.get_calendar_ids()
        return list(filter(lambda value: self.is_calendar_visible(value), ids))
    

    def is_calendar_visible(self, calendar_id: int) -> bool:
        local_calendar_data: dict = self.get_local_calendar_data()
        for calendar in local_calendar_data:
            if "id" in calendar:
                id = calendar["id"]
                if int(id) == calendar_id:
                    if "visible" in calendar:
                        return calendar["visible"]
                    else:
                        return True #optimistic policy: if there is no info, but calendar exists then return true.
        
        return False


    def update_local_calendar_data(self, overwrite_arguments: [dict] = []) -> dict:
        local_calendar_data = self.get_local_calendar_data()            
        with open("../custom-configuration/calendar_settings.json", "w+") as settings_file:
            church_tools_calendar_data: dict = self.polling_service.get_calendar_list()
            # update with data from ChurchTools
            for remote_calendar in church_tools_calendar_data:
                if "id" in remote_calendar:
                    remote_id = remote_calendar["id"]
                    entry_is_missing: bool = True
                    for local_calendar in local_calendar_data:
                        if "id" in local_calendar:
                            id = local_calendar["id"]
                            if not remote_id == id:
                                pass
                            else:
                                local_calendar.update(remote_calendar)
                                entry_is_missing = False
                                break
                    if entry_is_missing:
                        local_calendar_data.append(remote_calendar)
            
            # update with overwrite arguments
            for local_calendar in local_calendar_data:
                if "id" in local_calendar:
                    id = local_calendar["id"]
                    for argument in overwrite_arguments:
                        if "id" in argument:
                            overwrite_id = argument["id"]
                            if not overwrite_id == id:
                                pass
                            else:
                                local_calendar.update(argument)
                                break
            
            json.dump(local_calendar_data, settings_file, indent=4)
        
        return local_calendar_data


        
    def set_calendar_visibility(self, id: int, visible: bool) -> dict:
        arguments: dict = [{
            "id": id,
            "visible": visible
        }]
        return self.update_local_calendar_data(overwrite_arguments=arguments)
    
    def get_calendar_by_id(self, id: int) -> dict:
        local_data = self.get_local_calendar_data()
        for calendar in local_data:
            if "id" in calendar:
                if calendar["id"] == id:
                    return calendar
                
        return {}
    
                