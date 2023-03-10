from tensorflow.keras import models
import pickle
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.sequence import pad_sequences


class Predict():
    def __init__(self):
        with open('tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        self.okt = Okt()
        self.MAX_SEQUENCE_LENGTH = 20
        self.word_vocab = self.tokenizer.word_index
        self.model = models.load_model("./TextClassificationModel")

    def text_preprocessing(self, text):
        text = re.sub("^가-힣ㄱ-ㅎㅏ-ㅣ\\s", '', text)
        text = self.okt.morphs(text, stem=True)
        return text

    def predict(self, x_data):
        x_data = [self.text_preprocessing(text) for text in x_data]
        x_data = self.tokenizer.texts_to_sequences(x_data)
        x_data = pad_sequences(x_data, maxlen=self.MAX_SEQUENCE_LENGTH, padding='post')
        return self.model.predict(x_data)


if __name__ == "__main__":
    # label = {'anger': 0, 'angry': 0, 'sad': 1, 'sadness': 1, 'fear': 2, 'disgust': 3, 'neutral': 4, 'happiness': 5, 'surprise': 6}
    predictor = Predict()
    print(predictor.predict(["지진이 일어났나봐."]))