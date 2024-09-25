import tweepy
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

# set up Twitter API credentials
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

# authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def search_tweets(job_keywords, context_terms, days, exclude_words, max_tweets):
    """
    Search for tweets containing the most relevant combination of the given `job_keywords` and `context_terms` within the last `days` days.
    Exclude tweets containing any of the `exclude_words`.
    Return the `max_tweets` most relevant tweets.
    """
    
    tweets = []
    start_date = datetime.now() - timedelta(days=days)

    for tweet in tweepy.Cursor(api.search_tweets, q=' OR '.join(job_keywords), lang='en', since=start_date.strftime('%Y-%m-%d'), search_full_text=True).items():
        if exclude_words and any(word in tweet.text.lower() for word in exclude_words):
            continue

        relevance_score = sum(1 for keyword in job_keywords if keyword.lower() in tweet.text.lower())
        if any(term.lower() in tweet.text.lower() for term in context_terms):
            relevance_score += 1

        tweets.append({
            'user': tweet.user.screen_name,
            'text': tweet.text,
            'created_at': tweet.created_at,
            'url': f'https://twitter.com/user/status{tweet.id}',
            'relevance_score': relevance_score
        })

    sorted_tweets = sorted(tweets, key=lambda x: x['relevance_score'], reverse=True)
    return pd.DataFrame(sorted_tweets[:max_tweets])

def filter_tweets(df, sort_by='created_at'):
    """Filter the tweet DataFrame based on the specified and sort the results."""
    return df.sort_values(by=sort_by, ascending=True)

# example usage
if __name__ == "__main__":
    job_keywords = ['python developer', 'software engineer', 'software developer','backend engineer', 'frontend engineer','full stack engineer', 'ux engineer', 'product manager', 'ux researcher', 'frontend dev', 'backend dev']
    context_terms = ['hiring', 'we are hiring', 'is hiring', 'open positions', 'hiring alert', 'hiring now', 'hiring urgently']
    days = 3
    exclude_words = ['cracked', 'nsfw']
    max_tweets = 25
    tweets = search_tweets(job_keywords, context_terms, days, exclude_words, max_tweets)
    filtered_tweets = filter_tweets(tweets)
    print(filtered_tweets)
