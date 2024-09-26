import requests
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

# hardcoded context terms to locate hiring tweets
# algorithm is meant to automatically search for tweets with these terms
context_terms = ['hiring', 'we are hiring', 'is hiring', 'open positions', 'hiring alert', 'hiring now', 'hiring urgently', 'we\'re hiring', 'looking for', 'seeking', 'looking for talented', 'seeking talented']

def search_tweets(job_keywords, days, exclude_words, max_tweets):
    """
    Search for tweets containing the most relevant combination of the given `job_keywords` within the last `days` days using the mock API.
    Exclude tweets containing any of the `exclude_words`.
    Return the `max_tweets` most relevant tweets.
    """

    # make a GET request to the mock API
    response = requests.get('http://localhost:5000/api/search_tweets')

    # check if the request was successful
    if response.status_code != 200:
        print(f"Error: API request failed with status code {response.status_code}")
        return pd.DataFrame()
    
    # convert JSON response to a DataFrame for easier processing
    tweets = pd.DataFrame(response.json())
    # convert created_at to a datetime object
    tweets['created_at'] = pd.to_datetime(tweets['created_at'])

    # FILTERING
    # filter out tweets that don't contain at least one context term
    tweets = tweets[tweets['text'].str.lower().str.contains('|'.join(context_terms), na=False)]
    #print how many tweets remain after this filter

    # filter out tweets that don't contain any of the job keywords
    if job_keywords:
        tweets = tweets[tweets['text'].str.lower().str.contains('|'.join(job_keywords))]

    # filter by timeframe
    date_cutoff = datetime.now() - timedelta(days=days)
    tweets = tweets[tweets['created_at'] >= date_cutoff]

    # filter out tweets with exclude words
    if exclude_words:
        tweets = tweets[~tweets['text'].str.lower().str.contains('|'.join(exclude_words), na=False)]
    
    # CALCULATE RELEVANCE SCORE based on job keywords
    tweets['relevance_score'] = tweets['text'].apply(lambda x: sum(keyword.lower() in x.lower() for keyword in job_keywords))

    # reset index for clean output
    #tweets = tweets.reset_index(drop=True)

    return tweets

def present_tweets(df, sort_by='relevance_score'):
    """Filter the tweet DataFrame based on the specified and sort the results."""
    return df.sort_values(by=sort_by, ascending=False)

# example usage
if __name__ == "__main__":
    job_keywords = ['python developer', 'software engineer', 'software developer','backend engineer', 'frontend engineer','full stack engineer', 'ux engineer', 'product manager', 'ux researcher', 'frontend dev', 'backend dev']
    #search is customized by job keywords
    days = 7
    exclude_words = ['cracked', 'nsfw']
    max_tweets = 25
    tweets = search_tweets(job_keywords, days, exclude_words, max_tweets)
    filtered_tweets = present_tweets(tweets)
    print(filtered_tweets)
