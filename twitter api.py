import tweepy
from pprint import pprint
from tqdm import tqdm

api_key = "LqQ7AFiQgfzhqoQ9nzQmPswiD"
api_key_secret = "5yfv7uhMz1tCwTwKaYDqbvMyN6f94378tbJqclNyI9YVf4N6YH"
access_token = "1544650888786022401-HoylNNyHE6cQRe7IwcGBJLjlSRDBH0"
access_token_secret = "9YMHCRC1nw9jX31Sk4PeB8wg9P9og7eWoveSREwxABSlf"

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Success")
except:
    print("Failed")

for i in tqdm(range(1)):
    tmp = api.search_tweets(q='빼빼로', lang='ko', count=100)
    print(type(tmp), tmp)