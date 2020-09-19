import tweepy as tw
import datetime

class TwitterFetcher:

    def __init__(self):
        auth = tw.OAuthHandler('iv0nHdrJDysw4VCvJQft2RwIZ', '08dAPR7TGw9T180S23fZGcV0lrkqrLBxr6g0Zq7gKl5hgqVM9g')
        auth.set_access_token('1243802303209123841-8H3qXWOCLjrZVTPzV9JQjQ37QFBzVz', 'kNvLxeV7Pll7pSg2ol4oSAIgpVyiayouMTT1BXBVBRkhA')
        self.api = tw.API(auth, wait_on_rate_limit=True)

    def get_yesterday_twitter_data(self, tweet_no):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
    
        return self.get_twitter_data(yesterday, tweet_no)

    def get_twitter_data(self, date_param, tweet_no):
        query = 'coronavirus OR covid-19 OR lockdown OR masks OR pandemic OR epicemic OR wuhan OR virus OR restrictions -filter:retweets'
        tweets = tw.Cursor(self.api.search,
              q=query,
              geocode="54.463309,-2.073472,500km",
              lang="en",
              tweet_mode="extended",
              since=date_param).items(tweet_no)

        tweet_arr = []
        for tweet in tweets:
            if not tweet.retweeted:
                if tweet.full_text:
                    tweet_arr.append(tweet.full_text)
                else:
                    tweet_arr.append(tweet.text)
                
        return tweet_arr

if __name__ == "__main__":
    twitter_client = TwitterFetcher()
    print(twitter_client.get_yesterday_twitter_data(100))
