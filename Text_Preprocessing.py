import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
import json
from konlpy.tag import Okt
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


def text_preprocessing(text):
    text = re.sub("^가-힣ㄱ-ㅎㅏ-ㅣ\\s", '', text)
    text = okt.morphs(text, stem=True)
    return text


df1 = pd.read_csv("4차년도.csv", encoding="cp949")
df2 = pd.read_csv("5차년도.csv", encoding="cp949")
df3 = pd.read_csv("5차년도_2차.csv", encoding="cp949")

x_data = []
y_data = []
df = pd.concat([df1, df2, df3])

label = {'anger': 0, 'angry': 0, 'sad': 1, 'sadness': 1, 'fear': 2, 'disgust': 3, 'neutral': 4, 'happiness': 5, 'surprise': 6}

df.apply(lambda x : x_data.append(x[1]), axis=1)
df.apply(lambda x : y_data.append(label[x[2].lower()]), axis=1)
y_data = to_categorical(y_data)

okt = Okt()
x_data = list(map(text_preprocessing, x_data))

tokenizer = Tokenizer()
tokenizer.fit_on_texts(x_data)
x_data = tokenizer.texts_to_sequences(x_data)

word_vocab = tokenizer.word_index
MAX_SEQUENCE_LENGTH = 20

x_data = pad_sequences(x_data, maxlen=MAX_SEQUENCE_LENGTH, padding='post')
y_data = np.array(y_data)

np.save("x_data", x_data)
np.save("y_data", y_data)

print(x_data[:10])
print(y_data[:10])
print(MAX_SEQUENCE_LENGTH)

import pickle

# saving
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

