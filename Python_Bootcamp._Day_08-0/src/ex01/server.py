import uuid
import httpx
import uvicorn
import requests
from fastapi import FastAPI
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List


class Url(BaseModel):
    url: str


class UrlList(BaseModel):
    data: List[Url]


class Items(BaseModel):
    web_site: str
    link: str
    UUID4: uuid.UUID
    status: str


api = FastAPI()


@api.get("/")
async def root():
    return {"message": "Hello World"}


@api.post("/api/v1/tasks/", status_code=201)
async def create_item(data: UrlList):
    temp = data.dict()
    return None


@api.get('/api/v1/tasks/{data_value}', status_code=201)
async def tasks(data_value: str):
    url_value = f'https://ru.wikipedia.org/wiki/{data_value}'
    async with httpx.AsyncClient() as client:
        after_corutine = await client.get(url_value)
        soup_value = BeautifulSoup(after_corutine.content, 'lxml')
        response_value = requests.get(url_value)
    return Items(web_site=soup_value.title.string,
                 link=url_value,
                 UUID4=uuid.uuid4(),
                 status=response_value.status_code)


if __name__ == '__main__':
    uvicorn.run(api, host="127.0.0.1", port=8888)
