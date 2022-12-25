import json
import argparse
import requests
from bs4 import BeautifulSoup
import sys
import logging

count = 0
logging.basicConfig(stream=sys.stdout, level=logging.INFO, filemode="w")


def add_argv():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=str, required=False, default="Small-world_network")
    parser.add_argument('-d', type=int, required=False, default=3)
    args = parser.parse_args()
    return args


def get_links(link: str) -> list:
    response = requests.get(link).text
    soup = BeautifulSoup(response, 'html.parser')
    links = list()
    for link in soup.find('div', attrs={'id': 'bodyContent'}).findAll('a'):
        if count >= 999:
            break
        if link.get("title") is not None:
            if link.get("href").startswith("/wiki/"):
                links.append(link)
                logging.info(link.get("href"))
    return links


def get_all_links(entry_link: str, iteration: int):
    global count
    title = entry_link.rsplit("/")[-1]
    result = {"nodes": [], "edges": []}
    if entry_link.rsplit("/")[-1] not in result["nodes"]:
        result["nodes"].append(entry_link.rsplit("/")[-1])
    if iteration > 0 and count < 1000:
        for link in get_links(entry_link):
            if count >= 999:
                break

            if title not in result["nodes"]:
                result["nodes"].append(link["title"])
            else:
                if link["title"] not in result["nodes"]:
                    result["nodes"].append(link["title"])
                new_edge = {"from": title, "to": link['title'], "href": 'https://en.wikipedia.org' + link['href']}
                if new_edge not in result['edges']:
                    result['edges'].append(new_edge)
            count += 1
            if link.get("href") != entry_link and iteration - 1 > 0:
                result = get_all_links('https://en.wikipedia.org' + str(link.get("href")).replace("/wki/", ""),
                                       iteration - 1)
    return result


try:
    arguments = add_argv()
    name = str(arguments.p).replace(' ', '_')
    URL = f"https://en.wikipedia.org/wiki/{name}"

    result = get_all_links(URL, arguments.d)
    if count < 20:
        print("\nToo few links. Please, change other default starting page")
    else:
        json_object = json.dumps(result, indent=4, ensure_ascii=False)
        with open('wiki.json', 'w', encoding='utf-8') as w:
            w.write(json_object)

except requests.exceptions.ConnectionError:
    print("Bad URL")
