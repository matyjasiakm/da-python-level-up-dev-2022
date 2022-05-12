from datetime import datetime
from typing import Dict

import uvicorn
from fastapi import FastAPI, Response, status
import requests
from pydantic import BaseModel

app = FastAPI()


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
    except ValueError :
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    event_list = []
    for i in calendar:
        if i.date == date:
            event_list.append(i)
    if event_list.count == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    response.status_code = status.HTTP_200_OK
    return event_list
