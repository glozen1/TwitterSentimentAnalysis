from tkinter import *

from tkinter import messagebox

import sentimentAnalysis as sa

window = Tk()

window.title("Twitter Sentiment Analysis")

window.geometry('530x250')

positive_tweets = []

negative_tweets = []

neutral_tweets = []

all_words = ""

hashtag_label = Label(window, text="Enter a Twitter Hashtag", fg="blue", font=("Arial", 16))

hashtag_label.grid(row=0, column=0, padx=10, pady=10)

hashtag = Entry(window, background="white", fg="black", font=("Arial", 16))

hashtag.grid(row=0, column=1, padx=10, pady=10)

num_label = Label(window, text="Number of Tweets", fg="blue", font=("Arial", 16))

num_label.grid(row=1, column=0, padx=10, pady=10)

tweet_num = Entry(window, background="white", fg="black", font=("Arial", 16))

tweet_num.grid(row=1, column=1, padx=10, pady=10)


def analyzing():
    try:

        global all_words, positive_tweets, neutral_tweets, negative_tweets

        hash_text = hashtag.get()

        num = int(tweet_num.get())

        tweets = sa.orig_tweets(hash_text, num)

        cleaned_tweets = sa.clean_tweets(tweets)

        all_words = ' '.join(cleaned_tweets)

        polarity = sa.senti(cleaned_tweets)

        positive_tweets, positive_polarity, negative_tweets, negative_polarity, neutral_tweets, neutral_polarity = sa.segregate_tweets(
            polarity, tweets)

        sa.bar_graph(len(positive_tweets), len(neutral_tweets), len(negative_tweets), hash_text)

        sa.pie_chart(len(positive_tweets), len(neutral_tweets), len(negative_tweets), hash_text)

    except:

        messagebox.showerror("Error", "Wrong Input")


analyze = Button(window, text="Analyze", fg="red", background="yellow", font=("Arial", 16), command=analyzing)

analyze.grid(row=3, column=1, padx=10, pady=10)


def show_tweets():
    win = Tk()

    win.title("Tweets")

    win.geometry('1000x650')

    main_frame = Frame(win)

    main_frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(main_frame)

    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)

    scbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scbar.set)

    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    second_frame = Frame(canvas)

    canvas.create_window((0, 0), window=second_frame, anchor="nw")

    l1 = "Positive Tweets(" + str(len(positive_tweets)) + ")"

    l2 = "Negative Tweets(" + str(len(negative_tweets)) + ")"

    l3 = "Neutral Tweets(" + str(len(neutral_tweets)) + ")"

    posi_list = "Tweet--> " + '\nTweet--> '.join(positive_tweets)

    neg_list = "Tweet--> " + '\nTweet--> '.join(negative_tweets)

    neu_list = "Tweet--> " + '\nTweet--> '.join(neutral_tweets)

    p_label = Label(second_frame, text=l1, fg="green", font=("Arial", 18), background="yellow")

    p_label.grid(row=0, column=0, padx=10, pady=10)

    p_tweets = Text(second_frame, fg="black", font=("Arial", 16), background="white")

    p_tweets.grid(row=1, column=0, padx=10, pady=10)

    p_tweets.insert("1.0", posi_list)

    n_label = Label(second_frame, text=l2, fg="red", font=("Arial", 18), background="black")

    n_label.grid(row=2, column=0, padx=10, pady=10)

    n_tweets = Text(second_frame, fg="black", font=("Arial", 16), background="white")

    n_tweets.grid(row=3, column=0, padx=10, pady=10)

    n_tweets.insert("1.0", neg_list)

    nu_label = Label(second_frame, text=l3, fg="blue", font=("Arial", 18), background="lightblue")

    nu_label.grid(row=4, column=0, padx=10, pady=10)

    nu_tweets = Text(second_frame, fg="black", font=("Arial", 16), background="white")

    nu_tweets.grid(row=5, column=0, padx=10, pady=10)

    nu_tweets.insert("1.0", neu_list)


see_tweets = Button(window, text="Show Tweets", fg="black", background="green", font=("Arial", 16), command=show_tweets)

see_tweets.grid(row=4, column=0, padx=10, pady=10)


def show_word_cloud():
    if len(all_words) > 0:

        sa.word_cloud(all_words)

    else:

        messagebox.showwarning("Warning", "Analyze a hashtag first")


wordCloud = Button(window, text="Word Cloud", fg="black", background="lightblue", font=("Arial", 16),
                   command=show_word_cloud)

wordCloud.grid(row=4, column=1, padx=10, pady=10)

window.mainloop()