from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from services.date_data_service import DateDataService
from starlette.responses import FileResponse
from services.polling_service import PollingService
from services.calendar_manager import CalendarManager
from pydantic import BaseModel

app = FastAPI()
polling_service: PollingService = PollingService()
calendar_manager: CalendarManager = CalendarManager(polling_service)
date_service: DateDataService = DateDataService(polling_service, calendar_manager)

@app.on_event("startup")
async def startup_event() -> None:
    """tasks to do at server startup"""
    # Poll once in the beginning, which takes a bit longer. After that the values are cached for 1 hours
    try: # If a problem occours the try catch clause ensures, that the whole server is still able to start.
        date_service.get_upcomming_date(0) 
    except:
        pass
    

@app.get("/")
def read_root():
    return read_static_content(asset_type="html", path="main.html")

@app.get("/slide/upcommingEvents/{slideCount}")
def read_root():
    return read_static_content(asset_type="html", path="main.html")

@app.get("/static/{asset_type}/{path}")
def read_static_content(asset_type: str, path: str):
    return FileResponse("../static/{}/{}".format(asset_type, path))

@app.get("/html/{path}")
def read_html(path: str):
    return read_static_content(asset_type="html", path=path)

@app.get("/icons/{path}")
def read_html(path: str):
    return read_static_content(asset_type="icons", path=path)

@app.get("/script/{path}")
def read_script(path: str):
    return read_static_content(asset_type="script", path=path)

@app.get("/css/{path}")
def read_css(path: str):
    return read_static_content(asset_type="css", path=path)

@app.get("/date/upcomming/{nextUpcomming}")
def get_event(nextUpcomming: int):
    return date_service.get_upcomming_date(nextUpcomming)



@app.get("/test")
def test():
    return polling_service.api.get_AllEventData_ajax(431)

@app.get("/test2")
def test2():
    return DateDataService._tag_rule({"descriptionSequence": ["<biblicalBook>", "<#1>"], "replacement": ["<biblicalBook>", " <#1>"]})
    


class Visibility(BaseModel):
    visible: bool


@app.get("/calendar/{id}/visible")
def get_calendar_visibility(id: int):
    return {"visible": calendar_manager.is_calendar_visible(id)}


@app.post("/calendar/{id}/visible")
def set_calendar_visibility(id: int, visibility_data: Visibility):
    return calendar_manager.set_calendar_visibility(id = id, visible=visibility_data.visible)

