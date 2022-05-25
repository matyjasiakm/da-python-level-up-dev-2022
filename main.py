from datetime import datetime
from typing import Dict

import uvicorn
from fastapi import FastAPI, Response, status, Request, Depends, Query
import requests
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from starlette.responses import HTMLResponse

app = FastAPI()
security = HTTPBasic()


@app.get("/")
def root():
    return {"start": "1970-01-01"}


@app.post("/method", status_code=201)
def m_post():
    return {"method": "POST"}


@app.get("/method")
def m_get():
    return {"method": "GET"}


@app.delete("/method")
def m_del():
    return {"method": "DELETE"}


@app.put("/method")
def m_put():
    return {"method": "PUT"}


@app.options("/method")
def m_option():
    return {"method": "OPTIONS"}


class HelloResp(BaseModel):
    msg: str


week = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}


@app.get("/day")
def read_item(name: str, number: int, response: Response):
    if 7 >= number >= 1:
        if week[number] == name:
            response.status_code = status.HTTP_200_OK
            return
    response.status_code = status.HTTP_400_BAD_REQUEST
    return


class Event(BaseModel):
    date: str
    event: str


class EventInDb(BaseModel):
    id: int
    date: str
    name: str
    date_added: str


id_counter = 0
calendar = []


@app.put("/events", status_code=200)
def put_event(event: Event):
    global id_counter
    e = EventInDb(id=id_counter, date=event.date, name=event.event, date_added=str(datetime.now().date()))
    calendar.append(e)
    id_counter += 1
    return e


@app.get("/events/{date}")
def receive_event(date: str, response: Response):
    format = "%Y-%m-%d"
    try:
        datetime.strptime(date, format)
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    event_list = []
    for i in calendar:
        if i.date == date:
            event_list.append(i)
    if not event_list:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    response.status_code = status.HTTP_200_OK
    return event_list


@app.get("/start", response_class=HTMLResponse)
def get_html():
    return """
    <h1>The unix epoch started at 1970-01-01</h1>
    """


@app.post("/check", response_class=HTMLResponse)
def zad_3_2(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    format = "%Y-%m-%d"
    try:
        datetime.strptime(credentials.password, format)
    except ValueError:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    age = datetime.today().year - datetime.strptime(credentials.password, format).year - (
            (datetime.today().month, datetime.today().day) < (
        datetime.strptime(credentials.password, format).month, datetime.strptime(credentials.password, format).day))
    if age < 16:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return

    response.status_code = status.HTTP_200_OK
    return f"<h1>Welcome {credentials.username}! You are {age}</h1>"


@app.get("/info")
def zad_33(response: Response, request: Request, format: str = Query("")):
    if format == "html":
        c = "<input type=\"text\" id=user-agent name=agent value=\"" + request.headers.get("User-Agent") + "\">"
        return HTMLResponse(content=c, status_code=200)
    elif format == "json":
        return {"user_agent": request.headers.get("User-Agent")}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST


simple_db = []


@app.get("/save/{s}")
def zad_34(s: str, response: Response):
    if s not in simple_db:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    response.status_code = status.HTTP_301_MOVED_PERMANENTLY
    response.headers.append("Location", "/info")


@app.put("/save/{s}", status_code=200)
def zad_34_put(s: str):
    if s not in simple_db:
        simple_db.append(s)
    return


@app.delete("/save/{s}", status_code=200)
def zad_34_del(s: str):
    simple_db.remove(s)
    return



