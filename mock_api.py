import random
from flask import Flask, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)

users = ["user0", "user1", "user2", "user3", "user4", "user5", "user6", "user007", "user8", "user9"]

companies = ["TechCorp", "Shade Inc.", "Neuralink", "Octo", "Scale"]

roles = ["Software Engineer", "frontend dev", "frontend developer", "full-stack engineer","data scientist", "Product Manager", "UX designer", "ux researcher", "researcher", "designer"]

tweet_templates = [
    "We're hiring {role}s to join our team at {company}! 🚀",
    "{company} is looking for a {role} to join our team! 🌟",
    "We're hiring! Check out our open {role} positions at {company} 💼",
    "Join us at {company} and help shape the future! We're hiring {role}s",
    "We're hiring! Check out our open {role} positions at {company} 🌟",
    "Exciting opportunity for {role}s at {company}! Apply to join our team now.",
    "Looking for talented {role}s to join our team! Apply now.",
    "This is not a job posting.",
    "{company} is hiring {role}s! Apply now!",
    "Currently hiring for {role}s, {role2}s, and {role3}s at {company}. DM me if interested!",
    "looking for cracked {role}s, {role2}s, and {role3}s to join our team at {company}.",
    "looking for {role}s, {role2}s, and {role3}s to join our team at {company}."
    "Looking for something else."
]

def generate_mock_tweets(num_tweets):
    '''generate a specified number of mock tweets'''

    tweets = []

    for _ in range(num_tweets):
        user = random.choice(users)
        company = random.choice(companies)
        role = random.choice(roles)
        role2 = random.choice(roles)
        role3 = random.choice(roles)
        text = random.choice(tweet_templates).format(role=role, role2=role2, role3=role3, company=company)

        tweet = {
            'user': user,
            'text': text,
            'created_at': datetime.now() - timedelta(days=random.randint(0, 14)),
            'url': f'https://twitter.com/{user}/status/{random.randint(100000000000000000, 999999999999999999)}'
        }

        tweets.append(tweet)

    return tweets

mock_tweets = generate_mock_tweets(100)

@app.route('/api/search_tweets', methods=['GET'])

def search_tweets():
    # in a real API, this would search the tweets but for our mock API purposes, we'll just return the mock tweets

    # pagination parameters
    # page = int(request.args.get('page', 1))
    # per_page = int(request.args.get('count', 10)) #Twitter uses count instead of per_page

    # start_index = (page - 1) * per_page
    # end_index = start_index + per_page

    # return jsonify(mock_tweets[start_index:end_index])

    return jsonify(mock_tweets)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
