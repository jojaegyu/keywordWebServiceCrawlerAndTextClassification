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