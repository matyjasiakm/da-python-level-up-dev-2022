from typing import Dict

from fastapi import FastAPI

from pydantic import BaseModel


app = FastAPI()


@app.get("/")
def root():
    return {"start": "1970-01-01"}

@app.post("/method",status_code=201)
def m_post():
    return {"method": "POST"}

@app.get("/method")
def m_get():
    return {"method": "GET"}

@app.delete("/method")
def m_del():
    return {"method": "Delete"}

@app.put("/method")
def m_put():
    return {"method": "PUT"}

@app.options("/method")
def m_option():
    return {"method": "OPTIONS"}

class HelloResp(BaseModel):
    msg: str


@app.get("/hello/{name}", response_model=HelloResp)
def read_item(name: str):
    return HelloResp(msg=f"Hello {name}")


class GiveMeSomethingRq(BaseModel):
    first_key: str


class GiveMeSomethingResp(BaseModel):
    received: Dict
    constant_data: str = "python jest super"


@app.post("/dej/mi/coś", response_model=GiveMeSomethingResp)
def receive_something(rq: GiveMeSomethingRq):
    return GiveMeSomethingResp(received=rq.dict())





