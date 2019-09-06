import tweepy
# logging library is suggested in the tutorial, but since I don't know how it works
# I'm leaving it out for now
# import logging
# logger = logging.getLogger()

CONSUMER_KEY = 'iZd98gq6DjbZK4s7WJ1Hs2fU1'
CONSUMER_SECRET = 'Jcq2fy34JKy6pb09vLnhb87iH6cfW5h9jYPIxCnWrDK2H0wGpW'
ACCESS_TOKEN = '1131738695055290370-NAAfgQUvch2WsCITqyz09uoNf0IPZm'
ACCESS_TOKEN_SECRET = 'nUPl3mmv4qsYJ8fIwmis4fY4zUPLPy1GhaPM0hkPFfX8L'

def create_api():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    return api


