from bs4 import BeautifulSoup
import requests


class Content:
    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print("New article found for topic: {}".format(self.topic))
        print("URL: {}".format(self.url))
        print("TITLE: {}".format(self.title))
        print("BODY:\n{}".format(self.body))


class Website:
    def __init__(self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            return childObj[0].get_text()
        return ''

    def search(self, topic, site):
        bs = self.getPage(site.searchUrl + topic)
        searchResults = bs.select(site.resultListing)
        for result in searchResults:
            url = result.select(site.resultUrl)[0].attrs['href']
            if site.absoluteUrl:
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.post_url + url)
            if bs is None:
                print('Something aws wrong with that page or URL. Skipping!')
                return
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(topic, url, title, body)
                content.print()


crawler = Crawler()

siteData = [['0\'Reilly Media',
             'http://oreilly.com',
             'https://ssearch.oreilly.com/?q=',
             'article.product-result',
             'p.title a',
             True,
             'h1',
             'section#product-description'],
            ['Reuters', 'http://reuters.com',
             'http://www.reuters.com/search/news?blob=',
             'div.search-result-content',
             'h3.search-result-title a',
             False,
             'h1',
             'div.StandardArticleBody_body_1gnLA'],
            ['Brookings', 'http://www.brookings.edu',
             'https://www.brookings.edu/search/?s=',
             'div.list-content article',
             'h4.title a',
             True,
             'h1',
             'div.post-body']]
sites = []
for row in siteData:
    sites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

topics = ['python', 'data science']
for topic in topics:
    print('GETTING INFO ABOUT: ' + topic)
    for targetSite in sites:
        crawler.search(topic, targetSite)



