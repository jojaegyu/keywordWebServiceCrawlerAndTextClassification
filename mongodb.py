from pymongo import MongoClient, TEXT


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


class MongoRepository:
    def __init__(self):
        self.client = MongoClient()
        self.client = MongoClient(host='localhost', port=27017)
        self.db = self.client['text_data']
        self.Text = self.db['Text']
        self.Keyword = self.db['Keyword']

    def database_init(self):
        self.Text.create_index([('url', TEXT)], default_language='english')
        self.Keyword.create_index([('keyword', TEXT)])

    def insertText(self, text):
        return self.Text.insert_one(text.text2dictionary())

    def insertTextMany(self, texts):
        return self.Text.insert_many(texts)

    def findUrl(self, url):
        return self.Text.find({'url': url})

    def keywordUpdate(self, keyword, num):
        return self.Keyword.update_one({"keyword": keyword}, {"$inc": {"sum": num}}, upsert=True)

    def findAll(self):
        obj = self.Text.find({})
        return obj

    def __del__(self):
        self.client.close()


if __name__ == "__main__":
    mongorepository = MongoRepository()
    # mongorepository.insertText(Text("인프피는 잘못된 사람이다.", 'post', 'date', 'instiz', 'https://www.instiz.net/name'))
    # print(bool(list(mongorepository.findUrl("https://www.instiz.net/name"))))
    # mongorepository.insertTextMany([Text("인프피는 잘못된 사람이다.", 'post', 'date', 'instiz', 'https://www.instiz.net/name'), Text("인프피는 잘못된 사람이다.", 'post', 'date', 'instiz', 'https://www.instiz.net/nameaiwoeurh')])
    for idx, item in enumerate(mongorepository.findAll()):
        print(item)

    mongorepository.__del__()