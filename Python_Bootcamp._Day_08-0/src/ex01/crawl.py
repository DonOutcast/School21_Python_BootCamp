import warnings
import httpx
import json
import asyncio
import sys

# python3 crawl.py Python Go C++
a = sys.argv
body = {"data": [{"url": link} for link in a[1:]]}


async def get_data_api(data_value):
    api_url = "http://localhost:8888/api/v1/tasks/"
    async with httpx.AsyncClient() as client:
        resp = await client.post(api_url, data=json.dumps(body))
    warnings.simplefilter(action='ignore', category=DeprecationWarning)
    url_value = f'http://127.0.0.1:8888/api/v1/tasks/{data_value}'
    for i in range(3):
        async with httpx.AsyncClient() as client_value:
            response_value = await client_value.get(url_value)
            response_value.raise_for_status()
    data_value = response_value.json()
    print(data_value)


if __name__ == "__main__":
    task_list = list()
    for link in sys.argv[1:]:
        task_list.append(asyncio.ensure_future(get_data_api(link)))
    loop_value = asyncio.get_event_loop()
    loop_value.run_until_complete(asyncio.gather(*task_list))
    loop_value.close()
