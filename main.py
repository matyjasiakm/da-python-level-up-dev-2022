from datetime import datetime
from typing import Dict

from fastapi import FastAPI, Response, status

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
    date: datetime
    event: str


class EventInDb(BaseModel):
    id: int
    date: datetime
    event: str
    date_added: datetime


id_counter = 0
calendar = []


@app.put("/events")
def put_event(event: Event, response: Response):
    global id_counter
    e = EventInDb()
    e.date = event.date.date
    e.event = event.event
    e.id = id_counter
    id_counter += 1
    e.date_added = datetime.now().date()
    response.status_code = status.HTTP_201_CREATED
    return e


class GiveMeSomethingRq(BaseModel):
    first_key: str


class GiveMeSomethingResp(BaseModel):
    received: Dict
    constant_data: str = "python jest super"


@app.post("/dej/mi/coś", response_model=GiveMeSomethingResp)
def receive_something(rq: GiveMeSomethingRq):
    return GiveMeSomethingResp(received=rq.dict())
