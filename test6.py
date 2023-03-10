import pickle
import requests

url = "http://localhost:2/postEmotions"
with open('emotions.pickle', 'rb') as f:
    data = pickle.load(f)

print(data)
for key, emotion in data.items():
    emotion = emotion[0]
    mx = max(emotion)
    emotion = [int(100 * (e / mx)) for e in emotion]
    print(emotion)
    data = {"keyword": key, "angry": emotion[0], "sad": emotion[1], "fear": emotion[2]
               , "disgust": emotion[3], "neutral": emotion[4], "happiness": emotion[5], "surprise": emotion[6]}
    requests.post(url, data=data)
