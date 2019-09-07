import tweepy
import time
import json
import random
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
    for follower in api.followers():
        if not follower.following:
            try:
                follower.follow()
                print("following " + follower.name)
            except tweepy.TweepError:
                print("Cannot follow " + follower.name + ". (The follow request my be pending.)")
                continue

def like_friends_tweets2():
    followers = api.followers()
    last_favorite = data["last_favorite"]
    for follower in followers:
        try:
            recent_tweets = api.user_timeline(follower.id, since_id=last_favorite)
            if recent_tweets:
                for recent_tweet in recent_tweets:
                    print(str(recent_tweet.id) + " " + recent_tweet.text)
                    if not recent_tweet.favorited:
                        recent_tweet.favorite()
                    if recent_tweet.id > last_favorite:
                        last_favorite = recent_tweet.id
        except tweepy.TweepError:
            continue
    data["last_favorite"] = last_favorite
    update_data(data)


def reply_to_mentions():
    # needs further testing
    last_reply = data["last_reply"]
    mentions = api.mentions_timeline(since_id = last_reply)
    mentions.reverse()
    for mention in mentions:
        print(str(mention.id) + ": " + mention.text)
        screen_name = "@" + mention.user.screen_name
        reply_text = screen_name + " " + choose_random_reply()
        print(mention.user.name)
        print(mention.text)
        print("reply: " + reply_text)
        try:
            api.update_status(status = reply_text, in_reply_to_status_id = mention.id, )
            if not data["last_reply"] > mention.id:
                data["last_reply"] = mention.id
            update_data(data)
            time.sleep(15)
        except tweepy.TweepError:
            print("Reply failed. Not sure why. Hope that helps")
            continue

def choose_random_reply():
    reply = ""
    replies = data["replies"]
    num_choices = len(replies)
    index = random.randint(0, num_choices-1)
    reply = replies[index]
    return reply


def run_process():
    while True:
        try:
            print("searching for mentions")
            reply_to_mentions()
            print("waiting")
            time.sleep(60)
            print("searching tweets from followers")
            like_friends_tweets2()
            print("waiting")
            time.sleep(60)
            print("searching for new followers")
            follow_new_followers(api)
            time.sleep(60)
            print("waiting")
        except tweepy.TweepError:
            print("error")
            error_tweet = "I think something went wrong. I may not like any tweets "
            error_tweet += " for awhile until I can figure this out."
            api.update_status(error_tweet)


# follow_new_followers(api)
# like_friends_tweets2()
# reply_to_mentions()
run_process()



