import re

from konlpy.tag import Kkma
import mongodb
import Textpredict
from collections import defaultdict
from tqdm import tqdm
import pickle
import requests

MongoRepository = mongodb.MongoRepository()
Predictor = Textpredict.Predict()

tag = Kkma()
emotions = defaultdict(lambda: [0]*7)
url = "http://localhost:2/postEmotions"
items = list(MongoRepository.findAll())

# for idx, items in enumerate(items):
#     print(items)
# print(idx)
# with open('keywords.pickle', 'wb') as f:
#     pickle.dump(items, f, pickle.HIGHEST_PROTOCOL)

for item in tqdm(items):
    text = item['text']
    if len(text.split()) <= 2:
        continue
    emotion = Predictor.predict([text])
    text = re.sub(r'[^A-Za-z가-힣\s]', '', text)[:50]
    keywords = tag.nouns(text)

    for keyword in keywords:
        for idx, value in enumerate(emotion):
            emotions[keyword][idx] += value

print(emotions)

with open('emotions.pickle' + str(idx), 'wb') as f:
    pickle.dump(dict(emotions), f, pickle.HIGHEST_PROTOCOL)

# for key in emotions:
#     data = {'keyword': key, 'emotions': list(map(str, emotions[key]))}
#     requests.post(url, data=data)


# saving













