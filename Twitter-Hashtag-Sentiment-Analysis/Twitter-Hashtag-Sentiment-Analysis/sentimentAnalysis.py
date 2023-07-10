import snscrape.modules.twitter as sntwitter

from googletrans import Translator

import string

import re

from wordcloud import WordCloud

import matplotlib.pyplot as plt

from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize

from nltk.sentiment.vader import SentimentIntensityAnalyzer


def stop_word_removal(sent):
    stop_words = set(stopwords.words("english"))

    word_tokens = word_tokenize(sent)

    swr = [word for word in word_tokens if word.lower() not in stop_words]

    clear = ' '.join(swr)

    return clear


# Extracting Tweets and translating them in English

def orig_tweets(hashtag, num):
    tweets = []

    translator = Translator()

    for tweet in sntwitter.TwitterSearchScraper(hashtag).get_items():

        if len(tweets) == num:

            break

        else:

            translated = translator.translate(tweet.rawContent, dest="en")

            tweets.append(translated.text)

    return tweets


# Cleaning the extracted tweets

def clean_tweets(tweets):
    cleared = []

    for i in range(len(tweets)):
        sent = tweets[i]

        lower_case = sent.lower()

        lower_case = stop_word_removal(lower_case)

        cleaning = lower_case.translate(str.maketrans('', '', string.punctuation))

        cleaning = re.sub(r'@[A-Za-z0-9]+', '', cleaning)

        cleaning = re.sub(r'#', '', cleaning)

        cleaning = re.sub(r'RT[\s]+', '', cleaning)

        cleaning = re.sub(r'https?:\/\/\S+', '', cleaning)

        cleared.append(cleaning)

    return cleared


# Performing sentiment analysis on the cleaned Tweets

def senti(ctweets):
    sent_analyzer = SentimentIntensityAnalyzer()

    sentimentsList = []

    for text in ctweets:
        analysis = sent_analyzer.polarity_scores(text)

        sentiment = analysis["compound"]

        sentimentsList.append(sentiment)

    return sentimentsList


# Segregating tweets into Positive, Negative and Neutral

def segregate_tweets(sen, tweets):
    positive = []

    posiPol = []

    negative = []

    negPol = []

    neutral = []

    neutPol = []

    for i in range(len(sen)):

        if sen[i] >= 0.5:

            posiPol.append(sen[i])

            positive.append(tweets[i])

        elif sen[i] <= -0.5:

            negPol.append(sen[i])

            negative.append(tweets[i])

        else:

            neutPol.append(sen[i])

            neutral.append(tweets[i])

    return positive, posiPol, negative, negPol, neutral, neutPol


# For plotting a bar graph

def bar_graph(p, ne, n, h):
    values = [p, ne, n]

    attributes = ["Positive", "Neutral", "Negative"]

    plt.figure(figsize=(10, 5))

    plt.bar(attributes, values, color='maroon', width=0.4)

    plt.title("Bar Graph of #" + h)

    plt.xlabel("Emotions")

    plt.ylabel("Number of Tweets")

    plt.show()


# For plotting a pie chart

def pie_chart(p, ne, n, h):
    values = [p, ne, n]

    attributes = ["Positive", "Neutral", "Negative"]

    plt.title("Pie distribution of #" + h)

    plt.pie(values, labels=attributes, autopct='%2.1f%%')

    plt.show()


# For creating a word cloud

def word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110).generate(text)

    plt.figure(figsize=(10, 5))

    plt.imshow(wordcloud, interpolation="bilinear")

    plt.axis('off')

    plt.show()