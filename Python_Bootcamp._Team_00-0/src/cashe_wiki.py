import logging
import requests as requests
from bs4 import BeautifulSoup
import re
import json
import argparse

# logging.basicConfig(filename='tmp.log', level=logging.INFO, filemode="w")
#
# count = 0
#
#
# def get_links(link: str) -> list:
#     response = requests.get(link)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     links = list()
#     for link in soup.find('div', attrs={'id': 'bodyContent'}).findAll('a'):
#         # if link.get("href") is not None:
#         # string = str(link.get('href'))
#         # if link["href"].__contains__("wikipedia.org") and link["href"].startswith("https://"):
#         links.append(link)
#     return links
#
#
def add_argv():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=str, required=False, default="Harry_Potter")
    parser.add_argument('-d', type=int, required=False, default=3)
    args = parser.parse_args()
    return args

#
# def check_link(checked, current):
#     r = re.compile(r'^/wiki/[^/:]+$')
#     if 'class' in checked.attrs and checked['class'] == 'internal':
#         return False
#     if r.match(checked['href']) is not None and r.findall(checked['href']) != "/wiki/" + current:
#         return True
#     else:
#         return False
#
#
# def cache_wiki(article, result=None, depth=3, max_links=1000):
#     global count
#     if str(article).startswith("/wiki/"):
#         article = article.replace("/wiki/", "")
#     linked_nodes = []
#     if result is None:
#         result = {"nodes": [], "edges": []}
#     if depth < 0:
#         return result
#     p = re.compile(r'(.+) - Wikipedia')
#     print("See : ", article)
#     page = requests.get("https://en.wikipedia.org/wiki/" + article)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     print(p.findall(soup.title.string))
#     # title = p.findall(soup.title.string)[0]
#     title = article
#     logging.info(json.dumps({'title': title, 'href': "https://en.wikipedia.org/wiki/" + article}))
#     if title not in result['nodes']:
#         result['nodes'].append(title)
#         for link in get_links("https://en.wikipedia.org/wiki/" + article):
#             # if count >= 1000:
#             #     break
#             if 'title' in link.attrs and check_link(link, article) is True and len(result['nodes']) < max_links:
#                 if link['title'] not in result['nodes']:
#                     linked_nodes.append(link['title'])
#                     result['nodes'].append(link['title'])
#                     count += 1
#                 new_edge = {"from": title, "to": link['title'], "href": 'https://en.wikipedia.org' + str(link['href'])}
#                 if new_edge not in result['edges']:
#                     result['edges'].append(new_edge)
#             if link != "https://en.wikipedia.org/wiki/" + article:
#                 result = cache_wiki(link.get("href"), result, depth - 1, max_links)
#     json_tmp = json.dumps(result)
#     with open("cache.json", "w") as outfile:
#         outfile.write(json_tmp)
#     return result
#
#
# def main():
#     arguments = add_argv()
#     cache = cache_wiki(article=arguments.p, depth=arguments.d, max_links=arguments.m)
#     json_object = json.dumps(cache)
#     with open("cache.json", "w") as outfile:
#         outfile.write(json_object)
#
#
# if __name__ == "__main__":
#     main()
#     # with open("cache.json", "r") as f:
#     #     temp = json.load(f)
#     # # print(temp["edges"])
#     # for i in temp.get("edges"):
#     #     print(i)
#     # # for i in temp.get("nodes"):
#     # #     print(i)

import logging
import requests as requests
from bs4 import BeautifulSoup
import re
import json
import argparse

logging.basicConfig(filename='tmp.log', level=logging.INFO, filemode="w", )


def check_link(checked, current):
    r = re.compile(r'^/wiki/[^/:]+$')
    if 'class' in checked.attrs and checked['class'] == 'internal':
        return False
    if r.match(checked['href']) is not None and r.findall(checked['href']) != "/wiki/" + current:
        return True
    else:
        return False


def cache_wiki(article, result=None, depth=3, max_links=1000):
    linked_nodes = []
    if result is None:
        result = {"nodes": [], "edges": []}
    if depth < 0:
        return result
    p = re.compile(r'(.+) - Wikipedia')
    page = requests.get("https://en.wikipedia.org/wiki/" + article)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = p.findall(soup.title.text)[0]
    logging.info(json.dumps({'title': title, 'href': "https://en.wikipedia.org/wiki/" + article}))
    if title not in result['nodes']:
        result['nodes'].append(title)
        references = soup.find('div', attrs={'id': 'bodyContent'}).findAll('a')
        for link in references:
            if 'title' in link.attrs and check_link(link, article) is True and len(result['nodes']) < max_links:
                if link['title'] not in result['nodes']:
                    linked_nodes.append(link['title'])
                    result['nodes'].append(link['title'])
                new_edge = {"from": title, "to": link['title'], "href": 'https://en.wikipedia.org' + link['href']}
                if new_edge not in result['edges']:
                    result['edges'].append(new_edge)
        for node in linked_nodes:
            result = cache_wiki(node, result, depth - 1, max_links)
    json_tmp = json.dumps(result)
    with open("cache.json", "w") as outfile:
        outfile.write(json_tmp)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=str, required=False, default="Harry_Potter")
    parser.add_argument('-d', type=int, required=False, default=3)
    parser.add_argument('-m', type=int, required=False, default=10)
    args = parser.parse_args()
    depth = args.d if args.d is not None else 3
    max_l = args.m if args.m is not None else 100
    cache = cache_wiki(article=args.p, depth=depth, max_links=max_l)
    json_object = json.dumps(cache)
    with open("cache.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    main()
    with open("cache.json", "r") as f:
        temp = json.load(f)
    # print(temp["edges"])
    for i in temp.get("edges"):
        print(i)
    # for i in temp.get("nodes"):
    #     print(i)
