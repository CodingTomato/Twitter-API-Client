#-------------#
#    Setup    #
#-------------#

from collections import Counter
import os
from app import app
from flask import render_template, request
from pytwitter import Api
from afinn import Afinn

# Initialize the Twitter API 2 wrapper with a bearer token from a twitter project
apiV2 = Api(bearer_token= os.environ['BEARER_TOKEN'])



#-------------#
#  Functions  #
#-------------#

# Get the overall sentiment of a text as a string
def getSentiment(text):
    afinn = Afinn(emoticons=True)
    score = afinn.score(text)

    sentiment = "Neutral"
    if score > 0: sentiment = "Positive"
    elif score < 0: sentiment = "Negative"

    return sentiment

# Get the exact sentiment score of a text
def getSentimentScore(text):
    afinn = Afinn(emoticons=True)
    return afinn.score(text)

# Provided a list of strings the function finds each hashtag, 
# counts the occurences and returns a dictionary with these values
def analyzeTextHashtags(text_list):
    cnt = Counter()

    for text in text_list:
        # Split each tweet on spaces
        for word in text.split():
            # If word starts with # symbol add it to the counter
            if word[0] == "#":
                tag = word[1:].lower()
                cnt[tag] += 1

    return cnt

# Provided a list of tweets and author ids the function counts how
# many tweets each user wrote in the dataset
def analyzeTopUsersFromTweets(tweet_list):
    cnt = Counter()

    # Count the occurrence of each user_id
    for tweet in tweet_list:
        cnt[tweet.author_id] += 1

    return cnt


#-------------#
#   Routes    #
#-------------#

# The index route shows short instructions for the features 
@app.route("/")
def index():
    # Render the html page
    return render_template("public/home.html")

# The tweets route shows all the tweets of a given username
@app.route("/user/<user>/tweets")
def tweets(user):
    # Get the user object with public metrics
    user = apiV2.get_user(username=user, user_fields="public_metrics")
    
    tweets = []
    next_token = 1
    counter = 0

    # Make multiple requests for multiple pages of tweets
    while next_token != 0 and counter < 2:

        # First page without pagination_token
        if next_token == 1:
            raw_tweets = apiV2.get_timelines(user_id=user.data.id, max_results=100)
        # Next pages with last pagination_token
        else:
            raw_tweets = apiV2.get_timelines(user_id=user.data.id, max_results=100, pagination_token=next_token)

        for tweet in raw_tweets.data:
            tweets.append(tweet)

        # Set the next pagination token
        if raw_tweets.meta.next_token:
            next_token = raw_tweets.meta.next_token
        else:
            next_token = 0
        
        counter += 1

    # Render the html page with the required variables
    return render_template("public/tweets.html", getSentiment = getSentiment, getSentimentScore = getSentimentScore, tweets = tweets, user = user.data, number_of_tweets = len(tweets))

# The followers route shows all the followers of a given username
@app.route("/user/<user>/followers")
def followers(user):
    # Get the user object with public metrics
    user = apiV2.get_user(username=user, user_fields="public_metrics")

    followers = []
    next_token = 1
    counter = 0

    # Make multiple requests for multiple pages of followers
    while next_token != 0 and counter < 2:

        # First page without pagination_token
        if next_token == 1:
            raw_followers = apiV2.get_followers(user_id=user.data.id, max_results=100)
        # Next pages with last pagination_token
        else:
            raw_followers = apiV2.get_followers(user_id=user.data.id, max_results=100, pagination_token=next_token)

        for follower in raw_followers.data:
            followers.append(follower)

        # Set the next pagination token
        if raw_followers.meta.next_token:
            next_token = raw_followers.meta.next_token
        else:
            next_token = 0
        
        counter += 1

    # Render the html page with the required variables
    return render_template("public/followers.html", followers = followers, user = user.data, number_of_followers = len(followers))

# The sentiment route allows the user to analyze the sentiement of any english text
@app.route("/sentiment", methods=["GET", "POST"])
def sentiment():
    # If user sends the request with text
    if request.method == "POST":
        # Get the text from the form values
        text = request.form.get("input")
        sentiment_per_word = []
        for word in text.split():
            wordArray = []
            # Add the word, the sentiment string and
            # sentiment score for each word in the text
            wordArray.append(word)
            wordArray.append(getSentiment(word))
            wordArray.append(getSentimentScore(word))
            sentiment_per_word.append(wordArray)

        # Render the html page with the required variables
        return render_template("public/sentiment.html", getSentiment = getSentiment, getSentimentScore = getSentimentScore, sentiment_per_word = sentiment_per_word, text=text)

    # If the user doesn't send any text to analyze just render the empty html page
    return render_template("public/sentiment.html", getSentiment = getSentiment, getSentimentScore = getSentimentScore, sentiment_per_word = [], text="")

# The dataset route allows the user to analyze a user specified dataset of up to 1000 tweets
@app.route("/dataset", methods=["GET", "POST"])
def dataset():
    # If user sends the request with a search query
    if request.method == "POST":
        query = request.form.get("input")
        data = []
        tweets_text = []
        tweets_users = {}
        next_token = 1
        counter = 0

        # Make multiple requests for multiple pages of followers
        while next_token != 0:
            # First request without a pagination token
            if(next_token == 1):
                response = apiV2.search_tweets(query, expansions="author_id", max_results=100)
            # Next pages with last pagination_token
            else:
                response = apiV2.search_tweets(query, expansions="author_id", max_results=100, next_token= next_token)

            for user in response.includes.users:
                tweets_users.update({user.id: user})

            # Set the next pagination token
            if (response.meta.next_token and counter < 9):
                next_token = response.meta.next_token
            else:
                next_token = 0

            counter = counter + 1
            for tweet in response.data:
                tweets_text.append(tweet.text)
                data.append(tweet)

        # Count all tweets from each user in the dataset
        users_analysis = analyzeTopUsersFromTweets(data)
        # Count all hashtags from the dataset
        hashtag_analysis = analyzeTextHashtags(tweets_text)

        # Render the html page with the required variables
        return render_template("public/dataset_analysis.html", data = data, number_of_tweets = len(data), query=query, top10Hashtags = hashtag_analysis.most_common(10), top10UsersFromTweets = users_analysis.most_common(10),  tweets_users = tweets_users, number_of_users = len(tweets_users.values()))

    data = []

    # If the user doesn't send any text to analyze just render the html page without values
    return render_template("public/dataset_analysis.html", data = data, query="", number_of_tweets = 0, top10Hashtags = 0, top10UsersFromTweets = 0, tweets_users = 0, number_of_users = 0)