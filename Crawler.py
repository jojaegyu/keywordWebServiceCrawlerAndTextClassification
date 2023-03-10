from bs4 import BeautifulSoup
from collections import deque, defaultdict
from urllib.request import urlopen
import requests
import heapq
import re
from konlpy.tag import Kkma
import mongodb
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import time


class Text:
    def __init__(self, text, kind, date, website, url):
        self.text = text
        self.kind = kind
        self.date = date
        self.website = website
        self.url = url

    def text2dictionary(self):
        dic = {'text': self.text, 'kind': self.kind, 'date': self.date, 'website': self.website, 'url': self.url}
        return dic


class Crawler:
    def __init__(self):
        self.keywords = defaultdict(int)
        self.visited = defaultdict(lambda : False)
        self.urls = []
        self.heap = []
        self.noun_extraction = Kkma()
        self.MongoRepository = mongodb.MongoRepository()

    def init_Crawler(self):
        for i in range(1, 19):
            try:
                res = requests.get("https://www.instiz.net/pt?page={}&srt=3&srd=1".format(i))
            except:
                break
            bs = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')
            for title in bs.find_all("a", {"href": re.compile("page={}.*srd=1.*".format(i))}):
                if title.i != None:
                    split_text = self.textPreprocessing(title.get_text())
                    print(split_text)
                    for keyword in split_text:
                        if len(keyword) > 1:
                            self.keywords[keyword] += 1
        print("inited-------")
        print(self.keywords)

    def textPreprocessing(self, s):
        s = re.sub(r'[^A-Za-z가-힣\s]', '', s)
        return self.noun_extraction.nouns(s)

    def keywordsHeapify(self):
        self.heap = [(-self.keywords[key], key) for key in self.keywords.keys()]
        heapq.heapify(self.heap)
        while self.heap:
            value, key = heapq.heappop(self.heap)
            if not self.visited[key]:
                self.visited[key] = True
                del self.keywords[key]
                return key
        return ''

    def check_block(self, url):
        html = requests.get(url)
        while '403' in str(html):
            time.sleep(60)
            html = requests.get(url)
        return html

    def search(self, keyword, start_time, end_time):
        keyword = keyword
        BASE = "https://www.instiz.net/"
        start_time = start_time
        end_time = end_time
        corpus = []

        for page in range(1, 100):
            page_url = "https://www.instiz.net/pt?page={}&category=1&k={}&stype=1&starttime={}&endtime={}".format(
                page, keyword, start_time, end_time)

            html = self.check_block(page_url)
            bs = BeautifulSoup(html.content.decode('utf-8', 'replace'), 'html.parser')
            is_possible = bs.find('td', {"class": "searchlist"})
            if is_possible and "검색 결과가 없습니다" in is_possible.get_text():
                break

            for idx, post in enumerate(bs.find_all("td", {"class": re.compile(".*listsubject sbj")})):
                post_url = BASE + post.a['href']
                if not list(self.MongoRepository.findUrl(post_url)):
                    html = self.check_block(post_url)
                    # if self.check_block(html):
                    #     time.sleep(1800)
                    title = post.get_text()
                    bs = BeautifulSoup(html.content.decode('utf-8', 'replace'), 'html.parser')
                    text = Text(title, 'post', start_time, 'instiz', post_url)
                    self.MongoRepository.insertText(text)
                    corpus.append(text)
                    for content in bs.find_all("div", {"class": "comment_line"}):
                        text = Text(content.span.get_text(), 'comment', start_time, 'instiz', post_url)
                        self.MongoRepository.insertText(text)
                        corpus.append(text)

        return corpus


def generate_time(times):
    today = date.today()
    for day in range(12):
        times.append({"start_time": str(today-timedelta(days=day+1)).replace('-', ''), "end_time": str(today-timedelta(days=day)).replace('-', '')})
    for week in range(12):
        times.append({"start_time": str(today-timedelta(weeks=week+1)).replace('-', ''), "end_time": str(today-timedelta(weeks=week)).replace('-', '')})
    for month in range(12):
        times.append({"start_time": str(today-relativedelta(months=month+1)).replace('-', ''), "end_time": str(today-relativedelta(months=month)).replace('-', '')})
    return times


if __name__ == '__main__':
    crawler = Crawler()
    crawler.init_Crawler()
    times = generate_time([])

    while True:
        keyword = crawler.keywordsHeapify()
        for dic in times:
            start_time = dic["start_time"]
            end_time = dic['end_time']
            print(keyword, start_time, end_time, "-----------")
            print(crawler.search(keyword, start_time, end_time))



