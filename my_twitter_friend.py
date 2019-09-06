import tweepy
import time
import json
from configBot import create_api

api = create_api()
self = api.me()


def get_data():
    with open("my_twitter_friend_data.json", "r") as read_file:
        received_data = json.load(read_file)
        return received_data


data = get_data()


def update_data(updated_data):
    with open("my_twitter_friend_data.json", "w") as write_file:
        json.dump(updated_data, write_file)


def search_tweets(string):
    last_id = get_last_id()  # int
    tweets = api.search(q=string, lang="en", since_id=last_id)
    return tweets


def follow_new_followers(api):
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            print("following " + follower.name)
            follower.follow()

def like_friends_tweets2():
    followers = api.followers()
    last_favorite = data["last_favorite"]
    for follower in followers:
        recent_tweets = api.user_timeline(follower.id, since_id=last_favorite)
        if recent_tweets:
            for recent_tweet in recent_tweets:
                print(str(recent_tweet.id) + " " + recent_tweet.text)
                if not recent_tweet.favorited:
                    recent_tweet.favorite()
                if recent_tweet.id > last_favorite:
                    last_favorite = recent_tweet.id
    data["last_favorite"] = last_favorite
    update_data(data)


def like_followers_tweets():
    # possibly should delete this function (like_friends_tweets2 is an improvement on this)
    # filters out tweets that have already been liked
    # likes the tweets that haven't been liked yet
    # updates last_favorite in data
    last_favorite = data["last_favorite"]
    latest_tweets = api.home_timeline(since_id=last_favorite)
    latest_tweets.reverse()
    print("searching for recent tweets")
    if latest_tweets:
        print("liking...")
        for tweet in latest_tweets:
            print(str(tweet.id) + " " + tweet.text)
            if tweet.user.id != self.id and tweet.id > data["last_favorite"]:
                time.sleep(15)
                print(str(tweet.id) + " " + tweet.text)
                tweet.favorite()
                last_favorite = tweet.id
    data["last_favorite"] = last_favorite
    update_data(data)


def get_mentions(last_mention_id):
    # needs further testing
    mentions = tweepy.Cursor(api.mentions_timeline, since_id=last_mention_id).items()
    for tweet in mentions:
        print(tweet.user + ": " + tweet.text)
        new_last_mention_id = tweet.id
        data["last_mention_id"] = new_last_mention_id


def check_mentions(api, keywords, last_mention_id):
    #needs further testing
    new_last_mention_id = last_mention_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=last_mention_id).items():
        new_since_id = max(tweet.id, last_mention_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(
                status="Please reach us via DM",
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id


# like_followers_tweets()
# time.sleep(5)
# follow_new_followers(api)


def run_process():
    while True:
        try:
            print("searching tweets")
            like_friends_tweets2()
            print("waiting")
            time.sleep(60)
            # print(api.rate_limit_status())
            # time.sleep(30)
            print("searching for new followers")
            follow_new_followers(api)
            time.sleep(60)
        except tweepy.TweepError:
            print("error")
            error_tweet = "I think something went wrong. I may not like any tweets "
            error_tweet.append(" for awhile until I can figure this out.")
            api.update_status(error_tweet)


run_process()
