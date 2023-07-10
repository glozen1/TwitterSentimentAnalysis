import snscrape.modules.twitter as sntwitter
import pandas as pd

tweets = []

for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query = "#opportunity").get_items()):
    if i>100:
        break
    tweets.append([tweet.user.username, tweet.date, tweet.likeCount, tweet.retweetCount, tweet.replyCount, tweet.lang,
                   tweet.sourceLabel, tweet.content])