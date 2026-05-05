import os
import feedparser
import requests
from datetime import datetime
import time

# ====== YOUR TELEGRAM DETAILS ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URLS = [
    "https://nitter.net/elonmusk/rss",
    "https://nitter.poast.org/elonmusk/rss",
    "https://nitter.cz/elonmusk/rss",
    "https://nitter.privacydev.net/elonmusk/rss",
    "https://nitter.rawbit.ch/elonmusk/rss"
]

last_tweet_time = None

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def count_today():
    try:
        with open("tweets.txt", "r") as f:
            lines = f.readlines()

        today = datetime.now().date()
        count = 0

        for line in lines:
            t = datetime.fromisoformat(line.strip())
            if t.date() == today:
                count += 1

        return count
    except:
        return 0

last_tweet_time = None

while True:
    print("Checking tweets...")

    try:
        feed = None

        for url in URLS:
            temp_feed = feedparser.parse(url)
            if temp_feed.entries:
                feed = temp_feed
                break

        if not feed or not feed.entries:
            print("❌ All sources failed")
            time.sleep(180)
            continue

        latest = feed.entries[0]
        tweet_time = datetime(*latest.published_parsed[:6])

        if last_tweet_time is None:
            last_tweet_time = tweet_time

        elif tweet_time > last_tweet_time:
            send("🚀 Elon Musk tweeted!")
            last_tweet_time = tweet_time

    except Exception as e:
        print("Error:", e)
        time.sleep(120)