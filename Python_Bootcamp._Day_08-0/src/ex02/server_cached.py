import json
import uuid
import httpx
import aioredis
import requests
import asyncio
import uvicorn
import async_timeout
from typing import List
from fastapi import FastAPI
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Url(BaseModel):
    url: str


class UrlList(BaseModel):
    data: List[Url]


class Items(BaseModel):
    web_site: str
    link: str
    UUID4: uuid.UUID
    status: str


STOPWORD = "STOP"
api = FastAPI()


async def pubsub():
    redis = aioredis.Redis.from_url(
        "redis://localhost", max_connections=10, decode_responses=True
    )
    psub = redis.pubsub()

    async def reader(channel: aioredis.client.PubSub):
        while True:
            try:
                async with async_timeout.timeout(1):
                    message = await channel.get_message(ignore_subscribe_messages=True)
                    if message is not None:
                        print(f"(Reader) Message Received: {message}")
                        if message["data"] == STOPWORD:
                            print("(Reader) STOP")
                            break
                    await asyncio.sleep(0.1)
            except asyncio.TimeoutError:
                pass

    async with psub as p:
        await p.subscribe("channel:1")
        await reader(p)
        await p.unsubscribe("channel:1")
    await psub.close()


@api.get('/api/v1/tasks/{data_value}')
async def tasks(data_value: str):
    redis = aioredis.Redis.from_url(
        "redis://localhost", max_connections=10, decode_responses=True
    )
    url_value = f'https://ru.wikipedia.org/wiki/{data_value}'
    with httpx.Client() as client:
        soup_value = BeautifulSoup(client.get(url_value).content, "lxml")
        response_value = requests.get(url_value)
    cache = await redis.get(url_value)
    if cache is not None:
        return Items(web_site=soup_value.title.string,
                     link=url_value,
                     UUID4=uuid.uuid4(),
                     status=response_value.status_code)
    await redis.set(url_value, json.dumps(str(Items(web_site=soup_value.title.string,
                                                link=url_value,
                                                UUID4=uuid.uuid4(),
                                                status=response_value.status_code))), ex=100)
    return Items(web_site=soup_value.title.string,
                 link=url_value,
                 UUID4=uuid.uuid4(),
                 status=response_value.status_code)


if __name__ == '__main__':
    uvicorn.run(api, host="127.0.0.1", port=8888)
