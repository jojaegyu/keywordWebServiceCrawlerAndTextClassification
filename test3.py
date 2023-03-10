import re
import sys
from urllib import request
from bs4 import BeautifulSoup
import requests

keyword = '스키'
BASE = "https://www.instiz.net/"
start_time = "20210903"
end_time = "20210905"
for page in range(1, 100):
    corpus = []
    page_url = "https://www.instiz.net/name?page={}&category=1&k={}&stype=1&starttime={}&endtime={}".format(
        page, keyword, start_time, end_time)

    html = requests.get(page_url)
    bs = BeautifulSoup(html.content.decode('utf-8', 'replace'), 'html.parser')
    is_possible = bs.find('td', {"class": "searchlist"})
    if is_possible and "검색 결과가 없습니다" in is_possible.get_text():
        break

    for idx, post in enumerate(bs.find_all("td", {"class": re.compile(".*listsubject sbj")})):
        post_url = BASE + post.a['href']
        title = post.get_text()
        html = requests.get(post_url)
        bs = BeautifulSoup(html.content.decode('utf-8', 'replace'), 'html.parser')
        corpus.append(title)
        for content in bs.find_all("div", {"class": "comment_line"}):
            corpus.append(content.span.get_text())
    print(corpus)



