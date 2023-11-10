from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from churchtools_polling import PollingService

app = FastAPI()
polling = PollingService()

@app.on_event("startup")
async def startup_event() -> None:
    """tasks to do at server startup"""
    polling.poll_entries(3)

@app.get("/")
def read_root():
    return read_asset(asset_type="html", path="main.html")

@app.get("/assets/{asset_type}/{path}")
def read_asset(asset_type: str, path: str):
    return FileResponse("../assets/{}/{}".format(asset_type, path))

@app.get("/html/{path}")
def read_html(path: str):
    return read_asset(asset_type="html", path=path)

@app.get("/script/{path}")
def read_script(path: str):
    return read_asset(asset_type="script", path=path)

@app.get("/css/{path}")
def read_css(path: str):
    return read_asset(asset_type="css", path=path)

@app.get("/event/upcomming/{nextUpcomming}")
def get_event(nextUpcomming: int):
    # TODO this implementation is not efficient!!!
    entries = polling.poll_entries(nextUpcomming + 1)
    return entries[nextUpcomming].to_dictionary()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

