from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from services.polling_service import PollingService

app = FastAPI()
polling_service = PollingService()

@app.on_event("startup")
async def startup_event() -> None:
    """tasks to do at server startup"""
    polling_service.poll_entries(3)

@app.get("/")
def read_root():
    return read_static_content(asset_type="html", path="main.html")

@app.get("/static/{asset_type}/{path}")
def read_static_content(asset_type: str, path: str):
    return FileResponse("../static/{}/{}".format(asset_type, path))

@app.get("/html/{path}")
def read_html(path: str):
    return read_static_content(asset_type="html", path=path)

@app.get("/script/{path}")
def read_script(path: str):
    return read_static_content(asset_type="script", path=path)

@app.get("/css/{path}")
def read_css(path: str):
    return read_static_content(asset_type="css", path=path)

@app.get("/event/upcomming/{nextUpcomming}")
def get_event(nextUpcomming: int):
    # TODO this implementation is not efficient!!!
    entries = polling_service.poll_entries(nextUpcomming + 1)
    return entries[nextUpcomming].to_dictionary()

@app.get("/test")
def test():
    return polling_service.get_calendar_entries(10)

