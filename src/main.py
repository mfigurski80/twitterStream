import tweepy
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Auth and get api
auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_KEY_SECRET"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Set up stream
class Listener(tweepy.StreamListener):
    def __init__(self, output_file=sys.stdout):
        super(Listener, self).__init__()
        self.output_file = output_file

    def on_connect(self):
        print('Connected')

    def on_status(self, status):
        if hasattr(status, 'extended_tweet'):
            full_text = status.extended_tweet['full_text']
        else:
            full_text = status.text
        print(full_text, file=self.output_file)

    def on_error(self, status_code):
        print(status_code)
        return False


output = open("stream_output.txt", "w")
listener = Listener(output_file=output)
stream = tweepy.Stream(auth=api.auth, listener=listener, tweet_mode='extended')

try:
    print("Start streaming.")
    stream.filter(languages=["en"], track=['coronavirus'])
    # stream.sample(languages=["en"])
except KeyboardInterrupt as e:
    print("Stopped.")
finally:
    print("Done.")
    stream.disconnect()
    output.close()

# for tweet in tweepy.Cursor(api.search, q='coronavirus').items(10):
#     print(tweet.text)
