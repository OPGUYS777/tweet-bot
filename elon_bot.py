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

# ✅ TEST MESSAGE (to confirm bot works)
send("✅ Bot started successfully")

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

while True:
    print("Checking tweets...")

    feed = None

    # 🔁 Try multiple sources
    for url in URLS:
        temp_feed = feedparser.parse(url)
        if temp_feed.entries:
            feed = temp_feed
            print(f"Using: {url}")
            break

    # ❌ If all fail → retry
    if feed is None or not feed.entries:
        print("❌ All sources failed")
        time.sleep(60)
        continue

    print("Entries:", len(feed.entries))

    latest = feed.entries[0]
    tweet_time = datetime(*latest.published_parsed[:6])

    # 🧠 FIRST RUN
    if last_tweet_time is None:
        last_tweet_time = tweet_time

    # 🚀 NEW TWEET DETECTED
    elif tweet_time > last_tweet_time:
        today_count = count_today()

        send(f"🚀 Elon Musk tweeted!\n📊 Tweets today: {today_count}")

        with open("tweets.txt", "a") as f:
            f.write(str(tweet_time) + "\n")

        last_tweet_time = tweet_time

    time.sleep(120)